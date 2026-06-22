# ADR-003: AAA PENTAGON — Final Canonical Agent Architecture

| Field | Value |
|---|---|
| **Status** | **SEALED — VAULT999 chain 2505** |
| **Seal ID** | `PENTAGON-AGENTS-FORGE-20260602` |
| **Verdict** | SEAL |
| **Authority** | Muhammad Arif bin Fazil — F13 SOVEREIGN |
| **Ratified** | 2026-06-02T19:54:59.815809+00:00 |
| **Chain Length** | 2505 |
| **Merkle Leaf** | `69c65e7c64e3dd1fdc08aac7bf862be3...` |
| **Predecessor** | `TRUTH-BOUND-UPGRADE-20260602` (recursive alignment) |
| **Protocol** | A2A v1.0.1 |
| **Architecture** | PENTAGON — Hybrid 5 (3 PRIMARY + 2 SUPPORT) |
| **Total Skills** | 20 across 5 agents |
| **Supersedes** | ADR-001 (stage-based v1), ADR-002 (hybrid v2 draft) |
| **Motto** | DITEMPA BUKAN DIBERI |

---

## 1. The PENTAGON (Final Canonical)

### PRIMARY (3) — Active Decision Triangle

| Agent | Class | Role | Skills | Trinity |
|---|---|---|---|---|
| **333-AGI** | AGI | reasons + executes (FORGE subsumed) | **10** | Δ MIND |
| **555-ASI** | ASI | ethical + memory + audit lineage | **3** | Ω HEART |
| **888-APEX** | APEX | constitutional judge, F1-F13 arbitration | **2** | ΦΙ JUDGE |

### SUPPORT (2) — Parallel Observers (not in decision flow)

| Agent | Class | Role | Skills | Tag |
|---|---|---|---|---|
| **A-AUDIT** | APEX oversight | continuous ethical + safety monitor | **2** | [oversight] |
| **A-ARCHIVE** | ASI service | immutable ledger keeper + audit trail | **3** | SEAL |

**Total: 20 skills across 5 agents**

---

## 2. The 20 Skills

### 333-AGI (10 skills)

| # | Skill ID | Name | Category |
|---|---|---|---|
| 1 | `arif-evidence-reasoning` | Evidence Reasoning | Reasoning |
| 2 | `arif-hypothesis-generation` | Hypothesis Generation | Reasoning |
| 3 | `arif-task-decomposition` | Task Decomposition | Reasoning |
| 4 | `arif-session-init` | Session Init | Reasoning |
| 5 | `arif-sense-observe` | Sense & Observe | Reasoning |
| 6 | `arif-evidence-fetch` | Evidence Fetch | Reasoning |
| 7 | `arif-mind-reason` | Mind Reason | Reasoning |
| 8 | `arif-ops-measure` | Ops Measure | FORGE_subsumed |
| 9 | `arif-forge-execute` | Forge Execute | FORGE_subsumed |
| 10 | `arif-forge-deploy` | Forge Deploy | FORGE_subsumed |

### 555-ASI (3 skills)

| # | Skill ID | Name |
|---|---|---|
| 11 | `arif-ethical-critique` | Ethical Critique |
| 12 | `arif-deep-memory-synthesis` | Deep Memory Synthesis |
| 13 | `arif-anti-beautiful-one` | Anti-Beautiful-One Detection |

### 888-APEX (2 skills)

| # | Skill ID | Name |
|---|---|---|
| 14 | `arif-constitutional-arbitration` | Constitucional Arbitration (F1-F13) |
| 15 | `arif-hold-protocol` | 888_HOLD Protocol |

### A-AUDIT (2 skills)

| # | Skill ID | Name |
|---|---|---|
| 16 | `arif-floor-compliance-check` | Floor Compliance Check |
| 17 | `arif-inter-agent-consistency` | Inter-Agent Consistency Check |

### A-ARCHIVE (3 skills)

| # | Skill ID | Name |
|---|---|---|
| 18 | `arif-seal-write` | SEAL Write (Append-Only) |
| 19 | `arif-seal-read` | SEAL Read (Audit Query) |
| 20 | `arif-integrity-proof` | Ledger Integrity Proof |

---

## 3. Topology (The Truth-Bound Shape)

```
                    ┌─────────────────────────────────┐
                    │        000-SALAM (Human)         │
                    │   Sovereign · F13 · Final veto   │
                    └────────────────┬────────────────┘
                                     │
        ╔════════════════════════════╧════════════════════════════╗
        ║            PRIMARY TRIANGLE (bidirectional)              ║
        ║                                                          ║
        ║              ┌───────────────────────┐                   ║
        ║              │      333-AGI          │                   ║
        ║              │   Δ MIND · 10 skills  │                   ║
        ║              │   reason + execute     │                   ║
        ║              └───┬───────────┬───────┘                   ║
        ║      proposal +  │           │  draft for               ║
        ║       concern    │           │  ratification             ║
        ║                  ▼           ▼                            ║
        ║   ┌──────────────────┐   ┌──────────────────┐           ║
        ║   │    555-ASI       │   │    888-APEX       │           ║
        ║   │  Ω HEART · 3 sk │◄─►│  ΦΙ JUDGE · 2 sk │           ║
        ║   │  critique+memory │   │  F1-F13 arbitrate │           ║
        ║   └──────────────────┘   └────────┬─────────┘           ║
        ╚═══════════════════════════════════╪═════════════════════╝
                                             │
              ┌──────────────────────────────┼──────────────────┐
              │                              │                  │
              ▼                              ▼                  ▼
  ┌──────────────────┐          ┌──────────────────┐  ┌─────────────┐
  │    A-AUDIT       │          │   A-ARCHIVE      │  │  000-SALAM  │
  │  [oversight]     │          │   SEAL · 3 sk    │  │  (on HOLD)  │
  │  watches ALL 3   │─────────►│   VAULT999       │  │  resolves   │
  │  2 skills        │ receipt  │   append-only     │  │  888_HOLD   │
  └──────────────────┘          └──────────────────┘  └─────────────┘

  ─── LEGEND ─────────────────────────────────────────
  PRIMARY:  DO the work    (federation, A2A-visible)
  SUPPORT:  WATCH & RECORD (internal, control-plane)
  000-SALAM: SOVEREIGN     (human, not an agent)
  ◄─►  bidirectional propose/validate
  ─►   triggered flow
  ─────────────────────────────────────────────────────
```

---

## 4. Governance Boundary Matrix

| Boundary | 333-AGI | 555-ASI | 888-APEX | A-AUDIT | A-ARCHIVE |
|---|---|---|---|---|---|
| Generate reasoning | ✅ PRIMARY | ❌ | ❌ | ❌ | ❌ |
| Execute (FORGE) | ✅ SUBSUMED | ❌ | ❌ | ❌ | ❌ |
| Ethical critique | ❌ | ✅ PRIMARY | ✅ FINAL | ❌ | ❌ |
| Deep memory synthesis | ❌ | ✅ PRIMARY | ❌ | ❌ | ❌ |
| Issue verdicts | ❌ | ❌ | ✅ PRIMARY | ❌ | ❌ |
| Trigger 888_HOLD | ⚠️ request | ✅ trigger | ✅ authority | ✅ escalate | ❌ |
| Write to VAULT999 | ❌ | ❌ | ❌ | ❌ | ✅ PRIMARY |
| Verify floor compliance | ❌ | ⚠️ partial | ✅ arbitrate | ✅ verify | ❌ |
| Watch other agents | ❌ | ❌ | ❌ | ✅ PRIMARY | ❌ |
| Override other agents | ❌ | ❌ | ✅ VETO | ❌ | ❌ |
| Human escalation | ❌ | ❌ | ✅ escalate | ⚠️ via 888 | ❌ |
| Self-authorize destructive | ❌ | ❌ | ❌ | ❌ | ❌ |
| Override human (F13) | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 5. Key Decisions Ratified

1. **5 agents, not 6, not 3** — sovereign directive (3 primary + 2 support)
2. **FORGE is AGI** — subsumed into 333-AGI as sub-skills (`arif-ops-measure`, `arif-forge-execute`, `arif-forge-deploy`)
3. **555-ASI, not 666-ASI** — MEMORY stage for audit lineage
4. **A-AUDIT and A-ARCHIVE are support agents** — parallel, not in active decision flow
5. **A2A v1.0.1 spec** — `skills[]` arrays, `securitySchemes`, `capabilities`, `defaultInputModes/OutputModes`
6. **6 organs demoted to infrastructure** — no longer in agent registry
7. **Sovereign 000-SALAM above the registry** — the human is not an agent

---

## 6. What Was Forged

| File | What | Status |
|---|---|---|
| `/root/AAA/agents/PENTAGON.yaml` | Canonical source — 5 agents, 20 skills, topology, lifecycle, cascades | 🟢 written |
| `/root/AAA/public/a2a/agents.json` | A2A v1.0.1-spec compliant registry, 20 skills, `skills[]` + `securitySchemes` + `capabilities` | 🟡 generated |
| `/root/AAA/a2a-server/server.js` (line 1038-1055) | Peer list matches PENTAGON (5 agents) | 🟢 updated |
| `/root/AAA/README.md` (lines 136-149) | 3+2 split table, FORGE subsumed, A-AUDIT/A-ARCHIVE tagged support | 🟢 updated |
| `/root/AAA/dist/` | Built + deployed via rsync to aaa.arif-fazil.com | 🔵 deployed |
| `https://aaa.arif-fazil.com/a2a/agents.json` | Live verification — 5 agents, A2A v1.0.1, 20 skills | 🟢 live |
| `/root/VAULT999/outcomes.jsonl` line 2505 | SEAL entry `PENTAGON-AGENTS-FORGE-20260602` | 🔒 sealed |

---

## 7. Invariants (Non-Negotiable)

1. **Governance > Fluency** — constitutional compliance outranks response quality
2. **Fail-Closed** — weak evidence → UNKNOWN; high stakes → 888_HOLD
3. **Human Sovereignty (F13)** — no agent overrides the human. Ever.
4. **Trinity Consensus** — SEAL requires Δ(Mind) + Ω(Heart) agreement
5. **Append-Only Ledger** — A-ARCHIVE entries are immutable
6. **Gödel Lock** — the system must admit what it cannot know
7. **No Self-Authorization** — no agent approves its own high-risk outputs
8. **Two-Tier Separation** — primaries DO, supports WATCH. Never collapse tiers.
9. **A-AUDIT Independence** — cannot be disabled or bypassed by primaries
10. **555 = Deep Memory** — superintelligence is deeper remembering, not faster thinking

---

## 8. SEAL Receipt

```json
{
  "seal_id": "PENTAGON-AGENTS-FORGE-20260602",
  "verdict": "SEAL",
  "authority": "Muhammad Arif bin Fazil — F13 SOVEREIGN",
  "ratified": "2026-06-02T19:54:59.815809+00:00",
  "chain_length": 2505,
  "merkle_leaf": "69c65e7c64e3dd1fdc08aac7bf862be3...",
  "predecessor": "TRUTH-BOUND-UPGRADE-20260602"
}
```

---

*The PENTAGON is forged. The cockpit is live. The forge continues.*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE.*

*Forged: 2026-06-02T19:54:59+00:00 · Architect: Muhammad Arif bin Fazil*
