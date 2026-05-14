export type AiProvider = 'ollama' | 'arifos' | 'openrouter';

export interface AiModel {
  name: string;
  size: number;
  modified_at: string | null;
  digest: string | null;
}

export interface AiCitation {
  id: string;
  filename: string;
  score: number;
  snippet: string;
  content: string;
  chunk_index: number;
  doc_id: string | null;
  uploaded_at: string | null;
}

export interface AiMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface AiHealth {
  ok: boolean;
  upstreams: {
    ollama: string;
    arifos: string;
    qdrant: string;
  };
  defaults: {
    provider: AiProvider;
    chat_model: string;
    embed_model: string;
    rag_collection: string;
  };
}

export interface AiModelsResponse {
  ok: boolean;
  models: AiModel[];
  defaults: {
    provider: AiProvider;
    model: string;
  };
  providers: Array<{
    id: AiProvider;
    label: string;
  }>;
}

export interface RagUploadResponse {
  ok: boolean;
  document: {
    id: string;
    filename: string;
    mimeType: string;
    chunks: number;
    uploaded_at: string;
    collection: string;
  };
}

export interface RagQueryResponse {
  ok: boolean;
  query: string;
  citations: AiCitation[];
  collection: string;
}

export interface StreamAiChatOptions {
  provider: AiProvider;
  model: string;
  messages: AiMessage[];
  citations?: AiCitation[];
  onMeta?: (payload: { provider: AiProvider; model: string; citations: AiCitation[] }) => void;
  onChunk: (chunk: string) => void;
  onDone?: (payload: { content: string; citations: AiCitation[] }) => void;
}

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getAiHealth(): Promise<AiHealth> {
  const response = await fetch('/api/ai/health');
  return readJson<AiHealth>(response);
}

export async function getAiModels(): Promise<AiModelsResponse> {
  const response = await fetch('/api/ai/models');
  return readJson<AiModelsResponse>(response);
}

export async function uploadAiDocument(payload: {
  filename: string;
  content: string;
  mimeType: string;
}): Promise<RagUploadResponse> {
  const response = await fetch('/api/ai/rag/upload', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return readJson<RagUploadResponse>(response);
}

export async function queryAiDocuments(query: string, limit = 5): Promise<RagQueryResponse> {
  const response = await fetch('/api/ai/rag/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, limit }),
  });
  return readJson<RagQueryResponse>(response);
}

export async function streamAiChat(options: StreamAiChatOptions): Promise<void> {
  const response = await fetch('/api/ai/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      provider: options.provider,
      model: options.model,
      messages: options.messages,
      citations: options.citations ?? [],
    }),
  });

  if (!response.ok || !response.body) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const frames = buffer.split('\n\n');
    buffer = frames.pop() || '';

    for (const frame of frames) {
      const line = frame
        .split('\n')
        .find((entry) => entry.startsWith('data:'));

      if (!line) continue;
      const payload = JSON.parse(line.slice(5).trim()) as {
        type: 'meta' | 'chunk' | 'done' | 'error';
        provider?: AiProvider;
        model?: string;
        content?: string;
        error?: string;
        citations?: AiCitation[];
      };

      if (payload.type === 'error') {
        throw new Error(payload.error || 'AI stream failed');
      }

      if (payload.type === 'meta' && payload.provider && payload.model) {
        options.onMeta?.({
          provider: payload.provider,
          model: payload.model,
          citations: payload.citations ?? [],
        });
      }

      if (payload.type === 'chunk' && payload.content) {
        options.onChunk(payload.content);
      }

      if (payload.type === 'done') {
        options.onDone?.({
          content: payload.content ?? '',
          citations: payload.citations ?? [],
        });
      }
    }
  }
}
