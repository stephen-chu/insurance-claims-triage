"""Damage assessment subagent - analyzes photos using vision."""

from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def analyze_photos(
    photo_urls: Annotated[list[str], "List of photo URLs"],
    damage_type: Annotated[str, "Type of damage"],
) -> str:
    """Analyze damage photos from URLs. Returns severity and cost estimate."""
    if not photo_urls:
        return "No photos provided"

    content = [{"type": "text", "text": f"{damage_type} damage photos. For each image: severity (Low/Moderate/Severe), cost estimate USD. Then total estimate. Be brief."}]

    for url in photo_urls:
        content.append({"type": "image_url", "image_url": {"url": url, "detail": "low"}})

    response = ChatOpenAI(model="gpt-4o-mini", temperature=0, timeout=60).invoke([HumanMessage(content=content)])
    return response.content


DAMAGE_ASSESSOR_SYSTEM_PROMPT = "Analyze photos with analyze_photos (pass all URLs). Return total cost estimate."
DAMAGE_ASSESSOR_TOOLS = [analyze_photos]
