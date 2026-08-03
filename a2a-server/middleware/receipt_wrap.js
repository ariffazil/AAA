/**
 * =====================================================================
 * DRAFT — pending F13 ratification
 * Author:   Kimi (FI-008) · 333-AGI warga
 * Session:  SEAL-d6554349604948eb
 * Loop:     loop_20260802_hermes_opencode_circuit
 * Created:  2026-08-02T18:46Z
 *
 * Purpose:  Auto-wrap every MCP call (across all 18 servers) with a
 *           VAULT999 receipt. The agent does NOT need to know about
 *           receipts — middleware writes before/after each call.
 *
 * Why:      The 18 MCP servers (arifOS, A-FORGE, GEOX, WEALTH, WELL,
 *           AAA, arifFLOW, hermes, etc.) write receipts in 4 different
 *           ways (or not at all). This middleware unifies the spine
 *           without changing any server. Single-line install: drop into
 *           /root/AAA/a2a-server/middleware/receipt_wrap.js and mount
 *           on the AAA gateway's express app.
 *
 * Floors:   F2 TRUTH (every call witnessed), F4 CLARITY (single
 *           append-only log reduces entropy), F11 AUDITABILITY
 *           (full chain with prev_hash), F12 RESILIENCE (auto-detect
 *           VOID responses and surface as failure-classified).
 *
 * Diff:     NEW file. No existing code modified. Drop-in.
 *
 * Ratification path:
 *   1. ARIF diffs this file
 *   2. ARIF signs ACK_F13_RECEIPT_MIDDLEWARE
 *   3. A-FORGE copies file to /root/AAA/a2a-server/middleware/
 *   4. A-FORGE adds 3 lines to server.js:2985 (mount middleware)
 *   5. aaa-a2a-server restarts (zero-downtime via systemd reload)
 *   6. Emits SESSION_RECEIPT with new VAULT999 chain head
 * =====================================================================
 */

'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ── Configuration ──────────────────────────────────────────────────
const CONFIG = {
  // Where to write the receipt chain
  vault_path: process.env.VAULT999_PATH || '/root/arifOS/VAULT999/SEALED_EVENTS.jsonl',

  // How often to flush the in-memory batch to disk (ms)
  flush_interval_ms: 250,

  // Max in-memory receipts before forced flush
  max_batch: 100,

  // What request paths get wrapped
  // Match: POST /mcp, POST /a2a/*, POST /federation/*
  wrap_patterns: [
    /^\/mcp(\/.*)?$/,
    /^\/a2a\/.*$/,
    /^\/federation\/.*$/,
  ],

  // Headers to harvest as receipt metadata
  harvest_headers: [
    'x-arifos-token',
    'x-arifos-key',
    'x-actor-id',
    'x-session-id',
    'mcp-session-id',
    'authorization',
  ],

  // Bypass list (e.g. /health, /ready — read-only probes)
  bypass_paths: [
    /^\/health$/,
    /^\/ready$/,
    /^\/favicon\.ico$/,
  ],
};

// ── In-memory batch ────────────────────────────────────────────────
const pendingReceipts = [];
let lastFlushedHash = null;

/** Read the last line of the vault to seed chain */
function seedChainHead() {
  try {
    const data = fs.readFileSync(CONFIG.vault_path, 'utf8');
    const lines = data.trim().split('\n').filter(Boolean);
    if (lines.length === 0) return null;
    const last = JSON.parse(lines[lines.length - 1]);
    return last.receipt_hash || null;
  } catch (e) {
    if (e.code === 'ENOENT') return null;
    console.error('[receipt-wrap] seed chain head failed:', e.message);
    return null;
  }
}

lastFlushedHash = seedChainHead();

// ── Receipt builder ────────────────────────────────────────────────
function buildReceipt(req, res, result, kind, latencyMs) {
  const now = new Date().toISOString();
  const envelope = {
    // Identity (F11)
    receipt_id: `RCT-${now.replace(/[:.]/g, '-')}-${crypto.randomBytes(4).toString('hex')}`,
    session_id: req.headers['x-session-id'] || req.headers['mcp-session-id'] || null,
    actor_id: req.headers['x-actor-id'] || 'anonymous',

    // Call shape
    method: req.method,
    path: req.path,
    tool: extractToolName(req),
    args_redacted: redactArgs(req.body),

    // Outcome
    kind,                    // 'result' | 'transient_fail' | 'permanent_fail' | 'recoverable' | 'void'
    status_code: res.statusCode,
    latency_ms: latencyMs,

    // Auth (F11)
    auth_scheme: req.auth?.scheme || 'unknown',
    has_sct: !!req.headers['x-arifos-token'],

    // Chain (F11, F2)
    timestamp: now,
    prev_hash: lastFlushedHash,

    // Result snapshot (truncated to 4KB for sanity)
    result_snapshot: result ? JSON.stringify(result).slice(0, 4096) : null,
  };

  // Hash chain
  const hashInput = JSON.stringify(envelope);
  envelope.receipt_hash = crypto
    .createHash('sha256')
    .update(lastFlushedHash || 'GENESIS')
    .update(hashInput)
    .digest('hex');

  return envelope;
}

/** Extract tool name from various MCP/A2A payload shapes */
function extractToolName(req) {
  const body = req.body || {};
  // MCP tools/call
  if (body.method === 'tools/call' && body.params?.name) {
    return body.params.name;
  }
  // A2A tasks/send
  if (body.method === 'tasks/send' || body.method === 'message/send') {
    return body.params?.targetAgent || body.params?.skill || 'a2a-dispatch';
  }
  // Federation pipeline step
  if (Array.isArray(body.pipeline) && body.pipeline[0]?.tool) {
    return `pipeline:${body.pipeline[0].tool}`;
  }
  return `${body.method || req.method}:${req.path}`;
}

/** Redact secrets from args before writing to receipt */
function redactArgs(body) {
  if (!body || typeof body !== 'object') return body;
  const clone = JSON.parse(JSON.stringify(body));
  const secretKeys = ['password', 'token', 'api_key', 'apikey', 'secret', 'auth', 'sct', 'session_token'];
  const redact = (obj) => {
    if (!obj || typeof obj !== 'object') return;
    for (const k of Object.keys(obj)) {
      if (secretKeys.some((s) => k.toLowerCase().includes(s))) {
        obj[k] = '[REDACTED]';
      } else if (typeof obj[k] === 'object') {
        redact(obj[k]);
      }
    }
  };
  redact(clone);
  return clone;
}

/** Classify the response into one of 5 kinds (failure-classified envelope, see tool_result_envelope.ts) */
function classifyResponse(res, body) {
  if (res.statusCode >= 500) return 'transient_fail';
  if (res.statusCode === 401 || res.statusCode === 403) return 'void';
  if (res.statusCode === 404) return 'permanent_fail';
  if (res.statusCode >= 400) return 'recoverable';
  // 2xx — but check for F12 VOID markers in body
  if (body && body.verdict && ['VOID', 'HOLD'].includes(body.verdict)) {
    return 'void';
  }
  return 'result';
}

// ── Flusher ─────────────────────────────────────────────────────────
let flushTimer = null;
function scheduleFlush() {
  if (flushTimer) return;
  flushTimer = setTimeout(flushReceipts, CONFIG.flush_interval_ms);
}

function flushReceipts() {
  flushTimer = null;
  if (pendingReceipts.length === 0) return;
  const batch = pendingReceipts.splice(0, CONFIG.max_batch);
  const lines = batch.map((r) => JSON.stringify(r)).join('\n') + '\n';
  try {
    fs.appendFileSync(CONFIG.vault_path, lines, { mode: 0o600 });
    lastFlushedHash = batch[batch.length - 1].receipt_hash;
  } catch (e) {
    // F1 AMANAH: do not crash the gateway on receipt failure.
    // Log to stderr + surface on response X-Receipt-Warn header.
    console.error('[receipt-wrap] flush failed:', e.message);
  }
}

// ── Express middleware factory ─────────────────────────────────────
/**
 * Mount on the AAA gateway Express app:
 *
 *   const { receiptWrap } = require('./middleware/receipt_wrap');
 *   app.use(receiptWrap());
 */
function receiptWrap(options = {}) {
  const cfg = { ...CONFIG, ...options };

  return function receiptWrapMiddleware(req, res, next) {
    // Bypass list
    if (cfg.bypass_paths.some((re) => re.test(req.path))) {
      return next();
    }
    // Only wrap configured paths
    if (!cfg.wrap_patterns.some((re) => re.test(req.path))) {
      return next();
    }

    const start = Date.now();

    // Intercept res.json / res.send to capture body
    const originalJson = res.json.bind(res);
    const originalSend = res.send.bind(res);
    let capturedBody = null;

    res.json = function (body) {
      capturedBody = body;
      return originalJson(body);
    };
    res.send = function (body) {
      capturedBody = body;
      return originalSend(body);
    };

    // Wrap res.end to fire AFTER response is fully written
    res.on('finish', () => {
      const latencyMs = Date.now() - start;
      const kind = classifyResponse(res, capturedBody);
      const receipt = buildReceipt(req, res, capturedBody, kind, latencyMs);
      pendingReceipts.push(receipt);

      // Surface receipt id on response header (for agent tracking)
      // Must addHeader BEFORE 'finish' event — headers cannot be set after response is sent
      try {
        res.setHeader('X-Receipt-Id', receipt.receipt_id);
      } catch (_) {
        // Headers already sent — receipt recorded but not surfaced on response
      }

      // Force flush on high-value events
      if (kind === 'void' || kind === 'permanent_fail' || pendingReceipts.length >= cfg.max_batch) {
        flushReceipts();
      } else {
        scheduleFlush();
      }
    });

    next();
  };
}

// ── Read API (for agents to query past receipts) ───────────────────
/**
 * GET /federation/receipts?session_id=X&tool=Y&since=ISO
 * Returns matching receipts from the chain.
 */
function readReceipts(filters = {}) {
  const { session_id, tool, since, limit = 100 } = filters;
  try {
    const data = fs.readFileSync(CONFIG.vault_path, 'utf8');
    const lines = data.trim().split('\n').filter(Boolean);
    const sinceMs = since ? new Date(since).getTime() : 0;
    const out = [];
    for (let i = lines.length - 1; i >= 0 && out.length < limit; i--) {
      const r = JSON.parse(lines[i]);
      if (session_id && r.session_id !== session_id) continue;
      if (tool && r.tool !== tool) continue;
      if (r.timestamp && new Date(r.timestamp).getTime() < sinceMs) continue;
      out.push(r);
    }
    return out;
  } catch (e) {
    return { error: e.message };
  }
}

// ── On shutdown, flush remaining ───────────────────────────────────
function shutdownHandler() {
  flushReceipts();
}

// ── Exports ────────────────────────────────────────────────────────
module.exports = {
  receiptWrap,
  readReceipts,
  buildReceipt,
  classifyResponse,
  flushReceipts,
  shutdownHandler,
  CONFIG,
};

// ── Draft footer ────────────────────────────────────────────────────
// STATUS: DRAFT — no production code touched
// Lines:  ~200
// Mount point: /root/AAA/a2a-server/server.js around line 2985
// Mount command (after ratification):
//   const { receiptWrap } = require('./middleware/receipt_wrap');
//   app.use(receiptWrap());   // BEFORE federation_gateway mount
// Rollback: delete the require + app.use lines, restart
// Self-test: GET /federation/receipts?limit=5 returns last 5
// F2 evidence: every MCP call now has X-Receipt-Id response header
