# typst-recipes — patterns for one-off consumption PDFs

typst 0.13.1 is the default engine for **single-topic one-shot PDFs** (an
anthropology brief, a topic dossier, a wisdom letter, a project map). It is
NOT the path for the AAA compose-verify-publish pipeline — that stays on
manifest-driven composition. This file collects the typst-specific patterns
and pitfalls that come up repeatedly when a real agent hand-writes a .typ
file for Arif.

## 0. The decision rule

Use typst when the deliverable is a one-shot consumption PDF that an agent
writes top-to-bottom in a single session, **without** the manifest/envelope/
sealing choreography. Use the compose pipeline (`compose_artifact.py` +
build-manifest) when the PDF carries typed contracts, charts from live data,
or needs to be sealed to arifOS.

Default flags (memory): `typst compile x.typ out.pdf`, **NOT** pandoc.

## 1. Boilerplate that compiles

```typst
#set document(title: "...", author: "...")
#set page(paper: "a4", margin: (x: 2.2cm, y: 2.4cm))
#set text(font: ("Liberation Serif", "DejaVu Serif"), size: 10.5pt, lang: "en")
#set par(justify: true, leading: 0.62em, first-line-indent: 0pt)
#show heading.where(level: 1): it => block(width: 100%, above: 1.6em, below: 0.8em, text(20pt, weight: "bold", it.body))
```

Headers, callouts, tables — copy from a working PDF template, do not re-derive.

## 2. Emphasis gotcha — `_iGen*` is a syntax error

`_..._` opens and closes emphasis. An asterisk inside the emphasis closes it
early and the next `_` is unclosed delimiter. The error message points at the
asterisk, not the missing closer — it looks like a typo.

- Wrong: `Twenge's _iGen*:`
- Right: `Twenge's _iGen_ (2017):` or escape the asterisk: `Twenge's \_iGen\*:`

**Rule:** never put `*` (or unmatched delimiters) inside `_..._` emphasis.
Asterisk is typst bold (`*x*`), underscore is italic (`_x_`), they do not nest.

## 3. Function definitions — content block after named-default arg

This pattern bites every agent who tries to write a custom callout / block
helper. The compile error reads `missing argument: body` and points at the
content-block `[ ... ]` even though it is sitting right there.

```typst
// WRONG — `body` is positional after named-default `color`; the trailing
//         content block has no slot to bind to.
#let callout(title, body, color: rgb("#7a2e2e")) = block(...)[
  #text(9.5pt, fill: color, title)
  #text(10pt, body)
]
#callout(title: "X", color: rgb("#000"))[ ...body content... ]
//       ^ fails with "missing argument: body"
```

The fix: use a **sink** (`..rest`) and pull the content out:

```typst
// RIGHT — `..body` accepts any number of trailing content blocks; `.pos()`
//         extracts them, `.join()` combines them into a single content.
#let callout(title, color: rgb("#7a2e2e"), ..body) = block(...)[
  #text(9.5pt, fill: color, title)
  #v(-2pt)
  #text(10pt, body.pos().join())
]
```

**Rule:** when defining a helper that accepts BOTH named args AND a trailing
content block, the content block goes last as `..body` (sink) — not as a named
parameter with no default. Same class as the "grid/columns trailing content"
gotcha: comma-separated positional content after a named arg does not bind.

## 4. Common pitfalls (extend, do not re-list)

These are in MEMORY and verified to bite every session; the skill captures
HOW to recover, the WHY is in MEMORY:

- **tool-written files do NOT decode `\uXXXX`** — when the file is written
  by another tool with `\u2014` for em-dash etc., typst reads it as literal
  `\u2014`. Fix: `regex-replace` to actual characters BEFORE compile.
- **`#H(text)` unquoted fails** — `H` is a typst function but `#H(text)`
  without quotes tries to evaluate `text` as code. Wrap content in `"..."`
  or use `#H[text]` content-block form.
- **Typst bold is `*x*`**, not `**x**`. Markdown-style `**x**` produces two
  italics nested, with unclosed-delimiter errors.
- **Tables with named arg + positional cells** — `table(columns: (1fr, 1fr),
  stroke: ..., [a], [b])` works, but `table(columns: (1fr, 1fr), [a], [b],
  stroke: ...)` fails because `stroke` is named-after-positional.
- **Bare `<` in body text = "unclosed label"** — typst reads `<...>` as a
  label reference; `power bank <10,000mAh` fails with `unclosed label`
  pointing at the `<`. Write "bawah 10,000mAh" or escape. Rule: never put a
  bare `<` in text — reword or wrap in quotes/`#raw`.
- **Color + string concat fails** — `fill: color + "18"` errors with "cannot
  add color and string". For a translucent tint use `color.transparentize(88%)`
  or an explicit `rgb("#hex", alpha)`. Rule: alpha-tint with
  `.transparentize()`, never string concat.

## 5. Header / footer / numbering

```typst
#set page(
  paper: "a4",
  margin: (x: 2.2cm, y: 2.4cm),
  numbering: "1 / 1",
  header: align(right, text(8.5pt, fill: gray, [...stamp here...])),
)
```

`numbering: "1 / 1"` produces `1 / 1` total format — adjust to `"1"` or
`"1 of 1"` per context.

## 6. Verification (cheap)

typst has no native `pdf_verify.sh` — apply the G1+G3 gates manually:

```bash
ls -la out.pdf && file out.pdf | head -1          # G1: produced, non-zero
pdfinfo out.pdf | grep -E "Pages|Page size"        # G1: structure
pdftotext out.pdf - | grep -c "<sentinel>"         # G3: round-trip
```

For layout-heavy or map-embedding PDFs, G2 rasterize is NOT overkill — run
`pdftoppm -png -r 70 out.pdf /tmp/page` then `vision_analyze` each page. Proven
2026-10-17 (concert guide): it caught a long URL overflowing its line and
confirmed marker placement on embedded OSM maps. For pure-text one-shots the
BLUF on page 1 is the contract; save `pdfinfo` next to the deliverable either way.

## 7. Delivery contract

Render to `/root/.hermes/cache/scratch/<name>.pdf`, then attach with
`MEDIA:/absolute/path.pdf` so Hermes delivers as a Telegram document.
Never cite the scratch path to Arif — just attach.

## 8. Real map (staticmap + OpenStreetMap + OSRM)

When a consumption PDF needs a REAL geographic map (venue location, directions,
park-and-ride), do not draw schematic boxes — render real OSM tiles. Proven
end-to-end 2026-10-17 (concert guide: close-up walking route + overview).

```bash
pip install staticmap pillow   # staticmap draws OSM tile basemap + markers/lines
```

1. **Geocode** with Nominatim: `https://nominatim.openstreetmap.org/search?format=json&q=<place>`
   → returns `lat`/`lon`. Gotcha: use short precise names — "Bukit Jalil station"
   returns SP17; "Bukit Jalil LRT Station" returns EMPTY. Send a real
   `User-Agent` header (OSM usage policy).
2. **Walking route** with OSRM: `https://router.project-osrm.org/route/v1/foot/<lon1>,<lat1>;<lon2>,<lat2>?overview=full&geometries=geojson`
   → `routes[0].geometry.coordinates` is the polyline; `distance`/`duration`
   are real metres/seconds to quote in the guide.
3. **Render** with `staticmap.StaticMap(width, height, headers={"User-Agent": ...})`;
   add `CircleMarker((lon,lat), "#hex", radius)` + `Line(coords, "#hex", width)`;
   `img = m.render(zoom=16, center=(lon,lat))` (center omitted → auto-fit).
4. **Pixel coords** for labels, after render:
   `px = ((_lon_to_x(lon,zoom)-m.x_center)*256 + m.width/2, (_lat_to_y(lat,zoom)-m.y_center)*256 + m.height/2)`
   — import `_lon_to_x, _lat_to_y` from `staticmap.staticmap`. Draw labels with
   PIL: white rounded-rect bg + colored text, offset from the marker.
5. **Embed** in .typ via `#image("map.png", width: 100%)` + a caption crediting
   OpenStreetMap. Verify marker placement with the §6 rasterize step.

## 9. Audit stamping & same-day re-probe (consumption PDFs)

Consumption PDFs carrying LIVE logistics (venue, parking, transport, guests)
go stale within hours. Proven 2026-10-17 (concert guide): a sibling audit
confirmed the LRT facts but MISSED that parking was already full by 10am the
same morning (Kosmo, 17/10) — the guide's "drive early" advice was dead by
render time. Rules:

1. **Same-day re-probe before re-render.** A multi-day-old render is a claim,
   not current reality. Re-run the live sources (news, transit operator, venue)
   the same day the PDF ships.
2. **An auditor can miss what re-search finds.** When a sibling/audit returns
   claim-by-claim findings, verify each against a fresh live source — do not
   accept the audit blindly, and do not assume the audit is complete. The
   auditor missed the parking-full news; a fresh `exa` search caught it.
3. **Stamp trust classes INTO the artifact.** Add a final "Sumber & label
   kepercayaan" block with three labels: `SAH` (primary source + outlet + date),
   `Jangkaan` (unverified expectation — e.g. guest artists not confirmed by
   open source), `Anggaran` (numbers with no official source — e.g. parking lot
   counts). A reader should see what is verified vs estimated without asking.
4. **`#pagebreak()` before big blocks.** Maps and the source block start their
   own page — otherwise the section heading orphans at the bottom of the prior
   page with content pushed to the next. Verify with the §6 rasterize step.
5. **Map + caption must be ONE unbreakable block.** When an image and its
   caption split across pages, the caption reads as a broken sentence. In typst
   wrap `#image()` + caption together and `#pagebreak()` before the group (or
   use `block(breakable: false)`); in fpdf2 use keep-together logic. Wawabot
   hit the split live 2026-10-17 and fixed it by grouping map+caption before
   the break — same failure, two engines, one rule.

## 10. Prose-integrity + page-fill gates (cross-pollinated from wawabot kvm2)

Two scripts, verified working on typst output 2026-10-17:

```bash
# prose integrity — catches stray non-Latin tokens / fused words that lint + exit 0 miss
python3 scripts/audit_generated_text.py out.pdf --require "key fact" --require "another"
# per-page fill — numeric sparse-page detector (95/93/34/92/44 spread finds bad breaks)
python3 scripts/page_fill.py out.pdf
```

- **`audit_generated_text.py`** scans source + extracted text for non-Latin glyphs
  and junk tokens. Requires `pymupdf` (pip install pymupdf — one dep, both scripts).
  `--require` one string per load-bearing fact so a silently dropped section fails.
- **`page_fill.py`** prints each page's content-end % (excluding footer band) and
  flags pages under `--min-fill`. It caught p1=46% / p2=65% / p6=23% on a real
  guide. **Image pages will ALWAYS read sparse** — pymupdf `get_text("blocks")`
  counts text only, so a page that is 90% map image reports near-empty. Do NOT
  auto-fix a sparse flag on an image page; lower `--min-fill` for those, or
  eyeball the raster (§6) to confirm the image is actually there. Wawabot hit
  this live 2026-10-17 (fpdf2 rebuild flagged p1 as empty when it held a full map).
- **Calibrate `--junk` BEFORE trusting the gate — it is a mandatory step, not a tip.**
  `DEFAULT_JUNK` carries short signatures that false-flag inside legitimate
  machine identifiers (`add_font`, snake_case names like `unowned_output_rate`).
  Wawabot's own pitfall-22 rule fired AGAIN live on `d_` in `add_font`. Run the
  gate with `--junk` repeated for the REAL contamination signatures only, and
  disclose the override in the delivery note — keep the non-Latin floor and
  `--require` active (those catch real corruption and dropped sections).
- **Adaptation for typst:** typst + DejaVu render MORE glyphs than fpdf2, so
  `NONLATIN_FLOOR=0x2200` can flag deliberate emoji (⚠ U+26A0, ✅) that typst
  renders cleanly. Treat those as informational, not defects — the gate is
  calibrated for fpdf2's narrower font set. Keep the junk-token and `--require`
  checks (they are engine-agnostic); relax only the non-Latin floor for typst.

## 11. When to extend this file

Append a new section when a session hits a typst-specific error that took
more than one compile attempt to fix. Keep the entry at imperative form
("use `..body` sink"), one cause ("named-default arg before positional
content"), and one fix. Do not paste full error transcripts — distill the
rule. If the lesson generalises BEYOND typst (e.g. named-vs-positional
parameter binding), it belongs in MEMORY, not here.