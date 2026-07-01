/**
 * cognitive_hierarchy.js — APEX Master Seal Runtime Loader (JS)
 * =============================================================
 * Production runtime companion to TypeScript src/adapter/cognitive_hierarchy.ts.
 * Loads cognitive hierarchy from YAML and exposes ring/role checks.
 * 
 * APEX Master Seal 2026-07-01:
 *   - Hassabis Inversion: Role over Model
 *   - Thermodynamic Law: DeltaS < 0
 *   - Metabolizer Loop: Ingest -> Generate -> Metabolize -> Execute -> Seal
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const fs = require('fs');
const path = require('path');
const yaml = require('yaml');

const CONFIG_PATH = path.resolve('/root/AAA/contracts/cognitive_hierarchy.yaml');
let _cached = null;

/**
 * Load cognitive hierarchy from disk. Cached in memory.
 */
function loadHierarchy() {
  if (_cached) return _cached;

  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
    const parsed = yaml.parse(raw);
    
    // Resolve env var overrides for model slots
    if (parsed.model_slots) {
      for (const slot of parsed.model_slots) {
        const envVal = process.env[slot.env_var];
        if (envVal && envVal.length > 0) {
          slot.default = envVal;
        }
      }
    }
    
    _cached = parsed;
    return parsed;
  } catch (err) {
    console.error('[CognitiveHierarchy] Failed to load:', err.message);
    return null;
  }
}

/**
 * Get active generator model names.
 */
function getActiveGenerators() {
  const h = loadHierarchy();
  if (!h || !h.model_slots) return [];
  return h.model_slots
    .filter(s => s.ring === 'generator' && s.default && s.default.length > 0)
    .map(s => s.default);
}

/**
 * Get active epistemic floor model name.
 */
function getEpistemicFloorModel() {
  const h = loadHierarchy();
  if (!h || !h.model_slots) return null;
  const primary = h.model_slots.find(s => s.slot_id === 'epistemic_floor_primary');
  if (primary && primary.default && primary.default.length > 0) return primary.default;
  const fallback = h.model_slots.find(s => s.slot_id === 'epistemic_floor_fallback');
  return (fallback && fallback.default && fallback.default.length > 0) ? fallback.default : null;
}

/**
 * Validate pipeline invariant: EpistemicFloor requires at least one generator.
 */
function validatePipeline() {
  const generators = getActiveGenerators();
  if (generators.length === 0) {
    return { ok: false, reason: 'No active generators. EpistemicFloor cannot be invoked without generator output.' };
  }
  return { ok: true };
}

/**
 * Get the cognitive ring for an agent by its ID.
 */
function getRingForAgent(agentId) {
  // Map agent IDs to rings
  const RING_MAP = {
    '333-AGI': 'generator',
    '555-ASI': 'generator',
    '777-forge': 'generator',
    '888-APEX': 'epistemic_floor',
    'A-AUDIT': 'epistemic_floor',
    'A-ARCHIVE': 'neutral',
    'hermes-asi': 'generator',
    'openclaw': 'generator',
    'opencode': 'generator',
    'main': 'generator',
    'claude-code': 'generator',
    'gemini-cli': 'epistemic_floor',
    'grok-build': 'generator',
  };
  return RING_MAP[agentId] || 'unassigned';
}

/**
 * APEX Master Seal confidence cap.
 * F7 HUMILITY — EpistemicFloor confidence hard cap at 0.92.
 */
const CONFIDENCE_CAP = 0.92;
function capConfidence(value) {
  return Math.min(value, CONFIDENCE_CAP);
}

/**
 * Determine if JITU clearance is required.
 * F1 ABSOLUTE HOLD: Destructive actions require JITU.
 */
function requiresJitu(text) {
  const destructivePatterns = ['delete ', 'drop ', 'rm ', 'truncate', 'remove --force', 'push to prod', 'force push', 'DROP TABLE'];
  return destructivePatterns.some(p => text.toLowerCase().includes(p));
}

module.exports = {
  loadHierarchy,
  getActiveGenerators,
  getEpistemicFloorModel,
  validatePipeline,
  getRingForAgent,
  capConfidence,
  requiresJitu,
  CONFIDENCE_CAP,
};