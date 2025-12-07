# Shaya Sussman Content Generator

AI-powered content generator in Rabbi Shaya Sussman's distinctive voice — blending Breslov wisdom, psychological insight, and practical spirituality.

## Features

- **Voice Profile**: Based on analysis of Rabbi Shaya Sussman's published works on Breslov.org, Nach Daily, and other sources
- **Multiple Formats**: Articles, social media posts, class outlines, and short reflections
- **Flexible Integration**: CLI tool, REST API, or direct Python embedding
- **AI-Powered**: Uses Claude for intelligent content generation

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### CLI Usage

```bash
# Interactive mode
python shaya_content_generator.py --interactive

# Generate an article
python shaya_content_generator.py "Finding inner peace" --format article

# Generate a social media post
python shaya_content_generator.py "Dealing with anxiety" --format social_media

# Generate a class outline
python shaya_content_generator.py "The power of Tehillim" --format class_outline

# Get just the prompt (no API key needed)
python shaya_content_generator.py --prompt-only "Resilience in hard times"

# View the voice profile
python shaya_content_generator.py --show-voice-profile
```

### Environment Setup

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Live API

The API is deployed and available at:

**Production URL**: `https://shaya-content-api.onrender.com`

**Interactive Docs**: https://shaya-content-api.onrender.com/docs

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate` | POST | Generate content |
| `/formats` | GET | List available formats |
| `/voice-profile` | GET | Get voice profile |
| `/system-prompt` | GET | Get the full system prompt |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API documentation |

### Example API Request

```bash
# Generate a short reflection
curl -X POST "https://shaya-content-api.onrender.com/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Finding hope during difficult times",
    "format": "short_reflection"
  }'

# Generate a social media post
curl -X POST "https://shaya-content-api.onrender.com/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The power of gratitude",
    "format": "social_media"
  }'
```

### JavaScript/React Integration

```javascript
// Using the provided client SDK
import ShayaContentClient from './client/shaya-content-client';

const client = new ShayaContentClient('https://shaya-content-api.onrender.com');

// Generate content
const article = await client.generateArticle('Finding inner peace');
const socialPost = await client.generateSocialPost('Daily wisdom');
const classOutline = await client.generateClassOutline('The power of Tehillim');
const reflection = await client.generateReflection('Gratitude');
```

### React Hook Usage

```javascript
import { useShayaContent } from './client/shaya-content-client';

function ContentGenerator() {
  const { generate, isLoading, error, content } = useShayaContent({
    baseUrl: 'https://shaya-content-api.onrender.com'
  });

  const handleGenerate = async () => {
    await generate('Finding hope', 'article');
  };

  return (
    <div>
      <button onClick={handleGenerate} disabled={isLoading}>
        {isLoading ? 'Generating...' : 'Generate'}
      </button>
      {content && <pre>{content}</pre>}
    </div>
  );
}
```

## Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t shaya-content-generator .

# Run with API key
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your-key shaya-content-generator
```

### Docker Compose

```bash
# Set your API key in .env file
echo "ANTHROPIC_API_KEY=your-key" > .env

# Start the service
docker-compose up -d
```

## Python Embedding

Use the generator directly in your Python applications:

```python
from shaya_content_generator import (
    ContentFormat,
    ShayaVoiceProfile,
    generate_content_with_claude,
    generate_content_prompt_only,
    get_system_prompt
)

# Generate content directly
content = generate_content_with_claude(
    topic="Finding inner peace",
    format_type=ContentFormat.ARTICLE,
    api_key="your-api-key",
    additional_context="For young professionals"
)

# Or get just the prompt to use with any AI
prompt = generate_content_prompt_only(
    topic="Dealing with anxiety",
    format_type=ContentFormat.SOCIAL_MEDIA
)

# Access the voice profile
voice = ShayaVoiceProfile()
system_prompt = get_system_prompt(voice)
```

## Content Formats

### 1. Article/Essay
Long-form content (800-1200 words) with:
- Opening hook with Rebbe Nachman teaching
- Biblical/textual foundation
- Core teaching with rhetorical questions
- Psychological application
- Encouraging conclusion

### 2. Social Media
Short-form posts with:
- Compelling hook
- Core wisdom (2-4 sentences)
- Personal application
- Call to action
- Relevant hashtags

### 3. Class Outline
Nach Daily-style lesson plans with:
- Introduction and context
- Main teaching points
- Key quotes
- Psychological insights
- Discussion questions

### 4. Short Reflection
Brief daily wisdom (75-150 words):
- Opening thought
- Brief expansion
- Closing encouragement

## Voice Profile

The generator captures Rabbi Shaya Sussman's distinctive voice:

**Tone**
- Warm, encouraging, and hopeful
- Accessible yet spiritually grounded
- Conversational without being casual
- Compassionate and empathic

**Style Patterns**
- Rhetorical questions for engagement
- Biblical narratives as illustrations
- Contrasts (Yaakov vs. Esav, darkness vs. light)
- Blend of Hebrew terminology with plain English

**Key Influences**
- Rebbe Nachman of Breslov (Likutey Moharan)
- Rav Kook (Orot)
- Humanistic psychology (Rollo May, Irvin Yalom)
- Brene Brown (vulnerability and imperfection)

## Deployment

### Current Production (Render)

The API is currently deployed on Render at `https://shaya-content-api.onrender.com`

To deploy your own instance:

1. Fork this repository
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Set environment variable: `ANTHROPIC_API_KEY`
5. Render will auto-detect settings from `render.yaml`

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Run the server
uvicorn api:app --reload --port 8000
```

## Integration with Shaya Sussman Platforms

This API is designed to integrate with:
- **shayasussman.com** - Website content generation
- **Nach Daily** - Class content and summaries
- **Social media automation** - Scheduled posts
- **Email newsletters** - Weekly wisdom content

## License

MIT License - See LICENSE file for details.

## Credits

Built with Claude by Schulman Coaching.

Voice profile based on analysis of Rabbi Shaya Sussman's published works:
- [Breslov.org](https://breslov.org/author/shaya/)
- [Nach Daily](https://nachdaily.com/)
- [Mosaica Press](https://mosaicapress.com/blog/rabbi-shaya-sussman/)
