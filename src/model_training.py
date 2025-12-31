import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


# ===============================
# Load Dataset
# ===============================
DATA_PATH = "data/patient_symptoms_dataset.csv"

df = pd.read_csv(DATA_PATH)

# Drop non-predictive ID column if present
if "Patient_ID" in df.columns:
    df.drop(columns=["Patient_ID"], inplace=True)

# ===============================
# Handle Missing Values
# ===============================
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna(df[col].mode()[0])
    else:
        df[col] = df[col].fillna(df[col].median())

# ===============================
# Encode Categorical Features
# ===============================
feature_encoders = {}

categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
categorical_cols.remove("Disease")

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    feature_encoders[col] = le

# Encode target
target_encoder = LabelEncoder()
df["Disease"] = target_encoder.fit_transform(df["Disease"])

# ===============================
# Train-Test Split
# ===============================
X = df.drop(columns=["Disease"])
y = df["Disease"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ===============================
# Define Models
# ===============================
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Naive Bayes": GaussianNB(),
    "Support Vector Machine": SVC(kernel="rbf", probability=True),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
}

# ===============================
# Model Training & Evaluation
# ===============================
results = []

print("\n=== Model Comparison Results ===\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")

    results.append({
        "Model": name,
        "Accuracy": round(acc, 4),
        "F1_Score": round(f1, 4)
    })

    print(f"{name}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  F1-score : {f1:.4f}\n")

# ===============================
# Results Table
# ===============================
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="F1_Score", ascending=False)

print("\n=== Final Comparison Table ===")
print(results_df)

# Save comparison table for paper
results_df.to_csv("models/model_comparison_results.csv", index=False)

# ===============================
# Save Best Model
# ===============================
best_model_name = results_df.iloc[0]["Model"]
best_model = models[best_model_name]

joblib.dump(best_model, f"models/{best_model_name}_model.pkl")
joblib.dump(feature_encoders, "models/feature_encoders.pkl")
joblib.dump(target_encoder, "models/target_encoder.pkl")

print(f"\n Best Model Selected: {best_model_name}")
print(" Model and encoders saved successfully!")
