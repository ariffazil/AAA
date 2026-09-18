---
name: leadership-roster-archive
description: "Use when profiling every holder of an office or seat."
---

# Leadership Roster Archive

## Trigger

The ask is **not one named person** but the whole line of them:

- "every CEO and chairman ever", "senarai pengerusi", "profile all the leaders of X"
- "who led this thing from the beginning", "reconstruct the succession"
- "why did each of them deserve the seat / not deserve it — what did they bring, what did they get"
- Same request scoped to an institution, a ministry, a GLC, a federation, a company, a sport body

Deliverable = **one multi-person archive** (a page per holder) plus roster, pattern and source
sections. Not N free-standing dossiers.

## NOT for

- A single named person, shareable with the subject → `person-intelligence-dossier`
- One institution's crisis or decay history → `institutional-forensic-analysis`
- News/topic synthesis → `executive-intelligence-briefing`

## The procedure

### Step 1 — Map the seat architecture BEFORE profiling anyone (non-negotiable)

Establish and write down:

1. **Was the office ever combined?** Many institutions start with one person holding both the
   non-executive and executive title, then split them. Get the split date.
2. **Which holders were *acting*?** An acting occupancy is a governance finding, not a footnote.
3. **Who appoints the seat, and in what political moment?** Head of government, board, ministry
   nominee, election of members? "Why was X appointed" is unanswerable without this.
4. **Do any roles overlap or run concurrently?** Concurrent seats are common in GLCs and are a
   frequent source of wrong career timelines.

> **A roster built without this model invents phantom holders and phantom gaps.** The tell is a
> claim like "there was no chairman from 2004 to 2012" — usually true only as "no **non-acting**
> chairman". State which one you mean.

### Step 2 — Find the one paragraph that lists the whole succession

Business-press retrospective columns routinely print the complete succession in a sentence or two.
Locating that single column beats mining twenty news articles, and gives you the master list to
verify person-by-person. Search for the retrospective/anniversary column, not the news.

### Step 3 — Verify each name in two directions

- **Live institutional source**: the organisation's own leaders page, integrated/annual report
  director lists, appointment media releases.
- **Independent news source** for the appointment and departure dates — annual reports routinely
  omit mid-year changes, creating normal UNK windows of 6–18 months.

State UNK windows as UNK. **Never interpolate a date to make a table look complete.**

### Step 4 — Fan out per-person research to subagents

Batches of ~4, one dispatch per batch. Two rules make the returns usable:

- **Repeat the same hard-rules block verbatim in every child's `context`.** Children do not share
  the parent's context, and one child without the sourcing rule contaminates the whole archive.
- **Give every child the identical fixed output section list**, so dossiers concatenate without
  reformatting. Template in `references/office-holder-roster.md`.

### Step 5 — Assess fitness for the seat when asked

When the user asks "layak or not" / "did they deserve it", every holder gets: **what they brought**
(quantified outcomes, sourced), **what they got** (honours, post-tenure roles), **basis of
appointment** (merit / political proximity / necessity — each labelled), an explicit **verdict on a
stated scale**, and **steelman counter-points**. Schema and wording in
`references/office-holder-roster.md`. A verdict without a scale and counter-points is an opinion.

### Step 6 — Build the archive PDF

Cover → one page-section per holder (seat-type band/pill on each) → closing **roster table** →
**patterns** section → **sources & provenance** incl. the open questions.

Use `templates/roster_pdf_builder.py` — markdown → weasyprint, dark theme, page-per-person,
SHA256 receipt printed at the end. It is a starter: edit `manifest.json`, not the script.

### Step 7 — Deliver

Send the PDF with `MEDIA:` plus a short chat summary that leads with the **structural finding**
(the seat's architecture, or the pattern in how it changes hands), not with a name list.

## Always-on rules

1. **Dignity (F6).** Analyse decisions and outcomes. Never insult a holder, never speculate about
   private life, family, health or motive. Political/professional context is fair game; the person
   beyond the record is not.
2. **Institutional critique ≠ personal defamation.** A verdict on fitness for a seat is a judgement
   on the appointment and its outcomes, and it must be phrased that way.
3. **Every claim carries a source URL.** No source, no claim — write UNK.
4. **Open questions get their own section.** They are part of the deliverable and the honest
   receipt, not an internal note. Carry unresolved items forward explicitly; never smooth them.
5. **Verify current office-holders live before asserting them.** Never cite a cached name list as
   present-tense fact.
6. **Insider bias disclosure.** When the user works inside the institution being audited, say so in
   the archive's framing.

## Pitfalls

1. **Old office-holders are not on English Wikipedia.** For pre-internet public figures of a
   Commonwealth civil-service state, the yield order is: **vernacular Wikipedia** (far richer than
   the English page for civil servants — carries office dates, birth/death, honours) → the national
   news-archive library of scanned newspapers → university-hosted academic PDFs → the language
   authority's biographical database → national honours gazettes → the figure's published biography.
   Search the **vernacular name**, not the English transliteration. Ladder in the reference file.
2. **Two people can hold the same title in the same decade.** Combined seats, brief chairmanships
   and concurrent roles make naive "one holder per period" tables wrong. When sources disagree,
   present the competing readings rather than forcing a clean succession.
3. **Founders and early executive directors are often not on the official roster page.** If a source
   names someone by a short form (a single name, a nickname, a title), record that as the identifier
   and mark the full name OPEN. Do not silently drop a senior figure because they are hard to find —
   an unexplained absence in the roster is itself a defect.
4. **A partial-name holder must be flagged, not guessed at.** Cross-reference initials, role and
   employer before accepting any full-name expansion.
5. **Don't let the verdict section swallow the evidence.** Brought / got / basis / verdict, in that
   order, each sourced. Verdict last and short.
6. **Consistent per-person schema across every holder.** If holder 3 has "what they got" and holder 7
   does not, the archive reads as uneven treatment — which reads as bias.

## Support files

- `references/office-holder-roster.md` — seat-architecture checklist, source ladder for pre-internet
  public figures, the fitness-for-seat schema, the subagent hard-rules block, and a worked example.
- `templates/roster_pdf_builder.py` — markdown → weasyprint archive builder (manifest-driven, dark
  theme, page-per-person, SHA256 receipt).

## Companions

- `person-intelligence-dossier` — the single-person variant; this skill is the multi-holder variant
- `institutional-forensic-analysis` — institution-level forensics; this skill is leadership-level
- `executive-intelligence-briefing` — topic/news briefings; this skill is office-holder archives
