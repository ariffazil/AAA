export interface TaskMessage {
  role: 'user' | 'agent';
  parts: Part[];
  messageId: string;
  taskId?: string;
  contextId?: string;
}

export type Part = 
  | { kind: 'text'; text: string }
  | { kind: 'file'; file: { name?: string; mimeType: string; bytes?: string; uri?: string } }
  | { kind: 'data'; data: Record<string, unknown> };

export interface Task {
  id: string;
  contextId: string;
  status: {
    state: TaskState;
    message?: TaskMessage;
    timestamp: string;
  };
  artifacts: Artifact[];
  history: TaskMessage[];
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export type TaskState = 
  | 'submitted' 
  | 'working' 
  | 'input-required' 
  | 'completed' 
  | 'failed' 
  | 'canceled' 
  | 'rejected' 
  | 'auth-required' 
  | 'unknown';

export interface Artifact {
  artifactId: string;
  name: string;
  parts: Part[];
}

export interface MessageSendParams {
  message: TaskMessage;
  taskId?: string;
  contextId?: string;
  configuration?: {
    blocking?: boolean;
    acceptedOutputModes?: string[];
    pushNotificationConfig?: PushNotificationConfig;
  };
  metadata?: Record<string, unknown>;
}

export interface PushNotificationConfig {
  url: string;
  token: string;
  authentication?: { schemes: string[] };
}

export interface JSONRPCRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params: Record<string, unknown>;
}

export interface JSONRPCResponse {
  jsonrpc: '2.0';
  id: string | number;
  result?: unknown;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
}

export const ERROR_CODES = {
  PARSE_ERROR: -32700,
  INVALID_REQUEST: -32600,
  METHOD_NOT_FOUND: -32601,
  INVALID_PARAMS: -32602,
  INTERNAL_ERROR: -32603,
  TASK_NOT_FOUND: -32001,
  TASK_NOT_CANCELABLE: -32002,
  PUSH_NOTIFICATION_NOT_SUPPORTED: -32003,
  UNSUPPORTED_OPERATION: -32004,
  CONTENT_TYPE_NOT_SUPPORTED: -32005,
  INVALID_AGENT_RESPONSE: -32006,
  AUTHENTICATED_EXTENDED_CARD_NOT_CONFIGURED: -32007,
};
