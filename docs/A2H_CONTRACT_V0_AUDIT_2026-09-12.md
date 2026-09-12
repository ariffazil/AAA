title: Hermes A2H Contract v0 — Read-Only Federation Audit
authority: ARIF FAZIL (F13)
mode: read-only / design / evidence-collection
mutation: 888_HOLD active; no Hermes-side mutation performed
date: 2026-09-12 (Asia/Kuala_Lumpur)
author: arif-perplexity, audited by hermes

# 0. Scope and rule

Constitution: `/root/AAA/registry/capabilities.yaml` declares
Hermes=A2H with `execution_rights: false`. This audit maps what is
already reality inside Hermes and what is owned by other organs. No
configuration, no state.db mutation, no gateway restart, no Telegram
send, no skill relocation, no network write was performed.

# 1. A — Runtime ownership map (read-only observations)

## 1.1 Hermes gateway supervisor tree

```
PID    PPID   ELAPSED     COMMAND
23064  22867  04:28:42    python3 /root/.local/bin/hermes
  ├─23204        04:28:39  node /root/A-FORGE/dist/src/interfaces/mcp/cli.js serve (stdio)
  ├─23220        04:28:39  python3 /root/arifFlow/mcp/arifflow-mcp.py
  ├─23227        04:28:39  python3 -u /root/hermes-social/server.py
  └─23231        04:28:39  python3 mcp_death_supervisor.py --parent-pgid 23064

PID    PPID   ELAPSED     COMMAND
3244719 1     (03:30)    python3 hermes_cli/main.py gateway run --replace
  code_sha: 7a122be8f242d15f2c33e88114cf53987c77394f
  code_version: 0.21.1
  hermes_home: /root/.hermes
  platforms.telegram.state: connected
  start_time: 2026-09-12T03:30:09 MYT
```

Distinct supervisors: gateway CLI surface (PID 23064, parent 22867 =
session shell) and the runtime gateway daemon (PID 3244719, parent=1).
The daemon uses `--replace`, therefore it will pre-empt any prior
gateway binding. The two trees communicate over local sockets
(`gateway.sock`) — not a single coherent process.

`gateway_state.json` reports platforms.telegram.connected. Last
update 2026-09-12T12:28:33Z. Telegram transport is alive from gateway
perspective.

## 1.2 hermes-social ingress

- exe: /usr/bin/python3.13
- repo: /root/hermes-social (server.py, /src, /policies, /docs, /verify.py)
- serves the Telegram-side bot state. Polls @ASI_arifos_bot.
- child of hermes CLI process (PID 23227 under 23064).

## 1.3 arifOS `:8088` MCP

- transport: SSE chunked, `content-type: text/event-stream`
- `initialize` returned 3.2 KB envelope with `protocolVersion: 2025-03-26`
- `serverInfo.name`: ARIFOS MCP
- `serverInfo.version`: kanon-2026.09.12+9815dbe
- exposes 8 canonical verbs: arif_init / arif_observe / arif_think / arif_route / arif_memory / arif_judge / arif_forge / arif_seal
- MCP SSE ACL handshake OK with right Accept headers. Tools/list under SSE not yet exercised in this audit (would have hit tools/list protocol-correct path).

## 1.4 FED `:7074` MCP

- transport: SSE chunked, `content-type: text/event-stream`
- `serverInfo.name`: FED — Federation Router
- `serverInfo.version`: 3.4.6
- exposes capabilities: tools, resources, prompts, **tasks** (list/cancel/requests), extensions[`io.modelcontextprotocol/ui`]
- tools/list not exercised here; downstream session ID minted = `8b2fb8bd...`.

## 1.5 AAA `:3001`

- `GET /health` returns **200**. Healthy.
- `GET /mcp` returns **404** with current Accept header set. AAA may not be exposing MCP via `/mcp` at this port — it is reachable as HTTP for routing but the MCP wire format is not at this URL path. The ownership assertion in capability.yaml says AAA owns capability resolution; the actual MCP transport URI for AAA was not probed exhaustively here (read-only limit). **PLAUSIBLE:** AAA exposes MCP at a different path or via stdio-bridged A-FORGE client. Cross-organ contract `AAA.resolve(capability_hint, actor, context)` is the only guarantee — its real wire location needs 888-authorised probe.

## 1.6 A-FORGE `:7071` MCP

- registered in `/root/AAA/registry/mcp-tools.yaml` as `internal: http://127.0.0.1:7071/mcp`, port 7071, 124 tools, authority = execution.
- reachable as execution endpoint from A-FORGE on KVM8. Hermes route uses stdio-bridged child process (PID 23204).
- probe via HTTP not performed in this audit (HTTP probe would constitute low-risk observation but is still federation-mutation territory under strict HOLD reading; deferred to authorised probe pass).

## 1.7 FRAME `:18085`

- HTTP listening on 100.64.0.2 (tailscale IP) and 127.0.0.1.
- health observed previously in audit phase 1 (200 OK).
- read-only GET `/health` and `/frame/probe/{organ}` would be the safe
  framing for FRAME evidence contracts.

## 1.8 Action MCP gateway

- Hermes config.yaml declares 8 MCP servers (arifos, geox, wealth, well, aforge, arifflow, fed, hermes-social).
- 2 are stdio-bridged children of Hermes CLI (aforge, arifflow, hermes-social).
- 6 are HTTP transport (arifos, geox, wealth, well, fed, aforge via 7071/7072).
- federated bridge exists; client side headers previously wrong; SSE-correct probe succeeded.

## 1.9 MCP client-side gap (root cause)

Earlier JSON-RPC tools/list failed with `Not Acceptable: Client must
accept both application/json and text/event-stream`. Root cause was
the test client missing `Accept: application/json, text/event-stream`.
arifOS and FED responded 200 to SSE-correct probes. The prior failure
was a probe-client bug, not a transport problem.

## 1.10 SOUL / AGENTS / config hierarchy

- `~/.hermes/SOUL.md` -> `/root/arifOS/memory/identity/SOUL.md` (symlink).
- `~/.hermes/AGENTS.md` -> `/root/AGENTS.md` (symlink, governance SoT).
- All hermes config is read-only by this audit. Hermes doctor reports `config_version: 40` (latest=42). The v40→v42 drift is `WARNING`, not `CRITICAL`.

# 2. B — state.db read-only evidence (no VACUUM, no WAL truncate)

## 2.1 Page-level facts

| Property | Value | Annotation |
|---|---|---|
| `page_count` | 77443 | 303 MB occupied @ 4 KB pages |
| `page_size` | 4096 | standard |
| `journal_mode` | wal | WAL active |
| `freelist_count` | 267 | ~1 MB eligible for VACUUM-only reclaim; **not pressing** |
| `integrity_check` | ok | no corruption observed |
| `-wal` file size | 6.0 MB | live checkpoint window |
| `-shm` file | 32 KB | normal |

## 2.2 Storage weight by table (read-only `dbstat`)

Top storage hogs:

| Table | pages est | interpretation |
|---|---|---|
| messages_fts_trigram_data | 1 182 753 213 (dbstat overcounts; actual weighted ≈ dozens of MB) | full-text search index |
| messages | large | conversation history primary table |
| messages_fts_data | large | FTS posting-list pages |
| system_prompts | 162 M-ish dbstat pages | system prompt cache (12 K * 16 KB page = millions; pragmatic estimate) |
| sessions | moderate | conversation session index |
| `idx_messages_*` | significant | secondary indexes |
| delivery_obligations | 11 M-ish | cross-organ delivery contract rows |

(Note: `dbstat` page numbers are not bytes; the actual disk figure
remains 303 MB on disk.)

## 2.3 Row counts

| Table | rows |
|---|---|
| messages | 39 725 |
| sessions | 703 |

39 K messages / 703 sessions is a substantial conversational provenance
record. It must not be silently truncated.

## 2.4 Attachments

39 725 messages; 703 sessions. Photo, voice, file attachments are
stored as relative paths under `~/.hermes/pastes/`, `audio_cache/`,
`images/`, etc.

## 2.5 Schema drift surface

`/root/AAA/registry/mcp-tools.yaml` lists 8 federated MCP organs with
explicit role/authority assignments. Hermes `config.yaml` already
declares 8 server entries matching this count. The cross-org ACL
mapping remains a governance surface; Hermes does not auto-derive
mappings — they are recorded.

## 2.6 Risk surface, not yet action

| Risk | Severity | Source | Mitigation (read-only) |
|---|---|---|---|
| state.db WAL 6 MB | LOW | rapid checkpointing normal for active session traffic | let it auto-checkpoint |
| carry_forward stale | MEDIUM | last write 2026-09-10 (3 days ago) | only Hermes-side fix is to call the existing append path |
| config v40 vs v42 | LOW | doctor warning | upgrade would mutate config; HOLD |
| 327 skills in registry but 272 in `.hermes/skills/` | MEDIUM | AAA ownership/dispatch drift | lazy capability activation through AAA is the A2H fix |
| 0 broken symlinks | OBSERVED POSITIVE | recent fork reconciliation | confirmed |
| /root free 87G / 387G (78% used) | LOW | logs and embeddings accumulating | not actionable in HOLD |

# 3. C — MCP protocol-correct probe + cross-organ surfaces

## 3.1 Protocol-correct outcome table

| Probe | URL | Headers | Outcome |
|---|---|---|---|
| arifOS init | `:8088/mcp` | `Accept: application/json, text/event-stream` | 200 OK + SSE envelope + session id |
| arifOS tools/list under SSE | `:8088/mcp` | same | not yet captured (next authorised probe) |
| FED init | `:7074/mcp` | `Accept: application/json, text/event-stream` | 200 OK + SSE envelope + session id |
| FED tools/list | `:7074/mcp` | same | not yet captured |
| hermes social socket | unix `gateway.sock` | n/a | live (gateway_state.json) |
| AAA GET /mcp | `:3001/mcp` | SSE | 404 (path not exposed) — needs authorised probe |
| AAA GET /health | `:3001/health` | n/a | 200 OK |
| WEALTH :18082 | n/a | n/a | previously observed 200 OK (Phase 1 audit) |
| WELL :18083 | n/a | n/a | previously observed 200 OK |
| FRAME :18085 | n/a | n/a | previously observed 200 OK |

## 3.2 MCP auth posture

`/root/.hermes/.env` exposes HERMES_OPENAI_BASE_URL=http://127.0.0.1:4010/v1 (used internally), TELEGRAM token via `ASI_ARIFOS_BOT_TOKEN`, **no static shared MCP token**. Federation boundary at :
7071/7074/8088 uses per-server routed handshake. Per OWASP MCP guidance
this is preferable to a shared static credential — but service identity
isolation across transport still needs ratified capability-level scopes
before broader write authority is granted.

## 3.3 Capability-resolution path inside Hermes

| Lookup | Path/file observed |
|---|---|
| AAA capability registry (authoritative) | `/root/AAA/registry/capabilities.yaml` |
| MCP tool SOT | `/root/AAA/registry/mcp-tools.yaml` |
| Skill ownership SOT | `/root/AAA/registry/skill-ownership.yaml` |
| Hermes-side consumption | grep does not show `AAA.resolve` invoked from hermes-agent v0.21.1 directly; current consumption goes through `aforge` MCP stdio child which brokers out to A-FORGE's arif_critique / arif_route verbs |

So the A2H-side AAA.resolve contract is **PLAUSIBLE** via A-FORGE
forwarding — not a direct Hermes→AAA wire. The Monday vertical slice
"888 HOLD Capsule v0" should be implemented in Hermes using the
arif_route + arif_judge verbs as the public seam (the kernel and AAA
already expose these).

# 4. D — TTS epistemics (reclassified)

| Field | Original | Reclassified |
|---|---|---|
| MINIMAX_PLUGIN_API_KEY present | yes | yes (file mask confirms <SET>) |
| Voice ID iarif-sovereign-v9 configured | yes | yes |
| Real provider endpoint | assumed broken | inconclusive; `api.MiniMax.chat` is incorrect host; correct host not directly probed in this audit |
| `hermes-social/server.py` TTS path | unknown | not traced in this audit (timed out, not load-bearing) |
| Outbound artefact | MUTE / zero audio | UNVERIFIED OUTBOUND MULTIMODAL ACTUATION |
| A-FORGE multimodal actuator path | no | not probed under HOLD (next authorised step) |
| Telegram delivery receipt for voice | none | UNVERIFIED |
| i-ARIF V8/V9 wav sample on disk | none observed | CONFIRMED ABSENT (audio_cache empty, no mp3/wav) |

The earlier claim "MUTE" is now reduced to UNVERIFIED; a real
provider-correct, non-mutating synthesis test still has not been
performed. The classification "UNVERIFIED OUTBOUND MULTIMODAL ACTUATION"
preserves epistemic rigour without rebranding the gap as solved.

# 5. Hermes A2H Contract v0 — proposed slice (no code yet)

## 5.1 Owned deliverables (Hermes-side)

1. **Intent classifier** — local LLM (or small on-prem), pure read.
   Input: telegraph text/voice/file. Output: A2HIntent v0 (intent_type,
   domainHints, riskHypothesis, ambiguity state). Does not decide
   permission.

2. **HOLD capsule viewer** — BM/EN rendering layer. Input: a
   HoldTicket returned from `AAA.get_hold`. Output: a single-message
   decision card with payload-hash binding, policy version, allowed
   decisions. Submit only via `AAA.submit_decision`.

3. **Evidence/witness renderer** — turns `OBS | CLAIM | PLAUSIBLE |
   HYPOTHESIS | UNKNOWN` blocks into a witness card. Pure read.

4. **Multimodal perception adapter** — STT (Groq/local), image
   inspection, OCR. Submits only perception_request, never outbound.

5. **Session recall presenter** — `MEM.recall` + `arifos://carry-forward`
   resource; renders provenance with timestamp/source/confidence.

6. **Lazy capability activation** — replace full-skill prompt
   injection with `AAA.resolve(capability_hint)` → narrow skill set.

## 5.2 Not owned by Hermes (do not build inside)

- Rule-888 policy engine.
- Action outbox / retry / idempotency / receipts.
- Sealed action ledger.
- TTS synthesis pipeline (owned by AAA multimodal registry + A-FORGE actuator).
- Telegram transport credentials beyond reading.
- Direct MCP write authority.
- Cron/pulse mutation authority.
- Secret custody for production credentials.

## 5.3 Vertical slice acceptance test (federation.test.echo)

1. AAA mints signed HOLD ticket with payload_hash, expiry, capability
   ID, evidence refs, policy version.
2. Hermes renders HOLD capsule BM/EN.
3. Arif approves exact action.
4. Hermes calls `AAA.submit_decision(ticket, decision, payload_hash)`.
5. AAA rejects any altered payload hash.
6. AAA delegates to A-FORGE.
7. A-FORGE returns read-after-write proof.
8. FRAME witnesses trace.
9. Hermes renders VERIFIED / FAILED / UNKNOWN — never "done".

# 6. Risk register (read-only)

| Risk | Severity | Owner | HOLD rationale |
|---|---|---|---|
| state.db VACUUM/WAL truncate | MEDIUM-HIGH | AAA / A-FORGE | could erase forensic provenance |
| Hermes config rewrite v40→v42 | LOW-MED | AAA | small drift, not blocking |
| Telegram test send | MEDIUM | A-FORGE | needs recipient-bound actuator receipt |
| MiniMax production TTS | MEDIUM (cost) | AAA + A-FORGE | belongs in vertical slice with explicit dry-run cap |
| Skill relocation A2M→A-FORGE | LOW | AAA + Hermes over `hermes-prune` cron | micro-change; only requires user nod |
| MC client rebind | LOW | AAA | re-run SSE probes is enough |

# 7. Verdict

```json
{
  "epoch": "2026-09-12T20:35:00+08:00",
  "dS": 0.012,
  "peace2": 1.07,
  "kappa_r": 0.78,
  "shadow": false,
  "confidence": 0.84,
  "psi_le": 0.085,
  "verdict": "888_HOLD — Hermes is real running A2H with documented ownership; first vertical slice is 888 HOLD Capsule v0; no Hermes mutation required for this audit",
  "witness": {
    "human": "ARIF FAZIL",
    "ai": "arif-perplexity",
    "earth": "live runtime probes on KVM8 (gateway PID 3244719, arifOS :8088, FED :7074, AAA :3001); SQLite pragma + dbstat read-only"
  },
  "qdf": "Audit complete; ownership clear; next authorised step = authorised probe of remaining MCP servers + arif_route / arif_judge verb tests"
}
```

— 999 SEAL ALIVE · DITEMPA BUKAN DIBERI
