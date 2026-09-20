# Running a Store-Repair Campaign with Fan-Out

Companion to SKILL.md §6–§9. Consolidation of a skill family is parallelisable, but the parent owns
the verification. These are the rules that cost real defects when skipped.

---

## 1. A child's self-report is not evidence

Subagent summaries are claims, not observations. A child that says "merged, verified, all checks
passed" may still be wrong — not through dishonesty, but because it checked its own work with the same
assumption that produced the defect.

Verify on disk, per item, as the parent:

```
canonical file exists and is non-trivial in size
retired bodies GONE from the live tree            (not merely "moved")
frozen bodies PRESENT with matching digests
ledger parses, and every recorded frozen_path resolves
replacement links resolve (readlink -f), and the census reports broken=0
```

A cheap parent-side sweep script that walks every merge dir and prints these five facts pays for
itself immediately — in practice it caught a merge whose successor path was claimed but did not
exist, and another that left a stale alias dangling.

---

## 2. Run the retention gate yourself, over EVERY landed merge

Do not accept the child's own retention check as the gate. Re-run the discovery check
(`scripts/discovery_guard.py`) from the parent over all landed merges, including the ones the child
reported clean.

Measured outcome of doing this: two merges that had passed their own per-task checks still had lost
discovery — one had dropped every retired name from the merged body (an agent searching the old name
would find nothing and re-author the capability), another had lost the single most distinctive phrase
of the absorbed skill. Both were repaired before the sources left the tree. Had the parent trusted the
reports, the library would have ended LARGER than before the cleanup, six months later, with no trace
of why.

---

## 3. Never edit a file a child is currently writing

When a child is mid-write on a file, patching it from the parent races it: the child's next write
clobbers the edit, or the edit lands inside a half-written body. **Steer the child instead** — send it
the requirement ("this block must survive your next rewrite") and let one writer own the file. Record
which files each child owns before dispatch; disjoint paths are the cheapest correctness guarantee in
a fan-out.

---

## 4. Repoint the mirror views as part of the campaign, not after

Every retirement produces dangling links in every harness mirror, and the count is not small
(one retirement wave produced 47 across eight trees). Run the view sweep before declaring the campaign
done, and resolve each link by rule: **repoint** when the name has a live successor, **remove** when
the name itself is retired. Re-run the census afterwards — a campaign that turns `broken_symlinks`
from 0 to N fixed the bodies and forgot the views.

---

## 5. Give each child one family and one verdict rule

A child asked to "clean up the audit skills" will invent a taxonomy. A child asked to "merge these
six named bodies into this one existing name, organised as modes, preserving every trigger phrase, and
freeze the five losers" produces a verifiable result. Name the survivor explicitly (choose an EXISTING
name — never invent one), state the classification vocabulary it must use, and require the ledger
schema. Ambiguity in the brief becomes entropy in the store.

When a family turns out to be genuinely distinct, a child that reports "no merge recommended" is a
success, not a failure — say so in the brief, or you will get a merge manufactured to satisfy the
task.
