/**
 * Session D — AAA Registry Validator (Fail-Closed)
 * ═════════════════════════════════════════════════════
 *
 * Core invariants:
 *   advertised_tool ∈ runtime_callable_registry
 *   Any violation → registry_state = DRIFT
 *   Duplicate agentId → HARD FAILURE (no silent overwrite)
 *   UP ≠ READY (liveness does not imply readiness)
 *   ALIGNED ≠ SEALED (alignment does not imply authority)
 *
 * Anti-Calhoun: every degraded state emits explicit DEGRADED event.
 * No silent pass. No except: pass without audit trace.
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

import * as crypto from 'node:crypto';
import {
  CANONICAL_ORGANS,
  CANONICAL_TOOLS_PER_ORGAN,
  type ConformanceArtifact,
  type DuplicateEntry,
  type OrganIdentity,
  type OrganStatus,
  type RegistryAlignment,
  type ToolEntry,
} from './registry-types.js';

// ── MCP Protocol ──────────────────────────────────────────────────────────

interface JsonRpcRequest {
  jsonrpc: '2.0';
  id: string;
  method: string;
  params: Record<string, unknown>;
}

interface JsonRpcResponse {
  jsonrpc: '2.0';
  id: string;
  result?: { tools: Array<{ name: string; description?: string }> };
  error?: { code: number; message: string };
}

// ── Configuration ─────────────────────────────────────────────────────────

const MCP_TIMEOUT_MS = 5000;
const LOCALHOST = '127.0.0.1';

// ── Helpers ───────────────────────────────────────────────────────────────

function sha256(data: string): string {
  return crypto.createHash('sha256').update(data).digest('hex').slice(0, 16);
}

function isoNow(): string {
  return new Date().toISOString();
}

// ── MCP Probe ─────────────────────────────────────────────────────────────

/**
 * Fetch tools/list from an organ's MCP endpoint.
 * Returns tool names on success, null on failure.
 */
async function fetchToolsList(port: number, organId: string): Promise<string[] | null> {
  const url = `http://${LOCALHOST}:${port}/mcp`;
  const request: JsonRpcRequest = {
    jsonrpc: '2.0',
    id: `aaa-registry-${organId}-${Date.now()}`,
    method: 'tools/list',
    params: {},
  };

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), MCP_TIMEOUT_MS);

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      console.error(`[registry-validator] ${organId}:${port} HTTP ${response.status}`);
      return null;
    }

    const body = (await response.json()) as JsonRpcResponse;
    if (body.error) {
      console.error(`[registry-validator] ${organId}:${port} JSON-RPC error: ${body.error.message}`);
      return null;
    }

    const tools = body.result?.tools ?? [];
    return tools.map((t) => t.name);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(`[registry-validator] ${organId}:${port} probe failed: ${message}`);
    return null;
  }
}

// ── Probe Single Organ ────────────────────────────────────────────────────

async function probeOrgan(organ: OrganIdentity): Promise<OrganStatus> {
  const probedAt = isoNow();
  const startMs = Date.now();

  // Phase 1: Transport probe (health check)
  let transportReachability: OrganStatus['transportReachability'] = 'UNKNOWN';
  let processLiveness: OrganStatus['processLiveness'] = 'UNKNOWN';

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), MCP_TIMEOUT_MS);
    const resp = await fetch(`http://${LOCALHOST}:${organ.port}/health`, {
      signal: controller.signal,
    });
    clearTimeout(timeout);
    processLiveness = resp.ok ? 'UP' : 'DOWN';
    transportReachability = 'UP';
  } catch {
    processLiveness = 'DOWN';
    transportReachability = 'DOWN';
  }

  // Phase 2: tools/list probe
  const liveTools = await fetchToolsList(organ.port, organ.organId);

  // Phase 3: Compare declared vs live
  const declaredTools = CANONICAL_TOOLS_PER_ORGAN[organ.organId] ?? [];
  const liveSet = new Set(liveTools ?? []);
  const declaredSet = new Set(declaredTools);

  const tools: ToolEntry[] = [];
  const phantomTools: string[] = [];
  const missingTools: string[] = [];

  // Check declared tools — are they callable?
  for (const name of declaredTools) {
    const callable = liveSet.has(name);
    tools.push({ name, declared: true, callable, tested: false });
    if (!callable) phantomTools.push(name);
  }

  // Check live tools not in declared set — missing from canon
  if (liveTools) {
    for (const name of liveTools) {
      if (!declaredSet.has(name)) {
        missingTools.push(name);
        tools.push({ name, declared: false, callable: true, tested: false });
      }
    }
  }

  // Phase 4: Registry alignment
  let registryAlignment: RegistryAlignment;
  if (liveTools === null) {
    registryAlignment = 'UNKNOWN';
  } else if (phantomTools.length > 0 && missingTools.length > 0) {
    registryAlignment = 'DRIFT';
  } else if (phantomTools.length > 0) {
    registryAlignment = 'PHANTOM_DETECTED';
  } else if (missingTools.length > 0) {
    registryAlignment = 'MISSING_CANONICAL';
  } else {
    registryAlignment = 'ALIGNED';
  }

  // Phase 5: Organ readiness
  let organReadiness: OrganStatus['organReadiness'];
  if (processLiveness === 'DOWN' || transportReachability === 'DOWN') {
    organReadiness = 'HOLD';
  } else if (registryAlignment === 'DRIFT' || registryAlignment === 'PHANTOM_DETECTED') {
    organReadiness = 'DEGRADED';
    console.warn(`[registry-validator] ${organ.organId} DEGRADED: ${phantomTools.length} phantom, ${missingTools.length} missing`);
  } else if (registryAlignment === 'ALIGNED') {
    organReadiness = 'READY';
  } else {
    organReadiness = 'UNKNOWN';
  }

  // Phase 6: Mutation authority — NEVER derived from liveness alone
  const mutationAuthority: OrganStatus['mutationAuthority'] =
    registryAlignment === 'ALIGNED' && organReadiness === 'READY'
      ? 'AUTHORIZED'
      : 'HOLD';

  const freshnessMs = Date.now() - startMs;

  return {
    identity: organ,
    processLiveness,
    transportReachability,
    registryAlignment,
    organReadiness,
    mutationAuthority,
    tools,
    phantomTools,
    missingTools,
    probedAt,
    freshnessMs,
  };
}

// ── Duplicate Detection ───────────────────────────────────────────────────

/**
 * Scan all loaded agent cards for duplicate agentId.
 * agentId is the unique key — two cards with same agentId = HARD FAILURE.
 * No last-write-wins. No silent overwrite.
 */
export function detectDuplicates(
  cards: Array<{ agentId: string; source: string }>,
): DuplicateEntry[] {
  const seen = new Map<string, string[]>();
  const duplicates: DuplicateEntry[] = [];

  for (const card of cards) {
    const sources = seen.get(card.agentId) ?? [];
    sources.push(card.source);
    seen.set(card.agentId, sources);
  }

  for (const [agentId, sources] of seen) {
    if (sources.length > 1) {
      duplicates.push({
        agentId,
        sources,
        message: `Duplicate agentId '${agentId}' found in ${sources.length} locations: ${sources.join(', ')}. Rejecting — no last-write-wins.`,
      });
      console.error(`[registry-validator] ${duplicates[duplicates.length - 1]!.message}`);
    }
  }

  return duplicates;
}

// ── Canonical Tool List Hash ──────────────────────────────────────────────

function computeRegistryHash(organs: OrganStatus[]): string {
  const canonical = organs
    .flatMap((o) => o.tools)
    .filter((t) => t.declared)
    .map((t) => t.name)
    .sort();
  return sha256(canonical.join(','));
}

// ── Main: Full Registry Validation ────────────────────────────────────────

export interface RegistryValidationOptions {
  /** Runtime commit hash for the conformance artifact */
  runtimeCommit?: string;
  /** Additional card sources to check for duplicates */
  cardSources?: Array<{ agentId: string; source: string }>;
}

/**
 * Run full fail-closed registry validation across all canonical organs.
 * 
 * 1. Probe each organ (transport + tools/list)
 * 2. Compare declared vs callable tools
 * 3. Detect phantom tools, missing tools
 * 4. Detect duplicate agentIds across cards
 * 5. Produce deterministic ConformanceArtifact
 * 
 * Returns the artifact. Throws on hard failures (duplicate agentId).
 */
export async function validateRegistry(
  options: RegistryValidationOptions = {},
): Promise<ConformanceArtifact> {
  const startMs = Date.now();
  const generatedAt = isoNow();

  // Phase 1: Probe all organs
  const organPromises = CANONICAL_ORGANS.map((organ) => probeOrgan(organ));
  const organs = await Promise.all(organPromises);

  // Phase 2: Detect duplicate agentIds (HARD FAILURE)
  const cardSources = options.cardSources ?? [];
  // Include organ identities as card sources
  for (const organ of CANONICAL_ORGANS) {
    cardSources.push({ agentId: organ.agentId, source: `CANONICAL_ORGANS.${organ.organId}` });
  }
  const duplicates = detectDuplicates(cardSources);

  if (duplicates.length > 0) {
    const dupIds = duplicates.map((d) => d.agentId).join(', ');
    throw new Error(
      `AAA_REGISTRY_HARD_FAIL: ${duplicates.length} duplicate agentId(s) detected: ${dupIds}. ` +
      `Boot blocked — resolve duplicates before starting AAA.`,
    );
  }

  // Phase 3: Compute summary
  const totalTools = organs.reduce((sum, o) => sum + o.tools.filter((t) => t.declared).length, 0);
  const phantomTools = organs.reduce((sum, o) => sum + o.phantomTools.length, 0);
  const missingTools = organs.reduce((sum, o) => sum + o.missingTools.length, 0);
  const organsUp = organs.filter((o) => o.processLiveness === 'UP').length;
  const organsReady = organs.filter((o) => o.organReadiness === 'READY').length;
  const organsAligned = organs.filter((o) => o.registryAlignment === 'ALIGNED').length;

  let overallVerdict: RegistryAlignment;
  if (organsAligned === organs.length && duplicates.length === 0) {
    overallVerdict = 'ALIGNED';
  } else if (duplicates.length > 0) {
    overallVerdict = 'DUPLICATE_DETECTED';
  } else if (phantomTools > 0) {
    overallVerdict = 'PHANTOM_DETECTED';
  } else {
    overallVerdict = 'DRIFT';
  }

  const registryHash = computeRegistryHash(organs);

  const artifact: ConformanceArtifact = {
    schemaVersion: 'session-d.v1',
    generatedAt,
    runtimeCommit: options.runtimeCommit ?? 'unknown',
    registryHash,
    freshnessMs: Date.now() - startMs,
    organs,
    duplicates,
    summary: {
      totalOrgans: organs.length,
      organsUp,
      organsReady,
      organsAligned,
      totalTools,
      phantomTools,
      missingTools,
      duplicateAgents: duplicates.length,
      overallVerdict,
    },
  };

  return artifact;
}

/**
 * Lightweight check: are all organs reachable?
 * Does NOT probe tools/list — just transport liveness.
 */
export async function quickHealthCheck(): Promise<Record<string, boolean>> {
  const results: Record<string, boolean> = {};
  const probes = CANONICAL_ORGANS.map(async (organ) => {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 2000);
      const resp = await fetch(`http://${LOCALHOST}:${organ.port}/health`, {
        signal: controller.signal,
      });
      clearTimeout(timeout);
      results[organ.organId] = resp.ok;
    } catch {
      results[organ.organId] = false;
    }
  });
  await Promise.all(probes);
  return results;
}
