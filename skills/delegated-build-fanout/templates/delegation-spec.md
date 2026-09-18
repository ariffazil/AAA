# Delegation SPEC skeleton

> Copy into `<workdir>/SPEC.md`, fill every section, and point each child at it.
> Binding for every child. Read this before writing anything.

## What the objective means here

<Define the success PROPERTY, not the noun. What would make it true; what would prove it false.>

## HARD FORBIDDEN

<One line per ban, each with its rationale. Always include:>

- Do not restart the live gateway/service — it kills the session that dispatched this work.
- Do not write to <constitutional file paths> — prepare a diff and hold it.
- Never print, echo, log or commit a token, key, or secret. Reference env var NAMES only.
- Do not send anything to a real human except the single designated target below.
- Do not <invariant the objective would otherwise trample> — <why>.

## Designated verification target

<ONE chat id / path / endpoint, and the required prefix on test output.>

## Evidence contract

Every agent appends ONE JSON line to `<workdir>/RECEIPTS.jsonl`:

```json
{"agent":"<name>","wp":"<G1..Gn>","state":"PRODUCED|VERIFIED|HELD|BLOCKED","files":["..."],
 "command_run":"<exact command>","observed":"<verbatim output excerpt>","trace_id":"...",
 "blocked_op":"<if BLOCKED>","next_owner":"<if HELD>"}
```

and writes `<workdir>/<agent>.md` with the detail.

- `PRODUCED` = file written. `VERIFIED` = a command was run whose real output supports the claim.
- **Never write `VERIFIED` from reading your own code.**
- **HELD and BLOCKED are complete, acceptable answers.** Report the true state.

## Work packages

### <G1> — <name>   (priority)

Problem / evidence it is real: <...>
Deliverable: <...>
Read before editing: <exact paths>
Verify by: `<exact command>` — paste the output.
If it cannot be done: state HELD or BLOCKED and why. Do not substitute a lesser artifact silently.

(repeat per package)

## Reporting back

Final message ≤200 words: WP id, true state, the exact command and a verbatim output excerpt for each
VERIFIED claim, absolute paths touched, and anything you could not do. No summary of intentions.
If you did not run it, do not claim it.
