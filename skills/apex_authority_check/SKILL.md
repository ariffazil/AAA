---
name: apex_authority_check
description: Detect conflicting or parallel source-of-truth claims across federation repositories and resolve the canonical owner. Use after repository reorganization, when instructions conflict, or during federation authority audits.
agent: 888-APEX
namespace: apex_*
cluster: IDENTITY
---

# Parallel Authority Detection

## Overview

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


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
