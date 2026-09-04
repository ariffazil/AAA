# HERMES DAEMON MIGRATION PLAN — KVM4 → KVM8 (F13 HOLD)

> **Status**: STAGED for F13 ack. This plan was drafted 2026-09-04 after
> consolidation phase. **NOT executed** — waiting for sovereign directive.

## The move

Currently:
- KVM4 `hermes-asi-gateway.service` = ACTIVE (pid 670517)
- KVM8 `hermes-asi-gateway.service` = MASKED (deliberate — was to avoid dual gateway)

Goal: KVM8 = active gateway, KVM4 = thin client only.

## Risks

1. **Telegram bot downtime**: ~30-60 sec during swap
2. **Dual-polling conflict if both run simultaneously**: bot would reply twice
3. **State.db migration**: KVM4 gateway state may have session continuity value
4. **LiteLLM model path**: gateway uses `http://100.64.0.5:4000/v1` (KVM4 litellm) — this works FROM KVM4 (loopback) but needs to work TO KVM4 (cross-machine) when called FROM KVM8

## Migration steps (when F13 says "go")

### Pre-flight
1. Verify KVM8 `hermes-asi-gateway.service` unit file exists (`/root/.config/systemd/user/` or system)
2. Read ExecStart — confirm binary path (`/usr/local/bin/hermes`) is identical on KVM8
3. Read current KVM8 state.db size (`/root/.hermes/state.db`) — gateway will read this
4. Probe KVM8→KVM4 litellm `:4000/v1` directly (curl with api key) — must work

### State handover (no downtime yet)
5. Stop KVM4 daemon: `ssh kvm4 'systemctl --user stop hermes-asi-gateway'`
6. **GET**: pull any in-flight requests to completion (5 sec wait)
7. KVM4 is now OFFLINE for Telegram

### Bring up KVM8 daemon
8. Unmask: `systemctl --user unmask hermes-asi-gateway`
9. Edit KVM8 unit if model path needs adjustment (probably not — config already points to KVM4 litellm)
10. Enable + start: `systemctl --user enable --now hermes-asi-gateway`

### Verify
11. Curl KVM8 `/health/liveliness` (or appropriate endpoint) = healthy
12. Send test message to Telegram bot (Arif sends one message)
13. Confirm response from KVM8 daemon
14. Check openclaw-2026-09-04.log for errors

### Rollback plan
15. If fail at any step: `ssh kvm4 'systemctl --user start hermes-asi-gateway'` (restore from snapshot)

## Reversibility

- Full KVM8 snapshot: `/root/.hermes-zen-backups/consolidate-pre-<TS>/kvm8-root-hermes.tar.gz`
- Full KVM4 snapshot: `/root/.hermes-zen-backups/kvm4-pre-consolidate-<TS>.tar.gz`
- Both have SHA256 in consolidation receipt

## Why HOLD, not auto-execute

F13 doctrine: T3 irreversible gates need sovereign ack. Daemon swap = brief Telegram outage + could conflict with shell polling. Even with reversibility, the SWAP itself is F13. Other phases (file distillation) are reversible and T1.
