# ORGAN_HEALTH — Federation TOOLS & ORGANS Layer, Live Probe

> **Scope:** every MCP organ and tool surface reachable from this host — what is *actually* reachable vs *declared-but-dead*.
> **Method:** read-only. Port/socket enumeration → HTTP health probe → MCP JSON-RPC `initialize` + `tools/list` → MCP connector tool invocation → config/unit inspection. No mutation, no restart, no config write, no docker action.
> **Probe run (UTC):** 2026-09-14T17:50:17Z · **Reproduce:** `python3 /root/AAA/hardening/organs/probe_organs.py` (raw evidence → `probe_organs_raw.json`)
> **Evidence discipline (F2):** every verdict below carries its raw line. A service never probed is marked NOT VERIFIED, never assumed up.

## 0. Host identity — corrects the task premise

```
$ hostname
forge
$ tailscale ip -4
100.64.0.2
```

`MACHINE_MAP.md §0` fingerprint table: `forge + 100.64.0.2` = **KVM8 / "forge" / Truth node**. The task context described this box as "the workshop edge node" — that is **KVM4** (`srv1946043` + `100.64.0.5`). This probe ran on **KVM8 (truth)**, and `~/.hermes/config.yaml` agrees: `federation_role: kvm8-forge-canonical-home`, `singularity: federated-unified-kvm8-forge`.

This matters: on KVM8 the *full* federation organ set binds loopback, plus a tailnet mirror via `tailscaled`. Cross-node reachability was **not** probed here.

---

## 1. LOCAL HTTP — 41 surfaces, raw status

Interpretation rule applied: **401/403 = UP-AUTH**; only conn-refused/timeout = DOWN.

| # | Surface | Port | Verdict | Raw evidence |
|---|---|---|---|---|
| 1 | arifOS kernel (judge) | 8088 | **UP-OPEN** | `GET /health -> 200` |
| 2 | A-FORGE exec server | 7071 | **UP-OPEN** | `GET /health -> 200` |
| 3 | A-FORGE MCP | 7072 | **UP-OPEN** | `GET /health -> 200` |
| 4 | arifFlow daemon (REST) | 7073 | **UP-OPEN** | `GET /health -> 200` |
| 5 | FED fed-router | 7074 | **UP-OPEN** | `GET /health -> 200` |
| 6 | arifFlow MCP (fastmcp) | 7075 | **UP-OPEN (no /health route)** | `GET /health -> 404` (MCP surface itself UP — §2) |
| 7 | GEOX MCP | 8081 | **UP-OPEN** | `GET /health -> 200` → `{"status":"healthy","kernel_verdict":"SEAL","service":"geox-unified","version":"v2026.08.26"}` |
| 8 | WEALTH MCP | 18082 | **UP-OPEN** | `GET /health -> 200` |
| 9 | WELL organ | 18083 | **UP-OPEN** | `GET /health -> 200` |
| 10 | SIGNAL organ | 18084 | **UP-OPEN** | `GET /health -> 200` |
| 11 | FRAME organ | 18085 | **UP-OPEN** | `GET /health -> 200` |
| 12 | FRAME MCP (fastmcp) | 18086 | **UP-OPEN (no /health route)** | `GET /health -> 404` (MCP UP — §2) |
| 13 | AAA a2a-server | 3001 | **UP-OPEN** | `GET /health -> 200`; `GET /.well-known/agent-card.json -> 200` → `{"name":"AAA A2A Gateway","version":"2026.08.25","url":"https://aaa.arif-fazil.com"}` |
| 14 | AAA MCP (fastmcp) | 3002 | **UP-OPEN (no /health route)** | `GET /health -> 404` (MCP UP — §2) |
| 15 | 1mcp aggregator | 3050 | **UP-OPEN** | `GET /health -> 200` |
| 16 | playwright-mcp | 8931 | **UP-OPEN (no /health route)** | `GET /health -> 400` (MCP UP — §2) |
| 17 | FED intake (HAProxy) | 4000 | **UP-OPEN** | `GET /health/liveliness -> 200` |
| 18 | FED clamp (HAProxy) | 4012 | **UP-OPEN** | `GET /health/liveliness -> 200` |
| 19 | litellm (model brain) | 4013 | **UP-AUTH** | `GET /health -> 401` |
| 20 | fed-aware-middleware | 4010 | **UP-OPEN** | `GET /health -> 200` |
| 21 | apa-github-bridge | 18095 | **UP-OPEN** | `GET /health -> 200` (pid 1401415 = `github_bridge.py`) |
| 22 | gmail_bridge | 18097 | **UP-OPEN** | `GET /health -> 200` |
| 23 | gws_bridge | 18098 | **UP-OPEN** | `GET /health -> 200` |
| 24 | drive_bridge | 18099 | **UP-OPEN** | `GET /health -> 200` |
| 25 | gemini_bridge | 18092 | **UP-OPEN** | `GET /health -> 200` |
| 26 | email_bridge | 18093 | **UP-OPEN** | `GET /health -> 200` |
| 27 | calendar_bridge | 18094 | **UP-OPEN** | `GET /health -> 200` |
| 28 | sheets_bridge | 18075 | **UP-OPEN** | `GET /health -> 200` |
| 29 | signing_server | 18900 | **UP-OPEN** | `GET /health -> 200` |
| 30 | vault999-writer | 5001 | **UP-OPEN** | `GET /health -> 200` |
| 31 | l5_search_api | 8001 | **UP-OPEN** | `GET /health -> 200` |
| 32 | hermes-prod health | 18791 | **UP-OPEN** | `GET /health -> 200` |
| 33 | forge-bot | 8091 | **UP-OPEN** | `GET /health -> 200` |
| 34 | headscale (mesh) | 50443 | **UP-TCP / HTTP NOT VERIFIED** | `ss -ltnp` shows `127.0.0.1:50443 headscale`; `GET /health -> ConnectionResetError [Errno 104]` (TLS/gRPC listener resets plain HTTP — wrong probe protocol, not a down service) |
| 35 | hermes a2a platform | 9900 | **UP-OPEN** | `GET /health -> 200` |
| 36 | netdata | 19999 | **UP-OPEN** | `GET /api/v1/info -> 200` |
| 37 | prometheus | 9090 | **UP-OPEN** | `GET /-healthy -> 200` |
| 38 | grafana | 3000 | **UP-OPEN** | `GET /api/health -> 200` |
| 39 | ollama | 11434 | **UP-OPEN** | `GET /api/tags -> 200` |
| 40 | llama-server (qwen lane) | 42555 | **UP-OPEN** | `GET /health -> 200` |
| 41 | i-ARIF (REST) | — | **NOT VERIFIED / registry claim falsified** | `mcp-servers.yaml organs.iarif` declares `http://localhost:18095/health`. Live `:18095` = **apa-github-bridge** (`pid 1401415 github_bridge.py`). No process named i-ARIF binds any port. Registry entry is stale. |

**Also discovered but not organ-class** (owning process from `ss -ltnp`): postgres 5432, redis 6379/6380, qdrant 6333/6334, minio 9000/9001, nats 4222/7422/8222, otel 4317-4319/8888, node_exporter 9100, prisma engine 44197, caddy `*:80`/`*:443`, cloudflared 20241, headscale 8083, static `http.server` 8090, tier1-serve 8094, GAS/commodity node APIs 3456-3460, sshd 22888. Total listening TCP sockets: **103**.

**DOWN count among organ surfaces: 0.** No organ returned connection-refused. The only refusals on this host are the MiniMax MCP endpoints (§5).

---

## 2. MCP TOOLS — one read-only tool actually invoked per server

| Server | Tool invoked | Result | Verdict |
|---|---|---|---|
| arifos | `mcp__arifos__list_resources` | **returned** — 35 resources (`arifos://vitals`, `//carry-forward`, `//flow-state`, `//doctrine`, `//vault/head`, `skill://index`, `tree777://index`, …) | **UP** |
| aforge | `mcp__aforge__forge_health_check` | **returned** — `{"status":"healthy","version":"2.0.0-genome-stable"}`, genome `VAULT999_MERKLE_SEALED / F9_ANTI_HANTU_ACTIVE`, duration_ms 5, chain_hash `b1956cdf6101c763` | **UP** |
| fed | `mcp__fed__fed_health` | **returned** — `{"status":"LIVE","port":7074,"version":"3.3.0-zen-classifier","tables":["providers","route_health","route_latency","shadow_ledger","token_bank_spend"],"state_db":"/root/.local/share/arifos/token_bank.db"}` | **UP** |
| geox | `mcp__geox__list_resources` | **returned** — 56 resources incl. 20+ `ui://geox/*` MCP Apps, `geox://layers/index`, `geox://surface/truth`, `geox://data-sources/malaysia` | **UP** |
| wealth | `mcp__wealth__capital_health` | **FAILED — exact error below** | **UP / TOOL BROKEN** |
| well | `mcp__well__well_registry_status` | **returned** — `{"ok":true,"intended_tools":10,"registered_tools":31,"exported_tools":10,"callable_tools":10,"phantom_tools_count":0,"verdict":"REGISTRY_PASS","w0":"OPERATOR_VETO_INTACT"}` | **UP** |
| arifflow | `mcp__arifflow__flow_health` | **returned** — `{"status":"ok-v3-vector","fq":{"verdict":"OPTIMAL","diagnosis":"BALANCED","quotient":1.7778},"receipts":1000,"uptime_ms":842828}`, vector diagnosis `GOVERNANCE_COLLAPSE` (fused_rank 0.79), dimension `g` band `PATHOLOGICAL` (0.4952) | **UP** |
| context7 | `mcp__context7__list_resources` | **returned** — `{"resources": []}` (valid, no resources exposed) | **UP** |

### WEALTH `capital_health` — exact failure chain (3 separate defects)

1. **No args →** `tool_call ... missing required argument(s): mode`. `mode` is `required` in the schema with **no enum, no description** — the caller must guess.
2. **`mode=status`, no session →** `{"verdict":"VOID","error_code":"SESSION_REQUIRED","errors":["L11 AUTH: session_id required for all WEALTH tools (FORGE 2026-07-18: anonymous reads blocked)"]}` — organ is UP, auth-gated at L11.
3. **`mode=status` + valid `session_id` →** client-side MCP rejection:
   ```
   MCP call failed: RuntimeError: Invalid structured content returned by tool capital_health:
   'tool_name' is a required property
   Failed validating 'required' in schema: {... 'verdict': {'enum': ['SEAL','PARTIAL','SABAR',
   'HOLD','VOID','INSUFFICIENT_EVIDENCE','READONLY','C1_PASS']} ...}
   ```
   → **`capital_health` is unusable from any MCP client**: the server's declared `outputSchema` does not match what it actually returns.

**Blast radius bounded by test** — same session, same server:
- `capital_registry` → **works** (`"registry_truth":"PASS"`, 11 canonical tools, verdict `READONLY`, receipt persisted to `/root/VAULT999/wealth/receipts.jsonl`)
- `capital_entropy` (valid structured content, verdict `HOLD`) → **works**, but `mode` is again required with no enum; legal values are discoverable only from a runtime error: `"Use one of: power_consequence_map, metric_purpose_audit, responsibility_ledger, trust_capital_decay, coercive_order_cost, entropy_externality"`

→ **`capital_health` is the single broken tool.** WEALTH MCP overall is **UP**.

### Raw MCP `tools/list` probe (independent of the Hermes connector)

| Endpoint | Verdict | Live `tools/list` |
|---|---|---|
| `127.0.0.1:8088/mcp` | UP-MCP | 8 — `arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal` |
| `127.0.0.1:7072/mcp` | UP-MCP | **120** |
| `127.0.0.1:7074/mcp` | UP-MCP | 7 — `fed_route, fed_status, fed_probe, fed_contrast, fed_health, fed_classify, fed_report_latency` |
| `127.0.0.1:8081/mcp` | **UP-MCP-HANDSHAKE-OK / LIST-EMPTY** | `initialize` 200, `serverInfo {"name":"GEOX","version":"v2026.08.26"}`; `tools/list` returned **HTTP 200 + zero-byte body** on both attempts (a standalone run returned **26 tools**) — see §6 caveat |
| `127.0.0.1:18082/mcp` | UP-MCP | 11 — all `capital_*` + `wealth_judge_handoff` |
| `127.0.0.1:18083/mcp` | UP-MCP | 31 |
| `127.0.0.1:7075/mcp` | UP-MCP | 3 — `flow_health, flow_entity_report, flow_ingest` |
| `127.0.0.1:18086/mcp` | UP-MCP | 7 — `frame_health, frame_probe, frame_drift, frame_baseline, frame_trend, frame_report, frame_rsi_verify` |
| `127.0.0.1:3002/mcp` | UP-MCP | 4 — `aaa_health, aaa_agent_card, aaa_federation_manifest, aaa_discovery` |
| `127.0.0.1:3050/mcp` | UP-MCP | **0 tools** |
| `127.0.0.1:8931/mcp` | UP-MCP | 23 `browser_*` |

All endpoints answered `protocolVersion: 2025-06-18`.

---

## 3. MEDIA & PERCEPTION ORGANS — brokered vs shell

| Tool | Verdict | Raw evidence |
|---|---|---|
| `mcp__aforge__forge_web_extract` | **UP — WORKS** | `{"status":"ok","route":"static_fetch","source":{"title":"Example Domain"},"content":{"content_length":142},"receipt_id":"73f78706-…","duration_ms":95}` |
| `mcp__aforge__forge_visual_qa` | **UP — works; W³ never consensus** | Real image → `verdict PASS_CANDIDATE`, `w1_vision CONFIRMED conf 0.5`, `w2_linter CONFIRMED conf 0.9`, `w3_sovereign PENDING conf 0`, `consensus false`, `requires888hold true`, `screenshot_hash 87c729e7…`. Not a stub — falsified with a missing file: `HARD_FAULT`, `w1 REJECTED`, `SCREENSHOT_LOAD_FAILED: ENOENT: no such file or directory, open '/tmp/PROBE_ORGANS_DOES_NOT_EXIST_9f3a.png'`. F12 gate live: `<html>` payload → `VOID / F12 INJECTION: arg 'dom_payload' contains shell metacharacters` |
| `mcp__aforge__forge_browser_screenshot` | **SURFACE UP — ACTUATOR DEAD (silent failure)** | Returns envelope `"status":"SEAL"`, `message":"…completed"` while the payload is an error string: `"### Error\nError: async createBrowserWithInfo: Failed to launch chromium because executable doesn't exist at /root/.cache/ms-playwright/chromium-1232/chrome-linux64/chrome"`. Gate also blocks off-allowlist origins first: `HOLD / BROWSER_INJECTION_SENTINEL / F2 UNKNOWN_PAGE_ORIGIN: page origin 'example.com' is not in the trusted allowlist` |

**Root cause (verified):** `/root/.cache/ms-playwright/` **does not exist** (`ls: cannot access … No such file or directory`). Chromium *is* installed on the host (`/usr/bin/google-chrome-stable`, `/opt/google/chrome/chrome`, 293 MB) but playwright is hard-pointed at an absent path. The same break hits the standalone playwright MCP:

```
playwright-mcp 127.0.0.1:8931/mcp  tools/call browser_navigate {"url":"https://example.com"}
-> HTTP 200  {"result":{"content":[{"type":"text","text":"### Error\nError: async createBrowserWithInfo:
   Failed to launch chromium because executable doesn't exist at
   /root/.cache/ms-playwright/chromium-1232/chrome-linux64/chrome"}],"isError":true}}
```
It is launched with `--executable-path /root/.cache/ms-playwright/chromium-1232/chrome-linux64/chrome` (pid 3657434). `/home/ariffazil/.cache/ms-playwright/` exists but contains `mcp-chrome-ed24771`, not `chromium-1232`.

### Is there a MiniMax-media MCP organ?

- **In the Hermes MCP config: NO.** `/root/.hermes/config.yaml mcp_servers` = `aforge, arifflow, arifos, cloudflare, context7, datadog, fed, geox, hermes-social, hugging_face, wealth, well, zai_reader, zai_search, zai_vision`. The only `minimax:` key in that file is under `tts:` (a TTS provider, line 33). **NOT-CONFIGURED.**
- **On the box: it EXISTS, is DECLARED — and is DEAD.** See §5.

### Verdict — brokered vs shell

| Capability | Lane | Status |
|---|---|---|
| Web extraction / crawl | **BROKERED via MCP** (`aforge.forge_web_extract`) | UP |
| Visual QA / W³ tri-witness | **BROKERED via MCP** (`aforge.forge_visual_qa`) | UP (W1 confidence flat 0.5, `ai_involvement: NONE`) |
| Browser automation / screenshot | **BROKERED via MCP** (aforge `forge_browser_*`, playwright-mcp :8931) | **DEAD** — chromium binary missing; 2 overlapping broker lanes, both broken |
| Image generation (T2I/I2I) | **SHELL ONLY** — `mmx image generate` | mmx 1.0.22 reachable |
| Video generation (T2V/I2V/S2V) | **SHELL ONLY** — `mmx video generate` | mmx 1.0.22 reachable |
| Speech / TTS | **SHELL ONLY** — `mmx speech synthesize` (plus native Hermes `text_to_speech`, tts.provider `minimax`, voice `iarif-sovereign-v9`) | mmx 1.0.22 reachable |
| Image understanding (VLM) | **SHELL ONLY** — `mmx vision describe`; also MCP-brokered via `zai_vision` (8 tools) | mmx reachable; zai_vision configured |
| Music generation | **SHELL ONLY** — covered by the dead `minimax-media` unit | NOT AVAILABLE |

**That is the answer to the session question:** media is **shell-only on this host**. There is no live media MCP organ to broker through, which is exactly why every image/video/TTS call in the session fell through to the `mmx` CLI.

---

## 4. TOOL SCHEMA & WIRING DRIFT

### 4.1 Deferred tool count vs live `tools/list` vs registry declaration

| Server | Hermes deferred | Live `tools/list` | +4 admin (`list_resources`/`read_resource`/`list_prompts`/`get_prompt`) | `mcp-servers.yaml` declares | Registry accurate? |
|---|---|---|---|---|---|
| aforge | 124 | 120 | 124 ✓ | **75** | ✗ **understated by 45** |
| arifos | 12 | 8 | 12 ✓ | 8 (tools only) | ✓ |
| fed | 11 | 7 | 11 ✓ | 7 | ✓ |
| geox | 30 | 26 (observed) | 30 ✓ | **20** | ✗ **understated by 6** |
| wealth | 15 | 11 | 15 ✓ | **12** | ✗ off by 1 |
| well | 35 | 31 | 35 ✓ | **30** | ✗ off by 1 |
| arifflow | 3 | 3 | 3 ✓ | **0** | ✗ **declared "no MCP surface"** |
| frame | not wired | 7 | — | 7 | ✓ (but not wired — 4.3) |
| aaa | not wired | 4 | — | 4 | ✓ (but not wired — 4.3) |
| playwright-mcp | not wired | 23 | — | **absent from registry** | ✗ undeclared live MCP |
| 1mcp aggregator | not wired | 0 | — | **absent from registry** | ✗ undeclared live MCP |

### 4.2 Protocol declaration drift (registry gap G1 is stale)

`mcp-servers.yaml` declares `protocol: "2024-11-05"` for `arifos-kernel`, `geox`, `wealth`, `well` and lists gap **G1 (CRITICAL): "MCP specification drift — 2024-11-05 vs 2025-06-18 coexist"**.
**Live probe: every one of those endpoints answered `protocolVersion: 2025-06-18`.** G1 is stale — the surfaces have already converged.

### 4.3 Wiring drift — live MCP servers the gateway cannot see

`mcp-servers.yaml` claims `forge_instruments.hermes.mcp_servers: [kernel, aforge, geox, wealth, well, arifflow, frame, aaa, fed]` with `missing: []`.
**Actual `~/.hermes/config.yaml` has no `frame` and no `aaa` entry.** FRAME MCP (:18086, 7 tools) and AAA MCP (:3002, 4 tools) are **live and reachable but invisible to Hermes** — exactly registry gap **G2** ("FRAME, i-ARIF, AAA are NOT MCP-enabled"). G2 is half-false (they *are* MCP-enabled) and half-true (they are *not wired*).

### 4.4 Described parameters that do not match a live call

1. **`wealth.capital_health`** — declared `outputSchema` requires `tool_name`; live return omits it → every call rejected client-side. *(§2 defect 3)*
2. **`wealth.capital_health` / `wealth.capital_entropy`** — `mode` is `required` with **no enum and no description**; legal values surface only in a runtime error.
3. **`aforge.forge_browser_screenshot`** — advertises a success contract but returns an error *string* inside a `"status":"SEAL"` envelope. A caller that trusts the envelope takes a failure for a success. **Contract violation, not a schema mismatch.**
4. **`1mcp` aggregator** — declares 23 servers in `/root/.config/1mcp/mcp.json` (`disabled:false` for 20 of them) and live-advertises **0 tools** via `tools/list`.
5. **`aforge.forge_health_check`** — internally reports `telemetry.totalEvents: 1` (`{"forge_scar":1}`); a healthy organ surface with a near-empty telemetry window.

### 4.5 Silent-degradation signals inside successful responses

- `forge_visual_qa` integration receipts come back as **fallback** IDs: `arif_judge: {"status":"EMITTED","receipt_id":"judge-fallback-1789408067149"}`, `vault999: {"status":"EMITTED","receipt_id":"vault-fallback-1789408068624"}`, `well: {"status":"PENDING"}`. Whether `*-fallback-*` means the real judge/vault path is detached is **NOT VERIFIED** — but the naming is a degradation flag worth a follow-up.
- `arifflow` `flow_health` returns `provenance.missing_inputs: ["window_duration_s","apex_block","flow_block","projection_block"]` alongside `status: ok-v3-vector`.

---

## 5. DECLARED-BUT-DEAD INVENTORY

### 5.1 MiniMax MCP media organ — declared in 3 places, running in 0

**Declaration 1** — `/root/.config/1mcp/mcp.json` (1mcp aggregator):
```json
"minimax-media": {"type":"http","disabled":false,"url":"http://127.0.0.1:18090/rest","tags":["utility","media"]}
"minimax-code":  {"type":"http","disabled":true, "url":"http://127.0.0.1:18091/mcp","tags":["utility","code"]}
```

**Declaration 2** — `/etc/systemd/system/minimax-media.service` (header):
```
# Provides image generation, video generation, TTS, music generation
# via MiniMax API. Exposes MCP tools through REST HTTP on :18090.
# Endpoint: http://127.0.0.1:18090/rest
```

**Declaration 3** — unit is `enabled` and code exists: `/root/.npm-global/bin/minimax-mcp-js` → `../lib/node_modules/minimax-mcp-js/build/index.js`, env `/etc/minimax-media.env` present (142 B), source `/opt/minimax-mcp-media/`.

**Reality:**
```
$ systemctl status minimax-media
○ minimax-media.service - MiniMax MCP Media Server — Image, Video, TTS, Music
     Loaded: loaded (/etc/systemd/system/minimax-media.service; enabled; preset: enabled)
     Active: inactive (dead) since Wed 2026-09-02 08:11:04 +08; 1 week 5 days ago
   Duration: 3min 5.830s
   Main PID: 1120 (code=exited, status=0/SUCCESS)

$ (exec 3<>/dev/tcp/127.0.0.1/18090)  -> Connection refused     # declared endpoint
$ (exec 3<>/dev/tcp/127.0.0.1/18091)  -> Connection refused     # minimax-code
$ ss -ltnp | grep :18100
LISTEN 100.64.0.2:18100 tailscaled ...        # tailnet mirror only — NO local listener
```
→ **DOWN.** Exited cleanly (`status=0/SUCCESS`) after 3 minutes on 2026-09-02; `Restart=on-failure` never fires on a clean exit, so it has stayed dead for ~12 days without an alarm.

**Port drift inside the unit itself:**
```
# header comment + 1mcp aggregator  : :18090/rest
ExecStart=/root/.npm-global/bin/minimax-mcp-js --mode rest --port 18100
```
Even if it were started, it would bind **18100**, not the declared **18090** — the aggregator entry would still fail.

**Unit hygiene defect:** `StartLimitIntervalSec=300` is written in `[Service]`; systemd logs `Unknown key 'StartLimitIntervalSec' in section [Service], ignoring.` (repeatedly, most recently 2026-09-15 00:07). It belongs in `[Unit]` — so the intended restart-rate protection is silently inactive.

Related units, all **disabled**: `minimax-media-mcp.service` (`/opt/minimax-mcp-media/run_v2.py`), `minimax-code-mcp.service` (`/opt/minimax-mcp-code/run_sse.py`), `minimax-relay.service` (FED gateway :4011 → api.minimax.io).

### 5.2 Other declared-but-not-live

| Declared | Where | Reality |
|---|---|---|
| i-ARIF MCP + health `:18095` | `mcp-servers.yaml organs.iarif` | :18095 is **apa-github-bridge**; no i-ARIF process. Registry stale. (Registry itself already flags `status: NOT_MCP_ENABLED`.) |
| FRAME :18085 "transport: stdio", MCP bridge at `/root/FRAME/mcp/frame-mcp.py` | `mcp-servers.yaml organs.frame` | Live FRAME MCP is **fastmcp HTTP on :18086**; `/root/FRAME/mcp/frame_mcp_fastmcp.py` is the running file. Path+transport in registry are stale. |
| AAA MCP "transport: stdio", bridge `/root/AAA/mcp/aaa-mcp.py` | `mcp-servers.yaml organs.aaa` | Live AAA MCP is **fastmcp HTTP on :3002**; running file `/root/AAA/mcp/aaa_mcp_fastmcp.py`. Stale. |
| `minimax-media` in 1mcp (`disabled:false`) | `/root/.config/1mcp/mcp.json` | Endpoint dead → aggregator advertises a dead server |
| VAULT999 fallback receipts | `forge_visual_qa` integration receipts | `judge-fallback-*`, `vault-fallback-*` — real integration status NOT VERIFIED |

---

## 6. Limits, caveats and what is NOT verified

- **GEOX raw `tools/list` flakiness.** In back-to-back sweeps, `127.0.0.1:8081/mcp` intermittently answers `tools/list` with **HTTP 200 and a zero-byte body** (observed on both a primary attempt and its retry); a standalone handshake in the same minute returned the full **26-tool** payload. GEOX's `initialize` is deterministic (200, `serverInfo GEOX v2026.08.26`). **I could not determine whether this is a GEOX session-lifecycle bug or a probe artifact** — the probe never sends the session-terminating `DELETE`. GEOX is **UP** on the strength of: `GET /health -> 200` with `"status":"healthy","kernel_verdict":"SEAL"`, `initialize` 200 on every attempt, and the Hermes connector `mcp__geox__list_resources` returning 56 resources. **Flagged as an open question, not asserted as a defect.**
- **headscale :50443** — TCP listener confirmed; HTTP health **NOT VERIFIED** (plain-HTTP GET is reset by the TLS/gRPC listener; correct probe protocol not attempted).
- **litellm :4013** — `401` proves UP+AUTH-gated; no credential was used, so model-serving functionality is **NOT VERIFIED**.
- **Cross-node lanes NOT VERIFIED.** KVM4 (`100.64.0.5`) and KVM2 (`100.64.0.4`) were not contacted. OpenClaw edge (:18789, on KVM4) and the KVM2 forks were not probed. `ufw`/Headscale ACL state not inspected.
- **`forge_visual_qa` W1 quality NOT VERIFIED.** W1 reports `CONFIRMED` with a flat `confidence: 0.5` and `ai_involvement: "NONE"` while `w3_sovereign` is permanently `PENDING`, so `consensus` is never `true`. The tool demonstrably reads the file it is given (ENOENT falsification above) — whether W1 performs a genuine VLM interpretation could not be established from outside, and `ai_involvement: NONE` suggests it does not.
- **1mcp aggregator** answered `tools/list -> 0` — read as *not yet loaded* (started with `--enable-async-loading --async-min-servers=3`), **not** proven empty.
- Read-only throughout: no config was edited, no service started/stopped/restarted, no container touched, no file deleted. `probe_organs.py` opens sockets and issues `GET` / `initialize` / `notifications/initialized` / `tools/list` only.

---

## 7. Verdict summary — one line per organ

```
arifOS kernel      :8088   UP-OPEN      GET /health -> 200 ; MCP 8 tools ; 35 resources
A-FORGE            :7071   UP-OPEN      GET /health -> 200 ; health_check {"status":"healthy","version":"2.0.0-genome-stable"}
A-FORGE MCP        :7072   UP-OPEN      GET /health -> 200 ; MCP 120 tools
arifFlow daemon    :7073   UP-OPEN      GET /health -> 200
arifFlow MCP       :7075   UP-OPEN      /health -> 404 (no route) ; MCP 3 tools ; flow_health verdict OPTIMAL
FED fed-router     :7074   UP-OPEN      GET /health -> 200 ; fed_health {"status":"LIVE","version":"3.3.0-zen-classifier"}
FED intake         :4000   UP-OPEN      GET /health/liveliness -> 200
FED clamp          :4012   UP-OPEN      GET /health/liveliness -> 200
litellm            :4013   UP-AUTH      GET /health -> 401
GEOX               :8081   UP-OPEN      GET /health -> 200 {"kernel_verdict":"SEAL"} ; 56 resources ; 26 tools (one clean handshake)
WEALTH             :18082  UP-OPEN      GET /health -> 200 ; capital_registry OK ; capital_health BROKEN (outputSchema)
WELL               :18083  UP-OPEN      GET /health -> 200 ; well_registry_status REGISTRY_PASS (31 registered / 10 callable)
SIGNAL             :18084  UP-OPEN      GET /health -> 200
FRAME organ        :18085  UP-OPEN      GET /health -> 200
FRAME MCP          :18086  UP-OPEN      /health -> 404 ; MCP 7 tools ; NOT WIRED to Hermes
AAA a2a            :3001   UP-OPEN      GET /health -> 200 ; /.well-known/agent-card.json -> 200 "AAA A2A Gateway" v2026.08.25
AAA MCP            :3002   UP-OPEN      /health -> 404 ; MCP 4 tools ; NOT WIRED to Hermes
1mcp aggregator    :3050   UP-OPEN      GET /health -> 200 ; MCP tools/list -> 0
playwright-mcp     :8931   UP-MCP       /health -> 400 ; 23 tools ; BROWSER DEAD (chromium missing)
hermes a2a         :9900   UP-OPEN      GET /health -> 200
headscale          :50443  UP-TCP       TCP listener confirmed ; HTTP health NOT VERIFIED (reset)
i-ARIF (REST)      —       NOT VERIFIED registry claims :18095 ; :18095 is apa-github-bridge
minimax-media      :18090  DOWN         connection refused ; unit inactive(dead) since 2026-09-02 ; NOT in Hermes config
minimax-code       :18091  NOT-CONFIGURED  declared disabled:true in 1mcp ; connection refused
minimax-media-mcp  —       NOT-CONFIGURED  unit disabled
minimax-relay      —       NOT-CONFIGURED  unit disabled
media MCP organ    —       NOT-CONFIGURED  absent from ~/.hermes/config.yaml mcp_servers ; media = shell `mmx` only
KVM4 / KVM2 lanes  —       NOT VERIFIED not probed from this host
```

**Bottom line:** the federation's *organs* are healthy — 40/41 probed surfaces UP, zero organ refusals, every declared MCP endpoint that should answer does answer. The damage is one layer up, in the **tool and wiring layer**: one MCP tool broken by an outputSchema mismatch (`wealth.capital_health`), one capability dead behind a success envelope (`forge_browser_screenshot` + playwright-mcp, missing chromium), one whole media organ declared-but-dead (`minimax-media`, 12 days, no alarm), two live MCP servers the gateway cannot see (FRAME, AAA), and a registry that understates tool counts and protocols in six places.
