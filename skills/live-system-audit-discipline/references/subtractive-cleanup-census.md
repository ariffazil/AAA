# Subtractive Cleanup Census — build the removal map before removing anything

> Asked to make a live host smaller, simpler, cheaper, or "less entropy". The deliverable of the
> first pass is a **removal map**, not a removal. Everything here is read-only until authority,
> rollback and canary criteria are satisfied.
>
> Governing inversions — memorise these, they are the whole job:
> `UNKNOWN ≠ UNUSED` · `OLD ≠ USELESS` · `DUPLICATE-LOOKING ≠ DUPLICATE` ·
> `UNREFERENCED ≠ SAFE TO DELETE`. Prefer `DELETE > DUPLICATE`, `MERGE > PARALLEL`,
> `CANONICALIZE > FORK`, `QUARANTINE > UNCERTAIN DELETION`, `ARCHIVE > POLLUTE RUNTIME`.
>
> And the two protected absolutes: **never delete evidence to make the system look cleaner**, and
> **a clean system is not an empty system**. Optimise minimal *necessary* complexity, never minimal
> file count.

---

## 0. State the mode before you start

Write `OBSERVE_ONLY` at the top of the output and say so in the first line to the human. If the
session's own identity is unverified (no cryptographically verified actor, a session-token
mismatch, `authority_state = OBSERVE_ONLY`), then **the whole pass is discovery and classification**,
and that is a complete deliverable on its own — not a partial one. Do not partially execute because
it feels like progress. An unverified session that deletes is the exact failure the doctrine exists
to prevent.

---

## 1. The probe set

Batch these; they are independent. Record the timestamp once and stamp the whole report with it.

**Machine floor**
```bash
date '+%Y-%m-%d %H:%M:%S %Z %z'; uptime; free -h; df -h /; df -i /
```

**Port → owning unit** (a port with no owner is the P0 phantom; the reverse — every port owned —
is a clean negative worth publishing)
```bash
for p in $(ss -tlnH | awk '{print $4}' | sed 's/.*://' | sort -un); do
  pid=$(ss -tlnpH | awk -v P=":$p" '$4 ~ P {match($0,/pid=([0-9]+)/,m); print m[1]; exit}')
  [ -z "$pid" ] && continue
  unit=$(systemctl status "$pid" 2>/dev/null | head -1 | sed 's/^[● ]*//' | awk '{print $1}')
  printf "%-6s %-16s %s\n" "$p" "$(cat /proc/$pid/comm)" "${unit:-NO_UNIT}"
 done
```
A `NO_UNIT` verdict on every port is almost always wrong — the listener is usually `tailscaled`
fronting a loopback service, or a container's `docker-proxy`. Resolve the real process before
reporting an orphan.

**Service inventory — three lists, not one**
```bash
systemctl list-units --type=service --state=running --no-pager --no-legend | wc -l
systemctl list-unit-files --state=enabled|disabled|static --no-pager --no-legend   # three separate runs
systemctl list-units --type=service --state=failed --no-pager --no-legend
```
**Enabled is intent; active is reality.** The informative cell is a unit that is `enabled` and NOT
`active`, or `disabled` but reachable through a *timer* — list the timers, then cross-reference. A
disabled service whose timer is enabled and active is a live component wearing a disabled label;
conversely a service with no timer that is inactive is dead intent worth proposing for retirement.

**Orphan detection by missing binary** — catches phantom units that every other probe reports healthy
```bash
for u in $(systemctl list-unit-files --type=service --no-pager --no-legend | awk '{print $1}'); do
  ex=$(systemctl cat "$u" 2>/dev/null | grep -m1 '^ExecStart=' | sed 's/^ExecStart=//;s/^[-@+!]*//' | awk '{print $1}')
  case "$ex" in /*) [ -e "$ex" ] || echo "MISSING_EXEC  $u -> $ex";; esac
done
```
Ignore the distro's own units (`quotaon`, `rc-local`, `lxd-agent`, `sshd-keygen`). The finding is a
*federation* unit whose interpreter or binary has been deleted — the unit file survives as a claim
about something that no longer exists.

**Repo dirt sweep**
```bash
for d in /root/*/; do
  [ -e "$d/.git" ] || continue
  printf "%s | %s | dirty=%s | ahead=%s | %s\n" "$(basename $d)" \
    "$(git -C $d rev-parse --abbrev-ref HEAD 2>/dev/null)" \
    "$(git -C $d status --porcelain 2>/dev/null | wc -l)" \
    "$(git -C $d rev-list --count @{u}..HEAD 2>/dev/null || echo -)" \
    "$(git -C $d log -1 --format=%cs 2>/dev/null)"
done
```
Also list the top-level directories that are **not** repos — those are where the scratch, artifact and
near-duplicate trees live, and they are where the merge candidates are.

**Resource attribution — find the actual consumer**
```bash
du -sh /root/*/ | sort -rh | head -40          # but see §5 before believing a zero
du -sh /root/.cache/*/ /root/.arifos/*/ | sort -rh
docker system df
journalctl --disk-usage
find /root -maxdepth 5 -type d -name node_modules -exec du -sh {} + | sort -rh
find /root -maxdepth 4 -type d \( -name .venv -o -name venv \) -exec du -sh {} + | sort -rh
```

**Interactive-session memory** — see §6. This is where a "memory leak" usually is not.

---

## 2. Disposition buckets — exactly one per candidate

| Bucket | Test |
|---|---|
| **KEEP** | unique, used, healthy, owned, necessary |
| **CANONICALIZE** | several implementations exist, one should become authoritative |
| **MERGE** | two components genuinely overlap in function |
| **DEPRECATE** | still called today, must leave the active architecture |
| **QUARANTINE** | suspected unnecessary, evidence insufficient for destruction |
| **ARCHIVE** | provenance-valuable, unnecessary in active runtime |
| **DELETE** | proven redundant/dead **and** recoverable |
| **UNKNOWN** | cannot yet classify honestly — this is a valid answer, use it |

`UNKNOWN` is not a failure to decide. It is the honest bucket, and it is what stops an uncertain
candidate from being quietly promoted to DELETE by a later reader.

---

## 3. Protected by default — never propose these for deletion

Immutable audit / ledger / vault chains · witness evidence · historical outcome records · scar and
correction records · authority policy and canon · cryptographic identity material · recovery and
backup artifacts · human-owned data · unique raw observations · canonical schemas · currently
required secrets. Produce a reclaim figure **excluding** these, so the number cannot be met by
raiding them.

---

## 4. Order of operations, and the batch rule

`P0` externally exposed phantom state → `P1` contradictory runtime/config → `P2` duplicate authority
or ambiguous canonical ownership → `P3` dead services/agents/jobs → `P4` compatibility shims and stale
aliases → `P5` duplicate code/schemas/packages → `P6` stale open loops → `P7` stale docs/generated
clutter/caches → `P8` cosmetics.

**Never start at P8 while structural entropy remains.** A cosmetics pass on a system with a phantom
externally-reachable surface is negative work: it consumes the attention budget that the real finding
needed.

**Batch small, canary each batch, then proceed.** Do not delete a hundred things and test once. A
sensible batch is one class (all regenerable build artifacts), followed by: organ health, MCP tool
listing, one real tool invocation, authority-gate probe, witness path, memory path, public endpoints,
rollback path. Compare before/after and require `complexity ↓` with `capability unchanged`.

**Every removal gets a tombstone** — component, former purpose, why removed, evidence, replacement
owner, dependencies checked, removal time, commit/hash, rollback path, canary result. Deletion without
negative knowledge guarantees recurrence, because the next agent re-derives the same idea from the
same gap. Maintain the reverse index too: removed components, superseded schemas, canonical
replacements.

---

## 5. False positives that make a "safe to delete" list wrong

Each of these has already produced a real erroneous entry in this class of work.

1. **A `du` zero on a symlinked directory.** The path resolves to a live store several GB deep.
   `ls -la` / `readlink` the candidate before believing any size tool. An `l` in the mode column
   means you measured the link.
2. **Two trees of equal size that are one tree.** Hardlinked pairs also report equal *apparent*
   size. Measure together (`du -sc A B | tail -1`), compare inode sets, count `-links 1` files. A
   "12 GB of duplication" can be 6 GB of deliberate deduplication.
3. **A big directory assumed to be waste.** Large ≠ waste. Attribute every large path to a live
   consumer (service `WorkingDirectory`, `ExecStart` argv, a container mount) before calling it
   reclaimable; an unattributed big directory is `UNKNOWN`, not DELETE.
4. **A detached-HEAD worktree or a `.git`-less directory assumed to be scratch.** Verify against
   `git worktree list` and the service unit's working directory first.
5. **A near-duplicate directory name taken at face value.** Case-only pairs on a case-sensitive
   filesystem (`x` / `X`), and typo twins, are *not* the same tree — they are two trees, at least one
   of which is being read by something. They are the highest-value MERGE candidates **and** silent
   wrong-path hazards. Confirm which one the caller resolves before merging.
6. **An upstream clone that looks like a fork.** `ahead=N` in the thousands against a public remote
   means a vendored/upstream copy, not your divergence. Do not "sync" it, and do not treat its size
   as reclaimable without checking whether anything reads it.
7. **Multiplicity that is a secrets question, not a files question.** Several copies of the same
   credential file, all plaintext, all differing slightly, is an F13-class decision about retention
   and rotation — never an agent's cleanup item, and never summarised as "N duplicate files".
8. **Exit status read as health.** A unit that is `enabled` and exits non-zero on every start is not
   a working service; it is a claim with no process behind it.

---

## 6. Resource pressure: attribute before you diagnose

**When RAM is the finding, check interactive session scopes before hunting a service leak.**
```bash
systemctl list-units 'session-*.scope' --no-pager --no-legend
for s in $(systemctl list-units 'session-*.scope' --no-pager --no-legend | awk '{print $1}'); do
  tot=$(systemctl show -p MemoryCurrent --value "$s"); [ -z "$tot" ] && continue
  printf "%8.0f MB  %s\n" "$(echo "$tot/1048576"|bc -l)" "$s"
done | sort -rn
loginctl list-sessions --no-legend
```
On a host that runs several agent CLIs, a long-lived editor/agent session can hold more RSS than
every daemon combined, and the abandoned-scope case (`abandoned` but still holding ports) is a
recurring one. Also read the swap holders before concluding anything:
`awk '/^Name:/{n=$2}/^VmSwap:/{if($2>10000) printf "%-20s %8.1f MB\n", n, $2/1024}' /proc/*/status`.

**One sample is not a trend.** Do not call it a leak on a single reading. State the measurement you
would need — RSS slope per scope over 24 h, OOM events, swap-in/out, restart correlation — and say
explicitly that the leak hypothesis is **not yet supported**. An unsupported leak claim triggers a
restart cascade that costs far more than the pressure it was meant to relieve.

---

## 7. Reading a loop / task / carry-forward store

- **Read the schema before you filter on a field name.** Entry-kind fields are frequently named
  `kind`, not `type`; filtering the wrong key returns an empty set that looks exactly like a clean
  system and will be reported as "no open items". Print one entry's keys first, then aggregate.
- **The store may be a symlink** into a versioned location, with a generational schema and a
  `writers` / `succeeded_by` block. Resolve the real file; a stale copy of the same filename can exist
  in a second directory and be caught by neither reader nor writer.
- **Classify, then propose — do not close during a census.** Buckets that work: still-active →
  blocked-awaiting-authority → carries-a-resolution-marker → stale → explicitly superseded.
  Automated classification here is a **triage aid, never a verdict**; say so, because marker words
  inside unresolved entries produce false "resolved" hits.
- **Find the shared blocker before counting the items.** When a large fraction of open items are
  each waiting on the *same* external decision, they are one queue, not N problems — and collapsing
  them into a single decision request is the largest reduction available at zero information cost.
  Report both the raw count and the collapsed count.
- **A task list is not institutional memory.** Closing, merging or superseding a loop is a **state
  transition, not a delete**: preserve the historical receipt, remove the item from active attention,
  and record the supersession chain. Never make the count go down by destroying the record of why.
- **A closed loop with no owner, next action or deadline will reopen.** If the schema has no such
  fields, adding them is a higher-value change than closing anything — otherwise the count is a
  ratchet and the next census re-derives the same list.
- **An empty queue or output file is a post-consumption state, not proof of idleness.** A store that
  reads empty during a census has usually been *drained*, not never filled — the drainer rewrote it to
  hold only what remained. Before reporting "no open items" or "the producer emits nothing", find the
  consumer's own execution log and bucket files: the trace of a produced-then-consumed item lives
  there, and the empty artifact is the one place it does not. This is the same false negative as
  filtering on the wrong key name, arriving by a different route, and it manufactures a defect
  ("the producer is broken") that one read of the consumer's log would have disproved.
- **Compute the fill rate against the drain ceiling before classifying a store as merely untidy.**
  Classification cannot fix a throughput deficit. Count items created per day over the store's
  window (group entries by their own timestamp) and compare against the drain mechanism's documented
  capacity — and treat that capacity as a *ceiling*, not a current rate, since guard-excluded items
  reduce it further. Measured shape: 8.71 items/day created against a hard cap of 3/day, so the
  count grew ~5.7/day **even with the drainer working perfectly**. That converts "nobody is closing
  loops" from a discipline complaint into arithmetic, and it is a far stronger finding than the raw
  count — report the two rates and their ratio, not the backlog size. Only after the arithmetic is
  presented does a proposal about *how* to close them become answerable.
- **Read why the drainer refused, not just that it did.** When a drain mechanism reports success
  with zero closures, check whether its terminal judgments persist a reason. Count `reasons_written /
  judgments_made` across the consumer's log: a mechanism holding a 100% verdict rate beside a 0%
  reason rate is the shape that loops forever, because nothing downstream can act on a refusal whose
  cause was never recorded. The audit method and its general form are in
  `learning-loop-verification` § *Conservation accounting*.

---

## 8. Authority boundary — what a census may never do

State this as a table in the output, because it is what makes the map actionable instead of alarming.

| Action | Needs |
|---|---|
| Remove regenerable caches, build artifacts, bytecode, log vacuum | low tier — executable after a canary |
| Remove or mask a systemd unit | mid tier + canary |
| Delete anything under a backup/restore root | **sovereign** — restore path must be proven first |
| Touch credential files, retention, rotation | **sovereign** — never an agent's call |
| Rewrite history, remove worktrees, force-push | **sovereign** — recovery floor must be proven |

**A backup may not be removed on age.** It is removable only after the replacement state is
verified, the restore path is *tested*, unique/uncommitted/unpushed work is checked, integrity is
recorded, and retention is satisfied. If the restore path cannot be exercised in-session (a repo with
an unretrievable password, a host you cannot mount), the bucket is `UNKNOWN` and the report says the
restore path is unproven — not that the backup is redundant.

---

## 9. Output shape

The report the human actually needs, in this order:

```
CLEANUP STATE: MAPPED · <mode> · <mutation or none>
CANDIDATES FOUND: <n>
  KEEP / CANONICALIZE / MERGE / DEPRECATE /
  QUARANTINE / ARCHIVE / DELETE / UNKNOWN   — each with a count
REMOVED ENTROPY: <n>            (0 for a read-only pass — say so, do not imply progress)
CAPABILITY LOST: <n>
NEW CONTRADICTIONS: <n>
RESOURCE DELTA: before → after
OPEN LOOPS BEFORE → AFTER:
EVIDENCE: <where each figure came from>
ROLLBACK: <or N/A — nothing changed>
CANARY:   <or N/A — nothing changed>
NEXT HIGHEST-VALUE SUBTRACTION: <ranked, 3 items>
HOLD: <what an agent may not touch, and why>
```

**Publish the clean negatives too.** "All N listeners have an owning unit", "zero failed units",
"zero unattributed processes" are findings of the same rank as the defects, and they are what stops
the next session re-probing the same ground. A census that reports only problems looks like a system
in crisis; the same census with its verified-clean sections is a map.

**Report the traps you escaped.** When a candidate was about to be listed as removable and a probe
retracted it, say so explicitly. It is the single most useful part of the report: it teaches the
reader which entries in the list are load-bearing and how they were distinguished — and it
demonstrates the map was built by measurement rather than by pattern-matching on names.

**Stop condition.** Stop when the remaining candidates each have an unproven restore path or sit
behind a sovereign decision. Say that plainly as the conclusion. "Nothing else can be safely removed
by an agent on this evidence" is a successful census, not an incomplete one.
