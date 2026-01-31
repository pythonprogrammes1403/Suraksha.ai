#Below is used to detect intent of payment
def detect_intent(message: str) -> str:
    message = message.lower()

    if any(word in message for word in ["refund", "return", "send back", "reverse"]):
        return "REFUND"

    if any(word in message for word in ["kyc", "verify", "update kyc"]):
        return "KYC"

    if any(word in message for word in ["urgent", "immediately", "now", "fast"]):
        return "URGENT"

    return "NORMAL"

#Below is used to detect if the payment amount looks right or not
def is_amount_anomalous(amount: float, avg_amount: float) -> bool:
    if avg_amount <= 0:
        return False

    return amount > 5 * avg_amount

#Below is used to detect if the QR code is risky or not
def is_qr_risky(intent: str, qr_type: str) -> bool:
    if intent == "REFUND" and qr_type == "PAY":
        return True
    return False

#Below computes the risk score based on  certain criterias
def compute_risk(intent: str, amount_anomaly: bool, qr_risk: bool):
    score = 0
    reasons = []
    flags = []

    if intent == "REFUND":
        score += 2
        flags.append("REFUND_SCAM")
        reasons.append("Refund-related request detected")

    if intent == "KYC":
        score += 3
        flags.append("KYC_SCAM")
        reasons.append("Possible KYC scam attempt")

    if intent == "URGENT":
        score += 1
        flags.append("URGENT_LANGUAGE")
        reasons.append("Urgent language used to pressure payment")

    if amount_anomaly:
        score += 2
        flags.append("AMOUNT_ANOMALY")
        reasons.append("Amount is unusually high for this vendor")

    if qr_risk:
        score += 3
        flags.append("QR_MISMATCH")
        reasons.append("QR code may trigger unintended payment")

    if score >= 5:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return level, score, flags, reasons


#Below prints all the above info, finally telling the vendor if its dangerous or not
def analyze_transaction(
    message: str,
    amount: float,
    avg_amount: float,
    qr_type: str
):
    # Basic input validation
    if not message or amount <= 0:
        return {
            "intent": "UNKNOWN",
            "risk_level": "LOW",
            "risk_score": 0,
            "flags": [],
            "reasons": ["Insufficient transaction data"]
        }

    intent = detect_intent(message)
    amount_anomaly = is_amount_anomalous(amount, avg_amount)
    qr_risk = is_qr_risky(intent, qr_type)

    risk_level, risk_score, flags, reasons = compute_risk(
        intent, amount_anomaly, qr_risk
    )

    return {
        "intent": intent,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "flags": flags,
        "reasons": reasons
    }





