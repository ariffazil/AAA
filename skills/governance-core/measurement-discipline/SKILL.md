---
name: measurement-discipline
description: "Use when claiming a system bottleneck, cost, or capacity."
triggers:
  - "bottleneck"
  - "what is limiting"
  - "is it compute or memory"
  - "context tax"
  - "how many tokens"
  - "it is slow / slow response"
  - "the model is down"
  - "capability is missing"
  - "optimise this box"
  - "more hardware"
---

# Measurement Discipline

A diagnosis is only as good as its arithmetic, and most capacity findings are manufactured by the
probe rather than discovered by it. Use this for any claim of the form *"X is our bottleneck"*,
*"this costs N"*, or *"capability Y is unavailable"* — including when it is your own earlier claim
being re-examined.

**The governing rule: a resource binds only if it degrades work.** Occupancy, utilisation, size,
and count are inputs to that question, never answers to it. Before reporting a bottleneck, produce
the measurement that shows work got worse.

Pair this with `live-system-investigation` (read-only discipline while probing) and
`assertion-window-discipline` (before any negative or global claim).

## 1. A derived number outside its physical range means the parser is wrong

Read counters into **named** keys. Never index a positional argument list.

An off-by-N index silently attached one counter's totals to another's name and produced negative
stall times and negative paging rates, on a probe that looked like a capacity finding. Discard any
derived value outside its range — negative durations, >100% of wall — and re-derive from a parsed
mapping before reporting. The impossible sign is usually the only reason such an error surfaces at
all; treat it as a gift, not a nuisance.

## 2. Character count is not token count

Estimating tokens as `chars / 4` overstated by ~40% on this stack — the measured ratio was ≈5.5
chars/token (68,026 chars → 12,358 prompt tokens). Never publish a token figure derived from a file
size, a byte count, or an impression of a prompt. Read it from the provider's own usage block on a
real call, and re-use the same population when comparing two hosts.

## 3. A large prompt is not automatically expensive — measure the cache, then do not over-claim

Send the **same** system prompt with a **different** user message on each call and read
`prompt_tokens`, `prompt_cache_hit_tokens`, `prompt_cache_miss_tokens`. Varying only the user turn
isolates prefix caching from whole-request caching.

A hit count near `prompt_tokens` means the stable prefix is close to free in latency —
quadrupling the prompt cost ~180 ms against a ~0.9 s floor in one measurement. Two rules follow,
and they bind in opposite directions:

- **Never claim "context is expensive" from size alone.** A cache hit amortises the
  **compute/latency axis only**.
- **Never claim the context question is closed on that evidence.** The **cognitive axis** —
  salience dilution, instruction competition, tool-selection entropy, stale doctrine staying near
  attention — is untouched by caching and remains **unmeasured** until a behavioural A/B is run:
  same objective, full prompt vs minimal core, scored on correctness, missed constraints,
  unnecessary tool calls, and authority mistakes.

Report the two axes separately. A good cache number must not launder a context-tax thesis, and a
context-tax thesis must not survive one cache measurement.

## 4. Swap occupancy is not memory pressure

A box can sit at 95% swap used with zero paging. Pressure is a **rate**, and the evidence is the
full set: sustained `pswpin`/`pswpout`, `pgmajfault`, PSI, and — decisively — whether work slowed.

Sample over timed phases (idle → synthetic workload → recovery):

- `/proc/vmstat`: `pswpin`, `pswpout`, `pgmajfault`
- `/proc/pressure/memory`: `some` vs `full` deltas over wall time
- a **fixed-operation latency control** — the same query re-run in every phase, reported as median
  and p95

If the control latency is flat across phases (0.32 / 0.33 / 0.32 ms observed), the resource is not
binding regardless of how alarming the occupancy looks. `full ≫ 0` is system-wide paralysis;
`some ≫ 0` with `full ≈ 0` is localised contention, not exhaustion. Swap that is *occupied* but not
*moving* is cold history from a past event and says nothing about now.

Corollary: swap used + low OOM activity + only a handful of pages per phase means the swap file is
a leftover of an earlier event. Do not escalate machinery for it; the fix, if any, is working-set
hygiene.

## 5. Read the killer's semantics before provoking pressure

An OOM watcher's own manual decides whether an allocation stress test is even relevant — many
require **both** memory and swap below their minimums before acting, and most carry an avoid/prefer
list. Running a memory-allocation test while free memory sits near the trigger can kill a process
the watcher *prefers*; in this estate the prefer-list contained the live gateway's own interpreter.

Compute the blast radius from the watcher's configuration first. If it cannot be bounded, decline
the test and record the refusal with its reason — that is a finding, not a gap. **A probe that risks
the process running it is not read-only.**

## 6. Cold is not warm

Time a local model's **first call** and its steady state separately. A cold CPU-only 7B answered
6/6 on a bounded task set but took ~62 s on the first item (12 s mean across six), while the same
items on a remote frontier route returned in 0.7–1.1 s.

"Local" is therefore not automatically cheaper in the resource you care about. A benchmark that
warms the model before timing reports a number nobody experiences, and a routing policy written
from warm-only numbers will be wrong exactly when it matters. Report first-call latency always, and
never set a policy from a six-item run — say which conclusion the evidence supports and which it
does not.

## 7. Capability is not route — resolve in this order

Before declaring a capability absent, dead, or missing:

1. Does the process exist?
2. What does its **live** environment hold (`/proc/<pid>/environ` — not the config file)?
3. Which entry wins in the module's own **ordered fallback list** of setting names? First match
   wins; read the list in order rather than assuming.
4. Which endpoint does that resolve to, and does it answer?
5. What contract does the response carry — dimension, shape, units?
6. Does the **target's declared contract** match it?

A working model one hop from a broken route is a **routing fault, not a capability gap**, and the
two have opposite fixes. Most "capability absent" verdicts die at step 3 or step 4.

Two further rules on the repair:

- **Verify the resolver accepts a proposed value before flipping to it.** A silently rejected
  setting is worse than the outage it replaced, because it fails quietly and looks like empty
  results. "The docs list it as supported" is a docs claim, not a runtime claim.
- **An override changes one line; that is the whole rollback.** Prefer the single-line override over
  any migration, and check what a triggering backfill would actually touch before flipping.

## 8. Difference is not drift until ownership says they should be equal

Two stores at different dimensions, two schemas with different field sets, two agents with opposite
conclusions: these are defects only if a **shared contract** declares they must match. Find the
owner, read its declared contract, then judge.

A shadow index with its own declared size is correct by construction. Calling that difference a
mismatch manufactures a class of false positives that costs as much attention as the real faults —
and a false alarm spends the same budget as a true one.

It follows that the narrower verdict is the stronger one: *"this one surface is dead and
root-caused"* survives review; *"this pair has exactly one dead surface"* does not.

## 9. Bind the measurement to its population and its host

- One probe is not a population. A count on one host, one session, or one prompt is a fact about
  that instance — say so in the claim.
- Two hosts' numbers are not "cross-validated" unless the same probe ran against the same
  population. Two different prefixes on two different runtimes agree on **shape**, not on **value**;
  keep them labelled per host rather than merged into one figure, or a merged number with two
  machines' fingerprints on it becomes the next generation's stale fact.
- When the measured value contradicts a figure already circulating, correct the circulating figure
  explicitly and name it as corrected — an unamended number is re-quoted by the next reader.

## Support files

- [`references/measurement-probe-recipes.md`](references/measurement-probe-recipes.md) — runnable
  read-only harnesses: phased PSI/swap probe with a latency control, prefix-cache harness,
  cold/warm benchmark, and the six-step route/embedder resolution trace.
