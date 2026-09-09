# Federation Service Name Audit SOT — 2026-09-10

**Source of truth for systemd service names used by federation audits.**
**Updated:** 2026-09-10 by 333-AGI (SEAL-1a811cc14a3f4cba) — corrected after F13 audit drift finding.

## Canonical name mapping

| Old name (audit drift) | Canonical name (live) | Service function |
|---|---|---|
| `hermes-gateway.service` | `hermes-asi-gateway.service` | Hermes Telegram gateway (KVM8 LIVE) |
| `arifos-kernel.service` | `arifos.service` | arifOS Agent kernel |
| `frame-observer.service` | `frame-organ.service` | FRAME independent observer |
| `arifflow-daemon.service` | `arifflow.service` | Federation metabolism plane |

## Why the drift happened

Per VAULT999 entries.jsonl scar (`SEAL-7777c28af00a44a8`, 2026-09-10 00:12):
- M7/PHASE-B consolidation (2026-09-04) renamed units to current canonical names
- Audit SOT documents still referenced legacy names from before consolidation
- Heritage `hermes-gateway.service` is explicitly masked → `/dev/null` (deliberate suppression)

## How future audits should probe

```bash
# Canonical probe
for svc in hermes-asi-gateway arifos frame-organ arifflow; do
  systemctl is-active $svc.service
done

# DO NOT use legacy names — they return "inactive" by design (hermes-gateway)
# even though the canonical gateway is live.
```

## Audit result (F13 zen audit, 2026-09-10)

| Service | State | Evidence |
|---|---|---|
| `hermes-asi-gateway.service` | active running | `journalctl -u hermes-asi-gateway`, PID 3167739, uptime 14h+ |
| `arifos.service` | active running | `curl :8088/health` → 13/13 floors |
| `frame-organ.service` | active running | `curl :18085/health` → all chambers active |
| `arifflow.service` | active running | `curl :7073/health` → FQ 0.83+ BALANCED |

## Constitutional note

F1 AMANAH: heritage `hermes-gateway.service` mask is a deliberate scar (M7/PHASE-B).
F13 SOVEREIGN: dual-gateway prevention — see `entries.jsonl` scar at 2026-09-10 00:12.
F11 AUDIT: this document is the canonical reference. Update only via sovereign ratification.

DITEMPA BUKAN DIBERI ⚒️
