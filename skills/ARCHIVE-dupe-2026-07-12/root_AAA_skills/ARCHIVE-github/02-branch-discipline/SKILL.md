---
id: branch-discipline
name: GitHub Branch Discipline
version: 1.0.0
description: Branches are parallel realities. Never edit main directly.
owner: AAA
risk_tier: low
glyph: "🜂"
position: 2 of 12 in the GitHub Canon
canonical_siblings:
  - github-runbook
  - worktree-mastery
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
    - forge_git_log
    - forge_filesystem_read
version_lock:
  schema_version: '1'
  artifact_hash: 03e97b6ee3c4a5f0
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜂 2. GitHub Branch Discipline

> *"Branches are parallel realities. Never edit main directly."*
> — AAA GitHub Canon, position 2 of 12

## Purpose

Create, switch, and manage feature/fix branches that anchor every experiment to an Issue ID.

## When to Use

- Before any code change — branch from main (or a stable tag)
- When you need to isolate an experiment
- When fanning out a single Issue into multiple parallel attempts

## When NOT to Use

- Do NOT use to edit main directly (F13 SOVEREIGN + branch protection)
- Do NOT use for long-lived personal branches (>30 days) — they become canon drift
- Do NOT use worktrees without first reading worktree-mastery

## Procedure

1. Pull main first: `git checkout main && git pull --rebase origin main`
2. Create branch: `git checkout -b <type>/<issue-n>-<slug>`
3. Branch name patterns: `feat/123-apex-lease-guard`, `fix/456-forge-sudo-path`, `doctrine/floor-6-upgrade`, `chore/<slug>`, `audit/<scope>-<date>`
4. One Issue → one primary branch (can fan out later via sub-branches)
5. Never switch branches with uncommitted changes (stash or commit first)

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_git_status` | branch-discipline operation |
| `forge_git_log` | branch-discipline operation |
| `forge_filesystem_read` | branch-discipline operation |

## Forbidden Actions

- NEVER commit to main directly (F13 SOVEREIGN)
- NEVER delete a remote branch without explicit ack
- NEVER force-push to a shared branch
- NEVER name branches with spaces or special chars

## Output

Branch name anchored to Issue ID; working tree clean; remote tracking configured

## Sibling Skills

- `github-runbook`
- `worktree-mastery`

---

*Position 2 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
