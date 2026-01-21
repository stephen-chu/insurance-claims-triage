"""Reset claims for testing - clears results so claims get reprocessed."""

import json
from pathlib import Path

ROOT = Path(__file__).parent
CLAIMS = ROOT / "claims"
RESULTS = ROOT / "results"

SAMPLE_CLAIMS = [
    {
        "claim_id": "CLM-2024-001",
        "claimant": "Sarah Johnson",
        "policy_id": "POL-89234",
        "incident_date": "2024-01-15",
        "claim_type": "Auto Collision",
        "description": "Front-end collision at intersection. Other driver ran red light.",
        "estimated_damage": 4500,
        "attachments": [
            {"filename": "damage_front.png", "type": "photo"},
            {"filename": "damage_side.png", "type": "photo"}
        ]
    },
    {
        "claim_id": "CLM-2024-002",
        "claimant": "Mike Chen",
        "policy_id": "POL-76543",
        "incident_date": "2024-01-18",
        "claim_type": "Water Damage",
        "description": "Burst pipe in basement caused flooding.",
        "estimated_damage": 8200,
        "attachments": [
            {"filename": "ceiling_damage.png", "type": "photo"},
            {"filename": "wall_damage.png", "type": "photo"},
            {"filename": "pipe_damage.png", "type": "photo"}
        ]
    },
    {
        "claim_id": "CLM-2024-003",
        "claimant": "Emily Rodriguez",
        "policy_id": "POL-12345",
        "incident_date": "2024-01-20",
        "claim_type": "Theft",
        "description": "Laptop and electronics stolen from vehicle.",
        "estimated_damage": 2100,
        "attachments": []
    },
]

if __name__ == "__main__":
    # Clear results
    for f in RESULTS.glob("*.json"):
        f.unlink()
        print(f"Removed: {f.name}")

    # Write claim.json files
    for claim in SAMPLE_CLAIMS:
        claim_dir = CLAIMS / claim["claim_id"]
        claim_dir.mkdir(parents=True, exist_ok=True)
        (claim_dir / "claim.json").write_text(json.dumps(claim, indent=2))
        print(f"Created: {claim['claim_id']}/claim.json")

    print(f"\nReady: {len(SAMPLE_CLAIMS)} claims in {CLAIMS}")
