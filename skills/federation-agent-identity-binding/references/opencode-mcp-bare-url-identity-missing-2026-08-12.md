# OpenCode MCP Bare URL — Layer Zero Identity Missing

**Date:** 2026-08-12
**Trigger:** Arif asks why OpenCode said "session_token_status: DENY: actor not cryptographically verified"
**Agent:** OpenCode (FI-001, bound_to: 333-AGI)

## What happened

OpenCode tried to run `swapoff -a && swapon -a` (T1 reversible). The arifOS kernel denied the call. OpenCode attributed the denial to "Gödel Rule 2: no self-certification — the kernel will not mint an SCT for an identity that isn't crypto-bound."

## What the code actually shows

### OpenCode's MCP config (`/root/.config/opencode/opencode.json`)

```json
{
  "mcp": {
    "arifos": {
      "type": "remote",
      "url": "http://127.0.0.1:8088/mcp",
      "enabled": true
    }
  }
}
```

No headers. No actor_id. No auth tokens. Just a bare URL.

### OpenCode's identity files (DO EXIST)

- `/root/AAA/agents/opencode/identity.key` — 32-byte Ed25519 seed ✓
- `/root/AAA/agents/opencode/identity_pkcs8.pem` — PKCS8 PEM ✓
- `/root/AAA/agents/opencode/agent-card.json` — has `ed25519_pubkey: 2e9919ef...` ✓
- OpenCode is in `_ED25519_EXEMPT_SYSTEM_ACTORS` at `session_auth.py:62` ✓

### The kernel code path

1. `session_auth.py:82` `_resolve_authority_from_registry(actor_id=None)` → returns `"anonymous"`
2. `authority.py:227` `bind_authority_state()` → `state.actor.verified = False`
3. `sess["actor_verified"] = False`
4. Every MUTATE tool → DENY

### Why the exempt list didn't help

The `_ED25519_EXEMPT_SYSTEM_ACTORS` dict at `session_auth.py:54` contains:
```python
_ED25519_EXEMPT_SYSTEM_ACTORS = {
    "arif": "operator",
    "a-forge": "operator",
    "forge": "operator",
    "opencode": "operator",   # ← OpenCode IS listed here
    "hermes": "operator",
    ...
}
```

But the function only fires when `actor_id` is NOT None/empty:
```python
def _resolve_authority_from_registry(actor_id):
    if actor_id:
        _key = actor_id.strip().lower()
        if _key in _ED25519_EXEMPT_SYSTEM_ACTORS:
            return _ED25519_EXEMPT_SYSTEM_ACTORS[_key]  # → "operator"
```

Since the MCP config sends NO actor_id → the function receives None → skips the exempt check → returns `"anonymous"`.

### The arif_init call also failed

OpenCode tried to call `arif_init` directly via REST:
```bash
curl -X POST http://127.0.0.1:8088/tools/arif_init -d '{"actor_id":"opencode"}'
```
This returned `"Tool execution failed"` — because the REST surface doesn't inject the actor into the session context the same way MCP does. The identity must be carried in MCP headers or the arif_init arguments with a valid signature.

## The philosophical attribution trap

OpenCode's response to Arif was:
> "I cannot sign for myself. Gödel rule 2: no self-certification. If I hacked around the SCT gate, I'd be violating F11/F13 integrity."

This is **philosophically sound but diagnostically wrong**:
- Gödel Rule 2: no self-certification — correct in principle
- But the kernel never asked OpenCode to self-certify — it never RECEIVED an identity claim to evaluate
- The kernel returned "anonymous" because no identity was transmitted, not because it rejected one
- The fix is not philosophical (self-certification is impossible) but practical (transmit identity in the request)

## Key insight

The 9-location registry, challenge flow, PEM wrapping, canonical actor_id normalization — all of this is LAYER 1+. The LAYER 0 question is: **is the agent sending any identity at all?** This is the diagnostic that should always run first.

## Related files
- Kernel: `/opt/arifos/app/arifosmcp/runtime/authority.py` (lines 176-351)
- Kernel: `/opt/arifos/app/arifosmcp/runtime/session_auth.py` (lines 54-129)
- OpenCode config: `/root/.config/opencode/opencode.json`
- OpenCode keys: `/root/AAA/agents/opencode/identity.key`, `identity_pkcs8.pem`
- DID registry: `/opt/arifos/secrets/did-registry.json` (OpenCode NOT registered here)
