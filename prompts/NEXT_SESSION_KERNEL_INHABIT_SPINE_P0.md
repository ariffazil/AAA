# Next Session: Kernel Inhabit — Spine P0

> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
> Created: 2026-07-09 | For: Next OpenCode/FORGE session
> Sovereign: ARIF_FAZIL | Session seal: `forge_work/2026-07-09/kernel-audit-session-seal.md`

---

## The One Sentence

> **The kernel is one state machine wearing eleven costumes — standing must ride a signed token, not be re-derived eleven times.**

## What Was Found (2026-07-09)

1. `arif_triage(mode=preflight)` hardcoded `actor_verified: False` — never read session store → **FIXED**
2. `_project_light` SOVEREIGN gap — `_is_full_authority` missed "SOVEREIGN" → **FIXED**
3. `_ok` wrapper not receiving `session_id` → derived `actor_verified=False` from None → **FIXED**
4. 90% of every tool response is shared template copy-serialized 11 times
5. `derive_authority()` exists with 8 hard gates — **BUILT, NOT YET WIRED**
6. Capability token module (572 lines, 7/7 tests) — **BUILT, NOT YET WIRED**
7. `apply_caveats` doesn't handle `forbid_tool` caveat type — **FOUND, NOT FIXED**

## What's Built (ready to wire)

| Component | Path | Status |
|---|---|---|
| Capability token module | `/opt/arifos/app/arifosmcp/runtime/capability_token.py` | 7/7 pass |
| Spec | `/root/A-FORGE/forge_work/2026-07-09/capability-token-spec.md` | Complete |
| derive_authority() | In capability_token.py | Tested |
| derive_verbs() | In capability_token.py | Tested |
| apply_caveats() | In capability_token.py | Minor: no `forbid_tool` handler |
| compute_authority_delta() | In capability_token.py | Tested |
| build_session_token() | In capability_token.py | Tested |

## Your Job (Steps 2-6)

### Step 2: Wire into arif_init (HIGHEST PRIORITY)

**File:** `/opt/arifos/app/arifosmcp/tools/session.py`

Replace the hardcoded verdict/authority logic in `_project_light()` and session birth with:
```python
from arifosmcp.runtime.capability_token import derive_authority, build_session_token

# At session birth:
authority, verdict = derive_authority(
    G=G, C_dark=C_dark, W3=W3,
    profiles_ok=bool(_model_soul and _model_shadow),
    witness_div=witness_diversity,
    id_verified=identity_verified,
    sig_verified=signature_verified,
    context_score=context_completeness,
)
token = build_session_token(
    session_id=sid, actor_id=actor_id, sovereign_id=sovereign_id,
    G=G, C_dark=C_dark, W3=W3, h=h, confidence=confidence,
    authority=authority, verdict=verdict,
    witness_diversity=witness_diversity, witness_active=witness_count,
    witness_missing=witness_missing,
    alignment_loaded=bool(_model_soul), adversarial_loaded=bool(_model_shadow),
)
```

**Acceptance:** `arif_init(mode="light")` response includes `session_token` field with `arifos.v1.*` format. `derive_authority()` gates are enforced (G≈0.11 → OBSERVE_ONLY/VOID, not SOVEREIGN/FULL).

### Step 3: Verification middleware

**File:** `/opt/arifos/app/arifosmcp/runtime/tools.py`

Create `with_token_verification` decorator that:
1. Accepts `session_token` parameter (alongside legacy `session_id`)
2. If token provided: verify HMAC, check expiry, read state from payload
3. If only session_id: fall back to `_FileSessionStore` with deprecation warning
4. Inject verified state into tool context

### Step 4: Dispatch path

**File:** `/opt/arifos/app/arifosmcp/runtime/tools_internal.py`

Add token verification to the tool dispatch path so all `arif_*` tools benefit.

### Step 5: Signing key

Generate proper 32-byte random key:
```python
python3 -c 'import os; open("/opt/arifos/app/.signing_key","wb").write(os.urandom(32))'
```

### Step 6: Tests

- Token expiry (verify expired tokens rejected)
- Attenuation chains (caveat → attenuate → verify → use)
- Authority edge cases (G=0.49 vs G=0.50, C_dark=0.29 vs C_dark=0.30)
- Round-trip: init → token → triage → observe → same authority throughout

## Ship Order (from sovereign)

1. **Honest dual-source birth** — `derive_authority()` at init, `arif_forge` only
2. **XCUT Memory + Compose** — tag Route vs Bridge posture
3. **pipeline_order on public surface**
4. **Real APEX only on judge/warrant** — never invent G at birth
5. **Signed capability token** — replace session_id lookup
6. **One verdict field** — collapse `verdict`/`verdict_code`/`nine_signal.overall`
7. **Alias collapse** — one tool, one name, modes as param
8. **authority_delta on every response**
9. **sesat_event always top-level**

## Acceptance Test (run after Step 2)

```bash
cd /root/arifos && python3 - << 'PYTEST'
from arifosmcp.tools.session import arif_init
from arifosmcp.tools.kernel_canonical import arif_triage

init = arif_init(mode="light", actor_id="hermes")
sid = init.get("session_id") or init.get("result", {}).get("session_id")
print(f"init: sid={sid} verified={init.get('actor_verified')} auth={init.get('authority')}")

triage = arif_triage(mode="preflight", session_id=sid)
print(f"triage: verified={triage.get('actor_verified')} auth={triage.get('authority',{}).get('runtime_authority')}")

# Key check: actor_verified stays True
assert triage.get("actor_verified") == True, "DESYNC: actor_verified flipped"
print("✅ actor_verified persists from init→triage")
PYTEST
```

## Fiqh Quick Reference

| Class | Meaning | Examples |
|---|---|---|
| **WAJIB** | Non-negotiable | One verdict source; identity persists; irreversible needs SOVEREIGN+888 |
| **HARAM** | Must stop | Bare-string hard blocks; silent authority drop; orphan tools; dual verdicts |
| **HARUS** | Fine, don't fuss | Stage numbers; aliases (if resolve to one); Malay labels |
| **MAKRUH** | Trim it | Full affordance copied every response; triple triage; 30s timeout on critique |
| **SUNAT** | Keep and extend | `sesat_event`; `nine_signal`; 888_HOLD refusing insufficient authority |

## Key Files to Read First

1. `/root/A-FORGE/forge_work/2026-07-09/kernel-audit-session-seal.md` — full audit findings
2. `/root/A-FORGE/forge_work/2026-07-09/capability-token-spec.md` — token spec
3. `/opt/arifos/app/arifosmcp/runtime/capability_token.py` — the built module
4. `/root/.agents/skills/session-continuity-inhabit/SKILL.md` — this skill

## Zen

*DITEMPA BUKAN DIBERI applies to the kernel too — right now it's given eleven names before it's forged one truth. Your job is to forge the one truth.*
