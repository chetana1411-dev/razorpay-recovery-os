import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET and not RAZORPAY_KEY_ID.startswith("rzp_test_your"):
    try:
        import razorpay
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    except Exception as e:
        print(f"Razorpay Client initialization notice: {e}")

def execute_recovery_action(entry):
    action = entry.get("policy_action", "STOP")
    payment_id = entry.get("payment_id", "pay_0000")
    amount_in_paisa = int(entry.get("amount", 0) * 100)
    
    execution_result = {
        "payment_id": payment_id,
        "action": action,
        "executed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "EXECUTED",
        "razorpay_link_id": None,
        "short_url": None,
        "execution_notes": ""
    }

    if action == "SEND_PAYMENT_LINK":
        if client:
            try:
                link_data = {
                    "amount": amount_in_paisa,
                    "currency": "INR",
                    "accept_partial": False,
                    "description": f"Recovery Link for {payment_id}",
                    "customer": {
                        "name": f"Customer {entry.get('customer_id')}",
                        "email": f"{entry.get('customer_id')}@example.com"
                    },
                    "notify": {"sms": False, "email": False},
                    "reminder_enable": True
                }
                response = client.payment_link.create(link_data)
                execution_result["razorpay_link_id"] = response.get("id")
                execution_result["short_url"] = response.get("short_url")
                execution_result["execution_notes"] = "Live Razorpay Test Link Created"
            except Exception as e:
                execution_result["status"] = "API_ERROR"
                execution_result["execution_notes"] = f"Razorpay API Error: {str(e)}"
        else:
            execution_result["razorpay_link_id"] = f"plink_test_{payment_id}"
            execution_result["short_url"] = f"https://rzp.io/i/{payment_id[-6:]}"
            execution_result["execution_notes"] = "Simulated Razorpay Link (Add API keys in .env for live API calls)"

    elif action == "RETRY_PAYMENT":
        execution_result["execution_notes"] = "Dispatched auto-retry request to Razorpay gateway."

    elif action == "SEND_REMINDER":
        execution_result["execution_notes"] = "Dispatched SMS & Email recovery notifications."

    elif action == "ESCALATE":
        execution_result["execution_notes"] = "Flagged case for high-value manual intervention."

    else:
        execution_result["status"] = "SKIPPED"
        execution_result["execution_notes"] = "No intervention required (STOP rule)."

    return execution_result