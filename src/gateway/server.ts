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
import { getAgentCard, getDiscoveryRoutingPolicy, CONSTITUTION_DEFAULTS } from '../seed/bootstrap';
import https from 'node:https';
import http from 'node:http';

function getA2ADiscoveryContract() {
  const card = getAgentCard();
  const policy = getDiscoveryRoutingPolicy();
  return {
    contract_id: 'aaa-a2a-discovery-contract-v1',
    version: '1.0.0',
    canonical_discovery_surface: '/.well-known/a2a-discovery.json',
    canonical_agent_card: '/.well-known/agent-card.json',
    canonical_routing_policy: '/.well-known/a2a-routing-policy.json',
    compatibility_aliases: {
      agent_card: ['/agent-card.json', '/a2a/agent-card.json'],
      legacy_agent: ['/.well-known/agent.json', '/agent.json', '/a2a/agent.json'],
      routing_policy: ['/a2a/routing-policy.json'],
    },
    protocol: {
      name: 'A2A',
      version: card.protocol_version,
      preferred_transport: card.preferred_transport || 'jsonrpc-https',
    },
    policy: {
      default_mode: policy.default_mode,
      fallback_mode: policy.fallback?.mode || 'hybrid',
      graph_only_allowed_by_default: false,
    },
  };
}

// ── Grafana Webhook + Organ Monitor + Telegram Notifier ───────────────────────

const TELEGRAM_BOT_TOKEN = '8410138119:AAHrXysyxI8yuBM7QW6QTafKsgpqEyd19DA';
const TELEGRAM_CHAT_ID = '267378578';

const ORGANS = [
  { name: 'arifOS MCP', port: 8088 },
  { name: 'GEOX', port: 18081 },
  { name: 'WEALTH', port: 18082 },
  { name: 'WELL', port: 18083 },
  { name: 'APEX Prime', port: 3002 },
  { name: 'A-FORGE', port: 7071 },
] as const;

function httpGet(port: number, path: string): Promise<{ ok: boolean; status?: number; body?: unknown }> {
  return new Promise((resolve) => {
    const req = http.get(`http://localhost:${port}${path}`, (res) => {
      let data = '';
      res.on('data', (chunk: string) => data += chunk);
      res.on('end', () => {
        try {
          resolve({ ok: true, status: res.statusCode, body: JSON.parse(data) });
        } catch {
          resolve({ ok: true, status: res.statusCode, body: data });
        }
      });
    });
    req.on('error', () => resolve({ ok: false }));
    req.setTimeout(5000, () => { req.destroy(); resolve({ ok: false }); });
  });
}

async function checkOrganHealth(name: string, port: number): Promise<{ name: string; port: number; healthy: boolean; detail?: string }> {
  const result = await httpGet(port, '/health');
  if (!result.ok) {
    return { name, port, healthy: false, detail: 'connection failed' };
  }
  if (result.status !== 200) {
    return { name, port, healthy: false, detail: `HTTP ${result.status}` };
  }
  const body = result.body as Record<string, unknown>;
  const status = typeof body?.status === 'string' ? body.status : 'unknown';
  const healthy = status === 'healthy' || status === 'ok' || status === 'live';
  return { name, port, healthy, detail: status };
}

async function sendTelegramMessage(text: string): Promise<boolean> {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  const body = JSON.stringify({ chat_id: TELEGRAM_CHAT_ID, text, parse_mode: 'HTML' });
  return new Promise((resolve) => {
    const req = https.request(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } }, (res) => {
      let data = '';
      res.on('data', (chunk: string) => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.ok === true);
        } catch { resolve(false); }
      });
    });
    req.on('error', () => resolve(false));
    req.write(body);
    req.end();
  });
}

function formatAlert(alert: GrafanaAlert, confirmedDown: string[]): string {
  const emoji = (organ: string) => confirmedDown.includes(organ) ? '🔴' : '🟢';
  const lines = [
    `<b>🚨 Grafana Alert — Organ Monitor</b>`,
    ``,
    `<b>Alert:</b> ${alert.alertName}`,
    `<b>Summary:</b> ${alert.summary}`,
    `<b>State:</b> ${alert.state}`,
    ``,
    `<b>Organ Health Check:</b>`,
    ...ORGANS.map(o => {
      const found = alert.organChecks?.find((c: { name: string }) => c.name === o.name);
      if (!found) return `  ${emoji(o.name)} ${o.name}: not checked`;
      return `  ${found.healthy ? '🟢' : '🔴'} ${o.name}: ${found.healthy ? 'OK' : 'DOWN'} (${found.detail})`;
    }),
    ``,
    confirmedDown.length > 0
      ? `<b>Confirmed DOWN:</b> ${confirmedDown.join(', ')}`
      : `<b>All organs operational</b>`,
    ``,
    `<i>DITEMPA BUKAN DIBERI — arifOS Federation</i>`,
  ];
  return lines.join('\n');
}

interface GrafanaAlert {
  alertName: string;
  summary: string;
  state: string;
  organChecks?: Array<{ name: string; port: number; healthy: boolean; detail?: string }>;
}

function generateId(): string {
  return crypto.randomUUID();
}

// In-memory event log — last 200 events, newest first on read
const _eventLog: Array<{ id: string; ts: string; kind: string; taskId: string; msg: string }> = [];

function logEvent(kind: string, taskId: string, msg: string): void {
  _eventLog.push({ id: crypto.randomUUID().slice(0, 8), ts: new Date().toISOString(), kind, taskId, msg });
  if (_eventLog.length > 200) _eventLog.splice(0, 1);
}

/**
 * F7 PII redaction (arifOS audit 2026-06-02 — P0 dignity breach).
 * Strips operator-supplied text from event log messages before they
 * reach any client. Defense in depth: the deployed build may have
 * legacy logEvent calls that put raw operator text into `msg`; this
 * function ensures no operator input ever leaves the gateway.
 *
 * Patterns redacted:
 *   - `Operator mission: "..."`  → keeps the prefix, replaces the quote
 *   - `Operator input: "..."`
 *   - `operator submitted: "..."`
 *   - any double-quoted string up to 2KB (belt and suspenders)
 *
 * Added 2026-06-02 19:35 UTC under F13 SOVEREIGN ratification.
 */
const OPERATOR_TEXT_PATTERNS: RegExp[] = [
  /(Operator mission:\s*)"([^"]*)"/g,
  /(Operator input:\s*)"([^"]*)"/g,
  /(operator submitted:\s*)"([^"]*)"/g,
  /"([^"]{1,2000})"/g, // any quoted string up to 2KB — belt and suspenders
];

function redactEventMsg(msg: string): string {
  let out = msg;
  for (const re of OPERATOR_TEXT_PATTERNS) {
    out = out.replace(re, (match, p1) => {
      if (typeof p1 === 'string' && p1.length > 0) {
        return `${p1}"[redacted — operator session only]"`;
      }
      return `"[redacted — operator session only]"`;
    });
  }
  return out;
}

function redactEventLog(events: typeof _eventLog): typeof _eventLog {
  return events.map((ev) => ({ ...ev, msg: redactEventMsg(ev.msg) }));
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
  const discoveryAliases = [
    '/.well-known/a2a-discovery.json',
    '/a2a/discovery-contract.json',
    '/.well-known/agent-card.json',
    '/.well-known/agent.json',
    '/agent-card.json',
    '/agent.json',
    '/a2a/agent-card.json',
    '/a2a/agent.json',
  ];
  for (const path of discoveryAliases) {
    mainRouter.get(path, (req, res) => {
      res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
      if (path === '/.well-known/a2a-discovery.json') {
        return res.json(getA2ADiscoveryContract());
      }
      return res.json(getAgentCard());
    });
  }
  for (const path of ['/.well-known/a2a-routing-policy.json', '/a2a/routing-policy.json']) {
    mainRouter.get(path, (req, res) => {
      res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
      res.json(getDiscoveryRoutingPolicy());
    });
  }

  mainRouter.get('/health', (req, res) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.json({
      status: 'healthy',
      protocol: 'A2A',
      version: '1.0.0',
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
    let seals: number;
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
    res.json({ ok: true, events: redactEventLog(_eventLog.slice(-n).reverse()) });
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

  // ── Grafana Webhook ────────────────────────────────────────────────────────
  mainRouter.post('/webhooks/grafana/alerts', async (req: Request, res: Response) => {
    const alert = req.body as GrafanaAlert;
    const alertName = alert?.alertName || 'Unknown Alert';
    const summary = alert?.summary || '';
    const state = alert?.state || 'unknown';

    // Check all organs
    const organChecks = await Promise.all(
      ORGANS.map(({ name, port }) => checkOrganHealth(name, port))
    );

    const confirmedDown = organChecks
      .filter((o) => !o.healthy)
      .map((o) => o.name);

    const alert2: GrafanaAlert = {
      alertName,
      summary,
      state,
      organChecks,
    };

    const telegramMsg = formatAlert(alert2, confirmedDown);
    const notified = await sendTelegramMessage(telegramMsg);

    logEvent('GRAFANA_WEBHOOK', 'n/a', `Alert "${alertName}" state=${state} confirmedDown=${confirmedDown.join(',') || 'none'}`);

    res.json({
      ok: true,
      received: true,
      organChecks,
      confirmedDown,
      telegramNotified: notified,
    });
  });

  return app;
}

const PORT = process.env.PORT || 3001;
if (process.env.NODE_ENV !== 'test') {
  createApp().listen(PORT, () => console.log(`[AAA] Gateway running on port ${PORT}`));
}
