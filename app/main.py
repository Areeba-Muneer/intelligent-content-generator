import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models.schemas import ContentRequest
from app.services.text_generator import generate_text
from app.services.validator import validate_content
from app.services.image_prompt import create_image_prompt
from app.services.image_generator import generate_image


load_dotenv()

app = FastAPI(
    title="Intelligent AI Content Generator",
    version="1.0.0",
    description="Generates AI text and a matching AI image through a modular pipeline.",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount(
    "/generated_images",
    StaticFiles(directory="generated_images"),
    name="generated_images",
)


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "openai_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "text_model": os.getenv("TEXT_MODEL", "gpt-6-luna"),
        "image_model": os.getenv("IMAGE_MODEL", "gpt-image-2"),
    }


@app.get("/config")
async def config():
    # Safe diagnostics: never return the API key itself.
    return {
        "openai_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "text_model": os.getenv("TEXT_MODEL", "gpt-6-luna"),
        "image_model": os.getenv("IMAGE_MODEL", "gpt-image-2"),
    }


@app.post("/generate")
async def generate_content(request: ContentRequest):
    topic = request.topic.strip()

    if not topic:
        return {
            "success": False,
            "stage": "input",
            "message": "Please enter a topic.",
        }

    if not os.getenv("OPENAI_API_KEY"):
        return {
            "success": False,
            "stage": "configuration",
            "message": "OPENAI_API_KEY is not configured. Add it to your .env file.",
        }

    # 1. Text Generation
    try:
        text = generate_text(
            topic,
            request.tone,
            request.content_length,
        )
    except Exception as exc:
        print("Text generation error:", repr(exc))
        return {
            "success": False,
            "stage": "text_generation",
            "message": (
                "Text generation failed. "
                f"Check your API key, billing/access, and TEXT_MODEL setting. "
                f"Server error: {type(exc).__name__}: {exc}"
            ),
        }

    # 2. Validation
    valid, validation_message = validate_content(
        text,
        topic,
        request.content_length,
    )

    if not valid:
        return {
            "success": False,
            "stage": "validation",
            "text": text,
            "message": validation_message,
        }

    # 3. Image Prompt
    try:
        image_prompt = create_image_prompt(
            topic,
            text,
            request.visual_style,
        )
    except Exception as exc:
        print("Image prompt error:", repr(exc))
        return {
            "success": False,
            "stage": "image_prompt",
            "text": text,
            "message": (
                "Image prompt creation failed. "
                f"Server error: {type(exc).__name__}: {exc}"
            ),
        }

    # 4. Image Generation
    try:
        image_url = generate_image(image_prompt)
    except Exception as exc:
        print("Image generation error:", repr(exc))
        return {
            "success": False,
            "stage": "image_generation",
            "text": text,
            "image_prompt": image_prompt,
            "message": (
                "Image generation failed. "
                f"Check IMAGE_MODEL and image-generation access. "
                f"Server error: {type(exc).__name__}: {exc}"
            ),
        }

    # 5. Final Output
    return {
        "success": True,
        "stage": "completed",
        "text": text,
        "image_prompt": image_prompt,
        "image_url": image_url,
        "message": "Content generated successfully.",
    }
