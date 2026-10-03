from pydantic import BaseModel, Field


class ContentRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500)
    tone: str = Field(default="Professional")
    content_length: str = Field(default="Medium")
    visual_style: str = Field(default="Realistic")


class ContentResponse(BaseModel):
    success: bool
    stage: str
    text: str | None = None
    image_prompt: str | None = None
    image_url: str | None = None
    message: str | None = None
