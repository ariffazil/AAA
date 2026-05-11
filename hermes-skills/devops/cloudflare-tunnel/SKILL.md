---
name: cloudflare-tunnel
description: "Cloudflare Tunnel operations for arifOS — expose local services without opening firewall ports. Replaces direct exposure of Docker (*:2377), Dozzle (*:8888), and other debug ports."
triggers:
  - "cloudflare tunnel"
  - "cloudflared"
  - "expose local service"
  - "replace :2377"
  - "replace :8888"
  - "dozzle cloudflare"
category: devops
---

# cloudflare-tunnel — Zero-Port-Exposure Local Service Exposure

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given. Never expose raw ports to the internet.

## What This Solves

| Exposed Port | Risk | Cloudflare Tunnel Fix |
|---|---|---|
| `*:2377` (Docker swarm) | Full container takeover | Tunnel → `docker.sock` never exposed |
| `*:8888` (Dozzle) | Container logs + secrets | Tunnel → Dozzle dashboard, auth-gated |
| `*:8080` (arifOS MCP direct) | Unproxied API access | Tunnel → MCP via CF WAF |
| `*:3000` (debug endpoints) | Full internal access | Tunnel → with CF Access policy |

## Architecture

```
Internet → Cloudflare Edge → Tunnel → Local service
                         ↓
              No firewall ports open
              WAF + Zero Trust gates
```

## Setup

### 1. Install cloudflared
```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared
cloudflared --version
```

### 2. Authenticate
```bash
cloudflared tunnel login
# Opens browser for CF OAuth, saves cert to ~/.cloudflared/cert.pem
```

### 3. Create tunnel
```bash
cloudflared tunnel create arifos-fed
# Saves tunnel UUID to ~/.cloudflared/<tunnel-uuid>.json
```

### 4. Route DNS to tunnel
```bash
# Point a subdomain to the tunnel
cloudflared tunnel route dns arifos-fed dozzle.arif-fazil.com
cloudflared tunnel route dns arifos-fed mcp-internal.arif-fazil.com
```

## Common Configurations

### Dozzle (replace *:8888)
```yaml
# ~/.cloudflared/config.yml
tunnel: <tunnel-uuid>
credentials-file: /root/.cloudflared/<tunnel-uuid>.json

ingress:
  - hostname: dozzle.arif-fazil.com
    service: http://host.docker.internal:8888
  - hostname: mcp-internal.arif-fazil.com
    service: http://host.docker.internal:3000
  - service: http_status:404
```

### arifOS MCP internal surface
```yaml
ingress:
  - hostname: mcp-internal.arif-fazil.com
    service: http://host.docker.internal:8080
    originRequest:
      httpHostHeader: mcp.arif-fazil.com
  - service: http_status:404
```

### Docker daemon (REPLACE *:2377 — never expose directly)
```yaml
# ~/.cloudflared/docker-tunnel.yml
tunnel: docker-tunnel
credentials-file: /root/.cloudflared/docker-tunnel-uuid.json

ingress:
  - hostname: docker.arif-fazil.com
    service: unix:///var/run/docker.sock
    originRequest:
      connectTimeout: 30s
  - service: http_status:404
```

## Run Tunnel

### Option A — Systemd service (permanent)
```bash
cat > /etc/systemd/system/cloudflared-arifos.service << 'EOF'
[Unit]
Description=Cloudflare Tunnel for arifOS Federation
After=network.target

[Service]
ExecStart=/usr/local/bin/cloudflared tunnel run --config /root/.cloudflared/config.yml arifos-fed
Restart=always
RestartSec=5s
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl enable cloudflared-arifos
systemctl start cloudflared-arifos
systemctl status cloudflared-arifos
```

### Option B — Docker sidecar
```bash
docker run -d \
  --name cloudflared-tunnel \
  --restart unless-stopped \
  -v /root/.cloudflared:/etc/cloudflared \
  cloudflare/cloudflared:latest \
  tunnel run --config /etc/cloudflared/config.yml arifos-fed
```

## Verify Tunnel Health
```bash
# Check tunnel status
cloudflared tunnel list
cloudflared tunnel info arifos-fed

# Test from outside
curl -sI https://dozzle.arif-fazil.com | grep -E "^HTTP|^server:|^cf-"
```

## Security — Zero Trust Policies

Add CF Access policy so even if the tunnel URL leaks, it's useless without Auth:

### Via API
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/access/policies" \
  -H "Authorization: Bearer <CF_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "arifOS Internal Access",
    "domains": ["dozzle.arif-fazil.com", "mcp-internal.arif-fazil.com"],
    "include": [{"email": {"domain": "arif-fazil.com"}}],
    "require": [{"one_time_pin": true}],
    "action": "allow"
  }'
```

## Troubleshooting

### Tunnel shows "Connection refused" locally but works externally
```bash
# Test local service first
curl -s http://host.docker.internal:8888 | head -3

# Check tunnel logs
journalctl -u cloudflared-arifos -n 50 --no-pager
cloudflared tunnel run arifos-fed --loglevel debug
```

### DNS not propagating after route
```bash
# Force DNS update
cloudflared tunnel route dns -f arifos-fed dozzle.arif-fazil.com

# Verify DNS record
dig dozzle.arif-fazil.com CNAME
```

### 502 from tunnel
```bash
# Usually means local service is down
docker ps | grep dozzle
curl -s http://host.docker.internal:8888/health
```

## Quick Reference

```bash
# One-liner for new tunnel
cloudflared tunnel create NEW && cloudflared tunnel route dns NEW sub.domain.com

# Reload config without restarting tunnel
cloudflared tunnel update arifos-fed --config /root/.cloudflared/config.yml

# Access tunnel metrics
curl -s http://localhost:9100/metrics
```

## Constitutional Notes

- **F1 AMANAH**: Never expose `:2377` or `:8888` directly to the internet. Use tunnel.
- **F11 AUTH**: Pair every tunnel endpoint with a CF Access policy. No open tunnels.
- **F12 INJECTION**: Sanitize hostname inputs — CF API rejects invalid characters.

## Related Skills
- `cloudflare-agents` — CF token setup, account provisioning
- `diagnose-cloudflare-522` — when CF can't reach the tunnel origin
- `caddy-cloudflare-routing-debug` — routing debug when tunnel endpoint returns wrong content
