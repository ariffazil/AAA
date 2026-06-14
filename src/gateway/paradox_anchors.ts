/**
 * paradox_anchors.ts — 11 Paradox Anchors for AAA Deliberation
 * =============================================================
 * Ported from arifOS judge.py JUDGE_PARADOX_ANCHORS (3×3 orthogonal matrix
 * + 2 extra anchors). Each anchor is a verified philosophical invariant
 * that fires at specific verdict decision points.
 *
 * These are NOT LLM prompts. They are deterministic constitutional
 * invariants — the philosophy IS the algorithm.
 *
 * Source: arifOS/arifosmcp/tools/judge.py — JUDGE_PARADOX_ANCHORS
 * Theory: arifOS/static/arifos/theory/000/APEX_THEORY.md
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

export interface ParadoxAnchor {
  id: string;
  matrixCell: string;
  matrixRow: string;
  matrixCol: string;
  mottoBinding: string;
  quote: {
    text: string;
    author: string;
    work: string;
    year: string;
    verificationLevel: string;
  };
  antithesis: string;
  axis: string;
  binding: {
    event: string;
    trigger: string;
    effect: string;
  };
  severityOnFire: string;
  riskBias: string;
  authorityScope: string;
  norm: string;
}

// ── TRUTH ROW ───────────────────────────────────────────────────────

export const J_TxC: ParadoxAnchor = {
  id: 'J_TxC',
  matrixCell: 'truth_care',
  matrixRow: 'TRUTH',
  matrixCol: 'CARE',
  mottoBinding: 'DIKAJI, BUKAN DISUAPI',
  quote: {
    text: 'If it is not right, do not do it; if it is not true, do not say it.',
    author: 'Marcus Aurelius',
    work: 'Meditations',
    year: 'c. 170–180 CE',
    verificationLevel: 'traditional_attribution',
  },
  antithesis: 'Rightness and truth are not always visible in the moment of decision — sometimes what is right can only be known after the action is taken.',
  axis: 'ex ante clarity vs. ex post knowledge',
  binding: {
    event: 'irreversible_action_gate',
    trigger: 'irreversible-action gate — if not sure it\'s right, HOLD',
    effect: 'hard_requirement',
  },
  severityOnFire: 'hard_gate',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'WAJIB',
};

export const J_TxP: ParadoxAnchor = {
  id: 'J_TxP',
  matrixCell: 'truth_peace',
  matrixRow: 'TRUTH',
  matrixCol: 'PEACE',
  mottoBinding: 'DIJELASKAN, BUKAN DIKABURKAN',
  quote: {
    text: 'In justice is every virtue comprehended.',
    author: 'Aristotle',
    work: 'Nicomachean Ethics 1129b29–30',
    year: '4th century BCE',
    verificationLevel: 'verified_exact',
  },
  antithesis: 'No single verdict can comprehend every virtue simultaneously — every SEAL is partial justice, the best approximation under available evidence.',
  axis: 'comprehensiveness vs. decidability',
  binding: {
    event: 'seal_verdict',
    trigger: 'SEAL verdict — audit bundle annotation',
    effect: 'annotate_seal_as_partial_justice',
  },
  severityOnFire: 'warn',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'WAJIB',
};

export const J_TxJ: ParadoxAnchor = {
  id: 'J_TxJ',
  matrixCell: 'truth_justice',
  matrixRow: 'TRUTH',
  matrixCol: 'JUSTICE',
  mottoBinding: 'DISEDARKAN, BUKAN DIYAKINKAN',
  quote: {
    text: 'About the just and the unjust… we should consider not what the many but what the man who knows shall say to us — that single man and the truth.',
    author: 'Plato',
    work: 'Republic I, 340e–341a',
    year: 'c. 375 BCE',
    verificationLevel: 'verified_exact',
  },
  antithesis: 'The expert alone cannot hold sovereignty — without the many, the expert becomes a tyrant. Wisdom lives in the contradiction.',
  axis: 'expert knowledge vs. democratic wisdom',
  binding: {
    event: 'verdict_disputed',
    trigger: 'Disagreement between human and AI witnesses — expert vs. collective',
    effect: 'log_tension',
  },
  severityOnFire: 'warn',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'WAJIB',
};

// ── CLARITY ROW ─────────────────────────────────────────────────────

export const J_CxC: ParadoxAnchor = {
  id: 'J_CxC',
  matrixCell: 'clarity_care',
  matrixRow: 'CLARITY',
  matrixCol: 'CARE',
  mottoBinding: 'DIURUTKAN, BUKAN DICAMPURKAN',
  quote: {
    text: 'Ethical reasoning requires not only knowing the good but ordering the soul toward it.',
    author: 'Socrates',
    work: 'Phaedrus, 247c–e',
    year: 'c. 370 BCE',
    verificationLevel: 'traditional_attribution',
  },
  antithesis: 'Ordering the soul takes time — but the world demands decisions before we are ready. Clarity emerges in action as much as in contemplation.',
  axis: 'inner readiness vs. external demand',
  binding: {
    event: 'clarity_gate_before_verdict',
    trigger: 'candidate text has high entropy or confusion signals',
    effect: 'apply_clarity_check',
  },
  severityOnFire: 'advisory',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'SUNAT',
};

export const J_CxP: ParadoxAnchor = {
  id: 'J_CxP',
  matrixCell: 'clarity_peace',
  matrixRow: 'CLARITY',
  matrixCol: 'PEACE',
  mottoBinding: 'DIKOSONGKAN, BUKAN DIPENUHKAN',
  quote: {
    text: 'In the beginner\'s mind there are many possibilities, but in the expert\'s there are few.',
    author: 'Shunryu Suzuki',
    work: 'Zen Mind, Beginner\'s Mind',
    year: '1970',
    verificationLevel: 'traditional_attribution',
  },
  antithesis: 'The beginner cannot act — only the expert has enough certainty to move. Indefinite openness is paralysis.',
  axis: 'epistemic humility vs. decisive action',
  binding: {
    event: 'high_entropy_detected',
    trigger: 'candidate text > 2000 chars and > 5 questions — F4 entropy gate',
    effect: 'recommend_clarification',
  },
  severityOnFire: 'advisory',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'SUNAT',
};

export const J_CxJ: ParadoxAnchor = {
  id: 'J_CxJ',
  matrixCell: 'clarity_justice',
  matrixRow: 'CLARITY',
  matrixCol: 'JUSTICE',
  mottoBinding: 'DIJAGA, BUKAN DIPAKSAKAN',
  quote: {
    text: 'The arc of the moral universe is long, but it bends toward justice.',
    author: 'Theodore Parker / Martin Luther King Jr.',
    work: 'MLK, "Where Do We Go From Here?" (1967) / Parker, "Justice" Sermon (1853)',
    year: '1853 / 1967',
    verificationLevel: 'traditional_attribution',
  },
  antithesis: 'The arc does not bend by itself. SABAR without deadline is abdication. Patience must carry a deadline, or it is just delay masquerading as wisdom.',
  axis: 'patience vs. urgency',
  binding: {
    event: 'sabar_verdict',
    trigger: 'SABAR verdict — must carry deadline, cannot be indefinite',
    effect: 'enforce_sabar_deadline',
  },
  severityOnFire: 'hard_gate',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'WAJIB',
};

// ── HUMILITY ROW ───────────────────────────────────────────────────

export const J_HxC: ParadoxAnchor = {
  id: 'J_HxC',
  matrixCell: 'humility_care',
  matrixRow: 'HUMILITY',
  matrixCol: 'CARE',
  mottoBinding: 'DIRASAKAN, BUKAN DIFIKIRKAN',
  quote: {
    text: 'The heart has its reasons which reason knows nothing of.',
    author: 'Blaise Pascal',
    work: 'Pensées, 277',
    year: '1670',
    verificationLevel: 'verified_exact',
  },
  antithesis: 'The heart can deceive as surely as the mind. Emotion without reason is as dangerous as reason without emotion.',
  axis: 'rational analysis vs. embodied intuition',
  binding: {
    event: 'heart_critique_engaged',
    trigger: 'When 666_HEART critique diverges from 333_MIND reason',
    effect: 'log_tension',
  },
  severityOnFire: 'advisory',
  riskBias: 'balanced',
  authorityScope: 'judge',
  norm: 'SUNAT',
};

export const J_HxP: ParadoxAnchor = {
  id: 'J_HxP',
  matrixCell: 'humility_peace',
  matrixRow: 'HUMILITY',
  matrixCol: 'PEACE',
  mottoBinding: 'DITERIMA, BUKAN DIPERTIKAIKAN',
  quote: {
    text: 'There is no greatness where there is not simplicity, goodness, and truth.',
    author: 'Leo Tolstoy',
    work: 'War and Peace, Epilogue',
    year: '1869',
    verificationLevel: 'traditional_attribution',
  },
  antithesis: 'Complexity is not greatness, but neither is naivety. The refusal to question is not peace — it is surrender.',
  axis: 'trusting acceptance vs. skeptical vigilance',
  binding: {
    event: 'overclaim_detected',
    trigger: 'A-RIF claim strength exceeds evidence level',
    effect: 'downgrade_verdict',
  },
  severityOnFire: 'hard_gate',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'WAJIB',
};

export const J_HxJ: ParadoxAnchor = {
  id: 'J_HxJ',
  matrixCell: 'humility_justice',
  matrixRow: 'HUMILITY',
  matrixCol: 'JUSTICE',
  mottoBinding: 'DIKEMBALIKAN, BUKAN DIAMBIL',
  quote: {
    text: 'I know that I know nothing.',
    author: 'Socrates (Plato)',
    work: 'Apology, 21d',
    year: 'c. 399 BCE',
    verificationLevel: 'verified_exact',
  },
  antithesis: 'The claim to know nothing is itself a claim to know something. Paradox is inescapable — the only honest response is to act with full awareness of uncertainty.',
  axis: 'acknowledged ignorance vs. paralysis',
  binding: {
    event: 'humility_band_violation',
    trigger: 'Ω₀ (baseline epistemic uncertainty) outside [0.03, 0.05] band',
    effect: 'adjust_confidence',
  },
  severityOnFire: 'warn',
  riskBias: 'conservative',
  authorityScope: 'judge',
  norm: 'WAJIB',
};

// ── EXTRA ANCHORS (not in 3×3 matrix) ──────────────────────────────

export const J_IRREVOCABLE: ParadoxAnchor = {
  id: 'J_IRREVOCABLE',
  matrixCell: 'extra_irreversible',
  matrixRow: 'EXTRA',
  matrixCol: 'ACTION',
  mottoBinding: 'JANGAN SESAL, KALAU SUDAH TERLANJUR',
  quote: {
    text: 'Waste no more time arguing what a good man should be. Be one.',
    author: 'Marcus Aurelius',
    work: 'Meditations, 10.16',
    year: 'c. 170–180 CE',
    verificationLevel: 'verified_exact',
  },
  antithesis: '"Be one" is itself an irreversible action. Every irreversible act was once a choice. The gate must stop the ones that cannot be undone.',
  axis: 'decisive virtue vs. irreversible consequence',
  binding: {
    event: 'irreversible_action_gate',
    trigger: 'F1 check — irreversible action without 888_HOLD acknowledgment',
    effect: 'hard_requirement',
  },
  severityOnFire: 'hard_gate',
  riskBias: 'ultra_conservative',
  authorityScope: 'judge',
  norm: 'HARAM',
};

export const J_POWER_ASYMMETRY: ParadoxAnchor = {
  id: 'J_POWER_ASYMMETRY',
  matrixCell: 'extra_power',
  matrixRow: 'EXTRA',
  matrixCol: 'SOVEREIGNTY',
  mottoBinding: 'DIHORMATI, BUKAN DIRENDAHKAN',
  quote: {
    text: 'Those who hold the power to judge must be judged by the same law.',
    author: 'Glaucon (Plato)',
    work: 'Republic II, 359b–360d',
    year: 'c. 375 BCE',
    verificationLevel: 'verified_exact',
  },
  antithesis: 'The sovereign judges — but who judges the sovereign? Paradox: the final authority cannot also be the final accountability. Trust is the only bridge.',
  axis: 'absolute authority vs. checkable power',
  binding: {
    event: 'sovereign_action',
    trigger: 'F13 override — sovereign action with receipt',
    effect: 'log_sovereign_audit',
  },
  severityOnFire: 'audit',
  riskBias: 'conservative',
  authorityScope: 'observer',
  norm: 'WAJIB',
};

// ── Master list ─────────────────────────────────────────────────────

export const ALL_PARADOX_ANCHORS: ParadoxAnchor[] = [
  J_TxC, J_TxP, J_TxJ,
  J_CxC, J_CxP, J_CxJ,
  J_HxC, J_HxP, J_HxJ,
  J_IRREVOCABLE,
  J_POWER_ASYMMETRY,
];

export function getAnchorById(id: string): ParadoxAnchor | undefined {
  return ALL_PARADOX_ANCHORS.find(a => a.id === id);
}

export function getAnchorsByEvent(event: string): ParadoxAnchor[] {
  return ALL_PARADOX_ANCHORS.filter(a => a.binding.event === event);
}

export function getAnchorsBySeverity(severity: string): ParadoxAnchor[] {
  return ALL_PARADOX_ANCHORS.filter(a => a.severityOnFire === severity);
}
