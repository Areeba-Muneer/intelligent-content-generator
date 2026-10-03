import os
from openai import OpenAI


def create_image_prompt(topic: str, generated_content: str, visual_style: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("TEXT_MODEL", "gpt-6-luna")

    prompt = f"""
Create a professional image-generation prompt from the information below.

Topic:
{topic}

Generated content:
{generated_content}

Visual style:
{visual_style}

Requirements:
- Represent the main idea visually.
- Match the requested visual style.
- Include useful details about subject, composition, lighting, environment,
  perspective, and mood where appropriate.
- Make it suitable for a professional website/social-media content asset.
- Avoid unnecessary words or typography inside the image.
- Return only the image prompt.
"""

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text.strip()
