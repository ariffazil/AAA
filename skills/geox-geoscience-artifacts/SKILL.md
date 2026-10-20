---
name: geox-geoscience-artifacts
version: 1.0.0
description: "Use when forging or auditing a geological cross-section."
---

# GEOX — Geoscience Artifacts

Three connected jobs on one class of object: forge a cross-section, audit someone else's, publish the interactive page.

## Floors that apply to every geological artifact

1. **Every polygon is L2.** Publish the tier ladder in the figure and the footer: L0 = public measured data (station coordinates, radiometric ages, published well results), L1 = derived by calculation from L0, L2 = interpretation. A polygon is only a pick if you drew it from a pick.
2. **Wells come from a registry, never from prose.** A placeholder well has no outcome — omit it rather than assign one. Repeating a real well's status is fine only with its evidence tier (Tepat-1 = oil & gas discovery, 2018, operator release).
3. **Never emit a governance state you cannot produce an event for.** Ratified / sealed / approved belong to the human. A machine returns CANDIDATE, QUALIFIED, or HOLD.
4. **Keep competing models as a family.** Each gets a claim, evidence-for, evidence-against, and exactly one kill criterion phrased as an observation. Never average conflicting ages — render parallel models, or report a range with the source named.
5. **Label every number with the source it actually came from.** If the ages came off a reference geoseismic section, the caption says so. Attaching a different chart's name to them is provenance falsification, not a typo.

## Forging a section — order of work

1. **Probe canon before drawing.** `geox_basin(basin_name="Sabah Basin")`, then read `geox://resources/ontology/sabah_basin_strat.yaml` and `geox://earth-system/sabah-correlation`. Let the tectonic framework pick the geometry — see `references/sabah-basin-canon.md`.
2. **Choose the structural model first, geometry second.** Write down which model you are drawing and what the Moho does. If you cannot state how two models differ geometrically, the figure is decoration.
3. **Draw domains, not a stack.** The common failure is stacking formation thicknesses top-to-bottom over one regional basement. That reads as a passive-margin layer-cake even when every label is correct for the basin. NW Sabah is an underthrust margin with a mobile-shale wedge over an accretionary prism — not a layered passive margin.
4. **Render, screenshot, crop, look, fix.** Repeat until labels are legible (see Render QA).
5. **State the limits inside the artifact**: not fitted to seismic, no inversion, no restoration, not all possible models, geometry schematic.

## Pitfall — `geox_model(mode="geological_generate")` is a layer-cake

It takes `layers[]` of `{formation, lithology, thickness_m}` plus `geological_params` and renders a deterministic stacked column with a vertical fault. Below the fault the layer offsets do not stay constant, and the fault is drawn vertical whatever dip you pass. Use it for a quick stratigraphic column; never present its output as a basin cross-section. Inspect the produced PNG before shipping — the labels come back tidy, which makes the wrong geology easy to miss.

## Pitfall — GEOX renders land in the service's private tmp

`geox_model` returns `/tmp/geox/<file>.png` from the server process's view. The service runs with PrivateTmp, so on the host the file is at:

```
/tmp/systemd-private-<hash>-geox-mcp.service-*/tmp/geox/<file>.png
```

Glob that prefix and copy into your scratch dir before attaching. A whole-filesystem `find /` for the filename times out — do not use it.

## Auditing a geological artifact

Work in this order and report claim-by-claim: **BETUL / SALAH / SEPARUH** plus the source that settles it. Full pattern list in `references/artifact-audit-patterns.md`.

1. **Ground each number** against canonical, not against plausibility.
2. **Test self-consistency** — a document that contradicts its own evidence log is wrong no matter how good the prose is.
3. **Test attribution** — list every number, name where it actually came from, compare with the caption.
4. **Test well outcomes** against the registry.
5. **Test geography** — convert real coordinates to chainage and check the unit sits in the corridor it claims.
6. **Separate the failure classes.** A fabricated well outcome, a mis-calibrated marker and a wrong tectonic framing need three different fixes; say which is which.

## Render QA loop

```bash
google-chrome --headless=new --disable-gpu --no-sandbox \
  --virtual-time-budget=3000 --window-size=1600,1600 \
  --screenshot=/abs/out.png "file:///abs/page.html#C"
```

Then crop the panel with PIL and send the crop to `vision_analyze` with a defect-only prompt ("list problems only"). Full-size screenshots hide 9px collisions.

- Give labels a background box, or place them over dark fill. White text on a pale formation is unreadable at print size.
- Put the well label on the opposite side from the horizon labels — that is the most common collision.
- Taper wedge fills with an envelope function; a hard vertical step reads as a rendering bug.
- `vision_analyze` will confidently describe content that is not there. Crop first, ask narrow questions, trust it only for legibility.
- Render each model in the family (`#A`, `#F`, `#R`) — a shared drawing path breaks on the outliers, not on the default.

## Publishing to arif-fazil.com

Site-wide deploy rules live in `FORGE-agentic-web-builder` and the repo `AGENTS.md`. What is specific to an Earth page:

- Source `public/earth/<slug>/index.html` under `/root/arif-fazil.com/sites/arif-fazil.com`; mirror to `dist/earth/<slug>/index.html`.
- **Live root for `/earth*` is `/var/www/html/earth`, not `/var/www/html/arif/earth`.** The Caddy vhost block `handle /earth*` sets `root * /var/www/html`. Writing to the `/arif/` tree returns 404 at origin; the trees are separate inodes. Grep the handler for `root *` before copying.
- `chown www-data:www-data`; `chmod 755` dir, `644` file.
- Verify at origin before the edge: `curl -sk --resolve arif-fazil.com:443:127.0.0.1 https://arif-fazil.com/<path>`. Plain `http://127.0.0.1/...` returns 308 because Caddy upgrades to https.
- Gate: `cd /root/arif-fazil.com && make verify-pages`. Never run `make deploy` for a static page under an existing handle — it reloads Caddy.
- Self-contained is the requirement: no external JS/CSS, embed basemaps as base64 (≈72% JPEG quality keeps a page in the low hundreds of KB) so the page survives a sandboxed iframe and offline archive.

## References

- `references/sabah-basin-canon.md` — canonical ages, wells, crustal evidence, model identifiers and their discriminating tests.
- `references/geox-mcp-surfaces.md` — tool modes, resource URIs, response envelope, known surface defects.
- `references/artifact-audit-patterns.md` — the failure patterns to hunt in AI-generated geology.
