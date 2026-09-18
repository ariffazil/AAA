---
name: live-system-audit-discipline
description: "Use when auditing a live system or reporting probe results."
version: 1.0.0
license: MIT
---

# live-system-audit-discipline

> Auditing a system that is running while you investigate it. The characteristic failure is not
> missing evidence — it is stating more than the probe supports. Report the surface, the method,
> and the coverage; scope the claim to what you actually read.

## Every claim carries its method

A denominator without a method is not evidence. `0/1338` is three different claims depending on
how it was produced: every line scanned, a handful parsed, or a sample. State the method AND the
coverage alongside the figure — "full scan, exact marker" is a different object from "9 parsed".

A precise-looking number that cannot say how it was obtained is an unattributed claim wearing an
evidence costume.

**Decompose before you build on a figure, not just before you publish it.** A count inherited
from another writer carries their undecomposed denominator into your conclusion. Split it into
parts first — a large total often collapses to almost nothing once one contaminated source is
separated out. Do not propose a rule or invariant on an inherited denominator you have not
broken open yourself.

## Absence carries the same warrant as presence

"No drift found", "not in the registry", "no caller exists" are claims, not defaults. Each
states where you looked, on which host, and by which method.

- **Host-pin existence claims.** A miss on one node is not a global absence when the same
  logical name resolves to a different store elsewhere. Find which path the consumer actually
  reads before concluding anything about "the" store.
- **Never widen a single-surface probe into a claim about the system.** One endpoint, one
  client, or one output mode is a midpoint, not the organ. Probe a second surface, or scope the
  claim in the sentence itself.
- **An echo is not a measurement.** Before reporting a value as the system's, vary the
  parameter you sent and confirm the answer changes with it; some endpoints return what the
  caller supplied, so a fixed probe measures only itself.
- **Re-verify immediately before you write.** On a live shared repo another writer may land
  between your read and your patch. Re-check mtime/hash at write time.

## Two surfaces disagreeing is a finding, not a contradiction

When surface A and surface B report different values, the correct output is the divergence
itself. Do not resolve it by picking the one that matches your expectation, and do not assume
one is stale without evidence. Report both, then probe a third to locate the fault.

## Depth

`references/live-probe-discipline.md` — served artifact vs working checkout, same-name-two-stores,
working while others write, independent verification, treating a blocked mutation as a result.
