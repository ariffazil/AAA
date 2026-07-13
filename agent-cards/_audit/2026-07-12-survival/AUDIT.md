# SURVIVAL OF THE FITTEST — Federation Audit
**Date:** 2026-07-12
**Operator:** kimi-code (FI-003)
**Scope:** All federation organs — arifOS :8088, A-FORGE :7072, GEOX :8081, WEALTH :18082, WELL :18083, AAA :3001
**Authority:** F13 SOVEREIGN · arifOS kernel → AAA cockpit → A-FORGE stdio

---

## TL;DR

- **182 tools** across 5 organs. **0 cross-organ duplicates.** No chaos at the surface boundary.
- **4 contradictions** found across agent-card + registry layers.
- **3 resolved** (zombie card archived, 2 stale FI-009 claims corrected).
- **1 deferred** (deprecated WELL tools — KEEP, in-window deprecation honored).
- All 27 active agent cards **signed and re-verified**.
- Gateway **restarted clean**: discovery count 43 → 42, vault chain seq 62 SEAL, 0 zombies.

---

## Phase 1: Inventory (live MCP probe)

| Organ | Port | Tools | Resources | Prompts |
|-------|------|-------|-----------|---------|
| **arifOS**  | 8088  |   8 |  259 | 13 |
| **A-FORGE** | 7072  | 102 |    5 | 14 |
| **GEOX**    | 8081  |  31 |   31 | 14 |
| **WEALTH**  | 18082 |  12 |   15 |  7 |
| **WELL**    | 18083 |  29 |   30 | 15 |
| **TOTAL**   |       | **182** | **340** | **63** |

Probe method: `tools/list`, `resources/list`, `prompts/list` JSON-RPC with proper MCP
`Accept: application/json, text/event-stream` headers. GEOX required explicit session
initialization (`initialize` → `mcp-session-id` header → subsequent calls). Session ID was
`db2b082ec79342f39867b9185583b22a`.

Inventory JSON: `agent-cards/_audit/2026-07-12-survival/inventory.json` (848 KB).
Post-cleanup inventory: `inventory-post-cleanup.json`.

---

## Phase 2: Contradictions Identified

### C1 — Zombie agent card (777-forge) [RESOLVED]
- **Path:** `agent-cards/extensions/777-forge/agent-card.json`
- **Status:** `status: archived`, `retired_at: 2026-07-02T15:40:00Z`
- **Reason given:** "Protocol band-aid. Agent that receives the task IS the executor.
  No meta-executor needed. Witness protocol kept in `AAA/agents/protocols/777-forge-witness-protocol.md`."
- **Blast radius:** Mirrored in `a2a-server/agent-cards/extensions/777-forge.json`,
  `public/a2a/agents.json`, `dist/a2a/agents.json`. All four copies had `signature_present: true`
  and were being served by the live A2A gateway as `agentId: 777-forge`.

### C2 — Stale FI-009 claim (gemini-cli external copy) [RESOLVED]
- **Path A:** `agents/_external/gemini-cli/agent-card.json`
- **Path B:** `a2a-server/agent-cards/harnesses/gemini-cli.json`
- **Stale field:** `"fi_slot": "FI-009"` at 2 levels (top-level + metadata).
- **Truth:** Filesystem (`agent-cards/harnesses/fi-007-gemini-cli/`) and canonical
  registry (`registry/identity.yaml`) both say `FI-007`. The card itself had `id: FI-007`.
- **Cause:** Historical orphan-adapter allocation. The `auditNote` in
  `fi-007-gemini-cli/agent-card.json` records the saga: "Allocated FI-009 by Kimi Code
  (FI-008) Zen alignment 2026-07-12. Previously orphan adapter without FI slot." It then
  moved to FI-007 but the external mirror never caught up.

### C3 — Stale FI-009 claim (gemini-cli server mirror) [RESOLVED]
- Same as C2 but in `a2a-server/agent-cards/harnesses/gemini-cli.json`. Fixed in the same
  sweep.

### C4 — Deprecated WELL tools [DEFERRED — KEEP]
- `well_readiness` — description begins: "LEGACY ALIAS (deprecated 2026-07-12) →
  `well_validate_vitality(mode=\"readiness\")`. Target removal: 2026-09-01".
- `well_13_signal_coverage` — description begins: "[DEPRECATED — USE well_signal_coverage]
  This tool has been deprecated and replaced."
- **Why KEEP:** Production callers still bind to both:
  - `well_readiness` is referenced by **19 agent cards** (333-AGI, 555-ASI, 888-APEX,
    A-AUDIT, A-ARCHIVE, openclaw, all 9 harnesses, plus openclaw/a2a-server/identity),
    **telegram-miniapp production code** (`telegram-miniapp/api/index.ts:283`),
    `scripts/route_task.py:392`, and `explorer_federation_registry.json`.
  - `well_13_signal_coverage` is referenced by `contracts/capability-registry.yaml`,
    `contracts/readiness-gate.yaml`, `contracts/registry_truth_test.py`, and the
    organ card itself (`agent-cards/organs/well/agent-card.json`).
  - The replacement `well_signal_coverage` is universally wired in the new agent cards.
- **Decision:** Honor the documented deprecation windows. `well_readiness` has a published
  removal date (2026-09-01) — that is the authoritative deadline, not today (51 days early).
  Removing now would break production. `well_13_signal_coverage` removal is owned by the
  WELL organ itself (server-side); the agent-card layer has already migrated to
  `well_signal_coverage`.

### C5 — Documentation drift (out of scope, noted) [DOCUMENTED, NOT FIXED]
- `agents/_docs/AGENT_REGISTRY.md` and `agent-skill-binding-map.md` contain stale
  FI mappings (FI-009 = continue-cli / gemini-cli respectively). These are documentation
  files, not canonical registries. The canonical truth is `registry/identity.yaml` plus
  `SKILL_MANIFEST.json`. Drift in docs is a separate hygiene concern; not within scope
  of "federation surface cleanup."
- `public/a2a/agents.json` had `civ_path: "/agent-cards/harnesses/fi-009-agy/agent-card.json"`
  for FI-009 — a placeholder path. The actual agent is mesa-test-agent. This was a pre-existing
  registration drift; left for explicit F13 ratification since it requires creating the
  `fi-009-agy` directory or correcting the path.

---

## Phase 3: Decisions

| ID | Item | Decision | Rationale |
|----|------|----------|-----------|
| C1 | 777-forge | **ARCHIVE** | status=archived, retired_at stamped, no longer needed (witness protocol kept separately) |
| C2 | gemini-cli external FI-009 | **FIX → FI-007** | Filesystem truth + registry canonical |
| C3 | gemini-cli server mirror FI-009 | **FIX → FI-007** | Same |
| C4 | `well_readiness` / `well_13_signal_coverage` | **KEEP** | Active production callers + documented removal window |
| C5 | doc drift in `AGENT_REGISTRY.md` / `binding-map.md` | **OUT OF SCOPE** | Documentation only; canonical is `registry/identity.yaml` |

---

## Phase 4: Actions Executed

```
1. Archived agent-cards/extensions/777-forge → /root/AAA-archive/777-forge-2026-07-12/
   - Includes a2a-server mirror subfolder (777-forge.json also archived)
2. Removed 777-forge from public/a2a/agents.json   (43 → 42 entries)
3. Removed 777-forge from dist/a2a/agents.json     (29 → 28 entries)
4. Updated agents/_external/gemini-cli/agent-card.json:
     fi_slot: "FI-009" → "FI-007"  (top-level + metadata)
     auditNote rewritten to record canonical truth
5. Updated a2a-server/agent-cards/harnesses/gemini-cli.json:
     fi_slot: "FI-009" → "FI-007"  (recursive walk of nested structures)
6. Re-signed all modified cards via auth/sign_agent_card.py
7. Updated agent-cards/SKILL_MANIFEST.json audit_2026_07_12.survival_phase_5 trail
8. Restarted aaa-a2a.service (clean boot, vault chain seq 62 SEAL)
```

**Critical note on archive placement:** the gateway's `agent-card-registry.js` recursively
scans `agent-cards/` for JSON cards but does **not** skip `_*` directories. The archive was
first moved to `agent-cards/_archive/` and the gateway kept serving 777-forge. Final solution:
relocated the entire archive folder to `/root/AAA-archive/` (outside the scanned tree).
Gateway restart confirmed 777-forge absent from discovery.

---

## Phase 5: Verification Results

| Check | Before | After | Status |
|-------|--------|-------|--------|
| Live MCP tool count (5 organs) | 182 | 182 | ✓ unchanged (server-side untouched) |
| Live MCP resource count | 340 | 340 | ✓ unchanged |
| Live MCP prompt count | 63 | 63 | ✓ unchanged |
| Active agent cards (excl. _audit) | 28 | **27** | ✓ 777-forge archived |
| Unsigned / pending cards | 0 | **0** | ✓ all 27 signed |
| Gateway `/health` | healthy | **healthy** | ✓ |
| Gateway `/a2a/discover` count | 43 | **42** | ✓ -1 (777-forge removed) |
| 777-forge in discovery | yes | **no** | ✓ removed |
| Vault chain | seq 62 SEAL | **seq 62 SEAL** | ✓ |

---

## Files Written This Audit

- `agent-cards/_audit/2026-07-12-survival/AUDIT.md` (this file)
- `agent-cards/_audit/2026-07-12-survival/inventory.json` (pre-cleanup, 848 KB)
- `agent-cards/_audit/2026-07-12-survival/inventory-post-cleanup.json`
- `agent-cards/SKILL_MANIFEST.json` (audit_2026_07_12.survival_phase_5 trail added)

## Files Archived

- `/root/AAA-archive/777-forge-2026-07-12/agent-card.json`
- `/root/AAA-archive/777-forge-2026-07-12/skills.json`
- `/root/AAA-archive/777-forge-2026-07-12/a2a-server-mirror/777-forge.json`

## Recommendations for F13 (deferred, not executed without approval)

1. **WELL organ server-side removal** — When 2026-09-01 arrives, remove `well_readiness`
   and `well_13_signal_coverage` from the WELL MCP server. This requires WELL server restart.
   Currently 51 days early; removing now breaks telegram-miniapp production.
2. **FI-009 civ_path** — Either create `agent-cards/harnesses/fi-009-agy/` with a proper
   mesa-test-agent card, or fix `public/a2a/agents.json` civ_path to point to mesa-test-agent's
   actual location.
3. **`fi-007-gemini-cli/agent-card.json` auditNote** — Could be simplified now that the
   external mirrors are aligned; currently still carries the historical "previously FI-009"
   narrative. Low priority.
4. **Doc drift cleanup** — `agent-skill-binding-map.md` and `agents/_docs/AGENT_REGISTRY.md`
   should be regenerated from `registry/identity.yaml` (single source of truth).
   This is documentation-only and out of the chaos-removal scope.

---

*DITEMPA BUKAN DIBERI — sealed at 2026-07-12T23:53Z · vault chain seq 62 · ARIF verdict*
