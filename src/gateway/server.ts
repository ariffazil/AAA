import express, { Request, Response } from 'express';
import { 
  JSONRPCRequest, 
  ERROR_CODES, 
  Task, 
  MessageSendParams,
  TaskMessage,
  PushNotificationConfig
} from './schema';
import { createAuthMiddleware, AuthContext } from './auth';
import { TaskStore, EventBus } from './store';
import { GovernanceAdapter } from '../adapter/router';
import { getAgentCard, CONSTITUTION_DEFAULTS } from '../seed/bootstrap';

function generateId(): string {
  return crypto.randomUUID();
}

class AAAGatewayExecutor {
  private adapter = new GovernanceAdapter();

  async execute(
    taskId: string,
    contextId: string,
    message: TaskMessage,
    eventBus: EventBus,
    taskStore: TaskStore,
    pushNotificationConfig?: PushNotificationConfig
  ): Promise<void> {
    console.log(`[AAA Gateway] Processing task ${taskId} via Governance Adapter`);

    try {
      // 1. Initial State
      await taskStore.updateTask(taskId, {
        status: { state: 'working', timestamp: new Date().toISOString() }
      });

      // 2. Risk-Based Routing (The Adapter)
      const result = await this.adapter.routeIntent(message);

      // 3. Completion
      await taskStore.updateTask(taskId, {
        status: { 
          state: 'completed', 
          message: {
            role: 'agent',
            parts: [{ kind: 'text', text: `[AAA] Result from ${result.source}: ${result.status}` }],
            messageId: generateId(),
            taskId,
            contextId
          },
          timestamp: new Date().toISOString() 
        }
      });

      await eventBus.publish({
        kind: 'status-update',
        taskId,
        contextId,
        status: { state: 'completed', timestamp: new Date().toISOString() },
        final: true
      });

    } catch (error: any) {
      console.error(`[AAA Gateway] Execution failed: ${error.message}`);
      
      const isHold = error.message.includes('888_HOLD');
      const state = isHold ? 'auth-required' : 'failed';
      
      await taskStore.updateTask(taskId, {
        status: { 
          state, 
          message: {
            role: 'agent',
            parts: [{ kind: 'text', text: error.message }],
            messageId: generateId(),
            taskId,
            contextId
          },
          timestamp: new Date().toISOString() 
        }
      });

      await eventBus.publish({
        kind: 'status-update',
        taskId,
        contextId,
        status: { state, timestamp: new Date().toISOString() },
        final: true
      });
    }
  }
}

export function createApp(): express.Application {
  const app = express();
  app.use(express.json());

  const taskStore = new TaskStore();
  const eventBus = new EventBus();
  const executor = new AAAGatewayExecutor();
  const authMiddleware = createAuthMiddleware();

  app.use(authMiddleware as any);

  // ── Discovery ────────────────────────────────────────────────────────────
  app.get('/.well-known/agent.json', (req, res) => res.json(getAgentCard()));
  app.get('/agent.json', (req, res) => res.json(getAgentCard()));

  app.get('/health', (req, res) => {
    res.json({
      status: 'healthy',
      protocol: 'A2A',
      version: '0.3.0',
      gateway: 'AAA',
      auth: (req as any).authContext?.authenticated ? 'enabled' : 'development',
    });
  });

  // ── Message Ingress (Critical Trust Boundary) ───────────────────────────
  app.post('/message/send', async (req: Request, res: Response) => {
    const body = req.body as JSONRPCRequest;
    const params = body.params as MessageSendParams;
    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const contextId = params.contextId || generateId();

    const task: Task = {
      id: taskId,
      contextId,
      status: { state: 'submitted', timestamp: new Date().toISOString() },
      artifacts: [],
      history: [params.message],
      metadata: params.metadata || {},
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    await taskStore.setTask(task);
    
    // Execute via internal executor which uses the Adapter
    await executor.execute(taskId, contextId, params.message, eventBus, taskStore);
    
    const updatedTask = await taskStore.getTask(taskId);
    res.json({ jsonrpc: '2.0', id: body.id, result: updatedTask });
  });

  return app;
}

const PORT = process.env.PORT || 3001;
if (process.env.NODE_ENV !== 'test') {
  createApp().listen(PORT, () => console.log(`[AAA] Gateway running on port ${PORT}`));
}
