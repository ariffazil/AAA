---
id: github-pr-review
name: GitHub PR Governance Review
version: "1.0.0"
description: Governed checklist for reviewing GitHub pull requests in the arifOS federation. Ensures PRs meet constitutional, structural, and safety standards before merge.
owner: AAA
risk_tier: medium
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
dependencies:
  skills:
    - repo-hygiene-audit
  servers:
    - github
  tools:
    - github-pr-fetch
    - file-diff
examples:
  - Review a cross-repo architectural PR before merge
tests:
  - Detect constitutional file changes in non-arifOS repos
  - Verify REPO= trailer in commit messages
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# GitHub PR Governance Review

## Overview

Every PR in the federation must pass a governance review before merge. This skill provides the canonical checklist.

## When to Use

- Any PR touching >1 file
- Any PR modifying contracts, schemas, or registries
- Any PR from an external contributor
- Any PR marked as "high risk" by the author

## Procedure

### Step 1: Scope Check

- [ ] PR touches only the repo it claims to touch
- [ ] No cross-repo changes without explicit approval
- [ ] Commit messages include `REPO=<owner/repo>` trailer

### Step 2: Authority Check

- [ ] No constitutional files added to non-arifOS repos
- [ ] No `ROOT_CANON.yaml`, `arifos.init`, or `floors.py` in diff
- [ ] No secret exposure (env files, tokens, keys)

### Step 3: Structural Check

- [ ] New files follow repo's canonical structure
- [ ] No phantom directories (referenced but empty)
- [ ] Tests added or updated for new logic

### Step 4: Safety Check

- [ ] No `rm -rf` or destructive commands
- [ ] No irreversible database migrations without rollback plan
- [ ] No force-push or rebase references

### Step 5: Verdict

| Result | Action |
|--------|--------|
| All checks pass | Approve with comment |
| Minor issues | Request changes with checklist |
| Authority violation | Request 888_JUDGE review |
| Secret exposure | Immediate HOLD + alert Arif |

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| Constitutional file changed | arifOS 888_JUDGE |
| Secret exposed | Arim + security.agent |
| Cross-repo architectural change | Arif |

---

*Skill version 1.0.0 — AAA Skill Library*
