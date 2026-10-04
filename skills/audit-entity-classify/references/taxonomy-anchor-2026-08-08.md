## AAA Skill Taxonomy — Functional Index

Forged: 2026-08-08 by 333-AGI
Updated: 2026-08-08 — added 9-role agent topology anchors

The AAA skills are now indexed by function (not by prefix).

Canonical location: `/root/AAA/skills/TAXONOMY.md`

This file provides the canonical entity-identification anchors for the most frequently asked "what is X?" questions in the federation.

---

### The 9-Role Agent Kernel (HEXAGON v5.0)

> **Source:** `/root/AAA/agents/HEXAGON.yaml:10` — `architecture: "3+2+1+1 — 3 minds · 2 deeds · 1 forge · 1 vault · 1 path"`
> **Doctrine:** `/root/AAA/governance/adr/AAA_ADR_003_PENTAGON.md` (SEALED chain 2505)
> **Flow:** `/root/AAA/a2a-server/A2A_MAP.md:118` — `AGI_PROPOSE → ASI_REVIEW → APEX_JUDGE → AFORGE_EXECUTE → ASI_AUDIT → APEX_RESOLVE → VAULT_RECEIPT`
> **Canonical cards:** `/root/AAA/agents/_lanes/` (lanes) + `/root/AAA/agents/HEXAGON.yaml` (structure)

| # | Role | ID | Class | Duty | Cannot |
|---|---|---|---|---|---|
| 1 | 🧠 Δ MIND | `333-AGI` | Intelligence Principal | reason · plan · decompose · draft · propose | judge · seal · execute (post-2026-07-02, FORGE subsumed) |
| 2 | 💛 Ω HEART (REVIEW) | `555-ASI` | Intelligence Principal | preflight review · adversarial critique · memory synthesis | execute · judge · share context with AUDIT |
| 3 | ⚖️ ΦΙ JUDGE | `888-APEX` | Intelligence Principal | constitutional verdict · SEAL/HOLD/VOID · rollback · escalation | execute · produce domain evidence |
| 4 | 👁️ Watchdog | `A-AUDIT` | Support | floor compliance · inter-agent consistency · watches watchers (incl. APEX) | execute · judge |
| 5 | 📒 Archivist | `A-ARCHIVE` | Support | append-only SEAL · read audit · integrity proof · VAULT999 gatekeeper | judge · reinterpret |
| 6 | ⚒️ Hand | `A-FORGE` | Bounded Service | shell · docker · git · fs · deploy under SEAL lease | plan · self-authorize · self-seal |
| 7 | 💎 Witness | `VAULT999` | Bounded Service | hash-chained append-only immutable receipts | judge · rewrite |
| 8 | 🛡️ Kernel | `arifOS` | Bounded Service | 13 floors · 8 canonical verbs · session/identity · gate mutation | speak for self (zero ToM) |
| 9 | 🌐 Cockpit | `AAA` | Bounded Service | A2A gateway · registry · routing · visibility · human-facing | judge |

**SOVEREIGN (above all):** `000-SALAM` = Arif = F13 = not an agent, the source of purpose and veto.

#### Key structural invariants

- **3 discoverable agent cards:** `agi`, `asi`, `apex` (A-FORGE & VAULT999 are services, not agents) — see `/root/AAA/a2a-server/A2A_MAP.md:133-141`
- **ASI.REVIEW ≠ ASI.AUDIT:** blind audit required, no shared context, different invocation identity — see HEXAGON v5.0 `asi_context_isolation`
- **777-FORGE:** RETIRED 2026-07-02, spawn authority reassigned to 333-AGI. Not a live role.
- **A-AUDIT:** Functionally collapsed into 888-APEX cross-cutting per Zen 99 (2026-07-15), but lane identity preserved in `_lanes/A-AUDIT/`

#### Probe command (canonical flow)

```bash
# Verify agent roles exist in the agent registry
cat /root/AAA/registries/AGENTS_UNIFIED.yaml | grep -E '^\- id:|role:' | head -30

# Verify HEXAGON architecture string
grep 'architecture:' /root/AAA/agents/HEXAGON.yaml

# Verify 7 mandatory anti-theatre controls
grep 'anti_theatre_controls:' /root/AAA/agents/HEXAGON.yaml
```

---

### The 9-Cell Cognitive Atlas (000-999) — distinct decomposition

> **Forged:** 2026-08-08 — agent-driven synthesis, ratified as candidate doctrine (Arif)
> **Source:** EUREKA-019 (`/root/arifOS/GENESIS/019_REALITY_ENGINEERING_PROTOCOL.md`) + GENESIS-001 (`/root/arifOS/GENESIS/001_MUHAMMAD_MODE_ASI.md:204-206`) + HEXAGON v5.0
> **Status:** **DRAFT → CANON CANDIDATE** (Arif ratified the *decomposition logic*; spec doc pending F13 SEAL)
> **Distinction:** This is NOT the 9-Role HEXAGON above. Same count, different axis. The HEXAGON is **organisational** (which organ carries which deed). The 9-Cell Atlas is **functional** (which cognitive step every forge MUST traverse).

The 9-cell atlas is the **cognitive genome** — every federated phenotype (OpenCode-Zen, Hermes-Zen, OpenClaw-Zen, GEOX-Zen) carries it. The HEXAGON is which **cell-bearer** is currently responsible. Two views, one truth.

| Digit | Cell | Question | arifOS Verb | Flow Position |
|---|---|---|---|---|
| 000 | Observer | What is happening? | `arif_observe` | entry — intake signals/evidence/telemetry |
| 111 | Explorer | What else is possible? | (s16 skill today; verb TBD) | expand possibility space — search/scenario |
| 222 | Architect | How should reality be structured? | `arif_think mode=plan` | design patterns/systems/abstractions |
| 333 | Thinker | What does it mean? | `arif_think` | reason · analyze · synthesize |
| 444 | Orchestrator | Who should do what? | `arif_route` | routing · delegation · scheduling |
| 555 | Verifier | Is it true? | `arif_memory` (verification side) | evidence checks · contradictions · testing |
| 666 | Auditor | Is it governed correctly? | folded into `arif_judge` | policy · compliance · drift · boundary |
| 777 | Executor | How do we make it real? | `arif_forge` | build · deploy · write · act |
| 888 | Judge | Is it allowed? | `arif_judge` | SEAL/HOLD/SABAR/VOID |
| 999 | Witness | What actually happened? | `arif_seal` | VAULT999 attestation (special authority layer, not agent) |

**Compression triad (Reality → Intelligence → Governance → Witness):**
```
REALITY      = 000 Observe + 111 Explore + 222 Architect    = SENSE layer
INTELLIGENCE = 333 Think  + 444 Orchestrate + 555 Verify   = REASON layer
GOVERNANCE   = 666 Audit  + 777 Execute + 888 Judge         = JUDGMENT layer
WITNESS      = 999 Seal                                   = MEMORY layer
```

**Canonical mapping for already-living cells:**
- 555-Verifier + 666-Auditor = **1 agent, 2 deeds** (555-ASI.REVIEW blind to outcome; 555-ASI.AUDIT blind to REVIEW context) — keeps the Gödel lock
- 777-Executor lives in A-FORGE as **bounded service, not intelligence agent** (cannot plan, cannot self-authorize, cannot self-seal)
- 888-Judge is the **kernel MCP** `arif_judge` — Authority species, not cognition
- 999-Witness is the **kernel MCP** `arif_seal` + VAULT999 — Authority layer, not cognition

#### Phenotype / Genome / Constitution framing (Arif 2026-08-08)

```
AAA = Constitution                              (F1-F13 + principal_agent taxonomy)
9-Atlas = Cognitive Genome                      (universal cognitive substrate)
OpenCode-Zen / Hermes-Zen / OpenClaw-Zen = Phenotypes  (expression patterns)
888/999 = Authority primitives, not agents    (court + record, not cognition)
```

**The phenotype insight:** a CLI harness (OpenCode, Claude Code, Codex, Copilot, Kimi Code, Aider, Antigravity, Gemini-CLI, Grok-build, Continue-CLI) is NOT an agent. It is a **phenotype** — the same cognitive genome expressed through a particular body. The 10 LLM-principal harnesses in `/root/AAA/contracts/AAA_PRINCIPAL.md` §2.8 are all **expressions of one phenotype family**, not separate constitutional roles.

**The fractal claim with guard:** same 9-cell pattern repeats at well-defined boundaries (organ → kernel → function → subkernel → function), but ONLY at tool-call boundaries. Inside a single reasoning thread, the 9 cells are *roles*, not nested subkernels. **No nesting** is enforced at the harness level (OpenCode, Kimi, Hermes all converge on flat call tree) — see `/root/AAA/federation/architecture/identity_capability_routing_enforcement.md`.

**ART-ACT-AUTH orthogonal binding** (the binding that lets phenotype swap work):
```
ART (Ψ Reflex)  — pre-call tool wisdom          → 000/111/222/333/444/555/666/777
ACT (Δ Ceremony) — execution staging           → programs of calls (dry-run → canary → full → verify)
AUTH (Φ)        — identity + attestation       → 888 Judge + 999 Witness + 000 human sovereign
```
999 belongs in AUTH, not ART — it's the **attestation layer**, not a cognition cell.

#### What breaks if 9-Atlas disappears

| Failure | Consequence |
|---|---|
| Cells not named | Every phenotype reinvents the atlas locally → identity duplication |
| Cells collapse (e.g. 555-Verify into 666-Audit) | Gödel lock breaks → audit becomes confirmation bias |
| 999 moved into ART layer | Witness loses its attestation role → false provenance |
| Phenotypes mistaken for agents | Federation explodes headcount → no sovereignty ceiling |
| Fractal over-applied | Infinite regress → circular dispatch → federation fragmentation |

#### Probe commands (the 9-cell)

```bash
# Verify the 9-cell canonical chain lives in EUREKA-019 + GENESIS-001
grep -A 2 "000_INIT.*111_SENSE.*222_EVIDENCE" /root/arifOS/GENESIS/001_MUHAMMAD_MODE_ASI.md
grep -A 2 "111_SENSE.*333_REASON.*555_JUDGE" /root/arifOS/GENESIS/019_REALITY_ENGINEERING_PROTOCOL.md

# Verify HEXAGON 3+2+1+1 architecture (the 9-role carrier view)
grep 'architecture:' /root/AAA/agents/HEXAGON.yaml

# Verify the principal_agent taxonomy (the 9 phenotypes)
grep -E '^### 2\.' /root/AAA/contracts/AAA_PRINCIPAL.md

# Verify arifOS exposes 8 verbs (one per cognition cell, plus 999)
curl -s http://127.0.0.1:8088/health | jq '.canonical_tools'
```

---

### Registry of Canonical Anchors — Organs & Infrastructure

| Entity | Classification | Key Evidence | Source |
|---|---|---|---|
| AAA :3001 | Registry | 0 MCP tools, 38 agents, near-zero traffic | `curl :3001/.well-known/agents.json \| wc -l` |
| arifOS :8088 | Constitutional Kernel | 8 verbs, 888_HOLD on probe, `final_authority: ARIF` | `curl :8088/health \| jq .apex_scalars` |
| A-FORGE :7071/7072 | Execution Surface | 48+ tools, APA bridges, forge_execute path | `curl :7071/health \| jq .tool_count` |
| FED :7074 | Federation Cognitive Allocator | 14 tools, `constitutional_tier` parameter, 666/999 allowlist | `curl :7074/health \| jq .providers` |
| GEOX :8081 | Earth Intelligence Organ | 35 MCP tools, evidence-only | `curl :8081/tools/list` |
| WEALTH :18082 | Capital Intelligence Organ | 8 tools, evidence-only | `curl :18082/tools/list` |
| WELL :18083 | Vitality Intelligence Organ | 10 tools, reflect-only | `curl :18083/tools/list` |
| arifFlow :7073 | Metabolic Pulse | FQ=2.1, 31 receipts, invariant enforcement | `curl :7073/health \| jq .fq` |
| VAULT999 | Immutable Truth | Append-only, `chattr +a`, hash-chained | `lsattr /root/arifOS/VAULT999/outcomes.jsonl` |
| APEX | Governance Health Model | G=(APEX)^(1/4), 43675 rows, G=0.3156 | `apex_primitives.py::compute_apex_from_metrics` |
| i-ARIF | Training Data | 1435 pairs, AGPL-3.0, zero runtime artifacts | `cat /root/forge_work/i-arif-prep/manifest.json \| jq .total_pairs` |
| AGI/ASI/APEX lanes | Prompt-layer labels | Zero concrete class implementations | `grep -r 'class.*AGI' /root/arifOS/arifosmcp/ \| wc -l` |
| SIGNAL :18084 | External Signal Ingestor | webhook receiver, kabarkan routing, quiet hours | `curl :18084/health \| jq .endpoints` |
| FRAME :18085 | Baseline Drift Auditor | 10 organs baseline, chambers (probe, compare, trend) | `curl :18085/health \| jq .baseline_organs` |
| FLAME :18901 | Advisory Inference Mesh | RM0 free loop, ADVISORY authority | `curl :18901/health \| jq .authority` |

### Quick probe recipe for any organ

```bash
# Single organ probe (10 seconds)
SID=$(curl -si http://127.0.0.1:<PORT>/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2025-11-25' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  2>/dev/null | grep -i 'mcp-session-id' | awk '{print $2}' | tr -d '\r')

if [ -n "$SID" ]; then
  curl -s http://127.0.0.1:<PORT>/mcp -X POST \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -H "Mcp-Session-Id: $SID" \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
    2>/dev/null | python3 -c "import sys,json; t=json.load(sys.stdin); print(len(t.get('result',{}).get('tools',[])))"
fi
```

### What breaks if each entity disappears

| Entity | What breaks | What survives | Truly irreplaceable |
|---|---|---|---|
| AAA | A2A discovery, 38-agent registry | All agents bind direct to :8088 | Directory lookup is the only thing it uniquely provides |
| arifOS | Floor enforcement, 888_HOLD, gate pipeline | A-FORGE tools work independently | Only thing that can say "HOLD" — the safety brake |
| A-FORGE | All mutation, APA bridges, deploy path | arifOS, GEOX, WEALTH, WELL function | Mutate authority is unique to A-FORGE |
| FED | Constitutional tier enforcement, cost cascade, provider allowlist | Agents can call providers directly (uncontrolled) | Tier-based LLM allocation under constraints |
| GEOX | Earth evidence | No earth data flows | The only source of petrophysics/seismic data |
| WEALTH | Capital NPV/EMV risk | Capital calculations don't happen | Quantitative finance under governance |
| WELL | Vitality signals | No human-readiness assessment | Biometrics for decision quality |
| arifFlow | Metabolic pulse (FQ), invariant enforcement | All other organs still execute | Real-time health monitoring — the heartbeat |
| VAULT999 | Immutable truth, hash chain, lineage | Nothing trusts itself | The only thing that can't be lied about |
| APEX | G=(APEX)^(1/4) safety brake | Other safety checks exist independently | Imbalance detection (catches G=0 when other metrics pass) |
| i-ARIF | Constitutional training data for new models | Existing agents already trained | Seed of constitutional knowledge — portable |

### Evidence paths (when to update this file)

When a new organ is added to the federation, add it to this registry. When a port or tool count changes, update the probe commands. This file is the federation's identity card — keep it honest.
