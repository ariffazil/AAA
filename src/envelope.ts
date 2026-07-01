/**
 * arifOS Federation Metabolism Envelope — TypeScript Type Definitions
 * ==========================================================================
 * The one canonical blood packet every organ must use to talk to every other organ.
 * Converts 7 separate repositories into one governed metabolic loop.
 *
 * Usage:
 *   import { FederationEnvelope, sabahBasinEnvelope, validateEnvelope } from './envelope';
 *
 *   const envelope = sabahBasinEnvelope();
 *   const errors = validateEnvelope(envelope);
 *   if (errors.length > 0) throw new Error(`Envelope validation failed: ${errors.join(', ')}`);
 *
 * DITEMPA BUKAN DIBERI — Forged by FORGE (000Ω), 2026-07-01.
 */

// ─── Enums ──────────────────────────────────────────────────────────────────

export type Organ =
  | 'arifOS'
  | 'AAA'
  | 'A-FORGE'
  | 'GEOX'
  | 'WEALTH'
  | 'WELL'
  | 'VAULT999'
  | 'ariffazil';

export type EvidenceLayer =
  | 'OBSERVED'
  | 'DERIVED'
  | 'INTERPRETED'
  | 'SPECULATED'
  | 'UNKNOWN';

export type AutonomyBand =
  | 'T1_AUTO'
  | 'T2_ANNOUNCE'
  | 'T3_888_HOLD'
  | 'F13_SOVEREIGN';

export type ReversibilityClass =
  | 'FULL'
  | 'PARTIAL'
  | 'NONE'
  | 'UNKNOWN';

export type RiskClass =
  | 'LOW'
  | 'MEDIUM'
  | 'HIGH'
  | 'CRITICAL';

export type ExecutionStatus =
  | 'PENDING'
  | 'ROUTING'
  | 'DELIBERATING'
  | 'APPROVED'
  | 'EXECUTING'
  | 'COMPLETED'
  | 'FAILED'
  | 'ROLLED_BACK'
  | 'HOLD';

export type F13Verdict =
  | 'JITU'
  | 'HOLD'
  | 'SABAR'
  | 'VOID';

export type Floor =
  | 'F1'   // AMANAH
  | 'F2'   // TRUTH
  | 'F3'   // TRI_WITNESS
  | 'F4'   // CLARITY
  | 'F5'   // PEACE
  | 'F6'   // MARUAH
  | 'F7'   // HUMILITY
  | 'F8'   // LAW
  | 'F9'   // ANTI_HANTU
  | 'F10'  // ONTOLOGY
  | 'F11'  // AUDIT
  | 'F12'  // RESILIENCE
  | 'F13'; // SOVEREIGN

// ─── Organ Payloads ─────────────────────────────────────────────────────────

export interface GEOXPayload {
  claim_id?: string;
  evidence_summary?: string;
  confidence?: number;  // 0–0.9
  physics_invariants?: string[];
}

export interface WEALTHPayload {
  npv?: number;
  risk_score?: number;  // 0–1
  capital_class?: string;
  wisdom_dimensions?: Record<string, unknown>;
}

export interface WELLPayload {
  readiness_color?: 'GREEN' | 'YELLOW' | 'RED' | 'STALE';
  fatigue_level?: number;  // 0–1
  dignity_preservation?: number;  // 0–1
  recommendation?: 'PROCEED' | 'SIMPLIFY' | 'HOLD' | 'INJECT_NEEDED';
}

export interface AAAPayload {
  route?: string[];
  display_state?: string;
  warga_boundary_check?: boolean;
}

export interface ArifOSPayload {
  verdict?: 'SEAL' | 'HOLD' | 'SABAR' | 'VOID' | 'PARTIAL';
  g_score?: number;  // 0–1
  violated_floors?: string[];
  judge_reasoning?: string;
}

export interface AForgePayload {
  execution_id?: string;
  dry_run_result?: string;
  execution_result?: string;
  rollback_available?: boolean;
}

export interface VAULT999Payload {
  seal_id?: string;
  seal_hash?: string;
  sealed_at?: string;  // ISO 8601
  witness_count?: number;
}

export interface OrganPayloads {
  GEOX?: GEOXPayload;
  WEALTH?: WEALTHPayload;
  WELL?: WELLPayload;
  AAA?: AAAPayload;
  arifOS?: ArifOSPayload;
  'A-FORGE'?: AForgePayload;
  VAULT999?: VAULT999Payload;
}

// ─── Route Entry ────────────────────────────────────────────────────────────

export interface OrganRouteEntry {
  organ: string;
  received_at: string;  // ISO 8601
  processed_at?: string;
  verdict?: 'PROCESSED' | 'DELEGATED' | 'HOLD' | 'REJECTED';
  notes?: string;
}

// ─── Main Envelope ──────────────────────────────────────────────────────────

export interface FederationEnvelope {
  /** Unique trace identifier. Survives across organ boundaries. */
  trace_id: string;

  /** The agent or human initiating this metabolic cycle. */
  actor_id: string;

  /** The organ that originated this envelope. */
  organ_origin: Organ;

  /** The organ this envelope is addressed to. */
  organ_target: Organ;

  /** The chain of organs this envelope has passed through. Append-only. */
  organ_route: OrganRouteEntry[];

  /** Natural-language description of what the metabolic cycle intends to accomplish. */
  intent: string;

  /** Epistemic grounding of the evidence. F2 TRUTH binding. */
  evidence_layer: EvidenceLayer;

  /** The autonomy tier governing this action. */
  autonomy_band: AutonomyBand;

  /** Can this action be rolled back? F1 AMANAH binding. */
  reversibility_class: ReversibilityClass;

  /** Blast radius assessment. */
  risk_class: RiskClass;

  /** Which constitutional floors must be verified. */
  required_floor_checks: Floor[];

  /** The action being proposed or executed. */
  proposed_action: {
    action_type: string;
    parameters?: Record<string, unknown>;
    constraints?: string[];
  };

  /** Current execution state. */
  execution_status: ExecutionStatus;

  /** Quantitative or qualitative result of the action. */
  measurement_result?: {
    value?: unknown;
    unit?: string;
    confidence?: number;
    method?: string;
    evidence_refs?: string[];
  };

  /** VAULT999 seal ID if this cycle has been sealed. */
  vault_receipt_reference?: string;

  /** Does this action require explicit F13 sovereign approval? */
  f13_required_boolean: boolean;

  /** The sovereign's verdict. Only populated by Arif. */
  f13_verdict?: F13Verdict;

  /** Per-organ payloads attached during the metabolic cycle. */
  organ_payloads: OrganPayloads;

  /** Operational metadata. */
  metadata?: {
    created_at?: string;
    updated_at?: string;
    ttl_seconds?: number;
    priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    tags?: string[];
    correlation_id?: string;
  };
}

// ─── Validation ─────────────────────────────────────────────────────────────

export function validateEnvelope(envelope: FederationEnvelope): string[] {
  const errors: string[] = [];

  // Hard rules
  if (envelope.f13_required_boolean && envelope.autonomy_band !== 'T3_888_HOLD' && envelope.autonomy_band !== 'F13_SOVEREIGN') {
    errors.push('HARD_RULE: f13_required_boolean=true but autonomy_band is not T3_888_HOLD or F13_SOVEREIGN');
  }

  if (envelope.reversibility_class === 'NONE' && (envelope.risk_class === 'HIGH' || envelope.risk_class === 'CRITICAL')) {
    errors.push('HARD_RULE: Irreversible action with HIGH/CRITICAL risk. Requires F13 sovereign approval.');
  }

  if (envelope.execution_status === 'COMPLETED' && !envelope.vault_receipt_reference) {
    errors.push('HARD_RULE: Execution completed but no vault_receipt_reference. Must seal before completing.');
  }

  if (!envelope.required_floor_checks.includes('F13') && envelope.f13_required_boolean) {
    errors.push('HARD_RULE: f13_required_boolean=true but F13 not in required_floor_checks.');
  }

  if (envelope.organ_payloads?.VAULT999?.seal_id && !envelope.vault_receipt_reference) {
    errors.push('HARD_RULE: VAULT999 payload has seal_id but vault_receipt_reference is empty.');
  }

  if (envelope.organ_origin === 'ariffazil') {
    errors.push('HARD_RULE: ariffazil is the sovereign surface, not an organ. Cannot originate envelopes.');
  }

  return errors;
}

// ─── Pre-built Scenarios ────────────────────────────────────────────────────

export function sabahBasinEnvelope(): FederationEnvelope {
  return {
    trace_id: crypto.randomUUID(),
    actor_id: 'ARIF_FAZIL',
    organ_origin: 'GEOX',
    organ_target: 'WEALTH',
    organ_route: [],
    intent: 'Assess Sabah Basin opportunity/risk — subsurface viability, capital consequence, operator readiness',
    evidence_layer: 'OBSERVED',
    autonomy_band: 'F13_SOVEREIGN',
    reversibility_class: 'FULL',
    risk_class: 'MEDIUM',
    required_floor_checks: ['F1', 'F2', 'F4', 'F6', 'F8', 'F11', 'F13'],
    proposed_action: {
      action_type: 'basin_opportunity_assessment',
      parameters: {
        basin: 'Sabah',
        assessment_type: 'full_metabolic_loop',
        organs_involved: ['GEOX', 'WEALTH', 'WELL', 'AAA', 'arifOS', 'A-FORGE', 'VAULT999'],
      },
    },
    execution_status: 'PENDING',
    f13_required_boolean: true,
    organ_payloads: {},
    metadata: {
      created_at: new Date().toISOString(),
      priority: 'HIGH',
      tags: ['sabah_basin', 'metabolic_loop', 'end_to_end_test'],
      correlation_id: 'SABAH-BASIN-001',
    },
  };
}

// ─── Stamp helper ───────────────────────────────────────────────────────────

export function stampRoute(
  envelope: FederationEnvelope,
  organ: string,
  verdict: 'PROCESSED' | 'DELEGATED' | 'HOLD' | 'REJECTED' = 'PROCESSED',
  notes?: string,
): FederationEnvelope {
  const now = new Date().toISOString();
  envelope.organ_route.push({
    organ,
    received_at: now,
    processed_at: now,
    verdict,
    notes,
  });
  return envelope;
}