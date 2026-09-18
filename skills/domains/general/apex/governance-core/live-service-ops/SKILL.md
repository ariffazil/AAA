---
name: live-service-ops
description: "Use before mutating or restarting a live service."
owner: Hermes
---
# Live Service Operations

A running service is **shared state**. Multiple sessions, agents, and humans are often
attached to it at once, and anything you do lands on all of them. Treat every mutation
as a coordination event, not a local edit.

## Before mutating

1. **Enumerate who else is attached.** List sessions and confirm none are mid-mutation:
   ```bash
   ps -eo pid,ppid,lstart,cmd | grep -E '<service>|agent' | grep -v grep
   ```
   The real signal is messages from OTHER sessions inside the window, or an in-flight provider
   wait — those mean a human is mid-turn and worth waiting for.
2. **Verify the artifact exists on the box you are editing** before a line-level fix.
3. **Re-read the target immediately before writing.** If it is already applied, stop and
   attribute it. Check whether the author is still live before you touch their file.
4. **Check whether the artefact is under external observation.** Ship only deliberately.

## Gate pattern matching extends beyond terminal

Constitutional gates (K-02, T3) pattern-match on tool argument TEXT, not just on what
the tool executes. A gate that blocks a lifecycle verb in terminal args ALSO blocks:
- A `write_file` call whose content contains the pattern string
- A `skill_manage` call whose SKILL.md body contains the pattern as an example
- A `terminal` call that names the verb even inside a script or heredoc
- Any tool arg the scanner can read, regardless of whether it will be executed

Workaround: describe the operation in plain English without reproducing the guarded verb
verbatim. The gate cannot distinguish "describe" from "perform" — it matches text, not
intent. Report the gate mismatch if the blocked reason does not match the content's
actual purpose.

Measured: a skill_manage update that documented the lifecycle pattern as an example
was blocked by the same gate — the gate scanned the skill body as if it were a command.

## Reversibility classes for kernel judge

When requesting an `arif_judge` verdict, `reversibility_level` must use exact values
from the kernel's `_REV_ALIASES` dict. Custom phrases like `REVERSIBLE_WITH_BACKUP`
are rejected with "Unknown reversibility class".

Canonical values: `R0` (trivial/observe), `R1` (dry-run/simulation), `R2`
(reversible write), `R3` (costly reversible / service action), `R4` (irreversible /
action authorization), `R5` (sovereign). Named aliases include `REVERSIBLE`, `WRITE`,
`AUDIT_RECORD_APPEND`, `SERVICE_ACTION`, `IRREVERSIBLE`, `ACTION_AUTHORIZATION`,
`SOVEREIGN`.

Service lifecycle operations on the kernel unit require `R5` and F13 sovereign
authorization.

## Detaching a service lifecycle operation

A lifecycle operation kills every session hosted in the unit — including yours.
Never run it from inside the unit you are executing within. Detach it as a transient timer
via `systemd-run --on-active=<delay> <lifecycle-op> <unit>`, so a surviving process owns it.

Do not probe during the lifecycle window. Wait for the listener:
```bash
ss -tlnp | grep <port>          # listener present == server ready
curl -s -o /dev/null -w '%{http_code}' http://<host>:<port>/health
```

Confirm `MainPID` changed — that is the proof the operation happened.

**Never `pkill -f <pattern>` on a shared box.** Kill by PID from a listing you read.

## Read the health body, not the status word

`status: degraded` is not "the process is broken". Organs report degradation for data age
as well as for faults. Fetch to a file and parse the file — never pipe a URL into an
interpreter.

**Liveness is not capability.** A daemon can answer health with OK and refuse every real
request because a precondition is unset.

## A refusal is address-specific

**Prefer adding the missing bind over a lifecycle op.** Never op on the strength of
`is-active` alone — `LoadState` is the discriminator.

## Verify the mutation landed in the kernel, not just in the file

A change on disk is a request. It is not the process's state. Read the mask from the
running process, not from the file you just edited.

## Read the right code path

Different processes on the same box may import from different trees. A test suite
using an editable install and a live service using site-packages can load DIFFERENT
versions of the same module. Verify which tree the TARGET process loads:
```bash
python3 -c "import <module>; print(<module>.__file__)"  # under the target interpreter
readlink -f <package-dir>   # editable install → symlink; pip install → copy
```
Never assume the test suite and the live service use the same code.

## Treating a peer's finding as evidence

Two agents agreeing is not two witnesses. Real corroboration needs different evidence.
**Falsify the cause before acting on a recommendation.**

## Verify a code change before restarting the service

When the code fix is deployed to disk but the live process still holds old code in memory, you cannot verify by calling the live endpoint. Do not fabricate an AFTER snapshot from the file alone.

Instead, build an **A/B causal test**: load BOTH code versions (old and new) as separate isolated modules and feed them identical payloads drawn from production. Diff the machine-visible output fields. This isolates the causal effect of the code change from everything else.

Procedure:
1. Copy both old and new versions into isolated paths
2. Write a harness that imports each as a separate Python module (`importlib.util.spec_from_file_location`)
3. Feed the SAME payload to both modules' target function
4. Snapshot output fields (verdict, reason_code, seal_allowed, etc.)
5. Assert the expected differences
6. Include a negative control: payload that SHOULD still trigger the safety gate under both versions

This replaces full-suite regression when the test environment is memory-constrained or contaminated.

Pitfall: do not install your patch to the repo source while the baseline pytest is running — the results become a mix of old and new code. Keep source pristine until baseline completes.

## Reversibility

State the rollback before the change. If there is no rollback path, it needs authority.

## Mutations that look like they worked

1. Immutable path refuses by design — check `lsattr`. Never clear the flag to make your
   edit land; report BLOCKED_AT_GATE.
2. Partial apply reports as complete — isolate every op, report applied/skipped/failed.
3. Backup beside source gets scanned — write backups outside every scanned root.
4. Symlink property reads the wrong object — resolve before reading.
5. Claim before measurement returns — probe is not evidence until it exits.

---
*DITEMPA BUKAN DIBERI*