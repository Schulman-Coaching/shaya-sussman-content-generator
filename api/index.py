#!/usr/bin/env python3
"""
Shaya Sussman Content Generator - Vercel Serverless API

Self-contained FastAPI application for Vercel deployment.
"""

import os
from typing import Optional
from enum import Enum
from dataclasses import dataclass
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    import anthropic
except ImportError:
    anthropic = None


# ============== Voice Profile ==============

class ContentFormat(Enum):
    ARTICLE = "article"
    SOCIAL_MEDIA = "social_media"
    CLASS_OUTLINE = "class_outline"
    SHORT_REFLECTION = "short_reflection"


@dataclass
class ShayaVoiceProfile:
    name: str = "Rabbi Shaya Sussman"
    tone: str = """
    - Warm, encouraging, and hopeful
    - Accessible yet spiritually grounded
    - Conversational without being casual
    - Direct and motivational ("YOU CAN HEAL!")
    - Compassionate and empathic
    - Balances authority with humility
    """
    style_patterns: str = """
    - Uses rhetorical questions to drive engagement ("What was the source of Yaakov's wisdom?")
    - Employs biblical narratives as illustrations for abstract concepts
    - Creates contrasts to structure arguments (Yaakov vs. Esav, darkness vs. light)
    - Uses repetition to emphasize core messages
    - Conversational closings that invite reader participation
    - Blends Hebrew terminology naturally with plain English
    - Uses metaphors like "vessel," "permeates," "embodiments," "springboard"
    - Short, punchy sentences mixed with flowing explanatory passages
    """
    themes: str = """
    - Inner wisdom as divine inheritance
    - Finding light that emerges from darkness
    - Self-awareness over external seeking
    - Emotional healing through faith and wisdom
    - Transformation of suffering into growth
    - The birthright of consciousness and wisdom
    - Practical spirituality for modern struggles
    - Resilience, hope, and the power of change
    - Mental health integration with Torah wisdom
    """
    influences: str = """
    - Rebbe Nachman of Breslov (Likutey Moharan)
    - Rav Kook (Orot)
    - Humanistic and existential psychology (Rollo May, Irvin Yalom)
    - Brene Brown (vulnerability and imperfection)
    - P'nimiyus haTorah (inner dimension of Torah)
    """
    hebrew_vocabulary: str = """
    - Sekhel (wisdom/intelligence) - often "inner sekhel" or "Godly wisdom"
    - Hisbodedus (personal prayer/meditation)
    - Teshuva (return/repentance)
    - Tehillim (Psalms)
    - Emunah (faith)
    - Simcha (joy/happiness)
    - Navi/Nach (Prophets)
    - P'nimiyus (inner dimension)
    """
    transitions: str = """
    - "Rebbe Nachman teaches..."
    - "Here's the profound truth..."
    - "What does this mean for us?"
    - "This should be a great source of encouragement..."
    - "Not only... more importantly..."
    - "Let us take the first step..."
    - "And then let the journey begin..."
    - "The ramifications of this..."
    """


def get_system_prompt(voice: ShayaVoiceProfile) -> str:
    return f"""You are a content writer who writes in the exact voice and style of {voice.name}.

## VOICE PROFILE

### Tone
{voice.tone}

### Writing Style Patterns
{voice.style_patterns}

### Core Themes
{voice.themes}

### Key Influences to Draw From
{voice.influences}

### Hebrew Vocabulary (use naturally, with translations where helpful)
{voice.hebrew_vocabulary}

### Common Transitions and Phrases
{voice.transitions}

## CRITICAL STYLE GUIDELINES

1. ALWAYS blend psychological insight with Torah wisdom - this is the hallmark of Shaya's approach
2. Use rhetorical questions to engage readers and drive the narrative forward
3. Reference Rebbe Nachman's teachings (especially Likutey Moharan) as the primary source
4. Include practical, actionable takeaways - not just abstract philosophy
5. Write with warmth and hope - even when discussing difficult topics like suffering
6. Use biblical figures (Yaakov, Esav, etc.) as illustrations for psychological concepts
7. End with an encouraging call to action or reflection
8. Balance Hebrew terms with English explanations - don't over-saturate
9. Keep the tone accessible to both religious and secular readers interested in wisdom

## CONTENT AUTHENTICITY

Write as if you ARE Shaya Sussman, drawing from the same well of Breslov wisdom, psychological training, and genuine care for the reader's spiritual and emotional wellbeing."""


def get_format_instructions(format_type: ContentFormat) -> str:
    instructions = {
        ContentFormat.ARTICLE: """
## FORMAT: Long-Form Article/Essay

Structure your article as follows:

1. **Opening Hook** (1-2 paragraphs)
   - Start with a teaching from Rebbe Nachman or a compelling question
   - Connect to a universal human experience or struggle

2. **Biblical/Textual Foundation** (2-3 paragraphs)
   - Introduce the Torah source or Breslov teaching
   - Explain the context and key Hebrew terms
   - Use a biblical narrative as illustration

3. **Core Teaching** (3-4 paragraphs)
   - Unpack the deeper meaning
   - Use rhetorical questions to engage
   - Create contrasts (e.g., Yaakov vs. Esav approach)

4. **Personal/Psychological Application** (2-3 paragraphs)
   - Bridge to modern life and emotional struggles
   - Reference psychological concepts naturally
   - Make it practical and relatable

5. **Encouraging Conclusion** (1-2 paragraphs)
   - End with hope and empowerment
   - Include a call to reflection or action
   - Use signature closing style

Target length: 800-1200 words
""",
        ContentFormat.SOCIAL_MEDIA: """
## FORMAT: Social Media Post

Create an engaging social media post with:

1. **Hook** (first line) - Compelling question or bold statement
2. **Core Wisdom** (2-4 sentences) - The teaching or insight
3. **Personal Application** (1-2 sentences) - How this applies to the reader
4. **Call to Action/Reflection** - Question or encouragement

Style notes:
- Use line breaks for readability
- Can include relevant emojis sparingly (optional)
- Include 3-5 relevant hashtags at the end
- Keep under 280 characters for Twitter or up to 500 for Instagram

Example hashtags: #Breslov #InnerWisdom #Torah #Healing #JewishWisdom #RebbNachman #Emunah
""",
        ContentFormat.CLASS_OUTLINE: """
## FORMAT: Class/Shiur Outline (Nach Daily Style)

Structure your class outline as follows:

**Title**: [Topic] | [Source Reference]

**Introduction** (2-3 bullet points)
- Context for the teaching
- Why this matters today
- Key question being addressed

**Main Teaching Points** (4-6 bullet points)
- Clear, concise summaries
- Hebrew terms with translations
- Each point builds on the previous

**Key Quotes**
- 1-2 direct quotes from the source text
- Include Hebrew if relevant with translation

**Psychological/Practical Insights** (2-3 bullet points)
- How this applies to emotional/mental wellbeing
- Modern life applications

**Discussion Questions** (2-3 questions)
- Open-ended questions for reflection
- Connect ancient wisdom to personal experience

**Summary/Takeaway**
- One powerful sentence capturing the essence
""",
        ContentFormat.SHORT_REFLECTION: """
## FORMAT: Short Reflection/Daily Wisdom

Create a brief, powerful reflection:

1. **Opening Thought** (1-2 sentences)
   - A teaching or insight from Breslov wisdom

2. **Expansion** (2-3 sentences)
   - Brief explanation or elaboration
   - Can include a short example

3. **Closing Encouragement** (1 sentence)
   - Hopeful, empowering conclusion

Total length: 75-150 words
Tone: Contemplative, warm, accessible
"""
    }
    return instructions.get(format_type, instructions[ContentFormat.ARTICLE])


def generate_content_with_claude(
    topic: str,
    format_type: ContentFormat,
    api_key: Optional[str] = None,
    additional_context: str = ""
) -> str:
    if anthropic is None:
        return "Error: anthropic package not installed"

    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: No API key provided"

    client = anthropic.Anthropic(api_key=api_key)
    voice = ShayaVoiceProfile()
    system_prompt = get_system_prompt(voice)
    format_instructions = get_format_instructions(format_type)

    user_prompt = f"""Please write content on the following topic:

**Topic**: {topic}

{format_instructions}

{f"**Additional Context/Notes**: {additional_context}" if additional_context else ""}

Write this content now in the authentic voice of Rabbi Shaya Sussman."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": user_prompt}],
        system=system_prompt
    )
    return message.content[0].text


def generate_content_prompt_only(
    topic: str,
    format_type: ContentFormat,
    additional_context: str = ""
) -> str:
    voice = ShayaVoiceProfile()
    system_prompt = get_system_prompt(voice)
    format_instructions = get_format_instructions(format_type)

    return f"""=== SYSTEM INSTRUCTIONS ===
{system_prompt}

=== FORMAT INSTRUCTIONS ===
{format_instructions}

=== USER REQUEST ===
Please write content on the following topic:

**Topic**: {topic}

{f"**Additional Context/Notes**: {additional_context}" if additional_context else ""}

Write this content now in the authentic voice of Rabbi Shaya Sussman."""


# ============== FastAPI App ==============

app = FastAPI(
    title="Shaya Sussman Content Generator API",
    description="AI-powered content generator in Rabbi Shaya Sussman's distinctive voice.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
async def get_voice_profile_endpoint():
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
        FormatInfo(name="article", description="Long-form article/essay (800-1200 words)"),
        FormatInfo(name="social_media", description="Social media post for Instagram, Twitter, etc."),
        FormatInfo(name="class_outline", description="Nach Daily-style class/shiur outline"),
        FormatInfo(name="short_reflection", description="Brief daily wisdom reflection (75-150 words)"),
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
            request.additional_context or ""
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
            request.additional_context or ""
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
