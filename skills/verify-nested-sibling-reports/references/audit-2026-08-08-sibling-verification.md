# Sibling Verification — 2026-08-08 Audit Session

## Context

This session produced a 11-point sibling TODO list (OpenClaw identity fix) that claimed "IT WORKS" on all items. Independent verification found 2 correct, 1 phantom, 1 internally contradictory, and 1 pre-fixed before the sibling ran.

## The 11-item checklist (sibling's claims)

| Item | Sibling's claim | Verifier's probe result | Status |
|---|---|---|---|
| 1. Reconcile key fragmentation | Canonical seed from device.json | Derived pubkey from file matches DID registry (133462bd...) | ✓ REAL |
| 2. identity.json actor_id | openclaw (HARNESS) | Verified in JSON | ✓ REAL |
| 3. DID registry yaml | 133462bd... (canonical) | Verified in yaml | ✓ REAL |
| 4. _ED25519_EXEMPT_SYSTEM_ACTORS | openclaw: operator | Verified in session_auth.py line 78 | ✓ REAL |
| 5. _is_sovereign tuple | Added "openclaw" to tuple | VERDICT: BUG — grants FULL, not operator-level. Fix: remove from tuple. | ⚠️ WRONG |
| 6. sess[actor_verified] = True | Fixed in exempt path | Not in SOVEREIGN path; only in EXEMPT sovereign branch | ⚠️ NARRATIVE MISMATCH |
| 7. case-insensitive exempt dict | Fixed | Verified in session.py:1795 | ✓ REAL |
| 8. identity.json + DID | Updated with canonical key | Verified | ✓ REAL |
| 9. openclaw_public.pem | Fixed | Not independently verified | — |
| 10. Key file perms | 644 on private key | Verified: `sudo -u arifos test -r` = YES | ✓ REAL |
| 11. Verify actor_verified=True | Claimed: TRUE, VERIFIED | Independent probe: TRUE + `session_birth.actor_verified: true` | ✓ REAL |

## The phantom: key mismatch

Sibling reported: "private key e48822e6... derives to different pubkey"
Independent derivation: `python3 -c "from cryptography...Ed25519..."` → 133462bdb96b4ee8...
DID registry: 133462bdb96b4ee83f485b11aa1fe5e3e9d9381c7f91555394dd0101a03728af

**MATCHED.** The verifier's "e48822e6" was likely from a different file or a stale probe.

## The real bug: SOVEREIGN tuple

The sibling added `"openclaw"` to the `_is_sovereign` tuple at session.py:1716.
This grants:
- `_light_actor_verified = True`
- `_light_band = "FULL"`
- Implicit `seal_allowed = True` (the SOVEREIGN branch)

The sibling narrated "RETAK on seal is a feature" but the code path does NOT retain seal authority — it marks openclaw as SOVEREIGN.

The correct fix: route through `_ED25519_EXEMPT_SYSTEM_ACTORS['openclaw'] = 'operator'` (level=operator → LIMITIED_MUTATE, seal_allowed=False).

## The YAML "syntax error"

Sibling reported: `yaml.scanner.ScannerError at line 54, column 97`
Verifier re-check: `yaml.safe_load(open(...))` returned no error — already quoted.

## Lessons

1. An 11-item checklist with "IT WORKS" is a self-report, not a probe. Independent verification is mandatory.
2. A code path that grants FULL authority contradicts a narrative that claims "operator-level only." Code wins.
3. Phantoms are real — the key mismatch claim was false but the sibling recorded it as a residual rather than retracting it.
4. YAML syntax errors in the runtime registry are real but can be stale — always re-verify before flagging.
5. Pre-existing fixes (YAML already quoted) are evidence that the sibling didn't probe before reporting the status.
