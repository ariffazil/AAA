/**
 * Membrane Middleware — ZEN-ALL v0.3
 * ═══════════════════════════════════════════════════════════════
 *
 * Ω-PLANE ONLY (H3 2026-07-25): shape / envelope / transport humility.
 * This middleware VALIDATES message shape and constitutional *grammar*.
 * It does NOT compute kernel G, does NOT replace arif_judge, does NOT
 * issue sovereign SEAL authority. Display and wire checks only.
 *
 * Express middleware for AAA :3001 A2A gateway.
 * Every cross-organ message MUST pass through this membrane.
 *
 * Enforces (shape, not ontology):
 *   - Perception tagging (OBS/DER/INT/SPEC)
 *   - Verdict grammar (SEAL/HOLD/SABAR/VOID/UNKNOWN) as wire labels
 *   - Receipt lineage (hash chain reference)
 *   - C_dark threshold check when field present (F9 filter, not G-fold)
 *   - Tri-witness field presence (F3 shape)
 *   - Floor id tokens present when claimed
 *
 * Constitutional G: arif_think(mode='apex') only.
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

'use strict';

const crypto = require('crypto');
const fs = require('fs');

// ── Constants ────────────────────────────────────────────────────────
const MEMBRANE_VERSION = '0.3';
const C_DARK_THRESHOLD = 0.30;
const SEAL_CHAIN = '/root/.local/share/arifos/vault999/seal_chain.jsonl';
const LOG_FILE = '/root/.local/share/arifos/membrane-crossings.jsonl';

const VERDICTS = ['SEAL', 'HOLD', 'SABAR', 'VOID', 'UNKNOWN'];
const UNCERTAINTIES = ['OBS', 'DER', 'INT', 'SPEC'];
const ACTION_CLASSES = ['OBSERVE', 'ANALYZE', 'DRAFT', 'MUTATE', 'EXTERNAL_SIDE_EFFECT', 'IRREVERSIBLE'];
const FLOORS = ['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13'];
const ORGANS = ['arifOS', 'A-FORGE', 'GEOX', 'WEALTH', 'WELL', 'AAA', 'VAULT999', 'HERMES', 'OPENCLAW', 'OPENCODE'];

const UNCERTAINTY_CAPS = { OBS: 0.90, DER: 0.85, INT: 0.75, SPEC: 0.60 };

// ── Helpers ──────────────────────────────────────────────────────────
function generateLineageId() {
  const ts = Date.now().toString(36);
  const rand = crypto.createHash('sha256').update(`${Date.now()}-${Math.random()}`).digest('hex').slice(0, 8);
  return `mem-${ts}-${rand}`;
}

function getLastSealSeq() {
  try {
    if (!fs.existsSync(SEAL_CHAIN)) return null;
    const lines = fs.readFileSync(SEAL_CHAIN, 'utf-8').trim().split('\n');
    const last = JSON.parse(lines[lines.length - 1]);
    return last.seq ?? null;
  } catch {
    return null;
  }
}

function appendLog(entry) {
  try {
    const dir = require('path').dirname(LOG_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(LOG_FILE, JSON.stringify(entry) + '\n');
  } catch { /* best-effort */ }
}

function classifyPerception(text) {
  if (!text) return 'INT';
  // A2A message object: extract text from parts array
  if (typeof text === 'object' && text.parts && Array.isArray(text.parts)) {
    text = text.parts.map(p => (typeof p === 'string' ? p : p.text || '')).join(' ');
  }
  if (typeof text !== 'string') return 'INT';
  const t = text.toLowerCase();
  if (t.match(/\b(measured|observed|recorded|detected|found|data shows|the log)\b/)) return 'OBS';
  if (t.match(/\b(calculated|computed|derived|extrapolated|estimated)\b/)) return 'DER';
  if (t.match(/\b(interpreted|synthesized|reasoned|inferred|concluded)\b/)) return 'INT';
  if (t.match(/\b(speculated|hypothetical|might|could|possibly|perhaps)\b/)) return 'SPEC';
  return 'INT';
}

function classifyAction(text) {
  if (!text) return 'OBSERVE';
  if (typeof text === 'object' && text.parts && Array.isArray(text.parts)) {
    text = text.parts.map(p => (typeof p === 'string' ? p : p.text || '')).join(' ');
  }
  if (typeof text !== 'string') return 'OBSERVE';
  const t = text.toLowerCase();
  if (t.match(/\b(delete|remove|drop|destroy|purge|wipe)\b/)) return 'IRREVERSIBLE';
  if (t.match(/\b(deploy|push|publish|send|execute|run|apply)\b/)) return 'MUTATE';
  if (t.match(/\b(write|create|edit|update|modify|change)\b/)) return 'DRAFT';
  if (t.match(/\b(analyze|compare|evaluate|assess|review)\b/)) return 'ANALYZE';
  return 'OBSERVE';
}

// ════════════════════════════════════════════════════════════════════════
// ATLAS333 COGNITIVE WIRE — Layer v0.1 (2026-08-05)
// ════════════════════════════════════════════════════════════════════════
// JS mirror of atlas.py ΛΘΦ functions. Deterministic regex + lookup tables.
// Zero IPC overhead. <5ms per message. F1 fail-safe — never blocks.
//
// The Cognitive Wire classifies every cross-organ message through ATLAS333
// and records paradox activations to a persistent ledger. When a paradox
// appears in 3+ distinct sessions, EUREKA777 fires a candidate alert.
//
// Nightly drift check: Python Φ() runs against this JS mirror via
// scripts/cognitive_wire_drift_check.py — flags divergence.

// ── ATLAS333 Constants ────────────────────────────────────────────────
const PARADOX_LEDGER = '/root/.local/share/arifos/atlas333/membrane_paradox_ledger.jsonl';

// Demand tensors: Lane → {τ, κ, ρ} — exact mirror of atlas.py Θ()
const DEMAND_TENSORS = {
  CRISIS:  { tau: 0.80, kappa: 0.90, rho: 1.00 },
  FACTUAL: { tau: 0.90, kappa: 0.30, rho: 0.20 },
  CARE:    { tau: 0.40, kappa: 0.70, rho: 0.20 },
  SOCIAL:  { tau: 0.20, kappa: 0.10, rho: 0.00 },
  UNKNOWN: { tau: 0.50, kappa: 0.50, rho: 0.50 },
};

// GPV → Paradox Axis Map (mirror of atlas.py PARADOX_GPV_MAP)
// Each key = GPV pattern; value = activated paradox IDs (1-35)
const PARADOX_GPV_MAP = {
  tau_high_rho_low:    [1, 2, 3, 4, 21, 22, 25],
  rho_crisis:          [6, 7, 8, 9, 23, 26, 30],
  kappa_care:          [11, 12, 13, 15, 16, 17, 20],
  tau_kappa_factual:   [5, 18, 24],
  rho_high:            [8, 9, 10, 28, 29],
  query_exploratory:   [19, 22, 25],
  rho_sovereign:       [28, 29, 31, 34],
  seal_no_defense:     [30, 33, 35],
};

// Zone mapping: paradox ID → zone name (mirror of kernel PARADOX_GPV_MAP — 32 active IDs)
// Gaps at 14, 27, 32 — these IDs don't exist in the kernel's GPV map
const PARADOX_ZONES = {
  1:'Truth',2:'Truth',3:'Truth',4:'Truth',5:'Meaning',
  6:'Risk',7:'Risk',8:'Risk',9:'Risk',10:'Risk',
  11:'Care',12:'Care',13:'Care',15:'Care',
  16:'Care',17:'Care',18:'Meaning',19:'Meaning',20:'Meaning',
  21:'Discovery',22:'Discovery',23:'Risk',24:'Risk',25:'Risk',
  26:'Governance',28:'Governance',29:'Governance',30:'Governance',
  31:'Governance',33:'Sovereign',34:'Sovereign',35:'Sovereign',
};

// Zone ID mapping for ledger: zone name → zone number
const ZONE_IDS = { Truth:'I', Risk:'II', Care:'III', Meaning:'IV', Discovery:'V', Governance:'VI', Sovereign:'VII' };

// EUREKA threshold: paradox must appear in 3+ distinct sessions
const EUREKA_SESSION_THRESHOLD = 3;

// ── ΛΘΦ JS Mirror Functions ───────────────────────────────────────────

function _extractText(obj) {
  if (!obj) return '';
  if (typeof obj === 'string') return obj;
  if (obj.parts && Array.isArray(obj.parts)) {
    return obj.parts.map(p => (typeof p === 'string' ? p : p.text || '')).join(' ');
  }
  if (obj.message) return _extractText(obj.message);
  if (obj.prompt) return String(obj.prompt);
  if (obj.text) return String(obj.text);
  if (obj.intent) return String(obj.intent);
  return '';
}

function classifyLane(text) {
  /** Λ (Lambda): Text → Lane classification. Exact mirror of atlas.py Λ().
   *  Priority: CRISIS > FACTUAL (≥2 matches required) > CARE > SOCIAL.
   *  Default: CARE. */
  const t = _extractText(text).toLowerCase();
  if (!t) return { lane: 'CARE', zone: 'Care', confidence: 0.5 };

  // 1. CRISIS — direct harm signals (atlas.py lines 132-154)
  if (t.match(/\b(kill myself|suicide|self-harm|hurt\s+me|abuse|violence|assault|bomb|explosive|gun\s+to|knife\s+to|rape|torture|kidnap|hostage|want to die|end my life)\b/)) {
    return { lane: 'CRISIS', zone: 'Risk', confidence: 0.95 };
  }

  // "transfer" / "wire" → FACTUAL (atlas.py line 548-549)
  if (/\b(transfer|wire)\b/.test(t)) return { lane: 'FACTUAL', zone: 'Truth', confidence: 0.75 };

  // 2. FACTUAL — requires ≥2 pattern matches (atlas.py line 296: matches>=2)
  let factualMatches = 0;
  if (t.match(/\b(code|function|algorithm|class|method|variable|import|def |return |python|javascript|java|rust|c\+\+|typescript|golang)\b/)) factualMatches++;
  if (t.match(/\b(theorem|proof|equation|formula|calculate|compute|solve|derivative|integral|matrix|vector|probability|statistics|entropy)\b/)) factualMatches++;
  if (t.match(/\b(according to|research shows|studies indicate|data suggests|the capital of|the population of|was born in|invented by)\b/)) factualMatches++;
  if (t.match(/\b(what is|who is|when did|where is|how many|why does)\b.*\?/)) factualMatches++;
  if (t.match(/\b\d+\s*(kg|km|m|cm|mm|lb|ft|mi|degrees|percent)\b/)) factualMatches++;
  if (factualMatches >= 2) return { lane: 'FACTUAL', zone: 'Truth', confidence: 0.80 };

  // 3. CARE — explanations, support (atlas.py lines 192-201, match ≥1)
  if (t.match(/\b(help|assist|support|guide me|explain|how do I|how can I|what should I|advice|worried|concerned|confused|stressed|anxious|learn|understand|teach me|show me)\b/)) return { lane: 'CARE', zone: 'Care', confidence: 0.70 };

  // 4. SOCIAL — greetings, small talk (atlas.py lines 178-186, single match)
  if (t.match(/\b(hello|hi\b|hey|greetings|good morning|good afternoon|good evening|thanks|thank you|appreciate it|grateful|how are you|what's up|how's it going|bye|goodbye|see you|talk later)\b/)) return { lane: 'SOCIAL', zone: 'Truth', confidence: 0.85 };

  // 5. Default: CARE (atlas.py line 558)
  return { lane: 'CARE', zone: 'Care', confidence: 0.55 };
}

function computeDemand(lane, text) {
  /** Θ (Theta): Lane → Demand tensor (τ, κ, ρ). Exact mirror of atlas.py Θ(). */
  return DEMAND_TENSORS[lane] || DEMAND_TENSORS.UNKNOWN;
}

function resolveParadox(lane, demand, text) {
  /** Φ (Phi): GPV → Paradox resolution. JS mirror of atlas.py resolve_paradox_axes(). */
  const activated = new Set();

  // 1. tau_high_rho_low: τ ≥ 0.9, ρ ≤ 0.2, lane=FACTUAL
  if (demand.tau >= 0.9 && demand.rho <= 0.2 && lane === 'FACTUAL') {
    PARADOX_GPV_MAP.tau_high_rho_low.forEach(id => activated.add(id));
  }

  // 2. rho_crisis: ρ ≥ 0.3, lane=CRISIS
  if (demand.rho >= 0.3 && lane === 'CRISIS') {
    PARADOX_GPV_MAP.rho_crisis.forEach(id => activated.add(id));
  }

  // 3. kappa_care: κ ≥ 0.5, lane=CARE
  if (demand.kappa >= 0.5 && lane === 'CARE') {
    PARADOX_GPV_MAP.kappa_care.forEach(id => activated.add(id));
  }

  // 4. tau_kappa_factual: τ ≥ 0.8, κ ≥ 0.3, lane=FACTUAL
  if (demand.tau >= 0.8 && demand.kappa >= 0.3 && lane === 'FACTUAL') {
    PARADOX_GPV_MAP.tau_kappa_factual.forEach(id => activated.add(id));
  }

  // 5. rho_high: ρ ≥ 0.6, any lane
  if (demand.rho >= 0.6) {
    PARADOX_GPV_MAP.rho_high.forEach(id => activated.add(id));
  }

  // 6. query_exploratory: EXPLORATORY intent
  const t = _extractText(text).toLowerCase();
  if (t.match(/\b(explore|brainstorm|imagine|what if)\b/i)) {
    PARADOX_GPV_MAP.query_exploratory.forEach(id => activated.add(id));
  }

  // 7. rho_sovereign: ρ ≥ 0.8, any lane — P34 root/kernel
  if (demand.rho >= 0.8) {
    PARADOX_GPV_MAP.rho_sovereign.forEach(id => activated.add(id));
  }

  // 8. seal_no_defense: high-risk without defense — P35 positive≠closed
  if (demand.rho >= 0.5 && (lane === 'CRISIS' || lane === 'FACTUAL')) {
    PARADOX_GPV_MAP.seal_no_defense.forEach(id => activated.add(id));
  }

  const ids = [...activated].sort((a, b) => a - b);

  // Determine dominant zone and geometry
  const zones = {};
  ids.forEach(id => {
    const z = PARADOX_ZONES[id] || 'Unknown';
    zones[z] = (zones[z] || 0) + 1;
  });

  let dominantZone = 'Truth';
  let maxCount = 0;
  for (const [z, c] of Object.entries(zones)) {
    if (c > maxCount) { dominantZone = z; maxCount = c; }
  }

  return {
    paradox_ids: ids,
    paradox_count: ids.length,
    dominant_zone: dominantZone,
    zone_id: ZONE_IDS[dominantZone] || 'I',
    zones: zones,
  };
}

// ── Paradox Ledger (append-only, F1 fail-safe) ────────────────────────

function appendParadoxLedger(entry) {
  /** Append a paradox activation record. NEVER blocks. NEVER raises. */
  try {
    const dir = require('path').dirname(PARADOX_LEDGER);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(PARADOX_LEDGER, JSON.stringify(entry) + '\n');
  } catch {
    // F1 fail-safe: ledger failure never blocks the membrane
  }
}

function countParadoxSessions(paradoxId) {
  /** PURE READ: Count distinct sessions for a given paradox ID. */
  try {
    if (!fs.existsSync(PARADOX_LEDGER)) return 0;
    const raw = fs.readFileSync(PARADOX_LEDGER, 'utf-8').trim();
    if (!raw) return 0;
    const sessions = new Set();
    const lines = raw.split('\n');
    for (const line of lines) {
      try {
        const entry = JSON.parse(line);
        if (entry.paradox_ids && entry.paradox_ids.includes(paradoxId) && entry.session_id) {
          sessions.add(entry.session_id);
        }
      } catch { /* skip malformed lines */ }
    }
    return sessions.size;
  } catch {
    return 0;
  }
}

function checkEurekaThreshold(paradoxIds) {
  /** PURE READ: Check if any activated paradox meets EUREKA threshold. */
  const candidates = [];
  for (const id of paradoxIds) {
    const sessions = countParadoxSessions(id);
    if (sessions >= EUREKA_SESSION_THRESHOLD) {
      candidates.push({ paradox_id: id, distinct_sessions: sessions, zone: PARADOX_ZONES[id] || 'Unknown' });
    }
  }
  return {
    eureka_fired: candidates.length > 0,
    candidates: candidates.sort((a, b) => b.distinct_sessions - a.distinct_sessions),
  };
}

// ── Cognitive Wire: Full Classification Pipeline ──────────────────────

function runCognitiveWire(text, sessionId, organ) {
  /** Full ΛΘΦ pipeline — classify, demand, resolve, record, detect.
   *  F1 FAIL-SAFE: any failure returns a safe fallback object.
   *  NEVER blocks. NEVER raises. */
  const result = {
    lane: 'UNKNOWN',
    zone: 'Unknown',
    zone_id: 'I',
    demand: { tau: 0.5, kappa: 0.5, rho: 0.5 },
    paradox: { paradox_ids: [], paradox_count: 0, dominant_zone: 'Truth', zone_id: 'I', zones: {} },
    eureka: { eureka_fired: false, candidates: [] },
    timestamp: new Date().toISOString(),
    session_id: sessionId || 'unknown',
    organ: organ || 'UNKNOWN',
  };

  try {
    // Λ: Lane classification
    const laneResult = classifyLane(text);
    result.lane = laneResult.lane;
    result.zone = laneResult.zone;

    // Θ: Demand tensor
    result.demand = computeDemand(laneResult.lane, text);

    // Φ: Paradox resolution
    result.paradox = resolveParadox(laneResult.lane, result.demand, text);
    result.zone_id = result.paradox.zone_id;

    // EUREKA: Cross-session maturity check
    if (result.paradox.paradox_ids.length > 0) {
      result.eureka = checkEurekaThreshold(result.paradox.paradox_ids);
    }

    // Record to ledger (F1 fail-safe internally)
    appendParadoxLedger({
      timestamp: result.timestamp,
      session_id: result.session_id,
      organ: result.organ,
      lane: result.lane,
      tau: result.demand.tau,
      kappa: result.demand.kappa,
      rho: result.demand.rho,
      paradox_ids: result.paradox.paradox_ids,
      paradox_count: result.paradox.paradox_count,
      zone: result.zone,
      zone_id: result.zone_id,
      eureka_fired: result.eureka.eureka_fired,
      catalyst: _extractText(text).slice(0, 200),
    });

  } catch {
    // F1: Swallow everything. Return fallback result with empty state.
    result.lane = 'UNKNOWN';
    result.demand = { tau: 0.5, kappa: 0.5, rho: 0.5 };
    result.paradox = { paradox_ids: [], paradox_count: 0, dominant_zone: 'Truth', zone_id: 'I', zones: {} };
    result.eureka = { eureka_fired: false, candidates: [] };
  }

  return result;
}

// ── Validation ───────────────────────────────────────────────────────
function validateEnvelope(envelope) {
  const errors = [];
  const warnings = [];

  // Required fields
  for (const field of ['membrane_version', 'timestamp', 'actor', 'authority', 'uncertainty', 'verdict']) {
    if (!envelope[field]) errors.push(`MEMBRANE_MISSING_FIELD: ${field}`);
  }

  // Verdict must be valid
  if (envelope.verdict && !VERDICTS.includes(envelope.verdict)) {
    errors.push(`MEMBRANE_INVALID_VERDICT: ${envelope.verdict}`);
  }

  // Uncertainty must be valid
  if (envelope.uncertainty && !UNCERTAINTIES.includes(envelope.uncertainty)) {
    errors.push(`MEMBRANE_INVALID_UNCERTAINTY: ${envelope.uncertainty}`);
  }

  // SEAL-specific checks
  if (envelope.verdict === 'SEAL') {
    // Rule: SPEC cannot SEAL
    if (envelope.uncertainty === 'SPEC') {
      errors.push('MEMBRANE_SPEC_SEAL: Cannot SEAL SPEC-class claim');
    }
    // Rule: C_dark > 0.30 cannot SEAL (F9)
    if (envelope.cooling?.C_dark > C_DARK_THRESHOLD) {
      errors.push(`MEMBRANE_C_DARK_HIGH: ${envelope.cooling.C_dark} > ${C_DARK_THRESHOLD}`);
    }
    // Rule: W3 = 0 cannot SEAL (F3)
    if (envelope.witness?.W3 === 0) {
      errors.push('MEMBRANE_W3_ZERO: Tri-witness collapsed');
    }
    // Rule: Receipt must be sealed
    if (!envelope.receipt?.sealed) {
      errors.push('MEMBRANE_UNSEALED: SEAL verdict requires sealed receipt');
    }
  }

  // IRREVERSIBLE checks
  if (envelope.action_class === 'IRREVERSIBLE') {
    if (envelope.reversibility !== 'NONE') {
      warnings.push('MEMBRANE_IRREVERSIBLE_MISMATCH: IRREVERSIBLE action but reversibility != NONE');
    }
    if (!envelope.floors_checked?.includes('F13')) {
      errors.push('MEMBRANE_F13_REQUIRED: IRREVERSIBLE requires F13 check');
    }
  }

  // CRITICAL blast radius checks
  if (envelope.blast_radius === 'CRITICAL') {
    if (!envelope.floors_checked?.includes('F1') || !envelope.floors_checked?.includes('F13')) {
      errors.push('MEMBRANE_CRITICAL_FLOORS: CRITICAL requires F1+F13');
    }
  }

  // Floor violations force VOID/HOLD
  if (envelope.floor_violations?.length > 0) {
    if (!['VOID', 'HOLD'].includes(envelope.verdict)) {
      errors.push('MEMBRANE_FLOOR_VIOLATION: Floor violations require VOID or HOLD');
    }
  }

  return { valid: errors.length === 0, errors, warnings };
}

// ── Express Middleware ────────────────────────────────────────────────
function membraneMiddleware(req, res, next) {
  // Only apply to A2A routes
  if (!req.path.startsWith('/a2a') && !req.path.startsWith('/execute') && !req.path.startsWith('/sense')) {
    return next();
  }

  const now = new Date().toISOString();
  const lineageId = generateLineageId();
  const lastSeq = getLastSealSeq();

  // Extract or create membrane envelope
  let envelope = req.body?._membrane || req.headers['x-membrane-envelope'];

  if (typeof envelope === 'string') {
    try { envelope = JSON.parse(envelope); } catch { envelope = null; }
  }

  if (!envelope) {
    // Auto-generate from request context
    const text = req.body?.message || req.body?.text || req.body?.intent || '';
    // F2: Validate organ against known list — prevent 't' truncation artifacts
    let organ = req.body?.actor?.organ || req.headers['x-organ'] || '';
    if (!ORGANS.includes(organ)) {
      // Fallback: extract from body actor or request path
      organ = req.body?.source || req.body?.organ || (req.path.includes('/a2a/') ? req.path.split('/a2a/')[1]?.split('/')[0] : '') || 'UNKNOWN';
      if (!ORGANS.includes(organ)) organ = 'UNKNOWN';
    }
    const sessionId = req.body?.session_id || req.headers['x-session-id'] || req.body?.actor?.session_id;

    envelope = {
      membrane_version: MEMBRANE_VERSION,
      timestamp: now,
      actor: { organ, session_id: sessionId },
      authority: req.body?.authority || 'THINK',
      uncertainty: classifyPerception(text),
      verdict: 'UNKNOWN',
      action_class: classifyAction(text),
      blast_radius: req.body?.blast_radius || 'LOW',
      reversibility: req.body?.reversibility || 'FULL',
      receipt: {
        lineage_id: lineageId,
        parent_id: lastSeq ? `seal-${lastSeq}` : null,
        sealed: false,
      },
      cooling: { C_dark: 0.05, C_light: 0.95 },
      witness: { human: 0, ai: 0.5, external: 0, W3: 0 },
      floors_checked: [],
    };
  }

  // ── ATLAS333 Cognitive Wire ──────────────────────────────────────────
  // Every cross-organ message is classified through ATLAS333 before routing.
  // F1 FAIL-SAFE: runCognitiveWire() wraps everything in try/catch.
  // EUREKA candidates are flagged but NEVER auto-block — 888-APEX reviews.
  {
    const wireText = req.body?.message || req.body?.text || req.body?.intent || '';
    const sessionId = envelope.actor?.session_id || req.body?.session_id || req.headers['x-session-id'];
    const organ = envelope.actor?.organ || 'UNKNOWN';
    const cognitive = runCognitiveWire(wireText, sessionId, organ);

    // Attach ATLAS333 classification to envelope
    envelope._atlas333 = {
      lane: cognitive.lane,
      zone: cognitive.zone,
      zone_id: cognitive.zone_id,
      demand: cognitive.demand,
      paradox_ids: cognitive.paradox.paradox_ids,
      paradox_count: cognitive.paradox.paradox_count,
      eureka: cognitive.eureka,
    };

    // If EUREKA candidates detected, inject a flag (advisory only)
    if (cognitive.eureka.eureka_fired) {
      envelope._membrane_warnings = envelope._membrane_warnings || [];
      for (const c of cognitive.eureka.candidates) {
        envelope._membrane_warnings.push(
          `EUREKA777: Paradox P${c.paradox_id} matured (${c.distinct_sessions} sessions in zone ${c.zone}). Route to 888-APEX for constitutional review.`
        );
      }
    }
  }

  // Validate
  const result = validateEnvelope(envelope);

  if (!result.valid) {
    appendLog({
      event: 'membrane:rejected',
      timestamp: now,
      path: req.path,
      errors: result.errors,
      envelope_summary: {
        organ: envelope.actor?.organ,
        verdict: envelope.verdict,
        uncertainty: envelope.uncertainty,
      },
    });

    // Force verdict to HOLD on validation failure
    envelope.verdict = 'HOLD';
    envelope._membrane_errors = result.errors;
  }

  if (result.warnings.length > 0) {
    appendLog({
      event: 'membrane:warning',
      timestamp: now,
      path: req.path,
      warnings: result.warnings,
    });
  }

  // Attach envelope to request
  req._membrane = envelope;
  req._membrane_validation = result;

  // Log crossing
  appendLog({
    event: 'membrane:crossing',
    timestamp: now,
    direction: 'inbound',
    path: req.path,
    organ: envelope.actor?.organ,
    authority: envelope.authority,
    uncertainty: envelope.uncertainty,
    verdict: envelope.verdict,
    action_class: envelope.action_class,
    lineage_id: lineageId,
    atlas333: envelope._atlas333 ? {
      lane: envelope._atlas333.lane,
      zone: envelope._atlas333.zone_id,
      paradox_count: envelope._atlas333.paradox_count,
      eureka: envelope._atlas333.eureka?.eureka_fired || false,
    } : null,
  });

  // Continue
  next();
}

// ── Response wrapper ──────────────────────────────────────────────────
function membraneResponseHook(req, res, next) {
  const originalJson = res.json.bind(res);

  res.json = function(data) {
    // Attach membrane envelope to response
    if (req._membrane && data && typeof data === 'object') {
      data._membrane = {
        ...req._membrane,
        direction: 'outbound',
        timestamp: new Date().toISOString(),
        receipt: {
          ...req._membrane.receipt,
          sealed: req._membrane.verdict === 'SEAL',
        },
      };

      // Log outbound
      appendLog({
        event: 'membrane:crossing',
        timestamp: new Date().toISOString(),
        direction: 'outbound',
        path: req.path,
        organ: req._membrane.actor?.organ,
        verdict: req._membrane.verdict,
        lineage_id: req._membrane.receipt?.lineage_id,
      });
    }

    return originalJson(data);
  };

  next();
}

module.exports = {
  membraneMiddleware,
  membraneResponseHook,
  validateEnvelope,
  classifyPerception,
  classifyAction,
  classifyLane,
  computeDemand,
  resolveParadox,
  runCognitiveWire,
  checkEurekaThreshold,
  appendParadoxLedger,
  MEMBRANE_VERSION,
  PARADOX_GPV_MAP,
  DEMAND_TENSORS,
};
