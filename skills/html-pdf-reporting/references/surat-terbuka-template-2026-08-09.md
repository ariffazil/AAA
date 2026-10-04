# Surat Terbuka (Open Letter) PDF Template

> Forged: 2026-08-09. Source: `/tmp/surat-terbuka-v2.html` → `Surat_Terbuka_Petronas_20260809.pdf`

## Pattern

Unlike reports (data-heavy, charts), open letters are TEXT-HEAVY documents aimed at specific audiences (MPs, public). The visual design must:

1. **Cover page** — dark navy gradient + gold accents + document title + seal
2. **Letter header** — right-aligned, formal addressing
3. **Section headings** — gold underline, sans-serif font
4. **KPI cards** — for key numbers (red for negative, gold for neutral)
5. **Pull quotes** — grey box + gold left border + italic
6. **Callout boxes** — red (urgent demands) or gold (requests)
7. **Tables** — navy header, zebra striping, red last column for implications
8. **Signature block** — right-aligned with line

## CSS key differences from report template

```css
/* Cover uses flex-end alignment (text at bottom) */
.cover { display: flex; flex-direction: column; justify-content: flex-end; }

/* Pull quotes for strong lines */
.pullquote { background: #f4f4f4; border-left: 4px solid #c9a227; padding: 14px 18px; }

/* Callout boxes for demands */
.callout-red { background: #fdf2f2; border-left: 4px solid #c0392b; }
.callout-gold { background: #fef9e7; border-left: 4px solid #c9a227; }

/* KPI cards for key metrics */
.kpi-card { border-top: 3px solid #c0392b; text-align: center; }
.kpi-card .num { font-size: 18pt; font-weight: bold; color: #c0392b; }
```

## Font stack

System fonts only (WeasyPrint): `'Liberation Serif', 'DejaVu Serif', Georgia, serif` for body, `'DejaVu Sans', 'Liberation Sans', Arial, sans-serif` for headings/KPI.

## Rendering

```bash
weasyprint surat-terbuka.html output.pdf
# Or via Python:
python3 -c "from weasyprint import HTML; HTML('surat.html').write_pdf('output.pdf')"
```

## Pitfalls

- WeasyPrint does NOT execute JavaScript — all charts must be CSS or matplotlib base64
- `@page :first` overrides margins for cover page (no header/footer)
- `page-break-inside: avoid` on callout boxes and tables
- Malay text with special characters: ensure `<meta charset="UTF-8">`
