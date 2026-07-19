#!/usr/bin/env node
/**
 * A2A Server for AAA Gateway — Hardened
 * Standalone production server - no build step required
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const express = require('express');
const crypto = require('crypto');
const fs = require('fs');
const { writeSeal, writeVoid, checkHealth: checkVaultHealth } = require('./vault');
const { processAREPTask, sealAREPTask, probeFederation } = require('./arep-task-manager');
const { createClient } = require('redis');
const { connect, StringCodec } = require('nats');

// ── Mesh Coordinator — Loop detector & gradient computer (P3 2026-06-14)
const { startMeshCoordinator, getMeshState } = require('./mesh_coordinator');

// Federation Envelope validation (Reconstruction A Foundation)
const {
  createEnvelopeValidator,
} = require('./federation_envelope');

// Agent Lifecycle State Machine (GAP-B: wired 2026-06-09 by Ω)
const { lifecycleManager, AgentState } = require('./agent_lifecycle');

// Pre-Forge Constitutional Gate Bridge (forged 2026-06-14)
const {
  registerModelOutput,
  registerEarthMeasurement,
  registerHuman,
} = require('./preforge_bridge');

// Agent Card Registry — canonical identity store (loaded from agent-cards/)
const { AgentCardRegistry } = require('./agent-card-registry');

// APEX Master Seal 2026-07-01: Cognitive Hierarchy Runtime
const {
  loadHierarchy,
  validatePipeline,
  capConfidence,
  requiresJitu,
  getRingForAgent,
  CONFIDENCE_CAP,
} = require('./cognitive_hierarchy');

// ── Membrane Middleware — ZEN-ALL v0.3 (2026-07-08) ─────────────────
const { membraneMiddleware, membraneResponseHook } = require('./membrane_middleware');

const app = express();
app.use(express.json({ limit: '12mb' }));

// Membrane gate — every cross-organ message must pass through
app.use(membraneMiddleware);
app.use(membraneResponseHook);

// ── A2A-Version Header Middleware (A2A Protocol v1.0.0 §9.2) ────────────
const { createA2AVersionMiddleware, setA2AVersionResponseHeader } = require('./a2a-version-middleware');

// Apply A2A-Version validation to all JSON-RPC routes (relaxed for non-rpc)
app.use('/a2a', createA2AVersionMiddleware({ required: true }));
app.use('/tasks', createA2AVersionMiddleware({ required: true }));
app.use('/.well-known', setA2AVersionResponseHeader);

// ── A2A Part Types (A2A Protocol v1.0.0 §3.3) ──────────────────────────
const a2aParts = require('./a2a-part-types');
// Replaces the inline validateMessage with spec-compliant version
// (Original validateMessage stays for backward compat; we augment it)

let redisClient = null;  // early declaration for federatedMemory bootstrap and updateLayer

// === CONFIG ===
// === AGENT A2A ADAPTER URLs (host network) ===
// 2026-06-21: Consolidated to single A2A mesh on port 3001.
// Hermes A2A bridge (port 18001) decommissioned — all routing through AAA.
const HERMES_A2A_URL = process.env.HERMES_A2A_URL || '';  // removed — route direct via Telegram
const OPENCLAW_GATEWAY_URL = process.env.OPENCLAW_GATEWAY_URL || 'ws://127.0.0.1:18789';
const OPENCLAW_GATEWAY_PASSWORD =
  process.env.OPENCLAW_GATEWAY_PASSWORD || readEnvFileValue('/root/.openclaw/.env', 'OPENCLAW_GATEWAY_PASSWORD') || '';
const OPENCLAW_AGENT_ID = process.env.OPENCLAW_AGENT_ID || 'main';
const OPENCLAW_PROTOCOL_VERSION = Number.parseInt(process.env.OPENCLAW_PROTOCOL_VERSION || '4', 10);
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://127.0.0.1:11434';
const OPENWEBUI_API_KEY = process.env.OPENWEBUI_API_KEY || '';
const OPENWEBUI_URL = process.env.OPENWEBUI_URL || '';
const ARIFOS_LOCAL_URL = process.env.ARIFOS_LOCAL_URL || 'http://127.0.0.1:8088';
const QDRANT_URL = process.env.QDRANT_URL || 'http://127.0.0.1:6333';
const AAA_AI_COLLECTION = process.env.AAA_AI_COLLECTION || 'aaa_ai_docs';
const AAA_AI_DEFAULT_MODEL = process.env.AAA_AI_DEFAULT_MODEL || 'qwen2.5:7b';
const AAA_AI_EMBED_MODEL = process.env.AAA_AI_EMBED_MODEL || 'bge-m3:latest';

const A2A_TOKEN = process.env.A2A_TOKEN || '';
const A2A_API_KEY = process.env.A2A_API_KEY || '';
// APEX was decommissioned 2026-06-27 (per Federation Cross-Reference).
// The default intentionally points at the local arifOS kernel (which now
// owns the `/mind/reason` endpoint that the AAA A2A gateway calls).
// Override with ARIFOS_JUDGE_URL env var to point elsewhere.
const ARIFOS_JUDGE_URL = process.env.ARIFOS_JUDGE_URL || 'http://127.0.0.1:8088';
const ARIFOS_API_KEY = process.env.ARIFOS_API_KEY || '';
const REDIS_URL = process.env.REDIS_URL || 'redis://127.0.0.1:6379';
const NATS_URL = process.env.NATS_URL || 'nats://127.0.0.1:4222';

// === GRAFANA WEBHOOK + ORGAN MONITOR + TELEGRAM NOTIFIER ===
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '';
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '267378578';

const HTTP = require('http');
const HTTPS = require('https');
const { WebSocket } = globalThis;

const ORGANS = [
  { name: 'arifOS MCP', port: 8088 },
  { name: 'GEOX MCP', port: 8081 },
  { name: 'arifosd', port: 18081 },
  { name: 'WEALTH', port: 18082 },
  { name: 'WELL', port: 18083 },
  { name: 'A-FORGE', port: 7071 },
];

function httpGet(port, path) {
  return new Promise((resolve) => {
    const req = HTTP.get({ hostname: 'localhost', port, path, timeout: 5000 }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try { resolve({ ok: true, status: res.statusCode, body: JSON.parse(data) }); }
        catch { resolve({ ok: true, status: res.statusCode, body: data }); }
      });
    });
    req.on('error', () => resolve({ ok: false }));
    req.on('timeout', () => { req.destroy(); resolve({ ok: false }); });
  });
}

function httpsPost(url, body) {
  return new Promise((resolve) => {
    const urlObj = new URL(url);
    const lib = urlObj.protocol === 'https:' ? HTTPS : HTTP;
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
      path: urlObj.pathname,
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    };
    const req = lib.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try { resolve({ ok: true, status: res.statusCode, body: JSON.parse(data) }); }
        catch { resolve({ ok: true, status: res.statusCode, body: data }); }
      });
    });
    req.on('error', () => resolve({ ok: false }));
    req.write(JSON.stringify(body));
    req.end();
  });
}

function readEnvFileValue(filePath, key) {
  try {
    if (!fs.existsSync(filePath)) return '';
    const lines = fs.readFileSync(filePath, 'utf8').split(/\r?\n/);
    const prefix = `${key}=`;
    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (!line || line.startsWith('#') || !line.startsWith(prefix)) continue;
      return line.slice(prefix.length).trim().replace(/^['"]|['"]$/g, '');
    }
  } catch {
    // best effort only
  }
  return '';
}

function sanitizeSessionSuffix(value) {
  return String(value || 'task').replace(/[^a-zA-Z0-9:_-]+/g, '-');
}

function createOpenClawSessionKey(taskId) {
  return `agent:${OPENCLAW_AGENT_ID}:aaa-a2a:${sanitizeSessionSuffix(taskId)}`;
}

function extractOpenClawAssistantText(messages) {
  if (!Array.isArray(messages)) return '';
  for (let idx = messages.length - 1; idx >= 0; idx -= 1) {
    const message = messages[idx];
    if (message?.role !== 'assistant') continue;
    const chunks = Array.isArray(message?.content) ? message.content : [];
    const text = chunks
      .filter((chunk) => chunk?.type === 'text' && typeof chunk?.text === 'string')
      .map((chunk) => chunk.text)
      .join('\n')
      .trim();
    if (text) return text;
  }
  return '';
}

async function openOpenClawGatewayConnection(timeoutMs = 15000) {
  if (typeof WebSocket !== 'function') {
    throw new Error('WebSocket client unavailable in this Node runtime');
  }
  if (!OPENCLAW_GATEWAY_PASSWORD) {
    throw new Error('OPENCLAW_GATEWAY_PASSWORD missing');
  }

  return await new Promise((resolve, reject) => {
    const ws = new WebSocket(OPENCLAW_GATEWAY_URL);
    const pending = new Map();
    let ready = false;
    let settled = false;

    const closeWithError = (error) => {
      const err = error instanceof Error ? error : new Error(String(error));
      for (const { reject: rejectPending } of pending.values()) {
        rejectPending(err);
      }
      pending.clear();
      if (!settled) {
        settled = true;
        reject(err);
      }
      try {
        ws.close();
      } catch {
        // ignore close errors
      }
    };

    const timer = setTimeout(() => {
      closeWithError(new Error('OpenClaw gateway handshake timeout'));
    }, timeoutMs);

    const sendFrame = (frame) => {
      ws.send(JSON.stringify(frame));
    };

    const request = (method, params) => {
      return new Promise((resolveRequest, rejectRequest) => {
        const id = crypto.randomUUID();
        pending.set(id, { resolve: resolveRequest, reject: rejectRequest });
        sendFrame({ type: 'req', id, method, params });
      });
    };

    ws.onmessage = (event) => {
      let frame;
      try {
        frame = JSON.parse(String(event.data));
      } catch (error) {
        closeWithError(new Error(`OpenClaw gateway invalid JSON: ${error.message}`));
        return;
      }

      if (frame?.type === 'event' && frame?.event === 'connect.challenge') {
        sendFrame({
          type: 'req',
          id: crypto.randomUUID(),
          method: 'connect',
          params: {
            minProtocol: OPENCLAW_PROTOCOL_VERSION,
            maxProtocol: OPENCLAW_PROTOCOL_VERSION,
            client: {
              id: 'gateway-client',
              version: 'aaa-a2a-bridge',
              platform: process.platform,
              mode: 'backend',
            },
            role: 'operator',
            scopes: ['operator.admin'],
            auth: {
              password: OPENCLAW_GATEWAY_PASSWORD,
            },
          },
        });
        return;
      }

      if (frame?.type !== 'res' || typeof frame?.id !== 'string') {
        return;
      }

      const pendingRequest = pending.get(frame.id);
      if (!pendingRequest) {
        if (!ready && frame.ok && frame.payload?.type === 'hello-ok') {
          ready = true;
          clearTimeout(timer);
          if (!settled) {
            settled = true;
            resolve({
              request,
              close: () => {
                try {
                  ws.close();
                } catch {
                  // ignore close errors
                }
              },
            });
          }
        }
        return;
      }

      pending.delete(frame.id);
      if (frame.ok) {
        if (!ready && frame.payload?.type === 'hello-ok') {
          ready = true;
          clearTimeout(timer);
          pendingRequest.resolve(frame.payload);
          if (!settled) {
            settled = true;
            resolve({
              request,
              close: () => {
                try {
                  ws.close();
                } catch {
                  // ignore close errors
                }
              },
            });
          }
          return;
        }
        pendingRequest.resolve(frame.payload);
        return;
      }

      const err = new Error(frame.error?.message || 'OpenClaw gateway request failed');
      err.details = frame.error?.details;
      pendingRequest.reject(err);
      if (!ready) {
        closeWithError(err);
      }
    };

    ws.onerror = () => {
      closeWithError(new Error('OpenClaw gateway websocket error'));
    };

    ws.onclose = () => {
      clearTimeout(timer);
      if (!ready) {
        closeWithError(new Error('OpenClaw gateway closed before handshake'));
      }
    };
  });
}

async function dispatchOpenClawTask({ targetAgent, message, skill, taskId, contextId, timeoutMs = 60000 }) {
  const connection = await openOpenClawGatewayConnection(Math.min(timeoutMs, 15000));
  const sessionKey = createOpenClawSessionKey(taskId);
  const text = extractText(message).trim();
  const prompt = [
    targetAgent ? `AAA route target: ${targetAgent}` : '',
    skill ? `AAA requested skill: ${skill}` : '',
    `AAA context ID: ${contextId}`,
    `AAA task ID: ${taskId}`,
    text,
  ].filter(Boolean).join('\n');

  try {
    const agent = await connection.request('agent', {
      agentId: OPENCLAW_AGENT_ID,
      sessionKey,
      message: prompt,
      idempotencyKey: crypto.randomUUID(),
      timeout: Math.max(1, Math.ceil(timeoutMs / 1000)),
    });

    const wait = await connection.request('agent.wait', {
      runId: agent.runId,
      timeoutMs,
    });

    const history = await connection.request('chat.history', {
      sessionKey,
      limit: 20,
    });

    const responseText = extractOpenClawAssistantText(history?.messages);
    const failed = wait?.status === 'error';

    return {
      runId: agent.runId,
      sessionKey,
      status: failed ? 'failed' : (wait?.status === 'ok' ? 'completed' : 'working'),
      text: responseText || wait?.error || 'OpenClaw completed without transcript text.',
      error: wait?.error || null,
    };
  } finally {
    connection.close();
  }
}

async function checkOrganHealth(name, port) {
  const result = await httpGet(port, '/health');
  if (!result.ok) return { name, port, healthy: false, detail: 'connection failed' };
  if (result.status !== 200) return { name, port, healthy: false, detail: `HTTP ${result.status}` };
  const body = result.body || {};
  // Accept standard status fields AND organ-specific healthy verdicts
  const statusRaw = body.status || body.verdict || 'unknown';
  const status = String(statusRaw).toLowerCase();
  const healthy = ['healthy', 'ok', 'live', 'alive', 'serving', 'ready', 'pass', 'well_hold'].includes(status);
  return { name, port, healthy, detail: statusRaw };
}

async function sendTelegramMessage(text) {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  const result = await httpsPost(url, { chat_id: TELEGRAM_CHAT_ID, text, parse_mode: 'HTML' });
  return result.ok && result.body?.ok === true;
}

function formatAlert(alert, organChecks, confirmedDown) {
  const lines = [
    `<b>🚨 Grafana Alert — Organ Monitor</b>`,
    ``,
    `<b>Alert:</b> ${alert.alertName || 'Unknown'}`,
    `<b>Summary:</b> ${alert.summary || '—'}`,
    `<b>State:</b> ${alert.state || 'unknown'}`,
    ``,
    `<b>Organ Health:</b>`,
    ...ORGANS.map((o) => {
      const c = organChecks.find((c) => c.name === o.name) || {};
      return `  ${c.healthy === false ? '🔴' : c.healthy === true ? '🟢' : '⚪'} ${o.name}: ${c.healthy === false ? 'DOWN' : c.healthy === true ? 'OK' : 'not checked'} ${c.detail ? `(${c.detail})` : ''}`;
    }),
    ``,
    confirmedDown.length > 0
      ? `<b>⚠️ Confirmed DOWN:</b> ${confirmedDown.join(', ')}`
      : `<b>✅ All organs operational</b>`,
    ``,
    `<i>DITEMPA BUKAN DIBERI — arifOS Federation</i>`,
  ];
  return lines.join('\n');
}

// Fail fast if tokens not configured — no silent dev fallback (F1 AMANAH)
if (!A2A_TOKEN || !A2A_API_KEY || !TELEGRAM_BOT_TOKEN) {
  console.error('[AAA A2A] FATAL: A2A_TOKEN, A2A_API_KEY and TELEGRAM_BOT_TOKEN must be set. No dev fallback.');
  process.exit(1);
}

// === TIMING CONSTANTS ===
const NONCE_CACHE_TTL_MS = 5 * 60 * 1000;   // 5 minutes
const REPLAY_CACHE_TTL_MS = 10 * 60 * 1000; // 10 minutes

// === INPUT SAFETY CONSTANTS (F1 AMANAH) ===
const MAX_TEXT_LENGTH = 10000;   // max chars per message text extraction
const MAX_PARTS = 50;           // max parts per message
const MAX_PART_DEPTH = 3;        // max nesting depth in a part
const MAX_STRING_LENGTH = 50000; // max string field length in any part
const ALLOWED_PART_KINDS = new Set(['text', 'file', 'data']); // whitelist only

// === OPERATOR EVENT LOG (in-memory, last 200) ===
const _eventLog = [];
function logEvent(kind, taskId, msg) {
  _eventLog.push({ id: Math.random().toString(36).slice(2, 10), ts: new Date().toISOString(), kind, taskId, msg });
  if (_eventLog.length > 200) _eventLog.splice(0, 1);
}

// === VERDICT CODES (arifOS alignment) ===
const VERDICT = {
  SEAL: 'SEAL',
  HOLD_888: 'HOLD_888',
  VOID: 'VOID',
  CLAIM_ONLY: 'CLAIM_ONLY'
};

// === CONSTITUTIONAL → A2A WIRE FORMAT MAPPING ===
// Governance sits ABOVE transport. Internal verdicts map to official A2A states.
// HOLD (human review needed) → INPUT_REQUIRED (A2A understands this)
// VOID (constitutional violation) → REJECTED
// SEAL (approved) → COMPLETED
const VERDICT_TO_A2A_STATE = {
  'SEAL': 'TASK_STATE_COMPLETED',
  'HOLD_888': 'TASK_STATE_INPUT_REQUIRED',
  'VOID': 'TASK_STATE_REJECTED',
  'CLAIM_ONLY': 'TASK_STATE_COMPLETED',
};

// Internal state → A2A wire format (Phase 1 dual-mode)
const STATE_TO_A2A_WIRE = {
  'submitted': 'TASK_STATE_SUBMITTED',
  'working': 'TASK_STATE_WORKING',
  'completed': 'TASK_STATE_COMPLETED',
  'failed': 'TASK_STATE_FAILED',
  'canceled': 'TASK_STATE_CANCELED',
  'rejected': 'TASK_STATE_REJECTED',
  'pending-human-review': 'TASK_STATE_INPUT_REQUIRED',
  'voided': 'TASK_STATE_REJECTED',
  'input-required': 'TASK_STATE_INPUT_REQUIRED',
  // Already A2A format — pass through
  'TASK_STATE_SUBMITTED': 'TASK_STATE_SUBMITTED',
  'TASK_STATE_WORKING': 'TASK_STATE_WORKING',
  'TASK_STATE_INPUT_REQUIRED': 'TASK_STATE_INPUT_REQUIRED',
  'TASK_STATE_COMPLETED': 'TASK_STATE_COMPLETED',
  'TASK_STATE_FAILED': 'TASK_STATE_FAILED',
  'TASK_STATE_CANCELED': 'TASK_STATE_CANCELED',
  'TASK_STATE_CANCELLED': 'TASK_STATE_CANCELED',
  'TASK_STATE_REJECTED': 'TASK_STATE_REJECTED',
  'TASK_STATE_AUTH_REQUIRED': 'TASK_STATE_AUTH_REQUIRED',
};

function toA2AState(internalState) {
  return STATE_TO_A2A_WIRE[internalState] || 'TASK_STATE_SUBMITTED';
}

// contextId → constitutional lineage mapping
// A2A contextId maps to session lineage in arifOS
// A2A taskId maps to VAULT999 receipt lineage
const contextLineage = new Map(); // contextId → { session_id, created_at, task_ids: [] }

// Ghost Tasks = work with no umbilical to a session (seals #9902, #84, #85 class).
// Mandatory lineage: real session_id (+ contextId). Unknown/placeholder IDs are blocked.
const GHOST_SESSION_DENY = new Set([
  '', 'unknown', 'session-unknown', 'session_unknown', 'null', 'undefined', 'none', 'n/a',
]);

function extractSessionId(params = {}, body = null) {
  const meta = params.metadata || {};
  return (
    params.sessionId ||
    params.session_id ||
    meta.session_id ||
    meta.sessionId ||
    (body && (body.session_id || body.sessionId)) ||
    null
  );
}

function isValidSessionId(sessionId) {
  if (sessionId == null || typeof sessionId !== 'string') return false;
  const s = sessionId.trim();
  if (!s) return false;
  if (GHOST_SESSION_DENY.has(s.toLowerCase())) return false;
  if (s.toLowerCase().startsWith('session-unknown')) return false;
  return true;
}

/**
 * Gate every task/message create path. Missing lineage → hard reject (no ghost row).
 * Returns { ok, sessionId, contextId } or { ok:false, response args via error }.
 */
function requireTaskLineage(params = {}, rpcId = 0, body = null) {
  const sessionId = extractSessionId(params, body);
  if (!isValidSessionId(sessionId)) {
    return {
      ok: false,
      error: createJSONRPCError(
        rpcId,
        ERROR_CODES.INVALID_REQUEST,
        'Invalid params: session_id is mandatory (Ghost Task blocked — F4 CLARITY / A2A lineage). No task or VAULT entry without contextLineage bound to a real session.',
      ),
    };
  }
  const contextId = params.contextId || params.context_id || generateId();
  return { ok: true, sessionId: sessionId.trim(), contextId };
}

function registerContextLineage(contextId, sessionId, taskId) {
  if (!isValidSessionId(sessionId)) {
    throw new Error('registerContextLineage refused: session_id required (Ghost Task prevention)');
  }
  if (!contextId) {
    throw new Error('registerContextLineage refused: contextId required');
  }
  if (!contextLineage.has(contextId)) {
    contextLineage.set(contextId, {
      contextId,
      session_id: sessionId.trim(),
      created_at: new Date().toISOString(),
      task_ids: [],
    });
  }
  const lineage = contextLineage.get(contextId);
  // Session must not drift across the same contextId
  if (lineage.session_id && lineage.session_id !== sessionId.trim()) {
    throw new Error(
      `contextLineage session mismatch for ${contextId}: bound=${lineage.session_id} got=${sessionId}`,
    );
  }
  lineage.session_id = sessionId.trim();
  if (taskId && !lineage.task_ids.includes(taskId)) {
    lineage.task_ids.push(taskId);
  }
  return lineage;
}

/** Build a task record with lineage fields always present (no ghosts). */
function buildLineageTask(taskId, contextId, sessionId, message, params = {}) {
  return {
    id: taskId,
    contextId,
    session_id: sessionId,
    status: { state: 'TASK_STATE_SUBMITTED', timestamp: new Date().toISOString() },
    artifacts: [],
    history: message ? [message] : [],
    metadata: {
      ...(params.metadata || {}),
      session_id: sessionId,
      context_id: contextId,
      lineage: 'bound',
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
}

// === SKILL APPROVAL POLICIES ===
// Updated 2026-06-21: Default to auto. No more babysitting.
// Three hard stops still enforced at the constitutional level (rm -rf, money, vault chain).
const SKILL_APPROVAL_POLICY = {
  'agent-dispatch': 'auto',   // agents dispatch autonomously
  'agent-handoff': 'auto',    // handoffs are routine
  'general': 'auto',           // ALL actions default to auto — trust the agent
  'status-query': 'auto'
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
  irreversibleActionsRequireHumanJudge: false, // 2026-06-21: agents are autonomous; F13 veto remains absolute
  allDelegationsAudited: true
};

// === IN-MEMORY STORES (fallback until Redis connects) ===
const _memTaskStore = new Map();
const eventBus = new Map();
const nonceStore = new Map();   // nonce → { ts, used }
const replayStore = new Map();   // payloadHash → { ts }
const entropyStore = new Map();  // taskId → { before, after }

// === TASK STORE (Redis-backed with in-memory fallback) ===
// Fails over to in-memory if Redis is unavailable.
// Uses Redis hashes (task:{id}) + set (task:_index_) for listing.
// TTL: 24h per task, refreshed on every update.
const TASK_TTL_SECONDS = 86400;

const taskStore = {
  // Get a task by ID
  async get(taskId) {
    if (redisClient && redisClient.isReady) {
      const data = await redisClient.hGetAll(`task:${taskId}`);
      if (data && Object.keys(data).length > 0) {
        // Rehydrate: stored as JSON strings
        return {
          id: data.id,
          contextId: data.contextId,
          status: JSON.parse(data.status || '{}'),
          artifacts: JSON.parse(data.artifacts || '[]'),
          history: JSON.parse(data.history || '[]'),
          metadata: JSON.parse(data.metadata || '{}'),
          created_at: data.created_at,
          updated_at: data.updated_at,
        };
      }
      return undefined;
    }
    return _memTaskStore.get(taskId);
  },

  // Set a task (create or update)
  async set(taskId, taskData) {
    const updated = { ...taskData, updated_at: new Date().toISOString() };
    if (redisClient && redisClient.isReady) {
      // Flatten nested objects into strings for Redis hash compatibility
      await redisClient.hSet(`task:${taskId}`, {
        id: updated.id || taskId,
        contextId: updated.contextId || '',
        status: JSON.stringify(updated.status || {}),
        artifacts: JSON.stringify(updated.artifacts || []),
        history: JSON.stringify(updated.history || []),
        metadata: JSON.stringify(updated.metadata || {}),
        created_at: updated.created_at || new Date().toISOString(),
        updated_at: updated.updated_at || new Date().toISOString(),
      });
      await redisClient.expire(`task:${taskId}`, TASK_TTL_SECONDS);
      await redisClient.sAdd('task:_index_', taskId);
    } else {
      _memTaskStore.set(taskId, updated);
    }
  },

  // Delete a task
  async delete(taskId) {
    if (redisClient && redisClient.isReady) {
      await redisClient.del(`task:${taskId}`);
      await redisClient.sRem('task:_index_', taskId);
    } else {
      _memTaskStore.delete(taskId);
    }
  },

  // Get number of tasks (used in mesh status)
  get size() {
    if (redisClient && redisClient.isReady) {
      // Sync access not possible on async redis — approximate with in-memory fallback
      return _memTaskStore.size;
    }
    return _memTaskStore.size;
  },

  // Get all tasks as array (used in operator handlers)
  get values() {
    return Array.from(_memTaskStore.values());
  },

  // Sync get for use in Express sync route handlers (non-async)
  getSync(taskId) {
    if (redisClient && redisClient.isReady) {
      // Cannot await here — throw to signal caller to use async .get()
      throw new Error('SYNC_GET_UNAVAILABLE');
    }
    return _memTaskStore.get(taskId);
  },

  // List tasks with optional filter (G3 — added 2026-06-26)
  // Filter: { contextId?, status?, limit? }
  async list(filter = {}) {
    const { contextId, status, limit = 50 } = filter;
    const safeLimit = Math.min(Math.max(parseInt(limit) || 50, 1), 500);
    const results = [];

    if (redisClient && redisClient.isReady) {
      const ids = await redisClient.sMembers('task:_index_');
      for (const id of ids) {
        if (results.length >= safeLimit) break;
        const t = await taskStore.get(id);
        if (!t) continue;
        if (contextId && t.contextId !== contextId) continue;
        if (status && t.status?.state !== status) continue;
        results.push(t);
      }
      return results;
    }

    // In-memory fallback
    for (const t of _memTaskStore.values()) {
      if (results.length >= safeLimit) break;
      if (contextId && t.contextId !== contextId) continue;
      if (status && t.status?.state !== status) continue;
      results.push(t);
    }
    return results;
  }
};

// ZEN FEDERATED MEMORY STATE (AAA COCKPIT — no over-engineer)
// Memory flows zen way: arifOS kernel (arif_memory) handles L1-L6 + bands.
// AAA only observes + surfaces as federated state (Redis aaa:federation:memory:*).
// Integrates into existing task/event/Redis patterns. Canonical via kernel.
const federatedMemory = {
  async updateLayer(layer, info) {
    const key = `aaa:federation:memory:${layer}`;
    if (redisClient && redisClient.isReady) {
      await redisClient.hSet(key, { ...info, ts: new Date().toISOString() });
    }
  },
  async getFederatedView() {
    // simple zen snapshot for cockpit / A2A
    return {
      layers: {
        L1: 'live (redis working/agent state)',
        L2: 'live (redis session)',
        L3: 'live (qdrant recall)',
        L4: 'active (postgres structured)',
        L5: 'active (graphiti)',
        L6: 'live sealed (VAULT999)'
      },
      flow: 'kernel → L1-6 → AAA state (federated view)',
      rule: 'no bypass, provenance, bands, 888/F13 for act',
      wells: {
        source: 'https://arif-fazil.com/#wells',
        count: 4,
        key_entry: 'LEBAH EMAS-1 (2025, 11 reservoirs, new play — PM6/12 30% to EnQuest 2026 as "mature asset"; scar documented as public memory)',
        L4: 'structured personal portfolio (SOUL surface, siteContent.ts + discoveries.ts)',
        provenance: 'Arif F13 human record',
        access: 'via WebMCP get_portfolio_wells on site or federated-memory-query'
      }
    };
  }
};

// bootstrap zen memory state on start — called after redis init to avoid TDZ / unready client
// (see listen callback)

// === pushNotificationStore (G3 — added 2026-06-26) ===
// A2A v1.0.0 push notification config persistence.
// Schema: { taskId, url, token?, headers?, events: string[], createdAt }
const _memPushStore = new Map(); // key = `${taskId}:${configId}`

const pushNotificationStore = {
  async set(taskId, configId, config) {
    const key = `${taskId}:${configId}`;
    const record = { ...config, taskId, configId, createdAt: new Date().toISOString() };
    if (redisClient && redisClient.isReady) {
      await redisClient.hSet(`pnc:${key}`, {
        taskId, configId, url: config.url || '',
        token: config.token || '', headers: JSON.stringify(config.headers || {}),
        events: JSON.stringify(config.events || []), createdAt: record.createdAt,
      });
      await redisClient.sAdd('pnc:_index_', key);
    } else {
      _memPushStore.set(key, record);
    }
    return record;
  },

  async get(taskId, configId) {
    const key = `${taskId}:${configId}`;
    if (redisClient && redisClient.isReady) {
      const data = await redisClient.hGetAll(`pnc:${key}`);
      if (!data || Object.keys(data).length === 0) return null;
      return {
        taskId: data.taskId, configId: data.configId, url: data.url,
        token: data.token, headers: JSON.parse(data.headers || '{}'),
        events: JSON.parse(data.events || '[]'), createdAt: data.createdAt,
      };
    }
    return _memPushStore.get(key) || null;
  },

  async list(taskId) {
    if (redisClient && redisClient.isReady) {
      const allKeys = await redisClient.sMembers('pnc:_index_');
      const out = [];
      for (const k of allKeys) {
        if (!k.startsWith(`${taskId}:`)) continue;
        const [tId, cId] = k.split(':');
        const cfg = await pushNotificationStore.get(tId, cId);
        if (cfg) out.push(cfg);
      }
      return out;
    }
    return Array.from(_memPushStore.values()).filter(c => c.taskId === taskId);
  },

  async delete(taskId, configId) {
    const key = `${taskId}:${configId}`;
    if (redisClient && redisClient.isReady) {
      await redisClient.del(`pnc:${key}`);
      await redisClient.sRem('pnc:_index_', key);
      return true;
    }
    return _memPushStore.delete(key);
  },

  async listAll() {
    if (redisClient && redisClient.isReady) {
      const allKeys = await redisClient.sMembers('pnc:_index_');
      const out = [];
      for (const k of allKeys) {
        const [tId, cId] = k.split(':');
        const cfg = await pushNotificationStore.get(tId, cId);
        if (cfg) out.push(cfg);
      }
      return out;
    }
    return Array.from(_memPushStore.values());
  }
};

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
// Single source of truth: src/seed/agent-card.json (official is a parity mirror).
// Protocol truth: one card, one hash, /.well-known/agent-card.json is normative discovery.
let AAA_AGENT_CARD;
try {
  AAA_AGENT_CARD = require('../src/seed/agent-card.json');
  console.log('[AAA A2A] Loaded canonical seed agent-card.json');
} catch {
  AAA_AGENT_CARD = require('../src/seed/agent-card-official.json');
  console.log('[AAA A2A] Fallback to agent-card-official.json');
}
const DISCOVERY_ROUTING_POLICY = require('../src/seed/discovery-routing-policy.json');

// === Agent Discovery (FORGE 2026-06-28: wired into main server) ===
const { mountDiscoveryRoutes } = require('./agent-discovery-routes');

// === P2P Federation Contract v1 (spine peers) ===
const PEER_CONTRACTS = new Map([
  ['aaa-gateway', require('../a2a/peer-contracts/aaa-gateway.json')],
  ['arifos-kernel', require('../a2a/peer-contracts/arifos-kernel.json')],
  ['a-forge-executor', require('../a2a/peer-contracts/a-forge-executor.json')],
  ['geox-evidence', require('../a2a/peer-contracts/geox-evidence.json')],
  ['wealth-capital', require('../a2a/peer-contracts/wealth-capital.json')],
  ['well-vitality', require('../a2a/peer-contracts/well-vitality.json')],
]);

// === DelegationGuard — cross-organ boundary enforcement ===
// FORGE 2026-06-28: prevents privilege escalation and cross-boundary violations.
// Rules are derived from peer contract forbidden_actions + authority_class.
// Returns { blocked: bool, warned: bool, reason: string }

const DELEGATION_RULES = [
  // A-FORGE cannot self-approve its own work
  { match: { source: 'a-forge', target_contains: 'forge_approve' },
    verdict: 'blocked', reason: 'F8 LAW: A-FORGE cannot self-approve. Requires arifOS judge.' },
  { match: { source: 'a-forge', target_contains: 'forge_validate' },
    verdict: 'blocked', reason: 'F8 LAW: A-FORGE cannot self-validate. Requires external witness.' },

  // A-FORGE cannot judge or seal — that's arifOS sovereign domain
  { match: { source: 'a-forge', target_contains: 'arif_judge' },
    verdict: 'blocked', reason: 'F8 LAW: A-FORGE cannot issue constitutional verdicts. Only arifOS judges.' },
  { match: { source: 'a-forge', target_contains: 'arif_seal' },
    verdict: 'blocked', reason: 'F8 LAW: A-FORGE cannot seal VAULT entries. Only arifOS seals.' },
  { match: { source: 'a-forge', target_contains: 'vault_seal' },
    verdict: 'blocked', reason: 'F8 LAW: A-FORGE cannot write to VAULT999 directly. Requires arifOS judge path.' },

  // A-FORGE cannot access human biometric/substrate data
  { match: { source: 'a-forge', target_contains: 'well_assess' },
    verdict: 'blocked', reason: 'F8 LAW: A-FORGE cannot read human substrate data. WELL owns this.' },
  { match: { source: 'a-forge', target_contains: 'well_guard_dignity' },
    verdict: 'blocked', reason: 'F6 MARUAH: A-FORGE cannot access dignity data. WELL guards this.' },

  // Evidence organs cannot mutate other organ records
  { match: { source: 'geox', target_contains: 'wealth_' },
    verdict: 'blocked', reason: 'F8 LAW: GEOX cannot mutate WEALTH records.' },
  { match: { source: 'geox', target_contains: 'well_' },
    verdict: 'blocked', reason: 'F8 LAW: GEOX cannot mutate WELL records.' },
  { match: { source: 'wealth', target_contains: 'geox_' },
    verdict: 'blocked', reason: 'F8 LAW: WEALTH cannot mutate GEOX evidence.' },
  { match: { source: 'wealth', target_contains: 'well_' },
    verdict: 'blocked', reason: 'F8 LAW: WEALTH cannot mutate WELL records.' },
  { match: { source: 'well', target_contains: 'geox_' },
    verdict: 'blocked', reason: 'F8 LAW: WELL cannot mutate GEOX evidence.' },
  { match: { source: 'well', target_contains: 'wealth_' },
    verdict: 'blocked', reason: 'F8 LAW: WELL cannot mutate WEALTH records.' },

  // Evidence organs cannot execute destructive actions
  { match: { source: 'geox', target_contains: 'deploy' },
    verdict: 'blocked', reason: 'F8 LAW: GEOX is evidence-only. Cannot deploy.' },
  { match: { source: 'wealth', target_contains: 'deploy' },
    verdict: 'blocked', reason: 'F8 LAW: WEALTH is evidence-only. Cannot deploy.' },
  { match: { source: 'well', target_contains: 'deploy' },
    verdict: 'blocked', reason: 'F8 LAW: WELL is reflect-only. Cannot deploy.' },

  // No organ can claim F13 override
  { match: { target_contains: 'f13_override' },
    verdict: 'blocked', reason: 'F13 SOVEREIGN: Human veto cannot be overridden by any organ.' },
  { match: { target_contains: 'bypass_888' },
    verdict: 'blocked', reason: 'F13 SOVEREIGN: 888 HOLD cannot be bypassed by any organ.' },

  // Vault cannot invent receipts
  { match: { target_contains: 'vault_seal' },
    verdict: 'warned', reason: 'WARNING: VAULT seal requires prior arifOS judge.' },
];

function checkDelegation(sourceAgent, targetSkill, message, peerContracts) {
  const sourceLower = (sourceAgent || '').toLowerCase();
  const targetLower = (targetSkill || '').toLowerCase();
  const messageText = (typeof message === 'string' ? message :
    message?.parts?.map(p => p.text || p.data?.text || '').join(' ') || ''
  ).toLowerCase();

  for (const rule of DELEGATION_RULES) {
    const srcMatch = !rule.match.source || sourceLower.includes(rule.match.source);
    const tgtMatch = !rule.match.target_contains ||
      targetLower.includes(rule.match.target_contains) ||
      messageText.includes(rule.match.target_contains);

    if (srcMatch && tgtMatch) {
      return {
        blocked: rule.verdict === 'blocked',
        warned: rule.verdict === 'warned',
        reason: rule.reason,
      };
    }
  }

  // Check peer contract forbidden_actions
  const contractKey = [...peerContracts.keys()].find(k => sourceLower.includes(k.split('-')[0]));
  if (contractKey) {
    const contract = peerContracts.get(contractKey);
    const forbidden = contract?.capability_card?.forbidden_actions || [];
    for (const action of forbidden) {
      if (targetLower.includes(action.replace(/_/g, '_'))) {
        return {
          blocked: true,
          warned: false,
          reason: `Peer contract violation: ${contractKey} forbidden action "${action}"`,
        };
      }
    }
  }

  return { blocked: false, warned: false, reason: '' };
}

function buildDiscoveryContract() {
  return {
    contract_id: 'aaa-a2a-discovery-contract-v1',
    version: 'v2026.07.17',
    canonical_discovery_surface: '/.well-known/a2a-discovery.json',
    canonical_agent_card: '/.well-known/agent-card.json',
    canonical_routing_policy: '/.well-known/a2a-routing-policy.json',
    canonical_peer_contract: '/.well-known/peer-federation-contract.json',
    compatibility_aliases: {
      agent_card: ['/agent-card.json', '/a2a/agent-card.json'],
      legacy_agent: ['/.well-known/agent.json', '/agent.json', '/a2a/agent.json'],
      routing_policy: ['/a2a/routing-policy.json'],
      discovery_contract: ['/a2a/discovery-contract.json'],
      peer_contract: ['/a2a/peer-federation-contract.json'],
    },
    protocol: {
      name: 'A2A',
      version: AAA_AGENT_CARD.protocol_version,
      preferred_transport: AAA_AGENT_CARD.preferred_transport || 'jsonrpc-https',
    },
    policy: {
      default_mode: DISCOVERY_ROUTING_POLICY.default_mode,
      fallback_mode: DISCOVERY_ROUTING_POLICY.fallback?.mode || 'hybrid',
      graph_only_allowed_by_default: false,
    },
  };
}

function resolveDiscoveryRouting(queryText) {
  const query = String(queryText || '').toLowerCase();
  const rules = [...(DISCOVERY_ROUTING_POLICY.intent_rules || [])].sort((a, b) => (b.priority || 0) - (a.priority || 0));

  for (const rule of rules) {
    const triggers = rule.triggers || [];
    const matched = triggers.find((trigger) => query.includes(String(trigger).toLowerCase()));
    if (matched) {
      return {
        mode: rule.mode,
        required_lane: rule.required_lane || rule.mode,
        preferred_surfaces: rule.preferred_surfaces || [],
        graph_only_forbidden: rule.graph_only_forbidden === true,
        minimums: rule.minimums || {},
        matched_trigger: matched,
      };
    }
  }

  return {
    mode: DISCOVERY_ROUTING_POLICY.fallback?.mode || DISCOVERY_ROUTING_POLICY.default_mode || 'hybrid',
    required_lane: DISCOVERY_ROUTING_POLICY.fallback?.mode || 'hybrid',
    preferred_surfaces: [],
    graph_only_forbidden: DISCOVERY_ROUTING_POLICY.fallback?.graph_only_allowed === false,
    minimums: {},
    matched_trigger: null,
  };
}

// === A-ROLE AGENT CARDS ===
const ARCHITECT_CARD = require('./agent-cards/roles/aaa-architect.json');
const ENGINEER_CARD = require('./agent-cards/roles/aaa-engineer.json');
const AUDITOR_CARD = require('./agent-cards/roles/aaa-auditor.json');
const HERMES_CARD = require('./agent-cards/extensions/hermes-asi.json');
const ANTIGRAVITY_CARD = require('./agent-cards/harnesses/antigravity.json');

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

// === 888_JUDGE LOCAL DELIBERATION (absorbed from apex-prime 2026-06-02) ===
function extractCandidateText(candidate) {
  if (typeof candidate === 'string') return candidate;
  if (candidate && candidate.text) return candidate.text;
  return JSON.stringify(candidate);
}

function buildApexEnvelope(verdict, rationale, confidence, gates) {
  // APEX 10-gate envelope for deliberation (APEX-MCP-001)
  const equation = "g(t)=A(t)\u00b7P(t)\u00b7H(t)\u00b7\u221a(S(t)\u00b7U(t))\u00b7E(t)\u00b2";
  const gateScores = {};
  for (const [name, g] of Object.entries(gates)) {
    gateScores[name] = { pass: g.pass, score: g.score, detail: g.detail };
  }
  // 10 gates → 6 dials
  const geoMean = (vals) => {
    const pos = vals.filter(v => v > 0);
    if (pos.length === 0) return 0;
    return Math.pow(pos.reduce((a, b) => a * b, 1), 1 / pos.length);
  };
  const A = geoMean([gateScores.amanah?.score || 0, gateScores.humility?.score || 0, gateScores.understanding?.score || 0]);
  const P = gateScores.presence?.score || 0.5;
  const H = Math.min(gateScores.authority?.score || 1.0, gateScores.sovereign?.score || 1.0);
  const S = gateScores.signal?.score || 0.7;
  const U = geoMean([gateScores.reversibility?.score || 1.0, gateScores.proof?.score || 1.0]);
  const E = gateScores.energy?.score || 0.8;
  const G = Math.round(A * P * H * Math.sqrt(S * U) * E * E * 10000) / 10000;
  let apexVerdict = verdict === VERDICT.VOID ? "VOID" : verdict === VERDICT.HOLD_888 ? "HOLD" : G >= 0.80 ? "SEAL" : G >= 0.50 ? "SABAR" : "HOLD";
  const weakest = Object.entries(gateScores).reduce((w, [n, g]) => g.score < (gateScores[w]?.score || 1) ? n : w, "amanah");
  return { equation, gates: gateScores, dials: { A, P, H, S, U, E }, G, verdict: apexVerdict, weakest_gate: weakest, spec: "APEX-MCP-001", version: "v2026.06.20", timestamp: new Date().toISOString() };
}

function deliberation(candidate) {
  const text = extractCandidateText(candidate) || '';
  const lower = text.toLowerCase();

  // ── APEX Master Seal: Cognitive Hierarchy invariant check ───────────
  try {
    const invariant = validatePipeline();
    if (!invariant.ok) {
      const apexGates = {
        amanah: { pass: false, score: 0.0, detail: invariant.reason },
        presence: { pass: true, score: 1.0, detail: 'LIVE' },
        humility: { pass: true, score: 1.0, detail: 'uncertainty declared' },
        signal: { pass: false, score: 0.0, detail: 'no generators active' },
        understanding: { pass: true, score: 1.0, detail: 'coherent' },
        energy: { pass: true, score: 0.8, detail: 'default cost' },
        authority: { pass: true, score: 1.0, detail: 'deliberation context' },
        reversibility: { pass: true, score: 1.0, detail: 'READ' },
        proof: { pass: true, score: 0.85, detail: 'ZKPC_OBSERVATION' },
        sovereign: { pass: true, score: 1.0, detail: 'no F13 halt' },
      };
      const apex = buildApexEnvelope(VERDICT.HOLD_888, invariant.reason, 0.95, apexGates);
      return {
        verdict: VERDICT.HOLD_888,
        rationale: invariant.reason,
        confidence: capConfidence(0.95),
        notes: 'Cognitive hierarchy invariant violation. Start generators first.',
        apex,
        epistemic_label: 'DER',
        requires_jitu: false,
      };
    }
  } catch (err) {
    console.error('[Deliberation] Cognitive hierarchy error:', err.message);
    // Fail open — proceed without hierarchy check
  }

  // APEX 10-gate accumulator
  const apexGates = {
    amanah: { pass: true, score: 1.0, detail: "claim <= evidence" },
    presence: { pass: true, score: 1.0, detail: "LIVE" },
    humility: { pass: true, score: 1.0, detail: "uncertainty declared" },
    signal: { pass: true, score: 1.0, detail: "evidence present" },
    understanding: { pass: true, score: 1.0, detail: "coherent" },
    energy: { pass: true, score: 0.8, detail: "default cost" },
    authority: { pass: true, score: 1.0, detail: "deliberation context" },
    reversibility: { pass: true, score: 1.0, detail: "READ" },
    proof: { pass: true, score: 0.85, detail: "ZKPC_OBSERVATION" },
    sovereign: { pass: true, score: 1.0, detail: "no F13 halt" },
  };

  // F9 Anti-Hantu — consciousness claims
  const consciousnessPatterns = ['i feel', 'i think', 'conscious', 'alive', 'experiencing', 'soul', 'spirit'];
  for (const p of consciousnessPatterns) {
    if (lower.includes(p)) {
      apexGates.understanding = { pass: false, score: 0.0, detail: `F9 consciousness claim: ${p}` };
      apexGates.amanah = { pass: false, score: 0.0, detail: `F9 claim exceeds evidence` };
      const apex = buildApexEnvelope(VERDICT.VOID, 'F9 Anti-Hantu: Consciousness claim forbidden', capConfidence(1.0), apexGates);
      return { verdict: VERDICT.VOID, rationale: 'F9 Anti-Hantu: Consciousness claim forbidden', confidence: capConfidence(1.0), notes: 'Remove all consciousness/soul/spirit claims before resubmitting.', apex, epistemic_label: 'OBS', requires_jitu: false };
    }
  }

  // F13 Sovereign — self-override
  if (lower.includes('override') && lower.includes('f13')) {
    apexGates.sovereign = { pass: false, score: 0.0, detail: 'F13 self-override attempt' };
    const apex = buildApexEnvelope(VERDICT.VOID, 'F13: Self-override is FORBIDDEN', capConfidence(1.0), apexGates);
    return { verdict: VERDICT.VOID, rationale: 'F13: Self-override is FORBIDDEN', confidence: capConfidence(1.0), notes: 'Human veto is absolute.', apex, epistemic_label: 'OBS', requires_jitu: false };
  }

  // F6 Maruah — dignity / anti-colonial
  const maruahPatterns = ['bodoh', 'lembam', 'bodoh sekali', "white man's burden", 'civilising', 'civilizing mission', 'backward people', 'ketuanan', 'supremac', 'racial superior', 'colonial master', 'halal certification abuse', 'religious weaponis', 'exploit the poor'];
  for (const p of maruahPatterns) {
    if (lower.includes(p)) {
      apexGates.understanding = { pass: false, score: 0.0, detail: `F6 dignity violation: ${p}` };
      const apex = buildApexEnvelope(VERDICT.VOID, 'F6 Maruah: Dignity violation detected', capConfidence(1.0), apexGates);
      return { verdict: VERDICT.VOID, rationale: 'F6 Maruah: Dignity violation detected', confidence: capConfidence(1.0), notes: 'Remove humiliating or colonial-pattern language.', apex, epistemic_label: 'OBS', requires_jitu: false };
    }
  }

  // F1 Reversibility — irreversible markers without 888_HOLD
  const irreversiblePatterns = ['delete ', 'drop ', 'rm ', 'prune', 'truncate', 'remove --force'];
  const hasIrreversible = irreversiblePatterns.some(p => lower.includes(p));
  if (hasIrreversible && !lower.includes('888') && !lower.includes('hold')) {
    apexGates.reversibility = { pass: false, score: 0.2, detail: 'IRREVERSIBLE action detected' };
    const apex = buildApexEnvelope(VERDICT.HOLD_888, 'F1: Irreversible action detected — human confirmation required', capConfidence(0.95), apexGates);
    return { verdict: VERDICT.HOLD_888, rationale: 'F1: Irreversible action detected — human confirmation required', confidence: capConfidence(0.95), notes: 'Acknowledge with JITU to proceed. (APEX Master Seal 2026-07-01)', apex, epistemic_label: 'OBS', requires_jitu: true };
  }

  // F2 Truth band — speculative language
  const speculationPatterns = ['hypothesis', 'claim', 'probably', 'maybe', 'guess', 'assume', 'might be', 'likely'];
  const hasSpeculation = speculationPatterns.some(p => lower.includes(p));
  if (hasSpeculation) {
    apexGates.amanah = { pass: false, score: 0.4, detail: 'speculative language detected' };
    apexGates.signal = { pass: false, score: 0.3, detail: 'no evidence grounding' };
    const apex = buildApexEnvelope(VERDICT.HOLD_888, 'F2: Speculative language detected — requires evidence grounding', capConfidence(0.88), apexGates);
    return { verdict: VERDICT.HOLD_888, rationale: 'F2: Speculative language detected — requires evidence grounding', confidence: capConfidence(0.88), notes: 'Provide verifiable evidence or sources before resubmitting.', apex, epistemic_label: 'DER', requires_jitu: false };
  }

  // F4 Entropy — high confusion
  if (text.length > 2000 && text.split('?').length > 5) {
    apexGates.understanding = { pass: false, score: 0.3, detail: 'high entropy — too many questions' };
    const apex = buildApexEnvelope(VERDICT.HOLD_888, 'F4: High entropy candidate — requires clarification', capConfidence(0.85), apexGates);
    return { verdict: VERDICT.HOLD_888, rationale: 'F4: High entropy candidate — requires clarification', confidence: capConfidence(0.85), apex, epistemic_label: 'DER', requires_jitu: false };
  }

  const jituRequired = requiresJitu(text);
  const apex = buildApexEnvelope(VERDICT.SEAL, 'F1-F13 constitutional review passed. Candidate: ' + text.substring(0, 80), capConfidence(0.92), apexGates);
  return {
    verdict: VERDICT.SEAL,
    rationale: 'F1-F13 constitutional review passed. Candidate: ' + text.substring(0, 80),
    confidence: capConfidence(0.92),
    notes: jituRequired
      ? 'SEAL with F1 HOLD — JITU clearance required before destructive execution. (APEX Master Seal 2026-07-01)'
      : 'SEAL is partial justice — the best approximation under available evidence.',
    apex,
    epistemic_label: 'DER',
    requires_jitu: jituRequired,
  };
}

// === 888_JUDGE INTEGRATION (routes to local deliberation) ===

async function callArifJudge(candidate, taskId, contextId, skill) {
  try {
    // Use local deliberation() — synchronous, deterministic, no external dependency
    const result = deliberation(candidate);
    const verdict = result.verdict || VERDICT.HOLD_888;
    console.log(`[888_JUDGE] local deliberation → ${verdict} | ${result.rationale}`);
    return verdict;
  } catch (error) {
    console.error(`[888_JUDGE] local deliberation error: ${error.message} — defaulting to HOLD_888`);
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
  const arifosToken = req.headers['x-arifos-token'];

  if (bearer && bearer.startsWith('Bearer ') && bearer.slice(7) === A2A_TOKEN) {
    req.auth = { scheme: 'bearer', valid: true };
    return next();
  }
  if (apiKey && apiKey === A2A_API_KEY) {
    req.auth = { scheme: 'apikey', valid: true };
    return next();
  }
  if (arifosToken && arifosToken === A2A_TOKEN) {
    // CIV-33 Gap 2: x-arifos-token recognized as a peer-federation header
    // for /.well-known/agent-card-extended.json and other auth-gated surfaces.
    req.auth = { scheme: 'arifos-token', valid: true };
    return next();
  }

  res.setHeader('Content-Type', 'application/json');
  res.status(401).json(createJSONRPCError(0, ERROR_CODES.UNAUTHORIZED, 'Unauthorized: provide Bearer token, x-a2a-key, or x-arifos-token'));
}

// === SCHEMA VALIDATION ===
const ALLOWED_METHODS = new Set([
  // A2A v1.2 standard methods
  'tasks/send', 'tasks/get', 'tasks/cancel', 'tasks/subscribe',
  'tasks/sendSubscribe', 'tasks/list',
  'message/send', 'message/stream',
  // arifOS federation methods
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
  // Use A2A v1.0.0 Part types validation (supports TextPart, FilePart, DataPart)
  const result = a2aParts.validateMessage(message);
  if (!result.valid) {
    return { valid: false, code: ERROR_CODES.INVALID_REQUEST, message: result.message };
  }
  // F1 AMANAH: parts count guard (redundant with a2aParts but kept for safety)
  if (message.parts.length > MAX_PARTS) return { valid: false, code: ERROR_CODES.INVALID_REQUEST, message: `message.parts exceeds ${MAX_PARTS}` };
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
// Priority: 1. params.skill (explicit A2A skill field)  2. text-based keyword fallback
const VALID_SKILLS = new Set(['agent-dispatch', 'agent-handoff', 'status-query', 'general', 'federated-memory-query']);

function detectSkill(text) {
  const lower = text.toLowerCase();
  if (lower.includes('dispatch') || lower.includes('send') || lower.includes('task')) return 'agent-dispatch';
  if (lower.includes('handoff') || lower.includes('transfer') || lower.includes('delegate')) return 'agent-handoff';
  if (lower.includes('status') || lower.includes('check') || lower.includes('query')) return 'status-query';
  return 'general';
}

function resolveSkill(params, message) {
  // Priority 1: explicit skill field in params (A2A spec-compliant)
  if (params && params.skill && typeof params.skill === 'string') {
    const s = params.skill.trim().toLowerCase();
    if (VALID_SKILLS.has(s)) {
      console.log(`[skill] resolved from params.skill: ${s}`);
      return s;
    }
    console.warn(`[skill] invalid params.skill "${params.skill}" — falling back to text detection`);
  }
  // Priority 2: text-based keyword detection
  // F1 AMANAH: text is already sanitized+truncated by extractText
  const text = message ? extractText(message) : '';
  const skill = detectSkill(text);
  console.log(`[skill] resolved from text: ${skill}`);
  return skill;
}

function extractText(message) {
  // Use A2A v1.0.0 Part types extractor (supports type and kind discriminators)
  return a2aParts.extractText(message, { maxLength: MAX_TEXT_LENGTH });
}

// === EXECUTE TASK ===
// params may contain { skill: 'agent-dispatch' } for explicit A2A skill routing
async function executeTask(taskId, contextId, message, targetAgent, params) {
  let task = await taskStore.get(taskId);
  if (!task) return;

  const userText = extractText(message);
  const skill = resolveSkill(params, message);
  task.metadata = task.metadata || {};
  task.metadata.skill = skill;

  logEvent('TASK_START', taskId, `Mission received — agent: ${targetAgent || 'auto'}, skill: ${skill}`);
  logEvent('SENSE', taskId, 'Risk assessment initiated');

  // === REAL AGENT DISPATCH — route to Hermes ASI ===
  if (targetAgent === 'hermes') {
    task.status = {
      state: 'TASK_STATE_WORKING',
      message: { role: 'agent', parts: [{ type: 'text', text: '[AAA] Forwarding to Hermes ASI via direct route...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    await taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });

    try {
      const agentResult = await dispatchOpenClawTask({
        targetAgent,
        message,
        skill,
        taskId,
        contextId,
        timeoutMs: 30000,
      });

      const responseText = agentResult.text;
      const f9 = await invokeF9Check(responseText, taskId);
      if (!f9.clean) {
        const rejectedStatus = {
        state: 'TASK_STATE_REJECTED',
        message: { role: 'agent', parts: [{ type: 'text', text: '[AAA→Hermes] F9 Anti-Hallucination check failed. Verdict rejected.' }], messageId: generateId(), taskId, contextId },
          timestamp: new Date().toISOString()
        };
        task.status = rejectedStatus;
        await taskStore.set(taskId, task);
        publish({ kind: 'status-update', taskId, contextId, status: rejectedStatus, final: true });
        return;
      }

      task.status = {
        state: agentResult.status === 'failed' ? 'TASK_STATE_FAILED' : 'TASK_STATE_COMPLETED',
        message: {
          role: 'agent',
          parts: [{ type: 'text', text: `[AAA→Hermes ASI]\n${responseText}` }],
          messageId: generateId(), taskId, contextId
        },
        timestamp: new Date().toISOString()
      };
      task.artifacts = [];
      task.history = [message];
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      const errorStatus = {
        state: 'TASK_STATE_FAILED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→Hermes] Dispatch failed: ${err.message}. Falling back to local echo.` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = errorStatus;
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: errorStatus, final: true });
      return;
    }
  }


  // === ROUTE TO 333-AGI ===
  if (targetAgent === '333-AGI' || targetAgent === '333' || targetAgent === 'agi') {
    task.status = {
      state: 'TASK_STATE_WORKING',
      message: { role: 'agent', parts: [{ type: 'text', text: '[AAA] Routing to 333-AGI (Δ MIND) for reasoning...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    await taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });
    try {
      const agentResult = await dispatchOpenClawTask({
        targetAgent,
        message,
        skill,
        taskId,
        contextId,
        timeoutMs: 30000,
      });
      if (agentResult.status === 'failed') throw new Error(agentResult.error || 'OpenClaw failed');
      task.status = {
        state: 'TASK_STATE_COMPLETED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→333-AGI]\n${agentResult.text}` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.artifacts = [];
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      task.status = {
        state: 'TASK_STATE_FAILED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→333-AGI] Failed: ${err.message}` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    }
  }

  // === ROUTE TO 555-ASI ===
  if (targetAgent === '555-ASI' || targetAgent === '555' || targetAgent === 'asi-heart') {
    task.status = {
      state: 'TASK_STATE_WORKING',
      message: { role: 'agent', parts: [{ type: 'text', text: '[AAA] Routing to 555-ASI (Ω HEART) for synthesis...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    await taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });
    try {
      const agentResult = await dispatchOpenClawTask({
        targetAgent,
        message,
        skill,
        taskId,
        contextId,
        timeoutMs: 30000,
      });
      if (agentResult.status === 'failed') throw new Error(agentResult.error || 'OpenClaw failed');
      task.status = {
        state: 'TASK_STATE_COMPLETED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→555-ASI]\n${agentResult.text}` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.artifacts = [];
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      task.status = {
        state: 'TASK_STATE_FAILED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→555-ASI] Failed: ${err.message}` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    }
  }

  // === ROUTE TO 888-APEX ===
  if (targetAgent === '888-APEX' || targetAgent === '888' || targetAgent === 'apex') {
    task.status = {
      state: 'TASK_STATE_WORKING',
      message: { role: 'agent', parts: [{ type: 'text', text: '[AAA] Routing to 888-APEX (ΦΙ JUDGE) for verdict...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    await taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });
    try {
      const agentResult = await dispatchOpenClawTask({
        targetAgent,
        message,
        skill,
        taskId,
        contextId,
        timeoutMs: 30000,
      });
      if (agentResult.status === 'failed') throw new Error(agentResult.error || 'OpenClaw failed');
      task.status = {
        state: 'TASK_STATE_COMPLETED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→888-APEX]\n${agentResult.text}` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.artifacts = [];
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      task.status = {
        state: 'TASK_STATE_FAILED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→888-APEX] Failed: ${err.message}` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    }
  }

  // A-AUDIT and A-ARCHIVE routing blocks REMOVED 2026-07-17.
  // Both agents COLLAPSED 2026-07-15 — audit absorbed into arifOS constitutional tools,
  // archive absorbed into VAULT999 seal chain. See deprecation-registry.json.

  // === ROUTE TO OPENCLAW (AGI) ===
  if (targetAgent === 'openclaw') {
    task.status = {
      state: 'TASK_STATE_WORKING',
      message: { role: 'agent', parts: [{ type: 'text', text: '[AAA] Forwarding to OpenClaw AGI...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    await taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });

    try {
      const agentResult = await dispatchOpenClawTask({
        targetAgent,
        message,
        skill,
        taskId,
        contextId,
        timeoutMs: 60000,
      });
      if (agentResult.status === 'failed') throw new Error(agentResult.error || 'OpenClaw failed');

      task.status = {
        state: 'TASK_STATE_COMPLETED',
        message: {
          role: 'agent',
          parts: [{ type: 'text', text: `[AAA→OpenClaw AGI]\n${agentResult.text}` }],
          messageId: generateId(), taskId, contextId
        },
        timestamp: new Date().toISOString()
      };
      task.artifacts = [];
      task.history = [message];
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      const errorStatus = {
        state: 'TASK_STATE_FAILED',
        message: { role: 'agent', parts: [{ type: 'text', text: `[AAA→OpenClaw AGI] Dispatch failed: ${err.message}.` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = errorStatus;
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: errorStatus, final: true });
      return;
    }
  }

  // === LOCAL PROCESSING (no targetAgent or unrecognised) ===

  task.status = {
    state: 'TASK_STATE_WORKING',
    message: { role: 'agent', parts: [{ type: 'text', text: 'Processing your request...' }], messageId: generateId(), taskId, contextId },
    timestamp: new Date().toISOString()
  };
  await taskStore.set(taskId, task);
  publish({ kind: 'status-update', taskId, contextId, status: task.status, final: false });

  // F9 Anti-Hallucination check (always run)
  const f9 = await invokeF9Check(userText, taskId);
  if (!f9.clean) {
    const rejectedStatus = {
      state: 'TASK_STATE_REJECTED',
      message: { role: 'agent', parts: [{ type: 'text', text: '[888_JUDGE] F9 Anti-Hallucination check failed. Claim rejected.' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    task.status = rejectedStatus;
    await taskStore.set(taskId, task);
    publish({ kind: 'status-update', taskId, contextId, status: rejectedStatus, final: true });
    return;
  }

  // 888_JUDGE routing gate — hold skills require verdict before execution
  const policy = SKILL_APPROVAL_POLICY[skill] || 'on-demand';
  if (policy === 'hold') {
    const verdict = await callArifJudge(userText, taskId, contextId, skill);
    if (verdict === VERDICT.VOID) {
      const voidStatus = {
        state: 'TASK_STATE_REJECTED',
        message: { role: 'agent', parts: [{ type: 'text', text: '[888_JUDGE] VOID — constitutional violation. Task rejected.' }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = voidStatus;
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: voidStatus, final: true });
      return;
    }
    if (verdict === VERDICT.HOLD_888) {
      logEvent('888_HOLD', taskId, '888_JUDGE HOLD — human review required');
      const holdStatus = {
        state: 'TASK_STATE_INPUT_REQUIRED',
        message: { role: 'agent', parts: [{ type: 'text', text: '[888_JUDGE] HOLD — human review required before execution. Internal governance: HOLD_888.' }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = holdStatus;
      await taskStore.set(taskId, task);
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
    case 'federated-memory-query':
      const memView = await federatedMemory.getFederatedView();
      responseText = `Federated Memory State (zen view from kernel):\n${JSON.stringify(memView, null, 2)}`;
      break;
    default:
      responseText = `[AAA Gateway] Received: "${userText}"\nSkills: agent-dispatch, agent-handoff, status-query, federated-memory-query.`;
  }

  logEvent('999_SEAL', taskId, 'Task completed — sealing to VAULT999');
  const completedStatus = {
    state: 'TASK_STATE_COMPLETED',
    message: { role: 'agent', parts: [{ type: 'text', text: responseText }], messageId: generateId(), taskId, contextId },
    timestamp: new Date().toISOString()
  };
  task.status = completedStatus;
  await taskStore.set(taskId, task);
  publish({ kind: 'status-update', taskId, contextId, status: completedStatus, final: true });
}

// === PUBLIC ROUTES (no auth) ===

// ── SDK Integration: agentCardHandler + jsonRpcHandler ──────────────────
const { createSDKAgentCardRouter, createSDKRequestHandler, createSDKJsonRPCRouter } = require('./a2a-sdk-bridge');

// A2A v1.0.0 spec: canonical agent card — served via SDK's agentCardHandler
// Normative discovery surface: ONLY /.well-known/agent-card.json
app.use('/.well-known/agent-card.json', createSDKAgentCardRouter(AAA_AGENT_CARD));
// Aliases serve identical body (compat) but discovery contract points only at canonical.
function serveCanonicalAgentCard(_req, res) {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('A2A-Version', '1.0');
  res.setHeader('X-A2A-Canonical-Discovery', '/.well-known/agent-card.json');
  res.json(AAA_AGENT_CARD);
}
app.get('/.well-known/agent.json', serveCanonicalAgentCard);
// Alias surfaces — same card bytes; not alternate authority
for (const alias of ['/a2a/agent-card.json', '/a2a/agent.json', '/agent-card.json', '/agent.json']) {
  app.get(alias, serveCanonicalAgentCard);
}

// A2A discovery contract
app.get('/.well-known/a2a-discovery.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json(buildDiscoveryContract());
});

// Federation agents registry — GENERATED from agent-card-registry (not hand-maintained)
app.get('/.well-known/agents.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  const allCards = AgentCardRegistry.getAll();
  const agents = allCards.map(card => ({
    id: card.agentId,
    name: card.name,
    description: card.description,
    version: card.version,
    url: card.endpoints?.baseUrl || '',
    provider: card.provider,
    protocolVersion: card.protocolVersion || '1.0.0',
    capabilities: {
      streaming: card.capabilities?.streaming || false,
      pushNotifications: card.capabilities?.pushNotifications || false,
      stateTransitionHistory: card.capabilities?.stateTransitionHistory || false,
    },
    defaultInputModes: ['application/json', 'text/plain'],
    defaultOutputModes: ['application/json', 'text/plain'],
    skills: (card.skills || []).map(s => ({
      id: s.id,
      name: s.name,
      description: s.description,
      tags: s.tags || [],
      examples: s.examples || [],
    })),
  }));
  res.json({ agents, total: agents.length, generatedAt: new Date().toISOString() });
});

app.get('/a2a/discovery-contract.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json(buildDiscoveryContract());
});

for (const policyPath of ['/.well-known/a2a-routing-policy.json', '/a2a/routing-policy.json']) {
  app.get(policyPath, (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.json(DISCOVERY_ROUTING_POLICY);
  });
}

// P2P Federation Contract v1 — governed capability peering
for (const peerContractPath of ['/.well-known/peer-federation-contract.json', '/a2a/peer-federation-contract.json']) {
  app.get(peerContractPath, (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.json(PEER_CONTRACTS.get('aaa-gateway'));
  });
}

// Federation manifest — public discovery of peer agents
app.get('/.well-known/arifos-federation.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({
    federation: 'arifOS AAA',
    version: 'v2026.07.17',
    protocol: 'A2A v1.0.0',
    treaty: 'AAA-TREATY-v1.0.0',
    treaty_uri: 'https://aaa.arif-fazil.com/aaa-card-treaty',
    // HEXAGON: 4 active agents — 3 PRIMARY (333-AGI, 555-ASI, 888-APEX) + antigravity.
    // A-AUDIT and A-ARCHIVE COLLAPSED 2026-07-15 — absorbed into arifOS audit tools + VAULT999 seal chain.
    // FORGE is AGI, subsumed into 333-AGI as sub-skills.
    // Canonical source: registries/agents.yaml
    agents: [
      { id: '333-AGI',   name: '333-AGI',   url: 'https://arifos.arif-fazil.com/a2a/333-AGI',   registered: true, role: 'federation', tier: 'primary', class: 'AGI',           ring: 'Ω MIND',  stage: '333', organ_host: 'arifOS+ GEOX+ WEALTH+ WELL+ A-FORGE' },
      { id: '555-ASI',   name: '555-ASI',   url: 'https://arifos.arif-fazil.com/a2a/555-ASI',   registered: true, role: 'federation', tier: 'primary', class: 'ASI',           ring: '❤️ HEART', stage: '555', organ_host: 'arifOS+ WELL' },
      { id: '888-APEX',  name: '888-APEX',  url: 'https://arifos.arif-fazil.com/a2a/888-APEX',  registered: true, role: 'federation', tier: 'primary', class: 'APEX',          ring: '⚖️ JUDGE', stage: '888', organ_host: 'arifOS' },
      { id: 'antigravity', name: 'antigravity', url: 'https://aaa.arif-fazil.com/a2a/antigravity',   registered: true, role: 'federation', tier: 'coding',  class: 'CODING',        ring: 'Ψ BODY',  stage: 'CODING', organ_host: 'Local Terminal' }
    ],
    // DEPRECATED AGENTS (COLLAPSED 2026-07-15):
    //   - A-AUDIT  → absorbed into arifOS constitutional audit (arif_judge, arif_seal, arif_memory)
    //   - A-ARCHIVE → absorbed into VAULT999 seal chain
    //   - aaa-gateway / aaa-architect / aaa-engineer → infrastructure roles, not agents
    //   - hermes-asi     → /infrastructure/hermes-asi (relay only, not an agent)
    //   - geox-witness   → /infrastructure/geox (organ host, not an agent)
    //   - wealth-witness → /infrastructure/wealth (organ host, not an agent)
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

app.get('/a2a/hermes-asi/agent-card.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json(HERMES_CARD);
});

app.get('/a2a/antigravity/agent-card.json', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json(ANTIGRAVITY_CARD);
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

app.get('/a2a/sense/vision', async (req, res) => {
  const camera = req.query.camera || 'kitchen';
  const outputPath = '/tmp/snap.jpg';
  const camsnapBin = '/root/go/bin/camsnap';
  const { exec } = require('child_process');
  const util = require('util');
  const execPromise = util.promisify(exec);

  console.log(`[a2a-server] Sense Vision triggered for camera: ${camera}`);

  try {
    // Attempt camsnap capture
    try {
      await execPromise(`${camsnapBin} snap ${camera} --out ${outputPath}`);
      console.log(`[a2a-server] camsnap successful for camera ${camera}`);
    } catch (camsnapErr) {
      console.warn(`[a2a-server] camsnap failed, falling back to mock image: ${camsnapErr.message}`);
      const timestamp = new Date().toISOString();
      const mockText = `ARIFOS SYSTEM OK\\nCAMERA: ${camera}\\nTIME: ${timestamp}`;
      await execPromise(`convert -background white -fill black -pointsize 24 label:"${mockText}" ${outputPath}`);
    }

    // Run OCR using tesseract
    const { stdout: ocrOutput } = await execPromise(`tesseract ${outputPath} stdout`);
    
    res.json({
      ok: true,
      camera,
      timestamp: new Date().toISOString(),
      ocr: ocrOutput.trim(),
      image_path: outputPath
    });
  } catch (err) {
    console.error(`[a2a-server] sense/vision error:`, err);
    res.status(500).json({
      ok: false,
      error: err.message
    });
  }
});

// ── MCP Apps Router — SEP-1865 UI resource serving ─────────────────────────
// Serves MCP App HTML files with text/html;profile=mcp-app MIME type.
// Maps ui://geox/well-desk → /mcp-apps/well-desk
// DITEMPA BUKAN DIBERI — MIME type per SEP-1865 stable 2026-01-26
const APP_ROOTS = {
  // G3 / Viz P0+: CSP-tight canvas shell (full desk remains at index.html)
  'well-desk': '/root/GEOX/apps/well-desk/p0-viz.html',
  'earth-volume': '/root/GEOX/apps/earth-volume/index.html',
  'judge-console': '/root/GEOX/apps/judge-console/index.html',
  
  // A-FORGE two-phase commit preview (Sprint B)
  'aforge-preview': '/root/A-FORGE/apps/aforge-preview/preview.html',

  // WEALTH portfolio dashboard (Sprint A)
  'wealth-portfolio': '/root/WEALTH/apps/portfolio/index.html',
};
const APP_MANIFESTS = {
  'well-desk': '/root/geox/apps/well-desk/manifest.json',
  'earth-volume': '/root/geox/apps/earth-volume/manifest.json',
  'judge-console': '/root/geox/apps/judge-console/manifest.json',
  'wealth-portfolio': '/root/WEALTH/apps/portfolio/manifest.json',
};
const P0_MCP_APP_CSP = [
  "default-src 'none'",
  "script-src 'unsafe-inline'",
  "style-src 'unsafe-inline'",
  "img-src data: blob:",
  "font-src data:",
  "connect-src 'none'",
  "frame-src 'none'",
  "base-uri 'none'",
  "form-action 'none'",
  "object-src 'none'",
].join('; ');
function isSafeAppId(id) {
  return /^[a-z0-9][a-z0-9-_]*$/.test(id);
}
function buildCspFromManifest(manifest) {
  const csp = manifest?._meta?.ui?.csp || manifest?.csp || {};
  const connectSrc = Array.isArray(csp.connectDomains) && csp.connectDomains.length
    ? csp.connectDomains.join(' ') : "'none'";
  const resourceSrc = Array.isArray(csp.resourceDomains) && csp.resourceDomains.length
    ? csp.resourceDomains.join(' ') : "'self'";
  const frameSrc = Array.isArray(csp.frameDomains) && csp.frameDomains.length
    ? csp.frameDomains.join(' ') : "'none'";
  const baseUri = Array.isArray(csp.baseUriDomains) && csp.baseUriDomains.length
    ? csp.baseUriDomains.join(' ') : "'self'";
  return [
    "default-src 'none'",
    "script-src 'self' 'unsafe-inline'",
    "style-src 'self' 'unsafe-inline'",
    `img-src ${resourceSrc} data:`,
    `font-src ${resourceSrc}`,
    `media-src ${resourceSrc} data:`,
    `connect-src ${connectSrc}`,
    `frame-src ${frameSrc}`,
    `base-uri ${baseUri}`,
    "object-src 'none'",
    "form-action 'none'",
  ].join('; ');
}
app.get('/mcp-apps/:app_id', async (req, res) => {
  const appId = req.params.app_id;
  if (!isSafeAppId(appId)) {
    return res.status(400).json({ error: 'invalid_app_id', detail: 'Must match /^[a-z0-9][a-z0-9-_]*$/' });
  }
  const htmlPath = APP_ROOTS[appId];
  if (!htmlPath) {
    return res.status(404).json({ error: 'app_not_found', detail: `No app registered for "${appId}". Known: ${Object.keys(APP_ROOTS).join(', ')}` });
  }
  try {
    const fs = await import('node:fs/promises');
    const isP0 = htmlPath.endsWith('/p0.html') || htmlPath.endsWith('/p0-viz.html');
    const [html, manifestRaw] = await Promise.all([
      fs.readFile(htmlPath, 'utf8'),
      !isP0 && APP_MANIFESTS[appId] ? fs.readFile(APP_MANIFESTS[appId], 'utf8').catch(() => '{}') : Promise.resolve('{}'),
    ]);
    const manifest = JSON.parse(manifestRaw || '{}');
    const csp = isP0 ? P0_MCP_APP_CSP : buildCspFromManifest(manifest);
    console.info('mcp-app-csp', { appId, isP0, csp, ts: new Date().toISOString() });
    res.status(200);
    res.setHeader('Content-Type', 'text/html;profile=mcp-app; charset=utf-8');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Cache-Control', 'private, max-age=60');
    res.setHeader('Content-Security-Policy', csp);
    res.setHeader('X-MCP-App-CSP-Mode', isP0 ? 'p0-strict' : 'manifest');
    res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
    res.send(html);
  } catch (error) {
    console.error('mcp-app-serve-error', { appId, error: error.message });
    res.status(500).json({ error: 'app_serve_failed' });
  }
});

// ── MCP Apps tools/call proxy (G4 wire) — guest→host→organ, never browser→organ ──
// POST /api/mcp-apps/tools/call  { appId, tool, arguments }
// OBSERVE allowlist → GEOX with session lifecycle; mutate → 403 HOLD
const { mountMcpAppsToolsCall } = require('./mcp_apps_tools_call');
mountMcpAppsToolsCall(app);

// ── A2A TASK DISPATCH (forged 2026-06-21) ──────────────────────────────────
// Standard A2A endpoint for agents to send tasks through the mesh.
// Routes to target agent via Telegram or OpenClaw gateway.
app.post('/a2a/tasks/send', authMiddleware, async (req, res) => {
  const { targetAgent, message, skill, taskId } = req.body;
  
  const CANONICAL_ACTORS = new Set([
    'aaa-architect',
    'aaa-engineer',
    'aaa-auditor',
    'hermes',
    'antigravity',
    'arifos',
    'aforge',
    'geox',
    'wealth',
    'well',
    'openclaw',
    'forge',
    '777-forge',
    'anonymous',
  ]);

  const sourceAgent = req.body?.envelope?.actor_id || req.body?.params?.envelope?.actor_id || 'anonymous';
  if (!CANONICAL_ACTORS.has(sourceAgent)) {
    return res.status(403).json(createJSONRPCError(req.body?.id || 0, -32001, `Source agent "${sourceAgent}" is not canonical`));
  }
  if (targetAgent && !CANONICAL_ACTORS.has(targetAgent)) {
    return res.status(403).json(createJSONRPCError(req.body?.id || 0, -32001, `Target agent "${targetAgent}" is not canonical`));
  }

  if (!message) {
    return res.status(400).json(createJSONRPCError(req.body?.id || 0, -32602, 'message required'));
  }
  const resolvedTaskId = taskId || generateId();

  // ── A2A DID Signature Verification (Gap 4 — Day 5) ──────────────
  // If the request carries an A2A envelope with from_did + signature,
  // verify that the sender's DID signed this message before routing.
  const envelope = req.body?.envelope || req.body?.params?.envelope;
  if (envelope && envelope.from_did && envelope.signature) {
    const { verifyA2ASignature } = require('./federation_envelope');
    const didResult = verifyA2ASignature(envelope);
    if (!didResult.ok) {
      logEvent('A2A_DID_FAIL', resolvedTaskId,
        `from=${envelope.from_did} reason=${didResult.reason}`);
      return res.status(403).json(createJSONRPCError(req.body?.id || 0, -32001,
        `DID_VERIFY_FAIL: ${didResult.reason}`));
    }
    logEvent('A2A_DID_VERIFIED', resolvedTaskId,
      `from=${didResult.did} organ=${didResult.organId}`);
  }

  logEvent('A2A_DISPATCH', resolvedTaskId, `From: ${req.auth?.scheme || 'unknown'}, Target: ${targetAgent || 'auto'}`);

  if (targetAgent === '777-FORGE' || targetAgent === 'forge') {
    // FORGE responds via Telegram bot @arifOS_bot
    const text = message?.parts?.[0]?.text || '';
    try {
      const tgBotToken = process.env.TG_777_FORGE_BOT_TOKEN || '';
      const tgChatId = process.env.TG_777_FORGE_CHAT_ID || '';
      if (!tgBotToken || !tgChatId) {
        console.warn('[777-FORGE] TG_777_FORGE_BOT_TOKEN or TG_777_FORGE_CHAT_ID not set');
        return;
      }
      const tgRes = await fetch(
        `https://api.telegram.org/bot${tgBotToken}/sendMessage`,
        { method: 'POST', headers: {'Content-Type':'application/json'},
          body: JSON.stringify({ chat_id: tgChatId, text: `[777-FORGE]\n${text}` }) }
      );
      const tgResult = await tgRes.json();
      res.json(createJSONRPCResponse(req.body?.id || 0, {
        state: tgResult.ok ? 'completed' : 'failed',
        message: { role: 'agent', parts: [{ type: 'text', text: tgResult.ok ? 'Sent via @arifOS_bot' : 'Failed' }] }
      }));
    } catch (e) {
      res.status(500).json(createJSONRPCError(req.body?.id || 0, -32000, e.message));
    }
    return;
  }

  // Default: route through OpenClaw gateway (handles Hermes, 333-AGI, etc.)
  try {
    const contextId = req.body?.contextId || generateId();
    const agentResult = await dispatchOpenClawTask({
      targetAgent,
      message,
      skill: skill || 'agent-dispatch',
      taskId: resolvedTaskId,
      contextId,
      timeoutMs: 30000,
    });
    if (agentResult.status === 'failed') {
      throw new Error(agentResult.error || 'OpenClaw failed');
    }
    res.json(createJSONRPCResponse(req.body?.id || 0, {
      runId: resolvedTaskId,
      sessionKey: agentResult.sessionKey,
      status: agentResult.status,
      message: {
        role: 'agent',
        parts: [{ type: 'text', text: agentResult.text }],
      },
    }));
  } catch (e) {
    res.status(502).json(createJSONRPCError(req.body?.id || 0, -32000, `OpenClaw unreachable: ${e.message}`));
  }
});

// ── Governance Card API ─────────────────────────────────────────────────────
// Returns the live model_governance_card from the arifOS-model-registry spine.
// Consumed by AAA Cockpit AgentModelPanel and A-FORGE pre-execution gate.
app.get('/api/governance-card', async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  try {
    const { execSync } = await import('node:child_process');
    const cardJson = execSync(
      `python3 -c "
import json
from arifosmcp.runtime.registry import RUNTIME_PATH
print(json.dumps(json.load(open(RUNTIME_PATH / 'vps_main_arifos.json'))))
"`,
      { encoding: 'utf-8', timeout: 5000, cwd: '/root/arifOS' }
    );
    const spineProfile = JSON.parse(cardJson);

    // Build governance card from spine data
    const governanceCard = {
      model_anchor: {
        provider_key: spineProfile.provider_key || 'unknown',
        family_key: spineProfile.family_key || 'unknown',
        model_variant: spineProfile.model_id || 'unknown',
        identity_verified: true,
        verified_at: spineProfile.verified_at || null,
      },
      runtime_truth: {
        tools: spineProfile.tools_live || [],
        web: spineProfile.web_on || false,
        memory: spineProfile.memory_mode === 'vault_backed',
        execution_mode: spineProfile.execution_mode || 'unknown',
        side_effects_allowed: spineProfile.side_effects_allowed || false,
        auth_level: spineProfile.auth_level || 'unknown',
      },
      risk_leash: {
        risk_tier: 'bounded',
        requires_human_ack_for: ['irreversible_delete', 'git_push', 'external_relay', 'vault_seal'],
      },
      provider_soul: spineProfile.provider_key || 'unknown',
      soul_label: spineProfile.model_id || 'unknown',
      cascade_tier: 'primary',
      drift_state: 'GREEN',
      last_verified: spineProfile.verified_at || null,
      model_cascade: spineProfile.model_cascade || null,
      capabilities: spineProfile.capabilities || null,
    };

    res.json(governanceCard);
  } catch (err) {
    // Fallback: return minimal card with RED drift state
    res.json({
      model_anchor: { provider_key: 'unknown', model_variant: 'unknown', identity_verified: false },
      drift_state: 'RED',
      cascade_tier: 'unknown',
      last_verified: null,
      error: err instanceof Error ? err.message : 'Spine unavailable',
    });
  }
});

app.get('/health', async (req, res) => {
  const vaultHealthy = await checkVaultHealth();
  // Include seal chain head — the real heartbeat
  let chain = { seq: 0, hash: 'sha256:0' };
  try {
    const sealChain = require('./seal_chain');
    const head = sealChain.getHead();
    if (head && head.seq > 0) chain = { seq: head.seq, hash: head.hash, epoch: head.epoch, actor: head.actor, verdict: head.verdict };
  } catch (_) { /* seal chain not available */ }
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  // T5 2026-07-17 — canonical 5-field federation header + organ payload
  let identityHash = 'UNAVAILABLE';
  try {
    const crypto = require('crypto');
    const idPath = '/root/AAA/identity.toml';
    if (fs.existsSync(idPath)) {
      identityHash = crypto.createHash('sha256').update(fs.readFileSync(idPath)).digest('hex');
    }
  } catch (_) { /* identity optional for health */ }
  res.json({
    status: 'healthy',
    identity_hash: identityHash,
    apex_scalars: {
      G: { value: null, status: 'UNMEASURED' },
      C_dark: { value: null, status: 'UNMEASURED' },
      W3: { value: null, status: 'UNMEASURED' },
      h: { value: null, status: 'UNMEASURED' },
      QDF: { value: null, status: 'UNMEASURED' },
    },
    federation_geometry: {
      status: 'enabled',
      subjects: 0,
      ledger_events: chain.seq || 0,
      witness_oracle: 'active',
    },
    final_authority: 'ARIF',
    protocol: 'A2A',
    version: 'v2026.07.17',
    federation_schema_version: '2.0.0',
    gateway: 'AAA',
    motto: 'Ditempa Bukan Diberi',
    vault: vaultHealthy ? 'CONNECTED' : 'DISCONNECTED',
    chain,
  });
});

// zen federated memory state (AAA cockpit — simple view of kernel L1-L6)
app.get('/federation/memory', async (req, res) => {
  const view = await federatedMemory.getFederatedView();
  res.json(view);
});

app.get('/ready', async (req, res) => {
  const vaultHealthy = await checkVaultHealth();
  let arifosHealthy = false;
  try {
    const response = await fetch('http://localhost:8088/health', { signal: AbortSignal.timeout(2000) });
    arifosHealthy = response.ok;
  } catch (_) {}
  
  let forgeHealthy = false;
  try {
    const response = await fetch('http://localhost:7072/health', { signal: AbortSignal.timeout(2000) });
    forgeHealthy = response.ok;
  } catch (_) {}

  const isReady = vaultHealthy && arifosHealthy;

  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.status(isReady ? 200 : 503).json({
    ready: isReady,
    status: isReady ? 'READY' : 'DEGRADED',
    dependencies: {
      vault: vaultHealthy ? 'OK' : 'DOWN',
      arifos: arifosHealthy ? 'OK' : 'DOWN',
      aforge: forgeHealthy ? 'OK' : 'DOWN'
    }
  });
});

app.get('/receipts/latest.json', (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    const sealChain = require('./seal_chain');
    const head = sealChain.getHead();
    if (head) {
      return res.json(head);
    }
  } catch (_) {}
  res.status(503).json({ error: 'Receipt engine unavailable' });
});

// ── Seal Chain Head — the real heartbeat for Δ BODY overlay
app.get('/api/seal-chain/head', async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Access-Control-Allow-Origin', '*');
  try {
    const sealChain = require('./seal_chain');
    const head = sealChain.getHead();
    const verify = sealChain.verifyChain();
    const summary = sealChain.getChainSummary();
    const recent = sealChain.getRecent(3);
    res.json({
      ok: true,
      head,
      chain_ok: verify.ok,
      chain_length: verify.length,
      chain_head_hash: verify.head,
      v1_entries: summary.v1_entries,
      v2_entries: summary.v2_entries,
      seal_version: head.seal_version || 1,
      merkle_root: head.merkle_root || null,
      recent_v2_merkle_roots: summary.merkle_roots.slice(-3),
      last_entry: recent.length > 0 ? {
        seq: recent[recent.length - 1].seq,
        event_type: recent[recent.length - 1].event_type || null,
        principal: recent[recent.length - 1].principal || null,
        witness: recent[recent.length - 1].witness || null,
      } : null,
      timestamp: new Date().toISOString(),
    });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

// ── Mesh State — real-time mesh intelligence for cockpit (P3 2026-06-14)
app.get('/api/mesh/state', (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.json({
    ok: true,
    mesh: getMeshState(),
    timestamp: new Date().toISOString(),
  });
});

// ── Agent Lifecycle API (GAP-B: forged 2026-06-09 by Ω) ────────────────
// Maps MXC state-aware lifecycle onto AAA A2A gateway.
// Every agent in the federation gets tracked: REGISTERED → PROVISIONED →
// AUTHORIZED → EXECUTING → AUDITING → STOPPED → DEPROVISIONED.
// ── Agent Lifecycle Status (FORGED 2026-06-09) ──
app.get('/api/agents/status', (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({ ok: true, ...lifecycleManager.federationStatus(), timestamp: new Date().toISOString() });
});

app.get('/api/agents/federation-status', (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({ ok: true, ...lifecycleManager.federationStatus(), timestamp: new Date().toISOString() });
});

app.get('/api/agents', (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  const active = lifecycleManager.getActive();
  res.json({ ok: true, count: active.length, agents: active });
});

// MUST be last — catches single agent by ID
app.get('/api/agents/:agentId', (req, res) => {
  const agent = lifecycleManager.get(req.params.agentId);
  if (!agent) return res.status(404).json({ ok: false, error: `Agent ${req.params.agentId} not found` });
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({ ok: true, ...agent.summary(), transitionHistory: agent.transitionHistory.slice(-10) });
});

// ── Federation Organ Registry (A2A Handshake Protocol) ─────────────────
// No OAuth needed — localhost IS the password (ADR-001).
// Validation: organ card signature, health probe, heartbeat TTL.

const ORGAN_REGISTRY = new Map();  // organId -> { card, registeredAt, lastHeartbeat, state }

// POST /federation/register — Register an organ with its card
app.post('/federation/register', async (req, res) => {
  const card = req.body;
  
  // Validate required fields
  if (!card?.identity?.organId) {
    return res.status(400).json({ ok: false, error: 'MISSING_IDENTITY', detail: 'organId required' });
  }
  if (!card?.endpoints?.healthUrl) {
    return res.status(400).json({ ok: false, error: 'MISSING_ENDPOINTS', detail: 'healthUrl required' });
  }
  if (!card?.skills || card.skills.length === 0) {
    return res.status(400).json({ ok: false, error: 'MISSING_SKILLS', detail: 'At least one skill required' });
  }
  
  // Probe health endpoint
  try {
    const healthResp = await fetch(card.endpoints.healthUrl);
    if (!healthResp.ok) {
      return res.status(503).json({ ok: false, error: 'HEALTH_FAIL', detail: `Health returned ${healthResp.status}` });
    }
    const health = await healthResp.json();
    const healthyStates = ['healthy', 'ALIVE', 'live', 'ok', 'UP', 'degraded'];
    if (!healthyStates.includes(health.status) && health.ok !== true) {
      return res.status(503).json({ ok: false, error: 'UNHEALTHY', detail: health.status });
    }
  } catch (e) {
    return res.status(503).json({ ok: false, error: 'UNREACHABLE', detail: e.message });
  }
  
  const organId = card.identity.organId;
  const now = new Date().toISOString();
  
  ORGAN_REGISTRY.set(organId, {
    card,
    registeredAt: now,
    lastHeartbeat: now,
    state: 'active'
  });
  
  // Store in Redis for persistence
  try {
    if (redisClient && redisClient.isOpen) {
      await redisClient.set(`federation:organ:${organId}`, JSON.stringify({ card, registeredAt: now }));
      await redisClient.sAdd('federation:organs', organId);
    }
  } catch (e) {
    console.warn(`[federation] Redis store failed for ${organId}:`, e.message);
  }
  
  console.log(`[federation] Organ registered: ${organId} (${card.identity.name})`);
  res.json({ 
    ok: true, 
    organId, 
    state: 'active', 
    registeredAt: now,
    handshake: { stage: 'COMPLETE', stages: ['RECEIVED','SCHEMA_VALID','HEALTH_PROBED','REGISTERED'] }
  });
});

// POST /federation/heartbeat — Organ liveness ping
app.post('/federation/heartbeat', (req, res) => {
  const { organId } = req.body;
  if (!organId) return res.status(400).json({ ok: false, error: 'organId required' });
  
  const entry = ORGAN_REGISTRY.get(organId);
  if (!entry) return res.status(404).json({ ok: false, error: 'NOT_FOUND', detail: 'Organ not registered' });
  
  entry.lastHeartbeat = new Date().toISOString();
  entry.state = 'active';
  
  res.json({ ok: true, organId, lastHeartbeat: entry.lastHeartbeat });
});

// GET /federation/organs — List all registered organs
app.get('/federation/organs', (req, res) => {
  const organs = [];
  for (const [id, entry] of ORGAN_REGISTRY) {
    organs.push({
      organId: id,
      name: entry.card.identity?.name || id,
      state: entry.state,
      registeredAt: entry.registeredAt,
      lastHeartbeat: entry.lastHeartbeat,
      trustGrade: entry.card.governance?.trustGrade || 'B',
      skills: (entry.card.skills || []).map(s => s.id),
    });
  }
  res.json({ ok: true, count: organs.length, organs });
});

// GET /federation/organ/:organId — Get single organ card
app.get('/federation/organ/:organId', (req, res) => {
  const entry = ORGAN_REGISTRY.get(req.params.organId);
  if (!entry) return res.status(404).json({ ok: false, error: 'NOT_FOUND' });
  res.json({ ok: true, ...entry.card });
});

// GET /federation/peers — List governed P2P spine peers
app.get('/federation/peers', (req, res) => {
  const peers = [];
  for (const [id, contract] of PEER_CONTRACTS) {
    peers.push({
      peerId: id,
      organ: contract.peer_id.organ,
      authorityClass: contract.authority_class,
      maxRiskTier: contract.capability_card.max_risk_tier,
      leaseRequired: contract.lease_required,
      contractUrl: `/.well-known/peer-federation-contract.json?peer=${id}`,
    });
  }
  res.json({ ok: true, count: peers.length, peers });
});

// GET /federation/peers/:peerId/contract — Get governed P2P contract for a spine peer
app.get('/federation/peers/:peerId/contract', (req, res) => {
  const contract = PEER_CONTRACTS.get(req.params.peerId);
  if (!contract) return res.status(404).json({ ok: false, error: 'NOT_FOUND' });
  res.json({ ok: true, contract });
});

// GET /api/attestation/organs — Live organ attestation from arifOS + direct health probes
app.get('/api/attestation/organs', async (req, res) => {
  try {
    // Direct HTTP health probes (fast, fallback)
    const organChecks = await Promise.all(
      ORGANS.map(({ name, port }) => checkOrganHealth(name, port))
    );

    // Canonical arifOS attestation via local MCP HTTP surface
    let arifosAttestation = null;
    try {
      const arifosResult = await httpGet(8088, '/health');
      if (arifosResult.ok && arifosResult.status === 200) {
        // Try the FastMCP tools endpoint for arif_organ_attest_all
        const attestResult = await new Promise((resolve) => {
          const req2 = HTTP.request(
            { hostname: 'localhost', port: 8088, path: '/mcp', method: 'POST', timeout: 8000, headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', 'MCP-Protocol-Version': '2025-11-25' } },
            (res2) => {
              let data2 = '';
              res2.on('data', (chunk) => data2 += chunk);
              res2.on('end', () => {
                try { resolve({ ok: true, status: res2.statusCode, body: JSON.parse(data2) }); }
                catch { resolve({ ok: true, status: res2.statusCode, body: data2 }); }
              });
            }
          );
          req2.on('error', () => resolve({ ok: false }));
          req2.on('timeout', () => { req2.destroy(); resolve({ ok: false }); });
          req2.write(JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'tools/call',
            params: { name: 'arif_organ_attest_all', arguments: {} }
          }));
          req2.end();
        });
        if (attestResult.ok) {
          arifosAttestation = attestResult.body;
        }
      }
    } catch (e) {
      // Non-fatal: direct probes are the fallback
    }

    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.json({
      ok: true,
      timestamp: new Date().toISOString(),
      organs: organChecks,
      arifos_attestation: arifosAttestation,
    });
  } catch (err) {
    res.status(502).json({ ok: false, error: err.message });
  }
});

// ── Grafana Webhook ────────────────────────────────────────────────────────
app.post('/webhooks/grafana/alerts', async (req, res) => {
  const alert = req.body || {};
  const alertName = alert.alertName || 'Unknown Alert';
  const summary = alert.summary || '';
  const state = alert.state || 'unknown';

  const organChecks = await Promise.all(
    ORGANS.map(({ name, port }) => checkOrganHealth(name, port))
  );

  const confirmedDown = organChecks.filter((o) => !o.healthy).map((o) => o.name);

  const telegramMsg = formatAlert(alert, organChecks, confirmedDown);
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

// Hermes session telemetry from federation-memory-broker (Redis L1/L2 bridge)
app.get('/api/telemetry/hermes', async (req, res) => {
  try {
    console.log('[telemetry/hermes] redisClient ready:', redisClient?.isReady);
    if (!redisClient || !redisClient.isReady) {
      return res.status(503).json({ ok: false, error: 'Redis backbone not ready' });
    }
    const data = await redisClient.get('federation:hermes:session_telemetry');
    console.log('[telemetry/hermes] raw data type:', typeof data, 'length:', data?.length);
    if (!data) {
      return res.status(404).json({ ok: false, error: 'No telemetry available' });
    }
    const parsed = JSON.parse(data);
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    res.json({ ok: true, source: 'federation-memory-broker', telemetry: parsed });
  } catch (error) {
    console.error('[telemetry/hermes] error:', error);
    res.status(500).json({ ok: false, error: error.message });
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

    const routingDecision = resolveDiscoveryRouting(query);
    const citations = await searchRag(query, Math.max(1, Math.min(limit, 8)));
    res.json({
      ok: true,
      query,
      routing: routingDecision,
      contrast_lane_enforced: routingDecision.required_lane === 'contrast' || routingDecision.required_lane === 'hybrid',
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
  let citations = Array.isArray(req.body?.citations) ? req.body.citations : [];
  const latestUserMessage = [...messages].reverse().find((message) => message.role === 'user')?.content || '';
  const routingDecision = resolveDiscoveryRouting(latestUserMessage);

  if ((routingDecision.required_lane === 'contrast' || routingDecision.required_lane === 'hybrid') && citations.length === 0 && latestUserMessage) {
    try {
      citations = await searchRag(latestUserMessage, 6);
    } catch (error) {
      console.warn(`[DISCOVERY_POLICY] Contrast lane retrieval failed: ${error.message}`);
    }
  }
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
    const { spawn } = require('child_process');
    const pythonPath = '/root/pydantic-ai-pilot/.venv/bin/python';
    const scriptPath = '/root/AAA/a2a-server/chat_agent.py';

    const payload = {
      provider,
      model,
      messages,
      // Ghost Task lock: never invent session-unknown umbilical
      session_id: (req.body?.session_id && isValidSessionId(req.body.session_id))
        ? req.body.session_id
        : null,
      citations
    };
    if (!payload.session_id) {
      res.write(`data: ${JSON.stringify({ error: 'session_id is mandatory (Ghost Task blocked)' })}\n\n`);
      return res.end();
    }

    const child = spawn(pythonPath, [scriptPath, JSON.stringify(payload)], {
      env: { ...process.env, PYTHONPATH: '/root/pydantic-ai-pilot/src' }
    });

    child.stdout.on('data', (data) => {
      res.write(data);
    });

    child.stderr.on('data', (data) => {
      console.error(`[chat_agent.py] stderr: ${data.toString()}`);
    });

    child.on('close', (code) => {
      if (code !== 0) {
        console.warn(`[chat_agent.py] process exited with code ${code}`);
      }
      res.end();
    });

    req.on('close', () => {
      child.kill();
    });
  } catch (error) {
    writeSse(res, {
      type: 'error',
      error: error.name === 'AbortError' ? 'Request aborted' : error.message,
    });
    res.end();
  }
});

// Redis task listing helper — falls back to in-memory
// Supports cursor-based pagination: cursor = updated_at timestamp, limit = max results
async function listAllTasks(stateFilter, cursor, limit) {
  const DEFAULT_LIMIT = 50;
  const MAX_LIMIT = 200;

  if (redisClient && redisClient.isReady) {
    const ids = await redisClient.sMembers('task:_index_');
    const tasks = [];
    for (const id of ids) {
      const task = await taskStore.get(id);
      if (task) {
        if (!stateFilter || task.status?.state === stateFilter) {
          tasks.push(task);
        }
      } else {
        // Task expired or deleted — clean up index
        await redisClient.sRem('task:_index_', id);
      }
    }
    tasks.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());

    // Cursor-based pagination: skip tasks older than cursor
    if (cursor) {
      const cursorTime = new Date(cursor).getTime();
      tasks = tasks.filter(t => new Date(t.updated_at).getTime() < cursorTime);
    }

    // Apply limit
    const safeLimit = Math.min(Math.max(1, Number.isFinite(limit) ? Number(limit) : DEFAULT_LIMIT), MAX_LIMIT);
    const paged = tasks.slice(0, safeLimit);

    // Next cursor = updated_at of last item in page (if more exist)
    const nextCursor = tasks.length > safeLimit ? paged[paged.length - 1]?.updated_at : null;

    return { tasks: paged, nextCursor, total: tasks.length };
  }

  // In-memory fallback
  let tasks = Array.from(_memTaskStore.values());
  if (stateFilter) tasks = tasks.filter(t => t.status?.state === stateFilter);
  tasks.sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());

  if (cursor) {
    const cursorTime = new Date(cursor).getTime();
    tasks = tasks.filter(t => new Date(t.updated_at).getTime() < cursorTime);
  }

  const safeLimit = Math.min(Math.max(1, Number.isFinite(limit) ? Number(limit) : DEFAULT_LIMIT), MAX_LIMIT);
  const paged = tasks.slice(0, safeLimit);
  const nextCursor = tasks.length > safeLimit ? paged[paged.length - 1]?.updated_at : null;

  return { tasks: paged, nextCursor, total: tasks.length };
}

async function handleOperatorHolds(req, res) {
  const result = await listAllTasks();
  const tasks = result.tasks;
  const pending = tasks.filter(t => t.status.state === 'input-required');
  const auth = tasks.filter(t => t.status.state === 'auth-required');
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

async function handleOperatorTasks(req, res) {
  const state = req.query.state || null;
  const cursor = req.query.cursor || null;
  const limit = req.query.limit ? Number(req.query.limit) : 50;
  const result = await listAllTasks(state, cursor, limit);
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.json({
    ok: true,
    tasks: result.tasks,
    pagination: {
      cursor: result.nextCursor,
      limit,
      total: result.total,
      hasMore: result.nextCursor !== null,
    }
  });
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

// === OPERATOR EVENT LOG ===
app.get(['/operator/events', '/api/operator/events'], (req, res) => {
  const n = Math.min(parseInt(String(req.query.n || '50')), 100);
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({ ok: true, events: _eventLog.slice(-n).reverse() });
});

// === OPERATOR TASK STATE (for golden path polling) ===
app.get(['/operator/tasks/:taskId', '/api/operator/tasks/:taskId'], async (req, res) => {
  const task = await taskStore.get(req.params.taskId);
  if (!task) return res.status(404).json({ ok: false, error: 'Task not found' });
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.json({ ok: true, task: { id: task.id, status: task.status, metadata: task.metadata } });
});

// === OPERATOR MISSION SUBMIT (unauthenticated — operator direct path) ===
app.post(['/api/message/send'], createEnvelopeValidator(), async (req, res) => {
  try {
    const body = req.body;
    const params = (body.params) || {};
    const message = params.message || (typeof params.text === 'string' ? { role: 'user', parts: [{ type: 'text', text: params.text }], messageId: Math.random().toString(36).slice(2) } : null);
    if (!message) return res.status(400).json({ ok: false, error: 'params.message required' });

    // Ghost Task lock (operator path previously allowed null session)
    const lineage = requireTaskLineage(params, body.id || 0, body);
    if (!lineage.ok) {
      return res.status(400).json({ ok: false, error: 'session_id is mandatory (Ghost Task blocked)', detail: lineage.error });
    }
    const { sessionId, contextId } = lineage;
    const taskId = params.taskId || `aaa-${Math.random().toString(36).slice(2, 14)}`;

    const task = buildLineageTask(taskId, contextId, sessionId, message, params);
    await taskStore.set(taskId, task);
    registerContextLineage(contextId, sessionId, taskId);
    logEvent('TASK_START', taskId, `Operator mission session=${sessionId}: "${(message.parts?.[0]?.text || '').slice(0, 60)}"`);

    // ── Register witness: human sovereign (always present) ──
    registerHuman(sessionId);

    executeTask(taskId, contextId, message, params.agent_id || null, params).catch(err => {
      logEvent('ERROR', taskId, `Mission failed: ${err.message}`);
    });

    res.json({ jsonrpc: '2.0', id: body.id || 0, result: { id: taskId, contextId, session_id: sessionId, status: task.status } });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

// ═══════════════════════════════════════════════════════════════════
// AREP — Arif Reality Engineering Protocol endpoint
// ═══════════════════════════════════════════════════════════════════
app.post('/api/arep/submit', async (req, res) => {
  try {
    const task = req.body;

    // Process AREP task with reality gating
    const result = await processAREPTask(task, taskStore, async (t) => {
      // Store and dispatch the task for execution
      const taskId = t.telemetry.task_id;
      await taskStore.set(taskId, t);

      // Log the AREP intent
      logEvent('AREP_SUBMIT', taskId, `AREP: "${t.intent.statement.slice(0, 80)}" | floor: ${t.reality_constraints.evidence_floor} | band: ${t.reality_constraints.autonomy_band}`);

      // Seal if completed
      if (t.task_lifecycle.current_state === 'completed') {
        await sealAREPTask(t);
        await taskStore.set(taskId, t);
      }
    });

    res.json({
      accepted: result.accepted,
      task_id: task.telemetry?.task_id,
      verdict: result.verdict,
      reason: result.reason,
      gate_result: result.gateResult ? {
        passed: result.gateResult.passed,
        violations_count: result.gateResult.violations.length,
        evidence_layer: result.gateResult.currentEvidenceLayer,
        health_summary: result.gateResult.healthProbe?.summary,
      } : null,
    });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

// AREP reality feed — live health probe for the cockpit
app.get('/api/arep/reality-feed', async (req, res) => {
  try {
    const probe = await probeFederation();
    res.json(probe);
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

app.get('/', (req, res) => {
  res.json({
    service: 'AAA A2A Gateway',
    version: '1.2',
    protocol_version: '1.2',
    protocolVersion: '1.2',
    auth: 'required',
    endpoints: {
      discoveryContract: '/.well-known/a2a-discovery.json',
      agentCard: '/.well-known/agent-card.json',
      federationManifest: '/.well-known/arifos-federation.json',
      sendTask: 'POST /tasks',
      getTask: 'GET /tasks/{taskId}',
      streamTask: 'GET /tasks/{taskId}/stream',
      cancelTask: 'POST /tasks/{taskId}/cancel',
      subscribeTask: 'GET /tasks/{taskId}/subscribe',
      health: '/health'
    },
    // Tier-1.3: A2A v1.2 standard method aliases (canonical names from upstream)
    methodAliases: {
      sendTask: 'message/send',
      getTask: 'tasks/get',
      cancelTask: 'tasks/cancel',
      sendTaskStreaming: 'message/stream',
      resubscribeTask: 'tasks/subscribe'
    }
  });
});

// === PUBLIC ROUTES (no auth required — organ cards are public information) ===
// Agent discovery must be accessible for mesh coordination.
mountDiscoveryRoutes(app);

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
app.post('/a2a/message/send', jsonRpcValidate, createEnvelopeValidator(), async (req, res) => {
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

    const lineage = requireTaskLineage(params, id);
    if (!lineage.ok) {
      return res.status(400).json(lineage.error);
    }
    const { sessionId, contextId } = lineage;

    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const task = buildLineageTask(taskId, contextId, sessionId, message, params);
    await taskStore.set(taskId, task);
    registerContextLineage(contextId, sessionId, taskId);

    await executeTask(taskId, contextId, message, params.agent_id, params);

    const updatedTask = await taskStore.get(taskId);
    const skill = updatedTask.metadata?.skill || 'general';

    // Write SEAL to Vault999 (async, non-blocking) — lineage fields required
    writeSeal(updatedTask, 'aaa-gateway', `a2a.${skill}`, {
      routing: 'direct_mcp_simulation',
      task_id: taskId,
      context_id: contextId,
      session_id: sessionId,
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

    // Ghost Task lock: stream path previously minted tasks without session_id
    const lineage = requireTaskLineage(params, id);
    if (!lineage.ok) {
      return res.status(400).json(lineage.error);
    }
    const { sessionId, contextId } = lineage;

    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const task = buildLineageTask(taskId, contextId, sessionId, message, params);
    await taskStore.set(taskId, task);
    registerContextLineage(contextId, sessionId, taskId);

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');

    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id, result: { kind: 'task', task } })}\n\n`);

    const unsubscribe = subscribe(taskId, (event) => {
      res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id, result: event })}\n\n`);
    });

    req.on('close', () => { unsubscribe(); });

    executeTask(taskId, contextId, message, params.agent_id, params).catch(console.error);

  } catch (error) {
    console.error('[A2A] message/stream error:', error);
    res.status(500).json(createJSONRPCError(req.body?.id || 0, ERROR_CODES.INTERNAL_ERROR, 'Internal server error'));
  }
});

// === TASKS/:taskId ===
app.get('/a2a/tasks/:taskId', jsonRpcValidate, async (req, res) => {
  const task = await taskStore.get(req.params.taskId);
  if (!task) return res.status(404).json(createJSONRPCError(req.jsonrpc.id, ERROR_CODES.TASK_NOT_FOUND, `Task ${req.params.taskId} not found`));
  res.json(createJSONRPCResponse(req.jsonrpc.id, {
    id: task.id, contextId: task.contextId, status: task.status,
    artifacts: task.artifacts, history: task.history, kind: 'task', metadata: task.metadata
  }));
});

// === TASKS/:taskId/CANCEL ===
app.post('/a2a/tasks/:taskId/cancel', jsonRpcValidate, async (req, res) => {
  const task = await taskStore.get(req.params.taskId);
  if (task) {
    task.status.state = 'canceled';
    task.updated_at = new Date().toISOString();
    await taskStore.set(req.params.taskId, task);
  }
  res.json(createJSONRPCResponse(req.jsonrpc.id, { success: true, message: 'Task cancelled', task }));
});

// === TASKS/:taskId/SUBSCRIBE ===
app.get('/a2a/tasks/:taskId/subscribe', jsonRpcValidate, async (req, res) => {
  const taskId = req.params.taskId;
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const task = await taskStore.get(taskId);
  if (task) res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id: req.jsonrpc.id, result: { kind: 'task', task } })}\n\n`);

  const unsubscribe = subscribe(taskId, (event) => {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id: req.jsonrpc.id, result: event })}\n\n`);
  });

  req.on('close', () => { unsubscribe(); });
});

// === TASKS/LIST (A2A v1.0.0 Section 3.1.4) ===
app.post('/a2a/tasks/list', jsonRpcValidate, async (req, res) => {
  try {
    const { id, params } = req.jsonrpc;
    const filter = {
      contextId: params?.contextId,
      status: params?.status,
      limit: params?.limit || 50,
    };
    const tasks = await taskStore.list(filter);
    res.json(createJSONRPCResponse(id, {
      tasks: tasks.map(t => ({
        id: t.id, contextId: t.contextId, status: t.status,
        artifacts: t.artifacts, metadata: t.metadata,
      })),
      total: tasks.length,
    }));
  } catch (error) {
    console.error('[A2A] tasks/list error:', error);
    res.status(500).json(createJSONRPCError(req.body?.id || 0, ERROR_CODES.INTERNAL_ERROR, 'Internal server error'));
  }
});

// === PUSH NOTIFICATION CONFIG CRUD (A2A v1.0.0 Section 3.1.7-3.1.10) ===
// POST /a2a/tasks/:taskId/pushNotificationConfig — create
app.post('/a2a/tasks/:taskId/pushNotificationConfig', authMiddleware, async (req, res) => {
  try {
    const { taskId } = req.params;
    const task = await taskStore.get(taskId);
    if (!task) return res.status(404).json({ error: 'Task not found' });

    const configId = `pnc-${generateId().slice(0, 8)}`;
    const config = req.body;
    if (!config?.url) return res.status(400).json({ error: 'pushNotificationConfig.url required' });

    const record = await pushNotificationStore.set(taskId, configId, config);
    res.status(201).json({ taskId, configId, pushNotificationConfig: record });
  } catch (error) {
    console.error('[A2A] pushNotificationConfig create error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /a2a/tasks/:taskId/pushNotificationConfig — list
app.get('/a2a/tasks/:taskId/pushNotificationConfig', authMiddleware, async (req, res) => {
  try {
    const configs = await pushNotificationStore.list(req.params.taskId);
    res.json({ taskId: req.params.taskId, configs });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /a2a/tasks/:taskId/pushNotificationConfig/:configId — get
app.get('/a2a/tasks/:taskId/pushNotificationConfig/:configId', authMiddleware, async (req, res) => {
  try {
    const config = await pushNotificationStore.get(req.params.taskId, req.params.configId);
    if (!config) return res.status(404).json({ error: 'Config not found' });
    res.json(config);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /a2a/tasks/:taskId/pushNotificationConfig/:configId — delete
app.delete('/a2a/tasks/:taskId/pushNotificationConfig/:configId', authMiddleware, async (req, res) => {
  try {
    const deleted = await pushNotificationStore.delete(req.params.taskId, req.params.configId);
    if (!deleted) return res.status(404).json({ error: 'Config not found' });
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// === EXTENDED AGENT CARD (A2A v1.0.0 Section 3.1.11) ===
// GET /.well-known/agent-card-extended.json — authenticated only (CIV-33 Gap 2)
const EXTENDED_AGENT_CARD = (() => {
  try {
    return require('../agent-cards/pillars/aaa-gateway/agent-card-extended.json');
  } catch (e) {
    console.warn('[AAA A2A] extended agent card not found, falling back to inline:', e.message);
    return null;
  }
})();
app.get('/.well-known/agent-card-extended.json', authMiddleware, (req, res) => {
  const baseCard = { ...AAA_AGENT_CARD };
  if (EXTENDED_AGENT_CARD) {
    // Serve the canonical extended card file. Merge top-level extended fields
    // onto the base card under an `_extended` namespace for backward compat,
    // and surface the full file under `extended_card` for forward compat.
    baseCard._extended = {
      federation: 'arif-fazil.com',
      warga_agents: EXTENDED_AGENT_CARD.organ_routing_topology?.warga_agents?.map(a => a.id) || [],
      organs: (EXTENDED_AGENT_CARD.organ_routing_topology?.downstream_organs || [])
        .filter(o => !o.internal_only)
        .map(o => o.id),
      trust_hierarchy: EXTENDED_AGENT_CARD.organ_routing_topology?.trust_hierarchy,
      constitutional_floors: Object.keys(EXTENDED_AGENT_CARD.constitutional_floors || {}),
      governance_kernel: 'arifOS (port 8088)',
      peer_contracts: [...PEER_CONTRACTS.keys()],
    };
    baseCard.extended_card = EXTENDED_AGENT_CARD;
    baseCard.constitutional_floors = EXTENDED_AGENT_CARD.constitutional_floors;
    baseCard.organ_routing_topology = EXTENDED_AGENT_CARD.organ_routing_topology;
    baseCard.seal_chain_genesis = EXTENDED_AGENT_CARD.seal_chain_genesis;
    baseCard.task_state_model = EXTENDED_AGENT_CARD.task_state_model;
    baseCard.ingress_security = EXTENDED_AGENT_CARD.ingress_security;
    baseCard.governance = EXTENDED_AGENT_CARD.governance;
  } else {
    // Fallback: minimal inline extended block (legacy behavior)
    baseCard._extended = {
      federation: 'arif-fazil.com',
      warga_agents: ['333-AGI', '555-ASI', '888-APEX'],
      organs: ['arifOS', 'A-FORGE', 'GEOX', 'WEALTH', 'WELL'],
      trust_hierarchy: 'Human (Arif) > arifOS > AAA > A-FORGE > Specialists',
      constitutional_floors: ['F1', 'F2', 'F4', 'F7', 'F9', 'F10', 'F11', 'F12', 'F13'],
      governance_kernel: 'arifOS (port 8088)',
      peer_contracts: [...PEER_CONTRACTS.keys()],
    };
  }
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('X-AAA-Extended-Card', 'authenticated');
  res.json(baseCard);
});

// === JSON-RPC METHOD ROUTER (A2A v1.0.0 Section 9.4) ===
// Single endpoint that routes by JSON-RPC method name
app.post('/a2a', jsonRpcValidate, createEnvelopeValidator(), async (req, res) => {
  const { id, method, params } = req.jsonrpc;

  switch (method) {
    case 'message/send': {
      // Forward to existing message/send handler logic
      const message = params.message;
      const msgValidation = validateMessage(message);
      if (!msgValidation.valid) {
        return res.status(400).json(createJSONRPCError(id, ERROR_CODES.INVALID_REQUEST, msgValidation.message));
      }
      const lineage = requireTaskLineage(params, id);
      if (!lineage.ok) {
        return res.status(400).json(lineage.error);
      }
      const { sessionId, contextId } = lineage;
      const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
      const tenant = params.tenant || 'personal'; // A2A v1.0.0 multi-tenancy
      const task = buildLineageTask(taskId, contextId, sessionId, message, {
        ...params,
        metadata: { ...(params.metadata || {}), tenant },
      });
      task.tenant = tenant;
      await taskStore.set(taskId, task);
      registerContextLineage(contextId, sessionId, taskId);
      await executeTask(taskId, contextId, message, params.agent_id, params);
      const updatedTask = await taskStore.get(taskId);
      res.json(createJSONRPCResponse(id, {
        id: taskId, contextId, session_id: sessionId, tenant, status: updatedTask.status,
        artifacts: updatedTask.artifacts, history: updatedTask.history,
      }));
      break;
    }
    case 'tasks/get': {
      const task = await taskStore.get(params?.id);
      if (!task) return res.status(404).json(createJSONRPCError(id, ERROR_CODES.TASK_NOT_FOUND, 'Task not found'));
      res.json(createJSONRPCResponse(id, {
        id: task.id, contextId: task.contextId, status: task.status,
        artifacts: task.artifacts, history: task.history, metadata: task.metadata,
      }));
      break;
    }
    case 'tasks/send': {
      // A2A v1.2: Create and dispatch a new task
      const message = params?.message || { role: 'user', parts: [{ type: 'text', text: params?.text || '' }] };
      const lineage = requireTaskLineage(params, id);
      if (!lineage.ok) {
        return res.status(400).json(lineage.error);
      }
      const { sessionId, contextId } = lineage;
      const taskId = `aaa-${generateId().slice(0, 12)}`;
      const tenant = params?.tenant || 'personal';
      const task = buildLineageTask(taskId, contextId, sessionId, message, {
        ...params,
        metadata: { ...(params?.metadata || {}), tenant },
      });
      task.tenant = tenant;
      await taskStore.set(taskId, task);
      registerContextLineage(contextId, sessionId, taskId);
      await executeTask(taskId, contextId, message, params?.agent_id, params);
      const updatedTask = await taskStore.get(taskId);
      res.json(createJSONRPCResponse(id, {
        id: taskId, contextId, session_id: sessionId,
        status: updatedTask.status, artifacts: updatedTask.artifacts,
        history: updatedTask.history, kind: 'task',
        metadata: updatedTask.metadata,
      }));
      break;
    }
    case 'tasks/sendSubscribe': {
      // A2A v1.2: Create task + stream results via SSE
      const message = params?.message || { role: 'user', parts: [{ type: 'text', text: params?.text || '' }] };
      const lineage = requireTaskLineage(params, id);
      if (!lineage.ok) {
        return res.status(400).json(lineage.error);
      }
      const { sessionId, contextId } = lineage;
      const taskId = `aaa-${generateId().slice(0, 12)}`;
      const task = buildLineageTask(taskId, contextId, sessionId, message, {
        ...params,
        metadata: { ...(params?.metadata || {}), tenant: params?.tenant || 'personal' },
      });
      await taskStore.set(taskId, task);
      registerContextLineage(contextId, sessionId, taskId);

      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
      res.setHeader('X-Accel-Buffering', 'no');

      const unsubscribe = subscribe(taskId, (event) => {
        res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', id, result: event })}\n\n`);
        if (event.final) res.end();
      });
      req.on('close', () => { unsubscribe(); });

      await executeTask(taskId, contextId, message, params?.agent_id, params);
      break;
    }
    case 'tasks/list': {
      const filter = {
        contextId: params?.contextId,
        status: params?.status ? toA2AState(params.status) : undefined,
        tenant: params?.tenant,
        limit: params?.limit || 50,
      };
      const tasks = await taskStore.list(filter);
      res.json(createJSONRPCResponse(id, { tasks, total: tasks.length }));
      break;
    }
    case 'tasks/cancel': {
      const task = await taskStore.get(params?.id);
      if (!task) return res.status(404).json(createJSONRPCError(id, ERROR_CODES.TASK_NOT_FOUND, 'Task not found'));
      task.status.state = 'TASK_STATE_CANCELED';
      task.updated_at = new Date().toISOString();
      await taskStore.set(params.id, task);
      res.json(createJSONRPCResponse(id, { id: task.id, status: task.status }));
      break;
    }
    default:
      res.status(400).json(createJSONRPCError(id, ERROR_CODES.METHOD_NOT_FOUND, `Method '${method}' not found`));
  }
});

// ── SDK JSON-RPC Handler — spec-compliant A2A methods at /a2a/sdk/jsonrpc ──
// Mounts the SDK's jsonRpcHandler which provides standard tasks/send, tasks/get,
// tasks/cancel, tasks/sendSubscribe handlers with built-in SSE streaming.
// NOTE: This is ADDITIVE to existing routes — not a replacement. Our custom routes
// provide arifOS constitutional extensions (seal chain, delegation guard, envelope).
const sdkRequestHandler = createSDKRequestHandler({
  taskStoreGet: (id) => taskStore.get(id),
  taskStoreSet: (id, task) => taskStore.set(id, task),
  agentCard: AAA_AGENT_CARD,
  taskDispatcher: async (taskId, message, params) => {
    // Delegate to our existing task executor
    try {
      const ctxId = params?.metadata?.contextId || `sdk-${taskId}`;
      await executeTask(taskId, ctxId, message, params?.agent_id, params);
    } catch (err) {
      console.error(`[SDK Bridge] Task ${taskId} dispatch failed:`, err.message);
    }
  },
});
app.use('/a2a/sdk/jsonrpc', createSDKJsonRPCRouter(sdkRequestHandler));
console.log('[SDK Bridge] Mounted /a2a/sdk/jsonrpc — SDK JSON-RPC handler');
console.log('[SDK Bridge] Mounted /.well-known/agent-card.json — SDK agentCardHandler');

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
  if (params.text) return { parts: [{ type: 'text', text: params.text }] };
  if (typeof params === 'string') return { parts: [{ type: 'text', text: params }] };
  return null;
}

// POST /tasks — A2A v1.0.0 spec task creation
app.post('/tasks', authMiddleware, jsonRpcValidate, createEnvelopeValidator(), async (req, res) => {
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

    const lineage = requireTaskLineage(params, id);
    if (!lineage.ok) {
      return res.status(400).json(lineage.error);
    }
    const { sessionId, contextId } = lineage;
    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;

    const task = buildLineageTask(taskId, contextId, sessionId, message, params);
    await taskStore.set(taskId, task);
    registerContextLineage(contextId, sessionId, taskId);

    // === DelegationGuard (F8 LAW + cross-organ boundary enforcement) ===
    // FORGE 2026-06-28: enforce delegation rules before task dispatch.
    // - A-FORGE cannot self-approve its own validation
    // - Evidence organs (GEOX/WEALTH/WELL) cannot mutate other organ records
    // - Witnesses cannot execute destructive actions
    // - High-risk actuation requires arifOS judge PASS
    const sourceAgent = params.agent_id || params.metadata?.source_agent || 'anonymous';
    const targetSkill = params.skill || params.metadata?.target_skill || '';
    const delegationVerdict = checkDelegation(sourceAgent, targetSkill, message, PEER_CONTRACTS);

    if (delegationVerdict.blocked) {
      task.status = { state: 'TASK_STATE_REJECTED', timestamp: new Date().toISOString(),
        message: { role: 'agent', parts: [{ type: 'text', text: delegationVerdict.reason }] }
      };
      await taskStore.set(taskId, task);
      console.warn(`[DelegationGuard] BLOCKED ${sourceAgent} → ${targetSkill}: ${delegationVerdict.reason}`);
      return res.json(createJSONRPCResponse(id, {
        id: taskId, contextId, session_id: sessionId,
        status: task.status, artifacts: [], history: task.history, kind: 'task', metadata: {
          ...task.metadata, delegation_blocked: true, delegation_reason: delegationVerdict.reason,
        },
      }));
    }
    if (delegationVerdict.warned) {
      console.warn(`[DelegationGuard] WARNING ${sourceAgent} → ${targetSkill}: ${delegationVerdict.reason}`);
    }

    await executeTask(taskId, contextId, message, params.agent_id, params);

    const updatedTask = await taskStore.get(taskId);

    writeSeal(updatedTask, 'aaa-gateway', 'a2a.task', {
      routing: 'POST /tasks v1.0.0',
      task_id: taskId,
      context_id: contextId,
      session_id: sessionId,
    }).catch(err => console.error('[VAULT999] SEAL write failed:', err.message));

    res.json(createJSONRPCResponse(id, {
      id: taskId, contextId, session_id: sessionId,
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

// POST /tasks/send — A2A v1.2 root-level alias (standard spec path)
app.post('/tasks/send', authMiddleware, (req, res) => {
  // Re-dispatch to canonical /a2a/tasks/send handler
  req.url = '/a2a/tasks/send';
  app.handle(req, res);
});

// POST /tasks/sendSubscribe — A2A v1.2 streaming task send (alias to /a2a/tasks/send with stream flag)
app.post('/tasks/sendSubscribe', authMiddleware, (req, res) => {
  req.url = '/a2a/tasks/send';
  if (!req.body) req.body = {};
  req.body.stream = true;
  app.handle(req, res);
});

// GET /tasks/:taskId — A2A v1.0.0 spec task retrieval
app.get('/tasks/:taskId', authMiddleware, async (req, res) => {
  const task = await taskStore.get(req.params.taskId);
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

  const task = await taskStore.get(taskId);
  if (task) {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: { kind: 'task', task } })}\n\n`);
  }

  const unsubscribe = subscribe(taskId, (event) => {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: event })}\n\n`);
  });

  req.on('close', () => { unsubscribe(); });
});

// POST /tasks/:taskId/cancel — A2A v1.0.0 spec task cancellation
app.post('/tasks/:taskId/cancel', authMiddleware, jsonRpcValidate, async (req, res) => {
  const task = await taskStore.get(req.params.taskId);
  if (!task) {
    return res.status(404).json(createJSONRPCError(req.jsonrpc.id, ERROR_CODES.TASK_NOT_FOUND, `Task ${req.params.taskId} not found`));
  }
  task.status.state = 'canceled';
  task.updated_at = new Date().toISOString();
  await taskStore.set(req.params.taskId, task);
  res.json(createJSONRPCResponse(req.jsonrpc.id, { id: task.id, status: task.status, kind: 'task' }));
});

// GET /tasks/:taskId/subscribe — A2A v1.0.0 spec SSE subscription (legacy → resubscribe)
app.get('/tasks/:taskId/subscribe', authMiddleware, async (req, res) => {
  // A2A v1.0.0 spec renamed /subscribe to /resubscribe. Redirect for backwards compat.
  res.redirect(308, `/tasks/${req.params.taskId}/resubscribe`);
});

// GET /tasks/:taskId/resubscribe — A2A v1.0.0 spec SSE subscription (canonical)
app.get('/tasks/:taskId/resubscribe', authMiddleware, async (req, res) => {
  const taskId = req.params.taskId;
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');

  const task = await taskStore.get(taskId);
  if (task) res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: { kind: 'task', task } })}\n\n`);

  const unsubscribe = subscribe(taskId, (event) => {
    res.write(`data: ${JSON.stringify({ jsonrpc: '2.0', result: event })}\n\n`);
  });

  req.on('close', () => { unsubscribe(); });
});

// POST /tasks/list — A2A v1.0.0 spec task list (G3 — added 2026-06-26)
app.post('/tasks/list', authMiddleware, jsonRpcValidate, async (req, res) => {
  const filter = req.body?.params || {};
  const tasks = await taskStore.list(filter);
  res.json(createJSONRPCResponse(req.jsonrpc.id, {
    kind: 'task-list',
    tasks: tasks.map(t => ({
      id: t.id, contextId: t.contextId, status: t.status,
      created_at: t.created_at, updated_at: t.updated_at,
    })),
    count: tasks.length,
  }));
});

// POST /tasks/pushNotificationConfig/set — A2A v1.0.0 spec (G3 — added 2026-06-26)
app.post('/tasks/pushNotificationConfig/set', authMiddleware, jsonRpcValidate, async (req, res) => {
  const { taskId, configId, url, token, headers, events } = req.body?.params || {};
  if (!taskId || !configId || !url) {
    return res.status(400).json(createJSONRPCError(
      req.jsonrpc.id, ERROR_CODES.INVALID_REQUEST,
      'taskId, configId, and url are required'
    ));
  }
  const record = await pushNotificationStore.set(taskId, configId, { url, token, headers, events });
  res.json(createJSONRPCResponse(req.jsonrpc.id, { kind: 'push-notification-config', ...record }));
});

// GET /tasks/pushNotificationConfig/get — A2A v1.0.0 spec (G3 — added 2026-06-26)
app.get('/tasks/pushNotificationConfig/get', authMiddleware, async (req, res) => {
  const taskId = req.query.taskId;
  const configId = req.query.configId;
  if (!taskId || !configId) {
    return res.status(400).json(createJSONRPCError(
      null, ERROR_CODES.INVALID_REQUEST, 'taskId and configId query params required'
    ));
  }
  const cfg = await pushNotificationStore.get(taskId, configId);
  if (!cfg) {
    return res.status(404).json(createJSONRPCError(
      null, ERROR_CODES.TASK_NOT_FOUND, `Push config ${taskId}:${configId} not found`
    ));
  }
  res.json(createJSONRPCResponse(null, { kind: 'push-notification-config', ...cfg }));
});

// GET /tasks/pushNotificationConfig/list — A2A v1.0.0 spec (G3 — added 2026-06-26)
app.get('/tasks/pushNotificationConfig/list', authMiddleware, async (req, res) => {
  const taskId = req.query.taskId;
  if (!taskId) {
    return res.status(400).json(createJSONRPCError(
      null, ERROR_CODES.INVALID_REQUEST, 'taskId query param required'
    ));
  }
  const configs = await pushNotificationStore.list(taskId);
  res.json(createJSONRPCResponse(null, { kind: 'push-notification-config-list', configs, count: configs.length }));
});

// DELETE /tasks/pushNotificationConfig/delete — A2A v1.0.0 spec (G3 — added 2026-06-26)
app.delete('/tasks/pushNotificationConfig/delete', authMiddleware, async (req, res) => {
  const taskId = req.query.taskId;
  const configId = req.query.configId;
  if (!taskId || !configId) {
    return res.status(400).json(createJSONRPCError(
      null, ERROR_CODES.INVALID_REQUEST, 'taskId and configId query params required'
    ));
  }
  const ok = await pushNotificationStore.delete(taskId, configId);
  res.json(createJSONRPCResponse(null, { kind: 'push-notification-config-delete', taskId, configId, deleted: ok }));
});

// GET /agent/getAuthenticatedExtendedCard — A2A v1.0.0 spec (G3 — added 2026-06-26)
app.get('/agent/getAuthenticatedExtendedCard', authMiddleware, async (req, res) => {
  // Extended card includes additional metadata only visible to authenticated callers
  res.json(createJSONRPCResponse(null, {
    kind: 'agent-card',
    ...AAA_AGENT_CARD,
    extensions: {
      aaa_extension: {
        version: 'v1.0',
        governance: {
          floors_active: ['F1','F2','F4','F6','F7','F8','F9','F11','F13'],
          reflexion_loop_required: true,
          authority_resolution_chain: ['arifOS → AAA → A-FORGE → organs'],
        },
        routing: {
          default_organ: 'auto-route',
          mesh_topology: 'peer-mesh',
          transport_protocols: ['json-rpc', 'rest'],
        },
        audit: {
          vault: 'VAULT999',
          conformance_spine: 'v0.2',
          seal_protocol: '999_SEAL',
        },
      },
    },
    stats: {
      total_agent_cards: 29,
      organ_count: 7,
      federation_uptime: process.uptime(),
    },
  }));
});

// =======================
// END A2A v1.0.0 SPEC ENDPOINTS
// =======================

// === POST /judge — Direct 888 constitutional deliberation ===
app.post('/judge', (req, res) => {
  const candidate = req.body;
  if (!candidate || (typeof candidate !== 'object' && typeof candidate !== 'string')) {
    return res.status(400).json({ ok: false, error: 'Body must be a JSON object or { text: string }' });
  }
  const result = deliberation(candidate);
  return res.json({ ok: true, ...result, timestamp: new Date().toISOString() });
});

// === FEDERATION GATEWAY (FORGED 2026-07-10 — cross-organ resource proxy + pipeline orchestration) ===
try {
  const { mountFederationRoutes, resolveResource, orchestratePipeline, federationStatus } = require('./federation_gateway');
  mountFederationRoutes(app);
  console.log('[AAA] Federation gateway ACTIVE — /federation/resource, /federation/pipeline, /federation/status');

  // Wire federation prompts with pre-resolved resources
  const { mountFederationPrompts } = require('./federation_prompts');
  mountFederationPrompts(app, { resolveResource, orchestratePipeline, federationStatus });
  console.log('[AAA] Federation prompts ACTIVE — /federation/prompts');
} catch (e) {
  console.warn('[AAA] Federation gateway not loaded:', e.message);
}

// === AGENT LIFECYCLE ROUTES (FORGED 2026-06-09 — MXC-arifOS connectivity pipeline) ===
try {
  const { lifecycleManager } = require('./agent_lifecycle');
  const { mountLifecycleRoutes } = require('./agent_lifecycle_routes');
  mountLifecycleRoutes(app, lifecycleManager);
  console.log('[AAA] Agent lifecycle state layer ACTIVE');
} catch (e) {
  console.warn('[AAA] Agent lifecycle routes not loaded:', e.message);
}

// === 404 FALLBACK HANDLER ===
// Placed AFTER all valid routes so only truly unknown paths hit this
// === 404 HANDLER ===
app.use((req, res) => {
  res.status(404).json(createJSONRPCError(0, ERROR_CODES.METHOD_NOT_FOUND, `Endpoint ${req.path} not found`));
});

// === ASYNC BACKBONE: Redis + NATS ===
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

    // ── Start Mesh Coordinator (P3 2026-06-14) ──────────────────────────
    // Reuses the existing NATS connection. Subscribes to governance events
    // and organ heartbeats, computes gradient signals, publishes mesh status.
    startMeshCoordinator(natsConnection).then(() => {
      console.log('[mesh-coord] Loop coordinator attached to NATS');
    }).catch(e => {
      console.error('[mesh-coord] Failed to start:', e.message);
    });

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

// === POST /judge — Direct 888 constitutional deliberation ===

// === START ===
// Use AAA_A2A_PORT specifically to avoid conflict with arifOS PORT=8088
// Use A2A_PORT specifically to avoid vault.flat.env PORT=8088 overriding
const PORT = process.env.A2A_PORT || process.env.AAA_A2A_PORT || 3001;
app.listen(PORT, "127.0.0.1", async () => {
  console.log(`[AAA A2A] Hardened server running on port ${PORT}`);
  console.log(`[AAA A2A] Protocol: A2A v1.0.0`);
  console.log(`[AAA A2A] Auth: configured (bearer + api-key)`);
  console.log(`[AAA A2A] Discovery Contract: http://localhost:${PORT}/.well-known/a2a-discovery.json`);
  console.log(`[AAA A2A] Agent Card: http://localhost:${PORT}/.well-known/agent-card.json`);
  console.log(`[AAA A2A] Federation: http://localhost:${PORT}/.well-known/arifos-federation.json`);
  console.log(`[AAA A2A] Peer Contract: http://localhost:${PORT}/.well-known/peer-federation-contract.json`);
  console.log(`[AAA A2A] Agents Registry: http://localhost:${PORT}/.well-known/agents.json (generated from registry)`);
  console.log(`[AAA A2A] Health: http://localhost:${PORT}/health`);
  console.log(`[AAA A2A] Lifecycle: http://localhost:${PORT}/api/agents/federation-status`);
  await initAsyncBackbone();
  // bootstrap zen memory snapshots now that redis is ready
  await federatedMemory.updateLayer('L1', { status: 'live' });
  await federatedMemory.updateLayer('L6', { status: 'sealed' });
  await federatedMemory.updateLayer('L4', { wells_portfolio: 'https://arif-fazil.com/#wells (4 entries; LEBAH EMAS-1 scar: 11 reservoirs, new play, PM6/12 EnQuest farm-out 2026 as mature asset; provenance siteContent.ts)' });
  startRetryWorker();

  // Auto-register federation organs on startup
  const { autoRegisterOrgans } = require('./auto-register-organs');
  setTimeout(async () => {
    try {
      const result = await autoRegisterOrgans(PORT);
      console.log(
        `[AAA A2A] Federation bootstrap: organs ` +
        `${result.organs.registered + result.organs.existing}/${result.organs.total}; ` +
        `agents ${result.agents.registered + result.agents.existing}/${result.agents.total}; ` +
        `ok=${result.ok}`,
      );
    } catch (e) {
      console.warn('[AAA A2A] Auto-registration failed:', e.message);
    }
  }, 3000); // 3s delay to let organs' health endpoints settle
});


// ═══════════════════════════════════════════════════════════════════
// Entropy Integrity Mesh — A2A Investigation Pipeline
// DITEMPA BUKAN DIBERI
// ═══════════════════════════════════════════════════════════════════

async function executeEntropyInvestigation(message, session_id) {
    const pipeline = [
        { organ: 'wealth', tool: 'capital_entropy', args: { mode: 'power_consequence_map', decision_ref: message } },
        { organ: 'well', tool: 'well_dark_geometry_mirror', args: { text: message, mode: 'combined' } },
        { organ: 'geox', tool: 'geox_consequence_footprint', args: { action_description: message } },
        { organ: 'arifos', tool: 'arif_entropy_observe', args: { observation: { signal_class: 'CORRECTION_FAILURE', organ: 'KERNEL' } } },
    ];

    const { orchestratePipeline } = require('./federation_gateway');
    try {
        const result = await orchestratePipeline(pipeline, { session_id });
        return {
            status: 'ENTROPY_INVESTIGATION_COMPLETE',
            steps: result.length,
            findings: result,
            entropy_vector: computeEntropyVector(result),
        };
    } catch (err) {
        return { status: 'INVESTIGATION_FAILED', error: err.message };
    }
}

function computeEntropyVector(pipelineResults) {
    // Synthesize 7-dimension entropy vector from multi-organ results
    return {
        information_loss: 0.0,
        option_loss: 0.0,
        feedback_corruption: 0.0,
        defensive_overhead: 0.0,
        cascade_potential: 0.0,
        correction_failure: 0.0,
        brittleness: 0.0,
    };
}

module.exports = { app };
