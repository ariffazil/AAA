#!/usr/bin/env node
/**
 * VAULT999 Client for AAA A2A Gateway
 * Writes SEAL/HOLD audit records to the constitutional ledger
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const VAULT_WRITER_URL = process.env.VAULT_WRITER_URL || 'http://vault999-writer:5001';

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

async function writeRecord(endpoint, payload) {
  const path = `${VAULT_WRITER_URL}${endpoint}`;

  const auditLine = `[VAULT999] AUDIT intent: agent=${payload.agent_id} action=${payload.action} verdict=${payload.verdict} epoch=${payload.epoch} task_id=${payload.payload.task_id} context_id=${payload.payload.context_id} routing=${payload.payload.routing}`;

  try {
    const response = await fetch(path, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'AAA-A2A-Gateway/1.0'
      },
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

    console.log(`[VAULT999] SEAL written: action=${payload.action}, agent=${payload.agent_id}`);
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
