# arifOS before_model_callback infrastructure — Spec v1 (1 page, no build)

**Status:** SPEC ONLY. F13-stage. No code yet.
**Goal:** Let future agents plug PII redaction (and any other pre-call hook) into arifOS without rebuilding the lifecycle.
**Why now:** F9 ANTI-HANTU patterns exist in `witness_packet.py:264` but are run **after** the LLM call, not before. PII redaction needs to run **before** the call (per ADK pattern, per HERMES item #1).

## The hook surface (what arifOS is missing)

A **call lifecycle** with named, ordered hook points:
1. `before_call(query, payload) → modified_query` — PII redaction, context injection, scope guard
2. `after_call(query, response, cost) → modified_response` — LLM-as-judge, cost logging
3. `on_error(query, exception) → fallback` — graceful degradation

arifOS has #2 (via the audit log in `tool_13_arif_memory.py`) and #3 (HOLD verdicts). It does **not** have #1. This spec defines #1 only.

## What needs to exist (1 thing, ~50 LOC)

**File:** `/opt/arifos/arifosmcp/runtime/hooks/before_call.py` (new file, ~50 LOC)

```python
# Public API
def before_call(query: str, payload: dict, actor_id: str = None) -> tuple[str, dict]:
    """Run all registered before_call hooks in order. Returns (modified_query, modified_payload).
    Hooks are registered via @register_before_call decorator.
    If a hook raises, log and continue (graceful degrade)."""
    ...

# Decorator
def register_before_call(name: str, priority: int = 100):
    """Register a function as a before_call hook. Lower priority runs first."""
    ...

# Built-in hook to ship with v1 (PII redaction — implements HERMES item #1)
@register_before_call("pii_redaction_v1", priority=10)
def pii_redaction_v1(query: str, payload: dict, **kwargs) -> tuple[str, dict]:
    """Redact PII patterns from query before LLM call.
    Patterns sourced from /root/AAA/canon/ (F9 anti-hantu extension).
    Returns (redacted_query, payload_with_redacted_query)."""
    # redaction patterns from bank: see RECEIPTS below
    redacted = apply_patterns(query, PII_PATTERNS_V1)
    payload = {**payload, "query": redacted, "pii_redacted": True}
    return redacted, payload
```

## Where to wire it

In `tool_13_arif_memory.py` recall handler, **before** the v2 hybrid wire (around line 290):

```python
from arifosmcp.runtime.hooks.before_call import before_call
query, payload = before_call(query=query, payload=payload or {}, actor_id=actor_id)
# THEN the existing v2 wire check
if payload.get("hybrid") and mode == "recall":
    ...
```

## PII patterns (sourced from bank, not invented)

Pattern file at `/root/AAA/canon/pii_patterns_v1.yaml`:
```yaml
patterns:
  - name: ic_malaysia
    regex: '\b\d{6}-\d{2}-\d{4}\b'   # e.g. 850905-14-6217
    replacement: '[IC-REDACTED]'
  - name: phone_my
    regex: '\+60[\d-]{9,12}'
    replacement: '[PHONE-REDACTED]'
  - name: email
    regex: '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    replacement: '[EMAIL-REDACTED]'
  - name: passport_my
    regex: '\b[A-Z]\d{7,8}\b'
    replacement: '[PASSPORT-REDACTED]'
  # add as needed from /root/AAA/governance/OSS-DISTILLATION-ADK-EVAL-OBS-2026-10-03.md
```

## Acceptance criteria

- Send a query containing "IC 850905-14-6217" → audit log shows `pii_redacted: true` and stored query is `"IC [IC-REDACTED]"`
- Hook failure: graceful continue, audit log shows `before_call_error: <name>`
- No regression: existing v2 wire still fires, 50/50 hybrid path still works

## Reversibility

- Single new file, can be deleted to revert
- Wire is 5 lines, can be removed
- Pattern file is YAML, can be emptied to disable
- Total LOC: ~80 (file 50, wire 5, patterns YAML 20, tests 25)

## What this spec does NOT do (per Law 10)

- ❌ Does not write any code now
- ❌ Does not implement LLM-as-judge (out of scope, anti-F-A)
- ❌ Does not change F9 anti-hantu patterns themselves (they already exist)
- ❌ Does not touch Falkor
- ❌ Does not require new pip deps (re module stdlib)

## F13 ask (when ready)

Approve the build. Once deployed, HERMES item #1 (PII redaction) becomes executable by future agents via hook registration. Estimated 1-2 hours of FI-008 or similar work.
