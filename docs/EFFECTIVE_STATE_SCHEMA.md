# Effective State Schema — WAJIB 3

> **Canonical kernel state object.** All surfaces derive from this. No field may describe stronger authority than what this object declares.
> **Forged:** 2026-07-19 · **WAJIB 3**

## Schema

```json
{
  "effective_state": {
    "actor_verified": false,
    "identity_source": "envelope_derived | session_token | did_web | sovereign_key",
    "authority_band": "OBSERVE_ONLY | LIMITED_MUTATE | FULL | SOVEREIGN",
    "mutation_allowed": false,
    "seal_allowed": false,
    "judge_allowed": false,
    "session_id": "string | unknown",
    "verdict": "HOLD | PROCEED | VOID",
    "verdict_reason": "string",
    "actor_id": "string",
    "expires_at": "ISO8601",
    "degraded": false,
    "degraded_reason": null
  }
}
```

## Authority Bands

| Band | Mutate | Seal | Judge | When |
|------|--------|------|-------|------|
| OBSERVE_ONLY | ❌ | ❌ | ❌ | Default. Unverified actor, preflight, light mode. |
| LIMITED_MUTATE | ✅ (scoped) | ❌ | ❌ | Verified session with explicit scope. |
| FULL | ✅ | ✅ | ❌ | Fully verified identity. |
| SOVEREIGN | ✅ | ✅ | ✅ | F13 key present. |

## Transition Rules

1. **BOOT gate** (authority.py:81-95): If boot_state ≠ OK, demote to OBSERVE_ONLY
2. **Unverified actor** → OBSERVE_ONLY (even if client requests higher)
3. **Identity verified + session valid** → LIMITED_MUTATE or FULL per verification level
4. **F13 key present** → SOVEREIGN override

## Invariant

> No surface (health, MCP, REST, A2A, agent card) may describe higher authority than the canonical effective_state.

## Conformance Test

`conformance/kernel/test_effective_state.py` verifies:
1. arif_init(light) returns effective_verdict=HOLD, authority_scope=OBSERVE_ONLY
2. can_mutate=false when authority_scope=OBSERVE_ONLY
3. No field contradicts authority_scope
4. SCT claims match response claims

