/**
 * AREP Types — Arif Reality Engineering Protocol
 * ════════════════════════════════════════════════════════
 *
 * TypeScript type definitions for the AREP task contract.
 * Extends A2A v1.0 Task with reality engineering layers.
 * Used by the AAA cockpit to display delegation chains,
 * evidence floors, reality gates, and autonomy bands.
 *
 * Coined by Muhammad Arif bin Fazil (F13 SOVEREIGN), 2026-06-04.
 * Forged by Omega (DeepSeek V4 Pro) under F13 directive.
 *
 * DITEMPA BUKAN DIBERI
 */

import type { TaskState } from './schema';

// ── Reality Layers (AgenticReality model) ──────────────────────────

export type RealityLayer = 'GROUND_TRUTH' | 'VERIFIED_STATE' | 'CACHED_STATE' | 'INFERRED';

export const REALITY_LAYER_HIERARCHY: Record<RealityLayer, number> = {
  GROUND_TRUTH:    0,  // Sealed in VAULT999 — indisputable
  VERIFIED_STATE:  1,  // Live health probe — current truth
  CACHED_STATE:    2,  // From memory — may be stale
  INFERRED:        3,  // Agent reasoning — unverified
};

export interface RealityLayerDefinition {
  description: string;
  arifos_anchor: string;
  verification_method: string;
  staleness_threshold_seconds?: number;
  example: string;
}

// ── Intent (the only layer the human touches) ──────────────────────

export interface AREPIntent {
  statement: string;
  success_criteria: string[];
  failure_modes?: string[];
  context_tags?: string[];
}

// ── Principal ──────────────────────────────────────────────────────

export interface AREPPrincipal {
  actor_id: 'arif-fazil';
  ratification_mode: 'implicit' | '888_HOLD' | 'explicit_ack';
  sovereign_signature?: string;
}

// ── Reality Constraints ────────────────────────────────────────────

export interface RealityGate {
  condition: string;
  action_on_fail: 'HALT' | 'ESCALATE' | 'RETRY' | 'SKIP';
  evidence_layer?: RealityLayer;
}

export interface ModelIdentityConstraint {
  allowed_providers?: string[];
  required_capabilities?: string[];
  self_claim_boundary: 'verified_only';
}

export interface ReversibilityConstraint {
  maximum_action_class: 'OBSERVE' | 'PREPARE' | 'MUTATE' | 'ATOMIC';
  rollback_plan_required: boolean;
  irreversible_ack_required: boolean;
}

export interface RealityConstraints {
  evidence_floor: RealityLayer;
  reality_gates?: RealityGate[];
  autonomy_band: AutonomyBand;
  model_identity_constraint?: ModelIdentityConstraint;
  reversibility?: ReversibilityConstraint;
}

// ── Autonomy Bands ─────────────────────────────────────────────────

export type AutonomyBand = 'GREEN' | 'YELLOW' | 'ORANGE' | 'RED' | 'BLACK';

export const AUTONOMY_BAND_DESCRIPTIONS: Record<AutonomyBand, string> = {
  GREEN:   'Full autonomy — execute and report',
  YELLOW:  'Proceed but log every action',
  ORANGE:  'Pre-authorization required for MUTATE',
  RED:     'Human approval required for all actions',
  BLACK:   'Fully blocked — no execution permitted',
};

// ── Delegation Chain (Huawei attenuation model) ────────────────────

export type DelegationRole = 'PRINCIPAL' | 'KERNEL' | 'PRIMARY_AGENT' | 'SUB_AGENT' | 'TOOL';

export interface DelegationLink {
  actor_id: string;
  role: DelegationRole;
  scope: string;
  grant_id?: string;
  lease_seconds: number;       // 0 = permanent (principal only)
  max_subagent_depth: number;  // remaining delegation hops
}

// ── Constitutional Binding ─────────────────────────────────────────

export type FloorVeto = {
  floor: string;
  reason: string;
  timestamp: string;
};

export type GovernanceVerdict = 'SEAL' | 'SABAR' | 'HOLD' | 'VOID' | 'PENDING';

export interface ConstitutionalBinding {
  active_floors: string[];
  floor_vetoes?: FloorVeto[];
  governance_verdict: GovernanceVerdict;
}

// ── Task Lifecycle (A2A extension) ─────────────────────────────────

export interface LifecycleStateTransition {
  state: TaskState;
  timestamp: string;
  actor_id?: string;
  evidence_layer_at_transition?: RealityLayer;
  note?: string;
}

export interface TaskArtifact {
  artifact_id: string;
  artifact_type: 'code' | 'config' | 'seal' | 'report' | 'health_probe' | 'registry_entry';
  evidence_layer: RealityLayer;
  vault_seal_hash?: string;
}

export interface TaskLifecycle {
  current_state: TaskState;
  state_history: LifecycleStateTransition[];
  artifacts?: TaskArtifact[];
  a2a_task_id?: string;
  parent_task_id?: string;
}

// ── Telemetry ──────────────────────────────────────────────────────

export interface AREPTelemetry {
  task_id: string;
  created_at: string;
  updated_at: string;
  estimated_tokens?: number;
  actual_tokens?: number;
  model_used?: string;
  agent_shell?: 'opencode' | 'claude-code' | 'continue-cli' | 'hermes' | 'openclaw';
  session_id?: string;
}

// ── THE CANONICAL AREP TASK ────────────────────────────────────────

export interface AREPTask {
  arep_version: '1.0';
  intent: AREPIntent;
  principal: AREPPrincipal;
  reality_constraints: RealityConstraints;
  reality_layers?: Record<RealityLayer, RealityLayerDefinition>;
  delegation_chain: DelegationLink[];
  task_lifecycle: TaskLifecycle;
  constitutional_binding: ConstitutionalBinding;
  telemetry: AREPTelemetry;
}

// ── Cockpit Display Helpers ────────────────────────────────────────

/** Returns the current evidence layer as a human-readable badge label. */
export function realityLayerBadge(layer: RealityLayer): { label: string; color: string } {
  const map: Record<RealityLayer, { label: string; color: string }> = {
    GROUND_TRUTH:    { label: 'SEALED',   color: '#1a1a2e' },  // dark — final
    VERIFIED_STATE:  { label: 'VERIFIED', color: '#0d9488' },  // teal — trustworthy
    CACHED_STATE:    { label: 'CACHED',   color: '#f59e0b' },  // amber — needs refresh
    INFERRED:        { label: 'INFERRED', color: '#6b7280' },  // gray — unverified
  };
  return map[layer];
}

/** Returns the autonomy band as a human-readable badge. */
export function autonomyBandBadge(band: AutonomyBand): { label: string; color: string } {
  const map: Record<AutonomyBand, { label: string; color: string }> = {
    GREEN:   { label: 'AUTO',   color: '#16a34a' },
    YELLOW:  { label: 'LOG',    color: '#f59e0b' },
    ORANGE:  { label: 'ASK',    color: '#f97316' },
    RED:     { label: 'HUMAN',  color: '#dc2626' },
    BLACK:   { label: 'BLOCKED', color: '#000000' },
  };
  return map[band];
}

/** Validates that an evidence layer meets or exceeds the required floor. */
export function evidenceLayerMeetsFloor(current: RealityLayer, required: RealityLayer): boolean {
  return REALITY_LAYER_HIERARCHY[current] <= REALITY_LAYER_HIERARCHY[required];
}
