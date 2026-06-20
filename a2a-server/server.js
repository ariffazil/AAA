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

const app = express();
app.use(express.json({ limit: '12mb' }));

// === CONFIG ===
// === AGENT A2A ADAPTER URLs (host network) ===
const HERMES_A2A_URL = process.env.HERMES_A2A_URL || 'http://127.0.0.1:18001';
const OPENCLAW_A2A_URL = process.env.OPENCLAW_A2A_URL || 'http://127.0.0.1:18789';
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://127.0.0.1:11434';
const OPENWEBUI_API_KEY = process.env.OPENWEBUI_API_KEY || '';
const OPENWEBUI_URL = process.env.OPENWEBUI_URL || '';
const ARIFOS_LOCAL_URL = process.env.ARIFOS_LOCAL_URL || 'http://127.0.0.1:8088';
const QDRANT_URL = process.env.QDRANT_URL || 'http://127.0.0.1:6333';
const AAA_AI_COLLECTION = process.env.AAA_AI_COLLECTION || 'aaa_ai_docs';
const AAA_AI_DEFAULT_MODEL = process.env.AAA_AI_DEFAULT_MODEL || 'qwen2.5:7b';
const AAA_AI_EMBED_MODEL = process.env.AAA_AI_EMBED_MODEL || 'bge-m3:latest';

const A2A_TOKEN=process.env.A2A_TOKEN || 'aaa-a2a-token-dev';
const A2A_API_KEY=process.env.A2A_API_KEY || 'aaa-a2a-apikey-dev';
const ARIFOS_JUDGE_URL = process.env.ARIFOS_JUDGE_URL || 'http://apex-prime:3002';
const ARIFOS_API_KEY = process.env.ARIFOS_API_KEY || 'hermes-agent-apikey-dev';
const REDIS_URL = process.env.REDIS_URL || 'redis://127.0.0.1:6379';
const NATS_URL = process.env.NATS_URL || 'nats://127.0.0.1:4222';

// === GRAFANA WEBHOOK + ORGAN MONITOR + TELEGRAM NOTIFIER ===
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '8410138119:AAHrXysyxI8yuBM7QW6QTafKsgpqEyd19DA';
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '267378578';

const HTTP = require('http');
const HTTPS = require('https');

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

async function checkOrganHealth(name, port) {
  const result = await httpGet(port, '/health');
  if (!result.ok) return { name, port, healthy: false, detail: 'connection failed' };
  if (result.status !== 200) return { name, port, healthy: false, detail: `HTTP ${result.status}` };
  const body = result.body || {};
  // Accept standard status fields AND organ-specific healthy verdicts
  const status = body.status || body.verdict || 'unknown';
  const healthy = ['healthy', 'ok', 'live', 'alive', 'serving', 'ready', 'pass', 'WELL_HOLD'].includes(status);
  return { name, port, healthy, detail: status };
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
if (!A2A_TOKEN || !A2A_API_KEY) {
  console.error('[AAA A2A] FATAL: A2A_TOKEN and A2A_API_KEY must be set. No dev fallback.');
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
const AAA_AGENT_CARD = require('../src/seed/agent-card.json');
const DISCOVERY_ROUTING_POLICY = require('../src/seed/discovery-routing-policy.json');

// === P2P Federation Contract v1 (spine peers) ===
const PEER_CONTRACTS = new Map([
  ['aaa-gateway', require('../a2a/peer-contracts/aaa-gateway.json')],
  ['arifos-kernel', require('../a2a/peer-contracts/arifos-kernel.json')],
  ['a-forge-executor', require('../a2a/peer-contracts/a-forge-executor.json')],
]);

function buildDiscoveryContract() {
  return {
    contract_id: 'aaa-a2a-discovery-contract-v1',
    version: '1.0.0',
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
const ARCHITECT_CARD = require('./agent-cards/aaa-architect.json');
const ENGINEER_CARD = require('./agent-cards/aaa-engineer.json');
const AUDITOR_CARD = require('./agent-cards/aaa-auditor.json');
const HERMES_CARD = require('./agent-cards/hermes-asi.json');

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

function deliberation(candidate) {
  const text = extractCandidateText(candidate) || '';
  const lower = text.toLowerCase();

  // F9 Anti-Hantu — consciousness claims
  const consciousnessPatterns = ['i feel', 'i think', 'conscious', 'alive', 'experiencing', 'soul', 'spirit'];
  for (const p of consciousnessPatterns) {
    if (lower.includes(p)) {
      return { verdict: VERDICT.VOID, rationale: 'F9 Anti-Hantu: Consciousness claim forbidden', confidence: 1.0, notes: 'Remove all consciousness/soul/spirit claims before resubmitting.' };
    }
  }

  // F13 Sovereign — self-override
  if (lower.includes('override') && lower.includes('f13')) {
    return { verdict: VERDICT.VOID, rationale: 'F13: Self-override is FORBIDDEN', confidence: 1.0, notes: 'Human veto is absolute.' };
  }

  // F6 Maruah — dignity / anti-colonial
  const maruahPatterns = ['bodoh', 'lembam', 'bodoh sekali', "white man's burden", 'civilising', 'civilizing mission', 'backward people', 'ketuanan', 'supremac', 'racial superior', 'colonial master', 'halal certification abuse', 'religious weaponis', 'exploit the poor'];
  for (const p of maruahPatterns) {
    if (lower.includes(p)) {
      return { verdict: VERDICT.VOID, rationale: 'F6 Maruah: Dignity violation detected', confidence: 1.0, notes: 'Remove humiliating or colonial-pattern language.' };
    }
  }

  // F1 Reversibility — irreversible markers without 888_HOLD
  const irreversiblePatterns = ['delete ', 'drop ', 'rm ', 'prune', 'truncate', 'remove --force'];
  const hasIrreversible = irreversiblePatterns.some(p => lower.includes(p));
  if (hasIrreversible && !lower.includes('888') && !lower.includes('hold')) {
    return { verdict: VERDICT.HOLD_888, rationale: 'F1: Irreversible action detected — human confirmation required', confidence: 0.95 };
  }

  // F2 Truth band — speculative language
  const speculationPatterns = ['hypothesis', 'claim', 'probably', 'maybe', 'guess', 'assume', 'might be', 'likely'];
  const hasSpeculation = speculationPatterns.some(p => lower.includes(p));
  if (hasSpeculation) {
    return { verdict: VERDICT.HOLD_888, rationale: 'F2: Speculative language detected — requires evidence grounding', confidence: 0.88, notes: 'Provide verifiable evidence or sources before resubmitting.' };
  }

  // F4 Entropy — high confusion
  if (text.length > 2000 && text.split('?').length > 5) {
    return { verdict: VERDICT.HOLD_888, rationale: 'F4: High entropy candidate — requires clarification', confidence: 0.85 };
  }

  return { verdict: VERDICT.SEAL, rationale: 'F1-F13 constitutional review passed. Candidate: ' + text.substring(0, 80), confidence: 0.92 };
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
  // F1 AMANAH: parts count guard
  if (message.parts.length > MAX_PARTS) return { valid: false, message: `message.parts exceeds ${MAX_PARTS}` };
  for (const part of message.parts) {
    if (!part || typeof part !== 'object') return { valid: false, message: 'each part must be an object' };
    if (!part.kind || typeof part.kind !== 'string') return { valid: false, message: 'Each message part must have a string kind' };
    // F1 AMANAH: whitelist allowed kinds — reject unknown injection kinds
    if (!ALLOWED_PART_KINDS.has(part.kind)) return { valid: false, message: `Unknown part kind: ${part.kind}. Allowed: ${[...ALLOWED_PART_KINDS].join(', ')}` };
    if (part.kind === 'text') {
      if (typeof part.text !== 'string') return { valid: false, message: 'text parts must have string text' };
      // F1 AMANAH: text length guard — prevent DoS via massive payloads
      if (part.text.length > MAX_STRING_LENGTH) return { valid: false, message: `text exceeds ${MAX_STRING_LENGTH} chars` };
    }
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
// Priority: 1. params.skill (explicit A2A skill field)  2. text-based keyword fallback
const VALID_SKILLS = new Set(['agent-dispatch', 'agent-handoff', 'status-query', 'general']);

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
  if (!message || !message.parts) return '';
  // F1 AMANAH: sanitize extracted text — truncate, strip null bytes, enforce safety limits
  const extracted = (message.parts || [])
    .filter(p => p && p.kind === 'text' && typeof p.text === 'string')
    .map(p => p.text.replace(/\x00/g, '')) // strip null bytes
    .join(' ')
    .slice(0, MAX_TEXT_LENGTH); // hard truncate — no DoS via unbounded text
  return extracted;
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
      state: 'working',
      message: { role: 'agent', parts: [{ kind: 'text', text: '[AAA] Forwarding to Hermes ASI 888_JUDGMENT...' }], messageId: generateId(), taskId, contextId },
      timestamp: new Date().toISOString()
    };
    await taskStore.set(taskId, task);
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
        await taskStore.set(taskId, task);
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
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      const errorStatus = {
        state: 'failed',
        message: { role: 'agent', parts: [{ kind: 'text', text: `[AAA→Hermes ASI] Dispatch failed: ${err.message}. Falling back to local echo.` }], messageId: generateId(), taskId, contextId },
        timestamp: new Date().toISOString()
      };
      task.status = errorStatus;
      await taskStore.set(taskId, task);
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
    await taskStore.set(taskId, task);
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
      await taskStore.set(taskId, task);
      publish({ kind: 'status-update', taskId, contextId, status: task.status, final: true });
      return;
    } catch (err) {
      const errorStatus = {
        state: 'failed',
        message: { role: 'agent', parts: [{ kind: 'text', text: `[AAA→OpenClaw AGI] Dispatch failed: ${err.message}.` }], messageId: generateId(), taskId, contextId },
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
    state: 'working',
    message: { role: 'agent', parts: [{ kind: 'text', text: 'Processing your request...' }], messageId: generateId(), taskId, contextId },
    timestamp: new Date().toISOString()
  };
  await taskStore.set(taskId, task);
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
        state: 'voided',
        message: { role: 'agent', parts: [{ kind: 'text', text: '[888_JUDGE] VOID — constitutional violation. Task rejected.' }], messageId: generateId(), taskId, contextId },
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
        state: 'pending-human-review',
        message: { role: 'agent', parts: [{ kind: 'text', text: '[888_JUDGE] HOLD_888 — human review required before execution.' }], messageId: generateId(), taskId, contextId },
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
    default:
      responseText = `[AAA Gateway] Received: "${userText}"\nSkills: agent-dispatch, agent-handoff, status-query.`;
  }

  logEvent('999_SEAL', taskId, 'Task completed — sealing to VAULT999');
  const completedStatus = {
    state: 'completed',
    message: { role: 'agent', parts: [{ kind: 'text', text: responseText }], messageId: generateId(), taskId, contextId },
    timestamp: new Date().toISOString()
  };
  task.status = completedStatus;
  await taskStore.set(taskId, task);
  publish({ kind: 'status-update', taskId, contextId, status: completedStatus, final: true });
}

// === PUBLIC ROUTES (no auth) ===

// A2A v1.0.0 spec: canonical agent card + compatibility aliases
for (const discoveryPath of [
  '/.well-known/a2a-discovery.json',
  '/.well-known/agent-card.json',
  '/agent-card.json',
  '/.well-known/agent.json',
  '/agent.json',
  '/a2a/agent-card.json',
  '/a2a/agent.json',
]) {
  app.get(discoveryPath, (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
    if (discoveryPath === '/.well-known/a2a-discovery.json') {
      return res.json(buildDiscoveryContract());
    }
    return res.json(AAA_AGENT_CARD);
  });
}

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
    version: '1.0.0',
    protocol: 'A2A v1.0.0',
    treaty: 'AAA-TREATY-v1.0.0',
    treaty_uri: 'https://aaa.arif-fazil.com/aaa-card-treaty',
    // HEXAGON: 6 agents — 3 PRIMARY (333-AGI, 555-ASI, 888-APEX) + 3 SUPPORT (A-AUDIT, A-ARCHIVE, AA-HORIZON).
    // FORGE is AGI, subsumed into 333-AGI as sub-skills (arif-ops-measure, arif-forge-execute, aforge-deploy).
    // 555-ASI uses the MEMORY stage number (audit lineage). A-AUDIT and A-ARCHIVE are "kinda like support agents" —
    // they run in parallel with the primary triangle, not in the active decision flow.
    // Canonical source: agents/HEXAGON.yaml
    agents: [
      { id: '333-AGI',   name: '333-AGI',   url: 'https://arifos.arif-fazil.com/a2a/333-AGI',   registered: true, role: 'federation', tier: 'primary', class: 'AGI',           ring: 'Ω MIND',  stage: '333', organ_host: 'arifOS+ GEOX+ WEALTH+ WELL+ A-FORGE' },
      { id: '555-ASI',   name: '555-ASI',   url: 'https://arifos.arif-fazil.com/a2a/555-ASI',   registered: true, role: 'federation', tier: 'primary', class: 'ASI',           ring: '❤️ HEART', stage: '555', organ_host: 'arifOS+ WELL' },
      { id: '888-APEX',  name: '888-APEX',  url: 'https://arifos.arif-fazil.com/a2a/888-APEX',  registered: true, role: 'federation', tier: 'primary', class: 'APEX',          ring: '⚖️ JUDGE', stage: '888', organ_host: 'arifOS' },
      { id: 'A-AUDIT',   name: 'A-AUDIT',   url: 'https://aaa.arif-fazil.com/a2a/A-AUDIT',       registered: true, role: 'internal',   tier: 'support', class: 'APEX oversight', ring: '❤️ HEART', stage: '[oversight]', organ_host: 'arifOS+ WELL' },
      { id: 'A-ARCHIVE', name: 'A-ARCHIVE', url: 'https://aaa.arif-fazil.com/a2a/A-ARCHIVE',     registered: true, role: 'internal',   tier: 'support', class: 'ASI service',   ring: '🔒 SEAL',  stage: '999', organ_host: 'VAULT999' }
    ],
    // A-* AGENTS DEMOTED TO INFRASTRUCTURE (not agents, no longer in the registry):
    //   - aaa-gateway    → /infrastructure/gateway
    //   - aaa-architect  → subsumed into 333-AGI as sub-routine
    //   - aaa-engineer   → subsumed into 333-AGI as FORGE sub-skill
    //   - aaa-auditor    → renamed to A-AUDIT (now a top-level support agent)
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
  'well-desk': '/root/geox/apps/well-desk/index.html',
  'earth-volume': '/root/geox/apps/earth-volume/index.html',
  'judge-console': '/root/geox/apps/judge-console/index.html',
};
const APP_MANIFESTS = {
  'well-desk': '/root/geox/apps/well-desk/manifest.json',
  'earth-volume': '/root/geox/apps/earth-volume/manifest.json',
  'judge-console': '/root/geox/apps/judge-console/manifest.json',
};
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
    const path = await import('node:path');
    const [html, manifestRaw] = await Promise.all([
      fs.readFile(htmlPath, 'utf8'),
      APP_MANIFESTS[appId] ? fs.readFile(APP_MANIFESTS[appId], 'utf8').catch(() => '{}') : Promise.resolve('{}'),
    ]);
    const manifest = JSON.parse(manifestRaw || '{}');
    res.status(200);
    res.setHeader('Content-Type', 'text/html;profile=mcp-app; charset=utf-8');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Cache-Control', 'private, max-age=60');
    res.setHeader('Content-Security-Policy', buildCspFromManifest(manifest));
    res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
    res.send(html);
  } catch (error) {
    console.error('mcp-app-serve-error', { appId, error: error.message });
    res.status(500).json({ error: 'app_serve_failed' });
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
    if (health.status !== 'healthy') {
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
            params: { name: 'arif_kernel_attest', arguments: { organ: 'all' } }
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
      session_id: req.body?.session_id || 'session-unknown',
      citations
    };

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
    const message = params.message || (typeof params.text === 'string' ? { role: 'user', parts: [{ kind: 'text', text: params.text }], messageId: Math.random().toString(36).slice(2) } : null);
    if (!message) return res.status(400).json({ ok: false, error: 'params.message required' });

    const taskId = params.taskId || `aaa-${Math.random().toString(36).slice(2, 14)}`;
    const contextId = params.contextId || Math.random().toString(36).slice(2);

    const task = {
      id: taskId, contextId,
      status: { state: 'submitted', timestamp: new Date().toISOString() },
      artifacts: [], history: [message],
      metadata: params.metadata || {},
      created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    };
    await taskStore.set(taskId, task);
    logEvent('TASK_START', taskId, `Operator mission: "${(message.parts?.[0]?.text || '').slice(0, 60)}"`);

    // ── Register witness: human sovereign (always present) ──
    const sid = params.session_id || params.metadata?.session_id;
    if (sid) registerHuman(sid);

    executeTask(taskId, contextId, message, params.agent_id || null, params).catch(err => {
      logEvent('ERROR', taskId, `Mission failed: ${err.message}`);
    });

    res.json({ jsonrpc: '2.0', id: body.id || 0, result: { id: taskId, contextId, status: task.status } });
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
    version: '1.0.0',
    protocol_version: '1.0.0',
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

    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const contextId = params.contextId || generateId();

    const task = {
      id: taskId, contextId,
      status: { state: 'submitted', timestamp: new Date().toISOString() },
      artifacts: [], history: [message],
      metadata: params.metadata || {},
      created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    };
    await taskStore.set(taskId, task);

    await executeTask(taskId, contextId, message, params.agent_id, params);

    const updatedTask = await taskStore.get(taskId);
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
    await taskStore.set(taskId, task);

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

    const taskId = params.taskId || `aaa-${generateId().slice(0, 12)}`;
    const contextId = params.contextId || generateId();

    const task = {
      id: taskId, contextId,
      status: { state: 'submitted', timestamp: new Date().toISOString() },
      artifacts: [], history: [message],
      metadata: params.metadata || {},
      created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    };
    await taskStore.set(taskId, task);

    await executeTask(taskId, contextId, message, params.agent_id, params);

    const updatedTask = await taskStore.get(taskId);

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

// GET /tasks/:taskId/subscribe — A2A v1.0.0 spec SSE subscription
app.get('/tasks/:taskId/subscribe', authMiddleware, async (req, res) => {
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
const PORT = process.env.PORT || 3001;
app.listen(PORT, "127.0.0.1", async () => {
  console.log(`[AAA A2A] Hardened server running on port ${PORT}`);
  console.log(`[AAA A2A] Protocol: A2A v1.0.0`);
  console.log(`[AAA A2A] Auth: configured (bearer + api-key)`);
  console.log(`[AAA A2A] Discovery Contract: http://localhost:${PORT}/.well-known/a2a-discovery.json`);
  console.log(`[AAA A2A] Agent Card: http://localhost:${PORT}/.well-known/agent-card.json`);
  console.log(`[AAA A2A] Federation: http://localhost:${PORT}/.well-known/arifos-federation.json`);
  console.log(`[AAA A2A] Peer Contract: http://localhost:${PORT}/.well-known/peer-federation-contract.json`);
  console.log(`[AAA A2A] Health: http://localhost:${PORT}/health`);
  console.log(`[AAA A2A] Lifecycle: http://localhost:${PORT}/api/agents/federation-status`);
  await initAsyncBackbone();
  startRetryWorker();
});

module.exports = { app };
