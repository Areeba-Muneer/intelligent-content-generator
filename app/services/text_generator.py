import os
from openai import OpenAI


def generate_text(topic: str, tone: str, content_length: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("TEXT_MODEL", "gpt-6-luna")

    length_instructions = {
        "Short": "Write approximately 80-120 words.",
        "Medium": "Write approximately 180-250 words.",
        "Long": "Write approximately 350-500 words.",
    }

    instruction = length_instructions.get(
        content_length,
        length_instructions["Medium"],
    )

    prompt = f"""
You are a professional content writer.

Create high-quality content about:
Topic: {topic}
Tone: {tone}
Requested length: {content_length}

Requirements:
- {instruction}
- Stay focused on the topic.
- Use clear, useful, natural language.
- Do not mention that you are an AI.
- Do not add meta commentary.
- Return only the final content.
"""

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text.strip()
