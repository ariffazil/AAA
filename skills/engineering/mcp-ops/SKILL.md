---
name: mcp-ops
description: "Use when working with MCP servers — build, probe, wire, test, govern, retire. One owner for the whole MCP lifecycle."
id: mcp-ops
version: 3.0.1
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F8, F10, F11, F12, F13]
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
tags: [mcp, lifecycle, mcporter, fastmcp, probe, transport, wiring, conformance, mcpjam, governance, drift, compression, discovery, registry, ops]
supersedes:
  - FORGE-mcp-ops
  - FORGE-mcp-federation-ops
  - FORGE-mcp-lifeguard
  - FORGE-fastmcp
  - forge-fastmcp
  - FORGE-mcp-gui
  - forge-mcp-gui
  - FORGE-mcp-a2a-agentic
  - forge-mcp-a2a-agentic
  - mcp-organ-probe
  - mcp-edit-activation
  - mcp-transport-fix
  - mcp-ecosystem-indexing
  - forge-mcp-registry-publish
  - external-platform-mcp
  - mcp-context-compression
  - forge-minimax-mcp-direct-invoke
  - telegram-mcp-product-line
  - mcp-testing
  - forge-mcp-governance-wrapper
  - federation-mcp-drift-audit
triggers:
  - "MCP server"
  - "mcporter"
  - "MCP health"
  - "MCP operations"
  - "MCP server build"
  - "FastMCP"
  - "MCP deploy"
  - "MCP inspect"
  - "MCP call"
  - "MCP daemon"
  - "federation MCP"
  - "MCP lifeguard"
  - "MCP restart"
  - "MCP server down"
  - "MCP connection refused"
  - "MCP timeout"
  - "is this MCP tool broken"
  - "MCP handshake"
  - "SESSION_MISSING"
  - "MCP tool returns old output"
  - "is the fix live"
  - "MCP transport"
  - "SSE vs streamable-http"
  - "MCP conformance"
  - "MCPJam"
  - "MCP protocol version"
  - "MCP 2026-07-28"
  - "wire an MCP server into Hermes"
  - "MCP tool schemas eating context"
  - "publish MCP to Smithery or Glama"
  - "MCP Apps"
  - "MCP governance wrapper"
  - "MCP drift audit"
  - "MCP 400 on stateless probe"
  - "MCP CI gate"
  - "MCP OAuth conformance"
  - "MCP auto-recovery"
  - "MCP health check"
  - "MCP probe"
  - "MCP schema validation"
  - "MCP server test"
  - "MCP server validation"
  - "MCP server/discover fails"
  - "MCP smoke test"
  - "MCP test"
  - "MCP tool returns empty list"
  - "MCP tool still returns old output"
  - "MCP transport test"
  - "MCP-App surface"
  - "MCP-Protocol-Version 2026-07-28 vs 2025-11-25"
  - "MCPChatGPT conformance"
  - "MCPJam Inspector"
  - "Ollama cold-start"
  - "Unknown tool"
  - "advertised but unreachable"
  - "check the organ"
  - "declared vs callable"
  - "effect of a server.py edit"
  - "era mismatch diagnose"
  - "gate change not taking effect"
  - "is this tool broken"
  - "model fallback chain"
  - "patched an MCP server"
  - "probe this organ"
  - "registry drift"
  - "reload an MCP server"
  - "stateless MCP"
  - "surface truth"
  - "tool not callable"
  - "MCP server procurement"
  - "which MCP server to adopt"
negative_triggers:
  - "choosing WHICH MCP server to buy/adopt is PROCUREMENT — a lane inside this skill: Stage 1b / references/absorbed-mcp-sota-shopping-list.md (name tombstoned, not a separate skill)"
  - "the target is a WEALTH MCP tool → wealth-mcp-ops"
  - "the target is the Runpod MCP server → runpod-mcp"
  - "the target is the TouchDesigner twozero MCP → touchdesigner-mcp"
  - "generic does-it-work / claim-discipline on any non-MCP tool → agent-tool-verification"
  - "single-shot liveness + schema + transport classification instrument → runtime-probe"
  - "Qwen Token Plan built-in harness tools (not MCP) → qwen-harness-tools"
  - "Telegram bot lanes, tokens, group routing → telegram-bot-routing-doctrine"
  - "MCP health monitoring on a production organ as a standing cron → kabarkan-observability / telemetry-watchdog"
---

# MCP Operations — one owner for the MCP lifecycle

> **The flow:** `DISCOVER → PROBE → INTEGRATE → TEST → GOVERN → RETIRE`
> Find your stage, run its spine, then open the absorbed reference for depth.
> **mcporter** inspects and calls any MCP tool from a terminal. **FastMCP** builds them.
> **MCPJam** tests them. A file edit is never a live fix.
> *DITEMPA BUKAN DIBERI*

## Overview

Every MCP question lands here, at one of six stages. Do not hunt for 26 separate skills — the
sub-knowledge of each retired skill lives in `references/absorbed-<name>.md` (verbatim), linked from
the stage that owns it.

| Stage | Question you are actually asking | Spine |
|---|---|---|
| **1 DISCOVER** | Which servers exist, what do they expose, how do agents find ours? | `mcporter list`, beacon/registry publishing |
| **2 PROBE** | Is it alive, is it callable, is my edit live? | 3-step handshake, 4 numbers, PID-vs-mtime |
| **3 INTEGRATE** | Build it (FastMCP), wire it (config), keep it affordable | `fastmcp scaffold`, `hermes_mcp_wire.py`, `mcp-compress.sh` |
| **4 TEST** | Does it conform, does it work end-to-end? | MCPJam Inspector, smoke gate, stub sweep |
| **5 GOVERN** | Who may call what, and where has it drifted? | governance wrapper, drift audit |
| **6 RETIRE** | How do we deprecate a server or a name without losing it? | `<name>.DEPRECATED-<date>` + `.frozen/` |

## arifOS-ACT Embedding

Before this skill is used on any mutating, irreversible, or high-blast-radius task:

1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if the action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- Inspect, list, or call tools on any federation organ via mcporter.
- Build or extend a Python MCP server with FastMCP; add an MCP App / UI surface.
- Wire an MCP server (federation or external platform) into a live client config.
- Test or gate a server locally before client wiring or deployment.
- An MCP server returns connection refused, timeout, 5xx, `SESSION_MISSING`, or `Unknown tool`.
- A patch to a server file may not be live yet ("is the fix live?").
- External clients (Claude / ChatGPT / Cursor / Gemini) cannot connect — transport/auth shape.
- MCP tool schemas are eating the context window.
- Audit which MCP tools exist vs which are actually used; find bypass and drift.
- Publish a server so other agents can discover it.

## When NOT to Use

- **Do not use for production deployment** without site-architecture skills and arifOS judgment.
- **Do not mutate live federation servers** (restart, config change, port binding) without arifOS F1–F13 clearance.
- **Do not run untrusted MCP servers** outside the `arifos-untrusted-sandbox` skill.
- **Do not hardcode secrets** in server code or client configs; use env vars / SOPS.
- **Do not treat a successful health check as authority** to act beyond observer class.
- If the question is *which* server to adopt → **Stage 1b** / `references/absorbed-mcp-sota-shopping-list.md` (procurement is a lane **inside** this skill since v3.0.1; the name `mcp-sota-shopping-list` is a tombstone, not a separate skill).

---

## Stage 1 — DISCOVER

**Spine.** `mcporter` is pre-installed on af-forge at `/usr/bin/mcporter` (v0.9.0).

```bash
mcporter list                                    # list all known servers
mcporter list arifOS --schema                    # list tools + schemas for one server
mcporter list --http-url http://localhost:8081/mcp --name geox  # ad-hoc HTTP
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
mcporter config list                             # what is configured
mcporter generate-cli --server geox              # codegen: CLI wrapper
mcporter emit-ts <server> --mode client          # codegen: TypeScript client
```

Federation MCP servers (as known to mcporter):

```
arifOS MCP    → arifOS        (7 canonical tools, F1-F13)
GEOX          → geox          (28+ tools, earth intelligence)
WEALTH        → WEALTH        (11-20 tools, capital intelligence)
WELL          → WELL          (17+ tools, human readiness)
A-FORGE       → a-forge-mcp   (29 tools, execution engine)
AAA           → aaa-a2a       (A2A gateway + cockpit)
OpenClaw GW   → openclaw      (A2A mesh)
```

**Making OUR servers discoverable** (the outward direction — most requests forget this half):
4-layer discovery pipeline = HTTP beacon signals → registry before aggregators → proof badge →
re-probe. Canonical spec is MCP `2026-07-28` with OAuth metadata per RFC 8414 (AS metadata) and
RFC 8705 (PRM), advertised through the `MCP-Protocol-Version` header.

```bash
# registry publish (Smithery / Glama) — prepare config, authenticate, publish, verify 200 not 404
# namespace: arifbfazil
```

**Absorbed, read on demand:** `references/absorbed-mcp-ecosystem-indexing.md` (discovery pipeline,
beacon verification, pitfalls) · `references/absorbed-forge-mcp-registry-publish.md` (auth, scoped
tokens, scoped-namespace errors, verification).

### Stage 1b — SHOULD WE ADOPT IT AT ALL (procurement)

**Observable:** you are choosing *whether / which* server to install, not operating one you already have.
Read `references/absorbed-mcp-sota-shopping-list.md`: the MCP context tax (15+ servers consume 30–40% of the
session window before any work starts), the install rule (**MCPs for state or data an agent cannot reach from
a shell — never MCPs wrapping a local CLI**), and the 2026-09 per-category shortlist with live status.


---

## Stage 2 — PROBE

**The law:** *when a probe returns a protocol or lifecycle error, suspect the probe before reporting
the target as broken.* Most "organ X is broken" findings are probe-method artifacts.

### 2a. The handshake — before any interpretation

A streamable-HTTP MCP server answers only after a 3-step lifecycle. A raw `curl` that skips it gets
a protocol error, and that error is **correct server behaviour**.

```
1. POST initialize                 -> capture `Mcp-Session-Id` from the RESPONSE HEADER
2. POST notifications/initialized  -> 202, EMPTY body, NO `id` field (send WITH the session header)
3. POST tools/list | resources/list | tools/call  -> now returns real data
```

Send `Content-Type: application/json` **and** `Accept: application/json, text/event-stream` on every call.

```bash
for p in 8081:geox 18082:wealth 18083:well; do
  port=${p%%:*}; name=${p##*:}
  hdr=$(curl -s -D - -o /dev/null --max-time 10 -X POST "http://127.0.0.1:$port/mcp" \
    -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}')
  sid=$(echo "$hdr" | grep -i '^mcp-session-id:' | tr -d '\r' | awk '{print $2}')
  [ -n "$sid" ] || { echo "$name: NO SESSION HEADER"; continue; }
  curl -s -X POST "http://127.0.0.1:$port/mcp" \
    -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
    -H "Mcp-Session-Id: $sid" -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
done
```

**The three misreadings, verbatim.**

| Raw probe returned | What it actually is | What it is NOT |
|---|---|---|
| `SESSION_MISSING: Mcp-Session-Id header required` | the server asking for the documented handshake | an unsatisfiable contract |
| `Missing session ID` / `tools/call rejected until client sends notifications/initialized` | step 2 never sent | a runtime guard blocking the tool |
| `Unknown tool: '<name>'` | the name was never advertised | an advertised-but-unreachable tool |

### 2b. Four numbers, never one

```
curl -s :PORT/tools        # DECLARED   — what the REST surface advertises
# handshake + tools/list   # EXPOSED    — what a client can enumerate
# handshake + tools/call   # CALLABLE   — prove end-to-end; a list entry proves nothing
#                          # AUTHORIZED — does an envelope permit the call
```

Report the four separately. Never average them, never quote one as another. DECLARED and EXPOSED
may disagree in either direction and a one-entry gap is a finding. `callable: 0` on a tool you never
handshaked is not a finding — it is an unfinished probe.

Output contract, always name the **first failing transition**:

```
organ | port | DECLARED n | EXPOSED n | CALLABLE n | first failing transition | verdict
```

**Exact-name check** before any broken verdict (near-miss names differ only by a suffix and fail
identically to a real defect). **One organ label may be several surfaces** — enumerate `ss -tlnp`
first; two auditors comparing different ports will disagree with neither being wrong, so always
state which port a verdict came from. **Use the installed instrument, not a hand count.**

### 2c. Is it alive? — the health map

| Node | URL | Transport | Expected (NOT a failure) |
|------|-----|-----------|--------------------------|
| arifOS | http://127.0.0.1:8088/mcp | streamable-http | 200 / JSON |
| GEOX | http://127.0.0.1:8081/mcp | streamable-http | 405 (POST only) |
| WEALTH | http://127.0.0.1:18082/mcp | streamable-http | JSON-RPC error on GET |
| WELL | http://127.0.0.1:18083/mcp | streamable-http | JSON-RPC error on GET |
| A-FORGE | http://127.0.0.1:7072/mcp | streamable-http | JSON-RPC error on GET |

> **Only connection-refused / timeout / 000 / 502 / 503 is a real failure signal.** An HTTP
> 401/403 means the service is UP and auth-gated. WEALTH/WELL JSON-RPC errors on GET are normal.

```bash
for port in 8088 8081 18082 18083 7072; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://127.0.0.1:${port}/mcp" || echo "000")
  echo "Port $port: HTTP $code"
done
```

### 2d. Is my edit live? — a file edit is not a live fix

Expect **two independent loaders**, neither of which hot-reloads: a systemd HTTP unit owning a port,
and a **stdio child spawned once per gateway, not per session**. Both hold the imported module for
days.

- Compare the **loader PID start time against the edited file's mtime**: `PID start < file mtime` ⇒ stale code.
- Resolve symlinks before diffing; confirm with `systemctl cat` that `ExecStart` points at the file you edited.
- Verify on a **fresh stdio spawn**, not through the live transport. Tests import the module; the live process does not.
- A restart from **inside** a gateway session signals your own process — activation is an operator action.
- **Ghost capability:** a tool that returns a constant (or a collection initialised empty and never appended to) never errors, so nothing surfaces it. Probe with two payloads that must differ; if output does not move with input, it is a stub. Silence and failure must be distinguishable — an empty result needs an explicit reason field.

**Reporting contract:** state *what is fixed on disk* (with hash), *what the running process still
serves*, and *what activation requires*. "Fixed on disk, not live" is a complete and honest status.

### 2e. Transport / auth shape

External clients (Claude, ChatGPT, Cursor, Gemini) expect **Streamable HTTP** (`POST /mcp`), not SSE
(`GET /sse`). With `transport="sse"` they fail `POST /sse → 405` and `POST /mcp → 404`.

```python
# BEFORE: mcp.run(transport="sse", ...)      AFTER: mcp.run(transport="streamable-http", ...)
```

Also remove any Caddy `rewrite * /sse` so `POST /mcp` reaches the backend, then restart (transport is
module-level config). **Proven:** CHRON MCP (:18102). **Pitfall:** SSE still works for local clients,
so the defect only shows on external platforms — test both.

**Absorbed, read on demand:** `references/absorbed-mcp-organ-probe.md` (+ `references/absorbed-mcp-organ-probe/references/layer-drop-diagnosis.md`) · `references/absorbed-mcp-edit-activation.md` · `references/absorbed-mcp-transport-fix.md` · `references/absorbed-FORGE-mcp-lifeguard.md` (alert conditions, auto-restart loop, Ollama pre-warm).

**Related instrument:** `runtime-probe` (`core/mcp/runtime-probe`) — one-shot health + schema +
transport classification. **Related discipline:** `agent-tool-verification` — stub sweep and live-code
check for *any* tool, not only MCP.

---

## Stage 3 — INTEGRATE

### 3a. Build (FastMCP, Python)

```bash
uv add "fastmcp[tasks]==3.4.2"                          # in a federation repo
pip install --break-system-packages "fastmcp[tasks]==3.4.2"   # system-wide
fastmcp --version                                       # expect 3.4.2

fastmcp scaffold --template api_wrapper --name "My API" --output ./my_server.py
fastmcp inspect my_server.py:mcp                        # ALWAYS inspect before wiring a client
fastmcp list my_server.py:mcp --json
fastmcp call my_server.py:mcp get_customer customer_id=cust_123 --json
fastmcp run my_server.py:mcp --transport streamable_http --host 127.0.0.1 --port 8000
```

```python
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("my-server")

class CustomerOutput(BaseModel):
    id: str
    name: str
    segment: str
    confidence: float

@mcp.tool()
def get_customer(customer_id: str) -> CustomerOutput:
    """Fetch customer by ID with confidence score."""
    ...
```

**Federation conventions.**

| Convention | Rule |
|-----------|------|
| **Transport** | `streamable-http` for all federation servers |
| **Naming** | `{service}_{action}_{resource}` — e.g. `geox_well_analyze_log` |
| **Tool count** | Start with 1–3 high-value tools, expand only when stable |
| **Error handling** | Return structured errors, never raise raw exceptions |
| **Auth** | Environment variables only, never hardcoded |
| **Output schema** | Pydantic v2 BaseModel for all tool outputs |
| **Bind** | `127.0.0.1`; let Caddy terminate TLS |

### 3b. A UI surface (MCP Apps)

Three return channels, text fallback always shipped, data tools separated from render tools, CSP via
`_meta.ui.csp`, double-iframe sandbox, predeclared resources (not ad-hoc HTML). On the Python side,
FastMCP `app=True`. Tool annotations and `outputSchema` families are a host gate — see the absorbed
reference for the 4-annotation taxonomy and the ChatGPT-native (2026-07) binding keys.

### 3c. Wire a client — use the script, not hand-edits

**Mechanism:** `/root/scripts/hermes_mcp_wire.py` (`plan | apply --sanitize | verify`) plus
`/root/scripts/mcp_probe.py` (raw JSON-RPC stdio/HTTP prober). The script guarantees a timestamped
backup, atomic replace (chmod 600), fail-closed preflight (absolute command must exist; every
`${VAR}` must be defined in `/root/.hermes/.env`), semantic verify of every top-level key before and
after write, rollback on failure, and idempotency.

`${VAR}` interpolation **is** supported for `mcp_servers`; secrets live in `/root/.hermes/.env`
(mode 600). Restart-free proof: `hermes mcp test <name>` — it resolves the placeholder and lists tools.

Pitfalls that each cost real debugging time:

1. **Text-insert index shift = silent YAML corruption.** Re-verify by `yaml.safe_load` deep-compare after every insert.
2. **Never `npx` a server that 1mcp also runs** — shared `/root/.npm/_npx/<hash>` → `ENOTEMPTY`. Install globally, reference by absolute path.
3. **`yaml.safe_dump` emits indent-0** — indent by 2 before splicing under `mcp_servers`. Never `safe_dump` a config that carries provenance comments.
4. **`mcp-stderr.log` is never rotated by Hermes** — logrotate `copytruncate` only; `mv` orphans the live fd.
5. **In-place edits happen while other agents edit the same file** — re-read at apply time, diff against the backup you just took.
6. **`patch` is blocked for `/root/.hermes/config.yaml`** (security guard) — that is why the script exists.

### 3d. Keep it affordable — schema compression

Tool *metadata*, not reasoning, is often the binding constraint. Measured on our own servers:

| server | tools | schema tokens |
|---|---|---|
| aforge | 126 | **58,403** |
| geox | 31 | 12,721 |
| well | 31 | 5,356 |
| wealth | 11 | 4,034 |

Wrap with the federation wrapper — never the raw binary:

```bash
/root/scripts/mcp-compress.sh <name> -c medium -- <command> [args...]

python3 /root/scripts/hermes_mcp_compress.py plan   <server> [level]   # dry run
python3 /root/scripts/hermes_mcp_compress.py apply  <server> [level]   # backup+write+verify
python3 /root/scripts/hermes_mcp_compress.py revert <server>
python3 /root/scripts/hermes_mcp_compress.py status
```

`medium` by default (keeps descriptions; −89.3% on aforge). `max` saves most (−97.8%) and risks wrong
tool selection. After wrapping: discover (`get_tool_schema`) then invoke (`invoke_tool`); **prove one
real call** — listing tools is not evidence; restart the *consuming agent*, not just the server.

Limits: **stdio only** (HTTP/URL backends die on the OAuth handshake — bridge to stdio first); not
worth wrapping under ~15 tools; `skills + CLI beats MCP` for anything with a good local CLI. A
wrapper working in your shell can fail under systemd (`HOME`/`PATH`), and **secrets must load in every
entry point**, not just `main()`.

### 3e. External platforms and other targets

- **External platforms (Composio, social-mcp, xurl, Firecrawl)** wire the same way, with 3-band APA governance on the tool surface.
- **A2A** — MCP + A2A agentic inter-agent communication and task delegation; refusal surface documented.
- **Direct client invoke** — when a wrapper fails, call the server from a Python streamable-HTTP client (MiniMax media lane; model IDs and quota error codes documented).
- **Telegram products on MCP backends** — lane map and per-product delivery pattern; *bot lanes/tokens/routing belong to the telegram cluster, not here.*

**Absorbed, read on demand:** `references/absorbed-forge-fastmcp.md` · `references/absorbed-forge-mcp-gui.md` · `references/absorbed-forge-mcp-a2a-agentic.md` · `references/absorbed-external-platform-mcp.md` (+ its `references/`) · `references/absorbed-mcp-context-compression.md` · `references/absorbed-forge-minimax-mcp-direct-invoke.md` · `references/absorbed-telegram-mcp-product-line.md`. The `.hermes`-tree case-variants (`FORGE-fastmcp`, `FORGE-mcp-gui`, `FORGE-mcp-a2a-agentic`) are preserved as `references/absorbed-FORGE-*.md`; their only delta was a stale claim that the 2026-07-20 GUI blueprint still exists on disk (**it does not** — verified 2026-09-19; the AAA text is the corrected one).

---

## Stage 4 — TEST

> **Iron rule: MCP servers are tested with MCPJam Inspector, not with coding agents.** Coding agents
> build MCP servers; MCPJam tests them.

| Situation | Use |
|-----------|-----|
| Quick organ health (our 6 organs) | Smoke test |
| Protocol-era / stateless discovery on any endpoint | Probe (MCPJam CLI/SDK) |
| Deep conformance, tool-call verification, OAuth debugging | Testing (MCPJam Inspector) |
| CI gating on PRs | Probe (SDK) or Inspector evals |

```bash
npx @mcpjam/inspector@latest http://127.0.0.1:8088/mcp                 # probe one endpoint
npx @mcpjam/inspector@latest doctor http://127.0.0.1:8088/mcp          # smoke + capability report
npx @mcpjam/inspector@latest oauth --version 2025-11-25 http://127.0.0.1:8088/mcp
docker run -p 127.0.0.1:6274:6274 mcpjam/mcp-inspector                 # air-gap, 127.0.0.1 only

# federation sweep
for port in 8088 7071 7072 8081 18082 18083 3001; do
  echo "=== :$port ==="
  npx @mcpjam/inspector@latest doctor "http://127.0.0.1:$port/mcp" 2>&1 | head -30
done
```

Canonical baseline: `https://stateless.mcpjam.com/mcp` (stateless MCP 2.0 reference, protocol
`2026-07-28`, 13 tools, no auth). Every coding agent should wire it, probe it once at boot to confirm
its own client speaks the era, and use it as the comparison baseline.

**Three rules for a stateless `2026-07-28` call — all three are required:**
`MCP-Protocol-Version: 2026-07-28` as a **header** (not body `params.protocolVersion`); `Mcp-Method:
<method>` header for routing; `_meta.io.modelcontextprotocol/*` envelope keys (not `_meta.protocolVersion`).

| Era | Version | Wire shape | arifOS |
|-----|---------|------------|--------|
| **Modern (preferred)** | `2026-07-28` | stateless: `server/discover`, no `Mcp-Session-Id`, per-request `_meta` | supported |
| Legacy handshake | `2025-11-25` | initialize + session | supported |

Conformance matrices by layer (boot-contract invariants, `structuredContent` vs `outputSchema`, error
surface, auth matrix, host-surface evidence gates) plus the per-layer probe recipes live in the
absorbed reference — load it before claiming conformance.

**Absorbed, read on demand:** `references/absorbed-mcp-testing.md`.

---

## Stage 5 — GOVERN

Deterministic interception, not policy prose. The governance wrapper is four mechanisms: a **zero-LLM
intent router**, a **per-agent role ACL**, a **reversibility wrapper**, and a **governed dynamic policy
layer**; three-tier runtime governance (solo fast-path → musyawarah → gotong royong + F1 gate) decides
when a call needs deliberation. The failure it exists to kill is the **false-confidence paradox**.

**Drift audit — the questions that actually find defects:** run the inspector *then distrust it*.

- **Surface ≠ usage.** Inventory which tools exist vs which are actually used, measured from the ledger, before proposing a cut or an upgrade.
- **Many tools failing at once = dependency-pin drift, not per-organ breakage.**
- **Surface ≠ surface.** One server can present several disagreeing views; a split tells you there is a conflict, not who wins. A false paradox is usually two orthogonal measures.
- **Probe an attestation function per question, never as a single boolean.**
- **Verify an external audit artifact before acting on it.** Authority failures are silent (feedback asymmetry); the authority surfaces are disconnected.

**Lifeguard — standing recovery, when authorised.** Alert conditions: MCP HTTP 000/502/503 → restart
container + log; response > 3s → WARN; provider 401/402 → disable from the fallback chain; Ollama
cold-start > 15s → pre-warm via `/api/generate`.

1. **Never restart Vault999** — append-only ledger, human ack required.
2. **Restart one MCP at a time** — avoid federation cascade.
3. Log to `~/.openclaw/workspace/logs/mcp-lifeguard.log`.
4. Disable dead models — don't let 402s burn event-loop cycles.

**Absorbed, read on demand:** `references/absorbed-forge-mcp-governance-wrapper.md` (+ `templates/mcp-governance-policy.toml`, `references/`) · `references/absorbed-federation-mcp-drift-audit.md` (+ runnable `scripts/mcp_surface_usage_audit.py`, `scripts/mcp_surface_conformance_sweep.py`) · `references/absorbed-FORGE-mcp-lifeguard.md`.

---

## Stage 6 — RETIRE

A retired server or name must still be findable, and its content must never be lost.

1. **Freeze, do not delete.** `mv <skill-dir> /root/AAA/skills/.frozen/<YYYY-MM-DD>-<reason>/` and rename its `SKILL.md` → `SKILL.md.from.<tree>` (a literal `SKILL.md` inside `.frozen` inflates every census and can be re-loaded by a recursive scanner).
2. **Preserve the body where it stays discoverable** — `references/absorbed-<name>.md` inside the surviving owner, listed in `references/absorbed-INDEX.md`.
3. **Tombstone the name** — leave `<name>.DEPRECATED-<date>` resolving to the owner. Do not delete the old name; a name that stops resolving is indistinguishable from a name that was never there.
4. **Repoint inbound links** and re-run the census. **Check inbound dependents before moving or archiving anything** — a directory that looks empty may be the live body behind a symlink elsewhere, and removing it breaks every link silently.
5. **Re-measure.** A name is only retired when the census and the resolution gate both agree.

**Worked example — this skill.** 19 names were absorbed into `mcp-ops` on 2026-09-20: originals moved
to `.frozen/2026-09-20-mcp-consolidation/`, bodies preserved as `references/absorbed-*.md`, and every
old name left resolving as a symlink to this directory. See `references/absorbed-INDEX.md`.

---

## Troubleshooting

```bash
# MCP not responding — raw JSON-RPC (remember the 3-step handshake first)
curl -s -X POST http://localhost:8081/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Port conflict
ss -tlnp | grep <port>

# Which loader is serving this file?
ps -eo pid,ppid,lstart,cmd | grep "<server>.py" | grep -v grep
systemctl cat <name>-mcp.service

# FastMCP version / config sanity
fastmcp --version
mcporter config list
hermes mcp test <name>
```

## Allowed Tools

| Tool / Capability | Purpose |
|-------------------|---------|
| `fastmcp` CLI | Scaffold, inspect, list, call, run FastMCP servers |
| `mcporter` CLI | Discover and call servers; daemon, auth, config, codegen |
| `npx @mcpjam/inspector` | Conformance probe, doctor, OAuth check |
| `curl` / `python3 -m json.tool` | Health probes and raw JSON-RPC checks |
| `uv` / `pip` | Install FastMCP in repo or system context |
| `/root/scripts/hermes_mcp_wire.py` | Governed client-config wiring (plan/apply/verify) |
| `/root/scripts/hermes_mcp_compress.py` | Governed schema-compression wrap |
| `docker restart` | Auto-restart dead MCP containers (lifeguard, authorised only) |

## Forbidden Actions

- **NEVER** expose a FastMCP server on `0.0.0.0` in production; bind `127.0.0.1` and let Caddy terminate TLS.
- **NEVER** hardcode credentials; environment variables or SOPS only.
- **NEVER** call a mutating tool on a live federation organ without arifOS judgment.
- **NEVER** skip `fastmcp inspect` before wiring a new server into a client.
- **NEVER** report "fixed" from a diff alone — say "fixed on disk, not live" until a fresh process proves it.
- **NEVER** report an organ broken from a single un-handshaked probe.
- **NEVER** treat a successful health check as authorization to act beyond observer class.
- **NEVER** restart Vault999 — append-only ledger, human ack required.
- Escalate to **arifOS 888_JUDGE** for deletion, deployment, secrets, or constitutional files.

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Mutating action on live organ | arifOS 888_JUDGE | A2A / MCP verdict_request |
| Secret exposure in config or code | security agent + arifOS judge | A2A message |
| Federation organ degraded/down | A-FORGE + health triage | health probe + incident channel |
| Production deployment needed | arifOS 888_JUDGE + human (F13) | 888 HOLD |
| Tool call returns unexpected authority/scope | arifOS 888_JUDGE | hold with evidence |

## Sibling skills (kept separate, deliberately)

| Skill | Why it is not merged here |
|---|---|
| `wealth-mcp-ops` | WEALTH-organ MCP tools (testing + hardening); organ-bounded, own repo layout. |
| `runpod-mcp` | Platform lane: Runpod pods/endpoints/jobs. Distinct triggers and setup. |
| `touchdesigner-mcp` | Platform lane: twozero MCP for TouchDesigner. Distinct triggers and tool surface. |
| `runtime-probe` | Focused instrument: one-shot MCP health + schema + transport classification. |
| `agent-tool-verification` | General claim discipline for any tool, not only MCP. |
| `qwen-harness-tools` | Model-side built-in harness tools; not MCP at all. |
| ~~`mcp-sota-shopping-list`~~ | **FOLDED IN (2026-09-20, v3.0.1)** — now Stage 1b / `references/absorbed-mcp-sota-shopping-list.md`; the name is a tombstone. The v3.0.0 decision was to keep it separate as a procurement reference, the second pass folded it so that "which MCP server should we adopt" lands on a reference instead of routing away. **Both statements are kept: the contradiction is the trail.** |

## References

| File | Stage | Absorbed from |
|---|---|---|
| `references/absorbed-INDEX.md` | all | full name → phase → origin → preserved path map |
| `references/absorbed-*.md` | as listed above | the retired skills' bodies, verbatim |
| `references/pre-merge-mcp-ops-v2.1.0.md` | all | this skill's own pre-merge body (2026-08-26 consolidation) |

*Consolidated 2026-08-26 from FORGE-mcp-ops, FORGE-mcp-federation-ops, FORGE-mcp-lifeguard.*
*Consolidated 2026-09-20 (v3.0.0): 19 further MCP names absorbed — see `references/absorbed-INDEX.md`.*
*2026-09-20 (v3.0.1, second pass): trigger list completed to the full declared union of the 14
assigned MCP members (36 triggers added — the v3.0.0 list dropped the declared surfaces of mcp-testing,
mcp-organ-probe, mcp-edit-activation and mcp-ops); mcp-sota-shopping-list folded in as Stage 1b; all 14
member names archived to `.archive/merge-20260920/mcp/` and left resolving as tombstones.*
*AAA Skill Library — DITEMPA BUKAN DIBERI ⚒️*
