---
id: pull-discipline
name: GitHub Pull Discipline
version: 1.0.0
description: Pull is sync with reality. Pull before branching, before committing.
owner: AAA
risk_tier: low
glyph: "🜈"
position: 8 of 12 in the GitHub Canon
canonical_siblings:
  - branch-discipline
  - merge-protocol
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
    - forge_git_log
    - forge_git_status
    - forge_filesystem_read
version_lock:
  schema_version: '1'
  artifact_hash: 43feac4377ed4d2c
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜈 8. GitHub Pull Discipline

> *"Pull is sync with reality. Pull before branching, before committing."*
> — AAA GitHub Canon, position 8 of 12

## Purpose

Stay in sync with main (or the working branch). Resolve conflicts cleanly.

## When to Use

- Before starting new work on a branch — pull main
- Before pushing a branch — pull to catch up
- When conflicts appear during merge or rebase

## When NOT to Use

- Do NOT use `git pull --force` (it doesn't exist; if you want force, you mean `git fetch` + manual)
- Do NOT use to overwrite local commits without review

## Procedure

1. Fetch: `git fetch origin` (downloads remote refs without merging)
2. Inspect: `git log HEAD..origin/main --oneline` (what's new upstream)
3. Pull: `git pull --rebase origin main` (replay your commits on top; clean history)
4. Or: `git pull --no-rebase origin main` (merge commit; preserves your branch shape)
5. On conflict: read markers (`<<<<<<<`, `=======`, `>>>>>>>`), resolve intentionally, `git add`, `git rebase --continue`
6. Verify: `git status` clean, tests pass on the rebased branch

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_git_log` | pull-discipline operation |
| `forge_git_status` | pull-discipline operation |
| `forge_filesystem_read` | pull-discipline operation |

## Forbidden Actions

- NEVER force-push a branch others are using
- NEVER resolve conflicts blindly — read both sides
- NEVER pull into a dirty working tree (commit or stash first)

## Output

Local branch synchronized with remote; conflicts resolved (if any); tests pass

## Sibling Skills

- `branch-discipline`
- `merge-protocol`

---

*Position 8 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
