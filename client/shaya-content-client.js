/**
 * Shaya Sussman Content Generator - JavaScript Client
 *
 * A client library for integrating with the Shaya Sussman Content Generator API.
 *
 * Usage:
 *   import ShayaContentClient from './shaya-content-client';
 *
 *   const client = new ShayaContentClient('https://your-api-url.vercel.app');
 *   const article = await client.generate('Finding inner peace', 'article');
 */

class ShayaContentClient {
  constructor(baseUrl, apiKey = null) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
    this.apiKey = apiKey;
  }

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  /**
   * Get API information
   */
  async getInfo() {
    return this.request('/');
  }

  /**
   * Check API health
   */
  async health() {
    return this.request('/health');
  }

  /**
   * Get the voice profile
   */
  async getVoiceProfile() {
    return this.request('/voice-profile');
  }

  /**
   * Get available content formats
   */
  async getFormats() {
    return this.request('/formats');
  }

  /**
   * Get the system prompt used for generation
   */
  async getSystemPrompt() {
    return this.request('/system-prompt');
  }

  /**
   * Generate content in Shaya Sussman's voice
   *
   * @param {string} topic - The topic to write about
   * @param {string} format - One of: 'article', 'social_media', 'class_outline', 'short_reflection'
   * @param {string} additionalContext - Optional additional context
   * @param {boolean} promptOnly - If true, returns just the prompt without generating
   * @returns {Promise<{content: string, format: string, topic: string, prompt_only: boolean}>}
   */
  async generate(topic, format = 'article', additionalContext = '', promptOnly = false) {
    return this.request('/generate', {
      method: 'POST',
      body: JSON.stringify({
        topic,
        format,
        additional_context: additionalContext,
        prompt_only: promptOnly,
      }),
    });
  }

  /**
   * Generate an article
   */
  async generateArticle(topic, context = '') {
    const response = await this.generate(topic, 'article', context);
    return response.content;
  }

  /**
   * Generate a social media post
   */
  async generateSocialPost(topic, context = '') {
    const response = await this.generate(topic, 'social_media', context);
    return response.content;
  }

  /**
   * Generate a class outline
   */
  async generateClassOutline(topic, context = '') {
    const response = await this.generate(topic, 'class_outline', context);
    return response.content;
  }

  /**
   * Generate a short reflection
   */
  async generateReflection(topic, context = '') {
    const response = await this.generate(topic, 'short_reflection', context);
    return response.content;
  }

  /**
   * Get just the prompt (no API key needed)
   */
  async getPrompt(topic, format = 'article', context = '') {
    const response = await this.generate(topic, format, context, true);
    return response.content;
  }
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ShayaContentClient;
  module.exports.default = ShayaContentClient;
}

export default ShayaContentClient;
