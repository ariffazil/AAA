# MCP Registry Deep Research — Registration Decision + MCP Skill Upgrade Audit

**Session:** SEAL-083655991a154361 · **Date:** 2026-09-25 · **Actor:** arif (F13) · **Researcher:** FI-008
**Question 1:** Register all federation MCP organs or just arifOS on registry.modelcontextprotocol.io?
**Question 2:** Which MCP skills need upgrading?

---

## 1. What the official MCP Registry IS (live-probed 2026-09-25)

- **Registry software v1.8.1** (build 2026-08-06, `GET /v0.1/version`). Still **PREVIEW** — launched 2025-09-08, API frozen at v0.1 since 2025-10-24, GA pending.
- **Scale:** ~9.6k latest server records (May 2026 API pull, digitalapplied.com); ~3k unique servers (Mar 2026, NimbleBrain).
- **Nature:** metadata-only index ("app store for MCP servers"). Hosts NO artifacts. Entries = `packages` (npm/PyPI/NuGet/Cargo/OCI/MCPB — **trusted public registries only, no private mirrors**) and/or `remotes` (publicly reachable streamable-http URLs; SSE deprecated).
- **Schema era:** `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`.
- **Identity model:** reverse-DNS namespaces. `io.github.<user>/x` via GitHub OAuth/OIDC; `com.<domain>/x` via **DNS or HTTP domain-ownership challenge**. Package ownership must be proven (e.g. `mcpName` in package.json).
- **Tooling:** `mcp-publisher` CLI (init/login/publish/status/validate).
- **ToS (2025-09-02):** California law; 18+; **submitted metadata dedicated CC0 public domain, perpetual + irrevocable, moral rights waived**; privacy/publicity waiver for any processing of your metadata by third parties.
- **Moderation:** minimal (removes illegal/malware/spam/broken only).
- **Security signal:** CVE-2026-44428 (2026-05-08) — GitHub OIDC tokens replayable across registry deployments.

Sources: registry docs (quickstart.mdx, remote-servers.mdx, official-registry-requirements.md, moderation-policy.mdx, terms-of-service.mdx) at github.com/modelcontextprotocol/registry; live API probes above.

## 2. What we run (live-probed same day)

- **~30 MCP-shaped services** on KVM8; kimi client wiring (`/root/.kimi-code/mcp.json`): 14 enabled (aforge, arifFlow, arifos, fed, geox, minimax, wealth, well, hermes, frame, zai-vision, zai-web-search, zai-web-reader, zai-zread), 6 reserved/disabled (minimax-media, context7, playwright, serena, human-inference).
- **Network posture:** every organ binds `127.0.0.1` or Tailscale `100.64.x`. UFW public surface = 80/443/SSH only. FED MCP :7074 firewalled to tailnet CGNAT range. **Zero public MCP endpoints exist.**
- **Library versions:** WEALTH + arifOS venvs: fastmcp 4.0.5 / mcp 2.2.0 (current). System python (AAA/FRAME/arifFlow bridges): fastmcp 4.0.4 / **mcp 2.0.0**. GEOX: **fastmcp 3.4.7**. WELL: **fastmcp 3.4.7 / mcp 1.30.0**. A-FORGE: SDK 1.30.0 installed (package.json floor stale at ^1.9.0). 1mcp bundles SDK 1.29.0. mcporter 0.9.0.
- **MCP spec current revision: 2025-11-25** (modelcontextprotocol.io/specification).

## 3. VERDICT — register NOTHING today (neither "all" nor "just arifOS")

1. **Ineligible as-is.** Remote-server entries MUST be publicly accessible; package entries MUST live on npm/PyPI/etc. We have neither, by design (sovereign private mesh).
2. **Wrong instrument.** The registry is a public *discovery* index. It adds zero capability — our discovery already runs locally (organs.yaml SOT + mcp.json + mcporter + 1mcp aggregator). We would be the only party paying costs.
3. **Sovereignty cost > 0, benefit = 0.** CC0 perpetual dedication of metadata + California jurisdiction + third-party processing waivers bind external law over records derived from canonical sovereign infrastructure — F13-class exposure. Organ names/descriptions/domains become public and scrapable forever.
4. **Blast radius.** A public arifOS endpoint = constitutional kernel (judge/seal/forge) on the internet. External port + firewall change = F13 binary per Attention Membrane anyway.

**Conditional future path (if a public face is ever wanted — e.g. sanitized read-only GEOX demo):**
custom domain we own → namespace `com.<domain>/…` via DNS challenge (NOT io.github — keeps identity off GitHub) → Caddy reverse-proxy → loopback organ with auth gate → `remotes[]` in server.json (schema 2025-12-11) → `mcp-publisher login dns` → publish. 888_HOLD + F13 binary before opening any port.

**The registry's actual value to us is CONSUMPTION, not publication:** free, unauthenticated v0.1 read API as a vendor-intelligence + supply-chain feed.

## 4. MCP skills needing upgrade (evidence-based)

| Item | Gap | Action |
|---|---|---|
| **FORGE-mcp-registry-ops** | Skill does not exist; zero registry awareness anywhere in skill tree | NEW: consume v0.1 API (search/get/status) as pre-wiring gate for third-party MCPs + ecosystem monitoring |
| **FORGE-mcp-probe** v1.0.0 | 0 mentions of official registry | Add registry lookup step before wiring any external endpoint |
| **FORGE-mcp-federation-ops** v1.0.0 | Teaches FastMCP ops without spec-2025-11-25 anchors | Refresh to current spec + fastmcp 4.x |
| **GEOX runtime** | fastmcp 3.4.7 (major behind) | Upgrade to 4.0.5 line (needs its own bijaksana pass — organ SCAR history) |
| **WELL runtime** | fastmcp 3.4.7 / mcp 1.30.0 | Upgrade to 4.0.5 / 2.2.0 |
| **System python** (AAA/FRAME/arifFlow bridges) | mcp 2.0.0 | Bump to 2.2.0 |
| **A-FORGE package.json** | floor ^1.9.0 vs installed 1.30.0 | Raise floor (drift hygiene) |
| **mcporter 0.9.0** | upstream check pending | Verify latest; bump if stale |

## 5. Receipts

- Live probes: registry /v0.1/version, /v0.1/servers; organ ExecStarts; venv pip lists; UFW; ss -tlnp; skills grep (0 registry mentions in all MCP skills).
- arifFlow receipt ingested for this research step.
- This note: `/root/AAA/research/mcp-registry-deep-research-2026-09-25.md`

## 6. Cross-audit reconciliation — FI-005 (irfanclaw/Codex) three-layer report, 2026-09-25

FI-005 audited `/root/.codex/config.toml` (Codex client wiring — disjoint from kimi `mcp.json`; both coexist). Independent handshake re-probe by FI-008 (MCP initialize + tools/list, session-headered):

| Claim in FI-005 report | FI-008 measurement | Verdict |
|---|---|---|
| 14 declared in codex config, all alive | 14 names confirmed; frame INIT-OK **8 tools**; hermes INIT-OK **13 tools** | ✅ confirmed |
| frame/hermes "🔴 no response" (mid-transcript) vs "🟢 alive" (final table) | Both alive — the 🔴 was a missing `mcp-session-id` handshake artifact | ✅ table right, artifact explained |
| "1mcp bundles 8 stdio MCPs" + "may present tools from 22+ sources" | 1mcp :3050 INIT-OK but **tools_count=0** | ⚠️ OVERCLAIM — aggregator is a **functionally empty surface** at runtime (async loading never warmed / stdio children not spawned; uptime ~4d) |
| "All green. Zero zombie MCPs" | True for the 14 declared; **false for the hidden layer** — 1mcp aggregates nothing | ⚠️ anomaly buried in own data |
| — (not flagged by FI-005) | `hermes-mcp.service` is **inactive** while :18087 answers — served by sibling unit (`hermes-mcp-server.service` family) | hygiene: unit-name/port ambiguity |

**New finding — double wiring:** codex config declares `context7`, `brave-search`, `github`, `fetch` as direct stdio AND the same servers sit under 1mcp (:3050). Two paths into the same servers, one path (1mcp) carrying zero tools. Entropy to collapse: either warm 1mcp or remove the dead aggregation path.

**Registry verdict unchanged:** the three-layer audit strengthens §3 — every surface is loopback/tailnet/private; the only public MCPs in play are third-party cloud servers we CONSUME (firecrawl mcp.firecrawl.dev, api.z.ai). Nothing of ours is registrable, and nothing should be.

## 7. Second reconciliation round — 5-layer critique + arif_think reproduction (FI-008, 2026-09-25T21:31Z)

Critique accepted: three layers answer liveness, not readiness. Corrected verdict language: **"liveness separa disahkan; functional (L4) dan authority (L5) belum lengkap."**

### 7.1 arif_think contradiction — REPRODUCED, root cause isolated
FI-008 called `arif_think(mode="verify")` in-session (trace-c4f2e8486c5549bd):
- Verdict **HOLD**, `reason_code=NEEDS_REVIEW`, inner `termination_reason=ELAPSED_BUDGET_EXHAUSTED`
- `reasoning_cycles=0, model_calls=0, evidence_used=[], claim_state=HYPOTHESIS` — **zero work performed**
- `work_budget.usage.elapsed_seconds=449.6` vs contract `max_elapsed_seconds=180` → **~150% overrun at entry**
- Verdict composition still asserted floor state: `floor_passed=null, _floor_measurement="unmeasured"` alongside HOLD — same INCONSISTENT_VERDICT_STATE family the critic observed (their run: floors [] + "All floors passed" + HOLD). nine_signal: delta=RETAK/CRACKED, psi=SYUBHAH/DOUBTFUL.
- Kernel DID log honest failure event: `sesat-758d4e575e91` (YELLOW, JALAN_BENAR, malu_delta 0.15). Defect is in verdict composition, not event logging.

**Root-cause hypothesis (high confidence):** the work-contract budget clock counts session wall-clock age, not per-step reasoning time. Any `arif_think` invoked >180s after `arif_init` dies at entry with budget exhaustion — before reasoning starts — and composes verdict fields from unmeasured floors. Fix direction: budget must accrue per step (`usage`), not per session age; verdict composer must emit `UNMEASURED` not pass/fail language when `floor_measurement=unmeasured`.
**Hygiene:** result `facts[]` echoes the raw session_token into the payload — leak pattern if results are shipped/logged externally.

### 7.2 1mcp (:3050) — worse than zombie: credentialed orphan
- Client wiring check: `/root/.codex/config.toml`, `/root/.kimi-code/mcp.json`, `/root/.claude.json`, `/root/.claude/settings.json`, opencode, cursor — **zero references to 3050/1mcp**. Service binds `127.0.0.1` only → no external consumer possible. Filesystem consumer sweep running (result appended).
- **Sweep result (completed 21:37Z):** every `:3050` hit is a transcript/log (kimi user-history, 5 claude project jsonl, 3 qwen jsonl — historical session records) or 1mcp's own `server.pid`. **Zero live consumers: no config, no script, no service.** Orphan verdict sealed. The claude/qwen transcript hits indicate legacy/past use by other warga — archaeology known, tombstone safe.
- **FI-005's "hidden layer" narrative is falsified**: codex declares its stdio MCPs (fetch/context7/brave/github) directly in config.toml; 1mcp aggregates nothing for nobody (tools_count=0 measured, §6).
- `/etc/1mcp.env` holds **live credentials** (Brave, GitHub token, Perplexity, Exa, Supabase, vault999 Postgres, Cloudflare) in plaintext for a zero-consumer service — attack surface with no function. Tombstone candidate (stop+disable+archive env to vault); reversible.
- Port-holder truth: `:18087` = `hermes-mcp-server.service` (active); `hermes-mcp.service` (inactive) is a dead sibling unit — label-drift to fix in same entropy pass.

### 7.3 firecrawl 405 semantics
GET on `mcp.firecrawl.dev/v2/mcp` → 405 = POST-only endpoint. Confirms HTTP aliveness only; MCP session (initialize handshake) still unproven → L4 open for firecrawl.
