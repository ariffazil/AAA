# Capability Ledger — arifOS Truth Infrastructure

> **Implemented ≠ Reachable ≠ Governed**

This directory is the single source of truth for what Hermes can actually do,
through which route, under whose authority, and with what failure mode.

## Three-State Model

| State | Question | Example |
|---|---|---|
| **Implemented** | Does code/route/package exist? | `forge_email` bridge code exists in repo |
| **Reachable** | Can Hermes invoke it RIGHT NOW? | ACT gate blocked stale SCT → unknown |
| **Governed** | Does it have auth, receipts, rate limits, holds? | Weather: observe, fail-soft, receipt-required |

A capability is operational ONLY when all three are true.
Any one being false means the capability is not ready for autonomous action.

## Files

| File | Purpose |
|---|---|
| `capability-ledger.yaml` | The ledger — all capabilities with implementation, reachability, and governance state |
| `capability-ledger.schema.json` | JSON Schema for validation |
| `action-membrane.yaml` | Centralized action class policy — every tool invocation passes through |
| `probe-capabilities.py` | Read-only probe harness — converts assertions into timestamped evidence |
| `probe-results/` | JSONL evidence from probe runs (gitignored) |

## State Vocabulary

### implementation.state
`absent` | `partial` | `implemented` | `retired` | `vendor_candidate` | `implemented_or_claimed` | `external_institutional_api`

### reachability.state
`unreachable` | `not_wired` | `working_unprobed` | `reachable` | `degraded` | `pending_production_probe` | `intentionally_unreachable` | `unknown_by_governed_probe`

### governance.authority
`observe` | `draft` | `external_write` | `financial_write` | `admin_write`

### governance.activation_gate
`none` | `888_HOLD` | `F13_888_HOLD` | `valid_SCT_required` | `wire_only_when_concrete_workflow_exists`

### lifecycle
`active` | `partial` | `deferred` | `retired` | `blocked`

> **Vocabulary drift — F13 pending.** The enum sets above extend 888's canonical
> "State rules" table by 5 values. `external_institutional_api` and
> `wire_only_when_concrete_workflow_exists` were 888's own seed values; the other
> three (`implemented_or_claimed`, `unknown_by_governed_probe`, `valid_SCT_required`)
> were added by the concurrent build session. None are F13-ratified. Normalize to
> the canonical table or ratify — do not treat the extension as canonical silently.

## Usage

```bash
# List all capabilities
python3 probe-capabilities.py --list

# Validate ledger structure
python3 probe-capabilities.py --validate

# Probe a specific capability
python3 probe-capabilities.py --capability weather.current.kl

# Probe all capabilities with live probes
python3 probe-capabilities.py --all
```

## Adding a New Capability

1. Add an entry to `capability-ledger.yaml`
2. Fill all three dimensions: implementation, reachability, governance
3. If a live probe exists, add it to `PROBES` dict in `probe-capabilities.py`
4. Run `--validate` to check schema
5. Run `--capability <id>` to get initial probe evidence

## Preflight Rule

Every action must pass before execution:

```
ALLOW only if:
  1. capability exists in ledger
  2. lifecycle is active or explicitly approved partial
  3. reachability is reachable/degraded-with-approved-fallback
  4. requested action is within governance.authority
  5. required gate/confirmation is satisfied
  6. receipts can be emitted
ELSE:
  structured HOLD or DENY, never improvise a fallback write
```

## Design Principles

- **No database, no service, no new port.** YAML + Python script + JSONL.
- **Git-versioned.** Every state change is a commit.
- **Machine-validated.** Schema check catches structural drift.
- **Truthful non-errors.** Deferred capabilities report their state honestly, not as false alarms.
- **Evidence timestamps.** A capability is "reachable" only when a probe says so, with a timestamp.
- **888 HOLD on all external writes.** No autonomous expansion without human approval.

## Shadow

A ledger can drift if probes are not executed and evidence timestamps are not enforced.
The probe harness must run regularly (cron or manual) to keep reachability states current.
