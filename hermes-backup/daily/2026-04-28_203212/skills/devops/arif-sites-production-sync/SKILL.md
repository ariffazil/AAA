---
name: arif-sites-production-sync
description: Sync /999 credential artifacts from arif-sites source repo to live Nginx production web root — includes key consistency checks and manual deploy steps.
tags: [arif-sites, Nginx, production-deploy, /999, DID, Ed25519]
last_updated: 2026-04-27
---

# arif-sites Production Sync — /999 Credential Artifacts

## Context

The arifOS identity/verification surface lives at `https://arif-fazil.com/999/` (the "Verification Room"). Source code lives in `/root/sites/arif/` (GitHub: `ariffazil/arif-sites`), but production is served from a SEPARATE web root via Nginx — NOT via git push or Caddy.

## Key Discovery (2026-04-27)

**Production `did.json` key can differ from source repo `did.json` key.**

The production `/var/www/arif-fazil.com/.well-known/did.json` was independently updated and contained a DIFFERENT Ed25519 Multikey (`z6MkuQTtujH...`) than the source repo's version (`z6MkkWQz...`).

If you generate `.sig` files using a key from the source repo but the production `did.json` has a different key, verification will FAIL in production even though it works locally.

**Rule: Always read production files before making artifacts.**

## Production Stack

- **Web server:** Caddy (Docker container `caddy`)
- **Caddyfile:** `/root/compose/Caddyfile`
- **Web root:** `/var/www/html/arif/` (served at `https://arif-fazil.com/`)
- **Source repo:** `/root/sites/` (git remote: `github.com/ariffazil/arif-sites`)
- **Branches:** `site-autoresearch/apr26` is the working branch — commit here, push when verified

## Canonical Deploy Pattern

External agent deploy scripts often use wrong paths (e.g. `/mnt/agents/output/`,
`/root/sites/arif/` as root, or Nginx paths). **Always verify against git staging first.**

### Step 0 — Find the real files
```bash
# External agents stage work in /root/sites/ git repo
cd /root/sites && git status -s   # Shows all modified/new/untracked files
ls /root/sites/arif/              # Human surface source files
ls /root/sites/apex/              # Apex surface source files
```

### Step 1 — Copy to Caddy web root
```bash
# Human surface (arif-fazil.com)
cp /root/sites/arif/<file> /var/www/html/arif/
cp -r /root/sites/arif/888 /var/www/html/arif/
cp -r /root/sites/arif/history /var/www/html/arif/
cp -r /root/sites/arif/weight /var/www/html/arif/

# Apex surface (apex.arif-fazil.com)
cp /root/sites/apex/<file> /var/www/html/apex/

# Verify served correctly
curl -s -o /dev/null -w "%{http_code}" https://arif-fazil.com/<path>
```

### Step 2 — Reload Caddy (NOT Nginx)
```bash
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```
No `nginx reload` — Caddy handles everything.

### Step 3 — Commit to git
```bash
cd /root/sites
git add arif/888 arif/history arif/weight ...
git commit -m "feat(surface): <description>"
git push origin site-autoresearch/apr26
```

## DID/Keys Consistency Check

Before deploying, verify the key in `did.json` matches `keys.json`:

```python
import json

did_key = json.load(open('/path/to/.well-known/did.json'))['verificationMethod'][0]['publicKeyMultibase']
keys_key = json.load(open('/path/to/999/keys.json'))['keys'][0]['public_key']

assert did_key == keys_key, f"DID key ({did_key}) != keys.json ({keys_key}) — signatures will fail!"
print("Consistent ✅")
```

## Key Files Location

| File | Source | Production | Permissions |
|------|--------|------------|-------------|
| `did.json` | `/root/sites/arif/.well-known/` | `/var/www/arif-fazil.com/.well-known/` | 755 |
| `keys.json` | `/root/sites/arif/999/` | `/var/www/arif-fazil.com/999/` | 644 |
| `*.sig` files | `/root/sites/arif/999/` | `/var/www/arif-fazil.com/999/` | 644 |
| `verify.sh` | `/root/sites/arif/999/` | `/var/www/arif-fazil.com/999/` | 755 |
| `index.html` | `/root/sites/arif/999/` | `/var/www/arif-fazil.com/999/` | 644 |
| Private key | `/root/arifOS/secrets/did_ed25519_private.key` | N/A — never public | 600 |

## /999 Trust Ladder

Current state:
- L0 ✅ Published (file exists)
- L1 ✅ Structured (valid JSON)
- L2 ✅ Signed (Ed25519 .sig files, key consistent)
- L3 ⚠️ Anchored (GitHub commit verified but no timestamp authority)
- L4 ⚠️ Attested (third-party issuer pending — PETRONAS/university/professional body)
- L5 ⚠️ Monitored (CI not active)

## Symptoms Fixed This Session

1. `keys.json` had `PLACEHOLDER` — replaced with real Ed25519 Multikey
2. No `.sig` files existed — generated 4 detached Ed25519 signatures
3. `did.json` key ≠ `keys.json` key — discovered via production read, fixed both
4. `/proof/geologist-credential.json` links broken — fixed to `/999/` paths
5. No trust ladder badge — added L0–L5 visual to page
6. No claim status table — added honest label table to page

## Known Limitation

The `.sig` files are self-signed (issuer = did:web:arif-fazil.com). To reach L4, a third-party issuer must sign the geoscientist credential. This requires Arif to initiate, not an agent.