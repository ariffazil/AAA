---
name: doctrine-ratification-audit
description: "Use when ratified doctrine may not be live or complete."
---

# Doctrine Ratification Audit

> A ratification proves the text was agreed. It proves nothing about what acts on it,
> and nothing about what the compression removed to produce it.

## When this applies

A doctrine document arrives — pasted, cited, or already sitting in the instruction tree —
carrying a ratification phrase, a commit hash and a receipt, and the question is whether it
helps. Also whenever a long source has just been compressed into canon and someone wants to
know it survived intact.

Two independent questions. Ask them separately, always:

1. **Document integrity** — what did the ratification drop?
2. **Enforcement reach** — what acts on it?

A green answer to one is routinely reported as a green answer to both. The whole audit is the
discipline of not letting that happen.

---

## Part 1 — Compression loss

Ratifying a long source into canon is a lossy operation performed by someone who already believes
the content. Nothing in the ratification ceremony checks whether a rule survived the cut.

Grep the ratified file for **each heading of the source**, then grade how each concept survived:

| Survival shape | Verdict |
|---|---|
| its own heading, stated as a rule | kept |
| one row in a table | usually a fair compression — check **both** cells carry the rule |
| a bare noun inside an enumeration | **dropped** — and the surrounding list makes it read as retained |

Grade the third shape as absent, never as covered. A concept listed as an operator in a formula
is not the same as a rule governing that operator.

**The tell for a load-bearing loss:** the rule exists elsewhere in the canon and nowhere in the
file under review. It therefore holds only for readers who happen to load the other file — which
is not the same as holding. Name the specific losses that matter for whoever will actually read
this file, and say which of the source's sections were fair compressions. The deliverable is a
verdict on the compression, not on the doctrine.

---

## Part 2 — Enforcement reach

Doctrine is one layer. Enforcement is a separate claim, and it is the one that gets over-reported.

Report the rung, never a single verdict:

```
doctrine ratified -> machine contract written -> code exists ->
bench self-test green -> wired into a live caller -> output artifact observed
```

Partial credit collapses these rungs. "It is deployed" is not a state.

Three probes, cheapest first:

1. **Does the control's output artifact exist?** Anything that emits telemetry, holds or receipts
   writes a file. An absent file means it has never fired — one `ls`, and it outranks every document
   written about the control, including a receipt reading `DEPLOYED_AND_VERIFIED`. Measured shape:
   a sensor self-tested 61/61 green on the bench, shipped with a deployment receipt, and its
   telemetry file did not exist — nothing in the live dispatch path imported it. Zero events, zero
   blocks, green report.
2. **Grep the live tree for the import, not the test tree.** Hits landing only inside the module
   itself, its tests, and the docs mean zero call sites. A bench self-test exercises the logic; it
   never exercises the wiring.
3. **Read the artifact's own state line.** A header or config field carrying `STAGED` / `NOT_WIRED`
   / `ADVISORY` was written by whoever built it and describes the wire; a receipt describes an
   intention. When they disagree, the artifact is the one that runs.

---

## Choosing whether to enable a compiled control

Doctrine passing a machine contract does not say where the compiled control belongs in the path.
Benchmark an obvious case set **and** a realistic messy set — misspellings, a claim promoted across
two sentences, bare key-value with an ambiguous value, positive-valence assertions — and count
**both** error directions. Measured: 26/26 obvious against 19/29 realistic, the realistic set
carrying near-equal false HOLDs and misses. Place it by the false-positive count, not the accuracy:

- **Advisory / telemetry** — safe at any accuracy; nothing is blocked.
- **Block on the validated subset only** — HOLD wiring for the class that scored clean; rest emitting.
- **Full blocking** — only once realistic false-positives are zero.

A false HOLD on valid text costs more than a miss: a miss degrades one reading, a false HOLD refuses
a legitimate sentence and trains the operator to route around the control. When the harness prints
its declared blind spots after the pass rate, carry them into the verdict — a rate quoted without
the gaps it declared is a claim, not a measurement.

---

## Pitfalls

- **Do not re-litigate scope the document already polices.** A mature doctrine usually carries its
  own boundary — a disambiguation against a similarly-named artifact, or an explicit refusal to grow
  into a competing state set. Say that the guard is working; do not re-argue it or propose the
  expansion it already refused.
- **Two files can share one name while being different objects.** A doctrine of invariants that
  applies to every person and a data file recording one named person's history are complementary,
  not redundant. Establish which object each file is *about* before judging either, and report a
  name collision as a naming defect rather than a content defect.
- **A compression loss is not a defect in the doctrine.** Report it as a gap in the ratified file.
  Confusing the two makes the source look wrong when only its condensation was lossy.
- **Do not propose a parallel layer to fix a reach problem.** Missing enforcement is a wire, not a
  new registry, contract or doctrine file. Name the missing wire and the rung it belongs to — a
  second artifact restating the first is a duplicate, not coverage.
- **`no tests ran` is not a pass.** A `test_*.py` that is really a `main()` script collects zero
  tests and exits 0 — a clean-looking sweep line for a file never executed by it. Grep for `def test_`
  before trusting a collect count.

---

## Reporting shape

Three buckets, in this order — never one verdict on the whole artifact:

1. **What is already held**, with the file that holds it.
2. **What the ratification dropped** that matters, and what was fairly compressed.
3. **What the enforcement rung actually is**, as the ladder position plus the missing wire.

Close on the rung and the single decision that needs the sovereign's word — sealing or re-writing a
ratified document is his act, not the auditor's. Everything below that line is the auditor's work.
