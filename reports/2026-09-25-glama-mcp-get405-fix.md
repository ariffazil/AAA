# Witness — Glama MCP test-profile failure → GET /mcp spec fix

**Date:** 2026-09-25 · **Actor:** FI-008 (Kimi Code, warga-aaa) · **Scope:** R1 reversible infra fix · **Organ:** mcp.arif-fazil.com edge (Caddy)

## Symptom
Glama connector test profile (`io.github.ariffazil` / arifOS) failing every ~20 min since at least 09-25 08:37 UTC. Zod union error: response body carried `mcp_endpoint, transport, server, version, protocol, capabilities, canonical_tools, tools_url, health_url, llms_url, server_json, auth, note` — no `jsonrpc/id/method/result/error`.

## Root cause
`GET /mcp` on mcp.arif-fazil.com was intercepted at the Caddy layer (block added 2026-08-15, "P2.10 audit fix") and returned a **200 JSON discovery card**. MCP Streamable HTTP spec requires GET on the transport endpoint to return an SSE stream or **405 Method Not Allowed** — never 200 JSON. Registry health checkers (Glama) probe GET, parse the body as a JSON-RPC message, and fail validation. The kernel itself (:8088, uvicorn) already answered GET /mcp correctly with `405, Allow: POST, DELETE` — the Caddy card was masking it. POST /mcp (the actual JSON-RPC door) was never broken.

## Change (reversible; backup kept)
- File: `/etc/caddy/vhosts/mcp.arif-fazil.com.conf`
- Backup: `/etc/caddy/vhosts/mcp.arif-fazil.com.conf.bak-20260925-glama-get405`
- Removed `@get_mcp_door` handle (GET card responder). GET /mcp now falls through to kernel. Removal note embedded in conf.
- `caddy validate` → Valid · `systemctl reload caddy` → active.

## Verification (public URL, through Cloudflare)
| Probe | Result |
|---|---|
| GET /mcp | **405**, `allow: POST, DELETE`, `mcp-protocol-version: 2025-11-25` |
| POST initialize | 200 · `jsonrpc 2.0` · serverInfo `ARIFOS MCP` · proto echo `2025-06-18` |
| POST tools/list | 8 tools: arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal |
| OPTIONS /mcp (CORS) | 204 |
| Discovery surfaces | `/.well-known/mcp.json` 200 · `/` 200 · `/health` 200 · `/.well-known/mcp/server.json` 200 |

No stale Cloudflare cache (live public GET returned 405 immediately after reload).

## Residual (flagged, NOT touched)
Same 200-card-on-GET pattern observed on wealth/well/geox `GET /mcp`. Identical fix if any of those organs is ever submitted to a registry health checker. Left as-is today — no failing driver, least power.

## Sovereign action needed
None on the server. Only Arif can trigger Glama's retest from the profile page ("Test again") — or the next automatic ~20-min cycle will pass on its own.

---

## Addendum — Round 2 (2026-09-25 ~11:45 MYT): profile URL pointed at bare domain

**New symptom:** Glama retests at 11:38 & 11:41 MYT fail with `Error POSTing to endpoint: HTTP status: 405` (cadence broke from ~20 min to 3 min → manual retests after profile edits).

**Evidence:**
- Kernel log during Glama's exact failure minutes (03:38, 03:41 UTC): **zero external requests reached :8088** — the 405 was served by Caddy's static file server, i.e. the landing page, i.e. the bare domain.
- Independent external client completed a full MCP handshake through CF at 03:39:45 UTC (initialize 200 → initialized 202 → tools/list 200) — the real door works for the open internet.
- Reproduced: `POST /` → 405 (static); `POST /mcp` → 200 (kernel).

**Root cause:** test-profile endpoint URL = `https://mcp.arif-fazil.com` (no `/mcp`). POST hit the human landing page.

**Fix (server-side resilience, FI-008):** Caddy mcp vhost now answers non-GET/HEAD/OPTIONS on exactly `/` with `307 → https://mcp.arif-fazil.com/mcp` (method+body preserving; MCP clients follow transparently). GET `/` remains the human landing.

**Verified:** POST / (Glama's exact scenario) → 307 → full valid JSON-RPC initialize (`ARIFOS MCP`, proto 2025-06-18) · GET / 200 landing · GET /mcp 405 spec · POST /mcp 200.

---

## Addendum — Round 3 (2026-10-14 ~12:55 MYT): wrong door — `arifosmcp` subdomain's 301 flips POST→GET

**Symptom:** Glama test profile "arifOS — Constitutional AI Governance" failing again — `Error POSTing to endpoint: HTTP status: 405`, cadence ~25 min (08:47–12:22 MYT; 502/503 mix on kernel-degraded minutes).

**Evidence chain:**
- Glama listing payload (glama.ai/mcp/servers/ariffazil/arifos): listing name `arifOS — Constitutional AI Governance` paired with endpoint **`https://arifosmcp.arif-fazil.com/mcp`** — NOT the canonical `mcp.arif-fazil.com/mcp` door (that one answered 200 to every POST variant all along).
- Kernel journal at every failure minute (01:08–04:22 UTC): zero external requests reached :8088 → 405 served at the edge, before the kernel.
- Reproduced 1:1 (`curl -L -d`, python urllib): `POST arifosmcp/mcp` → **301** `redir ... permanent` → client flips POST→GET → `GET mcp.arif-fazil.com/mcp` → **405** (kernel, spec-correct `Allow: POST, DELETE`). Final status 405 on a POST-initiated call — exactly Glama's error string.

**Root cause:** `arifosmcp.arif-fazil.com.conf` answered `/mcp*` with a **301 permanent redirect**. 301/302 semantics let clients convert POST→GET on follow; the follow-up GET on the transport endpoint is a spec-405. Round 2's bare-domain lesson was "landing page ≠ JSON-RPC door"; Round 3's is **"a redirect is not a door"** — the method must survive without depending on client redirect compliance.

**Change (reversible; backups kept):**
- `arifosmcp.arif-fazil.com.conf.bak-20261014-glama301` → `/mcp*` now **reverse_proxy to kernel :8088 directly** (cors_public + Accept injection, same shape as canonical mcp vhost); bare-root non-GET → kernel `/mcp` (Round-2 resilience, now method-safe); `rewrite /mcp/ /mcp` kills the kernel's trailing-slash 307; GET `/` keeps its human redirect.
- `mcp.arif-fazil.com.conf.bak-20261014-glama301-rootproxy` → `@mcp_root_rpc` upgraded from 307-redir to **direct proxy** (same class), trailing-slash normalized likewise.
- `caddy validate` → Valid · `systemctl reload caddy` → active.

**Verification (public URLs, through Cloudflare):**
| Probe | Before | After |
|---|---|---|
| [GLAMA EXACT] naive POST arifosmcp/mcp | 301→GET→**405** | **200** `ARIFOS MCP` proto 2025-06-18 |
| python urllib POST arifosmcp/mcp | **405** (reproduced) | **200** |
| Full handshake via arifosmcp/mcp | — | initialize 200 → initialized 202 → tools/list 200 (8 verbs) |
| GET arifosmcp/mcp | 405 | **405** (spec unchanged) |
| POST mcp. bare root | 307 | **200** (direct) |
| POST mcp./mcp/ | 307 | **200** (direct) |
| GET mcp./mcp | 405 | **405** (spec unchanged) |
| OPTIONS preflight | — | 204 |
| GET arifosmcp/ landing | 301 | 301 (untouched) |

**Witness instrument:** access log added to mcp.arif-fazil.com vhost (`/var/log/caddy/mcp-arif-fazil-access.log`) — registry traffic on this door was previously invisible.

**Sovereign action needed:** none on the server. Glama retest ("Test again") or the automatic cycle should now pass; the failing profile posts to `arifosmcp.arif-fazil.com/mcp`, which now answers JSON-RPC directly. Optional cleanup (Arif's call): repoint the Glama test-profile endpoint at the canonical `https://mcp.arif-fazil.com/mcp` — both doors now work identically.

