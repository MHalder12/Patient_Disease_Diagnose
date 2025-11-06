# src/model_training.py
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report

# ===== Load dataset =====
df = pd.read_csv("data/patient_symptoms_dataset.csv")

# ===== Drop ID column if present =====
if "Patient_ID" in df.columns:
    df = df.drop("Patient_ID", axis=1)

# ===== Handle missing values =====
# For numeric columns — fill with median
for col in df.select_dtypes(include=['int64', 'float64']).columns:
    df[col] = df[col].fillna(df[col].median())

# For categorical columns — fill with mode
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# ===== Encode categorical features =====
categorical_cols = ['Gender', 'Cough', 'Headache', 'Fatigue', 'Blood_Pressure']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# ===== Encode target =====
target_le = LabelEncoder()
df['Disease'] = target_le.fit_transform(df['Disease'])

# ===== Split data =====
X = df.drop('Disease', axis=1)
y = df['Disease']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===== Train model =====
model = GradientBoostingClassifier()
model.fit(X_train, y_train)

# ===== Evaluate =====
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("✅ Model trained successfully!")
print(f"Accuracy: {acc:.3f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ===== Save models =====
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/GradientBoosting_model.pkl")
joblib.dump(encoders, "models/feature_encoders.pkl")
joblib.dump(target_le, "models/target_encoder.pkl")

print("✅ Model, encoders, and target encoder saved successfully!")
