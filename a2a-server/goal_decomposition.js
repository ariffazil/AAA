#!/usr/bin/env node
/**
 * Δ→Ω→Ψ Goal Decomposition — Encoder + Jacobian Skeleton
 * ════════════════════════════════════════════════════════════════
 * 
 * ENCODER (Δ ring, 333-AGI):   goal → task manifold mapper
 * JACOBIAN:                     ∂T/∂G — sensitivity of tasks to goal fields
 * DECODER (Ω ring, 555-ASI):    tasks → A2A envelopes (via task_routing.js)
 * METABOLIZER (Ψ ring, 888-APEX): results → Jacobian update → re-plan
 * 
 * INTEGRATION:
 *   cognitive_hierarchy.js  — ring/role resolution
 *   emd-validation-gate.js  — envelope validation (F12)
 *   federation_envelope.js  — governance grammar wrapping
 *   A2A Live Wire (19 routes) — task dispatch
 * 
 * EMD CYCLE:
 *   ENCODE: goal → structured task vector over agents/skills/tools
 *   METABOLIZE: critique, flag paradoxes, compute Jacobian stability
 *   DECODE: task → A2A envelope → dispatch → result → metabolize again
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ── Ring mapping from cognitive hierarchy ─────────────────────────────────
const COGNITIVE_HIERARCHY_PATH = '/root/AAA/contracts/cognitive_hierarchy.yaml';
const MANIFEST_PATH = path.resolve(__dirname, 'A2A_LIVE_WIRE_MANIFEST.json');

// Lazy-loaded
let _hierarchy = null;
let _manifest = null;

function loadHierarchy() {
  if (_hierarchy) return _hierarchy;
  try {
    const yaml = require('yaml');
    const raw = fs.readFileSync(COGNITIVE_HIERARCHY_PATH, 'utf-8');
    _hierarchy = yaml.parse(raw);
    return _hierarchy;
  } catch (e) {
    // Fallback: hardcoded ring definitions
    _hierarchy = {
      rings: [
        { id: 'generator', label: 'Outer Ring — Generator', thermodynamic_role: 'entropy_source',
          authority: { observe: true, suggest: true, simulate: true, draft: true, queue: true,
            execute_reversible: true, execute_high_impact: false, irreversible: false, seal: false }},
        { id: 'epistemic_floor', label: 'Inner Core — Metabolizer', thermodynamic_role: 'entropy_sink',
          authority: { observe: true, suggest: false, simulate: false, draft: false, queue: false,
            execute_reversible: true, execute_high_impact: true, irreversible: false, seal: true }},
      ]
    };
    return _hierarchy;
  }
}

function loadManifest() {
  if (_manifest) return _manifest;
  try {
    _manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf-8'));
  } catch (e) {
    _manifest = { routes: [] };
  }
  return _manifest;
}

// ── Ring → Agent → Skill → Tool resolution ──────────────────────────────

const AGENT_RING_MAP = {
  // Δ ring — generator/encoder
  '333-AGI':    { ring: 'generator', role: 'encoder', authority: 'reason', lane: 'Δ MIND' },
  'opencode':   { ring: 'generator', role: 'forge_instrument', authority: 'execute', lane: 'Δ FORGE' },
  'claude-code':{ ring: 'generator', role: 'architect', authority: 'reason', lane: 'Δ ARCHITECT' },
  'kimi-code':  { ring: 'generator', role: 'prototyper', authority: 'reason', lane: 'Δ PROTOTYPE' },
  'grok-build': { ring: 'generator', role: 'builder', authority: 'reason', lane: 'Δ BUILD' },
  
  // Ω ring — metabolizer/critique
  '555-ASI':    { ring: 'epistemic_floor', role: 'metabolizer', authority: 'critique', lane: 'Ω HEART' },
  'arifos':     { ring: 'epistemic_floor', role: 'kernel', authority: 'constitutional', lane: 'Ω KERNEL' },
  'geox':       { ring: 'epistemic_floor', role: 'earth_witness', authority: 'evidence', lane: 'Ω GEOX' },
  'wealth':     { ring: 'epistemic_floor', role: 'capital_witness', authority: 'evidence', lane: 'Ω WEALTH' },
  'well':       { ring: 'epistemic_floor', role: 'human_witness', authority: 'evidence', lane: 'Ω WELL' },
  
  // Ψ ring — decoder/verdict
  '888-APEX':   { ring: 'epistemic_floor', role: 'decoder', authority: 'verdict', lane: 'Ψ JUDGE' },
  'aforge':     { ring: 'epistemic_floor', role: 'executor', authority: 'execute', lane: 'Ψ FORGE' },
  'hermes-asi': { ring: 'generator', role: 'dispatcher', authority: 'route', lane: 'Δ DISPATCH' },
};

// Task type → preferred agent routing (for task→A2A envelope mapping)
const TASK_ORGAN_MAP = {
  'audit': 'arifos', 'constitutional': 'arifos', 'judge': 'arifos', 'seal': 'arifos',
  'build': 'aforge', 'deploy': 'aforge', 'execute': 'aforge', 'test': 'aforge',
  'code': 'opencode', 'refactor': 'opencode', 'engineering': 'opencode',
  'architecture': 'claude-code', 'prototype': 'kimi-code', 'research': 'grok-build',
  'geoscience': 'geox', 'seismic': 'geox', 'basin': 'geox', 'prospect': 'geox',
  'capital': 'wealth', 'npv': 'wealth', 'finance': 'wealth', 'market': 'wealth',
  'readiness': 'well', 'vitality': 'well', 'health': 'well',
  'dispatch': 'hermes-asi', 'route': 'hermes-asi',
};

// Skill → capability tags (for capability mapping)
const SKILL_CAPABILITY_MAP = {
  'audit-seal': ['audit', 'vault', 'receipt'],
  'kernel-bind': ['session', 'constitutional'],
  'observe-ground': ['evidence', 'probe'],
  'route-dispatch': ['routing', 'a2a'],
  'FORGE-github': ['git', 'repository'],
  'FORGE-ci-diagnose': ['ci', 'diagnostic'],
  'FORGE-pr-review': ['review', 'code'],
  'AGI-plan-dag': ['planning', 'dag', 'decomposition'],
  'arifos-constitutional-judge': ['verdict', 'seal'],
  'arifos-constitutional-judge': ['verdict', 'hold'],
  'atlas333-cognitive-geometry': ['paradox', 'reasoning'],
};

// ── Types ──────────────────────────────────────────────────────────────

/**
 * @typedef {Object} Goal
 * @property {string} id — unique goal identifier
 * @property {string} actor — who initiated the goal
 * @property {string} intent — natural-language description
 * @property {Object} constraints — {risk_band, time_horizon, budget, reversibility}
 * @property {string[]} org_scope — which organs are in scope
 * @property {string} risk_band — 'low' | 'medium' | 'high' | '888_HOLD'
 * @property {string} time_horizon — 'immediate' | 'session' | 'day' | 'week'
 * @property {Object} metadata — arbitrary key-value
 */

/**
 * @typedef {Object} Task
 * @property {string} id — unique task identifier
 * @property {string} name — human-readable task name
 * @property {string} status — 'pending' | 'running' | 'done' | 'failed'
 * @property {string} agent — target agent ID
 * @property {string} ring — 'generator' | 'epistemic_floor'
 * @property {string} skill — skill to invoke
 * @property {string[]} depends_on — prerequisite task IDs
 * @property {Object} jacobian — {field: weight} sensitivity to goal fields
 * @property {Object} receipt — dispatch receipt
 */

// ── Receipt chain ──────────────────────────────────────────────────────

let _receiptChain = [];
function emitReceipt(layer, action, data) {
  const r = {
    id: `rec-${crypto.randomUUID().slice(0, 8)}`,
    layer, action,
    timestamp: new Date().toISOString(),
    hash: crypto.createHash('sha256').update(
      JSON.stringify({ layer, action, data, ts: Date.now() })
    ).digest('hex').slice(0, 16),
    parentId: _receiptChain.length > 0 ? _receiptChain[_receiptChain.length - 1].id : null,
  };
  _receiptChain.push(r);
  return r;
}

function resetReceipts() { _receiptChain = []; }
function getReceipts() { return _receiptChain; }

// ── Δ ENCODER: goal → task manifold mapper ─────────────────────────────

/**
 * encodeGoalToTasks(G) — maps a goal into a structured task vector
 * over agents, skills, and tools using the cognitive hierarchy.
 * 
 * Algorithm:
 *   1. Semantic parse: extract sub-goals from intent
 *   2. Capability mapping: ring/agent/skill/tool per sub-goal
 *   3. Jacobian seed: ∂task/∂goal_field weights
 * 
 * @param {Goal} goal
 * @returns {{ tasks: Task[], jacobian: Object, receipts: Object[] }}
 */
function encodeGoalToTasks(goal) {
  resetReceipts();
  emitReceipt('Δ', 'encode_start', { goal_id: goal.id, intent: goal.intent });

  const hierarchy = loadHierarchy();
  const manifest = loadManifest();
  
  // Step 1: Semantic parse — split intent into sub-goals
  const subgoals = parseSubgoals(goal.intent);
  emitReceipt('Δ', 'parse_complete', { subgoals: subgoals.length });

  // Step 2: Capability mapping — each subgoal → (ring, agent, skill, tool)
  const tasks = [];
  for (let i = 0; i < subgoals.length; i++) {
    const sg = subgoals[i];
    const mapping = mapSubgoalToCapability(sg, goal.org_scope, manifest);
    
    const task = {
      id: `task-${i + 1}`,
      name: sg,
      status: 'pending',
      agent: mapping.agent,
      ring: mapping.ring,
      role: mapping.role,
      skill: mapping.skill,
      depends_on: i > 0 ? [`task-${i}`] : [],
      jacobian: seedJacobianWeights(sg, goal),
      receipt: null,
    };
    tasks.push(task);
  }

  // Step 3: Build Jacobian skeleton
  const jacobian = buildJacobian(goal, tasks);

  emitReceipt('Δ', 'encode_complete', { 
    tasks: tasks.length, 
    agents: [...new Set(tasks.map(t => t.agent))],
    rings: [...new Set(tasks.map(t => t.ring))],
  });

  return { tasks, jacobian, receipts: getReceipts() };
}

/**
 * parseSubgoals(intent) — split natural-language intent into sub-goals
 */
function parseSubgoals(intent) {
  // Pattern: "Do X, then Y, and Z" or "Do X. Then Y."
  // Split on sentence boundaries, conjunctions, and sequential markers
  const cleaned = intent
    .replace(/^forge\s+/i, '')
    .replace(/first[,:]?\s*/gi, '')
    .replace(/then[,:]?\s*/gi, '|')
    .replace(/and then[,:]?\s*/gi, '|')
    .replace(/finally[,:]?\s*/gi, '|')
    .replace(/next[,:]?\s*/gi, '|');

  // Split on pipe (sequential markers) or period+space
  const parts = cleaned
    .split(/\s*\|\s*/)
    .flatMap(p => p.split(/\.\s+(?=[A-Z])/))
    .map(p => p.trim())
    .filter(p => p.length > 5);

  // If no structure detected, treat the whole intent as one task
  if (parts.length <= 1) {
    // Try comma-splitting for parallel tasks
    const commas = cleaned.split(/,\s+(?=build|deploy|test|run|verify|check|audit|analyze|create|update|fix|add|remove|deploy|configure|setup|install)/i);
    if (commas.length > 1) return commas.map(c => c.trim()).filter(c => c.length > 5);
    
    // Default: single task
    return [cleaned];
  }

  return parts;
}

/**
 * mapSubgoalToCapability(subgoal, orgScope, manifest) → {ring, agent, role, skill}
 */
function mapSubgoalToCapability(subgoal, orgScope, manifest) {
  const sgLower = subgoal.toLowerCase();

  // 1. Check for explicit organ mentions
  if (orgScope && orgScope.length > 0) {
    for (const organ of orgScope) {
      if (sgLower.includes(organ.toLowerCase())) {
        const mapping = AGENT_RING_MAP[organ] || { ring: 'generator', role: 'worker', authority: 'execute', lane: 'Δ' };
        return { ...mapping, agent: organ, skill: resolveSkill(sgLower, organ) };
      }
    }
  }

  // 2. Check task keywords → agent mapping
  for (const [keyword, agent] of Object.entries(TASK_ORGAN_MAP)) {
    if (sgLower.includes(keyword)) {
      const mapping = AGENT_RING_MAP[agent] || { ring: 'generator', role: 'worker', authority: 'execute', lane: 'Δ' };
      return { ...mapping, agent, skill: resolveSkill(sgLower, agent) };
    }
  }

  // 3. Check manifest routes for matching agents
  const routes = manifest.routes || [];
  for (const route of routes) {
    if (sgLower.includes(route.to) || sgLower.includes(route.from)) {
      const agent = route.to;
      const mapping = AGENT_RING_MAP[agent] || { ring: 'generator', role: 'worker', authority: 'execute', lane: 'Δ' };
      return { ...mapping, agent, skill: resolveSkill(sgLower, agent) };
    }
  }

  // 4. Default: route to opencode (primary forge instrument)
  return { ring: 'generator', role: 'forge_instrument', agent: 'opencode', 
           authority: 'execute', lane: 'Δ FORGE', skill: resolveSkill(sgLower, 'opencode') };
}

/**
 * resolveSkill(taskDescription, agent) → best-matching skill name
 */
function resolveSkill(taskDescription, agent) {
  const lower = taskDescription.toLowerCase();
  
  for (const [skill, tags] of Object.entries(SKILL_CAPABILITY_MAP)) {
    if (tags.some(t => lower.includes(t))) return skill;
  }

  // Default skills per agent
  const agentDefaults = {
    'opencode': 'AGI-plan-dag',
    'arifos': 'kernel-bind',
    'aforge': 'FORGE-github',
    'geox': 'observe-ground',
    'wealth': 'observe-ground',
    'well': 'observe-ground',
    'hermes-asi': 'route-dispatch',
    'claude-code': 'AGI-plan-dag',
    'kimi-code': 'AGI-plan-dag',
    'grok-build': 'AGI-plan-dag',
  };

  return agentDefaults[agent] || 'AGI-plan-dag';
}

// ── JACOBIAN: ∂T/∂G — sensitivity of tasks to goal fields ─────────────

/**
 * seedJacobianWeights(taskDescription, goal) → {field: weight}
 * 
 * Initial sensitivity estimates based on keyword matching.
 * Higher weight = task more sensitive to changes in that goal field.
 */
function seedJacobianWeights(taskDescription, goal) {
  const lower = taskDescription.toLowerCase();
  const weights = {};

  // Risk sensitivity: if task mentions deploy/delete/execute → high risk sensitivity
  if (/deploy|delete|execute|restart|rm|drop|force/i.test(lower)) {
    weights.risk_band = 0.9;
  } else if (/test|verify|check|audit|probe|read/i.test(lower)) {
    weights.risk_band = 0.2;
  } else {
    weights.risk_band = 0.5;
  }

  // Org scope sensitivity: if task mentions specific organ → high org sensitivity
  for (const organ of (goal.org_scope || [])) {
    if (lower.includes(organ.toLowerCase())) {
      weights.org_scope = 0.8;
      break;
    }
  }
  if (!weights.org_scope) weights.org_scope = 0.3;

  // Time horizon sensitivity
  if (/immediate|now|urgent|asap/i.test(lower)) {
    weights.time_horizon = 0.9;
  } else if (/later|eventually|someday/i.test(lower)) {
    weights.time_horizon = 0.1;
  } else {
    weights.time_horizon = 0.4;
  }

  // Intent sensitivity — all tasks are sensitive to intent changes
  weights.intent = 0.6;

  return weights;
}

/**
 * buildJacobian(goal, tasks[]) → Jacobian matrix + analysis
 * 
 * J = ∂T/∂G — full Jacobian skeleton.
 * J[i][field] = task_i's sensitivity to goal field 'field'
 * 
 * Returns:
 *   - matrix: [task][field] → weight
 *   - blastRadii: per-task aggregated sensitivity
 *   - conditionNumber: max/min blast radius ratio
 *   - rePlanThresholds: which field changes trigger re-planning
 */
function buildJacobian(goal, tasks) {
  const fields = ['intent', 'risk_band', 'org_scope', 'time_horizon', 'constraints'];
  const matrix = [];
  const blastRadii = [];

  for (let i = 0; i < tasks.length; i++) {
    const row = {};
    const jw = tasks[i].jacobian || {};
    
    for (const field of fields) {
      // Priority: task's own jacobian weights > goal context > defaults
      let weight = jw[field] || 0;
      
      // Cross-task sensitivity: if task_j depends on task_i
      if (i > 0 && tasks[i].depends_on?.includes(tasks[i-1].id)) {
        weight += 0.2; // dependency chain amplification
      }
      
      // Ring-based sensitivity
      if (tasks[i].ring === 'epistemic_floor') {
        weight += 0.15; // inner core tasks more sensitive to constraint changes
      }
      
      row[field] = Math.round(Math.min(1.0, weight) * 100) / 100;
    }

    matrix.push(row);
    const totalSensitivity = Object.values(row).reduce((s, v) => s + Math.abs(v), 0);
    blastRadii.push({
      taskId: tasks[i].id,
      taskName: tasks[i].name,
      blastRadius: Math.round(totalSensitivity * 100) / 100,
      agent: tasks[i].agent,
      ring: tasks[i].ring,
    });
  }

  // Condition number = max blast radius / min blast radius
  const maxBR = Math.max(...blastRadii.map(b => b.blastRadius), 0.01);
  const minBR = Math.max(0.01, Math.min(...blastRadii.map(b => b.blastRadius)));
  const conditionNumber = Math.round((maxBR / minBR) * 100) / 100;

  // Re-plan thresholds: which goal field changes trigger task re-planning
  const rePlanThresholds = {};
  for (const field of fields) {
    const maxSensitivity = Math.max(...matrix.map(row => row[field] || 0));
    rePlanThresholds[field] = {
      maxSensitivity: Math.round(maxSensitivity * 100) / 100,
      rePlanIf: maxSensitivity > 0.6 ? 'any_change' : maxSensitivity > 0.3 ? 'significant_change' : 'no_replan_needed',
    };
  }

  emitReceipt('Δ', 'jacobian_computed', {
    tasks: tasks.length,
    condition: conditionNumber,
    maxBlast: maxBR,
  });

  return {
    matrix,
    blastRadii,
    conditionNumber,
    rePlanThresholds,
    interpretation: blastRadii.length > 0
      ? `Most sensitive task: ${blastRadii.sort((a,b) => b.blastRadius - a.blastRadius)[0]?.taskName}`
      : 'no tasks',
    note: 'Jacobian enables local linearity — small goal changes → predictable task changes',
  };
}

// ── Ω DECODER: tasks → A2A envelopes ───────────────────────────────────

/**
 * decodeTasksToEnvelopes(tasks, goal, sessionId) → A2AEnvelope[]
 * 
 * Maps each task to an A2A envelope that can be dispatched
 * through the AAA gateway's A2A Live Wire.
 * 
 * Integration: uses emd-validation-gate.js patterns + federation_envelope.js grammar
 */
function decodeTasksToEnvelopes(tasks, goal, sessionId) {
  const envelopes = [];

  for (const task of tasks) {
    const envelope = {
      header: {
        goal_id: goal.id,
        task_id: task.id,
        session_id: sessionId || 'goal-decomposer',
        timestamp: new Date().toISOString(),
      },
      route: {
        agent: task.agent,
        ring: task.ring,
        role: task.role,
        skill: task.skill,
        method: 'tasks/send',          // A2A method
      },
      constraints: {
        risk_band: goal.risk_band || 'low',
        time_horizon: goal.time_horizon || 'session',
        reversibility: task.ring === 'generator' ? 'reversible' : 'verify_before_irreversible',
      },
      emd_payload: {
        type: 'task_delegation',
        text: task.name,
        metadata: {
          jacobian: task.jacobian,
          depends_on: task.depends_on,
        },
      },
      governance: {
        receipt_required: true,
        signature_required: goal.risk_band === 'high' || task.ring === 'epistemic_floor',
        floor_gates: ['F1', 'F2', 'F12'],
      },
    };
    envelopes.push(envelope);
  }

  return envelopes;
}

// ── Ψ METABOLIZER: results → Jacobian update → re-plan ────────────────

/**
 * metabolizeResults(results, tasks, jacobian, goal) → updated state
 * 
 * Closes the Δ→Ω→Ψ cycle:
 *   1. Update task states from results
 *   2. Update Jacobian weights based on observed failures
 *   3. Signal if re-planning is needed
 * 
 * @param {Object[]} results — {taskId, status, agent, error?}
 * @param {Task[]} tasks
 * @param {Object} jacobian
 * @param {Goal} goal
 */
function metabolizeResults(results, tasks, jacobian, goal) {
  emitReceipt('Ψ', 'metabolize_start', { results: results.length });

  const updated = { tasks: [...tasks], jacobian: { ...jacobian }, needsReplan: false, signals: [] };

  for (const result of results) {
    const taskIdx = updated.tasks.findIndex(t => t.id === result.taskId);
    if (taskIdx === -1) continue;

    const task = { ...updated.tasks[taskIdx] };

    if (result.status === 'failed') {
      task.status = 'failed';

      // Run dual-sensitivity check on the failure
      const ds = dualSensitivityVerify(task, result.error || task.name, { sourceType: 'internal' });
      task.dualSensitivity = ds;

      // Update Jacobian: increase risk_band sensitivity when failure correlates with tight constraints
      if (task.jacobian) {
        task.jacobian.risk_band = Math.min(1.0, (task.jacobian.risk_band || 0.3) + 0.2);
        task.jacobian.time_horizon = Math.min(1.0, (task.jacobian.time_horizon || 0.3) + 0.1);
      }

      // Signal re-plan if high-sensitivity task failed
      if (task.jacobian?.risk_band > 0.7 || task.ring === 'epistemic_floor' || ds.verdict === 'VOID') {
        updated.needsReplan = true;
        updated.signals.push({
          type: 'replan_suggested',
          taskId: task.id,
          reason: `High-sensitivity task failed (risk_band sensitivity=${task.jacobian?.risk_band}, dualSensitivity=${ds.verdict})`,
        });
      }
    } else if (result.status === 'done') {
      task.status = 'done';

      // Run dual-sensitivity check on success
      const ds = dualSensitivityVerify(task, result.output || task.name, { sourceType: 'internal' });
      task.dualSensitivity = ds;

      // Decrease sensitivity — task proved reliable
      if (task.jacobian) {
        task.jacobian.risk_band = Math.max(0.1, (task.jacobian.risk_band || 0.3) - 0.05);
      }

      // Flag if ToAC detects hallucination in otherwise-successful task
      if (ds.verdict === 'HOLD' || ds.verdict === 'VOID') {
        updated.signals.push({
          type: 'toac_anomaly',
          taskId: task.id,
          reason: `Task completed but dual-sensitivity=${ds.verdict}: ${ds.unified.interpretation}`,
        });
      }
    }

    updated.tasks[taskIdx] = task;
  }

  // Rebuild Jacobian with updated weights
  updated.jacobian = buildJacobian(goal, updated.tasks);

  emitReceipt('Ψ', 'metabolize_complete', {
    tasks_updated: results.length,
    needs_replan: updated.needsReplan,
    signals: updated.signals.length,
  });

  return updated;
}

// ── ToAC: Perceptual Sensitivity — claim extraction + tri-witness ─────

/**
 * classifyPerception(text) → epistemic label (OBS|DER|INT|SPEC)
 * 
 * ToAC primitive: ∂F/∂Cₖ — how does this feature behave under contrast?
 * Heuristic classification based on linguistic markers of epistemic certainty.
 * Mirrors emd-validation-gate.js::classifyPerception() for standalone use.
 */
function classifyPerception(text) {
  if (!text) return 'INT';
  const t = text.toLowerCase();
  if (t.match(/\b(measured|observed|recorded|detected|found|data shows|the log|confirmed by)\b/)) return 'OBS';
  if (t.match(/\b(calculated|computed|derived|extrapolated|estimated|forecast)\b/)) return 'DER';
  if (t.match(/\b(interpreted|synthesized|reasoned|inferred|concluded|analyzed)\b/)) return 'INT';
  if (t.match(/\b(speculated|hypothetical|might|could|possibly|perhaps|assumed)\b/)) return 'SPEC';
  return 'INT';
}

/**
 * extractClaims(text) → [{text, epistemicLabel, confidence}]
 * 
 * Splits text into claim-sized chunks and classifies each.
 */
function extractClaims(text) {
  if (!text || text.length < 10) return [];
  const claims = [];
  const sentences = text.split(/(?<=[.!?])\s+/);
  const CONFIDENCE_CAPS = { OBS: 0.90, DER: 0.85, INT: 0.75, SPEC: 0.60 };
  
  for (const sentence of sentences) {
    const trimmed = sentence.trim();
    if (trimmed.length < 15) continue;
    const label = classifyPerception(trimmed);
    claims.push({ text: trimmed, epistemicLabel: label, confidence: CONFIDENCE_CAPS[label] || 0.75 });
  }
  return claims;
}

/**
 * computeTriWitness(claims, sourceType) → {W3, h, ai, ext, verdict}
 * 
 * W³ = ∛(Human × AI × External). Nash product of three witness channels.
 * Internal sources get higher baseline trust. External sources start at zero.
 */
function computeTriWitness(claims, sourceType = 'internal') {
  if (sourceType === 'external') {
    const h = 0.0, ai = 0.0, ext = claims.length > 0 ? 0.3 : 0.1;
    const W3 = Math.cbrt(h * ai * ext || 0.001);
    return { W3, h, ai, ext, verdict: W3 >= 0.30 ? 'WEAK' : 'DIVERGENT' };
  }
  const h = 0.5, ai = 0.7, ext = 0.6;
  const W3 = Math.cbrt(h * ai * ext);
  return { W3, h, ai, ext, verdict: W3 >= 0.60 ? 'CONSENSUS' : 'WEAK' };
}

// ── DUAL-SENSITIVITY KERNEL: Jacobian ∩ ToAC ──────────────────────────

/**
 * dualSensitivityVerify(task, outputText, options) → unified verdict
 * 
 * J ∩ ToAC = TRUTH. Runs both lenses on the same payload:
 * 
 *   COGNITIVE (Jacobian):  Does this task survive goal/constraint shifts?
 *     ∂T/∂G — sensitivity of task to goal fields.
 *     High sensitivity → task is fragile → HOLD on change.
 * 
 *   PERCEPTUAL (ToAC):     Is this output real or hallucinated?
 *     ∂F/∂Cₖ — stability of features under contrast transforms.
 *     High epistemic labels + strong tri-witness → real.
 *     Low tri-witness + speculative claims → hallucination.
 * 
 * VERDICT:
 *   SEAL — both Jacobian stable AND ToAC real (J ∩ ToAC = TRUE)
 *   SABAR — one lens weak, fixable (J ∩ ToAC = PARTIAL)
 *   HOLD — one lens fails, dangerous (J ∩ ToAC = FALSE on one axis)
 *   VOID — both lenses fail (J ∩ ToAC = FALSE)
 * 
 * @param {Task} task — the task being verified
 * @param {string} outputText — task result/output text
 * @param {Object} options — {jacobianContext, riskTolerance}
 * @returns {{verdict, jacobian: {}, toac: {}, unified: {}}}
 */
function dualSensitivityVerify(task, outputText, options = {}) {
  emitReceipt('Ψ', 'dual_sensitivity_start', { taskId: task.id });

  // ── LENS 1: Jacobian (cognitive sensitivity) ──
  const jw = task.jacobian || {};
  const riskSensitivity = jw.risk_band || 0.3;
  const scopeSensitivity = jw.org_scope || 0.3;
  const timeSensitivity = jw.time_horizon || 0.3;
  
  // Jacobian stability: lower = more stable across goal changes
  const maxSensitivity = Math.max(riskSensitivity, scopeSensitivity, timeSensitivity);
  const jacobianStable = maxSensitivity < 0.6;        // Task survives goal field changes
  const jacobianFragile = maxSensitivity >= 0.8;      // Task breaks on small goal changes
  const jacobianModerate = !jacobianStable && !jacobianFragile;

  const jacobianResult = {
    stable: jacobianStable,
    fragile: jacobianFragile,
    moderate: jacobianModerate,
    maxSensitivity: Math.round(maxSensitivity * 100) / 100,
    riskSensitivity: Math.round(riskSensitivity * 100) / 100,
    scopeSensitivity: Math.round(scopeSensitivity * 100) / 100,
    timeSensitivity: Math.round(timeSensitivity * 100) / 100,
    verdict: jacobianStable ? 'PASS' : jacobianFragile ? 'FAIL' : 'WEAK',
  };

  // ── LENS 2: ToAC (perceptual sensitivity) ──
  const claims = extractClaims(outputText || task.name);
  const triWitness = computeTriWitness(claims, options.sourceType || 'internal');
  
  // Epistemic quality: ratio of OBS+DER claims to total
  const obsCount = claims.filter(c => c.epistemicLabel === 'OBS').length;
  const derCount = claims.filter(c => c.epistemicLabel === 'DER').length;
  const intCount = claims.filter(c => c.epistemicLabel === 'INT').length;
  const specCount = claims.filter(c => c.epistemicLabel === 'SPEC').length;
  const totalClaims = claims.length || 1;
  const epistemicQuality = (obsCount + derCount) / totalClaims;
  
  // Anomaly detection: high SPEC count = possible hallucination
  const hallucinationRisk = specCount / totalClaims;
  
  const toacResult = {
    stable: epistemicQuality >= 0.5 && triWitness.verdict === 'CONSENSUS',
    fragile: hallucinationRisk > 0.5 || triWitness.verdict === 'DIVERGENT',
    epistemicQuality: Math.round(epistemicQuality * 100) / 100,
    hallucinationRisk: Math.round(hallucinationRisk * 100) / 100,
    triWitness: {
      W3: Math.round(triWitness.W3 * 100) / 100,
      verdict: triWitness.verdict,
      h: triWitness.h, ai: triWitness.ai, ext: triWitness.ext,
    },
    claimBreakdown: { obsCount, derCount, intCount, specCount },
    verdict: epistemicQuality >= 0.5 && triWitness.verdict !== 'DIVERGENT' ? 'PASS' 
           : hallucinationRisk > 0.5 ? 'FAIL' : 'WEAK',
  };

  // ── UNIFIED VERDICT: J ∩ ToAC ──
  let unifiedVerdict;
  if (jacobianResult.verdict === 'PASS' && toacResult.verdict === 'PASS') {
    unifiedVerdict = 'SEAL';         // Both lenses confirm — truth invariant under all transforms
  } else if (jacobianResult.verdict === 'FAIL' && toacResult.verdict === 'FAIL') {
    unifiedVerdict = 'VOID';         // Both lenses reject — artifact is unstable AND hallucinated
  } else if (jacobianResult.verdict === 'FAIL' || toacResult.verdict === 'FAIL') {
    unifiedVerdict = 'HOLD';         // One lens fails — cannot proceed
  } else {
    unifiedVerdict = 'SABAR';        // Both weak — fix and retry
  }

  const result = {
    verdict: unifiedVerdict,
    taskId: task.id,
    taskName: task.name,
    jacobian: jacobianResult,
    toac: toacResult,
    unified: {
      J_stable: jacobianResult.verdict === 'PASS',
      ToAC_stable: toacResult.verdict === 'PASS',
      intersection: unifiedVerdict === 'SEAL' ? 'TRUE' : unifiedVerdict === 'VOID' ? 'FALSE' : 'PARTIAL',
      interpretation: unifiedVerdict === 'SEAL' ? 'Truth survives both transforms — artifact is real and stable'
                    : unifiedVerdict === 'VOID' ? 'Truth fails both transforms — artifact is hallucinated and fragile'
                    : unifiedVerdict === 'HOLD' ? 'Truth fails one transform — cannot proceed without fix'
                    : 'Truth partially confirmed — proceed with caution',
    },
  };

  emitReceipt('Ψ', 'dual_sensitivity_complete', {
    verdict: unifiedVerdict,
    J: jacobianResult.verdict,
    ToAC: toacResult.verdict,
    intersection: result.unified.intersection,
  });

  return result;
}

// ── Full EMD pipeline ──────────────────────────────────────────────────

/**
 * emdPipeline(goal, options) → full Δ→Ω→Ψ decomposition
 * 
 * @param {Goal} goal
 * @param {Object} options — {sessionId, autoDispatch}
 * @returns {{goal, tasks, jacobian, envelopes, receipts, seal}}
 */
function emdPipeline(goal, options = {}) {
  resetReceipts();
  emitReceipt('EMD', 'pipeline_start', { goal_id: goal.id });

  // Δ: ENCODE — goal → tasks + Jacobian
  const encoded = encodeGoalToTasks(goal);
  
  // Ω: DECODE — tasks → A2A envelopes
  const envelopes = decodeTasksToEnvelopes(encoded.tasks, goal, options.sessionId);

  // Seal
  const allHashes = getReceipts().map(r => r.hash).join('');
  const seal = crypto.createHash('sha256').update(allHashes).digest('hex').slice(0, 16);

  emitReceipt('EMD', 'pipeline_complete', { seal });

  return {
    goal,
    tasks: encoded.tasks,
    jacobian: encoded.jacobian,
    envelopes,
    receipts: getReceipts(),
    seal,
    pipeline: 'Δ→Ω→Ψ',
    timestamp: new Date().toISOString(),
  };
}

// ── Exports ────────────────────────────────────────────────────────────

module.exports = {
  // Core
  encodeGoalToTasks,
  buildJacobian,
  decodeTasksToEnvelopes,
  metabolizeResults,
  emdPipeline,
  
  // Dual-Sensitivity Kernel
  dualSensitivityVerify,
  classifyPerception,
  extractClaims,
  computeTriWitness,
  
  // Utilities
  parseSubgoals,
  mapSubgoalToCapability,
  seedJacobianWeights,
  
  // State
  getReceipts,
  resetReceipts,
  
  // Constants
  AGENT_RING_MAP,
  TASK_ORGAN_MAP,
  SKILL_CAPABILITY_MAP,
};

// ── CLI test ────────────────────────────────────────────────────────────

if (require.main === module) {
  const goal = {
    id: `goal-${Date.now()}`,
    actor: 'arif',
    intent: process.argv[2] || 'Forge A2A goal decomposition, then test the flow, and verify integrity',
    constraints: { risk_band: 'medium', time_horizon: 'session' },
    org_scope: ['arifos', 'aforge', 'geox', 'wealth'],
    risk_band: 'medium',
    time_horizon: 'session',
  };

  console.log('╔════════════════════════════════════════╗');
  console.log('║   Δ→Ω→Ψ Goal Decomposition Pipeline   ║');
  console.log('╚════════════════════════════════════════╝');
  console.log(`\nGoal: ${goal.intent}`);

  const result = emdPipeline(goal);

  console.log(`\n── Δ ENCODER ──`);
  console.log(`Tasks: ${result.tasks.length}`);
  result.tasks.forEach(t => {
    console.log(`  ${t.id}: ${t.name}`);
    console.log(`    → agent=${t.agent} ring=${t.ring} skill=${t.skill}`);
    console.log(`    → jacobian risk_band=${t.jacobian?.risk_band} org_scope=${t.jacobian?.org_scope}`);
  });

  console.log(`\n── JACOBIAN ──`);
  console.log(`Condition: ${result.jacobian.conditionNumber}`);
  console.log(`${result.jacobian.interpretation}`);
  result.jacobian.blastRadii.forEach(b => {
    console.log(`  ${b.taskId}: blast=${b.blastRadius} agent=${b.agent} ring=${b.ring}`);
  });
  
  console.log(`\n── RE-PLAN THRESHOLDS ──`);
  for (const [field, info] of Object.entries(result.jacobian.rePlanThresholds || {})) {
    console.log(`  ∂T/∂${field}: max=${info.maxSensitivity} → ${info.rePlanIf}`);
  }

  console.log(`\n── DUAL-SENSITIVITY (J ∩ ToAC) ──`);

  // Run dual-sensitivity on a sample task result
  const sampleOutput = "The measured organ health is 6/6 confirmed by probe. All services are operational with average latency under 50ms. The computed federation stability index is 0.94 based on observed metrics.";
  const sampleTask = result.tasks[0] || { id: 'task-0', name: 'sample', jacobian: { risk_band: 0.3, org_scope: 0.3, time_horizon: 0.3 } };
  const ds = dualSensitivityVerify(sampleTask, sampleOutput);
  
  console.log(`  Verdict: ${ds.verdict}`);
  console.log(`  J (cognitive):  ${ds.jacobian.verdict} — max sensitivity=${ds.jacobian.maxSensitivity}`);
  console.log(`  ToAC (perceptual): ${ds.toac.verdict} — W³=${ds.toac.triWitness.W3} epistemic=${ds.toac.epistemicQuality}`);
  console.log(`  Claims: OBS=${ds.toac.claimBreakdown.obsCount} DER=${ds.toac.claimBreakdown.derCount} INT=${ds.toac.claimBreakdown.intCount} SPEC=${ds.toac.claimBreakdown.specCount}`);
  console.log(`  Intersection: ${ds.unified.intersection} — ${ds.unified.interpretation}`);

  // Run dual-sensitivity on a hallucinated sample
  const halluOutput = "The system might possibly be operational, perhaps all services are running, it could be that everything is fine based on assumed metrics which are speculated to be correct.";
  const ds2 = dualSensitivityVerify(sampleTask, halluOutput);
  console.log(`\n  Hallucination test:`);
  console.log(`  Verdict: ${ds2.verdict}`);
  console.log(`  ToAC: ${ds2.toac.verdict} — W³=${ds2.toac.triWitness.W3} epistemic=${ds2.toac.epistemicQuality} hallucinationRisk=${ds2.toac.hallucinationRisk}`);
  console.log(`  Claims: OBS=${ds2.toac.claimBreakdown.obsCount} DER=${ds2.toac.claimBreakdown.derCount} INT=${ds2.toac.claimBreakdown.intCount} SPEC=${ds2.toac.claimBreakdown.specCount}`);
  console.log(`  Intersection: ${ds2.unified.intersection} — ${ds2.unified.interpretation}`);

  console.log(`\n── SEAL ──`);
  console.log(`Receipts: ${result.receipts.length} | Seal: ${result.seal}`);
  console.log(`\nDITEMPA BUKAN DIBERI.`);
}
