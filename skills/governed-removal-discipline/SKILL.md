---
name: governed-removal-discipline
description: "Use when asked what to delete from a governed system."
version: 1.0.0
triggers:
  - a list of fields, gates, or vocab tokens is proposed for deletion
  - "this is security theatre / dead code / always null — remove it"
  - "what should we remove / clean up"
  - a sibling agent pastes a cleanup report for review
  - a field, flag or vocabulary token is labelled deprecated, unused or always-empty
  - a removal needs a live daemon restart
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Governed Removal Discipline

In a system that seals its own history, deleting is asymmetric: one line removes a field, and
thousands of records can no longer be compared. The second expensive error is deleting a control
because its *reporting* was wrong.

This skill governs the decision **what to remove**, not how to audit a claim in general.

## Procedure

### 1. Classify every proposed item before touching anything

Four kinds. Only two are deletable as stated.

| Claim | Test | Verdict |
|---|---|---|
| "always null" | count non-null across the **whole** store, not a sample | 0/N → dormant, read step 5 |
| "deprecated" | grep the **consumers**, not the producer | read step 3 |
| "never used" | grep emitters / call sites | 0 outside the definition → dead |
| "wrong value" | compare the value's shape to the field's name | read step 4 |

Report each item as BETUL / SEPARUH / SALAH with the count that proves it. A list of eight
proposals routinely contains two that are wrong in a way that would delete a working control.

### 2. Before deleting a field, find the hash that covers it

```bash
grep -rn "compute_.*_hash\|jcs_sha\|canonicalize" <repo>/src | head
```

If the hash serialises the whole struct (canonical JSON minus the hash field itself), removing or
renaming ANY field changes every future hash and breaks comparability with the sealed history.
Deletion is then legal only at one of:

- the projection / response layer — stop emitting it, keep it in the struct;
- a versioned schema migration with an explicit boundary in the chain.

Never delete from the struct first and reason about the chain afterwards.

### 3. Grep the consumer of anything called deprecated

The producer's label does not bind the consumer. When a deprecated and a current measure are both
emitted, the consumer decides which one a human sees, and `legacy_x or x` silently prefers the
fossil.

```bash
grep -rn "legacy_" --include=*.py --include=*.ts --include=*.rs <repo> | grep -v "/build/"
```

Also check that the replacement is the same **kind** of value. Two current fields can live on
different axes (a scalar band vs a vector constellation). Swapping one for the other replaces a
stale truth with a category error. When the payload emits nothing current on that axis at all, the
finding is "which axis does this surface represent" — an owner decision, not a deletion.

### 4. Remove the lie, not the measurement

A field is removable when its name and its content disagree, or when its formatter erases a
distinction. Both are reporting defects; the value behind them is usually sound.

- A field named `*_utc` carrying seconds-since-process-start. Emit a real timestamp, put the age
  in its own field, and state the window's basis alongside it.
- A status string formatting an optional quantity numerically: `None → 0.0` makes "could not be
  measured" identical to "measured zero". Print the underlying counts and say `UNMEASURED` where a
  quotient is not computable; keep the option type all the way to the formatter.
- A hold or alert whose stated reason came from a window that has since been replaced. Fix the
  reason string; do not release the hold.

### 5. Separate dormant from dead

```bash
grep -rn "<SYMBOL>" --include=*.py <pkg> | grep -v test | wc -l
```

- 0 references outside the definition → **dead**: removing it removes vocabulary only.
- Live call sites, 0 populated instances → **dormant**: the gate is present and wired. Deleting it
  deletes a capability. Report "never exercised since <date>" and leave it.

The distinction decides the action, and it is visible only by counting both sides.

### 6. Price the restart before deploying the removal

If the change needs a live daemon restart, determine what the restart resets and what it makes
falsely true. A restart that empties an evidence window while durable state survives will **add**
alerts immediately after your fix and make the fix look like a regression. State this before
deploying, and again after.

Quick cost model before you restart:

```bash
systemctl show <svc> -p ExecStart -p ActiveEnterTimestamp --no-pager   # what, and since when
ls -la <persist dir>                                                   # what survives
```

### 7. Verify on the live surface, then commit the mechanism

- Build and run the full suite — a reporting change reaches many assertions.
- Deploy behind a timestamped backup of the previous binary.
- Probe the live endpoint and show the new value beside the old one.
- Commit message names the mechanism, not the incident: what the field said, what it now says, and
  explicitly what did **not** change ("no threshold moved, no actor released").

## Pitfalls

- **Deleting a field from a hash-sealed struct.** Composite hashes make field removal a
  chain-breaking change. Projection layer or schema version — never both, never silently.
- **Trusting a "deprecated" label as a statement about consumers.** Producers label; consumers
  choose. A deprecated-band value can be the only one a dashboard ever renders.
- **Reading "always null" from a sample.** Count across the whole store and report `N/total` with
  the store's path so the number can be re-derived.
- **Treating a fired control as noise.** If a gate produces holds, read every reason before
  removing the gate. A wrong reason is a reporting bug; a firing signal is the gate working.
- **Fixing the label instead of the value.** Renaming `window_start_utc` to `uptime_s` is honest;
  leaving the name and changing the meaning silently is not.
- **Reporting a removal as done before the live probe.** A deployed binary is not changed behaviour
  until the endpoint returns the new shape.
- **Letting a cleanup review become the deliverable.** Give the four classifications, the one or two
  items that would cause harm, and the residual. Then stop.

## The one-line test

Would a future reader of the sealed record see the same thing the system sees today? If not, the
removal is a schema change, not a cleanup.
