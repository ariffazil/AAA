# Dispatch Protocol

One-line summary:
The dispatch protocol defines which agent owns which stage of the explorer loop, and how control passes between Hermes, OpenCode, OpenClaw, A-FORGE, AAA, and arifOS.

## 1. Purpose

S14, S15, and S16 give the organs the ability to run `OBSERVE -> HYPOTHESIZE -> FALSIFY -> VERIFY`.

This file closes the remaining gap:

- who dispatches the loop
- who owns each stage
- what packet moves between stages
- when a stage returns local control
- when escalation to AAA or arifOS is mandatory

## 2. Agent Roles

### Hermes

Primary role:

- entry router
- query normalizer
- observation dispatcher
- contradiction escalator

Hermes owns:

- initial `OBSERVE` dispatch
- first domain choice
- packet assembly start
- user-facing coordination

### OpenCode

Primary role:

- cognitive generator
- hypothesis branch expander
- design-space explorer

OpenCode owns:

- `HYPOTHESIZE`
- multi-branch candidate generation
- explicit falsifier declaration

### OpenClaw

Primary role:

- physical executor
- test runner
- runtime falsification operator

OpenClaw owns:

- executable `FALSIFY`
- bounded `VERIFY` actions when they require real runtime work
- concrete environment interaction

### A-FORGE

Primary role:

- governed execution substrate
- tool fitness and mutation layer

A-FORGE owns:

- heavy execution substrate
- mutation/build/test/deploy actions
- execution receipts

### AAA

Primary role:

- identity/state coordinator
- lease and capability authority context

AAA owns:

- dispatch legality at the civilization/state layer
- inter-agent continuity
- capability and lease continuity

### arifOS

Primary role:

- constitutional judge

arifOS owns:

- verdict boundary
- irreversible gate
- floor conflict resolution

## 3. Canonical Stage Ownership

Default stage mapping:

1. `OBSERVE` -> Hermes dispatches to owning organ
2. `HYPOTHESIZE` -> OpenCode expands candidate set
3. `FALSIFY` -> OpenClaw executes bounded attacks, using A-FORGE where substrate is needed
4. `VERIFY` -> OpenClaw and/or domain organ verifies, then arifOS judges if authority boundary is crossed

This means:

- Hermes is not the hypothesis factory
- OpenCode is not the runtime executor
- OpenClaw is not the constitutional judge
- A-FORGE is not the router

## 4. Dispatch Sequence

Canonical flow:

```text
User / sovereign signal
  -> Hermes
  -> owning organ OBSERVE
  -> OpenCode HYPOTHESIZE
  -> OpenClaw FALSIFY
  -> OpenClaw or owning organ VERIFY
  -> AAA if identity/lease/state ambiguity appears
  -> arifOS if judgment/authority/irreversibility appears
  -> A-FORGE if execution or tool mutation is required
```

## 5. Trigger Table

### Hermes -> owning organ

Trigger:

- query enters system
- contradiction source domain is clear
- fresh observation is needed

Payload:

- `explorer_packet` with query, initial route guess, empty hypotheses/tests

### Hermes -> OpenCode

Trigger:

- sufficient observations collected
- domain context stable enough for branching

Payload:

- packet with `observations`
- owning domain
- hypothesis count target

### OpenCode -> OpenClaw

Trigger:

- at least one ranked hypothesis exists
- falsifiers are declared

Payload:

- packet with `hypotheses`
- required tests
- runtime prerequisites

### OpenClaw -> A-FORGE

Trigger:

- falsification or verification needs build/test/deploy substrate
- tool mutation is part of the loop

Payload:

- packet plus execution request
- risk tier
- required receipts

### Any stage -> AAA

Trigger:

- identity ambiguity
- lease uncertainty
- cross-agent handoff continuity issue
- capability mismatch

### Any stage -> arifOS

Trigger:

- authority question
- floor conflict
- irreversible action
- verdict ambiguity

## 6. Return Paths

Legal returns:

- OpenCode -> Hermes when hypotheses are too weak and more observation is needed
- OpenClaw -> OpenCode when all main hypotheses are killed
- OpenClaw -> Hermes when a new domain route is needed
- AAA -> Hermes when state continuity is restored
- arifOS -> Hermes/OpenClaw/A-FORGE with `SEAL`, `SABAR`, `HOLD`, or `VOID`

## 7. Dispatch Rules

1. Hermes may dispatch, but must not silently self-complete all stages.
2. OpenCode must emit falsifiers, not just ideas.
3. OpenClaw must test the strongest candidates first.
4. A-FORGE executes substrate work, but does not decide truth.
5. AAA decides continuity and capability context, not domain truth.
6. arifOS decides judgment, not engineering method.

## 8. Minimal Handoff Example

```yaml
from_agent: hermes
to_agent: opencode
stage: hypothesize
packet_ref: xp-20260706-001
reason: "Observations sufficient. Need three ranked domain-law-grounded hypotheses."
required_output:
  - hypotheses
  - falsifiers
  - owning_domain
```

## 9. Law

If the system cannot answer:

- who dispatched
- why this agent owns this stage
- what packet crossed the boundary
- what condition triggers the next handoff

then the choreography is still implicit, not governed.
