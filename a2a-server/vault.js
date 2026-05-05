#!/usr/bin/env node
/**
 * VAULT999 Client for AAA A2A Gateway
 * Writes SEAL/HOLD audit records to the constitutional ledger
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const VAULT_DIR = path.join(os.homedir(), '.arifos');
const VAULT_FILE = path.join(VAULT_DIR, 'vault.jsonl');

// Vault999 service endpoint (health + future seal proxy)
// Fallback chain: env var → Docker DNS (vault999:8100) → localhost fallback
const VAULT_WRITER_URL = process.env.VAULT_WRITER_URL || 'http://vault999:8100';

function createSealPayload(task, agentId, action, metadata) {
  const now = new Date().toISOString();

  return {
    agent_id: agentId || 'aaa-gateway',
    action: action,
    payload: {
      task_id: task.id,
      context_id: task.contextId,
      status: task.status?.state,
      routing: task.metadata?.routing || 'direct',
      skill: task.metadata?.skill || null,
      ...metadata
    },
    epoch: now,
    verdict: 'SEAL',
    human_ratifier: 'arifOS_AutoKernel',
    human_signature: `SIG_AAA_GATEWAY_${Date.now().toString(36).toUpperCase()}`,
    ratified_at: now,
    irreversibility_ack: true,
    irreversibility_class: 'LOW_RISK_DIRECT',
    tags: ['aaa', 'a2a', 'audit'],
    metadata: {
      source: 'aaa-a2a-gateway',
      protocol: 'A2A/AAA-v1.0',
      ...metadata
    }
  };
}

async function writeSeal(task, agentId, action, metadata) {
  const payload = createSealPayload(task, agentId, action, metadata);
  return writeRecord('/seal', payload);
}

async function writeVoid(task, agentId, action, reason, metadata) {
  const payload = createSealPayload(task, agentId, action, { ...metadata, void_reason: reason });
  payload.verdict = 'VOID';
  payload.irreversibility_class = 'HOLD_VOID';
  return writeRecord('/seal', payload);
}

async function _writeLocalFallback(payload) {
  // Append seal to local JSONL when remote vault writer is unavailable.
  try {
    if (!fs.existsSync(VAULT_DIR)) {
      fs.mkdirSync(VAULT_DIR, { recursive: true });
    }
    const line = JSON.stringify({ ...payload, _source: 'local_fallback', _written_at: new Date().toISOString() }) + '\n';
    fs.appendFileSync(VAULT_FILE, line, 'utf8');
    console.log(`[VAULT999] Local fallback written: ${VAULT_FILE}`);
    return { ok: true, source: 'local_fallback', file: VAULT_FILE };
  } catch (err) {
    console.error(`[VAULT999] Local fallback ALSO failed: ${err.message}`);
    return { ok: false, error: err.message };
  }
}

async function writeRecord(endpoint, payload) {
  const remotePath = `${VAULT_WRITER_URL}${endpoint}`;

  const auditLine = `[VAULT999] AUDIT intent: agent=${payload.agent_id} action=${payload.action} verdict=${payload.verdict} epoch=${payload.epoch} task_id=${payload.payload.task_id} context_id=${payload.payload.context_id} routing=${payload.payload.routing}`;

  // 1. Try remote vault writer first
  try {
    const response = await fetch(remotePath, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'AAA-A2A-Gateway/1.0'
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(3000)
    });

    const body = await response.text();

    if (!response.ok) {
      console.error(`[VAULT999] Write failed (${response.status}) — falling back to local JSONL: ${auditLine}`);
      return _writeLocalFallback(payload);
    }

    let data;
    try { data = JSON.parse(body); } catch { data = body; }

    console.log(`[VAULT999] SEAL written remotely: action=${payload.action}, agent=${payload.agent_id}`);
    return { ok: true, source: 'remote', data };
  } catch (error) {
    console.error(`[VAULT999] Remote write error — falling back to local JSONL: ${auditLine}`);
    if (error.name === 'TimeoutError') {
      console.error('[VAULT999] Remote timed out — local fallback active');
    } else {
      console.error(`[VAULT999] Remote error: ${error.message}`);
    }
    return _writeLocalFallback(payload);
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
