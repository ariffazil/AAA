---
id: pr-review-governance
name: PR Review Governance
version: 1.1.0
description: High-level governance layer for pull request review across the federation.
  Ensures separation of duties, required signers, and constitutional compliance before
  merge. This is the **policy layer** that decides who must approve. The **checklist**
  lives in `github-pr-review`; do not duplicate it here.
owner: AAA
risk_tier: high
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
  - github-pr-review
  - github-runbook
  servers:
  - a-forge
  tools:
  - forge_github_pr
  - forge_github_search
examples:
- Govern a high-risk PR touching multiple organs
- Block self-approval on critical PR before merge
tests:
- Verify engineer cannot self-approve irreversible PR
- Verify required reviewer counts match risk tier (peer/architect/auditor/judge)
version_lock:
  schema_version: '1'
  artifact_hash: d70dd7343dcdca63
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  layer: CODING/FI
  autonomy_tier: T3
floor_scope:
- F1
- F2
- F4
- F9
- F11
- F13
canonical_siblings:
- github-pr-review        # checklist (T2)
- github-ci-diagnose      # if CI red blocks signoff
- secret-safety-scan      # if PR touches secrets
---

# PR Review Governance

## Overview

Not all PRs are equal. This skill is the **policy layer** above `github-pr-review`.
Where `github-pr-review` answers *"what should I check on this PR?"*, this skill
answers *"who must approve it before it can merge?"*

Risk tier maps to required reviewer roles. T3 autonomy means this skill
**refuses to relax rules without 888_JUDGE** — separation of duties is the load-
bearing property.

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

## When NOT to Use

- **Do NOT use for low-risk single-line docs fixes** — over-process is entropy.
- **Do NOT use to override the checklist in `github-pr-review`** — this skill is policy, not procedure.
- **Do NOT use to merge** — branch protection + 888_JUDGE do that.

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


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