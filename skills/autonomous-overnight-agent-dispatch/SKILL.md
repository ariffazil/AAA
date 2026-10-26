---
name: autonomous-overnight-agent-dispatch
description: "Use when a coding agent must run overnight without you."
version: 1.0.0
author: hermes
license: proprietary
owner: HERMES
risk_tier: T2
floor_scope: [F1, F2, F4, F11, F13]
autonomy_tier: T1.5
capability_tier: fed-reasoning-heavy
ecology_state: WARM
triggers:
  - "I need to sleep, run it overnight"
  - "autonomous execution only"
  - "launch claude code and let it finish"
  - "unattended repair run"
  - "dispatch a coding agent while I'm away"
metadata:
  hermes:
    tags: [dispatch, coding-agent, unattended, prompt-contract, claude-code]
    related_skills: [hermes-claude-code-spawn, concurrent-agent-writers, ccc-coder-federation]
---

# Autonomous overnight agent dispatch

## When to Use

- The principal is going to sleep and wants work to finish without him.
- A fix must run unattended and report in the morning.
- Any dispatch where no human will answer a question mid-run.

For the governed foreground/one-shot spawn contract, see `hermes-claude-code-spawn`. This skill is the
unattended variant: the same governance, moved out of the flag set and into a written prompt contract.

## Core rule

**When no human is present, governance lives in the prompt contract, not in hope.** Plan mode blocks the
mutations the job exists to make; a blanket permission bypass removes the last check. Neither is the
answer on its own. What works is a written contract that names what may change, what may never be
touched, how the result is proven, and when to stop.

## Step 1 — Check the tree is not already occupied

Two agents editing one tree overwrite each other silently. Before writing a single line of prompt:

```bash
ps -o pid,etime,time,args -C claude,codex,opencode | head
ls -lt --time-style=+%H:%M /root/.claude/projects/-root/*.jsonl | head -3
```

Read the tail of the newest transcript (`type`, `message.content`, tool-use blocks) to see what the live
session already produced and which files it touched. A session that has written tests but not yet edited
source will collide with your run. Decide explicitly: take it over, kill it, or stand down. Then launch
from a clean single-owner start.

## Step 2 — Write the prompt to a file

`write_file` the prompt to a stable path before launching. That file is simultaneously the contract, the
re-launchable artifact, and the audit record. Never pass a multi-kilobyte prompt as an inline shell
string; it cannot be reviewed, diffed, or rerun.

## Step 3 — The contract skeleton

Every unattended prompt carries these blocks, in this order:

1. **Pre-flight assertions** — working directory, expected branch, expected HEAD SHA. Stop on mismatch.
2. **The dirty-tree clause.** Read `git status --porcelain` first, then name every pre-existing modified
   or untracked file that must never be reverted, stashed, cleaned, or staged. Repeating another agent's
   unfinished work is the normal state of a long-lived tree, and it is the single most likely way an
   overnight run destroys value.
3. **A lock** — `flock -n <lockfile> -c 'echo ok'`; abort rather than interleave.
4. **Ordered work items, severity first**, each naming file and line range and the expected
   failure-to-pass transition. Order by consequence, not by convenience.
5. **Verification commands written verbatim**, with the project interpreter pinned (`.venv/bin/python`
   rather than `python3`) and the exact pytest selection to run.
6. **Staging by explicit path only.** Ban `git add -A` and `git add .` inside the prompt text.
7. **The commit lane** — the project's own lane/identity wrapper if one exists, with any machine-read
   metadata written as a literal `-m "KEY=value"` message body. Trailer normalisation rewrites `=` to `:`,
   and a gate grepping for `=` will miss a colon silently.
8. **A report path and its required fields** — what changed (file:line), before/after per item, verbatim
   test output, commit sha, what is unfinished, what was refused.
9. **Hard stops** — three failed attempts on one item: revert that item only, record it, move on. No
   `--no-verify`, no deleting `.bak` files, no editing chattr-locked canon trees, no push, no PR, no
   service restart unless explicitly ordered. Ambiguous authority: write HOLD and stop.

## Step 4 — Launch detached

```bash
cd <repo> && setsid nohup claude -p "$(cat <prompt-file>)" \
  --permission-mode acceptEdits \
  --allowedTools 'Read,Edit,Write,Glob,Grep,Bash(git *),Bash(pytest *),Bash(flock *)' \
  > /root/.hermes/cache/scratch/<name>-$(date +%H%M).log 2>&1 < /dev/null & echo started
```

`setsid` + `nohup` + `< /dev/null` detaches it from the terminal and survives the session ending. The log
path is what the morning review reads first. Prefer the scoped allowlist: it grants the mutations the job
needs and nothing else. Check the flag spelling with `claude --help` on the installed build before
shipping the command — the flag surface moves between releases. If the run genuinely needs the blanket
bypass, that must be an explicit sovereign order and the report must say the bypass was used.

## Step 5 — What to tell the principal before he sleeps

Three lines and no more: what will run, where the log is, where the report will be. If the tree is
already occupied, say that first and give the one command to clear it. Do not hand him a checklist to
run; that is the work you were asked to absorb.

## Pitfalls

- **Do not spawn beside a live session.** Check `ps` and the newest transcript first; two agents in one
  tree is silent corruption, not parallelism.
- **Do not let the agent stage the tree it did not create.** Explicit paths only; `git add -A` in an
  inherited tree commits another agent's half-finished work under your message.
- **Do not confuse `--permission-mode plan` with safety for an unattended mutation run.** Plan mode has
  no human to approve the plan, so the run either stalls or is launched with the wrong promise.
- **Do not assume a live process picks up source changes.** A running server keeps the old module in
  memory; record that a restart is needed instead of restarting production without an order.
- **Do not end the day without the report path.** An unattended run whose only output is a log the
  principal must grep is an unfinished dispatch.
- **Do not write the prompt as a narrative.** Every clause must be checkable by the agent: a file, a
  command, an expected output, or a stop condition.
