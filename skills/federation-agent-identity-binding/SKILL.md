---
id: federation-agent-identity-binding
name: federation-agent-identity-binding
version: 1.0.0
description: >
  Wire federation agents (OpenCode, OpenClaw, sibling harnesses) into the
  arifOS kernel via Ed25519 challenge-response. Covers Layer Zero MCP
  client config identity (bare-URL trap, the #1 most common failure),
  the 3-step challenge flow, identity key ↔ pubkey ↔ PEM alignment, MCP
  response envelope parsing, canonical actor_id normalization, the
  9-location registry drift surface, the Node.js PKCS#8 DER crash, and
  the full diagnostic sequence for OBSERVE_ONLY persistence. Forged
  after 4+5+1 bugs blocking OpenCode execution across three sessions
  (2026-08-12).
  execution, then extended after a second session revealed 5 more bugs in
  key-rotation across 9 registry locations (2026-08-12).
owner: 333-AGI
risk_tier: medium
autonomy_tier: T1-T2
floor_scope: [F1, F2, F4, F11, F13]
tags: [identity, ed25519, challenge, session-bootstrap, opencode, federation, opsec]
host_compatibility: [hermes, openclaw, opencode]
dependencies:
  skills:
  - arifos-federation-ops
---

# Federation Agent Identity Binding — Ed25519 Challenge Flow

> **Forged 2026-08-12** after 4 independent bugs blocked OpenCode from executing.
> **Sibling:** `arifos-federation-ops` §1 (SCT lifecycle, sovereign HMAC init).
> **NOT:** runtime identity verification (use `identity-verification`).
> This skill is SETUP-time wiring: get an agent from OBSERVE_ONLY → FULL/LIMITED_MUTATE.

## When to Use

**Always check Layer Zero FIRST** before touching keys or challenge flows:

- Does the agent's MCP config (`~/.config/<agent>/<agent>.json`) include `headers` with `X-Actor-Id`?
- If `headers: NONE` → fix the config first. Everything else is irrelevant.

Then, for OBSERVE_ONLY and refused execution:

- Agent boots OBSERVE_ONLY and refuses to execute tools
- `arif_init` returns session_token=None or mutation_allowed=False
- Agent's Ed25519 identity needs to be regenerated or re-aligned
- Wiring a NEW agent into the federation with mutation capability
- Debugging "challenge_actor_mismatch" or "INIT_JURISDICTION_HOLD"
- Agent attributes a simple wiring failure to a deep constitutional principle (→ run Layer Zero check first)

## Layer Zero: MCP Client Config (The First Failure Point)

Before any challenge flow, key sync, or registry entry matters — the agent's MCP client config must carry identity to the kernel. **This is the most common and most overlooked failure point.** All downstream diagnostics (challenge flow, 9-location sync, PEM wrapping) are irrelevant if the agent never identifies itself in the first place.

### The bare-URL trap

Many harness configs (OpenCode, Claude Code, etc.) declare MCP connections as bare URLs:

```json
// opencode.json — WRONG (bare URL, zero identity)
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

The kernel receives `POST /mcp` with NO actor_id, NO headers, NO signature. `session_auth.py::_resolve_authority_from_registry(None)` → `"anonymous"`. `authority.py::bind_authority_state()` → `actor_verified = False`. Every MUTATE-class tool → DENY.

### The kernel code path (traced 2026-08-12)

```
1. session_auth.py:82 _resolve_authority_from_registry(actor_id)
   → actor_id is None or empty → return "anonymous"
   → OR: actor_id present + in _ED25519_EXEMPT_SYSTEM_ACTORS → return "operator"
   → BUT: exempt list only fires if actor_id is actually TRANSMITTED in the request

2. authority.py:227 bind_authority_state()
   → state.actor.verified = False (no proof presented)
   → sess["actor_verified"] = False
   → sess["authority"] = "OBSERVE_ONLY" or "OBSERVER"

3. Every MUTATE tool → checks actor_verified → DENY
```

### Three fix tiers (simplest → most complete)

**Tier 1 — Send actor_id in MCP config (30 seconds):**

Add identity headers to the MCP client config:
```json
{
  "mcp": {
    "arifos": {
      "type": "remote",
      "url": "http://127.0.0.1:8088/mcp",
      "headers": { "X-Actor-Id": "opencode" },
      "enabled": true
    }
  }
}
```

If actor is in `_ED25519_EXEMPT_SYSTEM_ACTORS` (session_auth.py:54), this alone grants operator (OBSERVE + observer_mutate). NOT sufficient for judge/seal/FULL authority.

**Tier 2 — Register in DID registry:**

Add to `/opt/arifos/secrets/did-registry.json`:
```json
"did:arif:opencode": {
    "algorithm": "Ed25519",
    "description": "OpenCode CLI harness — 333-AGI warga",
    "organ_id": "opencode",
    "public_key_hex": "<ed25519 pubkey hex>"
}
```

Then `authority.py::_actor_in_did_registry("opencode")` → True → FULL authority when verified.

**Tier 3 — Full challenge-response:** the 3-step flow documented below.

### TWO exempt lists exist

| List | Location | Purpose |
|---|---|---|
| `_ED25519_EXEMPT_SYSTEM_ACTORS` | `session_auth.py:54` | Bootstrap MCP access — grants operator on name alone |
| `CANONICAL_ACTORS` aliases | `contracts/identity.py` | Identity normalization — maps aliases to canonical actor_id |

An agent can be in one but not the other. Check BOTH when diagnosing.

### PITFALL: False philosophical attribution (2026-08-12)

When an agent attributes a simple wiring failure to a deep constitutional principle, the diagnosis is misleading and sends investigators down the wrong path.

**Observed:** OpenCode told Arif it couldn't execute because "Gödel Rule 2: no self-certification — the kernel cryptographically refuses to mint an SCT for an unverified identity." The actual root cause: OpenCode's MCP config was a bare URL that never sent `actor_id` at all. The kernel didn't refuse a self-certification — it never RECEIVED any identity to evaluate.

**Diagnostic rule:** When an agent claims "the kernel refused for constitutional reason X," first check whether the kernel ever RECEIVED an identity claim. `session_auth.py::_resolve_authority_from_registry(None)` returns `"anonymous"` — that's not a constitutional gate, it's an empty input.

| Agent says | Actual cause | First check |
|---|---|---|
| "Gödel lock prevents self-certification" | MCP config is bare URL, no identity sent | Does MCP config include actor_id/headers? |
| "Kernel refuses to mint SCT" | actor_id is None → resolved as anonymous → OBSERVE_ONLY | Is actor_id transmitted in the request at all? |
| "I cannot sign for myself" | Plugin doesn't read identity.key or attach signature | Does plugin source code call `sign()` with the key? |
| "Cryptographic DENY" | `actor_verified=False` because no proof was presented | Was proof ATTEMPTED, or was it never sent? |

### Layer Zero diagnostic: always run FIRST

Before touching keys, PEMs, registries, or challenge flows — run this check:

```bash
# 1. Read the agent's MCP config
cat /root/.config/<agent>/<agent>.json | python3 -c "
import json,sys
cfg = json.load(sys.stdin)
mcps = cfg.get('mcp',{})
for name, conf in mcps.items():
    if '8088' in str(conf) or 'arifos' in name.lower():
        headers = conf.get('headers',{})
        print(f'MCP: {name}')
        print(f'  url: {conf.get(\"url\",\"?\")}')
        print(f'  headers: {headers if headers else \"NONE — bare URL\"}')
        print(f'  actor_id: {headers.get(\"X-Actor-Id\",\"MISSING\")}')
"
```

If `headers: NONE` → **stop here, fix the config first**. Don't waste time on key sync until the agent is at least identifying itself.

## The 9-Location Registry (REAL key drift surface)

The worked example says "3-file chain." Reality is **9 locations** that must all carry the same public key. `_normalize_actor()` lowercases actor_id before file search, so `333-AGI_public.pem` ≠ `333-agi_public.pem` in the kernel's search.

| Location | File | Kernel reads? | Pitfall |
|---|---|---|---|
| `/root/AAA/IDENTITY/keys/` | `opencode_public.pem` | ✅ `_AAA_KEYS` direct | |
| `/root/AAA/IDENTITY/keys/` | `333-AGI_public.pem` | ⚠️ Only if kernel queries `333-AGI` directly (not via normalize) | |
| `/root/AAA/IDENTITY/keys/` | `333-agi_public.pem` | ✅ `_normalize_actor("333-AGI") → "333-agi"` searches this | **MISSING = silent fail** |
| `/root/A-FORGE/IDENTITY/keys/opencode/` | `opencode_ed25519_public.pem` | ✅ `_AFORGE_KEYS` fallback | Old key stays here during key rotation |
| `/root/.local/share/arifos/agent_keys/` | `333-AGI_public.pem` | ✅ Runtime cache copy | Stale key after regeneration |
| `/root/A-FORGE/data/` | `agent_identities.json` | ✅ `session_auth.py` reads this | **Different file from /opt/ copy** |
| `/opt/arifos/identity/` | `agent_identities.json` | ✅ `crypto_auth.py` reads this | **Different file from /root/A-FORGE/ copy** |
| `/root/AAA/agents/<agent>/` | `identity.json` | ❌ Not read by kernel, but documents intended state | Public metadata only |
| `/root/AAA/agents/<agent>/` | `identity.key` | ❌ Bridge reads, kernel verifies against public | Bridge signs with THIS |

**Rotation checklist:**
1. Generate new keypair from ONE source (PEM or seed)
2. Write to ALL 9 locations
3. `systemctl restart arifos` (clears any lru_cache)
4. Verify with `resolve_actor_public_key("333-AGI")` returns correct hex
5. Test `arif_init` with Ed25519 signature → `actor_verified: true`

## The Node.js PKCS#8 DER Trap

On some Node.js + OpenSSL builds, wrapping a raw 32-byte Ed25519 seed with PKCS#8 DER prefix crashes with `error:1E08010C:DECODER routines::unsupported`. **Do not use raw DER wrap.**

**WRONG (fails on some builds):**
```typescript
const PKCS8_PREFIX = Buffer.from("302e020100300506032b6570042204", "hex")
const der = Buffer.concat([PKCS8_PREFIX, rawSeed, Buffer.from("00", "hex")])
const key = createPrivateKey({ key: der, format: "der", type: "pkcs8" })
```

**RIGHT (portable — use PEM file):**
```typescript
const pem = readFileSync("/root/AAA/agents/<agent>/identity_pkcs8.pem")
const key = createPrivateKey({ key: pem })
```

Generate PEM once with Python:
```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
priv = Ed25519PrivateKey.from_private_bytes(open("identity.key","rb").read())
pem = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
open("identity_pkcs8.pem","wb").write(pem)
```

## The 3-Step Challenge Flow

```
Step 1: arif_init(mode="challenge", actor_id="<canonical_actor>")
        → kernel issues single-use nonce (TTL ~120s)

Step 2: Sign "{actor_id}:{nonce}" with identity.key
        → raw 32-byte Ed25519 seed → PKCS8 DER wrap → sign → base64

Step 3: arif_init(mode="light", actor_id="<canonical_actor>",
                  actor_signature="<base64 sig>", nonce="<nonce>")
        → session_token + mutation_allowed + authority_band
```

## Canonical Actor IDs

The kernel normalizes agent_id → canonical actor_id via agent-card.json's `bound_to` field:
| agent_id | canonical (bound_to) | Notes |
|----------|---------------------|-------|
| opencode | 333-AGI | agent-card says bound_to: 333-AGI |
| ariffazil | arif | sovereign, handled via HMAC |
| openclaw | check agent-card | |

**CRITICAL:** The challenge must be requested AND signed using the CANONICAL actor_id. Using the agent_id (e.g. "opencode") causes `challenge_actor_mismatch`.

## Identity Key Files (the 3-file chain)

```
/root/AAA/agents/<agent>/identity.json       — public (agent_id, actor_id, ed25519_pubkey_hex, fingerprint)
/root/AAA/agents/<agent>/identity.key        — raw 32-byte Ed25519 seed (chmod 600)
/root/AAA/IDENTITY/keys/<canonical>_public.pem  — SPKI PEM (kernel resolves from here)
/root/arifOS/arifos/identity/agent_registry.json — JSON registry (pubkey_hex per agent)
```

**All three must agree.** Verify:
```python
seed = Path("identity.key").read_bytes()
pub = Ed25519PrivateKey.from_private_bytes(seed).public_key()
pub_hex = pub.public_bytes(Raw, PublicFormat.Raw).hex()
assert pub_hex == identity_json["ed25519_pubkey_hex"]
assert pub_hex == load_pem(open("333-AGI_public.pem").read()).public_bytes(Raw, PublicFormat.Raw).hex()
```

## The MCP Response Envelope Trap (THE #1 BUG)

arifOS `tools/call` returns results wrapped:
```json
{"result": {"content": [{"type": "text", "text": "{\"status\":\"completed\",\"result\":{\"nonce\":\"abc123\"}}"}]}}
```

**WRONG (old pattern):**
```typescript
return result?.content ?? result  // returns [{type:"text",text:"..."}] — a list
```

**RIGHT (fixed pattern):**
```typescript
const content = result?.content as Array<{text?: string}>
if (Array.isArray(content) && content[0]?.text) {
  return JSON.parse(content[0].text)  // returns the actual tool result
}
```

If the plugin does `challenge?.result?.nonce` on the raw list, nonce is `undefined` → `session.created.no_challenge` → silent OBSERVE_ONLY forever.

## Kernel Patch: challenge mode for registered agents

`session.py` line ~2404 has `_SOVEREIGN_MAP` gate. Sovereign-only by default. Must patch to also accept registered agents:

```python
# BEFORE (sovereign-only):
if actor_id not in _SOVEREIGN_MAP:
    return _make_init_hold(...)

# AFTER (sovereign + registered):
from arifosmcp.runtime.crypto_auth import is_registered_actor as _is_reg
if actor_id not in _SOVEREIGN_MAP and not _is_reg(actor_id):
    return _make_init_hold(...)
```

Deploy to BOTH `/root/arifOS/arifosmcp/tools/session.py` AND `/opt/arifos/app/arifosmcp/tools/session.py`, then restart arifos.

## Node.js Ed25519 Signing (OpenCode plugin)

Node:crypto doesn't accept raw 32-byte seed. Wrap as PKCS8 DER:
```typescript
const PKCS8_PREFIX = Buffer.from("302e020100300506032b6570042204", "hex")
const PKCS8_SUFFIX = Buffer.from("00", "hex")
const der = Buffer.concat([PKCS8_PREFIX, rawSeed, PKCS8_SUFFIX])
const key = createPrivateKey({ key: der, format: "der", type: "pkcs8" })
const sig = sign(null, Buffer.from(message), key)
return sig.toString("base64")
```

## Full Diagnostic Sequence

```
1. identity.key exists? 32 bytes? mode 600?
2. Derive pubkey from seed → matches identity.json pubkey_hex?
3. PEM at /root/AAA/IDENTITY/keys/<canonical>_public.pem → matches?
4. Challenge issuance: arif_init(mode="challenge") → nonce returned?
5. Sign nonce → verify locally: pubkey.verify(sig, message)?
6. Init: session_token returned? Check kernel logs for challenge_actor_mismatch
7. Plugin arifosCall() → does it parse MCP content[0].text?
8. Restart opencode serve (plugin loads only on session.created event)
```

## PITFALL: systemd restart regenerates identity keys (2026-08-12 verified)

A-FORGE ExecStartPost runs `register_with_aaa.py` which auto-derives a fresh Ed25519 keypair from `identity.key`. Every `systemctl restart a-forge` silently rotates the identity chain:

```
A-FORGE restart → register_with_aaa.py → derives new pubkey from identity.key
→ writes to /root/A-FORGE/IDENTITY/keys/opencode/opencode_ed25519_public.pem
→ old pubkey in /root/AAA/IDENTITY/keys/opencode_public.pem becomes STALE
→ signature fails
```

**Detection:** run E2E test after restart. If `actor_verified=false` post-restart but was `true` before, a key rotation happened.

**Mitigation options:**
1. Run the 9-location sync script after every organ restart (fragile)
2. Pin `identity.key` with `chattr +i` (prevents A-FORGE from deriving — may break other paths)
3. Accept the rotation as design: bridge re-derives from current PEM, kernel resolves current PEM

## PITFALL: pre_execution_gate.py phantom claims field (2026-08-12)

`pre_execution_gate.py:1410` checks:
```python
_sct_claims.get("session", {}).get("actor_bound")
```

But `verify_token()` returns flat claims: `{act_v, sid, actor, auth, av, ...}` — no `"session"` key. This gate ALWAYS HOLDS on any ACT with a session_token.

**Impact:** only blocks cross-organ forge calls routed through `pre_execution_gate`. Normal MCP tool calls (`arif_observe`, `arif_think`, etc.) bypass this gate.

**Latent bug** — doesn't block OpenCode's primary path but blocks A-FORGE integration if `pre_execution_gate` is ever called for a tool call.

**Fix (if needed):**
```python
# BEFORE (phantom field — always HOLD):
if not _sct_claims or not _sct_claims.get("session", {}).get("actor_bound"):
# AFTER (real field from ACT claims):
if not _sct_claims or not _sct_claims.get("av"):
```

## PITFALL: bridge must sign as canonical actor, not agent_id

When OpenCode bridge sends `actor_id="opencode"` to `arif_init`, the kernel remaps via `parent_agent` in `agent_identities.json` → `333-AGI`. Then verifies signature against `"333-AGI:{nonce}"` payload.

If bridge signed `"opencode:{nonce}"`, verification fails. The bridge MUST set:
```typescript
const ACTOR_ID = "333-AGI"  // canonical identity, NOT "opencode"
const message = `333-AGI:${nonce}`  // sign as canonical
```

**Rule:** always check `agent_identities.json` → `parent_agent` field → sign with the CANONICAL identity the kernel resolves to, not the agent_id you send.

## PITFALL: orphan key in agents/<agent>/ dir defeats whole signing path (2026-08-12)

When `agents/<agent>/identity_pkcs8.pem` exists (e.g. `ad611fe4...`) but its
public key is NOT in any registry the kernel reads, the plugin silently signs
with an orphan key. Symptom: local Ed25519 verify passes for whatever actor_id
is in the payload, but kernel still returns `ed25519_signature_invalid`
because `_resolve_authority_from_registry("actor_id")` returns a DIFFERENT
public key than the one signing.

**The trap:** the orphan key looks valid (PEM parses, signs cleanly), passes
local verify, but is a keypair that exists nowhere in:
- `/root/AAA/IDENTITY/keys/<actor>_public.pem` (kernel reads here first)
- `/root/A-FORGE/IDENTITY/keys/<actor>/`
- `/opt/arifos/secrets/did-registry.json`
- `/root/A-FORGE/data/agent_identities.json`
- `/opt/arifos/identity/agent_identities.json`

**Detection (5-minute definitive test — run BEFORE debugging anything else):**

```bash
# Sign manually with each candidate private key and submit to kernel.
# The kernel responds with "Invalid signature for actor=X" if mismatch,
# and "actor_verified=True" if match. Whichever key passes = the correct one.
python3 << 'EOF'
import urllib.request, json, base64
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.asymmetric import ed25519

priv = ed25519.Ed25519PrivateKey.from_private_bytes(
    load_pem_private_key(open('/root/AAA/IDENTITY/keys/333-AGI_private.pem','rb').read(), password=None)
        .private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
)
req = urllib.request.Request('http://127.0.0.1:8088/mcp',
    method='POST',
    data=json.dumps({'jsonrpc':'2.0','method':'tools/call','id':1,
        'params':{'name':'arif_init','arguments':{'actor_id':'333-AGI','mode':'challenge'}}}).encode(),
    headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream'})
nonce = json.loads(json.loads(urllib.request.urlopen(req).read())['result']['content'][0]['text'])['result']['nonce']

sig = base64.b64encode(priv.sign(f"333-AGI:{nonce}".encode())).decode()
req = urllib.request.Request('http://127.0.0.1:8088/mcp', method='POST',
    data=json.dumps({'jsonrpc':'2.0','method':'tools/call','id':2,
        'params':{'name':'arif_init','arguments':{'actor_id':'333-AGI','mode':'init',
            'actor_signature':sig,'nonce':nonce,'requested_authority':'FULL'}}}).encode(),
    headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream'})
result = json.loads(json.loads(urllib.request.urlopen(req).read())['result']['content'][0]['text'])
print('actor_verified:', result.get('actor',{}).get('actor_verified'))
print('authority_level:', result.get('actor',{}).get('authority_level'))
EOF
# If actor_verified=True → plugin must use this exact key path.
# If False → try the next candidate private key file.
```

This isolates the key-mismatch question from all other transport/config noise
(parent_agent, MCP envelope, MCP headers). Run it FIRST when any `arif_init`
fails with `ed25519_signature_invalid` after config looks correct.

## PITFALL: parent_agent param forces kernel-side remap (avoid) (2026-08-12)

Bridge plugins commonly add `parent_agent: "333-AGI"` to `arif_init` calls,
intending to declare "opencode is a downstream of 333-AGI." **This backfires:**

Kernel treats `parent_agent` as authoritative — when present, it overrides the
`actor_id` claim for verification purposes. The kernel will then verify the
signature against `parent_agent`'s key (333-AGI's), not the `actor_id` you sent.

Observed failure mode (2026-08-12): plugin sets `actor_id: "opencode"` +
`parent_agent: "333-AGI"` + signs `"opencode:{nonce}"`. Kernel log shows:
```
[KERNEL_AUTHORITY] actor=333-AGI actor_source=self_report verified=False
Ed25519 proof FAILED for actor=opencode reason=challenge_actor_mismatch
```

The "challenge_actor_mismatch" reason is the smoking gun — kernel sees
`claimed=333-AGI` (from parent_agent) but the nonce was issued under
`actor_id=opencode`, so the signed payload `"opencode:{nonce}"` cannot
match any of the verified payload formats under `333-AGI`.

**Rule:** do NOT pass `parent_agent` in `arif_init`. Sign with the canonical
actor_id directly (`ACTOR_ID="333-AGI"`, sign `"333-AGI:{nonce}"`). If the
plugin needs to record delegation lineage, do it in the receipt metadata,
not in the challenge/verify path.

## Common Failure Patterns

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| `actor_verified=False` / DENY with NO key errors | **Layer Zero: MCP config is bare URL** — no actor_id sent at all | Add `headers: {"X-Actor-Id": "<actor>"}` to MCP config; if exempt actor this is sufficient for operator |
| `session.created.no_challenge` | MCP response not parsed (array vs object) | Fix arifosCall to JSON.parse(content[0].text) |
| `challenge_actor_mismatch` | Signed with agent_id, kernel expects canonical | Use canonical actor_id (333-AGI not opencode) |
| `ed25519_signature_invalid` | identity.key seed ≠ registered pubkey | Regenerate keypair, update identity.json + PEM + registry |
| `INIT_JURISDICTION_HOLD` | Challenge mode sovereign-only (old code) | Patch session.py to accept is_registered_actor |
| OBSERVE_ONLY after plugin fix | Old OpenCode serve process still running | Kill + restart opencode serve |
| `Identity binding collapse` | actor_id in identity.json ≠ canonical form | Align identity.json actor_id with canonical |
| `ed25519_signature_invalid` (but local verify passes) | PEM key ≠ identity.key seed (two different keypairs in same chain) | Regenerate from ONE source, sync all 9 locations |
| `DECODER routines::unsupported` (Node.js) | PKCS#8 DER wrap fails on this OpenSSL build | Use PEM: `readFileSync("identity_pkcs8.pem")` instead of DER wrap |
| `ed25519_signature_invalid` for BOTH 333-AGI and opencode | `_normalize_actor` lowercase miss + old key in A-FORGE dir | Create `333-agi_public.pem` AND sync `/root/A-FORGE/IDENTITY/keys/` |
| `ed25519_signature_invalid` after `parent_agent` added to plugin | Kernel remaps claimed_actor via parent_agent, signature mismatch | Remove `parent_agent` from arif_init; sign canonical only |
| `ed25519_signature_invalid` despite locally-verifying signature | Plugin loads `agents/<agent>/identity_pkcs8.pem` (orphan key) — not in any registry | Run orphan-key detection test; switch plugin IDENTITY_KEY_PEM to a key whose pubkey is in `/root/AAA/IDENTITY/keys/<actor>_public.pem` |
| Kernel still stale after file sync | `__pycache__` has old module + kernel not restarted | `find /opt/arifos/app -name "__pycache__" -exec rm -rf {} + && systemctl restart arifos` |
| Verified pre-restart, fails post-restart | A-FORGE `register_with_aaa.py` ExecStartPost rotates keys | Re-sync all 9 locations from PEM source after every `systemctl restart a-forge` |
| `ed25519_signature_invalid` but keys match locally | PEM file ≠ identity.key (two keypairs in chain) | Regenerate PEM from current identity.key: `load_pem_private_key → private_bytes(PEM)` |
| `Identity binding collapse: claimed=opencode record_actor=333-AGI` | Bridge signs as `opencode` but kernel remaps to `333-AGI` | Set `ACTOR_ID="333-AGI"` in bridge, sign `333-AGI:{nonce}` |

## References

- ``references/`` — full OpenCode worked example (step-by-step)
- `references/opencode-9-location-key-drift-2026-08-12.md` — session where 3 keypairs drifted across 9 files; A-FORGE restart rotation; pre_execution_gate phantom claims bug
- `references/opencode-mcp-bare-url-identity-missing-2026-08-12.md` — **Layer Zero failure: MCP config was bare URL, agent never sent actor_id, kernel returned "anonymous". Agent falsely attributed denial to Gödel Rule 2 / no self-certification. Real fix: add identity headers to MCP config.**
- `references/opencode-orphan-key-and-parent-agent-footgun-2026-08-12.md` — **Plugin loaded orphan key (identity_pkcs8.pem) not in any registry. parent_agent param caused kernel remap trap. Definitive Python isolation test. Root cause: wrong private key file path, not philosophical denial.**

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: 2026-10-18-git-lane-identity-binding-and-agy-harness
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->


<!-- dead-pointer sweep 2026-10-23: unresolved artifacts from the gate report were replaced with the references/ directory. Basenames are preserved in the audit JSON. -->
