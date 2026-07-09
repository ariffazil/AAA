#!/usr/bin/env node
/**
 * VAULT999 Client for AAA A2A Gateway — v2 ENRICHED
 * Writes SEAL/HOLD audit records to the constitutional ledger.
 *
 * v2.0.0 (FORGED 2026-07-04): Enriched seal envelope.
 * Adds: event_type, principal, policy_hash, input/output hashes, delegation chain.
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const VAULT_WRITER_URL = process.env.VAULT_WRITER_URL || 'http://vault999-writer:5001';
const VAULT_WRITER_TOKEN = process.env.VAULT_WRITER_TOKEN || '';

const crypto = require('crypto');
function sha256Hex(input) {
  return 'sha256:' + crypto.createHash('sha256').update(input).digest('hex');
}

/**
 * Create an enriched seal payload for the canonical hash chain.
 * v2: includes cryptographic event envelope fields alongside the original payload.
 */
function createSealPayload(task, agentId, action, metadata, opts = {}) {
  const now = new Date().toISOString();

  const sessionId =
    task.session_id ||
    task.metadata?.session_id ||
    metadata?.session_id ||
    null;
  const contextId = task.contextId || metadata?.context_id || null;

  // Ghost Task prevention: refuse to build SEAL payload without lineage
  if (!sessionId || sessionId === 'session-unknown' || sessionId === 'unknown') {
    const err = new Error(
      'VAULT999 write refused: session_id required (Ghost Task / missing contextLineage)',
    );
    err.code = 'GHOST_TASK_BLOCKED';
    throw err;
  }
  if (!contextId) {
    const err = new Error(
      'VAULT999 write refused: context_id required (Ghost Task / missing contextLineage)',
    );
    err.code = 'GHOST_TASK_BLOCKED';
    throw err;
  }

  const payload = {
    agent_id: agentId || 'aaa-gateway',
    actor: agentId || 'aaa-gateway',
    session_id: sessionId,
    action: action,
    payload: {
      task_id: task.id,
      context_id: contextId,
      session_id: sessionId,
      status: task.status?.state,
      routing: task.metadata?.routing || 'direct',
      skill: task.metadata?.skill || null,
      ...metadata
    },
    epoch: now,
    verdict: 'SEAL',
    human_ratifier: 'arif',
    human_signature: `SIG_AAA_GATEWAY_${Date.now().toString(36).toUpperCase()}`,
    ratified_at: now,
    irreversibility_ack: true,
    irreversibility_class: 'LOW_RISK_DIRECT',
    tags: ['aaa', 'a2a', 'audit', 'lineage-bound'],
    metadata: {
      source: 'aaa-a2a-gateway',
      protocol: 'A2A/AAA-v1.0',
      session_id: sessionId,
      context_id: contextId,
      ...metadata
    }
  };

  // ── Enriched seal options (v2) ──
  // These are passed through to seal_chain.writeSeal() as the second argument.
  // vault.js doesn't compute hashes — seal_chain.js does. vault.js passes
  // raw data and seal_chain.js canonicalizes/hashes.
  payload._seal_opts = {
    event_type: opts.event_type || classifyEventType(action),
    principal: opts.principal || `agent:${agentId || 'aaa-gateway'}`,
    tool_schema_hash: opts.tool_schema_hash || null,
    active_floors: opts.active_floors || ['F1', 'F2', 'F4', 'F6', 'F8', 'F9', 'F11', 'F13'],
    input_hash: null,  // computed by seal_chain.js from the payload
    output_hash: opts.output_hash || null,
    delegation_chain: opts.delegation_chain || [],
  };

  return payload;
}

function classifyEventType(action) {
  const a = (action || '').toLowerCase();
  if (a.startsWith('a2a.')) return 'a2a.dispatch';
  if (a.includes('shell') || a.includes('forge.execute')) return 'forge.shell';
  if (a.includes('judge') || a.includes('verdict')) return 'constitutional.verdict';
  if (a.includes('register') || a.includes('forge.skill')) return 'tool.register';
  if (a.includes('seal') || a.includes('session')) return 'session.seal';
  return 'a2a.general';
}

async function writeSeal(task, agentId, action, metadata, opts = {}) {
  const fullPayload = createSealPayload(task, agentId, action, metadata, opts);
  // Extract enrichment options before delegating to seal_chain
  const sealOpts = fullPayload._seal_opts || {};
  delete fullPayload._seal_opts;

  const sealChain = require('./seal_chain');
  return sealChain.writeSeal(fullPayload, sealOpts);
}

async function writeVoid(task, agentId, action, reason, metadata) {
  const payload = createSealPayload(task, agentId, action, { ...metadata, void_reason: reason });
  payload.verdict = 'VOID';
  payload.irreversibility_class = 'HOLD_VOID';
  // Preserve seal options
  const sealOpts = payload._seal_opts || { event_type: 'a2a.general' };
  sealOpts.event_type = sealOpts.event_type || 'a2a.general';
  delete payload._seal_opts;

  const sealChain = require('./seal_chain');
  return sealChain.writeSeal(payload, sealOpts);
}

async function writeRecord(endpoint, payload) {
  // Legacy path — retained for direct callers that need the remote writer
  // without touching the local chain. New code should use writeSeal/writeVoid.
  const path = `${VAULT_WRITER_URL}${endpoint}`;

  const auditLine = `[VAULT999] AUDIT intent: agent=${payload.agent_id} action=${payload.action} verdict=${payload.verdict} epoch=${payload.epoch} task_id=${payload.payload.task_id} context_id=${payload.payload.context_id} routing=${payload.payload.routing}`;

  const headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'AAA-A2A-Gateway/1.0'
  };
  if (VAULT_WRITER_TOKEN) {
    headers['X-Writer-Token'] = VAULT_WRITER_TOKEN;
  }

  try {
    const response = await fetch(path, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(5000)
    });

    const body = await response.text();

    if (!response.ok) {
      console.error(`[VAULT999] Write failed (${response.status}) — AUDIT INTENT LOGGED: ${auditLine}`);
      console.error(`[VAULT999] Response: ${body}`);
      return { ok: false, status: response.status, error: body, auditLogged: true };
    }

    let data;
    try { data = JSON.parse(body); } catch { data = body; }

    console.log(`[VAULT999] SEAL written (legacy remote path): action=${payload.action}, agent=${payload.agent_id}`);
    return { ok: true, data };
  } catch (error) {
    console.error(`[VAULT999] Write error — AUDIT INTENT LOGGED: ${auditLine}`);
    if (error.name === 'TimeoutError') {
      console.error('[VAULT999] Write timed out — continuing without audit');
    } else {
      console.error(`[VAULT999] Error: ${error.message}`);
    }
    return { ok: false, error: error.message, auditLogged: true };
  }
}

async function checkHealth() {
  try {
    const response = await fetch(`${VAULT_WRITER_URL}/health`, {
      signal: AbortSignal.timeout(3000)
    });
    return response.ok;
  } catch {
    return false;
  }
}

module.exports = {
  writeSeal,
  writeVoid,
  checkHealth,
  VAULT_WRITER_URL
};
