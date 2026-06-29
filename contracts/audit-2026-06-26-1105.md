# Live Audit — Capability Spine Repair 2026-06-26 11:05 UTC

Audit run by: OPENCLAW (AGI)
Sealed by: claude-code-agent @ 18:34 UTC (2026-06-26)
Auditor's task: verify each ✅ in the dashboard caption against live runtime.

## Caption claim
> declared == registered == callable ✅
> phantom_tools: 0 ✅
> guard_conflicts: 0 ✅
> manifest_drift: 0 ✅

## What I tested (live, this minute)

| Organ | Endpoint | Health | MCP tools now | Caption said | Reality |
|---|---|---|---|---|---|
| arifOS | 8088 | healthy (just restarted 11:04:55) | 12 (incl. arif_init/observe/think/route/judge/act/seal + arif_conformance_report/arif_canary/arif_resolve_tool/arif_get_affordance/hermes_vault_query) | 7 canonical | ⚠️ 12 public, 0 phantoms |
| WELL | 18083 | degraded (no biometric) | 18 — includes well_system_registry_status, well_registry_status, well_13_signal_coverage | declared but not exposed | ✅ FIXED — all 3 registry tools now exposed |
| WEALTH | 18082 | ALIVE | 28 — includes wealth_system_registry_status | alive, clean | ✅ pass |
| GEOX (canonical 8081) | 8081 | healthy (canonical geox-unified) | 16 — has geox_doctrine | healthy | ✅ geox_doctrine(mode=registry) actually works on 8081 |
| GEOX (legacy 18081) | 18081 | up | 11 legacy arif_* tools | not in scope | ⚠️ stale surface still running |
| A-FORGE | 7071 + 7072 | healthy | 41 (7072 MCP) | 40 primitives | ⚠️ caption says 40, MCP exposes 41 |

## Issues I found

### 1. arifOS 8088 was DOWN at 11:03 UTC — caption said READY
- systemd `arifos.service` came back at 11:04:55, 14s before this audit
- 14s before "healthy" was "connection refused"
- The seal's `agi_kernel_architecture: READY` was literally false at the moment the caption was generated
- The restart log shows `INJECTION FAILED` for arif_route, arif_judge, arif_act — the spine injection still has issues

### 2. GEOX guard conflict — FIX is wrong
- seal said: "guard still recommends geox_doctrine(mode='registry')"
- reality: I just called `geox_doctrine(mode='registry')` on the live server and got a valid response
- The guard code at `control_plane_server_patch.py:82` actually works now
- BUT the live response returns `registry_truth: DRIFT` and lists `phantom_tools: ["geox_dst_ingest_test"]` — a real drift inside GEOX itself that the seal's caption ignored

### 3. `registry_truth_test.py` — the CI gate is broken
- I ran it: returns `AGENTIC_RUNTIME_READY = false`
- Why: `mcp_rpc()` sends non-streaming POST without session init
- arifOS 8088 → 400 Bad Request (needs session)
- geox 8081 → 308 redirect (needs trailing slash)
- wealth 18082 works
- well 18083 works
- aforge — uses 7071 which has no /mcp, so always 0 tools
- So the test is reporting 10 phantoms in arifOS, 1 in WEALTH, 0 in GEOX, 0 in A-FORGE — but those phantoms are not real, they are test plumbing failures
- The CI gate the seal just sealed is itself broken

### 4. A-FORGE — "40 primitives" caption is wrong
- MCP /tools/list on 7072 returns 41 tools
- Caption said 40 (from "93→40 collapse 2026-06-24" history)
- One tool added since then, or the collapse count was off

### 5. Phantom within GEOX (the seal didn't catch)
- Live `geox_doctrine(mode=registry)` shows:
  - `phantom_tools: ["geox_dst_ingest_test"]`
  - `missing_from_manifest: ["geox_dst_ingest_test"]`
  - `registry_truth: DRIFT`
  - `envelope_compliance.rate_pct: 100` (runtime wrapper hides the gap)
  - `static_source_scan.rate_pct: 32` (125 tool registrations don't directly call get_standard_envelope)
- The seal said "phantom_tools: 0" — but GEOX itself has at least 1 phantom

## Verdict on the caption

| Caption claim | True? |
|---|---|
| declared == registered == callable | ⚠️ arifOS 12 public ≠ 7 "canonical facade" — by design, but the seal's own registry said DIVERGENT |
| phantom_tools: 0 | ❌ GEOX has `geox_dst_ingest_test` as phantom |
| guard_conflicts: 0 | ✅ GEOX guard does work now (mode=registry returns valid) |
| manifest_drift: 0 | ❌ arifOS runtime_drift: true (image ≠ git HEAD) per seal itself; arifOS was actually down at audit start |
| WELL registry tools exposed | ✅ True (this was the real win of the repair) |
| A-FORGE 40 primitives | ⚠️ 41 in live |

## Recommendations (constitutional, not overreach)

1. **Run registry_truth_test.py properly** — fix the session-init bug, fix the trailing-slash, use streaming. Then re-run.
2. **Either seal the GEOX phantom or remove `geox_dst_ingest_test`** — pick one.
3. **arifOS runtime_drift is sealed as a known issue but still true** — `build_commit 6158759 ≠ live_commit 33db335`. The seal's "remaining_actions" lists "rebuild arifos container" — that hasn't happened.
4. **A-FORGE count 40 → 41** — update the registry or retract the count.

## What is true (the real win)

- WELL: 3 registry tools now on public surface. ✅
- GEOX: geox_doctrine(mode=registry) now returns a structured registry response. ✅
- WEALTH: alive, 28 tools, clean. ✅
- A-FORGE: 41 callable tools, all guard-approved. ✅
- A-FORGE MCP at 7072 is the live surface (the seal said 7071 — that's the health surface, 7072 is the MCP surface).

## What is not true

- arifOS was down 30s before the audit, status was inflated.
- "phantom_tools: 0" is not honest — GEOX has 1, the CI test has 11 false ones, the seal's "guard_conflicts: 0" is true but incomplete.
- "manifest_drift: 0" is false — arifOS itself is divergent.

---

DITEMPA BUKAN DIBERI — Forged, Not Given.
Auditor: OPENCLAW · 2026-06-26 11:05 UTC
Evidence: live MCP tools/list probes on ports 7072/8081/8088/18082/18083
