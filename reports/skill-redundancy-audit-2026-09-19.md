# Skill Name & Function Redundancy Audit — 2026-09-19

**Method:** enumerate every SKILL.md across all 11 roots → dedupe by realpath → classify
name-level, content-level, and description-level redundancy. No hand-counting.

## Corpus (measured)

| Measure | Value |
|---|---|
| Roots scanned | 11 (`AAA`, `.agents`, `.hermes`, 2 profiles, `.forge`, `GEOX`, `WELL`, `WEALTH`, `arifOS`, `A-FORGE`) |
| SKILL.md found | 1741 |
| Physical files reachable from >1 root (mirrors) | 691 |
| **Unique physical SKILL.md** | **1050** |
| Core (non-profile) bodies | 764 |
| Distinct routing names (core) | 733 |
| YAML frontmatter parse errors | 12 |

## R1 — NAME COLLISIONS: 28 names, 2 bodies each — CORRECTED 2026-09-19

**CORRECTION.** Most of these were an ARTIFACT of counting one tree twice: `/root/.agents/skills` is a
**symlink to `/root/AAA/skills`**, so 627 bodies appeared under two root labels. Re-measured against
the loader's actual read path there are only **4** genuine same-name collisions, listed in R5.
The 20 `agents↔forge` pairs are AAA vs `/root/.forge/skills` — a *different harness home*
(own `config.yaml`), not a redundant copy of AAA.

Classified by what actually differs, not by which looks newer:

| Class | Count | Meaning |
|---|---|---|
| FRONTMATTER-ONLY (>0.985 whole-file sim) | 12 | copies differing only in frontmatter/version |
| near-identical (0.80–0.985) | 8 | same design, small drift |
| DIVERGENT (<0.80) | 8 | genuinely different content under one name |

Root pairs: `agents`↔`forge` 20 · `agents` internal 4 · `arifOS`↔`forge` 3 · `agents`↔`arifOS` 1

**FRONTMATTER-ONLY set** (trivially collapsible): ascii-art, excalidraw, pretext, plan,
Agent Onboarding, touchdesigner-mcp, comfyui, github-code-review, github-repo-management,
github-pr-workflow, github-issues, weights-and-biases.

**DIVERGENT set** (real forks — need a human): RSI-recursive-improvement, skill-creator,
sovereign-recognize, openclaw-ops, AGI-decisions-reflect, google-workspace, notion, github-auth.

## R2 — FUNCTION-LEVEL OVERLAP: 10 pairs at description Jaccard ≥ 0.60

Cutoff stated. Same-name pairs excluded (covered by R1). Corpus 740 described skills.

| Jaccard | Content sim | Pair | Class |
|---|---|---|---|
| 1.00 | 0.98 | rsi-federation-mesh ↔ RSI - Federation Mesh | case-variant of one body |
| 0.88 | 0.83 | claude-meta-mesa ↔ qwen-meta-mesa | harness variant |
| 0.88 | 0.93 | qwen-zen-router ↔ claude-zen-router | harness variant |
| 0.83 | 0.52 | claude-agentic-state ↔ qwen-agentic-state | harness variant, partly drifted |
| 0.83 | 0.03 | enforcement-coverage-audit ↔ name-requires-mechanism | same job, different text |
| 0.81 | 0.86 | qwen-zen-router ↔ opencode-zen-router | harness variant |
| 0.81 | 0.85 | opencode-zen-router ↔ claude-zen-router | harness variant |
| 0.71 | 0.01 | name-requires-mechanism ↔ named-mechanism-audit | same job, different text |
| 0.67 | 0.10 | cross-host-artifact-delivery ↔ cross-node-artifact-transfer | same job, different text |
| 0.60 | 0.04 | ai-video-generation ↔ human-recognition-architecture | likely false positive |

## R3 — HARNESS-VARIANT FAMILIES: 3 stems duplicated across 3–4 harnesses (10 copies)

| Stem | Copies | Bytes per copy |
|---|---|---|
| agentic-state | 4 (claude, kimi, opencode, qwen) | 5695 / 5506 / 5133 / 4737 |
| meta-mesa | 3 (claude, opencode, qwen) | 5225 / 4280 / 4685 |
| zen-router | 3 (claude, opencode, qwen) | 4663 / 4237 / 4474 |

Content similarity 0.83–0.93 → near-identical bodies. 83 prefixed variants exist across 75 stems;
only these 3 stems are carried by ≥2 harnesses.

## R4 — THE CONTROL-AUDIT CLUSTER: 7 skills, one job, 49,941 bytes

Every one answers: *"is this named control actually doing anything?"*

| Skill | Bytes |
|---|---|
| enforcement-coverage-audit | 11412 |
| named-mechanism-audit | 8748 |
| control-mechanism-audit | 8287 |
| control-integrity-audit | 6800 |
| name-requires-mechanism | 5291 |
| declared-vs-enforced-control-audit | 5182 |
| control-seal-verification | 4499 |

**Pairwise content similarity: 0.02–0.07 across all 21 pairs.** Not copy-redundancy — seven
independent write-ups of the same procedure. This is the "second, thinner owner for one doctrine"
defect: all seven load, all seven sound right, none is canonical, and they will drift apart.

## R5 — FAILED COLLAPSES: 2 (highest severity) — CORRECTED 2026-09-19

**CORRECTION to the first version of this section.** It claimed "both stub and retired body still
load". That is wrong: the loader is FIRST-WINS by name, so exactly ONE body per name is reachable.
Measured against the loader's real read path (`get_scan_ordered_skills_dirs`), the true state:

| Skill | What the loader SERVES | What is unreachable | Successor |
|---|---|---|---|
| AGI-decisions-reflect | the **4980 B live body** (the retired doctrine) | the 1124 B stub | APEX-humility-godel |
| sovereign-recognize | the **1155 B stub** (the redirect) | the 5611 B live body | audience-scoped-disclosure |

So one collapse failed to take effect (still serving retired doctrine); the other took effect but
left an orphan. Neither had absorbed its content — heading check: 6/6 and 7/10 H2 headings absent
from the successor.

**Both "archive" pointers were CIRCULAR.** `.archive/2026-09-16-skill-zen-quartet/sovereign-recognize`
was a symlink back to the live orphan it claimed to have archived. So "the body is archived" was a
claim with no independent copy behind it — deleting first would have destroyed the only one.

**RESOLVED 2026-09-19 (commit f5bed9f88), tertib = recover first, then remove:**
content recovered into each successor's `references/absorbed-<name>.md` (payload hash verified ==
source), then both orphans quarantined to `/root/AAA/.quarantine-redundancy-2026-09-19/` with a
reversal ledger. 3 dependent symlinks fixed; 3 inventories updated. Verified: loader served count
unchanged, 0 links pointing at quarantined paths, census `broken_symlinks: 0`.


## R6 — DIR-NAME vs FRONTMATTER NAME MISMATCH: 2

| Directory | Declares `name:` |
|---|---|
| `FORGE-act-federation-ingress` | `FORGE-sct-federation-ingress` |
| `KERNEL-trinity-33` | `trinity-33-canonical` |

The directory name is the index key; where it disagrees with `name:` the skill is unreachable under
its declared name.

## Instrument defects found and fixed during this audit

1. `skill-sync.sh` printed `Registry total: 0 entries` forever — wrong filename AND wrong field
   convention. Fixed and verified (95 entries).
2. `skill-constitutional-audit.py` scanned one level only, auditing 281 of 626 bodies and publishing
   a rate over 55% of the library. Fixed to recursive; `--flat` preserves the old series.
3. **This audit's own analyzer** reported 0 function-level overlaps when 0.88 pairs existed — an
   index-aliasing bug (`D[a]` where `a` ranged over a token list, not the skill list). Caught by
   hand-checking one known pair before trusting the zero.

## What is NOT redundant (checked, cleared)

- 0 exact-content duplicates under differing names.
- 0 name-prefix duplicates (`FORGE-x` alongside `x`).
- 1 case-variant family only (`FORGE-federation-manifest` / `forge-federation-manifest`).

## Next actions (ranked by severity)

1. **R5** — remove the two retired bodies (quarantine, not delete); leaves the stubs authoritative.
2. **R6** — rename the two directories to their declared `name:`.
3. **R4** — collapse the 7 control-audit skills to one canonical owner + 6 aliases.
4. **R1 FRONTMATTER-ONLY (12)** — mechanical: keep one body, symlink the view.
5. **R1 DIVERGENT (8)** — a human decides; these are real design forks.
6. **R3** — decide whether per-harness variants stay (deliberate) or collapse to one body.
