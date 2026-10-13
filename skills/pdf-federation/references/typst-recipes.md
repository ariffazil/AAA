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

For one-shot consumption PDFs G2 rasterize is usually overkill — the BLUF
on page 1 is the contract. Save verification pdfinfo next to the deliverable.

## 7. Delivery contract

Render to `/root/.hermes/cache/scratch/<name>.pdf`, then attach with
`MEDIA:/absolute/path.pdf` so Hermes delivers as a Telegram document.
Never cite the scratch path to Arif — just attach.

## 8. When to extend this file

Append a new section when a session hits a typst-specific error that took
more than one compile attempt to fix. Keep the entry at imperative form
("use `..body` sink"), one cause ("named-default arg before positional
content"), and one fix. Do not paste full error transcripts — distill the
rule. If the lesson generalises BEYOND typst (e.g. named-vs-positional
parameter binding), it belongs in MEMORY, not here.