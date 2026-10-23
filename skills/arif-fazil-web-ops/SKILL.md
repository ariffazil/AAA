---
name: arif-fazil-web-ops
description: "Use when a request names the arif-fazil.com market pages, syedos.em as or the /_shared design system, or when old notes point at arif-fazil-web-ops. Pointer stub — the live owner is arif-sites-ops; this skill only routes and records where its content went."
version: "2.0.0-stub"
relations:
  - target: arif-sites-ops
    type: alternative_to   # canonical owner since 2026-10-23 (F13 consolidation, LAW 8)
  - target: arifos-site-patch-without-caddy-reload
    type: related
superseded_by: arif-sites-ops
superseded_on: 2026-10-23
---

# arif-fazil-web-ops — POINTER STUB

> **Not the procedure.** Since 2026-10-23 this capability is owned by one skill:
> **`arif-sites-ops`**. Load that. Four skills for one problem was a LAW 8 violation —
> 362KB across four bodies, each with its own stale copy of the same deploy rule.
> This stub is kept (not deleted) so old notes, links and agent memory still resolve.

## What this skill used to do (105KB)

Operated arif-fazil.com public surfaces: market pages (/gold /oil /gas /klci /usdmyr), the syedos EMAS dashboard, `/_shared` design-system assets, `/words/` section pages, the `/makcikgpt-md/` mirror, the `/world/` atlas landing page, live-data wiring, the Transmission Engine visualization, and the design-recovery recipes.

## Where its content went

- **Transmission Engine visualization (29KB, ExxonMobil IR style)** → `arif-sites-ops/references/transmission-engine-viz.md`
- **Archive archaeology, the serving-path rule, `/_shared` deploy-root trap, `/words/` and
  makcikgpt-md surfaces, live-data wiring, atlas, recovery recipes, memory anchors** →
  `arif-sites-ops/references/web-surfaces.md`
- **Its pitfall list (29KB)** → merged into `arif-sites-ops/references/pitfalls.md`
- **Its own 18 dated references** stay in place at `arif-fazil-web-ops/references/`
  (kept on disk; read them only if site-ops points you here).

## What to do instead

1. Load `arif-sites-ops` — the current rule, human-first gate, architecture map, dead-URL trace,
   sanctioned deploy path, and the merged pitfall ledger are there.
2. For the ship step itself: `arifos-site-patch-without-caddy-reload` (additive, no Caddy reload).
3. If you came here for a dated worked case, the file is still on disk under this skill's
   `references/` — read it as history, and let `arif-sites-ops` decide the action.
4. Do not add new content to this stub. New site knowledge goes to `arif-sites-ops`.
