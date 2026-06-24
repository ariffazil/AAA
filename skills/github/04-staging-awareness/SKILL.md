---
id: staging-awareness
name: GitHub Staging Awareness
version: 1.0.0
description: Staging is the thinking buffer. Three states: working / staged / committed.
owner: AAA
risk_tier: low
glyph: "🜄"
position: 4 of 12 in the GitHub Canon
canonical_siblings:
  - commit-craftsmanship
  - github-runbook
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
    - forge_git_status
    - forge_git_diff
    - forge_filesystem_read
version_lock:
  schema_version: '1'
  artifact_hash: d6020ae66ea6311c
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜄 4. GitHub Staging Awareness

> *"Staging is the thinking buffer. Three states: working / staged / committed."*
> — AAA GitHub Canon, position 4 of 12

## Purpose

Always know which state your changes are in. Prevents accidental commits and lost work.

## When to Use

- Before every commit — verify what's actually staged
- When resuming work after a break
- When debugging 'where did my change go?'

## When NOT to Use

- Do NOT use to commit secrets (F1)
- Do NOT use to bypass review (staging is not commit)

## Procedure

1. Three states: working tree (untracked + modified) / staging area (index) / committed (HEAD)
2. Inspect: `git status` (state map) + `git diff` (working vs staged) + `git diff --cached` (staged vs HEAD)
3. Move selectively: `git add <file>` (working → staged), `git restore <file>` (working discard), `git restore --staged <file>` (unstage)
4. Avoid blanket `git add .` — review first
5. Use `git stash` for temporary saves when switching context
6. Use `git stash pop` to restore — never lose work

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_git_status` | staging-awareness operation |
| `forge_git_diff` | staging-awareness operation |
| `forge_filesystem_read` | staging-awareness operation |

## Forbidden Actions

- NEVER `git add .` without explicit review
- NEVER `git restore` committed history without confirmation
- NEVER stash and forget (always come back)

## Output

Current state map: X files modified, Y staged, Z untracked, branch at <sha>

## Sibling Skills

- `commit-craftsmanship`
- `github-runbook`

---

*Position 4 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
