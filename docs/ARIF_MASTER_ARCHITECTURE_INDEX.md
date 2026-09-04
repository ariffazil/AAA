# arifOS Federation — Master Architecture Index
> **Generated:** 2026-08-10 04:02 MYT | **For:** Arif (F13 SOVEREIGN)
> **Usage:** Paste into any session to instantly load full system context.

---

## 1. GIT REPOS (Production)

| # | Repo | Path | Remote | Role |
|---|------|------|--------|------|
| 1 | **arifOS** | `/root/arifOS` | `ariffazil/arifOS` | CORE KERNEL — :8088, constitutional floors F1-F13 |
| 2 | **A-FORGE** | `/root/A-FORGE` | `ariffazil/A-FORGE` | CORE EXECUTE — :7071/:7072, mutation actuator |
| 3 | **AAA** | `/root/AAA` | `ariffazil/AAA` | CORE COCKPIT — :3001, control plane + A2A gateway |
| 4 | **GEOX** | `/root/GEOX` | `ariffazil/GEOX` | CORE EARTH — :8081, earth intelligence |
| 5 | **WEALTH** | `/root/WEALTH` | `ariffazil/WEALTH` | CORE CAPITAL — :18082, capital intelligence |
| 6 | **WELL** | `/root/WELL` | `ariffazil/WELL` | CORE VITALITY — :18083, human readiness |
| 7 | **HERMES** | `/root/HERMES` | `ariffazil/HERMES` | EDGE — :18089/:18789, Telegram bridge + cron |
| 8 | **arifFlow** | `/root/arifFlow` | `ariffazil/arifFLOW` | METABOLISM — :7073, receipt metabolism + FQ pulse |
| 9 | **FRAME** | `/root/FRAME` | `ariffazil/FRAME` | Design framework |
| 10 | **arif-fazil.com** | `/root/arif-fazil.com` | `ariffazil/arif-fazil.com` | PUBLIC — Caddy + Cloudflare |
| 11 | **ariffazil** | `/root/ariffazil` | `ariffazil/ariffazil` | GitHub org homepage |
| 12 | **web-canon** | `/root/web-canon` | `ariffazil/web-canon` | Web canonical |
| 13 | **arifOS-model-registry** | `/root/arifOS-model-registry` | `ariffazil/arifOS-model-registry` | Model registry |

**Workspace SOT:** `/root/AAA/federation/workspace.yaml`

---

## 2. CONSTITUTIONAL FLOORS (F1–F13)

**Source:** `/root/arifOS/GENESIS/FLOOR_TABLE.json` + `/root/arifOS/GENESIS/000_KERNEL_CANON.md`

| Floor | Name | Type | Rule |
|-------|------|------|------|
| F1 | AMANAH | HARD | Reversible-first. Irreversible → 888_HOLD |
| F2 | TRUTH | HARD | P(truth) ≥ 0.99. OBS/DER/INT/SPEC labels mandatory |
| F3 | TRI-WITNESS | DERIVED | Human × AI × Earth × Verifier ≥ 0.75 (Nash) |
| F4 | CLARITY | HARD | ΔS ≤ 0 — every output reduces entropy |
| F5 | PEACE² | SOFT | Non-destructive power |
| F6 | EMPATHY ⇄ MARUAH | SOFT | Dual-registry lossless bridge |
| F7 | HUMILITY | HARD | Ω₀ ∈ [0.03, 0.05]. Cap ≤ 0.97 |
| F8 | GENIUS | DERIVED | G = (A×P×E×X)^(1/4) ≥ 0.80 |
| F9 | ANTIHANTU | HARD | No deception. C_dark < 0.30 |
| F10 | ONTOLOGY | HARD | AI-only ontology. Soul = VOID |
| F11 | AUDITABILITY | HARD | Every decision logged, attributable |
| F12 | RESILIENCE | HARD | Injection defense. Risk < 0.85 |
| F13 | SOVEREIGN | HARD | Human veto FINAL. Arif owns. |

---

## 3. INVARIANTS & PROTOCOLS

### Core Invariants

| File | Path | What |
|------|------|------|
| **7 Physics + 7 Zen** | `/root/AAA/docs/INVARIANTS.md` | AAA-scope agent behavior |
| **Kernel Invariants** | `/root/AAA/docs/KERNEL_INVARIANTS.md` | MCP-level constitutional physics |
| **Genesis Invariants** | `/root/arifOS/GENESIS/INVARIANTS.md` | 7 MCP-level physics |
| **Sovereign Invariant** | `/root/AAA/docs/eureka/SOVEREIGN_INVARIANT.md` | F13 protection |
| **Skill Invariant Schema** | `/root/AAA/docs/SKILL-INVARIANT-SCHEMA.md` | Skill compliance gates |

### Key Governance Doctrine

| Document | Path | Purpose |
|----------|------|---------|
| **Zen Execution Doctrine** | `/root/AAA/governance/ZEN_EXECUTION_DOCTRINE.md` | **#1 execution SOT** — load at boot |
| **Gödel Lock Strange Loop** | `/root/AAA/governance/GODEL_LOCK_STRANGE_LOOP.md` | Doer ≠ Judge separation |
| **Double Helix ECHO↔SCAR** | `/root/AAA/governance/DOUBLE_HELIX_ECHO_SCAR.md` | Learning + human strand |
| **HERMES DNA** | `/root/AAA/governance/HERMES_DNA.md` | MAP·ATLAS·ECHO topology |
| **HERMES Cognitive Institution** | `/root/AAA/governance/HERMES_COGNITIVE_INSTITUTION.md` | Anti-chaos institution |
| **Human Memory Doctrine** | `/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md` | H1-H6 stratification |
| **HITL Removal Audit** | `/root/AAA/governance/HITL_REMOVAL_AUDIT_2026-08-09.md` | Authorization vs Cognitive HITL |
| **QQQ Protocol** | `/root/AAA/governance/QQQ_RECOMMENDATION_PROTOCOL.md` | 5-paths × BR/REV/Time/Conf/PA |
| **Agency Levels** | `/root/AAA/governance/AGENCY_LEVELS.md` | Seven-agent-contract + L0-L6 |
| **Entropic Compression** | `/root/AAA/governance/INSTITUTIONAL_COMPRESSION.md` | Compress ambiguity |
| **Institutional Paradoxes** | `/root/AAA/governance/AGENTIC_INSTITUTION_PARADOXES.md` | MAP·ATLAS·ECHO metrics |
| **AAA Tool Rights Policy** | `/root/AAA/governance/AAA_TOOL_RIGHTS_POLICY.md` | Tool authority mapping |
| **Evidence Routing Protocol** | `/root/AAA/governance/EVIDENCE_ROUTING_PROTOCOL.md` | OBS/DER/INT/SPEC flow |
| **Epistemic Collapse Diagnostic** | `/root/AAA/governance/EPISTEMIC_COLLAPSE_DIAGNOSTIC.md` | Detection + recovery |
| **Membrane Contract** | `/root/AAA/docs/MEMBRANE_CONTRACT.md` | Constitutional membrane |

### Architecture Decision Records (ADRs)

| ADR | Path |
|-----|------|
| ADR-001 Topology | `/root/AAA/governance/adr/ADR-001-AAA-PHASE1-TOPOLOGY.md` |
| ADR-002 Transport | `/root/AAA/governance/adr/ADR-002-ARIFOS-TRANSPORT.md` |
| ADR-010 Telegram Visibility | `/root/AAA/governance/adr/ADR-010-AAA-TELEGRAM-VISIBILITY.md` |
| ADR-011 Telegram Messaging | `/root/AAA/governance/adr/ADR-011-AAA-TELEGRAM-MESSAGING-PROTOCOL.md` |
| ADR-012 A2A Mesh | `/root/AAA/governance/adr/ADR-012-A2A-MESH-GOVERNANCE.md` |
| ADR-013 Federation Phase 2 | `/root/AAA/governance/adr/ADR-013-FEDERATION-PHASE2-BLUEPRINT.md` |
| ADR-014 MCP Concurrency | `/root/AAA/governance/adr/ADR-014-MCP-CONCURRENCY-PHOENIX-73C.md` |
| ADR-015 Federation Legibility | `/root/AAA/governance/adr/ADR-015-federation-legibility-doctrine.md` |
| ADR-016 Progressive Disclosure | `/root/AAA/governance/adr/ADR-016-PROGRESSIVE-DISCLOSURE.md` |

### Constitutional Laws

| Law | Path |
|-----|------|
| LC_ARCHITECT | `/root/AAA/governance/laws/LC_ARCHITECT.md` |
| LC_ARCHITECTURE | `/root/AAA/governance/laws/LC_ARCHITECTURE.md` |
| LC_COMPRESSED | `/root/AAA/governance/laws/LC_COMPRESSED.md` |
| LC_DISCOVERY | `/root/AAA/governance/laws/LC_DISCOVERY.md` |
| LC_MONEY | `/root/AAA/governance/laws/LC_MONEY.md` |
| LC_OUTSOURCE | `/root/AAA/governance/laws/LC_OUTSOURCE.md` |
| LC_RECOVERY | `/root/AAA/governance/laws/LC_RECOVERY.md` |
| LC_SUBSTRATE | `/root/AAA/governance/laws/LC_SUBSTRATE.md` |
| LC_TOOLS | `/root/AAA/governance/laws/LC_TOOLS.md` |
| LC_TRUTH | `/root/AAA/governance/laws/LC_TRUTH.md` |

---

## 4. GENESIS DOCUMENTS (arifOS Kernel Canon)

**Dir:** `/root/arifOS/GENESIS/`

| # | Title | Focus |
|---|-------|-------|
| 000 | KERNEL_CANON.md | **Root canon** — constitutional kernel |
| 001 | MUHAMMAD_MODE_ASI | ASI mode |
| 002 | SOVEREIGN_SOLITUDE | F13 isolation |
| 003 | ANDERSEN_CALHOUN_FABLE | Parable |
| 004 | OPUS_NAMING_PARADOX | Naming |
| 005 | POST_AGI_ECONOMICS | Post-AGI economics |
| 005b | POST_AGI_ECONOMICS_KERNEL | Kernel-level economics |
| 006 | PETRONAS_PARADOX | PETRONAS energy paradox |
| 007 | AIRLOCK_CONSERVATION_LAW | Airlock physics |
| 008 | NARRATIVE_TENSION_KERNEL | Narrative tension |
| 009 | MCP_BOUNDARY | MCP edge definition |
| 010 | ADAT_AGENTIC | Agentic custom |
| 011 | FEDERATION_AGI_SUBSTRATE | Federation as AGI substrate |
| 012 | CIVILIZATIONAL_INTENT | Civilizational purpose |
| 013 | APEX_FALSIFICATION_PROTOCOL | APEX testing |
| 014 | APEX_VALIDATION_REPORT | APEX validation |
| 015 | APEX_THEORY_KERNEL_VOICE | APEX voice |
| 016 | ILMU_AKAL_HIKMAH | Cognitive cosmology |
| 017 | MCP_AFFORDANCE_MEMBRANE | MCP affordance |
| 018 | REALITY_ENGINEERING_DOCTRINE | Reality engineering |
| 019 | REALITY_ENGINEERING_PROTOCOL | RE protocol |
| 020 | ARIFOS_TRUTH_RECEIPT_DOCTRINE | Truth receipts |
| 021 | HUMANENTROPY_LAW | Human entropy |
| 022 | EUREKA_ZEN_MARGIN | Eureka margin |
| 023 | MCP_EPISTEMIC_EXTENSION | Epistemic MCP |
| 024 | PETRONAS_SOVEREIGN_ENERGY | Petronas intelligence |
| 030 | ART_VS_KERNEL | Art vs kernel |
| 040 | ACT_PLAYBOOK | ACT execution |
| 041 | APEX_STACK | APEX stack |
| 045 | THREE_LAYER_SEPARATION | 3-layer separation |
| 046 | CONSTITUTIONAL_VSM | Viable System Model |
| 047 | S2_COORDINATION_PROTOCOL | S2 coordination |
| 048 | QUBIT_RUNTIME_DOCTRINE | Qubit runtime |
| 049 | THERMODYNAMIC_ENERGY_GRADIENT | Thermo gradient |
| 050 | APPROACH_A_ROUTING + SHADOW_INTEGRATION | Routing + shadow |
| 051 | INDIVIDUATION_AS_AIM | Individuation |
| 052 | INVARIANTS_OF_AI_AUTHORITY | AI authority invariants |
| 053 | METABOLIC_SYNTHESIS_PROTOCOL | Metabolic synthesis |
| 054 | DELTA_OMEGA_PSI | Multimodal cognition |
| 055 | MULTIMODAL_KERNEL_HARDENING | Kernel hardening |
| 056 | TRI_WITNESS_SPECIFICATION | Tri-witness spec |
| 057 | EUREKA_DISTILLATION | Eureka distillation |
| 058 | THREE_CLOSURES | Three closures |
| 059 | FQ_SEAL_GAUGE | FQ seal gauge |
| 060 | FEDERATION_INTENT_GRAMMAR | Intent grammar |
| 061 | AUTONOMOUS_GOVERNED_EXECUTION | Autonomous execution |

**Also:** `FLOOR_TABLE.json`, `INVARIANTS.md`, `TRINITY_HOST_LAW.md`, `LAYER_SEPARATION_DOCTRINE.md`, `AUTHORITY_LAYER_DOCTRINE.md`, `AUTOPILOT_DOCTRINE.md`, `VAULT999_BACKREF_DEDUP_SPEC.md`

---

## 5. AGENT CARDS (3-Layer Identity)

**Dir:** `/root/AAA/agent-cards/`

### 3-Lane Identity (§3 spec)
| Lane | Path | Card |
|------|------|------|
| 333-AGI | `identity/333-AGI/` | `agent-card.json` + `skills.json` |
| 555-ASI | `identity/555-ASI/` | `agent-card.json` + `skills.json` |
| 888-APEX | `identity/888-APEX/` | `agent-card.json` + `skills.json` |

### Organ Cards
| Organ | Path |
|-------|------|
| A-FORGE | `organs/aforge/agent-card.json` |
| GEOX | `organs/geox/agent-card.json` |
| WEALTH | `organs/wealth/agent-card.json` |
| WELL | `organs/well/agent-card.json` |

### Pillar Cards
| Pillar | Path |
|--------|------|
| AAA Gateway | `pillars/aaa-gateway/agent-card.json` + `agent-card-extended.json` |
| arifOS | `pillars/arifos/agent-card.json` |
| Sovereign | `pillars/sovereign/agent-card.json` |

### Extension Cards
| Extension | Path |
|-----------|------|
| Hermes | `extensions/hermes/skills.json` |
| MakcikGPT | `extensions/makcikgpt/agent-card.json` |
| OpenClaw | `functions/openclaw/agent-card.json` |

### Seals
- `SOVEREIGN_IDENTITY_SEAL.json`
- `META_MESA_SEAL.json`
- `SKILL_MANIFEST.json`

---

## 6. AAA INSTRUCTION FRAGMENTS (SOT — edit here)

**Dir:** `/root/AAA/instructions/` → rendered by `/root/scripts/render-agents.sh` → `/root/AGENTS.md`

| Fragment | Focus |
|----------|-------|
| `base.md` | Base constitution topology |
| `constitution.md` | F1-F13 floors |
| `topology.md` | Federation topology |
| `autonomy.md` | T0-T3 autonomy tiers |
| `security.md` | Secrets + memory landscape |
| `build.md` | Build/test/deploy conventions |
| `zen.md` | Zen doctrine |
| `pointers.md` | Canonical file pointers |
| `agentic-architecture.md` | Meta-Mesa doctrine |
| `reality-first.md` | Reality-first 8 rules |
| `human-memory.md` | H-axis memory doctrine |
| `emd-architecture.md` | EMD reflex arc |

---

## 7. AAA PROMPTS (Boot + Seal)

| Prompt | Path | When |
|--------|------|------|
| **INIT.md** | `/root/AAA/prompts/INIT.md` | Boot (Trinity-33 · RSI) |
| **INIT_HERMES** | `/root/AAA/prompts/INIT_HERMES.md` | Hermes boot |
| **INIT_HUMAN** | `/root/AAA/prompts/INIT_HUMAN.md` | Human session |
| **INIT_OPENCLAW** | `/root/AAA/prompts/INIT_OPENCLAW.md` | OpenClaw boot |
| **INIT-ZEN** | `/root/AAA/prompts/INIT-ZEN.md` | Zen alignment |
| **SEAL.md** | `/root/AAA/prompts/SEAL.md` | Exit (Lane A/B) |
| **AAA-ZEN-ALIGNMENT** | `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` | Federation-wide Zen |
| **APEX_JUDGE_SUBAGENT** | `/root/AAA/prompts/APEX_JUDGE_SUBAGENT.md` | Isolated judgment |
| **ADVERSARIAL_BOOT** | `/root/AAA/prompts/ADVERSARIAL_BOOT.md` | Adversarial testing |
| **FORGE_HERMES** | `/root/AAA/prompts/FORGE_HERMES.md` | Hermes forge |
| **FORGE_OPENCLAW** | `/root/AAA/prompts/FORGE_OPENCLAW.md` | OpenClaw forge |

---

## 8. FEDERATION SOT FILES

| File | Path | Role |
|------|------|------|
| **organs.yaml** | `/root/AAA/federation/organs.yaml` | Machine SOT — ports, roles, ceilings |
| **workspace.yaml** | `/root/AAA/federation/workspace.yaml` | Workspace topology |
| **person-register.json** | `/root/AAA/federation/person-register.json` | Human identity registry |
| **seats.yaml** | `/root/AAA/federation/seats.yaml` | Provider seat config |
| **repos.yaml** | `/root/AAA/federation/repos.yaml` | Repo registry |
| **STATE.yaml** | `/root/AAA/federation/STATE.yaml` | Federation state |
| **mcp-catalog.yaml** | `/root/AAA/federation/mcp-catalog.yaml` | MCP tool catalog |
| **call_map.yaml** | `/root/AAA/federation/call_map.yaml` | Cross-organ call map |
| **federation-manifest.yaml** | `/root/AAA/federation/federation-manifest.yaml` | Manifest |

---

## 9. SKILLS REGISTRY

| File | Path |
|------|------|
| **FEDERATED_SKILLS_REGISTRY_V3** | `/root/AAA/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` |
| **SKILL_ALIAS_TABLE** | `/root/AAA/skills/SKILL_ALIAS_TABLE.json` |
| **MASTER_SKILL_TO_AGENT_MAP** | `/root/AAA/skills/MASTER_SKILL_TO_AGENT_MAP.json` |
| **SKILL_TRUST_STATUS** | `/root/AAA/skills/SKILL_TRUST_STATUS.json` |

---

## 10. ORGAN LEGAL DOCS

| Document | Path |
|----------|------|
| **AGENT-CHARTER** | `/root/AAA/governance/AGENT-CHARTER.md` |
| **FEDERATION_CONTRACT** | `/root/AAA/governance/FEDERATION_CONTRACT.md` |
| **REPO_AUTHORITY** | `/root/AAA/governance/REPO_AUTHORITY.md` |
| **ADAT_AGENTIC** | `/root/AAA/governance/ADAT_AGENTIC.md` |
| **TWO_THRESHOLD_DOCTRINE** | `/root/AAA/governance/TWO_THRESHOLD_DOCTRINE.md` |
| **KILL_LIST** | `/root/AAA/governance/KILL_LIST.md` |
| **ZERO_DAY_SENTINEL** | `/root/AAA/governance/ZERO_DAY_SENTINEL_ARCHITECTURE.md` |

---

## 11. BOOT SEQUENCE (30-second)

```bash
1. source /root/.secrets/kunci-mas.env
2. cat /root/AGENTS.md + /root/CLAUDE.md
3. MCP '/init' prompt (arifos-kernel · 2026-09-04 supersede)
4. cat /root/.local/share/arifos/carry_forward.json
5. make health  # or: /root/scripts/doctor.sh
6. for d in /root/{arifOS,A-FORGE,AAA,GEOX,WEALTH,WELL}; do git -C "$d" status -s; done
7. cat /root/AAA/docs/deprecation-registry.json | jq .
```

---

## 12. HEALTH PROBE

```bash
for p in 8088 7071 7072 7073 3001 8081 18082 18083; do
  curl -sf http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ $p" || echo "❌ $p"
done
```

---

## 13. QUICK PROMPT TEMPLATES

### "Show me the full architecture"
```
Load /root/AGENTS.md. Load /root/AAA/federation/organs.yaml.
List all organs with ports, roles, authority ceilings.
List all public MCP doors.
```

### "What's the governance structure?"
```
Load /root/AAA/governance/ZEN_EXECUTION_DOCTRINE.md
Load /root/AAA/governance/GODEL_LOCK_STRANGE_LOOP.md
Load /root/AAA/governance/AGENCY_LEVELS.md
Load /root/AAA/governance/QQQ_RECOMMENDATION_PROTOCOL.md
```

### "What are all the invariants?"
```
Load /root/AAA/docs/INVARIANTS.md
Load /root/AAA/docs/KERNEL_INVARIANTS.md
Load /root/arifOS/GENESIS/INVARIANTS.md
Load /root/AAA/docs/SOUL.md if exists
```

### "Show me the EUREKA loop"
```
Load /root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md
Load /root/AAA/governance/DOUBLE_HELIX_ECHO_SCAR.md
Load /root/AAA/governance/INSTITUTIONAL_COMPRESSION.md
```

### "Show me the EMD architecture"
```
Load /root/AAA/instructions/emd-architecture.md
OpenClaw=SENSE · Hermes=COORDINATE · OpenCode=EXECUTE
```

### "Full agent identity"
```
Load /root/AAA/agent-cards/identity/333-AGI/agent-card.json
Load /root/AAA/agent-cards/identity/555-ASI/agent-card.json
Load /root/AAA/agent-cards/identity/888-APEX/agent-card.json
Load /root/AAA/agent-cards/SOVEREIGN_IDENTITY_SEAL.json
```

---

## 14. DOCUMENT COUNT

| Category | Count |
|----------|-------|
| Git repos (production) | 13 |
| Genesis docs | 50+ |
| Governance docs | 90+ |
| AAA docs | 200+ |
| AAA instruction fragments | 12 |
| Agent cards | 30+ |
| Federation YAML configs | 15+ |
| Skills registry entries | 95 logical (V3) |
| ADRs | 9 |
| Constitutional laws | 10 |

---

*DITEMPA BUKAN DIBERI ⚒️ | This file is a pointer cheat sheet, not doctrine.*
*For constitutional truth → `/root/arifOS/GENESIS/000_KERNEL_CANON.md`*
*For operational truth → `/root/AAA/docs/ORGAN.md`*
*For machine truth → `/root/AAA/federation/organs.yaml`*
