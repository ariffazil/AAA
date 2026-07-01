/**
 * cognitive_hierarchy.ts — Cognitive Hierarchy Runtime Loader
 * ============================================================
 * Loads the cognitive hierarchy configuration from AAA/contracts/cognitive_hierarchy.yaml
 * and exposes it as runtime types for the A2A routing adapter.
 *
 * APEX Master Seal 2026-07-01:
 *   - Hassabis Inversion: Role over Model
 *   - Thermodynamic Law: DeltaS < 0
 *   - Metabolizer Loop: Ingest -> Generate -> Metabolize -> Execute -> Seal
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import * as yaml from 'yaml';

// ── Types ────────────────────────────────────────────────────────────────────

export type RingId = 'generator' | 'epistemic_floor';

export interface RingConfig {
  id: RingId;
  label: string;
  thermodynamic_role: 'entropy_source' | 'entropy_sink';
  description: string;
  shadows: Record<string, string>;
  authority: {
    observe: boolean;
    suggest: boolean;
    simulate: boolean;
    draft: boolean;
    queue: boolean;
    execute_reversible: boolean;
    execute_high_impact: boolean;
    irreversible: boolean;
    seal: boolean;
  };
  routing: {
    placement: 'first' | 'final' | 'middle';
    parallelism: string;
    output_handoff: string;
    input_condition?: string;
  };
}

export interface ModelSlot {
  slot_id: string;
  ring: RingId;
  env_var: string;
  default: string;
  description: string;
  fallback: string;
}

export interface PipelineConfig {
  entry: string;
  exit: string;
  invariant: string;
  coalescence: {
    strategy: string;
    buffer_size: string;
    timeout_ms: number;
    required_quorum: number;
  };
  metabolizer_loop?: {
    description: string;
    steps: string[];
  };
  tri_witness_integration: {
    description: string;
    note: string;
  };
}

export interface ShadowMitigation {
  thermal_delay: { rule: string; mechanism: string; enforcement: string };
  over_constraint: { rule: string; mechanism: string; enforcement: string };
  oracle_trap: { rule: string; mechanism: string; enforcement: string };
}

export interface GovernanceConfig {
  master_seal: string;
  floor_gates: string[];
  change_control: Record<string, string>;
}

export interface CognitiveHierarchy {
  schema_version: string;
  kind: string;
  owner: string;
  authority: string;
  status: string;
  seal_ref: string;
  rings: RingConfig[];
  model_slots: ModelSlot[];
  pipeline: PipelineConfig;
  shadow_mitigation: ShadowMitigation;
  governance: GovernanceConfig;
}

// ── Runtime singleton ─────────────────────────────────────────────────────────

let _cached: CognitiveHierarchy | null = null;
const CONFIG_PATH = path.resolve('/root/AAA/contracts/cognitive_hierarchy.yaml');

/**
 * Load the cognitive hierarchy from disk.
 * Caches in memory for runtime performance.
 * Throws on invalid/missing config.
 */
export function loadCognitiveHierarchy(): CognitiveHierarchy {
  if (_cached) return _cached;

  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
    const parsed = yaml.parse(raw) as CognitiveHierarchy;

    // ── Structural validation ────────────────────────────────────────────
    if (!parsed.rings || parsed.rings.length < 2) {
      throw new Error('cognitive_hierarchy: must define at least 2 rings (generator + epistemic_floor)');
    }
    if (!parsed.model_slots || parsed.model_slots.length < 2) {
      throw new Error('cognitive_hierarchy: must define at least 2 model slots');
    }

    const ringIds = parsed.rings.map(r => r.id);
    if (!ringIds.includes('generator')) {
      throw new Error('cognitive_hierarchy: missing required ring "generator"');
    }
    if (!ringIds.includes('epistemic_floor')) {
      throw new Error('cognitive_hierarchy: missing required ring "epistemic_floor"');
    }

    // ── Resolve environment variable overrides ────────────────────────────
    for (const slot of parsed.model_slots) {
      const envValue = process.env[slot.env_var];
      if (envValue && envValue.length > 0) {
        slot.default = envValue;
      }
    }

    _cached = parsed;
    return parsed;
  } catch (err) {
    console.error('[CognitiveHierarchy] Failed to load:', err);
    throw err;
  }
}

/**
 * Get the resolved model name for a given slot.
 * Returns: env var value > config default > fallback > empty string.
 */
export function getModelForSlot(slotId: string): string {
  const hierarchy = loadCognitiveHierarchy();
  const slot = hierarchy.model_slots.find(s => s.slot_id === slotId);
  if (!slot) return '';
  return slot.default || slot.fallback || '';
}

/**
 * Get all active generator model names.
 */
export function getActiveGenerators(): string[] {
  const hierarchy = loadCognitiveHierarchy();
  return hierarchy.model_slots
    .filter(s => s.ring === 'generator' && s.default.length > 0)
    .map(s => s.default);
}

/**
 * Get the active epistemic floor model name.
 */
export function getEpistemicFloorModel(): string {
  const primary = getModelForSlot('epistemic_floor_primary');
  if (primary) return primary;
  return getModelForSlot('epistemic_floor_fallback');
}

/**
 * Validate that the pipeline invariant holds:
 * EpistemicFloor is NEVER invoked before at least one generator is active.
 */
export function validatePipelineInvariant(): { ok: boolean; reason?: string } {
  const generators = getActiveGenerators();
  const floor = getEpistemicFloorModel();

  if (generators.length === 0) {
    return { ok: false, reason: 'No active generators. EpistemicFloor cannot be invoked without generator output.' };
  }
  if (!floor) {
    return { ok: true, reason: 'No EpistemicFloor configured. Falling back to single-stage pipeline.' };
  }

  return { ok: true };
}

/**
 * Clear the in-memory cache (useful after config hot-reload).
 */
export function clearHierarchyCache(): void {
  _cached = null;
}