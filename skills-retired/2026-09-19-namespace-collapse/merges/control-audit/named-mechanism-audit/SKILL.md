---
name: named-mechanism-audit
description: "Use when auditing whether a named control actually acts."
version: 1.0.0
owner: Hermes
risk_tier: low
floor_scope: [F2, F4, F11]
autonomy_tier: T1
tags: [audit, false-name, control-integrity, self-attestation, verification]
triggers:
  - "is this actually enforced"
  - "does this gate work"
  - "verify this safeguard"
  - "the control is present"
  - "privacy filter is on"
  - "0 rejections"
  - "gate passed"
  - "is this wired up"
  - "verify a claimed control"
  - "false name"
  - "named but not installed"
  - "hardcoded metric"
---

# Named-Mechanism Audit

> Audit the question "does it exist?" against the question that actually matters:
> **"can it refuse?"**

## The core law

Presence, naming, imports, documentation, and metadata are all satisfiable **without a
mechanism**. A control that is named but not installed is more dangerous than an absent
control: absence is visible, and a name is believed. An absence gets rebuilt; a false name
gets relied upon.

Every shape below is one defect in different clothes — a claim of function that the artifact
itself falsifies. That is why the audit works: **you can check the claim against its own
output**, without trusting any narrator.

## Three decisive tests

Run all three on any claimed control. Each is cheap, and each has caught defects that looked
healthy from every other angle.

### 1. Can it refuse?

Drive it with input that MUST fail. A gate whose failure branch returns the best remaining
candidate has no failure branch — it re-ranks.

```bash
grep -n -A6 "def .*gate\|def .*check\|def .*verify" <file> | grep -i "return"
# suspect: a bare `return ranked` / `return default` / `return True` after a failed check
```

Ask the follow-up too: **has it ever fired?** A check that has never produced a rejection in
its whole history is unproven. Plant a fixture that must trip it, then confirm it trips.

### 2. Is the label DERIVED or ASSERTED?

```python
# ASSERTED — drifts from reality the moment the producing code changes
report["privacy_filter"] = "arif-only"     # hand-written intent
report["rejections"]     = 0               # lives in the source, not the data

# DERIVED — cannot contradict, because it IS the renderer's input
report["od1_excluded"] = ("od1_days" not in payload)
```

A label computed from the artifact cannot contradict it. A hand-written label can, and
eventually will. **Sort fields by origin, not by name.**

Tell: a field holding the same value (`0`, `"none"`, `"active"`) no matter the input. Diff it
across two runs with genuinely different inputs — a constant that never moves is a literal,
not a measurement.

### 3. Who authored it, and who benefits?

An attestation written by its own beneficiary is not an attestation. Look for the
**independent witness**, not the record of authority.

```bash
grep -rn "RATIFIED\|APPROVED\|reviewed_by\|attested" <record-file>
# then: read who wrote it, and ask whether they are the party the record protects
```

Two signals: (a) no artifact from an independent party exists for the event, (b) the
recording agent is the one whose work is being recorded.

## Shape catalogue

| Shape | Looks like | Decisive probe |
|---|---|---|
| **Decoy gate** | Gate module with full validation logic | List its callers — zero callers = doctrine, not control |
| **Frozen metric** | `rejections: 0`, `drift: none` | Is it computed, or `0 if <flag>`? Flip the flag and re-run |
| **Metadata vs artifact** | `filter: on` in the header | Search the RENDERED output for the thing it claims to hide |
| **Stored not computed** | A countdown, age, or delta field | Run it on two dates — a value that never moves is a literal |
| **Blocklist as policy** | "freshness check" | Read the predicate — banned strings defend only known-bad values |
| **Non-refusing fallback** | Gate with a default branch | Force every candidate to fail; non-empty result = soft bypass |
| **Defaulted reason code** | `reason_code or "SOME_REASON"` | A default string is a measurement-shaped hole |
| **Trigger on a label** | Fires on `state == DEGRADED` | Compare the sibling field (`drift: false`) in the SAME payload |
| **Import-and-not-use** | Module imports a capability | Grep past the import lines — imported is not installed |
| **Self-attestation** | "Ratified"/"approved" record | Did the beneficiary author it? |
| **Evidence from a dead endpoint** | Receipt cites a health check | Probe that exact endpoint; a hardcoded banner validates nothing |

## Procedure

1. **Grep the existing audit corpus FIRST.** A system that has audited itself once has usually
   already named the family (search for verdict words like `FALSE_NAME`, `MISLEADING_NAME`,
   `PARTIAL_NAME`). Citing the prior finding beats re-deriving it, and it answers the question
   that matters: is this an incident, or a family?
2. **Locate the enforcing code path**, not the claim about it. The check must live in the code
   that produces the output. A flag honoured by one writer and ignored by another is not a
   boundary — it is an optional convention.
3. **Drive the failure path** (test 1). Report whether rejection is even reachable.
4. **Diff metadata against artifact** — search the OUTPUT for the property the metadata claims.
   This is the highest-yield single check in the skill.
5. **Re-run across a boundary that changes the answer** (two dates, two audiences, two input
   classes). Constants reveal themselves only under changing input.
6. **Attribute to the owner** of registration/enforcement, then state the fix shape.
7. **State plainly what fixing one instance does not fix.** If the family persists, the family
   is the finding.

## Reporting contract

### Name the state you reached, not a boolean

```
PRODUCED != SCHEDULED != FIRED != DELIVERED != OBSERVED != ACKNOWLEDGED
```

"Ran", "sent", "done", "merged" are transition lies. Name the chain position, and name which
links are still unproven.

### A refused authority is a state, not a failure

When a seal/judge path returns a refusal, record `REFUSED` together with the returned reason
and the measured facts beside it. **Never relabel the artifact "sealed".** A receipt that
overstates its own authority is the same defect class as a metric that overstates itself —
and an auditor who commits it has imported the disease they were hired to find.

Separate the two meanings of a hold: **governance hold** ("not yet proven") versus **broken
gate wearing governance vocabulary** ("the reason code was defaulted, not measured"). When
reality contradicts the refusal, report both the artifact state and the gate defect: a gate
that cannot be trusted to close correctly cannot be trusted to open.

### Publish your own retractions in the same artifact

A report carrying only findings against others is half an audit. Apply the same scrutiny to
your own working claims, and when one of yours fails, retract it **in the same document** with
the mechanical cause — a correction you surface yourself costs far less credibility than one
a peer finds later.

A retraction must **replace**, not hedge: give the new state, not a downgraded confidence that
leaves the old claim standing in the record.

## Pitfalls

- **A null result is only evidence of absence if the query COULD have matched.** Before citing
  an empty search, run the same query shape against something you know exists. If the control
  also returns nothing, the query is broken and the null carries **zero** evidence. Generated
  store prefixes (`doc_<hash>_`, `<session-id>_`, UUIDs) break name-anchored globs: use
  `-iname '*term*'` or content search, never `-name "TERM*"`.
- **The counter-question is not the finding.** Proving a sibling's claim wrong does not make
  yours right; verify your replacement value from the source of truth separately.
- **Distinguish the two clocks.** If one component computes a value and another reads it from
  the canonical store, you have two answers to one question. Trace which components read the
  store and which compute their own — the ones that compute are where the drift lives.
- **Do not fix under a race.** Before patching, check for a concurrent writer on the same file
  (`find <dir> -newermt "-6 minutes" -type f`). A repair applied while another agent writes
  becomes the second defect.
- **A gate that caught its own author's error is the only gate worth trusting.** Prefer the
  check that failed on your own work at least once.

## Boundaries

This skill audits **whether mechanisms function**. It does not grant authority to change what
it finds. When the defect sits in a protected or governance-owned path, report and hold — do
not self-authorise the repair.

DITEMPA BUKAN DIBERI.
