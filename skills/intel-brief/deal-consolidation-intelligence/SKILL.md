---
name: deal-consolidation-intelligence
description: "Use when analysing a rumoured merger or stake sale."
version: 1.0.0
tags: [deal, ma, consolidation, rumour-verification, void-analysis, valuation, sovereign-brief]
---

# Deal & Consolidation Intelligence

> **Trigger:** "is this merger real", "deep dive on the [X] takeover", "what's happening with [company] and [company]", a stake-sale or pare-down story, a rumoured "largest [X] in the country" tie-up, or any question about whether a consolidation will actually happen.
> **Companion:** this skill covers the *deal-specific method*. The four-layer framework (tersurat / tersirat / quantum / void), the epistemic tags, the forge receipts and the constitutional audit live in `intelligence-brief-forge`. The render pipeline lives in `forge-pdf-delivery`. Load all three for a full brief; this skill carries what neither of those does.
> **Constitutional:** F2 (every numeric claim sourced or derived), F7 (gaps and analyst bias disclosed), F9 (no intent attribution — outcomes and disclosed positions only), F13 (intelligence product, not a policy directive). **Never issue investment advice, a rating, a price target, or a buy/hold/sell view** — on a live listed counterparty this is both an F12 breach and a real-world liability.

## The one distinction that governs every deal brief

**A standing condition is not an event.** Sustained coverage around an institution almost always grows from an unresolved *obligation* — an unmet regulator condition, a mandate the owner keeps deferring, a shareholder deadlock — rather than from an active *process*. Deal rumour volume tracks the condition, not the process. So the first analytic job is not to assess the deal; it is to establish which of the two exists, and say so in the opening paragraph.

- If the condition exists and process artifacts are absent: **"the pressure is real, the event is not."** Deliver that, date-stamp it, and name the single filing that would supersede it.
- If process artifacts exist: you have an event. Proceed to scenario work.

Getting this wrong is the cardinal failure of the class — it turns a decade of failed attempts into "sources say a deal is near".

## Procedure (in order)

**1. Correct the premise before answering.** Verify the ownership structure from primary sources before accepting the framing in the question. Rival premises are common: "his banks" plural when the subject owns one licensed institution; a "merger of X and Y" where one party is a subsidiary of a larger group; a "largest in the country" that only holds under one narrow definition. Naming the premise error in the first two paragraphs is the highest-value move available and it costs one filing.

**2. Build the ownership chain to beneficial-owner level, then compute the effective interest.** Walk: ultimate individual or state holder → listed vehicle → operating entity. Compute the controller's *effective economic interest* (their share of the vehicle × the vehicle's share of the target) — it is usually far below the headline percentage and it reframes what a sale would mean for them personally.

**3. Build the condition ledger.** Every regulatory condition, mandate, deadline or undertaking attached to the relevant licences or approvals, with its year of origin, whether it has been met, and how many times it has been extended. This ledger is the skeleton of the brief. Two derived diagnostics:
   - **A condition unmet across many years means the constraint is price and control, not execution.** Say so directly.
   - **Repeatedly granted extensions prove the regulator is not the binding party.** Stated plainly, this is often the most useful sentence in the document.

**4. Note where the legal constraint actually lives.** Check whether the binding rule is a statutory cap, a condition of a specific historic approval, or a policy expectation — they have completely different degrees of freedom (a condition of approval can be extended, waived or renegotiated; a statute cannot). Commentary routinely conflates these, and the distinction decides whether the deadlock is political or permanent. If the instrument itself cannot be located, say that it cannot be located rather than asserting its terms.

**5. Decompose the headline claim.** Never score a superlative once. Enumerate the competing definitions of the claim (subsidiary vs standalone licence vs co-operative vs group; national vs regional) and compute the subject against each, against every plausible combination, and against the actual market leader. Report which definition makes the claim true and by how much. A claim true only in one narrow lane by a few per cent is a narrative asset, not an economic one — say that, because the distance between the definitions is usually the story.

**6. Band the price from precedent, not from a model.** Where a price is disputed and no transaction is struck, build a band from the multiples that comparable assets actually cleared at: the price the current owner itself paid for the stake, the last comparable full acquisition in the sector, and the sector's prevailing trading multiple. Multiply by the target's book value and split by shareholding. Present a band with each edge attributed to its precedent. Then state the asymmetry that explains the deadlock: **a buyer anchors at the bottom of the band and a seller at the top, and neither has moved across years.** A single point estimate would be false precision; the band plus the asymmetry is the finding.

**7. Map the market frame and the licence landscape.** Sector size and growth, the share controlled by the top players, how many licensed participants exist, and any regulator policy on new licences or on consolidation size (minimum capital, foreign-equity rules). This is what turns a two-party story into a structural one — and it is where you find whether consolidation is sector-inevitable while remaining transaction-improbable.

**8. Cost the buyer side honestly.** For every plausible acquirer, record stated position, financial capacity, and the control terms they will not concede. Feed acquirers who have announced they are exiting, or who are winding down, as *sellers* not buyers. A weakened acquirer halves the probability of a deal while doubling the reason one is wanted — record both directions rather than one.

**9. Run the transaction-mechanics void sweep.** See `references/transaction-void-and-valuation.md` for the vocabulary categories. Uniform absence across all of them is the finding; non-uniform absence tells you the pressure is real and the deal is not.

**10. Build the scenario space with explicit probabilities, then falsify it.** Include the status quo as an explicit scenario with the largest share — it is the base case in most deadlocked situations, and omitting it biases the brief toward drama. Add the rarely-discussed structural alternatives (a partial sell-down that preserves control; a market listing) because they often dominate on feasibility and are invisible in the chatter. Then write the falsification table: for each claim, the evidence that would disprove it, with the monitoring list of where that evidence would first appear (exchange announcements, regulator pages, rating-agency action language, fund portfolio disclosures).

**11. Deliver with the counter-narrative and the gaps.** A mandatory section arguing the strongest case *against* your conclusion, and an explicit gaps table stating what could not be verified and how that would change the answer.

## Second briefs and companion reports

When a follow-up brief builds on an earlier one ("now suppose the goal were different — what would have to change?"), re-read the first brief's findings under the new objective before writing. **Findings routinely invert.** A deadlock that reads as institutional failure under one objective can read as a *precondition* under another — an owner who cannot sell and has already demonstrated a multi-decade willingness to hold an underperforming asset is also the only ownership form that can absorb a long period of low returns. State the inversion explicitly; it is usually the most valuable paragraph in the second document, and it is only visible because the first document exists. Always name the first brief as the companion so the pair reads as one body of work.

## When part of the question is normative

Deal briefs on regulated, cultural or religious institutions often carry a normative layer (which structure is *legitimate*, not merely which is *legal*). Separate the two classes of question on the page:

- **Structural / measurable** — ownership, capital, contract mix, disclosure, verification. Yours to answer fully.
- **Normative / juristic** — which practice is permissible or preferred, what the correct ruling is. Belongs to the competent authority. Issue no ruling, take no side, and tag every such passage with its own marker so analysis is never mistaken for authority.

State a standing qualification at the front *and* in the closing frame — no ruling issued, no authority claimed, rulings reserved to the competent body. Where two recognised bodies hold different positions, report the divergence as a documented fact without adjudicating it: naming it is analysis, choosing a side is not yours to do. Then convert the normative word into countable properties and measure those — "compliant", "authentic" or "ethical" are unusable as targets until translated into shares, disclosures and verifications, and that translation is the brief's actual contribution.

## Report production gates

Long-form deal briefs are usually delivered as a PDF. The rendering mechanics belong to `forge-pdf-delivery` — follow it. The report shell (cover page, running footers, epistemic tags, callouts, stat strip, and the page-break discipline already wired in) is `templates/report-shell.html` in this skill: copy and modify it rather than rebuilding the CSS. Two gates specific to this class:

- **Every chart carries its own source line.** A figure without a source is an unverifiable claim wearing a picture's authority. Bake the attribution into the chart-rendering helper so it cannot be forgotten under time pressure.
- **Run the layout and ink gate after every build, then re-run it after any layout fix.** Enumerate pages, check section order in the text layer, count embedded figures, and flag any page under ~2.5% coverage as a layout break. The common cause is forced page breaks landing mid-figure — constrain the blocks rather than adding more breaks, and report the before/after page count as evidence the fix worked.

## Pitfalls

- **Never let the volume of coverage stand in for evidence that something is happening.** Ten years of reporting on a deal that never happens is evidence of a *condition*, not of momentum. Count attempts and completions explicitly; a completion rate near zero is itself the finding.
- **Check the publication date inside the article body before citing anything as current.** Outlet templates stamp the live site's date on every page, so stale coverage of a failed negotiation is structurally identical to coverage of a live one. The real date sits in the body text. Getting this wrong silently corrupts a scenario probability.
- **An extract that returns only site chrome is not an article.** If a fetch yields navigation, "most read" lists and ticker widgets but no body text, you did not get the article — do not summarise the furniture and do not treat that page as confirmation of anything.
- **Do not attribute motive.** "He wants to keep control" is F9. "Every attempt has failed on price and control, and the holding is unchanged" is the same insight without the attribution, and it survives audit.
- **Do not present the undisclosed as the known.** Where the instrument, the condition or the private positions cannot be sourced, record the gap and its effect on the conclusion rather than smoothing it with plausible detail.
- **Do not omit intent-free arithmetic that reframes the story.** The controller's effective interest, the target's share of the parent's profit, and the stake's value against the parent's market capitalisation are all derivable from filings and each one changes how the reader weighs the deadlock. Compute them before writing prose.
- **Do not state a probability without its anchor.** Every scenario probability needs one clause naming what it is anchored on (a completion record, a capital requirement, a control demand). Unanchored percentages read as precision and carry none.

## Verification before delivery

- [ ] Premise corrected (ownership structure, singular vs plural, subsidiary vs standalone)
- [ ] Condition ledger complete with origins, extensions, and current status
- [ ] Constraint's legal location identified, or explicitly recorded as not located
- [ ] Headline claim scored against every competing definition
- [ ] Price band built from named precedents, each edge attributed
- [ ] Transaction-void sweep run across all vocabulary categories
- [ ] Status quo present as an explicit scenario with the largest share
- [ ] Falsification table + monitoring list present
- [ ] Counter-narrative section present
- [ ] Gaps table present
- [ ] No rating, price target, buy/sell view, or intent attribution
- [ ] Every exhibit carries its own source line

## References

- `references/transaction-void-and-valuation.md` — the transaction-mechanics void vocabulary by category; how to read uniform vs non-uniform absence; valuation-band construction with the anchor asymmetry; the companion-brief inversion pattern.
- `templates/report-shell.html` — copy-and-modify A4 report shell: cover page, `@page` margin-box footers with page counters, `@page :first` cover suppression, epistemic tag classes, callout / verdict / danger / normative components, stat strip, and the page-break discipline that keeps runt pages out of long reports. Carries the render and QA commands in a header comment.

## Related skills

- `intelligence-brief-forge` — the four-layer framework (tersurat / tersirat / quantum / void), epistemic tagging, forge receipts, constitutional audit. This skill assumes those conventions.
- `forge-pdf-delivery` — the render pipeline, layout and ink gates, and the report shell template. Follow it for delivery.
- `deep-research` — multi-source research procedure and source-vetting fallbacks.
