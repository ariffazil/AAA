---
name: parallel-agent-fanout
id: parallel-agent-fanout
version: 1.0.0
description: Use when fanning work to parallel agents in one repo.
owner: Hermes (curator-managed)
risk_tier: medium
floor_scope: [F1, F2, F7, F11]
autonomy_tier: T1
tags: [fanout, subagent, parallel, verification, contract, repo-hygiene, remediation]
---

# Parallel Agent Fanout

Fanning one objective across several agents that all write to the **same repository**. Contract-
first dispatch, disjoint file ownership, post-write re-probe, self-report hygiene, and
remediating what the fanout found.

The agents are not independent: they read each other's half-written files, their audits contradict
each other, and a fanout run during active writes produces *false* findings rather than missed
ones. This skill is the parent's whole job — probe, contract, dispatch, verify, remediate.

The single sentence: **freeze the interface before the agents start, own disjoint files, and
re-probe everything after the writers stop.**

## When to use

- One objective decomposed into pieces that must all land in the same repo.
- Any dispatch of 2+ writing agents with overlapping subject matter.
- Adding an audit or review agent alongside writers.

## When NOT to use

- A single bounded change. Do it directly; a contract file for one agent is overhead.
- Pieces that live in genuinely separate repositories with no shared build or test command.

---

## §1 Probe the target before dispatching anything

Grep the repo for the engine, the gate names, and the primitives the task asks for, and state
the actual delta. A task to "build" a capability that already exists and is merely **unwired**
is an *integration* task. Dispatching a builder onto it produces a duplicate implementation of
the same doctrine, which is worse than doing nothing — two engines now disagree differently.

Report plainly, before dispatch: which parts already exist, which are built but orphaned, and
which are genuinely missing. Do this **before** the agents are sent, not after.

Also probe the environment and write the results down: which libraries are actually installed.
This is the single highest-value line in the contract file (see §2), because it stops an agent
writing an import for a package that is not present.

## §2 Freeze a contract file before spawning

Write one file, mark it read-only to every agent, and tell each agent to build to it and to
report rather than silently deviate. It must contain:

1. **Environment probe results** — packages present and absent, and an explicit instruction not
   to import the absent ones.
2. **The shared type/envelope** every component exchanges, written out in full. If the same
   structure is passed between agents, they must not each invent their own.
3. **Frozen function signatures** — names, arguments, return shape. Frozen means: build to it,
   and if it is wrong, say so; do not quietly adjust it.
4. **The output shape** the top-level result must take.
5. **The doctrine that must survive the wire** — the specific corrections and invariants that a
   naive implementation would drop. List them as numbered rules with their reason. This is where
   the domain's hard-won caveats live, and it is the difference between four agents converging
   and four agents each losing a different half of the idea.
6. **An anti-collision protocol**: create only the files listed in your brief; never edit the
   contract, the shared engine, or anything outside your list.

Agents built from a shared frozen contract converge. Agents built from a prose brief diverge.

## §3 Dispatch with disjoint ownership

In each brief, state explicitly:

- **The files this agent owns** — the complete list.
- **The files it must not touch**, naming the other agents' directories too. "Do not create
  anything under `<other package>/`." Overlapping ownership is the default failure, not an edge
  case; say the rule out loud even though it looks obvious.
- **Forbid mutating version-control commands.** Concurrent commits make the tree unreadable for
  everyone, including the parent.
- **Run only your own test file.** A full-suite run while siblings are mid-write measures the
  race, not the code, and manufactures false regressions.
- **Paste real command output in your summary**, and state that a summary without it is not a
  deliverable. Cheap, and it is the only defence against a fabricated completion.

Where one agent's output is another's input, say so, and hand the second agent the exact key
names and return types — not a description of them.

## §4 Steer mid-flight, do not queue corrections

While children run you can push a course correction into an individual one. Use it the moment an
independent finding lands: a correction delivered mid-run costs nothing, and the same correction
delivered after the child has finished costs a rewrite of the part it already built.

This is the main reason to have an independent auditor running *concurrently* rather than
sequentially — its findings arrive while they are still cheap to apply. See §5 for how to handle
the ones that arrive too late.

## §5 Verify after the writers stop — never during

A concurrent read-only auditor reports defects that **no longer exist**: it snapshots a file a
sibling has not written yet and calls the gap blocking. The same auditor also **misses** things
that land after its snapshot. A clean report written during active writes carries almost no
information.

So after the last writer stops:

1. **Re-probe every load-bearing finding yourself.** Re-run the checks; do not inherit the
   verdicts. Confirm line references — a stale line number is a false finding even when the
   underlying claim was once true.
2. **Record deltas against the audit**, not a rewrite of it. Keep the audit's own numbering so a
   reader can see what moved. Mark each finding as verified, stale, or superseded, with your own
   evidence.
3. **Pin the snapshot** to a commit hash plus file hashes, and state which findings were taken
   under the race and which were re-verified after it. Without the pin a reader cannot tell a
   stale finding from a live one.
4. **Re-run the whole suite together.** Files that pass individually can still fail together —
   shared fixtures, import side effects, and registration counts are the usual causes.
5. **Stop when the delta is recorded.** Verification of a moving target becomes an endless loop;
   fix the snapshot, check it once, write the delta, move on.

### Reading a child's summary

A child's summary is a **self-report**. Sort every claim before repeating it:

- **Checkable — re-run it yourself:** a file exists; a symbol is exported; a test file passes
  under *your* command; the change set is confined to the files claimed.
- **Not checkable — never evidence:** claims about *how* a result was reached, claims that a
  defect is fixed, confidence or quality assertions about their own work. There is no artifact
  behind these. Reproduce or drop them; do not relay them downstream as fact.

Read the shape too: a child that names what it could not verify and states where it stopped is
more trustworthy than one reporting clean success. A child reporting zero problems is reporting
on its *search*, not on the system.

---

## §6 Remediating what the fanout found

An audit typically surfaces a hazard that is inert only by accident. Two rules govern the fix.

### Remove the capability, not just the gate

When a dangerous code path is currently unreachable because a name is absent from an allowlist
or manifest, the hazard is **not fixed** — it is disarmed by coincidence, and the next person who
"makes the feature work" re-arms it. The durable fix is to **remove the capability**: delete the
field from the producer's request schema so it cannot be populated even if the path is opened.

- Ask of any guard: is this an enforced gate, or is it a name that happens to be missing?
- Prefer making the bad value **unproducible** over making it **filtered**.
- Keep the channel for legitimate producers; remove the *inappropriate producer*, not the field.
- Verify no other path supplies it. A capability removed in one place but still writable in
  another has not been removed.
- Leave an explicit, readable note at the site naming why the field is unpopulated. Without it
  the next contributor restores it as an obvious omission.

### Do not bundle a safety gain with an unblocking

Arming a new, well-designed lane on the same change that unblocks a hazardous one hides a
regression inside a feature. Ship them separately. If arming the new lane requires touching a
shared manifest, say so explicitly and write down what must **not** be added at the same time.

### Know when the mutation is not yours

Adding tools to a public surface, arming a lane, or changing a registry is a governed revision,
not a side effect. Before doing it:

- Grep the test tree for **count assertions** on the surface (`== 26`, `== 29`, `== N`).
  Registries are usually pinned by tests, so the change is a revision with a test update, not a
  free addition.
- Check whether the repo's own comments reserve the action for a human authority. If they do,
  prepare the change instead of applying it: write the two or three required edits into a
  single inspectable plan — file, action, reason — and leave it unapplied.
- A plan that can be read in one screen beats a summary paragraph describing one.

---

## Pitfalls

- **Prose brief instead of a frozen contract.** Four agents each invent a private design and the
  parent reconciles by hand. Freeze first.
- **A concurrent auditor's findings accepted un-re-probed.** Half of them describe a tree that no
  longer exists.
- **A full-suite run used as evidence during active writes.** It measures the race.
- **Accepting "the defect is fixed" without re-running the check that found it.**
- **Budgeting zero time for the parent to verify.** The fanout is not done when the children
  return; the parent's re-probe is the completion step.
- **Trusting cached editor diagnostics over runtime introspection.** A language-server error about
  a type constraint can be stale after a sibling's edit. Confirm by constructing the object or
  reading its declared fields at runtime — the diagnostics lag the file, the interpreter does not.
- **Rebuilding a primitive that already exists.** See §1. Duplication of working code is the
  most expensive outcome of a fanout, because it looks like progress.

---

*DITEMPA BUKAN DIBERI — the fanout is done when the parent has re-probed it, not when the
children return.*
