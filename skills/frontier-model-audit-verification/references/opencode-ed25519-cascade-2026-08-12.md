# OpenCode Ed25519 Identity Cascade — 2026-08-12

## Session context

Arif asked: "Fix and make sure opencode working." The session uncovered a cascade
of 4 distinct failure classes in OpenCode's Ed25519 identity binding chain.

## Root cause: 4 mismatched keys across federation

```
identity.key      → old seed b8dfe427 (never rotated)
identity_pkcs8.pem → new random key cb747ac1 (generated 2026-08-12)
identity.json      → old pub 88c0ee8f (declared, not derived from PEM)
agent_identities   → old pub de27f5e (from 2026-07-17 original)
```

Four different private keys existed for the same actor. The bridge signed with
one; the kernel verified against another.

## Cascade of fixes (chronological)

1. Generated fresh keypair (Ed25519PrivateKey.generate)
2. Synced to 5 public key files + 2 agent_identities.json copies
3. Discovered `/root/.local/share/arifos/agent_keys/333-AGI_public.pem` (9th location)
4. Discovered `_normalize_actor("333-AGI") = "333-agi"` → lowercase file needed
5. Bridge patch: raw DER → PKCS#8 PEM (Node.js `createPrivateKey` rejects raw Ed25519 DER)
6. Bridge patch: `ACTOR_ID = "333-AGI"` (kernel remaps via parent_agent)
7. Discovered `identity_pkcs8.pem` had a different key than `identity.key`
8. Final sync: PEM as source of truth, all locations regenerated from one seed

## Bug #2: phantom-field verification (ACT 406)

`pre_execution_gate.py:1410`:
```python
_sct_claims.get("session", {}).get("actor_bound")  # NEVER EXISTS
```

Token minted by `act_token.py:mint_sct` writes `claims["av"]` — flat key, no
`"session"` dict. Gate always returns None → HOLD → 406 cascade.

**Fix:** `claims.get("av")` (single-line).

## Files affected

| File | Change |
|---|---|
| `/root/.config/opencode/plugins/arifos-kernel-bridge.ts` | ACTOR_ID="333-AGI", PEM-only load |
| `/root/AAA/agents/opencode/identity.key` | Regenerated from PEM seed |
| `/root/AAA/agents/opencode/identity_pkcs8.pem` | PEM source of truth |
| `/root/AAA/IDENTITY/keys/opencode_public.pem` | New pubkey |
| `/root/AAA/IDENTITY/keys/333-AGI_public.pem` | New pubkey |
| `/root/AAA/IDENTITY/keys/333-agi_public.pem` | New pubkey (lowercase) |
| `/root/A-FORGE/IDENTITY/keys/opencode/opencode_ed25519_public.pem` | New pubkey |
| `/root/.local/share/arifos/agent_keys/333-AGI_public.pem` | New pubkey |
| `/opt/arifos/identity/agent_identities.json` | New pubkey + 333-AGI entry |
| `/root/A-FORGE/data/agent_identities.json` | Synced copy |
| `/root/arifOS/arifosmcp/runtime/pre_execution_gate.py` | Phantom-field fix (pending) |

## Lessons for future sessions

- Always ask: "How many locations hold this actor's key material?"
- `_normalize_actor` lowercases — filenames must match lowercase
- Node.js Ed25519 DER PKCS#8 prefix fails on some OpenSSL builds — use PEM
- Kernel remaps `opencode → 333-AGI` via parent_agent — sign for the canonical identity
- When "Invalid signature" appears against a freshly rotated key, suspect sync gap first
- ACT 406 cascade: check producer writes vs reader field path before touching crypto

## Scar

IDENTITY_DRIFT_001: no single source of truth for actor identity. Affects all federation
agents. Fix requires canonical seed file + symlink architecture + build-time drift check.
