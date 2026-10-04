# OpenCode Ed25519 Challenge — Worked Example (2026-08-12)

## What was broken (4 independent bugs)

1. **identity.key seed ≠ identity.json pubkey** — existing keypair was from a different generation; `identity.key` derived `cb747ac1...` while `identity.json` had `88c0ee8f...`
2. **MCP response envelope** — `arifosCall()` returned `result.content` (list) instead of `JSON.parse(content[0].text)` → challenge nonce lost
3. **kernel challenge mode sovereign-only** — `session.py` `_SOVEREIGN_MAP` gate blocked `is_registered_actor("opencode")` → `INIT_JURISDICTION_HOLD`
4. **actor_id normalization** — kernel canonicalizes `opencode` → `333-AGI`; signing with `opencode:nonce` → `challenge_actor_mismatch`

## The fix cascade

### Fix 1: Regenerate keypair
```python
from cryptography.hazmat.primitives.asymmetric import ed25519
import json, os
from pathlib import Path

seed = os.urandom(32)
priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
pub = priv.public_key()
pub_hex = pub.public_bytes(Encoding.Raw, PublicFormat.Raw).hex()

# Update identity.json
with open("/root/AAA/agents/opencode/identity.json") as f: data = json.load(f)
data["ed25519_pubkey_hex"] = pub_hex
with open("/root/AAA/agents/opencode/identity.json", "w") as f: json.dump(data, f, indent=2)

# Write seed
Path("/root/AAA/agents/opencode/identity.key").write_bytes(seed)
os.chmod("/root/AAA/agents/opencode/identity.key", 0o600)

# Write PEM
pem = pub.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
Path("/root/AAA/IDENTITY/keys/333-AGI_public.pem").write_bytes(pem)  # canonical name

# Update registry
with open("/root/arifOS/arifos/identity/agent_registry.json") as f: reg = json.load(f)
reg["agents"]["opencode"]["pubkey_hex"] = pub_hex
with open("/root/arifOS/arifos/identity/agent_registry.json", "w") as f: json.dump(reg, f, indent=2)
```

### Fix 2: Patch plugin arifosCall
```typescript
// BEFORE: return result?.content ?? result
// AFTER:
const content = result?.content as Array<Record<string, unknown>>
if (Array.isArray(content) && content.length > 0 && typeof content[0]?.text === "string") {
  try { return JSON.parse(content[0].text as string) }
  catch { return content[0].text }
}
return result
```

### Fix 3: Patch session.py challenge gate
```python
# /root/arifOS/arifosmcp/tools/session.py + /opt/arifos/app/arifosmcp/tools/session.py
from arifosmcp.runtime.crypto_auth import is_registered_actor as _is_reg
if actor_id not in _SOVEREIGN_MAP and not _is_reg(actor_id):
    return _make_init_hold(...)
```

### Fix 4: Use canonical actor_id in plugin
```typescript
const ACTOR_ID = "333-AGI"  // NOT "opencode"
```

## Verified test result
```
Step 1: challenge → nonce received (333-AGI:EMM98Vx...)
Step 2: signed → ed25519 signature (base64)
Step 3: init → session_token=True, mutation_allowed=True, band=LIMITED_MUTATE
```

## PEM file locations (canonical)
- `/root/AAA/IDENTITY/keys/333-AGI_public.pem` ← kernel reads from here
- `/root/AAA/IDENTITY/keys/opencode_public.pem` ← also exists, but kernel uses canonical name
- `/root/AAA/keys/` ← DIFFERENT directory, kernel does NOT read from here (confused us during debug)

## Key lessons (2026-08-12 update)

### Lesson 1: 9 locations, not 3-file chain
The real federation has 9+ locations storing an actor's public key. Two are
different copies of `agent_identities.json` (`/opt/arifos/identity/` read by
`crypto_auth.py` vs `/root/A-FORGE/data/` read by `session_auth.py`). Both must
be updated, or verification passes on one path but fails on the other.

### Lesson 2: `_normalize_actor` case sensitivity
The kernel's `resolve_actor_public_key("333-AGI")` normalizes to `"333-agi"` and
searches for `333-agi_public.pem`. If only `333-AGI_public.pem` exists, the
lookup returns `None` → `public_key_unavailable` → silent rejection. Create BOTH
filename variants.

### Lesson 3: Node.js PKCS#8 DER crash
`createPrivateKey({ key: der, format: "der", type: "pkcs8" })` fails with
`DECODER routines::unsupported` on some OpenSSL builds. **Use PEM instead:**
`readFileSync("identity_pkcs8.pem")`. Generate PEM once via Python's
`cryptography` library from the raw 32-byte seed.

### Lesson 4: Bridge signs the kernel's canonical, not the agent's name
The bridge plugin's `ACTOR_ID` must match what the kernel verifies. When the
kernel remaps `opencode` → `333-AGI` via `parent_agent`, the bridge must sign
`333-AGI:{nonce}`, not `opencode:{nonce}`. Verify by checking `DEBUG_PRE_RETURN`
in kernel logs for `claimed_id: 333-AGI`.

### Lesson 5: Rotate ALL 9 locations from ONE source
When regenerating a keypair, pick ONE source (PEM file or raw seed) and write
to all locations atomically. The rotation checklist:
1. Generate from ONE source
2. Write to: identity.key, identity_pkcs8.pem, opencode_public.pem,
   333-AGI_public.pem, 333-agi_public.pem, opencode_ed25519_public.pem
   (A-FORGE), .local/share/arifos/agent_keys/333-AGI_public.pem,
   both agent_identities.json copies
3. `systemctl restart arifos`
4. Verify: `python3 -c "from arifosmcp.runtime.crypto_auth import resolve_actor_public_key; ..."`
5. E2E: `arif_init` → `actor_verified: true`

The original "3-file chain" framing is incomplete. The worked example at the
top of this file should be treated as a subset; the rotation above is the
exhaustive recipe that actually gets identity to bind.
