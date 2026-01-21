"""Fraud detection subagent - checks claim history."""

import json
from pathlib import Path
from typing import Annotated

DB = Path(__file__).parent.parent / "db"


def check_history(claimant: Annotated[str, "Claimant name"]) -> str:
    """Check claimant's claim history and fraud indicators."""
    data = json.loads((DB / "claimants.json").read_text()) if (DB / "claimants.json").exists() else {}
    record = data.get(claimant)

    if not record:
        return "NEW CUSTOMER - No prior claims, fraud score: 0.0"

    score = record.get("fraud_score", 0)
    flags = record.get("risk_flags", [])
    prior = len(record.get("prior_claims", []))

    risk = "HIGH" if score > 0.4 else "LOW"
    return f"Fraud score: {score} ({risk} RISK), Prior claims: {prior}, Flags: {flags or 'None'}"


FRAUD_DETECTOR_SYSTEM_PROMPT = "Check fraud risk. Flag HIGH RISK if score > 0.4."
FRAUD_DETECTOR_TOOLS = [check_history]
