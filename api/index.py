#!/usr/bin/env python3
"""
Shaya Sussman Content Generator - Vercel Serverless API

This is the main entry point for Vercel's serverless Python runtime.
"""

import os
import sys

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    allow_origins=[
        "*",
        "https://shaya-sussman-platform.manus.space",
        "https://shayasussman.com",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
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
    topic: str = Field(..., description="The topic to write about")
    format: ContentFormatEnum = Field(default=ContentFormatEnum.article)
    additional_context: Optional[str] = Field(default="")
    prompt_only: bool = Field(default=False)


class GenerateResponse(BaseModel):
    content: str
    format: str
    topic: str
    prompt_only: bool


class VoiceProfileResponse(BaseModel):
    name: str
    tone: str
    style_patterns: str
    themes: str
    influences: str
    hebrew_vocabulary: str
    transitions: str


class FormatInfo(BaseModel):
    name: str
    description: str
    instructions: str


class HealthResponse(BaseModel):
    status: str
    api_key_configured: bool


def get_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    return x_api_key or os.environ.get("ANTHROPIC_API_KEY")


@app.get("/")
async def root():
    return {
        "name": "Shaya Sussman Content Generator API",
        "version": "1.0.0",
        "description": "AI-powered content generator in Rabbi Shaya Sussman's voice",
        "docs": "/docs",
        "endpoints": {
            "generate": "POST /generate",
            "formats": "GET /formats",
            "voice_profile": "GET /voice-profile",
            "system_prompt": "GET /system-prompt",
            "health": "GET /health"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        api_key_configured=bool(os.environ.get("ANTHROPIC_API_KEY"))
    )


@app.get("/voice-profile", response_model=VoiceProfileResponse)
async def get_voice_profile():
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


@app.get("/formats")
async def list_formats():
    return [
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


@app.post("/generate", response_model=GenerateResponse)
async def generate_content(
    request: GenerateRequest,
    api_key: Optional[str] = Depends(get_api_key)
):
    format_type = ContentFormat(request.format.value)

    if request.prompt_only:
        content = generate_content_prompt_only(
            request.topic,
            format_type,
            request.additional_context
        )
    else:
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

        if content.startswith("Error:"):
            raise HTTPException(status_code=500, detail=content)

    return GenerateResponse(
        content=content,
        format=request.format.value,
        topic=request.topic,
        prompt_only=request.prompt_only
    )


@app.get("/system-prompt")
async def get_system_prompt_endpoint():
    voice = ShayaVoiceProfile()
    return {"system_prompt": get_system_prompt(voice)}
