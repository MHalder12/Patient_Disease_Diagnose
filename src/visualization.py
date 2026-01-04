import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# ----------------------------
# Load trained model & encoders
# ----------------------------
model = joblib.load("models/Random Forest_model.pkl")
feature_encoders = joblib.load("models/feature_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

# ----------------------------
# Load dataset
# ----------------------------
df = pd.read_csv("data/patient_symptoms_dataset.csv")

X = df.drop(columns=["Disease", "Patient_ID"])
y = df["Disease"]

# ----------------------------
# Handle missing values (same as training)
# ----------------------------
for col in X.columns:
    if X[col].dtype == "object":
        X[col] = X[col].fillna(X[col].mode()[0])
    else:
        X[col] = X[col].fillna(X[col].median())

# ----------------------------
# Encode categorical features
# ----------------------------
for col, le in feature_encoders.items():
    X[col] = le.transform(X[col])


y_encoded = target_encoder.transform(y)

# ----------------------------
# 1️⃣ Confusion Matrix
# ----------------------------
y_pred = model.predict(X)

cm = confusion_matrix(y_encoded, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=target_encoder.classes_,
    yticklabels=target_encoder.classes_
)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix for Disease Prediction Model")
plt.tight_layout()
plt.savefig("visuals/confusion_matrix.png", dpi=300)
plt.close()

print("✅ Confusion matrix saved.")

# ----------------------------
# 2️⃣ Feature Importance Plot
# ----------------------------
importances = model.feature_importances_
feature_names = X.columns

fi_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

plt.figure(figsize=(8, 6))
sns.barplot(x="Importance", y="Feature", data=fi_df)
plt.title("Feature Importance for Disease Prediction")
plt.tight_layout()
plt.savefig("visuals/feature_importance.png", dpi=300)
plt.close()

print("✅ Feature importance plot saved.")

# ----------------------------
# 3️⃣ Feature Distribution Plots
# ----------------------------
numerical_features = [
    "Body_Temperature",
    "Heart_Rate",
    "WBC_Count",
    "Sugar_Level"
]

plt.figure(figsize=(10, 8))

for i, col in enumerate(numerical_features, 1):
    plt.subplot(2, 2, i)
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")

plt.tight_layout()
plt.savefig("visuals/feature_distributions.png", dpi=300)
plt.close()

print("✅ Feature distribution plots saved.")


