import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib
import os
import json

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # 1. Cleaning
    initial_len = len(df)
    df = df[df['Age'] >= 0]
    print(f"Removed {initial_len - len(df)} records with negative age.")
    
    # Format dates
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay']).dt.normalize()
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay']).dt.normalize()
    
    # Target variable to numeric
    df['No_show_num'] = (df['No-show'] == 'Yes').astype(int)
    
    return df

def feature_engineering(df):
    print("Engineering features...")
    df = df.copy()
    
    # Lead time
    df['lead_time_days'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
    # Clean up negative lead times (invalid data where appointment is before scheduling day)
    df = df[df['lead_time_days'] >= 0]
    
    # Lead time bucket
    df['lead_time_bucket'] = pd.cut(
        df['lead_time_days'], 
        bins=[-1, 1, 7, 14, 10000], 
        labels=['0-1', '2-7', '8-14', '15+']
    )
    
    # Age bracket
    df['age_bracket'] = pd.cut(
        df['Age'], 
        bins=[-1, 18, 30, 50, 65, 200], 
        labels=['0-18', '19-30', '31-50', '51-65', '65+']
    )
    
    # Day of week and Month
    df['day_of_week'] = df['AppointmentDay'].dt.day_name()
    df['month'] = df['AppointmentDay'].dt.month.astype(str)
    
    # Historical no-show rate for repeat patients
    df = df.sort_values(by=['PatientId', 'AppointmentDay'])
    df['historical_no_show_rate'] = df.groupby('PatientId')['No_show_num'].transform(
        lambda x: x.shift().expanding().mean()
    )
    # Leave as NaN for first-time visits; we'll impute this later in the pipeline
    
    return df

def exploratory_data_analysis(df):
    print("\n--- Exploratory Data Analysis ---")
    overall_rate = df['No_show_num'].mean()
    print(f"Overall No-Show Rate: {overall_rate:.2%}")
    
    # Claim 1: >7 days lead time
    rate_under_7 = df[df['lead_time_days'] <= 7]['No_show_num'].mean()
    rate_over_7 = df[df['lead_time_days'] > 7]['No_show_num'].mean()
    print(f"\nClaim Check: Lead Time > 7 days")
    print(f"  No-Show Rate (<= 7 days): {rate_under_7:.2%}")
    print(f"  No-Show Rate (> 7 days): {rate_over_7:.2%}")
    
    if rate_over_7 > rate_under_7 * 1.5:
        print("  -> Claim SUPPORTED: Sharp rise in no-shows for >7 days lead time.")
    else:
        print("  -> Claim WEAK: Data does not show a sharp rise.")
        
    # Claim 2: Age
    print("\nClaim Check: Age Brackets")
    age_rates = df.groupby('age_bracket', observed=False)['No_show_num'].mean()
    print(age_rates.apply(lambda x: f"{x:.2%}"))
    if age_rates.loc['0-18'] > age_rates.loc['65+']:
        print("  -> Claim SUPPORTED: Younger patients have higher no-show rates.")
    else:
        print("  -> Claim WEAK: Data does not strictly support younger == higher rate.")
    print("---------------------------------\n")

def build_and_train_model(df):
    print("Building and training model pipeline...")
    
    # Define features
    num_features = ['Age', 'lead_time_days', 'historical_no_show_rate', 'Scholarship', 'Hipertension', 'Diabetes', 'SMS_received']
    cat_features = ['Gender', 'age_bracket', 'lead_time_bucket', 'day_of_week']
    
    X = df[num_features + cat_features]
    y = df['No_show_num']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # Preprocessing
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_features),
            ('cat', cat_transformer, cat_features)
        ])
    
    # Logistic Regression fits "explainable" requirement
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(penalty='l2', class_weight='balanced', max_iter=500, random_state=42))
    ])
    
    model.fit(X_train, y_train)
    
    # Evaluation
    print("Evaluating Model on Test Set...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(f"Precision: {precision_score(y_test, y_pred):.3f}")
    print(f"Recall: {recall_score(y_test, y_pred):.3f}")
    print(f"F1-Score: {f1_score(y_test, y_pred):.3f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.3f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nNote: Priority is on Recall and ROC-AUC due to class imbalance.")
    
    # Determine risk thresholds
    print("\nCalculating Risk Thresholds based on Test Probabilities...")
    p33 = np.percentile(y_prob, 33)
    p66 = np.percentile(y_prob, 66)
    
    # Adjust thresholds to be closer to 0.35/0.65 as suggested if they make sense, 
    # but use data percentiles for balanced tier distribution
    threshold_low_med = p33 if abs(p33 - 0.35) > 0.1 else 0.35
    threshold_med_high = p66 if abs(p66 - 0.65) > 0.1 else 0.65
    
    thresholds = {
        'LOW_MEDIUM': float(threshold_low_med),
        'MEDIUM_HIGH': float(threshold_med_high)
    }
    print(f"Selected Thresholds: LOW < {threshold_low_med:.2f} <= MED < {threshold_med_high:.2f} <= HIGH")
    
    return model, thresholds

if __name__ == "__main__":
    data_path = 'data/KaggleV2-May-2016.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please ensure the dataset is downloaded.")
        exit(1)
        
    df = load_and_clean_data(data_path)
    df = feature_engineering(df)
    exploratory_data_analysis(df)
    
    model, thresholds = build_and_train_model(df)
    
    # Save the model and thresholds
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/clinicflo_model.pkl')
    with open('model/thresholds.json', 'w') as f:
        json.dump(thresholds, f)
        
    print("\nTraining complete! Model saved to model/clinicflo_model.pkl")
    print("Thresholds saved to model/thresholds.json")
