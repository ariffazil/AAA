---
name: production-capacity-closure
description: Use when a resource, rate and facility may not all be true.
tags: [engineering, production, capacity, closure, fdp, forensics]
---

# Production capacity closure

Use when someone hands you a development case, a debottleneck claim, or a production forecast and you must decide whether the numbers are mutually possible. Applies to field development plans, facility upgrades, asset valuations, and any "can this plant deliver that book" question.

## The principle

**Recovery is an output of the facility-constrained profile, not an input.**

Applying a recovery factor to in-place volume and then asserting the plant delivers that volume is circular. The plant sets the rate; the rate and its decline set the recovered volume. Run the profile with the physical limits applied and report whatever falls out. A shortfall against the booked resource is the finding — it is not a modelling error to be normalised away by raising the recovery factor or stretching the field life.

## The closure test

When several quantities must hold simultaneously, test them in pairs first. A set that is pairwise compatible but jointly impossible is a finding, not a data gap.

For a facility-limited field, derive these four:

```
decline_required    = (rate × 365) / recoverable_volume      # %/yr, decimal form
decline_available   = expected decline given achievable pressure support
injection_required  = rate × Bo                              # for VRR = 1.0
rate_supported      = injection_available / Bo               # rate the plant can actually hold
water_headroom      = liquids_cap - rate                     # bopd of water before oil must fall
```

Then tabulate across the rate range:

| Plateau | Decline needed | Decline available | Injection needed | Injection available | VRR |

Read down the table for a row where **every** column passes. If no row passes, the stated development case cannot be true as written. Report it as OPEN with the arithmetic shown, and name which input would have to move to make it close — resource smaller, mechanism different, or facility larger. Never pick the rate that makes the table look closable; that is the failure the test exists to prevent.

The most common real finding is that a plateau which delivers the booked volume needs sustained full voidage replacement, and the plant's injection capacity cannot supply it. Two of the three numbers are true and the third is being carried on trust.

## Decline is load-bearing — always publish the sensitivity

A conclusion that rests on one assumed decline can be dismissed as an artefact. Before publishing, re-run across the plausible range (roughly 10–35 %/yr for waterflood-supported cases, higher for depletion) and show the table. If the shortfall survives every decline tested, the conclusion is structural and you can say so. If it only appears at one end, it is not a finding — it is your assumption talking.

The algebraic check is worth stating explicitly because it is assumption-free: for a flat-then-decline profile, `EUR ≈ q0 / Di`. A plateau that recovers volume R requires `Di = q0 / R`. Compute the required decline and compare it to what the recovery mechanism can actually deliver. This comparison needs no production history and survives any argument about curve shape.

## Pitfalls

- **Anchor the asset to a specific unit before using any capacity number.** Specs belong to a hull, a train, a plant — not to a class. Resolve by registry or catalogue number (IMO for vessels, serial or tag number for equipment) and carry the anchor as a ledger field. A datasheet found under a former name may be the same asset under two names, or a sister unit with different limits; the name cannot tell you which.
- **A quoted capacity may belong to a cancelled concept, not the live one.** When a project has been re-scoped, older public figures often describe the abandoned design. Tag every facility number with which concept it belongs to, and check the purchase or procurement record before trusting a number that appears in an early-phase document.
- **A ratio of totals is not a solution property.** Field GOR computed as total gas ÷ total oil mixes free and solution gas. It is valid for sizing the gas train against average production, and circular if used to derive voidage or per-well behaviour.
- **Water injection capacity is a recovery constraint, not a cost line.** Over-injection is a cost problem. Under-injection is a recovery problem, and recovery feeds every economic number downstream. Getting the sign of this wrong inverts conclusions across a whole plan.
- **The declared economic limit is not a physical limit.** Never derive the cutoff from a forecast's end date. If the fiscal basis is unresolved, say the economic limit is OPEN rather than borrowing a number — a drainage profile and an economic projection are different objects.
- **Truncation at a horizon is a result, not a detail.** An exponential decline has an asymptote; if the project life is shorter than the time to reach it, the recovered volume is lower than the integral suggests. Check whether the horizon is binding before quoting EUR.

## Reporting an open finding

State it as an open item, not a verdict, and say which of its inputs are unverified. The defensible form is:

> At this rate the facility supports X of the Y required, and no rate that delivers the booked volume is supported. This is stated as OPEN because [inputs] are unverified. What is solid is narrower and still serious: [the assumption-free arithmetic]. Either the volume is smaller than published, the recovery mechanism is different from the one assumed, or the facility is wrong for the field.

That form survives review because it names its own weak points. Asserting the conclusion outright invites one challenge to the weakest input and takes the whole finding down with it.
