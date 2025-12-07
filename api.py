#!/usr/bin/env python3
"""
Shaya Sussman Content Generator - REST API

FastAPI-based REST API for generating content in Rabbi Shaya Sussman's voice.
Can be deployed as a standalone service or integrated into larger platforms.

Usage:
    uvicorn api:app --reload --port 8000

Endpoints:
    POST /generate - Generate content
    GET /formats - List available formats
    GET /voice-profile - Get the voice profile
    GET /health - Health check
"""

import os
from typing import Optional
from enum import Enum
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import from our main module
from shaya_content_generator import (
    ContentFormat,
    ShayaVoiceProfile,
    get_system_prompt,
    get_format_instructions,
    generate_content_with_claude,
    generate_content_prompt_only
)

# Initialize FastAPI app
app = FastAPI(
    title="Shaya Sussman Content Generator API",
    description="""
    AI-powered content generator in Rabbi Shaya Sussman's distinctive voice.

    Blends Breslov wisdom, psychological insight, and practical spirituality
    to create authentic content in multiple formats.

    ## Features
    - **Articles/Essays**: Long-form inspirational pieces
    - **Social Media**: Engaging posts for Instagram, Twitter, etc.
    - **Class Outlines**: Nach Daily-style lesson plans
    - **Short Reflections**: Daily wisdom pieces

    ## Authentication
    Pass your Anthropic API key via the `X-API-Key` header, or configure
    a default key via the `ANTHROPIC_API_KEY` environment variable.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ContentFormatEnum(str, Enum):
    article = "article"
    social_media = "social_media"
    class_outline = "class_outline"
    short_reflection = "short_reflection"


class GenerateRequest(BaseModel):
    """Request body for content generation."""
    topic: str = Field(
        ...,
        description="The topic to write about",
        example="Finding inner peace during difficult times"
    )
    format: ContentFormatEnum = Field(
        default=ContentFormatEnum.article,
        description="The content format to generate"
    )
    additional_context: Optional[str] = Field(
        default="",
        description="Additional context or notes for the content",
        example="Target audience is young professionals"
    )
    prompt_only: bool = Field(
        default=False,
        description="If true, returns just the prompt instead of generated content"
    )


class GenerateResponse(BaseModel):
    """Response from content generation."""
    content: str = Field(..., description="The generated content or prompt")
    format: str = Field(..., description="The format that was used")
    topic: str = Field(..., description="The original topic")
    prompt_only: bool = Field(..., description="Whether this is a prompt or generated content")


class VoiceProfileResponse(BaseModel):
    """The voice profile characteristics."""
    name: str
    tone: str
    style_patterns: str
    themes: str
    influences: str
    hebrew_vocabulary: str
    transitions: str


class FormatInfo(BaseModel):
    """Information about a content format."""
    name: str
    description: str
    instructions: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    api_key_configured: bool


# Dependency for API key
def get_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    """Get API key from header or environment."""
    return x_api_key or os.environ.get("ANTHROPIC_API_KEY")


# Endpoints
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check API health and configuration status."""
    return HealthResponse(
        status="healthy",
        api_key_configured=bool(os.environ.get("ANTHROPIC_API_KEY"))
    )


@app.get("/voice-profile", response_model=VoiceProfileResponse, tags=["Voice"])
async def get_voice_profile():
    """Get the Shaya Sussman voice profile characteristics."""
    voice = ShayaVoiceProfile()
    return VoiceProfileResponse(
        name=voice.name,
        tone=voice.tone.strip(),
        style_patterns=voice.style_patterns.strip(),
        themes=voice.themes.strip(),
        influences=voice.influences.strip(),
        hebrew_vocabulary=voice.hebrew_vocabulary.strip(),
        transitions=voice.transitions.strip()
    )


@app.get("/formats", response_model=list[FormatInfo], tags=["Formats"])
async def list_formats():
    """List all available content formats with descriptions."""
    formats = [
        FormatInfo(
            name="article",
            description="Long-form article/essay (800-1200 words)",
            instructions=get_format_instructions(ContentFormat.ARTICLE).strip()
        ),
        FormatInfo(
            name="social_media",
            description="Social media post for Instagram, Twitter, etc.",
            instructions=get_format_instructions(ContentFormat.SOCIAL_MEDIA).strip()
        ),
        FormatInfo(
            name="class_outline",
            description="Nach Daily-style class/shiur outline",
            instructions=get_format_instructions(ContentFormat.CLASS_OUTLINE).strip()
        ),
        FormatInfo(
            name="short_reflection",
            description="Brief daily wisdom reflection (75-150 words)",
            instructions=get_format_instructions(ContentFormat.SHORT_REFLECTION).strip()
        ),
    ]
    return formats


@app.post("/generate", response_model=GenerateResponse, tags=["Generation"])
async def generate_content(
    request: GenerateRequest,
    api_key: Optional[str] = Depends(get_api_key)
):
    """
    Generate content in Rabbi Shaya Sussman's voice.

    Pass your Anthropic API key via the `X-API-Key` header.
    If no key is provided and `prompt_only` is false, the request will fail.
    """
    format_type = ContentFormat(request.format.value)

    if request.prompt_only:
        # Return just the prompt
        content = generate_content_prompt_only(
            request.topic,
            format_type,
            request.additional_context
        )
    else:
        # Generate with Claude
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="API key required. Pass via X-API-Key header or set ANTHROPIC_API_KEY environment variable."
            )

        content = generate_content_with_claude(
            request.topic,
            format_type,
            api_key,
            request.additional_context
        )

        # Check for errors from the generator
        if content.startswith("Error:"):
            raise HTTPException(status_code=500, detail=content)

    return GenerateResponse(
        content=content,
        format=request.format.value,
        topic=request.topic,
        prompt_only=request.prompt_only
    )


@app.get("/system-prompt", tags=["Voice"])
async def get_system_prompt_endpoint():
    """Get the full system prompt used for content generation."""
    voice = ShayaVoiceProfile()
    return {"system_prompt": get_system_prompt(voice)}


# For direct embedding in other Python apps
def create_app() -> FastAPI:
    """Factory function for creating the FastAPI app instance."""
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
