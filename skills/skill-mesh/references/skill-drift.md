<!-- PROVENANCE: member "skill-drift" folded into umbrella "skill-mesh" (merge-20260920, 2026-09-20) -->
<!-- original path: /root/AAA/skills/engineering/skill-drift/SKILL.md -->
<!-- archived at: /root/AAA/skills/.archive/merge-20260920/skill-mesh/skill-drift/ (body below is byte-identical to the archived original) -->
<!-- sha256 of the body below: 167bd9e9efa0e2545a36f589e06e7a55f5dec62aef843635586fb19ac97d0d2b -->
---
name: skill-drift
id: skill-drift
version: 2.1.0
description: "Drift detection, skill binding, and federated architecture management."
owner: AAA
risk_tier: medium
autonomy_tier: T1
floor_scope: [F2, F3, F4, F8, F11]
tags: [drift, audit, registry, manifest, binding, architecture, federation, skill-binding, federated, F2, F11]
capability_tier: fed-long-context
ecology_state: WARM
---

# Skill Drift — Detection, Binding & Federated Architecture

> **DITEMPA BUKAN DIBERI** — Drift is invisible until it causes a bug.

## What This Skill Is

A unified skill covering three concerns:

1. **Drift Detection** — compares live state against saved baselines and reports mismatches across tool manifests, agent cards, skill registries, and runtime-injected files
2. **Skill Binding** — discover, bind, and compose skills across all federation organs using AAA_SKILL.md orthogonal axes (Trinitarian Δ/Ω/ΦΙ + Functional)
3. **Federated Architecture** — design, validate, and manage skills with 3-layer architecture, 3-axis manifests, veto-generator separation, bootstrap signing, and CI validation gates

## When to Use

- "Check drift", "verify registry", "detect manifest drift", "tool surface audit", "runtime injection detection"
- Cross-organ synthesis tasks requiring skill composition
- Subagent orchestration requiring isolation, evidence, and floor gates
- Skill surface audits, drift detection, recursive self-forge
- Designing or validating skill architecture across a multi-agent federation
- "Skill architecture", "skill registry", "skill naming", "federated registry drift"

## When NOT to Use

- Single-organ direct MCP call (use the organ's MCP directly)
- Irreversible actions without explicit 888_HOLD + F13 (T3)
- Bypassing organ lanes (GEOX is EVIDENCE_ONLY, WELL is REFLECT_ONLY, WEALTH is advisory)
- Creating a single new skill from scratch (use `skill-creator`)

## §1. DRIFT DETECTION

### Drift Dimensions

1. **Build vs Runtime Manifest Drift** — Canonical drift check via `arifOS/arifosmcp/runtime/manifest.py` (`build_manifest` vs `runtime_manifest`). Live witness: `GET :8088/health` → `layer_health.runtime.{source_commit, built_commit, runtime_matches_build, deployment_attestation}`. **If both commits read `null`, the honest verdict is `UNKNOWN`, not `degraded`** (pitfall 11).
2. **Tool Manifest Drift** — Live MCP tools vs registered tools vs agent card references
3. **Skill Registry Drift** — SKILL_ALIAS_TABLE vs actual directories vs agent card skill IDs
4. **Agent Card Drift** — Card skill IDs vs existing skill directories
5. **Schema Drift** — Tool input schemas vs documented schemas
6. **Floor Drift** — Declared floor_scope vs actual floor enforcement
7. **Verdict Taxonomy Drift** — `verdict` / `effective_verdict` emissions vs `CANONICAL_VERDICTS`
   (OBSERVE_ONLY|SEAL|SABAR|VOID|HOLD|888_HOLD). **Read the instrument caveat before reporting this
   as a violation rate** — the key carries three vocabularies and the metric as written can never pass.

### Detection Pipeline

1. **Snapshot** — Capture current state of all registries
2. **Compare** — Diff against saved baseline (or last-known-good)
3. **Classify** — Each mismatch: CRITICAL (breaks routing), WARNING (orphan), INFO (cosmetic)
4. **Report** — Structured drift report with fix recommendations
5. **Escalate** — CRITICAL drift → 888_HOLD before any SEAL operation

### Runtime-Injected Files

Some organ services modify files at runtime. Known patterns:
- **WELL `index.html`**: WebMCP adapter injected on service start → dirty after commit
- **arifOS session-state**: Runtime state files that change during operation

When dirty after clean commit: check if injected content was already committed → if yes, re-commit; if no, actual drift.

### Baselines

> All paths re-probed on disk 2026-09-18. The three `arifOS/runtime/*` paths this list used to carry
> were **dead** — the package was nested under `arifosmcp/` and the skill was never folded back.
> A drift detector that cannot find its own baselines is the purest instance of what it detects.
>
> **Compartment tagging verified 2026-09-19 (Codex FI-005):** All 17 fragments in /root/AAA/instructions/
> carry <!-- compartment: PUBLIC --> + <!-- loaded_by: render-agents.sh -->. Default-Deny Rule = deleted.
> Old Observation Protocol = deleted. F13/SOVEREIGN = universal terms (not A2H-only). AGENTS.md = 591 lines.

- **Canonical drift check**: `/root/arifOS/arifosmcp/runtime/manifest.py` (`build_manifest` vs `runtime_manifest`)
- Tool registry: `/root/arifOS/arifosmcp/tool_registry.json` — and a **second** copy at
  `/root/AAA/registries/tool_registry.canonical.json`. The two disagree by one tool; see pitfall 8.
- Agent cards: `/root/AAA/a2a-server/agent-cards/` (42 cards as of 2026-09-18)
- Skill alias: `/root/AAA/skills/SKILL_ALIAS_TABLE.json` — the ONLY canonical copy. Verify by hash;
  24 files with this name exist on the box across 5 distinct hashes (pitfall 3).
- MCP surface: Live `tools/list` from each organ. The **live wire surface is 8 tools**, not 66 —
  `hermes_*` / `forge_*` are gated behind `ARIFOS_MCP_EXPOSE_DEV_TOOLS=true` (pitfall 9).
- Verdict taxonomy: `/root/arifOS/arifosmcp/runtime/verdict.py` — `CANONICAL_VERDICTS` = 6 values,
  but `_LEGACY_VERDICT_MAP` only normalises 13 of the 75+ values seen in the wild (dimension 7).
- Floor enforcement: `/root/arifOS/scripts/audit_floor_coverage.py` — **run it before claiming floors
  are enforced**; it reports 2/13 coverage and exits 0 regardless (pitfall 10).
- Census (skill side): `/root/scripts/skills-census.py`
- **Current receipt:** `${FORGE_WORK:-/root/forge_work}/2026-09-18/SKILL-DRIFT-REPORT-2026-09-18.md`

## §2. SKILL BINDING

### Overview

This meta-skill provides the single entry point for any agent to interact with the federation's skill surface in a constitutionally governed way. It implements the unified contract in `/root/AAA/contracts/AAA_SKILL.md`.

### Inputs

- intent: string (natural language task)
- organs: list (optional filter: ["GEOX", "WEALTH", "WELL", "arifOS", "A-FORGE", "Hermes-Ω"])
- autonomy_tier: "T1" | "T2" | "T3"
- max_parallel: int (default 3)
- required_evidence: bool

### Procedure

1. Probe capability surfaces via arifos-mcp-federation + organ MCPs
2. Map intent to orthogonal axes (Trinitarian + Functional)
3. Retrieve candidate skills with full contracts (subagent spawn schema, evidence_required, risk_band, floor_scope)
4. Compose DAG or subagent swarm with isolation (worktree for code, container for compute)
5. Verify floors (F1 reversible-first, F7 humility, F11 audit receipt)
6. Return bound plan + evidence bundle

### Output Format

```json
{
  "orthogonal_map": {"trinitarian": "Δ|Ω|ΦΙ", "functional": ["Governance", "Evidence", ...]},
  "skills_bound": [{"id": "...", "organ": "...", "floor_scope": [...], "subagent_contract": {...}}],
  "composed_plan": "DAG or subagent list",
  "evidence_bundle": {"provenance": "...", "uncertainty": "P50: ..."},
  "floor_receipt": "F1 pass, F7 humility applied, F11 auditable",
  "escalation": "none | 888_HOLD | F13"
}
```

### Forbidden Actions

- Direct organ execution without binding + lease
- Omitting orthogonal tags or subagent contract in output
- T3 actions without 888_HOLD + F13
- Fabricating epistemic labels

## §3. FEDERATED ARCHITECTURE

### The 3-Layer Architecture

```
Layer 1: SUBSTRATE (how agents think) — always loaded, agent-agnostic
Layer 2: KNOWLEDGE (what agents know) — always loaded, veto layer
Layer 3: DOMAIN (where agents operate) — load on demand, per-agent
```

### The 3-Axis Manifest

Every skill must declare three axes:

| Axis | Question | Test |
|---|---|---|
| **Invariant** | What's timeless? | Survives tool/org changes? |
| **Bridge** | What connects? | Linked to kernel verbs + other skills? |
| **Contrast** | What is this NOT? | Clear boundaries with neighbors? |

**Anti-drift rule:** If a skill has no invariant → kill. No bridge → isolate. No contrast → merge.

### Veto-Generator Separation

- **Domain skills = GENERATOR** — produce hypotheses. Authority: ADVISORY.
- **Universal skills = VETO** — enforce boundary conditions. Authority: BINDING.
- **Sovereign = TRUTH** — ratifies axioms the framework cannot verify.

Rule: Domain generates, universal vetoes. Never invert.

### Naming Convention: `{domain}-{verb}`

All lowercase kebab-case. Max 3 words. Domain prefix mandatory.

Domains: `kernel`, `geo`, `wealth`, `well`, `forge`, `a2a`, `meta`, `mem`, `sec`, `ops`, `dev`, `research`

### CI Validation Gates

1. **manifest_schema** — validate against schema
2. **skill_hash_integrity** — recompute hashes, compare to manifest
3. **three_axis_completeness** — invariant/bridge/contrast all present
4. **dependency_acyclicity** — no circular dependencies
5. **veto_generator_separation** — substrates don't generate, domains don't veto
6. **adversarial_contradiction** — inject contradictions, verify veto catches
7. **bootstrap_self_host** — deterministic self-host test
8. **signature_present** — at least 1 valid signature
9. **skill_count_bounds** — flag if growing beyond threshold
10. **entropy_budget** — verify entropy non-increasing across boot phases

### EUREKA-ZEN Workflow: Federation-Wide Skill Lifecycle

**Phase 1 — Deep Scan & Chaos Purge:** Map ALL surfaces, identify duplicates, archive by renaming, update alias table.

**Phase 2 — Architectural Alignment:** Refactor skills to the cognitive engine that will execute them (Claude Code / Codex / Hermes).

**Phase 3 — Forge Gaps:** Cross-reference agent-card skill IDs against skills on disk. Missing = architectural gaps.

> **BLOCKED as of 2026-09-18.** 731 of 927 card skill references resolve to nothing. Running this
> phase would forge 337 phantom skills. **Fix the cards first** (D-1 in the current receipt), then run
> the phase. A gap-forge loop fed by unresolvable IDs is a fabrication engine.

**Phase 4 — KERNEL Substrate Injection:** Every agent card must inherit arifOS baseline physics.

**Phase 5 — Seal:** Verify alias table synced, federation health green, write seal payload to VAULT999.

### Agent Loading Matrix

| Agent | Substrates | Knowledge | Domains |
|---|---|---|---|
| Full (Hermes) | 6 | 3 | research, meta, geo, wealth, well |
| Coder (Claude) | 6 | 3 | dev, forge, ops, meta |
| Metabolizer (OpenClaw) | 4 | 3 | mem, ops, a2a |
| Executor (Codex) | 6 | 3 | dev, forge, ops |
| Minimal (Kimi) | 6 | 3 | dev, forge, ops, meta, a2a |

### Three Gödelian Paradoxes

| Paradox | Mitigation |
|---|---|
| **Bootstrapping** — loader needs skills, skills need loader | Firmware primitive + signed manifest |
| **Compression** — universal ≠ derivable from domain | Veto pattern: universal constrains, domain generates |
| **Authority** — framework validates structure, not truth | External ratification: sovereign signs the truth |

### Pitfalls

1. **Same-content skills with different names** — choose FORGE-* as canonical
2. **Agent cards rot silently** — audit cards against live config monthly. Measured 2026-09-18:
   **731 of 927 card skill references resolve to no body** (285 compound-drift through dead alias
   rows, 337 pure phantoms). The rot mechanism is a stale skill-id list **copy-pasted into five
   federation cards** — one list, propagated by copy, never re-validated. Phase 3 (forge gaps) must
   NOT run against this card set: it would forge 337 phantoms.
3. **SKILL_ALIAS_TABLE copies** — not 3. Measured 2026-09-18: **24 files, 5 distinct sha256**, three
   of them on live surfaces an agent could read (opencode copy 6 weeks stale, `/opt/aaa/app` copy
   stale). Canonical is `/root/AAA/skills/SKILL_ALIAS_TABLE.json`; verify by hash every time — the
   pitfall's *instruction* was right, its *number* was the thing that rotted.
4. **Granularity gap** — counts disagree by design, so *always name the source*. Measured 2026-09-18:
   V3 registry `total_skills` 95 · BOOTSTRAP `universal_skills` 9 · alias rows 164 · census canonical
   706 / loadable 451 / whole_mesh 801. The old "64 vs 209" figures are dead. Use registry for layer
   classification, census for disk truth, cards for per-agent claims — never one for another.
5. **Sibling-agent file conflicts** — use `skill_manage(action='patch')` for targeted edits
6. **Behavioral vs Enforcement confusion** — behavioral governance alone is "vibe-based"; enforcement
   layer must survive a system prompt rewrite
7. **A loose regex manufactures a catastrophe.** A sweep for out-of-set verdicts returned 29,886 hits
   with `STABLE`/`CRITICAL` on top — because `"?verdict"?` also matched the tail of
   `"overall_verdict"`. With a negative lookbehind the number was 856. **Anchor the key boundary**
   (`(?<![A-Za-z0-9_])`) and sample one raw line before believing any detector count.
8. **Two artifacts both named "canonical" is a two-master defect.** `arifosmcp/tool_registry.json`
   (66 tools) vs `AAA/registries/tool_registry.canonical.json` (65) differ by `arif_telegram_send`.
   Body-identical otherwise, 5 days apart. Treat any file whose *name* asserts canon as unverified
   until diffed against its twin.
9. **A registered tool that is not live is not drift.** The live `:8088` wire surface is **8** tools;
   the registry holds 66 because `hermes_*` / `forge_*` are gated behind
   `ARIFOS_MCP_EXPOSE_DEV_TOOLS=true`. Reporting "58 missing tools" is a false positive — check the
   namespace ruling in `constitutional_map.py` before flagging.
10. **Some instruments cannot fail — that is itself the drift.** `audit_floor_coverage.py` reports
    **2/13** tools calling the floor enforcer, against a declared invariant that all 13 floors appear
    on ≥2 tools each, and then **exits 0**. No cron, no CI gate. Run the instrument, then ask who
    closes its output. Same class as any gate whose FAIL goes to a log nobody reads: detection without
    `{owner, deadline, timeout→SYNCHRONIZATION_FAULT}` is not governance.
11. **A drift verdict with `null` on both sides is not a measurement.** `/health` returns
    `status: degraded`, `deployment_attestation: "drift"`, `runtime_matches_build: true`, and
    `source_commit: null` + `built_commit: null`. `a != b` is unevaluable when both are null. When
    the attestation is unreadable, the honest state is `UNKNOWN` — not `degraded`.
12. **Runtime-injected-file drift must be measured, not assumed.** WELL `index.html` is the named
    case but measured **clean** (WELL dirty=0); AAA 55 / WEALTH 3 / arifOS 1 dirty are ordinary churn.
    Re-check `git status --porcelain` per repo instead of inheriting the example.
13. **Glued `---#` frontmatter corrupts YAML parsing across an entire skill library.** When a
    skill-forge tool emits `---# Heading` (closing `---` fused to first markdown heading) instead of
    `---\n# Heading`, the YAML parser treats the heading as a YAML key and raises
    `could not find expected ':'`. This is invisible to humans (skill renders fine) but breaks any
    agent that parses frontmatter (Codex skips 88+ skills). Detection: validate YAML frontmatter
    across all skills with `yaml.safe_load()` — any exception is a corrupted frontmatter. Fix:
    split `---#` into `---\n#` on the affected line. Batch fix: find lines matching `^---[^-]`
    within the first 80 lines of SKILL.md files where line 1 is `---`, then insert a newline
    after the first three dashes.
14. **Skill description length has a context budget ceiling.** When total description chars across
    all loaded skills exceed ~110KB, Codex truncates descriptions to fit. A single skill with a
    2,000+ char description is fine; 587 skills averaging 186 chars each is 109KB — right at the
    edge. Keep descriptions under 200 chars. If the library is large (>400 skills), target 120
    chars. The truncation is silent — agents still see the skill name but lose the trigger
    information that tells them WHEN to load it.

### Dimension 7 — read the instrument before the metric

`CANONICAL_VERDICTS` (6 values) is real and imported, not merely documented. But the `verdict` key
carries **three vocabularies**, and this is the actual drift:

| Vocabulary | Values | Status |
|---|---|---|
| Constitutional verdict | OBSERVE_ONLY SEAL SABAR VOID HOLD 888_HOLD | the canonical set |
| Stage verdict | `CLAIM_ONLY` (000/333 always emit), `999_SEAL` | **declared schema const** — not drift |
| Governance tier | `READONLY` (`RiskTier`, `organ_governance.py:46`), `ALLOW`, `DENY` | **cross-vocabulary leak into a `verdict` field** |

`_LEGACY_VERDICT_MAP` normalises only **13** of the **75+** values observed in the wild. So
`ALLOW/DEGRADED/FAIL/ERROR/BLOCKED/PARTIAL/UNKNOWN` are mapped-on-read (not drift), while
`CLAIM_ONLY / READONLY / READY_READONLY / COMPLETE / SEAL_OVERRIDE / SEAL_AMEND / 999_SEAL` pass
through un-normalised.

**A metric that can never pass is as useless as a gate that can never fail.** Report this dimension
as *vocabulary coverage* (mapped ÷ observed), never as a violation count against 6.

## Floors

- F2 TRUTH: Report only what is actually observed
- F3 PEACE: No unnecessary disruption during drift correction
- F4 CLARITY: Drift report must be actionable, not noise
- F8 GENIUS: Skill binding must optimize for capability, not convenience
- F11 AUDITABILITY: Every drift check logged with timestamp and findings

## Current receipt

`${FORGE_WORK:-/root/forge_work}/2026-09-18/SKILL-DRIFT-REPORT-2026-09-18.md` — 10 findings
(D-1 card drift + D-5 floor drift CRITICAL), 1 dimension recorded as PASS, 2 self-corrected false
findings disclosed, and an explicit §8 list of what was NOT witnessed (schema drift = UNKNOWN;
`/opt/aaa/app` tree unclassified).

Companion (skill-mesh lane): `${FORGE_WORK:-/root/forge_work}/2026-09-18/SKILL-INVENTORY-AUDIT-2026-09-18.md`
— the `skill-inventory` meta-skill's F-1…F-11. Read both together: they probe different surfaces of
the same mesh and their numbers are deliberately not merged.

## Retired-name landing (name retired, mode live here)

Trigger phrases carried forward when the `skill-portfolio-audit` identity was retired (2026-09-19; frozen body at
`/root/AAA/skills-retired/2026-09-19-v2-portfolio-audit/skill-portfolio-audit/SKILL.md`).

| Retired name | Retired trigger phrase (verbatim) | Live section here |
|---|---|---|
| `AUDIT-drift-detector` | "find drift across surfaces", "find drift", "drift detector" | §1 DRIFT DETECTION (Drift Dimensions 1–7 · Detection Pipeline · Baselines) |

This was the `mode=drift` row of the retired `skill-portfolio-audit`. The retired body's Drift Dimensions and
Detection Pipeline appear verbatim in §1 of this file; its absorbed pre-merge copy remains readable at
`references/absorbed-AUDIT-drift-detector.md` under the frozen path above.
