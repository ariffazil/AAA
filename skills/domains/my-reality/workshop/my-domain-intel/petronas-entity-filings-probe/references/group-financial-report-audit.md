# PETRONAS Group Financial Report — Audit Rules

The group report (petronas.com → Investor Relations → Interim / Financial Report, direct PDF) is the only authority for group numbers. Read it before repeating any figure, including one you are handed.

The **deck** ("Highlights", ~8 pages of charts) and the **financial report** (the statements) are two different documents from the same release. Both are primary; they can disagree on the same metric, and the disagreement is usually definitional, not an error. Cite which one you used.

## The accumulated-loss trap (biggest single misread)

A segment loss can be **recognition of previously unrecognised accumulated share of losses from a JV**, not an operating loss. The report states the operational number separately in the same paragraph.

- Do NOT quote the headline segment LAT as "the segment is losing money operationally".
- Read the sentence after it, which gives PAT excluding that item.
- Label clearly: *one-off prior-period recognition* vs *run-rate*.

Why it matters: quoting the headline alone is trivially rebutted by the next sentence of the same page, and it collapses the whole argument built on it.

**Corollary — get the SIGN of the adjustment right.** "Excluding the unrecognised prior-period item, PAT is X" means X is the *cleaner* number, not the worse one. Reading the exclusion as the hidden bad news inverts the report's own logic, and an inverted reading is more dangerous than a missing one because it carries a citation and looks like rigour. Before using any "excluding X" figure, ask whether the report is *clarifying* or *concealing* with that sentence.

## Net cash — read the statement of cash flows, do not compute it

Use **"Net (decrease)/increase in cash and cash equivalents"** from the cash flow statement. Do not subtract the balance-sheet closing balances and call it "cash burned" — that conflates FX translation, restricted cash and reclassification with operating outflow.

Also separate on the same page:
- CFFO (operating)
- net cash used in investing (this is where equity injections into JVs land)
- net cash from financing (borrowings, dividends)

Cross-check any "cash fell by X" claim against all three before accepting it.

A "cash fell by X" claim that is much larger than the cash-flow-statement movement is often actually a **net-debt** movement. Net debt moves with gross borrowings, lease liabilities and FX; cash flow does not. Name which metric the claim is really using and recompute on the matching basis.

## Two series on one page — never cross-label them

A highlights page commonly prints **two price series side by side**: a benchmark crude (Brent) and a dated/weighted reference (JCC single-month), each with its own prior-period figure and % change. Both are labelled; they are not interchangeable.

- Read the label attached to each number, not the row you think you are on. A prior-year figure lifted from the adjacent series produces a number that looks plausible, is not in the filing under that name, and is the first thing a hostile reader checks.
- Same trap applies to **production**: a financial report can carry one figure (e.g. working-interest basis) while the media release and deck carry another (entitlement/sales basis) for the same half-year. Both are valid; they are different measures. Cite the one you used and say which basis it is. Do not "correct" a document for citing the correct one.

## Deck percentage vs report absolute — they can disagree

A chart may round a segment share (e.g. "21%") while the statements give the absolute (e.g. RM8,990m) against a total that computes to 21.7%. Neither is wrong.

The error is **converting** one to the other and presenting the result as a filing figure: 21% × total = RM8.7b, which appears nowhere in either document.

- Quote the absolute from the statements; quote the share from the deck with its source named, or compute the share yourself and show the denominator.
- Note the direction of the resulting error. Understating a segment's spend weakens your own argument if that argument is "this segment is underfunded" — an error that *helps* your thesis is the one that gets caught.

## Dividend: declared vs estimated

- **Declared** = board decision, stated in the report and media release.
- **Analyst target** = a bank's projection ("potential", "assesses").

Never present the second as the first. If you must mention a projection, name the house and the word "estimate".

## Borrowings can rise without borrowing

A period-on-period rise in total borrowings is not automatically cash drawn. Lease-liability additions, FX revaluation of foreign-currency debt, and reclassification all move the closing balance. In a single half-year the non-cash component can be as large as the cash component.

Read the financing-activities section of the cash flow statement for the cash movement, and the debt note for the closing balance, then reconcile the two before writing "borrowings rose because they borrowed". A reader who opens that note will find the gap.

## Related-party and JV injections

A step-up in "capital investments" in a segment usually means an **equity injection into a JV**, not organic capex. Find the narrative line that says so; the number alone reads as growth.

Equity injections into a loss-making JV and workforce-reduction savings are the two numbers most often placed side by side to make an argument. Both are usably precise — pick the period that contains both, and divide one by the other rather than reaching for a headline figure from a different year.

## Verify corporate self-description against the live site

Purpose/mission/values wording drifts. Before claiming a phrase was removed or added, load the current page. Historically "national" and "peoples and nations" persisted in some surfaces even where the top-line descriptor changed to "society" — so a blanket "they deleted the nation" claim is falsifiable in one click.

The same rule applies to a **list of behaviours or values**: a short list quoted from an internal deck may not appear in any public document. Check the public report before treating an internal list as citable outside the company, and check whether items present in an older published list are *absent* from the newer one — a removal is a stronger finding than an addition.

## Unattributed third-party claims

"Analysts say X" with no name, house, date or link is not evidence. It is unfalsifiable, and it is the first sentence a technical reader attacks — which then taints the verified material around it.

- Name the source (person or house, date, link), or
- Restate it as your own labelled reading ("our reading of the structure is…"), or
- Delete it.

A first-party corporate identifier or a jurisdiction detail you hold in your own notes (a company number, the governing law of an entity) must not be attributed to a third party who never said it. Keep your own derivations labelled as yours.

**Precision without provenance is a shape, not evidence.** A claim carrying exact counts ("N mentions", "M engagements") while naming no study, author, platform or date is fabricated-metadata shape. Real measurement is attributed, because whoever did the counting wants credit for it. Treat unverifiable precision as a liability rather than a rhetorical asset: it hands a hostile reader an easy dismissal and contaminants the argued sections around it. A verified smaller number always beats an unverifiable precise one — so replace the figure or drop it, never keep it because it is vivid.

## When your own canon conflicts with the filing

The filing wins. If a number in your own stored knowledge base disagrees with the report currently in your hands, the stored number is what needs a correction label — do not quietly keep both, and do not edit the canon to a new value until it is re-verified from the primary.

- Mark the stored claim `CONTESTED` with the two conflicting values and where each came from. A canon that is *known* to be uncertain is safe; a canon that is silently wrong is not, because everything downstream inherits it.
- Grep the canon for the same figure before publishing anything that depends on it — one wrong number in a single-source-of-truth file propagates into every article and dashboard built on it.
- Reconcile the two numbers *within the stored file itself* first. A file whose summary table and whose own reconciliation table disagree is internally falsified, and a reader who opens both will say so.

## Announced target vs disclosed outturn

A programme can be announced with a headline target and later disclosed with a smaller measured actual, in the same document set, with no bridge between them. "A 10% reduction of the total workforce" and "a 6 per cent reduction from 2024, primarily associated with organisational and portfolio adjustments" are both true and do not explain each other.

- **The gap is itself the finding.** An announced figure is a commitment; a disclosed figure is a measurement. Where no statement reconciles them, one of the two is describing something else — a different population, a different window, or an intention that was not met. Report the gap rather than averaging it away.
- **Do not treat the disclosed actual as total.** A phased programme's interim disclosure is not its final state. Check the declared phases against their own completion dates: an announced end date that passes with no announcement of completion is the same class of gap, and a "concluded" programme followed by division-level changes the public record never mentions means the phasing in the document is not the phasing on the ground.
- **Distinguish the announced number's audience.** When a cut is announced alongside a dividend reduction, the headline serves the fiscal narrative as much as it describes an operating plan. State which number is the target, which is the measurement, and over what window each is defined — then let the reader see they are not the same quantity.

## Programme names may exist only in speech

A transformation can carry a name used constantly in internal decks, townhalls and the press that appears in **no** published corporate document — absent from the annual report, the results releases and the activity outlook. Verify by full-text search of the report before citing it as official.

Two consequences worth stating in an audit:

- **An undefined programme cannot be held to a standard.** No published end state, no published milestones and no published definition mean no basis for evaluating it, and no basis on which it can fail. That absence is a governance fact, not a formatting gap.
- **Internal-only language is not citable outside.** A behaviour list, a scorecard or a programme name drawn from an internal deck does not belong in anything leaving the organisation unless the public record carries it. Label internal provenance explicitly when the distinction matters to the reader.

## Audit output format

Report three buckets, in this order:
1. **Confirmed** — matches the filing, cite the line
2. **Wrong** — give the filed number and the delta (%)
3. **Unsupported** — plausible but not in any primary source; label UNVERIFIED

Then offer the *stronger true* version of the argument, using only confirmed numbers. A verified statistic that is 20× rather than the claimed 43× is worth more than an unverifiable 43×.

### Keep the near-misses visible

When a claim looked wrong and turned out correct, say so and say why (the two definitions, the two bases). Suppressing the near-misses and reporting only confirmed/wrong makes the audit look cleaner and makes it less trustworthy: the reader cannot tell whether you checked the hard ones or just the easy ones. A short "I nearly flagged this — here is why it stands" is the strongest available evidence that the audit was real.

### Do not write the corrected document from memory

If you are asked to produce a corrected version of someone else's document, you need the document. An audit note listing the corrections is not the document, and reconstructing their structure and remaining prose from the corrections alone will silently drop material and invent section boundaries. Produce the correction sheet if you have only the corrections; produce the corrected document only when you hold the original.
