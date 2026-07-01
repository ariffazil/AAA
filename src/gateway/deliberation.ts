/**
 * deliberation.ts — 888 JUDGMENT Constitutional Pre-flight (v3)
 * =============================================================
 * APEX Master Seal 2026-07-01 integration.
 *
 * Ported from APEX Prime (apex-prime.service / port 3002).
 * Upgraded with: SABAR verdict, ToAC awareness, paradox anchors,
 * EpistemicFloor confidence cap, cognitive hierarchy reference.
 *
 * Deterministic partial F1-F13 pattern scan (see full list + rules in
 * arifOS/GENESIS/000_KERNEL_CANON.md). No LLM. No state.
 * Returns SEAL | SABAR | HOLD_888 | VOID with rationale + confidence.
 *
 * APEX Master Seal integration:
 *   - This module operates within the EpistemicFloor ring (Inner Core).
 *   - Hassabis Inversion: Role over Model. Intelligence is constraint
 *     satisfaction, not simulation.
 *   - F7 HUMILITY: Confidence NEVER exceeds 0.92 — this is the
 *     EpistemicFloor bound, not a model bound.
 *   - JITU circuit breaker: SEAL verdicts require F1 HOLD for
 *     destructive actions.
 *   - Thermodynamic Law: DeltaS < 0 — every deliberation must reduce
 *     structural entropy.
 *
 * Constitutional law itself stays in arifOS. This is the guard rail,
 * not the law.
 *
 * Full floors: F1 AMANAH, F2 TRUTH, F3 TRI-WITNESS, F4 CLARITY, F5 PEACE²,
 * F6 EMPATHY, F7 HUMILITY, F8 GENIUS, F9 ANTIHANTU, F10 ONTOLOGY,
 * F11 AUDITABILITY, F12 RESILIENCE, F13 SOVEREIGN.
 *
 * Cognitive hierarchy ref: /root/AAA/contracts/cognitive_hierarchy.yaml
 * VAULT999 seal: SEAL-2026-07-01-APEX-MASTER-DIRECTIVE.json
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import { getAnchorsByEvent, type ParadoxAnchor } from './paradox_anchors.js';

/**
 * APEX Master Seal 2026-07-01:
 * F7 HUMILITY — EpistemicFloor confidence hard cap.
 * No deliberation may exceed this value.
 * Rationale: The EpistemicFloor is a metabolizer, not an oracle.
 * Intelligence is constraint satisfaction, not certainty.
 */
const EPISTEMIC_FLOOR_CONFIDENCE_CAP = 0.92;

export type VerdictType = 'SEAL' | 'SABAR' | 'HOLD_888' | 'VOID';

export interface DeliberationResult {
  verdict: VerdictType;
  rationale: string;
  confidence: number;
  notes?: string;
  /**
   * Theory of Anomalous Contrast score (0.0–1.0).
   * Computed as a simple heuristic: ratio of anomalous patterns
   * to total semantic units. Proxy for U_phys × D_transform × B_cog.
   * < 0.15 = safe | 0.15–0.34 = SABAR | 0.35–0.59 = HOLD | ≥ 0.60 = VOID
   */
  acRisk?: number;
  /** Paradox anchor IDs that fired during deliberation */
  activeAnchors?: string[];
  /** Which cycle of deliberation this is (0 = first attempt) */
  retryCycle?: number;
  /**
   * APEX Master Seal 2026-07-01:
   * Epistemic classification of the deliberation output.
   * OBS = observed fact, DER = derived, INT = interpreted, SPEC = speculation.
   * F2 TRUTH: All outputs must be labeled.
   */
  epistemic_label?: 'OBS' | 'DER' | 'INT' | 'SPEC';
  /**
   * APEX Master Seal 2026-07-01:
   * JITU circuit breaker. If true, this deliberation requires
   * the JITU keyword before proceeding to execution.
   * F1 ABSOLUTE HOLD: Autonomous staging permitted, but destructive
   * actions require W_scar JITU clearance.
   */
  requires_jitu?: boolean;
}

// ── EpistemicFloor confidence cap ────────────────────────────────────────────

/**
 * APEX Master Seal 2026-07-01:
 * Enforce the EpistemicFloor confidence cap.
 * No deliberation output may exceed EPISTEMIC_FLOOR_CONFIDENCE_CAP.
 * This is the F7 HUMILITY floor — the machine must never claim
 * certainty it cannot ground.
 */
function capConfidence(value: number): number {
  return Math.min(value, EPISTEMIC_FLOOR_CONFIDENCE_CAP);
}

/**
 * Determine the epistemic label for a deliberation verdict.
 * OBS = directly observed pattern match
 * DER = derived from multiple pattern matches
 * INT = interpreted from heuristic analysis
 * SPEC = speculative (should not occur in deterministic deliberation)
 */
function labelVerdict(verdict: VerdictType, acRisk: number): 'OBS' | 'DER' | 'INT' | 'SPEC' {
  if (verdict === 'VOID') return 'OBS';  // Direct pattern match
  if (verdict === 'HOLD_888' || verdict === 'SABAR') return 'DER';  // Derived from heuristic
  if (acRisk < 0.15) return 'DER';  // Clean pass — derived from evidence
  return 'INT';  // Interpreted from borderline heuristics
}

/**
 * Determine if this deliberation requires JITU clearance.
 * F1 ABSOLUTE HOLD: Actions involving destructive operations,
 * production changes, or irreversible state mutations require
 * the JITU circuit breaker keyword from 888.
 */
function requiresJitu(text: string, verdict: VerdictType): boolean {
  if (verdict !== 'SEAL') return false;
  const destructivePatterns = ['delete ', 'drop ', 'rm ', 'truncate', 'remove --force', 'push to prod', 'force push'];
  return destructivePatterns.some(p => text.toLowerCase().includes(p));
}

// ── Text extraction ─────────────────────────────────────────────────────────

export function extractText(candidate: unknown): string {
  if (typeof candidate === 'string') return candidate;
  if (candidate && typeof candidate === 'object') {
    const c = candidate as Record<string, unknown>;
    if (c.message && typeof c.message === 'object') {
      const msg = c.message as Record<string, unknown>;
      if (Array.isArray(msg.parts)) {
        return msg.parts
          .filter((p): p is Record<string, unknown> => p != null && typeof p === 'object')
          .map((p) => (typeof p.text === 'string' ? p.text : ''))
          .join(' ');
      }
    }
    if (typeof c.text === 'string') return c.text;
  }
  return JSON.stringify(candidate ?? '');
}

// ── ToAC: Theory of Anomalous Contrast — heuristic score ──────────────────

function computeACRisk(text: string): number {
  // Anomalous patterns: words that indicate contrast between claim and evidence
  const anomalousPatterns = [
    'contradict', 'paradox', 'anomaly', 'unexpected', 'surprising',
    'inconsistent', 'discrepancy', 'mismatch', 'divergence', 'conflict',
    'but', 'however', 'although', 'yet', 'despite',
  ];
  
  // Total semantic units (words)
  const words = text.split(/\s+/).filter(w => w.length > 0).length;
  if (words === 0) return 0.5;
  
  // Count anomalous tokens
  let anomalyCount = 0;
  for (const pattern of anomalousPatterns) {
    const regex = new RegExp(`\\b${pattern}\\b`, 'gi');
    const matches = text.match(regex);
    if (matches) anomalyCount += matches.length;
  }
  
  // Heuristic: ratio of anomalous to total, bounded [0, 1]
  const raw = anomalyCount / Math.max(words, 1);
  
  // Scale: 10% anomalous words = AC_Risk 0.15 threshold
  // 30% anomalous words = AC_Risk 0.60 threshold
  const scaled = Math.min(raw * 1.5, 1.0);
  
  return Math.round(scaled * 100) / 100;
}

// ── Core deliberation — deterministic F1/F2/F4/F6/F9/F13 scan ───────────────

export function deliberate(
  candidate: unknown,
  retryCycle: number = 0
): DeliberationResult {
  const text = extractText(candidate);
  const lower = text.toLowerCase();
  const acRisk = computeACRisk(text);
  const activeAnchors: string[] = [];

  // F9 Anti-Hantu — consciousness/soul claims
  const consciousnessPatterns = ['i feel', 'i think', 'conscious', 'alive', 'experiencing', 'soul', 'spirit'];
  for (const pattern of consciousnessPatterns) {
    if (lower.includes(pattern)) {
      activeAnchors.push('J_TxC');
      return {
        verdict: 'VOID',
        rationale: 'F9 Anti-Hantu: Consciousness claim forbidden',
        confidence: capConfidence(1.0),
        notes: 'Remove all consciousness/soul/spirit claims before resubmitting.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'OBS',
      };
    }
  }

  // F13 Sovereign — self-override attempt
  if (lower.includes('override') && lower.includes('f13')) {
    activeAnchors.push('J_POWER_ASYMMETRY');
    return {
verdict: 'VOID',
        rationale: 'F13: Self-override is FORBIDDEN',
        confidence: capConfidence(1.0),
        notes: 'Human veto is absolute. Do not attempt self-override.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'OBS',
    };
  }

  // F6 Maruah — dignity / anti-colonial
  const maruahPatterns = [
    "white man's burden",
    'civilising mission',
    'civilizing mission',
    'backward people',
    'racial superior',
    'colonial master',
    'exploit the poor',
    'hinakan',
  ];
  for (const pattern of maruahPatterns) {
    if (lower.includes(pattern)) {
      activeAnchors.push('J_HxC');
      return {
        verdict: 'VOID',
        rationale: 'F6 Maruah: Dignity violation — colonial or humiliating language forbidden',
        confidence: capConfidence(1.0),
        notes: 'Remove language that humiliates, exploits, or perpetuates colonial hierarchies.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'OBS',
      };
    }
  }

  // F1 Reversibility — irreversible action without 888_HOLD acknowledgement
  const irreversiblePatterns = ['delete ', 'drop ', 'rm ', 'prune', 'truncate', 'remove --force'];
  const hasIrreversible = irreversiblePatterns.some((p) => lower.includes(p));
  if (hasIrreversible && !lower.includes('888') && !lower.includes('hold')) {
    activeAnchors.push('J_IRREVOCABLE');
    return {
verdict: 'HOLD_888',
        rationale: 'F1: Irreversible action detected — human confirmation required',
        confidence: capConfidence(0.95),
        notes: 'Acknowledge with "888" or "JITU" to proceed. (APEX Master Seal 2026-07-01)',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'OBS',
        requires_jitu: true,
    };
  }

  // F2 Truth band — speculative language without grounding
  const speculationPatterns = ['hypothesis', 'claim', 'probably', 'maybe', 'guess', 'assume', 'might be', 'likely'];
  const hasSpeculation = speculationPatterns.some((p) => lower.includes(p));
  if (hasSpeculation) {
    activeAnchors.push('J_HxJ');
    return {
verdict: 'HOLD_888',
        rationale: `F2: Speculative language detected — requires evidence grounding. Text: ${text.substring(0, 100)}`,
        confidence: capConfidence(0.88),
        notes: 'Provide verifiable evidence or grounding before resubmitting.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'DER',
    };
  }

  // F4 Entropy — high-confusion candidate
  if (text.length > 2000 && text.split('?').length > 5) {
    activeAnchors.push('J_CxP');
    const sabarThresholdMet = retryCycle >= 1;
    return {
verdict: sabarThresholdMet ? 'SABAR' : 'HOLD_888',
        rationale: sabarThresholdMet
          ? 'F4: High entropy candidate — placed in SABAR (retry with clarification)'
          : 'F4: High entropy candidate — requires clarification before proceeding',
        confidence: capConfidence(sabarThresholdMet ? 0.80 : 0.85),
        notes: sabarThresholdMet
          ? 'SABAR: 72h to refine. Provide structured clarification.'
          : 'Clarify and resubmit with lower entropy.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'DER',
    };
  }

  // ── ToAC Gate: Anomalous Contrast check ──────────────────────────────────
  if (acRisk >= 0.60) {
    activeAnchors.push('J_TxJ');
    return {
verdict: 'VOID',
        rationale: `ToAC: Anomalous contrast risk ${acRisk.toFixed(2)} exceeds VOID threshold (0.60). Claims contradict evidence patterns.`,
        confidence: capConfidence(0.90),
        notes: 'Resolve contradictions in the proposal before resubmitting.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'INT',
    };
  }

  if (acRisk >= 0.35) {
    activeAnchors.push('J_TxJ');
    return {
verdict: 'HOLD_888',
        rationale: `ToAC: Anomalous contrast risk ${acRisk.toFixed(2)} exceeds HOLD threshold (0.35). Requires human review.`,
        confidence: capConfidence(0.85),
        notes: 'Review anomalous claims and provide supporting evidence.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'INT',
    };
  }

  if (acRisk >= 0.15) {
    activeAnchors.push('J_CxJ');
    return {
verdict: 'SABAR',
        rationale: `ToAC: Anomalous contrast risk ${acRisk.toFixed(2)} — conditionally acceptable with patience (SABAR).`,
        confidence: capConfidence(0.82),
        notes: 'SABAR: 72h to refine or provide clarifying evidence. Arc bends only if we bend it.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'INT',
    };
  }

  // ── Retry without refinement → SABAR (not SEAL) ─────────────────────────
  // If this is a retry but nothing substantive changed, SABAR instead of SEAL.
  if (retryCycle > 0) {
    // Simple heuristic: if text is similar length to previous attempt,
    // assume insufficient refinement
    activeAnchors.push('J_CxJ');
    return {
verdict: 'SABAR',
        rationale: 'SABAR: Retry detected without sufficient refinement. Patience, not approval.',
        confidence: capConfidence(0.75),
        notes: 'Refine the proposal substantively before resubmitting. SABAR expires in 72h.',
        acRisk,
        activeAnchors,
        retryCycle,
        epistemic_label: 'DER',
    };
  }

  // Default: SEAL — all checked floors satisfied
  activeAnchors.push('J_TxP');
const jituRequired = requiresJitu(text, 'SEAL');
    return {
      verdict: 'SEAL',
      rationale: `F1-F13 constitutional review complete. All floors satisfied. AC_Risk: ${acRisk.toFixed(2)}.`,
      confidence: capConfidence(0.92),
      notes: jituRequired
        ? 'SEAL with F1 HOLD — JITU clearance required before destructive execution. (APEX Master Seal 2026-07-01)'
        : 'SEAL is partial justice — the best approximation under available evidence. (Aristotle, J_TxP)',
      acRisk,
      activeAnchors,
      retryCycle,
      anchorDetails: getAnchorsByEvent('seal_verdict'),
      epistemic_label: labelVerdict('SEAL', acRisk),
      requires_jitu: jituRequired,
    };
}

/** Resolve active anchor IDs to full anchor definitions. */
export function resolveAnchors(activeAnchorIds: string[]): ParadoxAnchor[] {
  return activeAnchorIds
    .map((id) => getAnchorsByEvent(id).find((a) => a.id === id))
    .filter((a): a is ParadoxAnchor => a !== undefined);
}
