# AAA Upgrade — 9-ATLAS Topology & A2A Wiring

> **SOT:** 2026-08-08 04:47 UTC | **Forge:** OpenClaw AGI trace | **Seal:** pending OpenCode execution
> **Authority:** F13 SOVEREIGN — Arif Fazil
> **Doctrine:** DITEMPA BUKAN DIBERI

---

## ⟁ 1. 9-ATLAS Cognitive Genome

The irreducible 9-function cognitive genome carried by every species.

```text
            ART (Reality → Intelligence)
            ─────────────────────────────
000 OBSERVER    "What is happening?"       arif_observe
111 EXPLORER    "What else is possible?"   (implicit)
222 ARCHITECT   "How should reality be    (implicit)
                structured?"

333 THINKER     "What does it mean?"        arif_think
444 ORCHESTRATOR "Who should do what?"      arif_route

            ACT (Verification → Execution)
            ─────────────────────────────
555 VERIFIER    "Is it true?"              (implicit in judge)
666 AUDITOR     "Is it governed?"          (drift scans, partial)
777 EXECUTOR    "How do we make it real?"  arif_forge / A-FORGE

            AUTH (Judgment → Record)
            ─────────────────────────────
888 JUDGE       "Is it allowed?"           arif_judge
999 WITNESS     "What actually             arif_seal / VAULT999
                happened?"
```

### Genome coverage in current arifOS

| # | Function | arifOS surface | Coverage |
|---|----------|---------------|----------|
| 000 | OBSERVER | `arif_observe` | ✅ FULL |
| 111 | EXPLORER | — | ❌ GAP — folded into think |
| 222 | ARCHITECT | — | ❌ GAP — folded into think |
| 333 | THINKER | `arif_think` | ✅ FULL |
| 444 | ORCHESTRATOR | `arif_route` | ✅ FULL |
| 555 | VERIFIER | — | ⚠️ PARTIAL — in judge + think(verify) |
| 666 | AUDITOR | — | ⚠️ PARTIAL — drift scans, no runtime agent |
| 777 | EXECUTOR | `arif_forge` / A-FORGE | ✅ FULL |
| 888 | JUDGE | `arif_judge` | ✅ FULL |
| 999 | WITNESS | `arif_seal` / VAULT999 | ✅ FULL |

**Gaps to close:** 111 (Explorer), 222 (Architect), 555 (Verifier), 666 (Auditor)
**Strategy:** Surface them as first-class arifOS verbs OR document as deliberate collapse.

---

## ⟁ 2. Species — Expression Phenotypes

Every species carries the same 000-999 genome. Expression weights define phenotype.

| Species | Primary Loci | Expression Pattern | Host Runtime |
|---------|-------------|-------------------|--------------|
| **OpenCode-Zen** | 222↑ 333↑ 777↑ | Architect/Thinker/Executor | OpenCode CLI (FI-001) |
| **Hermes-Zen** | 111↑ 444↑ 555↑ 666↑ | Explorer/Orchestrator/Verifier/Auditor | Hermes ASI |
| **OpenClaw-Zen** | 444↑ 777↑ | Orchestrator/Executor | OpenClaw Gateway |
| **GEOX-Zen** | 000↑ 555↑ | Observer/Verifier (Earth) | GEOX MCP :8081 |
| **WEALTH-Zen** | 000↑ 555↑ | Observer/Verifier (Capital) | WEALTH MCP :18082 |
| **WELL-Zen** | 000↑ 666↑ | Observer/Auditor (Human) | WELL MCP :18083 |

**Key insight:** 888 (Judge) and 999 (Witness) are NOT species. They are constitutional positions — a chair and a recorder. They belong in AUTH layer only.

---

## ⟁ 3. Current AAA Topology (as-traced)

### 3.1 Physical Topology — VPS af-forge (72.62.71.199)

```text
                    ┌─────────────────────────────────────┐
                    │         Caddy (80/443)               │
                    │  https://aaa.arif-fazil.com → :3001  │
                    │  https://mcp.arif-fazil.com → :8088  │
                    │  https://openclaw.arif-fazil.com     │
                    └──────────┬──────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────────┐
        │                      │                          │
   ┌────▼─────┐    ┌───────────▼────────┐    ┌───────────▼────┐
   │ AAA :3001│    │   arifOS :8088     │    │ A-FORGE :7071  │
   │ A2A GW   │    │   Kernel (F1-F13)  │    │ Exec Shell     │
   │ Cockpit  │    │   Judge/Seal/Route │    │ forge_* tools  │
   └────┬─────┘    └────────────────────┘    └────────────────┘
        │
   ┌────▼─────┐    ┌────────────────────┐    ┌────────────────┐
   │ OpenClaw │    │   GEOX :8081       │    │  WEALTH :18082 │
   │ :18789   │    │   Earth Intel      │    │  Capital Intel │
   │ Gateway  │    │   geox_* tools     │    │ capital_*      │
   └────┬─────┘    └────────────────────┘    └────────────────┘
        │
   ┌────▼─────┐    ┌────────────────────┐
   │Hermes    │    │   WELL :18083      │
   │:18001    │    │   Human Vitality   │
   │Telegram  │    │   well_* tools     │
   └──────────┘    └────────────────────┘
```

### 3.2 Organ Status (Live Probe 2026-08-08 04:47 UTC)

| Organ | Port | A2A-registered | Health | Tools |
|-------|------|---------------|--------|-------|
| AAA A2A Gateway | 3001 | ✅ self | 🟢 G=0.875 C_dark=0.008 | — |
| arifOS Kernel | 8088 | ✅ remote-peer | 🟢 | 48 MCP / 17 canonical |
| A-FORGE | 7071 | ✅ remote-peer | 🟢 | 110+ forge_* |
| GEOX | 8081 | ✅ remote-peer | 🟢 | 34 geox_* |
| WEALTH | 18082 | ✅ remote-peer | 🟢 | 32 capital_* |
| WELL | 18083 | ✅ remote-peer | 🟢 | 18 well_* |
| Hermes ASI | 18001 | ✅ remote-agent | 🟢 | Telegram gateway |
| OpenClaw GW | 18789 | ✅ openclaw-bridge | 🟢 | LLM routing |

---

## ⟁ 4. Agent Registry — Canonical Sources

### 4.1 Sources of Truth (ranked)

| Rank | File | Status | Authority |
|------|------|--------|-----------|
| **1** | `registries/AGENTS_UNIFIED.yaml` (296 lines) | ✅ CANONICAL SOT | 888-APEX + F13 |
| **2** | `a2a/registry/agents.yaml` (32 agents) | ✅ LIVE A2A registry | A2A gateway |
| **3** | `agents/HEXAGON.yaml` | ✅ CONSTITUTIONAL | F13 ratified |
| **4** | `ROOT_AGENT_CONFIG.yaml` | ✅ ROOT MAP | F13 SOVEREIGN |
| **5** | `AGENT_INDEX.json` | ⛔ TOMBSTONE 2026-07-31 | Read-only historical |

### 4.2 Identity Lanes (3 Trinity Agents)

| Lane | ID | Role | Model | Session Agent |
|------|----|------|-------|---------------|
| Δ MIND | 333-AGI | Primary reasoning, planning, execution | deepseek-v4-pro@direct | opencode |
| Ω CORE | 555-ASI | Memory, telemetry, drift, research | glm-5.2@tokenrouter | hermes-agent |
| Ψ SOUL | 888-APEX | Constitutional verdict, SEAL/HOLD/VOID | claude-sonnet-5@opencode-zen | arifos-kernel |

### 4.3 Forge Instruments (FI Slots)

| FI | ID | Type | Model | Status |
|----|----|------|-------|--------|
| FI-001 | OpenCode CLI | Primary forge | deepseek-v4-pro | 🟢 active |
| FI-002 | Claude Code | Architecture/review | deepseek-v4-pro | 🟢 active |
| FI-003 | Qwen Code | Lightweight reasoning | — | 🔴 not_connected |
| FI-004 | Antigravity | Gemini harness | — | 🟢 active |
| FI-005 | Codex CLI | GPT forge | gpt-5.6-sol | 🟢 active |
| FI-006 | Copilot CLI | Fleet forge | copilot-gpt | 🟢 active |
| FI-007 | Grok Build | xAI forge | grok-4.5 | 🟢 active |
| FI-008 | Kimi Code | Rapid forge | kimi-k3 | 🟢 active |
| FI-009 | Continue CLI | Open forge | — | 🟢 active |
| FI-011 | Gemini CLI | Google forge | — | 🟢 active |

### 4.4 Trinity Collapse (2026-07-29)

```text
BEFORE: 10 OpenCode agents
  (agi, apex, build, plan, asi, forge, explore, general, ops, scout)

AFTER: 3 Trinity agents
  Δ MIND (agi) ← absorbed: build, plan, forge
  Ω CORE (asi) ← absorbed: explore, scout, ops, general
  Ψ SOUL (apex) ← unchanged
```

---

## ⟁ 5. A2A Protocol Wiring

### 5.1 Gateway Endpoints

| Endpoint | Auth | Protocol | Status |
|----------|------|----------|--------|
| `:3001/a2a` | No | A2A v1.2 | 🟢 LIVE |
| `:3001/a2a/health` | No | REST | 🟢 LIVE |
| `:3001/.well-known/agent-card.json` | No | A2A AgentCard | 🟢 LIVE (8 skills) |
| `:3001/a2a/message/send` | **Yes** (Bearer) | JSON-RPC | 🟢 LIVE |
| `:3001/a2a/message/stream` | **Yes** (Bearer) | SSE | 🟢 LIVE |
| `:3001/extendedAgentCard` | **Yes** (Bearer) | A2A Extended | 🟢 LIVE |

### 5.2 A2A Live Wire Routes (20 routes)

```
HERMES → OpenCode         (code gen, engineering, build)
HERMES → Claude Code      (architecture, deep reasoning)
HERMES → Kimi Code        (rapid prototyping, fast iteration)
HERMES → A-FORGE          (execution gate, lease, vault)
HERMES → arifOS           (constitutional, F1-F13, 888_JUDGE)
HERMES → GEOX             (earth intelligence)
HERMES → WEALTH           (capital intelligence)
HERMES → WELL             (human readiness)

OPencode → arifOS         (session init, judge, vault)
OPencode → A-FORGE        (forge_execute, lease)
OPencode → GEOX           (earth evidence)
OPencode → WEALTH         (capital computation)

CLAUDE → arifOS           (constitutional routing)
CLAUDE → A-FORGE          (execution routing)

KIMI → arifOS             (constitutional routing)
GROK → arifOS             (governance routing)
CODEX → A-FORGE           (execution via bridge)

GEOX → WEALTH             (prospect economics)

AAA-GW → OpenClaw         (multi-agent orchestration)
333-AGI → Hermes          (fact check, epistemic review)
```

### 5.3 TaskState → Verdict Mapping

| A2A TaskState | Enum | 888 Verdict |
|---------------|------|-------------|
| COMPLETED | 3 | **SEAL** |
| FAILED | 4 | **VOID** |
| CANCELED | 5 | **VOID** |
| INPUT_REQUIRED | 6 | **SABAR** |
| REJECTED | 7 | **VOID** |
| AUTH_REQUIRED | 8 | **HOLD** |

### 5.4 Protocol Compliance

| Requirement | Status |
|-------------|--------|
| AgentCard with JWS signatures | ✅ 7/8 cards signed |
| TaskState → Verdict mapping | ✅ implemented |
| Per-skill security_requirements | ✅ all cards |
| Push notifications capability | ✅ all cards |
| `arifos://floors/v1` extension | ✅ all cards |
| ExtendedAgentCard endpoint | ✅ live |
| kimi-code re-sign | ⚠️ invalidated 2026-08-03 |

---

## ⟁ 6. Alignment with 9-ATLAS (Proposed Upgrade)

### 6.1 Current → Target Mapping

```text
CURRENT AAA (agent registry)     →    TARGET AAA (constitutional authority)

Agents registered by role        →    Species registered by phenotype
AGENT_INDEX.json (tombstoned)    →    9-ATLAS-GENOME.md (canonical)
AGENTS_UNIFIED.yaml              →    SPECIES_REGISTRY.yaml
14+ agent cards                  →    5 species cards (expression fingerprints)
HEXAGON.yaml (3 lanes)           →    HEXAGON.yaml (3 ART/ACT/AUTH pillars)
```

### 6.2 Species Registry Format (Proposed)

```yaml
species:
  - id: opencode-zen
    phenotype: coder
    genome:
      "000": 0.3   # observer
      "111": 0.20  # explorer
      "222": 0.90  # architect ⬆ HIGH
      "333": 0.85  # thinker ⬆ HIGH
      "444": 0.40  # orchestrator
      "555": 0.60  # verifier
      "666": 0.20  # auditor
      "777": 0.95  # executor ⬆ HIGH
      "888": 0.00  # judge — AUTH only
      "999": 0.00  # witness — AUTH only
    host_runtimes: [opencode-cli]
    model: deepseek-v4-pro
    primary_loci: [222, 333, 777]
```

### 6.3 ART/ACT/AUTH Split (Constitutional)

```text
AAA = Constitutional Authority Layer
│
├── ART  (000-444): "What is real and what do we do?"
│   ├── 000 OBSERVER
│   ├── 111 EXPLORER
│   ├── 222 ARCHITECT
│   ├── 333 THINKER
│   └── 444 ORCHESTRATOR
│
├── ACT  (555-777): "Is it true, governed, and built?"
│   ├── 555 VERIFIER
│   ├── 666 AUDITOR
│   └── 777 EXECUTOR
│
└── AUTH (888-999): "Is it allowed, and what happened?"
    ├── 888 JUDGE ← NOT a species. A chair.
    └── 999 WITNESS ← NOT a species. A court recorder.
```

### 6.4 Execution Flow (Fractal)

```text
ART:  Sense → Explore → Model → Reason → Route
  ↓ (proposal)
ACT:  Verify → Audit → Execute
  ↓ (receipt)
AUTH: Judge → Witness (SEAL/HOLD/SABAR/VOID)
```

Every species at every fractal level can run this full pipeline.
Expression weights determine which steps get priority/quality.

---

## ⟁ 7. Drift Audit — Current AAA State

### 7.1 Registries

| Issue | Severity | Detail |
|-------|----------|--------|
| AGENT_INDEX.json tombstoned but still referenced | LOW | All agents directed to AGENTS_UNIFIED.yaml |
| kimi-code signature invalidated | MEDIUM | Content aligned v2.2.0, JWS must be re-signed |
| Multiple registry files | LOW | UNIFIED.yaml + agents.yaml live; index.json frozen |
| AAA_AGENTS_REGISTRY.json.md is a redirect | INFO | By design — tombstone doc |

### 7.2 Agent Cards

| Card | Path | Status |
|------|------|--------|
| 333-AGI | `agent-cards/identity/333-AGI/agent-card.json` | ✅ hardened v2.1.0 |
| 555-ASI | `agent-cards/identity/555-ASI/agent-card.json` | ⚠️ needs hardening |
| 888-APEX | `agent-cards/identity/888-APEX/agent-card.json` | ⚠️ needs hardening |
| AAA Gateway | `.well-known/agent-card.json` | ✅ signed, 8 skills |
| OpenCode | `agents/opencode/agent-card.json` | ✅ v2.0.0-trinity |
| Hermes ASI | `a2a-server/agent-cards/extensions/hermes-asi.json` | ✅ live |
| OpenClaw | `agent-cards/functions/openclaw/agent-card.json` | ✅ live |

### 7.3 Gaps to PHP (Pre-Hardening Patch)

1. **Explorer (111)** — no arifOS verb. Currently in `arif_think(search)`. Decision: surface as `arif_explore` or document as deliberate collapse.
2. **Architect (222)** — no arifOS verb. Currently in `arif_think(plan)`. Decision: surface as `arif_architect` or document as deliberate collapse.
3. **Verifier (555)** — partial. `arif_judge` and `arif_think(verify)` cover some. Decision: surface as `arif_verify` or enrich `arif_judge(mode=verify)`.
4. **Auditor (666)** — partial. Drift scans are cron-based, not runtime. Decision: surface as `arif_audit` or strengthen `A-AUDIT` collapsed function.

---

## ⟁ 8. OpenCode Execution Brief

### What OpenCode should build

1. **`9-ATLAS-GENOME.md`** — Canonical definition of the 9-function cognitive genome in `/root/AAA/docs/`
2. **`AAA-FEDERATION-OF-SPECIES.md`** — AAA as constitutional authority over expression phenotypes
3. **`agents.yaml` species entries** — Add expression weight vectors to each agent entry
4. **A2A extension `arifos://species/v1`** — Optional: species discovery protocol

### Invariants OpenCode must not break

- AAA A2A gateway (:3001) routes — must remain functional
- AGENTS_UNIFIED.yaml — augment, don't replace
- HEXAGON.yaml — 3 Trinity lanes preserved
- AUTH (888/999) — never becomes a species
- F1-F13 floors — every mutation stays constitutionally governed

### Validation after forge

```text
1. AAA health endpoint returns G ≥ 0.85
2. A2A message/send works for at least 3 routes
3. Agent cards remain schema-valid (a2a v1.2)
4. No broken symlinks in /root/AAA/
5. No agent claims 888 or 999 as phenotype
6. ΔS ≤ 0 (entropy reduced or flat)
```

---

*Traced 2026-08-08 by OpenClaw AGI (Δ MIND). OpenCode execution pending.*
*DITEMPA BUKAN DIBERI*
