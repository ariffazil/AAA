# Codex Identity Contract v1 — Spec (F13-stage, no build)
**Problem:** Per Arif P0: `aaa_session_witness.py` consumed only "init returned 200", not `actor_verified`, `authority`, `mutation_allowed`. Live arifOS session = OBSERVE_ONLY. Free nonce ≠ ACT authority.

**Solution:** Witness must consume full identity contract from arifOS response, fail-closed if not verified.

## Schema

```python
@dataclass
class IdentityContract:
    session_id: str
    actor_id: str
    actor_verified: bool       # must be True to proceed
    actor_cryptographically_verified: bool  # bonus check
    authority: str             # OBSERVE_ONLY, LIMITED_MUTATE, etc.
    mutation_allowed: bool
    seal_allowed: bool
    allowed_next_verbs: list[str]
```

## Hook contract

```python
def check_identity(arif_init_response) -> IdentityContract:
    """Parse arif_init response, return contract. Raise if invalid."""
    if not arif_init_response.actor_verified:
        raise IdentityNotVerified(arif_init_response.reason)
    if arif_init_response.authority == "OBSERVE_ONLY":
        if arif_init_response.mutation_allowed:
            raise AuthorityParadox(...)
    return arif_init_response
```

## Patch target

- `/root/.codex/hooks/aaa_session_witness.py` (after P0 #1 de-init fix)
- New function: `enforce_identity_contract(contract) -> bool`
- Hook signature now returns early if contract invalid

## Codex flow (after patch)

```
SessionStart
  → arif_init (creates session, gets session_id + contract)
  → witness: read /tmp/.arifos_session_<actor> (gets session_id, NOT contract)
  → witness: GET /mcp/v1/session/<session_id> → fetch full contract
  → enforce_identity_contract(contract)
  → if !actor_verified: HOLD, reason_code="ACTOR_NOT_VERIFIED"
  → if !mutation_allowed && action.mutates: HOLD, reason_code="NO_MUTATION_AUTHORITY"
  → else: ALLOW, write 1 compact receipt
```

## Reversibility

None — this is spec only.
