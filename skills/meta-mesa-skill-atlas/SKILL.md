---
name: meta-mesa-skill-atlas
description: Unified skill inventory, gap detection, and cross-cutting orchestration for AAA catalog + Grok/Claude/Codex/Hermes/Kimi/OpenClaw harness views. The mesa above the terrain — see the whole, find the missing, route the right skill. Load when starting a new task, auditing skill health, unifying CLI agent skills, onboarding a new organ, or when you don't know which skill to load.
version: 1.2.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil (888)
risk_tier: low
floor_scope: [F2, F4, F7, F9]
autonomy_tier: T1
tags: [meta, skill-atlas, gap-detection, routing, federation, inventory, multi-harness, grok, aaa]
forged: 2026-06-28
updated: 2026-07-12
sources:
  - AAA FEDERATED_SKILLS_REGISTRY_V3.yaml (63 logical)
  - AAA BOOTSTRAP_MANIFEST (9 universals)
  - Live harness mesh: ~/.grok ~/.claude ~/.codex ~/.agents AAA
  - forge_work/2026-07-12/GROK-CLI-AAA-SKILL-UNIFICATION-ATLAS.md
  - AGENTS.md federation organ index
---

# META-MESA — Skill Atlas & Gap Detection

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
> **The mesa above the terrain. See the whole. Find the missing. Route the right.**

## What This Skill Is

This is the **meta-skill** — a skill about skills. It provides:

1. **Inventory** — live multi-surface counts (not a frozen “35”)
2. **Gap detection** — missing, thin, dual-named, harness-divergent
3. **Routing** — given a task *and harness*, which skill(s) to load
4. **Health scoring** — freshness, collision, catalog vs view drift
5. **Cross-harness unification** — AAA catalog ↔ CLI agent views

It does NOT execute, judge, or seal. It classifies, routes, and illuminates.

**Iron rule:** AAA is the catalog. Harnesses are views. Do not invent parallel catalogs.

**Live atlas (T₁):** `/root/A-FORGE/forge_work/2026-07-12/GROK-CLI-AAA-SKILL-UNIFICATION-ATLAS.md`  
**JSON:** `…/GROK-CLI-AAA-SKILL-UNIFICATION-ATLAS.json`

---

## §0. MULTI-HARNESS UNIFICATION (Grok × CLI × AAA) — 2026-07-12

### Architecture

```
BOOTSTRAP_MANIFEST (9 universals)     ← always first
        ↓
AAA/skills  (catalog + V3 registry)   ← sole named truth
   +  .agents/skills (doctrine/stage) ← shared federation core
        ↓ symlink mesh
~/.grok | ~/.claude | ~/.codex        ← views (+ harness-native)
        ↓ separate trees
Hermes categories | Kimi roles | OpenClaw owned
```

### Live inventory (OBSERVED T₁)

| Surface | Count | Role |
|---------|-------|------|
| Grok `~/.grok/skills` | **116** resolvable | View: AAA 67 + agents 37 + **native 12** |
| AAA `/root/AAA/skills` | **70** top-level + substrate/knowledge | **Catalog** |
| V3 registry | **63** logical (6+3+54) | Short names |
| `.agents/skills` | **43–50** | Stage/domain doctrine |
| Claude / Codex | **104 / 107** | Same mesh (symlink) |
| Hermes | **180** SKILL.md / 34 cats | Category tree — **not** flat mesh |
| Kimi | 7 role contrast skills | Local, not catalog |
| **Legacy meta-mesa claim** | 37 | **STALE — do not use** |

### Grok native keepers (harness-only)

`arif-governed-autonomous-execution` · `grok-zen-aaa-substrate` · `grok-federation-skill-upgrader` · `orthogonal-skill-update` · `create-skill` · `check-work` · `help` · `imagine`  
**Prune candidates:** `docx` · `pptx` · `xlsx` · `code-review`

### Dual-name gap — SEALED (2026-07-12)

**Machine table (63/63 RESOLVED):** `/root/AAA/skills/SKILL_ALIAS_TABLE.json`  
**Human:** `A-FORGE/forge_work/2026-07-12/SKILL_ALIAS_TABLE.md`  
**Hermes bridge:** `A-FORGE/forge_work/2026-07-12/HERMES-V3-DOMAIN-BRIDGE.md`  
**Mesh sync:** `bash /root/AAA/skills/scripts/skill-mesh-sync.sh [--apply|--check]`

| V3 short | Primary disk path |
|----------|-------------------|
| `kernel-bind` … `audit-seal` | `AAA/skills/substrate/<name>` |
| `know-*` | `AAA/skills/knowledge/<name>` |
| `meta-atlas` | `meta-mesa-skill-atlas` |
| `geo-*` | `geox-*` / `geological-artifact-rigor` / `prospect-maturation-workflow` |
| `wealth-thermo` | `wealth-capital-thermodynamics` |
| `forge-verbs` / `forge-exec` | `kernel-verbs-aforge-hands` |
| (full list) | see JSON |

### Unification phases — status 2026-07-12

1. **AUTHORITY** — ✅ AAA + V3 sole catalog  
2. **ALIAS TABLE** — ✅ 63/63 sealed JSON  
3. **PROFILES** — ✅ `grok` + `opencode` in V3  
4. **META-MESA REFRESH** — ✅ v1.2.0+  
5. **MESH SYNC** — ✅ script + applied (substrate/knowledge links)  
6. **HERMES BRIDGE** — ✅ category→domain doc  
7. **PRUNE** — ✅ Grok docx/pptx/xlsx/code-review → `.deprecated`  
8. **BOOT GATE** — ✅ documented below + BOOTSTRAP_MANIFEST  

### BOOT GATE (all CLI agents)

```
BIND → GROUND → ROUTE → RECALL → VERIFY → SEAL → KNOW → READY
```

Only after **READY** may domain skills load. Source: `AAA/skills/BOOTSTRAP_MANIFEST.json` (9 universals).  

### Harness load packs

| CLI | Always | On demand |
|-----|--------|-----------|
| **Grok** | BOOTSTRAP 9 + `arif-governed` + `grok-zen-aaa-substrate` | Domain via this atlas / V3 |
| **Claude / Codex** | BOOTSTRAP 9 + mesh | Same domain pack |
| **Hermes** | `arifos-auto-init` + seven-zen + federated-skill-architecture | Category skill |
| **OpenClaw** | openclaw-agentic + memory | ops / a2a |
| **Kimi** | role contrast skills | forge / dev |

### Anti-patterns (multi-harness)

| Anti-pattern | Remedy |
|--------------|--------|
| Copy skill bodies into every `~/.X/skills` | Symlink to AAA / .agents |
| Second “Grok catalog” of 100+ natives | Keep ≤12 harness keepers |
| Flatten Hermes into AAA | Bridge map only |
| Route by V3 short name without path | Resolve via alias table |
| Trust meta-mesa “37 total” | Re-probe disk / use §0 |

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

## §2. DOMAIN SKILLS BY ORGAN (30 Skills)

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

### Infrastructure (8 skills)

| Skill | Domain | Purpose |
|-------|--------|---------|
| `mcp-mastery` | MCP | Trust surface, protocol, tool forging, transport |
| `mcp-apps-builder` | MCP | SEP-1865 interactive HTML UI in conversations |
| `webmcp-site-builder` | MCP | WebMCP sites, W3C origin trial |
| `github-operations` | Git | Issue triage, PR review, CI diagnostics |
| `federation-observability` | Ops | OTEL, Prometheus, Grafana, LGTM |
| `hf-mastery` | ML | Governed HuggingFace: hub, datasets, inference, fine-tune |
| `iron-shell-render` | Web | Three-layer site architecture |
| `forge-document-intelligence` | Document | EMD stack (Encode-Metabolize-Decode) — VLM perception, provenance, governed action |

### Forge & Agent (3 skills)

| Skill | Purpose |
|-------|---------|
| `aforge-execution` | Build, deploy, verify. Gated by SEAL. |
| `agentic-builder` | Build governed agents: identity, skills, tools |
| `skill-creator` | Bootstrap, design, package new skills |

### General / Meta (4 skills)

| Skill | Purpose |
|-------|---------|
| `apex-theory` | Physics + math + symbolic code + meaning |
| `entropy-thermo-zen` | Thermodynamic entropy management (TZQ) |
| `agentic-fitness-law` | Fitness law, extinction pressures, immune system for tools/agents |
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

> **Cleaned 2026-07-03:** Phantoms replaced with actual tool alternatives. Remaining = PLANNED skills only.

| Missing Skill | Status | Function |
|--------------|--------|----------|
| `070-lock-humility-godel` | ✅ CLEANED → `arif_think` mode=verify + `666-heart-critique-stress` | Final epistemic gate before SEAL-grade claims |
| `034-dag-plan-orchestrate` | ✅ CLEANED → `333-mind-plan-generate` | Multi-step execution graph for cross-organ work |
| `444-route-organ-direct` | ✅ CLEANED → `arif_route` + `tools-embodiment-application` | Organ routing and direct addressing |
| `950-seal-vault-audit` | ✅ CLEANED → `arif_seal` mode=verify | Vault999 seal verification and chain audit |
| `geox-basin-interpreter` | ✅ CLEANED → `geox_basin` directly | Upstream O&G basin interpretation for Petronas |
| `090-check-tool-preflight` | ✅ CLEANED → `666-heart-critique-stress` | Tool preflight check |
| `symbolic-order-solidarity-monitor` | 🔵 PLANNED | Calhoun Phase C population-level detection |
| `symbolic-order-mythic-attestor` | 🔵 PLANNED | Sacred domain violation detection |
| `symbolic-order-layer-governance` | 🔵 PLANNED | L1/L2/L3 hierarchy enforcement |

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
| ~~**Document intelligence**~~ | ~~A-FORGE~~ | ~~Filled 2026-07-02 — `forge-document-intelligence` forged~~ | ✅ FILLED |

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
| "fitness" / "tool evolution" / "why tools survive" | `agentic-fitness-law` | Fitness law + extinction pressures |
| "APEX" / "consciousness" / "physics of AI" | `apex-theory` | Theoretical framework |
| "A2A" / "agent communication" / "federation mesh" | `a2a-federation-builder` | Inter-agent surface |
| "bias" / "collective behavior" / "population" | `symbolic-order-collective-bias` | Social-symbolic |
| "trust" / "trust architecture" / "trust violation" | `symbolic-order-trust-architecture` | Trust mapping |
| "observability" / "tracing" / "metrics" | `federation-observability` | LGTM stack |
| "HuggingFace" / "model hub" / "fine-tune" | `hf-mastery` | ML governance |
| "PDF" / "OCR" / "scan" / "document" / "extract text" | `forge-document-intelligence` | EMD stack — VLM perception + provenance + governance |
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
    # T₁ 2026-07-12 — re-probe; do not trust frozen integers without fs check
    "v3_logical_skills": 63,      # AAA FEDERATED_SKILLS_REGISTRY_V3
    "aaa_top_level_dirs": 70,     # with SKILL.md (excl. deep archive noise)
    "grok_resolvable": 116,       # symlink mesh + 12 native
    "claude_resolvable": 104,
    "codex_resolvable": 107,
    "agents_core": 43,
    "hermes_skill_md": 180,       # category tree, not mesh
    "dual_name_debt": True,       # V3 short vs long disk names
    "thin_organs": ["WELL", "SYMBOLIC"],  # AAA thicker post-mesh
    "thick_organs": ["GEOX", "OPS", "META"],
    "unification_maturity": 0.70, # mesh-linked, catalog-split
    "collision_risk": float,      # dual naming + hermes overlap
    "stale_skills": int,
    "coverage_score": float,
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
| Tool / alias / fitness decision | agentic-fitness-law | 000 + agentic-fitness-law + entropy-thermo-zen + 999 |
| Build new agent | 000 + agentic-builder | 000 + agentic-builder + skill-creator + a2a-federation-builder |
| Skill gap detection | **This meta-skill** | This meta-skill + skill-creator |
| Constitutional judgment | 000 + 888 | 000 + 111 + 333 + 666 + 888 + 999 |
| Infrastructure change | 000 + aforge-execution | 000 + 111 + 333 + aforge-execution + mcp-mastery + 010 + 999 |
| Document processing / OCR / PDF extraction | 000 + forge-document-intelligence | 000 + 111 + forge-document-intelligence + 666 + 888 + 999 (if high-stakes) |

---

## §9. RECOMMENDATIONS — Priority Queue

> **2026-07-12:** Prefer **aliases, profiles, prune, mesh-sync** over forging more skills.  
> Many §3B “missing domains” are now **filled under long names** (docker-*, vault999-*, infra-guardian, hermes categories).

| Priority | Action | Why | Effort |
|----------|--------|-----|--------|
| **P0** | Seal **alias table** short→path | Dual naming is the real phantom | Low |
| **P0** | Add **grok** + **opencode** to V3 `agent_profiles` | Harnesses missing from catalog | Low |
| **P1** | Grok prune office/review → `.deprecated` | Entropy on harness surface | Low |
| **P1** | `skill-mesh-sync` script (dry-run first) | Prevent symlink drift | Medium |
| **P2** | Hermes category → V3 domain bridge doc | 180 skills outside mesh | Medium |
| **P2** | `symbolic-order-solidarity-monitor` | Incomplete symbolic cluster | Medium |
| **P3** | `well-fatigue-science` | WELL still thin on science depth | Medium |
| **P3** | `wealth-stock-analysis` skill wrap | 12 modes, no dedicated skill | Medium |
| **P4** | Cloudflare DNS skill | Ops gap | Low |

---

## §10. TELEMTRY

```json
{
  "skill_name": "meta-mesa-skill-atlas",
  "version": "1.2.0",
  "trigger_phrase": "{{trigger_phrase}}",
  "selected_reason": "{{selected_reason}}",
  "v3_logical": 63,
  "grok_resolvable": 116,
  "aaa_catalog_top": 70,
  "dual_name_debt": true,
  "unification_maturity": 0.70,
  "atlas_artifact": "A-FORGE/forge_work/2026-07-12/GROK-CLI-AAA-SKILL-UNIFICATION-ATLAS.md",
  "routing_decision": "{{routed_to_skill}}",
  "latency_ms": 0
}
```

---

## §11. RECURSIVE SCORECARD

| Metric | Target | Notes |
|--------|--------|-------|
| Activation Precision | > 0.95 | Don't load for domain tasks |
| Routing Accuracy | > 0.90 | Correct skill for intent **and harness** |
| Gap Detection Rate | > 0.85 | Find missing + dual-named |
| Phantom Resolution Rate | 1.00 | Resolve via alias table, never invent path |
| Doc Freshness | 1.00 | Re-probe disk; atlas in forge_work/ |
| Catalog/View drift | 0 | Grok/Claude/Codex mesh == AAA+.agents |

---

*Forged: 2026-06-28 by FORGE (000Ω) for F13 SOVEREIGN*  
*Updated: 2026-07-02 — forge-document-intelligence filled*  
*Updated: 2026-07-12 — multi-harness §0; live inventory; V3/bootstrap alignment; atlas artifact*  
*Canon: AAA catalog · harness views · BOOTSTRAP first*  
*DITEMPA BUKAN DIBERI — The mesa sees the terrain. The terrain does not see the mesa.*
