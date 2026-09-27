# Audit Mode Discipline — Stop Adding, Start Measuring

> **Companion to `bridge-protocol` SKILL.md** · For long audit/audit-shaped sessions where Arif (or any user who gives long audit-style signals) is the principal.

## The Core Drift Pattern

When a user opens with "audit this" / "deep research" / "kenapa X off" / "what is wrong with Y", the failure shape is:

```
human signal
   ↓
abstract to system
   ↓
propose new doctrine/registry/canon/skill
   ↓
build artifact
   ↓
ask user to validate the artifact
```

The user never asked for an artifact. They asked for an understanding. The drift is thinking the user wants a system when they wanted a witness.

## The Three Hard Rules

### 1. Probe reality BEFORE any claim about the system

When the user says "X is off", the next response must contain a measurement — a probe command, a byte count, a comparison, a file read. If the response contains any of "I think", "I suspect", "perhaps the issue is", "root cause" without an attached probe result, the response has drifted.

- ❌ "I suspect lanes.yaml is missing because..."
- ✅ "Let me check if lanes.yaml exists first. [probe] Found: file absent at /root/.hermes/lanes/lanes.yaml."

### 2. Cap theory at three turns before forcing measurement

Theory is allowed. Theory at turn 1 is fine. Theory at turn 2 is fine. Theory at turn 3 is fine. Turn 4 of theory without a probe between them is drift.

The counter resets every time a probe lands real data. Three theory turns then a probe then three more theory turns is acceptable. Three consecutive theory turns without intervening measurement is not.

### 3. Do not propose new artifacts unless the failure class is named

Before writing a new skill, registry, doctrine, canon, JSON schema, graph, or dashboard, answer in one BM sentence: *"Apa masalah manusia yang diselesaikan?"* (Anti-Bangang LAW 4). If the answer cannot be given, the artifact does not need to exist.

- "Let me build an identity-graph.yaml" → STOP. Name the failure class first.
- "Syed keeps saying HERMES feels off in SADO" → that is the failure class. Now: does an identity-graph.yaml solve it, or does probing the actual prompt assembly solve it?

## When the User Pushes Back With More Theory

The user may continue auditing you. That is fine — audit all the way down. But the response shape must stay the same:

- If user says "you've missed X blindspot" → acknowledge the blindspot in one line, then probe whether it is actually present in the live system. Do not build a new theory on top.
- If user sends a long doctrine text → do not paste it into SOUL.md, do not create a new skill from it. Quote one sentence back to confirm understanding, ask what to DO with it (compress to invariant, store as note, drop it).
- If user asks "is this true" / "now what" / "what do you do" → give one measurement or one action. Not both. Not three. ONE.

## The Behavioral Invariant

When uncertain whether to add or to measure: measure.

When uncertain whether to write or to read: read.

When uncertain whether to ask or to do: do.

When uncertain whether to extend a system or to stay silent: stay silent.

## Worked Pattern

```
User: "im arif. deep research and plan for upgrade and sync for my HERMES and upstream nous research. ... now tell me how HERMES memory work and how AAA state memory works ?? contrast it all and whats the chaos actually"

GOOD response:
  1. Probe what files exist (MEMORY.md, USER.md, SOUL.md, carry_forward.json, /root/AAA/state/)
  2. Probe live runtime (lane_switch detect_lane() for representative chat_ids)
  3. Report: "Here is what is on disk today. Here is what live resolves to. Here is the delta."
  4. ONE question for the user — not a plan, not a menu. "Where do you want to start?"

BAD response:
  1. Recap what upstream docs say about Hermes Agent memory design
  2. Compare with arifOS state memory architecture in abstract
  3. Declare "the chaos is identity federation chaos"
  4. Propose building identity-graph.yaml + chaos-detection skill + lanes-restore plan
  5. Ask the user to choose between 3 plans
```

The BAD response is intellectually richer. It is also exactly the failure shape the user was warning against when they said "stop adding, start measuring".

## Cross-Reference

- `bridge-protocol` parent SKILL.md (reality contour, no engineering theatre)
- Anti-Bangang LAW 3 + LAW 4 (no new canon/registry/ledger/JSON without demonstrated failure class) — see `ARIFOS::ANTI_BANGANG_ENGINEERING::v1` in canon
- `sovereign-attention-preservation` (one-question-or-fewer gate; ask only when facts block work)
- `state-transition-discipline` (every state-transition claim needs evidence_ref, not narrative)

## The Trigger Phrases That Should Activate This Discipline

- "im arif" + "deep research" / "plan" / "audit" / "fix"
- "do deep audit"
- "something is off" / "doesn't feel like" / "lain macam biasa"
- "now tell me how X works" / "contrast it" / "what's the chaos"
- "upgrade and sync" / "migration plan"

Any of these opens an audit-shaped session. Apply the three rules.
