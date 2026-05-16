import express, { Request, Response, Router } from 'express';
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

// In-memory event log — last 200 events, newest first on read
const _eventLog: Array<{ id: string; ts: string; kind: string; taskId: string; msg: string }> = [];

function logEvent(kind: string, taskId: string, msg: string): void {
  _eventLog.push({ id: crypto.randomUUID().slice(0, 8), ts: new Date().toISOString(), kind, taskId, msg });
  if (_eventLog.length > 200) _eventLog.splice(0, 1);
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
    logEvent('TASK_START', taskId, 'Mission received by kernel');

    try {
      // 1. Initial State
      await taskStore.updateTask(taskId, {
        status: { state: 'working', timestamp: new Date().toISOString() }
      });
      logEvent('SENSE', taskId, 'Risk assessment dispatched to A-FORGE');

      // 2. Risk-Based Routing (The Adapter)
      const result = await this.adapter.routeIntent(message);
      logEvent('MIND', taskId, `A-FORGE verdict: ${result.status}`);

      // 3. Completion or Hold
      const state = result.status === 'HOLD' ? 'input-required' : 'completed';

      if (result.status === 'HOLD') {
        logEvent('888_HOLD', taskId, `Hold triggered — ${result.reason}`);
      } else {
        logEvent('999_SEAL', taskId, 'Task authorized and sealed to VAULT999');
      }

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
      logEvent('ERROR', taskId, `Execution failed: ${error.message}`);

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

  // Single router mounted at both / and /api — so Caddy's /api/* proxy
  // strips nothing, and Express handles both /health and /api/operator/tasks
  const mainRouter = Router();

  // ── Discovery ────────────────────────────────────────────────────────────
  mainRouter.get('/.well-known/agent.json', (req, res) => res.json(getAgentCard()));
  mainRouter.get('/agent.json', (req, res) => res.json(getAgentCard()));

  mainRouter.get('/health', (req, res) => {
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
  mainRouter.get('/operator/tasks', async (req, res) => {
    const state = req.query.state as string;
    const tasks = await taskStore.listTasks(state ? { state: state as any } : undefined);
    res.json({ ok: true, tasks });
  });

  mainRouter.get('/operator/tasks/:taskId', async (req, res) => {
    const task = await taskStore.getTask(req.params.taskId);
    if (!task) return res.status(404).json({ ok: false, error: 'Task not found' });
    res.json({ ok: true, task });
  });

  mainRouter.get('/operator/holds', async (req, res) => {
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

  mainRouter.get('/operator/seals', async (req, res) => {
    let seals = 0;
    let vaultConnected = false;
    try {
      const fs = await import('node:fs');
      const vaultPath = process.env.VAULT999_PATH || '/var/vault999/outcomes.jsonl';
      const lines = fs.readFileSync(vaultPath, 'utf8').split('\n').filter(Boolean);
      seals = lines.length;
      vaultConnected = true;
    } catch {
      const completed = await taskStore.listTasks({ state: 'completed' });
      seals = completed.length;
    }
    res.json({ ok: true, seals, vaultConnected });
  });

  mainRouter.get('/operator/events', (req, res) => {
    const n = Math.min(parseInt(String(req.query.n || '50')), 100);
    res.json({ ok: true, events: _eventLog.slice(-n).reverse() });
  });

  mainRouter.post('/operator/tasks/:taskId/approve', async (req, res) => {
    const { taskId } = req.params;
    const { humanId, signature } = req.body;

    const task = await taskStore.getTask(taskId);
    if (!task || task.status.state !== 'input-required') {
      return res.status(404).json({ ok: false, error: 'Task not found or not awaiting approval' });
    }

    await taskStore.updateTask(taskId, {
      status: { state: 'working', timestamp: new Date().toISOString() },
      metadata: {
        ...task.metadata,
        approvedBy: humanId,
        humanSignature: signature,
        approvedAt: new Date().toISOString()
      }
    });

    logEvent('HUMAN_APPROVE', taskId, `Approved by ${humanId || 'operator'}`);
    await executor.execute(taskId, task.contextId, task.history[0], eventBus, taskStore);

    res.json({ ok: true, message: 'Task approved and execution resumed via A-FORGE' });
  });

  mainRouter.post('/operator/tasks/:taskId/reject', async (req, res) => {
    const { taskId } = req.params;
    const { reason } = req.body;

    logEvent('HUMAN_REJECT', taskId, `Rejected: ${reason || 'no reason given'}`);
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
  mainRouter.post('/message/send', async (req: Request, res: Response) => {
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
    await executor.execute(taskId, contextId, params.message, eventBus, taskStore);

    const updatedTask = await taskStore.getTask(taskId);
    res.json({ jsonrpc: '2.0', id: body.id, result: updatedTask });
  });

  // Mount at root (for /health, /.well-known/*, etc.) and at /api (for Caddy /api/* proxy)
  app.use('/', mainRouter);
  app.use('/api', mainRouter);

  return app;
}

const PORT = process.env.PORT || 3001;
if (process.env.NODE_ENV !== 'test') {
  createApp().listen(PORT, () => console.log(`[AAA] Gateway running on port ${PORT}`));
}
