"""Policy verification subagent - validates coverage."""

import json
from pathlib import Path
from typing import Annotated

DB = Path(__file__).parent.parent / "db"


def verify_coverage(
    policy_id: Annotated[str, "Policy ID"],
    claim_type: Annotated[str, "Type of claim"],
) -> str:
    """Check if policy covers the claim type."""
    data = json.loads((DB / "policies.json").read_text()) if (DB / "policies.json").exists() else {}
    policy = data.get(policy_id)

    if not policy:
        return f"POLICY NOT FOUND: {policy_id}"

    if policy.get("status") != "ACTIVE":
        return f"POLICY INACTIVE: {policy_id}"

    covered = any(claim_type.lower() in c.lower() for c in policy.get("coverage", []))

    if covered:
        return f"COVERED - {claim_type} is covered. Deductible: ${policy.get('deductible')}, Max: ${policy.get('max_coverage')}"
    else:
        return f"NOT COVERED - {claim_type} not in policy. Coverage: {policy.get('coverage')}"


POLICY_VERIFIER_SYSTEM_PROMPT = "Verify policy coverage for the claim type."
POLICY_VERIFIER_TOOLS = [verify_coverage]
