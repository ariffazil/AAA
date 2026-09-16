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

## Read the health body, not the status word

`status: degraded` is not a synonym for "the process is broken". Organs report degradation
for **data age** as well as for faults, so read the sub-objects before you touch anything:

```bash
curl -s http://127.0.0.1:<port>/health | python3 -c "
import sys, json; d = json.load(sys.stdin)
print({k: d.get(k) for k in ('status', 'truth_status')})
print(d.get('freshness'))
print({k: v for k, v in d.items() if 'degrad' in k.lower() or 'reason' in k.lower()})
"
```

- `freshness.status: expired` or a large `state_age_hours` is **data staleness, not a service
  fault**. A restart does not fix it and destroys the evidence; the fix is a fresh write from
  whoever owns the data.
- 401/403 on a health endpoint means the service is **up** and auth-gated. Only
  connection-refused and timeout are DOWN.
- A stale *snapshot file* is not a health signal, and a scheduled job told to read one instead
  of probing live will keep reporting old state indefinitely. When a job's output looks wrong,
  check what it was told to read before you check the service.

## Prefer the smallest change inside the mechanism already running

When the defect is one condition or one call site, extend what already exists rather than
adding a parallel thing — a new framework, a new state file, a new metric store all have to
be understood, refreshed and eventually removed by whoever reads the system next. The test:
could this be a field on a record the system already writes? Then it is a field, not a
subsystem.

Corollary — **every new piece of state must declare its lifetime where it is defined.** A
counter that resets per session must not be named or described as a repetition metric; the
next reader assumes the persistence the name implies and draws a conclusion from a number
that cannot see what it claims to measure. If the durable version of the same fact is already
recorded somewhere else, say so in the comment and point at it.

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

---
*DITEMPA BUKAN DIBERI*
