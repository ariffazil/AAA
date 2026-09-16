<!-- SOT: this file is a doctrine proposal. Tier: DRAFT_AWAITING_F13 unless ratified in chat. -->
# SKILL MESH ALIGNMENT — 3-Surface Reality & Plane Law
> Forged: 2026-09-16T02:1xZ · 333-AGI session SEAL-6ce0ea8cd0174aa9 · OBS-labeled from live disk
> Feeds: FEDERATED_SKILLS_REGISTRY_V3.yaml · supersedes the stale §5/§8 of TOOLBENCH_3WAY_CONTRAST.md (2026-07-18)

## 1. Reality map (OBS, probed 2026-09-16T02:05–02:15Z)

| Surface | Type | SKILL.md | Relation to canonical |
|---|---|---|---|
| `/root/AAA/skills` | CANONICAL SOT | 506 | source of truth (registry: 481 canonical, 409 loadable, 45 shells, 30 diverged, WARN, witness `b93ff045`) |
| `/root/.agents/skills` | symlink | — | → AAA (direct) |
| `/root/.claude/skills` | symlink | — | → AAA (direct) |
| `/root/.opencode/skills` | symlink→symlink | 506 via -L | → `.agents` → AAA (double hop, est. Aug 31) |
| `/root/.codex/skills` | symlink | 506 via -L | → AAA |
| `/root/.grok/skills` | symlink | 506 via -L | → AAA |
| `/root/.config/opencode/skills` | REAL dir | 31 | OpenCode-native overlay — OUTSIDE mesh |
| `/root/.qwen/skills` | REAL dir | 9 (+1 nested ghost `youtube-extraction-datacenter-ip/youtube-extraction-datacenter-ip/`) | OUTSIDE mesh |
| `/root/HERMES/skills` | **symlink → `/root/.hermes`** (since Sep 4 13:28) | **409 via `-L`** · 124 non-resolving · `ls -1`=162 | **SAME tree as `.hermes/skills` — NOT a separate root** — see §1a correction |

**FI harness drift = 0 by construction** (symlink farm). All "175 drift" from the 2026-09-15/16 dry-run resolves to the HERMES tree and overlay seams, not the harness roots.

## 1a. F2 CORRECTION — the HERMES row (probe 2026-09-16T02:30Z, HERMES lane)

The row above previously read `REAL dir · 162 · separate tree`. That is wrong in kind **and** in
number; both errors come from measuring the view surface instead of resolving it.

```
/root/HERMES                          -> /root/.hermes        (symlink, Sep 4 13:28)
/root/.hermes/skills                  137 real dirs + 27 symlinks   (173 entries)

ls -1 /root/.hermes/skills      | wc -l            = 162   <- TOP-LEVEL LISTING (the "162")
find    /root/.hermes/skills -name SKILL.md | wc -l  = 124   <- no -L, links never entered
find -L /root/.hermes/skills -name SKILL.md | wc -l  = 409   <- LOADABLE TRUTH
skills-census.py --json  viewed_skills / total_loadable_skills = 409   <- agrees
```

`124` is not a new finding — `skill-library-integrity` §LAW 3 named this exact number in advance:
*"use `followlinks=True` / `find -L`, or you will count **124** when the true figure is **409** and
conclude the tree collapsed."* The same file also says: **never hand-write a skill count; read the
census.** Both numbers in the original row are the two faces of that same bug.

**Consequences (these are the load-bearing part):**

1. `§2 HERMES tree anatomy` — every figure derived from 162 (prefix census, 112/57 plane split,
   79 name-shared / 83 HERMES-only / 188 AAA-only) is computed over **top-level directory names**,
   not over the resolved tree. Treat §2 as **superseded pending a `-L` recomputation**.
2. `S1` arithmetic double-counts one body set: `/root/AAA/skills` (canonical) and
   `/root/.hermes/skills` (a view whose 27 symlinks point *into* AAA, plus 137 real copies) are not
   additive surfaces. `506 + 162 + 31 + 10 ≈ 709` is not a target; it is one tree counted twice.
3. `S2` target is not "162 HERMES skills" — it is **409 loadable**, of which the real-copy subset is
   what can drift. (Sweep measurement 2026-09-16: 30 canonical→hermes divergences, 4 duplicate-name
   owners — the genuine drift set.)

The topology half of the correction was already made in prose; this is the doc catching up to it.

## 2. HERMES tree anatomy (OBS — **SUPERSEDED, see §1a**)
> The figures below were computed over a **top-level listing** (`ls -1` = 162), not the resolved tree.
> Loadable truth through this view: **409** (`find -L`, census-agreed). Recompute before acting on
> any number in this section.

- 162 skills. Prefix census: FORGE×58 (54 UPPER + 4 lower — case split visible), AUDIT×6, ASI×5, AGI×4, FLAME×2, APEX/AAA/HERMES/RSI/WELL/EUREKA777×1 each, ~80 long-tail singletons.
- Plane heuristic: **112 machine-plane** (forge/audit/asi/agi/fi/ops/infra naming), **57 human-plane** (counsel/well/voice/media/human/social/telegram-human).
- vs AAA canonical: 79 name-shared (19 byte-identical, 22 drifted, 38 structurally non-comparable), 83 HERMES-only, 188 AAA-only.
- Case-pair collision pattern confirmed: `HERMES/FORGE-github-ops` ↔ `AAA/forge-github-ops`; `FORGE-fastmcp` ↔ `forge-fastmcp`. This is the bulk of the 431 "penamaan" collisions (OBS sample of 2, DER for the pattern).

## 3. The Plane Law (proposal — the alignment is role-scoped, not homogenization)

Arif's framing is the law: **Hermes = human-facing reality bridge · OpenCode = forger, AGI-level for the state · AAA = the state's shared canon.**

| Plane | Owner / SOT | Case convention | Other surfaces get |
|---|---|---|---|
| **MACHINE_PLANE** (forge/audit/ops/dev/infra) | `/root/AAA/skills` — ONE copy | kebab-case (`forge-github-ops`) | symlink or loader-reference only. Never re-authored. |
| **HUMAN_PLANE** (counsel/well/voice/media/human-ops) | `/root/HERMES/skills` — Hermes authors | Hermes convention | AAA may mirror read-only into `AAA/knowledge/` band; never converges by force. |
| **SUBSTRATE CORE** (7 substrate + 4 knowledge) | `/root/AAA/skills` | kebab-case | every agent, byte-identical, ALWAYS FIRST (already registry law). |

**Thesis (INT):** Hermes's alignment debt is mostly *plane leakage* — 112 machine-plane skills living inside the human bridge. The fix is repatriation + one-copy law, not a merge of personalities. SOUL, register, and human-plane authorship stay Hermes's forever.

## 4. Staged convergence protocol (F1-safe, each stage: canary → rollback → receipt)

- **S1 · Census coverage** — verify `skill_store_census.py` cron sees every *real* surface (AAA canonical, the `.hermes` view, `.config/opencode`, `.qwen`, `.kimi-code`). **CORRECTED (§1a):** `skills-census.py --json` already reports `viewed_skills = 409` = `total_loadable_skills`, which IS the `.hermes` view resolved. The old `506+162+31+10 ≈ 709` target counted one body set twice (AAA canonical + its own view) — do not chase it. The open question is coverage of the **overlays** (`.config/opencode` 31 via `-L`, `.qwen` 9 own + `aaa-canonical` link, `.kimi-code` 77 own / 131 via `-L`), not of the main tree.
- **S2 · Plane tagging** — classify the **409 loadable** skills in the `.hermes` view (not "162"), plus 31 opencode + 9 qwen overlay skills; tag frontmatter `plane: machine|human|substrate`. Mechanical, reversible, no content change.
- **S3 · Machine-plane drift convergence (22 shared drifted)** — AAA wins; Hermes diff preserved in `HERMES/_archive/pre-align-<date>/`. Requires Hermes-loader symlink canary first (does `hermes skills list` follow symlinks INTO its tree? UNKNOWN — test with one sacrificial skill).
- **S4 · Case-pair dedup** — for each `FORGE-x`(HERMES) ↔ `forge-x`(AAA) pair: keep AAA copy, replace Hermes dir with symlink (post-S3 canary) or loader alias. This collapses most of the 431 collisions.
- **S5 · Overlay folding** — `.config/opencode/skills` (31) and `.qwen/skills` (9): promote real novelties into canonical, symlink the rest, delete the nested qwen ghost dir (`youtube-extraction-datacenter-ip/youtube-extraction-datacenter-ip/`).
- **S6 · Semantic verdict** — census emits `machine_drift` vs `human_divergence` separately. Machine drift MUST → 0. Human divergence is expected and healthy.

## 5. Debt ledger integration (from 2026-09-15/16 session, unchanged)

| Item | Count | Maps to |
|---|---|---|
| 45 canonical shells (classification debt 2026-09-15) | 45 | S1/S2 pass reclassifies as side-effect |
| 30 diverged skills (HOLD — human merge decision) | 30 | S3 — but merge stays F13-gated per skill |
| 431 cross-root collisions (naming) | 431 | S4 case-pair dedup |
| 175 HERMES-side missing_or_drift | 175 | S3+S4 |
| C17–C20 | PROPOSED | untouched here — not a skill-mesh item |

## 6. What must NEVER align

- Hermes SOUL, human register, counseling/voice/media authorship — human-plane, Hermes-owned.
- OpenCode forger bands and subagent rotation — build-plane, 333-owned.
- Substrate core text — byte-identical, no local edits anywhere (one writer: AAA).

*One truth · many views · plane decides the writer · DITEMPA BUKAN DIBERI ⚒️*
