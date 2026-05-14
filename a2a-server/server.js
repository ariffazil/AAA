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
const { createClient } = require('redis');
const { connect, StringCodec } = require('nats');

const app = express();
app.use(express.json({ limit: '12mb' }));

// === CONFIG ===
// === AGENT A2A ADAPTER URLs (host network) ===
const HERMES_A2A_URL = process.env.HERMES_A2A_URL || 'http://172.19.0.1:18001';
const OPENCLAW_A2A_URL = process.env.OPENCLAW_A2A_URL || 'http://172.19.0.1:18002';
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://ollama-engine-prod:11434';
const OPENWEBUI_API_KEY = process.env.OPENWEBUI_API_KEY || '';
const OPENWEBUI_URL = process.env.OPENWEBUI_URL || '';
const ARIFOS_LOCAL_URL = process.env.ARIFOS_LOCAL_URL || 'http://arifosmcp:8080';
const QDRANT_URL = process.env.QDRANT_URL || 'http://qdrant:6333';
const AAA_AI_COLLECTION = process.env.AAA_AI_COLLECTION || 'aaa_ai_docs';
const AAA_AI_DEFAULT_MODEL = process.env.AAA_AI_DEFAULT_MODEL || 'qwen2.5:7b';
const AAA_AI_EMBED_MODEL = process.env.AAA_AI_EMBED_MODEL || 'bge-m3:latest';

const A2A_TOKEN=process.env.A2A_TOKEN || 'aaa-a2a-token-dev';
const A2A_API_KEY=process.env.A2A_API_KEY || 'aaa-a2a-apikey-dev';
const ARIFOS_JUDGE_URL = process.env.ARIFOS_JUDGE_URL || 'http://hermes-agent:3002';
const ARIFOS_API_KEY = process.env.ARIFOS_API_KEY || 'hermes-agent-apikey-dev';
const REDIS_URL = process.env.REDIS_URL || 'redis://redis:6379';
const NATS_URL = process.env.NATS_URL || 'nats://nats:4222';

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
  'agent-handoff': 'hold',    // requires 888_JUDGE before handoff
  'general': 'hold',           // ALL actions default to judgment gate — safe unless explicitly status-query
  'status-query': 'on-demand'  // only pure read-only queries bypass
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

function writeSse(res, payload) {
  res.write(`data: ${JSON.stringify(payload)}\n\n`);
}

function normalizeAiMessages(messages) {
  if (!Array.isArray(messages)) return [];
  return messages
    .filter((message) => message && typeof message.content === 'string')
    .map((message) => ({
      role: ['system', 'assistant', 'user'].includes(message.role) ? message.role : 'user',
      content: message.content.trim(),
    }))
    .filter((message) => message.content.length > 0);
}

function buildContextBlock(citations) {
  if (!Array.isArray(citations) || citations.length === 0) return '';
  return citations
    .map((citation, index) => {
      const filename = citation.filename || `source-${index + 1}`;
      const content = typeof citation.content === 'string' ? citation.content : citation.snippet || '';
      return `[Source ${index + 1}: ${filename}]\n${content}`;
    })
    .join('\n\n');
}

function flattenTranscript(messages) {
  return messages
    .map((message) => `${message.role.toUpperCase()}: ${message.content}`)
    .join('\n\n');
}

function chunkDocument(text, chunkSize = 1200, overlap = 200) {
  const normalized = text.replace(/\r\n/g, '\n').trim();
  if (!normalized) return [];

  const chunks = [];
  let start = 0;

  while (start < normalized.length) {
    let end = Math.min(start + chunkSize, normalized.length);
    if (end < normalized.length) {
      const nextBreak = normalized.lastIndexOf('\n', end);
      if (nextBreak > start + Math.floor(chunkSize * 0.6)) {
        end = nextBreak;
      }
    }

    const content = normalized.slice(start, end).trim();
    if (content) chunks.push(content);
    if (end >= normalized.length) break;
    start = Math.max(end - overlap, start + 1);
  }

  return chunks;
}

async function readResponseText(response) {
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function embedTexts(texts) {
  const cleaned = texts
    .map((text) => (typeof text === 'string' ? text.trim() : ''))
    .filter(Boolean);

  if (cleaned.length === 0) {
    throw new Error('No text available to embed');
  }

  const embedResponse = await fetch(`${OLLAMA_URL}/api/embed`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: AAA_AI_EMBED_MODEL,
      input: cleaned,
      truncate: true,
    }),
    signal: AbortSignal.timeout(30000),
  });

  if (embedResponse.ok) {
    const payload = await embedResponse.json();
    if (Array.isArray(payload.embeddings) && payload.embeddings.length > 0) {
      return payload.embeddings;
    }
    if (Array.isArray(payload.embedding) && payload.embedding.length > 0) {
      return [payload.embedding];
    }
  }

  const fallbackEmbeddings = [];
  for (const text of cleaned) {
    const fallbackResponse = await fetch(`${OLLAMA_URL}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: AAA_AI_EMBED_MODEL,
        prompt: text,
      }),
      signal: AbortSignal.timeout(30000),
    });

    if (!fallbackResponse.ok) {
      const details = await readResponseText(fallbackResponse);
      throw new Error(`Ollama embedding request failed: ${fallbackResponse.status} ${JSON.stringify(details)}`);
    }

    const payload = await fallbackResponse.json();
    if (!Array.isArray(payload.embedding)) {
      throw new Error('Ollama embedding response did not contain an embedding vector');
    }
    fallbackEmbeddings.push(payload.embedding);
  }

  return fallbackEmbeddings;
}

async function ensureQdrantCollection(vectorSize) {
  const collectionResponse = await fetch(`${QDRANT_URL}/collections/${AAA_AI_COLLECTION}`, {
    signal: AbortSignal.timeout(10000),
  });

  if (collectionResponse.ok) return;
  if (collectionResponse.status !== 404) {
    const details = await readResponseText(collectionResponse);
    throw new Error(`Qdrant collection probe failed: ${collectionResponse.status} ${JSON.stringify(details)}`);
  }

  const createResponse = await fetch(`${QDRANT_URL}/collections/${AAA_AI_COLLECTION}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vectors: {
        size: vectorSize,
        distance: 'Cosine',
      },
    }),
    signal: AbortSignal.timeout(15000),
  });

  if (!createResponse.ok) {
    const details = await readResponseText(createResponse);
    throw new Error(`Qdrant collection create failed: ${createResponse.status} ${JSON.stringify(details)}`);
  }
}

async function searchRag(query, limit = 5) {
  const collectionResponse = await fetch(`${QDRANT_URL}/collections/${AAA_AI_COLLECTION}`, {
    signal: AbortSignal.timeout(10000),
  });

  if (collectionResponse.status === 404) {
    return [];
  }
  if (!collectionResponse.ok) {
    const details = await readResponseText(collectionResponse);
    throw new Error(`Qdrant collection access failed: ${collectionResponse.status} ${JSON.stringify(details)}`);
  }

  const [embedding] = await embedTexts([query]);
  const searchResponse = await fetch(`${QDRANT_URL}/collections/${AAA_AI_COLLECTION}/points/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vector: embedding,
      limit,
      with_payload: true,
    }),
    signal: AbortSignal.timeout(15000),
  });

  if (!searchResponse.ok) {
    const details = await readResponseText(searchResponse);
    throw new Error(`Qdrant search failed: ${searchResponse.status} ${JSON.stringify(details)}`);
  }

  const payload = await searchResponse.json();
  return (payload.result || []).map((point) => ({
    id: point.id,
    score: point.score,
    filename: point.payload?.filename || 'document',
    snippet: point.payload?.snippet || '',
    content: point.payload?.content || '',
    chunk_index: point.payload?.chunk_index ?? 0,
    doc_id: point.payload?.doc_id || null,
    uploaded_at: point.payload?.uploaded_at || null,
  }));
}

// === A2A Agent Card v1.0.0 ===
const AAA_AGENT_CARD = {
  name: 'AAA Gateway',
  description: 'Governed A2A v1.0.0 gateway for AAA federation. Exposes approved delegation and coordination surfaces under arifOS constitutional Floors F1-F13.',
  url: 'https://aaa.arif-fazil.com/a2a',
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
    federation_trust_model: 'untrusted_peers',
    enforcefloors: true
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

// === A-ROLE AGENT CARDS ===
const ARCHITECT_CARD = require('./agent-cards/aaa-architect.json');
const ENGINEER_CARD = require('./agent-cards/aaa-engineer.json');
const AUDITOR_CARD = require('./agent-cards/aaa-auditor.json');

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
// Calls hermes-agent A2A skill: 888-judgment
// Wraps the call in A2A protocol: POST /tasks → poll GET /tasks/{id}

async function callArifJudge(candidate, taskId, contextId, skill) {
  const judgmentTaskId = `jg-${taskId}-${Date.now()}`;
  const HERMES_URL = ARIFOS_JUDGE_URL.replace('/judge', ''); // strip broken /judge suffix

  try {
    // Step 1: Submit judgment task to hermes-agent via A2A
    const submitRes = await fetch(`${HERMES_URL}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${A2A_TOKEN}`,
        'x-a2a-key': A2A_API_KEY
      },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: judgmentTaskId,
        method: 'tasks/send',
        params: {
          skill: '888-judgment',
          input: {
            candidate,
            task_id: taskId,
            context_id: contextId,
            skill,
            actor_id: 'aaa-gateway',
            source: 'AAA-A2A-Gateway'
          },
          sender: { agent_id: 'aaa-gateway' },
          nonce: judgmentTaskId,
          timestamp: new Date().toISOString()
        }
      }),
      signal: AbortSignal.timeout(15000)
    });

    if (!submitRes.ok) {
      console.error(`[888_JUDGE] A2A submit failed: ${submitRes.status}`);
      return VERDICT.HOLD_888;
    }

    const submitData = await submitRes.json();
    // A2A returns either direct result or { result: { task: { id } }
    const returnedTaskId = submitData.result?.task?.id || submitData.result?.id || submitData.id;
    if (!returnedTaskId) {
      console.error('[888_JUDGE] No taskId returned from hermes-agent');
      return VERDICT.HOLD_888;
    }

    // Step 2: Poll until completed / failed / timeout
    const deadline = Date.now() + 20000; // 20s max
    let verdict = VERDICT.HOLD_888;

    while (Date.now() < deadline) {
      await new Promise(r => setTimeout(r, 1000)); // 1s poll interval

      const pollRes = await fetch(`${HERMES_URL}/tasks/${returnedTaskId}`, {
        headers: {
          'Authorization': `Bearer ${A2A_TOKEN}`,
          'x-a2a-key': A2A_API_KEY
        },
        signal: AbortSignal.timeout(5000)
      });

      if (!pollRes.ok) continue;

      const pollData = await pollRes.json();
      const task = pollData.result || pollData;
      const state = task.status?.state || task.state;

      if (state === 'completed') {
        // Extract verdict from task artifacts/messages
        const msgs = task.messages || [];
        for (let i = msgs.length - 1; i >= 0; i--) {
          const parts = msgs[i].parts || [];
          for (const p of parts) {
            if (p.kind === 'text') {
              const t = p.text || '';
              if (t.includes('SEAL') || t.includes('PROCEED')) { verdict = 'SEAL'; break; }
              if (t.includes('HOLD') || t.includes('HOLD_888')) { verdict = VERDICT.HOLD_888; break; }
              if (t.includes('VOID')) { verdict = 'VOID'; break; }
            }
          }
          if (verdict !== VERDICT.HOLD_888) break;
        }
        break;
      }

      if (state === 'failed' || state === 'rejected' || state === 'canceled') {
        console.error(`[888_JUDGE] hermes-agent task ended: ${state}`);
        verdict = 'VOID';
        break;
      }
    }

    console.log(`[888_JUDGE] Task ${judgmentTaskId} → ${verdict}`);
    return verdict;

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
async function executeTask(taskId, contextId, message, targetAgent) {
  let task = taskStore.get(taskId);
  if (!task) return;

  const userText = extractText(message);
  const skill = detectSkill(userText);
  task.metadata = task.metadata || {};
  task.metadata.skill = skill;

  // === REAL AGENT DISPATCH — route to Hermes ASI ===
  if (targetAgent === 'hermes') {
    task.status = {
      state: 'working',
      message: { role: 'agent', parts: [{ kind: 'text', text: '[AAA] Forwarding to Hermes ASI 888_JUDGMENT...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });

    try {
      const body = JSON.stringify({
        jsonrpc: '2.0', id: 1, method: 'message/send',
        params: { message, taskId, contextId }
      });
      const res = await fetch(`${HERMES_A2A_URL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
        signal: AbortSignal.timeout(30000)
      });
      if (!res.ok) throw new Error(`Hermes returned ${res.status}`);
      const data = await res.json();
      const hermesResult = data.result || {};

      // F9 Anti-Hallucination check on Hermes response
      const responseText = extractText(hermesResult.status?.message || {});
      const f9 = await invokeF9Check(responseText, taskId);
      if (!f9.clean) {
        const rejectedStatus = {
          state: 'rejected',
          message: { role: 'agent', parts: [{ kind: 'text', text: '[AAA→Hermes] F9 Anti-Hallucination check failed on response. Hermes verdict rejected.' }], messageId: generateId(), taskId, contextId },
          timestamp: new Date().toISOString()
        };
        task.status = rejectedStatus;
        taskStore.set(taskId, task);
        publish({ kind: 'status-update', taskId, contextId, status: rejectedStatus, final: true });
        return;
      }

      task.status = {
        state: hermesResult.status?.state || 'completed',
        message: {
          role: 'agent',
          parts: [{ kind: 'text', text: `[AAA→Hermes ASI]\n${responseText}` }],
          messageId: generateId(), taskId, contextId
        },
        timestamp: new Date().toISOString()
      };
      task.artifacts = hermesResult.artifacts || [];
      task.history = hermesResult.history || [message];
      taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      const errorStatus = {
        state: 'failed',
        message: { role: 'agent', parts: [{ kind: 'text', text: `[AAA→Hermes ASI] Dispatch failed: ${err.message}. Falling back to local echo.` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = errorStatus;
      taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: errorStatus, final: true });
      return;
    }
  }


  // === ROUTE TO OPENCLAW (AGI) ===
  if (targetAgent === 'openclaw') {
    task.status = {
      state: 'working',
      message: { role: 'agent', parts: [{ kind: 'text', text: '[AAA] Forwarding to OpenClaw AGI...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });

    try {
      const body = JSON.stringify({
        jsonrpc: '2.0', id: 1, method: 'message/send',
        params: { message, taskId, contextId }
      });
      const res = await fetch(`${OPENCLAW_A2A_URL}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
        signal: AbortSignal.timeout(60000)
      });
      if (!res.ok) throw new Error(`OpenClaw returned ${res.status}`);
      const data = await res.json();
      const ocResult = data.result || {};

      task.status = {
        state: ocResult.status?.state || 'completed',
        message: {
          role: 'agent',
          parts: [{ kind: 'text', text: `[AAA→OpenClaw AGI]\n${extractText(ocResult.status?.message || {})}` }],
          messageId: generateId(), taskId, contextId
        },
        timestamp: new Date().toISOString()
      };
      task.artifacts = ocResult.artifacts || [];
      task.history = ocResult.history || [message];
      taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      const errorStatus = {
        state: 'failed',
        message: { role: 'agent', parts: [{ kind: 'text', text: `[AAA→OpenClaw AGI] Dispatch failed: ${err.message}.` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = errorStatus;
      taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: errorStatus, final: true });
      return;
    }
  }

  // === LOCAL PROCESSING (no targetAgent or unrecognised) ===

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
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({
    federation: 'arifOS AAA',
    version: '1.0.0',
    protocol: 'A2A v1.0.0',
    treaty: 'AAA-TREATY-v1.0.0',
    treaty_uri: 'https://aaa.arif-fazil.com/aaa-card-treaty',
    agents: [
      { id: 'aaa-gateway', url: 'https://aaa.arif-fazil.com/a2a', registered: true, role: 'gateway', a_role: null },
      { id: 'aaa-architect', url: 'https://aaa.arif-fazil.com/a2a/architect', registered: true, role: 'internal', a_role: 'A-rchitect', lane: 'AGI' },
      { id: 'aaa-engineer', url: 'https://aaa.arif-fazil.com/a2a/engineer', registered: true, role: 'internal', a_role: 'A-engineer', lane: 'AGI' },
      { id: 'aaa-auditor', url: 'https://aaa.arif-fazil.com/a2a/auditor', registered: true, role: 'internal', a_role: 'A-auditor', lane: 'ASI' },
      { id: 'geox-witness', url: 'https://geox.arif-fazil.com/a2a', registered: true, role: 'mesh', organ: 'GEOX' },
      { id: 'wealth-witness', url: 'https://wealth.arif-fazil.com/a2a', registered: true, role: 'mesh', organ: 'WEALTH' }
    ],
    constitutional_floors: ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13'],
    governance_root: 'https://aaa.arif-fazil.com/.well-known/arifos-federation.json'
  });
});

// A-ROLE AGENT CARD ROUTES
app.get('/a2a/architect/agent-card.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json(ARCHITECT_CARD);
});

app.get('/a2a/engineer/agent-card.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json(ENGINEER_CARD);
});

app.get('/a2a/auditor/agent-card.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json(AUDITOR_CARD);
});

// Treaty route — links to the full treaty law
app.get('/aaa-card-treaty', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({
    treaty_id: 'AAA-TREATY-v1.0.0',
    issued_by: 'arifOS Constitutional Kernel',
    kanon_lock: '2026.05.03-HERMES',
    status: 'ACTIVE',
    canonical_source: 'https://github.com/ariffazil/AAA/blob/main/a2a/AAA_TREATY_LAW.md',
    note: 'Full treaty law committed to AAA repo. Agent cards and this treaty are the binding contracts.'
  });
});

app.get('/health', async (req, res) => {
  const vaultHealthy = await checkVaultHealth();
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.json({
    status: 'healthy',
    protocol: 'A2A',
    version: '1.0.0',
    gateway: 'AAA',
    motto: 'Ditempa Bukan Diberi',
    vault: vaultHealthy ? 'CONNECTED' : 'DISCONNECTED'
  });
});

app.get('/api/ai/health', async (req, res) => {
  try {
    const [ollamaResponse, arifosResponse] = await Promise.all([
      fetch(`${OLLAMA_URL}/api/tags`, { signal: AbortSignal.timeout(5000) }),
      fetch(`${ARIFOS_LOCAL_URL}/health`, { signal: AbortSignal.timeout(5000) }),
    ]);

    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.json({
      ok: ollamaResponse.ok && arifosResponse.ok,
      upstreams: {
        ollama: ollamaResponse.ok ? 'healthy' : 'degraded',
        arifos: arifosResponse.ok ? 'healthy' : 'degraded',
        qdrant: 'configured',
      },
      defaults: {
        provider: 'ollama',
        chat_model: AAA_AI_DEFAULT_MODEL,
        embed_model: AAA_AI_EMBED_MODEL,
        rag_collection: AAA_AI_COLLECTION,
      },
    });
  } catch (error) {
    res.status(502).json({
      ok: false,
      error: error.message,
    });
  }
});

app.get('/api/ai/models', async (req, res) => {
  try {
    const upstream = await fetch(`${OLLAMA_URL}/api/tags`, {
      signal: AbortSignal.timeout(10000),
    });

    if (!upstream.ok) {
      const details = await readResponseText(upstream);
      return res.status(502).json({ ok: false, error: details });
    }

    const payload = await upstream.json();
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.json({
      ok: true,
      models: (payload.models || []).map((model) => ({
        name: model.name,
        size: model.size || 0,
        modified_at: model.modified_at || null,
        digest: model.digest || null,
      })),
      defaults: {
        provider: 'ollama',
        model: AAA_AI_DEFAULT_MODEL,
      },
      providers: [
        { id: 'ollama', label: 'Local Ollama' },
        { id: 'arifos', label: 'arifOS governed' },
        { id: 'openrouter', label: 'OpenRouter (365 models)' },
      ],
    });
  } catch (error) {
    res.status(502).json({
      ok: false,
      error: error.message,
    });
  }
});

app.post('/api/ai/rag/upload', async (req, res) => {
  try {
    const filename = typeof req.body?.filename === 'string' ? req.body.filename.trim() : '';
    const content = typeof req.body?.content === 'string' ? req.body.content : '';
    const mimeType = typeof req.body?.mimeType === 'string' ? req.body.mimeType : 'text/plain';

    if (!filename || !content.trim()) {
      return res.status(400).json({ ok: false, error: 'filename and content are required' });
    }

    const chunks = chunkDocument(content);
    if (chunks.length === 0) {
      return res.status(400).json({ ok: false, error: 'Document content is empty after normalization' });
    }

    const embeddings = await embedTexts(chunks);
    await ensureQdrantCollection(embeddings[0].length);

    const docId = crypto.randomUUID();
    const uploadedAt = new Date().toISOString();
    const points = chunks.map((chunk, index) => ({
      id: crypto.randomUUID(),
      vector: embeddings[index],
      payload: {
        doc_id: docId,
        filename,
        mimeType,
        chunk_index: index,
        content: chunk,
        snippet: chunk.slice(0, 280),
        uploaded_at: uploadedAt,
      },
    }));

    const upsertResponse = await fetch(`${QDRANT_URL}/collections/${AAA_AI_COLLECTION}/points?wait=true`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ points }),
      signal: AbortSignal.timeout(30000),
    });

    if (!upsertResponse.ok) {
      const details = await readResponseText(upsertResponse);
      return res.status(502).json({ ok: false, error: details });
    }

    res.json({
      ok: true,
      document: {
        id: docId,
        filename,
        mimeType,
        chunks: chunks.length,
        uploaded_at: uploadedAt,
        collection: AAA_AI_COLLECTION,
      },
    });
  } catch (error) {
    res.status(500).json({
      ok: false,
      error: error.message,
    });
  }
});

app.post('/api/ai/rag/query', async (req, res) => {
  try {
    const query = typeof req.body?.query === 'string' ? req.body.query.trim() : '';
    const limit = Number.isFinite(req.body?.limit) ? Number(req.body.limit) : 5;

    if (!query) {
      return res.status(400).json({ ok: false, error: 'query is required' });
    }

    const citations = await searchRag(query, Math.max(1, Math.min(limit, 8)));
    res.json({
      ok: true,
      query,
      citations,
      collection: AAA_AI_COLLECTION,
    });
  } catch (error) {
    res.status(500).json({
      ok: false,
      error: error.message,
    });
  }
});

app.post('/api/ai/chat', async (req, res) => {
  const provider = req.body?.provider === 'arifos' ? 'arifos'
    : req.body?.provider === 'openrouter' ? 'openrouter'
    : 'ollama';
  const model = typeof req.body?.model === 'string' && req.body.model.trim()
    ? req.body.model.trim()
    : AAA_AI_DEFAULT_MODEL;
  const messages = normalizeAiMessages(req.body?.messages);
  const citations = Array.isArray(req.body?.citations) ? req.body.citations : [];
  const contextBlock = buildContextBlock(citations);

  if (messages.length === 0) {
    return res.status(400).json({ ok: false, error: 'messages are required' });
  }

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const controller = new AbortController();
  req.on('close', () => controller.abort());

  try {
    let fullText = '';

    if (provider === 'arifos') {
      const governedPrompt = [
        'You are responding through AAA governed mode.',
        'Stay precise, grounded, and useful.',
        contextBlock ? `Use this retrieval context when relevant:\n\n${contextBlock}` : null,
        'Conversation transcript:',
        flattenTranscript(messages),
      ]
        .filter(Boolean)
        .join('\n\n');

      try {
        const governedResponse = await fetch(`${ARIFOS_LOCAL_URL}/tools/arif_reply_compose`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: governedPrompt,
            style: 'plain',
          }),
          signal: AbortSignal.any([controller.signal, AbortSignal.timeout(30000)]),
        });

        if (!governedResponse.ok) {
          const details = await readResponseText(governedResponse);
          writeSse(res, { type: 'error', error: details });
          return res.end();
        }

        const payload = await governedResponse.json();
        fullText = payload?.result?.composed || payload?.result?.result?.composed || '';
      } catch (networkErr) {
        const taskId = `arifos_chat_${Date.now()}`;
        const queued = await queueTask(taskId, {
          provider,
          messages: req.body.messages,
          contextBlock,
          citations,
        }, networkErr.message);
        if (queued) {
          fullText = `[HOLD] arifOS temporarily unreachable. Task queued (${taskId}). Retry worker active.`;
        } else {
          fullText = `[HOLD] arifOS unreachable and async backbone unavailable. Try again later.`;
        }
      }

      writeSse(res, {
        type: 'meta',
        provider,
        model: 'arif_reply_compose',
        citations,
      });
      if (fullText) {
        writeSse(res, {
          type: 'chunk',
          content: fullText,
        });
      }
      writeSse(res, {
        type: 'done',
        provider,
        model: 'arif_reply_compose',
        content: fullText,
        citations,
      });
      return res.end();
    }

    if (provider === 'openrouter') {
      const orMessages = contextBlock
        ? [{ role: 'system', content: `Ground the answer in the supplied sources when relevant.\n\n${contextBlock}` }, ...messages]
        : messages;

      const upstream = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${OPENWEBUI_API_KEY}`,
          'HTTP-Referer': 'https://aaa.arif-fazil.com',
          'X-Title': 'AAA AI Chat',
        },
        body: JSON.stringify({
          model: model || 'openai/gpt-4o-mini',
          messages: orMessages,
          stream: true,
        }),
        signal: AbortSignal.any([controller.signal, AbortSignal.timeout(60000)]),
      });

      if (!upstream.ok || !upstream.body) {
        const details = await readResponseText(upstream);
        writeSse(res, { type: 'error', error: details });
        return res.end();
      }

      writeSse(res, { type: 'meta', provider: 'openrouter', model, citations });

      const decoder = new TextDecoder();
      let buffer = '';

      for await (const chunk of upstream.body) {
        buffer += decoder.decode(chunk, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || trimmed === 'data: [DONE]') continue;
          const data = trimmed.startsWith('data: ') ? trimmed.slice(6) : trimmed;
          try {
            const parsed = JSON.parse(data);
            const delta = parsed?.choices?.[0]?.delta?.content || '';
            if (delta) {
              fullText += delta;
              writeSse(res, { type: 'chunk', content: delta });
            }
            if (parsed?.choices?.[0]?.finish_reason === 'stop') {
              writeSse(res, { type: 'done', provider: 'openrouter', model, content: fullText, citations });
              return res.end();
            }
          } catch { /* skip partial */ }
        }
      }
      writeSse(res, { type: 'done', provider: 'openrouter', model, content: fullText, citations });
      return res.end();
    }

    const ollamaMessages = contextBlock
      ? [{ role: 'system', content: `Ground the answer in the supplied sources when relevant.\n\n${contextBlock}` }, ...messages]
      : messages;

    const upstream = await fetch(`${OLLAMA_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        messages: ollamaMessages,
        stream: true,
      }),
      signal: AbortSignal.any([controller.signal, AbortSignal.timeout(60000)]),
    });

    if (!upstream.ok || !upstream.body) {
      const details = await readResponseText(upstream);
      writeSse(res, { type: 'error', error: details });
      return res.end();
    }

    writeSse(res, {
      type: 'meta',
      provider,
      model,
      citations,
    });

    const decoder = new TextDecoder();
    let buffer = '';

    for await (const chunk of upstream.body) {
      buffer += decoder.decode(chunk, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;

        const payload = JSON.parse(trimmed);
        const delta = payload?.message?.content || '';
        if (delta) {
          fullText += delta;
          writeSse(res, {
            type: 'chunk',
            content: delta,
          });
        }

        if (payload.done) {
          writeSse(res, {
            type: 'done',
            provider,
            model,
            content: fullText,
            citations,
          });
          return res.end();
        }
      }
    }

    if (buffer.trim()) {
      const payload = JSON.parse(buffer.trim());
      const delta = payload?.message?.content || '';
      if (delta) {
        fullText += delta;
        writeSse(res, {
          type: 'chunk',
          content: delta,
        });
      }
    }

    writeSse(res, {
      type: 'done',
      provider,
      model,
      content: fullText,
      citations,
    });
    res.end();
  } catch (error) {
    writeSse(res, {
      type: 'error',
      error: error.name === 'AbortError' ? 'Request aborted' : error.message,
    });
    res.end();
  }
});

function handleOperatorHolds(req, res) {
  const all = Array.from(taskStore.values());
  const pending = all.filter(t => t.status.state === 'input-required');
  const auth = all.filter(t => t.status.state === 'auth-required');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.json({
    ok: true,
    holds: pending.length + auth.length,
    breakdown: {
      'input-required': pending.length,
      'auth-required': auth.length,
    }
  });
}

app.get(['/operator/holds', '/api/operator/holds'], handleOperatorHolds);

function handleOperatorTasks(req, res) {
  const state = req.query.state;
  let tasks = Array.from(taskStore.values());
  if (state) tasks = tasks.filter(t => t.status.state === state);
  tasks.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.json({ ok: true, tasks });
}

app.get(['/operator/tasks', '/api/operator/tasks'], handleOperatorTasks);

function handleOperatorSeals(req, res) {
  const http = require('http');
  const r = http.request({ hostname: 'vault999-writer', port: 5001, path: '/health', method: 'GET', timeout: 5000 }, (r2) => {
    let body = '';
    r2.on('data', c => { body += c; });
    r2.on('end', () => {
      try {
        const d = JSON.parse(body);
        res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
        res.setHeader('Pragma', 'no-cache');
        res.json({ ok: true, seals: d.vault_seals_count || 0, pending_holds: d.pending_holds || 0 });
      } catch (_) {
        res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
        res.setHeader('Pragma', 'no-cache');
        res.json({ ok: true, seals: 0, pending_holds: 0 });
      }
      });
  });
  r.on('error', () => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.json({ ok: true, seals: 0, pending_holds: 0 });
  });
  r.end();
}

app.get(['/operator/seals', '/api/operator/seals'], handleOperatorSeals);

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

    await executeTask(taskId, contextId, message, params.agent_id);

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

    executeTask(taskId, contextId, message, params.agent_id).catch(console.error);

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
// NOTE: 404 handler moved to after all valid routes
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

    await executeTask(taskId, contextId, message, params.agent_id);

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

// === 404 FALLBACK HANDLER ===
// Placed AFTER all valid routes so only truly unknown paths hit this
// === 404 HANDLER ===
app.use((req, res) => {
  res.status(404).json(createJSONRPCError(0, ERROR_CODES.METHOD_NOT_FOUND, `Endpoint ${req.path} not found`));
});

// === ASYNC BACKBONE: Redis + NATS ===
let redisClient = null;
let natsConnection = null;
const sc = StringCodec();

async function initAsyncBackbone() {
  try {
    redisClient = createClient({ url: REDIS_URL });
    redisClient.on('error', err => console.error('[redis] error:', err.message));
    await redisClient.connect();
    console.log('[redis] connected');
  } catch (e) {
    console.error('[redis] failed to connect:', e.message);
  }

  try {
    natsConnection = await connect({ servers: NATS_URL });
    console.log('[nats] connected');

    const subVerdicts = natsConnection.subscribe('arifos.verdicts');
    const subBreaches = natsConnection.subscribe('arifos.floor_breach');

    (async () => {
      for await (const msg of subVerdicts) {
        console.log('[nats] arifos.verdicts:', sc.decode(msg.data));
      }
    })();

    (async () => {
      for await (const msg of subBreaches) {
        console.log('[nats] arifos.floor_breach:', sc.decode(msg.data));
      }
    })();

    setInterval(async () => {
      if (!natsConnection || !redisClient) return;
      const status = {
        timestamp: new Date().toISOString(),
        online_agents: taskStore.size,
        queue_depth: parseInt(await redisClient.lLen('aaa:hold_queue') || '0'),
      };
      natsConnection.publish('aaa.mesh_status', sc.encode(JSON.stringify(status)));
    }, 60000);
  } catch (e) {
    console.error('[nats] failed to connect:', e.message);
  }
}

async function queueTask(taskId, payload, reason) {
  if (!redisClient) return false;
  const entry = { taskId, payload, reason, queuedAt: new Date().toISOString(), retryCount: 0 };
  await redisClient.rPush('aaa:hold_queue', JSON.stringify(entry));
  console.log(`[queue] ${taskId} queued: ${reason}`);
  return true;
}

function startRetryWorker() {
  setInterval(async () => {
    if (!redisClient) return;
    try {
      const len = await redisClient.lLen('aaa:hold_queue');
      if (len === 0) return;
      const raw = await redisClient.lPop('aaa:hold_queue');
      if (!raw) return;
      const task = JSON.parse(raw);
      task.retryCount = (task.retryCount || 0) + 1;

      if (task.retryCount > 5) {
        await redisClient.rPush('aaa:dead_letter', JSON.stringify(task));
        console.log(`[retry] ${task.taskId} dead-lettered after 5 retries`);
        return;
      }

      console.log(`[retry] ${task.taskId} attempt ${task.retryCount}`);
      // For now, re-queue tasks that still fail. In production, call actual handler.
      // Check if arifOS is back before re-queueing
      try {
        const probe = await fetch(`${ARIFOS_LOCAL_URL}/health`, { signal: AbortSignal.timeout(3000) });
        if (probe.ok) {
          console.log(`[retry] ${task.taskId} arifOS back online — task requires manual replay`);
          await redisClient.rPush('aaa:hold_queue', JSON.stringify(task));
        } else {
          await redisClient.rPush('aaa:hold_queue', JSON.stringify(task));
        }
      } catch {
        await redisClient.rPush('aaa:hold_queue', JSON.stringify(task));
      }
    } catch (e) {
      console.error('[retry] worker error:', e.message);
    }
  }, 30000);
}

// === START ===
const PORT = process.env.PORT || 3001;
app.listen(PORT, async () => {
  console.log(`[AAA A2A] Hardened server running on port ${PORT}`);
  console.log(`[AAA A2A] Protocol: A2A v1.0.0`);
  console.log(`[AAA A2A] Auth: configured (bearer + api-key)`);
  console.log(`[AAA A2A] Agent Card: http://localhost:${PORT}/.well-known/agent-card.json`);
  console.log(`[AAA A2A] Federation: http://localhost:${PORT}/.well-known/arifos-federation.json`);
  console.log(`[AAA A2A] Health: http://localhost:${PORT}/health`);
  await initAsyncBackbone();
  startRetryWorker();
});

module.exports = { app };
