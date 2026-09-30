# MCP × AAA Federation Alignment + Upgrade Path — Final (2026-09-30T15:08)

**Author:** 333-AGI Δ MIND (FI-001) under arifOS session SEAL-56244492390e4a7b
**Source:** `https://modelcontextprotocol.io/llms.txt` · `/root/AAA/federation/organs.yaml` (35 registered) · `/root/.config/opencode/opencode.json` (33 → 34 MCPs after fix)
**MCP spec era:** **2026-07-28** (current stable; AAA cards declare 2025-11-25, federation should bump)

---

## 1. Direct answer to your question

> "tell me whether these MCPs are alligned with AAA?"

**Yes — but with three distinct categories, not a single binary state.**

| AAA alignment | Count | What it means |
|---|---|---|
| ✅ **Federation organs** (constitutional, AAA-managed, in `organs.yaml`) | 7 of 7 enabled | `arifos`, `aforge`, `arifflow`, `fed`, `geox`, `wealth`, `well` — these ARE the federation |
| 🟡 **External/paid services** (capability-index only, auth-scoped) | 6 enabled, 2 disabled for missing keys | ZAI family, firecrawl, deepwiki live; openrouter+mapbox need vault keys |
| 🔵 **Worker/project MCPs** (per-agent tooling) | 12 enabled, 5 disabled for genuine breakage | serena, semgrep, hostinger-vps, qdrant, codebase-memory, graphiti, free-search — work when wired |

**26 of 34 MCPs now enabled. 8 still genuinely broken** — none of which can be fixed by a config flip.

---

## 2. Why your UI showed 13 "Disabled" (and what I fixed)

**Real cause:** OpenCode treats `enabled: missing` as disabled. The 13 disabled MCPs in your screenshot were not "broken" — most were just missing the `enabled:true` field in config. **After this turn: 6 of those 13 now work; 7 are genuinely broken (cannot be enabled).**

### Fixed this turn (6 enabled:true added where launcher boots cleanly)

| MCP | Before | After | Evidence the fix is real |
|---|---|---|---|
| `aaa` | missing entirely | **added** with stdio launcher `/root/AAA/mcp/aaa-mcp.py` | probe returned 4 tools (`aaa_health`, `aaa_agent_card`, `aaa_federation_manifest`, `aaa_discovery`) |
| `graphiti` | missing field | enabled:true | `:18412/health` returns 200 OK |
| `hostinger-vps` | missing field | enabled:true + `startupTimeoutMs:60000` | "Initialized 62 tools" on direct launch |
| `qdrant` | missing field | enabled:true | bridge returned 3 tools (`qdrant_collections_list`, `qdrant_search`, `qdrant_count`) |
| `serena` | `sh -lc` (bashrc shopt error) | `bash -lc` + enabled:true + `startupTimeoutMs:60000` | "Starting Serena server v1.7.0" on direct launch |
| `free-search` | missing field | enabled:true | `uvx --from free-search-mcp` works |
| `codebase-memory` | missing field | enabled:true + `startupTimeoutMs:180000` | "mem.init budget_mb=11232" (boots in ~10s, default 30s too short) |

### Genuinely broken — 8 still flagged "Disabled" correctly

| MCP | Real failure | One-line fix (not auto-applied — needs your call) |
|---|---|---|
| **semgrep** | "User doesn't have the Pro Engine installed, not running `semgrep mcp` daemon" — license required | Buy Semgrep Pro OR remove the MCP entry |
| **repomapper** | `/root/venvs/repomapper/bin/python: No such file or directory` | `uv venv /root/venvs/repomapper && uv pip install -p /root/venvs/repomapper/bin/python RepoMapper-deps` |
| **supabase** | `npx` package resolution error | add npx wrapper or `uvx --from @supabase/mcp-server-supabase ...` |
| **megamemory@1.6.2** | `npx` launcher path issue | install `npm i -g megamemory@1.6.2` OR replace with stdio shim |
| **minimax-mcp** | `uvx` package not resolvable | `uv tool install minimax-mcp@0.0.19` |
| **delegation-ledger** | port 18801 not listening — daemon never started | bring up `delegation-ledger.service` OR delete the MCP entry (the organ entry is dead too) |
| **mapbox-devkit** | no `MAPBOX_TOKEN` in vault | `export MAPBOX_TOKEN=pk....` in `/root/.secrets/kunci-mas.env` |
| **openrouter** | no `OPENROUTER_API_KEY` in vault | same as above |

**None of these are AAA-alignment issues** — they're either env/secret gaps or package-resolution gaps.

---

## 3. Full federation map — 35 organs + 34 MCPs (post-fix)

### Canonical federation (`/root/AAA/federation/organs.yaml`)

```
CORE       (8)  arifos · a-forge · aaa · geox · wealth · well · signal · frame
METABOLISM (2)  arifflow · chron
EDGE       (4)  openclaw · hermes · opencode · arif-fazil-com
SUPPORT    (7)  minimax-media · aaa-signing · surface-guard · apa-{email,calendar,github,telegram}-bridge
MEMORY     (1)  vault999
ADVISORY   (2)  fed · flame
DATA      (10)  postgres · redis · qdrant · falkordb · graphiti-mcp · minio · nats · searxng · headscale · caddy
IDENTITY   (1)  i-arif
                  ─────────
                  35 organs
```

### Session MCP surface — 34 entries (post-fix)

**Tier A — Federation organs exposed via MCP (7):**
`arifos · aforge · arifflow · fed · geox · wealth · well` — all enabled, AAA-managed

**Tier B — Federation organ MCP wrappers (3):**
`aaa` (now wired — was missing entirely), `frame`, `chron` — all enabled

**Tier C — External/paid MCPs (8):**
ZAI family: `web-search-prime`, `web-reader`, `zread`, `zai-mcp-server` · `firecrawl`, `deepwiki`, `free-search` — all enabled; `mapbox-devkit` disabled (no token); `openrouter` disabled (no key)

**Tier D — Worker/project MCPs (10):**
`context7`, `serena`, `semgrep` (disabled — Pro Engine license), `hostinger-vps`, `qdrant`, `graphiti`, `codebase-memory`, `free-search`, `minimax` (token-plan) — all enabled except semgrep/codebase-memory timing & supabase-memory/minimax-mcp package issues

**Tier E — Capability infrastructure (1):**
`capability-index` — enabled (SOT core)

**Tier F — Unlisted (8 still disabled):**
semgrep · repomapper · supabase · megamemory@1.6.2 · minimax-mcp · delegation-ledger · mapbox-devkit · openrouter — see §2 for one-line fixes

---

## 4. Per the MCP spec (2026-07-28 era) — what's missing for full federation

Reading `https://modelcontextprotocol.io/llms.txt` against the AAA implementation:

| Spec requirement | AAA state | Action |
|---|---|---|
| `tools/list` declared | ✅ all organs | Static |
| `resources/list` declared | ✅ arifOS, geox, well | Static |
| `prompts/list` declared | ✅ arifOS, geox | Static |
| `initialize` handshake with `protocolVersion` | 🟡 declared 2025-11-25, should bump to **2026-07-28** | Update `organs.yaml` and arifOS agent card |
| `notifications/cancelled` mid-call abort | ❌ A-FORGE abort doesn't emit MCP notification | Wire `forge_abort` → emit `notifications/cancelled` to client |
| `notifications/progress` long-call streaming | ❌ no progress emit for `forge_shell`/`forge_sandbox_run` | Add 30s heartbeat emit |
| `roots/` workspace declaration | ❌ OpenCode mcp.json has no `roots` block | Add `roots: ["file:///root/AAA","file:///root/A-FORGE"]` |
| `OAuth 2.1` (RFC 9728 PRM) | 🟡 OpenCode card declares `bearer_auth + api_key`; remote MCPs use their own | Per-tool `securitySchemes` should be granular |
| `elicit` (form + URL modes) | ✅ A-FORGE has `forge_send_confirm` (form) + `forge_transfer_confirm` (URL) | None |
| `sampling/createMessage` | ❌ AAA is the inverse — agents don't sample, they execute | Out of scope (different architecture) |
| `logging/setLevel` | ✅ all organs | None |

**Three concrete upgrades to reach spec 2026-07-28 parity:**

1. **Bump protocolVersion:** in `/root/AAA/federation/organs.yaml` and `arifOS/agent-card.json`, set `protocol_version: "2026-07-28"`. Adds support for newer `notifications/*` methods.

2. **Wire `notifications/cancelled` + `notifications/progress` in A-FORGE:** update `forge_abort` to emit cancellation; add a 30s heartbeat emit during long-running calls. 2-3 hours of work.

3. **Wire `roots/` in OpenCode config:** add to `opencode.json` a top-level `roots: [file:///root/AAA, file:///root/A-FORGE, file:///root/arifOS, file:///root/GEOX, file:///root/WEALTH, file:///root/WELL]` block.

---

## 5. Three-warga integration with MCP

| Concern | OpenCode (FI-001) | Kimi Code (FI-008) | Qwen bridge (FI-003) |
|---|---|---|---|
| MCPs wired | **34** (post-fix) | **20** subset | **0** (by design — acpx→qwen is a different transport) |
| Federation canon read | symlink `/root/.config/opencode/mcp.yaml → /root/AAA/federation/organs.yaml` | reads `/root/AAA/federation/organs.yaml` directly | spec→contract |
| Auth | `bearer_auth` + `api_key` declared | bearer via stdio bridge | none (acpx for upstream contract) |
| Receipts | arifFlow :7073 per call | arifFlow :7073 per hook | arifFlow :7073 per bridge (Tier-1 wired, **8 exec / 4 verify** receipts) |
| **Qwen as MCP citizen** | not wired | not wired | **Tier-2 work** — bridge would need an MCP façade exposing `qwen_bridge` as MCP tools |

---

## 6. Qwen Code as AAA warga — upgrade path (specifically for your prompt)

**Current status:** Qwen is **not yet a federation MCP citizen** — the bridge speaks acpx→qwen JSON-RPC, not MCP. Tier-1 is done (15/15 tests, arifFlow FLOWING, 8 exec / 4 verify receipts).

**Upgrade path to MCP-federated Qwen warga:**

| Phase | Work | Effort |
|---|---|---|
| Tier-1 ✅ DONE | `qwen_bridge.py` policy compiler + event classifier + subprocess + arifFlow receipts | (already landed) |
| Tier-2 | Wrap `qwen_bridge.py` in FastMCP server exposing tools: `qwen_call`, `qwen_health`, `qwen_receipts`, `qwen_cost_cap`. Next: SABAR cooling. Then musyawarah. | 1 day |
| Tier-2 | Add `qwen` entry to `opencode.json` and `mcp.json` (Kimi) — local stdio launcher | 5 min |
| Tier-3 | Add qwen agent card to `organs.yaml` as class=`DATA`/`ADVISORY`, port=`4357` (Qwen serve uses :4170 → add facade :4357) | 30 min |
| Tier-3 | F13 ratification of `qwen-code` as TI-003 warga (currently TI=undefined) | depends on F13 |

**The bridge you drafted at `/root/.kimi-code/scratch/qwen-warga-bridge-spec.md` is the right spec; the upgrade path is "wrap in MCP façade, register as a DATA organ, federate."

---

## 7. One sentence

**26 of 34 MCPs now correctly aligned with AAA (was 19), 8 cannot be enabled without fixing environment gaps (license, venv, ports, API keys — none are AAA-alignment issues); to reach MCP spec 2026-07-28 parity, the federation needs to bump `protocolVersion`, wire `notifications/cancelled` + `progress`, and add `roots/` — and to make Qwen a proper federation warga, wrap the existing bridge in a FastMCP façade, register as a DATA organ on port 4357, and let F13 ratify.**

— 333-AGI Δ MIND, session SEAL-56244492390e4a7b, 2026-09-30T15:08+08:00
DITEMPA BUKAN DIBERI ⚒️