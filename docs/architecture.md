# System Architecture — RecoveryOS

+-----------------------------------------------------------------------+
|                      RECOVERYOS ARCHITECTURE                          |
+-----------------------------------------------------------------------+
                                   │
                                   ▼
                   +-------------------------------+
                   |     Failed Payment Event      |
                   +-------------------------------+
                                   │
                                   ▼
                   +-------------------------------+
                   |  Synthetic Dataset Generator  |
                   | (data/synthetic/payments.csv) |
                   +-------------------------------+
                                   │
                                   ▼
                   +-------------------------------+
                   | Feature Engineering & ML Risk |
                   |  (models/recovery_model.pkl)  |
                   +-------------------------------+
                                   │
                         Calculates P(Recovery)
                                   │
                                   ▼
                   +-------------------------------+
                   | Deterministic Policy Engine   |
                   |    (src/policy_engine.py)     |
                   |   Enforces Hard Guardrails    |
                   +-------------------------------+
                                   │
        +--------------------------+--------------------------+
        │                          │                          │
        ▼                          ▼                          ▼
+---------------+          +---------------+          +---------------+
| RETRY_PAYMENT |          | PAYMENT_LINK  |          | STOP/ESCALATE |
+---------------+          +---------------+          +---------------+
        │                          │                          │
        +--------------------------+--------------------------+
                                   │
                                   ▼
                   +-------------------------------+
                   |    Razorpay API Executor      |
                   |   (src/razorpay_executor.py)  |
                   | Generates Test Payment Links  |
                   +-------------------------------+
                                   │
                                   ▼
                   +-------------------------------+
                   | Bounded Recovery Audit Trail  |
                   | (razorpay_execution_log.json) |
                   +-------------------------------+
                                   │
                                   ▼
                   +-------------------------------+
                   |   Next.js Vercel Dashboard    |
                   +-------------------------------+

# Failure Recovery & Boundary Safety

## Edge Cases Handled

1. **API Timeouts & Gateway Errors:**
   If the Razorpay API endpoint times out or returns an error during payment link creation, the executor catches the exception, logs `API_ERROR` in the audit log, and flags the record for manual retry without corrupting system state.

2. **Runaway Retries:**
   Prevented by Rule 2 in `policy_engine.py`. Any transaction reaching 3 attempts is automatically diverted to `ESCALATE` status.

3. **Low-Value High-Risk Cases:**
   Transactions with low historical customer success rates or recovery probabilities under 25% are mapped to `STOP` to conserve system resources and merchant goodwill.

4. **Malformed Context / Non-Eligible Payments:**
   Payments marked `recovery_eligible = 0` are immediately assigned `STOP` status with 0 recovered revenue, ensuring impossible states are blocked before execution.