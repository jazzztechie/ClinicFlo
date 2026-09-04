"""
Optional helper: trains a tiny placeholder scikit-learn model and saves it
to clinicflo_model.pkl, matching the contract services/prediction.py expects.

This is NOT required to run the backend -- services/prediction.py already
falls back to a built-in heuristic if no .pkl file is present. Run this
only if you want to test the "real model" code path before the ML team
delivers the actual trained model:

    python model/train_placeholder_model.py

Contract:
    - model.predict_proba(X) -> ndarray shape (n_samples, 2), column 1 = P(no-show)
    - X columns, in order: age, gender_code, scholarship, hypertension,
      diabetes, sms_received, lead_time
      (gender_code: 0=M, 1=F, 2=Other)
"""
import os

import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

RNG = np.random.default_rng(42)
N = 500

age = RNG.integers(1, 90, N)
gender_code = RNG.integers(0, 3, N)
scholarship = RNG.integers(0, 2, N)
hypertension = RNG.integers(0, 2, N)
diabetes = RNG.integers(0, 2, N)
sms_received = RNG.integers(0, 2, N)
lead_time = RNG.integers(0, 60, N)

X = np.column_stack(
    [age, gender_code, scholarship, hypertension, diabetes, sms_received, lead_time]
)

# Synthetic labels loosely following the same intuition as the dummy
# heuristic in services/prediction.py, plus noise.
logits = (
    -1.5
    + 0.03 * lead_time
    + 0.4 * ((age >= 18) & (age <= 35)).astype(float)
    - 0.6 * sms_received
    + 0.2 * scholarship
    - 0.2 * hypertension
    - 0.2 * diabetes
    + RNG.normal(0, 0.5, N)
)
prob = 1 / (1 + np.exp(-logits))
y = (RNG.random(N) < prob).astype(int)

model = LogisticRegression()
model.fit(X, y)

out_path = os.path.join(os.path.dirname(__file__), "clinicflo_model.pkl")
joblib.dump(model, out_path)
print(f"Placeholder model saved to {out_path}")
