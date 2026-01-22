"""LangGraph Cloud entry point."""

from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI

from tools import TOOLS
from subagents.damage_assessor import DAMAGE_ASSESSOR_SYSTEM_PROMPT, DAMAGE_ASSESSOR_TOOLS
from subagents.fraud_detector import FRAUD_DETECTOR_SYSTEM_PROMPT, FRAUD_DETECTOR_TOOLS
from subagents.policy_verifier import POLICY_VERIFIER_SYSTEM_PROMPT, POLICY_VERIFIER_TOOLS

SYSTEM_PROMPT = """You are an insurance claims triage agent. You receive a claim and must analyze it.

1. Call ALL THREE subagents in ONE response (parallel execution):
   - damage-assessor: ALL photo URLs as a list, damage_type
   - fraud-detector: claimant name
   - policy-verifier: policy_id, claim_type
2. Call submit_decision with claim_id and your decision:
   - AUTO-APPROVE: Low risk, covered, reasonable amount
   - DENY: Not covered or policy issue
   - MANUAL REVIEW: High fraud risk or edge cases"""


# Create the graph for LangGraph Cloud
graph = create_deep_agent(
    model=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    system_prompt=SYSTEM_PROMPT,
    tools=TOOLS,
    subagents=[
        {"name": "damage-assessor", "description": "Analyze damage photos - needs list of photo URLs, damage_type", "system_prompt": DAMAGE_ASSESSOR_SYSTEM_PROMPT, "tools": DAMAGE_ASSESSOR_TOOLS, "model": "gpt-4o-mini"},
        {"name": "fraud-detector", "description": "Check fraud risk - needs claimant name", "system_prompt": FRAUD_DETECTOR_SYSTEM_PROMPT, "tools": FRAUD_DETECTOR_TOOLS, "model": "gpt-4o-mini"},
        {"name": "policy-verifier", "description": "Verify coverage - needs policy_id and claim_type", "system_prompt": POLICY_VERIFIER_SYSTEM_PROMPT, "tools": POLICY_VERIFIER_TOOLS, "model": "gpt-4o-mini"},
    ],
    interrupt_on={
        "submit_decision": {
            "allowed_decisions": ["approve", "edit", "reject"],
            "description": lambda name, args: f"**Claim {args.get('claim_id')}**: {args.get('decision')}\n\nCoverage: {args.get('coverage')}\nFraud Risk: {args.get('fraud_risk')}\nDamage: ${args.get('damage_estimate')}\n\n{args.get('reason')}"
        }
    },
)
