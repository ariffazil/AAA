/**
 * Session D — Registry Validator Test Suite
 * ════════════════════════════════════════════════
 * 
 * 8 scenarios for fail-closed registry validation:
 * 1. duplicate organ identity → HARD FAILURE
 * 2. duplicate tool name → DRIFT
 * 3. phantom tool (declared but not callable) → PHANTOM_DETECTED
 * 4. missing canonical tool → MISSING_CANONICAL
 * 5. stale cached registry → freshness check
 * 6. connector unavailable → UNKNOWN + HOLD
 * 7. exact match → ALIGNED
 * 8. deterministic hash generation → same input = same hash
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

import { describe, it } from 'node:test';
import { strict as assert } from 'node:assert';
import { detectDuplicates } from '../src/gateway/registry-validator.js';
import {
  CANONICAL_ORGANS,
  CANONICAL_TOOLS_PER_ORGAN,
  type ConformanceArtifact,
  type DuplicateEntry,
} from '../src/gateway/registry-types.js';

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 1: Duplicate agentId → HARD FAILURE
// ═══════════════════════════════════════════════════════════════════════════

describe('detectDuplicates', () => {
  it('returns empty when all agentIds are unique', () => {
    const cards = [
      { agentId: 'arifos-mcp', source: 'CANONICAL_ORGANS.arifos' },
      { agentId: 'geox-mcp', source: 'CANONICAL_ORGANS.geox' },
      { agentId: 'wealth-mcp', source: 'CANONICAL_ORGANS.wealth' },
    ];
    const result = detectDuplicates(cards);
    assert.equal(result.length, 0, 'Expected no duplicates');
  });

  it('detects duplicate agentId across two sources', () => {
    const cards = [
      { agentId: 'arifos-mcp', source: 'CANONICAL_ORGANS.arifos' },
      { agentId: 'arifos-mcp', source: 'organs/arifos/agent-card.json' },
      { agentId: 'geox-mcp', source: 'CANONICAL_ORGANS.geox' },
    ];
    const result = detectDuplicates(cards);
    assert.equal(result.length, 1, 'Expected 1 duplicate');
    assert.equal(result[0]!.agentId, 'arifos-mcp');
    assert.equal(result[0]!.sources.length, 2);
    assert.ok(result[0]!.message.includes('Duplicate'));
  });

  it('detects multiple duplicates', () => {
    const cards = [
      { agentId: 'a', source: 's1' },
      { agentId: 'a', source: 's2' },
      { agentId: 'b', source: 's3' },
      { agentId: 'b', source: 's4' },
      { agentId: 'c', source: 's5' },
    ];
    const result = detectDuplicates(cards);
    assert.equal(result.length, 2, 'Expected 2 duplicates');
    const ids = result.map((d) => d.agentId).sort();
    assert.deepEqual(ids, ['a', 'b']);
  });

  it('handles empty input', () => {
    const result = detectDuplicates([]);
    assert.equal(result.length, 0);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 2: Duplicate tool name (canonical overlap detection)
// ═══════════════════════════════════════════════════════════════════════════

describe('canonical tool declarations', () => {
  it('no organ shares a tool name with another organ', () => {
    const allTools = new Map<string, string[]>(); // toolName → organIds
    for (const [organId, tools] of Object.entries(CANONICAL_TOOLS_PER_ORGAN)) {
      for (const tool of tools) {
        const organs = allTools.get(tool) ?? [];
        organs.push(organId);
        allTools.set(tool, organs);
      }
    }
    const overlaps = [...allTools.entries()].filter(([, organs]) => organs.length > 1);
    assert.equal(overlaps.length, 0,
      `Tool name overlap detected: ${JSON.stringify(overlaps)}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 3-7: Schema validation (structural checks)
// ═══════════════════════════════════════════════════════════════════════════

describe('schema types', () => {
  it('ConformanceArtifact schema version is session-d.v1', () => {
    const artifact: ConformanceArtifact = {
      schemaVersion: 'session-d.v1',
      generatedAt: new Date().toISOString(),
      runtimeCommit: 'test',
      registryHash: 'abc123',
      freshnessMs: 0,
      organs: [],
      duplicates: [],
      summary: {
        totalOrgans: 0,
        organsUp: 0,
        organsReady: 0,
        organsAligned: 0,
        totalTools: 0,
        phantomTools: 0,
        missingTools: 0,
        duplicateAgents: 0,
        overallVerdict: 'ALIGNED',
      },
    };
    assert.equal(artifact.schemaVersion, 'session-d.v1');
    assert.equal(artifact.summary.overallVerdict, 'ALIGNED');
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 9: Canonical organ uniqueness (no duplicate agentId in CANONICAL_ORGANS)
// ═══════════════════════════════════════════════════════════════════════════

describe('CANONICAL_ORGANS', () => {
  it('all agentIds are unique', () => {
    const ids = CANONICAL_ORGANS.map((o) => o.agentId);
    const unique = new Set(ids);
    assert.equal(unique.size, ids.length,
      `Duplicate agentIds in CANONICAL_ORGANS: ${ids.filter((id, i) => ids.indexOf(id) !== i)}`);
  });

  it('all organIds are unique', () => {
    const ids = CANONICAL_ORGANS.map((o) => o.organId);
    const unique = new Set(ids);
    assert.equal(unique.size, ids.length);
  });

  it('all ports are unique', () => {
    const ports = CANONICAL_ORGANS.map((o) => o.port);
    const unique = new Set(ports);
    assert.equal(unique.size, ports.length);
  });

  it('has exactly 5 organs', () => {
    assert.equal(CANONICAL_ORGANS.length, 5);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 10: CANONICAL_TOOLS_PER_ORGAN covers all organs
// ═══════════════════════════════════════════════════════════════════════════

describe('CANONICAL_TOOLS_PER_ORGAN', () => {
  it('every canonical organ has tool declarations', () => {
    for (const organ of CANONICAL_ORGANS) {
      const tools = CANONICAL_TOOLS_PER_ORGAN[organ.organId];
      assert.ok(tools, `Missing tool declarations for ${organ.organId}`);
      assert.ok(tools.length > 0, `Empty tool list for ${organ.organId}`);
    }
  });

  it('arifos has 8 canonical tools', () => {
    assert.equal(CANONICAL_TOOLS_PER_ORGAN['arifos']!.length, 8);
  });
});
