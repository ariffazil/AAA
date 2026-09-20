---
name: claimed-defect-verification
description: "Use when a probe reports something broken or missing."
version: 1.0.0
owner: Hermes
category: governance
tags: [probe, defect, handshake, false-positive, attribution, verification]
---

# Claimed Defect Verification

> **One line:** a failure report is a claim about the *probe* as much as a claim about a system.
> Before escalating it, prove the probe was capable of succeeding.

## Use when

1. A probe returns an error and the next sentence is going to be "X is broken" — especially
   `SESSION_MISSING`, `Missing session ID`, `Unknown tool`, `Not Acceptable`, a bare 400/403.
2. An external or lateral audit reports N defects on a system you own.
3. A tool, field, or capability is reported absent.
4. A metric reads `0`, `null`, or unanimous.

## The one rule

**A failed probe is evidence about the caller until proven otherwise.** Four independent things make a
probe fail while the system underneath is perfectly healthy. Check all four before the word "broken"
is written.

### Check 1 — did the probe complete the protocol lifecycle?

Multi-step protocols fail closed and **name the missing step**. That name is routinely escalated as a
capability, contract, or guard failure. The tell: the error names a *step*, not a *resource*.

**Never report a capability as broken, unreachable, contract-impossible, or guarded until the full
lifecycle has been completed and the call retried.** Recipe and decode table for the MCP case:
`references/mcp-session-lifecycle.md`.

This is the highest-yield check. In one pass it produced three separate false defects on three
organs, each of which would have consumed remediation effort on a system with nothing wrong.

### Check 2 — is the name the advertised name?

`Unknown tool: 'x'` means the server never advertised `x` — a **name error**, not a surface defect.
Dump the advertised list and grep it before filing anything as missing. Near-miss names read as
plausible and survive review, so verify the string character-for-character against the listing rather
than against recollection.

### Check 3 — is the metric's population verified?

A statistic is only as good as its denominator. `unanimity: 1.0` across N lanes is meaningless if the
lanes resolve to one shared backend. Before publishing an aggregate:

- Verify the members are **distinct actors**, not aliases.
- If members are fallback chains, they overlap — a dead primary silently promotes several members to
the same fallback, which manufactures agreement.
- Publish the denominator caveat **beside** the number.

"13 members agreed" and "fewer members, aliased" produce identical output. If your measurement cannot
separate them, report the independence property as `UNMEASURED` rather than implying it.

### Check 4 — which layer actually dropped it?

A field missing from a live payload can vanish in the **builder** or in a **projection / filter /
serialiser**. Never patch the projection first.

1. Invoke the builder **in isolation, inside the deployed environment** (not a checkout). If it
   returns a populated object, the builder is exonerated and the loss is downstream.
2. Then audit the projection — and confirm the keep-list you are patching is the one in force for the
   verbosity/mode you probed. A list governing `minimal` does nothing for a `full` request.

A keep-list cannot preserve a field that was never populated. Comparing *when the fix was written*
against *when the probe ran* is not evidence the fix works; only the post-restart payload is.

### Check 5 — whose lens produced the claim?

A defect claim is a measurement taken with *your* instruments. Before it is written down, re-take it
through the lens the system itself uses — the difference between the two lenses is very often the
entire finding.

| Claim shape | The wrong lens | Re-take it as |
|---|---|---|
| "service X's self-report contradicts its repo/state" | you reading the field | the command **that service runs**, in **its** context: `readlink /proc/<pid>/cwd`, `ps -o user= -p <pid>`, then `sudo -u <that-user> <cmd>`. A health field is computed with the process's own cwd, user and config — and a user-level ignore rule makes the same repo read clean to you and dirty to it. |
| "N jobs/items are dead — delete them" | the `disabled`/`paused` flag | the **reason** field. A paused-with-reason entry is a retirement *tombstone* naming its successor, migration target or authorising directive; it is a record, not a corpse, and deleting it deletes the answer to *why*. If the clutter is the real complaint, fix the **listing**. |
| "two supervisors / double lifecycle" | `systemctl` active AND the container healthy | `systemctl cat <unit>` — `ExecStartPre=-docker rm -f <name>` plus a launcher means systemd *owns* the container. One lifecycle. Rule out the boring explanation before filing a conflict. |
| "a monitor or check is failing" | its `last_status` field | compare its `last_run_at` against the mtime of the artefact it guards. An error logged by a run that happened **before** the fix landed is stale, not live — it clears at the next fire. |
| any of the above, during a long session | the reading you took earlier | re-probe. State moves inside a session — an upgrade, a restart, another writer's commit. Re-take the measurement immediately before any irreversible action; a reading that was true when taken can be false by the time it is acted on. |

**A claim whose consequence is destruction gets the harder probe.** "delete / remove / rewrite N" is the
load-bearing form of a defect claim: the next reader executes the written ledger, not this conversation.
Reproduce it through the system's own lens before it enters the ledger, and when it dies there, record
the retraction **in that same artefact** — a refutation left in chat gets re-filed by the next reader.
Replace the misleading line; do not append an "UPDATE: actually…" beneath it.

## Escalation discipline

- Separate **CONFIRMED** from **METHOD-ARTIFACT** from **UNMEASURED** in the write-up. Reporting all
  three as "defects" inflates a queue with items that can never be closed.
- **Re-probe a receipt before repeating it.** A receipt whose own reversal command cannot run is not
  a receipt — check that the recorded inverse operation still has a target.
- When a report is partly right, say which part. "Concept correct, method rejected" — otherwise the
  next reader either discards the whole thing or re-proposes the rejected half.
- When a probe was re-run and succeeded, the finding is about **timing**: report it as "was true at
  measurement time, not reproducible now", never as a standing defect.

## Pitfalls

- **A passed verification block does not license the claim.** Check whether the checks that ran are
  the ones that *could* have failed. A block asserting three green checks while the fourth — the one
  that actually broke — was never run is decoration, not verification.
- **A near-miss name is the most convincing false defect.** It reads as a real tool that "used to
  exist", inviting a hunt for a regression that never happened. Grep the listing.
- **A point-in-time reading is not a standing defect, and a stale one is not a live one.** A field
  that read `DIRTY`/`dead`/`error` can be correct for its own caller and wrong for yours, or correct
  when taken and wrong when cited. Both directions of that error are the same failure: quoting a
  measurement without its lens and its clock.
- **An unclear-but-valid error is still a client-side answer.** `unauthenticated`, `missing header`,
  `unsupported version` are the protocol doing its job. Read the probe's own actor/step fields before
  characterizing the remote side.
- **Do not let a scanner block tempt you into rewording correct guidance.** If a security gate flags a
  document for containing the very idiom it teaches against, that is a wall, not a policy — report
  the shape and leave the guidance intact.

## Adjacent

- `live-system-investigation` — how to probe without causing harm (redaction, mutation class,
  attribution). This skill covers the inbound direction: you were *given* a failure claim.
- `assertion-window-discipline` — the pre-assertion gate before any negative claim.
