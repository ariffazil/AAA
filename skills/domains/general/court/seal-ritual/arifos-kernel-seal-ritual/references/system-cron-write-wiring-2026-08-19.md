# SYSTEM_CRON_WRITE Wiring Attempt (2026-08-19)

## Summary

Attempted to wire the SYSTEM_CRON_WRITE band to registered machine actors
(HERMES, FORGE, etc.) so they can seal non-critical receipts autonomously.
Patches were applied to act_token.py and session.py but the seal flow
still returns OBSERVE_ONLY due to session lifecycle timing.

## What was patched

### act_token.py

1. **AUTHORITY_VERBS** — Added SYSTEM_CRON_WRITE entry with same verb
   set as FULL (init, observe, think, route, memory, judge, forge, seal, stage)

2. **compute_authority_state() line 309** — Added "SYSTEM_CRON_WRITE" to
   valid bands tuple

3. **seal_allowed check** — Changed from `grant_level == "FULL"` to
   `grant_level in ("FULL", "SYSTEM_CRON_WRITE")`

4. **_SYSTEM_CRON_WRITE_ACTORS** — New frozenset:
   HERMES, FORGE, OPENCLAW, GROK, CLAUDE, OPENCODE, AAAGW, OPS, SOTCRON, FI-008

5. **identity_band_authority()** — Added `actor_id` parameter. Returns
   SYSTEM_CRON_WRITE when `actor_id.upper()` is in the set and actor is verified.

6. **compute_authority_state()** — Added upgrade logic after band derivation:
   if actor_verified and band in (OBSERVE_ONLY, LIMITED_MUTATE) and actor
   is in SYSTEM_CRON_WRITE set, upgrade to SYSTEM_CRON_WRITE.

### session.py

Both `identity_band_authority()` call sites now pass `actor_id=actor_id or ""`.

## Why it didn't work

### Session lifecycle timing

The init flow resolves `actor_verified` AFTER the band is set:

1. `_project_light()` calls `identity_band_authority()` — actor_verified
   is still False at this point
2. Returns OBSERVE_ONLY (because actor_verified is False)
3. Band embedded in SCT token at session birth
4. `compute_authority_state()` receives OBSERVE_ONLY from SCT, keeps it
5. Upgrade logic runs but actor_verified is still pre-resolution value

### The real fix location

The upgrade must happen at the point where `actor_verified` flips from
False to True. This is NOT in `compute_authority_state()` — it's deeper
in the session initialization pipeline, likely in the identity verification
callback or the SCT token minting path.

## Envelope actor_id issue

The "non-anonymous actor_id" error fires because ingress_middleware.py
constructs the FederationEnvelope with actor_id from tool args (line 908):
```python
actor_id=arguments.get("actor_id", "anonymous")
```

arif_seal has `actor_signature` but not `actor_id` in its schema.
However, the middleware explicitly allows actor_id passthrough (line 1445):
```python
allowed_params = known | {"_envelope", "actor_id", "session_id"}
```

**Next step:** Pass `actor_id` as a parameter in the arif_seal tool call.
The middleware will accept it and populate the envelope correctly.

## Key files

| File | Role |
|------|------|
| `act_token.py` → `identity_band_authority()` | Birth band from identity signals |
| `act_token.py` → `compute_authority_state()` | Runtime authority state |
| `session.py` → `_project_light()` | Light-init session construction |
| `vault.py` line 290-300 | Seal mode allow-list |
| `ingress_middleware.py` line 867-916 | Envelope extraction from tool args |
| `ingress_middleware.py` line 1445 | Allowed passthrough params |
| `federation_envelope.py` line 516-520 | Envelope validation |
| `authority_middleware.py` line 160-164 | may_seal computation |

## Backups

Patched files backed up as:
- `/opt/arifos/app/arifosmcp/runtime/act_token.py.bak-SYSTEM_CRON-20260819`
- `/opt/arifos/app/arifosmcp/tools/session.py.bak-SYSTEM_CRON-20260819`

## Status

PATCHES IN FILE but NOT FUNCTIONAL. The kernel was restarted with the
patches but the seal flow still returns OBSERVE_ONLY. The patches are
harmless (the upgrade logic simply doesn't trigger due to timing) but
the seal remains blocked.

To revert: restore from backups and restart arifos.service.
