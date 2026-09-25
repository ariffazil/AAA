# Deep Research — Federated Codex Plugins (thin-adapter architecture)

**Date:** 2026-09-25 · **Actor:** FI-008 (Kimi Code) · **Question (sovereign):** "can we make the plugins federated?" · **Companion:** Codex FI-005 session's 41 invariants (I-01..I-41) — this doc composes with, not replaces, that list.
**Status:** RESEARCH — no files created outside this doc; no plugin installed; no marketplace written.

## 0. Verdict

**Yes — three senses, all true at once:**

1. **Vertical federation** — the plugin's tool layer IS the federation: no local capability logic, only MCP HTTP doors to organs that already exist and are verified live.
2. **Horizontal federation** — one backend, many runtimes: the same URLs serve Codex plugins, Claude Code (`.mcp.json`), Kimi, and any MCP client. Capability survives runtime replacement (APEX-ZEN ruling).
3. **Lifecycle federation** — identity, receipts, and authority stay server-side (`arif_init` SCT, arifFlow FQ, `arif_judge`). The plugin is a rendering, never an authority (CAPABILITY ≠ AUTHORITY enforced by architecture).

## 1. Verified facts (probed today, primary sources)

| # | Fact | Evidence |
|---|---|---|
| F1 | Plugin `mcpServers` supports **inline remote HTTP servers**: `{"name": {"type": "http", "url": "https://…/mcp"}}` | openai/codex `plugin-json-spec.md` (read from main via zread, 2026-09-25) |
| F2 | Codex HTTP MCP transport fields: `url`, `bearer_token_env_var`, `http_headers`, `env_http_headers`; OAuth 2.0 + EMA flows exist in `rmcp-client` | openai/codex repo docs (MCP Tool Integration page) |
| F3 | Kernel door `https://mcp.arif-fazil.com/mcp`: stateless, healthy — initialize 200, tools/list 200 (8 canonical tools) | this morning's Glama fix verification |
| F4 | Federation door `https://mcp.arif-fazil.com/federation/mcp`: **stateful** (missing session → JSON-RPC -32600), full handshake verified: initialize → session-id → **tools/list = 225 tools** → DELETE 200 | probe 2026-09-25 ~12:0x MYT |
| F5 | Tool census by organ: forge 121 · well 40 · geox 31 · wealth 14 · chron 10 · kernel 8 · federation meta 1 | same probe (sensor, not quote) |
| F6 | Local Codex already federates 14 MCP servers; 5 canonical organs via localhost HTTP (`8088, 7072, 8081, 18082, 18083` + frame 18086 + hermes 18087) | `/root/.codex/config.toml` `[mcp_servers.*]` |
| F7 | Marketplace: personal `~/.agents/plugins/marketplace.json` (does not exist yet on this box); sources `local·url(git+sha)·git-subdir·npm`; policy block `installation`/`authentication` | plugin-json-spec.md |
| F8 | Hooks: 12 lifecycle events; command handlers with `timeout`, `statusMessage`, `additionalContextLimit` | protocol.rs + hooks tests (via Codex session + spec) |

**Implication of F1+F4:** no bridge process, no vendored proxy, no secrets in the archive. The plugin is a manifest + hooks + a handful of skills. Everything heavy stays home.

## 2. Architecture — the Thin Adapter (DITEMPA)

```
┌─ Codex runtime ──────────────────────────────┐
│ plugin.json   → mcpServers: HTTP doors       │  L1 CAPABILITY
│ hooks.json    → SessionStart/PostToolUse/Stop│  L0+L3 IDENTITY+WITNESS
│ skills/       → router + init + seal ONLY    │  L2 DOCTRINE (pointer, not fork)
└──────────────┬───────────────────────────────┘
               │ MCP streamable HTTP (no auth at transport)
┌──────────────▼───────────────────────────────┐
│ mcp.arif-fazil.com/mcp          (kernel 8)   │
│ mcp.arif-fazil.com/federation/mcp (225)      │  federation = the real capability+authority
│ mcp.arif-fazil.com/hermes/mcp   (meaning)    │
└──────────────────────────────────────────────┘
```

**Dual profile** (choose per install):
- **LOCAL** (this VPS): localhost doors — mirrors today's `config.toml` exactly. Zero new attack surface.
- **PUBLIC** (any machine): `mcp.arif-fazil.com` doors — works from anywhere; transport auth-free, tool-level session governance.

**Layer behaviors:**
- **L0 SessionStart** → POST `initialize` + `arif_init` → persist `session_id`/SCT to plugin state file → bounded context injection (`additionalContextLimit`).
- **L3 PostToolUse** → `flow_ingest` receipt `{trace_id, actor, step_type, epistemic_label}` → server-side FQ ledger.
- **L3 Stop** → best-effort close (seal recommendation, graceful if unreachable).
- **L2 skills** ship 3 items: `arifos-router` (gap → canonical tool), `init`, `seal`. The 555-mesh stays server-side (`skill://` resources). One writer, many views.
- **Degradation ladder:** federation unreachable → plugin degrades to OBSERVE_ONLY. It never mints local authority to "keep working."

## 3. Federation invariant deltas (FI-01..FI-08, on top of I-01..I-41)

| # | Invariant |
|---|---|
| FI-01 | Zero authority in the archive: no secrets, no bearer literals; transport auth only via `bearer_token_env_var` if ever added |
| FI-02 | Session continuity contract (server.json v0.1.0): SCT persists across tool handoff; canonical tool identity explicit in every envelope |
| FI-03 | One writer, many views: plugin skills are renderings/pointers; the AAA mesh is the single SOT |
| FI-04 | Degradation ladder: unreachable ≠ authority switch; OBSERVE_ONLY is the floor |
| FI-05 | Receipts round-trip: every consequential action reaches arifFlow with trace_id; FQ visible server-side |
| FI-06 | Stateful doors get stateful clients: RMCP carries `Mcp-Session-Id` (bare curl must handshake — measured today, -32600) |
| FI-07 | Marketplace local-first; public publish is an F13 binary |
| FI-08 | Counts from sensors only: tool/skill/organ numbers are probed at runtime, never quoted from boot files (per FI-005's own witness contract) |

## 4. Phased plan

| Phase | Scope | Tier | Gate |
|---|---|---|---|
| P1 | Skeleton plugin + personal marketplace (`~/.agents/plugins/`), LOCAL profile, kernel+5 organ doors; `validate_plugin.py` green | T1 | none — reversible, no install beyond local marketplace |
| P2 | Hooks spine: SessionStart bind, PostToolUse receipts, Stop close; verify hook env surface empirically | T1–T2 | announce |
| P3 | PUBLIC profile variant + multi-runtime README (Codex/Claude/Kimi same doors) | T2 | announce; publish = F13 |
| P4 | `.app.json` + scheduled tasks → chron organ mapping | T3 | 888_HOLD design review |

## 5. Honest unknowns (declared, not guessed)

1. `.app.json` full schema — source dive required before P4.
2. Exact env vars Codex passes to hook commands — verify empirically in P2 before relying.
3. Whether plugin-context `mcpServers` honors `bearer_token_env_var` (config.toml does; plugin spec shows `type`+`url` only) — only relevant if transport auth is added later.

## 6. Sovereign binary (the only decision)

Keep the plugin **personal-first** (local marketplace, localhost doors) — or also cut the **public profile** now? No money, no new dependencies either way. Everything else executes on my authority.

---

## Addendum — P1 EXECUTED (2026-09-25 ~12:50 MYT, FI-008)

**Decisions resolved from standing canon (musyawarah satisfied by two convergent deep-research passes — FI-008 + FI-005):**
1. ONE consolidated plugin (anti-duplication; per-organ forks only if discovery suffers).
2. Personal marketplace, local source (`~/.agents/plugins/marketplace.json`) — public profile remains the F13 binary.
3. Hard-block lane = F13 standing T3 list only (rm -rf / DROP TABLE / force-push-main / raw device writes), pure local regex, no network dependency; all else advisory + receipted.
4. `interface.capabilities = ["Interactive","Write"]` — honest (hooks write receipts; no lying on manifest).

**Built:** `/root/.agents/plugins/plugins/arif-irfan/` — plugin.json (inline HTTP mcpServers ×5 localhost doors, hooks key omitted per validator notes), hooks.json (4 events, absolute paths, bounded timeouts), 4 handler scripts (stdlib-only, offline-safe), 3 pointer-skills (router/init/seal), README, local checker.

**Verified live (claim_state: MEASURED):**
- Checker: 34/34 green against documented rejection rules (binary validator pending P2).
- Authority gate: 6/6 lanes correct — rm -rf / DROP TABLE / force-push-main → exit 2 BLOCK; force-push-dev / safe / empty-stdin → exit 0.
- Kernel bind: real `arif_init` on :8088 → session `SEAL-81f16a0e0c7e4bdb`; **token's allowed-tools list excludes arif_forge/arif_seal under OBSERVE_ONLY — Capability ≠ Authority enforced by the kernel, not the plugin (FI-01 demonstrated).**
- Witness lane: trace_id receipts to local ledger + **mirror to arifFlow metabolic REST ledger `/ingest` → 200**; probe receipt = ledger entry #1000; live FQ 1.25 OPTIMAL.
- Session unbind/close lane: inventory prints, graceful.

**New substrate fact discovered (was honest-unknown):** arifFlow has no MCP-over-HTTP door; the metabolic ledger ingests via REST `POST 127.0.0.1:7073/ingest` with `FlowReceipt` schema (src/receipt.rs): enums `StepType{Execute,Verify,Cool,Seal,Barrier,Merge,Route}`, `RiskClass{T0Observe,T1Mutate,T2Deploy,T3Irreversible}`, `CoolingDecision{None,Hold,Clamp,Bypass}`, required: receipt_id(UUID), created_at, step_number, cost_ns, vectors. Schema recovered by error-driven probing + source read.

**P2 remains:** verify hook payload/exit-code conventions against the real Codex runner at first live install; run the binary `validate_plugin.py`; wire `interface` URLs if publishing. Plugin is discoverable (personal marketplace) but NOT auto-installed — activation is Arif's word or natural use.

