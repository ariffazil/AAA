/**
 * A2A Client for AAA Gateway
 * 
 * Implements A2A client capabilities for delegating to external agents.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

export interface A2AClientOptions {
  baseUrl: string;
  auth?: {
    type: 'none' | 'bearer' | 'apiKey' | 'oauth2';
    token?: string;
    headerName?: string;
  };
}

export interface SendMessageOptions {
  taskId?: string;
  contextId?: string;
  blocking?: boolean;
  acceptedOutputModes?: string[];
  pushNotificationConfig?: {
    url: string;
    token: string;
  };
}

export interface A2ATask {
  id: string;
  contextId: string;
  status: {
    state: TaskState;
    message?: {
      role: 'user' | 'agent';
      parts: Array<{ kind: string; text?: string; data?: unknown }>;
      messageId: string;
    };
    timestamp: string;
  };
  artifacts: Array<{
    artifactId: string;
    name: string;
    parts: Array<{ kind: string; text?: string }>;
  }>;
  history: Array<{
    role: 'user' | 'agent';
    parts: Array<{ kind: string; text?: string }>;
    messageId: string;
  }>;
  kind: 'task';
  metadata: Record<string, unknown>;
}

type TaskState = 
  | 'submitted' 
  | 'working' 
  | 'input-required' 
  | 'completed' 
  | 'failed' 
  | 'canceled' 
  | 'rejected' 
  | 'auth-required' 
  | 'unknown';

export interface StreamingResponse {
  taskId: string;
  contextId: string;
  event: {
    kind: 'task' | 'status-update' | 'artifact-update';
    taskId?: string;
    status?: { state: TaskState; message?: unknown; timestamp: string };
    artifact?: unknown;
    append?: boolean;
    lastChunk?: boolean;
    final?: boolean;
  };
}

export class A2AClient {
  private baseUrl: string;
  private authHeader?: string;

  constructor(options: A2AClientOptions) {
    this.baseUrl = options.baseUrl.replace(/\/$/, '');
    
    if (options.auth?.token) {
      if (options.auth.type === 'bearer') {
        this.authHeader = `Bearer ${options.auth.token}`;
      } else if (options.auth.type === 'apiKey') {
        const headerName = options.auth.headerName || 'X-API-Key';
        this.authHeader = `${headerName}: ${options.auth.token}`;
      }
    }
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (this.authHeader) {
      if (this.authHeader.includes(':')) {
        const [name, value] = this.authHeader.split(': ');
        headers[name] = value;
      } else {
        headers['Authorization'] = this.authHeader;
      }
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`A2A request failed: ${response.status} ${error}`);
    }

    return response.json();
  }

  async sendMessage(
    message: {
      role: 'user' | 'agent';
      parts: Array<{ kind: 'text'; text: string }>;
      messageId: string;
    },
    options?: SendMessageOptions
  ): Promise<A2ATask> {
    const id = crypto.randomUUID();
    
    const response = await this.request<{ jsonrpc: string; id: unknown; result: A2ATask }>(
      'POST',
      '/message/send',
      {
        jsonrpc: '2.0',
        id,
        method: 'message/send',
        params: {
          message,
          taskId: options?.taskId,
          contextId: options?.contextId,
          configuration: {
            blocking: options?.blocking ?? true,
            acceptedOutputModes: options?.acceptedOutputModes,
            pushNotificationConfig: options?.pushNotificationConfig,
          },
        },
      }
    );

    return response.result;
  }

  async sendMessageStream(
    message: {
      role: 'user' | 'agent';
      parts: Array<{ kind: 'text'; text: string }>;
      messageId: string;
    },
    options?: SendMessageOptions
  ): Promise<AsyncGenerator<StreamingResponse>> {
    const id = crypto.randomUUID();
    
    const response = await fetch(`${this.baseUrl}/message/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(this.authHeader ? {
          'Authorization': this.authHeader.includes('Bearer') ? this.authHeader : undefined,
        } : {}),
        ...(this.authHeader?.includes(':') ? {
          [this.authHeader.split(': ')[0]]: this.authHeader.split(': ')[1]
        } : {}),
      } as Record<string, string>,
      body: JSON.stringify({
        jsonrpc: '2.0',
        id,
        method: 'message/stream',
        params: {
          message,
          taskId: options?.taskId,
          contextId: options?.contextId,
          configuration: {
            blocking: false,
            acceptedOutputModes: options?.acceptedOutputModes,
          },
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`A2A stream request failed: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    async function* generate(): AsyncGenerator<StreamingResponse> {
      let currentReader = reader;
      
      while (true) {
        const { done, value } = await currentReader.read();
        
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.result) {
                yield {
                  taskId: data.result.taskId || '',
                  contextId: data.result.contextId || '',
                  event: data.result,
                };
                
                if (data.result.final || data.result.kind === 'status-update' && data.result.status?.state === 'completed') {
                  return;
                }
              }
            } catch {
              // Skip invalid JSON
            }
          }
        }
      }
    }

    return generate();
  }

  async getTask(taskId: string): Promise<A2ATask | null> {
    try {
      const response = await this.request<{ jsonrpc: string; id: unknown; result: A2ATask }>(
        'GET',
        `/tasks/${taskId}`
      );
      return response.result;
    } catch {
      return null;
    }
  }

  async cancelTask(taskId: string): Promise<boolean> {
    try {
      await this.request(
        'POST',
        `/tasks/${taskId}/cancel`,
        { jsonrpc: '2.0', id: 1, method: 'tasks/cancel', params: {} }
      );
      return true;
    } catch {
      return false;
    }
  }

  async subscribeToTask(
    taskId: string,
    callback: (event: StreamingResponse['event']) => void
  ): Promise<() => void> {
    const response = await fetch(`${this.baseUrl}/tasks/${taskId}/subscribe`, {
      headers: {
        'Accept': 'text/event-stream',
        ...(this.authHeader?.includes('Bearer') ? {
          'Authorization': this.authHeader
        } : {}),
      } as Record<string, string>,
    });

    if (!response.ok) {
      throw new Error(`Subscribe request failed: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    const cancel = () => reader.cancel();

    (async () => {
      try {
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) break;
          
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.result) {
                  callback(data.result);
                  
                  if (data.result.final) {
                    return;
                  }
                }
              } catch {
                // Skip invalid JSON
              }
            }
          }
        }
      } catch {
        // Stream closed
      }
    })();

    return cancel;
  }
}

// Factory function
export function createA2AClient(baseUrl: string, auth?: A2AClientOptions['auth']): A2AClient {
  return new A2AClient({ baseUrl, auth });
}

// Pre-configured clients for common agents
export const PRESET_AGENTS = {
  GEOX: {
    name: 'GEOX Specialist',
    url: process.env.GEOX_A2A_URL || 'http://localhost:3002',
    auth: { type: 'bearer' as const, token: process.env.GEOX_A2A_TOKEN },
  },
  WEALTH: {
    name: 'WEALTH Analyst',
    url: process.env.WEALTH_A2A_URL || 'http://localhost:3003',
    auth: { type: 'bearer' as const, token: process.env.WEALTH_A2A_TOKEN },
  },
  PLANNER: {
    name: 'Planner Agent',
    url: process.env.PLANNER_A2A_URL || 'http://localhost:3004',
    auth: { type: 'bearer' as const, token: process.env.PLANNER_A2A_TOKEN },
  },
} as const;

export type PresetAgent = keyof typeof PRESET_AGENTS;

export async function dispatchToAgent(
  agent: PresetAgent,
  message: string
): Promise<A2ATask> {
  const config = PRESET_AGENTS[agent];
  const client = createA2AClient(config.url, config.auth as A2AClientOptions['auth']);
  
  return client.sendMessage({
    role: 'user',
    parts: [{ kind: 'text', text: message }],
    messageId: crypto.randomUUID(),
  });
}

export async function dispatchWithStreaming(
  agent: PresetAgent,
  message: string,
  onEvent: (event: StreamingResponse['event']) => void
): Promise<void> {
  const config = PRESET_AGENTS[agent];
  const client = createA2AClient(config.url, config.auth as A2AClientOptions['auth']);
  
  const stream = await client.sendMessageStream({
    role: 'user',
    parts: [{ kind: 'text', text: message }],
    messageId: crypto.randomUUID(),
  });
  
  for await (const response of stream) {
    onEvent(response.event);
  }
}