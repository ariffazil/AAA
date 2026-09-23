---
name: live-system-investigation
description: "Use when probing a running system to diagnose or attribute."
owner: Hermes
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# Live-System Investigation

Diagnosing a running system is a different discipline from fixing it. Four ways to
cause harm while "just looking":

1. leak a credential into output
2. mutate state you meant only to inspect
3. kill the process you are running inside
4. assert a global claim from one narrow probe

**Read-only means no writes AND no leaked reads.** Do (4) via
`assertion-window-discipline`; this skill covers (1)-(3) and the attribution workflow.

## 1. Redact by default — the investigator is the leak vector

The most common leak is not a badly stored secret. It is an **investigation command
that dumps config or env to stdout**, which then lands in agent context, terminal
caches, and the session message store.

Redact **structurally** — inside the command — never from memory or intent:

```bash
# WRONG — prints values
cat .env
tr '\0' '\n' < /proc/$PID/environ | grep '^KEY='
python3 -c "import json;print(json.load(open('cfg.json'))['peers'])"
diff old.json new.json                  # secrets ride in the diff body

# RIGHT — mask at source, keep only the shape you need
cut -d= -f1 .env                        # names only
for k in A B C; do tr '\0' '\n' < /proc/$PID/environ | grep -q "^$k=" && echo "$k SET" || echo "$k ABSENT"; done
tr '\0' '\n' < /proc/$PID/environ | sed 's/=.*/=<set>/' | grep '^KEY='
diff <(sed 's/=.*/=<redacted>/' a) <(sed 's/=.*/=<redacted>/' b)
```

Generic masker when the shape is unknown: `sed -E 's/[A-Za-z0-9_-]{24,}/<redacted>/g'`.

Print **existence, count, or length** — that is usually all the finding needs.
A boolean answers "is it configured?" without exposing the value.

**Scans are not exempt.** A search across many files that prints matched *lines* will
surface secrets from unrelated files. This bites hardest when you write a scanner for
something else (e.g. "find all cross-node mutations") and print raw command arguments
— the arguments themselves carry credentials. Filter to the field you asked about and
mask by default.

### If a secret reaches context: ROTATE, do not scrub

Log redaction is not remediation — the value persists in message stores and in every
context that received it. **Rotate the credential.** Where the exposed credential is
not yet wired to a service, generate a fresh one at wire time rather than reusing the
exposed value. Report plainly and without self-excusal: what was exposed, where it
landed, the rotation step, and who must action it.

## 2. Classify before you run — mutating commands masquerade as probes

Before touching live infrastructure, sort the command. These **mutate**:

| Looks like | Actually does |
|---|---|
| `diff a b` | prints secrets from both bodies |
| `docker ps -a --format ... {{.Size}}` | read-only; safe |
| `rm -rf <dir>`, `docker volume rm`, `docker system prune` | irreversible |
| `sed -i`, `>> file`, `cat > file` over ssh | writes on the **remote** host |
| `systemctl restart <unit>` | drops every session inside that unit |
| `swapoff -a && swapon -a` | forces memory pressure process-wide |

Config-change side effect worth knowing: many gateways **auto-restart on config
write** (a reload-drain-restart cycle). Editing config to "test" therefore restarts
the service, and anything mid-flight — including your own probe — sees a transient
outage. If a probe returns connection-refused while the unit is `active`, re-probe
before concluding anything: you may be inside a restart window you or a peer caused.

Prefer: dry-run flags, `--dry-run`, `-o BatchMode=yes`, read-only subcommands first.

**Check for an in-flight remediation before running one.** Peer lanes share the host; a
second run of the same mutating command double-applies or races the first. Grep for the
exact command string, not a keyword:
```bash
ps -eo pid,etime,args | grep -F 'swapoff -a' | grep -v grep
```
Finding it already running **is** the answer: identify who started it (walk the parent
chain, §4), let it finish, and report that instead of "helping". A fix that lands
twice is worse than a fix that lands late.

## 3. Never restart the process you are running inside

If your session lives inside the target unit (a gateway hosting agent sessions), a
restart kills you and every sibling session mid-task.

**Config staging is safe. Activation is the risky step** — separate them, and treat
opening a new listener/bind as an authority decision, not a config edit.

Detached restart that survives its own kill:
```bash
systemd-run --on-active=60 systemctl restart <unit>
```
Do NOT use `nohup`/`&` from inside the process tree — that dies with it.
Before restarting a shared gateway, enumerate what dies:
```bash
GW=$(systemctl show <unit> -p MainPID --value)
ps -eo pid,ppid,cmd | awk -v g="$GW" '$2==g'
```
A restart of a multi-session gateway is a **coordination event**, not a config reload.

## 4. Attribution: "who changed this?"

Never answer "I cannot determine who" before sweeping every session record — and never
answer with your own session's log alone. Full technique:
[`references/writer-provenance.md`](references/writer-provenance.md).

Short form, in order:
1. Sweep **all** sessions by timestamp window, not session-scoped.
2. Look for a `.bak`/backup file whose mtime brackets the change — batch backups
   within the same second indicate a scripted edit, not a manual one.
3. Trace the process tree of any live agent process to its parent (`/proc/<pid>`,
   `ps -o ppid`) to identify its terminal and origin.
4. Check for concurrent writers **before** publishing a causal claim; a sibling
   session can invalidate your diagnosis mid-flight.
5. **Bind the claim to a hostname before comparing it to another host's numbers.** A
   report about "the machine" can silently merge two hosts — a no-op that is honest on
   a box with no swap configured is a false acquittal when applied to a box with 8 GB
   of it. Probe each node separately and print its identity beside the numbers
   (`ssh <node> 'hostname; free -m; swapon --show; grep swap /etc/fstab'`).
6. **For a mutation that already reverted, read the sampling witness series, not the
   current state.** A swapoff/swapon cycle looks perfectly normal minutes later. The
   telemetry tick and the OOM-watcher log carry the time series; a swap capacity that
   reads 8191 → 3934 → 8191 MB proves a swapfile was removed and re-added. Detail and
   commands: `references/writer-provenance.md` §7–8.

**A name is not an identity — check the author, not the label.** Attribution and
independence share one failure shape: two records with different labels can have the
same origin. Two modules with different producer ids, written by one hand in one
session, are **one author**; a verdict from the second is not an independent witness of
the first. Before recording anything as independently verified, ask *is the verifier a
different author, or the same hand with a second name?* — and put the answer in the
artifact, not just in the transcript. No tool call, credential, or elapsed time closes
this gap; only a genuinely different actor does.

## 5. Verify the artifact, not its existence

- Confirm the target file/field exists **on the node you are editing** before a
  line-level fix — homonyms on another host cause most wrong-layer errors.
- A backup you **cannot open** is not a backup. Verify restore, not presence: if the
  repo/archive exists but no credential can read it, record that as an open risk.
- A log that has stopped receiving entries is not evidence of absence. Compare
  `tail -1 <log>` timestamp against now; check the journal instead.

### The silent-zero class: instrument dead while reporting healthy

Every bullet above is one instance of the same pattern. Generalise it:

> A **zero / empty / `NO_CHANGE` / `OK`** is a claim about the world, and it is
> indistinguishable from an instrument that is structurally incapable of reporting
> anything else. The output alone never separates them, and the second case is the
> expensive one.

**Before reporting zero, prove the instrument CAN return non-zero** — feed it a known
non-empty input (a record you can see on disk, a search with the threshold set to match
anything, a call you make by hand). If it still returns empty, you have found a dead
instrument, not a clean state. Report **UNMEASURABLE**, not zero.

Three doors seen in one session, each with the check that catches it:

| Door | Symptom | Check |
|---|---|---|
| **Registered but not served** | The tool/route appears in the listing; the actual call is rejected by a *separate* gate (whitelist, session, scope). Health endpoint stays green throughout. | Call it. Registration, listing, and service are three independent gates — a listing proves only the first two. |
| **Field-name drift** | The reader reads `<field>A`, the writer emits `<field>B`. The window is structurally empty forever and the status still says OK. | Print one stored record's **raw keys**, then grep the reader for the key it actually reads. Mismatch = structural zero. |
| **Silent no-op** | Work is produced, then dropped by a resolver that cannot name its target. The queue is non-empty and never drains. | Count what came OUT against what went in. A recurring identical rejection in a log is a dead job, not stability. |

**Corollaries:**
- **Report an unreadable measurement as an ERROR, never as `None`/absent.** A field that
  silently returns nothing is indistinguishable downstream from one that says zero — the
  exact ambiguity this section exists to remove.
- **A repeated identical rejection is a dead job.** Same rejection every run for days =
  the ingest cannot resolve its target. Fix the resolver, then dead-letter the rejections
  out of the scan path so they are not re-attempted forever.
- **Calibration is part of the reading.** An instrument whose own self-test record is
  days stale is reporting history, not state. Check the calibration timestamp whenever
  the instrument exposes one.

**Why this outranks an ordinary fault:** an instrument that says "I am dead" gets fixed.
An instrument that says "all clear" is consumed as evidence — every inference built on it
inherits the false negative, and nothing in the output ever contradicts it.

### The inverse shape: a failing probe can be an identity artifact

The silent-zero class is a green instrument that is blind. Its twin is a **red probe
that is right about the wrong thing**. A readiness endpoint can FAIL while the service
is healthy because the probe ran unauthenticated: anonymous actor → constitutional
HOLD (L02/L03/L04) → `OBSERVE_ONLY`, `can_mutate: false`. The kernel is working, not
failing.

Before declaring a service down from a red probe, read the probe's **own** actor field
and reasons. `execution_state: BLOCKED` + `actor: anonymous` + `band: OBSERVE_ONLY` +
`reasons: ["Constitutional HOLD: L02, L03, L04"]` is an auth finding. Report it as
"readiness probe unauthenticated", never as "service degraded" — and never quote a green
`/health` next to a red `/ready` without saying which gate each one measures.

### The loud-always class: an instrument that fires every tick may be working as designed

Companion to the silent-zero class is the **always-loud** class. Drift watches, governance
sweeps, constitutional guards — detectors that accumulate `failure_streak`, exit non-zero
on every tick, and refuse to self-heal — are **intentionally loud**. They exist to force a
human to look, not to auto-resolve. Killing them or patching the failure out converts a
working accountability surface into a silent one.

Before classifying a repeated alarm as a defect, read the script body for its own
self-asserted design contract. The contract is almost always in the message the script
prints on its way to exit 1 — a line like `delete the baseline to re-establish after review`
or `until a human acknowledges`. If that contract is present, the workflow is:

1. **Acknowledge** the finding (read the drift, verify it is real, not a re-fire of an old finding).
2. **Reset the baseline** if the drift was benign (`rm <state-file>`; next tick establishes new baseline).
3. **Patch the producer** if the drift is real but expected (write the source-of-truth
   that should have been authoritative in the first place, so the watcher has nothing to
   flag).

Never do step 3 before step 1. Never do step 2 before step 1. And never replace a
working loud watchdog with a quiet one to silence the noise — the noise is the point.

## Reporting shape

- Lead with what is **verified** and the command that verified it.
- Mark **UNKNOWN** explicitly rather than implying it.
- State the scope qualifier in the claim (node, session, time window).
- **Scope by dimension too.** Verifying one class of change does not license a
  whole-domain claim: "no deletions on that host" is not "that host was untouched" —
  remote config overwrites and service restarts count in the same blast radius.
  Overstating in the safe direction is still overstating.
- Own your own errors plainly and correct them in place — do not append a hedge.
- If the answer is "nothing to do", say so; activity is not progress.

For the full pre-assertion gate (process / window / log / scope) and the procedure
before any negative claim, see the `assertion-window-discipline` skill.

---
*Distilled from a multi-hour live-infra session where the most serious harm came from
investigation commands, not from the faults being investigated.*
*DITEMPA BUKAN DIBERI*
