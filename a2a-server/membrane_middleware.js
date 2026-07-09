/**
 * Membrane Middleware — ZEN-ALL v0.3
 * ═══════════════════════════════════════════════════════════════
 * 
 * Express middleware for AAA :3001 A2A gateway.
 * Every cross-organ message MUST pass through this membrane.
 * 
 * Enforces:
 *   - Perception tagging (OBS/DER/INT/SPEC)
 *   - Verdict grammar (SEAL/HOLD/SABAR/VOID/UNKNOWN)
 *   - Receipt lineage (hash chain reference)
 *   - C_dark threshold (F9 ANTI-HANTU)
 *   - Tri-witness check (F3 WITNESS)
 *   - Floor compliance (F1-F13)
 * 
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
  const t = text.toLowerCase();
  if (t.match(/\b(measured|observed|recorded|detected|found|data shows|the log)\b/)) return 'OBS';
  if (t.match(/\b(calculated|computed|derived|extrapolated|estimated)\b/)) return 'DER';
  if (t.match(/\b(interpreted|synthesized|reasoned|inferred|concluded)\b/)) return 'INT';
  if (t.match(/\b(speculated|hypothetical|might|could|possibly|perhaps)\b/)) return 'SPEC';
  return 'INT';
}

function classifyAction(text) {
  if (!text) return 'OBSERVE';
  const t = text.toLowerCase();
  if (t.match(/\b(delete|remove|drop|destroy|purge|wipe)\b/)) return 'IRREVERSIBLE';
  if (t.match(/\b(deploy|push|publish|send|execute|run|apply)\b/)) return 'MUTATE';
  if (t.match(/\b(write|create|edit|update|modify|change)\b/)) return 'DRAFT';
  if (t.match(/\b(analyze|compare|evaluate|assess|review)\b/)) return 'ANALYZE';
  return 'OBSERVE';
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
    const organ = req.body?.actor?.organ || req.headers['x-organ'] || 'UNKNOWN';

    envelope = {
      membrane_version: MEMBRANE_VERSION,
      timestamp: now,
      actor: { organ, session_id: req.body?.session_id || req.headers['x-session-id'] },
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
  MEMBRANE_VERSION,
};
