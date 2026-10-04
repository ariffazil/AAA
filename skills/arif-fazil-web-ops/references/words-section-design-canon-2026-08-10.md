# Words Section Design Canon (2026-08-10)

## Unified Design Principle: Contrast yet Federated

All `/words/` sub-pages share:
- **5-lane nav:** Home · Earth · Words · World · Work
- **Brand:** ARIF FAZIL (top bar)
- **Design system:** tokens.css + hub-words.css
- **Dark theme:** #0A0B0D background, #EDEAE2 text
- **Gold accent:** #D4A853 (words domain)

## Per-Page Design

### /words/ (Landing)
- **Hero:** Compass SVG (slow rotation) + T.S. Eliot quote
- **Content:** 13 Floors preview (compact grid) + Featured Essays (4 cards)
- **CSS:** hub-words.css (compass animation, hero grid)

### /words/doctrine/
- **Hero:** Title "13 Floors." + subtitle + intro paragraph
- **Content:** 3 sections (Hard/Soft/Derived) with color-coded cards
- **Floor card:** number → name → badge → essence → explanation
- **F13 highlighted:** Gold border, elevated background
- **Colors:** --hard: #D4536B, --soft: #D49D53, --derived: #6BCF8B

### /words/writing/
- **Hero:** Title "Constitutional Essays" + description + stats
- **Featured:** 2×2 grid with "START HERE" badge
- **Listing:** Chronological groups with series labels (S4/S6/S8)
- **Card:** Gold accent line at top → title + date → excerpt → tags + CTA

### /words/constitution/
- **Hero:** Title "/constitution" + metadata (CANONICAL, Source, Issued, Authority)
- **Content:** Detailed floor cards with metrics, scale, violation, doctrine
- **Audience:** Agent-facing (detailed reference)

## Card Pattern (MakcikGPT-aligned)

Both MakcikGPT and Writing use the same card structure:
```
┌─ [accent line] ─────────────────────────┐
│ Title                          Date      │
│ Excerpt text...                         │
│ [tags]                    Read essay →  │
└─────────────────────────────────────────┘
```

**MakcikGPT:** Red accent (#E4572E), BM voice, domain tags
**Writing:** Gold accent (#D4A853), English academic, series tags

## Series Tag Colors
- S4 (Governance Canon): gold #D4A853
- S6 (Eureka Trilogy): cyan #4FC3F7
- S8 (Forge): ember #E4572E
- SITE: muted #8A8578

## Deploy Recipe
```bash
# 1. Write to live
write_file /var/www/html/arif/words/<subpage>/index.html
# 2. Fix permissions
chown www-data:www-data /var/www/html/arif/words/<subpage>/index.html
chmod 644 /var/www/html/arif/words/<subpage>/index.html
# 3. Sync to source repo
cp /var/www/html/arif/words/<subpage>/index.html \
   /root/arif-fazil.com/sites/arif-fazil.com/public/words/<subpage>/index.html
# 4. Verify live
browser_navigate → browser_vision
```

## Anti-Patterns
- ❌ Duplicate content (hidden flat-lists alongside card lists)
- ❌ Zen-pulse bar on sub-pages (only on hubs)
- ❌ Old 7-item nav (must be 5-lane)
- ❌ Old CSS imports (zen.css, economics.css — use tokens.css + hub-words.css)
- ❌ Agent-facing metadata on human pages (lane/org/ring badges)
