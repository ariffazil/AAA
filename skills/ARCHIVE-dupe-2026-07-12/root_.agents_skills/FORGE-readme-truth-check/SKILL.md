---
id: readme-truth-check
name: FORGE-readme-truth-check
version: 1.0.0
description: Verify that a repo's README accurately describes its current structure,
  ports, dependencies, and authority boundaries. Detect drift between docs and reality.
owner: AAA
risk_tier: low
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
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - ΦΙ
  functional:
  - Governance
  layer: HEXAGON
  autonomy_tier: T1
floor_scope:
- F2
- F4
- F9
- F10
- F11
---

# README Truth Check

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


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
- [ ] Claimed: GEOX 18081 — Actual: 8081 (canonical GEOX MCP organ port is 8081; 18081 is arifosd)

### Dependency Drift
- [ ] None / [list]

### Recommendations
1. Update README directory structure — P1
```

---

*Skill version 1.0.0 — AAA Skill Library*