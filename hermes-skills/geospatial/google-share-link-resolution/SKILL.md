---
name: google-share-link-resolution
description: "Workaround when user shares a Google Share link (share.google.com/...) and vision_analyze fails with 'Only real image files supported'. Ask user to open link in browser and provide place name, Place ID (ChIJ...), or coordinates from the URL."
category: geospatial
tags: [google-maps, share-links, vision_analyze, workaround]
version: 2026.05.08
seal: 999
---

# Google Share Link Resolution Workaround

## Problem
User shares a `share.google.com/...` link. `vision_analyze` rejects it with:
```
Error: Only real image files are supported for vision analysis
```

`vision_analyze` only handles local/remote image files (.jpg, .png, .webp), NOT:
- Google Share links (`share.google.com/...`)
- Google Maps URLs (`maps.google.com/...`, `goo.gl/...`)
- Shortened or redirect URLs

**Server-side limitations discovered (2026-05-09):**
- `curl share.google.com/...` → returns redirect to `www.google.com/share.google?q=...` then JS-heavy page (no parseable HTML)
- Even if you extract the CDN image URL (`lh3.googleusercontent.com/places/...`) from the share link → **HTTP 400 Bad Request** when passed to `vision_analyze`
- Google Places CDN URLs are signed per-session and expire quickly
- **Conclusion: Google Share links cannot be resolved server-side at all. User must provide direct input.**

## Solution
Ask the user to provide ONE of:
1. **Place name** — I can query via Nominatim OSM or Google Places (if API key available)
2. **Place ID** — format `ChIJ...` — I can query `arif_spatial_place_details`
3. **Coordinates** — format `lat,lng` from the URL after `@` — I can use directly
4. **Screenshot** — user opens link in browser and sends image file

## Extraction from Google Maps URLs
When user pastes a Google Maps URL, look for:
- Place ID: `/place/.../` section or `place_id=ChIJ...`
- Coordinates: `@lat,lng,zoom` pattern in URL
- Place name: usually visible before `@`

## Example Workflow
```
User: [shares link]
Hermes: "I can't read Google Share links directly. 
Could you open it in your browser and give me either:
- The place name, OR
- The Place ID (ChIJ...), OR  
- The coordinates from the URL"
```

---

*DITEMPA BUKAN DIBERI — 999 SEAL*
