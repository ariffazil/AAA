# RUNBOOK.md — AAA (Control Plane)

> **Organ:** AAA | **Port:** 3001
> **Last Updated:** 2026-06-21
> **Components:** React 19 Cockpit + A2A gateway + 5-agent HEXAGON

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
npm run dev         # Vite dev server
```

## A2A Server
```bash
cd /root/AAA
node a2a-server/server.js           # Production (port 3001)
npm run a2a:dev                      # Dev (tsx watch)
npm run validate:aaa                 # Validate AAA contracts
```

## Deploy
```bash
cd /root/AAA
git pull
npm install && npm run build
systemctl restart aaa-a2a
curl -s http://127.0.0.1:3001/health | python3 -m json.tool
```

## Logs
```bash
journalctl -u aaa-a2a -n 50 --no-pager
journalctl -u aaa-a2a -f         # Follow live
```

## Common Failure Modes
| Symptom | Likely Cause | Fix |
|---------|-------------|------|
| Agent cards not loading | A2A server down | `systemctl restart aaa-a2a` |
| Cockpit blank | Build stale | `npm run build` |
| Federation display stale | Organ health probes failing | Check individual organ /health |
| Warga auth failures | Agent lease expired | Re-attest via arifOS kernel |

## What NOT to Do
- Do NOT issue constitutional verdicts (arifOS only)
- Do NOT execute irreversible actions unilaterally
- Do NOT bypass warga boundary — non-warga tools route through A-FORGE /execute
- Do NOT bind to 0.0.0.0
