---
id: repo-hygiene-audit
name: Repository Hygiene Audit
version: 1.0.0
description: Inspect a GitHub repo for structural chaos, authority conflicts, and
  cleanup needs. Produce an audit report and remediation plan.
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
dependencies:
  skills: []
  servers:
  - github
  tools:
  - github-search
  - file-read
  - directory-list
examples:
- Audit ariffazil/AAA for constitutional leaks and debris
tests:
- Detect duplicate authority files in wrong repos
- Detect stale references to moved directories
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  layer: HEXAGON
  autonomy_tier: T2
floor_scope:
- F2
- F4
- F9
- F10
- F11
---

# Repository Hygiene Audit

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


Repos absorb debris over time: duplicate authority files, stale references, runtime artifacts, backup dumps, and constitutional leaks. This skill systematically inspects a repo and produces a cleanup plan.

## When to Use

- After a major reorganization
- When onboarding a new repo to the federation
- When agent reports confusion about authority boundaries
- Quarterly federation-wide hygiene sweep

## When NOT to Use

- Do not use on live production repos without 888_HOLD
- Do not use to justify deleting constitutional files — those move to arifOS, not deleted
- Do not use as an excuse to skip arifOS judgment for irreversible actions

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| repo_path | yes | Local path or `owner/repo` GitHub slug |
| repo_role | yes | Expected role: kernel, control-plane, execution, domain |
| depth | no | Audit depth: quick (top-level only), standard (3 levels), deep (full) |

## Procedure

### Step 1: Authority Boundary Check

Verify the repo does not claim authority it does not own:

- **Constitutional files** (`CONSTITUTION.md`, `floors.py`, `judgment.py`, `vault999/`) — must live in `arifOS` only
- **Routing constitution** (`REPO_ROUTING_CONSTITUTION.md`) — must live in `arifOS` only
- **Agent init scripts** (`arifos.init`) — must live in `arifOS` only
- **Root canon files** (`ROOT_CANON.yaml`) — must live in `arifOS` only

If found in non-arifOS repos → flag as **constitutional leak**.

### Step 2: Runtime Debris Check

Look for artifacts that do not belong in a source repo:

- Backup directories (`*backup*`, `*archive*`, `*old*` at root)
- Workspace copies (full agent workspaces nested inside)
- Skill dumps (79 skill directories at root)
- Runtime state files (`.env` with secrets, session JSON, memory dumps)
- Large binary assets (>1MB images, PDFs without purpose)
- `node_modules/` at root (should not be committed)

### Step 3: Structural Check

Verify directory structure matches the repo's canonical role:

| Role | Expected Structure |
|------|-------------------|
| `kernel` (arifOS) | `core/`, `floors.py`, `judgment.py`, `vault999/`, `tests/` |
| `control-plane` (AAA) | `src/`, `a2a/`, `agents/`, `contracts/`, `registries/`, `public/` |
| `execution` (A-FORGE) | `src/`, `engine/`, `tools/`, `agents/`, `deploy/` |
| `domain` (GEOX/WEALTH/WELL) | `src/`, domain-specific engines, `tests/` |

Flag phantom directories (referenced but empty) and missing canonical directories.

### Step 4: Reference Integrity Check

Scan for broken references caused by moves/renames:

- `import` / `require` / `from` statements pointing to moved modules
- Markdown links to deleted files
- Config files referencing archived paths
- Git submodules pointing to dead remotes

### Step 5: Skill Registry Check

If repo is AAA or A-FORGE:

- Every skill in `registries/skills.yaml` must have a `skills/<id>/SKILL.md`
- Every skill directory must be registered
- No orphan skills (directory exists but not registered)

### Step 6: Produce Report

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `file-read` | Read config and documentation |
| `directory-list` | Inspect structure |
| `github-search` | Search across repo for patterns |
| `git-status` | Check for uncommitted changes |

## Forbidden Actions

- **NEVER** delete files during audit — only flag for review
- **NEVER** modify constitutional files — escalate to arifOS
- **NEVER** run `rm -rf` or `git push --force` — these require Arif approval
- **NEVER** dismiss findings as "not important" — all leaks are important

## Output Format

```markdown
## Skill Result: repo-hygiene-audit

### Summary
[One-paragraph summary of repo health]

### Authority Boundary
- [ ] No constitutional leaks
- [ ] OR: Leaks found: [list]

### Runtime Debris
- [ ] No debris
- [ ] OR: Debris found: [list with sizes]

### Structural Issues
- [ ] Structure matches canonical role
- [ ] OR: Issues: [list]

### Broken References
- [ ] No broken refs
- [ ] OR: Broken refs: [list]

### Skill Registry
- [ ] Registry consistent
- [ ] OR: Orphan skills: [list]

### Recommendations
1. [Action] — [Priority] — [Owner]
2. [Action] — [Priority] — [Owner]

### Escalations
- None / [list]
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Constitutional leak found | arifOS 888_JUDGE | A2A verdict_request |
| Secrets exposed | security.agent + Arif | Immediate HOLD + Telegram |
| Cross-repo architectural change | Arif | 888_HOLD + human approval |
| Deletion of >100 files proposed | Arif | 888_HOLD + human approval |

---

*Skill version 1.0.0 — AAA Skill Library*