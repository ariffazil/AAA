/**
 * Session D — AAA Registry Fail-Closed Schema Types
 * ═══════════════════════════════════════════════════
 * 
 * Five separate dimensions. Never collapsed into one "healthy" flag.
 * 
 * invariant: advertised_tool ∈ runtime_callable_registry
 * Any violation → registry_state = DRIFT, readiness = false, mutation_authority = HOLD
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

// ── 5-Dimension State Vocabulary ──────────────────────────────────────────

/** Process liveness: is the organ process running? */
export type ProcessLiveness = 'UP' | 'DOWN' | 'UNKNOWN';

/** Transport reachability: can we reach the organ's endpoint? */
export type TransportReachability = 'UP' | 'DOWN' | 'UNKNOWN';

/** Registry alignment: do declared tools match runtime-callable tools? */
export type RegistryAlignment = 'ALIGNED' | 'DRIFT' | 'UNKNOWN' | 'MISSING_CANONICAL' | 'PHANTOM_DETECTED' | 'DUPLICATE_DETECTED';

/** Organ readiness: is the organ ready to serve requests? */
export type OrganReadiness = 'READY' | 'DEGRADED' | 'HOLD' | 'UNKNOWN';

/** Mutation authority: can the organ mutate? Only arifOS/judge can grant. Registry never authorizes. */
export type MutationAuthority = 'NOT_EVALUATED' | 'HOLD' | 'AUTHORIZED' | 'DENIED' | 'UNKNOWN';

// ── Organ Identity ────────────────────────────────────────────────────────

export interface OrganIdentity {
  organId: string;
  name: string;
  port: number;
  agentId: string;        // MUST be unique — duplicate → hard failure
  identityHash?: string;
}

// ── Tool Entry ────────────────────────────────────────────────────────────

export interface ToolEntry {
  name: string;
  description?: string;
  declared: boolean;       // Present in static declaration?
  callable: boolean;       // Present in live tools/list?
  tested: boolean;         // Invocation test passed?
  lastTested?: string;     // ISO-8601
}

// ── Organ Status (per-organ, all 5 dimensions) ────────────────────────────

export interface OrganStatus {
  identity: OrganIdentity;
  processLiveness: ProcessLiveness;
  transportReachability: TransportReachability;
  registryAlignment: RegistryAlignment;
  organReadiness: OrganReadiness;
  mutationAuthority: MutationAuthority;
  tools: ToolEntry[];
  /** Tools declared but not callable (phantom) */
  phantomTools: string[];
  /** Tools callable but not declared (missing from registry) */
  missingTools: string[];
  /** Timestamps */
  probedAt: string;       // ISO-8601
  freshnessMs: number;     // ms since probe
}

// ── Duplicate Detection ───────────────────────────────────────────────────

export interface DuplicateEntry {
  agentId: string;
  sources: string[];       // Paths where duplicate was found
  message: string;
}

// ── Conformance Artifact (deterministic, schema-versioned) ────────────────

export interface ConformanceArtifact {
  schemaVersion: 'session-d.v1';
  generatedAt: string;       // ISO-8601
  runtimeCommit: string;     // AAA runtime commit
  registryHash: string;      // SHA-256 of canonical tool list
  freshnessMs: number;       // Age of this artifact
  organs: OrganStatus[];
  duplicates: DuplicateEntry[];
  /** Summary counts */
  summary: {
    totalOrgans: number;
    organsUp: number;
    organsReady: number;
    organsAligned: number;
    totalTools: number;
    phantomTools: number;
    missingTools: number;
    duplicateAgents: number;
    overallVerdict: RegistryAlignment;
  };
}

// ── Canonical Organ Declarations ──────────────────────────────────────────

export const CANONICAL_ORGANS: OrganIdentity[] = [
  { organId: 'arifos',  name: 'arifOS Constitutional Kernel', port: 8088,  agentId: 'arifos-mcp' },
  { organId: 'geox',    name: 'GEOX Earth Intelligence',      port: 8081,  agentId: 'geox-mcp' },
  { organId: 'wealth',  name: 'WEALTH Capital Intelligence',  port: 18082, agentId: 'wealth-mcp' },
  { organId: 'well',    name: 'WELL Human Readiness',         port: 18083, agentId: 'well-mcp' },
  { organId: 'aforge',  name: 'A-FORGE Execution Shell',      port: 7071,  agentId: 'a-forge-mcp' },
];

/**
 * Tools that MUST be present on every organ for ALIGNED status.
 * If any canonical tool is missing → MISSING_CANONICAL.
 */
export const CANONICAL_TOOLS_PER_ORGAN: Record<string, string[]> = {
  arifos: ['arif_init', 'arif_observe', 'arif_think', 'arif_route', 'arif_memory', 'arif_judge', 'arif_forge', 'arif_seal'],
  geox: ['geox_basin', 'geox_petrophysics', 'geox_seismic_compute', 'geox_well_ingest', 'geox_surface_status'],
  wealth: ['capital_primitive', 'capital_health', 'capital_market', 'capital_registry'],
  well: ['well_assess_homeostasis', 'well_validate_vitality', 'well_registry_status'],
  aforge: ['forge_execute', 'forge_shell', 'forge_filesystem_read', 'forge_health_check'],
};
