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
- **Auditing a third-party PETRONAS critique or corporate document** — every number in it gets checked against the group's own report before you repeat it (see `references/group-financial-report-audit.md`)

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
- **Never repeat a number because it sounds authoritative.** Bank/analyst estimates, rounded recollections and third-party critiques are not company figures. Trace each number to the filing or drop it — one wrong figure discredits an otherwise-sound argument.
- **Verify a corporate statement against the live website, not memory.** Mission/purpose/values wording changes over time; quote what the site says today.

## Reporting standard

Give the group narrative and the entity reality side by side. State which entity signed. Flag any unresolved discrepancy explicitly rather than smoothing it. Distinguish what the filings prove from what they merely suggest.

### Do not build a case

The user is an insider assessing their own position. That makes anchoring the characteristic failure of this work: once they have stated a leaning (that a tenure should end, that they intend to leave), every fresh artifact you read will feel like corroboration, and you will silently weight it that way.

- **Weight each datum on its own merits.** A rising group LNG volume, positive operating cash flow, improving OEE, and independent forecasts of stable production are evidence, not noise to be explained away.
- **State the counter-signal in the same breath as the finding.** An argument the user can trust is one that has already survived its own counter-evidence. Presenting only confirming items is narrative over reality — and they will catch it.
- **Give data, not pressure.** The decision is the sovereign's. Your job is to make the picture accurate, not to move them toward the conclusion you have already formed.
- **Surface a contradiction with their own earlier position — as a map update, never as a gotcha.** If a prior plan and a current plan disagree, say so at the moment you notice it rather than following the newer one quietly. But the *manner* decides whether it lands: "this artifact is from July, here is what moved since" is help, while re-quoting his own sentence back as a refutation reads as hostile, and he will push back on it even having asked to be challenged. Date the artifact, name what changed, and let him draw the inference.
- **Separate decisions that share a form before arguing about either.** When he asks a yes/no, check whether the question is actually two: a strategic one (do I want to be here) and a procedural one (do I file this form, accept this offer). Doctrine governing the first cannot close the second — using it that way is a category error, and he catches it as being played with his own words. A filing that buys an option is not an act of leaving; answer the option question on its own terms, and say plainly when the form is not the decision.
- **A stated fear and a stated fact arrive in the same breath; separate them before responding.** Two fears can point opposite ways ("the company is going under, so take it now" / "the door will close, so take it now" is one fear; "I would be trapped" and "I would be sorry" is two). A principal paralysed for months is usually holding two fears in tension, not one indecision — naming which fear argues for which action is what breaks the loop, and it is not the same as telling him what to do.

### Date every first-party artifact before you use it

The insider's most persuasive evidence is their own earlier writing, and it is the easiest to mishandle. A stored analysis is a **snapshot of what was believed on the day it was written**, not a standing authority. Citing it as current is how you end up arguing against reality with the user's own words, which reads as hostile even when it is not intended that way.

- **Stamp the date on every artifact you quote**, and work out what has elapsed since. Cycles that were open may have closed; deadlines may have passed; a stated eligibility bar may have lapsed on its own; a person named as about to leave may still be in post.
- **Re-verify the load-bearing claims against the live record** before building on them. The artifact tells you what the position *was*; only the current source tells you what it is.
- **Say what changed**, briefly and without ceremony, when a plan built on the old snapshot is now moot. The user already knows things moved — they will say so — and being told the artifact is stale without being told what replaced it wastes the turn.
- **Two internal documents disagreeing is a finding, not a distraction.** If a stored doctrine and a stored model conflict, or a summary line conflicts with the reconciliation table in the same file, report the conflict and label both, rather than picking the one that fits the current argument.

## References

- `references/group-financial-report-audit.md` — auditing the PETRONAS group interim/FY report: the accumulated-share-of-losses trap, net-cash arithmetic, dividend-declared vs analyst estimate, operational-vs-one-off separation, two-series cross-labelling, deck-percentage vs report-absolute, non-cash borrowing movement, and how to handle a conflict with your own stored canon.
- `references/basin-thermal-maturity.md` — answering "can this basin cook?" for a petroleum geologist.
