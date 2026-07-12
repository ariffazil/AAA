---
id: commit-craftsmanship
name: GitHub Commit Craftsmanship
version: 1.0.0
description: Commits are atomic thoughts. Small, meaningful, attributable.
owner: AAA
risk_tier: low
glyph: "🜃"
position: 3 of 12 in the GitHub Canon
canonical_siblings:
  - github-runbook
  - staging-awareness
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
    - forge_git_diff
    - forge_git_status
    - forge_git_commit
version_lock:
  schema_version: '1'
  artifact_hash: fc642c044e400294
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜃 3. GitHub Commit Craftsmanship

> *"Commits are atomic thoughts. Small, meaningful, attributable."*
> — AAA GitHub Canon, position 3 of 12

## Purpose

Stage intentionally, commit small changes, write clear messages — produces clean lineage and reversible history.

## When to Use

- After a coherent unit of change is ready
- Before switching branches
- When you want to checkpoint without pushing

## When NOT to Use

- Do NOT use for dump commits (`git commit -am 'stuff'`)
- Do NOT use to bundle unrelated changes — split into multiple commits
- Do NOT use without first running `git diff --stat` to verify the change set

## Procedure

1. Inspect: `git status` + `git diff --stat` + `git diff` (review every line)
2. Stage intentionally: `git add <file>` — never `git add .` without review
3. Write message: `<type>(<scope>): <short description>` — max 72 chars subject
4. Body: wrap at 100 chars, explain WHY not WHAT
5. Footer: `REPO=<owner/repo>` for federation commits; co-authors; `BREAKING CHANGE:` if applicable
6. Commit types: feat, fix, docs, refactor, test, chore, forge(<scope>)

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_git_diff` | commit-craftsmanship operation |
| `forge_git_status` | commit-craftsmanship operation |
| `forge_git_commit` | commit-craftsmanship operation |

## Forbidden Actions

- NEVER commit secrets, .env files, or unredacted credentials
- NEVER skip `git diff` review before `git add .`
- NEVER amend a commit that has been pushed (write a new commit)
- NEVER write vague messages like 'fix' or 'update'

## Output

Commit hash + subject + body + footer; total files changed; total lines added/removed

## Sibling Skills

- `github-runbook`
- `staging-awareness`

---

*Position 3 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
