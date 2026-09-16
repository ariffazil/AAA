# F2 CORRECTION RECEIPT — mesh skill count (162 / 124 vs 409)

**Date:** 2026-09-16T02:30Z · **Actor:** HERMES (edge bridge) · **Trigger:** verification of the
333-AGI mesh report, per the standing rule *probe before assert*.

**Consequence class (C18):** documentation correction in two untracked DRAFT docs + one new sweep
check. Reversible via git. No external surface touched.

---

## 1. What was claimed, and what the disk says

| Claim | Measurement |
|---|---|
| "`/root/HERMES/skills` — REAL dir, separate tree" | `/root/HERMES` → `/root/.hermes` (symlink, **Sep 4 13:28**) — same tree; `.hermes/skills` itself is 137 real dirs + 27 symlinks |
| "162 SKILL.md" | `ls -1 /root/.hermes/skills \| wc -l` = **162** — a **top-level listing**, links never entered |
| "live truth today: 124" | `find /root/.hermes/skills -name SKILL.md` = **124** — no `-L` |
| loadable truth | `find -L /root/.hermes/skills -name SKILL.md` = **409** = census `viewed_skills` / `total_loadable_skills` |

**124 is not a new finding.** `skill-library-integrity` §LAW 3 named the number in advance:
*"use `followlinks=True` / `find -L`, or you will count **124** when the true figure is **409** and
conclude the tree collapsed."* The doctrine also bans the practice that produced both numbers:
**never hand-write a skill count — read the census.**

## 2. Why it matters (not pedantry)

1. `SKILL_MESH_ALIGNMENT §2` — prefix census, 112/57 plane split, 79/83/188 shared-vs-unique — all
   computed over **top-level directory names**. Marked SUPERSEDED pending `-L` recomputation.
2. `S1` target `506+162+31+10 ≈ 709` **double-counts one body set**: `/root/.hermes/skills` is the
   view whose 27 symlinks point into `/root/AAA/skills`. Chasing ~709 would have driven a patch to a
   census that is already correct (`viewed_skills = 409`).
3. `S2` target "162" → **409 loadable**; only the real-copy subset can drift (sweep: 30 divergences,
   4 duplicate-name owners).

The prose correction ("HERMES is a symlink; my map stands") was right; the docs had not caught up.

## 3. Executed

- `SKILL_MESH_ALIGNMENT_2026-09-16.md` — row corrected; new **§1a F2 CORRECTION** with the three
  commands and their outputs; §2 marked SUPERSEDED; S1/S2 corrected in place.
- `FI_CODING_MESH_2026-09-16.md` — §7 S1 corrected with the same receipt; overlay surfaces listed
  accurately (`.config/opencode` 31 via `-L` / 9 own · `.qwen` 9 own + `aaa-canonical` link ·
  `.kimi-code` 77 own / 131 via `-L`).
- **Eureka ledger defect widened:** the report flagged three ledgers; a wider sweep found a **fourth**
  (`/root/.local/share/arifos/atlas333/eureka/eureka-entries.jsonl`, schema `eureka777.v1`).
  Four writers, one filename, four shapes — recorded as a consolidation target, not silently merged.
- **New sweep check `C14 view_resolution`** — FAILs if a link-resolving walk returns ≤ the top-level
  listing, i.e. if the view stops being resolved. INFO otherwise, quoting both numbers so a future
  doc cannot quote the surface as if it were the tree.

## 4. What was NOT done

- No count in any doc was **rewritten to a number I did not measure** (§2 is marked superseded rather
  than filled with fresh figures — recomputation is owed, not guessed).
- `skills-census.py` was **not** patched: it feeds the canonical SOT and already reports 409 correctly.
- The eureka ledgers were **not** merged — four writers is a consolidation decision, not a cleanup.
- S1/S2/S3 convergence stages were **not** started: their targets changed tonight.

## 5. Verification

```
find -L  .hermes/skills -name SKILL.md   = 409
census   viewed_skills                   = 409   total_loadable_skills = 409
sweep    C14 view_resolution             = INFO  (listing=172 · loadable=409)
sweep    overall                          fail=0 warn=1 INFO=2
```

## 6. Verdict

- Mesh count: **CORRECTED on the record** (162/124 were the surface; 409 is the tree).
- Doc §2 figures: **SUPERSEDED, recomputation owed.**
- Eureka ledgers: **HOLD — 4 writers, human consolidation decision.**
- C14: **SEALED as a live check.**

DITEMPA BUKAN DIBERI ⚒️
