import pandas as pd
import pickle
import json
import os
import sys

# Add project root to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.policy_engine import PolicyEngine

# Ensure output directories exist
os.makedirs("data/output", exist_ok=True)

# 1. Load ML Model & Feature Specs
with open("models/recovery_model.pkl", "rb") as f:
    model_data = pickle.load(f)

model = model_data["model"]
model_features = model_data["features"]

# 2. Load Synthetic Dataset
df = pd.read_csv("data/synthetic/payments.csv")

# Initialize Policy Engine
engine = PolicyEngine()

audit_log = []

# Process payments
for idx, row in df.iterrows():
    payment_record = row.to_dict()
    
    # Extract ML Probability score
    if payment_record.get("recovery_eligible") == 1:
        # One-hot encode row to match training features
        row_df = pd.DataFrame([payment_record])
        row_encoded = pd.get_dummies(row_df[["amount", "attempt_number", "previous_success_rate", "time_since_failure_minutes", "is_subscription", "payment_method", "failure_reason"]])
        
        # Align columns with training features
        for col in model_features:
            if col not in row_encoded.columns:
                row_encoded[col] = 0
        row_encoded = row_encoded[model_features]
        
        pred_prob = float(model.predict_proba(row_encoded)[0, 1])
    else:
        pred_prob = 0.0

    # Pass through Policy Engine
    policy_outcome = engine.evaluate_policy(payment_record, pred_prob)

    # Calculate actual simulated financial result
    action = policy_outcome["allowed_action"]
    ground_truth_success = payment_record.get("recovery_success", 0)
    amount = payment_record.get("amount", 0.0)

    if action == "STOP":
        recovered_amount = 0.0
        final_status = "FAILED"
    elif ground_truth_success == 1 and action in ["RETRY_PAYMENT", "SEND_PAYMENT_LINK", "SEND_REMINDER"]:
        recovered_amount = amount
        final_status = "RECOVERED"
    else:
        recovered_amount = 0.0
        final_status = "FAILED"

    log_entry = {
        "payment_id": payment_record["payment_id"],
        "customer_id": payment_record["customer_id"],
        "amount": amount,
        "failure_reason": payment_record["failure_reason"],
        "attempt_number": payment_record["attempt_number"],
        "ml_predicted_recovery_prob": round(pred_prob, 4),
        "policy_action": action,
        "policy_rule": policy_outcome["rule_applied"],
        "policy_approved": policy_outcome["policy_approved"],
        "final_status": final_status,
        "recovered_amount": recovered_amount
    }
    
    audit_log.append(log_entry)

# Save Audit Log JSON
output_path = "data/output/recovery_audit_log.json"
with open(output_path, "w") as f:
    json.dump(audit_log, f, indent=2)

# Metrics summary
audit_df = pd.DataFrame(audit_log)
total_risk = audit_df["amount"].sum()
total_recovered = audit_df["recovered_amount"].sum()
recovery_rate = (total_recovered / total_risk) * 100 if total_risk > 0 else 0

print("--- RECOVERY SIMULATION COMPLETE ---")
print(f"Total Cases Processed: {len(audit_df)}")
print(f"Total Revenue at Risk: ₹{total_risk:,.2f}")
print(f"Total Recovered Revenue: ₹{total_recovered:,.2f}")
print(f"Policy Engine Recovery Rate: {recovery_rate:.2f}%")
print("Action Distribution:")
print(audit_df["policy_action"].value_counts().to_string())
print(f"\nSaved full audit trail to: {output_path}")