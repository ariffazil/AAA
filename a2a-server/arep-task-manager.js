/**
 * AREP Task Manager — Arif Reality Engineering Protocol
 * 
 * Coined by Muhammad Arif bin Fazil (F13 SOVEREIGN), forged 2026-06-04.
 * 
 * The server-side engine that:
 * 1. Validates AREP declarations against the canonical schema
 * 2. Manages task lifecycle aligned with A2A v1.0
 * 3. Performs reality gating — health probes block execution
 * 4. Tracks evidence layer progression
 * 5. Seals outcomes to VAULT999
 * 
 * An AREP task is NOT a prompt. It is a declaration of intent with reality constraints.
 * The agent self-prompts. The human only provides intent, evidence floor, and constraints.
 * 
 * Aligned with:
 *   - AgenticReality existential grounding model (March 2026)
 *   - A2A v1.0 task lifecycle (submitted → working → completed/failed)
 *   - arifOS constitutional floors F1-F13
 *   - Huawei governance paper: delegation chain attenuation (June 2026)
 */

const { writeSeal } = require('./vault');
const http = require('http');

// ═══════════════════════════════════════════════════════════════════
// REALITY LAYERS — the four-layer truth stack
// ═══════════════════════════════════════════════════════════════════

const REALITY_LAYERS = {
  GROUND_TRUTH: {
    ordinal: 0,
    label: 'GROUND_TRUTH',
    description: 'Verified right now. Sealed in VAULT999. Cannot be changed.',
    verification: 'Merkle chain integrity check',
    maxStalenessSeconds: 0, // always fresh — it's immutable
    autoUpgradable: false,  // human only (F13 SOVEREIGN)
  },
  VERIFIED_STATE: {
    ordinal: 1,
    label: 'VERIFIED_STATE',
    description: 'Checked recently via live probe. Trustworthy but subject to staleness.',
    verification: 'Live health probe',
    maxStalenessSeconds: 300,
    autoUpgradable: false,  // requires probe pass
  },
  CACHED_STATE: {
    ordinal: 2,
    label: 'CACHED_STATE',
    description: 'Once verified, now stale. Must re-verify before MUTATE/ATOMIC.',
    verification: 'Freshness timestamp check',
    maxStalenessSeconds: 3600,
    autoUpgradable: true,   // agent can promote from INFERRED
  },
  INFERRED: {
    ordinal: 3,
    label: 'INFERRED',
    description: 'Never verified. Agent reasoning. Bounded by constitutional floors.',
    verification: 'None — must escalate',
    maxStalenessSeconds: Infinity,
    autoUpgradable: true,   // starting point
  },
};

const LAYER_ORDINALS = {
  GROUND_TRUTH: 0,
  VERIFIED_STATE: 1,
  CACHED_STATE: 2,
  INFERRED: 3,
};

// ═══════════════════════════════════════════════════════════════════
// FEDERATION ORGAN HEALTH PROBES
// ═══════════════════════════════════════════════════════════════════

const FEDERATION_ORGANS = {
  arifos:  { port: 8088,  name: 'arifOS Kernel',     critical: true },
  geox:    { port: 8081,  name: 'GEOX Earth',        critical: false },
  wealth:  { port: 18082, name: 'WEALTH Capital',    critical: false },
  well:    { port: 18083, name: 'WELL Vitality',      critical: false },
  aforge:  { port: 7071,  name: 'A-FORGE Execution', critical: true },
  vault999:{ port: 5001,  name: 'VAULT999 Writer',   critical: true },
};

/**
 * Probe a single organ's health endpoint.
 * @returns {{ organ: string, healthy: boolean, status: string, latencyMs: number }}
 */
function probeOrgan(key, config) {
  return new Promise((resolve) => {
    const start = Date.now();
    const req = http.get(`http://127.0.0.1:${config.port}/health`, { timeout: 5000 }, (res) => {
      let body = '';
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        const healthy = res.statusCode === 200;
        resolve({
          organ: key,
          name: config.name,
          critical: config.critical,
          healthy,
          status: healthy ? 'GREEN' : 'RED',
          statusCode: res.statusCode,
          latencyMs: Date.now() - start,
          body: body.substring(0, 200),
        });
      });
    });
    req.on('error', () => {
      resolve({
        organ: key,
        name: config.name,
        critical: config.critical,
        healthy: false,
        status: 'RED',
        statusCode: 0,
        latencyMs: Date.now() - start,
        body: 'unreachable',
      });
    });
    req.on('timeout', () => {
      req.destroy();
      resolve({
        organ: key,
        name: config.name,
        critical: config.critical,
        healthy: false,
        status: 'RED',
        statusCode: 0,
        latencyMs: Date.now() - start,
        body: 'timeout',
      });
    });
  });
}

/**
 * Run full federation health probe.
 * @returns {{ allHealthy: boolean, criticalHealthy: boolean, organs: object[], summary: string }}
 */
async function probeFederation() {
  const probes = await Promise.all(
    Object.entries(FEDERATION_ORGANS).map(([key, config]) => probeOrgan(key, config))
  );
  const criticalHealthy = probes.filter(p => p.critical).every(p => p.healthy);
  const allHealthy = probes.every(p => p.healthy);

  let summary;
  if (allHealthy) summary = 'GREEN — all organs healthy';
  else if (criticalHealthy) summary = 'YELLOW — critical organs healthy, some non-critical degraded';
  else summary = 'RED — critical organ(s) unhealthy';

  return { allHealthy, criticalHealthy, organs: probes, summary, probedAt: new Date().toISOString() };
}

// ═══════════════════════════════════════════════════════════════════
// EVIDENCE TRACKING
// ═══════════════════════════════════════════════════════════════════

/**
 * Determine the current evidence layer for a task.
 */
function assessEvidenceLayer(task) {
  // If sealed to VAULT999 → GROUND_TRUTH
  if (task.lifecycle?.artifacts?.some(a => a.evidence_layer === 'GROUND_TRUTH' && a.vault_seal_hash)) {
    return 'GROUND_TRUTH';
  }
  // If health probe passed recently → VERIFIED_STATE
  if (task._lastHealthProbe && task._lastHealthProbe.allHealthy) {
    const age = (Date.now() - new Date(task._lastHealthProbe.probedAt).getTime()) / 1000;
    if (age < REALITY_LAYERS.VERIFIED_STATE.maxStalenessSeconds) {
      return 'VERIFIED_STATE';
    }
  }
  // If we have cached evidence → CACHED_STATE
  if (task._lastHealthProbe) {
    return 'CACHED_STATE';
  }
  // Default → INFERRED
  return 'INFERRED';
}

// ═══════════════════════════════════════════════════════════════════
// REALITY GATING — the core engine
// ═══════════════════════════════════════════════════════════════════

/**
 * Evaluate reality gates for a task.
 * Returns { passed: boolean, violations: [], currentEvidenceLayer: string, healthProbe: object }
 */
async function evaluateRealityGates(task) {
  const constraints = task.reality_constraints || {};
  const requiredFloor = constraints.evidence_floor || 'VERIFIED_STATE';
  const gates = constraints.reality_gates || [];

  // Run federation health probe
  const healthProbe = await probeFederation();
  task._lastHealthProbe = healthProbe;

  // Determine current evidence layer
  const currentLayer = assessEvidenceLayer(task);
  task._currentEvidenceLayer = currentLayer;

  const violations = [];

  // Check 1: Is the current evidence layer sufficient?
  const requiredOrdinal = LAYER_ORDINALS[requiredFloor];
  const currentOrdinal = LAYER_ORDINALS[currentLayer];
  if (currentOrdinal > requiredOrdinal) {
    violations.push({
      type: 'INSUFFICIENT_EVIDENCE',
      required: requiredFloor,
      current: currentLayer,
      message: `Task requires ${requiredFloor} evidence, but highest verified is ${currentLayer}.`,
      action: 'HALT',
    });
  }

  // Check 2: Evaluate each reality gate
  for (const gate of gates) {
    const result = evaluateGate(gate, healthProbe);
    if (!result.passed) {
      violations.push(result);
      if (gate.action_on_fail === 'HALT') return { passed: false, violations, healthProbe, currentEvidenceLayer: currentLayer };
    }
  }

  // Check 3: Critical organs must be healthy for MUTATE/ATOMIC
  if (constraints.reversibility?.maximum_action_class === 'MUTATE' || 
      constraints.reversibility?.maximum_action_class === 'ATOMIC') {
    if (!healthProbe.criticalHealthy) {
      violations.push({
        type: 'CRITICAL_ORGAN_UNHEALTHY',
        message: 'Cannot execute MUTATE/ATOMIC with unhealthy critical organs.',
        action: 'HALT',
      });
    }
  }

  return {
    passed: violations.filter(v => v.action === 'HALT').length === 0,
    violations,
    healthProbe,
    currentEvidenceLayer: currentLayer,
  };
}

/**
 * Evaluate a single reality gate condition.
 */
function evaluateGate(gate, healthProbe) {
  // Parse condition: "organ_health == GREEN" or "all_critical == healthy"
  const condition = gate.condition || '';
  
  if (condition.includes('organ_health')) {
    if (condition.includes('GREEN')) {
      const allGreen = healthProbe.organs.every(o => o.healthy);
      if (!allGreen) {
        const unhealthy = healthProbe.organs.filter(o => !o.healthy).map(o => o.name);
        return {
          passed: false,
          condition,
          action: gate.action_on_fail,
          message: `Organ health not GREEN. Unhealthy: ${unhealthy.join(', ')}`,
        };
      }
    }
  }

  if (condition.includes('critical')) {
    if (!healthProbe.criticalHealthy) {
      const unhealthy = healthProbe.organs.filter(o => o.critical && !o.healthy).map(o => o.name);
      return {
        passed: false,
        condition,
        action: gate.action_on_fail,
        message: `Critical organs unhealthy: ${unhealthy.join(', ')}`,
      };
    }
  }

  // Specific organ check
  for (const [key, config] of Object.entries(FEDERATION_ORGANS)) {
    if (condition.includes(key)) {
      const organ = healthProbe.organs.find(o => o.organ === key);
      if (!organ?.healthy) {
        return {
          passed: false,
          condition,
          action: gate.action_on_fail,
          message: `${config.name} is ${organ?.status || 'UNKNOWN'}`,
        };
      }
    }
  }

  return { passed: true, condition };
}

// ═══════════════════════════════════════════════════════════════════
// ARET TASK VALIDATION
// ═══════════════════════════════════════════════════════════════════

/**
 * Validate an AREP task declaration against the canonical schema.
 * Returns { valid: boolean, errors: string[] }
 */
function validateAREPDeclaration(task) {
  const errors = [];

  if (!task.arep_version || task.arep_version !== '1.0') {
    errors.push('Missing or invalid arep_version. Must be "1.0".');
  }

  if (!task.intent?.statement || typeof task.intent.statement !== 'string') {
    errors.push('Missing intent.statement — the human must declare WHAT they want.');
  }

  if (!task.intent?.success_criteria || !Array.isArray(task.intent.success_criteria) || task.intent.success_criteria.length === 0) {
    errors.push('Missing intent.success_criteria — must declare verifiable completion conditions.');
  }

  if (!task.principal?.actor_id || task.principal.actor_id !== 'arif-fazil') {
    errors.push('Invalid principal.actor_id — must be "arif-fazil" (F13 SOVEREIGN).');
  }

  if (!task.reality_constraints?.evidence_floor) {
    errors.push('Missing reality_constraints.evidence_floor — must declare minimum evidence layer.');
  }

  if (task.reality_constraints?.reversibility?.maximum_action_class === 'ATOMIC' && 
      task.principal?.ratification_mode !== 'explicit_ack') {
    errors.push('ATOMIC actions require explicit_ack ratification from principal.');
  }

  // Validate delegation chain
  if (!task.delegation_chain || !Array.isArray(task.delegation_chain) || task.delegation_chain.length === 0) {
    errors.push('Missing delegation_chain — must declare authority lineage.');
  } else {
    const firstHop = task.delegation_chain[0];
    if (firstHop.role !== 'PRINCIPAL' || firstHop.actor_id !== 'arif-fazil') {
      errors.push('Delegation chain must start with PRINCIPAL arif-fazil.');
    }

    // Validate attenuation: each hop should not be wider than parent
    for (let i = 1; i < task.delegation_chain.length; i++) {
      if ((task.delegation_chain[i].max_subagent_depth || 0) > (task.delegation_chain[i-1].max_subagent_depth || 0)) {
        errors.push(`Delegation chain violation at hop ${i}: subagent depth cannot exceed parent's.`);
      }
    }
  }

  return { valid: errors.length === 0, errors };
}

// ═══════════════════════════════════════════════════════════════════
// ARET TASK LIFECYCLE — state machine
// ═══════════════════════════════════════════════════════════════════

// A2A v1.0.0 9-state task lifecycle model. 8 states per the canonical wire
// protocol (SUBMITTED, WORKING, INPUT_REQUIRED, AUTH_REQUIRED, COMPLETED,
// FAILED, CANCELED, REJECTED). AUTH_REQUIRED was added in CIV-33 Gap 4 closure.
const VALID_STATES = [
  'TASK_STATE_SUBMITTED',
  'TASK_STATE_WORKING',
  'TASK_STATE_INPUT_REQUIRED',
  'TASK_STATE_AUTH_REQUIRED',
  'TASK_STATE_COMPLETED',
  'TASK_STATE_FAILED',
  'TASK_STATE_CANCELED',
  'TASK_STATE_REJECTED',
];
const VALID_TRANSITIONS = {
  'TASK_STATE_SUBMITTED':      ['TASK_STATE_WORKING', 'TASK_STATE_AUTH_REQUIRED', 'TASK_STATE_REJECTED', 'TASK_STATE_CANCELED'],
  'TASK_STATE_WORKING':        ['TASK_STATE_COMPLETED', 'TASK_STATE_FAILED', 'TASK_STATE_INPUT_REQUIRED', 'TASK_STATE_AUTH_REQUIRED', 'TASK_STATE_CANCELED'],
  'TASK_STATE_INPUT_REQUIRED': ['TASK_STATE_WORKING', 'TASK_STATE_AUTH_REQUIRED', 'TASK_STATE_CANCELED', 'TASK_STATE_REJECTED'],
  'TASK_STATE_AUTH_REQUIRED':  ['TASK_STATE_WORKING', 'TASK_STATE_CANCELED', 'TASK_STATE_REJECTED'],
  'TASK_STATE_COMPLETED':      [],  // terminal
  'TASK_STATE_FAILED':         [],  // terminal
  'TASK_STATE_CANCELED':       [],  // terminal
  'TASK_STATE_REJECTED':       [],  // terminal
};

/**
 * Transition a task to a new state. Records state history.
 */
function transitionTaskState(task, newState, actorId, note) {
  if (!VALID_STATES.includes(newState)) {
    throw new Error(`Invalid state: ${newState}`);
  }

  const currentState = task.task_lifecycle?.current_state || 'TASK_STATE_SUBMITTED';
  const allowed = VALID_TRANSITIONS[currentState] || [];
  
  if (!allowed.includes(newState)) {
    throw new Error(`Invalid transition: ${currentState} → ${newState}. Allowed: ${allowed.join(', ')}`);
  }

  if (!task.task_lifecycle) task.task_lifecycle = {};
  if (!task.task_lifecycle.state_history) task.task_lifecycle.state_history = [];

  task.task_lifecycle.state_history.push({ state: currentState, timestamp: new Date().toISOString() });
  task.task_lifecycle.current_state = newState;

  task.task_lifecycle.state_history.push({
    state: newState,
    timestamp: new Date().toISOString(),
    actor_id: actorId || 'arifos-kernel',
    evidence_layer_at_transition: task._currentEvidenceLayer || 'INFERRED',
    note: note || '',
  });

  task.telemetry = task.telemetry || {};
  task.telemetry.updated_at = new Date().toISOString();

  return task;
}

// ═══════════════════════════════════════════════════════════════════
// ARET TASK EXECUTION ENGINE
// ═══════════════════════════════════════════════════════════════════

/**
 * Main entry point: process an AREP task declaration.
 * 
 * Flow:
 * 1. Validate declaration
 * 2. Run reality gates
 * 3. If gates pass → working → delegate to agent
 * 4. If gates fail on HALT → rejected
 * 5. If gates fail on ESCALATE → input-required (waiting for human)
 * 
 * @param {object} task — Raw AREP task declaration
 * @param {object} taskStore — Redis-backed task store
 * @param {function} executeFn — function to call for actual execution
 * @returns {object} — { accepted, task, gateResult, verdict }
 */
async function processAREPTask(task, taskStore, executeFn) {
  // 1. Validate
  const validation = validateAREPDeclaration(task);
  if (!validation.valid) {
    task.task_lifecycle = task.task_lifecycle || {};
    task.task_lifecycle.current_state = 'TASK_STATE_REJECTED';
    return {
      accepted: false,
      task,
      gateResult: null,
      verdict: 'VOID',
      reason: `AREP validation failed: ${validation.errors.join('; ')}`,
    };
  }

  // 2. Initialize task
  task.task_lifecycle = task.task_lifecycle || {};
  task.task_lifecycle.current_state = 'TASK_STATE_SUBMITTED';
  task.task_lifecycle.state_history = [{
    state: 'TASK_STATE_SUBMITTED',
    timestamp: new Date().toISOString(),
    actor_id: task.principal.actor_id,
    evidence_layer_at_transition: 'INFERRED',
    note: 'AREP task received',
  }];

  task.telemetry = task.telemetry || {};
  task.telemetry.task_id = task.telemetry.task_id || `arep-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  task.telemetry.created_at = new Date().toISOString();

  // 3. Reality gating
  const gateResult = await evaluateRealityGates(task);

  // 4. Check evidence floor
  const requiredLayer = task.reality_constraints.evidence_floor;
  const currentLayer = gateResult.currentEvidenceLayer;

  if (LAYER_ORDINALS[currentLayer] > LAYER_ORDINALS[requiredLayer]) {
    // Evidence insufficient → hold or reject
    transitionTaskState(task, 'TASK_STATE_INPUT_REQUIRED', 'arifos-kernel',
      `Evidence insufficient: required ${requiredLayer}, current ${currentLayer}. Waiting for human ratification.`);
    
    return {
      accepted: true,
      task,
      gateResult,
      verdict: 'SABAR',
      reason: `Evidence floor not met. Required: ${requiredLayer}, Current: ${currentLayer}. Task held for human review.`,
    };
  }

  // 5. Check for HALT violations
  const haltViolations = gateResult.violations.filter(v => v.action === 'HALT');
  if (haltViolations.length > 0) {
    transitionTaskState(task, 'TASK_STATE_REJECTED', 'arifos-kernel',
      `Reality gate HALT: ${haltViolations.map(v => v.message).join('; ')}`);
    
    return {
      accepted: false,
      task,
      gateResult,
      verdict: 'VOID',
      reason: `Reality gates failed: ${haltViolations.map(v => v.message).join('; ')}`,
    };
  }

  // 6. Check for ESCALATE violations
  const escalateViolations = gateResult.violations.filter(v => v.action === 'ESCALATE');
  if (escalateViolations.length > 0) {
    transitionTaskState(task, 'TASK_STATE_INPUT_REQUIRED', 'arifos-kernel',
      `Reality gate ESCALATE: ${escalateViolations.map(v => v.message).join('; ')}`);
    
    return {
      accepted: true,
      task,
      gateResult,
      verdict: 'HOLD',
      reason: `Escalated to human: ${escalateViolations.map(v => v.message).join('; ')}`,
    };
  }

  // 7. All gates passed → execute
  transitionTaskState(task, 'TASK_STATE_WORKING', 'arifos-kernel', 'Reality gates passed. Executing task.');

  // Store task
  if (taskStore) {
    const taskId = task.telemetry.task_id;
    await taskStore.setTask(taskId, task);
  }

  // Execute
  if (executeFn) {
    try {
      await executeFn(task);
    } catch (execErr) {
      transitionTaskState(task, 'TASK_STATE_FAILED', 'arifos-kernel', `Execution error: ${execErr.message}`);
      return {
        accepted: true,
        task,
        gateResult,
        verdict: 'SABAR',
        reason: `Task failed during execution: ${execErr.message}`,
      };
    }
  }

  return {
    accepted: true,
    task,
    gateResult,
    verdict: 'SEAL',
    reason: 'Reality gates passed. Task dispatched.',
  };
}

/**
 * Seal a completed AREP task to VAULT999.
 */
async function sealAREPTask(task) {
  transitionTaskState(task, 'TASK_STATE_COMPLETED', 'arifos-kernel', 'Task completed. Sealing to VAULT999.');

  task.task_lifecycle.artifacts = task.task_lifecycle.artifacts || [];
  task.task_lifecycle.artifacts.push({
    artifact_id: `seal-${task.telemetry.task_id}`,
    artifact_type: 'seal',
    evidence_layer: 'GROUND_TRUTH',
    vault_seal_hash: null, // filled by VAULT999
  });

  task.constitutional_binding = task.constitutional_binding || {};
  task.constitutional_binding.governance_verdict = 'SEAL';
  task._currentEvidenceLayer = 'GROUND_TRUTH';

  try {
    const sealResult = await writeSeal(
      task,
      'arifos-kernel',
      `AREP task completed: ${task.intent.statement.substring(0, 100)}`,
      {
        arep_version: '1.0',
        success_criteria: task.intent.success_criteria,
        delegation_depth: task.delegation_chain.length,
        evidence_layer_at_seal: 'GROUND_TRUTH',
      }
    );
    task.task_lifecycle.artifacts[task.task_lifecycle.artifacts.length - 1].vault_seal_hash = sealResult?.hash || 'pending';
  } catch (err) {
    // Non-blocking — VAULT999 write failures don't invalidate the task
    console.error(`[AREP] VAULT999 seal failed for ${task.telemetry.task_id}: ${err.message}`);
  }

  return task;
}

module.exports = {
  REALITY_LAYERS,
  LAYER_ORDINALS,
  FEDERATION_ORGANS,
  probeFederation,
  assessEvidenceLayer,
  evaluateRealityGates,
  validateAREPDeclaration,
  transitionTaskState,
  processAREPTask,
  sealAREPTask,
};
