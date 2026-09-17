---
name: delegated-build-fanout
description: "Use when fanning one objective out to parallel subagents."
version: 1.0.0
tags: [delegation, subagent, verification, evidence, fan-out]
triggers:
  - "spawn agents to build"
  - "fan this out"
  - "get the fleet on it"
  - "several agents in parallel"
  - "did the subagents actually deliver"
floors: [F2, F11, F13]
---

# Delegated Build Fan-Out

For one objective handed to several parallel children at once (Hermes `delegate_task` with 2-10
tasks). Distinct from the bundled OpenClaw `sessions_spawn` template: children here have their own
contexts and terminals, cannot ask questions, and their summaries are **self-reports, not verified
facts**.

## Procedure

1. **Write ONE binding SPEC file before dispatching.** Put it in a shared workdir and point every
   child at it — do not repeat the constraints inside each task string. Each task string stays short:
   its work-package id, its deliverable, and "read the SPEC first".
   Skeleton: `templates/delegation-spec.md`.
2. **Define the success property, not the noun.** "Make the system care" and "improve reliability"
   are nouns. Write what would make it true and what would prove it false.
3. **Include the HARD FORBIDDEN list** — every invariant plus the specific destructive shortcuts, each
   with its rationale. Always name: restarting the live gateway (it kills the session that dispatched
   the work), writing to constitutional files, printing any secret, and any human-facing side effect
   beyond one designated target.
4. **Designate exactly one verification target** for side effects (one chat id, one file path, one
   endpoint) and require the child to prefix test output so it is recognisable.
5. **Set the evidence contract.** One JSON line per child into a shared ledger:
   `{agent, wp, state, files, command_run, observed, trace_id, blocked_op, next_owner}`.
6. **Require the true state, and say up front that HELD and BLOCKED are complete answers.** A child
   papers over a gap when the only outcome that looks like success is "done". Explicitly: "a held or
   blocked line is a full receipt, not a failure."
7. **Cap the final message** (WP id + state + the command + a verbatim output excerpt + absolute
   paths + what it could not do). Long summaries hide the missing line.
8. **Give each package its own "verify by <command>" instruction** so the child cannot substitute
   "I read my own code and it looks right".
9. **Dispatch, then verify yourself.** Open each child's artifacts, re-run the load-bearing command,
   and confirm the wiring is live before reporting value delivered.

## Pitfalls

- **A unit-verified artifact is not a working feature.** A green assertion suite, an exercised helper,
  a `PASS` from a function called by hand — all prove *the unit works*, none prove *the live system
  calls it*. Children will report `VERIFIED` on this basis and be technically correct, while the
  feature reaches no user. Check the mechanism is loaded:
  `grep -c "<plugin-or-module-name>" <live log>` (`0` = dormant) and
  `ls -la <registry/config file the mechanism requires>` (absent = never constructed).
- **Never accept `VERIFIED` derived from reading the artifact's own code** — by the child or by you.
  Self-report is the claim under test, not the test. Require the command and its real output.
- **When the intended mechanism is dormant, fix the surface that IS loaded.** Then report the dormant
  wiring as a finding in its own right — "built, verified, unreachable" is the complete and useful
  answer, and it is what the principal actually needs to know.
- **A config edit is not live until the process that reads it restarts.** Verify by observed
  behaviour, not by re-reading the file.
- **Constitutional files get a PREPARED diff, not an edit.** Have the child write the unified diff
  plus a `patch --dry-run` result into the workdir and hold the application for the principal's word.
- **Children cannot ask questions.** Anything ambiguous in the SPEC becomes a silent guess, and a
  guess that produces a file looks identical to work. Resolve ambiguity in the SPEC, not in the
  child's head.
- **Do not wait or poll.** Results arrive on their own; finish whatever does not depend on them and
  end the turn.

## Close-out

Report per work package: id, true state, the command, a verbatim output excerpt, absolute paths, and
what was not done. Distinct from `verify-runtime` (terminal-state verification) and from the bundled
`FORGE-subagent-spawn` (the OpenClaw single-spawn contract) — this is the coordinator side.
