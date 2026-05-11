---
name: arif-sites-production-sync
description: Sync arif-sites built artifacts to live VPS web root — includes rsync deploy pattern, GitHub Actions failure awareness, and /999 credential consistency checks.
tags: [arif-sites, Caddy, production-deploy, /999, DID, Ed25519, rsync]
last_updated: 2026-05-02
---

# arif-sites Production Sync — Live Deploy

**Updated: 2026-05-08** — Critical path corrections discovered.

## Context

The arifOS identity/verification surface lives at `https://arif-fazil.com/999/` (the "Verification Room"). Source code lives in `/root/arif-sites/` (GitHub: `ariffazil/arif-sites`).

**CRITICAL PATH DISCOVERY (2026-05-08): VPS has TWO different web roots serving different domains:**

| VPS Root | Served Domain | Cloudflare | Notes |
|----------|--------------|-----------|-------|
| `/var/www/arif-fazil.com/` | `arif-fazil.com` (main site, Next.js) | YES — proxied | Cache purge needed after updates |
| `/var/www/html/` | Subdomains: `aaa.`, `geox.`, `forge.`, `mcp.`, `wiki.`, `waw.`, `wealth.`, `apex.` | No — direct | Direct connect |

**Common mistake:** rsyncing to `/var/www/html/` and expecting it to appear on `arif-fazil.com` — it won't. File must go to `/var/www/arif-fazil.com/`.

## Key Paths

```
GitHub repo:      github.com/ariffazil/arif-sites
Source files:     /root/arif-sites/sites/arif-fazil.com/src/
Built output:     /root/arif-sites/sites/arif-fazil.com/dist/
LIVE site root:   /var/www/arif-fazil.com/    ← arif-fazil.com (main, Cloudflare)
Subdomain root:   /var/www/html/              ← *.arif-fazil.com subdomains
```

## Production Stack

- **arif-fazil.com:** Next.js static export → `/var/www/arif-fazil.com/` → Cloudflare CDN
- **Subdomains:** Static files → `/var/www/html/{subdomain}/` → direct VPS
- **GitHub Actions:** BROKEN since ~2026-04-14 (jobs die in 2 seconds pre-checkout)
- **Cloudflare:** CDN proxy for main domain only — NOT Pages, NOT auto-deploy

## Deploy Pattern for arif-fazil.com (main domain with Cloudflare)

### Step 1 — Build (if needed)
```bash
cd /root/arif-sites/sites/arif-fazil.com
npm ci
CI=false npm run build
```

### Step 2 — Sync to live site
```bash
# CRITICAL: destination is /var/www/arif-fazil.com/ NOT /var/www/html/
rsync -av /root/arif-sites/output/hat-yai-2026-trip.html root@72.62.71.199:/var/www/arif-fazil.com/
```

### Step 3 — Verify VPS file
```bash
ssh root@72.62.71.199 "ls -la /var/www/arif-fazil.com/hat-yai-2026-trip.html"
# Should show correct byte size
```

### Step 4 — PURGE CLOUDFLARE CACHE (mandatory)
Cloudflare will serve STALE cached content even after VPS file is updated. Without purge, `curl` from outside shows old content.

**Dashboard method (fastest):**
1. cloudflare.com → arif-fazil.com → Caching → Configuration
2. Click "Purge Everything"

**API method:**
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/purge_cache" \
  -H "Authorization: Bearer ${CF_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://arif-fazil.com/hat-yai-2026-trip.html"]}'
```

### Step 5 — Verify live (after purge)
```bash
curl -s "https://arif-fazil.com/hat-yai-2026-trip.html" | wc -c
# Should match VPS file size exactly
# If it doesn't match → Cloudflare still serving cached version
```

## Deploy Pattern for Subdomains (aaa., geox., etc.)

```bash
rsync -av /root/arif-sites/output/some-file.html root@72.62.71.199:/var/www/html/
# No Cloudflare purge needed — direct VPS, no CDN
curl -s "https://aaa.arif-fazil.com/some-file.html"  # works immediately
```

## Diagnosing Stale Content Through Cloudflare

**Symptom:** VPS file updated but `curl https://arif-fazil.com/file.html` returns wrong/old content.

**Diagnosis steps:**
```bash
# 1. Check VPS file size
ssh root@72.62.71.199 "ls -la /var/www/arif-fazil.com/file.html"

# 2. Check what curl returns
curl -s "https://arif-fazil.com/file.html" | wc -c

# 3. If sizes differ — Cloudflare cache, not VPS issue
#    VPS: 26519 bytes | curl: 3441 bytes → CF serving index.html cached response
```

**Why it happens:** Cloudflare sees `.html` extension and caches it aggressively. Even `rsync` overwrite doesn't invalidate CF cache.

## Cloudflare Cache Purge Notes

- Purge by specific URL is faster than "Purge Everything"
- Cache rules can be set to cache `.html` for only 1 hour
- After purge, verify with `curl` showing correct byte count
- `curl -sI https://arif-fazil.com/file.html` shows CF status (HIT/MISS/ERROR)

## DID/Keys Consistency Check

Before deploying /999 artifacts, verify the key in `did.json` matches `keys.json`:

```python
import json
did_key = json.load(open('/path/to/.well-known/did.json'))['verificationMethod'][0]['publicKeyMultibase']
keys_key = json.load(open('/path/to/999/keys.json'))['keys'][0]['public_key']
assert did_key == keys_key, f"DID key mismatch!"
print("Consistent ✅")
```

## Key Files Location (corrected 2026-05-08)

| File | Built Source | Production Live | Notes |
|------|-------------|----------------|-------|
| `did.json` | `dist/.well-known/` | `/var/www/arif-fazil.com/.well-known/` | Main domain, CF cached |
| `keys.json` | `dist/999/` | `/var/www/arif-fazil.com/999/` | Main domain, CF cached |
| `*.sig` files | `dist/999/` | `/var/www/arif-fazil.com/999/` | Main domain, CF cached |
| Static HTML files | `/root/arif-sites/output/` | `/var/www/arif-fazil.com/` | Main domain, CF cached |
| Subdomain files | `/root/arif-sites/output/` | `/var/www/html/{subdomain}/` | Direct, no CF |
| Private key | `/root/arifOS/secrets/` | N/A — never public | 600 permissions |

## /999 Trust Ladder

- L0 ✅ Published (file exists)
- L1 ✅ Structured (valid JSON)
- L2 ✅ Signed (Ed25519 .sig files, key consistent)
- L3 ⚠️ Anchored (GitHub commit verified but no timestamp authority)
- L4 ⚠️ Attested (third-party issuer pending — PETRONAS/university/professional body)
- L5 ⚠️ Monitored (CI not active)

## Symptoms Fixed This Session (2026-05-08)

1. **Cloudflare stale content** — artifact written to VPS `/var/www/arif-fazil.com/` but CF served old cached version. Fixed by purging CF cache. Always check file size vs curl size.
2. **Wrong rsync destination** — `/var/www/html/` serves subdomains only. Main domain files must go to `/var/www/arif-fazil.com/`.
3. **Next.js vs static split** — `arif-fazil.com` is a Next.js app (source in `sites/arif-fazil.com/src/`), not pure static. Static HTML artifacts go in the same root directory alongside the Next.js build.

## Known Limitation

The `.sig` files are self-signed (issuer = did:web:arif-fazil.com). To reach L4, a third-party issuer must sign the geoscientist credential. Requires Arif to initiate.

## Key Paths

```
GitHub repo:      github.com/ariffazil/arif-sites
Source files:     /root/arif-sites/sites/arif-fazil.com/src/
Built output:     /root/arif-sites/sites/arif-fazil.com/dist/
LIVE site root:  /var/www/html/arif/dist/          ← Caddy serves this
```

**Important:** The `dist/` subdirectory is the BUILT static output. Caddy serves `/var/www/html/arif/dist/` as `https://arif-fazil.com/`.

## Production Stack

- **Web server:** Caddy (Docker container)
- **Caddyfile:** `/root/compose/Caddyfile` or `/root/arifOS/Caddyfile`
- **Web root:** `/var/www/html/arif/dist/`
- **Cloudflare:** CDN proxy only — NOT Pages, NOT auto-deploy
- **GitHub Actions:** BROKEN since ~2026-04-14 (jobs die in 2 seconds pre-checkout)

## Deploy Pattern (rsync — the working method)

Since GitHub Actions auto-deploy is broken, use rsync directly:

### Step 1 — Build
```bash
cd /root/arif-sites/sites/arif-fazil.com
npm ci
CI=false npm run build
```

### Step 2 — Sync to live site
```bash
rsync -av --delete /root/arif-sites/sites/arif-fazil.com/dist/ /var/www/html/arif/dist/
```

### Step 3 — Verify
```bash
curl -sI https://arif-fazil.com | grep last-modified
# Should show today's timestamp (e.g. Sat, 02 May 2026 06:54:47 GMT)
```

## Key Discovery (2026-05-02)

**GitHub Actions "Build — Trinity Sites" has been failing for ~3 weeks.**
- Jobs complete in exactly 2 seconds
- Failure is pre-checkout (permissions/config issue, not build)
- All 3 sites (ARIF, ARIFOS, AAA) failed
- The workflow has a broken matrix entry for `sites/arifos.arif-fazil.com/` which no longer exists

**Fix:** Removed the broken Ring 2 ARIFOS job from `.github/workflows/deploy.yml`. But jobs still fail (2 seconds) — root cause unknown.

**Cloudflare Pages:** `ariffazil.pages.dev` has never resolved. CF Pages is NOT the serving layer. Do NOT rely on it for auto-deploy.

## DID/Keys Consistency Check

Before deploying /999 artifacts, verify the key in `did.json` matches `keys.json`:

```python
import json

did_key = json.load(open('/path/to/.well-known/did.json'))['verificationMethod'][0]['publicKeyMultibase']
keys_key = json.load(open('/path/to/999/keys.json'))['keys'][0]['public_key']

assert did_key == keys_key, f"DID key ({did_key}) != keys.json ({keys_key}) — signatures will fail!"
print("Consistent ✅")
```

## Key Files Location

| File | Built Source | Production Live |
|------|-------------|----------------|
| `did.json` | `/root/arif-sites/sites/arif-fazil.com/dist/.well-known/` | `/var/www/html/arif/dist/.well-known/` |
| `keys.json` | `/root/arif-sites/sites/arif-fazil.com/dist/999/` | `/var/www/html/arif/dist/999/` |
| `*.sig` files | `/root/arif-sites/sites/arif-fazil.com/dist/999/` | `/var/www/html/arif/dist/999/` |
| `index.html` | `/root/arif-sites/sites/arif-fazil.com/dist/` | `/var/www/html/arif/dist/` |
| Private key | `/root/arifOS/secrets/did_ed25519_private.key` | N/A — never public |

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