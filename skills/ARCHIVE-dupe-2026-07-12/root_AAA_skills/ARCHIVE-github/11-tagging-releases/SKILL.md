---
id: tagging-releases
name: GitHub Tagging & Releases
version: 1.0.0
description: Tags are frozen states of truth. The forge date IS the version.
owner: AAA
risk_tier: low
glyph: "🜋"
position: 11 of 12 in the GitHub Canon
canonical_siblings:
  - github-runbook
  - forensics-blame
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
    - github_release_create (via gh CLI)
version_lock:
  schema_version: '1'
  artifact_hash: 663bc03b0341209b
floor_scope:
  - F1
  - F2
  - F4
  - F11
  - F13
autonomy_tier: T1
---

# 🜋 11. GitHub Tagging & Releases

> *"Tags are frozen states of truth. The forge date IS the version."*
> — AAA GitHub Canon, position 11 of 12

## Purpose

Tag stable releases with date-stamp format. Link to CHANGELOG. Create historical anchors.

## When to Use

- After a merge to main that represents a stable state
- Before deploying to production
- When sealing a constitutional milestone (VAULT999 + tag)

## When NOT to Use

- Do NOT use semver (v1.2.3) — date-stamp only (vYYYY.MM.DD[-SUFFIX])
- Do NOT tag a commit that has not been merged to main
- Do NOT delete tags without explicit ack (tags are historical anchors)

## Procedure

1. Tag format: `vYYYY.MM.DD[-SUFFIX]` (e.g., `v2026.06.24`, `v2026.06.24-fiqhgeom`)
2. Tag locally: `git tag -a v2026.06.24 -m 'Forge milestone: <description>'`
3. Push tag: `git push origin v2026.06.24`
4. Create GitHub Release: optionally via UI or `gh release create v2026.06.24 --notes '<release notes>'`
5. Update CHANGELOG.md with the tagged version + summary
6. Seal to VAULT999 if the tag represents a constitutional milestone

## Allowed Tools

| Tool | Purpose |
|---|---|
| `forge_git_log` | tagging-releases operation |
| `forge_git_status` | tagging-releases operation |
| `github_release_create (via gh CLI)` | tagging-releases operation |

## Forbidden Actions

- NEVER use semver (v1.2.3) — date-stamp only
- NEVER tag a non-main commit as a release
- NEVER delete or move tags without explicit ack (F2 TRUTH — tags are historical)
- NEVER tag without updating CHANGELOG

## Output

Tag name + commit sha + release notes URL + CHANGELOG entry + (optional) VAULT999 seal

## Sibling Skills

- `github-runbook`
- `forensics-blame`

---

*Position 11 of 12 in the AAA GitHub Canon. Sovereign ruling 2026-06-24.*
*Consolidates and supersedes prior GitHub-related skills in the federation.*
*License: AGPL-3.0 · Sovereign: Arif bin Fazil*
*DITEMPA BUKAN DIBERI*
