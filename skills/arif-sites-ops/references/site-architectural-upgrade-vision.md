# Site Architectural Upgrade Vision — 2026-08-10

> Context: Deep kernel/state discussion produced a clear upgrade roadmap for arif-fazil.com.
> Status: VISION, not yet executed. P2 priority after /999/ live surfaces.

## Current State Diagnosis

The site is a **magazine**, not a **federation interface**. It publishes ABOUT the federation but doesn't SHOW the federation. The only live surface is `/999/verify` (reverse-proxy to arifOS :8088). Everything else is baked HTML.

SPA shell takes 6+ seconds to mount — anti-pattern for a governance site. Static shells load instantly.

## Three Upgrades (in priority order)

### 1. Static-First (T1, immediate)

Make static-first the primary experience. SPA becomes progressive enhancement only.

- The fallback page already does this (shows static links when SPA times out)
- Interactive elements (sliders on /propa/, globe on /earth/) load AFTER static shell renders
- SPA should never be the primary content path for governance pages
- Immediate UX win, no governance risk

### 2. Make /999/ The Living Proof (T2)

Extend the `/999/verify` pattern (reverse-proxy to kernel) to show live federation state:

| Surface | Source | What it shows |
|---|---|---|
| `/999/verify` | arifOS :8088 | Kernel attestation (EXISTS ✓) |
| `/999/health` | `make health` output | Federation organ status |
| `/999/vault` | VAULT999 tail | Last N sealed receipts |
| `/999/flow` | arifFlow :7073 | Live FQ pulse |

This makes doctrine OBSERVABLE, not just readable. "F1-F13 are binding constraints" → here's the live proof.

### 3. Cross-Lane Bridges (T3)

Connect doctrine to reality. Every floor page shows where in reality that floor is being tested RIGHT NOW.

Example:
```
/words/doctrine/F5/
  → "F5 PEACE² is stressed when:"
  → live link to /propa/ (corporate pressure)
  → live link to /malaysia/ (sovereign pressure)
  → live FQ reading from arifFlow
  → last seal that invoked F5 from VAULT999
```

The `/propa/` ↔ `/malaysia/` coupling (subsidy paradox) is the proven pattern — extend it to all floors.

## What NOT To Do

- Don't add JSON-LD / SEO before fixing the site to show live state
- Don't re-index sitemap until /999/ surfaces are live (Google should index reality, not snapshots)
- Don't add more essays until the bridge works (publication without connection is just a blog)
- Don't try to align /earth/ to the hub frame — it's a specialty page, not a template

## Implementation Notes

- /earth/ has its own design system (don't force hub alignment)
- Hub hero pattern is defined: kicker → h1 → visual → prose → pull-quote → hint
- Static shells use inline `<style>` (generator emits them)
- SPA route dead weight: WorldArrow.tsx serves nothing; static /world/ wins
- The site serves as both human interface AND machine interface (/llms.txt, /floors.json, /999/verify)
