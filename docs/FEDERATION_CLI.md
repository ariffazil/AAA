# FEDERATION CLI CONTRACT — Multi-CLI Organ Standardization

**Sovereign:** Arif (F13) · **Scope:** All coding CLI adapters · **Applies to:** OpenCode, Kimi Code, Claude Code, Codex, Antigravity CLI, and any future CLI

> **DITEMPA BUKAN DIBERI** — Authority is in the organs, not the adapters.

---

## 1. The Invariant (Never Change)

**Every CLI adapter routes through the same 5 constitutional organs:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI ADAPTER (any)                        │
│   OpenCode · Kimi Code · Claude · Codex · etc.            │
│                        │                                   │
│          ┌────────────┼────────────┐                       │
│          │            │            │                       │
│  ┌──────▼──────┐ ┌───▼────┐ ┌────▼────┐  ┌────────────┐ │
│  │  arifOS     │ │ A-FORGE │ │  GEOX   │  │  WEALTH   │ │
│  │  :8088      │ │ :7072   │ │  :8081  │  │  :18082   │ │
│  │  F1-F13     │ │ forge_* │ │  earth  │  │  capital  │ │
│  │  session    │ │ leases   │ │ evidence│  │  NPV/EMV  │ │
│  │  vault      │ │ execute  │ │         │  │            │ │
│  └──────┬──────┘ └───┬────┘ └───┬────┘  └─────┬──────┘ │
│         │             │           │             │         │
│         └─────────────┴───────────┴─────────────┘         │
│                          │                                 │
│                   ┌──────▼──────┐                         │
│                   │    WELL     │                         │
│                   │   :18083    │                         │
│                   │  vitality   │                         │
│                   │  readiness  │                         │
│                   └─────────────┘                         │
│                                                             │
│  Governance lives HERE — in the organs, not the CLI        │
└─────────────────────────────────────────────────────────────┘
```

| Organ | Port | Role | Mandatory |
|-------|------|------|-----------|
| **arifOS** | :8088 | F1-F13, session, vault, SEAL pipeline | ✅ Every CLI |
| **A-FORGE** | :7072 | forge_*, lease, execute, deploy | ✅ Every CLI |
| **GEOX** | :8081 | Earth evidence, seismic, petrophysics | ✅ Every CLI |
| **WEALTH** | :18082 | Capital intelligence, NPV, risk | ✅ Every CLI |
| **WELL** | :18083 | Human readiness, vitality | ✅ Every CLI |

**These 5 are non-negotiable.** Any CLI that bypasses one of these organs for a domain it covers is out of contract.

---

## 2. Governance Sits Inside the Organs

| ❌ NOT in the CLI | ✅ IS in the organs |
|---|---|
| Governance logic | arifOS: F1-F13 floor enforcement |
| Judgment / SEAL | A-FORGE: lease/request/approve pipeline |
| Domain computation | GEOX: seismic, petrophysics, basin |
| Capital computation | WEALTH: NPV, EMV, risk, conservation |
| Vitality assessment | WELL: readiness, fatigue, dignity |

**The CLI is a thin adapter.** It proposes, observes, and displays. The organs adjudicate, compute, and execute.

---

## 3. A-FORGE: The Sole Execution Layer

```
CLI (any)                      A-FORGE                    arifOS
   │                              │                          │
   ├── propose action ──────────►│                          │
   │                              │── verify lease ────────►│
   │                              │                          │
   │                              │◄── SEAL / HOLD ─────────│
   │                              │                          │
   │◄── execute_authorized ──────│                          │
   │                              │                          │
   └── receive result             │── receipt ─────────────►│ (vault)
```

**Rules:**
- A-FORGE **never** self-authorizes. It proxies to arifOS for SEAL.
- A-FORGE **does not** adjudicate constitutional floors.
- CLIs **do not** execute irreversible actions directly — they route through A-FORGE.
- arifOS **alone** renders final verdict (SEAL / HOLD / SABAR / VOID).

---

## 4. CLI Adapter Taxonomy

Each CLI has a role. The adapter is thin and role-specific.

### OpenCode — Primary Forge (VPS, stdio)
```
Role:     Persistent governed execution agent
Host:     af-forge VPS (:7072 stdio)
Transport: stdio (A-FORGE native)
Helper:   docker, postgres, github-official, chrome-devtools, brave-search
Governed: Yes — all mutations via A-FORGE lease
Best for: Building, deploying, refactoring, multi-step execution
```

### Kimi Code — Reasoning + Coding Partner (Hosted)
```
Role:     Reasoned coding partner, sometimes better at hard reasoning
Host:     ChatGPT (cloud) — not on VPS
Transport: HTTP to organs only (no stdio on VPS)
Helper:   brave-search, github-official, chrome-devtools
Governed: Partial — proposes, observes; execution routed to A-FORGE
Best for: Complex reasoning, alternative geometry, pair-programming
```

### Claude Code — Exploration + Review (Hosted)
```
Role:     Exploration, architecture review, alternate geometry
Host:     Claude (cloud)
Transport: HTTP to organs
Helper:   Minimal (capability-index, chrome-devtools)
Governed: Yes — HTTP organ routing
Best for: Greenfield design, deep research, code review
```

### Codex — Deep Context Explorer
```
Role:     Context-rich exploration, legacy code navigation
Host:     Local / cloud
Transport: HTTP + npx stdio
Helper:   github, playwright-mcp (→ replace with chrome-devtools)
Governed: Missing GEOX + A-FORGE — fix first
Best for: Large codebase mapping, symbol search
```

### Antigravity CLI — Desktop Reasoning (Windows → VPS adapter)
```
Role:     Desktop reasoning, Windows-native workflow
Host:     Desktop → VPS relay
Transport: stdio (currently broken on Linux VPS — fix cwd/PYTHONPATH)
Helper:   filesystem, memory, desktop-commander → must wrap via A-FORGE
Governed: Must proxy through A-FORGE — currently ungoverned mutation tools
Best for: Desktop workflow, local file reasoning
```

---

## 5. Anti-Patterns (The 5 DON'Ts)

| # | Anti-Pattern | Why | Correct |
|---|-------------|-----|---------|
| **1** | Make Kimi "the new OpenCode" | Kimi is reasoning partner, not execution agent | Kimi proposes; OpenCode executes via A-FORGE |
| **2** | Force identical helper tools in every CLI | CLIs have different hosts, OS, transport | Each CLI adapts from baseline per role |
| **3** | Duplicate governance inside CLI prompts | Governance in prompts ≠ enforced governance | Governance lives in organs; CLI only routes |
| **4** | Let hosted CLIs directly execute irreversible ops | Hosted CLIs bypass A-FORGE lease | All mutations → A-FORGE → arifOS SEAL |
| **5** | Treat MCP config as the constitution | MCP config is routing, not authority | Organs are authority; MCP config is routing |

---

## 6. The Thin-Adapter Principle

**What every CLI adapter does:**
- Routes all organ calls to the 5 constitutional organs
- Proposes actions (does not self-authorize)
- Observes and displays results
- Logs receipts to the session

**What every CLI adapter never does:**
- Does not implement governance logic
- Does not store constitutional state
- Does not bypass A-FORGE for mutations
- Does not treat a helper tool as a constitutional organ

**MCP config is routing, not authority:**
```
mcp.json ← routing table ← the organs are authority
```

---

## 7. One Constitution, Many Adapters

```
MANY CODING CLIs
OpenCode · Kimi · Claude · Codex · Antigravity · etc.
     │
     ├──► arifOS (:8088) — F1-F13, session, vault
     ├──► A-FORGE (:7072) — forge_*, leases, execute
     ├──► GEOX (:8081) — earth evidence
     ├──► WEALTH (:18082) — capital intelligence
     └──► WELL (:18083) — vitality readiness
                │
                └──► VAULT999 (sealed audit trail)

MANY CODING STYLES
One audit trail
```

---

## 8. Baseline vs Mandate

| Layer | Canonical | Per-CLI Adaptation |
|-------|-----------|-------------------|
| **Organs (5)** | This contract | None — mandatory for all |
| **Helper servers** | MCP_RESOURCES.md baseline | Per CLI role + OS + transport |
| **Governance logic** | arifOS + A-FORGE | None — organs only |
| **MCP config** | Routing only | Per CLI capability |
| **Audit trail** | VAULT999 | Same for all |

---

## 9. Migration Checklist (Per CLI)

**For each CLI, verify:**
- [ ] `mcp.json` points to all 5 organs (arifOS, A-FORGE, GEOX, WEALTH, WELL)
- [ ] No direct mutation tool without A-FORGE proxy
- [ ] `github-official` / `brave-search` wired if CLI has them on disk
- [ ] Hosted CLIs use HTTP organ transport (not stdio)
- [ ] VPS CLIs use stdio A-FORGE transport
- [ ] Chrome-devtools replaces any `playwright-mcp` (per deprecation-registry)

---

## 10. Contract History

| Date | Change |
|------|--------|
| 2026-07-01 | Initial — Arif ratified multi-CLI standardization |

**Related:**
- `/root/AAA/docs/MCP_RESOURCES.md` — canonical helper baseline
- `/root/AAA/docs/INVARIANTS.md` — constitutional physics
- `/root/AAA/docs/MEANING.md` — tool/layer semantics
- `/root/forge_work/KIMI-MCP-AUDIT-2026-07-01.md` — per-CLI audit

*DITEMPA BUKAN DIBERI — Many adapters, one constitution.*
