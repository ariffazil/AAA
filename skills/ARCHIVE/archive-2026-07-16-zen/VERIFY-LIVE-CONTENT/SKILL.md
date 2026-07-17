---
name: verify-live-content
description: Archived live-content verification law retained for audit provenance. Do not use as the active deployment verifier; use the current runtime verification skill for HTTP body, content-type, handler, redirect, and region checks.
---

# VERIFY_LIVE_CONTENT_LAW — Experience, Not Artifact

> **DITEMPA BUKAN DIBERI** — Forged, not given.
> Born from: False SEAL incident 2026-07-15 (verified bundle SHA, not URL content)

## The Problem
Agent verified: ✅ SHA on disk, ✅ HTTP 200, ✅ 13 slugs in bundle.
Agent did NOT verify: ❌ Response body contains intended content, ❌ Correct handler served it.

**200 OK ≠ correct content. SHA matched ≠ artifact served.**

## The Law (v1.0 — 2026-07-15)

A deploy is **NOT SEAL** until ALL pass:

### 1. Bundle exists on disk (SHA match)
```bash
sha256sum /path/to/file
# Compare to expected
```

### 2. HTTP status is 200
```bash
curl -sk -o /dev/null -w "%{http_code}" $URL
# Must be 200
```

### 3. Response body contains expected marker
```bash
curl -sk $URL | grep -q "EXPECTED_MARKER"
# Marker = unique string ONLY present in intended content
# If marker absent → verdict is VOID, not SEAL
```

### 4. Content-Type matches expected type
```bash
curl -skI $URL | grep -i content-type
# HTML → text/html
# JSON → application/json
# MCP → application/json or text/event-stream
```

### 5. Handler verification (if Caddy)
```bash
# Add to Caddy handler: header X-Caddy-Handler wealth-narrative
curl -skI $URL | grep -i x-caddy-handler
# Must match intended handler name
```

### 6. Cross-plane redirect (if applicable)
```bash
curl -skI $WRONG_URL | grep -i location
# Must redirect to correct plane
# Verify redirect target, not just status code
```

## Receipt Format
Every deploy receipt MUST include:
```json
{
  "url": "https://...",
  "status": 200,
  "content_type": "text/html",
  "handler": "wealth-narrative",
  "body_marker": "data-canon-id=\"makcik-cerita-v1\"",
  "body_marker_found": true,
  "bundle_sha": "sha256:...",
  "verdict": "SEAL" | "VOID" | "PARTIAL"
}
```

**If `body_marker_found` is false → verdict is VOID.**

## Region Presence Test (for cockpit pages)
```bash
for region in header chart decision nav footer; do
  curl -sk $URL | grep -q "data-region=\"$region\"" || echo "❌ REGION $region MISSING"
done
```

## Root Doctrine
- `200 OK` proves the server responded. Not that user reached intended content.
- `SHA on disk` proves artifact exists. Not that artifact is served.
- **Verify the EXPERIENCE, not the ARTIFACT.**
