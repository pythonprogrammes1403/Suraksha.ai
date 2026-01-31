"""
Validator Agent

Ensures transaction data is complete and safe
before entering the fraud detection pipeline.
"""

ALLOWED_QR_TYPES = {"PAY", "COLLECT"}


def validate_transaction(transaction: dict):
    required_fields = ["message", "amount", "avg_amount", "qr_type"]

    for field in required_fields:
        if field not in transaction:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(transaction["amount"], (int, float)):
        raise ValueError("Amount must be numeric")

    if transaction["amount"] <= 0:
        raise ValueError("Amount must be greater than zero")

    if transaction["avg_amount"] < 0:
        raise ValueError("Average amount cannot be negative")

    qr_type = transaction["qr_type"].upper()

    if qr_type not in ALLOWED_QR_TYPES:
        raise ValueError("QR type must be PAY or COLLECT")

    # Normalize values for downstream agents
    transaction["qr_type"] = qr_type
    transaction["message"] = transaction["message"].strip()

    return transaction
