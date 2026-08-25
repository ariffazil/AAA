# arifOS MCP Audit Report

**Date:** 2026-06-23T11:08:00Z  
**Auditor:** kimi-code (Constitutional Clerk)  
**Target:** arifOS MCP constitutional kernel (`/root/arifOS`, port 8088)  
**Deployed commit:** `6b87733`  
**Working-tree HEAD:** `a98ba22` (`freeze(kernel): canonical 16-tool surface — aliases removed from wire`)

---

## Executive Summary

arifOS MCP is **healthy and serving traffic**, but the runtime is in a **drift state**. The systemd service is running an image built from commit `6b87733`, while the working tree has advanced to `a98ba22` and contains uncommitted changes. The health endpoint now reports `runtime_drift: true`. A subset of the test suite fails on this drift, and there are outstanding lint errors in `arifosmcp/server.py`.

| Area | Verdict |
|---|---|
| Service availability | ✅ Healthy |
| Runtime drift | ⚠️ TRUE (live commit ≠ build commit) |
| Test suite (fast subset) | ⚠️ 10 failed, 164 passed, 21 deselected |
| Conformance spine | ⚠️ 7/9 PASS (2 explained failures) |
| Lint (ruff) | ⚠️ 4 errors (E731) |
| Static discovery schema | ⚠️ Non-standard shape (`tools` is object, not array) |
| VAULT999 health | ✅ healthy |

---

## 1. Service Health

```bash
systemctl is-active arifos arifosd vault999-api vault999-writer f11-bridge
# -> active active active active active

curl -s http://localhost:8088/health
```

Key health fields:

| Field | Value |
|---|---|
| `status` | healthy |
| `service` | arifOS-mcp |
| `version` | kanon-6b87733 |
| `git_commit` | 6b87733 |
| `live_commit` | a98ba22 |
| `build_commit` | 6b87733 |
| `runtime_drift` | **true** |
| `tools_loaded` | 16 |
| `canonical_tools_loaded` | 16 |
| `floors_active` | 13 |
| `floors_enforcement` | active |
| `vault999_health` | healthy |
| `surface_consistency.verdict` | CONSISTENT |

**Interpretation:** The MCP server is operationally healthy, but the running code does not match the deployed build image. The working tree is one commit ahead (`a98ba22`) and has additional uncommitted changes.

---

## 2. Git / Deployment Drift

### Commits

```text
a98ba22 freeze(kernel): canonical 16-tool surface — aliases removed from wire
6b87733 feat(kernel): align capability_map + static discovery with live arif_* canonical surface
```

### Uncommitted changes

```bash
cd /root/arifOS
git status --short
```

```text
 M deploy/vault999-writer/main.py
?? arifosmcp/cli/
```

### Modified: `deploy/vault999-writer/main.py`

- Adds `agent_id` column to two `INSERT INTO vault_seals` statements.
- Maps `req.agent_id` to both the `actor_id` and `agent_id` columns.
- This appears to be a schema-alignment change for VAULT999 writer, but it is **not committed**.

### Untracked: `arifosmcp/cli/`

New CLI subcommand package:

- `arifosmcp/cli/__init__.py`
- `arifosmcp/cli/check.py`
- `arifosmcp/cli/common.py`
- `arifosmcp/cli/judge.py`
- `arifosmcp/cli/main.py`
- `arifosmcp/cli/seal.py`

`server.py` already contains a CLI dispatch block that routes `check`, `judge`, `seal`, `help` to `arifosmcp.cli.main`. The CLI package is present on disk but **untracked**.

### Impact

- The live service reports `runtime_drift: true`.
- AGI-kernel readiness tests fail on `runtime_drift`.
- The deployment is not reproducible from `origin/main`.

---

## 3. Phase 3 Surface Freeze

HEAD `a98ba22` removes SDK long-name aliases from the public wire surface:

- `CANONICAL_LONG_NAME_ALIASES` remain defined in `public_surface.py` but are **excluded** from `CANONICAL13_PUBLIC_SURFACE` and `EXPANDED_45`.
- `ARIFOS_MCP_DUAL_MODE` defaults to false; the alias shim is disabled.
- Public surface is now **16 tools**: 15 canonical short names + 1 canary probe.

This is a significant contract change. The live service still runs the pre-freeze commit `6b87733`, so the freeze has **not been deployed**.

---

## 4. Test Results

### Fast subset (`not e3e and not slow`)

```bash
timeout 120 python -m pytest tests/ -m 'not e3e and not slow' --maxfail=10 -q --tb=line
```

```text
10 failed, 164 passed, 21 deselected, 18 warnings in 51.67s
```

### First 10 failures

| Test | Failure |
|---|---|
| `test_post_observe_gate.py::test_hantu_consciousness_claim_warns` | AssertionError |
| `test_post_observe_gate.py::test_soul_claim_warns` | AssertionError |
| `test_001_light_bootstrap_returns_session.py::test_light_bootstrap_next_actions_are_manifest_backed` | `light bootstrap should expose next_actions` (got `[]`) |
| `test_002_full_init_bound_session.py::test_full_binds_all_floors` | `initialize did not return mcp-session-id` |
| `test_002_full_init_bound_session.py::test_full_mutation_allowed` | `initialize did not return mcp-session-id` |
| `test_003_surface_rsi_canonical13.py::test_health_runtime_drift_false` | `runtime_drift must be false for Level 1+, got True` |
| `test_004_actor_identity_no_drift.py::test_actor_verified_true_under_light` | `initialize did not return mcp-session-id` |
| `test_004_actor_identity_no_drift.py::test_actor_id_echoed` | `initialize did not return mcp-session-id` |
| `test_004_actor_identity_no_drift.py::test_actor_not_anonymous_when_declared` | `initialize did not return mcp-session-id` |
| `test_005_reasoning_structured_output.py::test_mind_reason_returns_structured` | `initialize did not return mcp-session-id` |

### Root-cause clustering

1. **Runtime drift** — one direct failure in `test_003_surface_rsi_canonical13`.
2. **MCP initialize response missing `mcp-session-id`** — multiple AGI-readiness tests fail because the initialize handshake does not return the expected session header. This may be caused by the Phase 3 surface/interceptor changes or by drift between the running image and the test code.
3. **Post-observe gate ABIS assertions** — two tests expect warnings that are not being raised.

### Full suite

A broader run without `--maxfail` exceeded the 300-second timeout before completing. The test suite is currently too slow to run to completion in this state.

---

## 5. Conformance Spine (ARIF Conformance Spine v0.2)

```bash
arif_conformance_report
```

| Check | Verdict |
|---|---|
| arifos_alive | PASS |
| mcp_initialize | PASS |
| protocol_version | PASS |
| schema_echo_stable | PASS |
| session_starts | PASS |
| authority_checked | PASS |
| hold_blocks_mutation | PASS |
| vault_replay | FAIL |
| cooling_ledger | FAIL |

**Score:** 7/9  
**Substrate gate:** AMBER  
**Verdict:** EXPLAINED_BROKEN

### Explained failures

1. **vault_replay** — `hermes_vault_query` returned no entries / non-OK status. The vault file is present but the query interface did not return a recognisable entry.
2. **cooling_ledger** — `chain_integrity: BROKEN`, no WELL entropy seals found. This matches the documented sovereign ruling: pre-May-2026 migration gaps (ids 18-60) are a known non-issue.

The verifier is honest and explains its warnings; no unexplained critical evidence.

---

## 6. Lint / Static Analysis

```bash
ruff check arifosmcp/server.py arifosmcp/runtime/public_surface.py arifosmcp/runtime/alias_shim.py
```

Found **4 errors**, all in `arifosmcp/server.py`:

```text
E731 Do not assign a `lambda` expression, use a `def`
    arifosmcp/server.py:1632:9  (_f = lambda k: ...)
    arifosmcp/server.py:1633:9  (_n = lambda k: ...)
```

(Reported as 4 errors because the lambdas appear in multiple code paths / repeated in output.)

---

## 7. Static Discovery Schema

File: `static/.well-known/mcp/server.json`

| Field | Value |
|---|---|
| `$schema` | `https://static.modelcontextprotocol.io/schemas/mcp-server-card/v1.json` |
| `tools` type | **Object** (`{ count, frozen, naming, canonical: [...] }`) |
| `tools.count` | 16 |
| `tools.canonical` length | 16 |
| `aliases` | 0 |

**Note:** The standard MCP server-card schema expects `tools` to be an **array** of tool descriptor objects. The current file uses a custom object shape with a nested `canonical` array. Clients that expect the standard schema may fail to parse the discovery document.

---

## 8. Recommendations

1. **Commit or reset the uncommitted changes.** Either:
   - Commit the `vault999-writer/main.py` schema fix and the new `arifosmcp/cli/` package, or
   - Stash/revert them if they are experimental, to eliminate `runtime_drift`.

2. **Deploy the Phase 3 freeze.** The running image (`6b87733`) is behind HEAD (`a98ba22`). After tests pass, restart the `arifos` service from the clean commit.

3. **Fix MCP initialize session ID.** The AGI-readiness tests cannot complete initialize. Investigate whether the Phase 3 interceptor or transport layer is stripping the `mcp-session-id` response header.

4. **Fix ruff E731 lint errors** in `arifosmcp/server.py`.

5. **Reconcile the static discovery schema** with the MCP server-card specification, or document the custom shape if it is intentional.

6. **Run the full test suite** after drift is cleared. The current `--maxfail=10` subset already shows 10 failures; a full run is needed to assess total regression scope.

7. **Schedule a VAULT999 writer restart** after committing the `agent_id` column change, so the writer matches the new schema.

---

## 9. Telemetry

```json
{
  "audit_target": "arifOS MCP",
  "deployed_commit": "6b87733",
  "working_tree_head": "a98ba22",
  "runtime_drift": true,
  "service_status": "healthy",
  "conformance_score": "7/9",
  "fast_test_result": "10 failed, 164 passed, 21 deselected",
  "ruff_errors": 4,
  "uncommitted_files": 1,
  "untracked_dirs": ["arifosmcp/cli/"],
  "vault999_health": "healthy",
  "floors_active": 13
}
```

---

*No files were mutated during this audit.*
