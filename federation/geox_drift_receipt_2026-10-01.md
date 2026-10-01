# GEOX + MCP SKILL DRIFT RECEIPT — 2026-10-01

**Author lane:** 555 (read-only subagent, OBSERVE_ONLY mandate)
**Persisted by:** parent agent (Lane 555 had no Write tool, refused to author files, kept mandate)
**Status:** Read-only receipt. No production artifact was mutated.

---

## Provenance correction (load-bearing)

**The user's claim of three live RT1 rejections at "26 declared tools" is not substantiated by any receipt in the federation.**

Exhaustive scan across `/root/.claude/projects/-root/**/*.jsonl` yields **4 matches** with `RT1_GUARD: Tool '<name>' … has <N> declared`. **Every match reports 25, never 26.**

| timestamp | tool | declared count | source |
|---|---|---|---|
| 2026-09-19T15:12:59 | geox_well_desk_open | 25 | c2a76b7a-…jsonl |
| 2026-09-19T15:13:14 | geox_surface_status | 25 | c2a76b7a-…:352 |
| 2026-10-01T11:10:22 | geox_well_desk_open | 25 | agent-a048e6ecbef503911.jsonl |
| 2026-10-01T11:12:06 | geox_well_desk_open | 25 | agent-a048e6ecbef503911.jsonl |

Two findings follow.

**(a) The "26 declared tools" figure is a prompt echo.** The live server reports 26 on all five endpoints and has since at least 2026-09-24. The two 2026-09-19 rejections quote 25, consistent with `/root/GEOX/CANONICAL_PUBLIC_SURFACE.json:public_count = 25`, generated 2026-09-19 and lacking `geox_surface_status`. The two 2026-10-01 entries sit in `agent-a048e6ecbef503911.jsonl`, whose line 1 is the tasking prompt and whose line 151 contains the literal string `RT1_GUARD: Tool '[^'` — a regex fragment, not server output. That file was quoting source templates (`Tool '{tool_name}'` also appears). Those are echoes, not fresh rejections.

**(b) The three named tools have no RT1 receipt at all.** `geox_system_registry_status`, `geox_resource_registry_status`, `mcp_health_check` appear 16/6/8 times across transcripts but exclusively in prose and paste-cache — never inside a `tool_result`. They were never actually rejected by a live server; they were discussed as if they had been. All three are `ABSENT_FROM_MANIFEST`, so a real call would be correctly rejected, and `mcp_health_check` is not even GEOX's tool to reject.

**The `geox_surface_status` rejection was real but is now obsolete.** It was genuinely rejected on 2026-09-19 because it was not yet public (25-tool era). It is public today — first entry in live `/tools`, `visibility=public, tier=A`.

**This is the scar class `scar-2026-09-28-claimed-before-checking-twice`.** Lane 555 verified before asserting rather than propagating. The receipt caught it. The parent agent (me) did not, until now.

---

## 1. GEOX connector descriptor (S_declared)

**S_declared is not a number. It is nine numbers across ten artifacts.**

| Artifact | Declared public | Path |
|---|---|---|
| live `/health` `tools_loaded` | 26 | `http://127.0.0.1:8081/health` |
| live `/drift` `canonical_count` | 26 | `http://127.0.0.1:8081/drift` |
| live `/status` `canonical_tools` | 26 | `http://127.0.0.1:8081/status` |
| live `/tools` array length | 26 | `http://127.0.0.1:8081/tools` |
| live `/.well-known/mcp/server.json` `publicCount` | 26 (`totalRegistered` 65) | `http://127.0.0.1:8081/.well-known/mcp/server.json` |
| **disk connector card** | **19 governed / 81 registered, v2026.08.09** | `/opt/geox/.well-known/mcp/server.json` |
| disk tools manifest | **`surface_tools` 25 / `canonical_tools` 86** | `/opt/geox/.well-known/tools.json` |
| canonical surface snapshot | **25** (generated 2026-09-19) | `/root/GEOX/CANONICAL_PUBLIC_SURFACE.json:public_count` |
| MCP apps surface | **32** | `/root/GEOX/GEOX_MCP_APPS_SURFACE.json:total_canonical_tools` |
| manifest target | **31** | `/root/GEOX/src/geox_mcp/tools_manifest.yaml:public_count_target` |
| federation router note | **"33 canonical tools"** | `/root/AAA/mcp.json` (geox entry) |
| organ registry | **33** (2026-07-30) then **26** (2026-09-06) | `/root/AAA/federation/organs.yaml` geox `live_probe_*` |

The disk connector card at `/opt/geox/.well-known/mcp/server.json` is the one an external connector fetches. It advertises `v2026.08.09` and an OAuth static client `geox-claude-conn-20260804-a01` with `"expires_at": "2026-09-04T10:15:00Z"` — **expired 27 days ago**. The live card served at the same path returns different content (`v2026.08.26`, `publicCount` 26, `oauth` key absent entirely), so disk and wire disagree for the same URL.

**Five different version strings from one running process:** `v2026.08.26` (`/health`, `/status`), `2026.06.06` (`/webmcp/status`), `v2026.07.24` (`/mcp/tools` discovery doc), `v2026.08.09` (disk card), `2026.07.24-truth-loop-hardening` (`manifest_version`).

---

## 2. GEOX RT1 canonical (S_exported) — the 26

**S_exported = 26, and it is internally consistent.**

RT1 guard text lives at `/root/GEOX/src/geox_mcp/geox_middleware.py:727-729`. The surface is built at `/root/GEOX/src/geox_mcp/registry.py:57-67` (`SURFACE_TOOLS = public_tool_names() − GHOST_TOOLS`), sourced from `/root/GEOX/src/geox_mcp/tools_manifest.yaml` via `surface_manifest.py`.

**The 26 verbatim** (from live `/drift` `canonical_tools`, identical to `/tools`):

```
geox_basin                       geox_map
geox_calibration_register_witness geox_model
geox_claim                       geox_paleobiodb_query
geox_contrast_metabolize         geox_petrophysics
geox_deep_time                   geox_prospect
geox_extract_display_proxy       geox_register_native_source
geox_extract_native_trace        geox_seismic_compute
geox_geomechanics                geox_seismic_ingest
geox_glof                        geox_seismic_interpret
geox_list_registered_sources     geox_source
                                 geox_spatial
                                 geox_surface_status
                                 geox_temporal
                                 geox_well
                                 geox_well_ingest
                                 geox_well_qc
```

**compat_aliases (2):** `geox_well_desk`, `geox_well_view` — `/root/GEOX/src/geox_mcp/tools_manifest.yaml:5-7`.

**Declared-but-not-shipped / ghosted**, `/root/GEOX/src/geox_mcp/registry.py:27-51`: `geox_visual_generate_hypotheses` marked `GHOSTED 2026-07-29`; `geox_forbidden_claims_scan` and `geox_physical_reality_interpret` carry `RESURRECTED 2026-08-04` comments but are commented out of the ghost list; ~22 names total sit in `GHOST_TOOLS`. Manifest holds 87 entries: 26 public, 61 internal.

**A structural inversion worth flagging to Lane 333.** `geox_middleware.py:291` sets the *executable* surface to `public ∪ internal ∪ compat` = 26 + 61 + 2 = **89 callable names**, while `geox_middleware.py:294,416` filters `tools/list` to public only. So 63 tools are callable-but-undiscoverable. A client cannot enumerate two-thirds of what it is permitted to invoke.

**Internal count also drifts:** live `/status` reports `internal_tools: 39`; the manifest declares 61 internal.

---

## 3. GEOX runtime health

**Alive, responsive, and materially stale — but not in the way it self-reports.**

- `geox-mcp.service` active, `MainPID=2557583`, `ActiveEnterTimestamp=Wed 2026-09-30 18:16:03 +08`. Unit: `/etc/systemd/system/geox-mcp.service`, `WorkingDirectory=/opt/geox`, `ExecStart=/opt/geox/.venv/bin/python3 -m geox_mcp.server --host 127.0.0.1 --port 8081`.
- Listening: `127.0.0.1:8081` (python3 pid 2557583) + tailscaled mirrors on `100.64.0.2:8081`. `geox-heartbeat.service` and `geox-static-server.service` both active.
- HTTP: `/health` 200, `/mcp` 200, `/tools` 200, `/status` 200, `/drift` 200, `/webmcp/status` 200, `/webmcp/tools` 200. `/openapi.json` `/docs` `/surface` `/api/tools` → 404. `/.well-known/tools.json` → **404 live** despite existing on disk at `/opt/geox/.well-known/tools.json`.
- `/health` self-report: `surface_drift{canonical_count:26, live_count:26, drift_count:0, gap_count:0, ok:true}`. That part is **true and reproduced independently**.

### DRIFT — the deployment_drift block measures the wrong organ

**Severity: HIGH (false-alignment attestation).**

GEOX `/health` publishes `deployment_drift{source_commit:"297abcb04afd…", built_commit:"297abcb", deployed_commit:"297abcb", drift:false, status:"aligned"}`. `297abcb04afd163593b1bce078123a08a5b1f1e7` is **arifOS's HEAD, not GEOX's**:

```
git -C /root/arifOS rev-parse HEAD → 297abcb04afd163593b1bce078123a08a5b1f1e7
git -C /root/GEOX cat-file -t 297abcb… → fatal: bad object
git -C /opt/geox  cat-file -t 297abcb… → fatal: Not a valid object name
```

The code confirms it: `_probe_arifos_deployment_drift()` reads `running_sha` from `http://127.0.0.1:8088/api/build-info` and `source_sha` from `git -C /root/arifOS rev-parse HEAD`, then returns them under unqualified field names `source_commit`/`built_commit`/`deployed_commit` with `deployed_commit = running_sha` hardcoded ("built == deployed for the federation case"). The docstring is candid — this is *arifOS* drift surfaced from GEOX — but the JSON keys are not, so any consumer reading `deployment_drift` on GEOX `/health` gets a clean bill of health for a different organ while GEOX's own source↔runtime divergence goes unmeasured.

### GEOX's actual, unreported drift

**Severity: CRITICAL (disjoint histories).**

```
/opt/geox   HEAD = 7027ff64d4210cf5a9d624a724f13692469f3eb1  (2026-09-30 22:05:29 +0800)
/root/GEOX  HEAD = 17802197d9c4c81de19403125c32bd09736347ae  (2026-10-01 14:29:47 +0800)
git -C /root/GEOX cat-file -t 7027ff64 → fatal: Not a valid object name
git -C /opt/geox  cat-file -t 17802197 → fatal: Not a valid object name
commit counts: /opt/geox 1442, /root/GEOX 1521. Same origin URL. No shared object locally.
```

Neither commit exists in the other repository. Source and runtime cannot be reconciled without a network fetch. `organs.yaml` declares `source_path: /root/GEOX`, `runtime_path: /opt/geox` — the declared pairing is unverifiable.

**Supporting stale/phantom receipts:**

- `/opt/geox/.git_commit` = `7750a2b3` → **not a valid object in `/opt/geox`**. Phantom receipt.
- `/root/GEOX/.git_commit` = `658a921` → real, but dated **2026-08-08**, ~7.8 weeks behind HEAD `17802197`.
- `/opt/geox` has **40 uncommitted modified files**, including `src/geox_mcp/server.py`, `src/geox_mcp/geox_middleware.py`, `src/geox_mcp/session_enforcement.py`, `.well-known/tools.json`, `.well-known/openapi.json`, `llms.txt`. The runtime is not running its own committed source.
- `identity.git_version = "geox-3f344b84"`: `3f344b84` exists in `/opt/geox` but **not** in `/root/GEOX`.
- Manifest files differ between the two trees (`md5 37ccba76…` vs `5ce9e9d1…` for `tools_manifest.yaml`; all four core files differ), though the 26-name public **set is identical** on both sides. Drift is currently cosmetic at the public-surface level, not semantic.

---

## 4. GEOX S_callable table

**S_callable at the wire = UNMEASURED.** `POST /mcp` with a `tools/list` body returns `-32600 "Bad Request: Missing session ID"`, and completing it would require MCP `initialize`, which is out of mandate.

What was observed without side effects:

| tool_name | reachable | response_status | notes |
|---|---|---|---|
| `geox_surface_status` | listed, not invoked | UNMEASURED | Position 1 of live `/tools`; `annotations.read_only: true`, `governance.mutation: false` |
| all 26 canonical | listed, not invoked | UNMEASURED | Enumerated verbatim by `GET /tools` and `GET /drift` |
| `geox_system_registry_status` | **no** | would be RT1-rejected | Real function at `/root/GEOX/src/geox_mcp/tools/registry.py:103`, wired in `servers/witness.py:66`, but **ABSENT_FROM_MANIFEST** |
| `geox_resource_registry_status` | **no** | would be RT1-rejected | `/root/GEOX/src/geox_mcp/tools/registry.py:805`; **ABSENT_FROM_MANIFEST** |
| `mcp_health_check` | **no** | would be RT1-rejected | Not a GEOX tool. Legacy alias at `/root/GEOX/contracts/tools/unified_13.py:95`; live owner is arifOS at `/root/arifOS/arifosmcp/tools/health.py` |
| `geox_well_desk_open` | **no** | RT1-rejected (3 real receipts, all from 2026-09-19) | **Ghost.** DEREGISTERED ZEN-15 (`tools_wiring.py:3895`, decorator commented out) yet still in `/opt/geox/src/geox_mcp/server.py:132` (timeout 15.0) and `/opt/geox/src/geox_mcp/organ_governance.py:56` (`RiskTier.READONLY`) |
| `geox_well_desk` / `geox_well_view` | compat-only | UNMEASURED | In `compat_tools`, live at `tools_wiring.py:7090`; invoking triggers the T7 deprecation warning (`geox_middleware.py:736`) |

**Confidence that all 26 are callable: HIGH but unobserved.** `GET /tools` and `GET /drift` both emit 26 with `drift_count:0, ok:true`, and `/drift`'s source string is "live tools/list observation" — the server's own middleware filtered a real `tools/list` down to these 26. Strong indirect evidence, not a call receipt.

**The harness cannot reach GEOX as an MCP tool.** The connector allowlist is not merely the blocking path — GEOX is not loaded into this harness at all (§5). HTTP probes ran through `curl`, which is a different channel than the MCP connector.

---

## 5. MCP skill health matrix

### Root cause of S_observed = ∅ — a config-scope error, not a GEOX defect

**Severity: CRITICAL (entire federation MCP surface inert in this harness).**

```
claude mcp list → openrouter (needs auth), firecrawl (connected). Nothing else.
/root/.mcp.json                        (PROJECT scope, cwd=/root) → 1 server:  firecrawl
/root/.claude.json projects[/root]     (user scope)              → 2 servers: openrouter, firecrawl
/root/.claude/mcp.json                 (NOT a scope path)        → 33 servers, incl. geox :8081
/root/.claude/settings.json "mcpServers" (NOT a scope path)      → 21 servers, inert
/root/.claude/settings.local.json enabledMcpjsonServers          → ["arifos","geox","wealth","well","aforge","arifflow"]
```

`/root/.claude/mcp.json` declares 33 servers including `geox → http://localhost:8081/mcp`, but that filename is not a location Claude Code reads for MCP scope. The project-scope file `/root/.mcp.json` declares only `firecrawl`. `enabledMcpjsonServers` then names six servers that do not exist in any loaded file — **dangling enablement**, a no-op. The harness's own tool surface confirms it: zero `geox_*` tools available this session.

**This is the actual explanation for any "GEOX unreachable" claim from this harness.** Whatever issued GEOX rejections was not this harness's GEOX connector, because this harness has no GEOX connector.

### Federation MCP census

`/root/.hermes/MCP_HEALTH.json`, generated `2026-10-01T08:40:01+00:00` (fresh, ~11h):

| server | declared | exported | callable | observed | drift flags |
|---|---|---|---|---|---|
| **geox** | 33 (`/root/AAA/mcp.json`) | 26 (live `/drift`) | UNMEASURED | **0** | declared≠exported≠observed; not in harness scope |
| **hermes-mcp** | 15 (`PUBLIC_TOOL_NAMES`) | 15 resolved | UNMEASURED | 0 | no reachable MCP endpoint found |
| **arifos** | 8 `public_tools` | 8 (`declared_tools:8, exposed_tools:8`) | UNMEASURED | 0 | clean per own `/health`; 40 `diagnostic_tools` off-wire |
| **well** | 40 `tool_count` | 40 | UNMEASURED | 0 | `status:degraded`, **`drift:true`**, `source_commit 8eb479a` ≠ `deployed_commit d54a588`, `freshness_band:EXPIRED`, `state_age_hours:29.1`, `well_signal:WELL_HOLD` |
| **wealth** | 15 | 15 (`tools_loaded=public=canonical=15`) | UNMEASURED | 0 | clean; `working_tree:CLEAN`, `runtime_seal_state:SEALED`; all `apex_scalars` UNMEASURED |
| **aforge** | 121/124 (registry) | UNMEASURED | UNMEASURED | 0 | `status:stdio_present`, **`routable:false`** |
| **cloudflare** | — | — | — | 0 | **`status:disabled_intentional`, `enabled:false`** — the memory's "gold standard" is switched off. `owner_skill:forge-infra-guardian` is the only populated one |

**Census totals:** 31 servers; 15 healthy; 15 routable; 22 enabled; verdict `WARN`. Status breakdown: `healthy` 15, `stdio_present` 7, `disabled_undeclared` 5, `disabled_intentional` 4. **22 of 22 enabled servers have `owner_skill: null`** — the `scar-2026-09-30-mcp-health-owner-skill-gap` is unchanged in ratio (memory recorded 22 of 31; it is now 22 enabled-of-22, i.e. **100%** of the enabled set lacks routing authority).

### hermes :9900 is not an MCP server

**Severity: MEDIUM (misattributed surface).**

`:9900` is the hermes **gateway**, not `hermes_mcp`: process is `hermes … gateway run --replace` on `/root/.hermes/tools/python-3.14.7+20260901-linux-x64/bin/python3`, elapsed 01:56:18. Routes: `/` 200, `/health` 200, `/mcp` **404**, `/tools` 404, `/status` 404. `POST /mcp` → `-32601 "method not found: tools/list"`. Its `/health` returns only `{"status":"ok","agent":"hermes-forge","served_agents":[…]}` — **no `organs_alive` field**. The memory entry `scar-2026-09-30-hermes-mcp-organs-alive-vs-healthy` attributes `organs_alive: 6/6` to this port; that field is not served here.

### scar_wisdom — RESOLVED at source, unverified live

`scar-2026-09-30-hermes-mcp-scarwisdom-drift` is **fixed in the declared and exported layers**.

- `/root/.hermes/hermes_mcp/_constants.py:65` → `"hermes_scar_wisdom"` present in the `PUBLIC_TOOL_NAMES` composition.
- `/root/.hermes/hermes_mcp/tools/__init__.py:38,60` → imported and `scar_wisdom.register(mcp)` called.
- `/root/.hermes/hermes_mcp/tools/scar_wisdom.py` exists (mtime Oct 1 17:32), promoted from `_staging/tools/scar_wisdom.py` (mtime Sep 28 11:40), byte-identical size 7393.
- Runtime resolution: `PUBLIC_TOOL_NAMES` = **15** (11 canonical + 2 infra + 1 aux + gated `hermes_witness_signal`), and `hermes_scar_wisdom ∈ PUBLIC_TOOL_NAMES → True`.

Callable/observed remain UNMEASURED — no reachable `hermes_mcp` JSON-RPC endpoint found to issue `tools/list` against. The `_constants.py:75` docstring still reads "Every MCP tool this server exposes (**14 total**)" while the tuple resolves to 15. Cosmetic count drift.

---

## 6. Drift assessment — is the 4-way inequality confirmed?

| Axis pair | Verdict | Evidence |
|---|---|---|
| **S_declared ≠ S_exported** | **CONFIRMED — severely** | 9 distinct declared values (19, 25, 26, 31, 32, 33, 65, 81, 86) vs a single exported 26. The disk card says 19/81; the wire card for the same URL says 26/65. |
| **S_exported ≠ S_callable** | **UNTESTED** | `tools/call` requires an MCP session; `initialize` was out of mandate. Strong indirect evidence for 26/26 via `/drift` `ok:true`. |
| **S_callable ≠ S_observed** | **CONFIRMED — total** | 26 exported, **0 observed**. Cause is `/root/.mcp.json` declaring 1 server while `/root/.claude/mcp.json` declares 33 at a path the harness never reads. |
| **S_declared ≠ S_observed** | **CONFIRMED** | 33 declared in the federation router, 0 in this harness's tool surface. |
| **source ↔ runtime (bonus axis)** | **CONFIRMED — CRITICAL** | `/opt/geox@7027ff64` and `/root/GEOX@17802197` are mutually non-existent objects; 40 dirty files in runtime; two phantom `.git_commit` receipts. |
| **self-report ↔ reality (bonus axis)** | **CONFIRMED — HIGH** | GEOX `/health` attests `drift:false, status:aligned` using arifOS's SHA `297abcb`. Its own drift is never measured. |

**The inequality holds on three of four axes, is untested on one, and S_observed is confirmed empty.**

**The load-bearing correction:** GEOX the server is the healthiest component in this story. It answers 200 on seven endpoints, self-consistently reports 26 across `/health`, `/drift`, `/status`, `/tools`, and `/webmcp/status` with `drift_count:0`, and its manifest public set matches its live set exactly on both source and runtime trees. The failure is entirely in the layers around it — a mis-scoped harness config, a nine-way-inconsistent descriptor estate, and a health attestation that grades the wrong organ.

Same scar class as `scar-2026-09-30-hermes-mcp-organs-alive-vs-healthy` and `scar-2026-09-30-well-organ-probe-vs-substrate-drift`: the probe lies, the substrate is fine. Here it is sharper — the probe is honest about what it measured but publishes it under keys that imply it measured something else.

---

## 7. Recommendations for Lane 333 — concrete numbers to bake in

1. **Pin one canonical count and make every artifact derive from it.** The only source with an enforcement claim is `/root/GEOX/src/geox_mcp/tools_manifest.yaml` (`public_count_target: 31` — itself wrong, actual public is 26). Fix the target to 26, then regenerate all nine downstream artifacts from it. Any manifest that hardcodes a count should fail CI. The manifest's own rule string already says this: `"tools/list MUST equal public_tools. Docs must not hardcode counts."` — it is not enforced.

2. **Namespace cross-organ health fields.** `deployment_drift` on GEOX `/health` must become `upstream_arifos_deployment_drift`, or GEOX must add its own `self_deployment_drift` computed from `/opt/geox` HEAD vs `/root/GEOX` HEAD. Today a consumer cannot tell whose alignment it is reading.

3. **Require a git-object existence check before any `status:aligned` attestation.** `297abcb` is not an object in either GEOX repo; a one-line `git cat-file -e` would have caught it. Same for the two phantom `.git_commit` values.

4. **Close the discoverability inversion.** 89 executable names, 26 listable. Either publish the internal surface in a read-only discovery channel or stop accepting internal names at `on_call_tool`.

5. **Delete the `geox_well_desk_open` ghost** from `/opt/geox/src/geox_mcp/server.py:132` and `/opt/geox/src/geox_mcp/organ_governance.py:56`. Deregistered under ZEN-15; continued presence is what makes callers believe it exists.

6. **Fix the harness scope before designing anything else.** One-line change: add the six federation servers to `/root/.mcp.json` (project scope, the file actually read), or consolidate to user scope in `/root/.claude.json`. Until then, no GEOX manifest design can be validated by any agent in this harness.

7. **Populate `owner_skill` on all 22 enabled servers.** 100% of the enabled set currently lacks routing authority. `cloudflare` / `forge-infra-guardian` is the template — and it is `disabled_intentional`, so the one correctly-governed server is the one turned off.

8. **Renew or remove the expired OAuth static client** `geox-claude-conn-20260804-a01` (`expires_at: 2026-09-04T10:15:00Z`). An external connector following that card today is instructed to use a credential that lapsed 27 days ago.

9. **Reconcile the two GEOX repositories.** 1442 vs 1521 commits, disjoint object stores, same origin. Requires a network fetch — outside Lane 555 mandate and likely F13-adjacent.

10. **Correct two memory entries.** `scar-2026-09-30-hermes-mcp-scarwisdom-drift` is resolved. `scar-2026-09-30-hermes-mcp-organs-alive-vs-healthy` attributes `organs_alive` to `:9900`, which does not serve that field.

---

## 8. Open questions for Arif — F13-class only

**One binary.** GEOX's public connector card at `https://geox.arif-fazil.com/.well-known/mcp/server.json` is the federation's external port: it advertises 19 tools against a live 26, carries an OAuth client that expired 2026-09-04, and is served from disk content that contradicts what the running process returns for the same URL. External port + canonical record.

**Should the external GEOX connector card be corrected to match the live 26-tool surface — yes or no?**

If **no**, GEOX's public surface stays mis-advertised and the expired credential stays published, and that is recorded as accepted. If **yes**, it is a one-artifact regeneration from the manifest, reversible, and does not touch the running server.

Two further items are F13-adjacent but are **not** raised as binaries because both are reversible and inside an existing mandate: adding the six federation servers to `/root/.mcp.json` (harness config, not canonical record) and reconciling `/opt/geox` against `/root/GEOX` (requires a network fetch; flagged, not recommended).

---

## Scar-class evidence found

- **Phantom receipt, 2 instances.** `/opt/geox/.git_commit` = `7750a2b3` (not a valid object in its own repo); `/root/GEOX/.git_commit` = `658a921` (valid, 2026-08-08, 7.8 weeks stale). Class: `tier-0-phantom-evidence-2026-09-21`.
- **Cross-organ identity contamination.** GEOX `/health` publishes arifOS's SHA `297abcb04afd…` as its own `source_commit`/`built_commit`/`deployed_commit` with `drift:false`. Class: `scar-2026-09-30-forgel-init-seal-refused-deployment-drift` (DEPLOYMENT_DRIFT), inverted — there real drift was reported; here another organ's alignment is reported as self.
- **Probe disagrees with substrate, third instance.** GEOX substrate is healthy (26/26, `ok:true`); the descriptor estate and the harness config are what fail. Class: `scar-2026-09-30-well-organ-probe-vs-substrate-drift`, `scar-2026-09-30-hermes-mcp-organs-alive-vs-healthy`.
- **Claimed-before-checking caught.** Tasking asserted three live rejections at "26 declared tools." Zero receipts support it. Real receipts say 25, name two different tools, and two of the four are transcript echoes of source templates. Class: `scar-2026-09-28-claimed-before-checking-twice`, `scar-2026-09-28-audit-methodology-fork-bias`. Lane 555 verified before asserting rather than propagating.
- **Ghost tool still wired.** `geox_well_desk_open` deregistered under ZEN-15 but live in `/opt/geox/src/geox_mcp/server.py:132` and `organ_governance.py:56`. Class: `scar-2026-09-30-hermes-mcp-scarwisdom-drift` (realised-vs-declared), reversed polarity.
- **Governance vacuum unchanged.** 22 of 22 enabled MCP servers have `owner_skill: null`. Class: `scar-2026-09-30-mcp-health-owner-skill-gap`.
- **Dangling enablement.** `/root/.claude/settings.local.json:enabledMcpjsonServers` names six servers absent from every loaded scope file — an allowlist for tools that cannot resolve.
- **One scar closed.** `hermes_scar_wisdom` is now in `_constants.py:65`, registered at `tools/__init__.py:60`, and resolves into `PUBLIC_TOOL_NAMES` (15). Declared and exported verified; callable unverified.

---

## Mutation attestation

No production artifact was mutated. Every command was read-only: `cat`, `ls`, `find`, `grep`, `sed -n`, `git rev-parse`/`log`/`cat-file`/`status`/`diff`/`merge-base`, `systemctl status`/`cat`/`show`/`is-active`, `ss -tlnp`, `ps`, `md5sum`, `wc`, `python3 -c` (read/parse only), and `curl` against `/health`, `/status`, `/tools`, `/drift`, `/webmcp/*`, `/.well-known/*`, plus one `POST /mcp` rejected pre-dispatch at `-32600 Missing session ID` and one `POST :9900/mcp` rejected at `-32601 method not found`. No MCP `initialize` was issued. No service started, stopped, or restarted.

Post-probe verification: `/root/GEOX` dirty count **0** (unchanged); `/opt/geox` dirty count **40** (pre-existing, unchanged); `geox-mcp.service` still `active`, `MainPID` still **2557583**.

Single filesystem write: `/tmp/geox_public_health_probe.json` (2259 bytes, curl `-o` target for the read-only public `/health` GET). Ephemeral probe output in `/tmp`, not a production artifact.

---

## Receipt persisted

This file was written by the parent agent after Lane 555 returned inline (Lane 555 had no Write tool and correctly refused to author report files under its OBSERVE_ONLY mandate). The receipt content is verbatim from Lane 555's hand-back. The provenance correction at the top is parent-agent framing of the most load-bearing finding, not Lane 555's wording.