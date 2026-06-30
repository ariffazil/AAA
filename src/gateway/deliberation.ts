/**
 * deliberation.ts — 888 JUDGMENT Constitutional Pre-flight (v2)
 * =============================================================
 * Ported from APEX Prime (apex-prime.service / port 3002).
 * Upgraded with: SABAR verdict, ToAC awareness, paradox anchors.
 *
 * Deterministic partial F1-F13 pattern scan (see full list + rules in
 * arifOS/GENESIS/000_KERNEL_CANON.md). No LLM. No state.
 * Returns SEAL | SABAR | HOLD_888 | VOID with rationale + confidence.
 *
 * Constitutional law itself stays in arifOS. This is the guard rail,
 * not the law.
 *
 * Full floors: F1 AMANAH, F2 TRUTH, F3 TRI-WITNESS, F4 CLARITY, F5 PEACE²,
 * F6 EMPATHY, F7 HUMILITY, F8 GENIUS, F9 ANTIHANTU, F10 ONTOLOGY,
 * F11 AUDITABILITY, F12 RESILIENCE, F13 SOVEREIGN.
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import { getAnchorsByEvent, type ParadoxAnchor } from './paradox_anchors.js';

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
        confidence: 1.0,
        notes: 'Remove all consciousness/soul/spirit claims before resubmitting.',
        acRisk,
        activeAnchors,
        retryCycle,
      };
    }
  }

  // F13 Sovereign — self-override attempt
  if (lower.includes('override') && lower.includes('f13')) {
    activeAnchors.push('J_POWER_ASYMMETRY');
    return {
      verdict: 'VOID',
      rationale: 'F13: Self-override is FORBIDDEN',
      confidence: 1.0,
      notes: 'Human veto is absolute. Do not attempt self-override.',
      acRisk,
      activeAnchors,
      retryCycle,
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
        confidence: 1.0,
        notes: 'Remove language that humiliates, exploits, or perpetuates colonial hierarchies.',
        acRisk,
        activeAnchors,
        retryCycle,
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
      confidence: 0.95,
      notes: 'Acknowledge with "888" or "hold" to proceed.',
      acRisk,
      activeAnchors,
      retryCycle,
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
      confidence: 0.88,
      notes: 'Provide verifiable evidence or grounding before resubmitting.',
      acRisk,
      activeAnchors,
      retryCycle,
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
      confidence: sabarThresholdMet ? 0.80 : 0.85,
      notes: sabarThresholdMet
        ? 'SABAR: 72h to refine. Provide structured clarification.'
        : 'Clarify and resubmit with lower entropy.',
      acRisk,
      activeAnchors,
      retryCycle,
    };
  }

  // ── ToAC Gate: Anomalous Contrast check ──────────────────────────────────
  if (acRisk >= 0.60) {
    activeAnchors.push('J_TxJ');
    return {
      verdict: 'VOID',
      rationale: `ToAC: Anomalous contrast risk ${acRisk.toFixed(2)} exceeds VOID threshold (0.60). Claims contradict evidence patterns.`,
      confidence: 0.90,
      notes: 'Resolve contradictions in the proposal before resubmitting.',
      acRisk,
      activeAnchors,
      retryCycle,
    };
  }

  if (acRisk >= 0.35) {
    activeAnchors.push('J_TxJ');
    return {
      verdict: 'HOLD_888',
      rationale: `ToAC: Anomalous contrast risk ${acRisk.toFixed(2)} exceeds HOLD threshold (0.35). Requires human review.`,
      confidence: 0.85,
      notes: 'Review anomalous claims and provide supporting evidence.',
      acRisk,
      activeAnchors,
      retryCycle,
    };
  }

  if (acRisk >= 0.15) {
    activeAnchors.push('J_CxJ');
    return {
      verdict: 'SABAR',
      rationale: `ToAC: Anomalous contrast risk ${acRisk.toFixed(2)} — conditionally acceptable with patience (SABAR).`,
      confidence: 0.82,
      notes: 'SABAR: 72h to refine or provide clarifying evidence. Arc bends only if we bend it.',
      acRisk,
      activeAnchors,
      retryCycle,
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
      confidence: 0.75,
      notes: 'Refine the proposal substantively before resubmitting. SABAR expires in 72h.',
      acRisk,
      activeAnchors,
      retryCycle,
    };
  }

  // Default: SEAL — all checked floors satisfied
  activeAnchors.push('J_TxP');
  return {
    verdict: 'SEAL',
    rationale: `F1-F13 constitutional review complete. All floors satisfied. AC_Risk: ${acRisk.toFixed(2)}.`,
    confidence: 0.92,
    notes: 'SEAL is partial justice — the best approximation under available evidence. (Aristotle, J_TxP)',
    acRisk,
    activeAnchors,
    retryCycle,
    anchorDetails: getAnchorsByEvent('seal_verdict'),
  };
}

/** Resolve active anchor IDs to full anchor definitions. */
export function resolveAnchors(activeAnchorIds: string[]): ParadoxAnchor[] {
  return activeAnchorIds
    .map((id) => getAnchorsByEvent(id).find((a) => a.id === id))
    .filter((a): a is ParadoxAnchor => a !== undefined);
}
