<!-- SATELLITE | tier:satellite | sot:STATE.md | 2026-08-09 -->
> **Satellite** — historical elaboration / design note / prior draft.  
> **Canonical SOT:** [`STATE.md`](./STATE.md) (§1–16).  
> If this file conflicts with STATE.md, **STATE wins**. Do not fork law here.  
> *One truth · Many projections · 0 contradictions* · DITEMPA BUKAN DIBERI.

# AAA MCP FRAME — Federation Resource & Agent Mapping Engine

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-04 by 333-AGI Δ MIND
> **Updated:** 2026-08-10 — G9/G10 closed, ADR-005/006/007 ratified, 26-server registry live
> **Owner:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Domain:** AAA Control Plane — capability-to-agent mapping
> **NOT:** FED (provider routing, LiteLLM :4000) · FLAME (free inference lane, :18901) · ATLAS333 (cognitive geometry)
>
> **Registry:** `/root/AAA/registries/mcp_servers/INDEX.json` — 26 servers, 2026-07-28 stateless fields
> **Sync:** `/root/AAA/registries/mcp_servers/sync.py` — read-only diff emitter
> **Drift:** `/root/AAA/registries/mcp_servers/drift_audit.sh` — one-shot config vs live probe

---

## 0. Name Decision

```
FED    = provider router (LiteLLM proxy :4000) — "siapa bayar, route mana"
FLAME  = free inference lane (Hermes :18901) — "RM0 tools, stateless"
ATLAS333 = cognitive geometry (arifOS :8088) — "paradoxes, tension vectors"
AAA FRAME = MCP capability surface mapping — "agent mana ada tool apa"
```

**FRAME = Federation Resource & Agent Mapping Engine.** Lives under AAA control plane.

---

## 1. Agent Classes & Orthogonal Invariants

### 1.1 HERMES — EXTERNAL CLASS (Human Bridge)
**Invariant:** Hermes is the ONLY agent that communicates with Arif directly.
**Invariant:** Hermes must have access to ALL federation organs + ALL external bridges.
**Invariant:** Hermes never mutates production code — routes to coders.
**Invariant:** Hermes is the sensory surface — vision, audio, document, Telegram, email, calendar.

```
MCP surface: 13 active + 1 quarantined
Role:        Human ↔ Federation bridge
Authority:   OBSERVE + ROUTE only. Never EXECUTE code mutations.
Missing:     Gmail, Calendar, Sheets, Drive (Google Workspace surface)
             Telegram MCP (uses built-in toolsets instead)
             WhatsApp bridge
```

### 1.2 OPENCLAW — ORCHESTRATOR CLASS (Router + arifFLOW)
**Invariant:** OpenClaw controls arifFLOW — the metabolism nerve.
**Invariant:** OpenClaw routes tasks to coders but NEVER writes code itself.
**Invariant:** OpenClaw never communicates with Arif directly (that's Hermes).
**Invariant:** OpenClaw must have all 5 core organs + external search + filesystem.

```
MCP surface: 10 active
Role:        Task router + arifFLOW master
Authority:   ROUTE + OBSERVE. Never EXECUTE.
Missing:     arifFLOW MCP (should have it — the metabolism nerve owner)
             FED MCP (should know routing decisions)
```

### 1.3 CODER CLASS — OpenCode, Kimi Code, Codex, Copilot CLI
**Invariant:** Coders execute mutations through A-FORGE only.
**Invariant:** Coders never communicate with Arif directly (Hermes is the bridge).
**Invariant:** Coders must have: arifOS + A-FORGE + GEOX + WEALTH + WELL minimum.
**Invariant:** Coders route through FED for model selection — never direct provider.
**Invariant:** Git operations through A-FORGE governance, never raw git.

| Agent | MCP Count | FED Model Alias | Status |
|-------|----------|-----------------|--------|
| OpenCode | 25 | `opencode` | Primary coder (Δ MIND) — 21 extensions wired (5 disabled) |
| Kimi Code | 7 | `opencode` | FI-008 warga |
| Codex | 9 | `opencode` | GPT-5.6 solver |
| Copilot CLI | 29 ⚠️ | `opencode` | Too many MCPs — context warning |
| Claude Code | 6 | *(direct)* | Anthropic protocol, not FED |
| Aider | 0 | *(FED-only)* | No MCP config, provider-only |

### 1.4 CLAUDE CODE — CODER_DIRECT CLASS
**Invariant:** Claude Code uses Anthropic protocol directly — NOT routed through FED.
**Invariant:** Still must have all 5 core organs for federation work.
**Invariant:** Constitutional gating through arifOS — same as all coders.

### 1.5 AIDER — CODER_LIGHT CLASS
**Invariant:** Aider is provider-only — no MCP servers. Uses FED for model selection.
**Invariant:** All code mutations are local filesystem only — cannot use A-FORGE tools.

---

## 2. Orthogonal MCP Matrix

```
                        HERM  OCLAW  OPENC  KIMI  CODEX  COPIL  CLAUD  AIDER
                        ───── ───── ───── ───── ───── ───── ───── ─────
CORE ORGANS
  arifos    :8088         🟢     🟢     🟢     🟢     🟢     🟢     🟢     ·
  aforge    :7071/72      🟢     🟢     🟢     🟢     🟢     🟢     🟢     ·
  geox      :8081         🟢     🟢     🟢     🟢     🟢     🟢     🟢     ·
  wealth    :18082        🟢     🟢     🟢     🟢     🟢     🟢     🟢     ·
  well      :18083        🟢     🟢     🟢     🟢     🟢     🟢     🟢     ·

INFRASTRUCTURE
  fed       :7074         🟢     ·      🟢     🟢     ·      ·      ·      ·
  arifflow  :7073         ·      ·      🟢     🟢     ·      🟢     ·      ·
  hermes    :18901        🟢     ·      🟢     ·      ·      🟢     ·      ·
  hermes-agent :18090     ·      ·      🟢     ·      ·      ·      ·      ·
  hindsight :18087 (RETIRED 2026-08-05)  ·      ·      ·      ·      ·      ·      ·      ·

RESEARCH & SEARCH
  brave-search            ·      🟢     ·      ·      🟢     🟢     ·      ·
  context7                ·      ·      🟢     ·      ·      🟢     ·      ·
  minimax                 🟢     ·      🟢     ·      ·      ·      🟢     ·
  minimax-mcp             ·      🟢     ·      ·      ·      ·      ·      ·
  openrouter              🟢     ·      🟢     ·      ·      ·      ·      ·
  perplexity              ·      ·      ·      ·      ·      🟢     ·      ·
  exa                     ·      ·      ·      ·      ·      🟢     ·      ·
  fetch                   ·      ·      ·      ·      ·      🟢     ·      ·
  deep-research           🟢     ·      ·      ·      ·      ·      ·      ·
  free-search             ·      ·      🟢     ·      ·      ·      ·      ·

DATA & STORAGE
  supabase                ·      ·      🟢     ·      ·      🟢     ·      ·
  postgres                ·      ·      ·      ·      ·      🟢     ·      ·
  qdrant                  ·      ·      🟢     ·      ·      🟢     ·      ·
  sqlite                  ·      ·      🟢     ·      ·      🟢     ·      ·
  graphiti                ·      ·      🟢     ·      ·      🟢     ·      ·
  megamemory              ·      ·      🟢     ·      ·      ·      ·      ·
  memory                  ·      🟢     ·      ·      ·      🟢     ·      ·
  codebase-memory         ·      ·      🟢     ·      ·      ·      ·      ·

DEV TOOLS
  github                  🟢     ·      ·      ·      🟢     🟢     ·      ·
  semgrep                 ·      ·      🟢     ·      ·      🟢     ·      ·
  playwright              ·      ·      ·      ·      🟢     🟢     ·      ·
  hostinger-vps           ·      ·      🟢     ·      ·      🟢     ·      ·
  docker                  ·      ·      ·      ·      ·      🟢     ·      ·

META & UTILITY
  repomapper              ·      ·      🟢     ·      ·      🟢     ·      ·
  serena                  ·      ·      🟢     ·      ·      🟢     ·      ·
  capability-index        ·      ·      🟢     ·      🟢     🟢     ·      ·
  sequential-thinking     ·      ·      ·      ·      ·      🟢     ·      ·
  time                    ·      ·      ·      ·      ·      🟢     ·      ·
  filesystem              ·      🟢     ·      ·      ·      ·      ·      ·
  stealth-browser         ·      🟢     ·      ·      ·      ·      ·      ·
  hound                   🟢     ·      ·      ·      ·      ·      ·      ·
  mage                    🟢     ·      ·      ·      ·      ·      ·      ·
────────────────────────────────────────────────────────────────────────────
TOTAL:                    13     10     25      7      9     29      6      0
```

---

## 3. Archived / Off / Quarantined

| Server | Status | Agent | Reason |
|--------|--------|-------|--------|
| `serena-mcp` | 📦 QUARANTINED | Hermes | STDIO quarantine — migration target: streamable-http per-organ |
| `openrouter` | ⚠️ PHASING OUT | Hermes, OpenCode | Still wired but should be removed — FED replaces OpenRouter |

---

## 4. Gaps Identified

| # | Gap | Severity | Action |
|---|-----|----------|--------|
| G1 | **Copilot CLI has 29 MCPs** — context window warning | HIGH | Trim to ≤15. Copilot doesn't need `perplexity`, `exa`, `fetch`, `docker`, `time` — those are OpenCode's domain |
| G2 | **OpenClaw missing arifFLOW MCP** | HIGH | Wire `arifflow` — it's the metabolism nerve owner |
| G3 | **OpenClaw missing FED MCP** | MEDIUM | Should know routing decisions |
| G4 | **Hermes missing Google Workspace** (Gmail, Calendar, Sheets) | MEDIUM | External bridge incomplete |
| G5 | **Kimi Code has only 7 MCPs** | LOW | May need `github`, `context7`, `semgrep` for full coder capability |
| G6 | **Aider has 0 MCPs** | LOW | By design — lightweight, provider-only. Acceptable. |
| G7 | **OpenRouter still wired** in Hermes + OpenCode | LOW | Remove — FED replaces it completely |
| G8 | **Claude Code not on FED** | ARCHITECTURAL | Anthropic protocol limitation — cannot route through LiteLLM |
| G9 | **MCP registry incomplete** — 5 organs tracked, 21 extension servers missing | HIGH | ✅ CLOSED 2026-08-10 — INDEX.json extended to 26 servers, sync.py diff emitter live, per-server files created |
| G10 | **Stateless MCP readiness** — registry not tracking 2026-07-28 protocol changes | MEDIUM | ✅ CLOSED 2026-08-10 — all 26 entries carry protocol_versions_supported, mrtr_capable, subscriptions, cache_scope |

---

## 5. Architecture Decision Records

### ADR-001: FRAME, not FED, not FLAME
**Decision:** This MCP capability-to-agent mapping is called AAA MCP FRAME.
**Rationale:** FED = provider routing (LiteLLM). FLAME = free inference. ATLAS333 = cognitive geometry. FRAME = what tools each agent can see.
**Date:** 2026-08-04

### ADR-002: Hermes is the ONLY external bridge
**Decision:** No other agent may communicate with Arif or external humans.
**Rationale:** Single audit point for all human interaction. Hermes controls Telegram, email, calendar. Coders route through Hermes for any human-bound output.
**Date:** 2026-08-04

### ADR-003: Copilot CLI must shed MCPs
**Decision:** Copilot CLI's 29 MCPs is excessive. Target: 15 maximum.
**Rationale:** Context window warning is a Copilot-side issue from loading too many MCP servers. Copilot should focus on coding tools — research/data tools belong to OpenCode.
**Date:** 2026-08-04

### ADR-004: OpenClaw owns arifFLOW
**Decision:** `arifflow` MCP must be wired to OpenClaw.
**Rationale:** OpenClaw is the router/orchestrator. arifFLOW is the metabolism nerve. The nerve owner must have the nerve tool.
**Date:** 2026-08-04

### ADR-005: MCP registry is INDEX.json + per-server files + sync.py (read-only)
**Decision:** The AAA MCP registry lives at `/root/AAA/registries/mcp_servers/` with INDEX.json as the canonical map and one JSON file per server following the 2026 MCP server schema. A `sync.py` script emits diffs between harness configs (opencode.json, etc.) and the registry — it never writes directly.
**Rationale:** E6 (functions before entities), E18 (every compression creates a blind spot), and the AAA skill-catalog / harness-view boundary require: (a) no new registry entity, (b) no sync liability from mirroring, (c) drift detection as a function on existing tools (forge_mcp_lifeguard), not a new tool. sync.py is a read-only diff observer. The per-server files extend an existing pattern (5 organs already had files). ΔS ≤ 0 by construction.
**Date:** 2026-08-10
**Protocol:** Stateless MCP 2026-07-28 fields (protocol_versions_supported, mrtr_capable, subscriptions, cache_scope, endpoints) added to all entries. Mcp-Session-Id deprecated → entries drop session state.
**Scope:** opencode-aligned 26 servers. External candidates (223) remain in `external/INDEX.json` as reference only.

### ADR-006: MCP drift audit is a mode on forge_mcp_lifeguard, not a new tool
**Decision:** MCP surface drift detection (config vs live health vs tool-list snapshots) is a new `drift_audit` mode on the existing `forge_mcp_lifeguard` tool at A-FORGE, not a standalone entity.
**Rationale:** E6 — functions before entities. forge_mcp_lifeguard already has the health probe + auto-recovery surface. Extending it with a drift audit mode is adding a function to an existing agent, not creating a new one. Output is a receipt, not a persistent file.
**Date:** 2026-08-10

### ADR-007: Stateless MCP 2026-07-28 as federation default
**Decision:** All MCP servers in the federation registry declare `protocol_versions_supported` and target the 2026-07-28 stateless spec. The `Mcp-Session-Id` header is removed; round-robin LB is permissible; `Mcp-Method` + `Mcp-Name` headers are required for WAF-layer auth.
**Rationale:** Stateless MCP scales like the rest of the web — CDN-cacheable, load-balanced, identity-decoupled. Federation benefits: WAF can route on headers, multi-instance deployment is trivial, cache hints (`ttlMs` + `cacheScope`) reduce polling. The cost of supporting session state is no longer worth the operational complexity.
**Date:** 2026-08-10
**Migration window:** 12-month minimum per MCP feature lifecycle policy. Servers still on 2025-11-25 are NOT removed; they are flagged as `protocol_versions_supported: ["2025-11-25"]` in the registry and will be re-evaluated in 2027-Q3.

---

## 6. Canonical Source

This file (`/root/AAA/docs/MCP-FRAME.md`) is the canonical MCP capability map.
Changes to any agent's MCP config must be reflected here.

The 26-server registry at `/root/AAA/registries/mcp_servers/` is the machine-readable
twin of this document. `sync.py` keeps it in lockstep with `/root/.config/opencode/opencode.json`.
Per-server entries follow the MCP 2026 server schema and carry stateless-ready fields
(`protocol_versions_supported`, `endpoints[]`, `mrtr_capable`, `subscriptions`, `cache_scope`).

Drift check: `bash /root/AAA/registries/mcp_servers/drift_audit.sh` (one-shot, read-only,
emits JSONL receipt per server). This is the `forge_mcp_lifeguard mode=drift` surface.

Probe command for live verification:
```bash
python3 -c "
import json, os
agents = {
    'OpenCode': '/root/.config/opencode/opencode.json',
    'Hermes': '/root/.hermes/config.yaml',
    'OpenClaw': '/root/.openclaw/openclaw.json',
    'Kimi Code': '/root/.kimi-code/mcp.json',
    'Codex': '/root/.codex/mcp.json',
    'Copilot CLI': '/root/.copilot/mcp-config.json',
    'Claude Code': '/root/.claude/settings.json',
}
for name, path in agents.items():
    if not os.path.exists(path):
        print(f'{name}: CONFIG MISSING')
        continue
    # count MCP entries
    print(f'{name}: config exists')
"
```

---

*DITEMPA BUKAN DIBERI — capabilities are forged, not given.*
*AAA MCP FRAME v1.1 — 2026-08-10 — 333-AGI Δ MIND (registry extension)*
