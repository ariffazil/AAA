# ZEN CLARITY AUDIT — /earth Site
> **Date:** 2026-07-30 · **Auditor:** Claude (DeepSeek v4-pro) · **Authority:** arifOS F2 TRUTH, F4 CLARITY
> **Sovereign:** Arif · **Scope:** arif-fazil.com/earth + linked GEOX surfaces
> **SEAL:** PENDING — human ratify after improvements deployed

---

## 0. EXECUTIVE SUMMARY

The /earth site is the **best single page in the arif-fazil.com constellation**. The interactive globe with live Macrostrat pipes, USGS earthquakes, and PB2002 plate boundaries is genuinely impressive. But the page has **structural entropy**: CSS duplicated 5× across pages, key content hidden behind collapsing `<details>`, no earth-specific navigation, and the GEOX tool surfaces are disconnected from the earth narrative.

**Score: 7.2/10** — Solid foundation. 8 improvements needed, 3 critical.

**ΔS target:** Reduce CSS duplication 80%, unhide 2 hidden sections, add 1 navigation component.

---

## 1. COMPLETE SITE MAP

### 1.1 Earth pages (arif-fazil.com)

```
arif-fazil.com/                      ← MAIN SPA (React shell)
└── /earth/                          ← Φ GEOX · The Dynamic Planet (69KB, 1089 lines)
    ├── /earth/kinabalu-basin/       ← Kinabalu Basin geological dossier (628 lines)
    │   └── (embeds via iframe) → /earth/kinabalu-cross-section.html
    ├── /earth/malay-basin/          ← Malay Basin geological dossier (585 lines)
    │   └── (links to) → /earth/malay-basin-cross-section.html
    ├── /earth/kinabalu-cross-section.html  ← SVG cross-section, standalone (754 lines)
    ├── /earth/malay-basin-cross-section.html ← SVG cross-section, standalone (605 lines)
    ├── /earth/kinabalu-basin.pdf    ← PDF version of Kinabalu dossier
    └── /earth/data/
        ├── wells.json               ← 4 sovereign-canon wells
        ├── studies.json             ← 0 studies (honest register)
        └── plates/
            ├── PB2002_boundaries.geojson
            └── PB2002_plates.geojson
```

### 1.2 GEOX surfaces (geox.arif-fazil.com) — linked from /earth

```
geox.arif-fazil.com/                 ← GEOX landing
├── /basins/kinabalu/index.html      ← Prospect cockpit (linked from earth dossiers)
├── /apps/prospect-ui/               ← Prospect Forge (linked from earth cockpits)
├── /apps/well-desk/                 ← Well Witness (linked from earth cockpits)
└── (40+ other .html files — tools, cockpits, viewers, wiki, theory, docs, workspaces)
```

### 1.3 WEALTH surface — linked from /earth

```
wealth.arif-fazil.com/apps/capital_judge/  ← Capital Judge (linked from earth cockpits)
```

### 1.4 Navigation graph (current)

```
/earth
  ├── #top (globe hero)
  ├── #what (intent cards)
  ├── #example (live query demo)
  ├── #real (why this is real Earth + stats)
  ├── #dynamic (3 readings + hidden deep time + hidden case study)
  ├── #dossiers (basin cards)
  ├── #geox (cockpit cards)
  └── #studies (0 studies rendered)

External links from /earth:
  → geox.arif-fazil.com (header nav)
  → geox.arif-fazil.com/basins/kinabalu/ (dossier card)
  → geox.arif-fazil.com/apps/prospect-ui/ (cockpit)
  → geox.arif-fazil.com/apps/well-desk/ (cockpit)
  → wealth.arif-fazil.com/apps/capital_judge/ (cockpit)
```

---

## 2. SEVEN DIMENSIONS AUDIT

### 2.1 STRUCTURE — "Real Earth at the Center"

**Current state:** The globe IS the hero. Full-viewport 3D globe with Macrostrat geological tiles, not a satellite photo. This is genuinely the best single design decision on the page. Carl Sagan quote reinforces the perspective.

**Issues:**
1. **CSS entropy (P1):** 5 HTML files, each with ~200 lines of duplicate CSS. The same `:root` variables, header styles, zen-pulse, typography are copy-pasted. ΔS > 0 on every edit.
2. **No shared earth stylesheet:** Unlike `/_shared/zen-all.js` (JS), there's no `earth.css` that all earth pages load.
3. **Font dependency:** 3 Google Fonts requests (Inter, Fira Code, JetBrains Mono). Self-hosting would remove 3 external dependencies.

**Verdict: STRUCTURE_GOOD — Fix CSS duplication.**

### 2.2 NAVIGATION — "Easily Navigated"

**Current state:** Header shows federation links (Home, GEOX, AAA, arifOS, MCP). This is NOT earth navigation — it's site-wide chrome.

**Issues:**
1. **No earth-specific navigation (P0):** The page is a long scroll with anchor links (#what, #dynamic, #dossiers, #geox). No sticky TOC, no "where am I?" indicator beyond the zen-pulse strip.
2. **Zen pulse underused (P1):** The zen-pulse strip at the top is excellent (WHERE / WHY CARE / WHAT NEXT) but it's small, easily scrolled past, and not replicated on subpages consistently.
3. **No breadcrumbs between earth pages (P1):** Basin dossiers have a back button to /earth but no breadcrumb like `/earth → Kinabalu Basin → Cross-Section`.
4. **Cross-sections are semi-hidden (P2):** You can't reach a cross-section directly from /earth. You must go through the dossier first. For a geoscientist, the cross-section IS the product.
5. **GEOX external links break context (P1):** Clicking "Prospect Forge" opens geox.arif-fazil.com in the same tab. No "← Back to Earth" on the GEOX side.

**Verdict: NAVIGATION_WEAK — Needs earth-specific TOC + breadcrumbs.**

### 2.3 THREE-CLICK RULE — "Max 3 Clicks from Main Site"

| Path | Clicks | Pass? |
|------|--------|-------|
| arif-fazil.com → /earth | 1 | ✅ |
| /earth → kinabalu-basin dossier | 2 | ✅ |
| /earth → kinabalu-basin → cross-section | 3 | ✅ |
| /earth → malay-basin → cross-section | 3 | ✅ |
| /earth → geox.arif-fazil.com (external) | 2 | ⚠️ leaves earth |
| /earth → geox → prospect-ui | 3 | ⚠️ organ boundary |
| /earth → cross-section (direct) | — | ❌ no direct path |

**Issues:**
1. **Missing direct-to-cross-section links (P1):** Cross-sections should be linkable from /earth directly, not only through the dossier.
2. **GEOX external hop (P2):** The GEOX organ boundary is architecturally correct but cognitively jarring. A user asking "show me the Kinabalu prospect" gets sent to a different domain with different navigation.
3. **No Layang-Layang dossier (P2):** It's listed as a waypoint on the globe but has no corresponding earth page. This is a broken promise.

**Verdict: 3CLICK_PASS (barely) — Add direct cross-section links + Layang-Layang page.**

### 2.4 CONTENT VISIBILITY — "No Hidden Subpages"

**Current state:** Two content sections are hidden behind `<details>` elements:

1. **"For the curious · 4-billion-year tape recorder + case study"** — This contains the deep time bar AND the Malay Basin case study. It is THE most educational content on the page. Hiding it behind a collapsible labeled "For the curious" signals it's optional. It is not. **The deep time bar is the answer to "why should I care about rocks."**

2. **"How to read the cross-section"** (on kinabalu-basin dossier) — Acceptable as collapsible (it's reference material).

**Issues:**
1. **Deep time + Malay Basin case study hidden (P0):** UNHIDE. This is core earth content, not optional curiosity.
2. **Studies section is honest but empty (P2):** 0 studies renders "0 STUDIES ON THE PUBLIC REGISTER" with a message about curation. This is truthful per F2 but visually a dead zone. Either add seed content or collapse the section until populated.

**Verdict: HIDDEN_CONTENT_VIOLATION — Unhide deep time + case study.**

### 2.5 COGNITIVE DESIGN — "Cognitively Pleasant for Human Viewing"

**What works:**
- Dark theme (`#0a0a0f`) with gold (`#d4af37`) and cyan (`#00d4aa`) accents — excellent contrast, easy on eyes
- Monospace for data/technical (`Fira Code`), sans-serif for reading (`Inter`) — correct cognitive separation
- Globe as hero — immediate "this is Earth" recognition
- Intent cards ("What can I do here?") — perfect for cognitive onboarding
- Zen pulse strip — 3-second orientation is brilliant UX
- Live example panel — "show me what happens" before the user commits to clicking
- Stats with live pipe sources — builds trust

**What needs work:**
1. **Intent cards below the fold (P1):** The "What can I do here?" section is the best cognitive onboarding on the page but it's at scroll position 2 (after the globe). Many users won't scroll. Add a subtle floating indicator or mini-intent strip near the globe.
2. **Text density (P1):** Below the globe, the page becomes dense prose. The Dynamic Earth section has 3 text-heavy cards. Good writing but visually fatiguing.
3. **Mobile: deck overlaps globe (P2):** The control deck is `position:absolute` on the globe. On mobile it covers the lower-right of the globe.
4. **No visual breathing room between sections (P2):** Sections are separated by a thin border. Section padding is generous (5.5rem) but the content within sections is compact.
5. **"Dossier" vs "Cockpit" distinction unclear (P2):** Basin dossiers and GEOX cockpits are different cards but the visual distinction (gold vs cyan top-border) is subtle. A geoscientist might not immediately understand: dossier = human-readable geology, cockpit = MCP tool interface.

**Verdict: DESIGN_GOOD — 5 improvements to elevate from good to great.**

### 2.6 DATA PIPES — "Honest Numbers from Pipes"

**What works:**
- Macrostrat tiles via weserv.nl proxy (CORS workaround)
- Macrostrat API stats (columns, packages, measurements) — live
- USGS earthquake feed — real-time, 24h window
- PB2002 plate boundaries — local geojson, properly attributed
- Wells from sovereign canon (wells.json) — existence-tier markers jittered
- Studies from studies.json — honest 0 count
- Pipe status strip at bottom-left of globe — transparent about what's loading/failed
- Withheld stat display ("UNVERIFIED" instead of invented number)

**Issues:**
1. **Studies.json has 0 entries (P2):** The register is honest but empty. Seed with the Kinabalu and Malay Basin dossiers as studies entries so the section renders something.
2. **Tile proxy dependency (P3):** `images.weserv.nl` is a third-party proxy for Macrostrat tiles. If it goes down, the geological globe goes blank.

**Verdict: PIPES_EXCELLENT — Seed studies.json.**

### 2.7 DEAD / MISSING / BROKEN CONTENT

| Item | Status | Action |
|------|--------|--------|
| Layang-Layang dossier | Missing | Waypoint exists on globe, no page. Create `/earth/layang-layang/` |
| Studies section | Empty (0) | Seed with 2 study entries from existing dossiers |
| kinabalu-basin.pdf | Exists | ✓ Good — PDF backup of the dossier |
| Cross-section direct links | Missing from /earth | Add to dossier cards on /earth |
| GEOX → /earth backlink | Missing | Add to GEOX basins/kinabalu page |
| Earth sitemap | Missing | Create `/earth/map/` or `/earth/sitemap/` |

---

## 3. IMPROVEMENT PLAN (8 items, priority-ordered)

### P0 — CRITICAL (breaks cognitive contract)

| # | What | Why | Δ Risk |
|---|------|-----|--------|
| **1** | **Unhide deep time + case study** | Core earth content hidden behind "For the curious." The deep time bar IS the reason geology matters. The Malay Basin case study IS the founder's expertise. These should be full sections, not collapsed `<details>`. | Reversible. Just HTML. |
| **2** | **Add earth-specific navigation** | Sticky section TOC on /earth showing: Globe · What Can I Do · Why Real · Dynamic Earth · Deep Time · Malay Basin · Dossiers · Cockpits · Studies. Each clickable. Current position highlighted. | Reversible. |

### P1 — HIGH (design/navigation improvement)

| # | What | Why | Δ Risk |
|---|------|-----|--------|
| **3** | **Create shared earth CSS** | Extract duplicated CSS from 5 files into `/earth/_shared/earth.css`. 200 lines × 5 files → 1 shared file. ΔS ≤ 0 on all future edits. | Reversible. |
| **4** | **Add breadcrumbs to all earth pages** | Every earth subpage gets: `/earth → Current Page`. Dossier cross-sections get: `/earth → Basin Dossier → Cross-Section`. | Reversible. |
| **5** | **Add direct cross-section links to /earth** | The dossier cards on /earth should have a secondary link: "▸ VIEW CROSS-SECTION" beside "▸ READ THE DOSSIER". The cross-section IS the product for a geoscientist. | Reversible. |

### P2 — MEDIUM (content completeness)

| # | What | Why | Δ Risk |
|---|------|-----|--------|
| **6** | **Seed studies.json with 2 entries** | Add Kinabalu Basin and Malay Basin studies to the register. The section exists but renders 0 — honest but looks broken. | Reversible. JSON file. |
| **7** | **Create /earth/map/ — visual sitemap** | A single page showing all earth surfaces as a navigable grid with descriptions. Satisfies "map all" + "no hidden subpages." | Reversible. New file. |

### P3 — LOW (nice-to-have, out of scope for today)

| # | What | Why | Δ Risk |
|---|------|-----|--------|
| **8** | Self-host fonts | Remove 3 Google Fonts dependencies. Inter + Fira Code + JetBrains Mono served from `/assets/fonts/`. Privacy + performance. | Reversible. |
| **9** | Add Layang-Layang dossier | Waypoint promised on globe. Deepwater frontier basin. Needs research before writing. | Content creation. |

---

## 4. IMPLEMENTATION ORDER

```
Phase 1 (this session): P0 #1 + P0 #2 → unhide content + add navigation
Phase 2 (this session): P1 #3 + P1 #4 + P1 #5 → shared CSS + breadcrumbs + cross-section links
Phase 3 (this session): P2 #6 + P2 #7 → studies seed + sitemap
Phase 4 (next session): P3 #8 + P3 #9 → fonts + Layang-Layang
```

---

## 5. BEFORE / AFTER — KEY METRICS

| Metric | Before | After (target) |
|--------|--------|----------------|
| CSS duplication | 5 files, ~1000 lines duplicated | 1 shared file, 5 thin overrides |
| Hidden content sections | 2 (`<details>`) | 0 |
| Navigation elements | 0 earth-specific | 1 sticky TOC + breadcrumbs |
| Cross-section access from /earth | 0 direct links | 2 direct links |
| Studies rendered | 0 | 2 |
| Earth pages total | 5 HTML | 6 HTML (+sitemap) |
| 3-click compliance | 4/6 paths pass | 6/6 paths pass |
| Broken promises | 1 (Layang-Layang waypoint, no page) | Documented in sitemap as "coming" |

---

*Audit forged 2026-07-30 · F2 TRUTH · F4 CLARITY · Ω₀ = 0.04*
*To be sealed after sovereign review.*
