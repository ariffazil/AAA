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

      // 3. Completion or Hold
      const state = result.status === 'HOLD' ? 'input-required' : 'completed';
      
      let text = `[AAA] Result from ${result.source}: ${result.status}`;
      if (result.status === 'HOLD') {
        text = `[AAA] HUMAN CONFIRMATION REQUIRED. Risk: ${result.riskLevel}. ${result.reason}. Bond: ${result.irreversibilityBond}`;
      }

      await taskStore.updateTask(taskId, {
        status: { 
          state, 
          message: {
            role: 'agent',
            parts: [{ 
              kind: 'text', 
              text 
            }],
            messageId: generateId(),
            taskId,
            contextId
          },
          timestamp: new Date().toISOString() 
        },
        metadata: {
          ...result.proof,
          riskLevel: result.riskLevel,
          irreversibilityBond: result.irreversibilityBond
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
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.json({
      status: 'healthy',
      protocol: 'A2A',
      version: '0.3.0',
      gateway: 'AAA',
      auth: (req as any).authContext?.authenticated ? 'enabled' : 'development',
    });
  });

  // ── Operator Interface ───────────────────────────────────────────────────
  app.get('/operator/tasks', async (req, res) => {
    const state = req.query.state as string;
    const tasks = await taskStore.listTasks(state ? { state: state as any } : undefined);
    res.json({ ok: true, tasks });
  });

  app.get('/operator/holds', async (req, res) => {
    const pending = await taskStore.listTasks({ state: 'input-required' });
    const auth = await taskStore.listTasks({ state: 'auth-required' });
    res.json({
      ok: true,
      holds: pending.length + auth.length,
      breakdown: {
        'input-required': pending.length,
        'auth-required': auth.length,
      }
    });
  });

  app.post('/operator/tasks/:taskId/approve', async (req, res) => {
    const { taskId } = req.params;
    const { humanId, signature } = req.body;
    
    const task = await taskStore.getTask(taskId);
    if (!task || task.status.state !== 'input-required') {
      return res.status(404).json({ ok: false, error: 'Task not found or not awaiting approval' });
    }

    // Record human approval in metadata
    await taskStore.updateTask(taskId, {
      status: { state: 'working', timestamp: new Date().toISOString() },
      metadata: {
        ...task.metadata,
        approvedBy: humanId,
        humanSignature: signature,
        approvedAt: new Date().toISOString()
      }
    });

    // Execute via A-FORGE now that we have human confirmation
    await executor.execute(taskId, task.contextId, task.history[0], eventBus, taskStore);
    
    res.json({ ok: true, message: 'Task approved and execution resumed via A-FORGE' });
  });

  app.post('/operator/tasks/:taskId/reject', async (req, res) => {
    const { taskId } = req.params;
    const { reason } = req.body;

    await taskStore.updateTask(taskId, {
      status: { 
        state: 'rejected', 
        timestamp: new Date().toISOString(),
        message: {
          role: 'agent',
          parts: [{ kind: 'text', text: `Rejected by human operator: ${reason}` }],
          messageId: generateId(),
          taskId,
          contextId: (await taskStore.getTask(taskId))?.contextId || ''
        }
      }
    });

    res.json({ ok: true, message: 'Task rejected' });
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
