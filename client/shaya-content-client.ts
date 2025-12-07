/**
 * Shaya Sussman Content Generator - React/TypeScript Client
 *
 * A client library for integrating with the Shaya Sussman Content Generator API.
 *
 * Usage:
 *   import { ShayaContentClient, useShayaContent } from './shaya-content-client';
 *
 *   // Direct client usage
 *   const client = new ShayaContentClient('https://your-api-url.vercel.app');
 *   const article = await client.generate('Finding inner peace', 'article');
 *
 *   // React hook usage
 *   const { generate, isLoading, error } = useShayaContent();
 *   const content = await generate('Finding inner peace', 'article');
 */

// Types
export type ContentFormat = 'article' | 'social_media' | 'class_outline' | 'short_reflection';

export interface GenerateRequest {
  topic: string;
  format?: ContentFormat;
  additional_context?: string;
  prompt_only?: boolean;
}

export interface GenerateResponse {
  content: string;
  format: string;
  topic: string;
  prompt_only: boolean;
}

export interface VoiceProfile {
  name: string;
  tone: string;
  style_patterns: string;
  themes: string;
  influences: string;
  hebrew_vocabulary: string;
  transitions: string;
}

export interface FormatInfo {
  name: string;
  description: string;
  instructions: string;
}

export interface HealthStatus {
  status: string;
  api_key_configured: boolean;
}

export interface ApiInfo {
  name: string;
  version: string;
  description: string;
  docs: string;
  endpoints: Record<string, string>;
}

// Client Class
export class ShayaContentClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(baseUrl: string, apiKey?: string) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
    this.apiKey = apiKey;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
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
  async getInfo(): Promise<ApiInfo> {
    return this.request<ApiInfo>('/');
  }

  /**
   * Check API health
   */
  async health(): Promise<HealthStatus> {
    return this.request<HealthStatus>('/health');
  }

  /**
   * Get the voice profile
   */
  async getVoiceProfile(): Promise<VoiceProfile> {
    return this.request<VoiceProfile>('/voice-profile');
  }

  /**
   * Get available content formats
   */
  async getFormats(): Promise<FormatInfo[]> {
    return this.request<FormatInfo[]>('/formats');
  }

  /**
   * Get the system prompt used for generation
   */
  async getSystemPrompt(): Promise<{ system_prompt: string }> {
    return this.request<{ system_prompt: string }>('/system-prompt');
  }

  /**
   * Generate content in Shaya Sussman's voice
   */
  async generate(
    topic: string,
    format: ContentFormat = 'article',
    additionalContext?: string,
    promptOnly: boolean = false
  ): Promise<GenerateResponse> {
    return this.request<GenerateResponse>('/generate', {
      method: 'POST',
      body: JSON.stringify({
        topic,
        format,
        additional_context: additionalContext || '',
        prompt_only: promptOnly,
      }),
    });
  }

  /**
   * Generate an article
   */
  async generateArticle(topic: string, context?: string): Promise<string> {
    const response = await this.generate(topic, 'article', context);
    return response.content;
  }

  /**
   * Generate a social media post
   */
  async generateSocialPost(topic: string, context?: string): Promise<string> {
    const response = await this.generate(topic, 'social_media', context);
    return response.content;
  }

  /**
   * Generate a class outline
   */
  async generateClassOutline(topic: string, context?: string): Promise<string> {
    const response = await this.generate(topic, 'class_outline', context);
    return response.content;
  }

  /**
   * Generate a short reflection
   */
  async generateReflection(topic: string, context?: string): Promise<string> {
    const response = await this.generate(topic, 'short_reflection', context);
    return response.content;
  }

  /**
   * Get just the prompt (no API key needed)
   */
  async getPrompt(
    topic: string,
    format: ContentFormat = 'article',
    context?: string
  ): Promise<string> {
    const response = await this.generate(topic, format, context, true);
    return response.content;
  }
}

// React Hook (for use in React applications)
import { useState, useCallback } from 'react';

export interface UseShayaContentOptions {
  baseUrl: string;
  apiKey?: string;
}

export interface UseShayaContentReturn {
  generate: (
    topic: string,
    format?: ContentFormat,
    additionalContext?: string
  ) => Promise<GenerateResponse>;
  generateArticle: (topic: string, context?: string) => Promise<string>;
  generateSocialPost: (topic: string, context?: string) => Promise<string>;
  generateClassOutline: (topic: string, context?: string) => Promise<string>;
  generateReflection: (topic: string, context?: string) => Promise<string>;
  getPrompt: (topic: string, format?: ContentFormat, context?: string) => Promise<string>;
  getVoiceProfile: () => Promise<VoiceProfile>;
  getFormats: () => Promise<FormatInfo[]>;
  isLoading: boolean;
  error: Error | null;
  content: string | null;
  clearError: () => void;
  clearContent: () => void;
}

export function useShayaContent(options: UseShayaContentOptions): UseShayaContentReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [content, setContent] = useState<string | null>(null);

  const client = new ShayaContentClient(options.baseUrl, options.apiKey);

  const wrapAsync = useCallback(
    <T>(fn: () => Promise<T>) =>
      async (): Promise<T> => {
        setIsLoading(true);
        setError(null);
        try {
          const result = await fn();
          return result;
        } catch (err) {
          const error = err instanceof Error ? err : new Error(String(err));
          setError(error);
          throw error;
        } finally {
          setIsLoading(false);
        }
      },
    []
  );

  const generate = useCallback(
    async (
      topic: string,
      format: ContentFormat = 'article',
      additionalContext?: string
    ): Promise<GenerateResponse> => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await client.generate(topic, format, additionalContext);
        setContent(response.content);
        return response;
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        setError(error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [client]
  );

  const generateArticle = useCallback(
    async (topic: string, context?: string): Promise<string> => {
      const response = await generate(topic, 'article', context);
      return response.content;
    },
    [generate]
  );

  const generateSocialPost = useCallback(
    async (topic: string, context?: string): Promise<string> => {
      const response = await generate(topic, 'social_media', context);
      return response.content;
    },
    [generate]
  );

  const generateClassOutline = useCallback(
    async (topic: string, context?: string): Promise<string> => {
      const response = await generate(topic, 'class_outline', context);
      return response.content;
    },
    [generate]
  );

  const generateReflection = useCallback(
    async (topic: string, context?: string): Promise<string> => {
      const response = await generate(topic, 'short_reflection', context);
      return response.content;
    },
    [generate]
  );

  const getPrompt = useCallback(
    async (
      topic: string,
      format: ContentFormat = 'article',
      context?: string
    ): Promise<string> => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await client.generate(topic, format, context, true);
        setContent(response.content);
        return response.content;
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err));
        setError(error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [client]
  );

  const getVoiceProfile = useCallback(async (): Promise<VoiceProfile> => {
    setIsLoading(true);
    setError(null);
    try {
      return await client.getVoiceProfile();
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [client]);

  const getFormats = useCallback(async (): Promise<FormatInfo[]> => {
    setIsLoading(true);
    setError(null);
    try {
      return await client.getFormats();
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      setError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [client]);

  const clearError = useCallback(() => setError(null), []);
  const clearContent = useCallback(() => setContent(null), []);

  return {
    generate,
    generateArticle,
    generateSocialPost,
    generateClassOutline,
    generateReflection,
    getPrompt,
    getVoiceProfile,
    getFormats,
    isLoading,
    error,
    content,
    clearError,
    clearContent,
  };
}

// Default export for convenience
export default ShayaContentClient;
