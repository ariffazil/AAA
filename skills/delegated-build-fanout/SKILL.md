---
name: delegated-build-fanout
description: "Use when fanning one objective out to parallel subagents."
version: 1.0.0
tags: [delegation, subagent, verification, evidence, fan-out]
triggers:
  - "spawn agents to build"
  - "spawn coding agents"
  - "fan this out"
  - "get the fleet on it"
  - "several agents in parallel"
  - "several subagents on one repository"
  - "dispatch agents to fix this"
  - "did the subagents actually deliver"
floors: [F2, F11, F13]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Delegated Build Fan-Out

For one objective handed to several parallel children at once (Hermes `delegate_task` with 2-10
tasks). Distinct from the bundled OpenClaw `sessions_spawn` template: children here have their own
contexts and terminals, cannot ask questions, and their summaries are **self-reports, not verified
facts**.

## Before you dispatch — measure what you were handed

A defect list you did not measure is an unverified claim with a fan-out multiplier. Hand it to N children
and you broadcast its errors N times; each child then has an incentive to satisfy the brief rather than
contradict it, so a wrong finding comes back as N confirmations wearing the look of independent evidence.

Observed: an inherited finding-set named a duplicated prediction pair. Measuring it showed the two claims
were about *different* price levels, not one fact counted twice. Another inherited claim had been merged
with a genuine one, which hid that part of the brief would have commissioned a fix for a **false positive**.
Some inherited claims survived measurement and some did not, and only the measurement separated them. A
third inherited claim was a report of a stated total that matched neither store's record count.

- **Re-measure every inherited claim yourself, before it becomes a work package.** The other lane's report
  is a hypothesis about the system, not a reading of it. Confirm each claim against the live store, file or
  probe, and drop the ones that do not survive.
- **Write a correction clause into every brief:** *"if a number in this brief is wrong when you measure it,
  correct it in your report rather than propagating it — your measurement outranks this brief."* Without it
  the child treats the brief as authority and returns agreement, which is the one answer carrying no
  information.
- **State up front which claims you could not verify.** An explicit `UNVERIFIED` line becomes a work package
  for the child; an omitted one is an error the child has no reason to look for.
- **A claim that a fix is needed is itself a claim.** Verifying the observation and verifying the
  *prescription* are separate acts: the finding can be real while the repair it implies is unnecessary or
  destructive. Have the child classify the defect and report the blast radius before applying a fix.
- **Partition by file ownership and name the sibling owners inside each task string.** A fix-set spanning
  several subsystems invites two children onto one file; the write scopes must be disjoint and each child
  must be told which paths belong to someone else. Where a shared module is the boundary — one tree's
  entrypoint importing another tree's file — say so explicitly rather than assuming the partition is
  obvious from the paths.

## Procedure

1. **Write ONE binding SPEC file before dispatching.** Put it in a shared workdir and point every
   child at it — do not repeat the constraints inside each task string. Each task string stays short:
   its work-package id, its deliverable, and "read the SPEC first".
   Skeleton: `templates/delegation-spec.md`.
2. **Define the success property, not the noun.** "Make the system care" and "improve reliability"
   are nouns. Write what would make it true and what would prove it false.
3. **Include the HARD FORBIDDEN list** — every invariant plus the specific destructive shortcuts, each
   with its rationale. Always name: restarting the live gateway (it kills the session that dispatched
   the work), writing to constitutional files, printing any secret, and any human-facing side effect
   beyond one designated target.
4. **Designate exactly one verification target** for side effects (one chat id, one file path, one
   endpoint) and require the child to prefix test output so it is recognisable.
5. **Set the evidence contract.** One JSON line per child into a shared ledger:
   `{agent, wp, state, files, command_run, observed, trace_id, blocked_op, next_owner}`. Children
   append; nobody overwrites — say it explicitly, because two children writing one file is a silent
   loss of half the evidence.
6. **When the packages are documents or research rather than code, add an anti-fabrication clause
   and a per-claim source requirement.** A child with web access will write an external standard, a
   competitor's feature list or an industry statistic straight from memory, in fluent prose
   indistinguishable from fetched fact. Require, per external claim: the URL, the fetch date and a
   verbatim excerpt; and require `UNKNOWN` / `BLOCKED` where a source will not load. State that a
   package reporting `BLOCKED: source requires auth` is worth more than one reporting `DONE` on
   recalled content.
7. **When the subject of the study is an existing repository, freeze it.** Make the whole repo
   read-only for every child and route all output into a scratch workdir — one directory per work
   package plus a shared `evidence/ledger.jsonl` — with each child naming, at the top of its
   artifact, the target path the artifact is proposed *for*. The coordinator applies the change after
   verification. This extends the prepared-diff rule from constitutional files to any repo the
   principal owns.

   **When the children DO write into a shared repo, partition by path set, not by intent.** Give
   every package its own disjoint set of paths and name the sibling owners inside each task string
   ("do not touch X — another package owns it"), so no two children stage the same file. Also state
   per package, in the task string: **which branch to work on and whether to push.** Leaving either
   unspecified splits the batch — some packages pushed, some committed local-only, all landing on
   whatever branch happened to be checked out — and the coordinator inherits the reconciliation.
   Where the work is a fix rather than an artifact, "work on a new branch, branch only, no merge, no
   deploy" produces clean refs and a decision the principal can take later; the packages without a
   branch policy produce a shared, moving HEAD instead.
8. **Require the true state, and say up front that HELD and BLOCKED are complete answers.** A child
   papers over a gap when the only outcome that looks like success is "done". Explicitly: "a held or
   blocked line is a full receipt, not a failure."
9. **Cap the final message** (WP id + state + the command + a verbatim output excerpt + absolute
   paths + what it could not do). Long summaries hide the missing line.
10. **Give each package its own "verify by <command>" instruction** so the child cannot substitute
    "I read my own code and it looks right".
11. **Dispatch, then verify yourself.** Open each child's artifacts, re-run the load-bearing command,
    and confirm the wiring is live before reporting value delivered.

## Pitfalls

- **A unit-verified artifact is not a working feature.** A green assertion suite, an exercised helper,
  a `PASS` from a function called by hand — all prove *the unit works*, none prove *the live system
  calls it*. Children will report `VERIFIED` on this basis and be technically correct, while the
  feature reaches no user. Check the mechanism is loaded:
  `grep -c "<plugin-or-module-name>" <live log>` (`0` = dormant) and
  `ls -la <registry/config file the mechanism requires>` (absent = never constructed).
- **Never accept `VERIFIED` derived from reading the artifact's own code** — by the child or by you.
  Self-report is the claim under test, not the test. Require the command and its real output. For a
  document package the analogues are a citation whose page was never fetched, a row count taken from
  the child's own table, and a "the source says" with no excerpt — spot-check quoted claims against
  their stated URLs before the artifact reaches anyone.
- **When the intended mechanism is dormant, fix the surface that IS loaded.** Then report the dormant
  wiring as a finding in its own right — "built, verified, unreachable" is the complete and useful
  answer, and it is what the principal actually needs to know.
- **A config edit is not live until the process that reads it restarts.** Verify by observed
  behaviour, not by re-reading the file.
- **Constitutional files get a PREPARED diff, not an edit.** Have the child write the unified diff
  plus a `patch --dry-run` result into the workdir and hold the application for the principal's word.
- **Children cannot ask questions.** Anything ambiguous in the SPEC becomes a silent guess, and a
  guess that produces a file looks identical to work. Resolve ambiguity in the SPEC, not in the
  child's head.
- **When the package must evidence a figure that already exists in your own documents, require
  claimed and observed as two separate fields.** A child told to "gather the evidence for \<claim\>"
  will reproduce the document's number in a form that reads like measurement. Measured: one claim's
  figure existed only as prose in two doctrine files with no probe behind it, and the count a child
  actually reproduced was a different class of the same defect, an order of magnitude larger. Both
  belong in the return — the claimed figure, the reproduced figure, and which surfaces were searched.
  Publishing only the reproduced number hides that a documented claim was never true; publishing only
  the claimed number is the fabrication the anti-fabrication clause exists to prevent.
- **Any artifact whose purpose is proof must ship with an explicit "what this does NOT prove" field.**
  Children reliably disclose limits when asked for the field and silently omit them when not, and a
  proof artifact read without its boundary gets cited for more than it established. Require the field
  in the output contract, not as a follow-up: containment gaps, disabled gates, unsigned receipts and
  unexercised transports are exactly what a reader needs, and they are cheap to state up front and
  expensive to reconstruct later.
- **Name the in-repo precedent when the package is a behaviour change.** Point the child at the
  sibling implementation in the same file that already does the right thing, and require the patch to
  match its convention. A child told only *what* to change invents a new pattern, spreads the change
  across the file, and leaves two conventions for one decision; a child given the precedent returns a
  minimal patch with a comment tying it to its sibling, which is what a reviewer can accept.
- **Require the child to classify a defect as live or latent before fixing it.** Have the probe that
  distinguishes them recorded in the return (execute the code path and print the result). The class
  matters more than the fix: a defect framed as a live outage triggers a wrong deploy decision, one
  framed as latent gets ignored, and only the probe settles which it is. For any change to a gate or a
  control, also require the **blast radius and the revert path** in the return — what now denies that
  used to flow — because failing closed on a primary gate converts a silent availability fault into a
  hard refusal, and that trade is the principal's to make, not the child's.
- **Expect HEAD to move under concurrent children.** Several packages committing into one repo push
  the shared HEAD forward while a sibling is still working, so a child's diff base can be stale by the
  time it lands. Have each child stage only its named paths (never `git add -A`), re-read the parent
  commit immediately before committing, and report the parent it built on. In the coordinator's own
  commits, `git show --stat <sha>` to confirm no child's edit rode along unmentioned.
- **Do not wait or poll.** Results arrive on their own; finish whatever does not depend on them and
  end the turn.

## Close-out

Report per work package: id, true state, the command, a verbatim output excerpt, absolute paths, and
what was not done. Distinct from `verify-runtime` (terminal-state verification) and from the bundled
`FORGE-subagent-spawn` (the OpenClaw single-spawn contract) — this is the coordinator side.
