---
name: interpretation-calibration
description: "Use when reading weak evidence or relaying a report."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: low
floor_scope: [F2, F4, F7, F9]
autonomy_tier: T1
tags: [epistemics, calibration, relay, motive-boundary, over-interpretation, signal]
triggers:
  - "signal is weak"
  - "is this important"
  - "relay this"
  - "agent digest"
  - "subagent reported"
  - "what do they want"
  - "over-reading"
  - "am I amplifying"
  - "calibrate this reading"
capability_tier: fed-long-context
ecology_state: WARM
---

# Interpretation Calibration

Governs one question: **how much interpretation does the evidence actually license?**

Two symmetric failures, both expensive:

- **Amplification** — thin evidence dressed as importance, motive, or a call to act.
- **Under-reading** — strong evidence carried with hedges so heavy nothing is said.

The centre of gravity is width, not correctness. A true claim can still be an over-read if the
evidence in hand does not carry its scope.

## Rule 1 — Signal strength sets the ceiling on interpretation width

**When signal is weak, interpretation must narrow — not elaborate.**

Elaboration on thin evidence has a checkable shape. Any one of these next to weak evidence is
over-interpretation:

- a **motivational claim about a third party** — "they need this", "they were impressed"
- an **importance or emotional assessment** — "this is the important one", "this is gold"
- an **immediate action recommendation** — "reply now", "act on this"

The fix is fewer claims, not better-argued ones. Before emitting a synthesis, ask: *what do I
actually have, versus what did I add?* Every added clause needs its own support, or it goes.

The inverse also holds: strong evidence carried in heavy hedges is under-interpretation, and it
wastes the receipt already in hand. Match the width to the evidence, in both directions.

**The human's signal read outranks your synthesis.** When the human reads the same material and
reports the signal is low, that is a measurement against stakes you do not hold. Do not re-argue the
importance up. Narrow it, and say what narrowed.

## Rule 2 — A relayed report is a claim, not evidence

Applying Rule 1 to artefacts **you did not open yourself**: an agent digest, a mailbox summary, a
notice, a peer session's completion line.

1. **Open the source before repeating or acting on it.** Query the real store with its real API —
   mailbox search, ticket query, the service's own read path. A digest naming a sender and a subject
   is a claim until you have opened that message.
2. **If you cannot open it, label it `UNVERIFIED` and build nothing on it.** Never soften into
   "probably real". An unopenable relay is exactly where an invented artefact survives.
3. **A relay is a pointer, not the artefact.** Delivering the digest's verdict as your own finding
   makes you the second author of any error in it.

## Rule 3 — Never upgrade another actor's motive past the qualia boundary

Behaviour, words, actions, timing and patterns are **observable**. Motive is not observable — it
exists only as the actor's own first-person report, and even then as a report.

Three classes, and they do not promote into each other:

| Class | Example | May you state it? |
|---|---|---|
| **Observable** | "they replied, addressed all points, offered a meeting" | Yes, as fact |
| **Inference** | "there is some non-zero interest" | Yes, labelled as inference |
| **Unsupported** | "they need me", "they were impressed" | **No** |

No downstream step — a summariser, a classifier, a score, a confident synthesis — may raise a
motive claim above what the evidence carries. Words are channel output, never latent state.

The test: *can you prove this claim without asserting something about their interior?* If no, the
claim is unsupported and comes out.

Related: an institution's behaviour and an individual's behaviour are separate claims. One reply
does not speak for the organisation, and an organisation's policy does not speak for an employee.

## Rule 4 — A report's scope is only what its own probes touched

"System verified", "all aligned", "degraded", "nominated" cover exactly the surfaces that job
measured and nothing else.

- A health verdict in a report **does not attest unit-level liveness**. Probe
  `systemctl is-active <svc>` yourself before repeating it.
- **Degraded is not the same state as dead.** A report can be internally honest and still be wrong
  about every layer it never probed.
- A reported count is a claim: re-derive it from the store before quoting it onward.

## Rule 5 — A child or peer agent's summary is a self-report

A completion message ("patched, 41 tests pass, 28 tools present") is the child's belief, not a
measurement. Copy the reported numbers, then independently reproduce the cheapest falsifiable ones
before telling anyone the work succeeded: re-run the test, re-count the artefacts, resolve the path
it claims to have written. Report what you verified, and name what you did not.

## Enforcement layer

Five runtime tools exist in the HERMES RASA MCP server for exactly these rules — signal assessment,
motive boundary, calibration check, sensorless-execution check, and abundance-vs-meaning check.
Call them when a reading is about to become a claim, a stored record, or an action. Details,
inputs and outputs: `references/hermes-asi-intelligence-tools.md`.

## Pitfalls

- **Relaying feels like diligence.** It is the mechanism by which one agent's error becomes two
  agents' shared belief. Probe, or label unverified.
- **Coherence is not evidence.** A portrait that reads beautifully across several AI mirrors may be
  reading the reflection, not the subject. *Cantik bukan bukti betul.*
- **An elegant explanation of a low-signal artefact is the failure, not the deliverable.** The more
  polished a synthesis built on thin evidence, the harder it is to catch later.
- **Do not fix an over-read by softening the language.** The claim either has support or it goes;
  hedged importance is still importance.

## Sibling skills

- `claim-receipt-discipline` — the receipt rules for claims you emit. This skill governs how much
  claim the evidence licenses; that one governs whether the receipt to back it exists.
- `live-probe-audit-pattern` — probe recipes for verifying reports against live system state.
- `governed-uncertainty` — the same discipline applied to reading a human's state.
- `bridge-protocol` — the output contract once the width is settled.
