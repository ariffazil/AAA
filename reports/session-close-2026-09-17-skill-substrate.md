# Session Close — Skill-Substrate Hardening
**Date:** 2026-09-17 · **Node:** KVM8 (forge, truth) · **Actor:** Hermes (i-ARIF) · **Principal:** Arif Fazil (F13)
**Status:** EXECUTED TO AUTHORITY BOUNDARY — **SEAL CANDIDATE, awaiting F13**

> SEAL is F13. This file records what happened; it does not seal. Nothing here is canon until ratified.

---

## 1. What this session found (the load-bearing defect)

The federation's own **Wave-2 consolidation** (2026-09-16) recorded 14 skill merges and moved **no
content**:

```
14 tombstones written (moved_to + sha256_before + rollback command + deprecation window)
 0 of 14 targets carried their source's body    ← measured
147,531 bytes of procedure unreachable
```

The retirement was real; the merge was not. A retired name leaves the index and **nothing errors** —
so the loss was invisible until measured. Byte-level proof: the surviving `FORGE-cross-agent-handoff`
body still hashes to the exact `sha256_before` in its tombstone (`dad5a1f7d6c5…`), byte-identical to
its pre-merge state, while its declared target was a 63-line stub.

**Repaired:** all 14 bodies recovered from the tag the tombstones themselves name
(`entropy-wave2-pre-act-20260916T144144Z`) into `references/absorbed-<source>.md` with a provenance
header. Verified 14/14 PRESERVED. A new gate check `merge_completeness` proves it per tombstone; the
check was proved able to fail (remove one absorbed reference → FAIL with the missing headings).

## 2. Executed this session (all reversible; manifest per class)

| Class | Before | After | Manifest |
|---|---|---|---|
| Broken symlinks | 19 | **0** | `dead-symlink-repair.json` |
| Dead internal pointers | 74 | **0** | `package-repair-*.json` |
| Missing frontmatter | 2 | **0** | (direct) |
| Wave-2 merges incomplete | 14 | **0** | `complete-merges-manifest.json` |
| Headless shells | 43 | 3 → **0** | `shell-resolve.json`, `session-close.json` |
| Harness bodies with no canonical home | 9 | **0** | `session-close.json` |
| Phantom views (link resolves, no body) | 24 | **10 remaining** | `phantom-repair.json` |
| Instruction pointers on tombstoned names | 8+ | **0** in editable files | `name-pointer-repair.json` |
| Pending memory re-consolidation pile | 22 | **0** (archived verbatim first) | `memory-pending-archive-2026-09-17-evening.json` |

Also: the gate's own `CONTAINERS` set was declared but never consulted — every taxonomy container
counted as a headless shell (48 reported, 4 real). Fixed. A gate that cries wolf is read once and
then ignored.

## 3. Claims falsified against measurement (this is the session's real product)

Every one of these was asserted by a skill and found wrong by running the thing:

1. **`<hash>@vN` in the CLI file-history stores is NOT a content hash.** sha256/md5/sha1 of the blob,
   of the path, of basename/dirname variants — all miss. Locating a peer's edit by keying on
   `sha256(live_file)` returns nothing and reads as *"they never touched it"*: a false negative.
   Locate by content. (`agent-session-forensics/references/cross-agent-file-mutation-attribution.md`)
2. **The W_SCAR execution gate does not trip on symptom vocabulary.** Its exemption is anchored at
   the START of a command: `grep -a 'ubat' <log>` passes; `cd /root && grep -c 'ubat' <log>` and any
   `python3` heredoc are held. Four of six example words in the old rule (`tidur`, `sleep`, `test`,
   `polisi`) are not patterns at all. It also fires on **paths and prose** — a `read_file` of anything
   under `skills/domains/general/court/` is held because the path carries a legal-adjacent word, and
   a doctrine sentence containing "freshness law" trips it. Its "source evidence" test is a substring
   check (`resource` contains `source`). (`causal-attribution-discipline/references/…`,
   `sovereign-worry-witness`; predicates exercised by `test_gate_predicates.py`)
3. **Log rotation is size-driven, not clock-driven.** ~5 MB boundary, measured at 2026-09-16 20:33 —
   not midnight. A midnight-spanning window sat inside one file.
4. **`grep -a` prevents nothing on the emoji-bearing gateway log.** Plain and `-a` counts are
   identical; emoji do not make grep treat a file as binary. NUL bytes do.
5. **A record that says a thing moved is DECLARED, not moved.** A successful lookup at the target
   name proves REACHABLE only. (`bridge-lane-functional-probe` § Rule 1b)
6. **My own permission report to the principal was read off a symlink.** `stat` on a symlink returns
   the link's mode (`777`, meaningless), not the target's. The target is `750`, owner `arifazil`.
   Corrected to the principal in-session.

## 4. Three mistakes I made tonight, and the fix

Recorded because the next agent inherits the lesson, not the apology.

1. **100 links broken by a predicate that could not fire.** `find -L … -type l` — with `-L`, find
   FOLLOWS links, so `-type l` matches only already-broken ones. Three live containers were declared
   "no dependents" and archived. Restored from the archive within minutes; broken links back to 0.
   The correct check is in `dependents.py` (walk WITHOUT following). This is the same defect class the
   skill documents ("a check with no reachable failing branch") — committed by me, in the same hour.
2. **A "VERIFIED" claim written while the measurement was still running.** A commit message asserted a
   census that had not returned. Corrected in a follow-up commit with the scoped count.
3. **A gate check that reported a clean zero from an empty input space.** Wrong path → no inputs →
   `0 — clean`. Now the empty case is an explicit FAIL (`cannot witness`), and the input count prints
   beside the result count.

## 5. HELD — RESOLVED after the questions were put to the principal

**10 phantom views + their families.** A phantom view is a symlink that *resolves* while its target
directory holds no `SKILL.md` — the index advertises a capability that loads as nothing.

I first reported this as a naming decision needing the owner, because every candidate target had 3–5
further dependents. **That was the wrong diagnosis, and the principal sent it back.** The names were
never due for retirement. Probing each name against every tree, then against git, found the actual
cause:

```
commit c3ac34677  (333-AGI, 2026-09-16 00:10)
  "chore(nightly): consolidate 2026-09-15 multi-lane work (750 files) — verified scan clean"
  deleted 79 SKILL.md   added 1
  64 of those names have a body living elsewhere today
  17 do not — and those 17 are exactly the names with no body at the link target
```

**The bodies were deleted, not retired.** The commit's scan checked PII and credential patterns; it
could not see that the deletions removed load-bearing content. Recovered from `c3ac34677^` at the
exact paths they were deleted from — 15 in `engineering/`, 2 in `governance/` (`apex-gate-evaluator`,
`apex-verdict`), plus `code-review` and `skill-creator` (excluded from the first pass because a body
of the same NAME lives elsewhere, so a basename test passed while the path was still empty).

```
phantom_views   24 -> 0
gate            FAIL fail=1  ->  WARN fail=0
```

Manifest with per-file inverse (`rm <path>`): `forge_work/skill-hardening/restore-deleted-bodies.json`.

**Lesson for the record:** "the names look retired" was an inference from an empty directory. The
evidence that settles it is one level down — did a body ever exist, and what removed it. Same defect
class as the Wave-2 tombstones: a consolidation that recorded success while removing content, silent
because nothing errors when a body disappears.

The affected names were: `verify-work · security-audit · apex-gate-evaluator · apex-verdict ·
mcp-testing · incident-response · skill-inventory · cicd-deploy · federation-health · vps-ops ·
mcp-ops · skill-drift · drift-watch · pr-governance · telemetry-watchdog`.

## 6. State at close (verified from disk, not from memory)

```
gate verdict          WARN   fail=0  (all FAIL-class checks clear)
broken_symlinks       0
dead_internal_pointers 0
merge_completeness    14/14 PRESERVED
missing_frontmatter   0
phantom_views         0      (was 24)
commits    AAA 88d662825 [proposals/orthogonality-v02-hermes-mapping]
           .hermes 40f9b8c [main]
           scripts 9487667 [master]
```

**Note the branch.** The AAA work sits on `proposals/orthogonality-v02-hermes-mapping`; `main` is 26
commits behind. A `git checkout main` reverts the entire shape change. That is a fact the seal
decision should account for.

## 7. Seal candidate

**Proposed for F13 ratification, not sealed:**

> **A tombstone is a claim, not a move. A view that resolves is not a capability that loads.**
> Every recorded retirement, merge, or re-point must be verified by *content at the destination*, and
> every advertised capability must be proven by *a body at the path*, or it is a false all-clear.

This is the same invariant as the federation's own state-transition law — `PRODUCED ≠ SENT ≠
DELIVERED` / `RESOLVED ≠ AUTHORIZED` — extended to two surfaces it had not reached: the skill
store's retirement records, and its view symlinks. Both failure modes are silent in the same way: no
error, no log line, the agent simply stops knowing a thing it believes it has.

**Witness:** measured, not asserted — 14/14 tombstones re-verified, 24 phantom views found, 6 claims
falsified against the live gate, 3 self-errors recorded above. Gate: WARN, fail=1 (declared).

**Authority boundary reached:** executing the §5 naming decision, or ratifying this into canon, is
the sovereign's. I stop here.
