---
title: "SKILL: Caddy + Cloudflare"
type: skill
version: 1.0.0
category: infra
risk_band: MEDIUM
floors: []
evidence_required: true
sources: [/root/.opencode/skills/caddy-cloudflare/SKILL.md]
confidence: high
---

# SKILL: Caddy + Cloudflare

> **Source:** `/root/.opencode/skills/caddy-cloudflare/SKILL.md`
> **Agent:** OpenCode (Ω-FORGE)
> **Forged:** 2026-05-17

---

## Trigger Conditions

- Caddyfile editing, configuration
- Cloudflare DNS integration
- SSL/TLS certificate management
- Reverse proxy setup, domain routing
- ACME challenge, HTTPS automation
- Keywords: caddy, cloudflare, SSL, TLS, reverse-proxy, DNS, HTTPS

---

## Standard Reverse Proxy Template

```caddyfile
yourdomain.com {
    reverse_proxy localhost:8080 {
        health_uri /health
        health_interval 30s
    }
    tls {
        dns cloudflare {env.CF_API_TOKEN}
    }
    log {
        output file /var/log/caddy/access.log
    }
}
```

---

## Validation Sequence (Always in Order)

```bash
caddy validate --config /etc/caddy/Caddyfile
caddy fmt --overwrite /etc/caddy/Caddyfile
caddy reload --config /etc/caddy/Caddyfile
```

---

## Cloudflare Integration

| Setting | Value |
|---------|-------|
| Env var | `CF_API_TOKEN` with DNS:Edit permission |
| SSL Mode | Cloudflare SSL/TLS → "Full (Strict)" when Caddy manages cert |
| Orange-cloud ON | Traffic proxied through CF edge |
| Orange-cloud OFF | DNS only, Caddy handles everything |

---

## Troubleshooting Matrix

| Error | Cause | Fix |
|-------|-------|-----|
| 521 | Origin unreachable | Check caddy running, port open |
| 526 | SSL cert invalid | `caddy certificates`, check CF_API_TOKEN |
| ERR_TOO_MANY_REDIRECTS | SSL mismatch | Set CF SSL to "Full (Strict)" |
| ACME challenge fail | DNS propagation | Wait 60s, check `dig txt _acme-challenge.domain` |

---

## Certificate Inspection

```bash
caddy certificates
ls ~/.local/share/caddy/certificates/
journalctl -u caddy -f --since "10 min ago"
```

---

## FastMCP + Caddy Pattern

```caddyfile
mcp.yourdomain.com {
    reverse_proxy fastmcp:8000
    tls { dns cloudflare {env.CF_API_TOKEN} }
    header {
        Access-Control-Allow-Origin *
        Access-Control-Allow-Methods "GET, POST, OPTIONS"
    }
}
```

---

## Related Pages

- [[skill-fastmcp-deploy]] — FastMCP deployment
- [[skill-vps-audit]] — Caddy health checks
- [[skill-docker-security]] — port exposure
- [[SCHEMA.md]] — TREE777 governance schema

---

*DITEMPA BUKAN DIBERI — Caddy configured. Cloudflare connected.*
