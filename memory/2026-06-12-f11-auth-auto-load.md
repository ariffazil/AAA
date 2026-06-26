# F11 AUTH Auto-Load + Seal Attempt — 2026-06-12

**Status:** Problem 2 (auto-load) SHIPPED. Problem 1 (seal aab4daa6) BLOCKED on kernel.

## Sovereign directive

Arif (#31464, 18:44 UTC): "Found the key. It's on the machine, not in your head.
The agents were asking wrong. Let me fix both problems now — seal the commit AND
make sure no agent ever asks you again."

F13-waived by sovereign directive.

## What I shipped (auto-load)

Canonical sovereign key: `/root/compose/sekrits/arifos_sovereign.key` (PEM, 119B,
generated 2026-06-11 04:11 UTC, public key matches `/root/compose/sekrits/arifos_sovereign.pub`,
F0_FIQH 888 seal verified against this keypair).

Created:
- `/root/.arifos/sovereign.key` → canonical priv (symlink, mode preserved)
- `/root/.arifos/sovereign.pub` → canonical pub
- `/root/.arifos/rootkey` → `/root/compose/sekrits/arif_rootkey` (HMAC fallback)
- `/root/.arifos/sovereign_sign.py` (from Hermes skill, mode 700) — signs Ed25519
- `/root/.arifos/sovereign_self_test.sh` (mode 700) — keypair consistency check, **PASS**
- `/root/.arifos/sovereign_session_init.py` (mode 700) — one-shot sign+bind helper
- `/root/.arifos/auto_load_receipt.json` — full audit trail
- `/opt/arifos/app/identity.toml` ← `[sovereign_key]` section added (auto_load=true,
  f13_status=RATIFIED, sovereign=Muhammad Arif bin Fazil)

## What got blocked (seal)

Commit `aab4daa6` in `/root/AAA`: "feat(registry): map Anthropic Fable 5 / Mythos 5
/ Opus 4.8 soul/shadow stack" (by AGI OPENCLAW, 18:17:30 UTC, 33min before sovereign
directive). 4 files, +673/-9 lines.

Ed25519 sig generated correctly:
- actor_id=ariffazil, constitution_hash=sha256:8bea28833523c652
- nonce=f6dbe797484d43d0622960d22c80d6b9
- sig=icRImluuugPaHGePn273FYHo2CvqyaY41OLhmZiXh/FYT9bYvzCr+n3l35IJ8s79FRSjmHbjKJJdGRSf24cQDg==

But `arif_session_init` tools/call to live kernel (PID 1052898) at :8088 hangs/times
out. Kernel is in a stuck state: 21.4% CPU, 1.9G RSS, /health 5s timeout, no journal
entries for 30s. Likely a deadlock from the earlier F8 SCHEMA GATE noise burst
(hundreds of forge_plan/dry_run/query unknown-tool calls hammering the kernel).

## Decision (pending sovereign F13)

- 🅐 `systemctl restart arifos` then retry seal — RECOMMENDED
- 🅑 Wait for self-recovery
- 🅒 Escalate to APEX Phase 3

I did NOT auto-restart. F13 territory.

## Lessons / carry-forward

1. **Kernel was hammered with F8 noise from OpenClaw connectors trying to call
   non-existent arifOS native tools (`forge_plan`, `forge_dry_run`, `forge_query`)**.
   arifOS native tool set is 13 arif_* tools; the OpenClaw arifos__arif_forge_*
   connectors don't translate cleanly. Bug in connector routing, not arifOS.

2. **ARIF_ROOTKEY is NOT in the live arifOS service's env** (only in
   /root/compose/sekrits/arif_rootkey file, not exported). HMAC path
   (verify_hmac_signature) will fail with "hmac_rootkey_not_configured". Ed25519
   path is the only working F11 route for now.

3. **The /root/.ssh/operator_did_ed25519 keypair MISMATCH** (private key May 22,
   .pub file Jun 11, public keys are different) is a SEPARATE concern, NOT
   blocking the F11 work because the canonical F11 key is at /root/compose/sekrits/,
   not /root/.ssh/. Flagged to sovereign for separate triage.

4. **Hermes's hermes-a2a.py still references /root/.ssh/id_ed25519** (the regular
   SSH key, not the sovereign DID). This is why Hermes has been asking Arif for
   the signature. Needs separate update from Hermes (their framework, not mine
   to touch without their review).

5. **sovereign_sign.py self-test PASS** — the canonical key at
   /root/compose/sekrits/arifos_sovereign.key loads correctly via the PEM path
   (not the malformed-DER fallback), pub derived from priv matches on-disk .pub.
   My earlier "pub mismatch" was from a faulty seed-extract at offset [7:39]
   which only applies to the malformed-DER shape. The file is actually standard
   PKCS8 PEM, and the script handles it via Case 1.

## Receipts

- `/root/.arifos/auto_load_receipt.json` — auto-load audit
- `/root/.arifos/sovereign_session_init.py` — can be re-run after restart
- Keypair: `/root/compose/sekrits/arifos_sovereign.{key,pub}` (untouched)
