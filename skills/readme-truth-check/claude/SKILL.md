---
id: readme-truth-check
name: README Truth Check
version: "1.0.0"
description: Verify that a repo's README accurately describes its current structure, ports, dependencies, and authority boundaries. Detect drift between docs and reality.
owner: AAA
risk_tier: low
knowledge_basis:
  physics: false
  math: false
  language: true
host_compatibility:
  - claude-code
  - codex
  - opencode
dependencies:
  skills:
    - repo-hygiene-audit
  servers: []
  tools:
    - file-read
    - directory-list
examples:
  - Verify AAA README matches actual directory structure
tests:
  - Detect phantom directory referenced in README
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# README Truth Check

## Overview

READMEs become stale quickly. This skill compares the README's claims against the actual repo state and flags discrepancies.

## When to Use

- After any reorganization
- Before releasing a new version
- When onboarding a new developer
- Quarterly doc audit

## Procedure

### Step 1: Directory Structure Check

Compare README's directory tree against `ls -la`. Flag:
- Phantom directories (in README, not on disk)
- Missing directories (on disk, not in README)
- Renamed directories

### Step 2: Port/URL Check

Compare README's claimed ports/URLs against reality:
- `ss -tlnp` for listening ports
- `curl` for HTTP endpoints
- `systemctl status` for services

### Step 3: Dependency Check

Compare README's claimed dependencies against `package.json`, `pyproject.toml`, etc.

### Step 4: Authority Check

Verify README does not claim constitutional authority incorrectly.

## Output

```markdown
## README Truth Check: <repo>

### Structure Drift
- [ ] Phantom: `agent/` (README) vs `agents/` (disk)

### Port Drift
- [ ] Claimed: GEOX 8081 — Actual: 18081

### Dependency Drift
- [ ] None / [list]

### Recommendations
1. Update README directory structure — P1
```

---

*Skill version 1.0.0 — AAA Skill Library*
