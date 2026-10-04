# Ed25519 Identity Pitfalls — arifOS Federation

> Session-discovered failure modes when wiring agent Ed25519 identity into arifOS.
> Each pitfall was hit, diagnosed, and fixed during real bootstrap sessions.

## Pitfall 1: identity.key ≠ identity.json pubkey (KEY MISMATCH)

**Symptom:** Kernel returns `ed25519_signature_invalid` even though the signature is cryptographically correct.

**Root cause:** The raw 32-byte seed in `identity.key` derives to a DIFFERENT public key than what is stored in `identity.json` and `agent_registry.json`. This happens when:
- Key was regenerated but registry not updated
- Key was generated with a different library (nacl vs cryptography) that produced different outputs
- File was overwritten by a different process

**Detection:**
```python
seed = open("identity.key", "rb").read()
priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
derived = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
registered = json.load(open("identity.json"))["ed25519_pubkey_hex"]
if derived != registered:
    print("MISMATCH — registry has stale key")
```

**Fix:** Regenerate from the seed, update ALL three files: identity.json, identity.key, agent_registry.json.

## Pitfall 2: Kernel PEM resolve path is NOT AAA/keys/

**Symptom:** `resolve_actor_public_key("opencode")` returns None even though `opencode_public.pem` exists.

**Root cause:** The kernel reads from `/root/AAA/IDENTITY/keys/` (capital IDENTITY), NOT `/root/AAA/keys/`.

**Fix:**
```python
# CORRECT path
pem_path = Path("/root/AAA/IDENTITY/keys") / f"{actor_id}_public.pem"
```

## Pitfall 3: Node.js cannot load raw 32-byte Ed25519 seed

**Symptom:** `createPrivateKey()` throws `ERR_OSSL_UNSUPPORTED: DECODER routines::unsupported`.

**Root cause:** Node.js `createPrivateKey` expects PKCS#8 DER or PEM, not raw 32-byte Ed25519 seed. The raw seed must be wrapped in ASN.1 PKCS#8 structure.

**The wrong DER prefix (15 bytes + 0x00 suffix):**
```
WRONG: 302e020100300506032b6570042204 (15 bytes) + seed + 00 → 48 bytes but BROKEN
```

**The correct DER prefix (16 bytes, no suffix):**
```
RIGHT: 302e020100300506032b657004220420 (16 bytes) + seed → 48 bytes, WORKS
```

The missing byte `0x20` (decimal 32) is the ASN.1 length of the Ed25519 seed octet string.

**BEST PRACTICE:** Generate PKCS8 PEM via Python, load PEM in Node:
```python
# Python
pem = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
open("identity_pkcs8.pem", "wb").write(pem)
```
```typescript
// Node
const key = createPrivateKey({ key: readFileSync("identity_pkcs8.pem") })
```

## Pitfall 4: Kernel normalizes actor_id via agent-card bound_to

**Symptom:** `challenge_actor_mismatch` error in kernel logs.

**Root cause:** The kernel canonicalizes agent IDs. If agent-card says `bound_to: 333-AGI`, the kernel rewrites `opencode` → `333-AGI` before challenge verification. The challenge nonce is stored for `333-AGI`, but if the plugin signs with `opencode`, verification fails.

**Detection:**
```python
# Check what the kernel normalizes to
from arifosmcp.runtime.governance_identity import normalize_actor_id
canonical = normalize_actor_id("opencode")  # → "333-AGI" if bound_to=333-AGI
```

**Fix:** Plugin must use the CANONICAL actor_id in ALL signing operations:
```typescript
const ACTOR_ID = "333-AGI"  // NOT "opencode"
```

## Pitfall 5: MCP POST requires Accept header (HTTP 406)

**Symptom:** Plugin gets `HTTP 406` from arifOS MCP endpoint. Session binding works but subsequent calls (arif_judge, forge_shell) fail.

**Root cause:** arifOS FastMCP enforces MCP spec: `POST without Accept header → 406 Not Acceptable`. The judge-gate plugin only sent `Content-Type` but not `Accept`.

**Fix:** EVERY `fetch()` to arifOS MCP must include BOTH headers:
```typescript
headers: {
  "Content-Type": "application/json",
  "Accept": "application/json, text/event-stream",  // REQUIRED
}
```

**Scope:** This applies to ALL OpenCode plugins that POST to :8088/mcp:
- arifos-kernel-bridge.ts (arif_init calls)
- arifos-judge-gate.ts (arif_judge calls) ← WAS MISSING
- Any future plugin

## Pitfall 6: Deploy markers in DEPLOY_ROOT, not SOURCE_ROOT

**Symptom:** A-FORGE health shows `degraded`, `deployment_drift=true`, `deployed_commit=""`.

**Root cause:** A-FORGE health reads `deployed_commit` from `/opt/a-forge/app/.git_commit` (DEPLOY_ROOT), but `make deploy-local` writes to `/root/A-FORGE/.git_commit` (SOURCE_ROOT).

**Fix:**
```bash
cat /root/A-FORGE/.git_commit > /opt/a-forge/app/.git_commit
```

## Pitfall 7: arif_init challenge mode rejected registered agents

**Symptom:** `arif_init(mode="challenge", actor_id="333-AGI")` returns `INIT_JURISDICTION_HOLD`.

**Root cause:** session.py `_SOVEREIGN_MAP` only allowed sovereign actors (arif, ariffazil, 888). Registered agents like 333-AGI were rejected.

**Fix:** Patch session.py to also accept registered agents:
```python
from arifosmcp.runtime.crypto_auth import is_registered_actor as _is_reg
if actor_id not in _SOVEREIGN_MAP and not _is_reg(actor_id):
    return _make_init_hold(...)
```
Deploy to both `/root/arifOS/` and `/opt/arifos/app/`.
