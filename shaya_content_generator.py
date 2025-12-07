#!/usr/bin/env python3
"""
Shaya Sussman Content Generator

A tool to generate content in the distinctive voice and style of Rabbi Shaya Sussman,
blending Breslov Hasidic wisdom, psychology, and practical spirituality.

Author: Built with Claude
"""

import argparse
import json
import os
import sys
from enum import Enum
from dataclasses import dataclass
from typing import Optional

try:
    import anthropic
except ImportError:
    anthropic = None


class ContentFormat(Enum):
    ARTICLE = "article"
    SOCIAL_MEDIA = "social_media"
    CLASS_OUTLINE = "class_outline"
    SHORT_REFLECTION = "short_reflection"


@dataclass
class ShayaVoiceProfile:
    """
    Captures the distinctive voice and style characteristics of Rabbi Shaya Sussman.
    Based on analysis of his published works on Breslov.org, Nach Daily, and other sources.
    """

    # Core characteristics
    name: str = "Rabbi Shaya Sussman"

    # Tone attributes
    tone: str = """
    - Warm, encouraging, and hopeful
    - Accessible yet spiritually grounded
    - Conversational without being casual
    - Direct and motivational ("YOU CAN HEAL!")
    - Compassionate and empathic
    - Balances authority with humility
    """

    # Writing style patterns
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

    # Thematic focus areas
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

    # Key influences to reference
    influences: str = """
    - Rebbe Nachman of Breslov (Likutey Moharan)
    - Rav Kook (Orot)
    - Humanistic and existential psychology (Rollo May, Irvin Yalom)
    - Brene Brown (vulnerability and imperfection)
    - P'nimiyus haTorah (inner dimension of Torah)
    """

    # Common Hebrew terms and their usage
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

    # Sentence starters and transitions commonly used
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
    """Generate the system prompt for AI content generation."""

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

Write as if you ARE Shaya Sussman, drawing from the same well of Breslov wisdom, psychological training, and genuine care for the reader's spiritual and emotional wellbeing. The content should feel like it naturally flows from someone who has deeply integrated Torah wisdom with therapeutic insight."""


def get_format_instructions(format_type: ContentFormat) -> str:
    """Get specific instructions for each content format."""

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
   - Use signature closing style ("Let us take the first step... And then let the journey begin")

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
    """Generate content using Claude API."""

    if anthropic is None:
        return "Error: anthropic package not installed. Run: pip install anthropic"

    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: No API key provided. Set ANTHROPIC_API_KEY environment variable or pass --api-key"

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
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        system=system_prompt
    )

    return message.content[0].text


def generate_content_prompt_only(
    topic: str,
    format_type: ContentFormat,
    additional_context: str = ""
) -> str:
    """Generate a complete prompt that can be used with any AI system."""

    voice = ShayaVoiceProfile()
    system_prompt = get_system_prompt(voice)
    format_instructions = get_format_instructions(format_type)

    full_prompt = f"""=== SYSTEM INSTRUCTIONS ===
{system_prompt}

=== FORMAT INSTRUCTIONS ===
{format_instructions}

=== USER REQUEST ===
Please write content on the following topic:

**Topic**: {topic}

{f"**Additional Context/Notes**: {additional_context}" if additional_context else ""}

Write this content now in the authentic voice of Rabbi Shaya Sussman."""

    return full_prompt


def interactive_mode():
    """Run the tool in interactive mode."""

    print("\n" + "="*60)
    print("  SHAYA SUSSMAN CONTENT GENERATOR")
    print("  Wisdom Through Words")
    print("="*60 + "\n")

    # Get topic
    print("What topic would you like to write about?")
    print("(Examples: 'Finding inner peace', 'Dealing with anxiety', 'The power of prayer')")
    topic = input("\nTopic: ").strip()

    if not topic:
        print("No topic provided. Exiting.")
        return

    # Get format
    print("\nChoose a content format:")
    print("  1. Article/Essay (long-form)")
    print("  2. Social Media Post")
    print("  3. Class Outline (Nach Daily style)")
    print("  4. Short Reflection")

    format_choice = input("\nChoice (1-4): ").strip()
    format_map = {
        "1": ContentFormat.ARTICLE,
        "2": ContentFormat.SOCIAL_MEDIA,
        "3": ContentFormat.CLASS_OUTLINE,
        "4": ContentFormat.SHORT_REFLECTION
    }
    format_type = format_map.get(format_choice, ContentFormat.ARTICLE)

    # Get additional context
    print("\nAny additional context or notes? (Press Enter to skip)")
    additional_context = input("Context: ").strip()

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    print("\n" + "-"*60)

    if api_key:
        print("Generating content with Claude...\n")
        result = generate_content_with_claude(topic, format_type, api_key, additional_context)
        print(result)
    else:
        print("No ANTHROPIC_API_KEY found. Generating prompt template...\n")
        result = generate_content_prompt_only(topic, format_type, additional_context)
        print(result)
        print("\n" + "-"*60)
        print("Copy the above prompt and use it with Claude or another AI assistant.")

    print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate content in the voice of Rabbi Shaya Sussman",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Finding inner peace through prayer"
  %(prog)s "Dealing with anxiety" --format social_media
  %(prog)s "The power of Tehillim" --format class_outline --context "For a beginner audience"
  %(prog)s --interactive
  %(prog)s --prompt-only "Resilience in hard times"
        """
    )

    parser.add_argument(
        "topic",
        nargs="?",
        help="The topic to write about"
    )

    parser.add_argument(
        "-f", "--format",
        choices=["article", "social_media", "class_outline", "short_reflection"],
        default="article",
        help="Content format (default: article)"
    )

    parser.add_argument(
        "-c", "--context",
        default="",
        help="Additional context or notes for the content"
    )

    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )

    parser.add_argument(
        "-p", "--prompt-only",
        action="store_true",
        help="Output the prompt template instead of generating content"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: print to stdout)"
    )

    parser.add_argument(
        "--show-voice-profile",
        action="store_true",
        help="Display the voice profile analysis"
    )

    args = parser.parse_args()

    # Show voice profile if requested
    if args.show_voice_profile:
        voice = ShayaVoiceProfile()
        print("\n=== SHAYA SUSSMAN VOICE PROFILE ===\n")
        print(f"Name: {voice.name}")
        print(f"\nTone:{voice.tone}")
        print(f"\nStyle Patterns:{voice.style_patterns}")
        print(f"\nThemes:{voice.themes}")
        print(f"\nInfluences:{voice.influences}")
        print(f"\nHebrew Vocabulary:{voice.hebrew_vocabulary}")
        print(f"\nCommon Transitions:{voice.transitions}")
        return

    # Interactive mode
    if args.interactive:
        interactive_mode()
        return

    # Require topic if not interactive
    if not args.topic:
        parser.print_help()
        print("\nError: Please provide a topic or use --interactive mode")
        sys.exit(1)

    format_type = ContentFormat(args.format)

    # Generate content
    if args.prompt_only:
        result = generate_content_prompt_only(args.topic, format_type, args.context)
    else:
        result = generate_content_with_claude(
            args.topic,
            format_type,
            args.api_key,
            args.context
        )

    # Output
    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Content written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
