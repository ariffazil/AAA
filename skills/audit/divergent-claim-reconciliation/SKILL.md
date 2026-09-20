---
name: divergent-claim-reconciliation
description: "Reconcile observers who disagree about system state."
owner: Hermes
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
- A self-report is computed in the reporter's own context; reproduce it there (cwd, user) before
  calling it a contradiction.
- A reading carries a timestamp; an error older than the fix is stale, and state can move mid-session.
- Read an entry's reason field before declaring it dead — a paused-with-reason entry is a tombstone,
  not a corpse.
- Presence needs one surface; a true absence needs all of them.
- Check your own call shape before declaring a tool broken.
- Two live surfaces on one host disagreeing = real defect, not cache.
- Confirm shared axes before reporting a paradox.
- Open composite FAILs to per-item breakdown; separate "gone" from "cannot pass".
- Weight by doctrine recency; escalate canon reconciliation to the human.

See `references/reconciliation-probes.md` for the concrete commands.
