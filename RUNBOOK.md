# RUNBOOK.md — AAA (Control Plane)

> **Organ:** AAA | **Port:** 3001
> **Last Updated:** 2026-06-12

## Start / Stop
```bash
systemctl start aaa-a2a
systemctl stop aaa-a2a
systemctl restart aaa-a2a
systemctl status aaa-a2a
```

## Health Check
```bash
curl -s http://127.0.0.1:3001/health | python3 -m json.tool
```

## Build (Frontend)
```bash
cd /root/AAA
npm install
npm run build       # Vite → dist/
npm run lint        # ESLint
```

## A2A Server
```bash
cd /root/AAA
node a2a-server/server.js   # Production (port 3001)
npm run a2a:dev              # Dev (tsx watch)
```

## Logs
```bash
journalctl -u aaa-a2a -n 50 --no-pager
```

## Common Failure Modes
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Agent cards not loading | A2A server down | `systemctl restart aaa-a2a` |
| Cockpit blank | Build stale | `npm run build` |
| Federation display stale | Organ health probes failing | Check individual organ /health |

## What NOT to Do
- Do NOT issue constitutional verdicts (arifOS only)
- Do NOT execute irreversible actions
- Do NOT bind to 0.0.0.0
