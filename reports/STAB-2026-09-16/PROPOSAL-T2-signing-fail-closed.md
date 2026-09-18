# PATCH PROPOSAL — T2: Signing Lane Fail-Closed
> Author: Hermes (KVM8, truth node) · 2026-09-18 · **NOT APPLIED**
> Target: `/root/AAA/auth/signing_server.py`
> Class: containment · authority-critical component
> **Status: 888 HOLD — awaiting F13. This file is the authored patch, not a mutation.**

## Why not self-applied

The signing server mints sovereign Ed25519 signatures. Three reasons this is not a
self-execute:
1. It is a **verifier/authority component** — self-evolution asymmetry puts it under HOLD.
2. MACHINE_MAP places KVM8 as **truth** node; execution belongs to the execution lane.
3. Repo writer is **kimi-code/FI-008**, active through the night — any write races it.

---

## Defect A — PAM guard is opt-in (fail-open by omission)

### BEFORE
```python
        # PAM credential confirmation (transitional — not sovereign presence proof)
        pam_user = os.environ.get("AAA_PAM_USER", "")
        if pam_user:
            try:
                import pam

                if not pam.authenticate(pam_user, os.environ.get("AAA_PAM_PASS", "")):
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'{"error":"pam authentication failed"}')
                    return
            except ImportError:
                pass  # PAM not available — skip (transitional)
```

**Failure modes:**
- `AAA_PAM_USER` unset (current state — service sets only `PYTHONUNBUFFERED=1`) ⇒ **block skipped entirely**
- `import pam` fails ⇒ **silently skipped**

Both paths proceed to sign.

### AFTER
```python
        # Sovereign-presence guard — FAIL CLOSED.
        # Absent credential is a refusal, never a skip. (T2, 2026-09-18)
        pam_user = os.environ.get("AAA_PAM_USER", "").strip()
        if not pam_user:
            logger.error("SIGNING REFUSED: AAA_PAM_USER unset — sovereign presence unproven")
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error":"sovereign presence unproven: signing credential not configured"}')
            return
        try:
            import pam
        except ImportError:
            logger.error("SIGNING REFUSED: PAM unavailable — sovereign presence unverifiable")
            self.send_response(501)
            self.end_headers()
            self.wfile.write(b'{"error":"sovereign presence unverifiable: PAM not available"}')
            return
        if not pam.authenticate(pam_user, os.environ.get("AAA_PAM_PASS", "")):
            logger.warning("SIGNING REFUSED: PAM authentication failed for user=%s", pam_user)
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error":"pam authentication failed"}')
            return
```

### Predicted effect — BREAKING CHANGE, stated plainly
With `AAA_PAM_USER` unset (today's config), **the signing lane stops signing entirely.**
That is the intended semantic (fail-closed), but it means **the one-tap approval flow will
break until credentials are configured.** This is a deliberate availability-for-integrity
trade. F13 must accept it knowingly, or the alternative is:

- **Option B (soft):** keep current behaviour but log a **loud per-call WARNING** that
  sovereign presence is unproven, and surface a metric. Does not close the hole; makes it
  audible.
- **Option A (hard, above):** close the hole; accept the availability loss.

**Recommendation: Option A + configure `AAA_PAM_USER` in the same change**, so the lane
stays live *and* the guard is real.

---

## Defect B — legacy path signs unverified payloads

### BEFORE
```python
        else:
            # Legacy path — deprecated, logged
            logger.warning("LEGACY: signing raw canonical_json without challenge verification (deprecated path)")
            payload_to_sign = canonical_json
```
Warns, then signs. Bypasses the `critical_fields` binding
(`actor, nonce, candidate_hash, action_class, authorization_session_id`) that makes the
challenge path sound.

### AFTER
```python
        else:
            # Legacy path removed — T2 (2026-09-18).
            # Signing without challenge verification defeats the critical_fields binding.
            logger.error(
                "SIGNING REFUSED: no challenge_id — legacy unverified path is closed. "
                "Mint a challenge via arifOS crypto_auth first."
            )
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"challenge_id required — unverified signing is closed"}')
            return
```

### Check before applying
Confirm no live caller depends on the legacy path. Search for callers that POST
`canonical_json` without `challenge_id`. If any exist, they must be migrated first.

---

## Defect C — GENESIS AUTHORITY: who mints the first challenge?

OpenClaw's question: *arif_init is not a signing point; the signing lane is not a minting
point. So a third actor mints the initial challenge. Who?*

**Answer, from code:**

```python
# runtime/crypto_auth.py:208
def issue_authorization_challenge(
    actor: str,                    # ← TRUSTED PARAMETER, no identity check
    authorization_session_id: str,
    candidate_hash: str, ...
) -> dict:
```

and

```python
# runtime/tools.py:24570
async def _arif_challenge_tool(actor_id: str = "ARIF", ...)   # ← defaults to ARIF
```

**The minter performs no identity check.** It accepts `actor` as a trusted string and mints.

### Is that a hole? Assessed honestly — NOT an external one.

**Exposure check (static, no mint attempted):**
```
runtime/tools.py:25305  "arif_challenge": _arif_challenge_tool   ← in internal tool map
live MCP tools/list (8): arif_init, arif_observe, arif_think,
                         arif_route, arif_memory, arif_judge, arif_forge, arif_seal
arif_challenge exposed: False
```
**The genesis minter is internal-only — not reachable from the public MCP surface.**
`issue_authorization_challenge` is called from `arif_kernel_intercept.py` and the init anchor,
i.e. inside the kernel's own flow.

**Why unauthenticated minting is correct here:** a challenge is a *request*, not a grant.
Minting one confers nothing — it only creates a candidate for the sovereign to approve or
reject. Making minting unauthenticated is defensible precisely because the authorization
decision lives at the *signing* step.

**This relocates the severity rather than raising it:** if minting is open-but-harmless, then
**the signing step carries the entire security burden.** Which returns to Defect A — and Defect
A is that the only human-presence gate on that step is disabled.

### Corrected severity for the pair (A + C together)

| Layer | State |
|---|---|
| localhost-only bind (`127.0.0.1:18900`) | ✅ holds |
| origin check | ✅ holds |
| challenge must exist in authoritative store | ✅ holds |
| `critical_fields` payload binding | ✅ holds |
| **sovereign-presence proof (PAM/WebAuthn)** | ❌ **disabled** |

**What remains is network-locality plus state-binding — not presence.** An attacker with
localhost reach (or any local process/agent) who can mint a challenge internally could obtain a
sovereign signature, because the one layer that would demand *a human* is off.

**Not exploited, not tested.** Reported from code reading. No challenge minted, no signature
requested — attempting either would be forging sovereign authority.

### Feedback into the F13 decision on T2

This makes the Option A / Option B trade sharper: the PAM guard is not defence-in-depth
redundancy. It is **the only presence layer in the chain.** Option B (warn-only) leaves the
chain resting entirely on locality. Recommend Option A + configure credentials.

---

## T27 — STARTUP GUARD (the only item of OpenClaw's four not yet deployed)

Verified against deployed `e66b2643f`: OpenClaw's items 1–3 are **already live**.
Item 4 (startup check) is **genuinely missing** — `__main__` loads the sovereign key but never
asserts the credential. Authoring it here as the one remaining piece.

### Config-assert at startup (fail-loud, not silent-at-runtime)

Insert in `__main__` before `serve_forever()`:

```python
    # T27 (2026-09-18): fail-loud at startup. A signing lane with no credential is
    # not "running healthy" — it is dead and should say so before serving traffic.
    if not os.environ.get("AAA_PAM_USER", "").strip():
        logger.error(
            "STARTUP REFUSED: AAA_PAM_USER unset — signing lane would refuse every "
            "request. Set AAA_PAM_USER + AAA_PAM_PASS, or start with AAA_SIGNING_ALLOW_UNCONFIGURED=1 "
            "to acknowledge a deliberately-dead lane."
        )
        sys.exit(78)   # EX_CONFIG — config error, not a crash
```

**Why `sys.exit` and not a warning:** the lane is *already* refusing every request (401/503).
A process that is up-but-incapable, reporting `{"status":"ok"}`, is the T20 blind spot. Exiting
loudly converts a silent capability gap into a visible deployment failure.

**Escape hatch:** `AAA_SIGNING_ALLOW_UNCONFIGURED=1` lets a lane be deliberately started dead
(e.g. during migration) without disabling the guard globally.

### Health surface (pairs with T20)

```python
    "sovereign_presence_guard": "CONFIGURED" if os.environ.get("AAA_PAM_USER","").strip() else "UNCONFIGURED",
    "pam_module_available": <bool>,
```
So `/health` stops reporting `{"status":"ok"}` for a lane that cannot sign.

### Status
**NOT APPLIED — authored only.** File is under active edit by 333-AGI (`e66b2643f` is theirs);
writing it now would be the exact TOCTOU collision documented in ENTROPY-AUDIT-VERIFY.md.
Hand to the same seat, or apply after the lane settles. Cost: ~6 lines, no chain, no canon.

---

## Verification plan (per STAB §3 per-fix loop)

```
REPRODUCE  POST {canonical_json: "..."} with no challenge_id
           → BEFORE: returns a valid signature
           → AFTER : 400 challenge_id required
           → BEFORE: unset AAA_PAM_USER, valid challenge → signs
           → AFTER : 401 sovereign presence unproven

PREDICT    "after fix, unverified signing returns 400 and unproven-presence returns 401"

TEST       unit: mock env absent ⇒ assert 401; mock no challenge_id ⇒ assert 400
           both must FAIL before the patch and PASS after

DEPLOY     restart aaa-signing.service; confirm unit active + key_loaded=true

RE-PROBE   repeat both BEFORE probes; expect 400/401

REGRESSION oracle-verify /approve flow end-to-end with a real challenge

SCORE      TRUE / FALSE / PARTIAL per prediction
```

**Blocking dependency:** the oracle/approve flow must be tested *with credentials configured*,
or the fix will look like an outage. Sequence: configure credential → apply patch → test.

---

## Acceptance
```
unverified signing           → 400
unproven sovereign presence  → 401
valid challenge + credential → signature issued
service health               → {"status":"ok","key_loaded":true}
```

## Files touched
- `/root/AAA/auth/signing_server.py` (only)

## Rollback
Single file; `git checkout` restores. No state mutation, no chain touch.

---
**NOT APPLIED. Awaiting F13 verdict on the Option A / Option B trade.**
