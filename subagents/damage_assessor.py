"""Damage assessment subagent - analyzes photos using vision."""

import base64
from pathlib import Path
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

CLAIMS = Path(__file__).parent.parent / "claims"


def analyze_photo(
    claim_id: Annotated[str, "Claim ID"],
    filename: Annotated[str, "Photo filename"],
    damage_type: Annotated[str, "Type of damage"],
) -> str:
    """Analyze damage photo. Returns severity and cost estimate."""
    path = CLAIMS / claim_id / filename
    if not path.exists():
        return f"Photo not found: {filename}"

    b64 = base64.b64encode(path.read_bytes()).decode()
    media = "image/png" if path.suffix == ".png" else "image/jpeg"

    response = ChatOpenAI(model="gpt-4o-mini", temperature=0).invoke([
        HumanMessage(content=[
            {"type": "text", "text": f"{damage_type} damage. Reply: Severity (Low/Moderate/Severe), Cost estimate USD. Be brief."},
            {"type": "image_url", "image_url": {"url": f"data:{media};base64,{b64}"}}
        ])
    ])
    return response.content


DAMAGE_ASSESSOR_SYSTEM_PROMPT = "Analyze photos with analyze_photo. Return total cost estimate."
DAMAGE_ASSESSOR_TOOLS = [analyze_photo]
