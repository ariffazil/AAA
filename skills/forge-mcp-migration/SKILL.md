---
name: FORGE-mcp-migration
description: Migrate Python MCP organs to FastMCP 4.x — staging isolation, 8-receipt validation, rollback proof. Use when upgrading any Python organ's fastmcp dependency, planning a stateless MCP migration, or running the WELL/GEOX/WEALTH/arifOS organ upgrade path.
---

# FastMCP 4 Migration — Staging & Validation Playbook

> **Forged:** 2026-08-11 (first proven run: WELL :18083 → staging :28083, 8/8 receipts PASS)
> **For all AAA agents:** Hermes, OpenClaw, OpenCode, Kimi Code, Codex, AGY CLI
> **Authority:** F13 SOVEREIGN

## Iron Rule

**FastMCP 4 is beta as of 2026-08-11** (`4.0.0b2`). Never touch production first. Every migration runs in an isolated staging venv on a dedicated port, with a pre-mutation backup of the production venv. Rollback is provable via test #8.

## When to Use

- Upgrading any federation organ's `fastmcp` dependency (WELL, GEOX, WEALTH, arifOS)
- Validating that an organ speaks MCP 2026-07-28 (stateless) or 2025-11-25 (legacy)
- Planning the org-wide migration order (WELL → GEOX → WEALTH → arifOS)
- Deciding whether to wait for FastMCP 4.0.0 GA vs. apply beta to staging
- Diagnosing migration failures (breaking changes, middleware errors, SESSION_MISSING blocks)

## Pre-Migration Checklist

Before any FastMCP 4 work begins:

- [ ] Production venv path known (e.g. `/root/WELL/.venv`)
- [ ] Pre-mutation backup planned: `mv .venv .venv.bak.$(date +%Y%m%d)`
- [ ] Production port known and isolated from staging (e.g. prod `:18083`, staging `:28083`)
- [ ] 8-receipt test matrix ready (see ``references/``)
- [ ] Wave A/B/C/D tool classification done for the organ
- [ ] `_EXEMPT_TOOLS` candidates identified for read-only tools
- [ ] FastMCP 4 changelog reviewed for breaking changes (3 known — see `references/breaking-changes.md`)

## Staging Isolation Recipe (F1 AMANAH preserved)

```bash
# Step 1: Snapshot production venv — instant rollback safety
mv /root/<ORGAN>/.venv /root/<ORGAN>/.venv.bak.$(date +%Y%m%d)

# Step 2: Clone to staging venv (separate, isolated)
python3.12 -m venv /root/<ORGAN>/.venv.staging

# Step 3: Install FastMCP 4 beta + mcp SDK v2 in staging ONLY
# Note: 4.x requires --pre flag to find beta
/root/<ORGAN>/.venv.staging/bin/pip install --pre "fastmcp[tasks]==4.0.0b2" "mcp==2.0.0"

# Step 4: Copy production server.py → server.staging.py (never edit production!)
cp /root/<ORGAN>/server.py /root/<ORGAN>/server.staging.py

# Step 5: Set staging port via env var (production hardcodes its own port)
export <ORGAN>_STAGING_PORT=2<PROD_PORT>  # e.g. WELL_STAGING_PORT=28083

# Step 6: Launch staging in background, separate from production
/root/<ORGAN>/.venv.staging/bin/python /root/<ORGAN>/server.staging.py &
STAGING_PID=$!
echo "Staging PID: $STAGING_PID"

# Step 7: Verify staging is up on the NEW port (NOT the production port)
sleep 6
curl -sf http://127.0.0.1:2<PROD_PORT>/health
# Expected: healthy, with FastMCP version reflected
```

**Production never restarts during staging work.** If you need to "test production," you're not testing — you're deploying.

## 8-Receipt Test Matrix

Run this matrix against staging before declaring migration successful. **All 8 must pass.** See ``references/`` for the full curl commands.

| # | Test | Pass criterion |
|---|------|----------------|
| 1 | `initialize` (2026-07-28) | Server negotiates or falls back to 2025-11-25 |
| 2 | `tools/list` | Non-empty tool array |
| 3 | `tools/call <read-only>` (stateless) | No SESSION_MISSING error for exempt tool |
| 4 | `initialize` (2025-11-25, dual-era) | Server accepts legacy protocol |
| 5 | `tools/call <read-only>` (stateless, repeat) | Idempotent result |
| 6 | `tools/call <mutate>` (no session) | Properly blocked (SESSION_MISSING or auth error) |
| 7 | `traceparent` propagation (W3C) | Header accepted, no 400 |
| 8 | rollback — kill staging, verify prod | Production health unchanged before/during/after |

**Pass format for each test:** `Test N: PASS — <one-line evidence>`

## 3 Known Breaking Changes (FastMCP 3.x → 4.x)

See `references/breaking-changes.md` for full details.

| # | Change | Symptom | Fix |
|---|--------|---------|-----|
| 1 | Accept-headers method renamed | `_check_accept_headers` no longer exists | Rewrite monkey-patches as `async def _patched(self, request, scope, send)` |
| 2 | TasksExtension separated from core | `@mcp.tool(task=True)` silently broken | Install `fastmcp-tasks==4.0.0b2` + call `mcp.add_extension(TasksExtension())` |
| 3 | Strict `clientCapabilities` enforcement | Stateless clients get `-32602` | Always emit `clientCapabilities` in `_meta` |

## Rollback Path (if staging breaks mid-run)

```bash
# 1. Kill staging
kill $STAGING_PID

# 2. Confirm staging port is free
ss -tlnp | grep 2<PROD_PORT>  # should return nothing

# 3. Verify production is still untouched
curl -sf http://127.0.0.1:<PROD_PORT>/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'PROD: tool_count={d.get(\"tool_count\")} status={d.get(\"status\")}')"

# 4. (If needed) Restore production venv from backup
# mv /root/<ORGAN>/.venv.bak.<DATE> /root/<ORGAN>/.venv
# systemctl restart <organ>.service
```

**Rollback must complete in <30 seconds.** If it takes longer, the staging port is leaking into production — check systemd for accidental service creation.

## Migration Order (proven path)

Per F13 SOVEREIGN directive (2026-08-11):

```
WELL staging → 8/8 PASS → promote to production
GEOX staging → 8/8 PASS → promote to production
WEALTH staging → 8/8 PASS → promote to production
arifOS staging → 8/8 PASS → promote to production (LAST — highest risk)
```

Wait for **FastMCP 4.0.0 GA** before promoting any staging to production. Use A-FORGE Node.js (already on MCP SDK v2) as the production proving ground in the interim.

## Wave A/B/C/D Tool Classification

When auditing a tool surface for stateless migration, classify each tool:

| Wave | Definition | Migration cost | Examples |
|------|------------|----------------|----------|
| **A** | Stateless ready — pure compute, read-only | 0.5 days | `forge_health_check`, `forge_search`, `forge_fetch` |
| **B** | ACT migration — mutates, but doesn't need session continuity | 2-5 days | `forge_browser_*`, `forge_github_create_*` |
| **C** | Stateful — session continuity IS the model | keep | `forge_witness`, `forge_scar_*` |
| **D** | Long-running — async jobs need opaque ID | defer | `forge_pipeline_run`, `forge_sandbox_*` |

**Handler body inspection heuristic** — regex signals:

```
session_id, sessionstore, mcpsession → category=C, requires_session=True
act_v1, sct_v1, actor_id → requires_act=True
vault.write, write_file, cursor.execute → category=B
asyncio.create_task, subprocess, pipeline → category=D
seal, witness, scar, ledger → category=C
callmcp, bridge → category=C (depends on target)
none + readonly → category=A
```

**Confidence: ~75%** — always manually inspect the 4-5 most ambiguous tools before classification.

See ``references/`` for the full taxonomy and reference implementation.

## Quality Checklist (before declaring SEAL)

- [ ] Production venv backed up to `.venv.bak.<DATE>`
- [ ] Production health probed BEFORE staging run (baseline)
- [ ] 8-receipt test matrix: 8/8 PASS with evidence per test
- [ ] Production health probed AFTER staging run (unchanged)
- [ ] Rollback documented and tested (test #8)
- [ ] Staging artifacts in `_quarantine/` after FastMCP 4 GA ships
- [ ] F13 SOVEREIGN ratification if promoting staging → production

## When NOT to Use

- **To build new MCP servers** — use `FORGE-fastmcp` (the building skill)
- **To test existing MCP servers** — use `FORGE-mcp-testing` (testing skill)
- **To migrate A-FORGE Node.js** — A-FORGE is on MCP SDK v2 already (different path)
- **To skip staging** — never. Even "small" upgrades have broken in production.

## Linked References

- `references/breaking-changes.md` — FastMCP 4 API changes with code examples
- ``references/`` — Full curl commands for all 8 tests
- ``references/`` — Handler body inspection methodology
- ``references/`` — WELL 8/8 PASS reference run details

---

*Forged 2026-08-11 by 333-AGI under F13 SOVEREIGN directive. DITEMPA BUKAN DIBERI.*


<!-- dead-pointer sweep 2026-10-23: artifacts that could not be located were replaced with the references/ directory; see audit JSON for the missing basenames. -->
