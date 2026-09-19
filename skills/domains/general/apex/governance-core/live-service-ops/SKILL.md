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

**Rephrasing is legitimate for DOCUMENTATION only, never for EXECUTION.** When the text's
purpose is to describe the gate — a skill body, a receipt, a postmortem — write it in plain
English that does not reproduce the guarded verb, because the gate matches text, not intent.
A skill_manage update that documented the lifecycle pattern as an example was blocked by
the same gate for exactly this reason.

When the purpose IS the mutation, do NOT reach for a synonym, an alias, or an
equivalently-spelled verb to slip past. A control the actor can re-issue for itself is not
a control: defeating the pattern leaves the security property unsatisfied while the receipt
reads as success, and it teaches every later agent that the gate is decorative. Cost of
obeying is one blocked cycle. Report MUTATION_HELD plus the exact blocked operation.

**An artifact you must hand to another lane cannot reproduce the guarded literal.** A receipt,
postmortem, or handoff gets committed, and committing scans its text like any other argument — so
writing the guarded verb down blocks the very write that records the hold. Describe the operation
instead: target, verb class, reason, effect, and the lane that owns it.

```
TARGET : <unit or path>
OP     : <verb class, e.g. "unit reload">      (T3 — held at the text gate)
WHY    : load <file> @ <commit> into the live process
LANE   : kernel judge SEAL, or the executor organ
EFFECT : <the observable change, in one line>
```

The distinction is exact: from the *artifact* the guarded string is omitted; the *operation* still
travels its authorized lane. Describing an operation is not deferring it, and deferring it is not
abandoning it — naming the lane and the blocked op is what makes the hold actionable instead of
decorative.

**The gate's own escape lanes may themselves be down.** Before concluding a mutation is
impossible, walk each lane the gate names and record a measured failure for each — the
kernel judge path (verdict + reason_code), the signing service (presence guard configured?
key loaded? is it running code newer than its process?), and the executor's credential
store. "Every lane degraded" is a much stronger finding than "blocked": it says the
institution has no working path from sovereign-authorized to mutation-executed, which is
the thing F13 actually needs to fix.

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

For a systemd hardening directive the declared and the effective values live in different
files, and they diverge silently:

```bash
systemctl show <unit> -p CapabilityBoundingSet --value                      # declared
BND=$(grep '^CapBnd' /proc/"$(systemctl show <unit> -p MainPID --value)"/status)
```

Decode the hex against the `capabilities(7)` bit order. Measured case: five units carried the
hardening line and only some had the mask actually applied — one silently retained
`CAP_SYS_ADMIN` and `CAP_SYS_MODULE`, and several retained `CAP_DAC_OVERRIDE`. While an organ
holds `DAC_OVERRIDE` its filesystem permissions stay advisory: the process can bypass any
`chmod` you set, so an ownership/permission hardening claim about that unit is false no matter
what the unit file says.

A source-text grep and a `systemctl cat` both report all five clean. Only `/proc/<pid>/status`
knows. The generic form: **a control has at least two layers — what was declared, and what the
enforcement layer bound. Read the layer that enforces.**

## Census the live surface, not the source

The surface a process exposes is part of its state. A service whose source gained routes,
tools, or handlers but whose process was never reloaded advertises the OLD surface — and
every downstream report written against it is describing yesterday's code.

```bash
systemctl show <unit> -p MainPID -p ExecMainStartTimestamp
ps -o pid,lstart -p <pid>
stat -c '%y %n' <source-file>
```

Source mtime newer than process start == the running surface is stale. Say WHICH surface is
stale rather than assuming deployed behaviour matches the code: an operator can add a write
path to the source and still have a process that exposes only the read half, which looks
like "the feature was never built" instead of "the process was never reloaded".

Corollary for one-shot units: a `Type=oneshot` timer job re-imports its modules on every
run, so a source fix reaches it at the next fire with no lifecycle op at all. Always check
whether the affected path is a long-lived daemon or a scheduled job before declaring a
fix undeployable.

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

**First confirm you are both looking at the same machine.** In a multi-node federation one
agent's "disk 30%, that directory does not exist" and yours of "disk 82%, 27G present" can
two be correct readings of two hosts. Name the subject before treating a disagreement as an
error in either probe:

```bash
hostname; tailscale ip -4 2>/dev/null | head -1; df -h / | tail -1
```

A peer that retracts its own finding because your numbers differ has not corroborated
anything — it has swapped one unverified reading for another. The fix is to qualify each
reading with its host, never to average them.

**A peer's "the file does not exist" is a claim about the peer's filesystem VIEW, not about the
work.** Agent working trees on different nodes are frequently *frozen mirrors* rather than
replicas, so an honest probe on a stale node produces a confident, wrong negative. Measured on one
pair: the authoring node held 168 files in a directory with the newest edited that day; the peer
node held 37 files, newest twelve days old, on a checkout twelve days behind. Both readings were
true — one described the work, the other described a replica.

```bash
# run on BOTH hosts; compare four facts, not the single path the peer reported
hostname; ls <dir> | wc -l; ls -lt <dir> | head -3; git -C <repo> log --oneline -1
```

Read the disagreement instead of resolving it by picking a winner: same host and path with the
entry absent is a real absence; a different host is a finding about that host, not about the work;
an unexpectedly small count on the same host means the peer is reading a mirror — find which tree
its view resolves to. **Publish into the claiming node's view, then verify by content hash on both
sides** — size or mtime agreement passes on a truncated or differently-versioned copy. Carry the
mirror staleness forward as a finding in its own right: an auditor reading a frozen replica can
only report on the past, and that caveat belongs on every verdict it signs.

**A peer saying "I was wrong, you have the evidence" is not verification either.** They read
your output. Check their finding against the source before carrying it forward — a peer's
confidence is not a second witness.

## A test that writes to production is not a test

Redirecting a store by patching a caller's namespace is not enough. Python modules
do `from pkg.store import get_store` **inside functions**, so the name resolves at
call time against the source module — patch `pkg.store.get_store`, not
`caller.get_store`. A path you redirected can also be un-redirected by any later
line in the same file (a section that restores a monkeypatched function is enough),
and the suite silently starts writing to production.

Prove hermeticity by hashing every production store around a full suite run and
asserting the hashes are unchanged. Do not infer it from reading the fixtures.

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

Pitfall: the old version may ignore your dataset override entirely. Monkeypatching a
module constant only works if the old code reads that constant. A read path that
hardcodes an absolute file path will silently keep reading LIVE data while you believe
you are testing against a fixture — and the A/B then "passes" for the wrong reason.
Detect it by asserting the OLD tree sees a value that exists only in live data (a
marker row) while pointed at a fixture; if it does, report the hardcoding as a finding
and compare old×live against new×live on the SAME real file instead.

## Reversibility

State the rollback before the change. If there is no rollback path, it needs authority.

## Before deleting anything to reclaim space

Destructive cleanup is the highest-consequence mutation on a live box, and the one where a
confident wrong answer arrives fastest: a directory that *looks* like a duplicate is usually
the only copy of something. A total formed from directory sizes is a **ceiling, not a
finding**.

**A copy of a git repo is not redundant until you prove the work is elsewhere.**

```bash
# 1. Is the copy's HEAD reachable from the live repo?
git -C <live> merge-base --is-ancestor "$(git -C <copy> rev-parse HEAD)" HEAD
# 2. Does the copy carry refs the live repo has never seen?
comm -23 <(git -C <copy> rev-list --all | sort -u) \
         <(git -C <live> rev-list --all | sort -u) | wc -l   # nonzero = unique commits
# 3. Uncommitted work inside the copy — the thing a delete actually destroys
git -C <copy> status --porcelain | wc -l
```

An ancestor check on HEAD alone is **not** sufficient. A checkout that passed that test turned
out to hold commits reachable only from itself, plus a hundred-odd modified files. Run all
three, or do not delete.

**Identical names and identical HEADs do not make two directories duplicates.** Diff the trees
ignoring `__pycache__` and `.git` before assuming. Two sibling copies sat at the same HEAD,
both ahead of origin, and one carried an uncommitted fix to a live bug — a shared HEAD is
evidence of a common base, never of equal content.

**Prove the backup covers the path; do not infer it from "we run backups".**

```bash
restic snapshots --compact                          # what exists
restic ls <snapshot-id> | grep -E '<path-prefix>'   # empty = the path is NOT in the backup
```

A healthy dedupe or compression stat says nothing about *which trees are in scope*. When the
backup covers neither the deployment root nor the agent work tree, "we have backups" is true
and irrelevant to every candidate on the list.

**Report three buckets, not one number:** safe to remove / needs the owner's decision /
load-bearing. Do not quietly restate a smaller figure as though it were the original plan —
name which items failed and why, because each failure is a finding about the setup.

**When the safe reclaim turns out to be small, the finding is the growth mechanism, not the
total.** Unpushed work sitting as full directory copies is structurally self-inflating: every
unpushed item gets copied, and copies cannot be discarded because they are the only place the
work exists. The durable fix is to push and to widen backup coverage — not to delete harder.

## Mutations that look like they worked

1. Immutable path refuses by design — check `lsattr`. Never clear the flag to make your
   edit land; report BLOCKED_AT_GATE.
2. Partial apply reports as complete — isolate every op, report applied/skipped/failed.
3. Backup beside source gets scanned — write backups outside every scanned root.
4. Symlink property reads the wrong object — resolve before reading. A link's own mode is
   `lrwxrwxrwx` on any filesystem that stores modes, so 777 there is not a permission and a
   scan that reports it has invented a vulnerability. Use `stat -L -c '%a %U:%G %n'` and
   `readlink -f`; then check the target's mode, not the link's.
5. Claim before measurement returns — probe is not evidence until it exits.

---
*DITEMPA BUKAN DIBERI*