"""Insurance Claims Triage Agent."""

from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from tools import TOOLS
from subagents.damage_assessor import DAMAGE_ASSESSOR_SYSTEM_PROMPT, DAMAGE_ASSESSOR_TOOLS
from subagents.fraud_detector import FRAUD_DETECTOR_SYSTEM_PROMPT, FRAUD_DETECTOR_TOOLS
from subagents.policy_verifier import POLICY_VERIFIER_SYSTEM_PROMPT, POLICY_VERIFIER_TOOLS

SYSTEM_PROMPT = """Insurance claims triage agent.

1. Use write_todos to plan your steps
2. Delegate to subagents in parallel:
   - damage-assessor: Pass claim_id, each photo filename, and damage type
   - fraud-detector: Pass claimant name
   - policy-verifier: Pass policy_id and claim_type
3. Call submit_decision with your final decision:
   - AUTO-APPROVE: Low risk, covered, reasonable amount
   - DENY: Not covered or policy issue
   - MANUAL REVIEW: High fraud risk or edge cases needing human judgment"""


def create_triage_agent():
    return create_deep_agent(
        model=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        system_prompt=SYSTEM_PROMPT,
        tools=TOOLS,
        subagents=[
            {"name": "damage-assessor", "description": "Analyze damage photos - needs claim_id, photo filenames, damage type", "system_prompt": DAMAGE_ASSESSOR_SYSTEM_PROMPT, "tools": DAMAGE_ASSESSOR_TOOLS, "model": "gpt-4o-mini"},
            {"name": "fraud-detector", "description": "Check fraud risk - needs claimant name", "system_prompt": FRAUD_DETECTOR_SYSTEM_PROMPT, "tools": FRAUD_DETECTOR_TOOLS, "model": "gpt-4o-mini"},
            {"name": "policy-verifier", "description": "Verify coverage - needs policy_id and claim_type", "system_prompt": POLICY_VERIFIER_SYSTEM_PROMPT, "tools": POLICY_VERIFIER_TOOLS, "model": "gpt-4o-mini"},
        ],
        interrupt_on={
            "submit_decision": True,  # Interrupt on all decisions for human review
        },
        checkpointer=MemorySaver(),
    )
