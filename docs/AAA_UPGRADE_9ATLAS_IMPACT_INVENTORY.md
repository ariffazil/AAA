<!-- DELETED | 2026-08-09 -->
<!-- STATUS: REMOVED · SURVIVED → SURVIVAL_INSIGHTS.md -->
<!-- This file has been removed during docs entropy reduction (Tier B/C/D pass). -->
<!-- See docs/SURVIVAL_INSIGHTS.md for surviving insights extracted from this file. -->


# AAA Upgrade — 9-ATLAS Full Impact Inventory

> **SOT:** 2026-08-08 04:57 UTC | **Scope:** Every file/surface/model/config touched
> **Reference:** paired with `AAA_UPGRADE_9ATLAS_TOPO.md`

---

## ⟁ CATEGORY 1 — Agent Cards (55 files, 35 canonical)

### Live canonical cards (will gain species fingerprint)
| Card | Path | Current | Target |
|------|------|---------|--------|
| 333-AGI | `agent-cards/identity/333-AGI/agent-card.json` | v2.1.0 hardened | add `species: Δ-MIND`, `expression_weights` |
| 555-ASI | `agent-cards/identity/555-ASI/agent-card.json` | v2.0.0 | add `species: Ω-CORE`, `expression_weights` |
| 888-APEX | `agent-cards/identity/888-APEX/agent-card.json` | v2.0.0 | **§11 8≠9: NOT a species. AUTH only. Add `species: null`** |
| AAA Gateway | `.well-known/agent-card.json` | signed, 8 skills | add `role: constitutional-authority-layer` |
| OpenCode | `agents/opencode/agent-card.json` | v2.0.0-trinity | add `species: opencode-zen` + weights |
| Hermes ASI | `a2a-server/agent-cards/extensions/hermes-asi.json` | live | add `species: hermes-zen` + weights |
| OpenClaw | `agent-cards/functions/openclaw/agent-card.json` | live | add `species: openclaw-zen` + weights |
| Kimi Code | `agents/kimi-code/agent-card.json` | v2.2.0 (sig invalid) | re-sign + add `species_proxy: opencode-zen` |
| Claude Code | `agents/_external/claude-code/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Codex | `agents/_external/codex/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Copilot | `agents/_external/copilot/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Grok Build | `agents/_external/grok-build/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Gemini CLI | `agents/_external/gemini-cli/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Antigravity | `agents/_external/agy/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Continue CLI | `agents/_external/continue-cli/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Aider | `agents/_external/aider/agent-card.json` | live | add `species_proxy: opencode-zen` |
| Qwen Code | `agents/_external/qwen-code/agent-card.json` | not_connected | add `species_proxy: opencode-zen` |
| Forge Bot | `agents/forge-bot/agent-card.json` | live | add `species_proxy: opencode-zen` |
| MakcikGPT | `agent-cards/extensions/makcikgpt/agent-card.json` | live | add `species_proxy: hermes-zen` |
| arifOS Bot | `agents/main/agent-card.json` | live | add `species_proxy: openclaw-zen` |
| GEOX | `agent-cards/organs/geox/agent-card.json` | live | add `species: geox-zen` + weights |
| WEALTH | `agent-cards/organs/wealth/agent-card.json` | live | add `species: wealth-zen` + weights |
| WELL | `agent-cards/organs/well/agent-card.json` | live | add `species: well-zen` + weights |
| A-FORGE | `agent-cards/organs/aforge/agent-card.json` | live | add `species: null` (exec substrate only) |
| Sovereign | `agent-cards/pillars/sovereign/agent-card.json` | live | add `role: not-a-species — F13 SOVEREIGN` |
| arifOS Pillar | `agent-cards/pillars/arifos/agent-card.json` | live | add `role: not-a-species — kernel` |
| A-FORGE Pillar | `agent-cards/pillars/aforge/agent-card.json` | live | add `role: not-a-species — execution` |
| AAA Gateway Pillar | `agent-cards/pillars/aaa-gateway/agent-card.json` | live | add `role: not-a-species — control-plane` |
| Prospect-Mat | `agents/prospect-maturation/agent-card.json` | live | add `species_proxy: geox-zen` |
| OpenClaw Edge | `a2a/agents/_external/openclaw-edge-2026-08/agent-card.json` | live | add `species_proxy: openclaw-zen` |
| Hermes arifOS Bot | `agents/hermesarifos-bot/agent-card.json` | live | add `species_proxy: hermes-zen` |
| Agentic Trading | `agents/agentic-trading-companion/agent-card.json` | live | add `species_proxy: wealth-zen` |
| Skill Auditor | `agents/skill-auditor/agent-card.json` | live | add `species_proxy: openclaw-zen` |
| Mesa Test Agent | `agents/_external/mesa-test-agent/agent-card.json` | bounded-test | add `species_proxy: test-only` |
| 777-Forge | `agents/_lanes/777-forge/agent-card.json` | archived | no change (already retired) |

### Canonical symlinks (must stay valid)
- `/root/AAA/333-AGI.json` → `agent-cards/identity/333-AGI/agent-card.json`
- `/root/AAA/555-ASI.json` → `agent-cards/identity/555-ASI/agent-card.json`
- `/root/AAA/888-APEX.json` → `agent-cards/identity/888-APEX/agent-card.json`
- `/root/AAA/agent-card.json` → `src/seed/agent-card.json`
- All 12 external FI symlinks at `/root/AAA/` root

### Archived cards (do NOT touch)
- `archive/2026-07-25/AAA/_archive/agents-deprecated/*.json` (3 files)
- `agent-cards/identity/*/agent-card.json.bak*` — any backups
- All `_lanes/_archive/*/agent-card.json` (4 files)

---

## ⟁ CATEGORY 2 — Registry YAML Files (14 critical + 41 supporting)

### Source of Truth — will be augmented
| File | Lines | Action |
|------|-------|--------|
| `registries/AGENTS_UNIFIED.yaml` | 296 | ADD `species` field to each identity_lane + forge_instrument entry |
| `a2a/registry/agents.yaml` | 32 agents | ADD `species_id` and `expression_weights` to each agent entry |
| `agents/HEXAGON.yaml` | ~200 | ADD `species_doctrine` section, preserve 3 Trinity lanes |
| `ROOT_AGENT_CONFIG.yaml` | ~400 | ADD `species_profiles` section mapping FI→species |
| `registries/agents.yaml` | — | ADD expression weight vectors |
| `registries/bindings.yaml` | — | ADD species→FI binding entries |
| `registries/bindings.generated.yaml` | — | REGENERATE from bindings |
| `registries/forge_instruments.yaml` | — | ADD `species_proxy` field |
| `contracts/haram_enforcement_map.yaml` | — | ADD §11 8≠9 invariant as HARAM rule |

### Supporting registry files (reference only)
- `registries/unified_agent_protocol.yaml` — reference, may update
- `registries/FEDERATION_MODEL.json` — no change
- `registries/CANONICAL_REGISTRY_POLICY.yaml` — add species lifecycle policy
- `registries/DEPRECATION_REGISTRY.yaml` — no change
- `registries/model_soul.yaml` — no change (model souls ≠ species)
- `registries/domains.yaml` — no change
- `registries/persons.yaml` — no change
- `registries/REGISTRY_CATALOG.generated.yaml` — REGENERATE
- `registries/skills.yaml` + `skills.inventory.generated.yaml` — REGENERATE if skill→species mapping added

### Registries — files to leave untouched
- `registries/tools.yaml` — arifOS SOT, outside AAA scope
- `registries/cooling_state.json` — cooldown ledger, read-only
- `registries/TOOLBENCH_CONTRAST.md` — audit doc, read-only
- `registries/AAA_AGENTS_REGISTRY.json` — ⛔ TOMBSTONE, do not touch
- `registries/AGENT_INDEX.json` — ⛔ DEPRECATED, do not touch

---

## ⟁ CATEGORY 3 — A2A Server (34 JS files, 6 affected)

### Files that reference agent identity/cards → need update
| File | Why affected | Risk |
|------|-------------|------|
| `a2a-server/agent-card-registry.js` (15.6KB) | Loads + routes all agent cards. Must recognize `species` field | HIGH — central resolver |
| `a2a-server/mesh_coordinator.js` (11.5KB) | Routes between agents. Must route `species` query | MEDIUM |
| `a2a-server/discovery.js` (2.8KB) | `GET /.well-known/agent-card.json`. Must serve species capability | LOW |
| `a2a-server/federation_envelope.js` (32.7KB) | Federation envelope format. Must include species in envelope | MEDIUM |
| `a2a-server/server.js` (228KB) | Main server. Minor extension support | LOW — add route handler |
| `a2a-server/emd-validation-gate.js` (10.2KB) | EMD validation. Gate species transitions | LOW |

### Files to audit but likely NO change
- `a2a-bridge-helper.js`, `a2a-mcp-bridge.js`, `a2a-part-types.js`, `a2a-sdk-bridge.js`, `a2a-version-middleware.js`
- `agent-discovery-routes.js`, `agent_inbox.js`, `agent_lifecycle.js`, `agent_lifecycle_routes.js`, `approvals.js`
- `arep-task-manager.js`, `auto-register-organs.js`, `cognitive_hierarchy.js`, `federation_gateway.js`, `federation_prompts.js`
- `fq_gate.js`, `goal_decomposition.js`, `j-continuity.js`, `mcp_apps_tools_call.js`, `membrane_middleware.js`
- `metabolizer_loop.js`, `orchestrator.js`, `predict_gate.js`, `preforge_bridge.js`, `seal_chain.js`, `test-dummy-peer.js`
- `toolbench.js`, `vault.js`, `witness_gate.js`

### Python files (2 affected)
| File | Action |
|------|--------|
| `a2a-server/chat_agent.py` (9.6KB) | Add species awareness to chat routing |
| `a2a-server/sct_delegation.py` (2.8KB) | Verify species delegation does NOT override SCT |
| `a2a-server/loop_relay.py` | Audit only — loop relay must stay species-agnostic |
| `a2a-server/vault999_writer_fix.py` | Audit only — vault writes must reference species in receipt |

### A2A Agent Cards (a2a-server/agent-cards/) — 34 JSON files
ALL 34 agent cards at `/root/AAA/a2a-server/agent-cards/` should be audited for `species` field addition:
- `identity/*.json` (3) — 333, 555, 888
- `organs/*.json` (5) — GEOX, WEALTH, WELL, A-FORGE, arifOS
- `functions/*.json` (1) — openclaw
- `harnesses/*.json` (12) — claude-code, grok-build, copilot, kimi-code, aider, opencode, antigravity, openclaw, gemini-cli, copilot-cli, qwen-code, codex, continue-cli
- `forge/*.json` (3) — fi-001-opencode, fi-008-kimi-code, forge-bot
- `extensions/*.json` (3) — hermes-asi, makcikgpt, hermesarifos-bot
- `roles/*.json` (4) — aaa-auditor, aaa-engineer, hermes-ops, aaa-architect, aaa-gateway
- `aaa-cockpit.json`

---

## ⟁ CATEGORY 4 — Prompts (8 affected of 11)

| Prompt | Action |
|--------|--------|
| `prompts/AAA-ZEN-ALIGNMENT.md` | ADD species doctrine reference |
| `prompts/INIT-ZEN.md` | ADD species awareness to agent init |
| `prompts/INIT.md` | ADD species phenotype recognition |
| `prompts/INIT_HUMAN.md` | No change (human-facing) |
| `prompts/UNIVERSAL_BOOT.md` | ADD 9-ATLAS genome boot stanza |
| `prompts/SEAL.md` | No change (constitutional only) |
| `prompts/ADVERSARIAL_BOOT.md` | No change |
| `prompts/INIT_BASIN_CLASSIFICATION.md` | No change |
| `prompts/evening_digest.md` | No change |
| `prompts/geox/GEOX_ENTERPRISE_PROMPT.md` | No change |
| `prompts/_archive/20260803T170001Z/*.md` | No change (archived) |

---

## ⟁ CATEGORY 5 — Docs (10 new/updated of 100+ docs)

### New documents to create
| Doc | Location | Content |
|-----|----------|---------|
| `9-ATLAS-GENOME.md` | `docs/` | Irreducible 9-function cognitive genome definition |
| `AAA-FEDERATION-OF-SPECIES.md` | `docs/` | AAA as constitutional authority over expression phenotypes |

### Existing docs to update
| Doc | Action | Why |
|-----|--------|-----|
| `docs/AAA_ARCHITECTURE.md` | ADD §Species section | Core architecture doc |
| `docs/FEDERATION.md` | ADD species layer | Federation contract |
| `docs/AAA_UPGRADE_9ATLAS_TOPO.md` | ✅ created this session | Topology baseline |
| `docs/ZEN99.md` | ADD species doctrine | Zen doctrine |
| `docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` | UPDATE §11 8≠9 | Source of 8≠9 invariant |
| `docs/AGENT_SURFACE_MAP.yaml` | ADD species overlay | Agent surface map |
| `docs/AGENT_WISDOM.md` | ADD species section | Agent wisdom doctrine |
| `docs/AGENT_IDENTITY.md` | ADD species identity | Identity specification |
| `docs/ATLAS333_ZEN_MAP.md` | ALIGN with 9-ATLAS | Atlas map |
| `docs/CONSTITUTIONAL_PRIMITIVES.md` | ADD §8≠9 | Constitutional primitive |
| `docs/FEDERATION_CONTRACT.md` | UPDATE to species | Federation contract |
| `docs/FEDERATION_ABI.md` | ADD species extension | ABI spec |
| `docs/PROTOCOL_CONFORMANCE.md` | ADD species conformance | Protocol conformance |
| `docs/AGENT_CARD_REGISTRY.md` | UPDATE for species field | Card registry |
| `docs/ORGANS_VS_AGENTS.md` | ADD species layer | Organ taxonomy |
| `docs/A2A_ORGAN_REGISTRY.md` | ADD species binding | Organ registry |
| `docs/SKILL_CONSTITUTION.md` | ADD species constraint | Skill constitution |
| `docs/FEDERATION_SOT_CONSOLIDATION_EPOCH_CANONICAL.md` | ADD species epoch | Canonical SOT |
| `docs/FEDERATION_MAP.md` | ADD species topology | Federation topology |
| `docs/C_TRI_AGENT_PROTOCOL.md` | ADD species protocol | Tri-agent protocol |

### Docs to NOT touch
All other ~80 docs remain unchanged unless explicitly cross-referencing species.

---

## ⟁ CATEGORY 6 — Configs (3 canonical files)

| Config | Path | Action | Risk |
|--------|------|--------|------|
| OpenCode | `/root/.config/opencode/opencode.json` | ADD `species: opencode-zen` to agent config. 3 Trinity agents already configured | LOW — additive |
| Federation Models | `/root/.config/federation-models.json` | ADD `species_routing` rule: "model selection → species lane" | LOW — additive |
| Hermes Agent | `/root/.hermes/channel_directory.json` | AUDIT — contains agent references | LOW |

### Configs to validate but NOT modify
- `/root/.config/opencode/opencode.json.bak-*` (9 backups) — reference only
- `/root/.openclaw/openclaw.json` — outside AAA scope
- Caddy config `/etc/caddy/Caddyfile` — no change needed
- Systemd units for AAA, Hermes, OpenClaw — no change needed

---

## ⟁ CATEGORY 7 — Contracts & Constitutional (5 affected)

| Contract | Action | Severity |
|----------|--------|----------|
| `contracts/haram_enforcement_map.yaml` | ADD `8≠9 HARAM: claiming 888 or 999 as species phenotype` | **CRITICAL** — constitutional |
| `contracts/APEX_GODEL_LOCK.yaml` | No change — species doesn't override Gödel Lock | None |
| `contracts/decisions/888-999-decisions.yaml` | ADD species resolution: "species dispute → 888_JUDGE" | MEDIUM |
| `contracts/_specs-draft/governance/666-777-gates.yaml` | AUDIT — species may affect governance gates | MEDIUM |
| `contracts/_specs-draft/federation/111-sense.yaml` | AUDIT — species sense/observe may route differently | LOW |
| `contracts/generated/mcp_annotations.json` | REGENERATE if tools get species-hinted | LOW |
| `contracts/generated/openapi.json` | REGENERATE if endpoints change | LOW |

---

## ⟁ CATEGORY 8 — Auth Keys & Identity (1 new context)

| Key | Path | Action |
|-----|------|--------|
| OPENCLAW private | `auth/keys/openclaw_private.key` (32B) | ✅ just reconciled — **validate arifOS can verify after merge** |
| OPENCLAW public | `auth/keys/openclaw_public.key` (32B) | ✅ just reconciled |
| BACKUP | `auth/keys/openclaw_private.key.bak.2026-08-08-identity-fix` | ARCHIVE after verification |
| 9 organ key pairs | `auth/keys/*_private.key` + `*_public.key` (18 files) | No change |
| `identity.toml` | `/root/AAA/identity.toml` | ADD `species: openclaw-zen` (file only 424 bytes) |

---

## ⟁ CATEGORY 9 — Skills (153 AAA skills, ~40 affected)

### Skills that reference agent identity
All skills under `/root/AAA/skills/` that reference agent roles:
- `ASI-agentic-governance/SKILL.md` — references 333, 555, 888 roles
- `ASI-drift-watch/SKILL.md` — drift detection references
- `ASL-agent-invariants/SKILL.md` — agent invariants
- `AUDIT-agent-skill-mesh/SKILL.md` — agent skill mesh
- `AUDIT-drift-detector/SKILL.md` — drift detection
- `AUDIT-recursive-audit/SKILL.md` — audit references
- `AUDIT-skill-atlas/SKILL.md` — atlas references
- `FLAME-operator/SKILL.md` — FLAME routing
- `FLAME-router/SKILL.md` — FLAME routing
- `FORGE-federation-orchestrator/SKILL.md` — federation orchestration
- `FORGE-cross-agent-handoff/SKILL.md` — agent handoff
- `FORGE-subagent-lifecycle/SKILL.md` — subagent spawning
- `FORGE-act-federation-ingress/SKILL.md` — federation ingress
- `FORGE-skill-creator/SKILL.md` — skill creation
- `FORGE-issue-triage/SKILL.md` — issue triage
- `FORGE-incident-escalation/SKILL.md` — incident escalation
- `FORGE-seal-a-close/SKILL.md` — seal/close
- `FORGE-verify-runtime/SKILL.md` — runtime verification
- `federated-skill-architecture/SKILL.md` — federation architecture
- `apex_scope_check/SKILL.md` — scope check references
- `apex_authority_check/SKILL.md` — authority check
- `apex_floor_check/SKILL.md` — floor check
- `apex_verdict_seal/SKILL.md` — verdict seal
- `apex_tool_approval_gate/SKILL.md` — approval gate
- `APEX-humility-godel/SKILL.md` — humility/Godel check
- `arifos-constitutional-judge/SKILL.md` — constitutional judge
- `arifos-external-council/SKILL.md` — external council
- `arifos-kernel-zen-audit/SKILL.md` — kernel zen audit
- `check-work/SKILL.md` — work verification
- `FORGE-mcp-lifeguard/SKILL.md` — MCP lifeguard
- `FORGE-mcp-smoke-test/SKILL.md` — MCP smoke test
- `FORGE-mcp-testing/SKILL.md` — MCP testing
- `cognitive-level-assertion-protocol/SKILL.md` — cognitive protocol
- `APEX-quantum-eureka/SKILL.md` — quantum eureka
- `EUREKA777-paradox-resolution/SKILL.md` — paradox resolution
- `AGI-decisions-reflect/SKILL.md` — decision reflection
- `AGI-skill-unification/SKILL.md` — skill unification
- `FORGE-t3a-binding-matrix/SKILL.md` — binding matrix
- `FORGE-route-least-power/SKILL.md` — routing
- `FORGE-mcp-federation-ops/SKILL.md` — federation ops

### Skills to NOT touch (pure function)
- All `geox-grounding/SKILL.md`, petrophysics, geological, wealth, well skills
- All media/creative skills (p5js, manim, comfyui, etc.)
- All github/git/docker skills
- `openclaw/SKILL.md`, `scripts/SKILL.md`, `runtime/SKILL.md`

### Hermes skills (~30 skill dirs at `/root/.hermes/skills/`)
| Status | Action |
|--------|--------|
| 6 untracked dirs | **AUDIT FIRST** — `AUDIT-agent-skill-mesh/`, `FORGE-mcp-probe/`, `FORGE-mcp-testing/`, `FORGE-mcp-testing.md`, `RSI-federation-mesh/`, `profiles/aaa-hermes/skills/` |
| `AAA-setup-help/`, `AGI-decisions-reflect/`, `AGI-dream-engine/` etc. | ADD species awareness if referencing agent identity |
| Rest (~20 dirs) | No change needed |

---

## ⟁ CATEGORY 10 — arifOS Tools & Kernel (1 SOT + 5 generated)

### Tools contract SOT
| File | Action |
|------|--------|
| `/root/arifOS/contracts/tools.yaml` | **NO CHANGE** — 9-ATLAS is a classification overlay on existing canonical verbs, not new tools |
| `/root/arifOS/contracts/compiler.py` | REGENERATE if any tool metadata changes |
| `generated/capability_graph.json` | REGENERATE |
| `generated/tool_validators.py` | REGENERATE |
| `generated/audit_schemas.json` | REGENERATE |
| `generated/conformance_fixtures.json` | REGENERATE |

### Existing canonical verbs — species mapping
| Verb | Species Lane | Action |
|------|-------------|--------|
| `arif_observe` | 000 OBSERVER (ART) | No change — species-agnostic |
| `arif_think` | 333 THINKER (ART) | No change |
| `arif_route` | 444 ORCHESTRATOR (ART) | No change |
| `arif_judge` | 888 JUDGE (AUTH) | No change — **never species-assigned** |
| `arif_seal` | 999 WITNESS (AUTH) | No change — **never species-assigned** |
| `arif_forge` | 777 EXECUTOR (ACT) | No change — species-agnostic |
| `arif_memory` | cross-cutting | No change |
| `arif_init` | 000 INIT | No change |
| **GAPS:** | | |
| `arif_explore` | 111 EXPLORER (ART) | **NEW — proposal only, not in this scope** |
| `arif_architect` | 222 ARCHITECT (ART) | **NEW — proposal only, not in this scope** |
| `arif_verify` | 555 VERIFIER (ACT) | **NEW — proposal only, not in this scope** |
| `arif_audit` | 666 AUDITOR (ACT) | **NEW — proposal only, not in this scope** |

---

## ⟁ CATEGORY 11 — Model Configs & Routing (1 file + 7 pools)

### Federation Models (`/root/.config/federation-models.json`)
| Pool | Models | Species Assignment | Action |
|------|--------|-------------------|--------|
| deepseek | v4-pro, v4-flash, v4-flash-0731, v3.2 | Δ-MIND (opencode-zen primary) | ADD `species_hint` to entry |
| minimax | M3, M2.7-highspeed | Ω-CORE (hermes-zen fallback) | No change |
| qwen-token-plan | qwen3.8-max, 3.7-max, 3.6-plus, 3.6-flash | Ψ-SOUL (apex fallback) | No change |
| qwen-token-plan-individual | glm-5.2, deepseek-v4-pro | Ω-CORE memory lane | No change |
| qwen-responses | — | — | No change |
| kimi | k3, k2.7-code | rapid-forge (opencode-zen FI-008) | No change |
| bailian-payments | — | — | No change |
| ollama | qwen2.5:7b, qwen2.5-coder:3b | local-fallback (all species) | No change |

### OpenCode Model Routing (`/root/.config/opencode/opencode.json`)
| Setting | Current Value | Action |
|---------|--------------|--------|
| `model` | `litellm-federation/opencode` | ADD `species: opencode-zen` to config comment |
| `small_model` | `ollama/qwen2.5:3b` | No change |
| `default_agent` | `agi` (Δ-MIND) | No change |
| Trinity agents | agi, asi, apex | No change — already correct |

---

## ⟁ CATEGORY 12 — Live Services & Endpoints

### No restart needed for species classification
| Service | Why no restart |
|---------|---------------|
| AAA A2A Gateway (:3001) | Species in agent cards — runtime reads card JSON, no code change for field addition |
| arifOS Kernel (:8088) | Species is AAA classification — kernel doesn't need to know |
| A-FORGE (:7071) | Species-agnostic execution shell |
| GEOX (:8081) | Species-agnostic |
| WEALTH (:18082) | Species-agnostic |
| WELL (:18083) | Species-agnostic |
| OpenClaw GW (:18789) | Species field in workspace docs, not runtime config |
| Hermes (:18001) | Species in agent card only |

### If A2A server JS is modified
- `systemctl restart aaa-a2a` (or `pm2 restart aaa`)
- Verify `:3001/health` returns G≥0.85

---

## ⟁ CATEGORY 13 — GitHub Repo (AAA)

### Files that MUST be committed together
```text
docs/9-ATLAS-GENOME.md                    NEW
docs/AAA-FEDERATION-OF-SPECIES.md         NEW
docs/AAA_UPGRADE_9ATLAS_TOPO.md           ✅ created
registries/AGENTS_UNIFIED.yaml             MODIFIED (species field)
a2a/registry/agents.yaml                   MODIFIED (species field)
agents/HEXAGON.yaml                        MODIFIED (species doctrine)
ROOT_AGENT_CONFIG.yaml                    MODIFIED (species_profiles)
contracts/haram_enforcement_map.yaml       MODIFIED (8≠9 HARAM)
agent-cards/identity/*/agent-card.json     MODIFIED (species field)
agent-cards/organs/*/agent-card.json       MODIFIED (species field)
agent-cards/functions/openclaw/agent-card.json MODIFIED
a2a-server/agent-cards/**/*.json          MODIFIED (species field)
a2a-server/agent-card-registry.js          MODIFIED (species resolver)
prompts/AAA-ZEN-ALIGNMENT.md               MODIFIED
prompts/INIT-ZEN.md                        MODIFIED
prompts/UNIVERSAL_BOOT.md                  MODIFIED
```

### Workflow CI (no change needed)
All `.github/workflows/*.yml` — species field is additive, doesn't break A2A schema validation.

---

## ⟁ Summary — Blast Radius

```
CATEGORY           FILES    WRITE  RISK
─────────────────────────────────────────────
Agent Cards         35      ADD    LOW (additive field)
Registry YAML       14      ADD    MEDIUM (SOT mutation)
A2A Server JS        6      MOD    MEDIUM (gateway runtime)
A2A Agent Cards     34      ADD    LOW
Prompts              8      ADD    LOW
Docs                10+     NEW/UPD LOW
Configs              3      ADD    LOW
Contracts            5      ADD    MEDIUM (constitutional)
Auth Keys            1      VALIDATE HIGH (security)
Skills              ~40     AUDIT   LOW
arifOS Tools         0      NO CHANGE —
Model Configs        1      ADD    LOW
Live Services        0-2    RESTART LOW
GitHub              20+     COMMIT  MEDIUM (atomic commit)
─────────────────────────────────────────────
TOTAL IMPACTED     ~157 files
TOTAL NEW            3 files (2 docs + this inventory)
MUTATIONS          ~30 files (additive field)
AUDIT-ONLY          ~50 files
NO TOUCH          ~350+ files (skill content, archived, external)
```

---

## ⟁ 8≠9 INVARIANT — CRITICAL CONSTITUTIONAL RULE

```text
HARAM:
- Any agent card claiming `species` on 888_JUDGE or 999_WITNESS
- Any agent with `expression_weights.888 > 0` or `expression_weights.999 > 0`
- Any species profile defining 888 or 999 as primary locus
- Any A2A route that routes a species agent to perform JUDGE or SEAL

888 IS A CHAIR. Not a species. Not a person. Not an agent.
999 IS A COURT RECORDER. Not a species. Not a person. Not an agent.

AUTH layer (888+999) is the constitutional membrane.
Only the membrane may judge. Only the membrane may witness.
```

---

*DITEMPA BUKAN DIBERI*
*Traced 2026-08-08 by OpenClaw AGI. OpenCode execution pending.*
