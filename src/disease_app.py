'''
import streamlit as st
import pandas as pd
import joblib
from ui_components import DiseaseUI

# Load model and encoders
model = joblib.load("models/GradientBoosting_model.pkl")
encoders = joblib.load("models/feature_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

# Apply custom UI
DiseaseUI.apply_custom_css()

# Collect inputs
input_data = DiseaseUI.patient_form(encoders)

# Predict
if st.button("🔍 Predict Disease"):
    df = pd.DataFrame([input_data])

    # Replace "None" with neutral/normal values
    df.replace("None", "Normal", inplace=True)

    # Encode categorical features
    for col, le in encoders.items():
        if col in df.columns:
            df[col] = le.transform(df[col])

    # Make prediction
    pred_encoded = model.predict(df)[0]
    predicted_disease = target_encoder.inverse_transform([pred_encoded])[0]

    # Show result
    if predicted_disease.lower() == "healthy":
        DiseaseUI.show_result(predicted_disease, healthy=True)
    else:
        DiseaseUI.show_result(predicted_disease)

# Footer
DiseaseUI.show_footer()
'''

import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load trained model and encoders
model = joblib.load("models/GradientBoosting_model.pkl")
encoders = joblib.load("models/feature_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

st.title("🩺 Patient Disease Prediction App")
st.markdown("This AI tool predicts possible diseases based on patient symptoms and vitals.")

# Input fields with sensible defaults
age = st.number_input("Age", 1, 100, 30)
gender = st.selectbox("Gender", encoders["Gender"].classes_)
body_temperature = st.number_input("Body Temperature (°C)", 34.0, 42.0, 36.8)
cough = st.selectbox("Cough", ["None", "Mild", "Severe"])
headache = st.selectbox("Headache", ["None", "Mild", "Severe"])
fatigue = st.selectbox("Fatigue", ["None", "Moderate", "High"])
blood_pressure = st.selectbox("Blood Pressure", ["Normal", "Low", "High"])
heart_rate = st.number_input("Heart Rate (bpm)", 40, 180, 80)
wbc_count = st.number_input("WBC Count (x10⁹/L)", 2.0, 20.0, 7.0)
sugar_level = st.number_input("Sugar Level (mg/dL)", 50, 300, 100)

# --- Smart Healthy Rule ---
def is_healthy():
    return (
        cough == "None" and
        headache == "None" and
        fatigue == "None" and
        blood_pressure == "Normal" and
        36 <= body_temperature <= 37.2 and
        60 <= heart_rate <= 90 and
        4 <= wbc_count <= 11 and
        80 <= sugar_level <= 140
    )

# Predict button
if st.button("🔍 Predict Disease"):
    if is_healthy():
        predicted_disease = "Healthy"
        st.success("🩺 The patient appears **Healthy** based on provided values.")
    else:
        # Encode categorical inputs
        input_data = {
            "Age": age,
            "Gender": encoders["Gender"].transform([gender])[0],
            "Body_Temperature": body_temperature,
            "Cough": encoders["Cough"].transform([cough])[0] if cough in encoders["Cough"].classes_ else 0,
            "Headache": encoders["Headache"].transform([headache])[0] if headache in encoders["Headache"].classes_ else 0,
            "Fatigue": encoders["Fatigue"].transform([fatigue])[0] if fatigue in encoders["Fatigue"].classes_ else 0,
            "Blood_Pressure": encoders["Blood_Pressure"].transform([blood_pressure])[0] if blood_pressure in encoders["Blood_Pressure"].classes_ else 0,
            "Heart_Rate": heart_rate,
            "WBC_Count": wbc_count,
            "Sugar_Level": sugar_level
        }

        df = pd.DataFrame([input_data])
        pred_encoded = model.predict(df)[0]
        predicted_disease = target_encoder.inverse_transform([pred_encoded])[0]

        st.success(f"🩸 Predicted Disease: **{predicted_disease}**")

    st.info("Note: This prediction is based on trained AI model patterns. Consult a doctor for confirmation.")
