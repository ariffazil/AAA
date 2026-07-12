---
id: issue-literacy
name: GitHub Issue Literacy
version: 1.0.0
description: Issues are units of intent, uncertainty, and governance — not tickets.
owner: AAA
risk_tier: low
glyph: "🜁"
position: 1 of 12 in the GitHub Canon
canonical_siblings:
  - github-issue-triage
  - github-issues (OpenCode-scope monitor)
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
  - claude-code
  - codex
  - opencode
  - kimi-code
  - grok-build
  - copilot-cli
dependencies:
  skills: []
  servers:
    - a-forge
  tools:
    - forge_github_create_issue
    - forge_github_search_issues
    - forge_github_search_repos
version_lock:
  schema_version: '1'
  artifact_hash: 8e85c16fbe3fb4e1
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜁 1. GitHub Issue Literacy

> *"Issues are units of intent, uncertainty, and governance — not tickets."*
> — AAA GitHub Canon, position 1 of 12

## Purpose

Open, classify, label, route, and link Issues so every change in the federation starts with explicit, attributable intent.

## When to Use

- Before any code change — open or find an Issue first
- When intent crosses organ boundaries (multi-repo)
- When tracking a bug, feature, doctrine gap, or safety concern

## When NOT to Use

- Do NOT use for in-session note-taking (use forge_work/ instead)
- Do NOT use for personal todos (use memory/ instead)
- Do NOT close without documentation; never assign to Arif without his explicit ack

## Procedure

1. Open Issue with: title (clear intent) + body (context, evidence, risk, labels)
2. Classify: bug | feature | docs | question | routing-error | duplicate | spam
3. Label: `risk:low|medium|high|critical`, `organ:<x>`, `doctrine|runtime|tooling|AGI|ASI|needs-human`
4. Route: if wrong repo, draft polite redirect comment, apply `routing-error`
5. Detect duplicates: search open Issues in target repo, draft linking comment without closing
6. Anchor: every branch and PR must reference the Issue ID

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_github_create_issue` | issue-literacy operation |
| `forge_github_search_issues` | issue-literacy operation |
| `forge_github_search_repos` | issue-literacy operation |

## Forbidden Actions

- NEVER close without documenting why + waiting for ack
- NEVER assign to Arif without explicit ack
- NEVER write 'I will fix this' — only 'Routed to X organ for evaluation'
- NEVER apply wontfix/invalid without 888_JUDGE
- NEVER delete issue comments

## Output

Issue opened/labeled/routed with URL + classification + applied labels + duplicate-of ref + escalation flag

## Sibling Skills

- `github-issue-triage`
- `github-issues (OpenCode-scope monitor)`

---

*Position 1 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
