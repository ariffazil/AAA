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

**Default to a light palette.** White/near-white ground, dark text. Arif explicitly stated (2026-09-18, applies to every governance dossier since): *"I hate black dark background in pdf."* Dark decks are for screen; governance dossiers are for reading. **Do not ship a dark-theme governance cover or pull-quote box, even when the subject is institutional and serious.** This applies even to "forensic" dossiers on corporate misconduct — the topic is heavy, the document must not be.

Working palette for a governance dossier (validated by vision inspection on SEARAH dossier 24 Sep 2026):

| Role | Hex |
|---|---|
| Ground | `#efeae0` (warm bone) or `#ffffff` |
| Body text | `#12100e` (≈16:1 contrast) |
| Heading / table header | `#8c1818` deep brick — white text on it ≈9:1 |
| Accent rule / stamp | `#a08540` antique brass |
| Evidence tag | tinted badges — green=UKUR, amber=REPORTED, red=INFERENCE, blue=STATEMENT |
| Zebra row | `#e7e0d2` (lighter than ground) |
| Pull-quote / verdict box | `#f4eee2` cream interior with brick-red left rule. **NOT black/ink background.** |

Use WeasyPrint for portrait-A4 governance dossiers. CSS `@page { size: A4; margin: 19mm 17mm 21mm 17mm }`. Cover page uses `@page:first { margin:0 }` so the cover bleeds edge-to-edge — but the cover *ground* is still light (e.g. `#efeae0` or `#1c1c1c` only when Arif has asked for dark, which he has not). Tagged evidence in table with `tr { page-break-inside: avoid }`. Timeline as CSS-styled div with border-left and dot markers. Analyst verdict box is a light cream block with a brick-red left rule (4px solid) — never a dark inverted box.

Example cover structure (light palette):
```html
<div class="cover" style="height:297mm;width:210mm;background:#efeae0;color:#12100e;">
  <div class="rule-top" style="height:2px;background:#8c1818;width:100%"></div>
  <div class="stamp" style="border:1px solid #a08540;color:#a08540">FORENSIC ANALYSIS</div>
  <h1 style="color:#12100e">Title <em style="color:#8c1818">Subtitle</em></h1>
  <div class="one">Executive thesis paragraph</div>
  <div class="byline">Documented by / Motto</div>
</div>
```
