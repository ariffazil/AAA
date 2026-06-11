/**
 * AGENT STATE — Constitutional Agent State Machine
 * 
 * AAA is not a swarm. AAA is the state that makes swarms lawful.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 * 
 * Every agent must be: registered, manifested, contextualized, leased, audited.
 * No agent may act merely because it exists.
 * 
 * @module agent-state/schemas
 */

// ── Enums ─────────────────────────────────────────────────────────────

const AGENT_CLASSES = [
  'router', 'clerk', 'judge', 'forge', 'geox', 'wealth', 'well',
  'gateway', 'observer', 'worker', 'architect', 'auditor', 'agent'
];

const AGENT_STATES = [
  'UNBORN', 'CLAIMED', 'REGISTERED', 'MANIFESTED', 'ATTESTED',
  'CONTEXT_BOUND', 'LEASED', 'ACTIVE',
  'DEGRADED', 'SUSPENDED', 'COMPLETED', 'REVOKED',
  'SEALED', 'DEAD'
];

const HEALTH_STATUSES = ['cold', 'warming', 'active', 'degraded', 'suspended', 'revoked', 'dead'];

const STATUS_ALIGNMENT = ['ALIGNED', 'OVERCLAIM', 'UNDERCLAIM', 'UNKNOWN', 'DEAD'];

const CAPABILITY_STATES = ['UNATTESTED', 'STATIC_CLAIM', 'OBSERVED', 'TESTED', 'LIVE_ATTESTED', 'REVOKED'];

const RISK_TIERS = ['low', 'medium', 'high', 'atomic'];

const EXECUTION_MODES = ['ASSIST', 'MIXED', 'AGI_CHAIN'];

/**
 * VALID TRANSITIONS in the Agent State Machine.
 * 
 * UNBORN → CLAIMED → REGISTERED → MANIFESTED → ATTESTED
 *   → CONTEXT_BOUND → LEASED → ACTIVE
 *   → (DEGRADED | SUSPENDED | COMPLETED | REVOKED)
 *   → SEALED → DEAD
 */
const VALID_TRANSITIONS = {
  UNBORN:           ['CLAIMED'],
  CLAIMED:          ['REGISTERED', 'REVOKED'],
  REGISTERED:       ['MANIFESTED', 'REVOKED'],
  MANIFESTED:       ['ATTESTED', 'REGISTERED', 'REVOKED'],
  ATTESTED:         ['CONTEXT_BOUND', 'REVOKED'],
  CONTEXT_BOUND:    ['LEASED', 'SUSPENDED', 'REVOKED'],
  LEASED:           ['ACTIVE', 'SUSPENDED', 'REVOKED'],
  ACTIVE:           ['DEGRADED', 'SUSPENDED', 'COMPLETED', 'REVOKED'],
  DEGRADED:         ['ACTIVE', 'SUSPENDED', 'REVOKED'],
  SUSPENDED:        ['ACTIVE', 'REVOKED', 'SEALED'],
  COMPLETED:        ['SEALED'],
  REVOKED:          ['SEALED'],
  SEALED:           ['DEAD'],
  DEAD:             [],  // Terminal — resurrection requires explicit RESURRECT event
};

// ── 1. AGENT STATE — the full 13-field canonical object ─────────────

/**
 * @typedef {Object} IdentityBlock
 * @property {string} claimed_by
 * @property {boolean} verified
 * @property {string} verification_method — signature | vault_seal | runtime_attestation | none
 */

/**
 * @typedef {Object} BodyBlock
 * @property {string} runtime   — local | cloud | mcp | api | browser | shell | swarm
 * @property {string} model     — gpt | claude | local | deterministic_service
 * @property {string} host
 * @property {?number} process_id
 */

/**
 * @typedef {Object} ManifestBlock
 * @property {string} declared_purpose
 * @property {string[]} declared_capabilities
 * @property {string[]} declared_tools
 * @property {string[]} declared_limits
 * @property {string} version
 * @property {string} hash — sha256
 */

/**
 * @typedef {Object} CapabilityAttestationBlock
 * @property {string} status  — UNATTESTED | STATIC_CLAIM | LIVE_ATTESTED | REVOKED
 * @property {string[]} evidence
 * @property {?string} last_checked_at
 */

/**
 * @typedef {Object} ContextBlock
 * @property {string} context_id
 * @property {string} mission
 * @property {string[]} scope
 * @property {string[]} forbidden_context
 * @property {string[]} memory_window
 * @property {Object[]} evidence_bundle
 */

/**
 * @typedef {Object} LeaseBlock
 * @property {string} lease_id
 * @property {string} authority_granter
 * @property {string[]} allowed_actions
 * @property {string[]} forbidden_actions
 * @property {string} expires_at — ISO 8601
 * @property {boolean} revocable
 * @property {string} status — active | expired | revoked
 */

/**
 * @typedef {Object} PolicyBlock
 * @property {string[]} floors_bound
 * @property {string} risk_tier — low | medium | high | atomic
 * @property {boolean} requires_human_ack
 */

/**
 * @typedef {Object} HealthBlock
 * @property {string} status — cold | warming | active | degraded | suspended | revoked | dead
 * @property {?string} heartbeat_at — ISO 8601
 * @property {?string} error_state
 */

/**
 * @typedef {Object} AuditBlock
 * @property {string} vault_chain  — VAULT999
 * @property {Object[]} events
 * @property {?string} last_seal
 */

/**
 * @typedef {Object} TerminationBlock
 * @property {boolean} kill_switch
 * @property {?string} revocation_reason
 * @property {boolean} postmortem_required
 */

// ── 2. CONTEXT PACKET — the bounded working world ──────────────────

/**
 * @typedef {Object} ContextPacket
 * @property {string} context_id
 * @property {string} mission
 * @property {string} actor — who asked
 * @property {string} authority — who can approve
 * @property {string} domain  — geology | capital | governance | code | health | legal
 * @property {Object[]} evidence
 * @property {string[]} memory_scope
 * @property {string[]} forbidden_memory
 * @property {string} risk_level — low | medium | high | atomic
 * @property {Object} output_requirements
 * @property {string} created_at — ISO 8601
 * @property {string} expires_at — ISO 8601
 * @property {string} status — active | expired | revoked
 */

// ── 3. FEDERATION GRAPH — how agents relate ────────────────────────

/** @type {Object<string, string>} */
const EDGE_RULES = {
  may_delegate:  'Agent may delegate subtasks to the target',
  may_observe:   'Agent may read target state/output',
  may_execute:   'Agent may trigger target actions',
  may_escalate:  'Agent may forward decisions to target',
  may_revoke:    'Agent may revoke target authority',
  may_seal:      'Agent may write to VAULT999 on target behalf',
};

/**
 * @typedef {Object} FederationEdge
 * @property {string} from
 * @property {string} to
 * @property {string[]} rules  — may_delegate | may_observe | may_execute | may_escalate | may_revoke | may_seal
 * @property {string} note
 */

/**
 * @typedef {Object} FederationGraph
 * @property {Object.<string, string[]>} structure  — organ → [agent_ids]
 * @property {FederationEdge[]} edges
 * @property {Object.<string, Object>} organ_roles
 */

// ── 4. POLICY ENGINE — minimum gates ───────────────────────────────

const POLICY_GATES = [
  'identity_gate',
  'context_gate',
  'lease_gate',
  'capability_gate',
  'risk_gate',
  'memory_gate',
  'tool_gate',
  'external_boundary_gate',
  'audit_gate',
  'human_sovereignty_gate',
];

/**
 * Evaluate all policy gates for a proposed action.
 * @typedef {Object} PolicyResult
 * @property {boolean} allowed
 * @property {string} verdict — SEAL | HOLD | VOID
 * @property {string[]} failed_gates
 * @property {string} reason
 */

// ── 5. VAULT999 EVENTS ─────────────────────────────────────────────

const VAULT_EVENTS = [
  'AGENT_REGISTERED',
  'MANIFEST_SUBMITTED',
  'CAPABILITY_ATTESTED',
  'CONTEXT_ATTACHED',
  'LEASE_GRANTED',
  'ACTION_PROPOSED',
  'ACTION_EXECUTED',
  'LEASE_REVOKED',
  'AGENT_SUSPENDED',
  'AGENT_RETIRED',
  'SESSION_SEALED',
  'AGENT_RESURRECTED',
];

// ── 6. AAA INVARIANTS — the 13 laws ────────────────────────────────

const AAA_INVARIANTS = [
  'No anonymous agent.',
  'No action without context.',
  'No tool use without lease.',
  'No capability trusted from self-claim alone.',
  'No memory used as authority without provenance.',
  'No external IO without Gateway.',
  'No machine mutation without Forge boundary.',
  'No irreversible action without Arif approval.',
  'No agent may self-approve its own escalation.',
  'No context may silently expand.',
  'No agent identity may be reused after revocation without resurrection seal.',
  'No public claim without evidence state: CLAIM, HYPOTHESIS, VERIFIED, UNKNOWN.',
  'No intelligence without audit.',
];

// ── 7. AAA OPERATING MODEL ─────────────────────────────────────────

/**
 * AAA = SOVEREIGN INTELLIGENCE STATE
 * 
 * Constitution    → arifOS floors (F1-F13)
 * Civil Registry  → Agent Registry
 * Passport        → Agent Manifest
 * Work Permit     → Lease
 * Territory       → Context
 * Border Control  → Gateway
 * Judiciary       → Judge
 * Treasury        → WEALTH
 * Geological      → GEOX
 * Health          → WELL
 * Public Archive  → VAULT999
 * Killswitch      → Revocation Engine
 * Census          → Agent Inventory
 * Military/Eng    → FORGE (under lease only)
 */

// ── Exports ─────────────────────────────────────────────────────────

module.exports = {
  AGENT_CLASSES,
  AGENT_STATES,
  HEALTH_STATUSES,
  STATUS_ALIGNMENT,
  CAPABILITY_STATES,
  RISK_TIERS,
  EXECUTION_MODES,
  VALID_TRANSITIONS,
  EDGE_RULES,
  POLICY_GATES,
  VAULT_EVENTS,
  AAA_INVARIANTS,
};
