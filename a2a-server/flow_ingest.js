/**
 * arifFLOW Ingest — Metabolic Ledger Recording.
 * 
 * Records every task completion in arifFlow's metabolic ledger.
 * Non-blocking: failure is logged, not fatal to the task.
 * 
 * FQ = verify/execute ratio. Every ingest feeds the FQ pulse.
 * No receipts = no pulse = FQ STUCK.
 * 
 * DITEMPA BUKAN DIBERI.
 * Forged: 2026-08-08 by 333-AGI.
 */

const crypto = require('crypto');

const ARIFLOW_URL = process.env.ARIFLOW_URL || 'http://127.0.0.1:7073';

/**
 * Mint a flow receipt in arifFlow's metabolic ledger.
 * 
 * @param {object} params
 * @param {string} params.actorId - Agent performing the step
 * @param {string} params.sessionId - Governing session ID
 * @param {string} [params.stepType] - Execute | Verify | Cool | Seal | Barrier | Merge | Route
 * @param {string} [params.epistemicLabel] - Observation | Derivation | Interpretation | Specification | Seal
 * @param {string} [params.floorVerdict] - Pass | Caution | Hold | Void
 * @param {object} [params.payload] - Step-specific data
 * @param {number} [params.costNs] - Wall-clock step duration in ns
 * @returns {Promise<{ok: boolean, result?: object, error?: string}>}
 */
async function ingestFlow(params = {}) {
  const {
    actorId = 'aaa-gateway',
    sessionId = 'unknown',
    stepType = 'Execute',
    epistemicLabel = 'Derivation',
    floorVerdict = 'Pass',
    payload = null,
    costNs = 0,
    previousReceiptHash = null,
    stepNumber = 1,
  } = params;

  // Generate UUID v4 receipt_id if not provided
  const receiptId = params.receiptId || crypto.randomUUID();

  try {
    const body = {
      receipt_id: receiptId,
      previous_receipt_hash: previousReceiptHash !== undefined ? previousReceiptHash : null,
      created_at: new Date().toISOString(),
      actor_id: actorId || 'aaa-gateway',
      session_id: sessionId || 'unknown',
      session_token: params.sessionToken !== undefined ? params.sessionToken : null,
      step_type: stepType || 'Execute',
      step_number: stepNumber !== undefined ? stepNumber : 1,
      cost_ns: costNs !== undefined ? costNs : 0,
      epistemic_label: epistemicLabel || 'Derivation',
      floor_verdict: floorVerdict || 'Pass',
      cooling_decision: 'None',
      topology_id: params.topologyId !== undefined ? params.topologyId : null,
      lane_id: params.laneId !== undefined ? params.laneId : null,
      preceding_verify_cost_ns: null,
      tri_witness_votes: null,
      merkle_root: null,
      merkle_inclusion_proof: null,
      payload: payload !== undefined ? payload : null,
      formula_version: null,
    };

    const resp = await fetch(`${ARIFLOW_URL}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(3000),
    });

    if (!resp.ok) {
      console.warn(`[flow-ingest] arifFlow returned ${resp.status}: ${resp.statusText}`);
      return { ok: false, error: `HTTP ${resp.status}` };
    }

    const data = await resp.json();
    console.log(`[flow-ingest] ${stepType} ingested — FQ after: ${data.fq?.quotient || '?'}`);
    return { ok: true, result: data };

  } catch (err) {
    // Non-fatal — arifFlow may be down, that's OK
    console.debug(`[flow-ingest] arifFlow unreachable (non-fatal): ${err.message}`);
    return { ok: false, error: err.message };
  }
}

/**
 * Get current FQ health from arifFlow.
 * 
 * @returns {Promise<{ok: boolean, fq?: object, error?: string}>}
 */
async function getFlowHealth() {
  try {
    const resp = await fetch(`${ARIFLOW_URL}/health`, {
      signal: AbortSignal.timeout(3000),
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    return { ok: true, fq: data.fq, status: data.status, receipts: data.receipts };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

module.exports = { ingestFlow, getFlowHealth };
