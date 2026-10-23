---
name: arif-fazil-site-ops
description: "Use when a request names arif-fazil.com deploy, build pipeline or nav canon and an older note points here. Pointer stub — the live owner is arif-sites-ops; this skill only routes and records where its content went."
version: "2.0.0-stub"
relations:
  - target: arif-sites-ops
    type: alternative_to   # canonical owner since 2026-10-23 (F13 consolidation, LAW 8)
  - target: arifos-site-patch-without-caddy-reload
    type: related
superseded_by: arif-sites-ops
superseded_on: 2026-10-23
---

# arif-fazil-site-ops — POINTER STUB

> **Not the procedure.** Since 2026-10-23 this capability is owned by one skill:
> **`arif-sites-ops`**. Load that. Four skills for one problem was a LAW 8 violation —
> 362KB across four bodies, each with its own stale copy of the same deploy rule.
> This stub is kept (not deleted) so old notes, links and agent memory still resolve.

## What this skill used to do (99KB)

Covered building, integrating and deploying arif-fazil.com: topology, the `sites/arif-fazil.com` build pipeline, the deploy workflow, the proposal-manifest pattern, the design-invariants and design-lint chrome gate, archived-design recovery, and nav canon v7.

## Where its content went

- **Topology, build pipeline, deploy workflow, proposal manifest** →
  `arif-sites-ops/references/build-deploy.md`
- **Nav canon v7** → `arif-sites-ops/references/nav-canon-v7.md` (the longer of the two copies)
- **Pitfalls (47KB, 36 blocks)** → merged into `arif-sites-ops/references/pitfalls.md`
- **The static 28KB "Support files" directory dump was dropped** — an index of files is not
  a skill body; `ls references/` answers it live.
- **Its 18 dated references** stay on disk at `arif-fazil-site-ops/references/`.

## What to do instead

1. Load `arif-sites-ops` — the current rule, human-first gate, architecture map, dead-URL trace,
   sanctioned deploy path, and the merged pitfall ledger are there.
2. For the ship step itself: `arifos-site-patch-without-caddy-reload` (additive, no Caddy reload).
3. If you came here for a dated worked case, the file is still on disk under this skill's
   `references/` — read it as history, and let `arif-sites-ops` decide the action.
4. Do not add new content to this stub. New site knowledge goes to `arif-sites-ops`.
