---
id: github-runbook
name: GitHub Runbook - Federation Git and CLI Operations
version: 1.0.0
description: Basic git status, commit, branch, and GitHub CLI operations across the
  federation repos.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
dependencies:
  skills:
  - arifos-act
  servers: []
  tools: []
examples:
- Check working tree status and recent commits for arifOS
- Stage, commit, and diff changes in a federation repo
- List open issues and PRs with the GitHub CLI
- Create a feature branch before starting work
tests:
- git status returns expected state for a clean working tree
- gh issue list returns open issues for a known repo
- Skill refuses to push, force-push, or rebase without escalation
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  functional:
  - Ops
  layer: CODING/FI
  autonomy_tier: T1-T2
floor_scope:
- F1
- F2
- F4
- F10
- F11
- F13
---

# GitHub Runbook — Federation Git & CLI Operations

## Overview

This skill provides the standard operating procedure for inspecting and mutating git state across the arifOS federation repositories. It covers read-only inspection (`status`, `log`, `diff`, `remote`), local mutations (`add`, `commit`, `branch`), and GitHub CLI queries (`gh issue list`, `gh pr list`). It is a T1–T2 routing/ops runbook: safe to read, restricted to write.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.

## When to Use

- You need to inspect repository state before or after work.
- You need to commit local changes on a feature branch.
- You need to create or switch branches.
- You need to list or view open issues and pull requests.
- You need a quick build/test sanity check per repo.

## When NOT to Use

- **Do not use to push to `main` or any protected branch.** Escalate to Arif (F13 SOVEREIGN).
- **Do not use for `git push --force`, `git rebase`, or destructive branch deletion.** These are 888 HOLD actions.
- **Do not use to create cross-repo PRs or architectural refactors without prior constitutional judgment.**
- **Do not treat `git commit` as a substitute for `make test` or review.** Commit only after local validation.
- For secret exposure, suspected credential leakage, or unauthorized access → escalate to `security.agent` + arifOS 888_JUDGE.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| repo_path | yes | Absolute path to a federation repo (e.g., `/root/arifOS`) |
| operation | yes | One of: `status`, `log`, `diff`, `branch`, `checkout`, `commit`, `gh-issue`, `gh-pr`, `build-test` |
| branch_name | conditional | Required for `checkout -b` or switching branches |
| commit_message | conditional | Required for `git commit`; must use conventional-commit style |

## Procedure

### Step 1: Read-Only Inspection

Run these before any mutation:

```bash
cd /root/<repo>
git status                    # working tree state
git log --oneline -10         # recent history
git diff                      # unstaged changes
git remote -v                 # configured remotes
```

### Step 2: Local Commit Workflow

```bash
cd /root/<repo>
git status
git diff
git add .
git commit -m "<type>: <short description>"
```

Commit message style: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`.

### Step 3: Branch Management

```bash
git branch                    # list local branches
git checkout -b <branch>      # create and switch
git checkout main             # return to main
```

### Step 4: GitHub CLI Queries

```bash
gh auth status                # verify authentication
gh issue list -R ariffazil/<repo> --state open --limit 20
gh pr list -R ariffazil/<repo> --state open
gh pr view -R ariffazil/<repo> <number>
```

### Step 5: Per-Repo Build & Test Sanity

| Repo | Command |
|------|---------|
| arifOS | `cd /root/arifOS && uv sync --frozen && python -m pytest tests/ -q` |
| A-FORGE | `cd /root/A-FORGE && npm install && npm run build && npm test` |
| GEOX | `cd /root/geox && uv sync --frozen && PYTHONPATH=src pytest tests/ -q` |
| WEALTH | `cd /root/WEALTH && uv sync --frozen && make test` |
| WELL | `cd /root/WELL && uv sync --frozen && make test` |
| AAA | `cd /root/AAA && npm install && npm run build && npm run lint` |
| arif-sites | `cd /root/arif-sites && npm install && npm run build` |
| HERMES | `cd /root/HERMES && npm install && npm test` (local only, no remote) |

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `git` | Local repository inspection and mutation |
| `gh` | GitHub CLI read-only queries and authenticated status |
| `Bash` | Change directory and run repo-specific build/test commands |

## Forbidden Actions

- **NEVER** `git push` to `main` or any protected branch without F13 confirmation.
- **NEVER** `git push --force` under any circumstances.
- **NEVER** run `git rebase` or interactive rebase without 888 HOLD.
- **NEVER** delete remote branches or tags without explicit authorization.
- **NEVER** create PRs affecting more than one repo without architectural judgment.
- **NEVER** stage or commit secrets, `.env` files, or unredacted credentials.
- **NEVER** skip `git diff` review before `git add .`.
- Escalate to **arifOS 888_JUDGE** if a commit touches constitutional files (`GENESIS/`, `AGENTS.md`, `VAULT999/` lineage) or if blast radius exceeds the current repo.

## Output Format

```markdown
## Skill Result: github-runbook

### Summary
One-paragraph summary of what was inspected or changed.

### Evidence
- Repo inspected: <path>
- Operation performed: <status/log/diff/commit/branch/gh-issue/gh-pr/build-test>
- Working tree state: <clean / modified / untracked>
- Recent commits: <list if relevant>
- Build/test result: <pass / fail / skipped>

### Recommendations
- Next safe action, or
- Why further action requires escalation

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Push to main or protected branch needed | Arif (F13 SOVEREIGN) | 888 HOLD |
| Force-push, rebase, or remote deletion needed | arifOS 888_JUDGE | verdict_request |
| Secrets found in working tree | security.agent + arifOS judge | A2A message |
| Constitutional files affected | arifOS 888_JUDGE | A2A verdict_request |
| Cross-repo PR or architectural change | arifOS 888_JUDGE + Arif | hold with reason |
| Build/test failure after commit | Repo owner / A-FORGE | issue or task |

---

*Skill version 1.0.0 — AAA Skill Library*
