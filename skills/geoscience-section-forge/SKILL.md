---
name: geoscience-section-forge
id: geoscience-section-forge
risk_tier: low
description: "Forge or audit a geological cross-section."
version: 1.0.0
tags: [geology, cross-section, stratigraphy, sabah, falsification]
---

# Geoscience section forge

## When to Use

Building, redrawing, or auditing a regional geological cross-section (NW Borneo / Sabah, Malay Basin, or any basin), or answering "which model is closest to reality?".

## Non-negotiables

1. **Framework before formations.** Load the basin's tectonic framework first — phase model, unconformity set, structural style, crustal architecture. Only then choose lithologies. Starting from a named-formation list produces a passive-margin layer cake; on an active margin that is wrong.
   This is the most expensive error in this class: it renders cleanly, looks authoritative, and a domain expert rejects it in one glance.
2. **Every model geometrically distinct, or declared an alias.** Hash the crustal architecture per model. If two share it, say so on the card ("shares crust with A, C — differs only in the added body"). Undeclared duplication makes any compare UI theatre.
3. **Every model carries a kill criterion with a number.** "D could be wrong" is not a criterion. "D predicts an 8–12 km Moho low over 40–60 km width; a flat Moho kills it" is.
4. **Wells come from the registry.** Placeholder wells carry no outcome and are omitted, not assigned pay.
5. **Declare what is not drawn.** A model with no published along-section geometry goes in a "registered but not drawn" list. Never paint fake geometry to fill a menu.
6. **Disclose vertical exaggeration and datum** (below seabed vs below sea level) on the figure itself.
7. **Tier every element.** L0 public measured, L1 derived by calculation, L2 interpretation. Every polygon is L2.

## Procedure

1. Read the basin profile from the source of truth (GEOX `geox_basin`, the basin yaml, the published synthesis). Extract tectonic phases, unconformity names + ages, structural style, crustal architecture.
2. **Resolve age conflicts explicitly.** The same surface name carries different ages in different domains and calibrations. Store a range with provenance per domain; never collapse three sources into one number, and never label source A's numbers as source B's.
3. **Get real station coordinates** and compute geodesic chainage (WGS84). Every unit's position is then a number on that chainage, not an eyeball. A unit plotted in the wrong structural domain is P0.
4. Build surfaces as functions of chainage, not stacked constant thicknesses. Pinch-outs, underthrust tongues and basement highs are what make a section readable.
5. **Compute a physics check that can fail.** Isostasy is the cheapest:
   `e = ((ρm − ρc) / ρm) · (t − t0)`, with `ρc 2800`, `ρm 3300`, `t0 30 km`.
   A summit Airy cannot support on the local crust is direct evidence that something other than crustal thickness holds it up. Always print the density sensitivity range — required crust moves ~15 km across plausible ρc/ρm.
6. Render, then **read the render back**. Check: colliding labels, white-on-white, a label naming a different model than the panel shows, layers bleeding outside axes, unreadable at 390 px.
7. Publish and verify — see Publishing below.

## Pitfalls

- **Ophiolite is a sliver, not regional basement.** In NW Borneo, drawing ophiolite as the basement across the transect inverts the architecture.
- **The mobile-shale wedge is a body, not a colour.** Give it a tapered envelope (not a hard vertical step), a detachment at the published depth, and an overpressure argument.
- **Slab and drip live at different depths.** A slab remnant at 250–400 km cannot be drawn as a 45–60 km body. Drawing it shallow creates a model no dataset supports and that dies on the first reviewer question.
- **Do not delete a rejected model.** Keep it as FALSIFIED with the dataset that killed it, so the rejection stays auditable.
- **Do not prescribe the user's method.** They are the geologist. Produce the computed check — isostasy numbers, pressure thresholds, geometry hash, internal contradiction — and state it. Do not tell them what to date or what to shoot.

## Publishing a section (arif-fazil.com)

- Source: `/root/arif-fazil.com/sites/arif-fazil.com/public/...`; mirror into `dist/`, then the live root.
- **Caddy root pitfall:** the `/earth*` handle serves `root * /var/www/html`, *not* `/var/www/html/arif`. Copying to `/var/www/html/arif/earth/...` leaves the page 404 while the file "exists". Before debugging a 404, read the vhost: `grep -n -A8 'handle /earth' /etc/caddy/vhosts/arif-fazil.com.conf`.
- Copy, `chown www-data:www-data`, `chmod 644` files / `755` dirs.
- Gate: `make verify-pages` (or `./scripts/verify-pages.sh`) must PASS. Never run `make deploy` — it reloads Caddy.
- Verify origin then edge: `curl -sk --resolve arif-fazil.com:443:127.0.0.1 https://...` then the public URL.
- **Commit hygiene:** the tree is often dirty from other agents. `git add <file>` sweeps their uncommitted edits into your commit under your message. Before committing a file you did not originate, `git diff --stat` it and confirm every hunk is yours; otherwise note the co-edits in the message.
- Headless visual check: `google-chrome --headless=new --screenshot --window-size=W,H --virtual-time-budget=3000 file://...`, then crop and read the PNG. Wire `window.onerror` to a visible banner so a screenshot exposes JS failures.

## NW Sabah / NW Borneo framework (the domain this user works in)

- **Plate story:** PSCS subduction → Dangerous Grounds / Reed Bank collision (Hall 2013). *Not* Eurasia–Philippine Sea.
- **Crust:** DG continental crust underthrusts SE beneath Sabah. ~60 km under the Crocker Range, ~24 km central Sabah. No crustal suture and no relict oceanic crust beneath the Sabah Trough (Vijayan, Foss & Stagg 2013). Moho 32.8–52.5 km; the old flat "~30 km" is superseded.
- **NSPW mobile shale:** source shale ~2–4 km sub-sea, ~1 km thick; basal detachment ~5–8.7 km below seabed, dipping landward ~1.9° (ADS); mud canopy ~1900 km², ~50 volcanoes, mini-basins loaded up to 4 km. Coalesced at UIU ~10.5 Ma.
- **Overpressure to mobilise shale:** ~+24 MPa above hydrostatic at 3 km, ~+32 MPa at 4 km (0.8·Sv leak-off). Compaction alone cannot; gas generation plus rapid loading can.
- **Kinabalu:** granite U–Pb 7.85–7.22 Ma, sheeted laccolith-like, ~170 km³ over ~0.6 Myr, emplaced 7–12 km, exhumed ~7 mm/yr. Airy needs 57 km (range 51–68) to hold 4.095 km — if local crust is thinner, support is dynamic, and the granite is a symptom rather than the cause.
- **Telupid ophiolite:** 5.62 N 117.15 E → 567.5 km on A–A′; east of Kinabalu in the Sandakan Division, **not** Crocker Range basement. Age contested: Mesozoic (Tongkul 1997) vs Miocene zircons 9.2–10.5 Ma (Tsikouras 2021). The Ranau peridotites near Kinabalu are a separate body.
- **Ages — treat as families:** BMU/TCU 23–24 Ma (Lunt 2022 c.24; subduction ends ~21 — two different events, not a conflict). DRU 13.5–12.5 (Morley 2023) / 12–13 (Lunt 2022) / ~15.5 (spreading-end model) / 14.2–14.91 on some picks. SRU 8.5–9.4; top NN9 = 9.53 Ma in GTS2012, so "Top NN9 = 8.5" is internally inconsistent. UIU 10.5.
- **Heat is not proof of magma.** Local gradient with normal surface flux = advection along faults and pipes; broad anomaly with high flux plus a magnetic body = internal heat source. Test with BHT and heat-flow maps before invoking magmatism.
