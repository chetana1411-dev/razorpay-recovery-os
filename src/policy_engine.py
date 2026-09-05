import json

class PolicyEngine:
    """
    Deterministic Guardrail System for RecoveryOS.
    Enforces financial and operational business rules regardless of AI recommendations.
    """

    ALLOWED_ACTIONS = {
        "RETRY_PAYMENT",
        "SEND_PAYMENT_LINK",
        "SEND_REMINDER",
        "ESCALATE",
        "STOP"
    }

    def evaluate_policy(self, payment_record, predicted_prob):
        """
        Evaluates input features and ML risk score against hard coded business rules.
        """
        amount = payment_record.get("amount", 0)
        reason = payment_record.get("failure_reason", "")
        attempts = payment_record.get("attempt_number", 1)
        eligible = payment_record.get("recovery_eligible", 0)

        # Rule 1: Non-eligible or already stopped payments
        if eligible == 0:
            return {
                "allowed_action": "STOP",
                "policy_approved": True,
                "rule_applied": "RULE_NOT_ELIGIBLE: Payment marked non-eligible for recovery."
            }

        # Rule 2: Max attempts exceeded -> Mandatory Escalation
        if attempts >= 3:
            return {
                "allowed_action": "ESCALATE",
                "policy_approved": True,
                "rule_applied": "RULE_MAX_ATTEMPTS: Attempt threshold (3) exceeded; forcing manual escalation."
            }

        # Rule 3: Network timeouts -> Auto-retry allowed
        if reason in ["temporary_network_error", "timeout"]:
            return {
                "allowed_action": "RETRY_PAYMENT",
                "policy_approved": True,
                "rule_applied": "RULE_AUTO_RETRY: Transient technical error detected; safe for automatic retry."
            }

        # Rule 4: High amount OR insufficient funds -> Issue payment link (No forced retry)
        if amount > 10000 or reason in ["insufficient_funds", "limit_exceeded"]:
            return {
                "allowed_action": "SEND_PAYMENT_LINK",
                "policy_approved": True,
                "rule_applied": "RULE_PAYMENT_LINK: High value or liquidity failure; issue payment link instead of raw retry."
            }

        # Rule 5: Low recovery probability score from ML -> Stop action to save merchant fees
        if predicted_prob < 0.25:
            return {
                "allowed_action": "STOP",
                "policy_approved": True,
                "rule_applied": "RULE_LOW_PROBABILITY: Predicted recovery probability below 25%; stopping intervention."
            }

        # Default fallback rule
        return {
            "allowed_action": "SEND_REMINDER",
            "policy_approved": True,
            "rule_applied": "RULE_DEFAULT_REMINDER: Standard gentle recovery reminder."
        }