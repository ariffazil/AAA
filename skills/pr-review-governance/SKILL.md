---
id: pr-review-governance
name: PR Review Governance
version: "1.0.0"
description: High-level governance layer for pull request review across the federation. Ensures separation of duties, required signers, and constitutional compliance before merge.
owner: AAA
risk_tier: high
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
    - github-pr-review
  servers:
    - github
  tools:
    - github-pr-fetch
    - github-pr-review
examples:
  - Govern a high-risk PR touching multiple organs
tests:
  - Verify engineer cannot self-approve irreversible PR
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# PR Review Governance

## Overview

Not all PRs are equal. This skill applies governance rules based on risk tier:

| Risk Tier | Required Reviewers | Judge Required? |
|-----------|-------------------|-----------------|
| low | 1 peer | No |
| medium | 1 peer + 1 architect | No |
| high | 2 peers + 1 auditor | Yes (888_JUDGE) |
| critical | All of above + Arif | Yes |

## When to Use

- Any PR marked `high` or `critical` risk
- Any PR touching constitutional files
- Any PR with >100 changed files
- Any PR deleting files

## Procedure

### Step 1: Risk Classification

Classify PR risk based on:
- Files touched
- Lines changed
- Repos affected
- Authority boundaries crossed

### Step 2: Assign Reviewers

Per risk tier, assign required reviewer roles:
- peer (same domain)
- architect (cross-domain)
- auditor (compliance)
- judge (888_JUDGE for high/critical)

### Step 3: Verify Separation of Duties

- Author ≠ approver
- Engineer cannot self-seal
- Proposer ≠ final approver for high-risk

### Step 4: Block or Approve

| Condition | Action |
|-----------|--------|
| All required reviewers approved | Merge allowed |
| Missing required reviewer | Block with comment |
| Self-approval detected | Block + escalate |
| Constitutional file changed | Block + 888_JUDGE |

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| Self-approval on high-risk PR | arifOS 888_JUDGE |
| Constitutional file changed | arifOS 888_JUDGE |
| Author disputes risk tier | Arif |

---

*Skill version 1.0.0 — AAA Skill Library*
