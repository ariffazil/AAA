---
name: hermes-session-hygiene
version: 1.0.0
risk_tier: low
description: Secure Hermes session dumps; quick leak triage.
owner: Hermes Ops
autonomy_tier: T1
floor_scope: [F1, F2, F4, F11, F12]
---
# Hermes Session Hygiene

Class-level playbook to keep Hermes session/request dumps safe and to triage potential API-key exposure without drama.

## When to use
- After changing providers/routers that may emit `Authorization` headers into dumps
- After migrations that recreated the profile directory
- Whenever a user asks "did a key leak?" or "am I compromised?"

## Enforce permissions (idempotent)
- Sessions dir (and subdirs): chmod 700
- Files: chmod 600

```bash
SESS_DIR="/usr/local/lib/hermes-agent/profiles/aaa-hermes/sessions"
# Tighten directory+subdirs
chmod 700 "$SESS_DIR" && find "$SESS_DIR" -type d -exec chmod 700 {} +
# Tighten files
find "$SESS_DIR" -type f -exec chmod 600 {} +
# Verify
find "$SESS_DIR" -maxdepth 1 -type f -printf "%m %p\n" | head
```

## Scan for token-bearing headers (redacted)
```bash
SESS_DIR="/usr/local/lib/hermes-agent/profiles/aaa-hermes/sessions"
grep -RInE 'Authorization:|Bearer ' "$SESS_DIR" \
 | sed -E 's/(Authorization: Bearer) .+/\1 <redacted>/' \
 | head -n 40
```
Notes:
- Do not print raw tokens. Always redact.
- Mixed 644/600 modes on older dumps are not a leak on a single-tenant root host, but standardize to 600 to prevent regressions.

## Quick compromise triage (10-minute pass)
- Secrets file perms: `namei -mo /root/.secrets/kunci-mas.env && stat -c '%a %n' /root/.secrets/kunci-mas.env` → expect 600
- Outbound sockets (unexpected peers?): `ss -tnp state established | head -n 50`
- Cron sweep (unexpected jobs?): `crontab -l; ls /etc/cron.*`
- Escalate only if you see:
  - unknown remote peers with steady send-queues
  - world-readable token-bearing drop-ins under `/etc/systemd/system/*.d/`

## Support files
- See `references/hermes-session-perms.md` for a fuller checklist (copyable commands)
- Use `scripts/fix_hermes_session_perms.sh` for a one-shot perms fix
