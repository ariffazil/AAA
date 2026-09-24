# Slide-Deck PDFs: vision-fallback for `pdftotext`-empty extraction

## Trigger

A PDF arrives with `pdfinfo` showing `Producer: pdf-lib` (Hopding) OR
`pdftotext input.pdf - | wc -w` returns <200 chars across 3+ pages.
That signature = digital-born slide deck where text is rendered as
background imagery, not extracted as text.

## What breaks if you skip this

`pdftotext` returns the title slide's heading text only. The body of
each slide — kursus names, sinopsis, HPK, kredit, syarat — all live
inside PNG-composited slide imagery. Naive text extraction reports
"nothing here." Reasoning downstream hallucinates the rest.

## Pattern that worked

```bash
# 1. Probe char-count
pdftotext input.pdf - | wc -w
# → <200 on multi-page PDF = slide deck

# 2. Render pages to PNG
pdftoppm -r 80 input.pdf /tmp/slides -png
# → /tmp/slides-1.png, -2.png, ...

# 3. vision_analyze per page
# Ask for verbatim extraction — bullets, course codes, credits, years,
# prerequisites. Force "extract ALL text, do not paraphrase".
```

## Specific dimensions to force-extract on briefing-style slides

- **Kursus code** (e.g. SKPD2113)
- **Kredit** (often hidden, sometimes only inferred from last digit)
- **Tahun / Semester / Sesi**
- **Sinopsis** (full prose, not summary)
- **HPK / Hasil Pembelajaran** (numbered list)
- **Syarat** (often on a "Perincian Trek" or policy slide)
- **Nama trek / laluan** (e.g. Akademik / Kesukarelawanan / Keusahawanan)

## Cost

- `pdftoppm -r 80` → 80–900KB per page PNG, negligible CPU
- `vision_analyze` → 1 call per page, ~3–8s each

## Pitfalls

Don't fall back to Tesseract on rendered slide PNGs. Tesseract on
designed infographic layouts (color blocks, side-to-side columns,
icon grids) scrambles reading order. vision_analyze preserves layout
because it reads the slide as a human would.

Don't trust a single-page probe — slide decks often have a single
text-heavy cover slide that masks empty body slides. Probe body pages
directly.

Don't paste slide-deck content verbatim into a downstream PDF report
without re-asserting which source each fact came from. Cross-check
between vision_analyze output and any text-extractable page before
claiming a course code, kredit, or policy rule is correct — the
patch that fixes version 1 of a report based on a second source is
the same pattern that catches hallucinated course codes.
