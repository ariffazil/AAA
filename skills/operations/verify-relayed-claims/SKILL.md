---
name: verify-relayed-claims
description: "Use when acting on another agent's status report."
---

# Verifying Relayed Claims

Another agent's report is testimony, not measurement. When the sovereign pastes a verdict, an audit, or a "probe receipt" and asks what to do, ground each claim in something you measured yourself, then label it honestly. Agreement without grounding is how a federation grows folklore.

## Three labels, applied to every claim you repeat

- **VERIFIED** — measured in this session, with the command and its raw output beside it.
- **REPORTED** — the other agent said so; you did not measure it.
- **UNKNOWN** — cannot be measured from where you sit.

Never let REPORTED drift into VERIFIED inside your own summary. Say "I read it" separately from "I checked it".

## Rules that catch most errors

**One probe is a picture, not a line.** Do not infer direction from a counter across samples and call it a trend. Rolling windows, lifetime counters, and resets all produce the same shape. Without two controlled captures, report the number and refuse the direction.

**A counter that moves while the verdict is frozen measures lifetime, not work.** If the execute count climbs while verdict and diagnosis do not change, the engine is counting heartbeats. Volume is not verification.

**Absence of a field is not zero.** A tool named after a metric that omits that metric from its payload cannot verify the metric. Report "the probe does not emit it" — never "it is 0" and never "it is fine".

**Measured ≠ unmeasured ≠ failing.** `unmeasured_default`, "no instrument", and "empty signal" are coverage gaps — neither a pass nor a violation, and each demands a different repair. Name which of the three you are looking at.

**Same path, two hosts — both can be true.** Two agents describing one file path on different machines are not in conflict. Establish host and container name before refuting anyone. The same filename holds different contents in different containers; a claim is only contradictable once the host is pinned.

**Grep the provider's own words, not the status code you expect.** Searching for a literal `402` finds nothing when the provider emits `Insufficient Balance` as an exception body. Anchor on the message text you actually saw in a log, then widen the pattern.

**Who answered ≠ who failed.** A successful response's `served_by` / resolved model says which fallback took the call. It says nothing about which upstream credential was empty. Failure attribution needs the failing call's own chain.

**Aggregate gates are minimums.** When a rollup takes the minimum across actors, repairing the actor you own does not lift the aggregate while another actor sits lower. Enumerate every actor, find the minimum, and name all of them before proposing a fix.

**Comparison across time is not contradiction.** "All passing" recorded earlier and "degraded" measured now are both accurate. Carry the timestamp or drop the comparison.

**A verdict over unmeasured items is UNKNOWN, not PASS.** If the gate you are relying on returns null, say null and stop. Do not average it into a green.

## Procedure when handed a report

1. Extract the load-bearing claims as numbered items.
2. Mark each REPORTED and note whether it is measurable from your seat.
3. Measure what you can — one command each, keeping raw output.
4. Re-label each: VERIFIED / REPORTED / UNKNOWN, with the command beside it.
5. Only then give a verdict.

## Do not

- Do not write your receipt in the shape of the one you are auditing. If the report lacks an independent witness, yours does too — say so instead of borrowing authority.
- Do not fill an empty slot in someone else's template with a hypothesis and leave it unlabeled. Unknown is a legitimate value; invented content is not.
- Do not treat two agents reading the same corpus as independent verification. Same source, same lens is one witness twice.
- Do not accept a short eight-character SHA as a hash. Ask for the full hex before treating it as evidence.
