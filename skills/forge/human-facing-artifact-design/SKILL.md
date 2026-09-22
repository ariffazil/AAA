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
capability_tier: fed-reasoning-heavy
ecology_state: WARM
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

**A technical artifact's figures are part of the argument, not decoration.** When the reader is a domain specialist, prose and tables alone come back with a direct instruction to add the maps and sections. A geologist reading a basin or asset dossier expects the regional location map, at least one cross-section, and the stratigraphic column wherever reservoir, seal or velocity are discussed — ship them inside the document, at the density the text implies. Where the supporting geometry is not in the public record, **still draw it and mark it** `schematic` / `indicative` / `not to scale` in both the figure subtitle and the caption: an absent map costs more credibility than a correctly-labelled schematic, and the label is what keeps the schematic admissible. Figure production and its vision-QA loop live in `geological-figure-production`. The rule generalises: a specialist reader judges the artifact partly on whether it carries the instrument of the discipline it claims.

**Third case — the internal-audience artifact.** When the reader is the sovereign and the subject *is* his own system, neither rule above applies cleanly. Internal vocabulary is the payload, not a leak, and the failure mode inverts: stripping the terms that carry the meaning destroys the artifact. What such an artifact owes instead is its epistemic status rendered on its face — an assessment that was never ratified must say so in the frame. See `visual-artifact-delivery` §4c.

**Fourth case — the numeric-averse reader.** When the reader has signalled that figures themselves are the barrier ("aku pening matematik", "aku lemah matematik", "aku x faham hang tulis number", "cuba hang lukis"), a correct table is an unreadable artifact. The barrier is the *channel*, not the content, and repeating the number more slowly never fixes it. Re-render as a picture:

- Pick the single contrast that carries the lesson — two cases side by side beats a twelve-row scenario table.
- One panel per idea, three panels maximum. Every panel labelled in words. A number may appear inside the figure; an equation may not.
- Name the two things to look at in the caption, in ordinary language. The reader must not have to derive what the picture shows.
- Keep the accompanying text to the conclusion and the one mechanism sentence. Do **not** restate the figure as prose — that trains the reader to skip the image.
- On any comparison, show the **baseline** as well as the result. A score presented alone reads as skill; a score beside its trivial baseline is the actual finding.
- Convert PNG → JPEG (quality ~94) and deliver with `MEDIA:/abs/path.jpg`.

A correct answer in the wrong channel is still a failure to communicate — track the channel signal the same way you track an audience.

**Fifth case — one subject, two readers, two delivered artifacts.** When the ask is to extract lessons from a body of material (an essay series, a corpus, another operator's failure, a doctrine), the deliverable is a **pair**, and the two documents are not the same document twice:

- **The operational artifact** (Markdown, for agents) — the rules, pitfalls and imperatives, the concrete thing to do differently, with each adopted rule traceable to the source that earned it. It is scanned for compliance, so it carries no reflection, no narrative and no rhetorical framing.
- **The reflective artifact** (PDF, for the human) — the tension, the question that stays open, the part that must not be resolved, and what the subject means for the reader's own posture. It is read slowly, so it carries no instruction, no checklist and no imperative voice.

Keep the registers clean and let neither summarise the other — the agent artifact is the wrong place for reflection, the human artifact is the wrong place for a checklist, and collapsing the two into one document serves neither reader. The reflective piece **fails when it resolves the contradiction it exists to hold**: a document that settles a live question has done the reader's thinking for them and removed the thing they were meant to sit with. State the competing readings in full, say plainly that both may be true at once, and leave the resolution to them. The two artifacts may share a subject; they must not share a voice.

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

**On a dark-background document the measure inverts.** "Ink" is the share of pixels that *differ from the dominant background*, not the share that are non-white — a white-page threshold applied to a dark page reports every page as near-full and hides exactly the stranded fragment you are looking for. Sample the modal pixel value first, then count deviation from it.

**A page count roughly double the number of designed blocks means every block is spanning two pages.** The usual cause is a container taller than the printable box, so the block breaks and its tail lands on the next page. Compare the container height against the `@page` box before touching content — the fix is geometry, and adding or trimming text will not find it.

The fix is layout, not content: tighten the trailing block's top margin and line spacing so it joins the preceding page, and shorten its line lengths if that is what makes it fit. Do **not** delete the block, and do not pad it with filler to earn its page — filler on a closing page is more visible than the whitespace it replaced.

### Recurring artifacts: separate the POOL from the PUBLISHED surface

When an artifact is generated on a schedule — a daily card, a digest, a pulse, a dashboard — and it
comes back rejected for being unreadable (`too chaos`, `signal only`, "I can't find anything"), the fix
is **not** to delete content. Two different objects have been collapsed into one file:

- **POOL** — every candidate the search produced, with sources, tiers and provenance. This is
  RESEARCH. Keep all of it, in the file.
- **PUBLISHED surface** — the handful of lines the reader actually scans. This is the SELECTION.

A wide pool and a narrow published surface is the point: the pool proves the search was real, the
surface proves the judgement was. Delete the pool instead and nothing downstream can tell whether the
surface was chosen or merely left over.

**Measure the narrowing; do not assert it.** Count the visible text nodes and the characters a reader
must scan, before and after, and state both. A real case: **57 nodes / 5,973 chars → 16 nodes / 1,498
chars**, with nothing removed a reader could act on. What went was scaffolding only the machine needed
— category names, row numbers, the reader's name stamped on every row, a source line under each cell,
decorative quotes, and a footer restating the structure the page already showed.

**The published surface carries no machine scaffolding.** No tier or category labels, no row numbers,
no per-line source strings, no structural footer. Provenance is recorded for audit and *never printed*
— a source line under every item is the fastest way to make a card read as a log. If the artifact has
a duality worth keeping (one subject, two readers), carry it with a colour bar or a position, not by
stamping a name on each row.

**Narrowing is where a reader gets dropped — gate it.** The first lines to vanish from a "signal only"
pass are the ones whose subject is rarest in the day's source material, which may be the entire lane
of one of the readers. So the narrowing gets its own refusal list: a minimum and maximum line count, a
per-line length ceiling, no frozen counts written into prose, no private markers, no two lines about
the same event, and — critically — **at least one line surviving for each named reader's standing
interest**, plus a check that not every line belongs to one reader. Write the control that breaks each
rule and confirm it actually FIRES before trusting the check.

**A register rule that only warns is a debt, not a control.** If the generator flags machine
vocabulary in a human-facing line but still ships the line, the register is only partly enforced —
do not report it clean to the principal. Say which items still leak and that the check is advisory.

**Two render styles must not share a filename.** When one generator can emit two layouts of the same
period (a full grid and a narrow signal card), both share the same period label — so unless the
filenames differ by style, the second render silently overwrites the first's stable output, which is
the exact path a delivery contract names. Suffix by style, and refuse to render a style whose input
section is missing rather than falling back to the other layout: an artifact that quietly renders
something other than what was asked is lying about itself.

### Recurring artifact shape — anchor on a weekly template, not a per-issue structure

A weekly brief (Monday, Friday, end-of-month) shipped to the same reader or reader-pair becomes
muscle memory after two or three issues. The reader learns the section order, knows where their
"must-read this morning" line is, and the artifact does not need to re-justify itself. Encode the
recurrence on the first issue:

- **Lock the table of contents and section order from issue one.** A Monday market-and-policy brief
  that opens with markets then energy then rates then PETRONAS then war then AI then a "what to do"
  section will keep that order even when one week's news is dominated by an unexpected story —
  the unexpected story fits the existing section, it does not generate a new one. A reader who
  sees "your Monday brief has eight sections" stops scanning; a reader who sees "this brief
  has nine sections this week and only three last week" does not.
- **Mark the recurring vs the variable visibly.** A consistent small grey "WEEKLY" mark on the
  section headers that are always there, and an un-marked bold heading for whatever *this* issue
  changed. The reader learns to scan the un-marked headings first.
- **The reader's "what do I do" section is the most stable of all.** It is the only section
  guaranteed to be useful even when every other section is wrong. Write it as a numbered list of
  actions that survive any news week, then this week append the issue-specific delta. The reader's
  trust in the artifact sits on this section being dependable.
- **Mid-build pivots are real, and the template is what absorbs them.** A reader may ask, mid-build,
  "add more on PETRONAS" or "include the MSS chapter" — the answer is to fold the addition into an
  existing section, not to invent a new one. The artifact's structure has to be loose enough to
  accept a fifth or sixth paragraph inside an existing section without breaking the page geometry.

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

### A reader who communicates by forwarding, not by writing

Some readers never compose prose. They send a quoted card, a screenshot, a forwarded article, or a
three-word answer, and that IS the message. Two rules follow, and both are about the reader rather than the
artifact:

- **Do not credit them with authoring what they forwarded.** A quote they pasted is a signal that the idea
  landed with them — not their own writing. Replying "you wrote that yourself" is a factual error they will
  notice, and it reads as flattery aimed at someone who did not do the thing. Respond to the idea inside the
  quote; leave the attribution alone.
- **Keep replies to them short regardless of how much there is to say.** Length is a register error for this
  reader, independent of content, and it is detectable: "do you think I'm bothered to type that much?" A
  multi-paragraph answer to a forwarded quote is the same failure as a technical dump to a non-technical
  reader — the channel is wrong even when every sentence is correct. Compress to 2–4 lines and let them pull
  for more.

Read the channel the same way you read the audience: a reader who sends images and quotes is asking to be
answered in kind, not to be handed an essay about their own message.

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

### Health, rehab and training artifacts addressed to a named person

A document built for one person about their own body — a rehab timeline, a return-to-work plan, a training block — is a care artifact with an extra failure mode: it can be complete against the *previous version* and still be incomplete against the *person*.

- **Carry the constraint that actually governs their behaviour, not the headline diagnosis.** A person's file usually holds more than one finding, and the secondary one is often the binding one — a repaired structure heals slower than a reconstructed one and carries a lower load ceiling. An artifact covering only the flagship injury reads finished while spending the reader's effort on the wrong constraint. Before shipping, diff the document against everything the person has actually disclosed, not against the draft you are revising.
- **Never resolve the clinician's unknown for them.** Clearance timing, load ceilings and protocol progression belong to the treating professional. Put each unknown in the artifact as a written question the reader takes to that professional, and say plainly that the clinician's protocol wins. A plausible invented week number is the one error in this genre that causes harm.
- **The reader is the person, not the principal.** No internal vocabulary, no house sign-off, no federation footer. The whole furniture is a source line and a plain "not medical advice" line.
- **Ship a ladder, not a verdict.** Stage the progression — allowed now, gated, destination — so the reader can place themselves. A gated stage presented as a stage reads as guidance; the same gate presented as a bare refusal reads as punishment.
- **Lead with what changed.** When the reader already holds the earlier version, the top of the new one says what moved and why, before any of the standing content.

### Résumés and career documents that leave the institution

A CV is read by a stranger deciding whether to spend money on the subject, and it travels outside every boundary the source record sits behind. Two things dominate: the record must be checkable, and nothing restricted may travel with it.

- **Sweep the source record for access-class flags before drafting.** Personnel and project files carry entries marked restricted, held, or incident-class. Those do not enter a document a third party will hold — not paraphrased, not softened, not implied by a date the reader can look up. Confirm the exclusion back to the principal so the absence is never later read as an oversight.
- **Zero operational numbers.** Flow rates, volumes, pressures, acreage or well-test results belong to the institution, not the individual, and their presence is what makes a CV unsafe to forward. Close with one plain line stating the document carries no proprietary data.
- **Rank by what the reader is hiring for, not by what the subject is proudest of.** When the subject carries two identities — the profession and a personal initiative — the artifact is written for the reader's vacancy. Lead with the professional record; give the personal initiative a short block below it, explicitly labelled a personal project and not an employer one. Equal weight reads as a person whose attention is elsewhere, the opposite of the needed conclusion.
- **Every entry carries what it demonstrates, not only what happened.** One line of fact, one line of capability proven. A list of names with no demonstrated capability cannot be priced by the reader.
- **A selected-record block may lead the chronology.** For technical or research careers, the evidence above the employment history is often stronger than dates first — keep the chronological history beneath it for the reader verifying continuity.
- **Never derive a field the record does not hold.** Contact details, graduation year, start date, job titles. A résumé is the highest-consequence place to guess and the easiest to check; ship what is on file and return the gaps to the principal as a short confirm-list. Do not ship a plausible number with a caveat attached — the number is the part that gets read.
- **When the principal names an application date, time the artifact to it.** A posting deadline in the message is the reader's constraint, not background detail — say which version is which if an earlier one is already circulating.
- **A short or low-status attachment earns a line when a named technique transferred out of it.** An internship, secondment, or on-the-job stint the subject dismisses as "I did nothing there" is often the origin of a method they still use — a play analogue, a workflow, a tool habit. Record the **transfer**, not the role: name the technique and where it was later applied, and keep the donor organisation's proprietary specifics out. The subject under-reports this and will not volunteer it; ask before writing it off, because "I did nothing" and "nothing here is recordable" are different claims.
- **The document carries no compensation figure.** A number in the CV caps the negotiation before it opens. Position the band instead by naming the *scope of accountability* — an asset-wide remit rather than a single prospect, a portfolio rather than a field, a multi-year programme rather than a campaign — because that is what a reader uses to place a level. Keep the arithmetic for the conversation and, if asked to reason about a target, do it outside the artifact.
- **Describe a self-authored project by its verifiable surface, never by its vanity metrics.** When the subject's personal initiative is part of the pitch, probe its public claims live in the same session — registry version and licence, repository description, whether the live endpoint actually answers — and cite only what resolves. Star counts, follower counts and download totals invite the reader to price the person by the smallest number on the page; a published package, an open licence and a reachable service do not.
- **Where the subject is a systems thinker rather than an implementer, write that as the competence being hired.** An architect who specifies and then delegates implementation is exercising exactly what a senior technical post demands — precision sufficient that the work can be built *and audited* by somebody else. Name the method (architecture, ontology and constraint design by the subject; implementation through governed harnesses) instead of leaving a gap the reader will fill with "cannot code".

## 5. Probe before quoting any number

Market, salary, price and status figures must come from a live probe in the same session, with source and date stated alongside the number. Reciting remembered figures is fabrication-adjacent and gets caught.

**Build the provenance manifest into the artifact itself, not only into your reasoning.** A number-bearing document can be refused at write time by the house write gate when its payload asserts a critical variable with no resolvable source — and the gate is satisfied by provenance, not by rewording. Beyond clearing the gate, an in-artifact `SOURCES` / `EVIDENCE MANIFEST` block mapping every load-bearing figure → URL → access timestamp is what makes the document re-checkable months later by a reader who was not in the session. A closing "figures from public reports" line does the opposite: it grants authority to every number in the artifact, including the unsourced ones, while reading as rigour.

Where a domain convention differs from the obvious metric, report the convention rather than the raw metric. Example: Malaysian oil-and-gas compensation is quoted as a **total package** (base + bonus + allowances + rotation). Base alone is systematically low, and quoting it alone materially understates an offer — quote the package and say which components are in it.

**Tier the source before quoting a benchmark.** For pay, market and status figures the *sample* matters more than the headline. Rank what you hold: a structured industry pay guide published as role × experience × company tier outranks a specialist salary survey, which outranks a job-board aggregate, which outranks a forum anecdote. Job-board aggregates are the trap — they average every listing sharing one job title, so a "geologist" figure folds quarry, GIS and site work into a single number and lands far below the specialist band, and a survey quoting an annual figure for a role the market pays monthly invites a 12× misread. State the tier beside every number, and state what it excludes: in resource industries, offshore, hardship and hazardous-duty allowances commonly run 40–60% of take-home and are quoted separately from base, so a base-only comparison understates the offer by roughly half. Where several sources disagree by a factor of two, the disagreement is a sampling statement — say which tier you are quoting and why the others are not comparable, rather than averaging them.

**Read a figure off its row label, not its position.** Stacked tables put the prior-year cell of one series directly beneath the current-year cell of the next, so proximity is not identity. Match the number to its row label, then re-verify against both cells of that row. A cross-row misread is the first thing a checking reader finds, because they go straight to that page.

**When a release and a report give different values for the same metric, find the definitional reason before calling it a contradiction.** Two documents routinely define one metric differently and both are correct. Name which definition the artifact cites; never present the difference as a discrepancy, and never quietly pick one.

**Separate a freshness gap from a contradiction before resolving either.** Two sources quoting one instrument can disagree because one of them is *older*, not because one is wrong — a same-session local reading against a web figure still quoting the previous close is a time difference wearing the costume of an error. Compare the timestamps first; quote the fresher and label the age of the other. Where currency genuinely cannot be established (different sessions, an unclosed market, an ambiguous timezone), report both values with their timestamps and say the discrepancy is unresolved — never average them into a middle figure, and never silently choose one.

**Decompose an aggregate before it carries an argument.** State its composition, especially the cash/non-cash split. A number whose parts have not been separated cannot support a claim about money moving, and a large figure whose non-cash share is high collapses the argument built on it.

**Never annualise a positional delta into a rate.** A movement in a balance-sheet position can come from new borrowings, FX translation or declared distributions — none of which are operating burn. Check borrowings before using any cash delta as a run-rate.

**Assumed inputs stay visible.** A comparison built on an assumed unit cost reads as precise and cannot be checked. Label it an assumption inside the artifact or drop it — one unverifiable number contaminates the verifiable ones beside it.

**Never write an unattributable attribution.** "Analysts say", "sources indicate", "it is understood" — a claim with no named owner. If the source cannot be named, the claim does not ship; a checking reader finds that gap before they find the argument.

**No borrowed-prestige vocabulary in the rendered text.** A domain name is not evidence of rigour. Applying quantum-mechanical, thermodynamic or information-theoretic vocabulary to an ordinary decision — where none of the underlying measurement cost has been paid — inflates how well-founded the claim looks while doing no work. When the reader asks for "the quantum solution", "APEX theory", or an entropy reading of a decision, supply the legitimate form of the mathematics with its assumptions stated (a diffusion envelope `sigma*sqrt(t)`, a Kelly growth curve, a first-passage probability, a measured sensitivity/specificity pair) and name the retraction if a borrowed term has already been used in the thread. Canonical form: **a label must do work, not borrow prestige.** Where a term is retained — Shannon entropy with a defined distribution, metabolism with a biological substrate, field/gradient in a defined mathematical space — it ships with the structure that makes it precise; everywhere else drop the metaphor and keep the goal.

**Answer a claim of predictive skill with a test, not an argument.** When the reader asserts that a
chart, a signal, an organ or a model can forecast an outcome — "technical analysis can tell when a
company will die", "the model gives high-quality calls" — do not debate it and do not agree with it.
A dispute about predictive power cannot be settled in conversation, because whoever already knows
the outcome will find their pattern every time. Build a blind test instead: anonymised cases, seeded
labels, the answer sealed to a separate file, and the score published beside its trivial baseline.
Report the falsification of your OWN hypothesis first. The reader learns more from one honestly
scored test than from any amount of analysis, and a result that dissolves a confidently-held belief
is still the correct deliverable. Procedure and scaffold: `blind-prediction-testing`.

**A citation must resolve, not merely appear.** A citation-shaped string that 404s is not a source — shape is not witness, and a document full of dead references reads as authoritative while being uncheckable. Run `scripts/verify-citations.py` over the artifact before release and replace or drop anything that fails. Status semantics: `2xx`/`3xx` resolve; `403`/`405`/`429` mean *the host answered* — the resource exists and is refusing HEAD, so it counts as live; `404`/`410` and no-response are real failures. Verify against the **source file before the build**, not only the rendered artifact, because a dead link found after a build costs the whole build.

**When a publisher blocks automated retrieval, resolve the DOI's metadata instead of dropping the citation.** A `403` from a paywalled publisher, a JavaScript interstitial ("Just a moment…"), a CAPTCHA on a mirror, or a gateway error from an aggregator all mean *retrieval failed*, not *the source does not exist*. Query the registered metadata directly — `https://api.crossref.org/works/<doi>` returns JSON with no browser: title, journal, volume, issue, pages, DOI, the full author list and the abstract. Two things beyond bare existence come out of it, and both change the artifact:

- **Author affiliations are provenance.** A paper whose corresponding author sits at an operating company is that company's own account of the geology, not independent scholarship — a materially different thing to cite in a peer or competitor dossier, and worth saying in the caption rather than presenting it as neutral literature.
- **A confirmed DOI settles version questions.** Where a source is described loosely, the registered year, volume and page range are the version of record; cite those rather than a retrieval date or a working-paper label.

Never soften a citation to "a study found" because the page would not load. Resolve it or drop it — an unattributable attribution is already banned by this skill's own rules.

**An absence in the record ships as a named gap, not as silence.** Where a fact the reader will want does not exist in any source you can reach — a licence or contract term, a resource number, a headcount, a spud or first-gas date — record it in the artifact as an explicit *not found* / *not published* row and say why it matters, rather than omitting it and leaving the reader to notice the hole. Omitting it makes the document look complete and makes the reader wrong about their own exposure; naming it turns a gap into a question somebody can go and answer. Keep the two states distinct: **no public evidence is not evidence of absence** — write "no public evidence found" and give it a lower confidence, never "does not exist".

**Report the count you measured, not the count you intended.** If a register holds 30 pointers, say 30; a stated count that disagrees with the list beside it is the first thing a checking reader notices, and it discredits the entries that are correct.

**When the reader returns corrections:** reopen the primary source — do not reconstruct your reasoning from memory. Do not defend; verify and report. Separate *I was wrong* from *the figure was right but the definition differs*. Correct even when it hurts your own conclusion, and say so. Move claims the reader independently verified out of the unverified column. Then issue a **new version with a change table** (previous value | corrected value | why) and a count of corrections — never a silent edit, because a reader already holding the earlier number cannot otherwise tell which document they are reading.

## 6. Iterate one file, then send once

Build and refine a single output path; do not generate v2/v3/v4 side by side and ask the user to choose. Each intermediate is noise in their inbox. Send the artifact when it passes the checklist, then iterate if rejected, and offer to remove superseded drafts rather than leaving several near-identical files behind.

**For visual-identity work the failure mode is louder.** A logo, avatar or mark that loops
through eleven or six variants side-by-side is not iteration — the reader cannot tell which
variant is your pick from the file list alone. Build a contact sheet at small sizes (40 and 28 px)
so the choice is made on the evidence, name the one you're sending as the recommendation, ship the
contact sheet as the supporting evidence, and stop. The reader comes back with "yes" or "no" and a
reason — never with a list of files to pick from. A pick that splits a word (e.g. a five-letter
brand name rendered as a two-line stack) is a fundamental typographic error, not a stylistic
choice; if the only way to fit the word at small size is to break it, the fix is a narrower font,
not a wider container. Measure the inner-area coverage as a fraction — a single-line word in a
circular badge will measure around 7–8%; if it is above 15% the word is dominating the disc.

**"Bagus. Belajar drpd kesilapan." is a checkback signal.** When the reader — after rejecting the
artifact, after the redo, after you explained what you learned — says the artifact is good and to
remember the lesson, that is the moment to capture the lesson, not later. The closed feedback loop
is the only point at which the reader's correction is no longer being argued about and the rule
itself can be sealed.

**Skill-edit "success" is not the same as the bytes landing.** When this skill's own curve-of-fitting
section was edited mid-session, `skill_manage` returned success and the agent reported the
recording — but the file did not change. A downstream skill store had swept the SKILL.md while
the symlink and the catalog survived, so reads via skill_view kept returning the old body. Before
relying on any skill edit: read back the resolved path and grep for a distinctive phrase you just
added; if the target directory holds only `liveness.json`, the SKILL.md was swept — restore it
and re-issue the lesson, do not report it recorded.

**Distinction — drafts iterate in place, delivered artifacts version.** The rule above governs
*drafts*: several unshipped near-identical files are noise. It does not apply once an artifact has
been delivered and the reader returns corrections. A corrected artifact gets a **new version plus a
short table of what changed and why** — because a reader who already holds the earlier number
cannot otherwise tell which document they are reading, and because a visible correction is what
makes the surviving claims trustworthy. A change table covers **omissions as well as errors**: name what the earlier version left out and what it changes for the reader. An error is visible to anyone who checks the figure; an omission is invisible until it costs something. See `auditable-numeric-artifacts` for the full
receiving-an-audit procedure.

**Verification that did not return is not a pass.** When a QA call fails, times out, or comes back
without a verdict, the artifact is *unreviewed*, not *clean* — re-issue the call, and if the deliverable
must ship first, name the unverified item to the reader and invite them to flag it. Reporting an
unchecked figure or page as reviewed is the exact failure the check existed to prevent, and the reader
has no way to tell the two states apart from the document alone.

## 7. Pre-send checklist

```
[ ] Reader named, and the layout matches that reader (§1)
[ ] If the reader is numeric-averse: figures rendered as a picture, not a table, with the baseline shown beside the result (§1)
[ ] The one thing they must retain is the most visually weighted element (§2)
[ ] Technical artifact for a specialist reader: the discipline's own figures are present (map / cross-section / column), and every schematic element is labelled `schematic` / `indicative` in subtitle and caption (§1)
[ ] Every page is dense — chars/page counted from the built PDF, not eyeballed (§3)
[ ] No stranded near-empty final page — ink coverage measured per page (§3)
[ ] Recurring/dense artifact: pool kept in the file, published surface narrowed — and the narrowing MEASURED (nodes/chars before and after), not asserted (§3)
[ ] Every named reader still has a line surviving the narrowing; no surface serves only one reader (§3)
[ ] Published surface carries no machine scaffolding — no category tags, row numbers, per-line source strings or structural footer (§3)
[ ] Any machine-vocabulary check that only warns: reported as a debt, not claimed as enforced (§3)
[ ] Two render styles of one period write different filenames, and a missing input section refuses rather than falling back to the other layout (§3)
[ ] No number appears without a source and a date (§5)
[ ] No borrowed-prestige vocabulary (quantum / entropy / thermodynamics) applied to an ordinary decision — the maths stands on its own, or the term is dropped (§5)
[ ] A claim of predictive skill was tested blind and scored against its trivial baseline, with any sampling limitation stated on the artifact — or the claim is marked untested (§5)
[ ] No internal vocabulary in the rendered text — for an OUTSIDE reader (floor IDs, tags, tool names, PASS/FAIL). For an internal reader whose subject IS the system, internal vocabulary is the payload (§1)
[ ] No system references in personal reflection artifacts (§4)
[ ] Personal letters: no motto, no house sign-off, no sender's business unless asked (§4)
[ ] Person-specific artifact: diffed against everything the subject has disclosed, not against the draft being revised — the binding constraint is carried, not just the headline one (§4)
[ ] Health/rehab artifact: no clinician timeline invented; unknowns ship as questions for their professional; furniture is a source line plus a "not medical advice" line (§4)
[ ] Résumé/CV: restricted-class entries confirmed absent and reported to the principal; no operational numbers; a provenance/cleanliness line closes the document (§4)
[ ] Résumé/CV: every field absent from the record returned as a confirm-list — nothing invented and shipped (§4)
[ ] Résumé/CV: no compensation figure anywhere in the document — level positioned by scope of accountability instead (§4)
[ ] Résumé/CV: self-authored project cited by verifiable surface only (registry, licence, live endpoint probed this session) — no star, follower or download counts (§4)
[ ] Benchmark figure quoted with its source tier named, and what the number excludes (allowances, non-cash, rotation) stated beside it (§5)
[ ] If reaching a person: authentic source used, not a synthesis; one page sent, comparison held back (§4)
[ ] Every number traceable to a primary source; anything secondary is labelled (§5)
[ ] Every cited URL probed and resolving — `scripts/verify-citations.py`, run on the source before the build (§5)
[ ] Citations behind a paywall or bot-block: DOI metadata resolved via Crossref, and any operator affiliation read and reflected in how the source is framed (§5)
[ ] Any stated count of sources/items matches the list beside it — measured, not intended (§5)
[ ] Page count matches the limit, verified from the file
[ ] Text extracts cleanly (pymupdf / pdftotext returns real text, not empty)
[ ] No stranded near-empty page, measured on the rendered pages (§3)
[ ] Rendered pages actually LOOKED at, not just measured — composition defects (a top-heavy page, an unanchored footer, a stamp floating mid-page) are invisible to page counts and ink percentages (§3)
[ ] One file sent, not several drafts (§6)
```

## 8. Toolchain

See `references/pdf-and-image-toolchain.md` for the build-path decision (browser print vs ReportLab), the browser-print recipe for HTML that declares its own `@page` rule, ReportLab paged-footer and section-band recipes, the density
verification snippet, the in-memory ink-coverage sweep, Matplotlib gotchas that cost time, the geological cross-section orientation and figure-integrity rules, the Natural Earth regional-basemap recipe, and
Gemini image-model selection with the `responseModalities` contract for logos and marks.

See `references/well-log-and-subsurface-figure-recipes.md` when the artifact carries well data or a
regional map: the LAS parsing contract (mnemonic unit suffixes, data-column vs curve-header
reconciliation, null sentinel, metre/feet detection), log-track and petrophysics panel layout including
the twin-axis RHOB/NPHI track, the single-axes multi-well correlation pattern, a real Natural Earth
basemap without GeoPandas, and the subsurface number-integrity rules — report the computed zero, plot
the sensitivity of whatever assumption controls it, never claim a tie correlation without a seismic
volume, and label unpicked correlation levels as candidates.

`scripts/verify-citations.py` extracts every URL from an artifact (HTML / Markdown / text / JSON) and reports
which resolve, which are dead and which gave no response. Run it on the source before the build; it exits
non-zero when anything is dead, so it composes into a build gate.

`scripts/verify-html-artifact.py` runs a browser-free structural check on a source HTML artifact — unclosed
or mismatched tags, visible word count, per-class element counts, required strings present, and a
house-furniture leak scan — exiting non-zero on failure. Use it as the build gate when a real browser render
is not available, and prefer it to eyeballing: the defects it catches (a section that silently failed to
render, internal vocabulary sitting in text a human will read) are invisible to page counts. Build the
substance into the artifact file and run the checks from a checked-in script; keep shell payloads to short
read-only probes, since a long inline shell body that restates the artifact's own claims is the shape that
gets held at the write gate.

See `references/entity-dossier-from-public-record.md` when the artifact profiles an organisation — an
operator's or competitor's position, an institution's presence in a country. Covers building the asset
table from primary releases rather than coverage of them, splitting participating interest per field,
reading a leadership seat's background as an operating posture, checking whether the subject authored
the primary literature on its own ground, laying state-linked public affairs into national-narrative /
technical-authority / ground-level-licence / shadow layers, verifying that a fact actually belongs to
the entity you are profiling, and closing with a named-gap register instead of an estimate.

---

*DITEMPA BUKAN DIBERI — the artifact is the proof.*