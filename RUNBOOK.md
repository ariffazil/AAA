# 📋 RUNBOOK — AAA Operations

> **SOT:** 2026-07-20

## Quick Health
```bash
curl -s http://localhost:3001/health | python3 -m json.tool
```

## Restart
```bash
sudo systemctl restart aaa-a2a
```

## Logs
```bash
journalctl -u aaa-a2a --since "5 min ago" --no-pager
```

## Deploy
```bash
cd /root/AAA
# Build + test, then:
sudo systemctl restart aaa-a2a
curl -s http://localhost:3001/health
```

## Escalation
F13 SOVEREIGN: Muhammad Arif bin Fazil — 888_HOLD for irreversible actions.

