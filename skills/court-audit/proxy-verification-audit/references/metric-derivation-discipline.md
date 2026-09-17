# Metric Derivation Discipline

When a scalar in a governance/telemetry envelope surprises you (two calls return different values,
or a value looks like a quality judgement), the default failure is to hypothesise from the
observations. Agents will burn one hypothesis each and all of them can be wrong. Derive instead.

## Order of work

1. **Read the computing function.** Find the formula, the time window, the filter scope, and the
   zero-data branch. The docstring often names the historical bug that produced the current shape —
   read it as a map of what the value is NOT.
2. **Read the DB/table it queries.** Note whether the call site passes a scoping argument
   (`actor_id=`) or omits it. Every call site can differ; grep for all of them and report which
   scope each uses. A function with an optional scope parameter usually has callers on both sides.
3. **Recompute for every observation you hold.** Not a sample — all of them. For each, count only
   the rows that were visible *before* that call, then apply the formula. Report "N/N instants
   match". A model that explains five of six observations is a different model from one that
   explains six of six.
4. **Test sensitivity.** Vary the candidate driver across a wide range and see whether the output
   moves. If history volume spans three orders of magnitude and the scalar moves half a percent,
   volume is not the driver — say so explicitly, because "more data ⇒ better score" is the
   intuitive reading everyone will assume.
5. **Only then propose a mechanism**, and name the line numbers.

## Trap 1 — the floor constant

A geometric mean over clamped factors returns the root of the clamp whenever any factor is zero:

```
G = (max(0.01,A) * max(0.01,P) * max(0.01,E) * max(0.01,X)) ** (1/4)
P = 0, A = E = X = 1.0   →   G = 0.01 ** 0.25 = 0.3162
```

Recognise it: the observed value equals `<floor> ** (1/num_factors)` exactly, and *many* different
actors all show the same number. That is not agreement between actors; it is the floor speaking.
Report the constant and the reason it dominates (which factor is zero), then report the underlying
ratio fleet-wide — the zero factor is usually the real finding, and the scalar's narrow range is
precisely why it hides it.

Also check derived siblings: a term of the form `A*(1-P)*(1-X)` returns `0.0` when `A=X=1`, i.e. the
"nothing concealed" reading appears exactly when evidence is absent. A zero there is an artifact,
not a clean bill.

## Trap 2 — the cold-start regime and self-referential thresholds

A zero-data branch returning an explicit sentinel (`UNMEASURED` / `None`) is honest design, but it
creates a threshold that is easy to misread:

- `n = 0` → sentinel for every scalar
- `n ≥ 1` → computed, deterministic for the same row set

The measuring call is frequently the call that writes the first row. So an actor's first probe
returns UNMEASURED and its second returns a number, with nothing else changed. Do not attribute
that to transport, client, actor state, or runtime entropy — count the rows that existed at each
instant and the pattern explains itself.

When you hold two observations that differ, enumerate every variable that actually differed between
them (actor, lane, transport, time, prior history) and eliminate each one against data. The
surviving variable is the answer even when it is boring.

## Trap 3 — literal witnesses

Search the path that emits a "witness", "consensus", "diversity" or "confidence" field for
hardcoded numbers:

```
_hw = 0.95 if actor_verified else 0.42
_aw = 0.94 if <profile loaded> else 0.32
_ew = 0.93                      # unconditional literal, no sensor
score = round((_hw * _aw * _ew) ** (1/3), 4)
```

Recompute the literal combination and compare with the observed value. An exact match proves the
field is a restatement of the verified/unverified branch, not corroboration from independent
channels. Two consequences worth stating:

- It must never be cited as independent confirmation of an identity, a claim, or another metric.
- Note which branch the literals live in. A backfill inside `if not already_minted:` runs only for
  actors that pass the earlier gate, so unverified callers keep the honest sentinel while verified
  ones get the inflated number. The most convincing-looking score is the one awarded purely for
  passing a lookup. Verify this by reading the branch, not by inferring it.

Also check for a neighbouring module that deliberately refuses a proxy for the same field ("honest
None, never an inflated proxy"). The discipline holding in one file and being re-introduced as
literals three files over is the finding — cite both.

## Trap 4 — the label that outlives the meaning

When a scalar is derived this way, write the corrected label into whatever artifact you produce:

> `<metric>` — telemetry observation, not governance authority; computed from <source> over
> <window>; `<sentinel>` when history is empty; approximately `<floor>^(1/k)` whenever
> <factor> is zero. No gate may read it.

Then state the consequence for fixes: a control that depends on this scalar depends on whether the
caller happens to have prior rows in one table, i.e. on a history accident rather than on intent or
identity.
