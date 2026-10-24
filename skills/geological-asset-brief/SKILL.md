---
name: geological-asset-brief
description: "Use when forging a field brief or atlas with figures."
version: 1.0.0
owner: GEOX
risk_tier: low
floor_scope: [F2, F7, F9]
autonomy_tier: T1
license: DITEMPA BUKAN DIBERI
---

# Geological Asset Brief

One field, one contract stack, one set of figures, delivered as a document the sovereign can carry
into a meeting with an operator. The geology is usually the easy part — the failure modes are
invented numbers, figures that draw rock through a fault, and QA done at a scale where the reviewer
cannot read the labels.

## Companion skills (read these, do not restate them here)

- `geox-mcp-tool-invocation` — MCP session protocol, schema quirks, evidence envelope.
- `geological-figure-production` — matplotlib recipes, weasyprint multi-page assembly, vision-QA history.
- `geox-production-cockpit` — intent routing, corpus conflict map, primary-source rule for awards.

The three above live in read-only skill mesh; this skill covers what they do not — hand-authored SVG
inside a single-file HTML deliverable, and evidence honesty when the data lane is empty.

## 1 — Establish what evidence you have, before writing a word

1. **Probe the organ's registry first.** `geox_surface_status {"mode":"registry"}` returns version,
   build sha and the canonical tool list. A tool absent from that list is genuinely absent; one absent
   only from your own memory is not a capability gap.
2. **Resolve basin slugs, not display names.** `geox_basin` takes the directory slug (`malay_basin`),
   not the human name (`Malay`) — that returns `ok:false, "Basin data not found for: Malay"`. The
   lenient name path is `geox_workspace`.
3. **Check the well and source lanes.** `geox_well` on a real well with no ingested LAS returns
   `isError:true`, `status:NOT_FOUND`, `claim_state:HOLD`; `geox_list_registered_sources` returning
   `n_sources: 0` is also a HOLD on a healthy surface. Both mean *empty lane*, not outage.
4. **Name the artefact class inside the document.** If any lane is empty, the deliverable is a
   **literature synthesis** and must say so in a caption or footer where a reader sees it — not only in
   the tool log. Never let a reader infer an Earth witness that does not exist.
5. **Treat catalog tags as seeds.** Play/formation tags from the organ's knowledge graph come from a
   hand-maintained table, not well data. Cross-check against field literature and report a wrong tag as
   a corpus defect, naming the literature that contradicts it.

## 2 — Separate the contracts before describing the field

Fields routinely sit under more than one instrument with different end dates — an oil PSC and a gas PSC
over the same asset. Write the split before the geology, or every later sentence is ambiguous. Mine the
operator's own releases and technical papers for: the field list per instrument (news coverage drops
it, the release has it), term dates and minimum commitments, which instrument carries the hub and the
compression, and the operatorship transfer trail with effective dates.

Where a name and a signature date disagree (a contract named for one year, awarded in another), state
both readings rather than picking one. A register keyed on name and one keyed on date will disagree,
and neither is wrong.

## 3 — Figure geometry: generate it, never hand-place it

Author figures as programmatic SVG emitted by a Python script into the HTML. Hand-written `<path>`
coordinates fail in ways code review cannot see.

- **One polygon per fault block, never one path across the canvas.** A single `<path>` spanning the
  width draws strata straight through the fault and reads as unfaulted rock — the most damaging error
  in a structural section. Derive each block's horizons from one shared function and emit each block's
  band separately, so the same bed appears at two elevations across the fault.

```python
BLOCKS = [  # (x0, x1, cx, half_w, vert_shift, dip)
    ( 60, 300, 182, 122, 52, 11),   # west, downthrown
    (300, 700, 500, 200,  0, 13),   # crest
    (700, 940, 820, 120, 26,  9),   # east, gently downthrown
]
def y(base, xs, cx, hw, shift, dip):
    return [base + shift + dip * ((x - cx) / hw) ** 2 for x in xs]
# band(upper, lower) -> one <polygon> per block, top polyline forward + bottom reversed
```

- **Draw order:** water column → deepest band → shallower bands → horizon lines → faults last, thick.
  Let the fault's x drift a few units with depth; a perfectly vertical bar reads as a tie-line.
- **Water column per block**, filled from the seabed polyline up to the frame top. One rectangle leaves
  "water" buried under the downthrown block.
- **Throw annotation brackets the same horizon on both sides of the fault** — two stubs at the two
  elevations plus a connector. A bracket on the wrong bed is a wrong number presented as measured.
- **Relative depth when there is no datum.** No checkshot, velocity model, LAS or seismic horizon →
  relative vertical axis, caption says so, no absolute depth printed. An invented depth axis is
  fabrication, not a convenience.
- **Schematic and indicative are load-bearing words.** Unsureveyed platform positions, perforations and
  interval spacing belong in the caption as *indicative, not to scale*; keep stratigraphic order and the
  reservoir count literally correct even when spacing is not.
- **Two vintages of one facility are not a contradiction** — quote both with dates and say neither is
  "the" capacity.
- **Bars share one scale constant** computed from the axis (`unit = (base_y - top_y) / axis_max`); a
  per-bar eyeballed multiplier produces a chart contradicting its own ticks.

## 4 — Verify at native scale, or the review is fiction

- **Never QA a multi-figure page from one full-page screenshot.** The browser scales a 1000-unit
  viewBox to page width, text drops below the vision model's legibility, and it begins to *invent*:
  duplicated labels, wrong coordinates, a `29` read as `23`, collisions that are not there — while
  missing real ones.
- **Extract each `<svg>` into its own page at native width, carrying the parent's CSS classes**, and
  screenshot that. Inline SVG does not inherit the outer stylesheet; without the class definitions every
  label renders at 16 px default and you review a layout you did not ship.

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1010,$((H+20)) \
  --screenshot=chk$i.png --virtual-time-budget=4000 chk$i.html
```

- **Confirm any "defect" seen in a downscaled view before acting on it** — crop the region at 2× and
  re-read. Editing a figure because a downscaled read hallucinated a collision introduces real ones.
- **Full-page screenshots truncate.** Set window height well past expected content, find where content
  ends by scanning rows against the background colour, and confirm the footer is present before
  declaring the page complete.

## 5 — Values that are never invented

When the public record stops, the table says so. Each of these gets `not published` in a distinct style
plus a line telling the reader to request the deck — never a plausible number: reservoir depth/TVDss ·
gross and net thickness · porosity · permeability · net-to-pay · fluid contacts (OWC/GWC) · per-interval
OOIP · recovery factor per reservoir · any annual production series between two published points.

- **Label derived arithmetic as derived**, show both inputs beside it (remaining ÷ annual → years), and
  say what it ignores: EOR upside, blowdown, cost, and the fact that a mature hub keeps earning on gas
  after the oil rate is trivial.
- **A gap between two published points is missing data, not a trend.** Draw it as a gap.
- **Flag secondary sources that disagree with primaries** (ownership split, field count) rather than
  adopting either silently — especially when that same secondary source is your only reserves number.
- **Do not sign the sovereign's name to anything** and do not put words in his mouth.
- **Counts that moved over field life are date-stamped answers**, not contradictions: print both with
  their years.

## 6 — Delivery

- **Single file, zero external references** — inline CSS, inline SVG, no CDN, no webfonts; must open
  offline and print to A4. Grep for `src="http` / `href="http` before sending.
- **HTML for review, PDF for the meeting.** Front matter (title, standfirst, ~six metrics, bottom line in
  a box) → figure pages → data register and claim ledger.
- **Typst resolves `#image()` relative to the `.typ` file**; an absolute path fails with
  `file not found (searched at <dir>/root/...)`. Put the figure beside the source, use a bare filename.
- Deliver `MEDIA:/absolute/path` with one short paragraph of what is inside — no infrastructure
  commentary, no menu of options.

## Pitfalls

- **Rendering "successfully" is not rendering legibly.** `typst compile` and headless Chrome both exit 0
  on clipped columns and overlapping annotations. Only the native-scale review catches it.
- **A fix applied at the wrong scale makes it worse** — re-check the same region after every geometry
  edit, or the collision just moves.
- **`chromium-browser` on this host is a snap stub that exits non-zero with an install hint.** Use
  `google-chrome` for headless screenshots.
- **Text over a patterned fill disappears** — give edge labels a stroke halo
  (`paint-order: stroke; stroke: <paper colour>`) instead of moving them into the data.
- **Metrics rows orphan single words** — six big numbers get one-two-word captions; keep each under
  ~28 characters or widen the row.
- **Contract timelines need a zoomed inset for anything inside two years**; operatorship changes knot
  into mush at 60-year scale.
