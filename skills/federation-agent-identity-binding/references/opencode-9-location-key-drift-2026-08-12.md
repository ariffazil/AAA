# OpenCode 9-Location Key Drift — 2026-08-12 Session

> Session where 3 different keypairs existed simultaneously across 9 files.
> Root cause: A-FORGE restart silently rotates keys via register_with_aaa.py.

## The 3 Keypairs

| Source | Public Key (first 8) | Where |
|---|---|---|
| identity.key (original) | `88c0ee8f` | `/root/AAA/agents/opencode/identity.key` |
| opencode_public.pem (old) | `2e9919ef` | `/root/AAA/IDENTITY/keys/opencode_public.pem` |
| agent_identities.json (old) | `de27f5ee` | `/opt/arifos/identity/agent_identities.json` |

These 3 never matched each other. OpenCode was permanently OBSERVE_ONLY.

## Fix Sequence

1. Generated fresh keypair as single source of truth (PEM)
2. Synced all 9 locations from PEM-derived public key
3. Added `333-AGI` entry to both `agent_identities.json` files (parent_agent remap)
4. Created `333-agi_public.pem` (lowercase — `_normalize_actor` lowercases before file search)
5. Synced `/root/.local/share/arifos/agent_keys/333-AGI_public.pem` (third copy)
6. Cleared `__pycache__` on kernel to flush stale module caches
7. Patched bridge to use `createPrivateKey(PEM)` instead of raw DER (Node.js crash)
8. Set `ACTOR_ID = "333-AGI"` in bridge (sign as canonical, not agent_id)

## A-FORGE Restart Key Rotation

After `systemctl restart a-forge`:
- `register_with_aaa.py` (ExecStartPost) derives new pubkey from `identity.key`
- Writes to `/root/A-FORGE/IDENTITY/keys/opencode/opencode_ed25519_public.pem`
- Old pubkeys in other locations become stale
- Must re-sync after every A-FORGE restart

## The 9 Locations (final checklist)

```
/root/AAA/agents/opencode/identity.key         ← raw 32-byte seed
/root/AAA/agents/opencode/identity_pkcs8.pem   ← PKCS#8 PEM (bridge uses THIS)
/root/AAA/agents/opencode/identity.json         ← metadata (pubkey hex)
/root/AAA/IDENTITY/keys/opencode_public.pem     ← SPKI PEM
/root/AAA/IDENTITY/keys/333-AGI_public.pem      ← SPKI PEM (canonical actor)
/root/AAA/IDENTITY/keys/333-agi_public.pem      ← SPKI PEM (lowercase normalized)
/root/A-FORGE/IDENTITY/keys/opencode/opencode_ed25519_public.pem  ← A-FORGE fallback
/root/A-FORGE/IDENTITY/keys/opencode/opencode_ed25519_private.pem ← A-FORGE private
/root/.local/share/arifos/agent_keys/333-AGI_public.pem  ← runtime cache
/opt/arifos/identity/agent_identities.json      ← kernel registry (opencode + 333-AGI entries)
/root/A-FORGE/data/agent_identities.json        ← session_auth.py registry
```

## E2E Verification Command

```bash
# Sign as 333-AGI and verify against kernel
node -e "
const { createPrivateKey, sign, randomUUID } = require('node:crypto')
const { readFileSync } = require('node:fs')
const pem = readFileSync('/root/AAA/agents/opencode/identity_pkcs8.pem')
const privKey = createPrivateKey(pem)
const nonce = randomUUID()
const sig = sign(null, Buffer.from('333-AGI:'+nonce, 'utf8'), privKey)
fetch('http://127.0.0.1:8088/mcp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream' },
  body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name: 'arif_init', arguments: {
    actor_id: '333-AGI', actor_signature: sig.toString('base64'), nonce: nonce,
    intent: 'verify', requested_authority: 'FULL', verbosity: 'minimal'
  }}})
}).then(r => r.json()).then(d => {
  let result = {}; try { result = JSON.parse(d.result.content[0].text) } catch(e) {}
  const eff = result.result?.effective_state || {}
  console.log('verified:', eff.actor_verified, 'auth:', eff.authority_band, 'mut:', eff.mutation_allowed)
})
"
```

## pre_execution_gate.py Phantom Claims Bug

Line 1410 checks `claims["session"]["actor_bound"]` — phantom field.
Actual ACT claims have `"av"` (actor verified boolean).
Latent: only blocks cross-organ forge routing, not normal MCP tool calls.

DITEMPA BUKAN DIBERI ⚒️
