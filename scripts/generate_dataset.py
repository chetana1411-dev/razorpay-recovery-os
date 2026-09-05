import csv
import random
import os
import pandas as pd
import numpy as np

# Set reproducible seed
np.random.seed(42)
random.seed(42)

# Ensure directory exists
os.makedirs("data/synthetic", exist_ok=True)

NUM_RECORDS = 1500

PAYMENT_METHODS = ["upi", "card", "netbanking", "wallet"]
FAILURE_REASONS = [
    "temporary_network_error",
    "insufficient_funds",
    "authentication_failure",
    "bank_declined",
    "timeout",
    "limit_exceeded"
]

records = []

for i in range(1, NUM_RECORDS + 1):
    payment_id = f"pay_{i:04d}"
    merchant_id = f"merch_{random.randint(100, 105)}"
    customer_id = f"cust_{random.randint(1000, 1200)}"
    
    amount = round(random.choice([199, 499, 999, 1499, 2999, 4999, 9999, 15000, 25000]), 2)
    currency = "INR"
    method = random.choice(PAYMENT_METHODS)
    reason = random.choice(FAILURE_REASONS)
    status = "FAILED"
    attempts = random.choice([1, 1, 1, 2, 2, 3])
    prev_success_rate = round(random.uniform(0.1, 0.95), 2)
    time_since_fail = random.randint(1, 180) # in minutes
    is_sub = random.choice([0, 1])
    
    # Ground Truth Logic
    # Higher success rate if low amount, network/timeout error, high prev_success_rate
    recovery_prob = 0.5
    if reason in ["temporary_network_error", "timeout"]:
        recovery_prob += 0.3
    elif reason in ["insufficient_funds", "limit_exceeded"]:
        recovery_prob -= 0.2
        
    if prev_success_rate > 0.7:
        recovery_prob += 0.15
        
    if attempts > 2:
        recovery_prob -= 0.3

    recovery_prob = max(0.05, min(0.95, recovery_prob))
    recovery_eligible = 1 if recovery_prob > 0.2 and attempts < 4 else 0
    
    # Outcomes
    if not recovery_eligible:
        rec_action = "STOP"
        rec_success = 0
        rec_amount = 0.0
    else:
        # Determine intervention based on reason
        if reason in ["temporary_network_error", "timeout"]:
            rec_action = "RETRY_PAYMENT"
        elif amount > 5000 or reason == "insufficient_funds":
            rec_action = "SEND_PAYMENT_LINK"
        else:
            rec_action = "SEND_REMINDER"
            
        rec_success = 1 if random.random() < recovery_prob else 0
        rec_amount = amount if rec_success else 0.0

    records.append({
        "payment_id": payment_id,
        "merchant_id": merchant_id,
        "customer_id": customer_id,
        "amount": amount,
        "currency": currency,
        "payment_method": method,
        "failure_reason": reason,
        "payment_status": status,
        "attempt_number": attempts,
        "previous_success_rate": prev_success_rate,
        "time_since_failure_minutes": time_since_fail,
        "is_subscription": is_sub,
        "recovery_eligible": recovery_eligible,
        "recovery_action": rec_action,
        "recovery_success": rec_success,
        "recovered_amount": rec_amount
    })

df = pd.DataFrame(records)
output_path = "data/synthetic/payments.csv"
df.to_csv(output_path, index=False)

# Print Summary
print("--- DATASET GENERATED ---")
print(f"Total Payments: {len(df)}")
print(f"Eligible for Recovery: {df['recovery_eligible'].sum()}")
print(f"Total Revenue at Risk: ₹{df['amount'].sum():,.2f}")
print(f"Total Simulated Recovered: ₹{df['recovered_amount'].sum():,.2f}")
print(f"Recovery Success Rate: {(df['recovery_success'].sum() / len(df))*100:.2f}%")
print("Saved to:", output_path)