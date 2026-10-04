# arifOS key hierarchy — 2026-08-05 audit evidence

Reference for verifying claims about "the" signing key, TTL gate, and Gödel
lock on the arifOS kernel. All line numbers against live tree at audit time.

## 1. SCT TTL — three constants, one canonical default

"SCT TTL 3600s" is **correct**, but only if you cite the canonical minters:

| Constant | Value | File:line | Used by |
|---|---|---|---|
| `DEFAULT_TTL_SECONDS` | `3600` | `arifosmcp/runtime/sct.py:36` | `mint_sct(ttl=...)` default arg |
| `SESSION_TTL_SECONDS` | `3600` | `arifosmcp/runtime/session_auth.py:117` | legacy store-session expiry |
| `SESSION_TTL` | `3600` | `arifosmcp/runtime/webmcp/config.py:35` | WebMCP path |

**Trap:** `arifosmcp/runtime/session.py:170` and `session_registry.py:88`
both default `ARIFOS_SESSION_TTL_SECONDS=86400` (24 h) — that's the
**session-store** TTL, NOT the SCT token TTL. An audit citing 86400 for
the SCT TTL is conflating two stores.

TTL is a **config constant**, NOT a constitutional gate. No F13 ritual
needed to change it.

## 2. SCT signing-secret resolution chain (the dangerous fallback)

`_get_signing_secret()` in `arifosmcp/runtime/sct.py:113-146`:

1. `ARIFOS_SESSION_SECRET` env var
2. `ARIFOS_SESSION_SECRET_FILE` env var (read + strip)
3. `_PROD_SIGNING_KEY_PATHS` (sct.py:99-102):
   - `/opt/arifos/app/.signing_key`
   - `~/.arifos/signing_key`
   - Accepts 32 raw bytes OR any-length text (sct.py:134-137)
4. **Random fallback** (`secrets.token_bytes(32)`, sct.py:98) — non-strict mode only
5. Strict mode → `RuntimeError` at boot (sct.py:141-143)

### Key pitfalls
- **Random fallback post-restart** → SCTs unverifiable. Symptom: "all
  sessions invalid after restart." Fix: `ARIFOS_STRICT_MODE=1`.
- **"32 bytes gate everything" is wrong** — this HMAC key gates SCT
  session tokens ONLY. F13, vault attestation, observatory all use
  different keys (§3 below).
- **HMAC truncation**: `_sign()` (sct.py:428-431) truncates to 16 hex
  chars (8 bytes, 64 bits). Weak but acceptable given threat model. Flag
  if you encounter an SCT format with longer sigs — different signer.

## 3. F13 sovereign public key — candidates, legacy fragment, hardcoded divergence

`_PUBKEY_CANDIDATES` in `arifosmcp/core/f0_rootkey.py:58-66`:
1. `$ARIFOS_SOVEREIGN_PUBKEY_FILE` env override
2. `/run/sekrits/arifos_sovereign.pub`
3. `/run/secrets/arifos_sovereign.pub`
4. `/root/compose/sekrits/arifos_sovereign.pub`
5. `/root/.ssh/operator_did_ed25519.pub`

`arifosmcp/runtime/sovereign_verify.py:33-42` marks `did_arifos_public.key`
as **LEGACY FRAGMENT (different key)**, last resort only.
**But** `tools/forge.py:834` **hardcodes** that legacy path for per-call
Ed25519 verification of MUTATE/ATOMIC modes.

Implication: two different code paths resolve sovereign public keys by
different rules. Any audit that reads only one path will miss the
divergence. Always cross-check `sovereign_verify.py` against `forge.py:834`.

## 4. T3a Ed25519-exempt system actors (the designed "F13 bypass")

`tool_01_init_anchor.py:713-729` — `_ED25519_EXEMPT_SYSTEM_ACTORS` grants:
- `arif` → SOVEREIGN
- `forge/opencode/hermes` → operator

This skips Ed25519 proof at init. It is **constitutional-by-design** (bootstrap
bridge), not a hole. "F13 bypass" claims almost always refer to this code.
Verify: is the claim about THIS bridge, or about a genuinely missing gate?

## 5. Forge 3-stage F13 verification

`arif_forge` MUTATE/ATOMIC modes (`forge.py:805-870`), in order:

1. **Form check** (line 806): `actor_signature and nonce` non-empty → HOLD
   if missing, `f13_status: "ENFORCED — Ed25519 per-call signature required for mutation"`
2. **Key load** (line 834): `Path("/opt/arifos/secrets/did_arifos_public.key").read_bytes()`
   → missing file → HOLD, `f13_status: "REJECTED"`
3. **Ed25519 verify** (line 848): `verify(signature, sha256(session_id:actor_id:tool:mode:manifest:plan:chain:scope:nonce))`
   → fail → HOLD, `f13_status: "REJECTED — invalid Ed25519 signature (pre-execution gate)"`

## 6. Gödel lock — code exists AND is wired

`arifosmcp/runtime/godel_lock_gate.py:54-61`:
`SELF_CERTIFYING_TOOLS = frozenset({arif_judge, arifos_judge, arif_seal, arifos_seal, arif_forge})`

`_is_self_certifying()` (lines 78-101): compares `caller` vs `target_actor`
from params. Match → HOLD (lines 189-200) citing F11+F13:
`"F13 SOVEREIGN: sovereign cannot self-certify; external witness required"`

**What is NOT enforced (true gaps):**
- `godel_lock_gate()` is a **callable**, not auto-wired into every
  `arif_judge`. Search `godel_lock_gate(` in the pipeline to confirm.
- `_auditor_validated` (lines 121-132) reads `params.auditor_validated` —
  a forged param string WILL pass. Advisory, not cryptographic.
- `SELF_CERTIFYING_TOOLS` is a literal frozenset — adding a tool
  requires editing this file AND its test or it goes silent.

## 7. Consent token TTL (different beast)

`arifos/consent/consent_token.py:69` — default 300s (5 min), NOT the SCT.
This gates **human action approval** (Telegram → kernel), not session
capability tokens. A "3600 vs 300" TTL mismatch finding is usually
conflating these two.
