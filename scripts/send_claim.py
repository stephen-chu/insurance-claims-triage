"""Send a claim to the deployed triage agent."""

import json
import sys
from pathlib import Path

from langgraph_sdk import get_sync_client

# Your deployment URL
DEPLOYMENT_URL = "https://insurance-claims-agent-1d71606fdb2e59c4b10c2d85d0ca197c.us.langgraph.app"

DATA_DIR = Path(__file__).parent.parent / "data"


def load_claim(claim_id: str) -> dict:
    """Load a claim from the claims directory."""
    claim_path = DATA_DIR / claim_id / "claim.json"
    if not claim_path.exists():
        raise FileNotFoundError(f"Claim {claim_id} not found at {claim_path}")
    with open(claim_path) as f:
        return json.load(f)


def send_claim(claim_id: str):
    """Send a claim to the triage agent."""
    claim = load_claim(claim_id)

    client = get_sync_client(url=DEPLOYMENT_URL)

    # Create a thread and run
    thread = client.threads.create()

    run = client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="triage",
        input={
            "messages": [{
                "role": "user",
                "content": f"Process this claim: {json.dumps(claim)}"
            }]
        }
    )

    print(f"Sent claim {claim_id}")
    print(f"Thread ID: {thread['thread_id']}")
    print(f"Run ID: {run['run_id']}")
    return thread, run


def list_claims():
    """List available claims."""
    print("Available claims:")
    for claim_dir in sorted(DATA_DIR.iterdir()):
        if claim_dir.is_dir():
            claim_path = claim_dir / "claim.json"
            if claim_path.exists():
                with open(claim_path) as f:
                    claim = json.load(f)
                print(f"  {claim['claim_id']}: {claim['claim_type']} - {claim['claimant']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_claim.py <claim_id>")
        print("       python send_claim.py --list")
        print()
        list_claims()
        sys.exit(1)

    if sys.argv[1] == "--list":
        list_claims()
    else:
        send_claim(sys.argv[1])
