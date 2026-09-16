---
name: petronas-entity-filings-probe
description: Use when probing PETRONAS subsidiary filings (UK).
---

# PETRONAS Entity-Level Filings Probe

Press releases describe the group. Filings describe the entity that signed. The gap between them is where the real signal lives.

## When to use

- A PETRONAS subsidiary signs an SPA/JV and you need to know **which legal entity** signed and what it actually earns
- Testing "is this expansion or substitution?" for any PETRONAS global deal
- Any claim about PETRONAS offshore revenue, trading arms, or European/Atlantic LNG activity

## Core insight

PETRONAS runs parallel UK entities at the same address (60 Ludgate Hill, London EC4M 7AW). A deal signed by one entity can move revenue away from another with **no change in group headline numbers**. Only filing-level reading exposes this.

Known entity set:

| Entity | Co. No. | Role |
|---|---|---|
| PETCO Trading (UK) Ltd (PTUK) | 06695912 | trading arm; crude/products/LNG marketing, chartering |
| LNG Investments Europe Ltd (LIEL) | 09291740 | Dragon LNG (Milford Haven) offtake; UK NBP regas; global LNG resale |
| Searah | UK Co. #17027115 | upstream operatorship from Jul 2026 — moves gas cash flows under English Commercial Law |

## Procedure

1. **Identify the signing entity** from the press release. Note if the ceremony screen disagrees with the release — that discrepancy is itself a finding.
2. **Find the filing history**:
   `https://find-and-update.company-information.service.gov.uk/company/<NUMBER>/filing-history`
   Browser-driven (`js` on body innerText) works; the page is JS-heavy.
3. **Extract document links** via JS — each row has an `a[href*="document"]`:
   ```js
   [...document.querySelectorAll('a[href*="document"]')].map(a=>a.href)
   ```
   Prefer the **latest amended** filing if one exists (numbers usually identical to the original — note both dates).
4. **Download with curl** — the direct URL from the filing-history page returns the PDF:
   ```bash
   curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36" \
     -o out.pdf "<document?format=pdf&download=0 URL>"
   ```
5. **OCR — mandatory.** These are scanned images wrapped by `go-tiff2pdf`. `pdftotext` and `pypdf` return **~71 chars** for a 72-page doc. Do not report "no text" as "no data".
   ```bash
   pdftoppm -r 200 -gray -png out.pdf pages/p
   for f in pages/p-*.png; do tesseract "$f" "${f%.png}" -l eng --psm 6; done
   cat pages/p-*.txt > ocr.txt
   ```
   ~40–70s for 72 pages. Run backgrounded with notify for long docs.
6. **Read the KPI box first** (Strategic Report, usually page 3–8 of content). It usually carries volume + revenue + profit side by side — the single densest page.
7. **Then** Statement of Profit or Loss, revenue disaggregation (by product + geography), related-party notes, and **subsequent events**.

## What to extract every time

- Revenue, gross profit, operating profit, PBT, profit for year (2 years, compute the % change)
- **Volumes** — these expose substitution when revenue is distorted by accounting-basis changes
- Revenue split by **product line** AND **geography**
- Related-party balances ("amount due from ultimate holding company")
- **Onerous contract / impairment provisions** — these are where liabilities hide
- **Total equity** — negative equity is a finding
- Verbatim text explaining any change in accounting basis (principal→agent changes are usually disclosed in plain language)
- Note 1 "Reporting entity" for immediate/ultimate holding company

## Pitfalls

- **Principal vs agent changes silently move revenue.** A group can "restructure the operating model" and LNG revenue vanishes from one entity's top line while the cargoes keep flowing. Always read the Strategic Report narrative, not just the numbers.
- **Equity can be negative while the entity is "active and trading".** Negative total equity + a large IAS 37 onerous contract provision = the offtake obligation is underwater.
- **Do not equate one entity's decline with group decline.** Check group filings in parallel (petronas.com 1H/FY reports) before concluding — counter-signals are common.
- **"Amended full accounts"** filed months after the original means something was corrected. Pull both if the numbers differ.
- PERSON WITH SIGNIFICANT CONTROL filings are useful: they show when a ministry (e.g. Minister of Finance of Malaysia) was added or removed as PSC — a governance breadcrumb with dates.

## Reporting standard

Give the group narrative and the entity reality side by side. State which entity signed. Flag any unresolved discrepancy explicitly rather than smoothing it. Distinguish what the filings prove from what they merely suggest.
