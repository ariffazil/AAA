#!/usr/bin/env node
/**
 * EMD Validation Gate — A2A External Payload Sanitizer
 * ═══════════════════════════════════════════════════════════════
 * 
 * Arif: "External A2A agents are opaque. Their outputs are unverified raw signals.
 *        Every external payload must pass through EMD decode + tri-witness before 
 *        it reaches the arifOS kernel."
 * 
 * This middleware intercepts incoming A2A messages from external peers and:
 *   1. Classifies the source (internal vs external)
 *   2. Strips claims from the message, labeling them OBS/DER/INT/SPEC
 *   3. Computes tri-witness score W³ = ∛(Human × AI × External)
 *   4. Blocks or downgrades payloads below constitutional thresholds
 *   5. Appends validation metadata to the request for downstream handlers
 * 
 * F2 TRUTH: Every claim labeled.
 * F3 WITNESS: Tri-witness required for SEAL-grade payloads.
 * F12 INJECTION: External ≠ authority.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

'use strict';

const crypto = require('crypto');
const fs = require('fs');

// ── Constants ────────────────────────────────────────────────────────
const GATE_VERSION = '1.0.0';
const LOG_FILE = '/root/.local/share/arifos/emd-gate-crossings.jsonl';

// Internal peers (AAA mesh residents — trusted but still validated)
const INTERNAL_PEERS = [
  'arifos', 'aforge', 'geox', 'wealth', 'well', 'aaa', 'vault999',
  'hermes', 'opencode', 'openclaw', 'antigravity',
  '333-AGI', '555-ASI', '888-APEX',
  'aaa-gateway', 'aaa-gateway-internal',
  'aaa-architect', 'aaa-engineer', 'aaa-auditor',
];

// Epistemic label confidence caps (F7 HUMILITY)
const CONFIDENCE_CAPS = { OBS: 0.90, DER: 0.85, INT: 0.75, SPEC: 0.60 };

// Tri-witness thresholds (F3 WITNESS)
const W3_THRESHOLD = 0.30;   // Below this → payload BLOCKED
const W3_WARN = 0.60;        // Below this → downgrade to OBSERVE_ONLY

/**
 * Classify whether a payload originates from an external A2A peer.
 * @param {Object} req - Express request
 * @returns {{ external: boolean, sourceId: string }}
 */
function classifySource(req) {
  const body = req.body || {};
  const params = body.params || {};
  const metadata = params.metadata || {};
  const message = params.message || {};
  
  // Check for internal identity signals
  const sourceId = metadata.source_agent || 
                   metadata.agent_id || 
                   params.agent_id || 
                   req.headers['x-a2a-agent-id'] || 
                   'unknown';
  
  const isInternal = INTERNAL_PEERS.some(peer => 
    sourceId.toLowerCase().includes(peer.toLowerCase())
  ) || req.headers['x-arifos-internal'] === 'true' ||
     req.headers['x-a2a-internal'] === 'true';

  return { external: !isInternal, sourceId };
}

/**
 * Extract and label claims from a message payload.
 * Uses heuristic pattern matching for claim detection.
 * 
 * @param {Object} message - A2A message object
 * @returns {Array<{text: string, epistemicLabel: string, confidence: number}>}
 */
function extractClaims(message) {
  const claims = [];
  if (!message) return claims;

  // Extract text from message parts
  const parts = message.parts || [message];
  for (const part of parts) {
    if (typeof part === 'string') {
      const extracted = extractClaimsFromText(part);
      claims.push(...extracted);
    } else if (part && part.text) {
      const extracted = extractClaimsFromText(part.text);
      claims.push(...extracted);
    } else if (part && part.content) {
      const text = typeof part.content === 'string' ? part.content : JSON.stringify(part.content);
      const extracted = extractClaimsFromText(text);
      claims.push(...extracted);
    }
  }

  return claims;
}

/**
 * Heuristic claim extractor — splits text on claim-like patterns.
 */
function extractClaimsFromText(text) {
  if (!text || text.length < 10) return [];
  const claims = [];
  
  // Split on sentence boundaries
  const sentences = text.split(/(?<=[.!?])\s+/);
  
  for (const sentence of sentences) {
    const trimmed = sentence.trim();
    if (trimmed.length < 15) continue;
    
    const epistemicLabel = classifyPerception(trimmed);
    claims.push({
      text: trimmed,
      epistemicLabel,
      confidence: CONFIDENCE_CAPS[epistemicLabel] || 0.75,
    });
  }

  return claims;
}

/**
 * Classify the epistemic label of a text string.
 */
function classifyPerception(text) {
  if (!text) return 'INT';
  const t = text.toLowerCase();
  if (t.match(/\b(measured|observed|recorded|detected|found|data shows|the log|confirmed by)\b/)) return 'OBS';
  if (t.match(/\b(calculated|computed|derived|extrapolated|estimated|forecast)\b/)) return 'DER';
  if (t.match(/\b(interpreted|synthesized|reasoned|inferred|concluded|analyzed)\b/)) return 'INT';
  if (t.match(/\b(speculated|hypothetical|might|could|possibly|perhaps|assumed)\b/)) return 'SPEC';
  return 'INT';
}

/**
 * Compute tri-witness score W³ = ∛(Human × AI × External).
 * For external A2A payloads:
 *   - Human channel: 0.0 (Arif hasn't witnessed this)
 *   - AI channel: 0.0 (we can't verify the external agent's reasoning)
 *   - External channel: 0.3 (the payload itself exists, but is unverified)
 * 
 * @param {Object} source - Source classification
 * @param {Array} claims - Extracted claims
 * @returns {{ W3: number, h: number, ai: number, ext: number, verdict: string }}
 */
function computeTriWitness(source, claims) {
  if (source.external) {
    // External payloads: zero human + ai, minimal external evidence
    const h = 0.0;   // No human witness
    const ai = 0.0;  // Can't verify external agent's reasoning
    const ext = claims.length > 0 ? 0.3 : 0.1; // Payload exists but is unverified
    
    const W3 = Math.cbrt(h * ai * ext || 0.001); // Avoid exact zero for trace
    return { W3, h, ai, ext, verdict: W3 >= W3_THRESHOLD ? 'WEAK' : 'DIVERGENT' };
  }
  
  // Internal payloads: higher trust baseline
  const h = 0.5;   // Implicit human trust from sovereign domain
  const ai = 0.7;  // Internal agents share verification
  const ext = 0.6; // Internal messages carry provenance
  const W3 = Math.cbrt(h * ai * ext);
  return { W3, h, ai, ext, verdict: W3 >= W3_WARN ? 'CONSENSUS' : 'WEAK' };
}

/**
 * Log a gate crossing to the audit trail (F11 AUDIT).
 */
function logCrossing(entry) {
  try {
    const dir = require('path').dirname(LOG_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(LOG_FILE, JSON.stringify({
      ...entry,
      timestamp: new Date().toISOString(),
      gate_version: GATE_VERSION,
    }) + '\n');
  } catch { /* best-effort */ }
}

/**
 * Express middleware — EMD validation gate.
 * 
 * Usage: app.use('/a2a', emdValidationGate);
 * 
 * Attaches `req.emd` to the request:
 *   - req.emd.source: { external, sourceId }
 *   - req.emd.claims: [{ text, epistemicLabel, confidence }]
 *   - req.emd.witness: { W3, h, ai, ext, verdict }
 *   - req.emd.blocked: boolean (true if payload must be rejected)
 *   - req.emd.downgraded: boolean (true if authority must be reduced)
 */
function emdValidationGate(req, res, next) {
  // Only intercept A2A message/task operations, not discovery/agent-card GETs
  if (req.method !== 'POST') return next();
  
  const body = req.body || {};
  
  // Only validate JSON-RPC messages
  if (!body.jsonrpc || !body.method) return next();
  
  // Skip discovery methods
  if (body.method === 'agent/getCard' || body.method === 'agent/listSkills') return next();

  const message = body.params?.message;
  if (!message) return next(); // No message payload to validate

  // ── EMD Pipeline ──────────────────────────────────────────────
  
  // 1. Classify source
  const source = classifySource(req);
  
  // 2. Extract and label claims
  const claims = extractClaims(message);
  
  // 3. Compute tri-witness
  const witness = computeTriWitness(source, claims);
  
  // 4. Determine gate verdict
  let blocked = false;
  let downgraded = false;
  
  if (source.external) {
    if (witness.W3 < W3_THRESHOLD) {
      blocked = true;
    } else if (witness.W3 < W3_WARN) {
      downgraded = true;
    }
  }
  
  // 5. Attach EMD metadata to request
  req.emd = {
    source,
    claims,
    witness,
    blocked,
    downgraded,
    validatedAt: new Date().toISOString(),
    gateVersion: GATE_VERSION,
  };

  // 6. Log the crossing
  logCrossing({
    source: source.sourceId,
    external: source.external,
    method: body.method,
    claimCount: claims.length,
    W3: witness.W3,
    witnessVerdict: witness.verdict,
    blocked,
    downgraded,
  });

  // 7. Block or pass
  if (blocked) {
    console.warn(`[EMD GATE] BLOCKED external payload from "${source.sourceId}" — W³=${witness.W3.toFixed(3)}`);
    return res.status(403).json({
      jsonrpc: '2.0',
      id: body.id || 0,
      error: {
        code: -32001,
        message: 'EMD_VALIDATION_BLOCKED: External payload failed tri-witness threshold. Provide verifiable evidence.',
        data: {
          gate: 'emd-validation',
          W3: witness.W3,
          threshold: W3_THRESHOLD,
          claimsExtracted: claims.length,
          recommendation: 'Resubmit with human witness or verifiable external evidence.',
        },
      },
    });
  }

  if (downgraded) {
    console.warn(`[EMD GATE] DOWNGRADED external payload from "${source.sourceId}" — W³=${witness.W3.toFixed(3)}`);
    // Mark for downstream handlers to treat as OBSERVE_ONLY
    req.emd.authorityOverride = 'OBSERVE_ONLY';
  }

  next();
}

module.exports = {
  emdValidationGate,
  classifySource,
  extractClaims,
  computeTriWitness,
  logCrossing,
  GATE_VERSION,
  W3_THRESHOLD,
  W3_WARN,
  INTERNAL_PEERS,
};
