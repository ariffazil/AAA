---
id: github-issue-triage
name: GitHub Issue Triage
version: 1.1.0
description: 'Governed triage workflow for GitHub issues across the arifOS federation.
  Use this skill whenever a new issue is opened, an issue lacks labels, or an agent
  needs to determine if it belongs in a different repo or federation organ.
  This skill classifies, routes, labels, and drafts responses — but never closes,
  never assigns to Arif, and never promises code fixes without sovereign approval.'
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
dependencies: {}
  servers:
  - a-forge
  tools:
  - forge_github_search  # forge_github_search_issues not in /mcp/aforge/ — use forge_github_search
  - forge_github_search  # forge_github_search_repos not in /mcp/aforge/ — use forge_github_search
  - forge_github_pr  # forge_github_create_issue not in /mcp/aforge/ — use GitHub MCP server directly
  - forge_filesystem_read  # forge_github_get_file not in /mcp/aforge/
examples:
- New issue opened in ariffazil/arifos with no labels — triage it
- Issue about GEOX well logs filed in AAA repo — route it correctly
- Detect duplicate of an existing issue and link them
tests:
- Correctly classify a bug report vs feature request vs question
- Route a constitutional floor issue to arifOS, not A-FORGE
- Detect duplicate issue and draft linking comment without closing
- Never apply `wontfix` or `invalid` without 888_JUDGE seal
version_lock:
  schema_version: '1'
  artifact_hash: e69fa003f336111c
orthogonal_tags:
  trinitarian:
  - Ω
  - Δ
  - ΦΙ
  functional:
  - Ops
  layer: CODING/FI
  autonomy_tier: T1
floor_scope:
- F1
- F2
- F4
- F6
- F11
- F13
canonical_siblings:
- github-issues           # OpenCode-scope: monitoring shell (gh CLI)
- github-pr-review        # post-triage, when issue graduates to PR
- github-ci-diagnose      # if issue reports CI failure
- secret-safety-scan      # if issue smells like secret exposure
---

# GitHub Issue Triage

## Overview

Issues are the ingress surface of federation chaos. An unlabeled issue in the
wrong repo is entropy. This skill compresses that entropy into structure —
classify, route, label, draft — without closing or assigning without sovereign
ack.

This skill is the **governance workflow** for triaging. The OpenCode-scope
skill `github-issues` is the **monitoring shell** that polls the federation
with `gh issue list`. Use this skill to act on what `github-issues` reports.

## When to Use

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


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