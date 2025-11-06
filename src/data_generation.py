import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)

# Number of samples
n = 2000

# Generate synthetic patient data
def generate_patient_data(n=2000):
    ages = np.random.randint(18, 85, n)
    genders = np.random.choice(["Male", "Female", "Other"], n, p=[0.47, 0.47, 0.06])
    body_temp = np.round(np.random.normal(37.0, 0.8, n), 1)
    cough = np.random.choice(["None", "Mild", "Severe"], n, p=[0.5, 0.3, 0.2])
    headache = np.random.choice(["None", "Mild", "Severe"], n, p=[0.4, 0.4, 0.2])
    fatigue = np.random.choice(["None", "Moderate", "High"], n, p=[0.3, 0.4, 0.3])
    blood_pressure = np.random.choice(["Normal", "High", "Low"], n, p=[0.6, 0.25, 0.15])
    heart_rate = np.random.randint(55, 140, n)
    wbc_count = np.random.normal(7000, 1500, n).astype(int)
    sugar_level = np.round(np.random.normal(110, 30, n), 1)

    # Map symptoms to diseases (simplified synthetic logic)
    diseases = []
    for i in range(n):
        if body_temp[i] > 38 and cough[i] == "Severe":
            diseases.append("Pneumonia")
        elif sugar_level[i] > 150:
            diseases.append("Diabetes")
        elif blood_pressure[i] == "High" and heart_rate[i] > 100:
            diseases.append("Hypertension")
        elif fatigue[i] == "High" and wbc_count[i] < 5000:
            diseases.append("Anemia")
        elif headache[i] == "Severe" and fatigue[i] == "None":
            diseases.append("Migraine")
        elif all([
            36 <= body_temp[i] <= 37.5,
            cough[i] == "None",
            fatigue[i] == "None"
        ]):
            diseases.append("Healthy")
        else:
            diseases.append("Flu")

    # Combine into DataFrame
    df = pd.DataFrame({
        "Patient_ID": np.arange(1, n+1),
        "Age": ages,
        "Gender": genders,
        "Body_Temperature": body_temp,
        "Cough": cough,
        "Headache": headache,
        "Fatigue": fatigue,
        "Blood_Pressure": blood_pressure,
        "Heart_Rate": heart_rate,
        "WBC_Count": wbc_count,
        "Sugar_Level": sugar_level,
        "Disease": diseases
    })

    # Add some missing values randomly
    for col in ["Body_Temperature", "Heart_Rate", "WBC_Count", "Sugar_Level"]:
        df.loc[df.sample(frac=0.02, random_state=42).index, col] = np.nan

    return df


if __name__ == "__main__":
    df = generate_patient_data(n)
    df.to_csv("data/patient_symptoms_dataset.csv", index=False)
    print("✅ Synthetic patient dataset generated and saved to 'data/patient_symptoms_dataset.csv'")
    print(df.head())
