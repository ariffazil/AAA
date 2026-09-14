# Hook-Chain Monotonicity Specification
> **Status:** DRAFT_SPEC_READY

## Status: PATCH_SPEC_READY (draft only, no mutations)

## Decision Object Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "opencode.decision.v1",
  "title": "Hook Decision Object",
  "type": "object",
  "required": ["trace_id", "action_id", "action_class", "decision", "restriction_level", "issued_by"],
  "properties": {
    "trace_id": { "type": "string" },
    "action_id": { "type": "string" },
    "action_class": { "type": "string", "enum": ["READ", "LOCAL_REVERSIBLE", "MUTATE", "EXTERNAL", "IRREVERSIBLE"] },
    "decision": { "type": "string", "enum": ["ALLOW", "OBSERVE_ONLY", "SABAR", "HOLD", "VOID", "REVOKED"] },
    "restriction_level": { "type": "integer", "minimum": 0, "maximum": 5 },
    "reason_codes": { "type": "array", "items": { "type": "string" } },
    "issued_by": { "type": "array", "items": { "type": "string" } },
    "evidence_refs": { "type": "array", "items": { "type": "string" } },
    "locked": { "type": "boolean", "default": false },
    "timestamp": { "type": "string", "format": "date-time" }
  }
}
```

## Restriction Ordering

```
ALLOW       = 0
OBSERVE_ONLY = 1
SABAR       = 2
HOLD        = 3
VOID        = 4
REVOKED     = 5
```

## Rule

A later hook may only retain or increase restriction:

```
decision_{n+1}.restriction_level >= decision_n.restriction_level
```

## Violation Handling

Preserve the MAXIMUM restriction. Never downgrade.

```
if (proposed.restriction_level < existing.restriction_level):
    emit VERDICT_MONOTONICITY_VIOLATION
    keep existing.decision (not HOLD)
    keep existing.restriction_level (not 3)
    merge issued_by and reason_codes from both
    lock if existing was REVOKED
```

The effective decision is always:

$$D_{\text{effective}} = \argmax_{D_i}(\text{restriction level}(D_i))$$

## Hard Invariants

1. REVOKED (level 5) cannot be overridden by any code path — preserved, not replaced
2. VOID (level 4) cannot be downgraded — preserved, not replaced
3. Unknown action class defaults to HOLD (level 3)
4. A locked decision cannot be modified
5. Every decision must carry trace_id, action_id, issued_by, and evidence_refs
6. Downgrade attempts preserve existing higher restriction and add violation reason

## Implementation Location

Add to arifos-judge-gate.ts as a shared module:

```typescript
// lib/decision-object.ts
export const RESTRICTION_ORDER = {
  ALLOW: 0,
  OBSERVE_ONLY: 1,
  SABAR: 2,
  HOLD: 3,
  VOID: 4,
  REVOKED: 5,
} as const

export interface DecisionObject {
  trace_id: string
  action_id: string
  action_class: string
  decision: keyof typeof RESTRICTION_ORDER
  restriction_level: number
  reason_codes: string[]
  issued_by: string[]
  evidence_refs: string[]
  locked: boolean
  timestamp: string
}

export function mergeDecision(
  existing: DecisionObject | null,
  proposed: DecisionObject
): DecisionObject {
  // No existing decision → accept proposed
  if (!existing) return proposed
  
  // Locked decision cannot be modified
  if (existing.locked) {
    return { ...existing, issued_by: [...existing.issued_by, ...proposed.issued_by], evidence_refs: [...existing.evidence_refs, ...proposed.evidence_refs] }
  }
  
  // Downgrade attempt → preserve existing (max restriction)
  if (proposed.restriction_level < existing.restriction_level) {
    return {
      ...existing,
      issued_by: [...existing.issued_by, ...proposed.issued_by],
      reason_codes: [...existing.reason_codes, ...proposed.reason_codes, "VERDICT_MONOTONICITY_VIOLATION"],
      evidence_refs: [...existing.evidence_refs, ...proposed.evidence_refs],
      locked: existing.locked || existing.decision === "REVOKED",
    }
  }
  
  // Upgrade or same level → accept proposed, merge history
  return {
    ...proposed,
    issued_by: [...existing.issued_by, ...proposed.issued_by],
    reason_codes: [...existing.reason_codes, ...proposed.reason_codes],
    evidence_refs: [...existing.evidence_refs, ...proposed.evidence_refs],
    locked: existing.locked || proposed.locked,
  }
}
```

## Tests

1. ALLOW cannot overwrite existing HOLD
2. HOLD cannot be downgraded by later plugin
3. REVOKED cannot be downgraded by any code path
4. Unknown action class → HOLD
5. Locked decision cannot be modified
6. Same-level decisions are allowed (ALLOW→ALLOW)
7. Upgrade is allowed (HOLD→VOID)
