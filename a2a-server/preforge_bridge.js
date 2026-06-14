/**
 * Pre-Forge Bridge — AAA Gateway ↔ Pre-Forge Constitutional Gate
 * ================================================================
 *
 * Thin bridge module for the AAA A2A gateway. Registers witnesses
 * and can trigger pre-forge checks from Node.js.
 *
 * All functions are fire-and-forget (non-blocking) for witness
 * registration. Pre-forge check is awaited.
 *
 * Forged: 2026-06-14 — Opus Shadow → Eureka Engineering
 * DITEMPA BUKAN DIBERI
 */

const PRE_FORGE_URL = process.env.PRE_FORGE_URL || 'http://127.0.0.1:18990';

/**
 * Register a model output witness in a session.
 * Fire-and-forget — never blocks the gateway.
 */
function registerModelOutput(sessionId, modelId, isPrimary = true) {
  if (!sessionId) return;
  const body = JSON.stringify({
    session_id: sessionId,
    model_id: modelId || 'unknown',
    is_primary: isPrimary,
  });
  const req = require('http').request(
    `${PRE_FORGE_URL}/model`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, timeout: 2000 },
    (res) => { res.resume(); }
  );
  req.on('error', () => {}); // Fire-and-forget
  req.write(body);
  req.end();
}

/**
 * Register an Earth measurement witness (tool call result).
 * Fire-and-forget — never blocks the gateway.
 */
function registerEarthMeasurement(sessionId, toolName, evidenceRef) {
  if (!sessionId) return;
  const body = JSON.stringify({
    session_id: sessionId,
    tool_name: toolName || 'unknown',
    evidence_ref: evidenceRef || `tool:${toolName}`,
  });
  const req = require('http').request(
    `${PRE_FORGE_URL}/earth`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, timeout: 2000 },
    (res) => { res.resume(); }
  );
  req.on('error', () => {});
  req.write(body);
  req.end();
}

/**
 * Register a human witness.
 * Fire-and-forget.
 */
function registerHuman(sessionId, evidenceRef = 'session:sovereign') {
  if (!sessionId) return;
  const body = JSON.stringify({
    session_id: sessionId,
    witness_type: 'HUMAN',
    evidence_ref: evidenceRef,
  });
  const req = require('http').request(
    `${PRE_FORGE_URL}/witness`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, timeout: 2000 },
    (res) => { res.resume(); }
  );
  req.on('error', () => {});
  req.write(body);
  req.end();
}

/**
 * Register a secondary model witness (for Mode-3 collapse detection).
 */
function registerSecondaryModel(sessionId, modelId) {
  registerModelOutput(sessionId, modelId, false);
}

module.exports = {
  registerModelOutput,
  registerEarthMeasurement,
  registerHuman,
  registerSecondaryModel,
};
