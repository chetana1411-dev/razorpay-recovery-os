# AI vs. Deterministic Guardrail Boundaries

## Where AI/ML is Used
1. **Root Cause Diagnosis:** Analyzing payment failure codes, time since failure, customer history, and subscription status.
2. **Recovery Probability Scoring:** Predicting the probability ($0.0 - 1.0$) that an intervention will result in successful revenue recovery.

## Where AI is Strictly Forbidden (Deterministic Guardrails)
To prevent uncontrolled re-billing, runaway retries, or customer harassment, **no AI model is permitted to execute financial transactions directly.** 

All AI recommendations must pass through the **Deterministic Policy Engine** (`src/policy_engine.py`):
- **Hard Attempt Cap:** Max 3 retries $\rightarrow$ Forced `ESCALATE`.
- **Low Probability Threshold:** $P(\text{recovery}) < 0.25 \rightarrow$ Forced `STOP` to eliminate fee waste.
- **Transient Technical Failures:** Network/timeout $\rightarrow$ Authorized `RETRY_PAYMENT`.
- **Liquidity / High Value:** Amount > ₹10,000 or insufficient funds $\rightarrow$ Authorized `SEND_PAYMENT_LINK`.