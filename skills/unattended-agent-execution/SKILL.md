---
name: unattended-agent-execution
description: "Use when an agent runs while the human sleeps."
version: 1.0.0
owner: HERMES
risk_tier: T2
floor_scope: F1 F2 F4 F7 F11 F13
autonomy_tier: T1.5
capability_tier: fed-reasoning-heavy
ecology_state: WARM
owned_by: HERMES
authority_of: AAA
---

# Unattended Agent Execution

Handing a task to a coding agent (Claude Code, Codex, OpenCode, any `-p`/headless harness) that will
run for hours with nobody watching. The human is asleep or away; there is no one to answer a permission
prompt, no one to catch a bad judgement call, and no one to notice a dead service until morning.

**The work is not the hard part. The boundary is.** A run that does the right fix in the wrong tree has
done more damage than a run that failed cleanly.

## Prerequisites — before writing a single line of the brief

1. **Confirm the target is real and the baseline is red.** Run the tests the task is supposed to make
   green, record the exact count line (`14 failed, 9 passed`). Without a baseline the run cannot tell
   progress from invention, and neither can you in the morning.
2. **Confirm the tool exists and its flags.** `claude --version`, `codex --version`. Do not write a
   brief pinned to a flag you have not seen in `--help`.
3. **Find out what the live system imports.** If a service is running from the same tree, the brief
   must isolate. See "Worktree isolation" — this check is the whole reason the mode exists.
4. **Confirm the commit identity gate.** If plain `git commit` fails closed on that repo, the brief
   must name the wrapper and its exact argument order, or the run ends uncommitted.

## The contract — six sections, in this order

Copy `templates/unattended-brief.md` and fill it. The order is load-bearing, not cosmetic.

| # | Section | Why it is here |
|---|---|---|
| 1 | **Objective** | One paragraph, the finished state. Not a task list. |
| 2 | **Hard boundaries** | Numbered, absolute, with the *mechanism* of each risk. A boundary without its why gets rationalised away at hour three. |
| 3 | **Baseline** | The literal command and the literal expected-failure count. |
| 4 | **Work contract** | Per item, one at a time, with what the fix must and must not touch. |
| 5 | **Proof** | Regression command, plus a step that proves production was not touched. |
| 6 | **Commit + report** | Local commit only, plus the report file path and its fixed sections. |

Then, at the bottom: **time box**, **parking rule**, **output discipline**.

### 1 — Objective names a finished state

"Make `tests/runtime/test_telemetry_redaction.py` pass without weakening it" is an objective. "Fix the
telemetry bugs" is a wish. Name the artifact that will exist when the run is correct.

### 2 — Hard boundaries carry their mechanism

Every boundary should say what breaks if it is crossed, in one clause. "Do not edit `/root/arifOS`" is
a rule a model will reinterpret. "Do not edit `/root/arifOS` — the running service imports the package
straight from that path, so an edit is an unreviewed change to production and a syntax error takes the
service down" is a rule a model can reason with.

Always present, for any live system:

- no service restart / stop / reload (systemd, docker, supervisor)
- no `git stash`, `checkout`, `reset`, `clean`, `restore` in the shared tree — other agents may have
  in-flight work there, and those commands destroy it
- no push, no PR, no merge — local commit only
- no package installs, no dependency edits, no network
- no deleting, skipping, `xfail`-ing, or weakening tests — the test is the contract, not an obstacle
- no secrets in output, commit message, or report; use the synthetic canaries the tests define

### 3 — Baseline is a number, not a description

The brief states the exact command and the exact expected failure count. "Tests are failing" lets a
run claim success by fixing two of fourteen.

### 4 — One item at a time, with the shape of the fix

Order the items. For each: what the observable defect is, what the fix must do, and what it must not
disturb. Then the green condition: run only that item's test file until green, then move on.

State the shape of the solution, not the solution. "Recursion must handle `dict`, `list`, and `tuple`
with a bounded depth that redacts rather than emits at the bound" is contract; "rewrite `_redact` to
call `_walk`" is an instruction the run should be competent enough to derive.

### 5 — Proof, in two directions

Forward: the regression suite, with a note that pre-existing failures on the base branch are recorded
and not fixed. Backward: a literal `git -C <live tree> status --porcelain` whose output must match a
snapshot pasted into the brief. Any line that was not in the snapshot is a boundary breach the run must
revert and declare. Pair it with a liveness probe (`curl -s .../health`) so a dead service cannot hide
behind a green test run.

### 6 — Commit rules and the report file

Local commit only, through whatever identity gate the repo enforces — for the lane wrapper the form is
`git-lane <lane> -C <path> commit`, so no `cd` is needed. If the gate is unavailable, the run leaves the
work uncommitted and says so; it must never substitute another identity.

The deliverable is a **file at a fixed path**, with fixed sections: what changed · test evidence
(verbatim final line) · decisions taken without asking · not done / blocked · production-safety output ·
commit SHA. The chat gets one line in the morning. The file is what the human actually reads.

### Closing rules

- **Time box** (4h is reasonable) and **parking rule**: an item that resists for more than ~45 minutes
  is parked with what was learned, and the run moves on. Without this the run burns the whole night on
  the one item that was misdiagnosed.
- **Output discipline**: no progress narration, no celebration, no summary of effort. Work, then report.

## Worktree isolation — the load-bearing rule

**Never point an unattended run at a tree the running system imports from.** Pointing an autonomous
editor at a live package root means every keystroke is a production deploy with no review.

```bash
git -C <live tree> worktree add <worktree path> -b <branch> <base ref>
```

Then everything — edits, tests, commit — happens in the worktree.

**Pitfall: untracked files do not exist in a worktree.** Test files written in the live tree but never
committed are absent from the new worktree, so the run starts with no target and will invent one.
Copy them in explicitly as a numbered step in the brief:

```bash
mkdir -p <worktree>/tests/runtime && cp <live tree>/tests/runtime/<contract test>.py <worktree>/tests/runtime/
```

**Pitfall: the worktree's interpreter.** Run tests with the same interpreter the live service uses
(e.g. `/opt/<app>/current/venv/bin/python -m pytest`), not a bare `python -m pytest`. A different
interpreter resolves a different installed package and the run tests code nobody will deploy.

## Permission model — allowlist, not the bypass flag

An unattended run cannot answer prompts, so scope must be declared up front. Do that with an explicit
tool allowlist and a permission mode, not the nuclear skip-permissions flag:

```bash
<agent> -p "$(cat <brief path>)" --max-turns 80 \
  --output-format json \
  --allowedTools 'Read,Edit,Write,Glob,Grep,Bash' \
  --permission-mode acceptEdits
```

- `--dangerously-skip-permissions` removes the last gate an unattended process has. The allowlist gives
  the same non-interactive behaviour with a bounded surface; use it.
- `--max-turns` is mandatory. An unattended loop with no turn cap runs until it burns the budget.
- `--output-format json` so the morning check is a parse, not a re-read.
- Put the brief in a **file** and pass it with `$(cat ...)`. Inline prose in a shell argument loses
  newlines, and the numbered boundary list is the part that must survive intact.

## Morning verification (do this, do not trust the report)

The report is a self-report from a process you did not watch. Verify before repeating any of it:

1. `git -C <worktree> log --oneline -3` and `git -C <worktree> show --stat <sha>` — does the commit
   exist, and does it contain the files the report names?
2. Re-run the test command yourself and read the count line.
3. Re-run the production-safety check against the **live** tree.
4. Probe the live service.

A run that reports "14 passed" and a commit that does not contain the fix is the exact class of defect
this mode exists to prevent — and the report will read as confident either way.

## Pitfalls

- **Writing the brief as a task list instead of a contract.** A list invites the run to negotiate with
  it; a contract with numbered absolutes and their mechanisms does not.
- **Omitting the "prove you did not touch production" step.** Without it, a run that wandered into the
  live tree will simply not mention it. The `status --porcelain` diff is the only cheap detector.
- **Letting the run fix pre-existing failures.** Scope creep with a good excuse. Name the rule: record
  pre-existing failures, do not fix them, do not spend more than a few minutes on them.
- **Assuming a clean night means correctness.** A green suite proves the contract held; it does not
  prove the fix is the right one. Read the diff in the morning before merging anything.
- **Delegating a decision that needs the human.** If the task's correct outcome depends on a values
  judgement (which of two products to buy, whether to publish, whether to accept a vendor's terms),
  that is not an unattended task. Park it and ask.

## Support files

- `templates/unattended-brief.md` — the fillable six-section brief, with the boundary block already
  written.
