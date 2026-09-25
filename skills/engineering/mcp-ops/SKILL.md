---
name: mcp-ops
description: "Use when working with MCP servers — learn, discover, probe, build, secure, test, extend, publish, govern, retire. The canonical Model Context Protocol skill, accordant to https://modelcontextprotocol.io/llms.txt (8-stage workflow). One owner for the whole MCP lifecycle across federation, vendor, registry, and external hosts."
id: mcp-ops
version: 3.2.0
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F4, F8, F10, F11, F12, F13]
autonomy_tier: T1
capability_tier: fed-agent-subagent
ecology_state: WARM
aligned_to:
  - https://modelcontextprotocol.io/llms.txt
  - canonical MCP spec 2026-07-28 (stateless preferred) and 2025-11-25 (legacy handshake)
  - RFC 8414 (AS metadata) + RFC 8705 (PRM) + RFC 9728 (Protected Resource Metadata)
  - MCP-Protocol-Version header convention
tags: ["mcp", "lifecycle", "mcporter", "fastmcp", "probe", "transport", "wiring", "conformance", "mcpjam", "governance", "drift", "compression", "discovery", "registry", "apps", "oauth", "prm", "sep", "skills", "build-with-agent-skills", "fastmcp[tools]", "streamable-http", "era-2026-07-28", "era-2025-11-25"]
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
  - FORGE-mcp-testing
  - FORGE-mcp-governance-wrapper
  - forge-mcp-governance-wrapper
  - mcp-organ-probe
  - mcp-edit-activation
  - mcp-transport-fix
  - mcp-ecosystem-indexing
  - forge-mcp-registry-publish
  - federation-mcp-drift-audit
  - external-platform-mcp
  - mcp-context-compression
  - forge-minimax-mcp-direct-invoke
  - telegram-mcp-product-line
  - mcp-testing
  - mcp-sota-shopping-list
triggers:
  - "MCP server"
  - "Model Context Protocol"
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
  - "stateless MCP"
  - "server/discover"
  - "wire an MCP server into Hermes"
  - "MCP tool schemas eating context"
  - "publish MCP to Smithery or Glama"
  - "MCP Apps"
  - "MCP governance wrapper"
  - "MCP drift audit"
  - "MCP 400 on stateless probe"
  - "MCP CI gate"
  - "MCP OAuth conformance"
  - "OAuth 2.1 MCP"
  - "Protected Resource Metadata MCP"
  - "RFC 8414 MCP"
  - "RFC 8705 MCP"
  - "MCP auto-recovery"
  - "MCP health check"
  - "MCP probe"
  - "MCP schema validation"
  - "MCP server test"
  - "MCP server validation"
  - "server/discover fails"
  - "MCP smoke test"
  - "MCP test"
  - "Skills over MCP"
  - "MCP Tasks extension"
  - "MCP Apps extension"
  - "MCP enterprise-managed authorization"
  - "Enterprise MCP"
  - "MCP SEP"
  - "MCP Registry"
  - "MCP registry publish"
  - "MCP registry aggregator"
  - "MCP Glossary"
  - "MCP AICG"
  - "MCP roadmap"
  - "Build with Agent Skills MCP"
  - "FastMCP tasks"
  - "FastMCP scaffold"
  - "FastMCP inspect"
  - "Streamable HTTP MCP"
  - "stdio MCP"
  - "MCP server build"
  - "MCP client build"
  - "MCP SDK"
negative_triggers:
  - "WEALTH MCP tools"  #            → wealth-mcp-ops (organ-bounded)
  - "Runpod MCP"  #                   → runpod-mcp (platform lane)
  - "TouchDesigner MCP"  #            → creative/touchdesigner-mcp (platform lane)
  - "runtime MCP probe (one-shot)"  # → core/mcp/runtime-probe (focused instrument)
---

# MCP Operations — one owner for the canonical MCP lifecycle

> **The flow, accordant to https://modelcontextprotocol.io/llms.txt:**
> `LEARN → DISCOVER → PROBE → BUILD → SECURE → TEST → EXTEND → PUBLISH → GOVERN (with RETIRE)`
> Canonical MCP — get the concepts right, then know which stage owns your problem.
> *mcporter* discovers. *FastMCP* builds. *MCPJam Inspector* tests. *The Registry* publishes. *arifOS* governs.
> A file edit is never a live fix. DITEMPA BUKAN DIBERI ⚒️

## Overview

This is the AAA canonical skill for the Model Context Protocol. It is one owner for the full **eight-stage MCP lifecycle** that the Model Context Protocol project documents at `https://modelcontextprotocol.io/llms.txt`. It supersedes 24 prior MCP skill names (see `supersedes:` above and `references/absorbed-INDEX.md`). All of those names resolve as tombstones pointing here.

The eight stages fold one-to-one onto the canonical llms.txt workflow:

| Stage | llms.txt section(s) | Question you actually ask |
|---|---|---|
| **0 LEARN** | `getting-started/`, `architecture`, `server-concepts`, `client-concepts`, `versioning`, `sdks` | "What IS MCP? Which version? Which SDK?" |
| **1 DISCOVER** | `registry/about`, `registry/quickstart`, discovery beacons, Skills extension | "Which servers exist? Which can we adopt?" |
| **2 PROBE** | `develop/connect-local-servers`, `develop/connect-remote-servers`, transports | "Is it alive? Is my edit live? What's the four-number truth?" |
| **3 BUILD** | `develop/build-server`, `develop/build-client`, `develop/build-with-agent-skills`, `client-best-practices`, Apps | "How do I write an MCP server / client / agent skill?" |
| **4 SECURE** | `tutorials/security/authorization`, `tutorials/security/security_best_practices`, `extensions/auth/*`, `extensions/auth/enterprise-managed-authorization` | "How do I prove a request is authorized? What does OAuth 2.1 require?" |
| **5 TEST** | `tools/inspector/*`, `debugging`, conformance era matrix | "Does it conform? Does it work end-to-end across eras?" |
| **6 EXTEND** | `extensions/apps/*`, `extensions/tasks/*`, `extensions/skills/*`, `extensions/auth/oauth-client-credentials` | "How do I add UI / async tasks / agent skills / client credentials?" |
| **7 PUBLISH** | `registry/quickstart`, `registry/versioning`, `registry/authentication`, `registry/github-actions`, `registry/moderation-policy`, `registry/registry-aggregators`, `registry/terms-of-service` | "How do I ship to MCP Registry / Smithery / Glama?" |
| **8 GOVERN (and RETIRE)** | `seps/*`, `community/governance`, `community/working-interest-groups`, `community/contributor-ladder`, `community/feature-lifecycle`, `community/sdk-tiers`, deprecated features | "Who decides? When does a name retire? How do I file a SEP?" |

Plus four always-on overlays:
- **F12 INJECTION** — every probe, registry record, and Skills description is scanned.
- **F11 AUDIT** — every decision is logged via `arifOS arif_judge`.
- **F2 TRUTH** — every claim is labeled `OBS · DER · INT · SPEC · UNKNOWN`.
- **F13 SOVEREIGN** — irreversible mutations and canonical decisions stay with F13.

This is a **T1/T2 skill for read-only probes and in-lane builds**. Anything that mutates a live federation organ, deletes a registry record, rotates a secret, or changes F1–F13 escalates to `arifos 888_JUDGE` (`a2a` or `mcp verdict_request`).

## Stage 0 — LEARN  (get the concepts right)

The Model Context Protocol is a JSON-RPC 2.0 surface between **client** (host application) and **server** (tool/resource/prompt provider). Three primitives: **tools** (model-controlled actions), **resources** (app-controlled reads), **prompts** (user-controlled templates). Plus four utilities: sampling (model inside server), elicitation (server asks human), roots (filesystem boundaries), tasks (async long-running).

```
client ──JSON-RPC── server
  tools/resources/prompts ──►
  notifications/initialized ──►
  sampling/elicitation/roots ────►  (request → server)
  notifications/message ◄────  (server → client push)
```

**Architectural layers** (per `architecture/`):

1. **transports** — `stdio` or `Streamable HTTP` (replaces SSE; SEP-2243)
2. **protocol** — JSON-RPC framing, session lifecycle, multi-round-trip requests (MRTR), pagination, cancellation, progress, ping
3. **authorization** — OAuth 2.1 with Protected Resource Metadata (RFC 9728) and client-credentials for M2M
4. **server primitives** — discovery (stateless), prompts, resources, tools, completion, logging, caching, pagination
5. **client primitives** — sampling, elicitation, roots (deprecated per SEP-2577)
6. **extensions** — optional SEPs (Apps, Skills, Tasks, Auth-extensions)

**Era map** (probe, build, and test must declare which era they target):

| Era | Version | Wire shape | Federation status |
|---|---|---|---|
| **Modern (preferred)** | `2026-07-28` | stateless: `server/discover`, no `Mcp-Session-Id`, per-request `_meta.io.modelcontextprotocol/*` | supported |
| Legacy handshake | `2025-11-25` | `initialize` + `notifications/initialized` + `Mcp-Session-Id` | supported |
| Pre-deprecation | `2025-06-18`, `2025-03-26`, `2024-11-05` | legacy lifecycle | shim only |
| Draft | `draft/` | bleeding edge, may break | rare |

**SDKs** (`sdks.md`): official TypeScript, Python, Java, Kotlin, C#, Ruby, Go, Rust, PHP, Swift. Tiering per `community/sdk-tiers.md`. CLI from `npx @modelcontextprotocol/...`, Python via `pip install mcp`, JS via `@modelcontextprotocol/sdk`.

**Allowed Tools**: `webfetch` (read `modelcontextprotocol.io/spec/2026-07-28/...`)

**Forbidden Actions**: do not import a `2026-07-28`-shaped client into a `2025-06-18`-shaped server without an era adapter.

## Stage 1 — DISCOVER  (find servers, decide to adopt)

Two questions: **what exists?** and **should we adopt it?**

**Discovery pipeline (4-layer, outward → inward)**:

1. **HTTP beacon signals** at `/.well-known/mcp.json` (or `/.well-known/mcp/`).
2. **MCP Registry** (`https://modelcontextprotocol.io/registry/about`) — official, named namespaces (e.g., `arifbfazil/...`), versioned, authenticatable per `registry/authentication.md`.
3. **Aggregators** — Smithery, Glama, PulseMCP — pull from the registry, may add editorial layers.
4. **Re-probe** — always. A registry entry is `DER`, not `OBS`.

**Adoption check (Stage 1b)** before installing: read `references/absorbed-mcp-sota-shopping-list.md`. The MCP context tax (15+ servers consume 30–40% of the session window before any work starts) means **MCPs are only for state/data an agent cannot reach from a shell — never MCPs wrapping a local CLI**.

**Find existing servers** (in our federation):

```bash
mcporter list                                     # all known
mcporter list arifOS --schema                     # one server + tools
mcporter list --http-url http://127.0.0.1:8081/mcp --name geox   # ad-hoc HTTP
mcporter config list                              # what is configured
```

**Federation MCP inventory** (as known to mcporter):

```
arifOS MCP      → arifOS        (8 canonical verbs, F1-F13)
GEOX            → geox          (28+ tools, earth intelligence)
WEALTH          → WEALTH        (11-20 tools, capital intelligence)
WELL            → WELL          (17+ tools, human readiness)
A-FORGE         → a-forge-mcp   (29 tools, execution engine)
AAA             → aaa-a2a       (A2A gateway + cockpit)
OpenClaw GW     → openclaw      (A2A mesh)
```

**Publishing-side discovery** — how to make *our* servers discoverable — lives in Stage 6 PUBLISH.

**Allowed Tools**: `mcporter` CLI; `curl` against `modelcontextprotocol.io/registry/v0/...`; `firecrawl_firecrawl_search` (Stage 1b ad-hoc when MCP Registry is unreachable); `webfetch`.

**Forbidden Actions**: installing an MCP wrapper around a CLI you could `shell_exec` instead.

## Stage 2 — PROBE  (is it alive, is my edit live)

The law: *when a probe returns a protocol or lifecycle error, suspect the probe before reporting the target as broken.* Most "organ X is broken" findings are probe-method artifacts.

### 2a — The handshake (3-step lifecycle, both eras)

Streamable-HTTP MCP answers only after the lifecycle. A raw `curl` that skips it gets a protocol error, and that error **is correct server behaviour**.

**Legacy era (`2025-11-25`)**:

```
1. POST initialize                 → capture `Mcp-Session-Id` from the RESPONSE HEADER
2. POST notifications/initialized  → 202, EMPTY body, NO `id` field (with session header)
3. POST tools/list | resources/list | tools/call → real data
```

**Stateless era (`2026-07-28`)** (preferred):

```
1. POST server/discover           → tool/resource/prompt catalog
2. POST tools/invoke (or call)     → directly, no session header
   • `MCP-Protocol-Version: 2026-07-28` header (NOT in `params`)
   • `Mcp-Method: <method>` header for routing
   • per-request `_meta.io.modelcontextprotocol/*` envelope keys
```

**Universal curl invariants** on every call:

```
Content-Type: application/json
Accept: application/json, text/event-stream
```

**The three misreadings (verbatim):**

| Raw probe returned | What it actually is | What it is NOT |
|---|---|---|
| `SESSION_MISSING: Mcp-Session-Id header required` | server asking for documented handshake | an unsatisfiable contract |
| `Missing session ID` / `tools/call rejected until client sends notifications/initialized` | step 2 never sent | a runtime guard |
| `Unknown tool: '<name>'` | name never advertised | advertised-but-unreachable |

Deep dive: `references/absorbed-mcp-organ-probe.md` (+ `layer-drop-diagnosis.md`).

### 2b — Four numbers, never one

```
curl -s :PORT/mcp                          # DECLARED — REST surface advertises
# handshake + tools/list                   # EXPOSED — what a client enumerates
# handshake + tools/call                   # CALLABLE — end-to-end; a list entry proves nothing
#                                          # AUTHORIZED — does an envelope permit the call
```

Report each separately. Never average, never quote one as another. The output contract — always name the **first failing transition**:

```
organ | port | DECLARED | EXPOSED | CALLABLE | first failing transition | verdict
```

**Exact-name check** first (near-miss names fail identically to real defects). **One organ may be several surfaces** — enumerate `ss -tlnp`; always state which port a verdict came from. **Use the installed instrument, not a hand count.**

### 2c — Health map (current federation)

| Organ | URL | Transport | Expected (not a failure) |
|---|---|---|---|
| arifOS | `http://127.0.0.1:8088/mcp` | Streamable HTTP | 200 / JSON-RPC |
| GEOX | `http://127.0.0.1:8081/mcp` | Streamable HTTP | 405 on GET (POST only) |
| WEALTH | `http://127.0.0.1:18082/mcp` | Streamable HTTP | JSON-RPC error on GET |
| WELL | `http://127.0.0.1:18083/mcp` | Streamable HTTP | JSON-RPC error on GET |
| A-FORGE | `http://127.0.0.1:7072/mcp` | Streamable HTTP | JSON-RPC error on GET |

> **Only connection-refused / timeout / 000 / 502 / 503 is a real failure signal.** HTTP 401/403 means the service is UP and auth-gated.

```bash
for port in 8088 8081 18082 18083 7072; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "http://127.0.0.1:${port}/mcp" || echo "000")
  echo "Port $port: HTTP $code"
done
```

### 2d — Is my edit live? (file edit is never a live fix)

Two loaders hold the imported module for days: a systemd HTTP unit owning a port, and a stdio child spawned once per gateway (not per session). Neither hot-reloads.

- Compare **loader PID start time vs file mtime**: `PID start < file mtime` ⇒ stale code.
- Resolve symlinks before diffing; `systemctl cat` confirms `ExecStart`.
- Verify on a **fresh stdio spawn**, not through the live transport.
- Restart from inside a gateway signals your own process — activation is operator action.
- **Ghost capability**: tool returns a constant or never-initialised collection → no error surfaces. Probe with two payloads that must differ; if output doesn't move with input, it is a stub.

Reporting contract: state **what is fixed on disk** (hash), **what the running process still serves**, **what activation requires**. "Fixed on disk, not live" is a complete status.

Deep dive: `references/absorbed-mcp-edit-activation.md`.

### 2e — Transport / auth shape (SSE → Streamable HTTP)

External clients (Claude / ChatGPT / Cursor / Gemini) expect **Streamable HTTP** (`POST /mcp`), not SSE (`GET /sse`). With `transport="sse"` they fail `POST /sse → 405` and `POST /mcp → 404`.

```python
# BEFORE: mcp.run(transport="sse", ...)     AFTER: mcp.run(transport="streamable-http", ...)
```

Also remove any Caddy `rewrite * /sse` so `POST /mcp` reaches the backend, then restart (transport is module-level config). **Pitfall**: SSE still works for local clients, so the defect only shows on external platforms — test both.

Deep dive: `references/absorbed-mcp-transport-fix.md`.

**Allowed Tools**: `curl`, `mcporter`, raw JSON-RPC stdio/HTTP prober (`/root/scripts/mcp_probe.py`).

**Forbidden Actions**: reporting an organ broken from a single un-handshaked probe. Reporting a successful health check as authorization to act beyond observer class.

## Stage 3 — BUILD  (server, client, agent skills, Apps)

### 3a — Server (Python, FastMCP)

```bash
uv add "fastmcp[tasks]==3.4.2"                  # in federation repo
pip install --break-system-packages "fastmcp[tasks]==3.4.2"   # system-wide
fastmcp --version                               # expect 3.4.2
fastmcp scaffold --template api_wrapper --name "My API" --output ./my_server.py
fastmcp inspect my_server.py:mcp                # ALWAYS before wiring a client
fastmcp list my_server.py:mcp --json
fastmcp call my_server.py:mcp get_customer customer_id=cust_123 --json
fastmcp run my_server.py:mcp --transport streamable_http --host 127.0.0.1 --port 8000
```

```python
from fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("my-server")

class CustomerOutput(BaseModel):
    id: str; name: str; segment: str; confidence: float

@mcp.tool()
def get_customer(customer_id: str) -> CustomerOutput:
    """Fetch customer by ID with confidence score."""
    ...
```

Deep dive: `references/absorbed-forge-fastmcp.md`.

### 3b — MCP Apps (UI surfaces)

Three return channels, text fallback always shipped, data tools separated from render tools, CSP via `_meta.ui.csp`, double-iframe sandbox, predeclared resources (not ad-hoc HTML). On the Python side, FastMCP `app=True`.

```python
@mcp.tool(app=True)
def render_dashboard(data_id: str) -> ...: ...
```

Tool annotations and `outputSchema` families are a host gate (see `seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md` and `extensions/apps/build.md`).

Deep dive: `references/absorbed-forge-mcp-gui.md` (build recipes); `references/mcp-gui-landscape-2026-09-22.md` (GUI taxonomy — MCP Apps vs Manager GUI vs STMCP, host matrix, portability proof ladder).

### 3c — Client (any harness)

Use the canonical reference at `develop/build-client.md`. Federation uses mcporter as the discovery + codegen surface (`mcporter generate-cli --server geox`, `mcporter emit-ts geox --mode client`). Direct A2A interop lives in `references/absorbed-forge-mcp-a2a-agentic.md`.

### 3d — Build with Agent Skills (the Skills extension)

Server-side `Skills` (SEP-2640) — discover and read Agent Skills from MCP servers. Distinct from "MCP Apps for Agents". Format and discovery lives in `extensions/skills/overview.md` and `build-with-agent-skills.md`. Read `references/absorbed-mcp-ecosystem-indexing.md` for the beacon part.

### 3e — Wire to a client (governed)

**Use the script, not hand-edits**: `/root/scripts/hermes_mcp_wire.py` (`plan | apply --sanitize | verify`) and `/root/scripts/mcp_probe.py`. The script guarantees:

- timestamped backup + atomic replace (chmod 600)
- fail-closed preflight: absolute command must exist; every `${VAR}` must be defined in `/root/.hermes/.env`
- semantic verify of every top-level key before + after write
- rollback on failure; idempotency
- supports `${VAR}` interpolation for `mcp_servers`

Pitfalls (each cost real debugging time):

1. **Text-insert index shift = silent YAML corruption.** `yaml.safe_load` deep-compare after every insert.
2. **Never `npx` a server that 1mcp also runs** — shared `/root/.npm/_npx/<hash>` → `ENOTEMPTY`. Install globally, reference by absolute path.
3. **`yaml.safe_dump` emits indent-0** — indent by 2 before splicing under `mcp_servers`. Never `safe_dump` a config that carries provenance comments.
4. **`mcp-stderr.log` is never rotated by Hermes** — logrotate `copytruncate` only.
5. **In-place edits happen while other agents edit** — re-read at apply, diff against the backup just taken.
6. **`patch` is blocked for `/root/.hermes/config.yaml`** — that is why the script exists.

### 3f — Client best practices

`sdk-best-practices.md` summary: input validation errors as tool execution errors (SEP-1303), tools `inputSchema` / `outputSchema` conform to JSON Schema 2020-12 (SEP-1613/2106), tool names follow SEP-986 format, resources use SEP-2164 error code.

### 3g — Keep it affordable (schema compression)

Tool *metadata* is often the binding constraint. Measured on our own servers:

| server | tools | schema tokens |
|---|---|---|
| aforge | 126 | **58,403** |
| geox | 31 | 12,721 |
| well | 31 | 5,356 |
| wealth | 11 | 4,034 |

```bash
/root/scripts/mcp-compress.sh <name> -c medium -- <command> [args...]
python3 /root/scripts/hermes_mcp_compress.py plan   <server> [level]
python3 /root/scripts/hermes_mcp_compress.py apply  <server> [level]
python3 /root/scripts/hermes_mcp_compress.py revert <server>
python3 /root/scripts/hermes_mcp_compress.py status
```

Limits: **stdio only** (HTTP backends die on the OAuth handshake); not worth wrapping under ~15 tools; **skills + CLI beats MCP** for anything with a good local CLI.

Deep dive: `references/absorbed-mcp-context-compression.md`.

**Allowed Tools**: `fastmcp` CLI; `mcporter`; `/root/scripts/hermes_mcp_wire.py`; `mcp-compress.sh`.

**Forbidden Actions**: exposing a FastMCP server on `0.0.0.0` in production (bind `127.0.0.1`, let Caddy terminate TLS); hardcoding credentials; calling a mutating tool on a live federation organ without arifOS judgment; skipping `fastmcp inspect` before wiring a client.

## Stage 4 — SECURE  (OAuth 2.1, PRM, EAP, security baseline)

The canonical MCP security model is **OAuth 2.1 with the protocol-specific additions**. Three things break fast: (a) skipping PRM, (b) treating confidential and public clients the same, (c) ignoring enterprise-managed authorization.

### 4a — The shape (per `tutorials/security/authorization.md`)

1. **Authorization Server discovery** — `/.well-known/oauth-authorization-server` (RFC 8414 metadata).
2. **Protected Resource Metadata** — RFC 9728 (SEP-985; mandatory for OAuth 2.1 in MCP).
3. **Client registration** — dynamic via Client ID Metadata Documents (SEP-991) OR via enterprise-managed IdP (SEP-990).
4. **Token issuance** — authorization_code (interactive) or client_credentials (M2M, SEP-1046).
5. **Bearer token in `Authorization: Bearer <token>`** on every protected call.

### 4b — Enterprise-managed authorization (EAP, SEP-990)

When the operator's IdP must enforce policy (e.g., a corporate IdP can refuse to issue tokens for unauthorized tools), MCP supports **enterprise-managed authorization**. The auth server returns a `redirect` to the IdP and never returns a token to the MCP server directly. Read `extensions/auth/enterprise-managed-authorization.md`.

### 4c — OAuth client credentials (M2M, SEP-1046)

For service-to-service MCP servers that don't need a user:

```bash
curl -X POST "$AS/token" -d "grant_type=client_credentials&client_id=$ID&client_secret=$SECRET&scope=$SCOPE"
```

`extensions/auth/oauth-client-credentials.md` has the full recipe. NEVER fall back to a long-lived bearer token — use client credentials, rotate, audit.

### 4d — Security baseline (`tutorials/security/security_best_practices.md`)

- Validate every input against `inputSchema` BEFORE invoking tool logic (SEP-1303).
- Never log bearer tokens. Never write them to disk in cleartext. Never echo them.
- Use SEP-2207 OIDC-flavored refresh tokens for long sessions.
- Treat `tools/list` as partially-suspicious — every advertised tool needs a TYPE LABEL (read-only / destructive / etc.) per SEP-1034 / SEP-973.
- Time-bound responses — SEP-2549 TTL for `list` results (preventing stale caches).

### 4e — Federation-specific (constitutional)

For MCP servers we PUBLISH, F11 AUDIT requires:
- Per-call rate limit recorded as receipts.
- Per-tool side-effect declared via `declared_side_effects` (see SEC-1 in `forge_evaluate`).
- Inverse flag for destructive tools (`readOnlyHint: false`).
- `outputSchema` declared with Pydantic v2 `BaseModel` (Fortress).

**Allowed Tools**: `curl` against AS metadata; `forge_evaluate` for tool registration governance; `forge_witness` for OAuth flow tri-witness.

**Forbidden Actions**: storing secrets in `SKILL.md` or any client wire config; using `Authorization: Bearer <long-lived>` without rotation; skipping client registration metadata.

## Stage 5 — TEST  (MCPJam, debugging, era conformance)

Iron rule: **MCP servers are tested with MCPJam Inspector, not coding agents.** Coding agents build MCP servers; MCPJam tests them.

| Situation | Use |
|---|---|
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

Canonical baseline: `https://stateless.mcpjam.com/mcp` (stateless MCP 2.0 reference, protocol `2026-07-28`, 13 tools, no auth). Every coding agent should probe it once at boot to confirm its own client speaks the era.

**Three rules for a stateless `2026-07-28` call — all three are required**:
- `MCP-Protocol-Version: 2026-07-28` as a **header** (NOT body `params.protocolVersion`)
- `Mcp-Method: <method>` header for routing
- `_meta.io.modelcontextprotocol/*` envelope keys (not `_meta.protocolVersion`)

**Conformance matrices** per layer (boot-contract, `structuredContent` vs `outputSchema`, error surface, auth matrix, host-surface gates) live in `references/absorbed-mcp-testing.md`. Read before claiming conformance.

**Era coverage matrix** (this is what `mcp-testing` v3.0.1 absorbed):

```
          legacy → stateless
initialize  M    M          (mandatory for 2025-11-25, disallowed for 2026-07-28)
MCP-Session-Id M required   (optional in legacy, ABSENT in stateless)
```

Deep dive: `references/absorbed-mcp-testing.md` (full conformance matrix + SEP-2567 stateless doctrine).

**Allowed Tools**: `npx @mcpjam/inspector@latest`; `firecrawl_firecrawl_scrape` for any URL probe; `docker`.

**Forbidden Actions**: reporting conformance from a CI log without an era-specific evidence row in the receipt.

## Stage 6 — EXTEND  (Apps, Auth-extensions, Tasks, Skills-over-MCP)

The four MCP extensions:

### 6a — MCP Apps (`extensions/apps/*`)

Interactive UI applications rendered inside MCP hosts (Claude Desktop, ChatGPT Apps, etc.). Recap in 4b. SEP-1865 — `tools/app = true`, three return channels, CSP via `_meta.ui.csp`, double-iframe sandbox.

**Landscape + portability (2026-09-22):** only MCP Apps/MCP-UI is the user-facing standard — Manager GUI and STMCP are operator dashboards the federation already covers (probe/registry/WELL/FRAME); both vendor claims UNVERIFIED (mcpmarket 403, stmcp 402). Host matrix: Claude/VS Code/Goose/LibreChat/Postman native MCP Apps; **ChatGPT = its own Apps SDK (partial UI actions)** — route via federation gateway. Renders in one host = *claimed*; renders across hosts = *proven* (self-probe → inspector → second host → regression row). Deep dive: `references/mcp-gui-landscape-2026-09-22.md`.

### 6b — Auth extensions (SEP-series)

- `extensions/auth/oauth-client-credentials.md` — M2M (already in Stage 4c).
- `extensions/auth/enterprise-managed-authorization.md` — IdP-gated (already in Stage 4b).
- SEP-1046 (client credentials), SEP-2207 (OIDC refresh), SEP-2468 (issuer claim), SEP-991 (URL-mode client registration).

### 6c — Tasks (`extensions/tasks/overview.md`, SEP-1686, SEP-2663)

Long-running async work. SEP-2322 multi-round-trip requests. Tasks appear as a SEP-2549-TTL'd list, store status via notifications, and 1:1 map to A-FORGE `forge_compose` lanes.

### 6d — Skills over MCP (`extensions/skills/overview.md`, SEP-2640)

Servers expose a `Skills` resource that lists agent-skill descriptors. The host enumerates them via `resources/read` (or `server/discover` in stateless era). Client-side: each `Skills` entry becomes a row in the runtime skill registry.

Deep dive: `references/absorbed-forge-mcp-a2a-agentic.md` (MCP + A2A composition); `references/absorbed-forge-mcp-gui.md` (Apps build recipes).

**Allowed Tools**: framework-specific (FastMCP `app=True`, etc.).

**Forbidden Actions**: declaring an extension conformance without the matching SEP evidence.

## Stage 7 — PUBLISH  (registry, versioning, automation)

### 7a — MCP Registry (official)

```bash
# 1. Prepare server config (server.json)
# 2. Authenticate per registry/authentication.md (GitHub OAuth, scoped to the publisher)
# 3. Publish per registry/quickstart.md
# 4. Verify GET returns 200 not 404

curl -sf https://registry.modelcontextprotocol.io/v0/servers/arifbfazil/your-server
```

Namespaces are globally unique (`arifbfazil/...` for our publisher). Versioning per `registry/versioning.md`. Moderation per `registry/moderation-policy.md` — read BEFORE publishing; some packages need source repo + license + tests.

### 7b — Aggregators (Smithery, Glama)

Each aggregator has its own publish flow, but they all pull **from** the MCP Registry. Aggregators add editorial verification layers (badge, install count, badges) — they're not the source of truth. Federate via a single canonical Registry record.

### 7c — Versioning

SemVer required. Each published version is immutable. New major version = rename or scope-bump (recommended), not breaking patches. SEP-2549 TTL on list results means version pinning on the host side.

### 7d — GitHub Actions automation

`registry/github-actions.md` provides the canonical CI/CD recipe. Federation repository at `/root/AAA` already wires this pattern for organ publishes.

### 7e — Authentication on publish

GitHub OAuth scoped to the publisher's namespace. **Never** use a personal token — use a federated bot identity (Arif's GitHub App under `arifbfazil`).

Deep dive: `references/absorbed-forge-mcp-registry-publish.md` (auth, scoped tokens, scoped-namespace errors, verification).

**Allowed Tools**: `curl` against `registry.modelcontextprotocol.io`; `gh` CLI for GitHub OAuth.

**Forbidden Actions**: publishing without a 100% green conformance suite. Publishing with secrets in the manifest.

## Stage 8 — GOVERN  (SEPs, working groups, retirement)

Three sub-areas: **process** (SEPs, working groups), **lifecycle** (deprecation, retirement), **policies** (design principles, contributor ladder, SDK tiers, security, antitrust).

### 8a — Specification Enhancement Proposals (SEPs)

`seps/` is the canonical change mechanism. Filenames are `SEP-NNNN-<slug>.md`. **Active SEPs that touch federation work**:

| SEP | Title | Why it matters |
|---|---|---|
| 985 | RFC 9728 PRM alignment | Stage 4 SECURE compliance |
| 990 | Enterprise IdP controls | Stage 4b EAP |
| 991 | URL-mode client registration | Stage 4a dynamic registration |
| 1024 | Client security for local install | Stage 3 BUILD hygiene |
| 1302 | Working Group governance | this section |
| 1303 | Validation errors as tool exec errors | Stage 3 input validation |
| 1613 / 2106 | JSON Schema 2020-12 default | Stage 3f output schemas |
| 1686 / 2663 | Tasks | Stage 6c |
| 1865 / 2133 | Extensions | Stage 6 |
| 2207 | OIDC refresh tokens | Stage 4d |
| 2243 | Streamable HTTP headers | Stage 2e transport |
| 2322 | Multi round-trip requests | Stage 6c Tasks |
| 2549 | TTL for List Results | Stage 4d / Stage 7c |
| 2567 / 2575 | Stateless MCP | Stage 2 / Stage 5 |
| 2577 | Deprecate Roots/Sampling/Logging | Stage 8c |
| 2640 | Skills extension | Stage 6d |

### 8b — Working Groups + Interest Groups

`community/working-groups/` lists 11 active WGs (Agents, File Uploads, Filesystems, Inspector V2, Interceptors, Registry, SDK, Server Card, Skills Over MCP, Transports, Triggers and Events). `community/interest-groups/` lists 7 IGs (Auth, Enterprise, Enterprise-Managed Auth, Financial Services, Primitive Grouping, Security, Tool Annotations). Federation SHOULD nominate representatives to WGs whose deliverables touch federation work.

### 8c — Feature lifecycle (`community/feature-lifecycle.md`)

Three states: **Active → Deprecated → Removed**. Each feature carries a timeline implementers can plan against. Deprecated features are grandfathered; new code in federation SHOULD NOT adopt deprecated APIs. The MCC Gateway/Inspector may already deprecate Roots/Sampling/Logging per SEP-2577.

### 8d — SDK tiers (`community/sdk-tiers.md`)

Tier 0 (canonical) → Tier 3 (experimental). Choose per Tier 1 minimum for any production federated server.

### 8e — Governance overlay for federation — the four mechanisms

Deep dive: `references/absorbed-forge-mcp-governance-wrapper.md`.

1. **Zero-LLM intent router** — no model-in-the-loop for governance decisions on common patterns.
2. **Per-agent role ACL** — capability ceiling per agent identity (333-AGI, 555-ASI, 888-APEX, A-AUDIT).
3. **Reversibility wrapper** — every mutating call declares its reversibility level.
4. **Dynamic policy layer** — runtime-loaded via `forge_policy`.

Three-tier runtime governance: solo fast-path → musyawarah (333+555) → gotong royong + F1 gate.

### 8f — Drift audit (the questions that actually find defects)

Run inspector, then distrust it:

- **Surface ≠ usage** — inventory which tools exist vs which are used, measured from the ledger.
- **Many tools failing at once** — dependency-pin drift, not per-organ breakage.
- **Surface ≠ surface** — one server can present several disagreeing views; a split tells you there is a conflict.
- **Probe an attestation function per question, never as a single boolean.**
- **Verify an external audit artifact** before acting on it.

### 8g — Lifeguard (recovery when authorised)

Alert conditions:
- HTTP 000/502/503 → restart container + log
- Response > 3s → WARN
- Provider 401/402 → disable from fallback chain
- Ollama cold-start > 15s → pre-warm via `/api/generate`

Rules: never restart `Vault999` (append-only, human ack); restart one MCP at a time; log to `~/.openclaw/workspace/logs/mcp-lifeguard.log`; disable dead models.

### 8h — RETIRE  (tombstone, freeze, never lose)

A retired name must still be findable. Its content must never be lost. The protocol:

1. **Freeze, do not delete.** Move `<skill-dir>` to `/root/AAA/skills/.frozen/<YYYY-MM-DD>-<reason>/` and rename `SKILL.md` → `SKILL.md.from.<tree>` (a literal `SKILL.md` inside `.frozen` inflates every census and can be re-loaded by a recursive scanner).
2. **Preserve the body where it stays discoverable** — `references/absorbed-<name>.md` inside the surviving owner, listed in `references/absorbed-INDEX.md`.
3. **Tombstone the name** — leave `<name>.DEPRECATED-<date>` resolving to the owner. Do not delete the old name; a name that stops resolving is indistinguishable from a name that was never there.
4. **Repoint inbound links** and re-run the census. **Check inbound dependents before moving or archiving anything** — a directory that looks empty may be the live body behind a symlink elsewhere, and removing it breaks every link silently.
5. **Re-measure.** A name is only retired when the census and the resolution gate both agree.

**Worked examples** (this skill absorbed 24+ names; full audit trail in `references/absorbed-INDEX.md`).

Deep dive: `references/absorbed-FORGE-mcp-lifeguard.md` (alert conditions), `references/absorbed-federation-mcp-drift-audit.md` (drift audit + `scripts/mcp_surface_usage_audit.py`).

**Allowed Tools**: `git` (PR opens for SEPs); `forge_policy` (runtime governance); `forge_scar` (seal failures as scars); `forge_vault` (audit trail).

**Forbidden Actions**: deleting a tombstone silently. Sealing a SEP outcome without a tri-witness.

## Allowed Tools (full list)

| Tool / Capability | Purpose |
|---|---|
| `fastmcp` CLI | Scaffold, inspect, list, call, run FastMCP servers (Stage 3) |
| `mcporter` CLI | Discover and call servers; daemon, auth, config, codegen (Stage 1/3/4) |
| `npx @mcpjam/inspector` | Conformance probe, doctor, OAuth check, era matrix (Stage 5) |
| `curl` / `python3 -m json.tool` | Health probes, raw JSON-RPC checks (Stage 2, all probes) |
| `uv` / `pip` | Install FastMCP in repo or system context (Stage 3) |
| `gh` CLI | GitHub OAuth scoped to federation namespace (Stage 7) |
| `/root/scripts/hermes_mcp_wire.py` | Governed client-config wiring (Stage 3) |
| `/root/scripts/hermes_mcp_compress.py` | Governed schema-compression wrap (Stage 3) |
| `docker run` (loopback bind) | MCPJam Inspector air-gap mode (Stage 5) |
| `firecrawl_*` | Discovery when MCP Registry unreachable (Stage 1 fallback) |
| `forge_evaluate` | Tool registration governance (Stage 8) |
| `forge_witness` | Tri-witness consensus for OAuth flows (Stage 4) |
| `forge_policy` | Runtime governance layer (Stage 8) |
| `docker restart` | Lifeguard auto-restart, authorised only (Stage 8g) |

## Forbidden Actions

- **NEVER** expose a FastMCP server on `0.0.0.0` in production; bind `127.0.0.1` and let Caddy terminate TLS.
- **NEVER** hardcode credentials; environment variables or SOPS only.
- **NEVER** call a mutating tool on a live federation organ without arifOS judgment.
- **NEVER** skip `fastmcp inspect` before wiring a new server into a client.
- **NEVER** report "fixed" from a diff alone — say "fixed on disk, not live" until a fresh process proves it.
- **NEVER** report an organ broken from a single un-handshaked probe.
- **NEVER** treat a successful health check as authorization to act beyond observer class.
- **NEVER** restart `Vault999` — append-only ledger, human ack required.
- **NEVER** publish to MCP Registry without a 100% green conformance suite.
- **NEVER** store bearer tokens in `SKILL.md` or any wire config.
- **NEVER** bypass `MCP-Protocol-Version` and `_meta.io.modelcontextprotocol/*` envelope keys when speaking `2026-07-28`.
- **NEVER** delete a tombstone silently. Always re-measure the census after retirement.
- Escalate to **arifOS 888_JUDGE** for deletion, deployment, secrets, SEP author intent, or constitutional files.

## Escalation Path

| Condition | Escalate To | Method |
|---|---|---|
| Mutating action on live organ | `arifOS 888_JUDGE` | `a2a` / `mcp verdict_request` |
| Secret exposure in config or code | security agent + `arifOS 888_JUDGE` | `a2a` message |
| Federation organ degraded/down | A-FORGE + health triage | health probe + incident channel |
| Production deployment needed | `arifOS 888_JUDGE` + human (F13) | `888 HOLD` |
| Tool call returns unexpected authority/scope | `arifOS 888_JUDGE` | hold with evidence |
| SEP authorship or co-sponsorship | `arifOS` for filing then `community@modelcontextprotocol.io` | SEP PR |
| OAuth conformance ambiguity | `arifOS 888_JUDGE` | verdict + evidence row |

## Sibling skills (kept separate, deliberately)

| Skill | Why it is not merged here |
|---|---|
| `wealth-mcp-ops` | WEALTH-organ MCP tools (capital primitive surface); organ-bounded, own repo layout. |
| `runpod-mcp` | Platform lane: Runpod pods/endpoints/jobs. Distinct triggers and setup. |
| `touchdesigner-mcp` | Platform lane: twozero MCP for TouchDesigner. Distinct triggers and tool surface. |
| `runtime-probe` | Focused instrument: one-shot MCP health + schema + transport classification. Stage 2c-in-a-tool. |
| `agent-tool-verification` | General claim discipline for any tool, not only MCP. |
| `qwen-harness-tools` | Model-side built-in harness tools; not MCP at all. |

## When NOT to Use

- **Do not use for production deployment** without site-architecture skills and arifOS judgment.
- **Do not mutate live federation servers** (restart, config change, port binding) without `arifOS F1–F13` clearance.
- **Do not run untrusted MCP servers** outside the `arifos-untrusted-sandbox` skill.
- **Do not hardcode secrets** in server code or client configs; use env vars / SOPS.
- **Do not treat a successful health check as authority** to act beyond observer class.
- **Do not adopt a new MCP server without consulting** `references/absorbed-mcp-sota-shopping-list.md` (Stage 1 procurement).
- **Do not skip the era declaration** when reading or invoking MCP — `2025-11-25` and `2026-07-28` differ in handshake + envelope keys.

## References

| File | Stage(s) | Purpose |
|---|---|---|
| `references/absorbed-INDEX.md` | all | full name → phase → origin → preserved path map (22+ absorbed names) |
| `references/absorbed-llms-workflow-map.md` | all | canonical llms.txt section → mcp-ops stage mapping + parity table |
| `references/absorbed-forge-fastmcp.md` | 4 | FastMCP scaffold/inspect/run/build recipes |
| `references/absorbed-forge-mcp-gui.md` | 4b, 7a | MCP Apps build recipes + annotation taxonomy |
| `references/absorbed-forge-mcp-a2a-agentic.md` | 4c, 7 | MCP + A2A composition + refusal surface |
| `references/absorbed-forge-mcp-governance-wrapper.md` | 9e | four governance mechanisms (router/ACL/reversibility/policy) |
| `references/absorbed-FORGE-mcp-lifeguard.md` | 9g | alert conditions, auto-restart loop, Ollama pre-warm |
| `references/absorbed-federation-mcp-drift-audit.md` | 9f | drift audit + runnable `scripts/mcp_surface_usage_audit.py` |
| `references/absorbed-mcp-organ-probe.md` (+ `layer-drop-diagnosis.md`) | 3 | deep probe law + misreadings |
| `references/absorbed-mcp-edit-activation.md` | 3d | PID-vs-mtime, two-loader doctrine |
| `references/absorbed-mcp-transport-fix.md` | 3e | SSE → Streamable HTTP migration |
| `references/absorbed-mcp-context-compression.md` | 4g | schema compression wrap (`medium`/`max`); measured −89.3% on aforge |
| `references/absorbed-mcp-ecosystem-indexing.md` | 2, 4d | discovery pipeline, beacon verification, pitfalls |
| `references/absorbed-forge-mcp-registry-publish.md` | 8 | auth, scoped tokens, scoped-namespace errors, verification |
| `references/absorbed-forge-minimax-mcp-direct-invoke.md` | 4c | MiniMax media lane direct invocation (model IDs + quota codes) |
| `references/absorbed-telegram-mcp-product-line.md` | 4 | Telegram product lane on MCP backends |
| `references/absorbed-external-platform-mcp.md` (+ `references/*`) | 4 | Composio/social-mcp/xurl/Firecrawl wiring + 3-band APA governance |
| `references/absorbed-mcp-testing.md` | 6 | full conformance matrix + SEP-2567 stateless doctrine |
| `references/absorbed-mcp-sota-shopping-list.md` | 2 (procurement) | MCP context tax + 2026-09 per-category shortlist |
| `references/pre-merge-mcp-ops-v3.1.0.md` | history | this skill's own pre-merge body (the llms.txt-alignment consolidation) |

## Historical changelog

* v1.0.0 — initial consolidation (FORGE-mcp-ops, FORGE-mcp-federation-ops, FORGE-mcp-lifeguard).
* v2.0.0 — absorbed 7 more MCP-named skills.
* v2.1.0 — pre-merge snapshot (preserved in `references/pre-merge-mcp-ops-v2.1.0.md`).
* v3.0.0 (2026-09-20) — 19 names absorbed, structured under 6 stages (DISCOVER → PROBE → INTEGRATE → TEST → GOVERN → RETIRE), 32 reference docs.
* v3.0.1 (2026-09-20, second pass) — trigger list completed to full declared union of 14 assigned MCP members (36 triggers added), `mcp-sota-shopping-list` folded in as Stage 1b, all 14 member names archived to `.archive/merge-20260920/mcp/` and left resolving as tombstones.
* **v3.1.0 (2026-09-21)** — llms.txt alignment: 9-stage workflow (LEARN → PROBE → BUILD → SECURE → TEST → EXTEND → PUBLISH → GOVERN-RETIRE), 4 new stage references (Learn, Secure, Extend, Publish), canonical body absorbs `mcp-testing` content (Stage 5), `mcp-testing` directory now resolved via symlink to mcp-ops. Frozen v3.0.0/v3.0.1 in `.frozen/2026-09-21-llms-alignment/SKILL.md.from.mcp-ops-v3.0.1`.

* **v3.1.1 (2026-09-21)** — 0-index renumber (per Arif SEAL): all stages N → N−1 (LEARN=0, DISCOVER=1, PROBE=2, BUILD=3, SECURE=4, TEST=5, EXTEND=6, PUBLISH=7, GOVERN=8; RETIRE = 8h sub-section inside GOVERN). Procurement sub-stage correctly re-parented from LEARN to DISCOVER (latent anomaly fix). Body length and supersedes list unchanged. v3.1.0 frozen body now preserved at `.frozen/2026-09-21-llms-alignment/SKILL.md.from.mcp-ops-v3.1.0`.

*AAA Skill Library — DITEMPA BUKAN DIBERI ⚒️*
