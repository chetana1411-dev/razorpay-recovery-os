import pandas as pd
import numpy as np
import json
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, precision_score, recall_score, f1_score

# Ensure directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("docs", exist_ok=True)

# 1. Load Data
df = pd.read_csv("data/synthetic/payments.csv")

# Filter only recovery-eligible cases for ML scoring
eligible_df = df[df["recovery_eligible"] == 1].copy()

# 2. Feature Engineering & Preprocessing
features = ["amount", "attempt_number", "previous_success_rate", "time_since_failure_minutes", "is_subscription"]
categorical_cols = ["payment_method", "failure_reason"]

X = pd.get_dummies(eligible_df[features + categorical_cols], drop_first=True)
y = eligible_df["recovery_success"]

# Save feature columns list for later inference
feature_names = list(X.columns)

# 3. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Train Random Forest Model
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate Model
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_prob)
conf_matrix = confusion_matrix(y_test, y_pred).tolist()

metrics = {
    "total_samples": len(eligible_df),
    "test_samples": len(X_test),
    "precision": round(float(precision), 4),
    "recall": round(float(recall), 4),
    "f1_score": round(float(f1), 4),
    "roc_auc": round(float(roc_auc), 4),
    "confusion_matrix": conf_matrix,
    "feature_names": feature_names
}

# 6. Save Model Artifacts
with open("models/recovery_model.pkl", "wb") as f:
    pickle.dump({"model": model, "features": feature_names}, f)

with open("docs/model_evaluation.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("--- ML MODEL TRAINED SUCCESSFULLY ---")
print(f"ROC-AUC Score: {roc_auc:.4f}")
print(f"Precision: {precision:.4f} | Recall: {recall:.4f} | F1-Score: {f1:.4f}")
print("Saved model to: models/recovery_model.pkl")
print("Saved evaluation to: docs/model_evaluation.json")