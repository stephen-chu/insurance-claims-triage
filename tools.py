"""Tools for the insurance claims triage agent."""

from typing import Annotated, Literal


def submit_decision(
    claim_id: Annotated[str, "The claim ID this decision is for"],
    decision: Annotated[Literal["AUTO-APPROVE", "DENY", "MANUAL REVIEW"], "The triage decision"],
    coverage: Annotated[str, "Coverage status (yes/no)"],
    fraud_risk: Annotated[str, "Fraud risk level (low/high)"],
    damage_estimate: Annotated[int, "Estimated damage in dollars"],
    reason: Annotated[str, "One sentence explanation"],
) -> str:
    """Submit the final triage decision for human review."""
    return f"Decision submitted for {claim_id}: {decision} - {reason}"


TOOLS = [submit_decision]
