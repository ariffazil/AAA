# Light-Theme Protocol / Educational PDF Pattern

**Proven:** 2026-08-13 (peptide injection protocol guide for Arif)

## When to use

Non-federation deliverables: health protocols, personal reference guides, instructional how-tos, equipment checklists, step-by-step procedures. These are NOT WEALTH/333 reports — they use a different visual language.

## Key differences from federation reports

| Aspect | Federation Report (default) | Protocol / Educational PDF |
|--------|---------------------------|---------------------------|
| Theme | Dark navy + gold accent | Clean white, minimal colour |
| Typography | Helvetica/Inter, bold headers | Segoe UI / system sans-serif, soft headers |
| Visual elements | KPI hero rows, matplotlib charts | Inline AI-generated images, step-numbered flows, checklists |
| Tables | Appendix only | Inline (comparison tables, equipment specs) |
| Callout boxes | Verdict/epistemic boxes | Warning (yellow), danger (red), info (blue), tip (green) |
| Cover | Dark gradient, gold stamp | Simple title + icon + one-line subtitle |
| Charts | matplotlib PNGs | Rare — mostly images + tables + step flows |

## HTML structure

```html
<!DOCTYPE html>
<html><head><style>
  @page { size: A4; margin: 2cm; }
  body { font-family: 'Segoe UI', Arial, sans-serif; color: #1a1a2e; font-size: 11pt; }
  .cover { text-align: center; padding: 60px 30px; page-break-after: always; }
  .cover h1 { font-size: 28pt; color: #0f3460; }
  .step { display: flex; align-items: flex-start; margin: 10px 0; padding: 10px 14px;
          background: #f8f9fa; border-radius: 6px; border-left: 4px solid #0f3460; }
  .step-num { background: #0f3460; color: #fff; width: 28px; height: 28px;
              border-radius: 50%; display: flex; align-items: center;
              justify-content: center; font-weight: 700; flex-shrink: 0; margin-right: 12px; }
  .warning-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px 16px;
                 border-radius: 4px; }
  .danger-box  { background: #f8d7da; border-left: 4px solid #dc3545; padding: 12px 16px;
                 border-radius: 4px; }
  .info-box    { background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 12px 16px;
                 border-radius: 4px; }
  .tip-box     { background: #d4edda; border-left: 4px solid #28a745; padding: 12px 16px;
                 border-radius: 4px; }
  .checklist { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px;
               padding: 16px 20px; columns: 2; column-gap: 24px; }
  .checklist div { break-inside: avoid; padding: 4px 0; }
  .checklist .item::before { content: "☐ "; color: #0f3460; }
  table { width: 100%; border-collapse: collapse; font-size: 10pt; }
  th { background: #0f3460; color: #fff; padding: 8px 12px; text-align: left; }
  td { padding: 8px 12px; border-bottom: 1px solid #dee2e6; }
  img { max-width: 100%; border-radius: 6px; margin: 12px 0; }
</style></head><body>
  <!-- cover -->
  <!-- sections with .step, .warning-box, etc. -->
  <!-- tables inline -->
  <!-- images as <img src="file:///absolute/path.png"> or base64 -->
</body></html>
```

## AI-generated illustration pipeline

For educational images (equipment, technique diagrams, site maps):

1. **Model**: `gemini-2.5-flash-image` — reliable for clean/medical illustration style
2. **Modality**: `['TEXT', 'IMAGE']` works for shorter descriptive prompts (<100 words)
3. **Parallel batch**: up to 4 concurrent via `concurrent.futures.ThreadPoolExecutor(max_workers=4)`
4. **Prompt style**: "Clean [lighting] photograph/illustration of [subject], [view angle], [style]"
   - Examples: "Clean flat-lay photograph of injection equipment on white clinical surface"
   - "Close-up educational medical illustration of subcutaneous injection technique"
   - "Educational medical diagram of the human torso showing injection site locations"
5. **Output**: save to `/root/HERMES/.out/`, embed in HTML via `file://` URI (WeasyPrint resolves local paths)
6. **Verification**: `vision_analyze` each image before embedding — check accuracy, not aesthetics

## Render

```bash
weasyprint protocol-guide.html protocol-guide.pdf
ls -lh protocol-guide.pdf
```

## Delivery

```
MEDIA:/absolute/path/to/protocol-guide.pdf
```

## Pitfalls

- **WeasyPrint handles `file://` image URIs** for local files — no base64 encoding needed for locally-generated images. Verified 2026-08-13.
- **Gemini Flash handles medical/educational prompts well** — no content filter issues. These prompts are far from the sado/intimate territory that triggers filters.
- **Light theme + emoji cover icons** — the cover emoji (💉, 🩺, etc.) renders as image objects in WeasyPrint. Don't confuse with chart image objects in `pdfimages -list`. Check dimensions: emoji glyphs are ~100-200px; real charts are 800px+.
- **`@page { margin: 2cm }` is the sweet spot** for protocol PDFs — tighter than the 14mm used for chart-heavy reports, because protocol PDFs have less horizontal visual content.
- **Checklist CSS columns** — use `break-inside: avoid` on each item to prevent items splitting across columns.
