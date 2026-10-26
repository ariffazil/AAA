---
name: cross-harness-reality-test
description: "Reality-prompt tests of external apps' arifOS wiring."
triggers:
  - "test the arifOS MCP stack in <app>"
  - "give me a prompt to test <agent app>"
  - "reality prompt for Claude / Codex / Cursor"
  - "audit the run of the test prompt I pasted"
tags: [mcp, arifos, cross-harness, reality-test, prompt-authoring, session, identity]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Cross-Harness Reality Test — authoring the prompt, reading the run

An external agent app (Claude app, Codex, Cursor) is wired to the arifOS MCP stack. Arif wants one
prompt that exercises the whole verb stack, then pastes the app's answer back for audit. Two jobs:
author the prompt so it cannot be satisfied by pattern-matching, and read the run without
over-attributing failure.

## Job 1 — authoring the prompt

A reality prompt is a TEST INSTRUMENT. It must force the tested agent to reach reality, never let it
rest on recalled text.

1. **Never bake recalled facts into the prompt as truth.** Any dated fact (return dates, status of
   schemes, prices) is either omitted or explicitly assigned for verification. A stale fact hard-coded
   into the prompt becomes the test's false premise — the tested agent will either echo it (false pass)
   or flag it (true pass that indicts your memory instead of the stack). The prompt that burned this
   rule once began with a return-to-office date nine months in the past.
2. **Force the chain, in order, with no skips:** RECALL (list stored facts) → VERIFY (check each
   dated fact against today's date; flag stale loudly) → PROBE (live queries only for current state) →
   ROUTE (name the organ per sub-question — do not let keyword routing decide) → JUDGE → FORGE one
   concrete output.
3. **Require source discipline:** every factual claim from a live probe or a recalled memory with its
   source named; a dead tool must be declared dead, never back-filled with a plausible number.
4. **Require the register:** plain Bahasa Melayu, short sentences, no tables, no system jargon, no
   menus (Arif's standing output law).
5. **End with one verdict** (SEAL / PROVISIONAL / HOLD) plus the evidence chain behind it.

## Job 2 — the expected ceiling (so you don't audit a design as a bug)

An external harness without federation credentials hits a hard, deliberate ceiling. Know it before
reading the run:

- **Session threading:** the first call must be `arif_init(mode='init', actor_id='<app>/<model>')` and
  the returned `session_id` (plus token, if issued) must ride every later call. Without it, downstream
  verbs refuse with "bound session required" — that is the kernel enforcing, not a defect.
- **Authority cap:** an actor without a registered Ed25519 keypair gets a limited, observe-only token.
  `arif_judge` tops out at HOLD and `arif_forge` may refuse outright; a PROVISIONAL verdict is the
  design ceiling. The only upgrade path is the identity challenge→sign→init flow — renaming the
  actor_id changes nothing.
- **Recall source:** the app's RECALL leg may read its own memory files, not arifOS memory. Date
  staleness there indicts the app's memory, not the kernel.

## Job 3 — reading the run

Audit claim-by-claim against live probes (`ground-relayed-agent-claims`, `cross-audit-v1`). Beyond the
usual grounding, these signatures recur:

| Symptom in the run | Real meaning | Probe that settles it |
|---|---|---|
| "organ X: DOWN" from an init-time health layer | a summary surface self-reports degraded while the organ's own MCP surface is healthy — two surfaces of one entity disagree | call the organ's own tool directly; then diff the two surfaces before quoting either |
| "bound session required" / OBSERVE_ONLY everywhere | either the tested app skipped init, or YOUR re-probe skipped init — check whose call failed before blaming the audited run | complete your own init lifecycle, then retry |
| Every verdict PROVISIONAL / HOLD | observe-only ceiling, by design | check whether the app holds any registered keypair at all |
| Router sends a domain question to the wrong organ | keyword-classifier weakness; the kernel router matches on surface words | re-run with explicit organ names; if manual assignment fixes it, the finding is router precision |
| Two runs of the same prompt yield different "single highest-leverage moves" | the app is pattern-matching, not grounded — with no data it fills with confidence | diff the two runs' evidence chains; report divergence itself as the finding |
| A quoted `origin/main` SHA | local remote-tracking refs go stale; the claim may be hours behind | `git fetch` first, then re-probe |

## Pitfalls

- **Don't attribute your own probe's protocol error to the audited run.** A session/lifecycle error you
  hit while re-testing is evidence about YOUR call until proven otherwise — the error text names a
  step you may have skipped, not a defect in their run.
- **Don't "fix" the ceiling by tweaking names.** Authority escalation in arifOS is cryptographic, not
  nominal; an actor_id rename cannot lift observe-only.
- **Don't grade a well-flagged stale memory as a failure.** A run that loudly marks recalled facts
  LAPUK before using them is passing the test — the test punishes silent trust, not staleness itself.
- **Don't accept one run as the stack's verdict.** One run is one sample; the divergence between two
  identical-prompt runs is often the most valuable measurement the test produces.

## Adjacent

- `ground-relayed-agent-claims` — the claim-by-claim grounding flow for the pasted run
- `claimed-defect-verification` — before calling anything in the run a defect
- `federation-wiring-audit` — when the harness under test is Hermes itself
