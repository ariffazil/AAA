---
id: worktree-mastery
name: GitHub Worktree Mastery
version: 1.0.0
description: Worktrees are parallel working universes. Multiple branches, one working tree.
owner: AAA
risk_tier: low
glyph: "🜊"
position: 10 of 12 in the GitHub Canon
canonical_siblings:
  - branch-discipline
  - pull-discipline
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
    - forge_filesystem_read
    - forge_git_status
    - forge_git_log
version_lock:
  schema_version: '1'
  artifact_hash: b3b0e2c3f9f37e7d
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜊 10. GitHub Worktree Mastery

> *"Worktrees are parallel working universes. Multiple branches, one working tree."*
> — AAA GitHub Canon, position 10 of 12

## Purpose

Work on multiple branches simultaneously without switching context. Increases parallelism without chaos.

## When to Use

- When you need to test multiple branches side-by-side
- When switching branches would lose context (uncommitted experimental changes)
- When running long-lived processes (servers, watchers) on one branch while editing another

## When NOT to Use

- Do NOT use to circumvent branch discipline (still needs Issue anchor)
- Do NOT create worktrees without cleaning them up later (orphan worktrees drift)

## Procedure

1. Create: `git worktree add ../<repo>-<branch> <branch>`
2. List: `git worktree list`
3. Each worktree is its own working directory — cd into it to operate on that branch
4. Remove: `git worktree remove ../<repo>-<branch>` (after merging or abandoning)
5. Prune: `git worktree prune` (cleans up stale references)

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_filesystem_read` | worktree-mastery operation |
| `forge_git_status` | worktree-mastery operation |
| `forge_git_log` | worktree-mastery operation |

## Forbidden Actions

- NEVER create a worktree of the same branch twice (conflict)
- NEVER delete a worktree with uncommitted changes (data loss)
- NEVER use worktrees to bypass F13 SOVEREIGN on main — main worktrees still branch-protected

## Output

Worktree path + branch + parent repo; list of active worktrees; cleanup plan

## Sibling Skills

- `branch-discipline`
- `pull-discipline`

---

*Position 10 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
