# Shared Preflight — witness-biography-pdf + forensik-institutional-audit

ONE script, both skills reference it. Location:
`/root/AAA/skills/witness-biography-pdf/scripts/typst_preflight.py`

## Run before every `typst compile`

```bash
python3 /root/AAA/skills/witness-biography-pdf/scripts/typst_preflight.py subject.typ
# exit 0 = safe to compile | exit 1 = fix listed defects first
```

## What it catches (all verified against real failures)

| Check | Failure mode it prevents |
|---|---|
| BRACKET-MISMATCH | unclosed `[...]` inside #block/#figure |
| ODD-ASTERISK | `*word` unbalanced emphasis -> unclosed delimiter |
| TRIPLE-ASTERISK | `***` profanity/onomatopoeia from book quotes |
| MARKDOWN-TABLE | pipe rows render as LITERAL text, not a table |
| NEGATIVE-PAREN-DEPTH / UNCLOSED-PAREN | #block( missing its closing ) |
| MISSING-IMAGE | image() referencing a file not relative to the .typ |
| ORPHAN-HEADING | heading immediately before #pagebreak = stranded header page |

## Verified

- Planted-defect file (6 defects) -> all caught, exit 1.
- Three real production .typ (Hassabis/Musk/Altman) -> clean, exit 0.
- Balanced `*Bold intro* rest` at line start is LEGAL and not flagged (refined after false-positive).

## Not caught (compile-time only)

- Silent font substitution (DejaVu fallback). Check rendered output visually.
- Overflow/clipped cells. Only visible in rasterized page inspection.
- Wrong content. Preflight is syntax+structure, never semantic.

## Post-compile gate (unchanged, from typst-pdf-report)

```bash
head -c 8 out.pdf                                    # %PDF-
pdfinfo out.pdf | grep -E '^Pages|^File size'
pdftotext out.pdf - | wc -w                          # near-empty layer = failed render
pdftotext out.pdf - | grep -cE "/(root|home|usr|tmp|opt)/"   # must be 0
pdftoppm -png -r 55 out.pdf pg                       # then per-page ink check
```
