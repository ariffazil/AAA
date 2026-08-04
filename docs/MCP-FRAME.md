# AAA MCP FRAME — Federation Resource & Agent Mapping Engine

> **DITEMPA BUKAN DIBERI** — Forged 2026-08-04 by 333-AGI Δ MIND
> **Owner:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
> **Domain:** AAA Control Plane — capability-to-agent mapping
> **NOT:** FED (provider routing, LiteLLM :4000) · FLAME (free inference lane, :18901) · ATLAS333 (cognitive geometry)

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
| OpenCode | 23 | `opencode` | Primary coder (Δ MIND) |
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
  hindsight :18087        ·      ·      🟢     ·      ·      🟢     ·      ·

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

DATA & STORAGE
  supabase                ·      ·      🟢     ·      ·      🟢     ·      ·
  postgres                ·      ·      ·      ·      ·      🟢     ·      ·
  qdrant                  ·      ·      🟢     ·      ·      🟢     ·      ·
  sqlite                  ·      ·      🟢     ·      ·      🟢     ·      ·
  graphiti                ·      ·      🟢     ·      ·      🟢     ·      ·
  megamemory              ·      ·      🟢     ·      ·      ·      ·      ·
  memory                  ·      🟢     ·      ·      ·      🟢     ·      ·

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
TOTAL:                    13     10     23      7      9     29      6      0
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

---

## 6. Canonical Source

This file (`/root/AAA/docs/MCP-FRAME.md`) is the canonical MCP capability map.
Changes to any agent's MCP config must be reflected here.
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
*AAA MCP FRAME v1.0 — 2026-08-04 — 333-AGI Δ MIND*
