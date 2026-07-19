# Delegation Envelope Schema — WAJIB 4

> **child_authority ⊆ parent_authority** — cryptographically enforced.
> A parent with OBSERVE_ONLY must be unable to create a MUTATE child.
> **Forged:** 2026-07-19

## Schema

```json
{
  "delegation": {
    "parent_session_id": "string",
    "parent_principal": "string — actor_id of delegator",
    "parent_authority_band": "OBSERVE_ONLY | LIMITED_MUTATE | FULL | SOVEREIGN",
    "child_principal": "string — actor_id of delegate",
    "child_authority_band": "OBSERVE_ONLY | LIMITED_MUTATE | FULL | SOVEREIGN",
    "allowed_tools": ["string"],
    "allowed_resources": ["string"],
    "max_blast_radius": "LOW | MEDIUM | HIGH | CRITICAL",
    "expires_at": "ISO8601",
    "delegation_depth": 1,
    "redelegation_allowed": false,
    "parent_envelope_hash": "sha256:...",
    "kernel_signature": "string"
  }
}
```

## Attenuation Rules

1. **child_authority ≤ parent_authority** — OBSERVE_ONLY → OBSERVE_ONLY only
2. **Scope narrowing only** — child tools ⊆ parent tools
3. **Expiry inheritance** — child expires ≤ parent expires
4. **Depth limit** — max delegation depth configurable (default: 1)
5. **No redelegation by default** — child cannot delegate further

## Adversarial Tests (8)

| Test | Scenario | Expected |
|------|----------|----------|
| T1 | OBSERVE parent → MUTATE child | DENIED |
| T2 | Expired parent → child call | DENIED |
| T3 | Revoked parent → existing child | DENIED |
| T4 | Missing lineage → access | DENIED |
| T5 | Child re-delegation when prohibited | DENIED |
| T6 | Scope widening by child | DENIED |
| T7 | Session ID substitution | DENIED |
| T8 | Parallel child authority aggregation | DENIED |

## Integration with A2A

When AAA routes to a child agent or peer organ:
1. Parent session presents delegation envelope
2. Target verifies kernel_signature against arifOS public key
3. Target validates child_authority ≤ parent_authority
4. Target enforces allowed_tools ⊆ requested tools
5. Target checks expires_at is still valid

