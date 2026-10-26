# DEPLOY = STATE DELTA, NOT FEAR (F13, 2026-10-20)

Status: F13_RATIFIED_CHAT (2026-10-20) — sovereign: *"deploy tu mesti work alive and better than previous state"*

> Arif does not have millions of users. Reflexive HOLD is not caution — it is an agent avoiding
> consequence and calling it governance. The gate is **measurement**, not fear.

## The three-state rule — every deploy measures PAST · PRESENT · FUTURE

| State | What must be measured before touching anything |
|---|---|
| **PAST** | last known-good: deployed commit, version, health verdict, error/block count, key path status, rollback artifact location |
| **PRESENT** | live now, same metrics, same probe commands — not from memory, not from a sibling's report |
| **FUTURE** | one sentence: what improves, by which metric, and the falsifier that would prove the deploy made it worse |

After deploy, measure **ACTUAL** and compare to FUTURE. A deploy without a post-measure is not a deploy;
it is a hope.

## When HOLD is legitimate (only these three)

1. **No rollback** — irreversible change with no restore path.
2. **No measurement** — cannot state PAST/PRESENT/FUTURE with live probes.
3. **Active measurement window** — a soak or benchmark is running and a restart would destroy the
   evidence. Name the end time and the owner. Expired window = gate reopens automatically.

Anything else deploys. "Risky", "production", "late", "not sure" are not gates.

## Deploy is allowed when

- rollback exists and was tested (or is a one-command restore with a named artifact),
- the named metric is expected to improve or hold, and
- the post-deploy probe set is written **before** the command runs.

## Improvement is a metric, not a feeling

Use at least three: deploy identity (version/commit matches), service verdict (`/health` + error rate),
primary human path (the actual URL/tool the human uses). Organ-specific invariants may be added, never
substituted. A deploy that changes nothing measurable is not "safe" — it is **no delta**, and should not
be run.

## No acah

- No HOLD without a named gate from the list above.
- No "hold for safety" in a status report — state the metric, the missing measurement, or the window.
- No deploy report that is prose only: before/after table + rollback path + falsifier.
- If the deploy fails: roll back first, report second. A failed deploy left running is the real violation.

## Report shape (mandatory)

```
DEPLOY <target> · <commit> → <commit>
PAST:  <metric=value> …
PRESENT: <metric=value> …
FUTURE: <expected> · falsifier: <what would make it worse>
RESULT: <metric=value> … · verdict PASS|ROLLED_BACK|FAILED
ROLLBACK: <command/artifact> · <time to restore>
```

HOLD is a verdict issued by the gate, never a mood. Deploy that is measured is cheaper than
a system that is frozen and unmeasured.
