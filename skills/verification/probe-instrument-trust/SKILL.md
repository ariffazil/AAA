---
name: probe-instrument-trust
description: Use when a probe's OK/DOWN verdict must be trusted.
version: 1.0.0
tags: [probe, verification, monitoring, alerting, evidence]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Probe Instrument Trust

A probe's verdict is a claim about the world. This skill is about writing the ones that
survive being checked by someone who does not trust you.

> **A probe that says OK when the thing is dead is worse than no probe; a probe that says
> DOWN when the thing is fine is worse than both** — because a false alarm is how a working
> reader gets ignored, and an ignored reader is the failure the probe existed to prevent.

Both directions of that sentence are load-bearing. Most probe bugs are one of the two.

## When to use

Writing or reviewing anything whose output someone acts on: an auth/liveness/health check, a
key or token validator, a drift tripwire, a canary, an "is X up" script, a scheduled audit that
exits non-zero. Load before shipping, and re-read after the first time it fires unexpectedly —
that firing is data about the instrument, not only about the subject.

## Rule 1 — Three transport outcomes, only one retryable

```
unreachable          -> retry with backoff (transient)
served, any status   -> an ANSWER. never retry. never downgrade to "unreachable"
served, unparseable  -> still a RESPONSE. keep the status, mark the body as unusable
```

- **A served 4xx/5xx is a reply, not a failure to reach.** Retrying a served error makes a
  deterministic answer look like a flaky subject and buries the real cause under retry noise.
- **Never collapse a parse failure into the transport-error path.** If `json.loads(body)` raises
  inside the same `except` that catches socket errors, the subject reports DOWN the first time it
  returns plain text or an empty body. Return the status anyway — status is still truth.
- **Retry the connect, not the verdict.** With backoff, and a bounded attempt count.
- **Fail closed with a THIRD verdict, not a coerced one.** "Cannot assess" (exit 2 / `CANNOT WITNESS`)
  is distinct from OK and DOWN. Reporting a proxy outage as "DOWN" when the subject's own liveness is
  unknown misdirects the responder to the wrong subsystem.

## Rule 2 — Prove the OPERATION, not a catalogue

Existence, authorisation and capability are three different facts, and the cheap endpoint only
proves the first.

- A credential that answers `200` on a **list or health** endpoint can still be refused (`403`) on
  the object in question. Exercise the exact verb the consumer performs — the fetch, the write, the
  completion — and treat a clean listing as unproven until then.
- Conversely, a `403` on the object is a **scope fact, not an outage**. Report it as such; correcting
  it means fixing scope, never widening the credential.
- When the subject is multi-layer (frontend -> backend -> store), state which layer the probe
  exercised. A `200` from a gateway is not evidence about the store behind it, and vice versa.
- **Classify the caller before counting blast radius.** Read client env var NAMES: a client holding
  a service token plus an app URL is not a client of the thing you are probing. Which class is
  exposed is usually the real finding — the class with no monitoring, not the individual that failed.

## Rule 3 — Identify secrets by hash, never by value

Evidence must be quotable in a report, so make the identity safe to quote.

- Compare `sha256(value)[:16]`. It answers "is this still the key I think it is?" without printing
  anything usable.
- **Scrub a service's own partially-masked form before reprinting an error body.** Gateways emit
  `sk-aaa...ZZZZ`; a scrubber matching only whole keys will let that through. Match both shapes.
- Print lengths and hashes; never a value, even a truncated one, in a transcript or receipt.

## Rule 4 — Position the probe against the record, not instead of it

Persisted failures are not monitoring. A store that wrote hundreds of `status=failure` rows while
no component owned the rate is the canonical shape: the record was **produced**, never **observed**.

```
PRODUCED != SENT != DELIVERED != OBSERVED != ACKNOWLEDGED
```

- A check is only monitoring once its non-OK exit reaches something that acts. Pair every probe
  with a threshold that alerts **before** a human notices degraded output.
- **Set the threshold from observed base rates**, not from taste: a limit is only meaningful next
  to its justification ("would have fired at 14:12, not 22:00").
- **Record which instance served each session** where substitution is possible. A silent handover
  becomes a visible fact only if something writes it down; otherwise continuity is an assertion.

## Rule 5 — Test the instrument in both directions before trusting it

```
1. healthy subject      -> expect OK, and a stable exit code
2. dead/bogus subject   -> expect non-OK, naming the reason
3. broken subject       -> expect the THIRD verdict, not a coerced OK or DOWN
4. repeat 1 three times -> expect identical verdict (no flapping)
```

- **Include a deliberately bogus credential/input** among the fixtures. Without it you have not
  shown the check discriminates — only that it can pass.
- **Run the healthy case several times consecutively.** A probe that flaps between OK and DOWN
  across identical runs is indistinguishable from an unstable subject, and the flapping is yours.
- When one of those runs returns something unexpected, treat it as a defect in the instrument
  first. Tracing why it said DOWN while the subject was up found a real conflation bug, and
  reporting that DOWN as an incident would have put a false outage into the record.

## Pitfalls

- **A single failed request is not an outage.** One dropped socket, one slow handshake — retry with
  backoff before the verdict leaves the function.
- **A retired consumer's credential is an orphan, not a victim.** Liveness of the credential and
  liveness of its presenter are different facts; state both, or the blast radius is double-counted.
- **Do not rebuild a probe from memory when one already exists on disk.** Read it, run it, and only
  then extend it — otherwise you ship a second instrument that disagrees with the first.
- **Do not narrate the probe's internals into the human-facing verdict.** The verdict carries state,
  reason, and the next action; the rest belongs in the receipt.

## Related

Deeper siblings, load them when the task is broader than one instrument:
`background-monitor-design` (silence contract, alert anti-storm, writer gating),
`litellm-proxy-triage` (gateway topology and auth-surface forensics),
`secret-safe-inspection` (reading environment and config without emitting secrets),
`state-transition-discipline` (why a boolean is not a state).
