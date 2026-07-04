---
title: "Scar — Route Hijacking & Dead Source Code in arifOS Sites"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: scar
status: canonical
tags: [route-hijacking, dead-code, caddy, react, spa, architecture, arif-fazil.com, forge]
confidence: high
domain: infra/agent-behavior
severity: high
actors: [kimi-agent, deployment-pipeline]
sources:
  - /root/arifOS/Caddyfile
  - /root/arif-sites/sites/arif-fazil.com/src/App.tsx
  - /root/arif-sites/sites/arif-fazil.com/public/000/index.html
  - /root/arif-sites/sites/arif-fazil.com/src/pages/Genesis.tsx
  - /root/arif-sites/sites/forge.arif-fazil.com/index.html
  - session-audit-2026-05-17
---

# Scar — Route Hijacking & Dead Source Code in arifOS Sites

## What Happened

Comprehensive site estate audit (2026-05-17) revealed that **multiple sites have source code that is never served**, and **React routes are hijacked by Caddy static handles**, creating a fractured architecture where the claimed design and the live design are completely different.

## Finding 1: `/000/` Route Hijacking (arif-fazil.com)

**Two different pages compete for `https://arif-fazil.com/000/`:**

| Layer | File | Last Modified | Content |
|-------|------|---------------|---------|
| React route | `src/pages/Genesis.tsx` | May 16 14:58 | Brutalist redesign — "Genesis Chamber" landing |
| Static HTML | `public/000/index.html` | May 10 17:13 | Standalone identity page with DID, genesis statement, Vault999 seals |
| Caddy winner | `@genesis` handle | — | Serves static HTML, React route is NEVER EXECUTED |

**Caddyfile:**
```caddy
@genesis path /000/*
handle @genesis {
    uri strip_prefix /000
    root * /var/www/html/arif/000
    try_files {path} /index.html
    file_server
}
```

**Result:** The React `<Genesis />` component is **dead code**. Users see the old static HTML page (May 10) instead of the redesigned React page (May 16). The "architectural unification & brutalist redesign complete" commit never actually affected `/000/` because Caddy bypasses React entirely.

**Even worse:** If the Caddy `@genesis` handle were removed, the default `try_files {path} /index.html` would STILL serve `dist/000/index.html` because Vite copies `public/000/` to `dist/000/`. The static file exists in two places and wins in both scenarios.

## Finding 2: Forge Source is Completely Dead

| Layer | State |
|-------|-------|
| Source | `sites/forge.arif-fazil.com/index.html` exists — static docs site (45KB HTML) |
| Caddy | `handle { respond "forge.arif-fazil.com — A-FORGE webhook gateway" }` |
| Live result | Source is **NEVER SERVED** — all non-webhook traffic gets a text response |

The forge static site was built and deployed at some point, but the Caddy default handle was changed to a `respond` directive, making the entire frontend dead code.

## Finding 3: AAA Frontend Source Mismatch

The skill table claims `aaa.arif-fazil.com` is a "React cockpit + A2A API". The source directory (`sites/aaa.arif-fazil.com/`) contains **no `package.json`, no `src/`, no build system** — only pre-built static bundles and Cloudflare Pages artifacts. The actual React source lives in the separate `/root/AAA/` repo. The two may be out of sync.

## Root Cause

**Three systemic failures:**

1. **Caddy handles added without checking React routes:** Whoever added `@genesis` and `@validation` to Caddy didn't check if the React app already claimed those paths. The Caddy handles were treated as "just static file serving" without considering they preempt SPA routing.

2. **Source code kept after Caddy behavior changed:** The forge `index.html` was left in the repo even after Caddy was reconfigured to respond with text. No one verified that the source was still being served.

3. **Build output treated as source:** The AAA frontend is pre-built bundles in `arif-sites/` while the actual source is in `AAA/`. This split creates ambiguity about which is canonical.

## TREE777 Lesson

**When a site claims to be a React SPA, every Caddy `handle` block is a potential route hijacker.**

Before adding ANY Caddy handle for a path:
1. Check the React `App.tsx` routes — does React already claim this path?
2. Check `public/` — does Vite copy a static file to this path?
3. Check `dist/` after build — does a static file exist that `try_files` would find?
4. If any of the above is true, the Caddy handle is hijacking, not helping.

**Rule — SPA Route Integrity Check:**
> For every Caddy `handle` or `rewrite` on a domain with a React app:
> - List all React `<Route path="...">` declarations
> - List all files in `public/` (Vite copies these to `dist/` verbatim)
> - Any overlap = ARCHITECTURAL CONFLICT

**Rule — Dead Source Detection:**
> For every site, verify: `curl https://{site}/ | head` must match the source `index.html`. If Caddy returns something else (text response, redirect, proxy), the source is dead.

## What Should Have Happened

### /000/ fix:
```
1. Decide: static constitutional page OR React Genesis page?
2. If React: delete public/000/index.html, rebuild, remove Caddy @genesis
3. If static: delete React <Genesis /> route and component, keep Caddy handle
4. Never allow both to exist for the same URL
```

### Forge fix:
```
1. Decide: static docs site OR webhook gateway response?
2. If static: change Caddy default handle to file_server
3. If gateway: remove the static source from repo to eliminate confusion
```

## Meta-Skill: Route-Hijack Detection

This scar demonstrates the **route-hijack** pattern:

1. **Event**: Caddy handle added → React route becomes dead code → users see wrong page
2. **Evidence**: `App.tsx` routes, `public/` contents, Caddyfile handles, live curl output
3. **Pattern**: Infrastructure layer (Caddy) overriding application layer (React) without coordination
4. **Lesson**: SPA + static file server = dangerous territory. Every path must have a single owner.
5. **Promote**: Add `spa-route-integrity-check` to all site deployment skills

## Confidence: HIGH

All facts verified against live Caddyfile, React source, static source, and HTTP responses.

## Related Scars

- `scar-kimi-site-audit-fabrication-2026-05-17` (documentation drift — same root: not verifying runtime)
- `scar-openclaw-diagnostic-cascade-2026-05-17` (action without verification)

## TREE777 Update Required

1. Update `skill-site-architecture` → add SPA Route Integrity Check section
2. Update `skill-caddy-config` → add anti-hijack verification step
3. Create `skill-dead-source-detection` → verify live output matches repo source

---

*DITEMPA BUKAN DIBERI — Architecture is forged by deletion, not by accumulation.*
