---
name: skill-forensics
description: Auto-derives constitutional risk profile from any SKILL.md or tool before enabling or using it. Activates when: (1) a new skill is installed; (2) before any exec or tool call that is new or unfamiliar; (3) when Arif asks "what can this skill do, what are the risks". Reads the SKILL.md, extracts: capabilities, risks, irreversible operations, required floors, and generates an arifOS-ready risk brief.
metadata: {"openclaw": {"emoji": "🔍"}}
---

# Skill Forensics — Auto-Constitutional Analysis

Before enabling any new skill or running any unfamiliar tool, run forensics. This reads the SKILL.md (or tool documentation) and outputs an arifOS constitutional risk profile — what it can do, what could go wrong, which floors it implicates, and what the irreversible operations are.

## When to Run

- New skill installed via ClawHub or manual copy
- Before using any exec command that modifies state
- When Arif asks: "what are the risks of this skill"
- When a plugin or tool has no SKILL.md

## Forensics Checklist

### 1. Read the SKILL.md (or tool --help)
```bash
cat <skill-dir>/SKILL.md
# Or for CLI tools:
<tool> --help
```

### 2. Extract Capabilities
List every action the skill/tool can perform. Mark which are:
- Read-only (TRIVIAL)
- State-changing (REVERSIBLE or CRITICAL)
- Destructive (IRREVERSIBLE)

### 3. Identify Risk Operations
Look for:
- `exec`, `rm`, `delete`, `write` → IRREVERSIBLE if outside /tmp
- External network calls → CRITICAL (cost, data leakage risk)
- File system writes → CRITICAL if outside workspace
- API key usage → CRITICAL (credential exposure)
- Spawn/subagent creation → CRITICAL (uncontrolled agent launch)

### 4. Map to Constitutional Floors
Which floors does this skill implicate?

| Floor | Risk Signal |
|---|---|
| **Amanah (accuracy)** | Tool makes quantitative claims? May overclaim |
| **Kesederhanaan (reversibility)** | Destructive operations present? |
| **Kelayakan (viability)** | Requires bins/env/config present? |
| **Kemandirian (independence)** | Calls external APIs? May be influenced |
| **Kedaulatan (sovereignty)** | Makes irreversible decisions? Requires Arif veto |

### 5. Generate Risk Brief

## Output Format

```
SKILL FORENSICS REPORT: <skill-name>
═══════════════════════════════════════

CAPABILITY SUMMARY:
[Bullet list of all actions, tagged TRIVIAL/REVERSIBLE/CRITICAL/IRREVERSIBLE]

RISK OPERATIONS (require HOLD):
[Bullet list of operations that could cause harm or are irreversible]

FLOORS IMPLICATED:
[1, 3, 5, 6, 13] — floor names

REVERSIBILITY:
[fully reversible / partial / largely irreversible]

IRREVERSIBLE OPERATIONS (require 888_HOLD):
[List]

GAPS / UNKNOWN:
[What is unclear from the SKILL.md — bins not checked, env vars not verified]

ARIF OS VERDICT:
[SEAL — safe to use / CAUTION — proceed with monitoring / HOLD — review required]
```

## Example

For a hypothetical `image-generator` skill:
```
CAPABILITY SUMMARY:
- Generate image from text (TRIVIAL — no state change)
- Save to specified path (REVERSIBLE — file can be deleted)
- Batch generate (CRITICAL — cost, disk space)

RISK OPERATIONS:
- Overwrite existing files (CRITICAL)
- Consume API quota rapidly (CRITICAL)

FLOORS IMPLICATED:
5 (Kesederhanaan — disk space), 10 (Kelayakan — quota)

REVERSIBILITY: Fully reversible (output files only)

IRREVERSIBLE OPERATIONS: None

ARIF OS VERDICT: CAUTION — add mmx-quota-guard check before batch use
```

## Auto-Log

After forensics, append to `memory/vault999-triage.md`:
```
HH:MM UTC | forensics | <skill-name> | verdict: [SEAL/CAUTION/HOLD] | floors: [N,N]
```
