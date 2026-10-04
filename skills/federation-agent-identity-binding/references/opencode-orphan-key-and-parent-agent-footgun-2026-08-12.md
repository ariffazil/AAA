# OpenCode Orphan Key + parent_agent Footgun (2026-08-12)

## Session context

Third session debugging OpenCode ↔ arifOS SCT minting. Previous sessions fixed
Layer Zero (bare-URL config), the MCP response envelope, and actor_id
normalization. OpenCode now reports: "session_token_status: DENY: actor not
cryptographically verified — the swap recycle is a MUTATE, and the kernel will
not mint an SCT for an identity that isn't crypto-bound."

OpenCode attributed the denial to Gödel Rule 2 (no self-certification). Actual
root cause was a **wrong private key file**.

## Bug 1: Orphan key (root cause)

### Discovery

The plugin file `arifos-kernel-bridge.ts` loaded:

```typescript
const IDENTITY_KEY_PEM = "/root/AAA/agents/opencode/identity_pkcs8.pem"
```

This file exists and parses cleanly, but its public key is **not registered anywhere**:

```
AAA registry (kernel verify):  ca9609603e00849b8a80f75779be7e7fcaf991f31962e9e25296e95e88b68649
opencode_public.pem (AAA):     ca9609603e00849b8a80f75779be7e7fcaf991f31962e9e25296e95e88b68649  ← MATCHES AAA registry
333-AGI_public.pem (AAA):      b4dc368224acf81b93e7dcfebf341e35f66b91c8398a95a79657bed7cba91b03  ← KERNEL VERIFIES 333-AGI AGAINST THIS
identity_pkcs8.pem (plugin):   ad611fe4ef35178fd7bd400ed6b64c863ec953eba4196cda42a7e9c95881f555  ← ORPHAN (in no registry)
```

### Why it worked before F11 fix

Before the F11 registry sync (2026-08-12), `333-AGI` and `opencode` collided in
the registry — same keypair under both names. The orphan key accidentally
matched through the collision. F11 fix made them distinct, closing the hole —
and orphaning the plugin's key file.

### Fix

```typescript
// BEFORE (orphan key — not in any registry):
const IDENTITY_KEY_PEM = "/root/AAA/agents/opencode/identity_pkcs8.pem"

// AFTER (333-AGI's actual key — matches 333-AGI_public.pem in kernel's search path):
const IDENTITY_KEY_PEM = "/root/AAA/IDENTITY/keys/333-AGI_private.pem"
```

Verified:
```
actor_verified: True
authority_level: LIMITED_MUTATE
reason_code: APPROVED
session_token: act_v1.eyJhY3...zMtQ... (MINTED ✓)
```

## Bug 2: parent_agent remap trap

### Discovery

OpenCode's proposed fix was to change `ACTOR_ID` from `"333-AGI"` to `"opencode"`
and add `parent_agent: "333-AGI"` to declare delegation lineage. This was wrong.

### Kernel behavior

`arif_init` with `parent_agent: "333-AGI"` causes the kernel to remap the claimed
actor to `"333-AGI"` for verification. If the plugin signed as `"opencode"`, the
signed payload `"opencode:{nonce}"` doesn't match any of the verified payload
formats under `333-AGI`. Kernel logs:

```
[KERNEL_AUTHORITY] actor=333-AGI actor_source=self_report verified=False
Ed25519 proof FAILED for actor=opencode reason=challenge_actor_mismatch
```

`challenge_actor_mismatch` is the smoking gun — nonce was issued for `opencode`
but signature verification ran under `333-AGI` (because parent_agent override).

### Fix

Keep `ACTOR_ID = "333-AGI"` (the canonical identity), sign `"333-AGI:{nonce}"`,
and **do not pass `parent_agent`** in the arif_init call. Record delegation in
receipt metadata instead.

## Diagnostic test (definitive isolation)

The 5-minute Python test that isolated the key problem from all transport noise:

```python
# Sign directly with each candidate key, submit to kernel, observe verified status.
# Whichever key produces actor_verified=True is the correct one.
```

See SKILL.md "orphan key" pitfall section for the runnable script.

## Side effects cleaned up

During debugging, several wrong turns were taken and reverted:
- Added `did:arif:opencode` to DID registry → reverted (key was wrong)
- Overwrote opencode agent-card.json pubkey → reverted from backup
- Added `PARENT_AGENT` references to plugin → removed

## Scar

**"opencode-claims-but-mismatches-key"** — An agent claims an identity but
presents a key that no registry recognizes. The most insidious form of key drift:
local verify passes, but kernel-side verify fails. The fix is never philosophical
(Gödel, self-certification) — it's always a file path mismatch. Sealed in
VAULT999.
