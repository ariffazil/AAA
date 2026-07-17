---
id: github-ops
name: FORGE-github-ops
version: 1.0.0
description: "Runbook for GitHub & Git operations across federation repos — commit workflow, PR ops, branch discipline."
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T1
tags: [github, git, runbook, ops]
---

# GitHub & Git Operations

## Federation Repos (7 active)
```
ariffazil/arifOS       — Constitutional kernel (Python 3.12+)
ariffazil/A-FORGE      — Execution engine (TypeScript/Node.js)
ariffazil/GEOX         — Earth intelligence (Python 3.11+)
ariffazil/wealth       — Capital intelligence (Python 3.12+)
ariffazil/well         — Vitality intelligence (Python 3.12+)
ariffazil/AAA          — Control plane (TypeScript/React)
—                      — APEX (DECOMMISSIONED — deliberation moved to AAA)
—                      — HERMES (local only, no remote)
```

## Git Status & Inspection
```bash
cd /root/<repo> && git status
cd /root/<repo> && git log --oneline -10
cd /root/<repo> && git diff
cd /root/<repo> && git remote -v
```

## Git Commit Workflow
```bash
cd /root/<repo>
git status                    # what changed?
git diff                      # review changes
git add .                     # stage everything
git commit -m "feat: <what>"  # commit
# NEVER: git push without ARIF confirmation
```

## Git Branch
```bash
git branch                    # list branches
git checkout -b <name>        # create and switch to new branch
git checkout main             # switch back to main
```

## GitHub Issue / PR Check
```bash
gh issue list -R ariffazil/arifOS --state open --limit 20
gh pr list -R ariffazil/arifOS --state open
gh pr view -R ariffazil/arifOS <number>
```

## Build & Test per Repo
```bash
# arifOS
cd /root/arifOS && pip install -e ".[dev]" && pytest tests/ -q

# A-FORGE
cd /root/A-FORGE && npm install && npm run build && npm test

# GEOX
cd /root/geox && pip install -e ".[dev]" && pytest tests/ -q

# WEALTH
cd /root/WEALTH && pip install -e . && python internal/monolith.py

# WELL
cd /root/WELL && pip install -e . && python test_well.py

# AAA
cd /root/AAA && npm install && npm run build && npm run lint

# HERMES
cd /root/HERMES && npm install && npm test
```

## GH CLI Auth Check
```bash
gh auth status
```

## Sensitive Actions (ask ARIF first)
- `git push` to main/master
- `git push --force`
- `git rebase`
- Deleting branches on remote
- Creating PRs that affect >1 repo
