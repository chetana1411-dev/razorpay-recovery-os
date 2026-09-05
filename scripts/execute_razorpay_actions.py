import os
import sys
import json

# Force Python to recognize the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.razorpay_executor import execute_recovery_action

audit_log_path = os.path.join(project_root, "data", "output", "recovery_audit_log.json")
output_execution_path = os.path.join(project_root, "data", "output", "razorpay_execution_log.json")

if not os.path.exists(audit_log_path):
    print("Error: Audit log not found. Running recovery simulation first...")
    os.system("python scripts/run_recovery_simulation.py")

with open(audit_log_path, "r") as f:
    audit_log = json.load(f)

print(f"--- EXECUTING RAZORPAY RECOVERY ACTIONS ({len(audit_log)} cases) ---")

execution_results = []
link_count = 0

# Sample the first 50 cases for fast execution
sample_log = audit_log[:50]

for entry in sample_log:
    res = execute_recovery_action(entry)
    execution_results.append({**entry, **res})
    if res.get("action") == "SEND_PAYMENT_LINK":
        link_count += 1

with open(output_execution_path, "w") as f:
    json.dump(execution_results, f, indent=2)

print(f"Successfully processed {len(sample_log)} payment recovery actions.")
print(f"Razorpay Payment Links Generated: {link_count}")
print(f"Saved execution log to: {output_execution_path}")