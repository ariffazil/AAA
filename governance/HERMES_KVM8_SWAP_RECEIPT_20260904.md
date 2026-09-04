# HERMES KVM8 SWAP RECEIPT (after recovery) — 2026-09-04 (FI-003, F13)

## What landed (after recovery)

### Phase A (was correct in prior turn)
- bot_token_env = ASI_ARIFOS_BOT_TOKEN
- bot_username = @ASI_arifos_bot
- Allowlist expanded (Syed 1042200555 + WAWA + others all in)
- @ASI_arifos_bot polling verified via /getUpdates

### Phase B recovery (THIS turn)
- KVM4 hermes-asi-gateway.service: stopped, disabled, MASKED (FragmentPath=/dev/null via mask)
- KVM4 hermes gateway processes: killed (no residual)
- KVM8 hermes-asi-gateway.service: re-written (was deleted by mistake of `unmask` + pre-existing masked unit)
- KVM8 daemon: daemon-reload + enable + start
- Bot identity = @ASI_arifos_bot (token 8410138119)

## Operational state
- KVM8: hermes-asi-gateway.service ACTIVE (canonical)
- KVM4: hermes-asi-gateway.service masked (retired)
- Telegram @ASI_arifos_bot now polls from KVM8

## Reversibility
- Snapshot: /root/.hermes-zen-backups/kvm8-swap-pre-20260904/kvm8-state.tar.gz
- Config backup: /usr/local/lib/hermes-agent/profiles/aaa-hermes/config.yaml.bak-pre-asibot-*

## Outstanding
- Wait 30s, then test real DM end-to-end (Syed → bot → reply)
- Persona routing (lane_switch_syed.py / SOUL-syed-dm.md) needs verification post-restart

Log: /tmp/kvm8-swap-recovery-20260904-125615.log
