---
name: unattended-agent-runs
description: "Use when a coding run must continue while he sleeps."
version: 1.0.0
owner: HERMES
risk_tier: T2
floor_scope: F1 F2 F4 F11 F13
autonomy_tier: T2
triggers:
  - "I need to sleep"
  - "autonomous execution only"
  - "run it overnight"
  - "let it run while I'm away"
  - "no human available"
  - "launch a background agent"
  - "what prompt do I give claude code"
  - "init prompt for autonomous execution"
capability_tier: fed-long-context
ecology_state: WARM
owned_by: HERMES
authority_of: AAA
---

# Unattended agent runs

One class of task: the principal is stepping away, a coding agent must keep working alone, and there is
nobody to answer a question or approve a prompt at 3am.

The job is not "make the agent autonomous". It is **move the safety boundary from interactive
approval to declared scope**, then write a spec complete enough that the agent never needs to guess.

## 1. Decide before writing anything

An unattended run is only safe when all four hold. If one does not, the deliverable is a smaller task,
not a bigger prompt.

| Condition | Test |
|---|---|
| The work is decomposable | each item has its own file, its own test, its own commit point |
| Success is machine-checkable | a test suite or a probe decides pass/fail, not an opinion |
| Blast radius is containable | one branch, no push, no deploy, no data migration |
| The spec can name every path | if you cannot write `file:line`, the agent will spend the night searching |

Findings from an audit are the ideal shape: bounded, per-file, each one falsifiable by a test.
"Make the product better" is not.

## 2. Check whether another agent is already in the tree

Shared hosts run several coding agents against the same checkouts. Two writers on one working copy is
how a night's work disappears.

```bash
pgrep -af 'claude|opencode|codex|qwen' | head
cd <repo> && git status --porcelain            # whose edits are in flight
ls -lt --time-style=+%H:%M:%S <dir> | head     # mtimes inside the target tree
flock -n /root/.locks/<task>.lock -c 'echo ok' # take the lock; failure = another writer
```

- Alive for hours at low CPU = idle REPL, harmless. Rising CPU **and** mtimes in the target tree within
  the last ~10 minutes = mid-task. Kill it or wait; never spawn alongside.
- Read what the earlier session produced before writing the prompt. Tests written but source untouched
  is a half-done pass: tell the new session to **adopt and extend** those files rather than rewrite.
- Put the same lock acquisition in the child's pre-flight so a second spawn aborts instead of racing.
- If the branch already carries the change, do not spawn at all.

## 3. Containment replaces approval

The permission flag is not the risk; an unscoped blast radius is. Declare containment inside the
prompt, so the agent enforces it on itself with no human present:

- one named branch, never `main`; no push, no PR, no merge, no remote writes
- stage **explicit paths**; never `git add -A` / `git add .` — other agents' uncommitted work sits in
  the same tree
- list the pre-existing dirty and untracked files **by name** and state: you did not make these, never
  revert, stash, checkout, clean or commit them. An unattended agent with `git checkout .` in its
  repertoire deletes a sibling's work.
- no service restart, no redeploy, no writes under the deployed path
- hard stops: N failed attempts on one item → revert **that item only**, record, move on
- report path fixed in advance

Identity-gated commits: give the exact `git-lane` command and the literal `-m "REPO=<repo>"` line.
Trailer normalisation rewrites `=` to `:` and CI gates that grep for `=` then miss it.

## 4. Prompt anatomy

Order matters more than wording. Each section exists because a night-long run loses the threads a human
would have held.

1. **Opening** — "No human is available. Do not ask questions; decide, act, verify, record."
2. **PRE-FLIGHT** — branch + HEAD assertion, dirty-file inventory by name, adopt prior work, take the lock.
3. **ENVIRONMENT** — the repo venv interpreter by absolute path. Bare `python3` on this host lacks the
   deps and the agent burns turns on `ModuleNotFoundError`.
4. **FIX ORDER** — severity order, one section per item.
5. **Per item** — `file:line`, the bug with its reproduction, the required behaviour, the constraints,
   the required tests (phrased as assertions, including the must-not-regress cases).
6. **VERIFICATION** — exact commands, "keep the output".
7. **COMMIT** — exact command, only when the named tests pass.
8. **REPORT** — path plus required contents, ending with a short summary in the principal's language.
9. **HARD STOPS** — immutable trees, `.bak` files, `--no-verify`, ambiguity ⇒ HOLD.

See `## Appendix — prompt skeleton` at the bottom for a fill-in-the-blanks version.

Write the prompt to `/root/AAA/prompts/<task>.md` and hand over **one** copy-paste box. Not a menu — he
is going to sleep.

## 5. Detach

```bash
cd <repo> && setsid nohup claude -p "$(cat /root/AAA/prompts/<task>.md)" \
  --dangerously-skip-permissions --max-turns 200 \
  > /root/.hermes/cache/scratch/<task>-$(date +%H%M).log 2>&1 < /dev/null &
```

`--dangerously-skip-permissions` is authorized here **only** because the principal explicitly ordered an
unattended run; the containment list in §3 is what makes it defensible. Never enable it on your own
initiative, and never leave `--max-turns` off.

## 6. Morning check

The child's summary is a self-report. Verify before reporting success:

- `git log --oneline -5` in the target repo — did the commit land, on the right branch
- the tests it named, run by you
- the report file exists at the path you specified
- `git status --porcelain` — did it disturb files it was told to leave alone

Report `PRODUCED` / `TESTS-GREEN` / `COMMITTED` as separate states.

## Pitfalls

- **A prompt that asks a question at 3am gets a night of no work.** Any "confirm before proceeding" in
  the spec is a deadlock; replace it with a decision rule ("if X, take the narrower path and record it").
- **Do not bundle unrelated fixes.** A run that fails halfway leaves you unable to say which item broke.
  One item, one test, one revert point.
- **Do not let the agent choose the interpreter.** Absolute venv path, or it invents its own environment.
- **Tests written by an earlier session are not the spec.** Read them; if they encode the wrong
  contract, fixing them is part of the task, not a shortcut around it.
- **A free-running agent will "improve" adjacent code.** Name the files it may touch, and say that
  anything else is out of scope even if it looks broken.
- **Never hand over the prompt as an inline wall of prose.** A file plus one copy-paste block; he copies
  once and sleeps.
- **A pre-existing skill may forbid the permission flag outright.** That rule was written for attended
  runs. Do not silently violate it and do not obey it into a deadlock: state which rule you are
  overriding, why the order to run unattended authorizes it, and what containment replaces the gate.

## Appendix — prompt skeleton

`CONTEXT`: the work and why, three sentences; name the source of the findings and whether they were
independently reproduced.

`PRE-FLIGHT`: confirm branch and HEAD; `git status --porcelain` and list the pre-existing dirty and
untracked paths by name with "you did not make these"; adopt any prior session's files; take the lock
and stop if it is held.

`ENVIRONMENT`: repo venv python by absolute path; no installs into the deployed environment; no
service restarts.

`FIX ORDER`: severity order. Then per fix — file, function, line range; the bug mechanism; the exact
reproduction; the required behaviour; the constraint that must not change; the required tests as
assertions including the must-not-regress case.

`VERIFICATION`: the focused test command, the broader regression command, then any read-only live
smoke. If the live process needs a restart to pick up the change, note it and leave it alone.

`COMMIT`: exact `git-lane` command with the literal `REPO=` line; explicit paths only; no push, no PR,
no merge, no remote writes; stop rather than `--no-verify`.

`REPORT`: path; what changed with file:line, before/after per finding, verbatim test output, commit
sha, what remains unfinished, what was refused. End with three sentences in Bahasa Melayu.

`HARD STOPS`: three failed attempts on one item → revert that item only and move on; immutable trees;
`.bak` files; the pre-existing dirty files; no installs or restarts; ambiguity ⇒ HOLD.
