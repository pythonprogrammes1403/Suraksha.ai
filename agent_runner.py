"""
Suraksha.AI Agent Orchestrator

Coordinates multiple fraud detection agents
to generate a real-time explainable risk score.
"""

import time

from fraud.fraud_logic import (
    detect_intent,
    is_amount_anomalous
)

from agents.validator import validate_transaction
from agents.qr_risk_agent import qr_risk_agent
from agents.decision_engine import decision_agent


def run_agents(transaction: dict):
    start_time = time.time()

    transaction = validate_transaction(transaction)

    message = transaction["message"]
    amount = transaction["amount"]
    avg_amount = transaction["avg_amount"]
    qr_text = transaction["qr_text"]

    intent = detect_intent(message)

    amount_anomaly = is_amount_anomalous(amount, avg_amount)

    qr_result = qr_risk_agent(qr_text=qr_text, intent=intent)
    qr_risk = qr_result["qr_risk"]

    risk_result = decision_agent(
        intent,
        amount_anomaly,
        qr_risk
    )

    latency_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "intent_detected": intent,
        "amount_anomaly": amount_anomaly,
        "qr_risk": qr_risk,
        "qr_type": qr_result["qr_type"],
        "latency_ms": latency_ms,
        **risk_result
    }
