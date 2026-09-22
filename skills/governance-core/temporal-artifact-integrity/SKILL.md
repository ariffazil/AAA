---
name: temporal-artifact-integrity
description: "Use when a countdown or hash-sealed ledger must verify."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Temporal Artifact Integrity

Four laws, each learned by finding the defect live. Every one of them fails
SILENTLY: the artifact looks correct while being wrong, so a reader who checks
the newest state sees success.

## Law 1 — One clock, or none

Exactly ONE component may compute a day-count. Every other component reads it.

A second clock does not create redundancy; it creates two truths. Observed: an
engine carried its own `_chrono()` returning 377 days for an event whose
canonical store said 21, while both fed the same product. Nothing crashed.
Neither number looked wrong on its own.

**Rule:** a content supplier does not own time. If two components can each
answer "how many days until X", delete one.

**Also compute dates, never offsets:** `(target - today).days` on `date`
objects. Subtracting `datetime` objects truncates the partial day and every
count is silently 1 short.

## Law 2 — Content-address the artifact, or the ledger rots

A ledger row is only worth keeping if its hash can be RE-CHECKED later. If the
artifact lives at a fixed path and each run overwrites it, every earlier row
records the hash of a file state that no longer exists.

Observed: 4 of 7 rows stale, all because the renderer wrote
`ALPHA-ZEN-{MODE}.png`. A verifier who checked only the newest row reported
"chain intact".

**Rule:** name the artifact after its content hash and keep the stable name only
as a copy for any consumer that requires a fixed path.

```python
h8 = hashlib.sha256(source.read_bytes()).hexdigest()[:8]
artifact = out / f"NAME-{h8}.png"        # ledger points here — never moves
stable   = out / "NAME.png"              # delivery contract points here
...
stable.write_bytes(artifact.read_bytes())
```

## Law 3 — A constant in a ledger is a claim, not a measurement

`privacy_rejections: 0` is not "none were rejected". It is an assertion that the
funnel was measured and found empty, on no evidence. Worse than a missing field:
a reader who greps for the control finds it and concludes protection exists.

**Rule:** if nothing populates a field, write `null` and a sibling
`*_tracking: NOT_MEASURED`. Never `0`.

## Law 4 — Word-bound the gate, or it gets switched off

A gate that fires on correct content is worse than no gate: it trains its own
removal. Observed: a privacy gate rejected `forward-deployed` (contains "ward")
and `ketakselarasan` — the geology term for an unconformity — because it
contained "rasa".

**Rule:** every deny pattern uses `\b` — but only on PROSE. Host paths and
identifiers (`/root/|file://`, `niat_candidates|carry_forward`) are literal
tokens where a boundary is meaningless; requiring one there is itself a false
alarm.

Ship a two-way self-test: a list the gate MUST catch and a list it MUST allow.
A detector that has never rejected anything is decoration.

### The writer of the gate will make the same mistake

Measured, not hypothesised. A nine-check spine gate was written specifically to
catch this defect, and its own self-test then caught THREE false alarms inside
it:

1. It read `cell.tier` when the field is `cell.tag` — failed a correctly tagged
   artifact.
2. It required `\b` on literal path patterns — failed a correct privacy set.
3. It regexed for a module constant when the mode was an env var — reported
   UNBUILT on a component that was provably live.

The cause was structural: the self-test covered 4 of the 9 checks, so the other
five were free to be wrong. **Cover every check in the self-test, both
directions — accept-on-good and reject-on-bad.** And name helpers for what they
return: an inverted name (`_unbounded_ok` that returned "has unbounded") made
the test read its own inverse.

Write the false alarms INTO the file as comments. A quietly corrected false
alarm teaches the next reader nothing.

### UNBUILT is a verdict, not a pass

A boundary with no artifact yet must report UNBUILT, never PASS. Reporting PASS
because nothing currently violates a rule is the same confident-falsehood class
as a permanently-zero counter: it reads as protection that does not exist.

## The shared failure shape

All four defects are the same shape: **the claim was checked against the newest
or most convenient state, and is true of that state while false of the object it
describes.**

So when a report says "verified", ask which state was inspected. Verified-here
is not verified-everywhere.

## Retired things must say so

A scheduler that reconciles a declared registry against a live one will report
every retired entry as drift, forever, burying the real ones. Mark retirements
explicitly (`status: retired`) and have the reconciler skip them. Count the false
alarms removed — 1 per run x 96 runs/day = 96/day in the observed case.

## Permanent conflicts are not failures

A loop failed 169 times trying to rewrite an append-only vault file. Not a bug:
two deliberate rules that cannot both hold. The fix is a clean SKIP naming the
conflict, never a retry loop or a weakened guarantee.

## Pre-flight before any scheduled send

1. Clock reads live, and matches the canonical store.
2. Ledger rows resolve (hash matches bytes on disk).
3. No false alarm currently firing in the log it shares with real alerts.
4. Artifact exists at the exact path the delivery contract names.

## DECLARATION != ENFORCEMENT — the control-name defect family

Seven instances in one session were one defect wearing seven names: a gate
module with zero imports, a rejection funnel of constants, a privacy flag its
own artifact contradicted, a receipt naming a nonexistent file, a
self-authored ratification, a liveness endpoint returning a literal, and a
ledger gate that printed `[BLOCK]` 2862 times while exiting 0.

**The invariant:**

```
SEMANTIC_AUTHORITY = NAME ∩ CALL_PATH ∩ MEASURED_EFFECT
                   ∩ BYPASS_RESISTANCE ∩ EVIDENCE
```

Any empty term → `AUTHORITY_CLAIM = VOID`. Not FAIL: VOID — the claim was never
valid, so there is nothing to be wrong about. Auditor:
`/root/AAA/scripts/semantic_authority_gate.py` (verdicts BOUND / VOID /
UNTESTED / ARTIFACT; UNTESTED is honest and is NOT a pass).

**Three questions replace the old ones.**

| old question | question that matters |
|---|---|
| Is there a security gate? | Can an action happen WITHOUT passing it? |
| Is there a liveness check? | If a dependency dies, do the bytes change? |
| Is there a sandbox? | Can a payload escape the containment path? |

**A guard that cannot fire is a guard-shaped comment.** Two stacked dead guards
observed: the caller hardcoded `--dry-run`, the callee only exits non-zero when
not dry-run, so the caller's `RC -ne 0` test was unreachable even with the
strict flag set. Check the whole chain, not each link.

**A control's proof depends on its invocation mode.** A library must be
imported. A CLI must be scheduled or invoked by path. Requiring imports of CLI
tools flagged 40+ working scripts as orphans — including the auditor itself.

**Rename before fix.** A banner called `liveness` is a working banner with a
dishonest name, and the name is the hazard. Correcting the name ships in
seconds; the name is what misleads, not the missing measurement.

**When your own auditor trips this defect, say so in the file.** The semantic
auditor above fired 40+ false orphans on run one and invented 14 endpoints on
run two. Both are recorded in its own comments. A quietly corrected false alarm
teaches the next reader nothing.
