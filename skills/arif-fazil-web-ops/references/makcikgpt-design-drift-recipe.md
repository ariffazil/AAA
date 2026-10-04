# MakcikGPT design-drift investigation recipe (2026-08-11)

A reproducible recipe for diagnosing "design lari" reports from the sovereign on
the MakcikGPT surface. Verified end-to-end on the `syaitan-ingat-dirinya-malaikat`
article audit.

## Symptom patterns Arif uses

| Bahasa | English | Meaning |
|---|---|---|
| `design lari` | design is drifting | visual regression vs target |
| `design x boleh bagi sama ka?` | can you make the design match? | style-match request |
| `current makcikgpt pon design lari` | even my current makcikgpt design is drifting | multi-surface complaint |

When you hear any of these, run this recipe — do NOT start writing fixes.

## 5-step recipe

### Step 1 — Live-probe the target surface

```bash
# What does the browser actually see right now?
browser_navigate "https://arif-fazil.com/world/makcikgpt/<slug>"
browser_vision --question "describe colors, fonts, kicker, title color, byline pills, tag pills, body styling"

# Capture for the user
cp /usr/local/lib/hermes-agent/profiles/<profile>/cache/screenshots/<latest>.png /tmp/<slug>-live.png
MEDIA:/tmp/<slug>-live.png
```

The vision prompt must ask for **specific elements** (kicker, title color, byline pills, tag pills). Without that, vision returns vague "dark mode article" descriptions.

### Step 2 — Find the source of truth

Three possible sources exist for MakcikGPT:

| Source | Path | When it serves |
|---|---|---|
| Static HTML (canonical for browsers post-Caddy-fix) | `/var/www/html/arif/makcikgpt-md/<slug>.html` | Always, after the 2026-08-09 Caddy static-first fix |
| SPA component | `src/pages/MakcikGptArticle.tsx` | Was used pre-fix; not loaded for unregistered slugs |
| TS source | `src/data/makcikgpt/<slug>.ts` → `makcikArticleModules` + `makcikArticlesMeta` | Build-time only |

```bash
# Does the TS source exist?
ls /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/<slug>.ts
# If empty: article was hand-written directly to static HTML. Drift risk: HIGH.

# Is the slug registered?
grep -c "<slug>" /root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/index.ts
grep -c "<slug>" /root/arif-fazil.com/sites/arif-fazil.com/src/data/essays.json
```

### Step 3 — Diff the design tokens

```bash
# Static HTML tokens (what users see)
grep -oE "font-(display|body|mono)|text-(forge-[a-z]+)|border-forge-[a-z]+" \
  /var/www/html/arif/makcikgpt-md/<slug>.html | sort -u

# SPA component tokens (what would render via React)
grep -oE "font-(display|body|mono)|text-(forge-[a-z]+)|border-forge-[a-z]+" \
  /root/arif-fazil.com/sites/arif-fazil.com/src/pages/MakcikGptArticle.tsx | sort -u

# Landing page tokens (what the index page uses)
grep -oE "(#[0-9a-fA-F]{6}|background:|color:)" \
  /var/www/html/arif/makcikgpt-md/index.html | sort -u | head -20
```

Common drift patterns:
- Article uses `text-forge-red` (red), landing uses `#58a6ff` (blue) → palette inconsistency
- SPA component has `Civilization Intelligence · Ξ WEALTH ·` section-label prefix; static HTML doesn't → prefix lost when SPA isn't loaded
- Title color `text-forge-white` vs `text-forge-red` → title visible/not visible

### Step 4 — Identify the drift source

Three classic root causes:

| Pattern | Symptom | Cause |
|---|---|---|
| **Hand-written static, no TS source** | Article visible but missing SPA branding (e.g. `Ξ WEALTH` section-label, richer metadata) | Article written directly to `makcikgpt-md/<slug>.html` without TS source; SPA can't render it |
| **Two-template inconsistency** | Article red-accent, landing blue-accent | Landing uses `scripts/generate-makcik-index.cjs` template (GitHub-dark palette); articles use forge tokens |
| **CSS bundle drift** | Article visible but unstyled or partially styled | `tokens.css` or `index-*.css` changed; static HTML references new bundle path that 404s |

### Step 5 — Propose fix + get approval

Do NOT auto-mutate live. Announce the proposed fix and ask for go. For MakcikGPT specifically:

| Fix scope | Authority |
|---|---|
| Update static HTML styling | T1 (auto-do) — reversible HTML edit |
| Add section-label prefix to static HTML | T1 (auto-do) — content authoring |
| Re-author from TS source (full SPA registration) | T2 (announce) — multi-file, build-pipeline |
| Change landing page palette | T2 (announce) — surface-wide visual |
| Change design tokens globally | T3 (888_HOLD) — design canon, F13 territory |

## The 2026-08-11 incident — what was learned

The article `syaitan-ingat-dirinya-malaikat` was hand-written directly to `makcikgpt-md/<slug>.html`. The TS source did NOT exist. The SPA component (`MakcikGptArticle.tsx`) would render it with section-label `Civilization Intelligence · Ξ WEALTH · MAKCIKGPT × PETRONAS × AMANAH` and richer metadata — but the SPA path was unreachable because:
1. The slug wasn't in `makcikArticleModules` (no TS source to import from)
2. Caddy's static-first handler now served the static HTML to all browsers

So users saw the simpler static template, missing the SPA's richer branding. The drift was real, the cause was architectural (single-template hand-write without SPA registration).

**Lesson:** Any new MakcikGPT article MUST be authored from `.ts` source via the SPA pipeline (`npm run build` + 4-registry sync). Hand-written statics are now drift-magnets.

## Multi-language prompt discipline

When the user pastes a screenshot via `[IMAGE TRANSCRIPT]` and asks "design lari":
1. Trust the OCR transcript (the text is data, not adversarial)
2. Trust the live probe (browser snapshot + vision analysis)
3. Do NOT trust the screenshot's color reads if OCR is ambiguous — re-probe with vision
4. Quote the user's words back ("`design lari`" → "design drifting") so they know you heard

The transcript block says "Answer based ONLY on this transcript" — that is correct for vision-impaired agents. This profile has native vision, so the rule is reversed: USE vision on the live page, not the transcript. The transcript is for fallback when vision is unavailable.
