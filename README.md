# RecoveryOS — Autonomous AI Revenue Recovery

> **Razorpay AI Challenge Submission**  
> **Track:** AI Revenue Recovery (Payment Failure Degradation & Bounded Intervention)

RecoveryOS is an autonomous revenue recovery engine that detects failed payments, diagnoses root causes using machine learning, and executes policy-bounded interventions (auto-retries, Razorpay test payment links, gentle reminders, or safe stops) without exposing merchants to uncontrolled re-billing risks.

---

## 🚀 Live Demo & Links

- **Live Dashboard:** https://razorpay-recovery-os.vercel.app/
- **Repository:** (https://github.com/chetana1411-dev/razorpay-recovery-os.git)

---

## 🎯 Core Capabilities

1. **Diagnosis & Failure Analysis:** Classifies bank declines, network timeouts, authentication failures, and insufficient funds.
2. **ML Risk Scoring:** Predicts ground-truth recovery probability using historical customer metrics and transaction context.
3. **Deterministic Policy Engine:** Enforces hard financial guardrails (Max 3 retries, high-value payment links, low-probability auto-stops).
4. **Razorpay Test API Integration:** Automatically dispatches official Razorpay Payment Links (`plink_...`) via the Razorpay API.
5. **Full Audit Trail:** Every action produces a transparent decision log with rule metadata, risk scores, and execution timestamps.

---

## 🏗️ Architecture

Failed Payment Event
│
▼
ML Risk Model (Scikit-Learn / XGBoost)
│
▼
Policy Guardrail Engine (Deterministic Rules)
│
┌───┴────────────────────────┐
▼                            ▼
[STOP / ESCALATE]       [SEND_PAYMENT_LINK / RETRY]
│                            │
▼                            ▼
Audit Trail Log          Razorpay Test API
│                            │
└────────────┬───────────────┘
▼
Vercel Next.js Dashboard

---

## 🛠️ Tech Stack

- **ML & Data Pipeline:** Python, Pandas, Scikit-Learn
- **Payment Execution:** Razorpay Python SDK
- **Frontend Dashboard:** Next.js (App Router), TailwindCSS, Vercel
- **Version Control:** GitHub

