import os
import json
import pandas as pd
import numpy as np
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/clinicflo_model.pkl')
THRESHOLDS_PATH = os.path.join(os.path.dirname(__file__), '../model/thresholds.json')

# Load model and thresholds lazily to avoid loading on import
_model = None
_thresholds = None
_feature_names = None

def _load_resources():
    global _model, _thresholds, _feature_names
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        with open(THRESHOLDS_PATH, 'r') as f:
            _thresholds = json.load(f)
        
        # Get feature names from preprocessor
        # sklearn's ColumnTransformer names them like "num__Age", "cat__Gender_F"
        _feature_names = _model.named_steps['preprocessor'].get_feature_names_out()

# User-friendly explanation mapping for features
EXPLANATION_MAP = {
    'num__Age': 'Age factor',
    'num__lead_time_days': 'Booking lead time',
    'num__historical_no_show_rate': 'Historical no-show rate',
    'num__Scholarship': 'Enrolled in welfare program',
    'num__Hipertension': 'Hypertension diagnosis',
    'num__Diabetes': 'Diabetes diagnosis',
    'num__SMS_received': 'SMS reminder received',
    
    # Categorical features
    'cat__Gender_F': 'Female patient',
    'cat__Gender_M': 'Male patient',
    
    'cat__age_bracket_0-18': 'Younger age group (0-18)',
    'cat__age_bracket_19-30': 'Young adult age group (19-30)',
    'cat__age_bracket_31-50': 'Adult age group (31-50)',
    'cat__age_bracket_51-65': 'Older adult age group (51-65)',
    'cat__age_bracket_65+': 'Senior age group (65+)',
    
    'cat__lead_time_bucket_0-1': 'Very short booking lead time (0-1 days)',
    'cat__lead_time_bucket_2-7': 'Short booking lead time (2-7 days)',
    'cat__lead_time_bucket_8-14': 'Medium booking lead time (8-14 days)',
    'cat__lead_time_bucket_15+': 'Long booking lead time (15+ days)'
}

def predict(patient_data: dict) -> dict:
    """
    Predict probability of a patient no-show.
    
    Expected input format:
    {
      "age": 23,
      "gender": "F",
      "scholarship": false,
      "hypertension": false,
      "diabetes": false,
      "sms_received": true,
      "lead_time": 12
    }
    """
    _load_resources()
    
    # 1. Feature translation and imputation
    lead_time = patient_data.get('lead_time', 0)
    age = patient_data.get('age', 0)
    
    # Compute buckets
    if lead_time <= 1: lead_time_bucket = '0-1'
    elif lead_time <= 7: lead_time_bucket = '2-7'
    elif lead_time <= 14: lead_time_bucket = '8-14'
    else: lead_time_bucket = '15+'
        
    if age <= 18: age_bucket = '0-18'
    elif age <= 30: age_bucket = '19-30'
    elif age <= 50: age_bucket = '31-50'
    elif age <= 65: age_bucket = '51-65'
    else: age_bucket = '65+'
        
    # We estimate appointment day of week by assuming it's lead_time days from now
    appointment_date = pd.Timestamp.now() + pd.Timedelta(days=lead_time)
    day_of_week = appointment_date.day_name()
    
    # Create DataFrame matching training columns
    input_df = pd.DataFrame([{
        'Age': age,
        'Gender': patient_data.get('gender', 'F'),
        'Scholarship': int(patient_data.get('scholarship', False)),
        'Hipertension': int(patient_data.get('hypertension', False)), # Note spelling matches kaggle data
        'Diabetes': int(patient_data.get('diabetes', False)),
        'SMS_received': int(patient_data.get('sms_received', False)),
        
        # Engineered features
        'lead_time_days': lead_time,
        'lead_time_bucket': lead_time_bucket,
        'age_bracket': age_bucket,
        'day_of_week': day_of_week,
        
        # Unknown for API, set to NaN to let pipeline median-impute it
        'historical_no_show_rate': np.nan 
    }])
    
    # 2. Prediction
    probability = float(_model.predict_proba(input_df)[0, 1])
    
    # 3. Risk Tiering
    if probability < _thresholds['LOW_MEDIUM']:
        risk_level = "LOW"
        recommended_action = "Send normal reminder"
    elif probability < _thresholds['MEDIUM_HIGH']:
        risk_level = "MEDIUM"
        recommended_action = "Send reminder and monitor"
    else:
        risk_level = "HIGH"
        recommended_action = "Alert reception / contact patient"
        
    # 4. Explainability (Feature Contributions)
    # Get transformed features
    X_transformed = _model.named_steps['preprocessor'].transform(input_df)[0]
    
    # Get coefficients
    coef = _model.named_steps['classifier'].coef_[0]
    
    # Calculate contribution of each feature: coefficient * feature_value
    contributions = coef * X_transformed
    
    # Pair with feature names and sort by contribution (we want top positive contributors pushing probability UP)
    feature_contributions = list(zip(_feature_names, contributions))
    feature_contributions.sort(key=lambda x: x[1], reverse=True)
    
    # Map top 2-3 positive contributors to human readable strings
    reasons = []
    for feat_name, contrib in feature_contributions:
        if contrib > 0 and len(reasons) < 2:
            # Fallback to feature name if not in map
            friendly_name = EXPLANATION_MAP.get(feat_name, feat_name)
            # Remove day_of_week as a primary reason as it might confuse clinicians in prototype, 
            # but keep it if it's the only one
            if 'day_of_week' not in friendly_name:
                reasons.append(friendly_name)
                
    # Fallback if no strong positive reasons
    if not reasons:
        reasons = ["General patient profile"]
        
    # Format output
    return {
        "probability": round(probability, 2),
        "risk_level": risk_level,
        "reasons": reasons,
        "recommended_action": recommended_action
    }

if __name__ == "__main__":
    # Test block
    test_input = {
      "age": 23,
      "gender": "F",
      "scholarship": False,
      "hypertension": False,
      "diabetes": False,
      "sms_received": True,
      "lead_time": 12
    }
    
    print("Testing predict() function:")
    print(json.dumps(test_input, indent=2))
    
    try:
        result = predict(test_input)
        print("\nOutput:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\nError: {e}")
