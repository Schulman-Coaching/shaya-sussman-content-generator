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

## REST API

### Start the API Server

```bash
# Install API dependencies
pip install fastapi uvicorn

# Run the server
uvicorn api:app --reload --port 8000
```

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
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-anthropic-api-key" \
  -d '{
    "topic": "Finding hope during difficult times",
    "format": "article",
    "additional_context": "For young professionals"
  }'
```

### JavaScript/React Integration

```javascript
// From your React app
const generateContent = async (topic, format = 'article') => {
  const response = await fetch('https://your-api-url/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': process.env.ANTHROPIC_API_KEY,
    },
    body: JSON.stringify({
      topic,
      format,
      additional_context: '',
    }),
  });

  const data = await response.json();
  return data.content;
};

// Usage
const article = await generateContent('Finding inner peace', 'article');
const socialPost = await generateContent('Daily wisdom', 'social_media');
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

## Deployment Options

### 1. Vercel/Railway/Render
Deploy the FastAPI app to any Python-compatible platform:

```bash
# Procfile for Heroku/Render
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

### 2. AWS Lambda
Use Mangum for serverless deployment:

```python
from mangum import Mangum
from api import app

handler = Mangum(app)
```

### 3. Google Cloud Run
```bash
gcloud run deploy shaya-content-api \
  --source . \
  --set-env-vars ANTHROPIC_API_KEY=your-key
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
