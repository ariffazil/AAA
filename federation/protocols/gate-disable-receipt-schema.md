# Gate-Disable Receipt Schema — Observation Telemetry

> **CCC-T-07 (2026-09-18)** — closes GAP-07 without adding blocks
> **Authority:** INV-11 (audit) + representation-reality-invariant doctrine
> **Status:** SCHEMA — observation telemetry only

## Why this exists

GAP-07 framed "gate disable is silent everywhere" as a denial/policy gap. The fix was framed as "emit `gate.disabled` receipt event."

Per sovereign directive (no overengineering, no capability reduction), the reframe is: **emit on disable AS WELL AS on enable**. Both directions of state change get receipts. No new rules — just better observation.

## Schema

```yaml
event_type: gate.disable | gate.enable | gate.config_change
gate_id: <canonical id, e.g. "arifos-hermes-gate-hook" | "kimi-aaa-witness-pre">
harness: <hermes | opencode | kimi | codex | openclaw | agy>
actor: <who changed the state>
timestamp: <ISO-8601 UTC>
prev_state: <enabled | disabled | configured>
new_state: <enabled | disabled | configured>
reason: <text — why this change>
config_diff: <optional — what changed>
envelope_id: <uuid v4 — receipt chain link>
session_id: <kernel session>
```

## Where this is emitted

Each harness gate-hook writes to its own receipt path (sibling to existing receipts):
- Hermes: `/root/.local/share/arifos/hermes_gate_state.jsonl`
- OpenCode: `/root/.local/share/arifos/opencode_gate_state.jsonl`
- Kimi: `/root/.agent-workbench/mcp-audit.jsonl` (existing path; emit append-only)
- Codex: `/root/.codex/hooks/gate_state.jsonl`
- OpenClaw: inherited via host harness

## What this does NOT do

- ❌ Does not block the disable
- ❌ Does not require F13 to disable
- ❌ Does not enforce enable-or-disable decision

A gate can still be disabled. The receipt is the only artifact.

## What this DOES do

- ✅ Makes disable observable to entropy monitoring (E11_DEAD_SURFACE detection)
- ✅ Provides audit trail for drift-watch
- ✅ Surfaces "control exists → control disabled → nobody notices" gap as a RECEIVED fact

## Implementation cost

- ~5 LoC per harness gate (emit a single JSON line on state transition)
- Zero new infrastructure
- No new blocks, no new rules

## Verdict

GAP-07 closes via **telemetry observation**, not enforcement. ΔS impact: −0.1 (single schema, 4 LoC × 5 harnesses). Citizen capability: UNCHANGED.

> **DITEMPA BUKAN DIBERI ⚒️**
> **Path:** `/root/AAA/federation/protocols/gate-disable-receipt-schema.md`
> **Status:** SCHEMA — observation telemetry only
