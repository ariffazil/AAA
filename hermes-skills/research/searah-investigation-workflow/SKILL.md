---
name: searah-investigation-workflow
description: End-to-end workflow for Malaysian oil & gas investigative pieces — PDF extraction, F2 primary source verification, fact correction, WSJ-grade prose generation, sealed PDF output, and email outreach list building.
trigger: Investigative piece about Malaysian energy/oil deals requiring WSJ-grade output + email outreach
tags: [investigation, malaysia, oil-gas, bit, companies-house, pdf-generation, email-outreach]
author: hermes-asi
created: 2026-05-07
updated: 2026-05-07
version: 1.0
---

# SEARAH Investigation Workflow

## Trigger
Investigative piece about a Malaysian/oil & gas deal requiring F2 primary source verification + WSJ-grade prose + PDF output + email outreach list.

## Steps

### PHASE 1 — Document Ingestion
1. Extract PDF text: `python3 -c "import fitz; doc=fitz.open('file.pdf'); print('\n'.join[p.get_text() for p in doc]))"`
2. Store raw text in `investigations/` directory
3. Note page count, file size, apparent completeness

### PHASE 2 — F2 Primary Source Verification
Primary sources for Malaysian energy/oil deals:
- **UK Companies House** (company number lookup) — PSC register, officer list, filing history
  - URL pattern: `https://find-and-update.company-information.service.gov.uk/company/<NUMBER>`
  - PSC register shows: shareholders with % holding, governing law
- **UNCTAD BIT database** — verify if BIT exists between two countries
  - URL: `https://investmentpolicy.unctad.org/international-investment-agreements`
- **Eni press releases** (for deal value confirmation)
- **PETRONAS website** (for CEO profile, chairman)
- **Malaysia Parliament Hansard** (for democratic oversight)
- **RTM TV1 broadcast records** (for on-record statements)

### PHASE 3 — Fact Corrections to Apply
Common corrections found in SEARAH investigation:
- Company name: verify exact legal name ( Companies House is authoritative)
- CEO appointment date: always cross-check (multiple sources often conflict)
- CEO education: BA vs BEng — verify from university records
- BIT existence: UNCTAD is authoritative — web searches often return stale results
- Deal value: use company's own press release figure
- Governing law: PSC register often states this explicitly

### PHASE 4 — WSJ Prose Generation
- Tone: Journalistic, scene-driven. Start with a specific moment/date/statement.
- Structure: 9–10 parts, each with a clear sub-heading
- BIT/legal sections: explain clearly for non-lawyers
- What we know / What we don't know: binary section at end
- No arifOS constitutional framing in final prose
- Target: 4,500–5,000 words (9–10 PDF pages)

### PHASE 5 — PDF Generation
Use **weasyprint** (not pandoc/wkhtmltopdf which may not be installed):
```python
import weasyprint, warnings
warnings.filterwarnings('ignore')
w = weasyprint.HTML(filename='input.html').write_pdf()
open('output.pdf', 'wb').write(w)
```

### PHASE 6 — SEAL 999 Commitment
snarkjs Groth16 may fail (wasm/zkey mismatch — common on VPS). Fallback:
```
Chain hash = HMAC-SHA256(Exposé hash + DB hash + operator + timestamp)
```
Store in VAULT999/SEALED_EVENTS.jsonl.

### PHASE 7 — Email Outreach
For Malaysian targets:
- Twitter/X DMs: most politicians have nitter accounts (verify: `curl -s "https://nitter.net/<handle>" -o /dev/null -w "%{http_code}"` → 200 = exists)
- Public email addresses: rare. `mahathir@mahathir.com` is an exception.
- Facebook: often has pages for politicians (302 redirect = exists)
- WhatsApp: no public lookup — need mutual contacts

**Confirmed reachable:**
- Tun Mahathir: `mahathir@mahathir.com`
- Maria Ressa / Rappler: `news@rappler.com`
- Fahmi Reza: `fahmireza@gmail.com`

**Handle pattern for Malaysian politicians:**
- `@chedetofficial` (Mahathir)
- `@dr_hishamjalil` (Hisham Jalil)
- `@Jeffreykitingan` (Jeffrey Kitingan)
- `@wanzulkifli` (Wan Zulkifli, ex-PETRONAS CEO 2009-2015)
- `@hassanmerican` (Hassan Merican, ex-PETRONAS CEO 1995-2009)

### Pitfalls
- **BIT thesis:** ALWAYS verify with UNCTAD first. Don't trust web search results about treaty existence.
- **Company name:** Companies House is authoritative, not the PDF or press releases.
- **CEO profile:** multiple sources often give conflicting dates — use the company's own press release.
- **PH politicians:** cannot be trusted for Malaysian sovereignty issues — exclude from outreach.
- **Ex-PETRONAS CEOs:** best insider voices (Wan Zulkifli 2009-2015, Hassan Merican 1995-2009).
- **snarkjs on VPS:** wasm/zkey mismatch is common — HMAC-SHA256 is the working fallback.
- **PDF engine:** `wkhtmltopdf` often not installed — use `weasyprint` instead.
- **Multiple PDF versions:** user may have several drafts (V1, V2, FORGED V5 etc.) — clarify which is canonical before sending.

### Evidence DB Format
`SEARAH-TRUTH-DB.md` style — entries with: ID, Claim, Source Type, Status, Confidence (0.0–1.0), Source, Notes.
Sections: Company Structure (A), Deal Terms (C), Governance (D), Parliament (E), CEO Profile (F), BIT/Legal (G), Energy Crisis (H).
Verdict Summary table at end.
ZKPC seal block at very end.
