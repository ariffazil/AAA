---
name: agent-exploration-discipline
description: "Use when a search or verify loop is circling."
version: 1.0.0
license: MIT
---

# Agent Exploration Discipline

Load when a search, probe or verification loop keeps returning the same class of result, or
before declaring a capability blind or a tool broken.

## The rule

An exploration failure is usually a prior that hardened into a filter, not a missing fact.
The prior ("it is in the car") stops being a hypothesis and becomes the search filter itself,
so the search runs *inside the prior* instead of inside the world.

> Registry says where it should be. Witness says where it is.
> Intelligence discovers the difference. Governance changes behaviour because of it.

## Diagnostic — run before every repeated check

**Has any new evidence entered since the last iteration?**

If no: stop iterating. The loop is self-confirming. Restating the same hypothesis with rising
confidence is not corroboration — repetition mistaken for evidence is the actual failure mode.
Switch primitive instead of spending another cycle.

## Five blindness mechanisms

| Mechanism | Human form | Agent form |
|---|---|---|
| Prior filter | Searching only where memory says it was placed | Only testing the hypothesis already in context |
| Stress narrowing | Adrenaline narrows the visual field; working memory drops | Context / objective saturation narrows the explored space |
| Route repetition | Eye saccades retrace one path; the brain marks it "checked" | Re-running the identical probe, then treating it as verified |
| Habituation | Constantly present objects stop being perceived | Ignoring the component that appears in every output |
| Inattentional blindness | Counting passes, the gorilla is never seen | Answering the literal objective and missing the real constraint |

The operational asymmetry: a fresh observer finds the object because it inherits no search
trace. It is not smarter — it is unfiltered. **The absence of a prior is the capability.**

## Five counter-primitives

1. **Blindness detector** — periodically ask: *what am I assuming that I have not witnessed?*
2. **Opposite search** — every N steps: *if the primary hypothesis is wrong, what is the most plausible alternative?*
3. **Fresh-perspective observer** — spawn a verifier with no access to the prior reasoning or search trace.
4. **Angle shift** — re-examine at data level, capability level, governance level, consequence level.
5. **Search pause** — enforce `SEARCH → PAUSE → RE-OBSERVE → SEARCH`. Never `SEARCH × N`.

The pause is the active ingredient. Releasing the search prior is why the answer frequently
arrives after stopping — mechanism, not luck.

## Capability vs lane

**A failed lane is not a failed capability.** Before declaring anything blind or unavailable:

1. Sweep the inventory of what actually exists.
2. Test an alternate lane.
3. A spawned child may carry a different lane set than the caller — the same request routed
   through a delegate can succeed where it failed in-line. Prefer that over retrying the lane.
4. Report the lanes tried. Never emit a bare "tool broken" — that claim outlives the fault and
   gets cited against you later.

Declare "cannot witness" only after the sweep.

## Instrument vs hand-roll

**A hand-rolled probe is not a missing instrument.** The same inventory discipline applies to the
measuring tool itself: before writing your own counter, meter, classifier or diff, sweep for the
canonical sensor.

```bash
ls /root/scripts/              # census, entropy gate, notation probe, consolidators, sensors
ls /root/scripts/tests/        # fixture + regression case files
ls /root/tests/                # fixtures a doctrine's own re-run schedule names
```

Measured in one session: a skill count, a notation-namespace sweep and a doctrine-drift inference
were each hand-rolled while an instrument that already existed — and that nobody had run — said
something materially different. In every case the instrument was right and the hand-rolled method
was the defect; the hand-rolled count was also **inflated**, so it manufactured work that did not
exist.

Two consequences worth holding:

- **A hand-rolled method has no shared definition.** The canonical instrument encodes what the
  quantity *means* — which roots count, which walk flags, which exclusion classes. Re-deriving the
  number silently re-derives the definition, and the two figures then cannot be reconciled at all.
- **When your number and the instrument disagree, do not average and do not pick one.** Re-run the
  instrument, read its machine-readable output, and treat your own method as the thing under
  suspicion until it explains the difference.

## Budgets worth holding

- **Contradiction budget** — time spent actively trying to falsify the current belief
- **Novelty budget** — time spent looking somewhere not yet looked
- **Random-exploration budget** — spent even while the main hypothesis still looks correct

Without an explicit budget, all of it gets spent on H1 regardless of how wrong H1 is. A prior
with no competing budget is a prior that cannot be abandoned.

## When to stop verifying

**Stop when additional verification cannot change the decision.**

Before spending another cycle, name the decision it would change. If there is none, the cycle
buys comfort for the loop, not safety for the work. Signals you are already past the point:

- Every new check returns the same class of result as the last
- You are re-running a probe against an unchanged input
- You are verifying your own verification

### Mutable targets

When the thing under verification can change underneath the check (a live ledger, a running
service, a shared file), either **pin a snapshot** — record source hash and position at OPEN,
re-check at CLOSE, demand a frozen-snapshot re-run if anything appended concurrently — or
**declare the target in motion** and say which part of the reading is point-in-time. Never call
a moving target immutable. Refusing to do so *is* the value of the audit.

## Pitfalls

- **Reporting a failure as neutral.** "No data" is not "no problem". Absence of signal is a
  finding about observability, not about reality. Never let a silent fallback stand in for a result.
- **Averaging disagreeing readings.** Independent readings usually establish *different* things.
  Combine them and label which reading supports what; erasing the disagreement destroys the
  reason you collected more than one.
- **A report that reads as complete.** Every analysis must name one condition under which it
  would fail. A report with no failure condition has stopped being a report.
- **Repeating a lane after in-line failure.** That is route repetition. Change lane, change
  observer, or pause.
- **Hand-rolling an instrument that ships.** A bespoke counter beside a canonical sensor guarantees
  the two will disagree, with nothing to reconcile them. Locate the sensor first; if none exists, say
  so explicitly when you publish the number — a figure with no named method is not evidence, and one
  that *under*-counts reads as less work than there is.
