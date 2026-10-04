---
name: opencode-ed25519-bootstrap-fix
description: "Class-level: wire any federation agent's Ed25519 identity into arifOS for MUTATE authority. Covers: identity registration (PEM path, agent-card bound_to, kernel normalization), 2-step challenge flow (mode=challenge → sign → mode=init), Node.js PKCS8 PEM key loading, MCP transport Accept header pitfall, A-FORGE deploy markers. Trigger: agent boots OBSERVE_ONLY (identity_declared ✓, authenticated ✗), or kernel returns HTTP 406, or arif_judge fails with verify-side rejection."
version: 1.0.0
---

# OpenCode Ed25519 Bootstrap Fix

## Symptom
OpenCode boots as `OBSERVE_ONLY (identity_declared ✓, authenticated ✗)`. All MUTATE-class tools gated. Bash, filesystem, A-FORGE proxy blocked.

## Root Causes (6 cascading failures)

### 1. identity.key ≠ identity.json (KEY MISMATCH)
The raw 32-byte seed in `identity.key` derived to a DIFFERENT public key than what was registered in `identity.json` and `agent_registry.json`.

**Fix:** Regenerate keypair, update all three files:
```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
seed = os.urandom(32)
priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
# Write identity.key (raw 32 bytes), update identity.json + agent_registry.json
```

### 2. Public key PEM not in kernel's resolve path
`resolve_actor_public_key()` in `crypto_auth.py` looks for PEM files in `/root/AAA/IDENTITY/keys/`, NOT `/root/AAA/keys/`.

**Fix:** Write PEM to correct path:
```python
# SPKI DER → PEM
pub.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
# Write to /root/AAA/IDENTITY/keys/{actor_id}_public.pem
```

### 3. arif_init(mode="challenge") rejected registered agents
`session.py` `_SOVEREIGN_MAP` only allowed sovereign actors (arif, ariffazil, 888) to request challenges.

**Fix:** Patch session.py to accept registered agents:
```python
from arifosmcp.runtime.crypto_auth import is_registered_actor as _is_reg
if actor_id not in _SOVEREIGN_MAP and not _is_reg(actor_id):
    return _make_init_hold(...)
```
Deploy to `/opt/arifos/app/arifosmcp/tools/session.py` + restart arifOS.

### 4. Actor ID normalization mismatch
Kernel normalizes "opencode" → "333-AGI" via agent-card.json `bound_to`. Challenge issued for "333-AGI" but plugin signed as "opencode" → `challenge_actor_mismatch`.

**Fix:** Plugin must use the CANONICAL actor_id that the kernel normalizes to:
```typescript
const ACTOR_ID = "333-AGI"  // NOT "opencode"
```

### 5. MCP response parsing (arifosCall)
MCP `tools/call` returns `{ result: { content: [{ type: "text", text: "<json string>" }] } }`. The plugin was returning `result.content` (the array) instead of parsing the inner JSON.

**Fix:**
```typescript
const content = result?.content as Array<Record<string, unknown>> | undefined
if (Array.isArray(content) && content.length > 0 && typeof content[0]?.text === "string") {
    try { return JSON.parse(content[0].text as string) }
    catch { return content[0].text }
}
return result
```

### 6. A-FORGE deployment markers
A-FORGE health reads `deployed_commit` from `/opt/a-forge/app/.git_commit` (DEPLOY_ROOT), but `make deploy-local` writes to `/root/A-FORGE/.git_commit` (SOURCE_ROOT).

**Fix:**
```bash
cat /root/A-FORGE/.git_commit > /opt/a-forge/app/.git_commit
```

## Node:crypto Ed25519 — PKCS8 PEM (PREFERRED) vs raw DER

### ⚠️ CRITICAL: PKCS8 DER prefix is 16 bytes, NOT 15

The **wrong** DER prefix (15 bytes + spurious 0x00 suffix) causes `ERR_OSSL_UNSUPPORTED: DECODER routines::unsupported` on Node.js 22+:

```
WRONG: 302e020100300506032b6570042204 (15 bytes) + seed + 00 suffix
RIGHT: 302e020100300506032b657004220420 (16 bytes) + seed, NO suffix
```

The byte `0x20` (decimal 32) after `0422` is the ASN.1 length of the Ed25519 seed.
Without it, OpenSSL cannot parse the structure.

### BEST PRACTICE: Use PKCS8 PEM, not raw DER

Generate once via Python, load via Node `createPrivateKey({key: pemBuffer})`:

```python
# Python: generate PEM from raw seed
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
seed = open("identity.key", "rb").read()
priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
pem = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
open("identity_pkcs8.pem", "wb").write(pem)
```

```typescript
// Node: load PEM (no DER wrapping needed)
const key = createPrivateKey({ key: readFileSync("identity_pkcs8.pem") })
const sig = sign(null, Buffer.from(message, "utf8"), key).toString("base64")
```

### Fallback: raw DER (if PEM not available)

```typescript
// CORRECT 16-byte prefix, no suffix
const PKCS8_PREFIX = Buffer.from("302e020100300506032b657004220420", "hex")
const der = Buffer.concat([PKCS8_PREFIX, rawSeed]) // 48 bytes total
const key = createPrivateKey({ key: der, format: "der", type: "pkcs8" })
```

## Cross-References
- **Pitfall encyclopedia:** `references/ed25519-pitfalls.md` — 7 categorized pitfalls with code + detection recipes
- **Verification script:** `scripts/verify-bootstrap.py` — run after any identity change, returns exit code 0/1

## When to Use (Class-Level Triggers)

- Agent boots `OBSERVE_ONLY (identity_declared ✓, authenticated ✗)`
- `arif_init(mode=challenge)` returns `INIT_JURISDICTION_HOLD`
- `arif_init(mode=init)` returns but `actor_cryptographically_verified: false`
- Kernel returns HTTP 406 on plugin POSTs
- A-FORGE health shows `deployment_drift=true` despite fresh build
- `sign_failed` errors in plugin receipt trail
- `challenge_actor_mismatch` in kernel logs



## Files Modified
- `/root/AAA/agents/opencode/identity.json` — new keypair
- `/root/AAA/agents/opencode/identity.key` — new seed (mode 600)
- `/root/AAA/agents/opencode/identity_pkcs8.pem` — PKCS8 PEM (for Node crypto)
- `/root/AAA/IDENTITY/keys/opencode_public.pem` — PEM
- `/root/AAA/IDENTITY/keys/333-AGI_public.pem` — PEM (canonical name)
- `/root/arifOS/arifos/identity/agent_registry.json` — updated pubkey
- `/root/arifOS/arifosmcp/tools/session.py` — registered agents can challenge
- `/opt/arifos/app/arifosmcp/tools/session.py` — deployed
- `/root/.config/opencode/plugins/arifos-kernel-bridge.ts` — full rewrite
- `/root/.config/opencode/plugins/arifos-judge-gate.ts` — Accept header fix
- `/opt/a-forge/app/.git_commit` — deploy marker

## Pitfall 7: HTTP 406 — MCP Accept Header (Silent Killer)

**Symptom:** Plugin gets `HTTP 406` when calling arif_judge or any MCP endpoint. The 406 is NOT a token rejection — it's a **transport layer rejection**.

**Root cause:** arifOS FastMCP server enforces MCP spec compliance:
```
POST without Accept header → 406 Not Acceptable
POST with Accept: application/json, text/event-stream → 200 OK
```

**The trap:** A plugin can successfully bind (get session_token) but then fail on every subsequent MCP call (judge gate, forge_shell) because those calls only send `Content-Type` but not `Accept`.

**Fix:** EVERY `fetch()` to arifOS MCP must include BOTH headers:
```typescript
headers: {
  "Content-Type": "application/json",
  "Accept": "application/json, text/event-stream",  // REQUIRED
}
```

This applies to:
- `arifos-kernel-bridge.ts` (arif_init calls) ← was OK
- `arifos-judge-gate.ts` (arif_judge calls) ← WAS MISSING, caused 406
- Any future plugin that POSTs to :8088/mcp

## Pitfall 8: identity.key permissions

`identity.key` must be `chmod 600`. Default file creation may leave it world-readable (644), which is a security violation. Always check after writing:
```bash
chmod 600 /root/AAA/agents/{agent_name}/identity.key
```

## Pitfall 9: Lowercase PEM filename OUTRULES canonical (silent resolver trap)

`resolve_actor_public_key()` in `crypto_auth.py` walks filename variants in this order:
```python
for name in (f"{aid}_public.pem", f"{actor_id}_public.pem", f"{aid}.pem"):
    p = _AAA_KEYS / name
    if p.is_file():
        key = _load_pem_public(p.read_bytes())
        if key: return key
```

If both `333-AGI_public.pem` AND `333-agi_public.pem` exist in `/root/AAA/IDENTITY/keys/`, the FIRST match wins, BUT the lowercase variant is matched by the same glob — making the result non-deterministic depending on filesystem ordering, OR worse: a stale lowercase file from prior rotation overrides fresh canonical updates.

**Symptom:** Bootstrap verification shows `kernel resolves 333-AGI` to pubkey X, but signature was made with key for pubkey Y. Verification silently fails.

**Fix:** Always check for BOTH case variants and overwrite the lowercase:
```bash
# After updating 333-AGI_public.pem:
cp /root/AAA/IDENTITY/keys/333-AGI_public.pem \
   /root/AAA/IDENTITY/keys/333-agi_public.pem

# Or delete the lowercase variant entirely:
rm /root/AAA/IDENTITY/keys/333-agi_public.pem
```

**Why this matters:** If you regenerate the keypair (Pitfall 1 fix), update `333-AGI_public.pem`, but forget the lowercase file — kernel still returns the OLD pubkey. Session binding appears to work but signature verification fails. Errors look like "challenge_actor_mismatch" but the actual mismatch is at the PEM level.

The `scripts/verify-bootstrap.py` script tests for this — if kernel pubkey ≠ derived pubkey, it returns exit 1 with both values printed.

## Pitfall 10: 5/5 verification = real, not ritual

Don't trust partial chain checks. "challenge returned nonce" + "init returned token" can both pass while mutation is still OBSERVE_ONLY. The full chain is:

```
1. Files exist (seed + PEM + identity.json)
2. pubkey consistent across PEM + keypair derivation
3. kernel.resolve_actor_public_key() returns matching pubkey
4. kernel.is_registered_actor() returns True
5. arif_init(challenge) returns nonce
6. arif_init(init, signed) returns session_token
7. session_token is non-null
8. mutation_allowed is True
9. authority_band is LIMITED_MUTATE (not OBSERVE_ONLY)
10. arif_judge does NOT return HTTP 406

Failure at any step → bootstrap is broken. Run all 10 before declaring MUTATE-capable.
```

`scripts/verify-bootstrap.py` runs steps 1-9 (10 is implicit via the Accept-header check).

## Verification Script

Run `scripts/verify-bootstrap.py` to test the full chain end-to-end.
