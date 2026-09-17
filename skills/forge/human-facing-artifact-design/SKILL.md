---
name: human-facing-artifact-design
id: human-facing-artifact-design
version: 1.0.0
description: Use when forging PDFs, briefs, resumes, dossiers, logos.
owner: Hermes (curator-managed)
risk_tier: low
floor_scope: [F1, F2, F4, F6]
autonomy_tier: T1
tags: [artifact-design, pdf, reportlab, resume, dossier, brief, logo, audience, hierarchy, density]
---

# Human-Facing Artifact Design

> The human reads the artifact. The agent reads the source. Never confuse the two.

Load when asked to build any document a person will read — resume, interview brief, dossier, decision memo,
one-pager, encouragement note — or a logo/mark, or when a draft comes back rejected as too sparse, too dense,
or laid out for the wrong reader.

## 1. Audience decides the layout — split the two explicitly

Name the reader **before** laying anything out. There are two, and they want opposite things:

- **Human artifact** (resume, interview brief, encouragement note, decision memo, logo) — meaning first, confidence second, technical depth only as a backup annex. The reader must leave feeling something is now clear, not that they must study.
- **Technical artifact** (basin dossier, prospect review, interpretation record) — evidence first, epistemic tags mandatory, density is a virtue.

Never fuse them. Handing a technical dump to a human reader is a failure even when every fact is correct. For a human artifact the question is not "is this complete?" but "does the reader now know what to do or feel?"

Related: `FORGE-artifact-publisher` covers the EMD pipeline mechanics (HTML → Chrome headless → delivery). This skill owns the layer above it — who is reading, and how the page is weighted.

## 2. Attention hierarchy — visual weight follows consequence

Rank content by consequence *before* styling it. A page where a career-defining achievement renders with the same weight as a membership line has no hierarchy, and the reader will not retain the thing that mattered.

- The single most consequential item gets a dedicated band, box, or half-page block.
- Supporting items get compact rows.
- Trivia gets a comma-separated line, or is cut.

If you cannot name the one thing the reader must retain, the layout is not finished.

## 3. Density beats page count

A page limit is a density target, not permission to ship whitespace. A sparse two-page document reads worse than a packed one. When told "max N pages", produce N full pages of signal and verify by counting characters per page from the built PDF — never by eyeballing. Snippet in `references/pdf-and-image-toolchain.md`.

**Count ink, not just characters, when a document ends in a short block.** A closing epigraph, dedication, signature block or footer carrying a generous top margin will commonly overflow onto a page of its own. That page is genuinely sparse — on the order of one percent ink coverage — and reads to the recipient as a defect, because a near-empty final page looks like something failed to render.

Detect it by rasterising the built pages and computing dark-pixel share per page rather than trusting the page count; a spread where one page sits an order of magnitude below its neighbours is the signature of a stranded fragment, not of intentional design.

The fix is layout, not content: tighten the trailing block's top margin and line spacing so it joins the preceding page, and shorten its line lengths if that is what makes it fit. Do **not** delete the block, and do not pad it with filler to earn its page — filler on a closing page is more visible than the whitespace it replaced.

## 4. Care artifacts are not information transfer

When the artifact exists to steady a person — interview preparation, encouragement, hard news — the body is: their proven record stated plainly, what is actually at stake, what they control, and three or fewer instructions. Not a curriculum.

Probing the domain surfaces far more material than the person needs. The discipline is **selection, not compilation**. A twenty-page technical annex is a fine *annex*; it is not the artifact. Offer the annex as backup and lead with the short thing.

Do not answer a request for clarity with volume. When a person asks for confidence, handing them fifty more technical questions increases their load rather than transferring capability. Establish what state they are actually in before deciding what to build.

### Writing in the sovereign's own voice

When asked to say something *as* the user to another human, match his register: plain Malay/English code-switch, short sentences, no headers-as-therapy, no bullet list of feelings, no numbered framework where one sentence will do. Ground it in specific shared history rather than general encouragement — a named moment he witnessed lands; a generic pep talk does not.

- **Offer the shortest true form, then expect it to get shorter still.** He will cut a list down to one item. Give the short version first and name the longer one as available; never make him edit your draft down before he can send it.
- **Adopt his phrasing verbatim.** When he supplies his own line, it is better than any rewrite — it is his voice. Build around it, and never polish it back toward formal.
- **No strategy inside the message.** Positioning, visibility requests, risk hedging and leverage do not belong in text a human will read as coming from him; he strips them. If a point has to be made indirectly, say it to him as counsel outside the draft.
- **The strongest drafts are questions and plain statements.** A line that asks after the person, or states one plain fact about them, outperforms any structured argument — because it is the only thing he would actually say.
- **Match the form's language, but offer his.** If the form is in English, provide English and offer Malay. For anything personal or emotional he will usually want his own register.
- **Leave one slot for a real event, never invent the event.** Say where a concrete moment of his belongs; fabricating an anecdote in his voice is the one unrecoverable error here.

### Personal letters to a colleague, mentor or superior

A letter the sovereign sends to someone in his working life is a short, narrow artifact: it says
one thing he has wanted to say to that person. Do not build it like a reflective letter to family.

- **One to two pages.** The reader is a working adult who will read it once. A four-to-six page
  wisdom piece is the wrong form here.
- **Anchor on observed conduct, not adjectives.** There is no person-card and no shared family
  history to draw on, so the only usable material is conduct the writer personally witnessed,
  ideally repeated — how the person runs a meeting, how they treat people under pressure, what they
  do when someone is struggling. A named behaviour lands; "you are a great leader" does not.
- **Keep the sender's own business out of it unless he asks.** Not the restructuring, not the
  package, not the numbers, not the plan to leave. If a transition has to be signalled, the whole
  of it is one soft first-person line near the close — never analysis, never a status update.
- **Honorific and pronoun register.** Address by honorific ("Encik"/"Puan"), first person as the
  sovereign actually speaks, and none of the formal-correspondence furniture that turns a letter
  into HR correspondence.
- **Page furniture is: address line, body, signature, date. Nothing else.** No federation motto,
  no house sign-off, no footer credit. The motto is internal punctuation; on a letter to a real
  human it is a leak — the same rule that keeps organ names out of the body keeps the motto out of
  the footer.
- **When he hands over content as terse numbered fragments, fold them in — do not query them.**
  Mid-task shorthand is body copy he has already decided, not a spec to be clarified. Asking him to
  expand it spends the attention the artifact exists to protect.

### When the goal is to reach a person, hand over the primary source

If the artifact exists to move, thank or persuade a human, prefer the authentic original over a synthesis. Produce the real page, the real document, the real record.

A sourced original is evidence and cannot be accused of spin; a graphic built to persuade is visibly built to persuade. Sourcing also surfaces things nobody was looking for — an original page can carry a fact that changes the message.

**Rendering a true page from a source PDF:** locate the page from extracted text first, confirm the page number, then rasterise that page at 300 dpi so it is legible on a phone. Verify the rendered text against the extracted text before sending — a screenshot of the wrong page is worse than no artifact at all.

**Send one page, not a bundle.** If a comparison is worth making, send the authentic source first and hold the comparison back until he asks. A drift exhibit aimed at a person converts recognition into accusation.

### Zero system references in personal reflection artifacts

When the artifact is a personal reflection, life document, or wisdom piece — anything addressed to the human about his own life — the rendered text must contain ZERO references to any technical system: no MCP, no organs, no federation, no agents, no tools, no code, no architecture, no federation nodes. The human reads this, not the machine. 'No coding stuff' is the rule, not a suggestion. If the underlying work used 14 MCP tools and 3 subagents to produce it, the human never sees that. The artifact reads as if it was written by someone who sat with him and thought deeply — because that is exactly what happened, the tools are just the cognitive infrastructure.

**Pitfall:** Subagents asked to generate personal artifacts will default to describing their process or embedding system context if the prompt does not explicitly forbid it. The ban must be stated in the delegation prompt, not assumed.

## 5. Probe before quoting any number

Market, salary, price and status figures must come from a live probe in the same session, with source and date stated alongside the number. Reciting remembered figures is fabrication-adjacent and gets caught.

Where a domain convention differs from the obvious metric, report the convention rather than the raw metric. Example: Malaysian oil-and-gas compensation is quoted as a **total package** (base + bonus + allowances + rotation). Base alone is systematically low, and quoting it alone materially understates an offer — quote the package and say which components are in it.

**Read a figure off its row label, not its position.** Stacked tables put the prior-year cell of one series directly beneath the current-year cell of the next, so proximity is not identity. Match the number to its row label, then re-verify against both cells of that row. A cross-row misread is the first thing a checking reader finds, because they go straight to that page.

**When a release and a report give different values for the same metric, find the definitional reason before calling it a contradiction.** Two documents routinely define one metric differently and both are correct. Name which definition the artifact cites; never present the difference as a discrepancy, and never quietly pick one.

**Decompose an aggregate before it carries an argument.** State its composition, especially the cash/non-cash split. A number whose parts have not been separated cannot support a claim about money moving, and a large figure whose non-cash share is high collapses the argument built on it.

**Never annualise a positional delta into a rate.** A movement in a balance-sheet position can come from new borrowings, FX translation or declared distributions — none of which are operating burn. Check borrowings before using any cash delta as a run-rate.

**Assumed inputs stay visible.** A comparison built on an assumed unit cost reads as precise and cannot be checked. Label it an assumption inside the artifact or drop it — one unverifiable number contaminates the verifiable ones beside it.

**Never write an unattributable attribution.** "Analysts say", "sources indicate", "it is understood" — a claim with no named owner. If the source cannot be named, the claim does not ship; a checking reader finds that gap before they find the argument.

**When the reader returns corrections:** reopen the primary source — do not reconstruct your reasoning from memory. Do not defend; verify and report. Separate *I was wrong* from *the figure was right but the definition differs*. Correct even when it hurts your own conclusion, and say so. Move claims the reader independently verified out of the unverified column. Then issue a **new version with a change table** (previous value | corrected value | why) and a count of corrections — never a silent edit, because a reader already holding the earlier number cannot otherwise tell which document they are reading.

## 6. Iterate one file, then send once

Build and refine a single output path; do not generate v2/v3/v4 side by side and ask the user to choose. Each intermediate is noise in their inbox. Send the artifact when it passes the checklist, then iterate if rejected, and offer to remove superseded drafts rather than leaving several near-identical files behind.

**Distinction — drafts iterate in place, delivered artifacts version.** The rule above governs
*drafts*: several unshipped near-identical files are noise. It does not apply once an artifact has
been delivered and the reader returns corrections. A corrected artifact gets a **new version plus a
short table of what changed and why** — because a reader who already holds the earlier number
cannot otherwise tell which document they are reading, and because a visible correction is what
makes the surviving claims trustworthy. See `auditable-numeric-artifacts` for the full
receiving-an-audit procedure.

## 7. Pre-send checklist

```
[ ] Reader named, and the layout matches that reader (§1)
[ ] The one thing they must retain is the most visually weighted element (§2)
[ ] Every page is dense — chars/page counted from the built PDF, not eyeballed (§3)
[ ] No stranded near-empty final page — ink coverage measured per page (§3)
[ ] No number appears without a source and a date (§5)
[ ] No internal vocabulary in the rendered text (floor IDs, tags, tool names, PASS/FAIL)
[ ] No system references in personal reflection artifacts (§4)
[ ] Personal letters: no motto, no house sign-off, no sender's business unless asked (§4)
[ ] If reaching a person: authentic source used, not a synthesis; one page sent, comparison held back (§4)
[ ] Every number traceable to a primary source; anything secondary is labelled (§5)
[ ] Page count matches the limit, verified from the file
[ ] Text extracts cleanly (pymupdf / pdftotext returns real text, not empty)
[ ] One file sent, not several drafts (§6)
```

## 8. Toolchain

See `references/pdf-and-image-toolchain.md` for ReportLab paged-footer and section-band recipes, the density
verification snippet, Matplotlib gotchas that cost time, the geological cross-section orientation rule, and
Gemini image-model selection with the `responseModalities` contract for logos and marks.

---

*DITEMPA BUKAN DIBERI — the artifact is the proof.*