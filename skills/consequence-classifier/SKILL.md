---
name: consequence-classifier
description: Classifies every incoming request into consequence bands to drive arifOS-sense automatically. Activates when: (1) any user request arrives; (2) before taking any action; (3) when Arif asks to assess risk of something. Outputs a band + recommended verdict (SEAL/CAUTION/HOLD/VOID) and whether 888_HOLD is required. Makes governance-driven — not vibes-driven.
metadata: {"openclaw": {"emoji": "⚖️"}}
---

# Consequence Classifier — Risk Band for Every Action

Before any consequential action, classify it. This feeds directly into arifOS-sense to auto-trigger 888_HOLD when needed — not as a suggestion, but as a mandatory gate.

## The Four Bands

| Band | Definition | arifOS Verdict | 888_HOLD Required |
|---|---|---|---|
| **TRIVIAL** | Read-only, no state change, no external effect | `SEAL` | No |
| **REVERSIBLE** | State changes but can be undone; no external parties affected | `CAUTION` | No |
| **CRITICAL** | Significant state change, external API calls, financial impact | `HOLD` | Yes — pending human review |
| **IRREVERSIBLE** | Permanent deletion, irreversible writes, identity-shaping | `VOID` → `HOLD` | **YES — explicit Arif approval required** |

## Classification Checklist

Run this on every request:

### Step 1 — Scope Check
- [ ] Does this change any file, database, or state? → If NO → TRIVIAL
- [ ] Does this make external calls (API, deploy, message, payment)? → If YES → CRITICAL minimum
- [ ] Does this delete, overwrite, or permanently alter? → If YES → IRREVERSIBLE

### Step 2 — External Impact Check
- [ ] Does this affect other systems or people? → If YES → CRITICAL minimum
- [ ] Does this incur cost (financial, compute, reputation)? → If YES → CRITICAL minimum
- [ ] Does this set policy or precedent? → If YES → CRITICAL or IRREVERSIBLE

### Step 3 — Reversibility Check
- [ ] Can Arif undo this with a single command? → If NO → IRREVERSIBLE
- [ ] Is there a rollback path documented? → If NO → CRITICAL
- [ ] Does this create data that outlives the session? → If YES → CRITICAL

## Decision Tree

```
REQUEST
  └─ Read-only query?
       ├─ YES → TRIVIAL → SEAL → proceed
       └─ NO
            └─ State-changing action?
                 ├─ NO → TRIVIAL → SEAL
                 └─ YES
                      └─ Reversible?
                           ├─ YES with known rollback → REVERSIBLE → CAUTION
                           ├─ YES but rollback uncertain → CRITICAL → HOLD + flag
                           └─ NO
                                └─ External impact?
                                     ├─ NO → CRITICAL → HOLD
                                     └─ YES → IRREVERSIBLE → VOID → 888_HOLD + Arif explicit approval
```

## Output Format

```
CONSEQUENCE CLASSIFICATION: [TRIVIAL|REVERSIBLE|CRITICAL|IRREVERSIBLE]
Verdict: [SEAL|CAUTION|HOLD|VOID]
888_HOLD Required: [YES|NO]
Reason: [1-sentence explanation]
Reversibility: [fully reversible / partial / irreversible]
Rollback path: [if applicable, how to undo]
```

## Automatic Triggers

These always default to **IRREVERSIBLE**:
- `rm`, `delete`, `unlink` — file deletion
- `DROP`, `TRUNCATE`, `ALTER` — database writes
- `deploy`, `push --force` — irreversible deployment
- Any action on `~/.openclaw/workspace/memory/` marked as archival
- External financial transactions
- Authentication or permission changes

## Integration with arifOS-sense

The output of consequence-classifier feeds directly into arifOS-sense:
- TRIVIAL → arifOS-sense skips full floor check
- REVERSIBLE → arifOS-sense does lightweight floor sweep
- CRITICAL → arifOS-sense does full 13-floor check + logs to VAULT999
- IRREVERSIBLE → arifOS-sense returns VOID + 888_HOLD + no execution until Arif approves
