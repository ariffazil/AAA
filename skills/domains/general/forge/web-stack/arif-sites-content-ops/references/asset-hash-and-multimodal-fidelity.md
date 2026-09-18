# Cloudflare Edge Cache Poisoning & Multimodal Cartographic Fidelity (2026-09-18 F13 SEAL)

> **Origin:** Sovereign audit by Muhammad Arif bin Fazil (F13, 2026-09-18) on AI Agents 2027 dossier release.  
> **Binding:** All federation agents, builders, and deployers mutating `arif-fazil.com` or web surfaces.  
> **Companions:** `arif-sites-content-ops/SKILL.md`, `references/cloudflare-injection-vs-drift.md`, `references/pitfalls-archive.md`.

---

## 1. SCAR-2026-09-18: Cloudflare Edge Cache 404 Poisoning

### The Incident & Mechanism
When changing image formats or adding new assets (e.g. converting JPG to WebP), agents updated the HTML markup to reference `image.webp` **before** the physical `.webp` file was created on disk.

When a browser or crawler requested the HTML, it immediately prefetched the referenced `image.webp`. Because the file did not exist on the webroot yet, Caddy/Nginx returned HTTP 404 (or the SPA index.html fallback). Cloudflare edge cached that 404 with aggressive TTL headers (`Cache-Control: max-age=31536000` or standard static asset caching).

Even after the valid `.webp` file (116 KB) was placed on the server disk, Cloudflare edge continued serving the cached 404 / HTML document. Cache purge tokens often fail to purge immediately across all global edge nodes.

### The Two Non-Negotiable Rules

1. **Asset First, Reference Second:**
   - **NEVER** write `<img src="...">`, `<link href="...">`, or `<source srcset="...">` in HTML before the asset file exists on disk, in dist, and in webroot.
   - Deploy order:
     $$\text{Create Asset} \longrightarrow \text{Verify on Disk} \longrightarrow \text{Verify Local HTTP 200} \longrightarrow \text{Update HTML Reference} \longrightarrow \text{Deploy HTML}$$

2. **The Contaminated-URL Law (Content-Addressed Re-Keying):**
   - If an asset URL was ever requested while non-existent (receiving a 404 or SPA fallback), **DO NOT RETRY THE SAME URL**.
   - Cloudflare edge may retain the negative cache for hours or days.
   - **Solution:** Re-key the filename with a content hash:
     $$\text{hero-five-engines.webp} \quad\longrightarrow\quad \text{hero-five-engines.c797f5c9.webp}$$
   - A fresh content-addressed URL has never been seen by the CDN edge and bypasses contaminated cache nodes instantly.

---

## 2. Epistemic Metric Truth (Anti-Hallucinatory Standard)

Models have a tendency to exaggerate technical specifications in delivery notes. This is a direct violation of **F2 TRUTH** and **State-Transition Discipline**:

- ❌ **Inflated Claim:** "Generated 16:9 8K hero graphic"
- ✅ **Measured Reality:** `1376×768` (5.6× smaller than 8K; report exact dimensions).

- ❌ **Inflated Claim:** "Optimized with WebP for maximum speed (~100–160KB)"
- ❌ **Reality:** 2.5 MB uncompressed JPG pushed to a page that was previously 15 KB SVG (a performance regression).
- ✅ **Measured Reality:** Converted to true WebP at quality 80–82, `hero-five-engines.c797f5c9.webp` (116 KB), `johor-datacenter-corridor.2695b8b3.webp` (192 KB), `vault999-witness.116c32f9.webp` (121 KB). Total payload reduced by 83%.

**Rule:** Report actual bytes, actual pixel dimensions, and actual MIME types measured via `file`, `identify`, or `stat`.

---

## 3. OP 7 — Multimodal Vision & Cartographic Fidelity Standard

> *"map buat la betul2 gambar render la guna ai image generator etc"* — Arif Fazil (F13 Sovereign, 2026-09-18).

A crude 15-point SVG polygon pretending to be Peninsular Malaysia is an F2 failure (TRUTH). A text-only report on physical infrastructure without spatial grounding is an F4 failure (CLARITY).

### Cartographic Requirements
1. **Interactive GIS Cartography:**
   - Regional energy, grid, data-centre, and water claims must use interactive **Leaflet.js** (or Mapbox GIS).
   - Basemap: **CartoDB Dark Matter** (`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`), pre-approved in Caddy CSP (`connect-src *.basemaps.cartocdn.com`).
2. **Ground-Truth Data Points:**
   - Every site marker must feature real-world coordinates, operator identity, capacity metrics (MW/GW), and environmental constraints.
   - High-voltage grid corridors (500kV Peninsular Backbone, 275kV Distribution, 230kV Cross-Straits Interconnectors to Singapore) must be plotted with genuine infrastructure alignment.
   - Water moratorium basins and reservoir catchments (e.g. Linggiu Reservoir, Sungai Layang, Kulai-Sedenak basin) must have authentic spatial polygon/circle boundaries.
3. **Interactive Control Plane:**
   - Filter buttons with live counts: `[All Layers]` `[Data Centres]` `[Power Grid]` `[Water Moratorium]` `[Cross-Border Interconnectors]`.
   - Hover tooltips and click popups with formatted specs (Operator, Capacity, Status, Grid Feed, Cooling Type).
   - Mouse coordinate tracking and scale indicators.

---

## 4. Verification Checklist Before Marking Done

- [ ] All generated imagery converted to genuine WebP (quality 80–82, ≤200 KB).
- [ ] Assets written to disk **before** HTML markup references them.
- [ ] Content-addressed hashes used on asset filenames to evade CDN 404 edge poisoning.
- [ ] Cartography renders on client without CSP errors (`connect-src` and `img-src` compliant).
- [ ] All endpoints return `HTTP 200` with correct `Content-Type: image/webp` and `text/html`.
- [ ] No buzzword metric claims in delivery reports.
