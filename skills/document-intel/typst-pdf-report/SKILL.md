---
name: typst-pdf-report
description: Build a Typst PDF report for Arif. Escape $@# then verify.
tags: [pdf, typst, report, artifact, delivery]
metadata:
  hermes:
    tags: [pdf, typst, report, artifact, delivery]
    related_skills: [pdf-report-generation, artifact-emission-pipeline]
---

# Typst PDF Report

Arif's standing delivery preference: articles/reading material arrive as a **PDF in chat** (via Typst), not as a `/tmp` path and not as prose. Typst (`typst`, at `~/.local/bin/typst`) compiles a markdown-like `.typ` source to PDF fast with zero HTML/CSS. Use it for reports, dossiers, and evidence packs.

## Procedure

1. Write the `.typ` source with `#set page(paper: "a4", margin: ...)` and `#set text(font: "DejaVu Sans", size: 10.5pt)`. Use `#align(center)[...]` for titles, `== Heading` for sections, `- item` for bullets, `#figure(image("x.jpg", width: 40%), caption: [...])` for images, `#grid(columns: (1fr, 1fr), gutter: 8pt)[...]` for side-by-side.
2. **Escape every special char that Typst treats as markup** (see Pitfalls) BEFORE compiling.
3. Copy images into the same directory as the `.typ` and reference them by relative filename.
4. Compile: `typst compile report.typ report.pdf`.
5. Verify — never ship an unverified PDF:
   - `pdftotext report.pdf - | head -40` (then the tail) to confirm text renders (catches garbled/cut content). **This is the text check.** Judge wording, names and numbers from this extraction only — a vision pass over the raster re-describes the page in its own words and will substitute names and paraphrase bullets while reporting the page clean.
   - `pdftoppm -png -r 50 -f 1 -l 1 report.pdf p && ls p*.png` to rasterize page 1, then `vision_analyze` the PNG for LAYOUT only: overlap, cut-off, stranded near-empty page. Rasterize first — vision_analyze cannot read a PDF directly.
6. Deliver: emit `MEDIA:/abs/path/report.pdf` in the reply.

## Pitfalls (each cost a compile failure this class of task)

- **`$` starts math mode** — every dollar amount (`$300`, `$3,000`) breaks compilation with "unclosed delimiter". Escape as `\$`. Do a global `text.replace('$', '\\$')` before compiling.
- **`@` starts a label reference** — `@luntz_666` raises "label `<...>` does not exist in the document". Escape as `\@` (global replace `'@' -> '\\@'`).
- **`#` starts a variable/function call** — `#IFBB` raises "unknown variable". Escape as `\#`.
- **Image paths must be relative** to the `.typ` file's directory — Typst searches relative to the source file, and an absolute `/root/...` path silently resolves against the compile cwd. Copy images next to the source (`cp src ev_a.jpg`) and reference `ev_a.jpg`.
- **`$` and `@` and `#` all need escaping in the same file** — a report with prices AND handles AND hashtags needs all three replaces. Do them in one `execute_code` pass, not piecemeal.
- **Vertical spacing is `#v(...)`, not `#vspacel(...)`** — an unknown function aborts the compile at that exact line and the caret points mid-document; fix the function name rather than rewriting the document around the error.
- **Cap the body BEFORE you write the source.** Long prose drafted straight into a `.typ` degenerates into repeating filler, and it compiles happily into a garbage document. Draft the body as a list of short lines, assert a word budget before writing the file, and when the assert fires: discard and redraft short — trimming a degenerate draft still ships its texture.
- **Write the source in one call, not a shell pipeline.** `printf`/`sed` chains against a file full of `\n`, `#` and quotes produce escaping errors that READ like Typst errors. Use `write_file` (or one `printf '%s\n'`), and only chase compile errors once the source reads correctly.

## Why this beats the alternatives

- HTML→PDF (weasyprint/chromium) is heavier and needs CSS for layout; Typst gives a clean print layout from a single lightweight source file.
- For multi-image "evidence packs", Typst `#figure` + `#grid` produce a tight report where each image carries a numbered caption — the layout a dossier wants.
