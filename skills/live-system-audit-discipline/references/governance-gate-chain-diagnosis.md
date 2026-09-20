# Governance gate-chain diagnosis

## The rule

When an authority system refuses an action, **"it was blocked" is not a finding.** A refusal
is usually one gate in an ordered chain, and reporting the refusal without naming the gate
tells the next reader nothing actionable — it reads as a system fault when the real answer may
be "your call omitted a required field" or "the default parameter can never pass."

Procedure:

1. **Enumerate the gates** in the order the system evaluates them.
2. **Satisfy them one at a time.** Each fix reveals the next gate — expect several rounds. A
   single attempt tells you almost nothing about the shape of the chain.
3. **Record the MEASURED margin at each gate**, not pass/fail. "0.802 against a 0.85 floor" is
   a finding; "it HOLDed" is not.
4. **Classify every blocker**: caller error / system defect / intentional constraint.
5. **Report the gate you reached**, its margin, and the parameters that got you past the
   earlier ones — so the next attempt starts further along.

## Distinguishing a defect from a design choice

A gate that refuses you is not automatically wrong. Three classes, and the fix differs:

- **Caller error** — you omitted a required field. Fix the call.
- **Parameter-default defect** — the default can never satisfy the gate. The tell is that the
   gate's own reasoning text contradicts its own threshold (e.g. a budget whose description
   says "single LLM pass" while allowing 200 ms, which no such pass can meet). Every caller
   using the default is refused. Fix the default or route around it.
- **Intentional constraint** — the gate encodes a rule about *who* may do this. The tell is
   that satisfying it would require a party who is not present in the loop at all (a human
   witness, a second independent signature). **Ratify it, do not patch it.** Say plainly that
   the agent alone cannot satisfy it and hand the decision to the owner.

Conflating the second and third wastes the most time: one is a bug, the other is the
constitution working.

## Worked example — a seal chain that reveals one gate at a time

Measured on the arifOS kernel judge path. Each row became visible only after the row above it
was satisfied; the first attempt returned only `EVIDENCE_EMPTY`.

| Gate | Refusal | Resolution |
|---|---|---|
| no prior observation | `EVIDENCE_EMPTY` — "judge received no evidence" | run the observe verb in the same session first (fail-closed, correct) |
| latency budget | `LATENCY_TIMEOUT ... degraded to SABAR (deliberation did not complete)` | default tier maps to the 200 ms budget; pass the elevated tier → 1000 ms, deliberation completes in ~300 ms |
| candidate shape | `parse_warning: "candidate JSON unparseable — verification state not extracted"` then L02 fails at 0.99 | send `candidate` as JSON (`claim` + `verification_state` + evidence) → L02 passes at the 0.95 threshold |
| consensus floor | `L03 W4 Consensus: 0.802 >= 0.85 (H:0.70, A:0.99, E:0.60, V:1.00)` | weakest planes are human witness and evidence — reads as an intentional "a witness must be in the loop" constraint |
| class gate | reports `declared: OBSERVATION`, `class: OBSERVATION`, `agree: true`, *then* refuses with `class=UNCLASSIFIED is not action-eligible` | report the self-contradiction; do not re-word the claim to satisfy it |

**The honest conclusion the chain produced:** it was not "broken." It was *correctly refusing a
self-graded claim.* Naming the gates turned an apparent system failure into a specific list,
and separated two real defects (a default parameter that can never pass; a gate contradicting
its own output) from one intended constraint.

## Pitfalls

- **Do not retry the identical call hoping for a different result.** Each refusal is a distinct
  gate, not noise. Change exactly one thing per attempt so you learn which change mattered.
- **Do not fabricate the field a gate asks for.** If it wants a state hash, a signature, or a
  witness, inventing a plausible value converts a clean HOLD into a floor breach and destroys
  the audit trail you were trying to create.
- **Do not patch away a constraint you cannot satisfy.** Record it, classify it, hand the
  decision to the owner.
- **A gate that contradicts its own output is itself the finding.** Quote both halves; do not
  paper over it by adjusting your input until it stops complaining.
- **Report the parameters that worked.** The next session should not repeat your four attempts.
