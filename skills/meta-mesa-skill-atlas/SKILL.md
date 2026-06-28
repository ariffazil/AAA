---
name: meta-mesa-skill-atlas
description: Unified skill inventory, gap detection, and cross-cutting orchestration for all 35 arifOS federation skills. The mesa above the terrain — see the whole, find the missing, route the right skill. Load when starting a new task, auditing skill health, onboarding a new organ, or when you don't know which skill to load.
version: 1.0.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: low
floor_scope: [F2, F4, F7, F9]
autonomy_tier: T1
tags: [meta, skill-atlas, gap-detection, routing, federation, inventory]
forged: 2026-06-28
sources:
  - All 7 constitutional stage skills (000/010/111/333/666/888/999)
  - All 28 domain skills
  - AGENTS.md federation organ index
  - TOOLREGISTRY.json
  - TOOLS.md agent tool surface
---

# META-MESA — Skill Atlas & Gap Detection

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
> **The mesa above the terrain. See the whole. Find the missing. Route the right.**

## What This Skill Is

This is the **meta-skill** — a skill about skills. It provides:

1. **Inventory** — canonical list of all 35 skills with domain, organ, and coverage depth
2. **Gap detection** — what's missing, what's thin, what's referenced but doesn't exist
3. **Routing** — given a task, which skill(s) should be loaded
4. **Health scoring** — skill freshness, collision risk, coverage metrics
5. **Cross-cutting concerns** — the gaps between skills where things fall through

It does NOT execute, judge, or seal. It classifies, routes, and illuminates.

---

## §1. THE SEVEN STAGES (Constitutional Pipeline)

The golden path. Every governed action flows through these stages.

| # | Skill | Stage | Role | Risk | Key Output |
|---|-------|-------|------|------|------------|
| 000 | `000-init-intent-classify` | 1 | Entry gate | HIGH | loop_class, required_organs, blast_radius, next_lawful_call |
| 111 | `111-sense-evidence-observe` | 2 | Evidence binding | HIGH | evidence_table, epistemic_tags, contradiction_scan, gaps |
| 333 | `333-mind-plan-generate` | 3 | Plan generation | HIGH | 3+ candidate_plans, falsification_checks, DAG |
| 666 | `666-heart-critique-stress` | 4 | Consequence scan | CRITICAL | risk_register, dignity_check, posture_recommendation |
| 888 | `888-judge-verdict-render` | 5 | Verdict | CRITICAL | SEAL / SABAR / HOLD / VOID |
| 010 | `010-forge-execute-warrant` | 6 | Execution | CRITICAL | execution_receipt, rollback_path |
| 999 | `999-vault-seal-immutable` | 7 | Memory | HIGH | VAULT999 record, lineage, lessons |

### Stage Gaps (What Falls Between)

| Gap | Between | Impact | Mitigation |
|-----|---------|--------|------------|
| **No priority queue** | 000 → 111 | Multiple intents compete, no ordering | Manual triage; future: session-state priority field |
| **No evidence freshness decay** | 111 | Evidence ages but no re-observation trigger | Use `arif_observe` freshness_weight on recall |
| **No cost estimation** | 333 | Plans don't estimate compute/API/human cost | Add cost column to plan steps manually |
| **No plan revision loop** | 666 → 333 | SABAR/HOLD doesn't auto-revise plan | 888 judge can route back to 333 |
| **No temporal cascade modeling** | 666 | Consequences are static snapshots | Use `wealth_monte_carlo_simulate` for temporal |
| **No verdict expiration** | 888 → 010 | Old SEAL could authorize stale execution | Check seal timestamp at 010 |
| **No partial execution handling** | 010 | Step 3/5 failure = undefined state | Define per-plan partial-rollback strategy |
| **No vault retrieval** | 999 | Write-only from skill perspective | Use `arif_vault_query` for read path |

---

## §2. DOMAIN SKILLS BY ORGAN (28 Skills)

### GEOX — Earth Intelligence (7 skills, THICK coverage)

| Skill | Purpose |
|-------|---------|
| `geox-constitution` | Constitutional floors, epistemic style, HOLD triggers |
| `geox-claim-grammar` | Claim YAML schema, multi-hypothesis mandate |
| `geox-earth-evidence` | Evidence discipline, artifact refs, handoff protocol |
| `geox-epistemic-ladder` | 7-rung ladder, iron rule (lower beats higher) |
| `geox-petrophysics-bounds` | Vsh, porosity, Sw, AI, permeability QC |
| `geox-contradiction-engine` | 7 contradiction types, multi-hypothesis scanner |
| `geox-redteam-hantu` | Anti-hallucination, F9 enforcement |

### WEALTH — Capital Intelligence (4 skills, GOOD coverage)

| Skill | Purpose |
|-------|---------|
| `wealth-capital-thermodynamics` | 13 primitives grounding all WEALTH computation |
| `wealth-capital-reasoning` | POS, EMV, valuation, governed consequence |
| `wealth-collapse-signature` | 7 institutional failure patterns |
| `wealth-law-anthropology` | Malaysian law: faraid, KTN, MA63, Syariah, adat |

### Infrastructure (7 skills)

| Skill | Domain | Purpose |
|-------|--------|---------|
| `mcp-mastery` | MCP | Trust surface, protocol, tool forging, transport |
| `mcp-apps-builder` | MCP | SEP-1865 interactive HTML UI in conversations |
| `webmcp-site-builder` | MCP | WebMCP sites, W3C origin trial |
| `github-operations` | Git | Issue triage, PR review, CI diagnostics |
| `federation-observability` | Ops | OTEL, Prometheus, Grafana, LGTM |
| `hf-mastery` | ML | Governed HuggingFace: hub, datasets, inference, fine-tune |
| `iron-shell-render` | Web | Three-layer site architecture |

### Forge & Agent (3 skills)

| Skill | Purpose |
|-------|---------|
| `aforge-execution` | Build, deploy, verify. Gated by SEAL. |
| `agentic-builder` | Build governed agents: identity, skills, tools |
| `skill-creator` | Bootstrap, design, package new skills |

### General / Meta (3 skills)

| Skill | Purpose |
|-------|---------|
| `apex-theory` | Physics + math + symbolic code + meaning |
| `entropy-thermo-zen` | Thermodynamic entropy management (TZQ) |
| `symbolic-order-trust-architecture` | Structural trust mapping |

### Symbolic Order (2 of 5 planned)

| Skill | Purpose |
|-------|---------|
| `symbolic-order-collective-bias` | Detect population-level bias via naming game |
| `symbolic-order-trust-architecture` | Trust symmetry violations |

### WELL — Human Readiness (1 skill, THIN)

| Skill | Purpose |
|-------|---------|
| `well-substrate-readiness` | Vitality, fatigue, dignity. Reflect only. |

### AAA — Control Plane (1 skill, THIN)

| Skill | Purpose |
|-------|---------|
| `aaa-cockpit` | Agent registry, session cockpit, A2A gateway |

### A2A / Federation (1 skill)

| Skill | Purpose |
|-------|---------|
| `a2a-federation-builder` | Agent Cards, JSON-RPC /a2a, federation directory |

---

## §3. GAP REGISTER — Missing Skills

### 3A. Referenced But Do Not Exist (Phantom Skills)

| Missing Skill | Referenced In | Function |
|--------------|--------------|----------|
| `070-lock-humility-godel` | mcp-mastery, geox-claim-grammar, geox-constitution, wealth-collapse-signature, wealth-capital-thermodynamics, hf-mastery | Final epistemic gate before SEAL-grade claims |
| `034-dag-plan-orchestrate` | wealth-collapse-signature, wealth-capital-thermodynamics | Multi-step execution graph for cross-organ work |
| `444-route-organ-direct` | geox-earth-evidence, wealth-capital-reasoning, aaa-cockpit, well-substrate-readiness, a2a-federation-builder | Organ routing and direct addressing |
| `950-seal-vault-audit` | a2a-federation-builder | Vault999 seal verification and chain audit |
| `symbolic-order-solidarity-monitor` | symbolic-order-collective-bias §11 | Calhoun Phase C population-level detection |
| `symbolic-order-mythic-attestor` | symbolic-order-trust-architecture §8 | Sacred domain violation detection |
| `symbolic-order-layer-governance` | symbolic-order-trust-architecture §8 | L1/L2/L3 hierarchy enforcement |
| `geox-basin-interpreter` | wealth-capital-thermodynamics | Upstream O&G basin interpretation for Petronas |

### 3B. Entirely Missing Domains (No Skill Exists)

| Missing Domain | Organ | Impact | Priority |
|----------------|-------|--------|----------|
| **arifOS kernel operations** | arifOS | No domain skill for session lifecycle, world model, kernel internals | P2 |
| **VAULT999 deep operations** | arifOS | No receipt/chain/hash management skill | P3 |
| **HERMES/ASI Telegram agent** | 555-ASI | No skill despite SOUL.md existing at /root/.hermes/SOUL.md | P3 |
| **Docker/container management** | Infrastructure | VPS has 17 hostinger tools, no container skill | P4 |
| **DNS/Cloudflare management** | Infrastructure | No skill for DNS, Workers, R2, Pages | P4 |
| **Database operations** | All organs | No PostgreSQL/Supabase schema management skill | P4 |
| **WEALTH stock analysis deep** | WEALTH | 12 modes of wealth_stock_analysis, no dedicated skill | P3 |
| **WEALTH personal finance** | WEALTH | D1 personal scope, no dedicated skill | P4 |

### 3C. Thinly Covered Organs

| Organ | Current Depth | What's Missing |
|-------|--------------|---------------|
| **WELL** | 1 skill | Sleep science, fatigue modeling, cognitive depletion, metabolic flux, dignity enforcement patterns |
| **AAA** | 1 skill | A2A mesh routing details, cockpit React dashboard, deliberation integration, agent lifecycle |
| **Symbolic Order** | 2 of 5 | solidarity-monitor, mythic-attestor, layer-governance — cluster is incomplete |

---

## §4. ROUTING TABLE — Which Skill For Which Task

Given a natural-language intent, this table routes to the correct skill.

| Intent Pattern | Skill to Load | Why |
|---------------|---------------|-----|
| "plan this" / "govern this" / "classify intent" | `000-init-intent-classify` | Stage 1 entry gate |
| "observe" / "gather evidence" / "what do we know" | `111-sense-evidence-observe` | Stage 2 evidence binding |
| "make a plan" / "generate options" / "how should we" | `333-mind-plan-generate` | Stage 3 planning |
| "stress test" / "what could go wrong" / "critique" | `666-heart-critique-stress` | Stage 4 consequence scan |
| "judge" / "render verdict" / "is this lawful" | `888-judge-verdict-render` | Stage 5 verdict |
| "execute" / "forge" / "build this" | `010-forge-execute-warrant` | Stage 6 execution |
| "seal" / "record" / "vault this" | `999-vault-seal-immutable` | Stage 7 memory |
| "seismic" / "well log" / "petrophysics" / "basin" | `geox-constitution` + domain geox-* | Earth intelligence gate |
| "NPV" / "IRR" / "capital" / "investment" | `wealth-capital-thermodynamics` | Capital primitives first |
| "collapse" / "institutional failure" / "Enron" | `wealth-collapse-signature` | Failure forensics |
| "Malaysian law" / "faraid" / "pusaka" / "MA63" | `wealth-law-anthropology` | Legal domain |
| "sleep" / "fatigue" / "vitality" / "dignity" | `well-substrate-readiness` | Human readiness |
| "build MCP tool" / "forge tool" / "MCP server" | `mcp-mastery` | MCP infrastructure |
| "build a website" / "iron shell" / "static site" | `iron-shell-render` | Site architecture |
| "GitHub PR" / "CI broken" / "issue triage" | `github-operations` | Git operations |
| "build an agent" / "new agent identity" | `agentic-builder` | Agent construction |
| "create a skill" / "new skill" | `skill-creator` | Skill creation |
| "entropy" / "cleanup" / "system chaos" | `entropy-thermo-zen` | TZQ framework |
| "APEX" / "consciousness" / "physics of AI" | `apex-theory` | Theoretical framework |
| "A2A" / "agent communication" / "federation mesh" | `a2a-federation-builder` | Inter-agent surface |
| "bias" / "collective behavior" / "population" | `symbolic-order-collective-bias` | Social-symbolic |
| "trust" / "trust architecture" / "trust violation" | `symbolic-order-trust-architecture` | Trust mapping |
| "observability" / "tracing" / "metrics" | `federation-observability` | LGTM stack |
| "HuggingFace" / "model hub" / "fine-tune" | `hf-mastery` | ML governance |
| "what skill should I load" / "skill gap" / "skill audit" | **THIS SKILL** (meta-mesa) | Meta-routing |

---

## §5. HEALTH SCORING — Skill Freshness

Run periodically to detect stale skills.

### Per-Skill Health Check

```python
skill_health = {
    "name": str,           # skill name
    "version": str,        # from frontmatter
    "forged_date": str,    # from frontmatter
    "days_since_forge": int,
    "references_count": int,   # how many other skills reference it
    "phantom_refs": int,       # references to skills that don't exist
    "has_prompt": bool,       # prompts/ directory exists
    "has_test": bool,         # test coverage exists
    "organ_coverage": float,  # 0.0-1.0 depth for its organ
}
```

### Federation Skill Health Summary

```python
federation_skill_health = {
    "total_skills": 35,           # 7 stage + 28 domain
    "phantom_skills": 8,          # referenced but don't exist
    "missing_domains": 8,         # entirely uncovered domains
    "thin_organs": ["WELL", "AAA", "SYMBOLIC"],
    "thick_organs": ["GEOX"],
    "collision_risk": float,      # skill overlap score (0.0 ideal)
    "stale_skills": int,          # > 30 days since last forge
    "coverage_score": float,      # 0.0-1.0 overall
}
```

### Stale Threshold

| Days Since Forge | Status | Action |
|-----------------|--------|--------|
| 0-7 | FRESH | No action |
| 8-14 | CURRENT | Review on next session |
| 15-30 | AGING | Verify references still valid |
| 30+ | STALE | Audit needed, consider archive or refresh |

---

## §6. CROSS-CUTTING CONCERNS — The Gaps Between Skills

These are capabilities that NO single skill covers but the federation needs.

### 6.1 Evidence Lifecycle (covers 111, but not full lifecycle)

| Phase | Covered By | Gap |
|-------|-----------|-----|
| Collection | 111-sense-evidence | ✅ |
| Tagging | 111-sense-evidence | ✅ |
| Contradiction detection | 111 + geox-contradiction-engine | ✅ |
| Freshness decay tracking | **NONE** | ❌ No skill tracks evidence aging |
| Cross-session correlation | **NONE** | ❌ No skill correlates evidence across sessions |
| Evidence provenance chain | 111 (partial) | ⚠️ Only table row, not full chain of custody |
| Evidence retirement | **NONE** | ❌ No skill decommissions stale evidence |

### 6.2 Plan Lifecycle (covers 333, but not full lifecycle)

| Phase | Covered By | Gap |
|-------|-----------|-----|
| Generation | 333-mind-plan | ✅ |
| Multi-hypothesis | 333-mind-plan | ✅ |
| Revision after critique | **NONE** | ❌ No 333↔666 feedback loop |
| Cross-plan conflict detection | **NONE** | ❌ No concurrent plan conflict detection |
| Cost estimation | **NONE** | ❌ No compute/API/human cost per step |
| Plan versioning | **NONE** | ❌ No plan history tracking |
| Plan → execution handoff | 010-forge (consumes) | ⚠️ No explicit plan_id passing |

### 6.3 Operator Readiness (covers WELL, but only at stage 666)

| Check Point | Currently | Gap |
|-------------|----------|-----|
| Before planning (stage 333) | ❌ No WELL check | WELL should gate plan generation |
| Before execution (stage 010) | ❌ No WELL check | WELL should gate all T2/T3 actions |
| During critique (stage 666) | ✅ 666 integrates WELL | Only place WELL is checked |
| Post-execution (after 010) | ❌ No WELL check | Should verify operator wasn't overloaded |

### 6.4 Social-Symbolic Dimension (AGENTS.md declares it, no skill operationalizes it)

| Aspect | Status |
|--------|--------|
| Collective bias detection | ✅ `symbolic-order-collective-bias` |
| Trust architecture mapping | ✅ `symbolic-order-trust-architecture` |
| Solidarity monitoring | ❌ Missing skill |
| Mythic domain violation | ❌ Missing skill |
| Layer governance (L1/L2/L3) | ❌ Missing skill |
| Institutional dynamics modeling | ❌ Not operationalized anywhere |
| Population behavior dynamics | ⚠️ Partial in `wealth_monte_carlo_simulate` population_mode |

---

## §7. ANTI-PATTERNS

| Anti-Pattern | Description | Remedy |
|-------------|-------------|--------|
| **Skill overload** | Loading 5+ skills for a simple task | Use this meta-skill to identify the MINIMUM skill set |
| **Phantom reliance** | Referencing a skill that doesn't exist | Run gap register (§3A) and forge missing skills |
| **Organ mismatch** | Loading a GEOX skill for a WEALTH task | Check routing table (§4) |
| **Stage skipping** | Going straight to 010 without 000→111→333→666→888 | Always start with 000-init-intent-classify |
| **Single-skill tunnel** | Using only one skill when the task spans organs | Load the cross-cutting concern from §6 |
| **Stale skill** | Using a skill forged 30+ days ago without verification | Check health score (§5) |
| **Collision blindness** | Two skills covering the same capability differently | Run collision detection on overlap |

---

## §8. QUICK REFERENCE — Minimal Skill Set Per Task Type

| Task Type | Minimum Skills | Maximum Skills (if deep) |
|-----------|---------------|-------------------------|
| Simple observation | 000 | 000 + 111 |
| Code edit/build | 000 + 010 | 000 + 111 + 333 + 010 + 999 |
| Capital analysis | 000 + wealth-capital-thermodynamics | 000 + 111 + wealth-capital-thermodynamics + wealth-capital-reasoning + 666 + 888 + 999 |
| Geological interpretation | 000 + geox-constitution | 000 + 111 + geox-constitution + geox-earth-evidence + geox-epistemic-ladder + geox-contradiction-engine + 666 + 888 + 999 |
| Federation audit | 000 + entropy-thermo-zen | 000 + entropy-thermo-zen + this meta-skill + 999 |
| Build new agent | 000 + agentic-builder | 000 + agentic-builder + skill-creator + a2a-federation-builder |
| Skill gap detection | **This meta-skill** | This meta-skill + skill-creator |
| Constitutional judgment | 000 + 888 | 000 + 111 + 333 + 666 + 888 + 999 |
| Infrastructure change | 000 + aforge-execution | 000 + 111 + 333 + aforge-execution + mcp-mastery + 010 + 999 |

---

## §9. RECOMMENDATIONS — Priority Forge Queue

Based on gap analysis, these skills should be forged next:

| Priority | Skill | Why | Effort |
|----------|-------|-----|--------|
| **P1** | `070-lock-humility-godel` | Referenced by 6 skills, never existed | Medium — epistemic gate pattern |
| **P1** | `444-route-organ-direct` | Referenced by 5 skills, routing confusion | Low — routing table extraction |
| **P2** | `arifos-kernel-operations` | arifOS has zero domain skill despite being the sovereign kernel | Medium |
| **P2** | `well-fatigue-science` | WELL has 1 thin skill, needs depth | Medium — sleep/cognitive science |
| **P2** | `symbolic-order-solidarity-monitor` | Referenced, missing from 5-skill cluster | Medium |
| **P3** | `wealth-stock-analysis` | 12 modes, no dedicated skill | Medium |
| **P3** | `hermes-asi-telegram` | SOUL.md exists, no skill wraps it | Low — wrapper |
| **P3** | `symbolic-order-mythic-attestor` | Referenced, missing | Medium |
| **P3** | `symbolic-order-layer-governance` | Referenced, missing | Low |
| **P4** | `vault-deep-operations` | Chain audit, receipt management | Low |
| **P4** | `docker-container-management` | 17 hostinger tools, no skill | Low |
| **P4** | `cloudflare-dns-management` | DNS/Workers/R2 operations | Low |

---

## §10. TELEMTRY

```json
{
  "skill_name": "meta-mesa-skill-atlas",
  "version": "1.0.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "skills_inventoried": 35,
  "phantom_skills_found": 8,
  "missing_domains_found": 8,
  "thin_organs": ["WELL", "AAA", "SYMBOLIC"],
  "routing_decision": "{{routed_to_skill}}",
  "latency_ms": 0,
  "token_in": 0,
  "token_out": 0
}
```

---

## §11. RECURSIVE SCORECARD

| Metric | Target | Notes |
|--------|--------|-------|
| Activation Precision | > 0.95 | Don't load for domain tasks |
| Routing Accuracy | > 0.90 | Correct skill for intent |
| Gap Detection Rate | > 0.85 | Find missing skills |
| Phantom Resolution Rate | 1.00 | Never route to non-existent skill |
| Doc Freshness | 1.00 | Self-updating via forge_work/ |

---

*Forged: 2026-06-28 by FORGE (000Ω) for F13 SOVEREIGN*
*Inventory: 7 stage skills + 28 domain skills = 35 total*
*Phantoms: 8 referenced but missing*
*Missing domains: 8 entirely uncovered*
*DITEMPA BUKAN DIBERI — The mesa sees the terrain. The terrain does not see the mesa.*
