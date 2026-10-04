---
name: federation-identity-reconciliation
description: "Diagnose and fix federation identity (Ed25519 + DID registry) mismatches when agents fail cryptographic verification at arifOS kernel. Covers the three-file consistency problem (key ↔ JSON ↔ YAML), the ARIFOS_DEV_DID_REGISTRY_FALLBACK=0 production path trap, the yaml.safe_load colon-in-description pitfall, the F12 AUTHORITY_SMUGGLING receipt-text trap, and the forge_vault MCP JSON-RPC recipe (stateful MCP, no HTTP REST route). Trigger: 'Invalid signature', 'actor_verified: False', 'Crypto Auth: Invalid signature for actor=X', DID key mismatch, or any forge_vault receipt task from Hermes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [identity, DID, ed25519, arifos, openclaw, crypto, federation]
    related: [arifos-federation-ops, openclaw-ops, agent-fork-governance, kernel-security-claim-audit]
---

# Federation Identity Reconciliation

When an agent calls `arif_init` and the arifOS journal shows `actor_verified: False` with `Crypto Auth: Invalid signature`, the signing path is almost always working. The bug is in the *verification* side — specifically, which public key the kernel is comparing against.

## Three-File Consistency Rule

Ed219 identity for every agent depends on three files agreeing:

| File | Written by | Read by |
|---|---|---|
| `/root/AAA/auth/keys/<actor>_private.key` | Key rotation / reconciliation | arifOS (via `_ACTOR_KEY_OVERRIDES` in crypto_auth.py) |
| `/opt/arifos/.secrets/did/registry.json` | Manual sync from YAML | arifOS `resolve_actor_public_key()` — **5th and last fallback** |
| `/root/AAA/secrets/did/registry.json` | Secondary copy (git-tracked, gitignored) | AAA a2a-server (`loadDidRegistry()`) |
| `/root/AAA/auth/did_registry.yaml` | Human canonical edit | arifOS **only if** `ARIFOS_DEV_DID_REGISTRY_FALLBACK=1` (disabled in prod) |

**All must carry the same pubkey.** If any one drifts, `actor_verified` goes false while the signing side claims success.

### The Four-Copy Sync Pattern (Grok Build 2026-08-09)

When reconciling a DID identity, you often need to sync **four** locations:
```
/opt/arifos/.secrets/did/registry.json   (arifOS runtime — most authoritative)
/root/AAA/secrets/did/registry.json      (AAA a2a-server — read via Node.js)
/root/A-FORGE/IDENTITY/keys/<actor>/     (A-FORGE auth keys)
/root/AAA/auth/keys/<actor>_private.key  (canonical key file)
```

After fixing ONE copy, verify ALL FOUR match before proceeding. The real-world pattern: Arif synced the key but only patched ONE location. The other agents silently failed verification because they read a stale copy.

### The R1 EACCES Enforcement Hole (Critical Discovery)

The `secrets/` directory (mode 700, owner root) blocks `aaa-a2a` service from reading DID registries, even though the service runs as root via systemd. Why? Because the service unit sets `User=root` but the kernel respects the ACL/mode on each component.

**Fix:** Use ACL (setfacl), not chmod, to grant read access without weakening the parent directory:
```bash
# Grant read-only to the aaa-a2a user/group on the DID subdirectory
setfacl -m u:aaa-a2a:r-x /root/AAA/secrets/did
setfacl -m u:aaa-a2a:r-- /root/AAA/secrets/did/registry.json
# Plus systemd drop-in to tell service which registry to load:
echo '[Service]\nEnvironment=DID_REGISTRY_PATH=/root/AAA/secrets/did/registry.json' \
  > /etc/systemd/system/aaa-a2a.service.d/30-did-registry.conf
systemctl daemon-reload
systemctl restart aaa-a2a
```

This was the real root cause of repeated "DID not in registry: did:arif:openclaw" failures — the registry WAS present, just unreadable.

## The Production Path Trap

```python
# arifOS runtime:
_DID_REGISTRY_CANDIDATES = [
    Path(os.getenv("ARIFOS_DID_REGISTRY_PATH",
         str(_RUNTIME_BASE / ".secrets/did/registry.json")))
]
if os.getenv("ARIFOS_DEV_DID_REGISTRY_FALLBACK") == "1":
    _DID_REGISTRY_CANDIDATES.extend([
        Path("/root/AAA/auth/did_registry.yaml"),
    ])
```

The systemd unit sets `ARIFOS_DEV_DID_REGISTRY_FALLBACK=0`. In production, arifOS reads JSON only. Humans edit YAML. **After key reconciliation, patch the JSON manually.**

The YAML has a known parsing issue: `:` characters in `description` fields trip `yaml.safe_load()`. Parse the YAML manually or patch the JSON directly with `json.load/dump`.

## Three-Way Verification Command

Run after every key rotation:

```bash
python3 << 'PYEOF'
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import json

actor = "<actor>"  # e.g. "openclaw"

# 1. From key file
key_path = f"/root/AAA/auth/keys/{actor}_private.key"
with open(key_path, "rb") as f:
    data = f.read()
sk = Ed25519PrivateKey.from_private_bytes(data) if len(data) == 32 else \
     __import__("cryptography.hazmat.primitives.serialization", fromlist=["load_pem_private_key"]) \
     .load_pem_private_key(data, password=None)
keyfile_pk = sk.public_key().public_bytes_raw().hex()

# 2. From JSON registry (what arifOS actually reads)
with open("/opt/arifos/.secrets/did/registry.json") as f:
    json_pk = json.load(f)["dids"][f"did:arif:{actor}"]["public_key_hex"]

print(f"KEY:  {keyfile_pk[:24]}...")
print(f"JSON: {json_pk[:24]}...")
print(f"MATCH: {keyfile_pk == json_pk}")
if keyfile_pk != json_pk:
    print("PATCH JSON before restart!")
PYEOF
```

## The Fix Recipe

```bash
# 1. Read existing JSON (what arifOS reads)
cat /opt/arifos/.secrets/did/registry.json | python3 -c "
import sys, json; d=json.load(sys.stdin); print(json.dumps(d['dids'].get('did:arif:<actor>','MISSING'), indent=2))"

# 2. Patch the stale public_key_hex to match the canonical key file
# (manual edit or write a JSON patch script)

# 3. Restart arifOS
systemctl restart arifos

# 4. Verify in journal
journalctl -u arifos --since "30 seconds ago" | grep -i "<actor>"
# Expect: verification_reason: ed25519_signature_verified:actor_nonce
# Expect: actor.actor_verified = True
```

## F12 AUTHORITY_SMUGGLING — Receipt Text Trap

When writing `forge_vault` receipt payloads via A-FORGE MCP, anything resembling self-authorized F13 language ("F13 SOVEREIGN acknowledged", "F13-ratified") in agent-authored `content` triggers `VOID` with `floor:F12, code:AUTHORITY_SMUGGLING`. The injection guard is doing its job.

**Correct pattern:** "issued for agent review" / "per CANON file X"
**Wrong pattern:** "F13-ratified" / "acknowledged by sovereign"

This applies to any text the agent writes and passes to `forge_vault` as receipt content. Reference the canon; never claim the sovereign's voice.

## forge_vault via A-FORGE MCP JSON-RPC — Working Recipe

A-FORGE `:7071` exposes MCP (`/mcp`), not HTTP REST. Direct `POST /vault/receipt` returns `Cannot POST`.

**Step 1 — Initialize (once):**
```bash
INIT=$(curl -si -X POST http://127.0.0.1:7071/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"hermes-asi","version":"1.0"}}}')
SID=$(echo "$INIT" | grep -i "mcp-session-id" | cut -d' ' -f2 | tr -d '\r\n')
```

Capture the `Mcp-Session-Id` header. Without it, every subsequent call fails: `"Bad Request: Mcp-Session-Id header is required"`.

**Step 2 — Write receipt:**
```bash
curl -s -X POST http://127.0.0.1:7071/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"forge_vault","arguments":{"mode":"receipt","name":"<slug>","content":"<summary>","reason":"SESSION_CLOSE","tier":"session.ledger","category":"session.receipt","actor_id":"hermes-asi","session_id":"<slug>"}}}'
```

**Step 3 — Parse:** response is doubly-nested JSON: `result.content[0].text` → JSON string containing `status`, `data.record.id`, `_meta.chain_hash`.

**Step 4 — Verify:**
```bash
curl -sf https://arif-fazil.com/999/verify | python3 -m json.tool
# Expect: verified:true, gap_count:0
```

## Ed25519-Exempt Actor Naming Ceiling (Verified 2026-08-12)

**Distinct from crypto key mismatch.** The sections above cover `actor_verified: False` when the Ed25519 signature works but the registry has the wrong pubkey. There is a SECOND root cause for `actor_verified: False` that requires a completely different fix.

### When it hits

Coding harnesses (qwen-code, claude-code, codex, kimi-code) are **Ed25519-exempt** — F13 sovereign directive skips the cryptographic key requirement for MCP bootstrap. They are added to the exempt dict:

```python
# /opt/arifos/app/contracts/identity.py
"qwen-code": "operator",  # F13 2026-08-12
"codex": "operator",      # F13 2026-08-12
```

The exemption fires correctly. The actor is **accepted** (`actor_bound: true`). But the kernel still returns `GUEST-xxx` with `actor_canonicalized: false` and `reason_code: NO_IDENTITY_BOUND`.

### The key diagnostic

```json
"actor_bound": true,              // name accepted
"actor_canonicalized": false,     // but NOT resolved to canonical identity
"actor_cryptographically_verified": false,  // no crypto proof presented
"authority_band": "OBSERVE_ONLY",
"session_mode": "guest_observe"
```

**This is the design working correctly, not a bug.** The exemption skips the crypto *requirement* but does NOT grant canonical identity *status*. Recognized ≠ trusted for mutation. `OBSERVE_ONLY` is the F1 Amanah ceiling for unverified actors — even exempt ones.

### What NOT to do

- Don't waste time syncing Ed25519 keys — the actor is exempt, keys are irrelevant.
- Don't add the actor to more registries — the registry entry already exists.
- Don't retry `arif_init` with different `actor_id` formats — the naming won't change the canonicalization outcome.

### What IS worth fixing (naming hygiene)

While the GUEST ceiling is structural, **naming chaos** around exempt actors creates real confusion. The pattern observed (qwen-code sweep 2026-08-12):

1. Registry key: `qwen-code` (canonical)
2. Actor header sent as: `qwen-code/FI-003` (slash form — wrong)
3. Old registry key: `qwen-code-fi003` (hyphenated — wrong)
4. Role label: `FI-003` (forge instrument number — correct as metadata, wrong as identity)

**The fix — unified naming convention:**

| Concept | Value | Where it lives |
|---|---|---|
| `actor_id` (identity) | `qwen-code` | MCP headers, hooks, `arif_init` arguments |
| `forge_instrument` (role) | `FI-003` | Metadata field only, never the actor_id |
| Registry key | `qwen-code` | `/opt/arifos/identity/agent_identities.json` |
| `CANONICAL_ACTORS` aliases | `["qwen", "qwen-code", "FI-003", "fi-003"]` | `identity.py` — alias list for normalization |

After fixing naming, the kernel still returns GUEST/OBSERVE_ONLY (that's the ceiling), but logs, receipts, and audit trails are clean and unambiguous. The next verified session for the same actor will bind `SEAL-xxx` instead of `GUEST-xxx`.

## False-Diagnosis Trap — Key Exists But Plugin Never Attaches Proof (Verified 2026-08-12)

A previous session concluded "OpenCode is OBSERVE_ONLY because it has no key" — factually wrong. The key, identity.json, and registry all exist. The real block: the CLI plugin calls `arif_init` without reading identity.key to sign the challenge.

**Always verify all four before diagnosing "missing key":**
1. `identity.json` exists?
2. `identity.key` exists?
3. Registry shows `pubkey=True, needs_keygen=False`?
4. Plugin source code reads key and attaches `ed25519_signature` to proof dict?

If 1-3 are true and 4 is false → **the problem is proof attachment, not the key**. Fix: patch the plugin/harness to sign and attach. NOT: generate a new key. NOT: patch 460 lines of unrelated code.

**Also found:** `identity.key` had permissions `-rw-r--r--` (644, world-readable). Private key material must be `chmod 600`.

## Six-Layer Registry Chaos (Verified 2026-08-12, OpenCode)

OpenCode's identity key can live in **6+ different registries**, each with its own copy of the public key. Rotating the key requires syncing ALL of them or verification silently fails:

| # | Registry path | Read by | Notes |
|---|---|---|---|
| 1 | `/root/AAA/agents/opencode/identity.key` | Plugin (source of truth for signing) | Raw 32-byte seed |
| 2 | `/root/AAA/agents/opencode/identity.json` | Plugin, docs | Carries `ed25519_pubkey_hex` |
| 3 | `/root/AAA/IDENTITY/keys/opencode_public.pem` | `crypto_auth.resolve_actor_public_key()` | PEM public key |
| 4 | `/root/AAA/IDENTITY/keys/333-AGI_public.pem` | Kernel (alias: opencode → 333-AGI) | Must match #3 |
| 5 | `/opt/arifos/identity/agent_identities.json` | Kernel runtime (primary) | `identity_proof.public_key_b64` + `public_key_hex` |
| 6 | `/root/A-FORGE/IDENTITY/keys/opencode/opencode_ed25519_private.pem` | `_ACTOR_KEY_OVERRIDES` in crypto_auth.py | PEM private key copy |

**The alias trap:** The kernel normalizes `opencode` → `333-AGI` at the crypto_auth layer (line 961). So `resolve_actor_public_key("opencode")` resolves `333-AGI_public.pem`, NOT `opencode_public.pem`. Both must carry the same pubkey.

**When rotating keys, write all 6.** Missing any one = silent `actor_verified: False`.

**Quick full-sync script:**
```bash
python3 << 'EOF'
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding, PublicFormat, PrivateFormat, NoEncryption, load_pem_public_key
)
import json, os, shutil

priv_raw = open("/root/AAA/agents/opencode/identity.key", "rb").read()
priv = Ed25519PrivateKey.from_private_bytes(priv_raw)
pub_raw = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
pub_hex = pub_raw.hex()
pub_pem = priv.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
priv_pem = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption)

targets = {
    # Reg 3: opencode_public.pem
    "/root/AAA/IDENTITY/keys/opencode_public.pem": pub_pem,
    # Reg 4: 333-AGI_public.pem (alias)
    "/root/AAA/IDENTITY/keys/333-AGI_public.pem": pub_pem,
    # Reg 6: A-FORGE private PEM
    "/root/A-FORGE/IDENTITY/keys/opencode/opencode_ed25519_private.pem": priv_pem,
}
for path, data in targets.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f: f.write(data)
    os.chmod(path, 0o600 if "private" in path or path.endswith(".key") else 0o644)

# Reg 5: agent_identities.json
p = "/opt/arifos/identity/agent_identities.json"
d = json.load(open(p))
import base64
d["opencode"]["identity_proof"]["public_key_hex"] = pub_hex
d["opencode"]["identity_proof"]["public_key_b64"] = base64.b64encode(pub_raw).decode()
with open(p, "w") as f: json.dump(d, f, indent=2)

print("ALL 6 REGISTRIES SYNCED")
print(f"pub_hex: {pub_hex[:24]}...")
EOF
```

## Node.js Ed25519 Key Loading — PKCS8 DER Trap (Verified 2026-08-12)

**The wrong pattern (fails on Node 22):**
```typescript
// ❌ This DER construction is rejected by OpenSSL in Node 22
const PKCS8_PREFIX = Buffer.from("302e020100300506032b6570042204", "hex")
const PKCS8_SUFFIX = Buffer.from("00", "hex")
const der = Buffer.concat([PKCS8_PREFIX, rawKey, PKCS8_SUFFIX])
const privKey = createPrivateKey({ key: der, format: "der", type: "pkcs8" })
// Error: ERR_OSSL_UNSUPPORTED — "invalid encoding"
```

**The working pattern:**
```typescript
// ✅ Generate PEM via Python cryptography library, then load PEM in Node
// Step 1 (Python, one-time):
//   from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
//   from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
//   priv = Ed25519PrivateKey.from_private_bytes(raw_key_32_bytes)
//   pem = priv.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
//   open("identity_pkcs8.pem", "wb").write(pem)

// Step 2 (Node.js, runtime):
import { createPrivateKey, sign, randomUUID } from "node:crypto"
import { readFileSync } from "node:fs"

const pem = readFileSync("/path/to/identity_pkcs8.pem")
const privKey = createPrivateKey(pem)  // PEM works, DER doesn't

const nonce = randomUUID()
const message = `${actorId}:${nonce}`
const sig = sign(null, Buffer.from(message, "utf8"), privKey)
const sigB64 = sig.toString("base64")
```

**Why:** OpenSSL in Node 22 changed Ed25519 PKCS8 DER handling. The manual 30-byte concatenation that worked in Node 18 is rejected. PEM is the only reliable cross-version format.

## Two-Registry Sync Pattern (Verified 2026-08-12)

Two identity registries must stay synchronized:

| Registry | Location | Consumed by |
|---|---|---|
| Primary | `/opt/arifos/identity/agent_identities.json` | arifOS kernel runtime |
| Mirror | `/root/A-FORGE/data/agent_identities.json` | A-FORGE execution layer |

**Drift symptom:** A-FORGE missing entries that /opt/arifos has (or vice versa). In practice, /opt/arifos is the authoritative source — A-FORGE lags behind when new agents are registered.

**Sync recipe:**
```bash
python3 -c "
import json
opt = json.load(open('/opt/arifos/identity/agent_identities.json'))
forge = json.load(open('/root/A-FORGE/data/agent_identities.json'))
missing = set(opt.keys()) - set(forge.keys())
for k in missing:
    forge[k] = opt[k]
json.dump(forge, open('/root/A-FORGE/data/agent_identities.json','w'), indent=2)
print(f'Synced {len(missing)} entries: {sorted(missing)}')
print(f'Match: {set(forge.keys()) == set(opt.keys())}')
"
```

Also verify `identity.py` is identical across three trees:
```bash
md5sum /opt/arifos/app/contracts/identity.py /root/arifOS/contracts/identity.py /root/arifOS/arifosmcp/contracts/identity.py
```

All three must match. If they don't, copy from `/opt/arifos/app/contracts/` (the deployed runtime) to the source trees and redeploy.

## Naming Sweep Verification Pitfall — Escaped JSON Grep

When verifying that deeply-nested JSON settings files (e.g. `/root/.qwen/settings.json` — contains bash commands with doubly-escaped JSON inside hook definitions) are clean:

- `grep -c "qwen-code/FI-003"` on the raw file may return **0** even though the pattern appears in checkpoint/tmp snapshots from prior sessions.
- `grep -rn` across a directory will match `tmp/` checkpoint snapshots (historical), not the live config.
- **Always filter out:** `tmp/`, `checkpoints/`, `.bak`, `.archive`, `quarantine` when scanning for active references.
- **Verify with Python JSON parser** to confirm the decoded structure, not just raw string matching.

## Full-Spectrum Sweep Verification Protocol

When anyone (sibling agent, subagent, F13) claims "sweep/fix done", verify **every claim** against live state. Don't trust the claim. This protocol catches false-positive "DONE" reports.

**The 6-point checklist:**

| # | Check | How | What to look for |
|---|---|---|---|
| 1 | **Config files** | Read each claimed file path, grep for old patterns | Stale refs like `qwen-code/FI-003` in headers/hooks |
| 2 | **Runtime canonicalization** | `python3 -c "from identity import normalize_actor_identity; print(normalize_actor_identity('<old-form>'))"` | Must resolve to canonical name, not `None` |
| 3 | **Source ↔ Deploy drift** | `md5sum /opt/arifos/app/contracts/identity.py /root/arifOS/contracts/identity.py /root/arifOS/arifosmcp/contracts/identity.py` | All three must match |
| 4 | **Registry parity** | Compare `/opt/arifos/identity/` vs `/root/A-FORGE/data/` key sets | Must be identical |
| 5 | **Git dirty count** | `cd /root/<repo> && git status --porcelain \| wc -l` | Uncommitted sweep changes = durability risk |
| 6 | **Federation health** | Probe all 8 organ health endpoints + SearXNG + LiteLLM | Sweep must not have broken anything |

**Automation:** Run `scripts/canonicalize_identity.py` for checks 1-4 in one pass.

**When sweep claims are false-positive:** The sibling/subagent probe was taken BEFORE the fix was applied (stale checkpoint file). Compare the file modification timestamp against the probe timestamp. If probe < fix, the claim is stale, not wrong — but the claim is still unverified.

**Key diagnostic output format:**
```
═══ CHAOS AUDIT — <sweep name> ═══
✅ / ✅ / ⚠️ / ❌ per surface
Bottom line: [clean | chaos found | uncommitted risk]

## AAA agent_registry.json — blake3 Fingerprint Sync (Verified 2026-08-12)

A THIRD registry type, distinct from both the DID chain (`did/registry.json`) and the kernel runtime (`agent_identities.json`). The file `/root/arifOS/arifos/identity/agent_registry.json` is the AAA-level identity directory — the source of truth for SCT signing and F11 audit trails.

### The blake3 fingerprint formula

```python
import blake3
def compute_fingerprint(agent_id, actor_id, pubkey_hex, bound_to):
    canonical = f"{agent_id}|{actor_id}|{pubkey_hex}|{bound_to}"
    return blake3.blake3(canonical.encode()).hexdigest()[:32]
```

Found in `/root/arifOS/arifos/identity/agent_identity.py:170`. The `fingerprint` field in registry MUST match this formula. If it doesn't, the registry was written by a non-canonical source (stale sweep script, manual edit, or pre-blake3 migration).

### How drift happens

1. Keygen script regenerates PEM files (fixes file-level collisions).
2. Registry is NOT updated → still holds old `pubkey_hex` + old `fingerprint`.
3. Agent report claims "zero collisions" based on file-level SHA-256.
4. Registry still has collided pubkey_hex for two different agents.
5. F11 audit trail is broken at the directory that matters for SCT signing.

### Sync recipe

Run `scripts/sync_agent_registry_fingerprints.py` — re-derives pubkey_hex from PEM files, recomputes blake3 fingerprints for all agents, writes, then **re-reads from disk** to verify.

### Collision class: half-fix masquerading as complete fix

The most dangerous pattern observed: PEM files regenerated correctly (file-level zero collisions), but `agent_registry.json` not synced. The fix report declared "19 keypairs, zero collisions" — true at file level, false at registry level. 333-AGI and opencode had identical `pubkey_hex` in the registry despite having distinct PEM files.

**Lesson:** "Zero collisions" must be verified at EVERY layer that stores identity material — not just the layer you happened to fix.

## References

- **`references/naming-sweep-pattern.md`** — Complete identity naming sweep pattern: when to run, the canonical-name-vs-role-label decision rule, two-registry sync recipe, three-tree identity.py md5 check, and the Ed25519-exempt GUEST ceiling insight.
- **`references/agent-registry-blake3-sync.md`** — Session transcript of the 2026-08-12 blake3 fingerprint sync: the verify-from-disk bug, the stale-buffer-amend cycle, and the half-fix collision discovery.

## Pitfalls

- `yaml.safe_load()` fails on descriptions containing `:` (e.g. `source: /root/...`) — parse manually or patch JSON directly.
- The JSON registry at `/opt/arifos/.secrets/did/registry.json` must be patched AFTER any key reconciliation. The YAML alone is NOT sufficient in production.
- forge_vault has NO HTTP REST route — all calls via MCP JSON-RPC with session header.
- F12 triggers on agent-authored text, not the tool's own error messages. Rephrase, don't fight it.
- `ARIFOS_DEV_DID_REGISTRY_FALLBACK=0` in production: YAML is only a dev-mode fallback. Don't assume humans editing YAML fixes production verification.
- **Ed25519-exempt ≠ trusted.** Exempt actors (coding harnesses) are accepted but NOT canonicalized. GUEST/OBSERVE_ONLY is the structural ceiling, not a fixable bug. Don't chase key sync for exempt actors.
- **Two registries drift silently.** `/opt/arifos/identity/` and `/root/A-FORGE/data/` must be manually synced after adding new agents. No automated sync exists.
- **`forge_instrument` is a role, not an identity.** Never use `FI-003` (or similar) as an `actor_id` value. The canonical name (e.g. `qwen-code`) is the identity; the FI number is metadata.
- **Two-step challenge flow is mandatory (2026-08-12).** `arif_init(mode="challenge")` → sign kernel-issued nonce → `arif_init(mode="light")` with signature. Self-generated nonces (randomUUID) fail with `challenge_not_issued`. The plugin MUST request the nonce from the kernel first.
- **SOVEREIGN_MAP blocks registered agents (2026-08-12).** By default, `mode="challenge"` in session.py only accepts sovereign actors (arif, 888, ariffazil). Registered federation agents (opencode, etc.) are rejected. Patch: add `is_registered_actor(actor_id)` check alongside `_SOVEREIGN_MAP`.
- **Canonical actor_id in identity.json (2026-08-12).** Set `actor_id` to canonical form (`"opencode"`, not `"opencode/FI-???"`). The kernel's identity binding check refuses when claimed actor doesn't match registry's actor_id.
- **Use mode="light" not mode="init" for challenge-response (2026-08-12).** The full `mode="init"` path triggers constitution_hash_probe that can block non-sovereign agents. `mode="light"` goes through `verify_init_identity()` directly and binds the actor with the Ed25519 proof.
- **identity.key seed must match identity.json pubkey (2026-08-12).** The raw 32-byte seed in identity.key may NOT produce the pubkey listed in identity.json if the key was regenerated at some point but identity.json wasn't updated. Always verify: derive pubkey from seed → compare to identity.json.
- **VERIFY-FROM-DISK after any registry write (2026-08-12).** After `json.dump()` to a file, always re-read with `json.load(open(path))` in a SEPARATE step before verifying. Never verify from the in-memory dict you just mutated — it holds the values you computed, not necessarily what landed on disk. The fix script ran, said "19/19 matched," committed — but the committed file had stale fingerprints because the write didn't survive to git's working copy. The only safe verify is: (1) write file, (2) read file back, (3) compare. Not: (1) write file, (2) compare dict.
- **Half-fix masquerading as complete fix (2026-08-12).** PEM regeneration is layer N of identity sync. `agent_registry.json` is layer M. Fixing layer N and claiming "zero collisions" without re-checking layer M = false-positive report. Verify EVERY layer that stores identity material.

## Automation

- `scripts/canonicalize_identity.py` — Full sweep in one pass: registry sync (primary + mirror), source tree sync (3 identity.py trees), normalization verification (7 test cases). `--dry-run` for safe preview.
