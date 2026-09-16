# Scanned Malaysian Court PDF → Vision Transcription (no GPU)

Working pattern for the Hermes CLI agent (no GPU, no DeepSeek-OCR, no Bailian API roundtrip) when the PDF is image-only.

## When to use this

- `pdftotext file.pdf -` returns empty output → confirmed scanned, no text layer
- `pdfinfo file.pdf` shows `Producer: iOS Version ... Quartz PDFContext` or `CamScanner` origin
- Document is Malaysian Syariah court saman, civil court order, land title, or any CamScanner-originated PDF

Do NOT use this for digital-born PDFs (text-extractable). For those, `pdftotext` is enough.

## Recipe

```bash
# Step 1 — confirm no text layer
pdftotext /path/to/court-doc.pdf - | head -10
# empty output = scanned, proceed

# Step 2 — render the pages you need as PNG (80 dpi is the sweet spot)
# -r 80: high enough for typed legal text, low enough to fit context budget
# -f N -l M: page range (default = all pages)
pdftoppm -png -r 80 -f 1 -l N /path/to/court-doc.pdf /tmp/court-pg

# Step 3 — for each page, call vision_analyze with a transcript prompt
```

## Prompt template (vision_analyze question)

> "This is a scanned Malaysian [Syariah/civil/land] court document. Extract ALL text exactly as written. Preserve: party names, IC numbers, case number, court name, dates (in dd/mm/yyyy), claim amounts (RM), orders. Transcribe verbatim — do not summarise. Output as plain text, no markdown."

Why this prompt: Malaysian court docs follow a tight form (Borang MS2, Borang MS3, etc.). Asking for verbatim + key field preservation gives the VLM concrete extraction targets. Don't ask for "all text in markdown" — the tables are easier to verify as plain text fields.

## Worked example — Nabilah binti Fazil nafkah anak case

Source PDF: `/root/.hermes/lanes/private/nabilah/kes-nafkah-anak-2026-08-17.pdf`
- `pdfinfo` Producer: `iOS Version 26.5 (Build 23F77) Quartz PDFContext` — confirmed scanned
- `pdftotext` returned nothing
- `pdftoppm -png -r 80 -f 1 -l 4` rendered 4 PNG pages
- `vision_analyze` with the prompt above returned the full BORANG MS2 saman + PERNYATAAN TUNTUTAN contents:
  - Case: Nabilah binti Fazil v. Fahim bin Ahmad Shukri, Kes Mal No. 2008-040-0633
  - Court: Mahkamah Rendah Syariah Seberang Perai Utara, Pulau Pinang
  - Plaintiff IC: 941108-07-5114, address No. 17 Jalan Seri Indah, Taman Seri Indah, 13200 Kepala Batas, P.Pinang
  - Defendant IC: 941119-02-6027, address No. 56 Kampung Banggol Leban, Bongor, 09100 Baling, Kedah Darul Aman
  - Marriage: 09/09/2022, Masjid Ibadurrahman Seri Gerdang, 13200 Kepala Batas, P.Pinang
  - Wali at akad: Fazil bin Khamis (Arif's late father)
  - Child: Fattah Nuqman bin Fahim, age 3
  - Peguam: Tuan Shazril Khairy bin HJ Mustafa @ Shazril Khairy Mustapha & Associates
  - Peguam address: No. 2109-A Tingkat 1, Wisma Speaik Abdullah Fahim, 13200 Kepala Batas, Seberang Perai Utara, P.Pinang
  - Tarikh saman: 27 haribulan 7 / 2026 (signature date; case filed earlier)

## Reuse rule (learned the hard way)

Before re-rendering a scanned lane PDF, check `session_search` and the skill's own worked examples — a sibling session may have already transcribed the exact same file days earlier. Re-OCRing a 7-page court doc that another agent read two days ago costs ~6 vision calls and re-introduces transcription variance between sessions. Stale-by-days transcriptions of legal fields are fine for briefing, but re-verify case-critical numbers against a fresh render before quoting them to the sovereign.

## Pitfalls

- **`pdftotext` returning empty is the SIGNAL** — don't waste a tool call on Tesseract or qwen3-omni-flash OCR. They need image input, not text-extraction input.
- **Don't go above 100 dpi** — explodes context budget per page and slows vision analysis. 80 dpi is enough for typed legal forms.
- **Vision_analyze per page, not all pages at once** — multi-page vision calls lose detail and cost more context. Loop over single pages.
- **Watch for handwritten IC numbers, signatures, dates** — CamScanner-origin docs often have hand-filled fields. The VLM will read typed text well; handwritten text may need lower confidence flagging.
- **Stamp overlap** — Malaysian court docs have Pendaftar stamps over text. Crop bbox around stamped regions for verification if any field looks ambiguous.
- **Rubber-stamp + scanned + multi-language = full re-grounding trigger** per `FORGE-document-intelligence` skill §4. This is high-stakes data (legal); treat any extracted figure as provisional until cross-checked against original.

## When this fails

- Severe scan degradation (pre-1990 docs, faxed faxes) → confidence < 0.70 per field → flag for manual review or higher dpi re-render
- Handwritten letters/medical records → VLM still works but more verification needed per field
- Image-only PDF where pages are tiny photos of paper (not flatbed scans) → render at -r 150 minimum
