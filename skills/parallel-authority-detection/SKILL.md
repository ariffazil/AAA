---
id: parallel-authority-detection
name: Parallel Authority Detection
version: "1.0.0"
description: Detect when two or more repos claim the same authority, responsibility, or canonical source of truth. Resolve conflicts through ROOT_CANON.yaml precedence.
owner: AAA
risk_tier: high
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
    - github-search
    - file-read
examples:
  - Detect both AAA and arifOS claiming 888_JUDGE authority
tests:
  - Find duplicate `CONSTITUTION.md` files across repos
version_lock:
  schema_version: "1"
  artifact_hash: pending
---

# Parallel Authority Detection

## Overview

When two repos claim to be the "source of truth" for the same thing, agents get confused and chaos follows. This skill detects parallel authority claims.

## When to Use

- After any repo reorganization
- When agents report conflicting instructions
- Quarterly federation authority audit

## Procedure

### Step 1: File Collision Scan

Search all federation repos for files with the same name:
- `CONSTITUTION.md`
- `floors.py`
- `judgment.py`
- `ROOT_CANON.yaml`
- `arifos.init`
- `REPO_ROUTING_CONSTITUTION.md`

### Step 2: Content Comparison

If duplicates found, compare contents. Identical = copy. Different = conflict.

### Step 3: Precedence Resolution

Per `ROOT_CANON.yaml` (arifOS):
- `arifOS` wins for constitutional files
- `AAA` wins for agent cards and routing
- `A-FORGE` wins for build/deployment

### Step 4: Report

Flag each conflict with recommended owner and migration path.

## Escalation Path

| Condition | Escalate To |
|-----------|-------------|
| Constitutional conflict | arifOS 888_JUDGE |
| Cross-repo boundary dispute | Arif |

---

*Skill version 1.0.0 — AAA Skill Library*
