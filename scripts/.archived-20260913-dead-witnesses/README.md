# Retired dead witnesses — 2026-09-13 (kimi-code/FI-008)

## watchdog-heartbeat.sh
Retired because it could never succeed and was never scheduled:
- probes `http://127.0.0.1:18789/health` → **0 listeners** on that port (dead target)
- **0 crontab references**, no systemd timer → never ran
- its json check expects `{"ok": true}` while the canonical surface returns `{"overall_ok": true}`

Replaced by the canonical witness surface: **hermes-health.service** → `127.0.0.1:18791/health`.
Per F13 SEAL 2026-09-13: "repoint toward the canonical health surface, or retire.
Keeping dead witnesses increases entropy."
