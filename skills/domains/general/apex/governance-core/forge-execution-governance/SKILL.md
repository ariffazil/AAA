---
id: forge-execution-governance
name: forge-execution-governance
description: >
  Use when checking whether a service is actually governed, not just alive — verify services enforce their gates.
version: 1.0.0
owner: AAA
risk_tier: medium
autonomy_tier: T1
triggers:
  - "is this governed"
  - "alive but not governed"
  - "verify governance surface"
  - "tool registration check"
  - "immutable file"
  - "monotonicity"
  - "rollback scope"
---

# forge-execution-governance

## Core Principle

$$
\text{alive} \neq \text{governed}
$$

A service returning HTTP 200 on /health is liveness. Governance is whether that service's actions pass through the constitutional control plane (arifOS judge, lease validation, receipt emission, revocation check). These are independent properties.

## Verification Protocol

### 1. Health ≠ Governance

After confirming a service is alive, verify governance separately:

| Check | What it proves | How to verify |
|-------|---------------|---------------|
| Health endpoint 200 | Liveness | `curl :PORT/health` |
| tools/list returns tools | Tool surface exists | MCP tools/list call |
| **The tool can actually be CALLED** | The call path is open | **Call it** — not just list it |
| Tools pass FloorEnforcer | Governance enforcement | Tool execution with authority check |
| Receipts emitted | Audit trail | arifFlow receipt query |
| Revocation check works | Stop capability | Test revoke + verify denial |

A bridge can be alive (200), have tools listed, but NOT pass through FloorEnforcer. That is alive-but-not-governed.

### 1a. Listing is not calling — gates are layered, and each rejects separately

Registration, listing, and service are **three independent gates**. A tool can be
registered in code, present in `tools/list`, and still be rejected at call time by a
*separate* transport gate — a stateless whitelist, a session/ownership requirement, a
scope filter. The health endpoint stays green throughout, because the gate is working
as designed.

**Consequence:** a measurement, loop, or monitor that depends on that tool reads a
clean zero and concludes "nothing to report", while in truth it can never report
anything. **A structural zero is not a measurement.**

Probe order when a tool is expected to be usable:

```bash
# 1. Is it in the listing?          → proves registration only
tools/list | grep <name>

# 2. Can it be CALLED?             → proves the call path is open
tools/call <name> {minimal-args}
#   SESSION_REQUIRED / whitelist rejection = the tool is unreachable in this mode

# 3. Does the result mean anything? → proves the instrument works
#   Feed a known-non-empty input. If it still returns empty, it is a dead instrument.
```

Two sibling failure modes with the same signature (green light, empty result):

| Mode | Symptom | Check |
|---|---|---|
| **Registered but not served** | Listed, but every call rejected by a sibling gate | Call it; read the rejection envelope's gate name |
| **Field-name drift** | Reader reads a field the writer never emits; window structurally empty, status `OK` | Print one stored record's raw keys; grep the reader for the key it reads |

**Rule:** before reporting zero / empty / `NO_CHANGE` from any governed surface, prove the
instrument **can** return non-zero. Report **UNMEASURABLE**, not zero, when it cannot. An
instrument that reports "all clear" while incapable of saying anything else is consumed as
evidence — every inference built on it inherits the false negative, and nothing in its
output ever contradicts it.

### 2. Immutable File Protection

Canonical identity files (SOUL.md, agent identity artifacts) may have `chattr +i` set. This is a protection boundary, not a bug.

- `lsattr <file>` — check for `i` flag
- Removing immutable protection without authorization = governed mutation violation
- Restoration: `git checkout` + `chattr +i` (if git-tracked)
- SOUL.md is often symlinked to arifOS repo — canonical source is centrally owned

### 3. Monotonicity

In hook chains, restriction can only increase or stay same:

$$
D_{\text{effective}} = \argmax_{D_i}(\text{restriction level}(D_i))
$$

Ordering: ALLOW(0) < OBSERVE_ONLY(1) < SABAR(2) < HOLD(3) < VOID(4) < REVOKED(5)

On attempted downgrade: preserve existing maximum restriction. Never replace REVOKED/VOID with HOLD.

### 4. Rollback Scope

In degraded sandbox mode, only sandbox-contained rollback is permitted:
- Allowed: delete_created, restore_backup, restore_process_local_state
- Denied: git_revert, service_rollback, config_restore, database_rollback, external reversal

If the action requires non-sandbox rollback, the action class is not LOCAL_REVERSIBLE.

### 5. Context Loading

Hermes context files have different loading rules:

| File | Loading rule |
|------|-------------|
| SOUL.md | Always loaded from $HERMES_HOME |
| AGENTS.md | Loaded from cwd only |
| MEMORY.md | NOT auto-loaded (mem0 injection only) |
| USER.md | NOT auto-loaded (mem0 injection only) |
| CLAUDE.md | Loaded from cwd only |

## Failure Modes
| Mode | Action |
|------|--------|
| Service alive but not governed | Wire into MCP governance surface |
| Tool listed but not callable (transport gate) | Read the rejection's gate name; fix the gate or the caller — do not treat the listing as evidence |
| Instrument returns a structural zero | Report UNMEASURABLE, not zero; repair the read/write field contract before trusting any value |
| Immutable flag removed without auth | Restore immediately, incident report |
| Downgrade in hook chain | Preserve max restriction, log violation |
| Rollback escapes sandbox | HOLD, scope violation |
| Context file loaded when it shouldn't be | Check loading rules, adjust config |

## References
- Federation topology: FORGE-federation-manifest
- Verification: FORGE-verify-runtime
- Drift detection: ASI-drift-watch
- Hermes context loading: `hermes-agent` skill, `references/project-context-files.md` (present in the aaa-hermes profile's skill tree, not this one)