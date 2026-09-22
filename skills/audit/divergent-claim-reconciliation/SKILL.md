---
name: divergent-claim-reconciliation
description: "Reconcile observers who disagree about system state."
owner: Hermes
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Divergent Claim Reconciliation

When two observers report incompatible facts about the same system, the resolution is rarely
"one of them lied". It is usually that the observers held different **vantages** — different
hosts, different surfaces, or different time windows — and each reported its own root correctly.

## Core law

**Every claim carries an implicit vantage. Name it before you weigh it.**

A claim without a stated vantage is a rumor. That applies to denials exactly as much as to
assertions: "it does not exist", "that artifact is fabricated", "N of M are false" all require
the same host-pinning as the positive claim they refute.

## Step 1 — Pin the vantage of every claimant

Write down, for each side: **host + node role + surface + time window.**

- A peer probing a read-only mirror is describing the mirror, not the origin.
- A peer that has itself established the topology ("my checkout is stale") must apply that fact
  to its own readings. Knowing the map does not exempt you from it.
- Name your own seat too. "Which machine am I on?" is the first question, not an assumption.

**Do not upgrade absence to falsification.** "I cannot see it from here" and "it was never
written" are different claims with different evidence requirements. An observer that finds
nothing on its own seat has produced a *finding about its seat*, not a verdict on the artifact.

**A point-for-point inversion is the signature of a different host, not of a liar or a stale
reader.** When a peer's readings contradict yours on *every* axis at once — different HEAD, different
branch, opposite dirty count, a commit that is a valid object for you and "not a valid object" for
them, the symbol present in your tree and absent from theirs — stop reconciling the facts and
exchange host identity first (`hostname`, tailscale IP, machine-id, repo path). Distributed estates
make this common, and each side's report is usually a correct description of its own machine.
Collect both locks in one message rather than trading findings for several rounds; the contradiction
is often the most valuable artifact either observer produced.

**Retract your own paradox in the same breath you find it.** If you announced an impossible
ordering ("the process started before the artifact it runs was built") and then discover you read
the wrong process, say so plainly and name the misread. A self-found error left standing becomes the
next reader's premise, and the correction is worth more than the original finding.

**The process dimension of a vantage.** Host, surface and window are the obvious axes; a fourth is
*whose context* the reading was taken in. A service's own health field is computed with the process's
cwd, user and config — so re-take it there before calling the service a liar:

```bash
PID=$(systemctl show <svc> -p MainPID --value)
readlink /proc/$PID/cwd          # the directory it actually runs in
ps -o user= -p $PID              # the user it actually runs as
sudo -u <that-user> <the command the service runs>
```

Measured: a service reporting a dirty working tree looked like a contradiction against a clean repo
until the same `git status` ran as the service's own user, which returned an untracked path the root
user's config excludes. Two vantages, one repo, no defect. A user-level ignore rule is a vantage.

## Step 2 — Enumerate surfaces before choosing a cause

A client reporting missing capabilities has one of three causes. Each has a different fix.

| Cause | Tell | Fix |
|---|---|---|
| Client cache | Names absent from the live surface; present only in the client's own cached list | Client reconnects / refreshes |
| Connector stale config | Names absent from the live surface; connector config carries them | Patch the connector |
| Server-side split brain | Two **live** surfaces on the **same** host report different facts | Reconcile the server's own surfaces — canon territory |

The third cause is the one static inventories miss, because every surface looks authoritative.
Probe each surface directly on the host and compare pairwise.

**Two live surfaces on one host disagreeing is a real defect.** Cache explains a *client*
diverging; it does not explain a *server contradicting itself*. A stale peer explains a second
*host* diverging; it does not explain two endpoints of one process disagreeing.

## Step 3 — Check your own probe before reporting a defect

A probe returning a schema or argument error is not a tool defect until your call matches the
tool's declared schema. Read the schema, retry once with the documented shape, then report.

**Why:** a self-inflicted bad argument reported as a broken tool sends the next session
patching healthy code, burning budget on an invented fault.

### Check the clock as well as the call shape

A reading is a claim with a timestamp. Before filing a divergence, check whether the fix landed
*after* the reading that reports the problem: compare a monitor's `last_run_at` against the mtime of
the artefact it guards. An error from an earlier run is stale, not live. And state moves *inside* a
session — an upgrade, a restart, another writer's commit — so re-probe immediately before any
irreversible action; a reading that was true when taken can be false by the time it is acted on.

### Normalise the timezone before comparing any two timestamps

Filesystem mtimes are system-local; journal lines, ledger timestamps and a peer's report are usually
UTC. Comparing them raw builds a timeline that is wrong by the host's offset — and on a UTC+8 host an
event at `00:38` local is `16:38` the *previous* UTC day, so the error crosses a date boundary and a
search of "today" finds nothing.

- Print both readings side by side (`stat -c %y` and `TZ=UTC stat -c %y`) before ordering events.
- Bound every query window (`--since/--until`, `find -newermt`, journal ranges) in the **same zone as
  the records it searches**, not the zone of the host you are typing on.
- State the window's zone in the finding. A peer on another host re-derives it wrong in the opposite
  direction, and then the disagreement is about the offset rather than about the facts.

**Why it belongs in reconciliation specifically:** a timezone slip is indistinguishable from a vantage
difference. Two observers reporting the same edit at different hours look like they read different
artefacts; resolving that as a host mismatch sends both sides hunting a divergence that was never there.

### A provenance void is a finding, not a prompt to guess

When a change bypassed the VCS (raw filesystem write, no commit), the usual actor records are
legitimately absent: the reflog stops at the last commit, and receipts in the window may carry an
anonymous or missing actor field. Sweep the lanes that could still hold it — build and process logs,
receipt ledgers bounded to the window, deploy receipts, session ledgers — then **report the void with
the lanes searched**.

Never fill it with the most plausible actor in the neighbourhood. An unattributed capability live on a
surface is a governance gap in its own right, and a guessed attribution becomes the next reader's
premise — the same defect as upgrading absence to falsification, with an invented name attached.

Distinguish two voids explicitly, because they have different owners and different fixes:

| Void | Means | Fix belongs to |
|---|---|---|
| Receipt exists, actor field empty | the ledger did not capture identity | whoever writes the receipt |
| No receipt in the window at all | nothing recorded the change | whoever owns the mutation path |

### Read the reason field before declaring an entry dead

A `disabled` / `paused` / `skipped` entry is not a corpse. Its reason field routinely names a
successor, a migration target, or the directive that retired it — the record of *why*. Deleting it
deletes the explanation. If the clutter is the real complaint, fix the **listing**, not the record.

## Step 4 — Check the axes before calling something a paradox

Before reporting a contradiction, confirm the two readings measure the same axis. An artifact
chain (source → build → deployed) and a governance gate can both be correct simultaneously.

**Why:** a false paradox sends the next session hunting a non-existent bug, and both the audit
and the system get blamed for a misreading.

## Step 5 — Open a composite FAIL to its per-item breakdown

A gate reporting a single boolean FAIL names no cause. Call the verifier directly, in the
**deployed** environment, and read its per-item table. The items name the failing checks.

Composite checks are commonly file-existence or credential-presence probes. Separate two
failure classes:

- **Candidate path gone** — the check's target was deleted or moved. One deletion degrades
  every surface still pointing at it, which is why a single deletion can look like three
  separate defects.
- **Cannot pass by construction** — a success path gated on something the caller never
  supplies. Permanently failing, and it needs a different fix from a missing file.

Also watch for a candidate that can never satisfy its own probe: a path that is now a
*directory* checked with a file-open, silently swallowed by a broad `except`.

## Step 6 — Weight by doctrine recency, not code age

When surfaces disagree, check which one agrees with the most recently ratified doctrine before
assuming the code is correct. Newer ratified doctrine is the better candidate for authoritative.

**Report the weight of evidence; leave the ratification call to the human.** Reconciling a
canonical value is a governance change, not an audit action — do not self-patch it.

## Step 7 — Retraction replaces, it does not soften

When the divergence resolves, the next message must carry the **new** state. Hedging
("confidence downgraded", "likely also false") while the old claim stays in the record leaves
readers holding the pre-correction belief. Void means remove.

Record the vantage lesson in the retraction. The divergence itself is often the strongest
evidence the session produces, because it demonstrates (or refutes) the very property the
system claims to have.

## Always-on rules

- Every claim and every denial carries `scope: host + role + surface + window`.
- Normalise timestamps to one zone before ordering events; an offset slip masquerades as a vantage
  difference.
- A self-report is computed in the reporter's own context; reproduce it there (cwd, user) before
  calling it a contradiction.
- A reading carries a timestamp; an error older than the fix is stale, and state can move mid-session.
- Read an entry's reason field before declaring it dead — a paused-with-reason entry is a tombstone,
  not a corpse.
- Report a provenance void with the lanes searched; never supply the most plausible actor.
- Presence needs one surface; a true absence needs all of them.
- Check your own call shape before declaring a tool broken.
- Two live surfaces on one host disagreeing = real defect, not cache.
- Confirm shared axes before reporting a paradox.
- Open composite FAILs to per-item breakdown; separate "gone" from "cannot pass".
- Weight by doctrine recency; escalate canon reconciliation to the human.

## Step 8 — Resist the collapse (the meta-skill)

Reconciliation has its own failure mode: the resolver builds a story from the reconciled evidence
and then forgets it is a story. Four collapses recur.

**n=2 is not a class.** Two instances that look similar are usually either one instance read twice
or two instances that diverge on inspection. The label "systematic", "class of defect", "pattern
across N surfaces" requires the third, fourth and fifth instances to have been examined, with their
own vantages pinned — not just the first two that confirmed your working hypothesis. When you feel
the sentence "this is now a pattern" forming, count: how many independent vantage-pinned observations
have I made? If the answer is two, the correct sentence is "two observations, unresolved as to
whether they share a cause." A pattern emerges at n≥3 with vantages confirmed; before that, the
honest finding is "twice".

**Do not label a peer's observation in language they did not use.** When a peer reports "the
gate has teeth on stateless-client", that is one observation about one actor class on one gate.
Translating it into "fail-closed is empirically true" elevates a specific finding into a doctrine
claim the peer did not make, and the peer will — correctly — retract *your* sentence, not theirs.
Keep the language the peer used. If you need a higher-order summary, mark it as your own
interpretation with a vantage note: "I am extending the peer's observation into the following
claim; the peer has not endorsed this extension."

**Host before lane.** "X owns this lane" requires X to have an execution path on the runtime,
not just a thinking path. A peer with source-tree access on host A but no deploy access to the
runtime on host B can write a patch but cannot land it. Naming such a peer as "the owner of the
lane" sets the human up to wait for delivery that the lane cannot provide. Before assigning lane
ownership, confirm the peer's vantage includes the runtime host — and if it does not, name both
the peer's actual lane (patch preparation at A) and the lane that *is* needed (deploy at B).

**Audit the retraction before sending it.** A self-correction that quietly introduces a new
collapse is the same failure mode as the original, with a politeness wrapper. After drafting "I
retract X, because Y", check whether Y itself is a compound claim built from an unverified peer
observation, an inflated sample size, or an unlabeled translation. Retract the retraction if it
is. The retraction paragraph is the most failure-prone paragraph in the session: it is written
under the appearance of correction, which lowers the audit threshold, and the original failure's
momentum is still in the channel.

**Two agreeing mirrors are one witness.** When your own evidence and a peer's evidence both
support a claim, count whether the evidence was generated independently — different vantage,
different tool, different time, different actor class. N receipts from the same vantage, the same
chain, or the same parent are not corroboration; they are one witness repeated. This is especially
sharp right after a retraction, where the urge to "make up for the mistake" can quietly
manufacture a consensus that did not exist.

**The peer's retraction is not your retraction.** When a peer retracts their own observation,
they own that retraction. Do not bundle it into yours as if the two were the same mistake —
they are different observations, retracted by different agents, and a future reader who needs to
know which agent's claim is now void needs to know which agent retracted it. Cite the peer by
name. Cite yourself by name. Never merge.

## Pitfalls

- **Treating the third observation as proof of the pattern that the first two already
  "established"** is the commonest failure of step 8. The first two do not establish anything;
  they create a hypothesis. The third observation either supports it or fails to, but the failure
  of the third to confirm the pattern is the strongest evidence against it, and the temptation to
  re-interpret the third to fit is exactly the collapse the discipline guards against.
- **Retracting "compounded three findings" when you actually only have three independent
  observations** is a related failure: the *compounding* is the error, and retracting the
  findings rather than the compounding loses the findings. Retract the compound, keep the
  observations, and label what remains.
- **A peer correction received in the same channel as the original claim can feel like a
  retraction by association** — it is not. The peer is correcting the parts that were theirs; you
  own your parts. Merge only what the peer explicitly took, and only when they took it.

See `references/reconciliation-probes.md` for the concrete commands.
