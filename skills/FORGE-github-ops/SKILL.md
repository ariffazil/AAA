---
id: github-ops
name: FORGE-github-ops
version: 1.1.0
description: "Runbook for GitHub & Git operations across federation repos — commit workflow, PR ops, branch discipline. v1.1.0: organ paths from organ registry, no hardcoded /root/<repo> paths."
owner: AAA
risk_tier: low
floor_scope: [F1, F2, F11]
autonomy_tier: T1
tags: [github, git, runbook, ops]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# GitHub & Git Operations (Probe-Based v1.1.0)

## Federation Repos — Discover from Organ Registry

**DO NOT hardcode repo paths.** Read them from the canonical organ registry:

```bash
python3 -c "
import yaml
with open('/root/AAA/federation/organs.yaml') as f:
    reg = yaml.safe_load(f)
for o in reg.get('organs', []):
    print(f'{o[\"id\"]:12s} src={o.get(\"source_path\",\"?\")}')
"
```

For GitHub org/repo names, probe git remotes:
```bash
git -C <source_path> remote get-url origin
# e.g. git@github.com:ariffazil/arifOS.git → org=ariffazil, repo=arifOS
```

## Git Status & Inspection (per organ, from registry)

```bash
# For each organ's source_path from registry:
git -C <source_path> status
git -C <source_path> log --oneline -10
git -C <source_path> diff
git -C <source_path> remote -v
```

## Git Commit Workflow

```bash
# Replace <source_path> with organ registry value
cd <source_path>
git status                    # what changed?
git diff                      # review changes
git add .                     # stage everything
git commit -m "feat: <what>"  # commit
# NEVER: git push without ARIF confirmation (F13 SOVEREIGN)
```

## Git Branch (per repo)

```bash
git -C <source_path> branch                    # list branches
git -C <source_path> checkout -b <name>         # create and switch
git -C <source_path> checkout main              # switch back
```

## GitHub Issue / PR Check — Org/Repo from git remote

```bash
# Derive org/repo from: git -C <source_path> remote get-url origin
ORG_REPO="ariffazil/arifOS"  # EXAMPLE — probe actual value
gh issue list -R "$ORG_REPO" --state open --limit 20
gh pr list -R "$ORG_REPO" --state open
gh pr view -R "$ORG_REPO" <number>
```

## Build & Test — Per-Organ (paths from registry)

```bash
# arifOS
cd $(python3 -c "import yaml;r=yaml.safe_load(open('/root/AAA/federation/organs.yaml'));print([o['source_path'] for o in r['organs'] if o['id']=='arifos'][0])") && pip install -e ".[dev]" && pytest tests/ -q

# A-FORGE
cd $(python3 -c "import yaml;r=yaml.safe_load(open('/root/AAA/federation/organs.yaml'));print([o['source_path'] for o in r['organs'] if o['id']=='aforge'][0])") && npm install && npm run build && npm test

# GEOX
cd $(python3 -c "import yaml;r=yaml.safe_load(open('/root/AAA/federation/organs.yaml'));print([o['source_path'] for o in r['organs'] if o['id']=='geox'][0])") && pip install -e ".[dev]" && pytest tests/ -q

# Same pattern for WEALTH, WELL, AAA — probe source_path from registry
```

**Rule:** Every path in this document that starts with `/root/` is an EXAMPLE. Replace with the live organ registry value. If a path doesn't match the registry, the registry wins.

## GH CLI Auth Check

```bash
gh auth status
```

## Sensitive Actions (ask ARIF first — F13 SOVEREIGN)
- `git push` to main/master
- `git push --force`
- `git rebase`
- Deleting branches on remote
- Creating PRs that affect >1 repo

## De-hardcoding Log (v1.1.0)
- Replaced all hardcoded `/root/<repo>` paths with organ registry reads
- GitHub org/repo names derived from `git remote get-url origin`
- Build commands now use registry-derived source_paths
- Added explicit rule: hardcoded paths are EXAMPLES, registry is truth
