---
name: forge-pdf-delivery
description: Turn markdown into a real PDF and deliver via MEDIA:. Never claim an attachment that was not built and verified.
capability_tier: fed-long-context
ecology_state: WARM
---

# forge-pdf-delivery

Class-level skill. Trigger: the user wants a portable document, not a chat reply. Examples: KWSP briefing for a friend, contract summary, research digest, weekly report, market brief. Trigger phrases: "bagi pdf", "buat pdf", "send me the PDF", "I need a doc on X".

## The one rule

**A file with the `.pdf` extension is NOT a PDF.** Always confirm via `file <path>` that the output shows `PDF document, version 1.7` (or similar) before delivering. If `file` returns `Unicode text`, you wrote text with a wrong extension — fix the pipeline, don't ship.

## Pipeline (use this exact order)

1. **Author content as Markdown.** One source of truth. Use proper headings (`##`, `###`), pipe-table syntax, lists — pandoc/weasyprint render them well.
2. **Build HTML.** Either:
   - Wrap markdown manually with a styled HTML template (recommended for design control).
   - Or `pandoc input.md -o output.html --standalone --metadata title="..."`.
3. **Render PDF.** `weasyprint input.html output.pdf` — local, no API call, renders tables / emoji / unicode (✅ ❌ ⚠️ ·) cleanly. Engine is at `/usr/local/bin/weasyprint`.
4. **Verify.** `file output.pdf` must return `PDF document, version 1.7`. If it returns `Unicode text`, start over from step 1 with the real content.
5. **Layout QA without a vision lane.** When the active model has no native vision (or `vision_analyze` returns no transcript), verify layout programmatically instead of eyeballing screenshots: `pdfinfo <file>.pdf | grep -E 'Pages|Page size'` — page count must match the number of designed `.page` blocks (a mismatch = overflow spilled an extra page) — then `pdftotext -f N -l N <file>.pdf - | head` per page to confirm each section landed in order with no truncation. `pdftoppm` still works for pixel-render smoke checks but the text-layer check is the reliable gate.

5b. **Browser-print engine gate.** If the PDF came from headless Chrome/Chromium (`--print-to-pdf`) or any HTML deck, the page-count check is the primary defect detector, and it fails silently. Full recipe: `references/browser-print-layout-gate.md`. Two recurring traps:
   - **Fixed-size slide divs + non-zero `@page` margin = every slide splits into two pages.** A `.slide { width:297mm; height:210mm }` under `@page { size: A4 landscape; margin: 1cm }` leaves only 277×190 mm printable, so each slide overflows and Chrome emits *two* pages per slide — title on one, figure on the next, plus a blank tail. A 12-slide deck silently became a 24-page PDF with four near-empty pages. Fix: `@page { margin: 0 }` (the deck supplies its own padding) or size the slide to the printable box.
   - **Browser furniture prints on every page** unless suppressed: render date/time, document title, and the raw `file:///` source path. Always pass `--no-pdf-header-footer`. Never ship a third-party deliverable carrying an internal filesystem path.

5c. **Ink-coverage sweep — the automated blank-page detector.** Counting pages is not enough; a page can be counted and still be empty.

```bash
pdftoppm -png -r 110 out.pdf /tmp/qa/page
python3 - <<'EOF'
import glob
from PIL import Image
for f in sorted(glob.glob('/tmp/qa/page-*.png')):
    im = Image.open(f).convert('L'); w,h = im.size; px = im.load()
    dark = tot = 0
    for y in range(0,h,3):
        for x in range(0,w,3):
            tot += 1
            if px[x,y] < 235: dark += 1
    print(f, f"{100*dark/tot:5.2f}%")
EOF
```

Healthy text-and-figure pages land ~4–25 %. Under ~2 % is a split or empty page; a wide spread (0.3 % beside 24 %) is the signature of a layout break, not of intentional design. Over ~60 % is a full-bleed cover — fine on screen, but it eats toner and its gradients band on paper, so flag it if the deliverable is meant to be printed.
6. **Copy to forge_work.** `cp output.pdf /root/AAA/forge_work/<date>-<slug>/<descriptive-name>.pdf` — durable location, not `/tmp`.
7. **Deliver.** Include `MEDIA:/absolute/path/to/file.pdf` in your Telegram reply. Hermes auto-attaches as a document.

## Carrying numbers in the deliverable — content gate (not layout)

The five checks above prove the file renders. They do **not** prove the document says what you think. When the deliverable carries monetary figures, invoices, ledgers, settlements or splits of any kind:

**One invoice per order.** A document that prints a prior settled payment alongside a new unpaid item, then subtracts one from the other to derive a "balance", manufactures a debt that did not exist in any contract. The recipient reads the resulting "balance due" as a claim. If a prior transaction belongs on the page at all, it sits in a separate EXCLUDED block with a status label (SETTLED / VOID / REFUNDED) and does not enter the arithmetic that decides what is owed. See `references/invoice-content-discipline.md` for the full rule set and the canonical "one order / one page" template.

**Lock the source on the original receipt, not on whichever party spoke last.** When two people describe the same transaction differently, the temptation is to revise the document after each speech act. Hold the record on its first source (a receipt photograph, a logged transfer, a confirmed reply) until that source is contradicted by a higher-warrant observation. Surface disagreements inside the document ("party A states X; party B states Y") instead of re-rendering. A fresh-looking PDF built on an unverified record is the same defect as a stale figure presented as current.

**Tag every line with its evidence class on the page itself.** When two readers can have read the same artifact and come away with different amounts, the artifact failed — not the readers. Print three classes inline, each with its own visual treatment: `VERIFIED` (printed on a receipt the user photographed), `REPORTED` (spoken by one of the parties), `DERIVED` (your arithmetic, every input labelled). Empty cells are the right answer for line items where no source exists — never a confident blank-style default.

## Pitfalls (read before authoring)

- **Pandoc CANNOT read PDFs.** `pandoc file.pdf -o out.html` errors with "Unknown input format pdf". The reverse direction (md → html → pdf) is the only valid flow.
- **Weasyprint unicode.** ✅ ❌ ⚠️ · (middle dot) — and Malay diacritics all render fine. If you see boxes/squares, install `fonts-noto-core`.
- **Tables.** Always pipe-table syntax in markdown. Don't lay out tables with spaces or hand-rolled HTML — pandoc/weasyprint will eat them.
- **Don't `cat << EOF > file.pdf`.** That writes text with a misleading extension. Use the pipeline.
- **Don't try to generate PDFs inside execute_code.** The sandbox doesn't ship matplotlib/weasyprint. Use `terminal` or write `/tmp/script.py` and run via `python3 /tmp/script.py`.
- **NEVER claim an attachment you did not build.** If a reply says "[PDF Attachment]" but no file was created and no `MEDIA:` path was included, that is fabrication — the user WILL call it out ("Tepek sini"). Recovery: build the real file via the pipeline above, deliver with `MEDIA:/abs/path.pdf`, and own the miss plainly in one line. The `file <path>` verify step exists precisely to gate this.
- **Simple one-pagers can use reportlab directly** (`from reportlab.pdfgen import canvas`) when the content is headings + bullets, no markdown source needed. Still verify with `file output.pdf` → `PDF document` and still deliver via `MEDIA:` with a durable path (forge_work), not `/tmp`.

## Companion pattern

For live market data charts that get delivered the same way (PNG image via MEDIA:), see `forge-finance-chart-delivery` — same verify-then-deliver discipline, same forge_work destination convention.

For PDF + multi-image infographic bundles (timeline + checklist + chart), see `references/infographic-image-companion.md` — matplotlib pipeline proven for Malaysian biohacking/competition guides.

For image-based magazine-style PDFs (custom layout per page, dark themes, callout boxes, code-switching typography), see `references/image-based-pdf-pipeline.md`. Read it before attempting multi-page visual PDFs — the pitfalls there (matplotlib text truncation, AI cover text artifacts, unicode glyph missing, vision-only verification) cost several re-renders each time.