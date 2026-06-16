/**
 * Federation Envelope Validator — A2A Bridge
 * ═══════════════════════════════════════════════════════════════
 *
 * Mirrors the Python FederationEnvelope validation from
 * arifosmcp/schemas/federation_envelope.py for the Node.js A2A server.
 *
 * Hard rules:
 *   - No envelope + MUTATE/ATOMIC → HOLD
 *   - Legacy wrap ceiling = T2 (OBSERVE + PREPARE only)
 *   - Authority must be verified for MUTATE/ATOMIC
 *   - Receipts required: MUTATE needs observe, ATOMIC needs arif_ack
 *
 * DITEMPA BUKAN DIBERI
 */

'use strict';

// ── Risk Tier Constants ─────────────────────────────────────────────
const RISK_TIERS = ['T0', 'T1', 'T2', 'T3', 'T4', 'T5'];
const ACTION_CLASSES = ['OBSERVE', 'PREPARE', 'MUTATE', 'ATOMIC'];
const AUTHORITY_SOURCES = ['token', 'session', 'delegated', 'human_888', 'fallback', 'unknown'];

// ── Canonical Tool Risk Map (mirrors risk_classifier.py) ────────────
const CANONICAL_TOOL_RISKS = {
  'arif_forge_execute':       { tier: 'T5', action_class: 'ATOMIC' },
  'arif_judge_deliberate':    { tier: 'T5', action_class: 'ATOMIC' },
  'arif_vault_seal':          { tier: 'T5', action_class: 'ATOMIC' },
  'arif_heart_critique':      { tier: 'T5', action_class: 'ATOMIC' },
  'arif_session_init':        { tier: 'T5', action_class: 'ATOMIC' },
  'arif_kernel_route':        { tier: 'T3', action_class: 'MUTATE' },
  'arif_gateway_connect':     { tier: 'T3', action_class: 'MUTATE' },
  'arif_memory_recall':       { tier: 'T3', action_class: 'MUTATE' },
  'arif_mind_reason':         { tier: 'T2', action_class: 'PREPARE' },
  'arif_evidence_fetch':      { tier: 'T2', action_class: 'PREPARE' },
  'arif_sense_observe':       { tier: 'T1', action_class: 'OBSERVE' },
  'arif_ops_measure':         { tier: 'T1', action_class: 'OBSERVE' },
  'arif_reply_compose':       { tier: 'T1', action_class: 'OBSERVE' },
};

// ── Extract envelope from request params ────────────────────────────
function extractEnvelope(params) {
  if (!params || typeof params !== 'object') return null;

  // 1. Try nested envelope
  if (params.envelope && typeof params.envelope === 'object') {
    return params.envelope;
  }

  // 2. Try flattened fields
  const hasFlat = ['actor_id', 'session_id', 'trace_id', 'authority', 'risk']
    .some(k => params[k] !== undefined);
  if (!hasFlat) return null;

  return {
    trace_id: params.trace_id || `auto-${Date.now()}`,
    actor_id: params.actor_id || 'anonymous',
    session_id: params.session_id || 'unknown',
    agent_id: params.agent_id || null,
    tool_id: params.tool_id || null,
    organ: params.organ || 'arifOS',
    niat: params.niat || null,
    matlamat: params.matlamat || null,
    authority: params.authority || { source: 'fallback' },
    risk: params.risk || { tier: 'T0', action_class: 'OBSERVE' },
    receipts: params.receipts || {},
    legacy_wrap: true,
    // Structural Coherence Transmission — EUREKA v2026.06.05
    // Governance architecture is signal compression. Envelopes that carry
    // explicit structural_coherence markers survive cross-modal transfer.
    structural_coherence: params.structural_coherence || {
      cross_modal_stability: 0.50,
      semantic_density_score: 0.30,
      dim_spot_flag: false,
      note: 'Legacy wrap — structural coherence not verified.',
    },
  };
}

// ── Wrap legacy call (no envelope provided) ─────────────────────────
function wrapLegacyCall(toolName) {
  const toolRisk = CANONICAL_TOOL_RISKS[toolName] || { tier: 'T0', action_class: 'OBSERVE' };
  return {
    envelope_version: '1.0',
    trace_id: `legacy-${Date.now()}`,
    actor_id: 'anonymous',
    session_id: 'unknown',
    tool_id: toolName,
    organ: 'arifOS',
    authority: { source: 'fallback', verified: false },
    risk: {
      tier: toolRisk.action_class === 'MUTATE' ? 'T2' : toolRisk.tier,
      action_class: toolRisk.action_class,
      blast_radius: 'local',
      reversibility: 'high',
      secret_touch: 'none',
      external_effect: 'none',
    },
    receipts: {},
    legacy_wrap: true,
    // Structural Coherence Transmission — EUREKA v2026.06.05
    // Legacy calls have low structural coherence because they lack explicit
    // governance grammar. They are more vulnerable to cross-modal corruption.
    structural_coherence: {
      cross_modal_stability: 0.30,
      semantic_density_score: 0.20,
      dim_spot_flag: true,
      note: 'Legacy wrap — governance grammar not explicitly encoded. Signal may degrade in modality transfer.',
    },
  };
}

// ── Validate envelope for execution ─────────────────────────────────
function validateEnvelope(envelope, toolName) {
  const result = { ok: false, reason: '', envelope, action_taken: 'HOLD' };

  // 1. Tool risk classification and envelope upgrade
  const toolRisk = CANONICAL_TOOL_RISKS[toolName] || { tier: 'T0', action_class: 'OBSERVE' };
  const envRisk = envelope.risk || { tier: 'T0', action_class: 'OBSERVE' };

  if (envRisk.action_class === 'OBSERVE' && toolRisk.action_class !== 'OBSERVE') {
    envRisk.action_class = toolRisk.action_class;
    envRisk.tier = toolRisk.tier;
  }

  // 2. Legacy wrap policy: ceiling = T2 (PREPARE max)
  const acl = envRisk.action_class;
  if (envelope.legacy_wrap) {
    if (acl === 'MUTATE' || acl === 'ATOMIC') {
      result.reason = `LEGACY_WRAP cannot execute ${acl} on ${toolName}. Upgrade client to send FederationEnvelope with verified authority.`;
      return result;
    }
    // For legacy, enforce T2 ceiling even if tool says higher
    const tierIdx = RISK_TIERS.indexOf(envRisk.tier);
    const t2Idx = RISK_TIERS.indexOf('T2');
    if (tierIdx > t2Idx) {
      envRisk.tier = 'T2';
      envRisk.action_class = 'PREPARE';
    }
  }

  // 3. Identity check
  // FALLBACK policy: anonymous allowed for OBSERVE/PREPARE (Green/Yellow bands)
  // MUTATE/ATOMIC requires real identity
  const isAnonymous = !envelope.actor_id || envelope.actor_id === 'anonymous';
  const isUnknownSession = !envelope.session_id || envelope.session_id === 'unknown';

  if (isAnonymous && (acl === 'MUTATE' || acl === 'ATOMIC')) {
    result.reason = 'MUTATE/ATOMIC requires identified actor_id';
    return result;
  }
  if (isUnknownSession && (acl === 'MUTATE' || acl === 'ATOMIC')) {
    result.reason = 'MUTATE/ATOMIC requires identified session_id';
    return result;
  }

  // 4. Authority check for mutating actions
  const auth = envelope.authority || { source: 'unknown' };
  if ((acl === 'MUTATE' || acl === 'ATOMIC') &&
      (auth.source === 'unknown' || auth.source === 'fallback')) {
    result.reason = `${acl} requires verified authority. Send AuthorityEnvelope with source=token|session|delegated|human_888.`;
    return result;
  }

  // 5. Receipt check
  const receipts = envelope.receipts || {};
  if (acl === 'MUTATE' && !receipts.observe_receipt_id) {
    result.reason = 'MUTATE requires observe_receipt_id (observe-before-mutate)';
    return result;
  }
  if (acl === 'ATOMIC' && !receipts.arif_ack_id) {
    result.reason = 'ATOMIC requires arif_ack_id (F13 sovereign approval)';
    return result;
  }

  // 6. Risk ceiling check
  const ceiling = envRisk.risk_ceiling || null;
  if (ceiling) {
    const tierIdx = RISK_TIERS.indexOf(envRisk.tier);
    const ceilIdx = RISK_TIERS.indexOf(ceiling);
    if (tierIdx > ceilIdx) {
      result.reason = `Risk ${envRisk.tier} exceeds ceiling ${ceiling}`;
      return result;
    }
  }

  // 7. Delegation expiry check
  if (auth.delegator && auth.expires_at) {
    const now = Date.now();
    const expiry = new Date(auth.expires_at).getTime();
    if (now > expiry) {
      result.reason = 'Delegation expired';
      return result;
    }
  }

  // 7.5 Phase 4: Biometric Pacing (WELL Organ Telemetry)
  try {
    const fs = require('fs');
    const WELL_STATE_PATH = '/root/WELL/state.json';
    if (fs.existsSync(WELL_STATE_PATH)) {
      const wellState = JSON.parse(fs.readFileSync(WELL_STATE_PATH, 'utf8'));
      const wellScore = wellState.well_score || 100;
      const fatigue = wellState.metrics?.decision_fatigue || 0;
      const cogLoad = wellState.metrics?.cognitive_load || 0;

      // If vitality is low (entropy is high), throttle non-critical execution
      if (wellScore < 50 || fatigue > 0.7 || cogLoad > 0.85) {
        const tierIdx = RISK_TIERS.indexOf(envRisk.tier);
        // Only allow OBSERVE (T0/T1). Block T2+ (PREPARE/MUTATE/ATOMIC).
        if (tierIdx >= 2) {
          result.reason = `WELL_BIOMETRIC_PACING: Sovereign entropy critical (well_score=${wellScore}, fatigue=${fatigue}). Task blocked to protect metabolic capacity. Proceed manually if WAJIB.`;
          return result;
        }
      }
    }
  } catch (err) {
    // Fail open if WELL organ is unreachable
  }

  // 8. Agent Policy check (GAP-E: forged 2026-06-09 by Ω)
  // Every agent must have a registered policy. Default: DENY ALL.
  const policyResult = validateAgentPolicy(envelope, toolName);
  if (!policyResult.ok) {
    result.reason = policyResult.reason;
    return result;
  }

  // Structural Coherence check — EUREKA v2026.06.05
  // Envelopes with dim_spot_flag=true have negative constraints that may not
  // survive cross-modal transfer. Warn but do not block.
  const sc = envelope.structural_coherence || {};
  if (sc.dim_spot_flag === true && result.ok) {
    result.reason = 'SEAL_WITH_DIM_SPOT';
    result.structural_coherence_warning = (
      'STRUCTURAL_COHERENCE_ALERT: This envelope carries negative constraints ' +
      '(VOID, absence, dim spots) that have LOW cross-modal fidelity. ' +
      'If this task flows through image, audio, or external protocols, ' +
      'the absence may be lost. Re-encode with explicit positive governance markers.'
    );
  }

  result.ok = true;
  result.reason = result.reason || 'SEAL';
  result.action_taken = acl;
  return result;
}

// ── Middleware factory ──────────────────────────────────────────────
function createEnvelopeValidator(options = {}) {
  const { requireEnvelope = false, logFn = console.log } = options;

  return function envelopeMiddleware(req, res, next) {
    const params = req.body?.params || req.body || {};
    const toolName = params.tool_name || params.tool || req.path;

    let envelope = extractEnvelope(params);
    if (!envelope) {
      envelope = wrapLegacyCall(toolName);
    }

    const result = validateEnvelope(envelope, toolName);

    // Attach to request for downstream use
    req.federationEnvelope = result.envelope;
    req.envelopeValidation = result;

    if (!result.ok) {
      logFn(`[ENVELOPE HOLD] ${toolName}: ${result.reason}`);
      return res.status(403).json({
        jsonrpc: '2.0',
        id: req.body?.id || 0,
        error: {
          code: -32001,
          message: `888_HOLD: ${result.reason}`,
          data: { tool: toolName, actor_id: envelope.actor_id },
        },
      });
    }

    next();
  };
}

// ── Agent Policy Registry (GAP-E: forged 2026-06-09 by Ω) ──────────
// Mirrors arifOS AgentPolicy Pydantic model. Maps MXC SandboxPolicy
// concept onto AAA federation envelope validation.
// Default: DENY ALL — agents must be explicitly registered with policy.

const AGENT_POLICIES = new Map();

function registerAgentPolicy(agentId, policy) {
  const p = {
    agent_id: agentId,
    agent_role: policy.agent_role || 'observer',
    allowed_tools: policy.allowed_tools || [],
    denied_tools: policy.denied_tools || [],
    allowed_organs: policy.allowed_organs || [],
    irreversibility_threshold: policy.irreversibility_threshold || 0.5,
    network_posture: policy.network_posture || 'ALLOWLIST',
    allowed_domains: policy.allowed_domains || [],
    max_tokens_per_call: policy.max_tokens_per_call || 100000,
    max_runtime_seconds: policy.max_runtime_seconds || 3600,
    policy_version: policy.policy_version || '1.0.0-forge',
  };
  AGENT_POLICIES.set(agentId, p);
  return p;
}

function getAgentPolicy(agentId) {
  return AGENT_POLICIES.get(agentId) || null;
}

function validateAgentPolicy(envelope, toolName) {
  const agentId = envelope.actor_id;
  if (!agentId || agentId === 'anonymous') {
    // No agent = no policy = fallback to legacy wrap behavior
    return { ok: true, reason: 'NO_POLICY_LEGACY_FALLBACK' };
  }

  const policy = getAgentPolicy(agentId);
  if (!policy) {
    // Registered agent without policy = DENY ALL (MXC default-deny)
    return { ok: false, reason: `Agent ${agentId} has no registered policy — DENY ALL` };
  }

  // Check denied tools (explicit block)
  if (policy.denied_tools.includes(toolName)) {
    return { ok: false, reason: `${toolName} is explicitly DENIED for agent ${agentId}` };
  }

  // Check allowed tools (explicit allow)
  if (policy.allowed_tools.length > 0 && !policy.allowed_tools.includes(toolName)) {
    return { ok: false, reason: `${toolName} not in allowed_tools for agent ${agentId}` };
  }

  // Check risk tier against irreversibility threshold
  const toolRisk = CANONICAL_TOOL_RISKS[toolName] || { tier: 'T0', action_class: 'OBSERVE' };
  const riskTierNum = RISK_TIERS.indexOf(toolRisk.tier);
  if (riskTierNum >= 3 && policy.irreversibility_threshold < 0.3) {
    return { ok: false, reason: `T${riskTierNum} tool exceeds irreversibility threshold for agent ${agentId}` };
  }

  return { ok: true, reason: 'POLICY_PASS' };
}

// Seed federation agents with policies
registerAgentPolicy('omega-forge', {
  agent_role: 'engineer',
  allowed_tools: ['arif_sense_observe', 'arif_ops_measure', 'arif_mind_reason', 'arif_memory_recall',
                   'arif_evidence_fetch', 'arif_heart_critique', 'arif_forge_execute', 'arif_vault_seal',
                   'arif_judge_deliberate', 'arif_session_init', 'arif_reply_compose'],
  allowed_organs: ['arifOS', 'GEOX', 'WEALTH', 'WELL', 'A-FORGE', 'AAA'],
  irreversibility_threshold: 0.8,
});

registerAgentPolicy('hermes-asi', {
  agent_role: 'relay',
  allowed_tools: ['arif_sense_observe', 'arif_ops_measure', 'arif_memory_recall', 'arif_reply_compose'],
  allowed_organs: ['arifOS'],
  irreversibility_threshold: 0.2,
});

// ── Exports ─────────────────────────────────────────────────────────
module.exports = {
  extractEnvelope,
  wrapLegacyCall,
  validateEnvelope,
  createEnvelopeValidator,
  CANONICAL_TOOL_RISKS,
  RISK_TIERS,
  ACTION_CLASSES,
  // Agent Policy (GAP-E)
  registerAgentPolicy,
  getAgentPolicy,
  validateAgentPolicy,
  AGENT_POLICIES,
};
