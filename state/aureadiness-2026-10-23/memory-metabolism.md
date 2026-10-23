# Memory Metabolism — P0 #2

**measured** 2026-10-23T03:48:28+00:00 · host forge · observer hermes-kvm8 · classification OBSERVED_SELF
**action taken: analysis only. Nothing deleted, nothing rewritten.**

## Three measurements of the same two quantities (none agree)

| quantity | brief (PDF) | on disk now | injected at session start |
|---|---|---|---|
| USER.md | 10,590 / 10,000 (over 590) | **10,435** (over **435**) | 10,435 / 10,000 (100%) |
| MEMORY.md | 16,171 / 16,000 (over 171) | **15,958** (under by **42**) | 15,614 / 16,000 (97%) |

Recorded as a contradiction, not resolved by preference. The *config* budget is unambiguous:
`memory_char_limit: 16000`, `user_char_limit: 10000`.

**Two real findings:**
1. USER.md **is** over its hard budget (10,435 > 10,000). That is a live admission defect.
2. MEMORY.md is **not** over budget on disk (15,958 ≤ 16,000) — the brief's 16,171 does not
   reproduce. But the injected figure (15,614) is 344 chars smaller than the file, so the
   injection path is measuring something other than the raw file. Which measure gates admission
   is **UNKNOWN** and matters more than the number.

## Entry census

| file | entries | median | max | tags present |
|---|---|---|---|---|
| USER.md | 36 | 299c | 638c | 12 distinct |
| MEMORY.md | 50 | 241c | 1,591c | 21 distinct |

Classification across both files (86 entries):

```
GATE           22   binding rules — never delete, never compress below the imperative
SCAR            8   behavioural scars — keep, they are the point
LEDGER         28   dated facts about state (ENV/MAP/CAPABILITY/ARCH)
EPISODE         3   one-off events
SKILL_OR_NOISE 25   overlaps a skill body or is no longer load-bearing
```

## What can move without loss (proposed, NOT executed)

**Procedural blocks in MEMORY → skill references** — 3 entries, **649 chars**, all of which
already have a canonical skill home:

| chars | entry | existing home |
|---|---|---|
| 276 | `[ENV] WIKI wiki.arif-fazil.com: producer /root/scripts/wiki-build.sh …` | skill `wiki-arif-fazil-ops` |
| 231 | `[ENV] Git commit arifOS/AAA/WEALTH/WELL = LANE IDENTITY GATE …` | `/root/AAA/instructions/build.md` + git-lane header |
| 142 | `[CANON LOCK] /root/AAA/governance, canon, GENESIS chattr +i …` | `canon-mutate --help` (self-documenting) |

Moving these frees 649 chars in MEMORY — more than the brief's reported 171-char overage — and
**loses nothing**, because the knowledge already lives in the destination and is reachable there.

**Dated LEDGER entries** — scan caveat: the classifier only inspected the first 88 chars of
each entry, so this count is a **floor, not a total** (0 found in that window; dates commonly
appear later in an entry). A full-entry scan is required before acting on this class. They are
history. Proposed: move the *specific* ones whose claim has since been superseded to an episode
ledger, keeping the still-true routing fact in memory. **Requires a per-entry judgement by ARIF or
a designated owner; not automated here**, because a dated ENV fact is often still the current
address (e.g. ports do not expire).

**USER.md overage (435 chars)** — the candidates are the longest PREF/WORLDVIEW entries. **Do not
touch the `[CORE INVARIANT] "Arif is Arif"` line** (638c) — it is the highest-value entry in the
file and the one whose loss would cost most. The safe cut is an older `[WORLDVIEW]` block whose
content is already carried by `SOUL.md` and the `/root/AAA/instructions/` fragments.

## The rule this must obey (from F13)

> Never delete memory only to satisfy size.

So the gate before any write:

1. classify the entry (GATE / SCAR / LEDGER / EPISODE / SKILL / NOISE)
2. prove the destination exists and is reachable
3. record provenance, owner, status and falsifier for the moved item
4. emit before-hash and after-hash
5. emit a **loss ledger** naming exactly what text is no longer in the hot prompt and where it now lives

Until that gate runs, this file is a plan, not a change.

## Verdict

```
MEMORY ADMISSION: AT_LIMIT      (42 chars free on disk; injection path measures differently)
USER ADMISSION:   OVER_BUDGET   (435 chars over a hard limit — live defect)
```

## Falsifier

If `wc -m` on both files differs from this table at re-measure, or if `memory_char_limit` /
`user_char_limit` in config.yaml have been changed since, this analysis is stale and must be redone.
