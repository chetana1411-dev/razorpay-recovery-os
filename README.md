# RecoveryOS — Autonomous AI Revenue Recovery

## 🚀 Live Demo & Links

- **Live Dashboard:** https://razorpay-recovery-os.vercel.app/
- **Repository:** (https://github.com/chetana1411-dev/razorpay-recovery-os.git)
- **Track:** AI Revenue Recovery (Payment Degradation & Bounded Recovery)
---

## 🎯 Core Capabilities

1. **Diagnosis & Failure Analysis:** Classifies bank declines, network timeouts, authentication failures, and insufficient funds.
2. **ML Risk Scoring:** Predicts ground-truth recovery probability using historical customer metrics and transaction context.
3. **Deterministic Policy Engine:** Enforces hard financial guardrails (Max 3 retries, high-value payment links, low-probability auto-stops).
4. **Razorpay Test API Integration:** Automatically dispatches official Razorpay Payment Links (`plink_...`) via the Razorpay API.
5. **Full Audit Trail:** Every action produces a transparent decision log with rule metadata, risk scores, and execution timestamps.

---

RecoveryOS is an autonomous revenue recovery engine built for the Razorpay challenge. It detects payment failures and subscription degradation, diagnoses root causes using Machine Learning, and executes policy-bounded interventions (auto-retries, Razorpay test payment links, gentle reminders, or safe stops) with complete auditability.

---

## 🎯 Meeting "The Bar"

- **Identify & Diagnose:** Categorizes 1,500+ failed payment scenarios by root failure reason (network errors, insufficient funds, timeouts, limit errors).
- **Right Intervention:** ML model predicts recovery likelihood and maps optimal interventions (`RETRY_PAYMENT`, `SEND_PAYMENT_LINK`, `SEND_REMINDER`).
- **Bounded Workflow & Guardrails:** Hard-coded Policy Engine enforces max 3 retry caps, low-probability stops, and escalation rules.
- **Measured Money Recovered:** Live batch dashboard tracking Revenue at Risk vs. Recovered Revenue and Recovery Rate %.
- **Audit Trail:** Transparent JSON audit log (`data/output/razorpay_execution_log.json`) recording every rule applied, risk score, and timestamp.

---

## 🏗️ Tech Stack

- **ML & Data Pipeline:** Python, Pandas, Scikit-Learn (Random Forest Classifier)
- **Policy Engine & Guardrails:** Python (Deterministic Rule Engine)
- **Payment Execution:** Razorpay Python SDK (Test Mode API Links)
- **Frontend Dashboard:** Next.js, TailwindCSS, Vercel
- **Version Control:** Git & GitHub

---

## 🛠️ How to Run Locally

Follow these steps to run RecoveryOS locally from scratch, generate data, train the ML model, execute payment actions, and launch the dashboard.

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- Git

---

### Step 1: Clone Repository & Setup Environment
```bash
git clone [https://github.com/your-username/razorpay-recovery-os.git](https://github.com/your-username/razorpay-recovery-os.git)
cd razorpay-recovery-os

Create a .env file in the project root:
RAZORPAY_KEY_ID=rzp_test_your_key_id_here
RAZORPAY_KEY_SECRET=your_key_secret_here

(Note: If no API key is set, the system automatically uses built-in fallback test link generators so local execution never breaks.)

Step 2: Install Python Dependencies

python -m pip install pandas numpy scikit-learn razorpay python-dotenv

Step 3: Generate Synthetic Payment Dataset (Step 3 Target)
Generates 1,500+ realistic payment failure records categorized by root cause (temporary_network_error, insufficient_funds, bank_declined, etc.) and ground-truth recovery conditions.

Bash
python scripts/generate_dataset.py
Output: data/synthetic/payments.csv

Step 4: Train ML Recovery Risk Model (Step 4 Target)
Trains a Random Forest classifier on recovery-eligible failure cases to predict ground-truth recovery probabilities. Calculates Precision, Recall, F1, and ROC-AUC metrics.

Bash
python scripts/train_model.py
Outputs:

Trained Model: models/recovery_model.pkl

Metrics Evaluation: docs/model_evaluation.json

Step 5: Run Policy Engine & Simulation (Step 5 & 6 Target)
Passes payment records and ML risk probabilities through the Deterministic Policy Engine (src/policy_engine.py) to apply strict financial guardrails (Max 3 retries, high-value payment links, auto-stops).

Bash
python scripts/run_recovery_simulation.py
Output: data/output/recovery_audit_log.json

Step 6: Execute Razorpay Test API Actions (Step 7 & 9 Target)
Dispatches policy-approved recovery actions via the official Razorpay Python SDK to generate active test payment links (plink_...) and log execution timestamps.

Bash
python scripts/execute_razorpay_actions.py
Output: data/output/razorpay_execution_log.json

Step 7: Launch Next.js Vercel Dashboard (Step 11 Target)
Copy the execution audit log into the dashboard application and launch the web interface locally:

Bash
# Copy latest audit logs into dashboard source
Copy-Item "data\output\razorpay_execution_log.json" "dashboard\src\app\data.json"

# Navigate to dashboard directory and start local dev server
cd dashboard
npm install
npm run dev
Open your browser and navigate to http://localhost:3000 to inspect live financial metrics, risk scores, applied policy guardrail rules, and active Razorpay test links.


---

### Final Push to GitHub

Once you paste and save `README.md`, run this in PowerShell:

```powershell
git add .
git commit -m "docs: finalize root README with complete submission details and local run guide"
git push
