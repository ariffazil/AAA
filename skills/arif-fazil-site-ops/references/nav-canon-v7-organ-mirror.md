# Nav canon v7.0 — the organ→site mirror

The 5-item top-nav is not decorative. It is the **human mirror** of the federation's
organ outputs. Agents consuming `.well-known/` / `llms.txt` / `machine_links` see the same
organ topology from the other side. Pages for humans, contexts for agents — the Zen.

## The locked mapping (2026-08-06)

| Top nav | Organ | What the page is the portal for |
|--------|-------|----------------------------------|
| HOME | AAA | The cockpit — identity, trust root, you land here |
| EARTH | GEOX | Geology, seismic, basins, wells |
| WORDS | arifOS | Doctrine, constitution, F1–F13, essays, law, MakcikGPT |
| WORLD | WEALTH | Commodities, markets, vitals, politics + organ portals |
| WORK | WELL | Exploration wells, missions, resume |

Organs are **agent-owned** — they live in `machine_links` (footer + .well-known) and are
referenced FROM the human pages, not promoted as nav items.

**Words absorbs ALL written/doctrinal content** — Voice (MakcikGPT) + Essays + Doctrine + Law + /writing/ + /world/makcikgpt/ are all aliases to `/writing/`. URL didn't move; the LABEL unified under one nav item. The MakcikGPT corpus stays at `/world/makcikgpt/` for URL stability (zero redirect hell, articles already indexed), but is reachable via the WORDS alias and surfaced as a card on the World hub.

Aliases in canon (so old URLs keep working):

```json
{
  "label": "Words",
  "href": "/writing",
  "aliases": ["/read", "/essays", "/doctrine", "/law", "/world/makcikgpt"]
}
```

## The Words rename — full iteration trail (avoid this in future renames)

- v5.0 — "Words" = single replacement for Voice + Essays only
- v5.1 — expanded to absorb Doctrine + Law (user: *"nope. PETRONAS, POLITICS, ECONOMICS all collapse under world. So nav only have HOME, EARTH, WORDS, WORLD, WORK. LAW DOCTRINE ALL UNDER WORDS."*)
- v6.0 — added explicit `organ: arifOS` field per nav item; HOME got organ=arifOS-kernel
- v7.0 — corrected HOME organ via principal-relationship check (HOME: HERMES was wrong → AAA is right because AAA is principal's control plane, not an agent). HERMES moved to machine_links as agent bridge (Telegram gateway).

**The lesson:** when the user is renaming a nav label, expect 3-5 iterations before lock. Each iteration expands the alias list. Don't apply aliases piecemeal — wait until the user says the label is final, then write the full alias array in one `navCanon.ts` regeneration. Multiple regenerations in a row = drift between `navigation.json` and `navCanon.ts`.

## Organ-assignment rule (principal-relationship check)

When choosing which organ owns a nav slot, ask: *"what is the principal's relationship to this organ?"*. HOME went through HERMES → AAA in one session because:

- HERMES is the messenger (Telegram gateway) — the agent you talk to.
- AAA is the control plane (cockpit, registry, A2A gateway) — where the principal *binds* to agents.
- The sovereign lands at HOME; the sovereign doesn't *land* at an agent.
- Organs belong to agents; pages belong to humans.

So the nav slot is human-facing; assign to the organ whose outputs the human actually consumes on that page. AAA is the principal's dashboard, so HOME → AAA.

## Hero-core doctrine (locked 2026-08-06)

Every top-level homepage carries a CENTER HERO with one dynamic visual that IS the nav item's core metaphor. The hero is the first thing the reader sees; it must move; it must be different per nav.

| Page | Hero core | Metaphor |
|------|-----------|----------|
| HOME | ⏰ clock | time, identity, arrow-of-time |
| EARTH | 🌍 globe | earth, geology, basins |
| WORDS | 🧭 compass | doctrine, law, direction |
| WORLD | 🗺️ atlas | what's happening, GDELT map |
| WORK | ❤️‍🩹 heart | wells, missions, life-work |

Heroes are JS-rendered canvas/SVG (not PNG screenshots). Static hero = dead hero. For WORLD, the existing `/world/sot/` D3+GDELT globe is the hero — don't add a separate hero, link to the atlas. For HOME, the live clock dial already exists. For EARTH, WORDS, WORK: hero forge is pending — use agy CLI or equivalent dynamic-visual forger.

## All-artifacts-fit-under-5 rule (locked 2026-08-06)

Every artifact on arif-fazil.com MUST live under one of the 5 top-level pages. No orphans. No root-dangling routes. Audit recipe and current artifact inventory: see `references/5-page-artifact-fit-map.md`.

Decision rule for new artifacts:
1. Does it fit under an existing 5-page home? → put it there.
2. Does it fit under WORLD (the catch-all for "what's happening")? → put it there.
3. Is it a new organ? → escalate to F13 for 6th nav item OR make it an organ door in machine_links + portal card on the closest page.
4. Is it a one-off experiment? → `forge_work/proposals/`, not `public/`.
5. Is it a PDF/report? → `forge_work/out/`, not `public/`. PDFs are artifacts, not pages.

## File locations

| Layer | Path | What it does |
|-------|------|--------------|
| Canon (single source of truth) | `/root/web-canon/canon/navigation.json` | `primary_links`, `secondary_links`, `machine_links`, `keyboard_shortcuts`, `frame`, `doctrine` |
| Generator | `/root/arif-fazil.com/sites/arif-fazil.com/scripts/generate-nav-canon.cjs` | Reads canon → writes `src/data/navCanon.ts` |
| TypeScript output | `/root/arif-fazil.com/sites/arif-fazil.com/src/data/navCanon.ts` | Imported by `ArrowNavbar.tsx`, `AtlasGate.tsx`, etc. |
| Live SPA nav | `/root/arif-fazil.com/sites/arif-fazil.com/src/components/ArrowNavbar.tsx` | Renders `primaryNav` from navCanon |
| Static hubs | `/root/arif-fazil.com/sites/arif-fazil.com/public/<route>/index.html` | Each hand-rolled, but links must match `primaryNav` |

**NEVER hand-edit `navCanon.ts`** — it's a build artifact. Edit `navigation.json`,
regenerate, rebuild. The TS file carries a comment: "AUTO-GENERATED — DERIVED — never hand-edit."

## How to add a new organ

1. **Edit `navigation.json`** — add organ to `primary_links.items` if it deserves human
   visibility, else to `secondary_links` (footer) or `machine_links` (agent-only).
2. **Set `mode: "spa"` if a React Router route exists**, else `"static"` if the page is a
   hand-rolled HTML shell in `public/<route>/index.html`.
3. **List keyboard shortcut** (one per top-nav item — `g <letter>`).
4. **Regenerate** `navCanon.ts` via `scripts/generate-nav-canon.cjs`.
5. **Update static hubs** — if the page lives under `public/<route>/`, manually update its
   inline nav list to match the new primaryNav order.
6. **Gate** — `bash scripts/verify-pages.sh` must still pass.

## The five-card contract (proven 2026-08-06)

After multiple revamp cycles, the hub `public/world/index.html` now has 4 cards instead
of an unstructured list:
1. **Words (civic + essays)** → hub links to all written/doctrinal content
2. **State of the World (live atlas)** → the D3 globe + GDELT/WorldBank pipeline
3. **Commodity dashboards** → oil, gas, gold, klci, usdmyr
4. **Politics (secondary)** → shadow PMs, NS election map

This pattern — **card-group by content type, not by URL prefix** — keeps the hub scannable
even as the surface underneath grows.

## Why this matters for agents

An agent hitting `/.well-known/agent.json` will see organ endpoints listed. An agent
hitting `/llms.txt` will see the 5 nav items as the top-level entry points. An agent
hitting `/world/page.json` will see the section's surfaces listed under the WORLD nav.

**The same map** appears in three layers:
1. Top nav (human)
2. llms.txt + page.json (machine)
3. .well-known/*.json (discovery)

If the maps diverge, agents navigate to wrong places. **Probe all three** when adding a
new surface.

## Organs vs pages: the cardinal rule

An **organ** is an autonomous computational unit (kernel, registry, treasury).
A **page** is a human-readable surface that consumes organ outputs.

Organs are agent-owned. Pages are human-owned.

The 5-item nav is the **page→organ pointer**. Each item points to the page that consumes
that organ's outputs. Organs themselves never appear in the nav — they're agent doors in
`machine_links`.

If you ever feel like adding an organ to the top nav, **stop**. The organ belongs in
`machine_links` or `secondary_links` instead.
