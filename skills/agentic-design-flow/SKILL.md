---
name: agentic-design-flow
description: "ONE door for every design ask on federation web surfaces. Classifies the lane (new sovereign page / restyle existing / diagnose drift / generate imagery), then runs the pipeline READ → COMPOSE → BUILD → RENDER+MEASURE → DELIVER using the five design skills as stages. Trigger - any design request on arif-fazil.com, syedos, cockpit, MCP GUI, or any new sovereign surface - 'make it nicer', 'design a page', 'redesign', 'audit design drift', 'generate site imagery', or confusion about which design skill to load."
version: 1.0.0
forged: "2026-10-29 333-AGI, F13 ask 'make all the design skills into one agentic flow'"
---

# Agentic Design Flow — one door, five stages

The five design skills are STAGES of one pipeline, never rivals. Load this skill first; it routes to the stage skill. Skills are referenced, never copied (FEDERATION INIT law).

## Stage 0 — CLASSIFY (which lane?)

| Ask sounds like | Lane | Stage skill to load |
|---|---|---|
| "design/build a new page" for a sovereign-owned surface | NEW | `sovereign-surface-design` |
| "restyle / make nicer / align" an EXISTING live page | RESTYLE | `web-surface-design-fidelity` |
| "pages inconsistent / not aligned / drift" | DIAGNOSE | `federation-web-design-audit` |
| "generate image / hero / cover / share card / video loop" | IMAGERY | §Image lane below |
| injected body looks unstyled vs siblings / after deploy | PARITY | `injected-html-design-parity` |

`forge-design-intelligence` = reference layer for ALL lanes (industry patterns, palettes, typography, WCAG, anti-patterns, pre-delivery checklist). Load it second in every lane.

## Stage 1 — READ (all lanes)

The target page's own system is the specification. Never design from a sibling page's stack or from generic token fallbacks. Fetch the live page; verify fonts/colors against rendered reality, not docs.

## Stage 2 — COMPOSE (lane skill + reference layer)

Editorial law (sovereign surfaces): one loud element, ≥10:1 scale contrast, hairline rules not boxes, weight 300–400 at display size, neutral ground (warmth in the light, not the paper), canon tokens only (`/_shared/design-system/tokens.css`) — never a private `:root` palette.

## Stage 3 — BUILD (PARITY rules apply always)

Edit the SOURCE template, never the built output. Generator-owned artifacts revert. Deploy = HTML + assets together, one content hash across the webroot. Body must be flat HTML in host components.

## Stage 4 — RENDER + MEASURE (never eyeball-only)

Headless Chrome screenshot both viewports (phone 430 + desktop 1440, tall enough for footer). Prove JS ran (dump-dom + id grep). Measure pixels (near-black coverage, colour coverage, WCAG ratios) via `sovereign-surface-design/scripts/render_and_measure.py`. Then LOOK with vision for hierarchy.

## Stage 5 — DELIVER

Two options side by side, ask for one word. PNG in chat, not .html. State the weakest point (which ratio only clears large-text, what is estimate). Nothing deployed without F13; state reversibility.

## Image lane (free-quota generation, forged 2026-10-29)

```bash
bl image generate --model <model> \
  --api-key "$DASHSCOPE_API_KEY" \
  --base-url https://dashscope-intl.aliyuncs.com \
  --prompt "..." --size 1024*1024 --n 1 --watermark false --out-dir <dir>
```
- Models+quota: see `/root/forge_work/site-audit/image-quota-opportunities-2026-10-29.md` (image-3.0 expires FIRST — spend it on masters).
- ⚠ `qwen-mt-image-2.0` (edit) raw API shape UNKNOWN ("url error" on multimodal-generation) — use `bl` verbs only.
- Text/typesetting on generated art = PIL overlay (our job), never the model (boxes/garbled glyphs).
- Visual vocabulary: gold-ink hairline engraving on #08080A (canon `--soul-accent`), precedent = `/words/` compass hero.
- Every generated asset passes Stage 4 (measure + vision) before any site use; real-person imagery follows `forge-real-person-reference-photos` law (Wikimedia first, attribute, no T2I of real people).

## Iron rules

1. One door in, one deliverable out (2 viewports PNG + measurements + weakest point).
2. Never skip READ (type mismatch) or MEASURE (mud page found only by pixels).
3. Audit lane produces ranked fixes; the moment F13 says "buat ja", execute-on-say (audit skill P1).
4. Anti-bangang LAW 8: this flow ROUTES — it does not duplicate stage-skill bodies.
5. Deploy governance lives in `arif-sites-ops`; this flow stops at DELIVER unless F13 says deploy.

## Failure classes learned 2026-10-29 (deployed cases: /arifos/ + aaa.arif-fazil.com)

1. **Share-card probe (new audit step):** og:image must be probed as VALID URL + HTTP 200 on the asset. Found live: `/arifos/` shipped an unparseable og URL (`https://arifos observatory/og-image.jpg`) for months — invisible to every content gate that only checks markup presence. Also: a *working* borrowed card (`aaa` used the personal site's `og-identity.png`) is an identity miss — each sovereign surface carries its own master-derived card.
2. **JS-nav orphan:** a client-rendered `<nav>` (web component, SPA) reads fine to humans and is INVISIBLE to no-JS crawlers — the page audits as 0-nav. Audit rule: count nav links in RAW HTML; if zero but a nav component exists, require static fallback links (header home link + noscript lane).
3. **Symlink-served state files:** a webroot `index.html` may be a symlink into an organ state file (`/var/www/html/aaa/index.html → /root/AAA/state/federation-cockpit.html`). Patch the STATE file (SOT); verify with `file`/`ls -la` before assuming two copies. A double-patch script will assert-fail on the second pass — that failure is the tell.
4. **Master→asset pipeline (proven):** `m2-seal → /arifos/ og+emblem`, `m7-constellation → AAA og+emblem`. Recipe: center-crop 1.91:1 → 1200×630 JPEG q88 for og; 256px PNG for emblem; `alt` preserves any replaced glyph.
5. **Age-label pattern:** when a page already carries `data-observed-at` on `<body>`, a self-contained 8-line JS span renders "observed Xh ago" — honest freshness without touching the app.

Deployed receipts: /root/forge_work/receipts/RECEIPT-qwen-individual-seat-sambung-2026-10-29.md · audits in /root/forge_work/site-audit/.
