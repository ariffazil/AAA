#!/usr/bin/env node
/**
 * metabolizer_loop.js — Goal Decomposition Metabolic Cycle
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Closes the Δ→Ω→Ψ loop: takes result envelopes back in, updates task state,
 * adjusts Jacobian weights, and triggers seals when goals are fully metabolized.
 *
 * Metabolic cycle:
 *   encodeGoalToTasks(G)  — Δ / 333-AGI   (encoder)
 *   decodeTasksToEnvelopes — Ω / 555-ASI   (decoder)
 *   metabolizeResults      — Ψ / 888-APEX  (metabolizer — this file)
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

'use strict';

const crypto = require('crypto');
const { encodeGoalToTasks, decodeTasksToEnvelopes, getMetabolicRing } = require('./goal_decomposition.js');

// ── State ────────────────────────────────────────────────────────────────────

/** In-memory store of active goal decompositions. Keyed by goal_id. */
const _activeDecompositions = new Map();

// ── Core API ─────────────────────────────────────────────────────────────────

/**
 * Decompose a goal and register it for metabolic tracking.
 *
 * @param {Object} G — goal object
 * @param {string} G.id
 * @param {string} G.actor
 * @param {string} G.intent
 * @param {string[]} [G.org_scope]
 * @param {string} [G.riskband="LOW"]
 * @param {number} [G.time_horizon_ms=300000]
 * @param {Object} [G.constraints={}]
 * @returns {Object} decomposition result with tasks + envelopes
 */
function decomposeGoal(G) {
  const goal = {
    id: G.id || `goal-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`,
    actor: G.actor || 'hermes-asi',
    intent: G.intent,
    org_scope: G.org_scope || ['arifos','geox','wealth','well','aforge'],
    riskband: G.riskband || 'LOW',
    time_horizon_ms: G.time_horizon_ms || 300000,
    constraints: G.constraints || {},
  };

  // ENCODER: G → T
  const { tasks, meta } = encodeGoalToTasks(goal);

  // DECODER: T → A2AEnvelope[]
  const envelopes = decodeTasksToEnvelopes(tasks, meta.jacobian_skeleton);

  // Register in metabolic tracker
  _activeDecompositions.set(goal.id, {
    goal,
    tasks,
    meta,
    envelopes,
    started_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    metabolic_cycles: 0,
  });

  return { goal_id: goal.id, tasks, envelopes, meta };
}

/**
 * Metabolize result envelopes → update task states + adjust Jacobian.
 *
 * @param {string} goalId      — which goal to metabolize
 * @param {Object[]} results   — result envelopes from executed tasks
 * @param {Object} [options]
 * @param {boolean} [options.seal_on_complete=true] — auto-seal when all done
 * @returns {Object} updated decomposition state
 */
function metabolizeResults(goalId, results, options = {}) {
  const sealOnComplete = options.seal_on_complete !== false;

  const record = _activeDecompositions.get(goalId);
  if (!record) {
    return { ok: false, error: `Goal ${goalId} not found in active decompositions` };
  }

  // Update task states from result envelopes
  for (const result of results) {
    const task = record.tasks.find(t => t.id === result.task_id);
    if (!task) continue;

    task.state = result.state || 'DONE';

    if (result.receipt_hash) {
      task.receipt_hash = result.receipt_hash;
    }

    // Adjust Jacobian weights based on outcome
    if (result.state === 'FAILED' && task.jacobian) {
      // Task failed — increase sensitivity to risk and constraints
      task.jacobian.risk = Math.min(1.0, (task.jacobian.risk || 0.3) * 1.2);
      task.jacobian.constraints = Math.min(1.0, (task.jacobian.constraints || 0.3) * 1.2);
    }

    if (result.state === 'DONE' && task.jacobian) {
      // Task succeeded — slightly decrease sensitivity (evidence gained)
      task.jacobian.risk = Math.max(0.1, (task.jacobian.risk || 0.3) * 0.95);
      task.jacobian.constraints = Math.max(0.1, (task.jacobian.constraints || 0.3) * 0.95);
    }
  }

  // Rebuild envelopes
  const jacobian = buildMetabolicJacobian(record.tasks);
  record.envelopes = decodeTasksToEnvelopes(record.tasks, jacobian);
  record.meta.jacobian_skeleton = jacobian;
  record.metabolic_cycles++;
  record.updated_at = new Date().toISOString();

  // Check completion
  const done = record.tasks.every(t => t.state === 'DONE');
  const failed = record.tasks.some(t => t.state === 'FAILED');

  if (done && sealOnComplete) {
    record.seal = generateSealPayload(record);
    record.state = 'SEALED';
  } else if (failed) {
    record.state = 'DEGRADED';
  } else {
    record.state = 'METABOLIZING';
  }

  return {
    ok: true,
    goal_id: goalId,
    state: record.state,
    tasks: record.tasks,
    envelopes: record.envelopes,
    meta: record.meta,
    seal: record.seal || null,
    metabolic_cycles: record.metabolic_cycles,
  };
}

/**
 * Get the current decomposition state for a goal.
 */
function getGoalState(goalId) {
  const record = _activeDecompositions.get(goalId);
  if (!record) return null;
  return {
    goal_id: goalId,
    state: record.state || 'DECOMPOSING',
    tasks: record.tasks,
    metabolic_cycles: record.metabolic_cycles,
    started_at: record.started_at,
    updated_at: record.updated_at,
  };
}

/**
 * List all active decompositions.
 */
function listActiveDecompositions() {
  const result = [];
  for (const [id, record] of _activeDecompositions) {
    result.push({
      goal_id: id,
      state: record.state || 'DECOMPOSING',
      intent: record.goal.intent.slice(0, 80),
      task_count: record.tasks.length,
      cycles: record.metabolic_cycles,
      started_at: record.started_at,
    });
  }
  return result;
}

// ── Internal ─────────────────────────────────────────────────────────────────

/**
 * Build Jacobian from current task state.
 */
function buildMetabolicJacobian(tasks) {
  const goalFields = ['intent', 'scope', 'risk', 'time', 'constraints'];
  const matrix = {};
  for (const field of goalFields) {
    matrix[field] = {};
    for (const task of tasks) {
      const sensitivity = (task.jacobian && task.jacobian[field]) || 0;
      if (sensitivity > 0.3) {
        matrix[field][task.id] = sensitivity;
      }
    }
  }
  return { fields: goalFields, task_ids: tasks.map(t => t.id), matrix };
}

/**
 * Generate seal-ready payload for a completed decomposition.
 */
function generateSealPayload(record) {
  const hashInput = record.tasks.map(t => `${t.id}:${t.state}:${t.receipt_hash || 'null'}`).join('|');
  const sealHash = crypto.createHash('sha256').update(hashInput).digest('hex');

  return {
    goal_id: record.goal.id,
    intent: record.goal.intent,
    total_tasks: record.tasks.length,
    all_sealed: record.tasks.every(t => t.receipt_hash),
    seal_hash: sealHash,
    metabolic_cycles: record.metabolic_cycles,
    completed_at: new Date().toISOString(),
    task_ids: record.tasks.map(t => t.id),
    doctrince: 'DITEMPA BUKAN DIBERI',
  };
}

// ── Test: Full Δ→Ω→Ψ Cycle ─────────────────────────────────────────────────

/**
 * Run a full decomposition, execution simulation, and metabolic close.
 * Used for testing and demonstration.
 */
function runTestCycle(goalIntent) {
  const goal = {
    id: `test-goal-${Date.now()}`,
    actor: 'hermes-asi',
    intent: goalIntent,
    riskband: 'MEDIUM',
    time_horizon_ms: 60000,
  };

  // Phase 1: Encode (Δ / 333-AGI)
  console.log(`[Metabolizer] Δ ENCODE: "${goal.intent}"`);
  const { goal_id, tasks, envelopes, meta } = decomposeGoal(goal);
  console.log(`  → ${tasks.length} tasks across ${meta.agent_count} agents`);
  console.log(`  → Rings: ${meta.generator_tasks} gen / ${meta.epistemic_tasks} epi / ${meta.metabolizer_tasks} meta`);

  // Phase 2: Simulate execution (all DONE with receipts)
  const results = tasks.map(task => ({
    task_id: task.id,
    state: 'DONE',
    receipt_hash: crypto.createHash('sha256').update(task.id).digest('hex').slice(0, 16),
  }));

  // Phase 3: Metabolize (Ψ / 888-APEX)
  console.log(`[Metabolizer] Ψ METABOLIZE: closing ${tasks.length} tasks`);
  const closed = metabolizeResults(goal_id, results, { seal_on_complete: true });
  console.log(`  → State: ${closed.state}`);
  console.log(`  → Cycles: ${closed.metabolic_cycles}`);
  console.log(`  → Seal hash: ${closed.seal?.seal_hash?.slice(0, 16) || 'none'}`);

  return closed;
}

// ── Exports ──────────────────────────────────────────────────────────────────

module.exports = {
  decomposeGoal,
  metabolizeResults,
  getGoalState,
  listActiveDecompositions,
  runTestCycle,
};
