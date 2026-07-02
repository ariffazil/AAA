/**
 * A2A Protocol v1.0.0 — Official Schema Types
 * ══════════════════════════════════════════════
 * Aligned to: https://a2a-protocol.org/latest/specification/
 * Migration: 2026-07-02 by FORGE (000Ω)
 *
 * BREAKING CHANGES from previous schema:
 * - Task states now use TASK_STATE_* prefix
 * - Parts use direct fields (text/raw/url/data) instead of kind discriminator
 * - Added tasks/list, push notification config, extended agent card
 */

// ── Task States (Section 4.1.3) ────────────────────────────────────────
export type TaskState =
  | 'TASK_STATE_SUBMITTED'
  | 'TASK_STATE_WORKING'
  | 'TASK_STATE_INPUT_REQUIRED'
  | 'TASK_STATE_COMPLETED'
  | 'TASK_STATE_CANCELED'
  | 'TASK_STATE_FAILED'
  | 'TASK_STATE_REJECTED';

// Backward-compatible aliases (Phase 1 dual-mode)
export type LegacyTaskState =
  | 'submitted'
  | 'working'
  | 'input-required'
  | 'completed'
  | 'failed'
  | 'canceled'
  | 'rejected'
  | 'auth-required'
  | 'unknown';

// State normalization map
export const TASK_STATE_MAP: Record<LegacyTaskState, TaskState> = {
  'submitted': 'TASK_STATE_SUBMITTED',
  'working': 'TASK_STATE_WORKING',
  'input-required': 'TASK_STATE_INPUT_REQUIRED',
  'completed': 'TASK_STATE_COMPLETED',
  'failed': 'TASK_STATE_FAILED',
  'canceled': 'TASK_STATE_CANCELED',
  'rejected': 'TASK_STATE_REJECTED',
  'auth-required': 'TASK_STATE_INPUT_REQUIRED', // closest match
  'unknown': 'TASK_STATE_SUBMITTED',
};

export function normalizeTaskState(state: string): TaskState {
  if (state.startsWith('TASK_STATE_')) return state as TaskState;
  return TASK_STATE_MAP[state as LegacyTaskState] || 'TASK_STATE_SUBMITTED';
}

// ── Parts (Section 4.1.6) ─────────────────────────────────────────────
// Official: Part has oneof content field (text, raw, url, data)
// Plus optional: mediaType, filename, metadata

export interface TextPart {
  text: string;
  mediaType?: string;  // default: 'text/plain'
  filename?: string;
  metadata?: Record<string, unknown>;
}

export interface RawPart {
  raw: string;         // base64-encoded bytes
  mediaType: string;   // required for raw
  filename?: string;
  metadata?: Record<string, unknown>;
}

export interface UrlPart {
  url: string;
  mediaType?: string;
  filename?: string;
  metadata?: Record<string, unknown>;
}

export interface DataPart {
  data: unknown;       // structured JSON
  mediaType?: string;  // default: 'application/json'
  filename?: string;
  metadata?: Record<string, unknown>;
}

export type Part = TextPart | RawPart | UrlPart | DataPart;

// Type guards
export function isTextPart(part: Part): part is TextPart {
  return 'text' in part;
}
export function isRawPart(part: Part): part is RawPart {
  return 'raw' in part;
}
export function isUrlPart(part: Part): part is UrlPart {
  return 'url' in part;
}
export function isDataPart(part: Part): part is DataPart {
  return 'data' in part;
}

// ── Legacy Part (backward compat, Phase 1) ────────────────────────────
export interface LegacyPart {
  kind: 'text' | 'file' | 'data';
  text?: string;
  file?: { name?: string; mimeType: string; bytes?: string; uri?: string };
  data?: Record<string, unknown>;
}

export function normalizePart(legacy: LegacyPart): Part {
  switch (legacy.kind) {
    case 'text':
      return { text: legacy.text || '', mediaType: 'text/plain' };
    case 'file':
      if (legacy.file?.bytes) {
        return { raw: legacy.file.bytes, mediaType: legacy.file.mimeType, filename: legacy.file.name };
      }
      if (legacy.file?.uri) {
        return { url: legacy.file.uri, mediaType: legacy.file.mimeType, filename: legacy.file.name };
      }
      return { text: '', mediaType: 'text/plain' };
    case 'data':
      return { data: legacy.data || {}, mediaType: 'application/json' };
    default:
      return { text: JSON.stringify(legacy), mediaType: 'application/json' };
  }
}

// ── Role (Section 4.1.5) ──────────────────────────────────────────────
export type Role = 'user' | 'agent';

// ── Message (Section 4.1.4) ───────────────────────────────────────────
export interface Message {
  role: Role;
  parts: Part[];
  messageId: string;
  contextId?: string;
  taskId?: string;
  referenceTaskIds?: string[];  // for multi-turn refinement
  metadata?: Record<string, unknown>;
  extensions?: Record<string, unknown>;
}

// Legacy message type (backward compat)
export interface TaskMessage {
  role: 'user' | 'agent';
  parts: Part[];  // Updated to use official Part type
  messageId: string;
  taskId?: string;
  contextId?: string;
  referenceTaskIds?: string[];
  metadata?: Record<string, unknown>;
}

// ── TaskStatus (Section 4.1.2) ────────────────────────────────────────
export interface TaskStatus {
  state: TaskState;
  message?: Message;
  timestamp: string;
}

// ── Artifact (Section 4.1.7) ──────────────────────────────────────────
export interface Artifact {
  artifactId: string;
  name: string;
  description?: string;
  parts: Part[];
  metadata?: Record<string, unknown>;
  extensions?: Record<string, unknown>;
}

// ── Task (Section 4.1.1) ──────────────────────────────────────────────
export interface Task {
  id: string;
  contextId: string;
  status: TaskStatus;
  artifacts: Artifact[];
  history?: Message[];
  metadata?: Record<string, unknown>;
  extensions?: Record<string, unknown>;
  created_at?: string;
  updated_at?: string;
}

// ── Streaming Events (Section 4.2) ────────────────────────────────────
export interface TaskStatusUpdateEvent {
  taskId: string;
  contextId: string;
  status: TaskStatus;
  final: boolean;
  metadata?: Record<string, unknown>;
}

export interface TaskArtifactUpdateEvent {
  taskId: string;
  contextId: string;
  artifact: Artifact;
  append?: boolean;
  lastChunk?: boolean;
  metadata?: Record<string, unknown>;
}

export type StreamEvent = TaskStatusUpdateEvent | TaskArtifactUpdateEvent;

// ── Push Notifications (Section 4.3) ──────────────────────────────────
export interface PushNotificationConfig {
  url: string;
  token?: string;
  authentication?: {
    schemes: string[];
    credentials?: string;
  };
}

export interface TaskPushNotificationConfig {
  taskId: string;
  configId: string;
  pushNotificationConfig: PushNotificationConfig;
}

// ── Agent Card (Section 4.4) ──────────────────────────────────────────
export interface AgentProvider {
  organization: string;
  url?: string;
}

export interface AgentCapabilities {
  streaming?: boolean;
  pushNotifications?: boolean;
  stateTransitionHistory?: boolean;
  extensions?: Record<string, unknown>;
}

export interface AgentSkill {
  id: string;
  name: string;
  description: string;
  tags?: string[];
  inputModes?: string[];
  outputModes?: string[];
  examples?: string[];
}

export interface SecurityScheme {
  type: 'http' | 'apiKey' | 'oauth2' | 'openIdConnect' | 'mutualTLS';
  scheme?: string;        // for http type
  bearerFormat?: string;  // for http bearer
  in?: string;            // for apiKey
  name?: string;          // for apiKey header/query param name
  description?: string;
}

export interface AgentExtension {
  uri: string;
  description?: string;
  data?: unknown;
}

export interface AgentCard {
  name: string;
  description: string;
  url: string;
  provider?: AgentProvider;
  version: string;
  documentationUrl?: string;
  capabilities?: AgentCapabilities;
  defaultInputModes?: string[];
  defaultOutputModes?: string[];
  securitySchemes?: Record<string, SecurityScheme>;
  security?: Record<string, string[]>[];
  skills?: AgentSkill[];
  extensions?: AgentExtension[];
  metadata?: Record<string, unknown>;
}

// ── JSON-RPC (Section 9) ──────────────────────────────────────────────
export interface JSONRPCRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: Record<string, unknown>;
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

// ── SendMessage Params (Section 3.2.1) ────────────────────────────────
export interface MessageSendParams {
  message: Message;
  configuration?: {
    blocking?: boolean;
    acceptedOutputModes?: string[];
    pushNotificationConfig?: PushNotificationConfig;
    historyLength?: number;
  };
  metadata?: Record<string, unknown>;
}

// ── GetTask Params (Section 3.1.3) ────────────────────────────────────
export interface GetTaskParams {
  id: string;
  historyLength?: number;
  metadata?: Record<string, unknown>;
}

// ── ListTasks Params (Section 3.1.4) ──────────────────────────────────
export interface ListTasksParams {
  contextId?: string;
  status?: TaskState;
  limit?: number;
  offset?: number;
  metadata?: Record<string, unknown>;
}

// ── CancelTask Params (Section 3.1.5) ─────────────────────────────────
export interface CancelTaskParams {
  id: string;
  metadata?: Record<string, unknown>;
}

// ── Error Codes (Section 9.5) ─────────────────────────────────────────
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
  // arifOS-specific extensions
  HOLD_888: -32008,
  VOID_CONSTITUTIONAL: -32009,
} as const;

// ── A2A Method Names (Section 9.4) ────────────────────────────────────
export const A2A_METHODS = {
  SEND_MESSAGE: 'message/send',
  SEND_STREAMING_MESSAGE: 'message/stream',
  GET_TASK: 'tasks/get',
  LIST_TASKS: 'tasks/list',
  CANCEL_TASK: 'tasks/cancel',
  SUBSCRIBE_TO_TASK: 'tasks/subscribe',
  CREATE_PUSH_CONFIG: 'tasks/pushNotificationConfig/create',
  GET_PUSH_CONFIG: 'tasks/pushNotificationConfig/get',
  LIST_PUSH_CONFIGS: 'tasks/pushNotificationConfig/list',
  DELETE_PUSH_CONFIG: 'tasks/pushNotificationConfig/delete',
  GET_EXTENDED_CARD: 'agent/getAuthenticatedExtendedCard',
} as const;

// ── Helper: extract text from official Part format ─────────────────────
export function extractTextFromParts(parts: Part[]): string {
  return parts
    .filter(isTextPart)
    .map(p => p.text)
    .join(' ')
    .trim();
}

// ── Helper: convert legacy parts to official ──────────────────────────
export function normalizeParts(parts: unknown[]): Part[] {
  return parts.map(p => {
    if (!p || typeof p !== 'object') return { text: String(p), mediaType: 'text/plain' };
    // Already official format
    if ('text' in p || 'raw' in p || 'url' in p || 'data' in p) return p as Part;
    // Legacy format
    if ('kind' in p) return normalizePart(p as LegacyPart);
    return { text: JSON.stringify(p), mediaType: 'application/json' };
  });
}
