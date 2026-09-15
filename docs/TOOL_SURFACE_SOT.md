# TOOL SURFACE — Single Source of Truth (MCP + organs)

> **Verified live 2026-09-15 15:16 UTC (23:16 MYT) from KVM8 forge.**
> This is a MEASUREMENT RECORD, not doctrine. Re-probe before acting — these numbers age.
> Companion to `/root/AAA/docs/MACHINE_MAP.md` (machines) — this file covers **tool surfaces**, which MACHINE_MAP does not.
> Every row was produced by a probe whose command is given. If a number here disagrees with a doc, a dashboard, or an LLM's summary, **this file wins until re-probed.**

## 0. How to re-verify (copy-paste)

```bash
# HTTP organs: initialize -> notifications/initialized -> tools/list
for p in 8088 7074 8081 18082 18083; do echo "=== :$p ==="; \
  printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
    '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
    '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | python3 -c 'import sys,json,urllib.request; [print(json.dumps(json.loads(l))) for l in sys.stdin]' ; done

# A-FORGE (stdio)
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"p","version":"1"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
| timeout 60 node /root/A-FORGE/dist/src/interfaces/mcp/cli.js serve --transport stdio

# Kernel registry semantics
curl -s http://127.0.0.1:8088/health | python3 -m json.tool   # see registry block
curl -s http://127.0.0.1:8088/tools   | python3 -m json.tool   # public wire
```

## 1. Live MCP tool surface (measured)

| Server | Transport | Tools on wire | Protocol (measured) |
|---|---|---|---|
| arifOS kernel | http `127.0.0.1:8088/mcp` | **8** | `2026-07-28` stateless **SUPPORTED** |
| FED router | http `127.0.0.1:7074/mcp` | **7** | `2026-07-28` stateless **SUPPORTED** |
| GEOX | http `127.0.0.1:8081/mcp` | **31** | `2025-11-25` legacy only |
| WEALTH | http `127.0.0.1:18082/mcp` | **11** | `2025-11-25` legacy only |
| WELL | http `127.0.0.1:18083/mcp` | **31** | `2025-11-25` legacy only |
| A-FORGE | stdio (also http `:7072`) | **126** | stdio handshake |
| **TOTAL** | | **214** | |

**Protocol-era probe** (stateless test) — POST with `MCP-Protocol-Version: 2026-07-28`, `Mcp-Method: server/discover`, and a `_meta.io.modelcontextprotocol/*` envelope. Result: arifOS + FED return a valid result; **GEOX, WEALTH, WELL return HTTP 400** (legacy-only).

## 2. Kernel registry — read the semantics before calling it a gap

`GET :8088/health` → registry block:

```json
{"status":"healthy","registry_size":62,"declared_tools":48,"exposed_tools":8,
 "note":"registry_size includes aliases; diagnostic_tools not on public wire"}
```

The kernel's own source (`/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py:2350-2382`) defines these fields:

```
tools_registry_size  = internal registry callables (canonical + aliases)
total_declared_tools = public wire + diagnostic declared surface
```

So the arithmetic is: `declared_tools(48) = exposed(8) + diagnostic(40)`, and `registry_size(62)` = those plus aliases.

**The 8 public tools ARE the complete constitutional operating chain** — nothing is missing from it:

| Tool | Kernel | Role |
|---|---|---|
| `arif_init` | 000 | Session ignition |
| `arif_observe` | 111 | Sense reality → evidence |
| `arif_think` | 333 | Structured reasoning |
| `arif_route` | 444 | Intent → organ router |
| `arif_memory` | 555 | Governed semantic recall |
| `arif_judge` | 666 | Binding verdict |
| `arif_forge` | 777 | Execution gate |
| `arif_seal` | 999 | VAULT999 append |

**This is a designed boundary, not an oversight.** The 40 diagnostic tools are labelled `diagnostic` *in the code*. Whether any of them *should* be promoted to the public wire is a legitimate F13 governance question — but it is a question, not a defect. Never report "8/62 = 13% exposure" as a failure without this context.

## 3. Usage truth (from `/root/.hermes/state.db`, all sessions)

Total tool calls ever: **23,536**. Calls routed via MCP: **475 (2.0%)**.

| MCP server | Calls |
|---|---|
| aforge | 182 |
| arifos | 144 |
| wealth | 45 |
| arifflow | 36 |
| geox | 31 |
| well | 15 |
| zai_vision | 10 |
| fed | 8 |
| zai_search | 3 |
| context7 | 1 |

Per-organ zero-call share: arifOS 1/8 · FED 3/7 · WEALTH 3/11 · GEOX 22/31 · WELL 25/31 · A-FORGE 80/126. **134 of 214 (62%) never invoked.** Report as a measurement; "unexercised", not "useless".

## 4. Second MCP layer — the 1mcp aggregator (easily missed)

A separate aggregator runs on `127.0.0.1:3050` (1mcp v0.34.0, 14 healthy of 14 reported), config `/root/.config/1mcp/mcp.json` — **23 servers defined**:

`aforge · arifflow · arifos · brave-search · chrome-devtools · cloudflare · context7 · docker · exa · geox · github · hermes · hostinger-vps · meyhem · minimax-code · minimax-media · perplexity · postgres · qdrant` (+4 more)

Servers that look "unwired" in Hermes `config.yaml` may already be reachable here. Check both layers before declaring anything a ghost.

## 5. Full port map (live)

| Port | Service | Notes |
|---|---|---|
| 8088 | arifOS kernel (judge) | THE federation kernel |
| 7071 | A-FORGE `sense` | 122 tools loaded |
| 7072 | A-FORGE MCP bridge | streamable-http |
| 7073 | arifFlow | metabolic ledger |
| 7074 | FED router | intent classification |
| 3050 | 1mcp aggregator | 23 servers defined |
| 3001 | AAA a2a-server | `node /root/AAA/a2a-server/server.js` |
| 8081 | GEOX | |
| 18082 | WEALTH | |
| 18083 | WELL | |
| 18084 | signal organ | uvicorn `signal_organ.main:app` |
| 18085 | FRAME | independent observer |
| 9900 | Hermes A2A listener | |
| 4000 | HAProxy (KVM8) | **not** WEALTH |
| 4012 | FED model gateway (HAProxy) | |
| 5001 | VAULT999 writer | |
| 18789 | OpenClaw edge (KVM4) | |

## 6. Known defects at time of measurement

1. **WELL freshness expired** — `state_age_hours: 269.5`; `freshness.status: "expired"`. Downstream cron reads stale human-substrate data.
2. **`/root/AAA/state/sys_health.json` stale since 2026-08-01** — `evening_digest.md` instructs agents to read it and "assume ALL_GREEN" if stale. Void-Guard violation.
3. **Dependency pin drift** — arifOS `requirements.txt` declares `mcp==2.0.0 fastmcp==4.0.3`; installed is `mcp=1.29.0 fastmcp=3.4.6`. WELL on `mcp=1.28.1`.
4. **KVM4 gateway down since 2026-09-12 17:03 UTC** (clean exit, no systemd unit) — 10 cron jobs were orphaned there.
5. **Concurrent writers on config.yaml** — multiple sessions edited it within 10 minutes on 2026-09-15 (23:06 and 23:11 backups). Use flock or serialize.

## 7. Rule

A health payload number is **channel output**, not a verdict. `exposed_tools: 8` is not a deficiency; `status: healthy` is not a claim of perfection. Read the code's own field definitions before interpreting a metric as a defect.
