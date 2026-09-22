# Governance Mapping Pattern — Power, Vendors, Timing

Use when mapping corporate governance risk: power consolidation, conflict-of-interest chains, and timing convergence in a GLC or sovereign-controlled entity.

## When to use

- CEO/Board appointments that concentrate operational + governance power in one person
- Vendor relationships where an executive has a family/personal link
- Asset transfers that coincide with litigation or regulatory proceedings
- Any analysis where the individual events are unremarkable but the pattern is not

## The four-pattern framework

| Pattern | What to map | Key question |
|---------|-------------|-------------|
| **Power consolidation** | Who holds operational, governance, and vendor-network power? Is it concentrating? | Who cannot be removed? |
| **Asset transfer architecture** | What assets are moving, to whom, and outside whose jurisdiction? | What is shielded from whom? |
| **Vendor governance chain** | Executive → family link → vendor → contract. Is it disclosed? Recused? | Who approved, and did they declare? |
| **Timing convergence** | Do all patterns peak in the same window? Do they share a common driver? | Coincidence requires independence. If events share a beneficiary, they are coordinated. |

## Epistemic tag system for analyst documents

Every claim carries a tag. No exceptions.

| Tag | Meaning | When to use |
|-----|---------|-------------|
| VERIFIED / UKUR | Primary source, checkable | Official press release, filing, court record |
| REPORTED | Media-reported, not independently confirmed | Industry source via Bloomberg/Edge/FMT |
| INFERENCE / ANDAI | Pattern reading, not proven | "X benefits from Y" — logical but unproven intent |
| GAP / UNKNOWN | Explicitly not verified | Internal governance records, Board minutes |

**Rule:** If an analyst can't tell from the tag whether a claim is fact or interpretation, the tag is wrong.

## Mandatory sections in a governance dossier

1. **Executive summary** — thesis in one paragraph, four patterns named
2. **Timeline** — every event with date, description, source, and tag
3. **Financial surface** — numbers that the market sees, with context the market misses
4. **What is not said** — gaps explicitly listed as UNKNOWN/GAP
5. **Analyst verdict** — rating implication, watch items, upgrade criteria, downgrade criteria

**The "what we would need to downgrade this to noise" section is mandatory.** A dossier that only argues FOR its thesis is advocacy, not analysis. Offering the falsification path is what makes it credible.

## Pitfalls

- **Do not allege illegality from public sources alone.** Governance risk ≠ criminal conduct. State the pattern, name the questions, note what internal records would answer them. The reader draws the legal conclusion.
- **Do not confuse timing with causation.** "X happened after Y" is timing. "X happened because of Y" requires evidence of mechanism. Present timing; note the common driver; label the causal claim INFERENCE.
- **Weight counter-signals in the same breath as findings.** If the company also did something that weakens your thesis, present it immediately. An argument that has survived its own counter-evidence is credible; one that hides it is advocacy.
- **Check whether the counterparty's filings carry structure the host-country release does not.** A listed counterparty (EnQuest, Aramco, Eni) must disclose in SEC/home filings what PETRONAS need not publish in Malaysia. Always check the counterparty's filing before concluding on deal terms.

## Render pipeline

Use WeasyPrint for portrait-A4 governance dossiers. CSS @page rules for cover page (dark background, @page:first { margin:0 }). Pull-quote boxes as div.pull with dark background. Tagged evidence in table with tr { page-break-inside: avoid }. Timeline as CSS-styled div.timeline with border-left and dot markers. Analyst verdict as dark div.verdict box.

Example cover structure:
<div class="cover" style="height:297mm;width:210mm;background:var(--ink);...">
  <div class="stamp">FORENSIC ANALYSIS</div>
  <h1>Title <em>Subtitle</em></h1>
  <div class="one">Executive thesis paragraph</div>
  <div class="byline">Documented by / Motto</div>
</div>
