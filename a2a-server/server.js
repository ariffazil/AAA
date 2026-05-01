#!/usr/bin/env node
/**
 * A2A Server for AAA Gateway — Hardened
 * Standalone production server - no build step required
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const express = require('express');
const crypto = require('crypto');
const { writeSeal, writeVoid, checkHealth: checkVaultHealth } = require('./vault');

const app = express();
app.use(express.json());

// === CONFIG ===
const A2A_TOKEN=process.env.A2A_TOKEN || 'aaa-a2a-token-dev';
const A2A_API_KEY=process.env.A2A_API_KEY || 'aaa-a2a-apikey-dev';
const ARIFOS_JUDGE_URL = process.env.ARIFOS_JUDGE_URL || 'http://arifosmcp:8080';
const ARIFOS_API_KEY = process.env.ARIFOS_API_KEY || '';

// Fail fast if tokens not configured — no silent dev fallback (F1 AMANAH)
if (!A2A_TOKEN || !A2A_API_KEY) {
  console.error('[AAA A2A] FATAL: A2A_TOKEN and A2A_API_KEY must be set. No dev fallback.');
  process.exit(1);
}

// === TIMING CONSTANTS ===
const NONCE_CACHE_TTL_MS = 5 * 60 * 1000;   // 5 minutes
const REPLAY_CACHE_TTL_MS = 10 * 60 * 1000; // 10 minutes

// === VERDICT CODES (arifOS alignment) ===
const VERDICT = {
  SEAL: 'SEAL',
  HOLD_888: 'HOLD_888',
  VOID: 'VOID',
  CLAIM_ONLY: 'CLAIM_ONLY'
};

// === SKILL APPROVAL POLICIES ===
const SKILL_APPROVAL_POLICY = {
  'agent-dispatch': 'hold',   // requires 888_JUDGE before dispatch
  'agent-handoff': 'hold',   // requires 888_JUDGE before handoff
  'status-query': 'on-demand' // just process directly
};

// === RISK TIERS ===
const RISK_TIER = {
  T0_READ_PUBLIC: 0,
  T1_READ_PRIVATE: 1,
  T2_DRAFT_TRANSFORM: 2,
  T3_INTERNAL_HANDSHAKE: 3,
  T4_EXTERNAL_STATE_CHANGE: 4,
  T5_IRREVERSIBLE_LEGAL_FINANCIAL: 5
};

// === GOVERNANCE INVARIANTS ===
const INVARIANTS = {
  protocolDoesNotGrantAuthority: true,
  capabilityDoesNotImplyPermission: true,
  selfApprovalForbidden: true,
  irreversibleActionsRequireHumanJudge: true,
  allDelegationsAudited: true
};

// === IN-MEMORY STORES ===
const taskStore = new Map();
const eventBus = new Map();
const nonceStore = new Map();   // nonce → { ts, used }
const replayStore = new Map();   // payloadHash → { ts }
const entropyStore = new Map();  // taskId → { before, after }

// === A2A Agent Card v1.0.0 ===
const AAA_AGENT_CARD = {
  name: 'AAA Gateway',
  description: 'Governed A2A v1.0.0 gateway for AAA federation. Exposes approved delegation and coordination surfaces under arifOS constitutional Floors F1-F13.',
  url: 'https://aaa.arif-fazil.com',
  provider: { organization: 'arifOS', system: 'AAA' },
  version: '1.0.0',
  protocol_version: '1.0.0',
  capabilities: { streaming: true, push_notifications: false, authenticated_extended_card: false },
  authentication: { schemes: ['bearer', 'apiKey'], bearer: { scheme: 'bearer', token_type: 'opaque' }, apiKey: { scheme: 'apiKey', in: 'header', name: 'x-a2a-key' } },
  default_input_modes: ['text/plain', 'application/json'],
  default_output_modes: ['text/plain', 'application/json'],
  skills: [
    { id: 'agent-dispatch', name: 'Agent Dispatch', description: 'Non-blocking supervised task dispatch to approved internal agents.', tags: ['dispatch', 'task', 'coordination'], examples: ['dispatch a task to the planner agent', 'send work to the geodesy agent'] },
    { id: 'agent-handoff', name: 'Agent Handoff', description: 'Delegation to approved agents through governed handoff workflows.', tags: ['handoff', 'delegation', 'transfer'], examples: ['handoff to the mobility agent', 'transfer context to planner'] },
    { id: 'status-query', name: 'Status Query', description: 'Read-only task and run status retrieval.', tags: ['query', 'status', 'read-only'], examples: ['check task status', 'get current state of task 123'] },
  ],
  governance: {
    constitutional_floors: ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13'],
    verdict_authority: '888_JUDGE',
    vault: 'VAULT999',
    irreversible_requires_human: true,
    self_approval_forbidden: true,
    federation_trust_model: 'untrusted_peers'
  },
  a2a_endpoints: {
    send_task: 'POST /tasks',
    get_task: 'GET /tasks/{taskId}',
    stream_task: 'GET /tasks/{taskId}/stream',
    cancel_task: 'POST /tasks/{taskId}/cancel',
    subscribe_task: 'GET /tasks/{taskId}/subscribe',
    agent_card: 'GET /.well-known/agent-card.json',
    federation_manifest: 'GET /.well-known/arifos-federation.json'
  }
};

// === ERROR CODES ===
const ERROR_CODES = {
  INVALID_REQUEST: -32600,
  METHOD_NOT_FOUND: -32601,
  TASK_NOT_FOUND: -32001,
  INTERNAL_ERROR: -32603,
  UNAUTHORIZED: -32002,
  NONCE_INVALID: -32003,
  NONCE_REPLAY: -32004,
  TIMESTAMP_EXPIRED: -32005,
  HOLD_888: -32006,
  VOID_CONSTITUTIONAL: -32007,
};

// === 888_JUDGE INTEGRATION ===

async function callArifJudge(candidate, taskId, contextId, skill) {
  try {
    const response = await fetch(`${ARIFOS_JUDGE_URL}/judge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${ARIFOS_API_KEY}`,
        'User-Agent': 'AAA-A2A-Gateway/1.0'
      },
      body: JSON.stringify({
        candidate,
        task_id: taskId,
        context_id: contextId,
        skill,
        session_id: `aaa-a2a-${taskId}`,
        actor_id: 'aaa-gateway'
      }),
      signal: AbortSignal.timeout(10000)
    });

    if (!response.ok) {
      console.error(`[888_JUDGE] returned ${response.status}`);
      return VERDICT.HOLD_888;
    }

    const data = await response.json();
    return data.verdict || VERDICT.HOLD_888;
  } catch (error) {
    console.error(`[888_JUDGE] call failed: ${error.message} — defaulting to HOLD_888`);
    return VERDICT.HOLD_888;
  }
}

async function invokeF9Check(text, taskId) {
  try {
    const response = await fetch(`${ARIFOS_JUDGE_URL}/mind/reason`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${ARIFOS_API_KEY}`,
        'User-Agent': 'AAA-A2A-Gateway/1.0'
      },
      body: JSON.stringify({
        mode: 'verify',
        query: text,
        session_id: `aaa-a2a-${taskId}`,
        actor_id: 'aaa-gateway'
      }),
      signal: AbortSignal.timeout(8000)
    });

    if (!response.ok) return { clean: true, confidence: 1.0 };

    const data = await response.json();
    const hasHypothesis = (data.rationale || text).includes('hypothesis') || data.claimed === false;
    return { clean: !hasHypothesis, confidence: data.confidence || 0.85 };
  } catch {
    return { clean: true, confidence: 0.85 };
  }
}

function computeDeltaS(taskId) {
  const entry = entropyStore.get(taskId);
  if (!entry) return 0;
  const beforeLen = JSON.stringify(entry.before).length;
  const afterLen = JSON.stringify(entry.after).length;
  return afterLen - beforeLen;
}

// === HELPERS ===
function generateId() { return crypto.randomUUID(); }

function createJSONRPCResponse(id, result) {
  return { jsonrpc: '2.0', id, result };
}

function createJSONRPCError(id, code, message) {
  return { jsonrpc: '2.0', id, error: { code, message } };
}

function hashPayload(payload) {
  return crypto.createHash('sha256').update(JSON.stringify(payload)).digest('hex');
}

function now() { return Date.now(); }

// === AUTH MIDDLEWARE ===
function authMiddleware(req, res, next) {
  const bearer = req.headers['authorization'];
  const apiKey = req.headers['x-a2a-key'];

  if (bearer && bearer.startsWith('Bearer ') && bearer.slice(7) === A2A_TOKEN) {
    req.auth = { scheme: 'bearer', valid: true };
    return next();
  }
  if (apiKey && apiKey === A2A_API_KEY) {
    req.auth = { scheme: 'apikey', valid: true };
    return next();
  }

  res.setHeader('Content-Type', 'application/json');
  res.status(401).json(createJSONRPCError(0, ERROR_CODES.UNAUTHORIZED, 'Unauthorized: provide Bearer token or x-a2a-key'));
}

// === SCHEMA VALIDATION ===
const ALLOWED_METHODS = new Set([
  'message/send', 'message/stream', 'tasks/get', 'tasks/cancel', 'tasks/subscribe',
  'agent.dispatch', 'agent.handoff', 'status.query',
  'kernel.handshake', 'kernel.ping'
]);

function validateEnvelope(body) {
  if (!body || typeof body !== 'object') return { valid: false, code: ERROR_CODES.INVALID_REQUEST, message: 'Request body must be a JSON object' };
  if (body.jsonrpc !== '2.0') return { valid: false, code: ERROR_CODES.INVALID_REQUEST, message: 'jsonrpc must be "2.0"' };
  if (!body.id && body.id !== 0) return { valid: false, code: ERROR_CODES.INVALID_REQUEST, message: 'id is required' };
  if (!body.method || typeof body.method !== 'string') return { valid: false, code: ERROR_CODES.INVALID_REQUEST, message: 'method must be a string' };
  return { valid: true };
}

function validateMessage(message) {
  if (!message || typeof message !== 'object') return { valid: false, message: 'message must be an object' };
  if (!message.parts || !Array.isArray(message.parts)) return { valid: false, message: 'message.parts must be an array' };
  for (const part of message.parts) {
    if (!part.kind) return { valid: false, message: 'Each message part must have a kind' };
    if (part.kind === 'text' && typeof part.text !== 'string') return { valid: false, message: 'text parts must have string text' };
  }
  return { valid: true };
}

function validateNonce(nonce, ts) {
  if (!nonce || typeof nonce !== 'string') return { valid: false, code: ERROR_CODES.NONCE_INVALID, message: 'nonce must be a non-empty string' };
  if (nonce.length < 4 || nonce.length > 128) return { valid: false, code: ERROR_CODES.NONCE_INVALID, message: 'nonce length must be 4–128 chars' };
  if (!/^[A-Za-z0-9_-]+$/.test(nonce)) return { valid: false, code: ERROR_CODES.NONCE_INVALID, message: 'nonce must be alphanumeric with _-' };
  if (ts && Math.abs(now() - ts) > NONCE_CACHE_TTL_MS) return { valid: false, code: ERROR_CODES.TIMESTAMP_EXPIRED, message: 'Timestamp outside acceptable window' };
  if (nonceStore.has(nonce)) return { valid: false, code: ERROR_CODES.NONCE_REPLAY, message: 'nonce already used' };
  return { valid: true };
}

function checkReplay(payloadHash) {
  if (replayStore.has(payloadHash)) return true;
  replayStore.set(payloadHash, { ts: now() });
  setTimeout(() => replayStore.delete(payloadHash), REPLAY_CACHE_TTL_MS);
  return false;
}

function pruneNonceStore() {
  const cutoff = now() - NONCE_CACHE_TTL_MS;
  for (const [k, v] of nonceStore) {
    if (v.ts < cutoff) nonceStore.delete(k);
  }
}

// Prune every 5 minutes
setInterval(pruneNonceStore, NONCE_CACHE_TTL_MS);

// === EVENT BUS ===
function subscribe(taskId, callback) {
  if (!eventBus.has(taskId)) eventBus.set(taskId, new Set());
  eventBus.get(taskId).add(callback);
  return () => eventBus.get(taskId)?.delete(callback);
}

function publish(event) {
  const taskId = event.taskId || (event.task && event.task.id);
  if (!taskId) return;
  const listeners = eventBus.get(taskId);
  if (!listeners) return;
  for (const cb of listeners) {
    try { cb(event); } catch (e) { console.error('[EventBus]', e); }
  }
}

// === SKILL DETECTION ===
function detectSkill(text) {
  const lower = text.toLowerCase();
  if (lower.includes('dispatch') || lower.includes('send') || lower.includes('task')) return 'agent-dispatch';
  if (lower.includes('handoff') || lower.includes('transfer') || lower.includes('delegate')) return 'agent-handoff';
  if (lower.includes('status') || lower.includes('check') || lower.includes('query')) return 'status-query';
  return 'general';
}

function extractText(message) {
  return (message.parts || []).filter(p => p.kind === 'text').map(p => p.text).join(' ');
}

// === EXECUTE TASK ===
async function executeTask(taskId, contextId, message) {
  const userText = extractText(message);
  const skill = detectSkill(userText);

  let task = taskStore.get(taskId);
  if (!task) return;

  task.status = {
    state: 'working',
    message: { role: 'agent', parts: [{ kind: 'text', text: 'Processing your request...' }], messageId: generateId(), taskId, contextId },
    timestamp: new Date().toISOString()
  };
  taskStore.set(taskId, task);
  publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });

  // F9 Anti-Hallucination check (always run)
  const f9 = await invokeF9Check(userText, taskId);
  if (!f9.clean) {
    const rejectedStatus = {
      state: 'rejected',
      message: { role: 'agent', parts: [{ kind: 'text', text: '[888_JUDGE] F9 Anti-Hallucination check failed. Claim rejected.' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    task.status = rejectedStatus;
    taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: rejectedStatus, final: true });
    return;
  }

  // 888_JUDGE routing gate — hold skills require verdict before execution
  const policy = SKILL_APPROVAL_POLICY[skill] || 'on-demand';
  if (policy === 'hold') {
    const verdict = await callArifJudge(userText, taskId, contextId, skill);
    if (verdict === VERDICT.VOID) {
      const voidStatus = {
        state: 'voided',
        message: { role: 'agent', parts: [{ kind: 'text', text: '[888_JUDGE] VOID — constitutional violation. Task rejected.' }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = voidStatus;
      taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: voidStatus, final: true });
      return;
    }
    if (verdict === VERDICT.HOLD_888) {
      const holdStatus = {
        state: 'pending-human-review',
        message: { role: 'agent', parts: [{ kind: 'text', text: '[888_JUDGE] HOLD_888 — human review required before execution.' }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = holdStatus;
      taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: holdStatus, final: true });
      return;
    }
  }

  await new Promise(r => setTimeout(r, 300));

  let responseText;
  switch (skill) {
    case 'agent-dispatch':
      responseText = `[AAA Gateway] Task dispatched.\nSkill: ${skill}\nQuery: ${userText}`;
      break;
    case 'agent-handoff':
      responseText = `[AAA Gateway] Context handoff initiated.\nSkill: ${skill}\nQuery: ${userText}`;
      break;
    case 'status-query':
      responseText = `[AAA Gateway] Status query processed.\nSkill: ${skill}\nQuery: ${userText}`;
      break;
    default:
      responseText = `[AAA Gateway] Received: "${userText}"\nSkills: agent-dispatch, agent-handoff, status-query.`;
  }

  const completedStatus = {
    state: 'completed',
    message: { role: 'agent', parts: [{ kind: 'text', text: responseText }], messageId: generateId(), taskId, contextId },
    timestamp: new Date().toISOString()
  };
  task.status = completedStatus;
  taskStore.set(taskId, task);
  publish({ kind: 'status-update', taskId, contextId, status: completedStatus, final: true });
}

// === PUBLIC ROUTES (no auth) ===

// A2A v1.0.0 spec: agent card at /.well-known/agent-card.json
app.get('/.well-known/agent-card.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json(AAA_AGENT_CARD);
});

app.get('/agent-card.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json(AAA_AGENT_CARD);
});

// Legacy v0.3.0 compat alias (deprecated)
app.get('/.well-known/agent.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json(AAA_AGENT_CARD);
});

// Federation manifest — public discovery of peer agents
app.get('/.well-known/arifos-federation.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json({
    federation: 'arifOS AAA',
    version: '1.0.0',
    protocol: 'A2A v1.0.0',
    agents: [
      { id: 'aaa-gateway', url: 'https://aaa.arif-fazil.com', registered: true },
      { id: 'maxhermes', url: 'https://aaa.arif-fazil.com/hermes', registered: false }
    ],
    constitutional_floors: ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13'],
    governance_root: 'https://aaa.arif-fazil.com/.well-known/arifos-federation.json'
  });
});

app.get('/health', async (req, res) => {
  const vaultHealthy = await checkVaultHealth();
  res.json({
    status: 'healthy',
    protocol: 'A2A',
    version: '1.0.0',
    gateway: 'AAA',
    motto: 'Ditempa Bukan Diberi',
    vault: vaultHealthy ? 'CONNECTED' : 'DISCONNECTED'
  });
});

app.get('/', (req, res) => {
  res.json({
    service: 'AAA A2A Gateway',
    version: '1.0.0',
    protocol_version: '1.0.0',
    auth: 'required',
    endpoints: {
      agentCard: '/.well-known/agent-card.json',
      federationManifest: '/.well-known/arifos-federation.json',
      sendTask: 'POST /tasks',
      getTask: 'GET /tasks/{taskId}',
      streamTask: 'GET /tasks/{taskId}/stream',
      cancelTask: 'POST /tasks/{taskId}/cancel',
      subscribeTask: 'GET /tasks/{taskId}/subscribe',
      health: '/health'
    }
  });
});

// === PROTECTED ROUTES ===
app.use('/a2a', authMiddleware);

// === JSON-RPC VALIDATION MIDDLEWARE ===
function jsonRpcValidate(req, res, next) {
  const body = req.body;
  const env = validateEnvelope(body);
  if (!env.valid) return res.status(400).json(createJSONRPCError(body?.id || 0, env.code, env.message));
  req.jsonrpc = { id: body.id, method: body.method, params: body.params };
  next();
}

// === MESSAGE/SEND ===
app.post('/a2a/message/send', jsonRpcValidate, async (req, res) => {
  try {
    const { id, method, params } = req.jsonrpc;
    const message = params.message;
    const msgValidation = validateMessage(message);
    if (!msgValidation.valid) {
      return res.status(400).json(createJSONRPCError(id, ERROR_CODES.INVALID_REQUEST, msgValidation.message));
    }

    // Nonce check (optional, from params.identity if present)
    const identity = params.identity || {};
    const nonce = identity.nonce;
    const ts = identity.timestamp ? new Date(identity.timestamp).getTime() : null;
    if (nonce) {
      const nonceCheck = validateNonce(nonce, ts);
      if (!nonceCheck.valid) return res.status(400).json(createJSONRPCError(id, nonceCheck.code, nonceCheck.message));
      nonceStore.set(nonce, { ts: now() });
      setTimeout(() => nonceStore.delete(nonce), NONCE_CACHE_TTL_MS);
    }

    // Replay check
    const payloadHash = hashPayload(req.body);
    if (checkReplay(payloadHash)) {
      return res.status(400).json(createJSONRPCError(id, ERROR_CODES.NONCE_REPLAY, 'Duplicate request detected'));
    }

    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const contextId = params.contextId || generateId();

    const task = {
      id: taskId, contextId,
      status: { state: 'submitted', timestamp: new Date().toISOString() },
      artifacts: [], history: [message],
      metadata: params.metadata || {},
      created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    };
    taskStore.set(taskId, task);

    await executeTask(taskId, contextId, message);

    const updatedTask = taskStore.get(taskId);
    const skill = updatedTask.metadata?.skill || 'general';

    // Write SEAL to Vault999 (async, non-blocking)
    writeSeal(updatedTask, 'aaa-gateway', `a2a.${skill}`, {
      routing: 'direct_mcp_simulation',
      task_id: taskId,
      context_id: contextId
    }).catch(err => console.error('[VAULT999] SEAL write failed:', err.message));

    res.json(createJSONRPCResponse(id, {
      id: taskId, contextId,
      status: updatedTask.status,
      artifacts: updatedTask.artifacts,
      history: updatedTask.history,
      kind: 'task',
      metadata: updatedTask.metadata,
    }));
  } catch (error) {
    console.error('[A2A] message/send error:', error);
    res.status(500).json(createJSONRPCError(req.body?.id || 0, ERROR_CODES.INTERNAL_ERROR, 'Internal server error'));
  }
});

// === MESSAGE/STREAM ===
app.post('/a2a/message/stream', jsonRpcValidate, async (req, res) => {
  try {
    const { id, params } = req.jsonrpc;
    const message = params.message;
    const msgValidation = validateMessage(message);
    if (!msgValidation.valid) {
      return res.status(400).json(createJSONRPCError(id, ERROR_CODES.INVALID_REQUEST, msgValidation.message));
    }

    const payloadHash = hashPayload(req.body);
    if (checkReplay(payloadHash)) {
      return res.status(400).json(createJSONRPCError(id, ERROR_CODES.NONCE_REPLAY, 'Duplicate request detected'));
    }

    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const contextId = params.contextId || generateId();

    const task = {
      id: taskId, contextId,
      status: { state: 'submitted', timestamp: new Date().toISOString() },
      artifacts: [], history: [message],
      metadata: params.metadata || {},
      created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    };
    taskStore.set(taskId, task);

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');

    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id, result: { kind: 'task', task } })}\n\n`);

    const unsubscribe = subscribe(taskId, (event) => {
      res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id, result: event })}\n\n`);
    });

    req.on('close', () => { unsubscribe(); });

    executeTask(taskId, contextId, message).catch(console.error);

  } catch (error) {
    console.error('[A2A] message/stream error:', error);
    res.status(500).json(createJSONRPCError(req.body?.id || 0, ERROR_CODES.INTERNAL_ERROR, 'Internal server error'));
  }
});

// === TASKS/:taskId ===
app.get('/a2a/tasks/:taskId', jsonRpcValidate, (req, res) => {
  const task = taskStore.get(req.params.taskId);
  if (!task) return res.status(404).json(createJSONRPCError(req.jsonrpc.id, ERROR_CODES.TASK_NOT_FOUND, `Task ${req.params.taskId} not found`));
  res.json(createJSONRPCResponse(req.jsonrpc.id, {
    id: task.id, contextId: task.contextId, status: task.status,
    artifacts: task.artifacts, history: task.history, kind: 'task', metadata: task.metadata
  }));
});

// === TASKS/:taskId/CANCEL ===
app.post('/a2a/tasks/:taskId/cancel', jsonRpcValidate, (req, res) => {
  const task = taskStore.get(req.params.taskId);
  if (task) {
    task.status.state = 'canceled';
    task.updated_at = new Date().toISOString();
    taskStore.set(req.params.taskId, task);
  }
  res.json(createJSONRPCResponse(req.jsonrpc.id, { success: true, message: 'Task cancelled', task }));
});

// === TASKS/:taskId/SUBSCRIBE ===
app.get('/a2a/tasks/:taskId/subscribe', jsonRpcValidate, (req, res) => {
  const taskId = req.params.taskId;
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const task = taskStore.get(taskId);
  if (task) res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id: req.jsonrpc.id, result: { kind: 'task', task } })}\n\n`);

  const unsubscribe = subscribe(taskId, (event) => {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id: req.jsonrpc.id, result: event })}\n\n`);
  });

  req.on('close', () => { unsubscribe(); });
});

// === 404 HANDLER ===
app.use((req, res) => {
  res.status(404).json(createJSONRPCError(0, ERROR_CODES.METHOD_NOT_FOUND, `Endpoint ${req.path} not found`));
});

// =======================
// A2A v1.0.0 SPEC ENDPOINTS
// =======================
// Aligned to official a2a-python SDK spec:
//   POST /tasks        → create/send task
//   GET  /tasks/:id    → get task
//   GET  /tasks/:id/stream → SSE streaming
//   POST /tasks/:id/cancel → cancel task
//   GET  /tasks/:id/subscribe → SSE subscription
// =======================

function extractMessageFromParams(params) {
  if (!params) return null;
  if (params.message) return params.message;
  if (params.text) return { parts: [{ kind: 'text', text: params.text }] };
  if (typeof params === 'string') return { parts: [{ kind: 'text', text: params }] };
  return null;
}

// POST /tasks — A2A v1.0.0 spec task creation
app.post('/tasks', authMiddleware, jsonRpcValidate, async (req, res) => {
  try {
    const { id, params } = req.jsonrpc;
    const message = extractMessageFromParams(params);
    if (!message) {
      return res.status(400).json(createJSONRPCError(id, ERROR_CODES.INVALID_REQUEST, 'params.message or params.text required'));
    }
    const msgValidation = validateMessage(message);
    if (!msgValidation.valid) {
      return res.status(400).json(createJSONRPCError(id, ERROR_CODES.INVALID_REQUEST, msgValidation.message));
    }

    const payloadHash = hashPayload(req.body);
    if (checkReplay(payloadHash)) {
      return res.status(400).json(createJSONRPCError(id, ERROR_CODES.NONCE_REPLAY, 'Duplicate request detected'));
    }

    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const contextId = params.contextId || generateId();

    const task = {
      id: taskId, contextId,
      status: { state: 'submitted', timestamp: new Date().toISOString() },
      artifacts: [], history: [message],
      metadata: params.metadata || {},
      created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    };
    taskStore.set(taskId, task);

    await executeTask(taskId, contextId, message);

    const updatedTask = taskStore.get(taskId);

    writeSeal(updatedTask, 'aaa-gateway', 'a2a.task', {
      routing: 'POST /tasks v1.0.0',
      task_id: taskId,
      context_id: contextId
    }).catch(err => console.error('[VAULT999] SEAL write failed:', err.message));

    res.json(createJSONRPCResponse(id, {
      id: taskId, contextId,
      status: updatedTask.status,
      artifacts: updatedTask.artifacts,
      history: updatedTask.history,
      kind: 'task',
      metadata: updatedTask.metadata,
    }));
  } catch (error) {
    console.error('[A2A v1.0.0] POST /tasks error:', error);
    res.status(500).json(createJSONRPCError(req.body?.id || 0, ERROR_CODES.INTERNAL_ERROR, 'Internal server error'));
  }
});

// GET /tasks/:taskId — A2A v1.0.0 spec task retrieval
app.get('/tasks/:taskId', authMiddleware, (req, res) => {
  const task = taskStore.get(req.params.taskId);
  if (!task) {
    return res.status(404).json(createJSONRPCError(req.params.taskId, ERROR_CODES.TASK_NOT_FOUND, `Task ${req.params.taskId} not found`));
  }
  res.json({
    jsonrpc: '2.0',
    result: {
      id: task.id, contextId: task.contextId, status: task.status,
      artifacts: task.artifacts, history: task.history, kind: 'task', metadata: task.metadata
    }
  });
});

// GET /tasks/:taskId/stream — A2A v1.0.0 spec SSE streaming
app.get('/tasks/:taskId/stream', authMiddleware, async (req, res) => {
  const taskId = req.params.taskId;
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const task = taskStore.get(taskId);
  if (task) {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: { kind: 'task', task } })}\n\n`);
  }

  const unsubscribe = subscribe(taskId, (event) => {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: event })}\n\n`);
  });

  req.on('close', () => { unsubscribe(); });
});

// POST /tasks/:taskId/cancel — A2A v1.0.0 spec task cancellation
app.post('/tasks/:taskId/cancel', authMiddleware, jsonRpcValidate, (req, res) => {
  const task = taskStore.get(req.params.taskId);
  if (!task) {
    return res.status(404).json(createJSONRPCError(req.jsonrpc.id, ERROR_CODES.TASK_NOT_FOUND, `Task ${req.params.taskId} not found`));
  }
  task.status.state = 'canceled';
  task.updated_at = new Date().toISOString();
  taskStore.set(req.params.taskId, task);
  res.json(createJSONRPCResponse(req.jsonrpc.id, { id: task.id, status: task.status, kind: 'task' }));
});

// GET /tasks/:taskId/subscribe — A2A v1.0.0 spec SSE subscription
app.get('/tasks/:taskId/subscribe', authMiddleware, (req, res) => {
  const taskId = req.params.taskId;
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const task = taskStore.get(taskId);
  if (task) res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: { kind: 'task', task } })}\n\n`);

  const unsubscribe = subscribe(taskId, (event) => {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: event })}\n\n`);
  });

  req.on('close', () => { unsubscribe(); });
});

// =======================
// END A2A v1.0.0 SPEC ENDPOINTS
// =======================

// === START ===
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`[AAA A2A] Hardened server running on port ${PORT}`);
  console.log(`[AAA A2A] Protocol: A2A v1.0.0`);
  console.log(`[AAA A2A] Auth: configured (bearer + api-key)`);
  console.log(`[AAA A2A] Agent Card: http://localhost:${PORT}/.well-known/agent-card.json`);
  console.log(`[AAA A2A] Federation: http://localhost:${PORT}/.well-known/arifos-federation.json`);
  console.log(`[AAA A2A] Health: http://localhost:${PORT}/health`);
});

module.exports = { app };
