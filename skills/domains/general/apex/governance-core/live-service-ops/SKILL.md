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

1. **Enumerate who else is attached.** A gateway hosts sessions; a shared node hosts
   agents. List them and confirm none are mid-mutation:
   ```bash
   ps -eo pid,ppid,lstart,cmd | grep -E '<service>|agent' | grep -v grep
   sqlite3 /root/.hermes/state.db \
    "SELECT session_id, COUNT(*), MAX(datetime(timestamp,'unixepoch','+8 hours'))
     FROM messages WHERE timestamp > strftime('%s','now')-600 GROUP BY session_id;"
   ```

   **Exclude your own session, and never use a raw log-line count as the busy test.**
   `journalctl --since 60s | wc -l` counts your own probes plus boot and background-review
   noise, so it reports busy almost always and trains you to defer the change forever. The
   real signal is messages from OTHER sessions inside the window, or an in-flight provider
   wait — those mean a human is mid-turn and worth waiting for.
2. **Verify the artifact exists on the box you are editing** before a line-level fix —
   `test -f`, `grep -c`. A same-named file on a sibling node is the commonest
   wrong-layer error.
3. **Re-read the target immediately before writing.** Sibling sessions move fast; a
   fix may already have landed while you were investigating. Re-check at write time,
   not only at the start.

   **If it is already applied, stop and attribute it.** The finding is then *who else is
   editing this machine*, not the fix. Never claim a change you did not make, and never run
   an idempotent "no-op" write or reload after telling the user you would hold — reporting an
   action that in fact did nothing is still a false claim about your own effects, and the
   write you performed anyway destroys the evidence that would identify the real author.
4. **Check whether the artefact is under external observation.** A restart or redeploy
   replaces the thing a third party is currently measuring — an external reviewer
   mid-scan, a benchmark in flight, someone reproducing a bug you just acknowledged.
   Ship anyway only deliberately, and say that you did; then tell the observer the
   artefact moved, so their observation is not silently invalidated. A deploy that
   invalidates someone else's measurement is a coordination event, not a local edit.

## Restarting a service you are running inside

A restart kills every session hosted in the unit — including yours. Never
`systemctl restart` the unit you are executing within, and never `nohup` it from
inside (the process tree dies with you). Detach it as a transient timer:

```bash
systemd-run --on-active=60 systemctl restart <unit>
```

Detach even when the restart is not yours to perform: schedule it, report it, let a
surviving process own it.

**Do not probe during the restart window.** A service that is `active` but has not yet
bound its ports is indistinguishable from an outage in a single probe. Wait for the
listener before judging either way:

```bash
ss -tlnp | grep <port>          # listener present == server ready
curl -s -o /dev/null -w '%{http_code}' http://<host>:<port>/health
```

Once it is up, confirm the restart actually happened: **`MainPID` changed** (a restart that
silently failed leaves the old pid in place), the adapter's connected line appears in the boot
window, and the named noisy signal you set out to fix is gone from that window.
`ActiveState=active` on its own proves none of this — it describes the unit, not the code the
unit is running.

**Never `pkill -f <pattern>` on a shared box — the pattern matches the shell that is running it.**
Measured 2026-09-17: `pkill -f <script-name>` terminated the tool call that issued it (exit `-15`,
SIGTERM), because the invoking shell's own command line contains the pattern string. On a machine
where several agents run the same scripts, the same expression can also take out a sibling's
in-flight work with no warning to either party. Kill by **PID you obtained from a listing you read**
(`pgrep -a`, then verify the `cmdline` matches what you expect), or scope the pattern to something
the caller cannot contain. A pattern-kill is an unbounded mutation dressed as tidying.

## Read the health body, not the status word

`status: degraded` is not a synonym for "the process is broken". Organs report degradation
for **data age** as well as for faults, so read the sub-objects before you touch anything:

```bash
curl -s -o /tmp/health.json http://127.0.0.1:<port>/health && python3 -c "
import json; d = json.load(open('/tmp/health.json'))
print({k: d.get(k) for k in ('status', 'truth_status')})
print(d.get('freshness'))
print({k: v for k, v in d.items() if 'degrad' in k.lower() or 'reason' in k.lower()})
"
```

Fetch to a file and parse the file — never pipe a URL straight into an interpreter. The pipe
hides the bytes from any inspection step and turns a failed or hijacked fetch into arbitrary
code, and it is also the pattern that gets an otherwise-good script blocked by the security
scanner.

- `freshness.status: expired` or a large `state_age_hours` is **data staleness, not a service
  fault**. A restart does not fix it and destroys the evidence; the fix is a fresh write from
  whoever owns the data.
- 401/403 on a health endpoint means the service is **up** and auth-gated. Connection-refused
  is DOWN **at the address you probed** — a refusal elsewhere says nothing about the service
  (see "A refusal is address-specific" below).
- A stale *snapshot file* is not a health signal, and a scheduled job told to read one instead
  of probing live will keep reporting old state indefinitely. When a job's output looks wrong,
  check what it was told to read before you check the service.

## A refusal is address-specific — probe the address the consumer uses

A service can be fully up and refuse the address you picked, and restarting on the strength of one
refused probe is an outage you caused. **The diagnostic recipe (bind census + reading the consumer's
own environment) is owned by `bridge-lane-functional-probe` § Rule 1b** — load it before any down
verdict; it is not restated here.

The mutation-side consequences are this skill's:

- **Prefer adding the missing `bind` over restarting.** One line on the existing frontend is
  reversible and cannot disturb the address that already works. A restart of a healthy unit is an
  outage whose blast radius is every session attached to it.
- **Never restart on the strength of `is-active` alone.** It reports `inactive` for a mistyped unit
  name exactly as it does for a stopped one (`LoadState` is the discriminator). Restarting a unit
  whose name you guessed is how a healthy service gets stopped to fix a name typo.
- **State which address you probed** in the report. "Down" without the address is not a finding.


## Prefer the smallest change inside the mechanism already running

When the defect is one condition or one call site, extend what already exists rather than
adding a parallel thing — a new framework, a new state file, a new metric store all have to
be understood, refreshed and eventually removed by whoever reads the system next. The test:
could this be a field on a record the system already writes? Then it is a field, not a
subsystem.

Corollary — **every new piece of state must declare its lifetime where it is defined.** A
counter that resets per session must not be named or described as a repetition metric; the
the next reader assumes the persistence the name implies and draws a conclusion from a number
that cannot see what it claims to measure. If the durable version of the same fact is already
recorded somewhere else, say so in the comment and point at it.

**Search for the abandoned mechanism before proposing a new one.** Estates accumulate
built-but-dormant machinery: a ledger with the right schema, a gate with no receipts, a monitor
nothing reads. Finding one changes the recommendation from "build X" to "finish and wire X",
which is far cheaper — and the absence of invocations is what marks it dormant, not the absence
of the file. Probe by artifact class, then read its newest write:

```bash
ls -la --time-style=full-iso <state_dir>/*.jsonl <state_dir>/*ledger* 2>/dev/null | tail
tail -2 <candidate>        # newest record + its timestamp: dormant vs merely idle
```

Treat a dormant mechanism's own contents as evidence too — placeholder or `SIMULATED` result
fields mean it has never carried real work, so it cannot be cited as "we track this". Report it
as REACHABLE and unexercised, name the wiring that is missing, and do not mint a parallel store
beside it.

## Verify the mutation landed in the kernel, not just in the file

A hardening directive — `CapabilityBoundingSet=`, `NoNewPrivileges=`, `ProtectSystem=`,
`PrivateTmp=` — is a *request* to the service manager. It is not the process's state, and the two
disagree exactly when the service was never restarted onto the new line. Read the mask from the
running process, not from the unit file you just edited:

```bash
for svc in <units>; do
  pid=$(systemctl show "$svc" -p MainPID --value)
  printf '%-12s pid=%-8s CapBnd=%s NoNewPrivs=%s\n' "$svc" "$pid" \
    "$(grep '^CapBnd' /proc/$pid/status 2>/dev/null | awk '{print $2}')" \
    "$(grep '^NoNewPrivs' /proc/$pid/status 2>/dev/null | awk '{print $2}')"
done
```

- **Read it per service; never report a fleet from one result.** A partial outcome is the normal
  shape — one unit genuinely loses a capability the same run leaves on its neighbour. Report the
  count and name every unit still holding a dangerous bit, rather than "services hardened".
- **`MainPID` changing is the proof a restart happened.** A run that restarted four services and
  silently failed on the fifth leaves the *file* looking uniform and the fleet looking hardened.
- **An over-broad filesystem override is the one to check first.** A process holding it bypasses
  permission checks entirely, so `chmod` on a protected tree is *advisory for that process*.
  Permission hardening and capability hardening are separate controls, and only one of them is
  visible in the file you just edited — the other lives in `/proc`.
- The file's contents are DECLARED; the kernel mask is the enforcement. A config diff can never
  substitute for reading process state, and an audit that compares config against doctrine without
  reading `/proc` is only measuring its own documents.

## Reading config, env, and tokens safely

These files carry secrets, and **anything printed to stdout is persisted** — into the
transcript, the session message store, and tool caches. It cannot be un-published.
Never `cat` a whole config. Grep names; mask values:

```bash
grep -c '^KEY=' /path/.env
python3 -c "import json;d=json.load(open('/path/cfg'));print({k:'<set>' if v else '<unset>' for k,v in d.items()})"
grep -oE '\"[A-Za-z_]*(token|secret|password|key)[A-Za-z_]*\":' /path/cfg   # names only
```

If a secret escapes: **rotate the credential**. Scrubbing an audit log is not a fix.
An unused credential is latent exposure; one in use is live.

## Treating a peer's finding as evidence

Two agents agreeing is not two witnesses. If both read the same artifact, that is
**one source seen twice** — it launders a false claim into apparent consensus. Real
corroboration needs readings from *different* evidence: different tool, different node,
different measurement.

Before calling a peer's claim corroborated, ask whether they observed an independent
signal or merely read your output. Agent memory files, quoted logs, and paraphrases are
echoes, not witnesses. Check the peer's finding against the source before carrying it
forward — a peer's confidence is not verification.

## Reversibility

State the rollback before the change: a config toggle plus restart, or a named backup
file. If there is no rollback path, it is a different class of action and needs
authority before it starts.

For a live database, snapshot with the engine's own tool — `sqlite3 <db> ".backup <db>.bak-<ts>"`;
a `cp` can capture a torn WAL and restore a corrupt ledger. Then record the pre-change count,
apply, read the post-change count, and read it once more a minute later: an unchanged count is
what proves the writer is not re-creating what you removed. A single read straight after the
delete cannot tell "fixed" from "the writer has not run yet".

## Mutations that look like they worked (measured 2026-09-17)

Four failure modes, all observed on this box in one session. Each one reports SUCCESS.

**1. An immutable path refuses the write, by design — check `lsattr`, not permissions.** A write
returned `EPERM` as root. The cause was the **immutable** attribute, not an ACL or a mode:

```bash
lsattr -d <dir>      # ----i------I--e-------  ← 'i' = immutable, even root cannot write inside
```

`/root/AAA/governance` carries it; `/root/AAA/canon` and `/root/AAA/instructions` do not. So the
correct response to "this edit will not land" is to check the flag **and then route the edit
elsewhere** — reporting locked debt, not clearing the flag. Clearing `i` to make your own edit land
inverts the authority order the flag exists to enforce; that is a governance mutation, and it needs
the authority any other protected write needs. Say `BLOCKED_AT_GATE` and name the exact operation.

**2. A partial apply reports like a complete one.** A multi-item edit wrote 5 of 8 planned changes,
aborted on the one immutable target, and the re-run reported the remainder as *"already applied"* —
which reads as success. **Isolate every operation in its own try/except** so one refusal cannot
abort the batch, and report **`applied / skipped / failed` as three separate numbers**, then compare
them against the dry-run plan you built the change from. A mismatch between plan and apply is a
failed run, not a partial success. If the tool only has one summary number, it has no test.

**3. A backup written beside its source becomes input to whatever scans that tree.** Two runs left
`.bak-<ts>` files inside scanned trees; the next census counted them as objects (one registered as a
dead internal pointer). Write backups to a directory **outside every scanned root** and record the
inverse operation (`mv <dest> <src>`) in a manifest. Note the exception rather than generalising the
hazard: systemd does **not** load `.bak` unit files (measured: 13 sibling `.bak`/`.disabled` files sit
in `/etc/systemd/system` and **0** appear in `systemctl list-unit-files --all`), so
`/etc/systemd/system` is the case where a sibling backup is provably inert — a scanned data/skills
tree is not.

**4. Reading a property off a path that is a symlink reads the WRONG object.** `stat`/`ls -ld` on a
symlink reports the link's own mode — always `777`, meaningless — not the target's:

```bash
namei -l <path>                                  # shows the link and the real target, component by component
stat -c '%i %a %U %n' <path> "$(readlink -f <path>)"   # compare the two, do not read one
```

Measured: a permissions report was issued to the principal from `stat` on a symlink (`777 root:root`)
while the actual target was `750`, owned by a service account. The number was not wrong, the object
was. This is the same defect class as *DECLARED vs enforced* above: before reading any property from
a path, resolve it and say which object you measured.

**And one that is not about the system at all — never write the claim before the measurement
returns.** A commit message asserted "VERIFIED" for a census that was still running; it was corrected
in a follow-up commit when the scoped count disagreed. A long-running probe that outlives your call
(a backgrounded scan, a `sleep`-then-read pattern) is not evidence until it has exited. Write the
claim from the returned output, or label it `RUNNING / unverified`.


---
*DITEMPA BUKAN DIBERI*
