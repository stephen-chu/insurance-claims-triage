"""Generate realistic damage photos using OpenAI's image generation."""

import base64
from pathlib import Path
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var
CLAIMS = Path(__file__).parent / "claims"

IMAGES = [
    ("CLM-2024-001", "damage_front.png",
     "Photograph for auto insurance claim: front view of a silver sedan with collision damage. "
     "Crumpled front bumper, dented hood, cracked headlight. Realistic photo, daylight, parking lot setting."),

    ("CLM-2024-001", "damage_side.png",
     "Photograph for auto insurance claim: side view of a silver sedan with collision damage to "
     "front fender and door. Dented metal, scratched paint, visible crease. Realistic photo, daylight."),

    ("CLM-2024-002", "ceiling_damage.png",
     "Photograph for home insurance claim: residential ceiling with water damage from burst pipe. "
     "Brown water stains, sagging wet drywall, peeling paint. Realistic interior photo."),

    ("CLM-2024-002", "wall_damage.png",
     "Photograph for home insurance claim: interior wall with water damage. Water stains, bubbling "
     "paint, discoloration near floor. White wall with visible moisture damage. Realistic photo."),

    ("CLM-2024-002", "pipe_damage.png",
     "Photograph for home insurance claim: burst copper water pipe in basement. Corroded pipe with "
     "visible split/crack, water residue. Realistic close-up photo of plumbing failure."),
]

if __name__ == "__main__":
    for claim_id, filename, prompt in IMAGES:
        print(f"Generating {claim_id}/{filename}...")

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="high"
        )

        image_data = base64.b64decode(response.data[0].b64_json)
        path = CLAIMS / claim_id / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(image_data)
        print(f"  Saved: {path}")

    print("\nDone! Generated 5 realistic damage photos.")
