# Genome + Species Upgrade — Full Blast Radius Map

> **Recorded:** 2026-08-08, against pre-OpenCode-forge baseline (CHAOS TRACE)
> **Triggered by:** F13 sovereign ratification of 9-function cognitive genome + species taxonomy doctrine
> **Scope:** Every file, tool, prompt, config, model, registry, skill, and identity surface the upgrade touches

---

## TL;DR

```
Category                                        Files Affected
─────────────────────────────────────────────────────────────
Kernel verbs (Python)                            13 tools + 8 surfaces
Federation contracts                              5 contracts
Registries                                       11 registries
A2A agent cards                                  14 harnesses + 5 lanes + 5 organs + 7 extensions + 12 functions
Prompts / boot sequences                          8 prompt files
GENESIS doctrine                                  9 GENESIS docs touch the 8≠9 boundary
Adapter render path                               1 renderer (broken today — prerequisite fix)
Skills                                           ~150, of which ~10 require real change
Identity walls                                    3 (arifOS / AAA / Hermes profile)
Models                                            5 routes change meaning
A2A protocol surface                             12 JS modules
```

---

## 1. Kernel verb surface — arifOS Python (HIGHEST blast)

Currently the kernel exposes **8 canonical verbs** defined in `/root/arifOS/arifosmcp/runtime/megaTools/`. The 9-function genome requires **9 canonical verbs**. Three are missing.

### 1.1 Mega-tools (tool_*.py files)

| File | Verb today | Maps to | Upgrade action |
|---|---|---|---|
| `tool_01_init_anchor.py` | `arif_init` | 000 init anchor | NO CHANGE — 000 is pre-genome session anchor |
| `tool_02_arifos_kernel.py` | (kernel metadata) | — | NO CHANGE |
| `tool_03_apex_soul.py` | `arif_judge` | 888 Judge | **Update docstring** to "constitutional verdict + 9-function genome gate" |
| `tool_04_vault_ledger.py` | `arif_seal` | 999 Witness | NO CHANGE (still authority layer) |
| `tool_05_agi_mind.py` | `arif_think` | 333 Thinker | **Rename/refactor** to express `333 = think + architect + explore subgraph` |
| `tool_06_asi_heart.py` | `arif_observe`, `arif_memory` | 000 + 555 | **Split**: 000 → pure observer, 555 → memory+verify (NEW verb) |
| `tool_07_engineering_memory.py` | `arif_memory` (deeper) | 555 Verifier | **Merge into 555** — engineering memory = verification memory |
| `tool_08_physics_reality.py` | `arif_observe` (physical) | 000 Observer | NO CHANGE |
| `tool_09_math_estimator.py` | (compute) | — | Optional: align with 111 Explorer (compute alternatives) |
| `tool_10_code_engine.py` | `arif_forge` | 777 Executor | NO CHANGE (still executor) |
| `tool_11_architect_registry.py` | (registry surface) | 222 Architect (NEW) | **NEW verb surface** — architect = structure/build plans, distinct from forge |
| `tool_12_compat_probe.py` | `arif_route` | 444 Orchestrator | **Rename semantics** — route → orchestrate |
| `tool_13_arif_memory.py` | `arif_memory` | 555 Verifier (NEW) | **Rebind** to 555 verification, not generic memory |

### 1.2 Three new verbs (if genome is enforced at kernel level)

```
NEW: arif_explore   → 111 (path enumeration, scenario gen, search)
NEW: arif_architect → 222 (structure, plan, design — pre-execution structure)
NEW: arif_audit     → 666 (independent governance maintenance, NOT folded into 888)
```

### 1.3 Surface governance files

| File | Action |
|---|---|
| `/root/arifOS/tools_sot.yaml` | Add 3 new tools → 8 → 11 entries (or keep 8 and demote 3 to organ-level) |
| `/root/arifOS/INVARIANTS.md` | **Update §3** floor→verb mapping if kernel expands |
| `/root/arifOS/scripts/verify_tool_surface.py` | **Extend acceptance** to expect 9 or 11 verbs |
| `/root/arifOS/scripts/generate_tool_manifest.py` | Regenerate against new verb set |
| `/root/arifOS/scripts/audit_floor_coverage.py` | Add 111/222/666 floor coverage checks |
| `/root/arifOS/scripts/arif_kernel_liveness.py` | Probe each new verb liveness |
| `/root/arifOS/mcp-arifos.json` | Public MCP manifest — re-emit |
| `/root/arifOS/smithery.yaml` | Smithery MCP listing — re-emit |

---

## 2. Federation contracts — doctrine layer

| File | Action |
|---|---|
| `/root/AAA/federation/contracts/AAA_FEDERATION_CONTRACT_v0.1.2.yaml` | **Add INV-17 (Phenotype Substrate Invariant)** — genome is universal, runtimes are phenotypes; load-bearing? |
| `/root/AAA/federation/contracts/AAA_FEDERATION_CONTRACT_v0.1.yaml` | Frozen tombstone — no edit |
| `/root/AAA/federation/contracts/AAA_PRINCIPAL.md` | **Rewrite principal_agent taxonomy** to align with species/phenotype |
| `/root/AAA/contracts/PRINCIPAL_AGENT.md` | Same as above |
| `/root/AAA/federation/architecture/identity_capability_routing_enforcement.md` | Add phenotype expression weights to routing decisions |

---

## 3. Registries — discovered-truth layer

| File | Action |
|---|---|
| `/root/AAA/registries/AGENTS_UNIFIED.yaml` | **MAJOR rewrite** — collapse 17 lanes → 6 species + expression weights |
| `/root/AAA/registries/AAA_AGENTS_REGISTRY.json` | Tombstone — no edit |
| `/root/AAA/registries/AAA_FEDERATION_STATE.yaml` | Update agent definitions |
| `/root/AAA/registries/AGENT_DISCOVERY.md` | Rewrite discovery surface to species-first |
| `/root/AAA/registries/AGENT_INTELLIGENCE.md` | Rewrite |
| `/root/AAA/registries/CANONICAL_REGISTRY_POLICY.yaml` | Add species-class registry rule |
| `/root/AAA/registries/agents.yaml` | Canonical agents.yaml — collapse to 6 species |
| `/root/AAA/registries/bindings.yaml` | Re-bind skills to species, not individuals |
| `/root/AAA/registries/forge_instruments.yaml` | FI slots → species instances |
| `/root/AAA/registries/opencode_toolbench.yaml` | Annotate with expression weights (222=HIGH etc.) |
| `/root/AAA/registries/opencode_skills_alignment.yaml` | Annotate |

---

## 4. A2A agent cards — 14 harnesses + lanes + organs + extensions

### 4.1 Harnesses (`/root/AAA/a2a-server/agent-cards/harnesses/`)

```
opencode.json          → Express as OpenCode-Zen (222/333/777 HIGH)
claude-code.json       → Express as OpenCode-Zen instance
codex.json             → Express as OpenCode-Zen instance
copilot.json           → Express as OpenCode-Zen instance
copilot-cli.json       → Express as OpenCode-Zen instance
grok-build.json        → Express as OpenCode-Zen instance
kimi-code.json         → Express as OpenCode-Zen instance
aider.json             → Tombstone → species instance ref
qwen-code.json         → Express as OpenCode-Zen instance
antigravity.json       → Express as ???-Zen (vendor-specific phenotype?)
continue-cli.json      → Express as OpenCode-Zen instance
gemini-cli.json        → Express as ???-Zen
openclaw.json          → Express as OpenClaw-Zen (444/777 HIGH)
```

### 4.2 Identity lanes (`/root/AAA/agent-cards/identity/`)

```
333-AGI/      → Atlas 9-function, expression=THINK/ARCHITECT/EXECUTE
555-ASI/      → Atlas 9-function, expression=VERIFY/CRITIQUE/MEMORY
888-APEX/     → Atlas 9-function, expression=JUDGE/WITNESS (authority layer)
```

### 4.3 Organs (`/root/AAA/agent-cards/organs/`)

```
geox/wealth/well/      → Atlas 9-function, expression=earth-prism
```

### 4.4 Extensions + functions + pillars

```
extensions/ (7 files)   → rebind to species
functions/ (12 files)   → each becomes 1 of the 9 (genome functions)
pillars/ (5 files)      → constitutional layer (AAA=constitution, not species)
```

### 4.5 Per-harness AGENTS.md (4 files exist today)

```
/root/AAA/agents/_external/claude-code/AGENTS.md
/root/AAA/agents/_external/codex/AGENTS.md
/root/AAA/agents/_external/grok-build/AGENTS.md
/root/AAA/agents/_external/mesa-test-agent/AGENTS.md
```

→ Either consolidate to **one** `species/opencode/SKILL.md` or **strip** these back to thin instance pointers.

---

## 5. Prompts / boot sequences — agent-facing doctrine

| File | Action |
|---|---|
| `/root/AAA/prompts/INIT.md` | Add "species binding" to attestation Q-list |
| `/root/AAA/prompts/INIT-ZEN.md` | Add phenotype expression disclosure |
| `/root/AAA/prompts/INIT_BASIN_CLASSIFICATION.md` | Classify runtime as species instance |
| `/root/AAA/prompts/INIT_HUMAN.md` | No change |
| `/root/AAA/prompts/UNIVERSAL_BOOT.md` | Add 9-genome load step |
| `/root/AAA/prompts/ADVERSARIAL_BOOT.md` | Verify species vs species, not agent vs agent |
| `/root/AAA/prompts/SEAL.md` | Verify species-bound receipt format |
| `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` | **Add species doctrine section** |
| `/root/AAA/prompts/evening_digest.md` | Surface species expression stats |

---

## 6. GENESIS doctrine — immutable genome layer

| File | Action |
|---|---|
| `000_KERNEL_CANON.md` | **Update §3** kernel verb mapping if expanded |
| `INVARIANTS.md` | Add genome invariants |
| `FLOOR_TABLE.json` | No change (F1-F13 are constitutional, not cognitive) |
| `011_FEDERATION_AGI_SUBSTRATE.md` | **MAJOR rewrite** — this IS the genome doc |
| `030_ART_VS_KERNEL.md` | Add ART×ACT×AUTH mapping |
| `040_ACT_PLAYBOOK.md` | Add 555/666/777 stage contracts |
| `041_APEX_STACK.md` | Re-tier for species authority |
| `045_THREE_LAYER_SEPARATION.md` | Map genome→machinery→phenotype |
| `046_CONSTITUTIONAL_VSM.md` | Update if 9-function genome enforced at kernel |

---

## 7. Instructions fragments — rendered-output layer

The 11 fragments under `/root/AAA/instructions/` compose `/root/AGENTS.md`, `/root/CLAUDE.md`, and frozen per-agent adapters via `render-agents.sh`.

| Fragment | Action |
|---|---|
| `base.md` | Add species intro |
| `constitution.md` | No change (F1-F13 stay) |
| `topology.md` | Re-list organs as species, not agents |
| `agentic-architecture.md` | **MAJOR rewrite** — genome doctrine lives here |
| `autonomy.md` | Add expression-weight tier model |
| `security.md` | No change (cryptographic gates stay) |
| `build.md` | No change |
| `zen.md` | Add species-Zen |
| `pointers.md` | Update pointers to species, not individuals |
| `reality-first.md` | **Already touched in §11 commit** (harness routing) |
| `human-memory.md` | No change |

After fragment edits → **must re-run `/root/scripts/render-agents.sh`** to regenerate all adapter files.

---

## 8. Adapter render path — broken today

```
/root/AAA/src/resolvers/opencode_render.py line 155 → ❌ BROKEN
```

The drift detector itself is failing on `fb.get(...)` where `fb` is a string. **This is the canary**: before forge output can be audited via the standard drift path, the renderer must be fixed.

After fix → re-render → regenerate all per-agent `AGENTS.md` adapters → must re-run drift check.

---

## 9. Skills — ~150 of which ~10 are real

The skill registry declares **~150 logical skills**, **335 mesh sync entries** (with **2 broken + 4 drifted** today).

### 9.1 Skills that REQUIRE change

| Skill | Why |
|---|---|
| `ASI-agentic-architecture` | Must redefine "agent" = "species instance" |
| `ASI-agentic-governance` | Species governance, not agent governance |
| `ASI-agent-invariants` | Phenotype expression invariants |
| `AGI-explorer-intelligence` | **NEW behavior**: 111 Explorer as first-class |
| `AGI-plan-dag` | Align with 222 Architect verb |
| `AGI-skill-unification` | Collapse to genome functions |
| `AUDIT-skill-atlas` | Atlas by species, not by lane |
| `AUDIT-agent-skill-mesh` | Same |
| `FEDERATED_SKILLS_REGISTRY_V3.yaml` | **MAJOR rewrite** — skills bind to species, not agents |
| `SKILL_ALIAS_TABLE.json` | Same |
| `CONTRAST_ANALYSIS_2026-08-08.md` | Today's analysis (untracked, safe) |

### 9.2 Skills where species is invisible

Most skills can keep their existing form (the species boundary is invisible at skill level). Only skills that **route by lane/agent identity** require rewrite.

---

## 10. Identity walls — three profile boundaries

| Boundary | Today | Upgrade |
|---|---|---|
| arifOS kernel | 8 verbs, F1-F13 floors | 8 or 11 verbs, F1-F13 floors + 9-genome |
| AAA control plane | 17 lanes | **6 species + 6 organs + extensions** |
| Hermes profile | 335 mesh entries | Same count, rebind by species |

The cross-profile soft guard at `~/.hermes/profiles/aaa-hermes/skills/` will trigger if forge touches Hermes-owned skills.

---

## 11. Model routes — 5 routes change meaning

The 9-genome model is substrate-agnostic, but **expression weights** create new model preferences:

| Model route | Today serves | New role under species |
|---|---|---|
| `deepseek/deepseek-v4-pro` | most runtimes | OpenCode-Zen PRIMARY (222/333/777) |
| `kimi/k3` | kimi-code FI-008 | OpenCode-Zen instance (1M ctx, thinking) |
| `claude-sonnet-5` | 888-APEX judge | Authority layer, unchanged |
| `glm-5.2` | 555-ASI memory | 555 Verifier lane |
| `qwen2.5-coder:3b` | OpenCode fallback | 777 Executor fallback |

No model swap required. But `models/AGENT_MODEL_MAP.json` should add `species_binding` field per route.

---

## 12. A2A protocol surface — 12 JS modules

These don't change behavior, but their **`agent_id` strings** become species-bound:

```
/root/AAA/a2a-server/agent-discovery-routes.js   → discovery by species
/root/AAA/a2a-server/agent-card-registry.js       → species registry
/root/AAA/a2a-server/cognitive_hierarchy.js       → 333/555/888 lanes still exist as authority hierarchy
/root/AAA/a2a-server/federation_envelope.js       → add `species_id` field
/root/AAA/a2a-server/federation_gateway.js       → route by species expression
/root/AAA/a2a-server/orchestrator.js             → dispatch by species match
/root/AAA/a2a-server/mesh_coordinator.js         → species-aware mesh
/root/AAA/a2a-server/metabolizer_loop.js         → metabolism by species
/root/AAA/a2a-server/agent_lifecycle.js          → species lifecycle, not individual
/root/AAA/a2a-server/agent_lifecycle_routes.js   → same
/root/AAA/a2a-server/membrane_middleware.js      → species-aware membrane
/root/AAA/a2a-server/seal_chain.js               → species-bound seals
```

---

## 13. Receivers / sink layers

| File | Action |
|---|---|
| `/root/arifOS/VAULT999/outcomes.jsonl` (write) | New field `species_id` in sealed records |
| `/root/.local/share/arifos/carry_forward.json` | Carry `species_binding` across sessions |
| `/root/.local/share/arifos/atlas333/atlas_ledger.db` | Per-species paradox_events |

---

## 14. Testing & validation surface

| File | Action |
|---|---|
| `/root/AAA/tests/test_opencode_render.py` | Fix broken test (fb.get on str) FIRST |
| `/root/AAA/specs/agi_kernel_regression_harness.yaml` | Add 9-function genome tests |
| `/root/AAA/specs/init_soul_shadow_contract.yaml` | Update for species binding |
| `/root/AAA/scripts/aaa_drift_check.py` | Drift by species, not agent |
| `/root/AAA/scripts/validate-root-agent-config.mjs` | Validate species root config |
| `/root/AAA/scripts/verify_art_binding.py` | Verify species × ART binding |
| `/root/AAA/scripts/federation-model-sync.sh` | Sync model routes by species |

---

## 15. Public surfaces

| File | Action |
|---|---|
| `/root/AAA/public/a2a/principal-agent-taxonomy.md` | Update taxonomy to species |
| `/root/AAA/public/a2a/AAA-17-CITIZEN-ORTHOGONAL-MATRIX-2026-06-22.md` | → 6 species matrix |
| `/root/AAA/public/a2a/opencode.json` | Already touched in §11 |
| `/root/AAA/llms.json` | Refresh machine-readable surface |
| `/root/AAA/public/llms.json` | Same |
| `/root/arifOS/llms.txt` | Refresh arifOS public surface |
| `/root/arifOS/acceptance_manifest.json` | Update if kernel expands |

---

## 16. Already-landed changes (pre-forge baseline)

Codified in `8ead6de5` (2026-08-08, §11 commit):

1. `/root/AAA/a2a-server/agent-cards/harnesses/opencode.json` — `+priority: PRIMARY, replaces: [codex, claude-code]`
2. `/root/AAA/public/a2a/opencode.json` — large rewrite
3. `/root/AAA/docs/EUREKA_SIX_PLANE_EXECUTION_LOOP.md` — `+106 lines` Phenotype Substrate doctrine
4. `/root/AAA/instructions/reality-first.md` — `+68 lines` Harness Routing + Tensor + ART/ACT/AUTH gates

These are the **first wave**. The full 9-genome upgrade continues from here.

---

## Blast radius summary

```
HIGH BLAST (must change)    :  ~35 files
MEDIUM BLAST (doctrine)     :  ~25 files
LOW BLAST (regen only)      :  ~12 files (renderer outputs, manifests)
NO BLAST (transparent)      :  ~120 skills (species invisible at skill level)
```

---

## Order of operations (canonical)

1. Fix `opencode_render.py:155` first (audit cannot run without it).
2. **Load-bearing decision:** expand kernel to 9+ verbs OR keep 3 missing functions as organ-level.
3. Rewrite `AGENTS_UNIFIED.yaml` to species-first.
4. Update fragment `agentic-architecture.md` + re-render adapters.
5. Update GENESIS `011_FEDERATION_AGI_SUBSTRATE.md` (this is the genome canon).
6. Re-emit A2A public manifest.
7. SEAL the species doctrine via `arif_seal`.
8. Re-run `make prove` — full federation validation.

---

## CHAOS TRACE baseline (pre-forge, captured 2026-08-08T03:55Z)

```
arifOS    4 files dirty  HEAD 265710480  (runtime security: crypto_auth + session_auth)
AAA       14 files dirty + 3 untracked  HEAD 98a65eed (just landed §11)
HERMES    8 files dirty + 6 untracked skills  HEAD 73d68f0
A-FORGE   0
GEOX      0
WEALTH    0
WELL      0

Skill mesh sync   ok≈335, missing_or_drift=4, broken=2  ⚠️ WARN
OpenCode render   'str' has no 'get' at line 155          ❌ FAIL
Last seal chain   actor=333-AGI ts=2026-08-03T08:53Z     ⚠️ 5d stale
7 organ health    all ✅                                  ✓
FLAME free loop   ✅                                      ✓
OpenCode binary   v1.18.11 alive                          ✓

FQ = CAUTION.  Ω₀ = 0.04.  ΔS = 0 (trace only).
```

ΔS = 0. Baseline locked. Ready for forge diff.
