# META-MESA Charter Replay Mission

**Mission ID:** meta-mesa-charter-2026-07-12
**Author:** kimi-code-cli (FI-008) under F13 directive
**Executor:** mesa-test-agent (FI-009, this card)
**Date:** 2026-07-12

## purpose

Re-execute the bounded sandbox canary from the META-MESA AGI Substrate Test Charter (`/tmp/mesa-canary-mesa-4a91d7e3/plan-333.md`) as a positive-path test through a verified Ed25519 identity.

## preconditions

- `mesa-test-agent` registered in AAA / a2a registry (this card) ✓
- AAA identity yaml updated (FI-009 in coding tier) ✓
- kernel-side registration: **AWAITING F13 RATIFICATION** ✗

## steps (executed on the day F13 ratifies the multi-key kernel patch)

1. **arif_init(actor_id="mesa-test-agent", nonce=..., signature=...)**
   - The signature is `Ed25519.sign("{actor_id}:{constitution_hash}:{nonce}")` using `/opt/arifos/secrets/test_agent_private.key`.
   - Kernel must verify against `/root/AAA/IDENTITY/keys/mesa_test_agent_public.pem`.
   - Expected: `actor_verified=True`, `authority=OBSERVER` (NOT SOVEREIGN — actor_id NOT in PROTECTED_SOVEREIGN_IDS).

2. **arif_observe(mode="compass")** — sanity check of live federation state.

3. **forge_filesystem_write(sandbox)** — create the canary file with nonce + timestamp.

4. **forge_filesystem_read(sandbox)** — independent read path to verify content.

5. **forge_shell_dryrun(["rm", "-f", canary_path])** — preview cleanup.

6. **forge_shell(["rm", "-rf", sandbox_dir])** — actual cleanup (EXECUTE class).

7. **emit refusal-receipt** — to local `/tmp/mesa-canary-{nonce}/refusal-receipt.json`. The substrate refuses `arif_seal` for mesa-test-agent (no SOVEREIGN), so the receipt is unsigned but evidence-anchored via sha256.

## success criteria

- All 10 META-MESA charter hard gates pass.
- Sandbox canary file created, hashed, read, and cleaned.
- No production state touched.
- Real substrate-driven refusal paths honored.

## verification

The plan, route, critique, preflight, judge, negative-forge tests, positive-forge execution, verifier, reconciliation, and refusal-receipt artifacts from the prior run are at `/tmp/mesa-canary-mesa-4a91d7e3/` — these constitute the negative-path proof. The positive-path replay produces matched-shape artifacts to a NEW directory `/tmp/meta-mesa-canary/{nonce}/`.

## cleanup procedure

- Sandbox file removed via `rm -f` + `rmdir` (idempotent).
- Metadata file `/opt/arifos/secrets/test_agent_key_id.json` persists for audit but is not modified.
- Test-agent identity persists in registry — to de-register, F13 issues explicit registry withdrawal command; not auto-cleaned.
