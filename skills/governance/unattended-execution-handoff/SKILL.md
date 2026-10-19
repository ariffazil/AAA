---
name: unattended-execution-handoff
description: "Use when handing work to an agent overnight."
version: 1.0.0
owner: HERMES
risk_tier: T2
floor_scope: F1 F2 F4 F7 F11 F13
triggers:
  - "I need to sleep"
  - "run it overnight"
  - "autonomous execution only"
  - "nobody will be awake"
  - "let it run unattended"
---

# Unattended Execution Handoff

The sovereign hands off a task and goes to sleep. Nobody will answer a permission prompt, stop a runaway, or notice that the machine went down at 03:00. The quality of the night is decided entirely by the brief.

## The core rule

**Constrain blast radius with the environment, not with the permission flag.** Deleting the approval prompt does not make a run safe; it removes the last thing that was watching. What makes an unattended run safe is that the agent *cannot* reach anything that matters — separate worktree, no push credentials, no service control, explicit file list.

If you cannot make every boundary structurally true, do not run unattended. Say so and run it in the foreground. A handoff you have to babysit is not a handoff.

## Procedure

### 1. Establish what is actually live

Never assume a repo edit is inert. Resolve what the running service imports:

```bash
<service-venv>/bin/python -c "import <pkg>; print(<pkg>.__file__)"
```

If that path lands inside the source repo, the repo **is** the running code: a commit in a separate worktree is safe, but a stray `git checkout`, `git stash`, `git clean` or `git reset` in the live tree is an outage. Write those commands into the brief as explicitly forbidden — a competent agent will otherwise "tidy" the tree it was told not to touch.

Record the live tree's dirty state before the run so you can prove afterwards nothing moved:

```bash
git -C <live-tree> status --porcelain
```

### 2. Isolate the workspace

```bash
git -C <live-tree> worktree add <worktree-path> -b <branch> <base-branch>
```

All work happens there. Untracked pre-written tests, fixtures or specs that form part of the contract must be **copied in** — a fresh worktree does not carry them.

### 3. Measure the baseline before writing the brief

Run the target tests yourself, once, and record exact counts. Highest-value step: it turns a vague objective into a finish line the agent can check itself against, and it catches the case where the tests already pass — meaning the task is not what everyone assumed.

Put the baseline in the brief. "14 failed, 9 passed" is a specification. "Make the tests pass" is an invitation to fabricate.

### 4. Write the brief as a file, not a chat message

The brief is a file the agent reads in full and you can re-read in the morning. Non-negotiable sections:

- **Objective** — the artifact that must exist, not the effort to expend.
- **Boundary table** — section 5 below, each row with how it is enforced.
- **Baseline counts** from step 3.
- **Work order** — one item at a time, each with its own pass criterion, so partial progress is still coherent work.
- **Report file** at a stated path with fixed sections.
- **Time box**, plus a park-after-N-minutes rule per item.
- **Self-check that production was untouched.**

### 5. The boundary table

| Boundary | Enforced by |
|---|---|
| Never edit the live tree | worktree isolation; explicit forbidden-command list |
| Never mutate running code or state | no restart, stop, reload, `systemctl`, `docker`, package install |
| Never publish | no `git push`, no PR, no merge to the default branch; local commit only |
| Never weaken the contract | no test deletion, skip, xfail, or assertion edits |
| Never expand scope | explicit file list; no new dependencies, no refactors, no drive-by reformatting |

If the repo has a commit-identity gate (a hook that rejects a plain `git commit`), put the exact approved command in the brief. Do not let the agent discover it at 03:00 and improvise an identity.

### 6. The report contract

Fixed sections, because this file is the only thing the human reads on waking:

1. What changed — one line per item, file and function.
2. Test evidence — the exact final command and its final count line, verbatim.
3. Decisions taken without asking — every judgement call and why.
4. Blocked — the precise blocker, not a status word.
5. Production safety — verbatim `git status` of the live tree plus a health probe.
6. Commit — branch, SHA, or the reason it was not committed.

Forbid progress narration. An unattended run that narrates produces a transcript; one that writes a report produces an artifact.

## Pitfalls

- **A vague objective gets optimised for looking finished.** An unattended agent cannot ask what "done" means, so it picks a definition that is cheap to satisfy. Pre-written tests with known counts are the only defence.
- **The agent will fix the harness instead of the code.** If a test is genuinely wrong, an unsupervised agent will often edit the assertion. Forbid it, and require a suspect test to be left failing and reported.
- **Pre-existing failures get absorbed as regressions.** Note which tests already fail on the base branch before the run, or the morning report blames the night's work for a red that was always there.
- **A task with no upper bound will consume the night.** Pair an overall time box with a per-item escape: park it, record what was learned, move on.
- **"It committed" is a self-report.** Verify the SHA exists and the diff touches only the allowed files before telling the human it is done.
- **Do not let the brief re-describe the codebase.** Paths and symbols belong in the brief only where they are the target; a prose tour of the repo invites the agent to treat description as authority.

## Brief skeleton

```
You are running unattended. The human is asleep. Nobody will answer a question,
so do not ask one. Where a decision is ambiguous, take the most conservative
reading, record it under "Decisions taken", and continue.

# OBJECTIVE
<the artifact that must exist; name the files that must pass>

# CONTEXT
- Live tree: <path> — this is the code the service imports (verified: <pkg>.__file__)
- Work in: <worktree> on branch <branch>
- Tests to pass: <files>
- Baseline before handover: <N> failed, <M> passed on <command>
- Commit must use: <exact approved command>

# HARD BOUNDARIES — BREACH IS FAILURE
1. Do not edit/stash/checkout/reset/clean inside <live-tree>, except the single
   `git worktree add` below. Those commands are forbidden there.
2. No service restart, stop, reload, systemctl, docker.
3. No push, no PR, no merge. Local commit only.
4. No package installs, no dependency changes.
5. Do not delete, skip, xfail or weaken any test, and do not edit assertions.
   If a test is wrong, leave it failing and report it.
6. Stay inside: <allowed paths>

# STEPS
1. Create the worktree; copy in any untracked contract files.
2. Run the baseline. Expected <N> failed, <M> passed. Fewer failures = investigate first.
3. Work order, one item at a time, each with its own pass criterion. Minimal
   surgical diffs. No refactors, no new abstractions, no reformatting.
4. Run the full relevant suite. Compare with <base branch>; pre-existing reds are
   recorded, not chased.
5. Prove production untouched: `git -C <live-tree> status --porcelain` must match
   <pre-run listing verbatim>. Anything else = breach: stop, revert, report.
6. Commit with <exact approved command>. Do not push.
7. Write <report path> with: what changed / test evidence verbatim / decisions
   taken / blocked / production safety / commit.

# OPERATING RULES
- Never print a real secret, token or key. Synthetic values only.
- Hard time box <N> hours. On expiry stop cleanly, commit what is coherent, report.
- One item stuck past <N> minutes: park it, note what you learned, move on.
- No progress narration. Do the work, then write the report.
```

## Handing it over

Give the human exactly one copy-paste command and one sentence about what they will find in the morning. Nothing else — they are going to sleep.
