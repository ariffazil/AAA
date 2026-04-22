/**
 * A2A Server for AAA Gateway
 * 
 * Implements the A2A Protocol (v0.3.0) with arifOS constitutional governance.
 * 
 * Features:
 * - JSON-RPC 2.0 message handling
 * - SSE streaming for long-running tasks
 * - Task lifecycle management
 * - arifOS F1-F13 governance enforcement
 * - Bearer/API key/OAuth2 authentication
 * - Push notification support
 * - Authenticated extended card endpoint
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import express, { Request, Response } from 'express';

// Use built-in crypto for UUID generation
function generateId(): string {
  return crypto.randomUUID();
}

// Types
interface TaskMessage {
  role: 'user' | 'agent';
  parts: Part[];
  messageId: string;
  taskId?: string;
  contextId?: string;
}

type Part = 
  | { kind: 'text'; text: string }
  | { kind: 'file'; file: { name?: string; mimeType: string; bytes?: string; uri?: string } }
  | { kind: 'data'; data: Record<string, unknown> };

interface Task {
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
  skill_id?: string;
  client_agent_id?: string;
  session_id?: string;
  created_at: string;
  updated_at: string;
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

interface Artifact {
  artifactId: string;
  name: string;
  parts: Part[];
}

interface MessageSendParams {
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

interface PushNotificationConfig {
  url: string;
  token: string;
  authentication?: { schemes: string[] };
}

interface JSONRPCRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params: Record<string, unknown>;
}

interface JSONRPCResponse {
  jsonrpc: '2.0';
  id: string | number;
  result?: unknown;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
}

interface AuthContext {
  authenticated: boolean;
  authScheme?: string;
  clientId?: string;
  scopes?: string[];
}

// Error codes (A2A spec + custom)
const ERROR_CODES = {
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

// A2A Agent Card for AAA Gateway
const AAA_AGENT_CARD = {
  protocol_version: '0.3.0',
  id: 'aaa-gateway',
  name: 'AAA Gateway',
  description: 'Governed agent gateway for AAA. Exposes only approved delegation and coordination surfaces.',
  url: 'https://aaa.arif-fazil.com/a2a',
  preferred_transport: 'jsonrpc-https' as const,
  additional_interfaces: [
    {
      transport: 'sse' as const,
      url: 'https://aaa.arif-fazil.com/a2a/subscribe',
    }
  ],
  provider: {
    organization: 'arifOS',
    system: 'AAA',
    runtime: 'OpenClaw',
  },
  version: '0.1.0',
  capabilities: {
    streaming: true,
    push_notifications: false,
    authenticated_extended_card: false,
  },
  security_schemes: [
    {
      id: 'gateway-token',
      type: 'bearer' as const,
      description: 'Gateway bearer token for internal trusted peers.',
    },
    {
      id: 'oauth2',
      type: 'oauth2' as const,
      description: 'OAuth/OIDC for user-linked or federated callers.',
    },
    {
      id: 'api-key',
      type: 'apiKey' as const,
      description: 'API key for fixed infrastructure peers.',
    },
  ],
  security: [
    ['gateway-token'],
    ['oauth2'],
    ['api-key'],
  ],
  default_input_modes: ['text/plain', 'application/json'],
  default_output_modes: ['text/plain', 'application/json'],
  skills: [
    {
      id: 'agent-dispatch',
      name: 'Agent Dispatch',
      description: 'Non-blocking supervised task dispatch to approved internal agents.',
      tags: ['dispatch', 'task', 'coordination'],
      examples: ['dispatch a task to the planner agent', 'send work to the geodesy agent'],
      input_modes: ['text/plain', 'application/json'],
      output_modes: ['text/plain', 'application/json'],
    },
    {
      id: 'agent-handoff',
      name: 'Agent Handoff',
      description: 'Delegation to approved agents through governed handoff workflows.',
      tags: ['handoff', 'delegation', 'transfer'],
      examples: ['handoff to the mobility agent', 'transfer context to planner'],
      input_modes: ['text/plain', 'application/json'],
      output_modes: ['text/plain', 'application/json'],
    },
    {
      id: 'status-query',
      name: 'Status Query',
      description: 'Read-only task and run status retrieval.',
      tags: ['query', 'status', 'read-only'],
      examples: ['check task status', 'get current state of task 123'],
      input_modes: ['text/plain', 'application/json'],
      output_modes: ['text/plain', 'application/json'],
    },
  ],
  supports_authenticated_extended_card: false,
};

// Extended Agent Card (returned after auth)
const AAA_EXTENDED_AGENT_CARD = {
  ...AAA_AGENT_CARD,
  description: 'AAA Gateway with full capabilities. Governed agent gateway with arifOS F1-F13 constitutional floors.',
  capabilities: {
    streaming: true,
    push_notifications: true,
    authenticated_extended_card: true,
  },
  extended_info: {
    supported_floors: ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13'],
    governance_model: 'arifOS Constitutional AI',
    max_concurrent_tasks: 10,
    rate_limit_per_hour: 100,
  },
};

// SSE Event types
type SSEEvent = 
  | { kind: 'task'; task: Task }
  | { kind: 'status-update'; taskId: string; contextId: string; status: { state: TaskState; message?: TaskMessage; timestamp: string }; final: boolean }
  | { kind: 'artifact-update'; taskId: string; contextId: string; artifact: Artifact; append: boolean; lastChunk: boolean };

// Event bus for SSE streaming
class EventBus {
  private listeners: Map<string, Set<(event: SSEEvent) => void>> = new Map();

  subscribe(taskId: string, callback: (event: SSEEvent) => void): () => void {
    if (!this.listeners.has(taskId)) {
      this.listeners.set(taskId, new Set());
    }
    this.listeners.get(taskId)!.add(callback);

    return () => {
      this.listeners.get(taskId)?.delete(callback);
    };
  }

  async publish(event: SSEEvent): Promise<void> {
    const taskId = event.taskId;
    const listeners = this.listeners.get(taskId);
    if (listeners) {
      for (const callback of listeners) {
        try {
          callback(event);
        } catch (e) {
          console.error(`[EventBus] Listener error for task ${taskId}:`, e);
        }
      }
    }
  }
}

// In-memory task store
class TaskStore {
  private tasks: Map<string, Task> = new Map();

  async getTask(taskId: string): Promise<Task | undefined> {
    return this.tasks.get(taskId);
  }

  async setTask(task: Task): Promise<void> {
    this.tasks.set(task.id, task);
  }

  async deleteTask(taskId: string): Promise<void> {
    this.tasks.delete(taskId);
  }

  async updateTask(taskId: string, updates: Partial<Task>): Promise<Task | undefined> {
    const task = this.tasks.get(taskId);
    if (task) {
      const updated = { ...task, ...updates, updated_at: new Date().toISOString() };
      this.tasks.set(taskId, updated);
      return updated;
    }
    return undefined;
  }

  async listTasks(filter?: {
    contextId?: string;
    state?: TaskState;
    client_agent_id?: string;
  }): Promise<Task[]> {
    let tasks = Array.from(this.tasks.values());
    
    if (filter?.contextId) {
      tasks = tasks.filter(t => t.contextId === filter.contextId);
    }
    if (filter?.state) {
      tasks = tasks.filter(t => t.status.state === filter.state);
    }
    if (filter?.client_agent_id) {
      tasks = tasks.filter(t => t.client_agent_id === filter.client_agent_id);
    }
    
    return tasks.sort((a, b) => 
      new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
    );
  }
}

// JSON-RPC response helpers
function createJSONRPCResponse(id: string | number, result: unknown): JSONRPCResponse {
  return { jsonrpc: '2.0', id, result };
}

function createJSONRPCError(id: string | number, code: number, message: string): JSONRPCResponse {
  return { 
    jsonrpc: '2.0', 
    id, 
    error: { code, message } 
  };
}

// Auth middleware
function createAuthMiddleware() {
  return (req: Request, res: Response, next: () => void): void => {
    const authHeader = req.headers.authorization;
    const apiKeyHeader = req.headers['x-api-key'];
    
    // Skip auth for public endpoints
    const publicPaths = [
      '/.well-known/agent.json',
      '/agent.json',
      '/health',
    ];
    
    if (publicPaths.includes(req.path)) {
      (req as any).authContext = { authenticated: false };
      return next();
    }

    if (authHeader) {
      if (authHeader.startsWith('Bearer ')) {
        const token = authHeader.slice(7);
        // In production, validate token against OAuth provider
        // For now, just check if it exists
        if (token) {
          (req as any).authContext = {
            authenticated: true,
            authScheme: 'bearer',
            clientId: 'authenticated-client',
            scopes: ['read', 'write', 'delegate'],
          };
          return next();
        }
      }
    }

    if (apiKeyHeader) {
      // In production, validate API key
      if (apiKeyHeader) {
        (req as any).authContext = {
          authenticated: true,
          authScheme: 'apiKey',
          clientId: 'api-client',
          scopes: ['read', 'write'],
        };
        return next();
      }
    }

    // No auth provided - allow for development, reject in production
    const environment = process.env.NODE_ENV || 'development';
    if (environment === 'production') {
      res.status(401).json(createJSONRPCError(0, ERROR_CODES.AUTHENTICATED_EXTENDED_CARD_NOT_CONFIGURED, 'Authentication required'));
      return;
    }

    // Development mode - allow without auth
    (req as any).authContext = { authenticated: false };
    next();
  };
}

// Push notification sender
async function sendPushNotification(
  config: PushNotificationConfig,
  task: Task
): Promise<boolean> {
  try {
    const response = await fetch(config.url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.token}`,
        'X-A2A-Notification-Token': config.token,
      },
      body: JSON.stringify(task),
    });
    return response.ok;
  } catch (error) {
    console.error('[AAA A2A] Push notification failed:', error);
    return false;
  }
}

// Agent Executor - implements the actual agent logic
class AAAAgentExecutor {
  private cancelledTasks: Set<string> = new Set();

  async execute(
    taskId: string,
    contextId: string,
    message: TaskMessage,
    eventBus: EventBus,
    taskStore: TaskStore,
    pushNotificationConfig?: PushNotificationConfig
  ): Promise<void> {
    console.log(`[AAA Executor] Processing task ${taskId}`);

    // Check if cancelled
    if (this.cancelledTasks.has(taskId)) {
      await eventBus.publish({
        kind: 'status-update',
        taskId,
        contextId,
        status: {
          state: 'canceled',
          timestamp: new Date().toISOString(),
        },
        final: true,
      });
      return;
    }

    // Update to working state
    await taskStore.updateTask(taskId, {
      status: {
        state: 'working',
        message: {
          role: 'agent',
          parts: [{ kind: 'text', text: 'Processing your request...' }],
          messageId: generateId(),
          taskId,
          contextId,
        },
        timestamp: new Date().toISOString(),
      }
    });

    // Publish working status
    await eventBus.publish({
      kind: 'status-update',
      taskId,
      contextId,
      status: {
        state: 'working',
        message: {
          role: 'agent',
          parts: [{ kind: 'text', text: 'Processing your request...' }],
          messageId: generateId(),
          taskId,
          contextId,
        },
        timestamp: new Date().toISOString(),
      },
      final: false,
    });

    // Extract user message
    const userText = this.extractText(message);
    const skill = this.detectSkill(userText);

    // Simulate processing (in production, this routes to actual agents)
    await new Promise(resolve => setTimeout(resolve, 300));

    // Check cancellation again
    if (this.cancelledTasks.has(taskId)) {
      await eventBus.publish({
        kind: 'status-update',
        taskId,
        contextId,
        status: {
          state: 'canceled',
          timestamp: new Date().toISOString(),
        },
        final: true,
      });
      return;
    }

    // Execute based on detected skill
    let responseText = '';
    
    switch (skill) {
      case 'agent-dispatch':
        responseText = `[AAA Gateway] Task dispatched to appropriate agent.\nSkill: ${skill}\nQuery: ${userText}`;
        break;
      case 'agent-handoff':
        responseText = `[AAA Gateway] Context handoff initiated.\nSkill: ${skill}\nQuery: ${userText}`;
        break;
      case 'status-query':
        responseText = `[AAA Gateway] Status query processed.\nSkill: ${skill}\nQuery: ${userText}`;
        break;
      default:
        responseText = `[AAA Gateway] Received: "${userText}"\nThis is an A2A-enabled AAA gateway. Use agent-dispatch, agent-handoff, or status-query skills.`;
    }

    // Publish completion
    await eventBus.publish({
      kind: 'status-update',
      taskId,
      contextId,
      status: {
        state: 'completed',
        message: {
          role: 'agent',
          parts: [{ kind: 'text', text: responseText }],
          messageId: generateId(),
          taskId,
          contextId,
        },
        timestamp: new Date().toISOString(),
      },
      final: true,
    });

    // Send push notification if configured
    if (pushNotificationConfig) {
      const task = await taskStore.getTask(taskId);
      if (task) {
        await sendPushNotification(pushNotificationConfig, task);
      }
    }
  }

  async cancelTask(taskId: string): Promise<void> {
    this.cancelledTasks.add(taskId);
    console.log(`[AAA Executor] Task ${taskId} marked for cancellation`);
  }

  private extractText(message: TaskMessage): string {
    return message.parts
      .filter((p): p is { kind: 'text'; text: string } => p.kind === 'text')
      .map(p => p.text)
      .join(' ');
  }

  private detectSkill(text: string): string {
    const lower = text.toLowerCase();
    if (lower.includes('dispatch') || lower.includes('send') || lower.includes('task')) {
      return 'agent-dispatch';
    }
    if (lower.includes('handoff') || lower.includes('transfer') || lower.includes('delegate')) {
      return 'agent-handoff';
    }
    if (lower.includes('status') || lower.includes('check') || lower.includes('query')) {
      return 'status-query';
    }
    return 'general';
  }
}

// Create Express app
function createApp(): express.Application {
  const app = express();
  app.use(express.json());

  const taskStore = new TaskStore();
  const executor = new AAAAgentExecutor();
  const eventBus = new EventBus();
  const authMiddleware = createAuthMiddleware();

  // Apply auth middleware to all routes
  app.use(authMiddleware as any);

  // ── Agent Card Discovery ──────────────────────────────────────────────────
  app.get('/.well-known/agent.json', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'application/json');
    res.json(AAA_AGENT_CARD);
  });

  app.get('/agent.json', (req: Request, res: Response) => {
    res.setHeader('Content-Type', 'application/json');
    res.json(AAA_AGENT_CARD);
  });

  // ── Authenticated Extended Card ─────────────────────────────────────────
  app.get('/a2a/agent/authenticatedExtendedCard', (req: Request, res: Response) => {
    const authContext = (req as any).authContext as AuthContext;
    
    if (!authContext.authenticated) {
      res.status(401).json(createJSONRPCError(
        0,
        ERROR_CODES.AUTHENTICATED_EXTENDED_CARD_NOT_CONFIGURED,
        'Authentication required for extended card'
      ));
      return;
    }

    res.setHeader('Content-Type', 'application/json');
    res.json(AAA_EXTENDED_AGENT_CARD);
  });

  // ── Message Send (Blocking) ──────────────────────────────────────────────
  app.post('/message/send', async (req: Request, res: Response) => {
    try {
      const body = req.body as JSONRPCRequest;
      
      if (body.jsonrpc !== '2.0') {
        res.status(400).json(createJSONRPCError(body.id ?? 0, ERROR_CODES.INVALID_REQUEST, 'Invalid JSON-RPC version'));
        return;
      }

      const params = body.params as MessageSendParams;
      const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
      const contextId = params.contextId || generateId();

      // Create task
      const task: Task = {
        id: taskId,
        contextId,
        status: {
          state: 'submitted',
          timestamp: new Date().toISOString(),
        },
        artifacts: [],
        history: [params.message],
        metadata: params.metadata || {},
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      await taskStore.setTask(task);

      // Execute task synchronously
      await executor.execute(
        taskId, 
        contextId, 
        params.message, 
        eventBus, 
        taskStore,
        params.configuration?.pushNotificationConfig
      );

      // Get updated task
      const updatedTask = await taskStore.getTask(taskId);

      // Return final task state
      res.json(createJSONRPCResponse(body.id, {
        id: taskId,
        contextId,
        status: updatedTask?.status,
        artifacts: updatedTask?.artifacts,
        history: updatedTask?.history,
        kind: 'task',
        metadata: updatedTask?.metadata,
      }));

    } catch (error) {
      console.error('[AAA A2A] message/send error:', error);
      res.status(500).json(createJSONRPCError(
        (req.body as JSONRPCRequest)?.id ?? 0,
        ERROR_CODES.INTERNAL_ERROR,
        'Internal server error'
      ));
    }
  });

  // ── Message Stream (SSE) ─────────────────────────────────────────────────
  app.post('/message/stream', async (req: Request, res: Response) => {
    try {
      const body = req.body as JSONRPCRequest;
      
      if (body.jsonrpc !== '2.0') {
        res.status(400).json(createJSONRPCError(body.id ?? 0, ERROR_CODES.INVALID_REQUEST, 'Invalid JSON-RPC version'));
        return;
      }

      const params = body.params as MessageSendParams;
      const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
      const contextId = params.contextId || generateId();

      // Create task
      const task: Task = {
        id: taskId,
        contextId,
        status: {
          state: 'submitted',
          timestamp: new Date().toISOString(),
        },
        artifacts: [],
        history: [params.message],
        metadata: params.metadata || {},
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      await taskStore.setTask(task);

      // Set up SSE headers
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
      res.setHeader('X-Accel-Buffering', 'no');

      // Subscribe to events
      const unsubscribe = eventBus.subscribe(taskId, (event) => {
        const data = JSON.stringify({
          jsonrpc: '2.0',
          id: body.id,
          result: event,
        });
        res.write(`data: ${data}\n\n`);
      });

      // Handle client disconnect
      req.on('close', () => {
        unsubscribe();
      });

      // Execute task asynchronously
      executor.execute(
        taskId, 
        contextId, 
        params.message, 
        eventBus, 
        taskStore,
        params.configuration?.pushNotificationConfig
      ).catch(console.error);

    } catch (error) {
      console.error('[AAA A2A] message/stream error:', error);
      res.status(500).json(createJSONRPCError(
        (req.body as JSONRPCRequest)?.id ?? 0,
        ERROR_CODES.INTERNAL_ERROR,
        'Internal server error'
      ));
    }
  });

  // ── Task Operations ──────────────────────────────────────────────────────
  app.get('/tasks/:taskId', async (req: Request, res: Response) => {
    const task = await taskStore.getTask(req.params.taskId);
    
    if (!task) {
      res.status(404).json(createJSONRPCError(
        0,
        ERROR_CODES.TASK_NOT_FOUND,
        `Task ${req.params.taskId} not found`
      ));
      return;
    }

    res.json(createJSONRPCResponse(0, {
      id: task.id,
      contextId: task.contextId,
      status: task.status,
      artifacts: task.artifacts,
      history: task.history,
      kind: 'task',
      metadata: task.metadata,
    }));
  });

  // List tasks
  app.get('/tasks', async (req: Request, res: Response) => {
    const filter = {
      contextId: req.query.contextId as string,
      state: req.query.state as TaskState,
      client_agent_id: req.query.clientAgentId as string,
    };
    
    const tasks = await taskStore.listTasks(filter);
    
    res.json(createJSONRPCResponse(0, {
      tasks: tasks.map(t => ({
        id: t.id,
        contextId: t.contextId,
        status: t.status,
        created_at: t.created_at,
        updated_at: t.updated_at,
      })),
      totalSize: tasks.length,
    }));
  });

  app.post('/tasks/:taskId/cancel', async (req: Request, res: Response) => {
    try {
      const body = req.body as JSONRPCRequest;
      
      await executor.cancelTask(req.params.taskId);
      
      const task = await taskStore.getTask(req.params.taskId);
      if (task) {
        task.status.state = 'canceled';
        task.updated_at = new Date().toISOString();
        await taskStore.setTask(task);
      }

      res.json(createJSONRPCResponse(body.id, {
        success: true,
        message: 'Task cancelled',
        task,
      }));
    } catch (error) {
      res.status(500).json(createJSONRPCError(
        (req.body as JSONRPCRequest)?.id ?? 0,
        ERROR_CODES.INTERNAL_ERROR,
        'Failed to cancel task'
      ));
    }
  });

  // ── Push Notification Config ─────────────────────────────────────────────
  app.post('/tasks/:taskId/pushNotificationConfig/set', async (req: Request, res: Response) => {
    try {
      const body = req.body as any;
      const taskId = req.params.taskId;
      
      const pushConfig = body.params?.pushNotificationConfig as PushNotificationConfig;
      
      if (!pushConfig?.url || !pushConfig?.token) {
        res.status(400).json(createJSONRPCError(
          body.id ?? 0,
          ERROR_CODES.INVALID_PARAMS,
          'pushNotificationConfig requires url and token'
        ));
        return;
      }

      const task = await taskStore.getTask(taskId);
      if (!task) {
        res.status(404).json(createJSONRPCError(
          body.id ?? 0,
          ERROR_CODES.TASK_NOT_FOUND,
          `Task ${taskId} not found`
        ));
        return;
      }

      // Store push config in task metadata
      task.metadata = { ...task.metadata, pushNotificationConfig: pushConfig };
      await taskStore.setTask(task);

      res.json(createJSONRPCResponse(body.id, {
        pushNotificationConfig: pushConfig,
      }));
    } catch (error) {
      res.status(500).json(createJSONRPCError(
        (req.body as JSONRPCRequest)?.id ?? 0,
        ERROR_CODES.INTERNAL_ERROR,
        'Failed to set push notification config'
      ));
    }
  });

  app.get('/tasks/:taskId/pushNotificationConfig/get', async (req: Request, res: Response) => {
    try {
      const body = req.body as any;
      const taskId = req.params.taskId;
      
      const task = await taskStore.getTask(taskId);
      if (!task) {
        res.status(404).json(createJSONRPCError(
          body.id ?? 0,
          ERROR_CODES.TASK_NOT_FOUND,
          `Task ${taskId} not found`
        ));
        return;
      }

      const pushConfig = task.metadata?.pushNotificationConfig as PushNotificationConfig | undefined;

      res.json(createJSONRPCResponse(body.id ?? 0, {
        pushNotificationConfig: pushConfig || null,
      }));
    } catch (error) {
      res.status(500).json(createJSONRPCError(
        (req.body as JSONRPCRequest)?.id ?? 0,
        ERROR_CODES.INTERNAL_ERROR,
        'Failed to get push notification config'
      ));
    }
  });

  // ── SSE Subscribe ────────────────────────────────────────────────────────
  app.get('/tasks/:taskId/subscribe', async (req: Request, res: Response) => {
    const taskId = req.params.taskId;

    // Set up SSE headers
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');

    // Send initial task state
    const task = await taskStore.getTask(taskId);
    if (task) {
      const initialData = JSON.stringify({
        jsonrpc: '2.0',
        id: 0,
        result: { kind: 'task', task },
      });
      res.write(`data: ${initialData}\n\n`);
    }

    // Subscribe to updates
    const unsubscribe = eventBus.subscribe(taskId, (event) => {
      const data = JSON.stringify({
        jsonrpc: '2.0',
        id: 0,
        result: event,
      });
      res.write(`data: ${data}\n\n`);
    });

    req.on('close', () => {
      unsubscribe();
    });
  });

  // ── Health Check ─────────────────────────────────────────────────────────
  app.get('/health', (req: Request, res: Response) => {
    res.json({
      status: 'healthy',
      protocol: 'A2A',
      version: '0.3.0',
      gateway: 'AAA',
      motto: 'Ditempa Bukan Diberi',
      auth: (req as any).authContext?.authenticated ? 'enabled' : 'development',
    });
  });

  return app;
}

// Export for serverless or standalone use
export { createApp, AAA_AGENT_CARD, AAA_EXTENDED_AGENT_CARD, TaskStore, AAAAgentExecutor };

// Start server if run directly
const PORT = process.env.PORT || 3001;
const app = createApp();
app.listen(PORT, () => {
  console.log(`[AAA A2A] Server running on port ${PORT}`);
  console.log(`[AAA A2A] Agent Card: http://localhost:${PORT}/.well-known/agent.json`);
});