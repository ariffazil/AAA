---
id: github-issue-triage
name: GitHub Issue Triage
version: "1.0.0"
status: DEPRECATED
deprecated_by: github-operations
redirect_to: github-operations §1 (issue-triage mode)
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
  section: "§1 ISSUE TRIAGE"
  mode: issue-triage
  effective_date: "2026-06-26"
  reason: "Unified into single github-operations skill covering issue + PR + CI"
---

# ⚠️ DEPRECATED — Use `github-operations` §1 Instead

> **This skill is deprecated.** Load `github-operations` instead and specify `mode="issue-triage"`.
> This file is retained for reference only and will be removed in a future version.

**Old usage:**
```
skill_load(github-issue-triage, issue_url=...)
```

**New usage:**
```
skill_load(github-operations, mode="issue-triage", issue_url=...)
```

---

# GitHub Issue Triage (DEPRECATED — see github-operations §1)

## Overview

Issues are the ingress surface of federation chaos. An unlabeled issue in the
wrong repo is entropy. This skill compresses that entropy into structure.

## When to Use

- New issue opened with no labels
- Issue appears to be in the wrong repo
- Issue references multiple federation organs
- Agent needs to understand if issue is duplicate, spam, or valid

## When NOT to Use

- Do NOT use if issue requires immediate code fix — escalate to A-FORGE engineer
- Do NOT use if issue reports secret exposure — escalate to secret-safety-scan
- Do NOT use if issue is a constitutional violation — escalate to 888_JUDGE

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| issue_url | yes | Full GitHub issue URL |
| repo_context | yes | Which repo the issue lives in |
| existing_labels | no | Current labels on the issue |

## Procedure

### Step 1: Read & Classify

Read the issue title and body. Classify into exactly one bucket:

- `bug` — something is broken
- `feature` — new capability requested
- `docs` — documentation incorrect or missing
- `question` — user needs clarification
- `routing-error` — issue filed in wrong repo
- `duplicate` — identical to existing issue
- `spam/void` — noise, not actionable

### Step 2: Authority & Routing Check

Use the canonical repo map:

| Keyword / Domain | Correct Repo |
|------------------|--------------|
| F1–F13, constitutional, floors, vault, judge | ariffazil/arifos |
| agent engine, build, orchestration, TypeScript | ariffazil/A-FORGE |
| petrophysics, well logs, seismic, earth | ariffazil/geox |
| finance, capital, portfolio, NPV, risk | ariffazil/wealth |
| vitality, metabolic, WELL, health | ariffazil/well |
| control plane, AAA, routing, skills | ariffazil/AAA |
| website, static, arif-fazil.com | ariffazil/arif-sites |

If issue is in wrong repo:
- Draft a polite comment: "Thanks for filing. This belongs in [correct-repo] because [reason]."
- Apply `routing-error` label.
- Do NOT close. Let sovereign or repo owner transfer it.

### Step 3: Duplicate Detection

Search open issues in target repo for similar titles. If duplicate found:
- Draft comment: "This appears to be a duplicate of #XXX. Closing as duplicate is gated — please confirm."
- Do NOT close without Arif ack.

### Step 4: Label & Respond

Apply labels based on classification:
- `bug`, `feature`, `docs`, `question`, `routing-error`, `duplicate`
- Add organ label if cross-organ: `organ:arifos`, `organ:geox`, etc.
- Add risk tier if obvious: `risk:low`, `risk:medium`, `risk:high`

Draft response comment:
- Acknowledge the issue
- State classification
- State routing (if applicable)
- State next step (e.g., "Awaiting sovereign review for priority")
- NEVER promise a fix timeline
- NEVER assign to Arif without his explicit ack

### Step 5: Evidence Log

Append a line to your internal reasoning trace:
```
[ISSUE-TRIAGE] <issue-url> | <classification> | <routing> | <labels-applied>
```

## Forbidden Actions

- **NEVER** close an issue without documenting why and waiting for ack
- **NEVER** assign to Arif without his explicit ack
- **NEVER** write "I will fix this" — only "Routed to X organ for evaluation"
- **NEVER** apply `wontfix` or `invalid` without 888_JUDGE
- **NEVER** delete issue comments

## Output Format

```markdown
## Issue Triage Result

- **Issue:** <url>
- **Classification:** <bucket>
- **Routing:** <same-repo | target-repo>
- **Labels Applied:** <list>
- **Duplicate Of:** <issue-number-or-none>
- **Response Drafted:** <yes/no>
- **Escalation Required:** <none | 888_JUDGE | secret-safety-scan | A-FORGE>
```
