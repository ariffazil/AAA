#!/usr/bin/env node
/**
 * J-Continuity Kernel — Jacobian Persistence Engine
 * 
 * Forged 2026-07-25 by FORGE (000Ω) under F13 SOVEREIGN directive.
 * 
 * This module bridges the application-layer Jacobian (∂T/∂G in goal_decomposer.js)
 * to kernel-level J-continuity (∂K/∂S across sessions).
 * 
 * The Jacobian of the federation's belief/state manifold:
 *   J = ∂(state_final) / ∂(state_initial, action_vector)
 * 
 * Without J-continuity, every arif_init creates a fresh manifold.
 * With J-continuity, the manifold shape persists through VAULT999 checkpoints.
 * 
 * Architecture:
 *   Session N: J_state → VAULT999 J-checkpoint → carry_forward J-fields
 *   Session N+1: carry_forward.load() → J_state restored → Jacobian evolves
 * 
 * DITEMPA BUKAN DIBERI.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ── Constants ────────────────────────────────────────────────────────────
const CARRY_FORWARD_PATH = '/root/.local/share/arifos/carry_forward.json';
const J_STATE_PATH = '/root/.local/share/arifos/j-state.json';
const COOLING_LEDGER_PATH = '/root/.local/share/arifos/cooling_ledger.jsonl';
const VAULT999_OUTCOMES = '/root/.local/share/arifos/vault999/outcomes.jsonl';

/**
 * J-State Schema (v1.0.0)
 * 
 * The Jacobian state is a snapshot of the federation's belief manifold
 * at a specific point in time. It captures:
 * 
 *   manifold_shape:  [dimensions, curvature, tension_vectors]
 *   sensitivity_matrix:  ∂K/∂S per state dimension
 *   invariants:  values that must be preserved across sessions
 *   checkpoints:  list of previous VAULT999 anchor points
 * 
 * {
 *   "version": "1.0.0",
 *   "session_id": "xxx",
 *   "timestamp": "ISO-8601",
 *   "predecessor_seq": "VAULT999 seq of previous checkpoint",
 *   
 *   "manifold": {
 *     "dimensions": ["goal_alignment", "agent_health", "constraint_satisfaction", 
 *                    "uncertainty_entropy", "skill_saturation", "organ_connectivity"],
 *     "state_vector": [0.0-1.0, ...],    // current position in J-space
 *     "curvature": float,                 // local curvature estimate
 *     "tension_vectors": [{from_dim, to_dim, magnitude}]
 *   },
 *   
 *   "sensitivity": {
 *     "condition_number": float,          // how fragile is the current state
 *     "blast_radii": [{agent_id, radius, affected_dimensions}],
 *     "eigenvalues": [float, ...],        // principal sensitivity directions
 *     "stability_margin": float           // distance to nearest constraint violation
 *   },
 *   
 *   "invariants": {
 *     "f1_amanah_breaches": 0,           // must never increase across sessions
 *     "f2_truth_violations": 0,
 *     "identity_hash": "sha256",         // must match kernel identity
 *     "organ_count": 6,                   // federation topology invariant
 *     "agent_count": 33                   // A2A registry size
 *   },
 *   
 *   "delta_J": {
 *     "magnitude": float,                 // ||J_curr - J_prev||
 *     "direction": "CONVERGING|DIVERGING|STABLE",
 *     "drift_dimensions": ["dim_name"],   // which dimensions shifted most
 *     "cooling_entries_written": int
 *   },
 *   
 *   "receipt": {
 *     "hash": "sha256 of J-state",
 *     "parent_hash": "sha256 of previous J-state",
 *     "sealed_to_vault": false
 *   }
 * }
 */

// ── J-State Initializer ──────────────────────────────────────────────────
function initializeJState(sessionId) {
  return {
    version: '1.0.0',
    session_id: sessionId,
    timestamp: new Date().toISOString(),
    predecessor_seq: null,
    
    manifold: {
      dimensions: [
        'goal_alignment', 'agent_health', 'constraint_satisfaction',
        'uncertainty_entropy', 'skill_saturation', 'organ_connectivity'
      ],
      state_vector: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  // neutral initial
      curvature: 0.0,
      tension_vectors: []
    },
    
    sensitivity: {
      condition_number: 0.0,
      blast_radii: [],
      eigenvalues: [],
      stability_margin: 1.0  // max stability at start
    },
    
    invariants: {
      f1_amanah_breaches: 0,
      f2_truth_violations: 0,
      identity_hash: null,
      organ_count: 6,
      agent_count: 33
    },
    
    delta_J: {
      magnitude: 0.0,
      direction: 'STABLE',
      drift_dimensions: [],
      cooling_entries_written: 0
    },
    
    receipt: {
      hash: null,
      parent_hash: null,
      sealed_to_vault: false
    }
  };
}

// ── J-State Loader — restore from carry_forward + vault ─────────────────
function loadJState() {
  let jState = null;
  
  // Try carry_forward first
  try {
    if (fs.existsSync(CARRY_FORWARD_PATH)) {
      const cf = JSON.parse(fs.readFileSync(CARRY_FORWARD_PATH, 'utf8'));
      if (cf.j_state) {
        jState = cf.j_state;
        console.log('[J-CONTINUITY] Loaded J-state from carry_forward:', 
          `session=${jState.session_id?.slice(0,8)}...`,
          `ΔJ=${jState.delta_J?.magnitude?.toFixed(4)}`,
          `direction=${jState.delta_J?.direction}`
        );
      }
    }
  } catch (e) {
    console.warn('[J-CONTINUITY] carry_forward load failed:', e.message);
  }
  
  // Fall back to disk J-state
  if (!jState) {
    try {
      if (fs.existsSync(J_STATE_PATH)) {
        jState = JSON.parse(fs.readFileSync(J_STATE_PATH, 'utf8'));
        console.log('[J-CONTINUITY] Loaded J-state from disk');
      }
    } catch (e) {
      console.warn('[J-CONTINUITY] disk load failed:', e.message);
    }
  }
  
  // Fall back to neutral manifold
  if (!jState) {
    console.log('[J-CONTINUITY] No prior J-state found. Initializing neutral manifold.');
    jState = initializeJState('fresh');
  }
  
  return jState;
}

// ── J-State Mutation — evolve the manifold after an action ──────────────
function evolveJState(jState, action, decompositionJacobian = null) {
  const prevState = JSON.parse(JSON.stringify(jState));
  
  // 1. Update manifold state vector based on action outcome
  if (action.agent_affected) {
    const agentIdx = jState.manifold.dimensions.indexOf('agent_health');
    if (agentIdx >= 0) {
      jState.manifold.state_vector[agentIdx] = 
        Math.max(0, Math.min(1, jState.manifold.state_vector[agentIdx] + 
          (action.success ? 0.02 : -0.05)));
    }
  }
  
  // 2. Update goal_alignment dimension
  const goalIdx = jState.manifold.dimensions.indexOf('goal_alignment');
  if (goalIdx >= 0 && action.goal_progress != null) {
    jState.manifold.state_vector[goalIdx] = 
      Math.max(0, Math.min(1, jState.manifold.state_vector[goalIdx] + 
        action.goal_progress * 0.1));
  }
  
  // 3. Incorporate decomposition Jacobian if available
  if (decompositionJacobian) {
    jState.sensitivity.condition_number = 
      decompositionJacobian.conditionNumber || jState.sensitivity.condition_number;
    
    // Map blast radii to manifold dimensions
    if (decompositionJacobian.blastRadii) {
      jState.sensitivity.blast_radii = decompositionJacobian.blastRadii
        .filter(b => b.blastRadius > 0)
        .map(b => ({
          task_id: b.taskId,
          radius: b.blastRadius,
          affected_dimensions: ['goal_alignment', 'constraint_satisfaction']
                                 .slice(0, Math.ceil(b.blastRadius))
        }));
    }
  }
  
  // 4. Update constraint satisfaction
  const constraintIdx = jState.manifold.dimensions.indexOf('constraint_satisfaction');
  if (constraintIdx >= 0 && action.violations != null) {
    jState.manifold.state_vector[constraintIdx] = 
      Math.max(0, jState.manifold.state_vector[constraintIdx] - action.violations * 0.1);
  }
  
  // 5. Compute delta-J — how much the manifold shifted
  const deltaMagnitude = computeManifoldDistance(prevState, jState);
  jState.delta_J = {
    magnitude: deltaMagnitude,
    direction: deltaMagnitude < 0.01 ? 'STABLE' : 
               deltaMagnitude < 0.05 ? 'CONVERGING' : 'DIVERGING',
    drift_dimensions: detectDriftDimensions(prevState, jState),
    cooling_entries_written: (jState.delta_J.cooling_entries_written || 0) + 1
  };
  
  // 6. Update receipt hash
  jState.receipt.parent_hash = jState.receipt.hash;
  jState.receipt.hash = computeStateHash(jState);
  jState.timestamp = new Date().toISOString();
  
  // 7. Compute stability margin
  jState.sensitivity.stability_margin = computeStabilityMargin(jState);
  
  return jState;
}

// ── Helper: manifold distance (Frobenius norm on state vectors) ──────────
function computeManifoldDistance(prev, curr) {
  const pv = prev.manifold.state_vector;
  const cv = curr.manifold.state_vector;
  let sumSq = 0;
  for (let i = 0; i < Math.min(pv.length, cv.length); i++) {
    sumSq += (cv[i] - pv[i]) ** 2;
  }
  return Math.sqrt(sumSq);
}

// ── Helper: detect which dimensions drifted most ─────────────────────────
function detectDriftDimensions(prev, curr) {
  const pv = prev.manifold.state_vector;
  const cv = curr.manifold.state_vector;
  const dims = prev.manifold.dimensions;
  const diffs = [];
  for (let i = 0; i < Math.min(pv.length, cv.length, dims.length); i++) {
    diffs.push({ dim: dims[i], delta: Math.abs(cv[i] - pv[i]) });
  }
  diffs.sort((a, b) => b.delta - a.delta);
  return diffs.filter(d => d.delta > 0.01).slice(0, 3).map(d => d.dim);
}

// ── Helper: stability margin — distance to nearest constraint violation ──
function computeStabilityMargin(jState) {
  const sv = jState.manifold.state_vector;
  // Stability = mean distance from bounds [0,1]
  let totalDist = 0;
  for (const v of sv) {
    totalDist += Math.min(v, 1 - v);  // distance to nearest bound
  }
  return sv.length > 0 ? totalDist / sv.length : 1.0;
}

// ── Helper: compute state hash for receipt chain ─────────────────────────
function computeStateHash(jState) {
  const core = {
    session_id: jState.session_id,
    state_vector: jState.manifold.state_vector,
    condition_number: jState.sensitivity.condition_number,
    delta_J_magnitude: jState.delta_J.magnitude,
    invariants: jState.invariants,
    parent_hash: jState.receipt.parent_hash
  };
  return crypto.createHash('sha256')
    .update(JSON.stringify(core))
    .digest('hex');
}

// ── J-State Persistence ─────────────────────────────────────────────────
function saveJState(jState) {
  // Write to disk
  try {
    fs.writeFileSync(J_STATE_PATH, JSON.stringify(jState, null, 2));
    console.log('[J-CONTINUITY] J-state saved to disk:', 
      `hash=${jState.receipt.hash?.slice(0, 12)}...`,
      `ΔJ=${jState.delta_J.magnitude.toFixed(4)}`
    );
  } catch (e) {
    console.error('[J-CONTINUITY] Save failed:', e.message);
  }
  
  // Inject into carry_forward
  try {
    if (fs.existsSync(CARRY_FORWARD_PATH)) {
      const cf = JSON.parse(fs.readFileSync(CARRY_FORWARD_PATH, 'utf8'));
      cf.j_state = jState;
      cf.j_continuity = {
        active: true,
        last_checkpoint_hash: jState.receipt.hash,
        manifold_stability: jState.delta_J.direction,
        delta_S: jState.delta_J.magnitude
      };
      fs.writeFileSync(CARRY_FORWARD_PATH, JSON.stringify(cf, null, 2));
      console.log('[J-CONTINUITY] Injected J-state into carry_forward');
    }
  } catch (e) {
    console.warn('[J-CONTINUITY] carry_forward injection failed:', e.message);
  }
}

// ── J-Checkpoint to VAULT999 ────────────────────────────────────────────
function checkpointToVault(jState, actorId = 'j-continuity-engine') {
  const checkpoint = {
    type: 'J_CHECKPOINT',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    session_id: jState.session_id,
    actor_id: actorId,
    j_state: {
      state_vector: jState.manifold.state_vector,
      condition_number: jState.sensitivity.condition_number,
      stability_margin: jState.sensitivity.stability_margin,
      delta_J_magnitude: jState.delta_J.magnitude,
      delta_J_direction: jState.delta_J.direction,
      invariants: jState.invariants
    },
    receipt_hash: jState.receipt.hash,
    parent_hash: jState.receipt.parent_hash
  };
  
  try {
    const entry = JSON.stringify(checkpoint);
    fs.appendFileSync(VAULT999_OUTCOMES, entry + '\n');
    jState.receipt.sealed_to_vault = true;
    console.log('[J-CONTINUITY] ✅ J-checkpoint sealed to VAULT999');
    return true;
  } catch (e) {
    console.error('[J-CONTINUITY] ❌ Vault seal failed:', e.message);
    return false;
  }
}

// ── J-Cooling — write ΔJ to cooling ledger ──────────────────────────────
function coolJacobian(jState, sessionId, actorId = 'j-continuity-engine') {
  if (jState.delta_J.magnitude < 0.001) return; // nothing to cool
  
  const coolingEntry = {
    receipt_id: `j-cool-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`,
    timestamp: new Date().toISOString(),
    claim_type: 'JACOBIAN_COOLING',
    gate_verdict: jState.delta_J.direction === 'DIVERGING' ? 'HOLD' : 'SEAL',
    tier_assigned: 'L4',
    tier_required: 'L4',
    downgraded: false,
    emitted_as: 'COOLING_RECEIPT',
    claim_text: `J-manifold shift: ΔJ=${jState.delta_J.magnitude.toFixed(4)}, ` +
                `direction=${jState.delta_J.direction}, ` +
                `drift_dims=[${jState.delta_J.drift_dimensions.join(',')}], ` +
                `stability=${jState.sensitivity.stability_margin.toFixed(4)}`,
    agent_id: actorId,
    session_id: sessionId,
    action: 'j_continuity_cool',
    delta_J: {
      magnitude: jState.delta_J.magnitude,
      direction: jState.delta_J.direction,
      drift_dimensions: jState.delta_J.drift_dimensions,
      condition_number: jState.sensitivity.condition_number
    }
  };
  
  try {
    fs.appendFileSync(COOLING_LEDGER_PATH, JSON.stringify(coolingEntry) + '\n');
    console.log('[J-CONTINUITY] ❄️  J-cooling entry written to ledger');
  } catch (e) {
    console.warn('[J-CONTINUITY] Cooling write failed:', e.message);
  }
}

// ── Full Cycle: load → evolve → save → checkpoint ───────────────────────
function jCycle(sessionId, action = null, decompositionJacobian = null) {
  // 1. Load previous J-state (carries forward from prior session)
  const jState = loadJState();
  
  // 2. Update session identity
  jState.session_id = sessionId;
  
  // 3. Evolve if there's an action to process
  if (action) {
    evolveJState(jState, action, decompositionJacobian);
  }
  
  // 4. Persist
  saveJState(jState);
  
  // 5. Checkpoint to VAULT999 if significant change
  if (jState.delta_J.magnitude > 0.01) {
    checkpointToVault(jState);
  }
  
  // 6. Cool if diverging
  if (jState.delta_J.direction === 'DIVERGING') {
    coolJacobian(jState, sessionId);
  }
  
  return jState;
}

// ── ΔJ Metric — thermal stability of the federation ─────────────────────
function getThermalStability(jState) {
  const sv = jState.manifold.state_vector;
  const mean = sv.reduce((a, b) => a + b, 0) / sv.length;
  const variance = sv.reduce((s, v) => s + (v - mean) ** 2, 0) / sv.length;
  
  return {
    thermal_stability: 1 - Math.sqrt(variance),  // high = stable
    manifold_mean: mean,
    manifold_variance: variance,
    is_diverging: jState.delta_J.direction === 'DIVERGING',
    is_converging: jState.delta_J.direction === 'CONVERGING',
    is_stable: jState.delta_J.direction === 'STABLE',
    stability_margin: jState.sensitivity.stability_margin,
    condition_number: jState.sensitivity.condition_number
  };
}

// ── Exports ─────────────────────────────────────────────────────────────
module.exports = {
  initializeJState,
  loadJState,
  evolveJState,
  saveJState,
  checkpointToVault,
  coolJacobian,
  jCycle,
  getThermalStability,
  computeManifoldDistance,
  CARRY_FORWARD_PATH,
  J_STATE_PATH
};

// ── CLI: direct invocation for testing ──────────────────────────────────
if (require.main === module) {
  const sessionId = process.argv[2] || `j-test-${Date.now()}`;
  const action = process.argv[3] || 'test';
  
  console.log(`[J-CONTINUITY] Direct invocation — session=${sessionId}`);
  const jState = jCycle(sessionId, { 
    success: action !== 'fail', 
    goal_progress: 0.1,
    agent_affected: true,
    violations: 0
  });
  
  const stability = getThermalStability(jState);
  console.log('\n═══ J-MANIFOLD STATE ═══');
  console.log(`  State vector:  [${jState.manifold.state_vector.map(v=>v.toFixed(3)).join(', ')}]`);
  console.log(`  Condition #:   ${jState.sensitivity.condition_number.toFixed(4)}`);
  console.log(`  ΔJ magnitude:  ${jState.delta_J.magnitude.toFixed(4)}`);
  console.log(`  Direction:     ${jState.delta_J.direction}`);
  console.log(`  Drift dims:    [${jState.delta_J.drift_dimensions.join(', ')}]`);
  console.log(`  Stability:     ${stability.thermal_stability.toFixed(4)}`);
  console.log(`  Receipt hash:  ${jState.receipt.hash?.slice(0,16)}...`);
  console.log(`  Vault sealed:  ${jState.receipt.sealed_to_vault}`);
}
