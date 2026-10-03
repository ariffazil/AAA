# Control vs document — the one question that sorts a skill library

Before a skill tells a future agent that something is *enforced*, ask: **can this thing withhold anything?**

A named instrument carries three possible statuses, and skills routinely blur them:

1. **A control** — it runs, it is called, it can refuse, and a refusal has been recorded.
2. **A check** — it runs and reports, but cannot refuse. A useful sensor; not a guard.
3. **A document** — it describes the control. It may be accurate, well-written, and entirely inert.

Blurring 3 into 1 is the defect this reference exists to stop: a skill that says "run X to enforce Y" when X is inert has moved the false confidence one layer deeper, where the next reader cannot see it.

## When writing or editing a skill that cites an instrument

- Name the status explicitly: *control*, *sensor*, or *planned*. A reader who knows which one they are holding can act.
- If the instrument lives outside the skill, cite its path and say what it can do — do not restate its logic, which then drifts from the source.
- If the instrument does not exist yet, say **NOT IMPLEMENTED** rather than describing intended behaviour in the present tense. Present tense is a claim, not a status.
- When a skill is the only remaining copy of a retired instrument's logic, move that logic into `references/absorbed-<name>.md` **before** the source leaves the tree, and verify the payload digest against the source.

## When a control and its documentation disagree

Trust the running artifact, and check its scope in code rather than in its description:

- Read the audience/mode switch. If two declared modes behave identically for the gate you care about, the scoping is nominal.
- Read the exemption logic. An exemption applied to every rule but one leaves that one rule measuring the wrong thing.
- Read the caller's invocation line and confirm which flags it actually passes. The tool's default mode is the operative one, whatever the docs say.

Record the disagreement as a finding with both sides quoted, and leave the artifact alone unless the edit is inside your own envelope.
