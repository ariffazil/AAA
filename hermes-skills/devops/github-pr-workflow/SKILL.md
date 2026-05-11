---
name: github-pr-workflow
description: Bulk PR operations and jq quirks for arifOS GitHub org — multi-repo status checks, self-approval blocks, merge sequencing.
category: devops
---

# GitHub PR Workflow (arifOS Federation)

## Multi-Repo PR Status Check
```bash
# List open PRs across 4 repos
for repo in arifOS A-FORGE GEOX WEALTH; do
  gh pr list --repo "ariffazil/$repo" --state open --json number,title,baseRefName --jq '.[] | "  #\(.number) \(.baseRefName)"'
done
```

## Bulk PR Inspection (mergeable, review, checks)
```bash
gh pr view N --repo owner/repo --json title,mergeable,reviewDecision,mergeStateStatus,statusCheckRollup --jq '{title, mergeable, review: .reviewDecision, state: .mergeStateStatus, checks: [.statusCheckRollup[] | .status]}'
```

**Key jq gotchas:**
- `gh pr list` — no `base` field, use `baseRefName`
- `gh pr view --json statusCheckRollup` — returns array of CheckRun objects, NOT a summary object. Cannot use `.status` or `.counts` directly. Must iterate: `[.statusCheckRollup[] | .status]`

## Self-Approval Block
Branch protection with "require 1 review" prevents the PR author from approving their own PR:
```
GraphQL: "Review Can not approve your own pull request"
```
**Workarounds:**
1. Owner approves manually (GitHub UI)
2. Add bot as collaborator with write access
3. Relax branch protection to "dismiss stale reviews"

## Merge Sequence (arifOS federation)
arifOS must merge FIRST (constitutional law), then A-FORGE/GEOX/WEALTH in any order:
```bash
gh pr merge 402 --repo ariffazil/arifOS --squash --delete-branch
# Then:
gh pr merge 5 --repo ariffazil/A-FORGE --squash --delete-branch
gh pr merge 30 --repo ariffazil/GEOX --squash --delete-branch
gh pr merge 5 --repo ariffazil/WEALTH --squash --delete-branch
```

## Pre-Merge Checklist
- [ ] All checks ✅ COMPLETED
- [ ] PR MERGEABLE (not blocked by conflicts)
- [ ] Review approved (not self-approved)
- [ ] Merge sequence respected (arifOS → others)
