---
id: forensics-blame
name: GitHub Forensics & Blame
version: 1.0.0
description: Blame is lineage tracing. Essential for accountability.
owner: AAA
risk_tier: low
glyph: "🜌"
position: 12 of 12 in the GitHub Canon
canonical_siblings:
  - tagging-releases
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
    - forge_git_log
    - forge_git_diff
    - forge_filesystem_read
version_lock:
  schema_version: '1'
  artifact_hash: e7ea79ce48facb3d
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜌 12. GitHub Forensics & Blame

> *"Blame is lineage tracing. Essential for accountability."*
> — AAA GitHub Canon, position 12 of 12

## Purpose

Trace who changed what, when, and why. Use blame to debug regressions. Use bisect to find the breaking commit.

## When to Use

- When debugging a regression — when did this line change?
- When investigating a security incident — who introduced the vulnerable code?
- When understanding codebase history before refactoring
- When performing a post-mortem (incident → root cause → commit → actor)

## When NOT to Use

- Do NOT use blame as personal attack (it's a tool, not a verdict)
- Do NOT bisect on dirty trees (clean first)

## Procedure

1. Blame: `git blame <file>` (line-by-line: commit, author, timestamp)
2. Blame specific lines: `git blame -L 10,20 <file>`
3. Log with file history: `git log --follow -- <file>`
4. Pickaxe: `git log -S '<string>' --oneline` (find when a string was added/removed)
5. Bisect: `git bisect start` → `git bisect bad` → `git bisect good <known-good-sha>` → test each commit → `git bisect reset`
6. For constitutional forensics: cross-reference with VAULT999 seal IDs

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_git_log` | forensics-blame operation |
| `forge_git_diff` | forensics-blame operation |
| `forge_filesystem_read` | forensics-blame operation |

## Forbidden Actions

- NEVER weaponize blame in PR reviews (focus on the code, not the author)
- NEVER bisect without a known-good commit
- NEVER rely on blame for legal attribution — use VAULT999 seals for that

## Output

Commit history + actor list + line-level provenance + (optional) bisect-verified breaking commit

## Sibling Skills

- `tagging-releases`
- `github-runbook`

---

*Position 12 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
