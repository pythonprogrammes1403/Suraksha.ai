"""
Decision Engine

Aggregates signals from detection agents
to compute an explainable fraud risk score.
"""

from core.fraud_logic import compute_risk


def behavioral_risk_engine(intent, amount_anomaly, qr_risk):
    """
    Central risk scoring engine.
    """

    risk_level, risk_score, flags, reasons = compute_risk(
        intent,
        amount_anomaly,
        qr_risk
    )

    # Hackathon WOW feature
    fraud_probability = round(min(risk_score / 10, 1.0) * 100, 2)

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "fraud_probability": fraud_probability,  # percentage
        "flags": flags,
        "reasons": reasons
    }
