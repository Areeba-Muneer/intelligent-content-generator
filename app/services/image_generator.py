import base64
import os
import uuid
from pathlib import Path

from openai import OpenAI


IMAGE_FOLDER = Path("generated_images")


def generate_image(image_prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("IMAGE_MODEL", "gpt-image-2")

    IMAGE_FOLDER.mkdir(parents=True, exist_ok=True)

    result = client.images.generate(
        model=model,
        prompt=image_prompt,
        size="1024x1024",
    )

    image_data = result.data[0].b64_json
    if not image_data:
        raise RuntimeError("Image API did not return image data.")

    filename = f"{uuid.uuid4().hex}.png"
    filepath = IMAGE_FOLDER / filename

    filepath.write_bytes(base64.b64decode(image_data))

    return f"/generated_images/{filename}"
