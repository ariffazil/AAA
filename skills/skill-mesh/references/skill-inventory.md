<!-- PROVENANCE: member "skill-inventory" folded into umbrella "skill-mesh" (merge-20260920, 2026-09-20) -->
<!-- original path: /root/AAA/skills/engineering/skill-inventory/SKILL.md -->
<!-- archived at: /root/AAA/skills/.archive/merge-20260920/skill-mesh/skill-inventory/ (body below is byte-identical to the archived original) -->
<!-- sha256 of the body below: 2ef28be9182b9a0dfd2d8612605a1eabc311ce8c2e1e7d8fdba6936d6dfbef55 -->
---
name: skill-inventory
id: skill-inventory
version: 2.1.0
description: "Unified skill inventory, audit, mesh health, and cross-surface contrast."
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F7, F9, F11]
tags: [meta, skill-atlas, gap-detection, routing, federation, inventory, multi-harness, audit, mesh, sync, version, divergence, unification, alias]
capability_tier: fed-long-context
ecology_state: WARM
---

# Skill Inventory — Unified Audit, Atlas, Mesh Health & Unification

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
> **The mesa above the terrain. See the whole. Find the missing. Route the right.**

## What This Skill Is

This is the **meta-skill** — a skill about skills. It provides:

1. **Inventory** — live multi-surface counts (not a frozen number)
2. **Gap detection** — missing, thin, dual-named, harness-divergent
3. **Routing** — given a task *and harness*, which skill(s) to load
4. **Health scoring** — freshness, collision, catalog vs view drift
5. **Cross-harness unification** — AAA catalog ↔ CLI agent views
6. **Mesh sync** — per-skill SYNC / DIVERGED / MISSING_FROM_X status
7. **Cross-surface contrast** — 10-agent audit with rot classification

It does NOT execute, judge, or seal. It classifies, routes, and illuminates.

**Iron rule:** AAA is the catalog. Harnesses are views. Do not invent parallel catalogs.

## When to Use

- Reviewing the overall capabilities, naming conventions, and performance of the active skill portfolio
- A new skill is drafted or proposed for installation
- An existing skill's SKILL.md is updated or modified
- Executing portfolio maintenance checks to clean up outdated APIs, dead links, or legacy documentation
- Tuning the triggering accuracy of skills when experiencing trigger drift
- Answering "are my agents in sync right now?"
- Auditing skill mesh, resolving dual names, rebinding harness skills
- Before claiming skill inventory is complete

## When NOT to Use

- Creating a single new skill from scratch (use `skill-creator`)
- Linting individual skill trigger statements (use `skill-creator` linter mode)
- The task is a general system performance audit unrelated to skills

## §0. MULTI-HARNESS UNIFICATION

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

### Live inventory — WITNESS, NOT TRUTH (re-probe before every claim)

> Counts below are a dated witness (2026-09-18). **Do not inherit them.** Any sentence of the form
> "the mesh has N skills" must be produced by the probe in the right-hand column **in the same
> session as the claim**. The previous version of this file carried ~108 / 64 / 133 frozen numbers
> for ~2 months; the live mesh had moved far past them.

```bash
AAA_HOME=${AAA_HOME:-/root/AAA}
# the ONE canonical census — writes disk_reconciliation + witness_hash, exit 1 on disagreement
python3 /root/scripts/skills-census.py            # human    | --json | --write | --quiet
# mesh propagation + CI gate (exit 1 = drift/broken)
bash $AAA_HOME/skills/scripts/skill-mesh-sync.sh --check
# raw enumeration with correct depth (skill dirs nest up to 8 deep)
find /root/AAA/skills -name SKILL.md | wc -l
```

| Surface | Live (2026-09-18) | Role |
|---------|--------------------|------|
| AAA canonical `${AAA_HOME:-/root/AAA}/skills` | 629 raw `find` SKILL.md · census 706 canonical / 634 physical | **Catalog / SOT** |
| Hermes view `~/.hermes/skills` | 452 indexed / 451 loadable | copy |
| Hermes profile `~/.hermes/profiles/aaa-hermes/skills` | 222 | copy (census-witnessed) |
| install profile `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills` | **487** | **NOT witnessed by the census** |
| overlays: kimi / qwen / opencode / gemini | 109 / 28 / 18 / 12 (167 local) | harness-local |
| `~/.grok` · `~/.claude` · `~/.codex` · `~/.agents` | symlink → AAA (view) | view, never counted twice |
| `whole_mesh_skills` | 801 | **lower bound — see §1 note** |
| V3 registry | `total_skills: 95`, `logical_registry_count: 95` | short-name registry |
| Alias table `aliases[]` | **164 rows** (124 RESOLVED · 7 FORGED · 1 ALIAS_RESOLVED · 1 active · 31 TOMBSTONE) | the registry's `alias_table_rows: 133` is **stale** |
| duplicate identity | 29 groups / 81 skills (24 re-implementations) | dedupe candidates |
| shells / diverged / broken symlinks | 2 / 4 / 5 | shells = indexed dir with no SKILL.md |

**The three AAA numbers disagree on purpose** — 629 raw `find`, 634 physical, 706 canonical — because
census counts are symlink-aware and carry their own exclusion rules. Report *which command produced
the number* alongside the number. A count without its command is a claim, not a measurement.

**Current receipt:** `${FORGE_WORK:-/root/forge_work}/2026-09-18/SKILL-INVENTORY-AUDIT-2026-09-18.md`
(11 classified defects F-1…F-11 with command-level evidence).

### Canonical artifacts

| Artifact | Path |
|----------|------|
| Alias table | `${AAA_HOME:-/root/AAA}/skills/SKILL_ALIAS_TABLE.json` |
| Mesh sync | `${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh` |
| **Canonical census** | `${AAA_HOME:-/root/AAA}/skills/scripts/../` → `/root/scripts/skills-census.py` (cron 4x/day, `--write`) |
| Dead-pointer sweep | `/root/scripts/skill-entropy-gate.py` (cron 4x/day, `--quiet`) — log `/var/log/arifos/skill-entropy.log` |
| V3 registry | `${AAA_HOME:-/root/AAA}/skills/FEDERATED_SKILLS_REGISTRY_V3.yaml` |
| BOOTSTRAP manifest | `${AAA_HOME:-/root/AAA}/skills/BOOTSTRAP_MANIFEST.json` |
| Historical receipt | `${AAA_HOME:-/root/AAA}/skills/docs/SKILL-UNIFICATION-COMPLETE-2026-07-12.md` |
| **Current receipt** | `${FORGE_WORK:-/root/forge_work}/2026-09-18/SKILL-INVENTORY-AUDIT-2026-09-18.md` |
| Hermes bridge | `${AFORGE_HOME:-/root/A-FORGE}/forge_work/2026-07-12/HERMES-V3-DOMAIN-BRIDGE.md` |

### Resolve a V3 short name

```bash
python3 -c "import json;d=json.load(open('${AAA_HOME:-/root/AAA}/skills/SKILL_ALIAS_TABLE.json'));
print([a for a in d['aliases'] if a['v3_name']=='meta-atlas'][0])"
```

### Mesh hygiene

```bash
# dry-run
bash ${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh
# apply missing links
bash ${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh --apply
# CI / pre-seal
bash ${AAA_HOME:-/root/AAA}/skills/scripts/skill-mesh-sync.sh --check
```

### BOOT gate

```
BIND → GROUND → ROUTE → RECALL → VERIFY → SEAL → KNOW → READY
```

Only after **READY** may domain skills load.

**BOOTSTRAP manifest — read it correctly:**

```bash
python3 -c "import json;d=json.load(open('/root/AAA/skills/BOOTSTRAP_MANIFEST.json'));\
print(len(d['universal_skills']))"   # → 9
```

- ⚠️ The array key is **`universal_skills`**, *not* `skills`. A `d['skills']` read returns empty and
  produces a false "the manifest is empty" claim. Field-name traps fabricate findings.
- The 9 universals live at `substrate/{kernel-bind,observe-ground,route-dispatch,memory-manage,verify-gate,audit-seal}`,
  `know-physics`, `know-math`, `knowledge/know-language` — all resolve (verified 2026-09-18).
- `_runtime_corrections` remaps 2 verbs that are **not** registered MCP tools:
  `arif_verify → arif_judge`, `arif_compose → arif_think`. Consume the override, never the signed body verb.
- `status: SIGNED`, `expires: 2026-10-11`. `root_keys[1] kernel-steward-001` is still
  `PENDING_STEWARD_SIGNATURE` — one signature, one human. Do not claim dual-custody.

## §1. CROSS-SURFACE INVENTORY (16 Surfaces)

### 1a. Named surfaces

| # | Surface | Path | Type |
|---|---------|------|------|
| 1 | AAA canonical | `/root/AAA/skills/` | SOT |
| 2 | kimi | `/root/.kimi-code/skills/` | copy |
| 3 | opencode | `/root/.arifos/agents/opencode/skills/` | symlink |
| 4 | grok | `/root/.grok/skills/` | symlink → AAA |
| 5 | claude | `/root/.claude/skills/` | symlink → AAA |
| 6 | codex | `/root/.codex/skills/` | symlink → AAA |
| 7 | hermes | `/root/.hermes/skills/` | copy |
| 8 | hermes-asi install | `/usr/local/lib/hermes-agent/skills/` | copy |
| 9 | openclaw-ws | `/root/.openclaw/workspace/skills/` | copy |
| 10 | openclaw-bundled | bundled | built-in |

### 1b. Organ-native + profile surfaces (ADDED 2.1.0 — the old “10 surfaces” map was blind to these)

| # | Surface | Live bodies | Meaning |
|---|---------|-------------|---------|
| 11 | `/root/GEOX/skills/` | 5 | organ-native doctrine — **not in AAA canon, not census-witnessed** |
| 12 | `/root/WELL/skills/` | 4 | organ-native |
| 13 | `/root/WEALTH/skills/` | 4 | organ-native |
| 14 | `/root/arifOS/skills/` | 35 | organ-native |
| 15 | `/root/A-FORGE/skills/` | 1 | organ-native |
| 16 | `/usr/local/lib/hermes-agent/profiles/aaa-hermes/skills/` | 487 | install-profile view — **not census-witnessed** |
| — | `/opt/aaa/app/skills/` | 208 | **separate inode** from AAA = deploy copy or stale snapshot — status UNKNOWN |
| — | `/root/.forge/skills/` · lanes `555-ASI`/`333-AGI` · `registries/antigravity` · `~/.grok/bundled` | 88 · 23/2 · 36 · 25 | sub-surface trees |

**Re-probe before any "mesh total" claim:**

```bash
find /root /opt /usr/local/lib -maxdepth 6 -type d -name skills 2>/dev/null | while read d; do
  n=$(find "$d" -maxdepth 5 -name SKILL.md 2>/dev/null | wc -l); [ "$n" -gt 0 ] && printf "%5d  %s\n" "$n" "$d"; done | sort -rn
```

> **Consequence for every count in this file:** `whole_mesh_skills` from the census is a **lower
> bound**. Until `/opt/aaa/app` is classified live-vs-snapshot and the organ homes are either
> promoted into AAA or formally declared sanctioned-non-canonical, no total is defensible.
> That classification is **F13-class** (it moves where "the catalog" is) — do not take it in an audit run.

### Cross-surface compare

```bash
# Dump each surface (symlink-aware — plain `comm` on `ls` lies across symlinked roots)
comm -23 <(ls /root/AAA/skills/ | sort) <(ls /root/.kimi-code/skills/ | sort)   # orphans: AAA has, kimi lacks
comm -13 <(ls /root/AAA/skills/ | sort) <(ls /root/.kimi-code/skills/ | sort)   # drift: kimi has, AAA lacks
```

**PITFALL — symlink blindness produces FALSE ABSENCE.** `/root/.agents/skills`, `~/.grok/skills`,
`~/.claude/skills`, `~/.codex/skills` are all symlinks to `/root/AAA/skills`. A bare
`os.walk()` / `find` **without** `followlinks` / `-L` skips them and reports bodies as missing
when they are merely behind a link. Always `os.path.realpath` and dedupe before counting.

### Classification Matrix

| Verdict | Condition | Action |
|---------|-----------|--------|
| ✅ PROMOTE | kimi/agent has it, AAA lacks, universal | Copy to AAA, register V3, add alias |
| 📦 ARCHIVE | agent has it, AAA has better version | Move to `_retired/<date>/` |
| 🔧 HARNESS-NATIVE | agent-specific | OK — don't promote |
| 🔲 NEED MIRROR | AAA has it, agent lacks | Copy/symlink to agent |
| ⚠️ DUAL-NAME | Same skill, different names | Alias table entry or symlink |
| ☠️ VOID | Zero invocations, zero evidence | SKILL.md → SKILL.md.VOID |

## §2. MESH SYNC PROTOCOL

### Compare command

```bash
find /root/AAA/skills /root/.hermes/skills /root/.kimi-code/skills -maxdepth 2 -name 'SKILL.md' | xargs grep '^version:' | sort
```

**PITFALL:** `-maxdepth 1` returns empty on this mesh — and `-maxdepth 2` is **also wrong now**.
Skill dirs nest up to 8 levels (`domains/general/aaa/skill-mesh/skill-inventory/SKILL.md`), and
`find` does not traverse the symlinked roots without `-L`. Use an unbounded
`find <root> -name SKILL.md` (or `os.walk(..., followlinks=True)`), never a hand-picked depth.

**PITFALL:** `find … -xtype l` finds broken symlinks — but **not one byte of it is a defect until you
check whether the link points at a pruned shell.** `/root/AAA/skills/.archive/shells-20260917/`
holds 14 empty shells; the 19 BROKEN opencode links are links to those shells, left behind by the
prune. Classify before deleting: *link to pruned shell* → delete; *link whose body exists elsewhere*
→ re-point.

### Health report format

```
skill_name | AAA_version | hermes_version | kimi_version | status
```

### Status values

| Status | Meaning |
|--------|---------|
| `SYNC` | Present in all trees, same version |
| `DIVERGED` | Present in ≥2 trees with different versions |
| `MISSING_FROM_X` | Absent from tree X but present in AAA |

### Escalation protocol

| Detection | Action | Owner |
|---|---|---|
| `DIVERGED` | Flag — log the row | AUDIT agent |
| `DIVERGED` > 3 sessions | Fix — align to AAA version | A-FORGE |
| `MISSING_FROM_X` | Propagate from AAA | A-FORGE |
| `MISSING_FROM_aaa` | Flag + reverse-propagate | AUDIT → A-FORGE |

## §3. ROT CLASSIFICATION

| Rot Class | Description |
|-----------|-------------|
| `doc-rot` | References external URLs/paths no longer accessible |
| `api-rot` | SDK/CLI packages past compatibility versions |
| `trigger-rot` | Triggering criteria overlap with other skills |
| `unused-rot` | No telemetry execution within threshold |
| `archive-void-rot` | Physically archived but still discoverable |
| `drift-rot` | Exists on agent surface but NOT in AAA (or vice versa) |
| `dual-name-rot` | Same skill has different names across surfaces |

### Age thresholds

| Days Since Forge | Status | Action |
|-----------------|--------|--------|
| 0-7 | FRESH | No action |
| 8-14 | CURRENT | Review on next session |
| 15-30 | AGING | Verify references still valid |
| 30+ | STALE | Audit needed, consider archive or refresh |

## §4. ROUTING TABLE (all targets re-probed against disk 2026-09-18)

> A routing table that routes to tombstones is worse than no table. **Verify every target with
> `[ -d <path> ]` before adding a row.** 5 of the 8 rows in v2.0.0 pointed at skills that no longer exist
> anywhere on the box (`geox-constitution`, `wealth-capital-thermodynamics`, `well-substrate-readiness`,
> `mcp-mastery`, `github-operations`).

| Intent Pattern | Skill to Load |
|---------------|---------------|
| "seismic" / "well log" / "petrophysics" / "basin" | `geox-grounding` → `/root/GEOX/skills/{geox-seismic-interpretation, geox-well-log-qc, geox-basin-evaluation}` · AAA `geo/basin-charge-screening`, `geo/seismic-interpretation-alignment` |
| "prospect" / "volumetrics" / "POS" / "EMV" | `/root/GEOX/skills/geox-prospect-evaluation` |
| "NPV" / "IRR" / "capital" / "investment" | `/root/WEALTH/skills/wealth-capital-primitives` · `wealth-runway-conservation` · AAA `wealth/market-analysis-scope` |
| "sleep" / "fatigue" / "vitality" / "dignity" | `/root/WELL/skills/well-substrate-readiness` · `well-triadic-ops` |
| "build MCP tool" / "forge tool" | `forge-fastmcp` · AAA `engineering/mcp-ops` · `engineering/mcp-testing` |
| "GitHub PR" / "CI broken" / "issue triage" | `forge-github-ops` (AAA) · AAA `github/*` · `FORGE-pr-governance` |
| "create a skill" / "new skill" | `skill-creator` → `${AAA_HOME:-/root/AAA}/skills/.system/skill-creator` |
| "what skill should I load" / "skill gap" | **THIS SKILL** |
| "multi-agent deliberation before a decision" | `FORGE-musyawarah-gotong` (hermes view) |
| "kernel init / judge / seal" | `substrate/kernel-bind` + `arifos-kernel-ceremony` |

## §5. HEALTH SCORING

### Per-skill health check

```python
skill_health = {
    "name": str, "version": str, "forged_date": str,
    "days_since_forge": int, "references_count": int,
    "phantom_refs": int, "has_prompt": bool, "has_test": bool,
    "organ_coverage": float,
}
```

## §6. ANTI-PATTERNS

| Anti-Pattern | Remedy |
|-------------|--------|
| Copy skill bodies into every `~/.X/skills` | Symlink to AAA / .agents |
| Second "Grok catalog" of 100+ natives | Keep ≤12 harness keepers |
| Route by V3 short name without path | Resolve via alias table **and then `os.path.exists` the resolved path** — 90 of 164 alias rows resolve to nothing |
| Trust frozen counts | Re-probe disk — every count carries the command that produced it |
| Skill overload (5+ for simple task) | Use this meta-skill for minimum set |
| Phantom reliance | Run gap register and forge missing |
| Stage skipping | Always start with 000-init |
| Treat a green/red log as closure | A sensor writing `verdict=FAIL` into a log nobody reads is decoration. Every gate needs `{expected_event, owner, deadline}` and timeout→SYNCHRONIZATION_FAULT |
| Blanket `--apply` propagation | 248 missing/drift entries is a **profile-scoping decision**, not a sync job — it changes the live loader surface (context cost, W₈₈₈) |
| Counting with a symlink-blind walk | Realpath + dedupe, else false absence (see §1 pitfall) |

## §7. PRE-SEAL CHECKLIST

1. `skill-mesh-sync.sh --check` exits 0 — **as of 2026-09-18: exit 1** (MISSING 231 · DRIFT 14 · BROKEN 19 · EXTRA 3)
2. `skills-census.py` VERDICT is not FAIL — **as of 2026-09-18: FAIL** (5 broken symlinks), 3+ consecutive runs
3. `skill-entropy-gate.py` reports `fail=0` — **as of 2026-09-18: fail=4** (broken_symlinks 3, missing_frontmatter 1, registry_witness blank, dead_internal_pointers 2)
4. Alias table: no non-tombstone row whose `primary_path` is missing — **as of 2026-09-18: 90 such rows**
5. Registry `alias_table_rows / active / tombstone` equal a fresh census — **as of 2026-09-18: 133/104/29 vs disk 164/125/31**
6. No live primary resolves through a tombstone row (currently PASS)
7. Harness-native keepers remain real directories (currently PASS)
8. BOOTSTRAP 9 universals all resolve on disk (currently PASS — all 9 resolve; manifest `expires: 2026-10-11`)
9. No archived body is discoverable by a live loader (`archive-void-rot`) — **as of 2026-09-18: FAIL** (`.archive-2026-09-18/exact-dups`, `.profile-archive`, `.archive-20260912`)
10. This skill points to a dated live receipt — PASS (`forge_work/2026-09-18/SKILL-INVENTORY-AUDIT-2026-09-18.md`)

**Read this checklist as a state machine, not a Boolean.** Each line names the command, the value it
returned, and the date. "Checklist complete" is never a deliverable; `VERIFIED` + evidence is.

## §8. INDEPENDENT VERIFICATION LANE (WAJIB 2)

A-FORGE planning, execution, AND verification in the same trust chain is a **primary substrate defect**. The required separation:

```
A-FORGE executes mutation
    ↓
Independent observe-lane verifier reads resulting reality
    ↓
Kernel checks evidence against original success criteria
    ↓
Only then may completion be recorded to VAULT999
```

### Verifier hard rules

The verifier MUST:
- NOT have performed the mutation
- Use independently obtained state
- Receive original success criteria, NOT executor's rewritten summary
- Be unable to modify the state it is checking
- Return: VERIFIED, MISMATCH, INCONCLUSIVE, or STALE
- NEVER issue constitutional approval — only the kernel may SEAL

### Kernel rejection rules

The kernel MUST reject "completion" when:
- Verifier identity == executor identity
- Evidence originated ONLY from the executor
- Verifier had mutation permission over the target
- Evidence is older than freshness_requirement
- Original success criteria are missing
- Results cannot be independently reproduced

## §9. BOUNDED INDEPENDENT AUDIT PROTOCOL

Subagents are optional, scope-bounded evidence collectors. They do not inherit authority, cannot validate one another recursively, and never replace a live source-of-truth probe.

### Rules

1. Route uncertainty to the owning evidence source first
2. Spawn only when scopes are independent and handoff cost < direct inspection
3. Do not ask one model to recursively agree with copies of itself
4. The root agent compares evidence, labels contradictions/UNKNOWNs
5. Irreversible SEAL still requires real human/external witness path

## §10. LESSONS FROM THE 2026-09-18 AUDIT (procedural — keep, do not re-derive)

1. **A meta-skill's own counts rot first.** Frozen numbers survived ~2 months past their truth and
   *became* the false authority they warn about. If a count has no command and no date next to it,
   delete it or make it a probe.
2. **A routing table is a claim about the disk.** Re-verify every target with `[ -d ]` on the run that
   uses it. 5 of 8 rows pointed at tombstones.
3. **A gate that fires into a log nobody reads has not failed — the *closure* has.**
   `skill-entropy-gate` reported the same 4 defects four times a day for days. Detection without an
   owner + deadline + timeout→SYNCHRONIZATION_FAULT is not governance.
4. **A prune must clean the links it invalidates.** Archives that remove bodies but leave the symlink
   mesh dangling convert a tidy prune into 19 BROKEN entries — and into a surface agents stop trusting.
5. **Archive must be a wall, not a curtain.** Bodies moved to `.archive*` were still offered by the live
   loader. Discovery is a capability; pruning the file is not pruning the capability.
6. **Alias tables describe a topology, not a file list.** When organ suites move to organ-native homes
   (`/root/GEOX|WELL|WEALTH|arifOS/skills`), every `primary_path` written against the old root becomes a
   lie while still reading `status: RESOLVED`. Re-resolve against reality, not against the field.
7. **Symlink-blind counting manufactures false absences.** (Cost: one wrong finding caught in self-review.)
8. **Never collapse a whole mesh into one number.** 629 / 634 / 706 / 801 are all correct — for different
   questions. State the question with the number, or the number is noise.

## References

- `contracts/AAA_SKILL.md` — full orthogonal + subagent contract spec
- `contracts/HERMES_ROLE.md` — polymorphic runtime
- `BOOTSTRAP_MANIFEST.json` — signed manifest; `universal_skills` = 9 entries (key name matters)
- `FEDERATED_SKILLS_REGISTRY_V3.yaml` — registry; its `total_skills` / `alias_table_rows` are **derived and stale** until `skills-census.py --write` runs
- `SKILL_ALIAS_TABLE.json` — 164 rows on disk (124 RESOLVED · 7 FORGED · 1 ALIAS_RESOLVED · 1 active · 31 TOMBSTONE); **90 non-tombstone rows point at nothing**
- `${FORGE_WORK:-/root/forge_work}/2026-09-18/SKILL-INVENTORY-AUDIT-2026-09-18.md` — the dated receipt for this version
- `/var/log/arifos/skill-entropy.log` · `/var/log/arifos/skills-census.log` — the two sensors whose exit states define §7

## Retired-name landing (names retired, modes live here)

Trigger phrases carried forward when the `skill-portfolio-audit` identity was retired (2026-09-19; frozen body at
`/root/AAA/skills-retired/2026-09-19-v2-portfolio-audit/skill-portfolio-audit/SKILL.md`). The names below are
RETIRED routing names — this skill is their live mode owner; nothing is re-forged under them.

| Retired name | Retired trigger phrase (verbatim) | Live section here |
|---|---|---|
| `AUDIT-skill-atlas` | "skill atlas", "unified skill inventory", "unified inventory" | §0 multi-harness unification · §1 cross-surface inventory (16 surfaces) · §3 rot classification · §4 routing table |
| `AUDIT-agent-skill-mesh` | "skill mesh sync", "check skill mesh sync", "skill mesh" | §2 MESH SYNC PROTOCOL (`SYNC` / `DIVERGED` / `MISSING_FROM_X`) |

These were the `mode=atlas`, `mode=mesh` and `mode=inventory` rows of the retired `skill-portfolio-audit`
("Unified skill inventory, audit, mesh health, and cross-surface contrast"). Its absorbed pre-merge bodies remain
readable at the frozen path above (`references/absorbed-AUDIT-skill-atlas.md`,
`references/absorbed-AUDIT-agent-skill-mesh.md`).
