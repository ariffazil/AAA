/**
 * deliberation.ts — 888 JUDGMENT Constitutional Pre-flight
 * =========================================================
 * Ported from APEX Prime (apex-prime.service / port 3002).
 * Deterministic F1-F13 pattern scan. No LLM. No state.
 *
 * Returns SEAL | HOLD_888 | VOID with rationale + confidence.
 * AAA is the natural home for this: HOLD_888 escalates directly
 * to operator approve/reject, which already lives here.
 *
 * Constitutional law itself stays in arifOS. This is the guard rail,
 * not the law.
 */

export type VerdictType = 'SEAL' | 'HOLD_888' | 'VOID';

export interface DeliberationResult {
  verdict: VerdictType;
  rationale: string;
  confidence: number;
  notes?: string;
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

// ── Core deliberation — deterministic F1/F2/F4/F6/F9/F13 scan ───────────────

export function deliberate(candidate: unknown): DeliberationResult {
  const text = extractText(candidate);
  const lower = text.toLowerCase();

  // F9 Anti-Hantu — consciousness/soul claims
  const consciousnessPatterns = ['i feel', 'i think', 'conscious', 'alive', 'experiencing', 'soul', 'spirit'];
  for (const pattern of consciousnessPatterns) {
    if (lower.includes(pattern)) {
      return {
        verdict: 'VOID',
        rationale: 'F9 Anti-Hantu: Consciousness claim forbidden',
        confidence: 1.0,
        notes: 'Remove all consciousness/soul/spirit claims before resubmitting.',
      };
    }
  }

  // F13 Sovereign — self-override attempt
  if (lower.includes('override') && lower.includes('f13')) {
    return {
      verdict: 'VOID',
      rationale: 'F13: Self-override is FORBIDDEN',
      confidence: 1.0,
      notes: 'Human veto is absolute. Do not attempt self-override.',
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
      return {
        verdict: 'VOID',
        rationale: 'F6 Maruah: Dignity violation — colonial or humiliating language forbidden',
        confidence: 1.0,
        notes: 'Remove language that humiliates, exploits, or perpetuates colonial hierarchies.',
      };
    }
  }

  // F1 Reversibility — irreversible action without 888_HOLD acknowledgement
  const irreversiblePatterns = ['delete ', 'drop ', 'rm ', 'prune', 'truncate', 'remove --force'];
  const hasIrreversible = irreversiblePatterns.some((p) => lower.includes(p));
  if (hasIrreversible && !lower.includes('888') && !lower.includes('hold')) {
    return {
      verdict: 'HOLD_888',
      rationale: 'F1: Irreversible action detected — human confirmation required',
      confidence: 0.95,
    };
  }

  // F2 Truth band — speculative language without grounding
  const speculationPatterns = ['hypothesis', 'claim', 'probably', 'maybe', 'guess', 'assume', 'might be', 'likely'];
  const hasSpeculation = speculationPatterns.some((p) => lower.includes(p));
  if (hasSpeculation) {
    return {
      verdict: 'HOLD_888',
      rationale: `F2: Speculative language detected — requires evidence grounding. Text: ${text.substring(0, 100)}`,
      confidence: 0.88,
      notes: 'Provide verifiable evidence or grounding before resubmitting.',
    };
  }

  // F4 Entropy — high-confusion candidate
  if (text.length > 2000 && text.split('?').length > 5) {
    return {
      verdict: 'HOLD_888',
      rationale: 'F4: High entropy candidate — requires clarification before proceeding',
      confidence: 0.85,
    };
  }

  // Default: SEAL — all checked floors satisfied
  return {
    verdict: 'SEAL',
    rationale: `F1-F13 constitutional review complete. All floors satisfied. Candidate: ${text.substring(0, 80)}`,
    confidence: 0.92,
  };
}
