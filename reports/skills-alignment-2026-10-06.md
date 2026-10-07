# Skills Alignment Map — HERMES ↔ AAA Agents ↔ Cross-Organ Domains

**Mission:** F13 sovereign directive 2026-10-06 — "map all skills from HERMES and do proper alignment with AAA agents and cross-organ domains. Reduce any chaos redundants. Make sure skills flow connected to each other."
**Executor:** FI-008 (kimi-code) · **Mode:** OBSERVE → EXECUTE (reversible only) · **Session:** SEAL-cef617cbd37c4439
**Method:** 3 parallel read-only mapping agents (registry infra / agent roster / HERMES capabilities) + live registry probes (`hermes_registry_status` full) + git-history verification before every mutation.

---

## 1. The core finding

**HERMES's entire meaning-integrity surface (15 MCP tools, 13 capability families) had ZERO skill-mesh coverage.** Of 683 top-level skills, exactly ONE (`persona-triad-reasoning`) referenced a live HERMES tool. The 29 `hermes-*` entries are runtime plumbing (telegram/gateway/session/state-db) — necessary, but nobody could discover "how do I check a claim about a person?" by skill lookup. **Fixed:** `hermes-meaning-integrity` connector skill forged (see §2).

## 2. HERMES capability map (the 13 families → tools → flow-connections)

Canonical index: `/root/AAA/skills/hermes-meaning-integrity/SKILL.md`

| Family | Question | Live tool | Flows into (skills / canon / organ) |
|---|---|---|---|
| claim-integrity | What exactly is the claim? | `hermes_claim_validate` | verify-gate · claim-receipt-discipline · testimony-gate |
| provenance | Where from? | `hermes_claim_validate` | source-type-promotion-gate · CHRON episodes |
| perspective-sovereignty | Whose perspective? | `hermes_perspective_scope` | persona-triad-reasoning · hermes-persona-alignment |
| qualia-boundary | What's interior-only? | `hermes_qualia_boundary` | care-governor H5 · human-substrate · agentic-anthropology |
| paradox-tolerance | Two truths coexist? | `hermes_contradiction_scan` | contradiction-as-evidence · CHRON attention-debt |
| divergence-detection | Declared ≠ revealed? | `hermes_contradiction_scan` | representation-reality-invariant · AUDIT-repo-reality |
| counterstory | What else explains it? | `hermes_counterstory_test` | persona-triad-reasoning · APEX-humility-godel · hermes-asi-intelligence D1 |
| multi-principal | Org ≠ one mind | `hermes_perspective_scope` + `hermes_handoff_package` | institutional-forensic-analysis · WEALTH capital_polix |
| uncreated-futures | Answer exists yet? | `hermes_uncreated_classify` | OPEN-QUESTIONS lane · CHRON predictions |
| consent-boundaries | Accessible ≠ permitted | `hermes_handoff_package` | consent canon · WELL well_guard_dignity |
| moral-physics | Where do costs land? | `hermes_moral_physics` | WEALTH capital_entropy · dalio-distillate-witnessed-debt |
| institutional-decay | Truth metabolised? | `hermes_institutional_decay` | hermes-asi-intelligence D5 · anti-collapse-doctrine |
| reality-grounding | Doc = execution? | `hermes_reality_grounding` | AUDIT-repo-reality · readme-truth-check · live-probe-audit-pattern |
| *(gate)* voice law | Outbound human text | `hermes_makcik_render` | SOUL.md KALIBRASI · makcikgpt |
| *(gate)* posture | Pre-turn witness | `hermes_witness_signal` | witness-mode canon |
| *(infra)* | memory / SOT | `hermes_retrieve` · `hermes_scar_wisdom` · `hermes_registry_status` | hermes:// 31 resources · AAA scars · F1 |

**Verdict routing (five-verb law, HERMES never judges):** verdicts → arifOS `arif_judge` · mutations → A-FORGE · readiness → WELL · consequence math → WEALTH · temporal truth → CHRON.

## 3. AAA agent alignment (skill→agent SOT: `ZEN_SKILL_MANIFEST.json`, 27 agents)

New bindings added 2026-10-06:
- **`hermes-meaning-integrity`** → hermes-asi · 555-ASI · 888-APEX · kimi-code · makcikgpt
- **`hermes-align`** (F13-sealed, was hermes-store orphan) → hermes-asi

Mandatory-call discipline (in connector skill):
| Agent | Must call |
|---|---|
| hermes-asi / hermes bridge | makcik_render + witness_signal every human-facing turn |
| 555-ASI (evidence) | claim_validate + counterstory_test before findings |
| 888-APEX (judge input) | qualia_boundary + moral_physics + institutional_decay before verdicts |
| coding FIs (kimi/opencode/claude/codex) | reality_grounding for doc-vs-code; scar_wisdom pre-mutation |
| makcikgpt | makcik_render gate |

Lane roles (from `_lanes/`, HEXAGON v5): 333-AGI Δ mind · 555-ASI Ω heart/evidence · 777-forge governed execution · 888-APEX judgment (666-AUDITOR = sub-mode of 888, not an agent).

## 4. Cross-organ domain map

| Organ | Port | Owns | Skill-bridge |
|---|---|---|---|
| arifOS | 8088 | verdicts, kernel, memory | kernel-bind · arifos-evals · hermes→arif_judge routing |
| A-FORGE | 7071 | mutations, forge verbs | FORGE-* suite (50 skills, aforge profile) |
| GEOX | 8081 | geoscience truth | geox-basin/prospect/well-log-qc (organ-native homes) |
| WEALTH | 18082 | consequence/capital | wealth-capital-primitives + moral-physics flow |
| WELL | 18083 | readiness/dignity | well-substrate-readiness + consent flow |
| AAA | 3001 | knowledge, A2A cards | agent-cards · this skill mesh |
| HERMES | 18087 | meaning-integrity, bridge | hermes-meaning-integrity (new) |
| CHRON | — | temporal truth | predictions ↔ uncreated-futures flow |
| FRAME | 18085 | independent witness | drift probes (frame_probe caveat: see hermes-federation-audit §11) |

## 5. Chaos reduced (every fix, before → after)

| # | Defect | Fix | Evidence |
|---|---|---|---|
| 1 | 15 HERMES tools invisible to mesh | Forged `hermes-meaning-integrity` connector + registry `hermes-core` group | `/root/AAA/skills/hermes-meaning-integrity/SKILL.md` |
| 2 | `hermes-asi-intelligence`: 6 dead tool names | Remapped to live tools (claim_validate, qualia_boundary, counterstory_test, moral_physics, institutional_decay, witness_signal) with in-file remap note | SKILL.md remap block |
| 3 | `hermes-pdf-intelligence` two-writer (AAA full copy vs .hermes tombstone) | .hermes side → symlink to AAA canonical (commit cb66bcc7); tombstone preserved at `.hermes/skills/.tombstone-hermes-pdf-intelligence-20261006.md`; routing note added to canonical frontmatter | `ls -la` receipt |
| 4 | `hermes-align` F13-sealed orphan invisible to federation | Symlinked into AAA store | `/root/AAA/skills/hermes-align` |
| 5 | `hermes` namespace manifest claimed 2 dead children | Manifest truth-fixed (children → web-ops, migration noted) | NAMESPACE.md |
| 6 | ZEN (27 agents) vs MASTER (26) map drift | MASTER regenerated as mirror of ZEN; copilot-cli now present; both 27 agents / 286 skills | verify block in session log |
| 7 | Registry V3 lies: count 183 vs 100 listed; total 95 vs 112 | Reconciled: 102 listed = count 102; total 114 (=8+4+102) | YAML re-parse ✓ |
| 8 | Alias figures stale (164/133/31, dead 91) | Re-measured: 183 rows / 105 live / 78 tombstone / 104 resolvable / **1 dead → fixed → 0 dead** (ops-mcp-probe re-pointed to canonical) | SKILL_ALIAS_TABLE.json |
| 9 | 2 broken symlinks (census verdict FAIL) | geo reference retargeted to cold-archive original; census re-run: **broken_symlinks 0, verdict WARN** | census witness_hash 6760bc68d5a14ee4 |
| 10 | `MASTER_SKILL_INVENTORY_REPORT.json` triple-stale (Jul-26, 64 skills) | Archived; pointer file redirects to live SOTs | `.kimi-code/skills/.archive/` |
| 11 | 3 stray `.bak` files in kimi skills root | Moved to `.archive/` | ls receipt |

## 6. Residual debt (FLAGGED, not fixed — F13-class or deeper-scope)

1. **Census WARN: 34 duplicate-identity groups (62 skills)** claiming same capability — needs per-group verdicts (merge/tombstone), a full mission by itself.
2. **`BOOTSTRAP_MANIFEST.json`** — **RESOLVED 2026-10-06: F13 binary [2] BIAR MATI + tombstone.** Probe: expires enforced by nothing; signed body stale since 2026-08-07 corrections; 9 substrate skills canonically live in registry layers. Sovereign signature (root-arif-888) preserved byte-for-byte at `skills/.archive/bootstrap-manifest-retired-20261006/`; canonical path now carries tombstone pointer; LOAD_SPEC retired; CI-001/007/008 dormant; alias-table path repointed. No signature tampering, no deletion.
3. **Ghost/conflicting agent defs:** `kernel-scribe` (yaml def, no artifact) · opencode ×3 definitions · claude-code ×2 · antigravity ×3 · FI-slot collisions (grok-build vs aider FI-007; skill-auditor vs continue-cli FI-009) between ROOT_AGENT_CONFIG / _docs/AGENT_REGISTRY / skill-auditor identity.
4. **`ROLE_AGENTS_OPencode.yaml`** config/context paths missing on disk.
5. **Exposure asymmetry:** ~54 hermes-native namespace dirs + 12 organ-store symlinks visible to HERMES but not in AAA top level (mesh direction is hermes-mirrors-AAA; acceptable, but orphans like `hermes-align` were invisible — now fixed for the one that mattered).
6. **`HERMES-opencode-protocol` vs `hermes-opencode-protocol`** — deliberate documented case-alias, byte-identical; left as-is.
7. **skills_index.federation.json** (Sep-22, 754 skills) — no generator/consumer; candidate for archive next sweep.

## 7. Canonical sources of truth (after this mission — ONE per question)

| Question | SOT | Mirrors |
|---|---|---|
| Physical skill inventory | `SKILLS_INDEX.json` (v2, single_writer) + census block in registry V3 | skills_index.json (single-root, regenerable) |
| Logical registry | `FEDERATED_SKILLS_REGISTRY_V3.yaml` layers (114 names) | — |
| Skill → agent | `ZEN_SKILL_MANIFEST.json` (27 agents) | MASTER_SKILL_TO_AGENT_MAP.json (generated mirror) |
| Aliases | `SKILL_ALIAS_TABLE.json` (183 rows, 0 dead) | symlinked everywhere |

**Verification:** YAML re-parse ✓ · census re-run ✓ (0 broken, WARN only for pre-existing dup groups) · 105/105 live aliases resolve ✓ · ZEN/MASTER agent counts agree ✓ · all stores git-reversible (AAA, HERMES, .kimi-code repos; no commits made — trees were pre-dirty, changes left staged-in-worktree for the next git sweep).

DITEMPA BUKAN DIBERI ⚒️
