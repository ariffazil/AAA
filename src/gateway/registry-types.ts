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
export type MutationAuthority = 'NOT_EVALUATED' | 'HOLD' | 'DENIED';
// NOTE: AUTHORIZED removed. Only arifOS kernel/judge/SCT can grant authority.

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
  inputSchemaHash?: string;   // SHA-256 of inputSchema (MCP schema alignment)
  outputSchemaHash?: string;  // SHA-256 of outputSchema
  descriptionHash?: string;   // SHA-256 of description text
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
  /** MCP protocol state */
  mcpInitialized: boolean;
  mcpNegotiatedVersion?: string;
  mcpSessionId?: string;
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

/** Session D v1 — backward compatibility */
export interface ConformanceArtifactV1 {
  schemaVersion: 'session-d.v1';
  generatedAt: string;
  runtimeCommit: string;
  registryHash: string;
  freshnessMs: number;
  organs: OrganStatus[];
  duplicates: DuplicateEntry[];
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

/** v2 — Federation Conformance Artifact with MCP/A2A protocol dimensions */
export interface ConformanceArtifact {
  schemaVersion: 'federation-conformance.v2';
  generatedAt: string;
  runtimeCommit: string;
  registryHash: string;
  freshnessMs: number;

  /** Organ-level status (5 dimensions per organ) */
  organs: OrganStatus[];
  duplicates: DuplicateEntry[];

  /** Identity: who we verified */
  identity: {
    internalRegistryId: string;
    agentCardHash?: string;
    signatureVerified: boolean;
  };

  /** A2A protocol conformance */
  a2a: {
    cardSchemaValid: boolean;
    selectedInterface?: { url: string; protocolBinding: string; protocolVersion: string };
    taskLifecycleTest?: 'PASS' | 'FAIL' | 'NOT_RUN';
    streamingTest?: 'PASS' | 'FAIL' | 'NOT_ADVERTISED';
    pushTest?: 'PASS' | 'FAIL' | 'NOT_ADVERTISED';
  };

  /** MCP protocol conformance */
  mcp: {
    initialized: boolean;
    negotiatedProtocolVersion?: string;
    sessionBound: boolean;
    serverCapabilities?: Record<string, unknown>;
    toolNameAlignment: number;   // count of tools where name matches declared
    toolSchemaAlignment: number; // count of tools where schema hash matches
    toolsPerOrgan: Record<string, { declared: number; callable: number; schemaMatched: number }>;
  };

  /** Governance dimensions — authority is NEVER derived from registry */
  governance: {
    actorBound: boolean;
    traceBound: boolean;
    judgeReceiptVerified: boolean;
    vaultReceiptVerified: boolean;
    mutationAuthority: 'NOT_EVALUATED' | 'HOLD' | 'AUTHORIZED' | 'DENIED';
  };

  /** Summary */
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

export type { ConformanceArtifactV1 };

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
