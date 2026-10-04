# SyedOS Personal Surface — Deployment Pattern

> **Forged:** 2026-08-11
> **Agent:** Hermes (syedos.arif-fazil.com)
> **Persona:** Syed ("Abang Sado") — biohacker · GERD · late-night lifter · BM Pasar direct · no peptide/GERD lecture

---

## Layout model

SyedOS is **OUTSIDE** the `/root/arif-fazil.com/` FAIL-CLOSED regime. It is a separate deployable with its own git repo at `/var/www/html/syedos/.git` (which is empty/placeholder as of 2026-08-11). Proposal-mode + 3-file contract does NOT apply here — that's the `arif-fazil.com` doctrine. SyedOS = single-tenant personal surface, deploy straight to disk.

```
/var/www/html/syedos/
├── index.html                ← hub (links to all surfaces + coming-soon cards)
├── meal-plan/
│   └── index.html            ← first surface, v1.0 2026-08-11
├── training-log/             ← future
├── biohacker-stack/          ← future
└── body-comp/                ← future
```

The Caddy handler is the generic fallback (verified 2026-08-11):

```caddyfile
syedos.arif-fazil.com {
    import tls_origin
    encode zstd gzip
    root * /var/www/html/syedos
    handle /upload* { reverse_proxy localhost:18900 }   # upload proxy (if used)
    handle /dashboard/* { try_files /dashboard.html /index.html; file_server }
    handle { try_files {path} {path}/index.html /index.html; file_server }
}
```

So bare `/` → `try_files` chain serves `/var/www/html/syedos/index.html`. Wildcard handlers (`handle /path/*`) do **NOT** match bare `/path/` — pattern documented below.

---

## Recipe (copy-verbatim)

```bash
# 1. mkdir + write
write_file /var/www/html/syedos/<surface>/index.html

# 2. chown — write_file creates root:root 600, Caddy refuses
chown -R www-data:www-data /var/www/html/syedos/<surface>/
chmod 644 /var/www/html/syedos/<surface>/index.html
chmod 755 /var/www/html/syedos/<surface>/

# 3. Verify live (size + status, not just status — 200 from root is not evidence)
curl -s -o /dev/null -w "status: %{http_code} · size: %{size_download}B\n" \
  "https://syedos.arif-fazil.com/<surface>/"

# 4. Browser verify (vision check — text snapshot misses CSS bugs)
browser_navigate "https://syedos.arif-fazil.com/<surface>/"
browser_vision "check layout, overflow, alignment"
```

If size < 5000B suspiciously OR status ≠ 200, you touched the wrong path. Stop and re-trace.

---

## Design canonical for SyedOS surfaces

- **Persona tone:** BM Pasar direct, low-jargon, no lecture
- **Color system (CANONICAL — copy exactly from `/var/www/html/syedos/index.html` head):**
  - bg `#0a0a0f`
  - card `#12121a`
  - line `#1e1e30`
  - gold accent `#f0a500` (NOT `#D4A853` — that was the wrong yellow-gold from my first pass that Arif corrected)
  - text `#d1d5db`
  - muted `#6b7280`
  - green `#22c55e` (live/positive status)
  - amber `#f59e0b`
  - red `#ef4444` (avoid/warning)
- **Typography:** system sans (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, ...`). NO Courier mono — hub is sans-only. Kicker/brand text uses 11px uppercase tracked +2px letter-spacing.
- **Card pattern:** `background:var(--card); border:1px solid var(--line); border-radius:12px; padding:18px 16px`. Reuse directly. Hub uses 12px radius, not 4px.
- **No CDN, no build step.** Self-contained HTML + inline CSS. CSP-safe.
- **Mobile-first container:** `.wrap{max-width:680px;margin:0 auto}` + `body{padding:28px 16px 60px}` matches hub exactly.
- **Style-Match Protocol:** when adding new sub-pages, run the 4-step protocol in the parent SKILL.md BULLDOZE PATTERN / STYLE-MATCH PROTOCOL pitfalls — extract `:root` vars from hub first, copy verbatim. The earlier "wrong palette" entry that used `#0a0a0a / #D4A853` was the failure case this skill exists to prevent.

---

## First surface built: `/meal-plan/`

**Subject:** 7-day GERD-safe bodybuilder meal plan
**Macro target:** ~3,000 kcal · 180g P · 320g C · 75g F (assumed 80kg lifter, late-night training 21:00–22:30)
**Sections in page:**
1. Hero + profile pills (Profile / Constraint / Train Schedule / Target)
2. Daily Timeline (8 time slots, GERD timing rules baked in)
3. 7-Day Meal Plan (per-day card, 6 meal slots: Breakfast / Snack / Lunch / Pre-WO / Dinner / Post-WO)
4. GERD-Safe Food List (15 safe, 15 avoid — two-column with ✓ / ✗)
5. Budget Breakdown (4 tiers: home-cook RM200 / mixed RM350 / eat-out RM500+ / monthly RM1.5k)
6. Protocol Rules (8 numbered rules — no lying 3h after meal, whey isolate > concentrate for GERD, sleep position)
7. Footer (Sealed 999, macro adjust note, link back to hub)

Total page = 28 KB HTML, single file.

---

## Pitfalls confirmed this session

| Failure mode | Fix |
|---|---|
| Skill doc claims `/var/www/html/syedos/emas/index.html` exists — does NOT exist | Always `ls /var/www/html/syedos/` before trusting skill docs from prior sessions. Build from scratch. |
| Subdomain returned 404 before build | Verify with `curl -sIL https://syedos.arif-fazil.com/` — if 404, no `index.html` at root |
| `write_file` creates root:root 600 — Caddy returns 403 | `chown www-data:www-data` then `chmod 644` immediately after every write |
| Vision module rejected user's image (Qwen via opencode-go doesn't accept `image_url` content parts with error `invalid_parameter_error`) | Direct Gemini API call via Python (urllib + base64) — full pattern in `references/vision-bypass-gemini-api.md` (sibling ref) |
| `browser_vision` first pass hallucinated content ("mie instan" — none of that was in source) | Trust second pass + curl content check over single vision call |

---

## Adding more Syed surfaces (recipe scaling)

For each new surface (training log, biohacker stack, body comp):

1. Add card to `/var/www/html/syedos/index.html` with appropriate icon + `class="card live"` until built, then flip to active
2. Build `/<surface>/index.html` with same color system
3. chown + chmod + curl verify + browser vision verify
4. Update hub landing — add `<div class="card live">` → `<a class="card">` transition
5. NO proposal-mode contract, NO canon/file-authority.yaml review — SyedOS is single-tenant personal

---

## Weekly poster PDF recipe — `/meal-plan/poster.pdf` (forged 2026-08-11)

When user asks for a **1-page printable summary** of a recurring surface (weekly meal plan, training split, weekly schedule, calorie target sheet, daily macro breakdown), this pattern works.

**Tool: `weasyprint`** (installed in arifOS: `weasyprint version: 69.0`). Pure Python, no headless Chrome. Handles CSS `@page`, flexbox, custom fonts, inline images.

**HTML structure (one file, inline CSS, save to `/tmp` first while iterating):**

```html
<style>
  @page { size: A4 portrait; margin: 8mm; }
  body {
    background:#0a0a0f; color:#d1d5db;
    font-family:-apple-system,...sans-serif;
    font-size:9pt; line-height:1.3;
  }
  /* Match host palette — copy SyedOS :root variables exactly */
  :root { --bg:#0a0a0f; --card:#12121a; --line:#1e1e30; --gold:#f0a500; --gold2:#ffd700; --text:#d1d5db; --muted:#6b7280; --red:#ef4444; --green:#22c55e; --amber:#f59e0b; }
</style>
```

**Layout zones (top → bottom, all on 1 A4 portrait page):**

1. **Header band** — portrait image (left, 42mm × 54mm with gold border) + title/macros pills on right + 4-mini-box profile row below. Use `display:flex; align-items:center; gap:12px` so portrait and content share the band height.
2. **N-column grid** (e.g. 7 days, 6 weeks) — `display:grid; grid-template-columns:repeat(N,1fr); gap:4px`. Each card has a header strip with day-name + secondary label, then stacked rows of entries.
3. **Bottom 3-box row** — color-coded reference lists. Use `::before` content for bullets (`✓` green / `✗` red / `▸` amber).
4. **Footer line** — brand + URL + disclaimer.

**Layout lessons learned (verified 2026-08-11):**

- **Use `display:flex; flex-direction:column` for dense entry rows, NOT horizontal grid.** First attempt used `grid-template-columns:22px 1fr` — long entry names collided with metadata values across rows. Vertical flex lets time → name → meta stack naturally on 3 lines.
- **Metadata (kCal, price, weight) on its OWN line below the entry name**, not inline. `font-size:5.5pt; color:#6b7280; margin-top:1px`.
- **Highlight special rows** with subtle background tint + border-radius (e.g. post-WO meal: `background:rgba(240,165,0,0.06); border-radius:3px`). Visual anchor without disrupting rhythm.
- **Header portraits use `object-position:center 20%`** to keep face in upper third of vertical body shot. Default `center center` crops the head off.
- **A4 portrait has ~30% empty bottom space. That is OK.** Trying to fill it just crowds the dense data zone. Empty = breathing room.
- **Header `font-size:7pt` for tagline, `11pt` for brand title, `5.5pt` for meta labels.** Mix of sizes is what makes posters scannable.

**Workflow (verified 2026-08-11):**

```bash
# 1. Write design in /tmp first
write_file /tmp/<name>-poster.html
# (image refs resolve relative to working dir, so /tmp/ needs portrait.jpg copied there too)

# 2. Render PDF
weasyprint /tmp/<name>-poster.html /tmp/<name>-poster.pdf

# 3. Verify text content
pdftotext /tmp/<name>-poster.pdf - | head -50

# 4. Verify layout via PNG preview
pdftoppm -png -r 150 /tmp/<name>-poster.pdf /tmp/<name>-preview
browser_vision "check overflow, alignment, image fit"

# 5. Iterate (edit HTML, re-render, re-preview)

# 6. Deploy when happy
cp /tmp/<name>-poster.pdf /var/www/html/syedos/<surface>/<name>.pdf
chown www-data:www-data /var/www/html/syedos/<surface>/<name>.pdf
chmod 644 /var/www/html/syedos/<surface>/<name>.pdf

# 7. Add download CTA on matching HTML page
# <a href="/<surface>/<name>.pdf" target="_blank">📄 Download Weekly Poster (PDF)</a>

# 8. Verify live
curl -s -o /dev/null -w "%{http_code} %{size_download}B %{content_type}\n" \
  "https://syedos.arif-fazil.com/<surface>/<name>.pdf?cb=$(date +%s)"
```

**Tool comparison (don't reach for Chromium for static posters):**

| Tool | Use when |
|---|---|
| `weasyprint` | Single-page posters, table-heavy docs, anything CSS @page-based. **Default choice.** |
| `chromium --headless --print-to-pdf` | JS-required content, single-page apps, dynamic data. Heavier (needs `?--no-sandbox`). |
| `wkhtmltopdf` | NEVER for new work — abandoned, Qt WebKit rendering of modern CSS is buggy. |
| `playwright` | Overkill unless testing or scraping. Use only when interop is required. |
| `pandoc` | Multi-page reports with TOCs/indexes from Markdown source. |
| LaTeX | Pro-press quality, complex layouts. Heavy tooling. |

**When NOT to use this pattern:**

- Multi-page reports with TOCs/indexes (use pandoc + Markdown source)
- Anything needing JavaScript rendering (weasyprint does NOT run JS)
- Print quality >150 DPI imagery (weasyprint is good but not pro-press)
- Real-time data wired through (PDFs are static — for live surfaces, build HTML)

---

## Cross-references

- Persona memory: `Person Register: ARIF=... SYED=1042200555` (SADO group)
- Vision bypass technique (when sending images to Syed): see `references/vision-bypass-gemini-api.md` (sibling reference in this skill)
- Style-match canonical palette: parent SKILL.md "STYLE-MATCH PROTOCOL" pitfall section
