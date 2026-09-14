# Degraded Mode Fence Specification
> **Status:** DRAFT_SPEC_READY

## Status: PATCH_SPEC_READY (draft only, no mutations)

## Current Behavior

```
LOCAL_REVERSIBLE + arifOS down → ALLOWED_WITHOUT_JUDGE
```

This is in arifos-judge-gate.ts lines 456-465.

## Problem

Without strict bounding, this clause creates a path where:
1. arifOS goes down
2. Agent can write/edit/patch without judgment
3. No lease validation, no revocation check
4. Potential for ungoverned mutation

## Required Constraints

Degraded local action is permitted ONLY when ALL conditions are true:

| Condition | Check | Fail → |
|-----------|-------|--------|
| Sandbox root declared | output.args.sandbox_root exists and is absolute path | HOLD |
| No network egress | tool is not http/fetch/curl/telegram/email/calendar | HOLD |
| No Git operation | tool is not git_commit/git_push/git_checkout | HOLD |
| No system service | tool is not systemctl/docker/cron | HOLD |
| No canonical config | sandbox_root not under /root/arifOS, /root/AAA, /root/A-FORGE, /root/.hermes | HOLD |
| No identity/authority mutation | tool is not forge_vault/arif_seal/arif_forge | HOLD |
| No memory promotion | tool is not memory_write/memory_promote | HOLD |
| Rollback plan exists | output.args.rollback_plan is non-empty object | HOLD |
| Idempotency key present | output.args.idempotency_key exists | HOLD |
| Bounded TTL | output.args.ttl_seconds <= 300 (5 min max) | HOLD |

## Implementation

```typescript
// In arifos-judge-gate.ts, replace the degraded mode block:

// BEFORE (current):
if (classification.actionClass !== "LOCAL_REVERSIBLE") {
  // BLOCKED
}
// ALLOWED_WITHOUT_JUDGE

// AFTER (hardened):
if (classification.actionClass !== "LOCAL_REVERSIBLE") {
  // BLOCKED
}

// Degraded mode — strict envelope
const degradedChecks = [
  { name: "sandbox_root", ok: !!args.sandbox_root && typeof args.sandbox_root === "string" && args.sandbox_root.startsWith("/") },
  { name: "no_network", ok: !/^(http|fetch|curl|telegram|email|calendar)/i.test(toolName) },
  { name: "no_git", ok: !/^(git_|forge_git)/i.test(toolName) },
  { name: "no_service", ok: !/^(systemctl|docker|cron)/i.test(toolName) },
  { name: "no_canonical_config", ok: args.sandbox_root && !args.sandbox_root.startsWith("/root/arifOS") && !args.sandbox_root.startsWith("/root/AAA") && !args.sandbox_root.startsWith("/root/A-FORGE") && !args.sandbox_root.startsWith("/root/.hermes") },
  { name: "no_identity_mutation", ok: !/^(forge_vault|arif_seal|arif_forge)/i.test(toolName) },
  { name: "no_memory_promotion", ok: !/^(memory_write|memory_promote)/i.test(toolName) },
  { name: "rollback_plan", ok: !!args.rollback_plan && typeof args.rollback_plan === "object" },
  { name: "idempotency_key", ok: !!args.idempotency_key },
  { name: "bounded_ttl", ok: typeof args.ttl_seconds === "number" && args.ttl_seconds <= 300 },
]

const failedChecks = degradedChecks.filter(c => !c.ok)
if (failedChecks.length > 0) {
  blockedCount++
  receipt({
    event: "judge-gate.blocked.degraded-envelope",
    tool: toolName,
    failed_checks: failedChecks.map(c => c.name),
    blocked_count: blockedCount,
    timestamp: new Date().toISOString(),
  })
  throw new Error(`KERNEL_UNAVAILABLE: arifOS unreachable AND degraded envelope check failed for '${toolName}': ${failedChecks.map(c => c.name).join(", ")}. HOLD until kernel resumes.`)
}

// All checks passed — allow with degraded receipt
receipt({
  event: "judge-gate.degraded-allowed",
  tool: toolName,
  sandbox_root: args.sandbox_root,
  checks_passed: degradedChecks.map(c => c.name),
  timestamp: new Date().toISOString(),
})
return
```

## Degraded Receipt Format

```json
{
  "event": "judge-gate.degraded-allowed",
  "tool": "write",
  "action_class": "LOCAL_REVERSIBLE",
  "sandbox_root": "/tmp/sandbox-test-abc123",
  "checks_passed": ["sandbox_root", "no_network", "no_git", "no_service", "no_canonical_config", "no_identity_mutation", "no_memory_promotion", "rollback_plan", "idempotency_key", "bounded_ttl"],
  "arifos_status": "unreachable",
  "timestamp": "2026-09-14T02:35:00.000Z",
  "degraded_mode": true
}
```

## Tests

1. arifOS down + Git write → HOLD_KERNEL_UNAVAILABLE
2. arifOS down + network action → HOLD_KERNEL_UNAVAILABLE
3. arifOS down + sandbox write with rollback → ALLOWED_WITH_DEGRADED_RECEIPT
4. arifOS down + canonical config path → HOLD_KERNEL_UNAVAILABLE
5. arifOS down + identity mutation → HOLD_KERNEL_UNAVAILABLE
6. arifOS down + no rollback plan → HOLD_KERNEL_UNAVAILABLE
7. arifOS down + TTL > 300 → HOLD_KERNEL_UNAVAILABLE
8. arifOS down + all checks pass → ALLOWED with receipt
