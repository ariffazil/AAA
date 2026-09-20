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

**A panel can report a healthy component dead for weeks, and nobody notices.** A monitor that
hardcodes one endpoint shape (`/health` on every port) across heterogeneous services asks the
wrong question of the one component whose surface differs: a 404, or a 400 meaning *server up,
request malformed*, reads as failure and the component is marked dead on every run. Refused and
not-found are not down. The tell that the probe was never re-validated is a **second stale
field in the same entry** — usually the component's role/label, which still names an older
identity. So when a panel says a component is dead but you can reach it, do not argue with the
panel and do not restart the component: compare the probe's URL **and port** against the
component's real surface, then fix the probe. `:PORT/mcp` answering 400 while `:PORT/health`
answers 404 is one entry in a config table, not an outage. A monitor that invents absence is
worse than no monitor, because the report it signs reads as confident.

**A cold first read is the same invented absence with the endpoint right.** A monitor that probes
once and treats the response as the surface reports a live MCP as holding zero tools whenever the
first request lands before the server warmed. `tool_count: 0` is not a reachable state for a running
MCP transport, so it always means the *read* failed — never that the tools were removed. A guard's
own transient filter will not catch it: a container that is cold on the *first* probe every time
looks like a stable change, not a flap, so it passes straight through the "matched on confirmation"
check and is written as real drift. Rule: any verdict of the form "the whole surface was removed"
must re-probe before it is written, because a total is the one reading that cannot be a delta.
Measured: a guard emitted `TOOL_REMOVED` at `CRITICAL` for a unit that answered 123 tools on three
consecutive probes with byte-identical bodies. Baseline such an organ while it is warm — record the
body hash, not just the count — and compare later aggregates against that hash.

## A refusal is address-specific

**Prefer adding the missing bind over a lifecycle op.** Never op on the strength of
`is-active` alone — `LoadState` is the discriminator.

**A monitor's endpoint is part of its claim, so read the address before you believe the
verdict.** A probe that returns "down" has told you only that nothing answered *at that
host, port and path*. Three of those four are usually wrong when a service is healthy.
Discriminate by the status code — only the last two are actually down:

| What came back | What it means |
|---|---|
| `200` | up |
| `401` / `403` | **up**, auth-gated |
| `400` | **up** — the server parsed the request and rejected its shape |
| `404` | the **path** is wrong, not the service |
| connection refused | nothing is listening **on that address** — check the bind |
| timeout | down, or hung mid-request |

`ss -lntp | grep <port>` shows which addresses a port actually answers on; a service bound to
one interface is refused on every other. Measured: a gateway bound only to a tailnet address
answered `200` there and refused on `127.0.0.1`, so two consumers configured against localhost
reported it unreachable while it served traffic the whole time. Both readings were true.

**A probe list with one hardcoded path for N heterogeneous services mislabels the odd one out,
and nothing re-checks it.** Measured: a cockpit prober fetched `/health` on a fixed port for every
organ. Eight matched. The ninth ran an MCP transport on the configured port, so `/health` returned
`404` there while the real service sat on another port and answered `200` — and the organ was
published as **dead for 44 days**, ~120 000 missed probes, zero humans noticed, because everything
else in the list was green. The stale label on the same row (an old role name) was a second tell
that nobody had read it since it was written.

When you correct such a probe, verify the **verdict flips** (`8/9 alive` → `9/9 alive`), keep a
backup of the prober before editing, and confirm the new target live rather than trusting the
edit. A monitoring fix whose before/after verdict is not recorded is indistinguishable from a
monitoring fix that did nothing.

**A monitor is a service too, and it inherits the same rule as any other claim: verify the
instrument before acting on its reading.** The same failure looks different from the other side —
the instrument is honest about what it fetched, and the narrative laid over it ("organ down") is
the false part.

**An identical value across consecutive reports means the monitor stopped observing.** For any
counter that only ever grows — a ledger length, a seal sequence, a receipt count — a byte-identical
figure on two successive runs is not stability, it is a cached or truncated read. Before quoting it,
compare the value against the artefact's own mtime and against the counter's advance: a chain length
pinned at the same figure while new entries accumulate means the report is quoting a copy, not the
ledger. Say which file the number came from and when that file was last written.

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

**And read the TIMER, not the service, before calling a scheduled job dead.** A `Type=oneshot`
unit sits at `inactive (dead)` between fires and is normally `disabled` for boot purposes — both
are correct for a timer-driven job and neither means it stopped running. The liveness fact lives in
the timer:

```bash
systemctl list-timers --all | grep <job>      # LAST and NEXT are the evidence
systemctl show <job>.timer -p NextElapseUSecRealtime -p LastTriggerUSec
```

Measured: three outcome-closure units all read `disabled` + `inactive dead` — exactly the shape of
an abandoned job — while their timers had fired successfully that same morning and were scheduled
again for the next day. `is-enabled` answers "does this start at boot"; `is-active` answers "is a
process alive right now"; for a scheduled job the question is neither. Reading the service alone
produces a confident false outage report about machinery that is working, and it is the same
invented-absence defect as a probe with the wrong endpoint.

### An intervention is not credited until it was in effect while the fault was live

Three clocks decide whether a fix caused a recovery, and all three must be read before you claim it:

```bash
stat -c '%y %n' <file-you-edited>                        # when the change reached DISK
systemctl show <unit> -p ExecMainStartTimestamp --value  # when the process RE-IMPORTED it
stat -c '%y' <event-ledger-or-report>                    # when the symptom last OCCURRED
```

A long-lived process holds your module in memory, so a file edit is **not in effect** until it
restarts. If the condition stopped before that moment, your change was never exercised and cannot be
credited — record `NOT_EXERCISED`, not "fixed". Measured: a change landed on disk, the storm's last
event followed within the minute, and the process restarted only eleven seconds *after* that last
event, while the detector's own verdict flipped to healthy on its own. The patch was real and its
regression passed, and it had still never seen the fault live. Report exactly that. A fix presented
as the remedy for an incident it never overlapped is a claim the next recurrence falsifies — and the
reader then discounts your probes as well as your conclusions.

**Before/after proof needs the condition present in the "before".** If the detector already reports a
clean verdict when you start, you are measuring a system that has recovered; the deltas you record
are weather, not the effect of your edit. Say which of the two you measured.

## Reading `/proc` — names, never values

Verifying a live process means reading `/proc`, and one of those files is a credential store.
`/proc/<pid>/environ` holds every secret the unit loaded, and a diagnostic that prints it publishes
them: tool output is persisted into the session transcript, so a value printed once is a value
published. Filter to names before anything reaches your output.

```bash
tr '\0' '\n' < /proc/$pid/environ | cut -d= -f1 | sort        # NAMES ONLY — safe
systemctl show <unit> -p EnvironmentFiles                      # which file supplies them
```

**Never grep the `KEY=VALUE` lines and redact afterwards.** A line-level pattern matches the whole
line, so a **value** that happens to contain the pattern token selects that line — and `grep` has
already written the value down the pipe before any `sed` runs. Measured: a filter for the substrings
`chron|store|db|path`, intended to locate where an organ kept its data, emitted a provider API key
because that key's value contained `db`. The pattern was not the defect — filtering full lines is.
Cut to the field *before* emitting; the same applies to `cmdline` and any config dump.

Use the name-only wrapper rather than hand-typing a filter: `/root/scripts/secretsafe.py`
(`env <pid|unit>` · `file <path>` · `units` · `agentcheck`) prints variable names and, for a
credential, only `<redacted len=N fp=hash>`. Raw mode needs a real tty and is refused in any
agent/pipe context. Regression suite `/root/scripts/tests/test_secretsafe.py` asserts names surface
and zero values reach stdout with live secrets in scope.

The same applies to `cmdline` and to any config dump. **If a value does escape, the credential is
rotated — not scrubbed.** Editing the log removes the evidence and leaves the credential live;
order the rotation first, name plainly which credential was exposed, and never leave the decision
to whoever reads the transcript next.

**Push the escaped value to its blast radius before reporting.** If a whole environ dump was
emitted you cannot enumerate from memory which values landed in it — treat **every** secret that
process inherited as exposed, not just the one you noticed, and audit the *persisted* surface
(session traces, `state.db`/`-wal`, terminal cache, search indexes, memory exports) for the value's
presence. Report file counts and paths; never print the value again to prove it is there. Rotation
is ordered by the **issuer** (provider console, bot owner, DB owner) — a boundary the agent cannot
cross alone, so this is a sovereign binary, not a task to complete quietly.

## De-scoping a unit's secret inheritance

Units that share one flat `EnvironmentFile` each inherit every secret in it, so one file leaking
leaks everything and no unit's requirement was ever scoped. Count before you change anything — per
unit, load its `EnvironmentFile=` list and compute:

```
SECRETS_PRESENT     every credential name in the files it loads
SECRETS_REQUIRED    credential names referenced in the service's OWN code tree
                    (grep the source for each name — never infer need from the unit's name)
EXCESS_SECRETS      PRESENT - REQUIRED   ← drive this to ∅
```

Measured: **30** canonical units loading broad flat stores — 27 still carrying 74–153 credentials
each, 3 already clean. One temporal organ inherited 7 with **zero** referenced anywhere in its own
source, so de-scoping it removed every credential it held.

**Count units canonically, never by file glob.** Globbing `/etc/systemd/system/*.service` together
with `*/*.service` double-counts: a unit reachable through a `.wants/` symlink appears twice, and the
naive pass reported 43 where the canonical census found 30. Enumerate with
`systemctl list-unit-files --type=service`, resolve each via
`systemctl show <unit> -p FragmentPath --value`, and dedupe on that resolved path. An inflated count
overstates the work and, worse, hides how many units are genuinely over-broad.

Target invariant:
`secret(service_i) ∩ unnecessary_credentials = ∅` — compromise of one organ must not imply
compromise of every external account.

Procedure:

1. Back up the unit file beside the source tree, not inside a scanned root.
2. Confirm the service needs none of them by grepping its code for each name; then remove the
   `EnvironmentFile=` line, leaving a comment naming the backup path and why it was removed.
3. **Preflight that the unit can come back** before you restart it:
   ```bash
   readlink -f "$(systemctl show <unit> -p ExecStart --value | grep -o '/[^ ]*python3' | head -1)"
   <interpreter> -c "import <every non-stdlib module in the tree>"   # deps still importable?
   curl -s -m 8 http://127.0.0.1:<port>/health                        # BASELINE, saved
   ```
   An `ExecStart` path that resolves and modules that import are the two ways a green-looking unit
   still fails to return.
4. `systemctl daemon-reload && systemctl restart <unit>`, then re-read health and compare to the
   baseline: the number of `*_count` fields must be unchanged or advancing, not reset.
5. Re-read the process env and assert the credential names are gone:
   ```bash
   tr '\0' '\n' < /proc/$(systemctl show <unit> -p MainPID --value)/environ | cut -d= -f1 | sort
   ```
6. **Restart the unit that carries your own conversation last, or not in this turn.** When the
   list of over-broad units includes the gateway hosting the session, batch-restarting it ends the
   conversation; leave it for a detached, scheduled lane and say so.

A service that comes back on fewer credentials and serves the same health body is the proof the
removal was safe — record the before/after env var count alongside it.

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

**Enumerate EVERY module-level path the code will write to, not just the one you set out to isolate.**
A module often carries several path constants — a store dir *and* a receipt log *and* an offset file —
and redirecting one leaves the writer still appending to production through the others. Measured: a
module holding both a dedup-directory constant and a receipt-log constant was isolated on the first
only, and six test records landed in the durable production ledger. The tell is that the test *passes*.
Write the isolation as "list every module-level constant that names a path", and assert each one
resolves under the temporary root **before** the suite runs, not after.

**Recover by quarantining the records, not by deleting them.** Genuine and test entries are
interleaved in one append-only file, so removing the file destroys both — and destroys the evidence
that pollution happened. Move the identified test records to an explicit
`quarantine-<who>-<what>.jsonl` beside the original, leave the genuine records in place, and state the
before/after line counts. A production ledger whose contents you cannot reconstruct after cleanup is a
second, larger defect than the one you were fixing.

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

## Reproduce the service's own filesystem access

A read or write that fails for the service can succeed for you, and the reverse. Four distinct
causes all present as the same permission error:

| Cause | Probe |
|---|---|
| Immutable attribute | `lsattr <path>` — `i` in the flags |
| Mode / ownership | `stat -c '%A %U:%G %n' <path>` |
| ACL | `getfacl -p <path>` — group ACLs grant access that mode bits deny |
| systemd sandbox | `ReadOnlyPaths`, `InaccessiblePaths`, `ProtectSystem`, `RootDirectory` in the unit and drop-ins |

`sudo -u <user>` does **not** reproduce the service context: it drops supplementary groups and
omits every sandbox directive. Use a transient unit instead:

```bash
systemd-run --unit=diag-read --uid=<user> --gid=<group> \
  --property=SupplementaryGroups=<group> --property=Type=oneshot --wait --pipe \
  /usr/bin/test -r <path>
```

Always `systemctl reset-failed diag-*.service` afterwards. A diagnostic unit you leave failed shows
up in `systemctl --failed` and gets read later as a live organ outage.

**A service starts in the context systemd builds, not the one you can type.** A precondition that
fails at start time and succeeds when you reproduce it is not evidence the gate is fine — it is a
non-deterministic precondition until you can show the difference. Two identical probes disagreeing
seconds apart is signal, not flakiness.

## A start loop that has exhausted is not a service that will recover

Check the counter and the give-up line before assuming anything self-heals:

```bash
systemctl show <unit> -p NRestarts -p ActiveEnterTimestamp -p ExecMainStatus
journalctl -u <unit> --since '-10 min' | grep -E 'restart counter|repeated too quickly|Failed to start'
```

`Start request repeated too quickly` means systemd stopped trying — the unit stays down until a
human or a lane acts. Report `DOWN — start budget exhausted`, never "it is probably back". Name the
failing precondition (the `ExecStartPre` exit status identifies it). If that precondition cannot be
reproduced, classify `FLAKY_PRECONDITION` and leave the mechanism open rather than naming a culprit
— an unresolved cause is more useful than a guessed one, and the flakiness itself is the finding
that matters, because it means any future start can fail permanently too.

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

**Hash the doomed set before you remove it.** A purge destroys the ability to measure anything about
the population afterwards — its rate, its distribution, its first-seen date — and those are usually
the questions asked next. Write a receipt first: file count, byte total, oldest and newest timestamps,
an aggregate census by status and reason class, a sorted `name<TAB>size` manifest hash over the whole
doomed set, exactly what you deliberately retained as samples, and the reversal path (for a
regenerating artifact, "the producer writes a fresh one on the next tick" is a reversal). Then
delete. The manifest is a few hundred bytes and turns an irreversible act into an auditable one;
without it the purge leaves behind only a number.

**Say what the purge cost you in measurement, not just in disk.** If the pile you are deleting was
the only record of how often a condition occurred, the honest receipt names that as a limitation of
the removal, in the same document. Destroying the instrument and the evidence in one action is
recoverable for disk and not recoverable for the question.

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
4. Symlink reads AND writes resolve to the wrong object. Reading: a link's own mode is
   `lrwxrwxrwx` on any filesystem that stores modes, so 777 there is not a permission and a
   scan that reports it has invented a vulnerability — use `stat -L -c '%a %U:%G %n'` and
   `readlink -f`, then check the target's mode, not the link's. Writing: a file-write to a path
   that is a symlink replaces the **target's** contents, so "create a small shim here" can
   silently destroy the implementation it pointed at. Never author a shim as a symlink to the
   thing it wraps — make it a wrapper that execs the target — and if a link already sits at that
   path, unlink it first. Recoverable only if the target is under version control.
5. Claim before measurement returns — probe is not evidence until it exits.
6. **A write to a symlinked path lands on the TARGET.** The same resolution that makes `readlink -f`
   correct for *reading* makes an unguarded write destructive. `test -L <path>` before writing; if it
   is a link, remove the link and write a real file. A "thin wrapper" placed at a link path wraps
   nothing — it overwrites the file the link points at, and the loss is silent because the path you
   wrote to still exists and still looks right. **The tell: the file you meant to create is absent,
   and the file you meant to call now contains your content.** Recover from version control before
   doing anything else, then re-verify the target runs.

## `logrotate --force` is not a dry run

`logrotate -d <conf>` is the only non-mutating mode. Adding `--state <tmp>` does
not make `--force` safe: it makes logrotate perform a **real** rotation while
writing its bookkeeping elsewhere. Measured case: a "parse test" run this way
renamed three retained evidence files to `*.1` and left 0-byte stubs in their
place — the artifacts a purge receipt pointed at, silently emptied.

```bash
logrotate -d /etc/logrotate.d/<rule>        # parse + decide, touches nothing
```

If it has already run: the content sits in the `*.1` file, not gone. Remove the
0-byte stub, rename `.1` back, then verify byte sizes against the receipt.
Never re-run `--force` "to check" — the check is `-d`.

**A rotation rule must not include the monitor's live state file.** Directories
holding a single always-current file (`latest.json`, `.last-signature`) need those
names excluded from the rotation pattern, or the next run rotates the monitor's own
state and the following probe emits a spurious transition.

## A control surface is not a service

When the change being shipped alters *what a governance/watchdog component
decides to emit*, treat it as a control mutation, not a bugfix: state the
before/after observable, prove it with an A/B run of the deployed artifact, and
record the authority that ordered it. A behaviour that silently changes what the
institution can see needs a receipt naming who authorized it and why.

## Support files

- `references/systemd-oneshot-notify.md` — wiring `ExecStartPost` / `ExecStopPost` on a oneshot unit
  so the job reports honestly: which hook fires when, which variable is the verdict (and why
  comparing the disposition word to `0` reports every success as a failure), and why a self-test
  must never write into the production channel.

---
*DITEMPA BUKAN DIBERI*