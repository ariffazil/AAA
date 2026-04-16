# TODO.md — GEOX · 2026-04-12

## PRIORITY 1 — Immediate (Before Next Session)

### arifosmcp server.json fix
- [ ] Regenerate `server.json` — tool count says "7" but /tools shows 17
- [ ] Version mismatch — runtime is `2026.04.07`, server.json has `2026.03.10`
- [ ] Location: `/opt/arifos/sites/arif-fazil.com/arifosmcp/` or wherever it lives

### /a2a surface claim
- [ ] Returns HTML fallback, not JSON agent routes
- [ ] Either wire it properly or remove from public surfaces list
- [ ] Apply 888 HOLD — do not claim LIVE if not confirmed

### /prompts surface
- [ ] Returns HTML fallback, not prompts list
- [ ] Either wire it or remove from surfaces

### SEO layer for geox-site
- [ ] Generate `sitemap.xml` for geox-site
- [ ] Add `robots.txt`
- [ ] Add canonical URLs to all pages
- [ ] Add OpenGraph meta tags to map/index.html

### status.json for geox-site
- [ ] Generate `/opt/arifos/sites/arif-fazil.com/geox/status.json`
- [ ] Auto-refresh via cron or on deploy

---

## PRIORITY 2 — MAP Enhancements

### Click chain end-to-end test
- [ ] User clicks a point in Borneo → inspector shows geology + quakes + coords
- [ ] Verify / Context / Signals modes each fire correctly
- [ ] Bottom tray logs each MCP call with timestamp

### GEBCO deep zoom quality
- [ ] WMS tiles grainy at zoom 10+
- [ ] Consider tile caching or alternative tile source
- [ ] Add GEBCO attribution to map attribution layer

### Transform tool proj4 wiring
- [ ] Wire `transformCoords()` to actual proj4 library or backend MCP tool
- [ ] Add EPSG:3857 ↔ 4326 bidirectional transform
- [ ] Show input/output CRS labels in inspector

### Faults layer resolution
- [ ] Document why USGS Quaternary Faults is BLOCKED
- [ ] Find alternative service path or honest label
- [ ] GEM Global Active Faults same

### Layer toggles on mobile
- [ ] Verify all layer checkboxes toggle correctly on mobile
- [ ] Test GEBCO toggle on mobile — does it add/remove correctly?

---

## PRIORITY 3 — Platform Pages

### /prospect audit
- [ ] Check for stale data or broken links
- [ ] Verify layer status honest
- [ ] Check 888 HOLD triggers

### /wiki audit
- [ ] Cross-check against UNIFIED_ROADMAP.md for accuracy
- [ ] Update if roadmap has drifted from wiki
- [ ] Fix any broken internal links

### /tools audit
- [ ] Verify skills/index.html wired to actual skills registry
- [ ] Check MCP tools listed match actual /tools endpoint

---

## PRIORITY 4 — Architecture

### Git push for geox map
- [ ] Add SSH key to this machine OR push from machine that has it
- [ ] Push commits f7b04819 and c9dc827c to GitHub

### Traefik routing for geox.arif-fazil.com
- [ ] Currently returns 404 via traefik
- [ ] Direct IP:port works — fix routing

### arifOS MCP GitHub push
- [ ] Same SSH key issue — resolve once

---

## Done (2026-04-12)
- [x] GEOX MAP v4 — GEBCO WMS fixed, probe working, real geology data
- [x] Mobile CSS — sidebar top bar, map 55vh, inspector bottom slide
- [x] Visual polish — margins, tray height 110px, active tab green underline
- [x] Inspector 7 sections live
- [x] Bottom tray 3 tabs live
- [x] MCP chains wired
- [x] 10-layer catalog with honest status
- [x] Commits f7b04819 + c9dc827c

---

## Principles
- **DITEMPA BUKAN DIBERI** — forged, not given
- **888 HOLD** before claiming anything LIVE that isn't confirmed
- **Provenance always visible** — source, license, status per layer
- **Federate don't mirror** — prefer BBOX queries, tiles, WMS over local copies
