---
name: arif-sites-content-ops
description: "Use when editing essays or route-level pages on arif-fazil.com and an older note points here. Pointer stub — the live owner is arif-sites-ops; this skill only routes and records where its content went."
version: "2.0.0-stub"
relations:
  - target: arif-sites-ops
    type: alternative_to   # canonical owner since 2026-10-23 (F13 consolidation, LAW 8)
  - target: arifos-site-patch-without-caddy-reload
    type: related
superseded_by: arif-sites-ops
superseded_on: 2026-10-23
---

# arif-sites-content-ops — POINTER STUB

> **Not the procedure.** Since 2026-10-23 this capability is owned by one skill:
> **`arif-sites-ops`**. Load that. Four skills for one problem was a LAW 8 violation —
> 362KB across four bodies, each with its own stale copy of the same deploy rule.
> This stub is kept (not deleted) so old notes, links and agent memory still resolve.

## What this skill used to do (83KB)

Covered content on arif-fazil.com (React 19 + Vite): essay location and structure, route-level pages, SENSE_ALIGN design gate, canon-driven navigation, file governance states, partial-rsync failures, dual-lane UA routing, served-truth audit, site cron, and the Caddyfile patching workflow.

## Where its content went

- **All sections** (deployment gate, architecture, build & deploy, governance fix workflow,
  NS Election GIS, web-canon atlas, SENSE_ALIGN, canon nav, file governance, partial rsync,
  served-truth audit, essays/homepage zen design, site cron, ABCD framework, route pages,
  design preferences, Caddyfile patching) → `arif-sites-ops/references/content-ops.md`
- **Pitfalls** → merged into `arif-sites-ops/references/pitfalls.md`
- **Its 29 references** stay on disk at `domains/general/forge/web-stack/arif-sites-content-ops/references/`.

## What to do instead

1. Load `arif-sites-ops` — the current rule, human-first gate, architecture map, dead-URL trace,
   sanctioned deploy path, and the merged pitfall ledger are there.
2. For the ship step itself: `arifos-site-patch-without-caddy-reload` (additive, no Caddy reload).
3. If you came here for a dated worked case, the file is still on disk under this skill's
   `references/` — read it as history, and let `arif-sites-ops` decide the action.
4. Do not add new content to this stub. New site knowledge goes to `arif-sites-ops`.
