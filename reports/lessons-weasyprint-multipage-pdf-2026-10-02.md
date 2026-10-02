# LESSONS — WeasyPrint multi-page HTML→PDF (session 2026-10-02)

Context: built ARIF_FAZIL_PETRONAS_PORTFOLIO_2026.pdf (18pp A4) via WeasyPrint 70.0.
These are reusable layout rules for any designed multi-page PDF. Candidate to fold into
`pdf-federation` (SKILL.md patch was blocked by the skill security scanner this session).

## Layout recipe that works

```css
@page { size: A4; margin: 0; }
.page { page-break-after: always; width: 210mm; height: 297mm;
        position: relative; overflow: hidden; box-sizing: border-box; }
.pad  { padding: 15mm 17mm; height: 100%; box-sizing: border-box;
        display: flex; flex-direction: column; justify-content: space-between; }
.pad > * { flex: 0 0 auto; }
.pfoot { position: absolute; left: 17mm; right: 17mm; bottom: 8mm; }
```

`justify-content: space-between` on the page container is what kills the bottom-third
whitespace of fixed-height page layouts. It took 15 pages from ~65% fill to ~92%.

## Pitfalls (all hit live)

1. **Nested `display:flex` rows containing images break WeasyPrint.** The row collapses,
   the image crops, and the page's own header can disappear. Fix: use
   `<table style="border-collapse:separate; border-spacing:9mm 0"><tr><td>…</td></tr></table>`
   with `vertical-align: top`. Tables are robust where nested flex is not.

2. **`.page { overflow: hidden }` clips silently, and the page count does NOT reveal it.**
   After a spacing bump the page count stayed at 18 while one page's content was clipped.
   Never infer "it fits" from a stable page count.

3. **Page-fill audit (no vision needed).** Rasterize then measure ink extent per page:
   ```
   pdftoppm -png -r 130 out.pdf renders/page
   # per page: last row containing ink / page height; flag < 80% as under-filled
   ```
   Ink threshold: `a < 200` on light pages, `a > 90` on dark pages (pick by median).
   This catches under-fill AND silent clipping in one pass.

4. **Low-DPI renders mislead vision models.** At 72 dpi, small captions are read wrong and
   look like document defects. Render at >= 130 dpi before visual QA; cross-check any
   suspected defect with `pdftotext -f N -l N`.

5. **A confined binary may return `Permission denied` on the scratch dir.** `qpdf --check`
   under an AppArmor profile could not read `/root/.hermes/cache/scratch/**` and reported a
   structural failure that was really a path refusal. Build and ship the final artifact from
   a plain readable dir (e.g. `/root/<name>/`), then run the structural gates there.

6. **Letter-spaced titles break multi-word sentinels in `pdf_verify.sh`.** `REALITY > EVERYTHING`
   fails an exact substring match because of `letter-spacing`. Pass single-token sentinels.

7. **Telegram document delivery (declared destination clears the transport lock).**
   ```
   source /root/.hermes/.env            # token env name is read from config.yaml: telegram.bot_token_env
   curl -sS -X POST "https://api.telegram.org/bot${ASI_ARIFOS_BOT_TOKEN}/sendDocument" \
        -F "chat_id=267378578" -F "document=@f.pdf;type=application/pdf" -F "caption=…"
   ```
   Receipt = `result.message_id` (+ `document.file_id`). Absence of an error is not delivery.
