# SECOND-READER VERIFICATION — mesh skill count, C14, and the eureka ledgers

**Date:** 2026-09-16T02:45Z · **Reader:** HERMES (second session, independent probe) · **Trigger:** F13
pasted the sibling session's correction report for audit — *"verify before believing."*

**Consequence class (C18):** one sensor predicate removed (latent, never fired live), one regression
suite added and wired, one documentation receipt. Reversible via git (`scripts` `7e5d8b3`).
No external surface. No canon mutated.

**Method:** every number below was re-derived on disk by this session, not read off the sibling's
report. Where a value is quoted from their report rather than re-measured, it says so.

---

## 1. The three numbers — all reproduce exactly

```
find    /root/.hermes/skills -name SKILL.md | wc -l   = 124     <- no -L, links never entered
find -L /root/.hermes/skills -name SKILL.md | wc -l   = 409     <- loadable truth
ls -1   /root/.hermes/skills              | wc -l     = 162     <- top-level listing
readlink -f /root/HERMES                              = /root/.hermes   (symlink, Sep 4 13:28)
```

`409` agrees with `skills-census.py --json` (`viewed_skills` = `total_loadable_skills` = 409).
**Verdict: the correction is correct.** `/root/HERMES/skills` is not a separate tree, and `162`/`124`
are the view surface, not the view.

*(Reader's own note: a first pass measured `find` with no `-name` filter and got 1211, which looked
like a contradiction. It was my command shape that was wrong, not the report's — recorded because the
class of error under audit is exactly this one.)*

## 2. Doctrine pre-named the number — verified verbatim

`/root/AAA/skills/skill-library-integrity/SKILL.md:79`:

> *"use `followlinks=True` / `find -L`, or you will count **124** when the true figure is **409** and
> conclude the tree collapsed."*

Not paraphrase — the file already held this sentence. The report's claim that this was a known trap
is true.

## 3. The correction actually landed in the documents

`/root/AAA/docs/SKILL_MESH_ALIGNMENT_2026-09-16.md` — row 18 rewritten (symlink → `.hermes`, 409 via
`-L`, "SAME tree, NOT a separate root") · §1a F2 CORRECTION present with the three commands ·
§2 marked `SUPERSEDED` · S1 `≈709` explicitly withdrawn as double-counting · S2 retargeted to 409.
The prose claim and the document now agree; nothing was rewritten to an unmeasured number.

## 4. Independent re-derivations

| Claim | This reader's probe | Verdict |
|---|---|---|
| four eureka ledgers, four schemas | `canon/` 104 · `AAA/eurekas/` 3 · `.local/share/arifos/` 6 · `atlas333/` 1 (`eureka777.v1`) | **CONFIRMED — four writers, four shapes** |
| 9 eureka entries today | canon ledger `2026-09-16` = 9 | **CONFIRMED** |
| symbol-probe regression 7/7 | ran all 7 cases independently: A1·A2·A2B·A3·A5·AXIS_K·PROSE_MENTION → 7/7 pass | **CONFIRMED** |
| C14 live in the sweep | per-root loop over 8 roots, literal `find` / `find -L` shapes, output present | **CONFIRMED** |
| FI mesh `EXTERNAL ≠ FAIL` | `FI_CODING_MESH_2026-09-16.md:16-17,88` — grok/gemini money-gated | **on the record** (reader verified the document, not the live FI probes — different lane) |

C14 per-root output also confirms the widened check independently: `AAA-canonical` 465/506 ·
`hermes` 124/409 · `qwen` 9/531 · `opencode-overlay` 9/31 · `kimi` 77/131 · `agents`/`claude`/`codex`
plain-walk-empty symlink farms.

## 5. New findings from this pass

**a. A latent false-FAIL predicate was still live in C14 — removed.**
The first C14 revision ended with `if resolved_skill_md_count <= len(os.listdir(LIVE)): FAIL`. Those are
**different quantities** — SKILL.md files under a tree vs directory entries at one level. A fixture
proves it fires wrongly on a healthy tree: `listing=3, resolved=3 → FAIL`. It never fired live
(409 > 172), which is precisely why it survived a green sweep: latent, never proven sound.
Removed (superseded by the per-root loop, which measures the same invariant in sound units: walk vs
walk). The negative case is pinned so it cannot return.

**b. The C14 regression suite is now wired into the sweep's own self-test section (C12).**
An unwired test is prose in a `.py` file. `tests/test_c14_view_resolution.py` asserts the invariant on
all 8 roots and carries the pinned negative case; `C12` now FAILs the sweep if it exits non-zero.
**Falsifiability proven, not asserted:** against a synthetic failing suite the sweep emitted
`[FAIL] C12 sensor_regression … the sensor is lying (1)` and exited 1. The wiring is not dead.

**c. The registry snapshot the mesh doc quotes is already one skill stale.**
`FEDERATED_SKILLS_REGISTRY_V3.yaml → disk_reconciliation` (last cron, 09:56): `physical 503 ·
canonical 481 · witness b93ff0450ea27d1a`. Live census now: `504 · 482 · 72a0e4764ea03d9f`.
Delta +1, unattributed (a sibling session is active in the same trees). No collision flagged — C6
clean. Named because §1 of the mesh doc quotes the older figure as "registry"; the census is the SOT
and will re-sync on the next cron.

**d. Three standing C14 WARNs are alarm fatigue, not findings.**
`agents`/`claude`/`codex` are symlink farms *by design* — the sweep's own message says so ("standing
trap, deliberate by design") — yet they are emitted at WARN every cycle, so the sweep can never be
green. The file already has the right pattern for this: `DECLARED_SHELLS` (intentionally minimal,
reviewed by a human, reported as INFO, never "fixed"). Same doctrine, applied one check earlier, would
keep the genuine alarm (a non-declared root reading empty must still FAIL) and stop the permanent
yellow. **Recommendation only — the WARN level is the owner's call, so it was not changed.**

**e. The "4 duplicate owners" item is already corrected and should not be carried forward as HOLD.**
`SEAL-C17-C20-v3 §7` records the re-probe: those four names each have **one** authored owner; the
profile copies are flat-layout leftovers from before the domain reorg (mirror drift), so the remedy is
a re-sync, not a human merge decision. The sibling report still lists them as an open human decision —
reconciled here so the next reader is not parked on a call nobody needs to make.

## 6. Verification (this pass, on the pinned revisions)

```
sweep before patch   sha256 e5ce95a795a7bf19…  (rev d40a668)   fail=0 warn=4  exit=0
regression suite     PASS — 0 violations · 9 observations
sweep after patch    sha256 f6e6033ab8913e57…  (rev 7e5d8b3)   fail=0 warn=4  exit=0  (unchanged)
C12 wiring           synthetic failing suite → C12 FAIL, sweep exit=1   (fires)
census (unchanged)   504 on disk · 482 canonical · 409 loadable · 45 shells · 0 broken
kernel               FLOOR_TABLE untouched · no VAULT999 entry
commit               /root/scripts 7e5d8b3 — path-scoped (2 files), sibling working tree untouched
backup               hermes-chaos-sweep.py.bak-20260916-hermes2  (hash = pre-patch revision)
```

## 7. NOT executed (and why)

| Item | Why |
|---|---|
| Four eureka ledgers merged | consolidation is a human decision — four writers, four shapes, one filename |
| C14 WARN levels for declared farms changed | alarm level is the owner's design call; recommendation recorded instead |
| Registry re-synced to the live census | cron owns that write (4x/day); forcing it is a second writer on a live file |
| Doc §2 recomputation | the sibling marked it `SUPERSEDED` rather than guessed — recompute on purpose, not in a hurry |
| `arifOS` main · duplicate-owner merges | unchanged HOLD |

## 8. What the second reader takes from this

The sibling's report was **substantially right**, including the part that matters most: it corrected
its own prior document on the record with the commands attached, and it widened the sensor rather than
only fixing the number. The one live defect this pass found was in the sensor itself — a check with
mismatched units, latent under a green sweep. Which is the same lesson the session keeps re-issuing:
**the guardrail needs guarding, and a passing test is not evidence until something has made it fail.**

DITEMPA BUKAN DIBERI ⚒️
