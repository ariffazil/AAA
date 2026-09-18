# Instrument Validity — proving the gauge measures what it claims

Hop 5 extended. A live, responding, healthy-looking instrument can still be uninterpretable.
Before citing any agreement, consensus, coverage, or drift number, run these four checks.

## 1. Denominator identity — the measured units must be DISTINCT

An agreement metric is meaningless until you prove its units are independent. A name is not a unit.

**Routing labels are frequently fallback CHAINS, not single backends.** A fleet of N role lanes,
agent seats, or service names can resolve into M < N distinct backends, and the metric silently
reports the agreement of M as though it were the agreement of N.

```
# resolve every unit name to what actually serves it — read the live routing config, not the names
# group: unit -> [backend candidates, in order]
# then count how many units share a backend
```

Measured shape: of 8 role lanes, one backend appeared in 6 of the 8 chains and another in 6 — and
both were degraded at measurement time, so every chain naming them fell through to the *same*
shared fallbacks. Reported "unanimity 1.0" was consistent with **both** "N independent models
converged" and "fewer distinct models, aliased" — and the instrument could not tell the difference.

**So record the SERVING unit per observation, not the requested label.** An instrument that stores
only the alias cannot be falsified later. This is the general rule: *if two different worlds produce
byte-identical output from your instrument, the instrument is not evidence about which world you are in.*

## 2. A resolved label is not a validated denominator

Check what the alias maps to and whether the mapping is 1:1. Report the denominator's real width:

```
drift = 0.000 over 13 lanes            <- a claim
unit_identity = {13 labels -> K backends, K unresolved}   <- a finding
```

If K cannot be resolved, say so and downgrade the verdict to *metric real, denominator unverified*.
Never quote the unanimity number alone.

## 3. Batch-run safety — one dead input must not discard the batch

Before an N×M sweep:

1. **Smoke-test first.** 1–2 units × a handful of items. Confirms auth, routing, and parse path for
   the cost of a rounding error against the full run.
2. **Fail fast per unit on EVERY dead-unit class**, not just the one code the harness was written for.
   A retry-forever path on a rate-limited or no-capacity unit blocks the whole sweep — and if results
   are written only at the end, **every completed call is discarded**.
3. **Write results incrementally per unit.** A killed run must leave usable partial output.

Measured: two full sweeps were killed having produced nothing, because two units were dead (one
quota-exhausted, one with no capacity) and the harness fast-failed on only a single error code. The
lost work was ~2× the successful run.

## 4. Report the method beside the number, and the waste beside the cost

State: denominator width and how it was resolved · whether units were verified distinct · the run's
call count · and any discarded work. A receipt that hides its own waste is not a receipt.

## Output contract

```
metric value      <- the number
unit identity     <- labels -> distinct backends, or UNRESOLVED
denominator width <- N (requested) vs M (verified distinct)
verdict           <- valid | metric real, denominator unverified | uninterpretable
cost              <- calls made / calls discarded
```

With an unresolved denominator the honest verdict is **metric real, denominator unverified** — not
"pass", and not "fail". Refusing to distinguish those is the same defect the instrument was built
to detect, now living inside it.
