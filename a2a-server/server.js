#!/usr/bin/env node
/**
 * A2A Server for AAA Gateway
 * Standalone production server - no build step required
 * 
 * Usage: node server.js [--port 3001]
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// In-memory stores
const taskStore = new Map();
const eventBus = new Map();

// A2A Agent Card
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
    { id: 'gateway-token', type: 'bearer', description: 'Gateway bearer token for internal trusted peers.' },
    { id: 'oauth2', type: 'oauth2', description: 'OAuth/OIDC for user-linked or federated callers.' },
    { id: 'api-key', type: 'apiKey', description: 'API key for fixed infrastructure peers.' },
  ],
  security: [['gateway-token'], ['oauth2'], ['api-key']],
  default_input_modes: ['text/plain', 'application/json'],
  default_output_modes: ['text/plain', 'application/json'],
  skills: [
    { id: 'agent-dispatch', name: 'Agent Dispatch', description: 'Non-blocking supervised task dispatch to approved internal agents.', tags: ['dispatch', 'task', 'coordination'], examples: ['dispatch a task to the planner agent', 'send work to the geodesy agent'] },
    { id: 'agent-handoff', name: 'Agent Handoff', description: 'Delegation to approved agents through governed handoff workflows.', tags: ['handoff', 'delegation', 'transfer'], examples: ['handoff to the mobility agent', 'transfer context to planner'] },
    { id: 'status-query', name: 'Status Query', description: 'Read-only task and run status retrieval.', tags: ['query', 'status', 'read-only'], examples: ['check task status', 'get current state of task 123'] },
  ],
  supports_authenticated_extended_card: false,
};

const EXTENDED_AGENT_CARD = {
  ...AAA_AGENT_CARD,
  description: 'AAA Gateway with full capabilities. arifOS F1-F13 constitutional floors.',
  capabilities: { streaming: true, push_notifications: true, authenticated_extended_card: true },
};

function generateId() {
  return crypto.randomUUID();
}

function createJSONRPCResponse(id, result) {
  return { jsonrpc: '2.0', id, result };
}

function createJSONRPCError(id, code, message) {
  return { jsonrpc: '2.0', id, error: { code, message } };
}

const ERROR_CODES = {
  INVALID_REQUEST: -32600,
  METHOD_NOT_FOUND: -32601,
  TASK_NOT_FOUND: -32001,
  INTERNAL_ERROR: -32603,
};

// Event bus helpers
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

// Skill detection
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

// Execute task
async function executeTask(taskId, contextId, message) {
  const userText = extractText(message);
  const skill = detectSkill(userText);

  let task = taskStore.get(taskId);
  if (!task) return;

  // Update to working
  task.status = { state: 'working', message: { role: 'agent', parts: [{ kind: 'text', text: 'Processing your request...' }], messageId: generateId(), taskId, contextId }, timestamp: new Date().toISOString() };
  taskStore.set(taskId, task);
  publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });

  // Simulate processing
  await new Promise(r => setTimeout(r, 300));

  // Build response
  let responseText;
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
      responseText = `[AAA Gateway] Received: "${userText}"\nThis is an A2A-enabled AAA gateway. Skills: agent-dispatch, agent-handoff, status-query.`;
  }

  const completedStatus = { state: 'completed', message: { role: 'agent', parts: [{ kind: 'text', text: responseText }], messageId: generateId(), taskId, contextId }, timestamp: new Date().toISOString() };
  task.status = completedStatus;
  taskStore.set(taskId, task);
  publish({ kind: 'status-update', taskId, contextId, status: completedStatus, final: true });
}

// Routes
app.get('/.well-known/agent.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json(AAA_AGENT_CARD);
});

app.get('/agent.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json(AAA_AGENT_CARD);
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    protocol: 'A2A',
    version: '0.3.0',
    gateway: 'AAA',
    motto: 'Ditempa Bukan Diberi'
  });
});

app.get('/', (req, res) => {
  res.json({
    service: 'AAA A2A Gateway',
    version: '0.1.0',
    endpoints: {
      agentCard: '/.well-known/agent.json',
      messageSend: '/message/send',
      messageStream: '/message/stream',
      tasks: '/tasks/:taskId',
      health: '/health'
    }
  });
});

app.post('/message/send', async (req, res) => {
  try {
    const { jsonrpc, id, method, params } = req.body;
    if (jsonrpc !== '2.0') return res.status(400).json(createJSONRPCError(id || 0, ERROR_CODES.INVALID_REQUEST, 'Invalid JSON-RPC version'));

    const message = params.message;
    if (!message) return res.status(400).json(createJSONRPCError(id || 0, ERROR_CODES.INVALID_REQUEST, 'message is required'));

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

    // Execute synchronously
    await executeTask(taskId, contextId, message);

    const updatedTask = taskStore.get(taskId);
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

app.post('/message/stream', async (req, res) => {
  try {
    const { jsonrpc, id, method, params } = req.body;
    if (jsonrpc !== '2.0') return res.status(400).json(createJSONRPCError(id || 0, ERROR_CODES.INVALID_REQUEST, 'Invalid JSON-RPC version'));

    const message = params.message;
    if (!message) return res.status(400).json(createJSONRPCError(id || 0, ERROR_CODES.INVALID_REQUEST, 'message is required'));

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

    // Send initial task event
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id, result: { kind: 'task', task } })}\n\n`);

    const unsubscribe = subscribe(taskId, (event) => {
      res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id, result: event })}\n\n`);
    });

    req.on('close', () => { unsubscribe(); });

    // Execute async
    executeTask(taskId, contextId, message).catch(console.error);

  } catch (error) {
    console.error('[A2A] message/stream error:', error);
    res.status(500).json(createJSONRPCError(req.body?.id || 0, ERROR_CODES.INTERNAL_ERROR, 'Internal server error'));
  }
});

app.get('/tasks/:taskId', (req, res) => {
  const task = taskStore.get(req.params.taskId);
  if (!task) return res.status(404).json(createJSONRPCError(0, ERROR_CODES.TASK_NOT_FOUND, `Task ${req.params.taskId} not found`));
  res.json(createJSONRPCResponse(0, { id: task.id, contextId: task.contextId, status: task.status, artifacts: task.artifacts, history: task.history, kind: 'task', metadata: task.metadata }));
});

app.post('/tasks/:taskId/cancel', (req, res) => {
  const task = taskStore.get(req.params.taskId);
  if (task) { task.status.state = 'canceled'; task.updated_at = new Date().toISOString(); taskStore.set(req.params.taskId, task); }
  res.json(createJSONRPCResponse(req.body?.id || 0, { success: true, message: 'Task cancelled', task }));
});

app.get('/tasks/:taskId/subscribe', (req, res) => {
  const taskId = req.params.taskId;
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const task = taskStore.get(taskId);
  if (task) res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id: 0, result: { kind: 'task', task } })}\n\n`);

  const unsubscribe = subscribe(taskId, (event) => {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id: 0, result: event })}\n\n`);
  });

  req.on('close', () => { unsubscribe(); });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json(createJSONRPCError(0, ERROR_CODES.METHOD_NOT_FOUND, `Endpoint ${req.path} not found`));
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`[AAA A2A] Server running on port ${PORT}`);
  console.log(`[AAA A2A] Agent Card: http://localhost:${PORT}/.well-known/agent.json`);
  console.log(`[AAA A2A] Health: http://localhost:${PORT}/health`);
});

module.exports = { app };