---
id: github-pr-review
name: GitHub PR Governance Review
version: "1.0.0"
status: DEPRECATED
deprecated_by: github-operations
redirect_to: github-operations §2 (pr-review mode)
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
replaced_by:
  skill: github-operations
  section: "§2 PR GOVERNANCE REVIEW"
  mode: pr-review
  effective_date: "2026-06-26"
  reason: "Unified into single github-operations skill covering issue + PR + CI"
---

# ⚠️ DEPRECATED — Use `github-operations` §2 Instead

> **This skill is deprecated.** Load `github-operations` instead and specify `mode="pr-review"`.
> This file is retained for reference only and will be removed in a future version.

**Old usage:**
```
skill_load(github-pr-review, pr_url=...)
```

**New usage:**
```
skill_load(github-operations, mode="pr-review", pr_url=...)
```

---

# GitHub PR Governance Review (DEPRECATED — see github-operations §2)

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
