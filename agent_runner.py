"""
Suraksha.AI Agent Orchestrator

Coordinates multiple fraud detection agents
to generate a real-time explainable risk score.
"""

import time

from core.fraud_logic import (
    detect_intent,
    is_amount_anomalous,
    is_qr_risky
)


from agents.validator import validate_transaction
from agents.decision_engine import behavioral_risk_engine


def run_agents(transaction: dict):
    start_time = time.time()

    # ✅ Step 1 — Validate
    transaction = validate_transaction(transaction)

    message = transaction["message"]
    amount = transaction["amount"]
    avg_amount = transaction["avg_amount"]
    qr_type = transaction["qr_type"]

    # ✅ Step 2 — Intent Agent
    intent = detect_intent(message)

    # ✅ Step 3 — Behavioral Agent
    amount_anomaly = is_amount_anomalous(
        amount,
        avg_amount
    )

    # ✅ Step 4 — QR Agent
    qr_risk = is_qr_risky(
        intent,
        qr_type
    )

    # ✅ Step 5 — Decision Engine
    risk_result = behavioral_risk_engine(
        intent,
        amount_anomaly,
        qr_risk
    )

    latency_ms = round((time.time() - start_time) * 1000, 2)

    # Final explainable output
    return {
        "intent_detected": intent,
        "amount_anomaly": amount_anomaly,
        "qr_risk": qr_risk,
        "latency_ms": latency_ms,
        **risk_result
    }
