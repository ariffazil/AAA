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
const A2A_TOKEN = process.env.A2A_TOKEN || 'aaa-a2a-token-dev';      // Bearer token
const A2A_API_KEY = process.env.A2A_API_KEY || 'aaa-a2a-apikey-dev'; // x-a2a-key
const NONCE_CACHE_TTL_MS = 5 * 60 * 1000; // 5-minute nonce window
const REPLAY_CACHE_TTL_MS = 30 * 60 * 1001; // 30-minute replay window

// === IN-MEMORY STORES ===
const taskStore = new Map();
const eventBus = new Map();
const nonceStore = new Map();   // nonce → { ts, used }
const replayStore = new Map();   // payloadHash → { ts }

// === A2A Agent Card ===
const AAA_AGENT_CARD = {
  protocol_version: '0.3.0',
  id: 'aaa-gateway',
  name: 'AAA Gateway',
  description: 'Governed agent gateway for AAA. Exposes only approved delegation and coordination surfaces.',
  url: 'https://aaa.arif-fazil.com/a2a',
  preferred_transport: 'jsonrpc-https',
  additional_interfaces: [{
    transport: 'sse',
    url: 'https://aaa.arif-fazil.com/a2a/subscribe'
  }],
  provider: { organization: 'arifOS', system: 'AAA', runtime: 'OpenClaw' },
  version: '0.1.0',
  capabilities: { streaming: true, push_notifications: false, authenticated_extended_card: false },
  security_schemes: [
    { id: 'gateway-token', type: 'bearer', description: 'Gateway bearer token for internal trusted peers.' },
    { id: 'api-key', type: 'apiKey', description: 'API key for fixed infrastructure peers.' },
  ],
  security: [['gateway-token'], ['api-key']],
  default_input_modes: ['text/plain', 'application/json'],
  default_output_modes: ['text/plain', 'application/json'],
  skills: [
    { id: 'agent-dispatch', name: 'Agent Dispatch', description: 'Non-blocking supervised task dispatch to approved internal agents.', tags: ['dispatch', 'task', 'coordination'], examples: ['dispatch a task to the planner agent', 'send work to the geodesy agent'] },
    { id: 'agent-handoff', name: 'Agent Handoff', description: 'Delegation to approved agents through governed handoff workflows.', tags: ['handoff', 'delegation', 'transfer'], examples: ['handoff to the mobility agent', 'transfer context to planner'] },
    { id: 'status-query', name: 'Status Query', description: 'Read-only task and run status retrieval.', tags: ['query', 'status', 'read-only'], examples: ['check task status', 'get current state of task 123'] },
  ],
  supports_authenticated_extended_card: false,
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
};

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
app.get('/.well-known/agent.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json(AAA_AGENT_CARD);
});

app.get('/agent.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json(AAA_AGENT_CARD);
});

app.get('/health', async (req, res) => {
  const vaultHealthy = await checkVaultHealth();
  res.json({
    status: 'healthy',
    protocol: 'A2A',
    version: '0.3.0',
    gateway: 'AAA',
    motto: 'Ditempa Bukan Diberi',
    vault: vaultHealthy ? 'CONNECTED' : 'DISCONNECTED'
  });
});

app.get('/', (req, res) => {
  res.json({
    service: 'AAA A2A Gateway',
    version: '0.1.0',
    auth: 'required',
    endpoints: {
      agentCard: '/.well-known/agent.json',
      messageSend: '/message/send',
      messageStream: '/message/stream',
      tasks: '/tasks/:taskId',
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

// === START ===
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`[AAA A2A] Hardened server running on port ${PORT}`);
  console.log(`[AAA A2A] Auth: configured (bearer + api-key)`);
  console.log(`[AAA A2A] Agent Card: http://localhost:${PORT}/.well-known/agent.json`);
  console.log(`[AAA A2A] Health: http://localhost:${PORT}/health`);
});

module.exports = { app };
