---
name: arifos-a2a-hub-vault-connection
description: Diagnose and fix A2A Hub (port 3001) showing vault=DISCONNECTED. The A2A Hub proxy-vaults writes through vault999-writer (port 5001); if the writer is dead, the hub shows DISCONNECTED even when vault999 itself is healthy. Fix is to restart vault999-writer, not vault999.
category: devops
tags: [arifOS, vault999, a2a, federation, docker]
version: 1.0.0
trigger: "A2A Hub health shows vault=DISCONNECTED, or A2A task routing fails with vault write errors"
---

# arifos-a2a-hub-vault-connection

## Diagnostic Chain

Always probe in order — never assume the vault itself is down:

```bash
# Step 1: Check A2A Hub vault status
curl -s http://127.0.0.1:3001/health

# Step 2: Check vault999-writer (port 5001)
curl -s http://127.0.0.1:5001/health

# Step 3: Check vault999 itself (port 8100)
curl -s http://127.0.0.1:8100/health
```

## Expected States

| Component | Healthy | Dead |
|---|---|---|
| A2A Hub (3001) | `{"status":"healthy","vault":"CONNECTED"}` | `{"status":"healthy","vault":"DISCONNECTED"}` |
| vault999-writer (5001) | `{"status":"healthy","vault_seals_count":N}` | Exited (255) |
| vault999 (8100) | `{"status":"healthy","vault":"connected"}` | unresponsive |

## Root Cause Pattern

The A2A Hub (`aaa-a2a`) calls `vault.js` which POSTs to `vault999-writer` (port 5001). The writer then writes to `vault999` (port 8100).

```
A2A Hub (3001)
    └── vault999-writer (5001)  ← this dies, causing DISCONNECTED
         └── vault999 (8100)    ← this stays alive
```

`vault999-writer` has **no auto-restart policy** in compose. It exits silently with code 255 (often coincident with AAA container crashes).

## Fix

```bash
# Restart vault999-writer
docker compose -f /root/compose/docker-compose.yml up -d vault999-writer

# Verify
sleep 2 && curl -s http://127.0.0.1:5001/health
curl -s http://127.0.0.1:3001/health
```

Expected: `vault999-writer` returns `{"status":"healthy"}` and A2A Hub returns `{"vault":"CONNECTED"}`.

## Why NOT vault999

Do NOT restart vault999 when A2A Hub shows DISCONNECTED. vault999 is almost certainly fine. The writer is the broken link.

## Why Restarting A2A Hub Alone Does Not Fix It

Restarting the A2A Hub container does not fix the DISCONNECTED state because the vault connection is a runtime dependency on the writer service — not a configuration in the hub itself. The writer must be alive for the hub to report CONNECTED.

## Prevention

Consider adding `restart: unless-stopped` to `vault999-writer` in `/root/compose/docker-compose.yml` to prevent future silent deaths.
