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
capability_tier: fed-agent-subagent
ecology_state: WARM
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
- **Measure on the axis the DECISION turns on, not the axis the probe finds easy.** A resemblance,
  similarity, or "looks/sounds like the reference" score is a proxy for the property you care about,
  and it cannot fail on the axis that decides the outcome. Measured: two candidate engines fed the
  same reference sample and the same line were indistinguishable on timbre, and a listener confirmed
  "the output is the same" — while one returned the text verbatim and the other garbled several words
  per sentence. The verdict became measurable only after switching the scoring axis from resemblance to
  **words**. Before quoting a proxy, ask *what would this number say if the artefact were wrong in the
  way that matters?* If the answer is "nothing", you are measuring the wrong axis — name the proxy as a
  proxy, or re-score on the deciding axis.
 - **Verify the SERVED identity of every row before comparing rows — N labels are not N samples.** When
 probes reach a model or service through a routing layer of aliases, each name can resolve through its
 own deployment order and then its fallback rungs, so several names can land on **one** backend while
 the rest are dead. Measured: three distinct aliases returned **byte-identical** output (and one
 returned an empty body) — which reads as "three models agree" and is actually a single model answering
 three times. Never present aliased rows as independent opinions, a diversity check, or cross-validation.
 Send a unique nonce per row, record the identity the response reports for itself, and dedupe on it
 before drawing any conclusion; to characterise a provider, probe its endpoint directly rather than
 through the routing layer.

## 10. Name the substrate the number belongs to

A reclamation or capacity claim is meaningless without its substrate attached. `du` answers for
**disk**; a `/tmp` may be **tmpfs (RAM)**; a journal vacuum frees disk; deleting a compile cache
frees neither for long. Purging ~3 GB from a tmpfs `/tmp` moves disk by zero.

Before writing "freed N GB":

1. `findmnt -no SOURCE,FSTYPE <path>` — is that path a real filesystem at all?
2. Read the counter for the resource you are actually claiming: `df -B1 /`, `free -m`,
   `swapon --show`, `/proc/pressure/*`.
3. Put the substrate in the sentence: *"2.8 GB freed on tmpfs — RAM and swap, not disk."*

Generalised: **a purge is not "space freed" until you name which space.** Same discipline as §4 —
the number is not the finding; the resource it binds is. When the two disagree (a multi-GB
"reclaim" that leaves `df` unchanged), believe the counter you claimed and correct the sentence in
place rather than shipping the flattering version.

**Quarantine-by-move frees nothing on the same filesystem.** `mv` into a `.archive/` sibling
changes a path, not a byte count — it is a *reversibility* move, not a space move. Say which one
you are doing. When the only remaining candidates are archives and free space is not scarce, that
is the owner's decision, not one to take under an "entropy reduction" heading.

## 11. A number nobody acts on is ceremony — and a gate that measures its own noise is worse

Before keeping a check, name the decision its output changes. If no decision moves when the number
moves, the check is decoration: it costs a run, a parse and an explanation per instance, and it turns
a judgement into a ritual. Cut it, and keep the checks that each caught a real failure.

Two diagnostic forms:

- **The score nobody reads.** A similarity / health / quality ratio whose pass threshold no one can
  state, and whose failures get adjudicated by reading the artefact anyway. The **artefact is the
  witness**; the score is a lead at best.
- **The instrument measuring itself.** A gate whose noise is neutralised by building a growing mapping
  table — substitutions, respellings, unit fixups — before its number means anything. That table is
  effort spent on the *probe*, not the subject, and the ratio stays blind to the real failure class
  (a fused pair and a one-word semantic flip both score as a perfect match).

**Keep-vs-cut test, applied per check:** does it fail on a real defect you have actually seen? Retain
it if yes — a contamination detector and a speaker-identity check each earned their place that way.
Cut it if its only product is a number.

**Declare the residual when you cut.** Removing a machine-readable verdict hands judgement back to the
reader; that is a real loss in delegation even when no artefact changes. State it in one line rather
than claiming a free simplification.

**Do not apply this to a scan for a silent class.** A check that exists to catch something nobody can
see by inspection (contamination, a wrong voice, a stale read) is not ceremony — it is the only
witness. Ceiling applies to the *reporting*, never to the sensor.

## 12. A test whose outcome is the same either way proves nothing

Before trusting a verification run, ask what it would print if the fix were broken. If the answer is
"the same thing", it is not a test.

Measured: an idempotency guard was patched, then re-run — all seven subjects skipped, zero appends.
That result was **non-discriminating**: every subject was already recorded, so an entirely broken
guard would also have skipped all seven. The real proof came from the next two scheduled cycles, in
which four genuinely new items were written and the duplicate count stayed exactly where it was.

- **Prefer the next real cycle over a hand-run replay.** A scheduled run exercises the production
  path, the production data, and the production cadence; a manual invocation usually exercises a
  state where nothing is left to do.
- **If you must test now, build the discriminating case.** Inject the condition the guard exists for
  (a marker placed outside the guard's window) and assert the guard sees it, then assert the
  opposite case still behaves. One fixture that passes under both hypotheses is decoration.
- **Name which hypothesis the run could have falsified.** If none, say the fix is staged-but-unproven
  and state what observation would prove it.

## 13. Count the population you mean, and say which boundary you stopped at

`git status --porcelain` in one repo root does not include sibling repos, submodules, or nested
checkouts. A fleet-wide "uncommitted files" figure assembled from one root undercounts — measured:
194 reported against 209 actual, with a single sub-repo holding 162 of them and therefore dominating
any conclusion drawn from the total.

- **Enumerate the units first, then sum.** Loop the repo list, print per-repo counts beside the
  total, so a reader can see where the mass sits. A bare total hides both the undercount and the
  concentration.
- **A total with no per-unit breakdown is unverifiable and usually wrong.** When someone quotes one
  number for a heterogeneous population, reproduce it per unit before adopting it.
- **State the boundary in the claim** ("209 across 7 repos; excludes X") rather than letting the
  number travel without its scope.

## Support files

- [`references/measurement-probe-recipes.md`](references/measurement-probe-recipes.md) — runnable
  read-only harnesses: phased PSI/swap probe with a latency control, prefix-cache harness,
  cold/warm benchmark, and the six-step route/embedder resolution trace.
