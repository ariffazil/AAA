# Office-Holder Roster — Method Depth

## 1. Seat-architecture checklist

Answer all six before writing a single profile. Each one changes what the roster looks like.

| Question | Why it changes the answer |
|---|---|
| Was the office ever combined (chairman + chief executive in one person)? | A combined era has one holder where later eras have two; the split date is a structural finding |
| Which holders were *acting*? | Acting occupancy is a governance finding (often an unfilled seat), not a footnote |
| Who appoints the seat, and who removes? | Distinguishes merit appointment from political appointment before you judge anyone |
| Has the appointment mechanism itself changed? | "Appointed by PM" → "appointed by board" is a governance shift worth stating |
| Are any roles concurrent? | Concurrent board seats are normal in GLCs and routinely produce wrong timelines |
| Did anyone die, resign or retire in office? | Death in office and forced exit are different data points and get different treatment |

**Test your model:** for every gap between two holders, ask "who was actually in the seat during
that gap, and in what capacity?". If the answer is "nobody, or the CEO acting", write it that way.

## 2. Source ladder — pre-internet public figures (Commonwealth civil-service states)

Work in this order. English Wikipedia is near the bottom for civil servants; the vernacular
edition is near the top.

1. **Live institutional source** — the organisation's own leaders/board page, annual or integrated
   reports (director lists, "commitment to governance" sections, director remuneration).
2. **Appointment and departure news** — national wire and business press carry the *who replaced
   whom and when* that annual reports omit.
3. **Business-press retrospective columns** — the single paragraph that lists the whole succession.
   Find this early; it is the master list.
4. **Vernacular Wikipedia** (`ms.wikipedia.org` and equivalents) — office dates, birth/death,
   education, honours and family in one place for civil servants.
5. **National news-archive libraries of scanned newspapers** from the 1970s–2000s — obituaries,
   appointment announcements, death notices (these give day-level dates).
6. **University-hosted academic PDFs** — administrative-history journals carry full career
   reconstructions of senior civil servants, with footnotes.
7. **Language/authority biographical databases** — short but reliably dated reference entries.
8. **National honours gazettes** — confirm a title (and therefore a career milestone) and its year.
9. **Published biography**, if the figure got one. Often written by the figure's own biographer and
   quoted in a retrospective column — read the column first, then chase the book.
10. **Industry/social club histories** — long-running institutions' founder and past-president lists
    independently corroborate who led the company and when.

**Naming:** search the **vernacular spelling** and the name without titles. Patronymics are not
surnames — index the person under their given name, and expect the source to carry a long honorific
string (title + orders + patronymic) that will not match a plain query.

## 3. Fitness-for-seat schema (use verbatim, every holder)

```
**Identity**             — birth/death, birthplace, education, public family facts
**Career before**        — the path that produced the appointment
**Brought**              — quantified outcomes during tenure, each with a source
**Got**                  — honours, post-tenure positions, recognition
**Basis of appointment** — merit / political proximity / necessity, each labelled
**Verdict**              — one scale value, 3 evidence bullets, 2 steelman counter-points
**Controversies**        — public record only
**UNKNOWNs**
**Sources**              — URL list
```

**Verdict scale** (state it once in the archive's framing, then use it consistently):
`WELL-SUITED` / `SUITED WITH RESERVATIONS` / `NOT SUITED`. One scale per archive — never invent a
new vocabulary per holder.

**Why the steelman is mandatory:** a one-sided verdict reads as character assassination and gets
discarded by the reader. Two genuine counter-points make the verdict defensible, which is the whole
point of writing it down.

## 4. Subagent hard-rules block (repeat verbatim in every child's `context`)

```
HARD RULES: (1) every factual claim must carry a real source URL; (2) if you cannot verify, write
UNKNOWN — never invent dates, numbers or quotes; (3) prefer primary sources: the institution's own
reports and media releases, vernacular + English Wikipedia, national news archives, serious
business press, wire services, academic PDFs; (4) dignity rule — analyse decisions and outcomes,
never insult a person or speculate about private life; (5) label each claim FACT (sourced) /
INFERENCE / SPECULATION / UNKNOWN.

OUTPUT (markdown, no preamble, follow this section list exactly):
Identity / Career before / Tenure and outcomes with numbers + source / What they got /
Basis of appointment with labels / Verdict (scale + 3 evidence bullets + 2 steelman counter-points) /
Controversies / UNKNOWNs / Sources (URL list).
```

Batch ~4 children per dispatch. Never give one child a different section list — the returns must
concatenate.

## 5. Archive structure and build

```
archive/
  ROSTER.md            # verified anchors as you go (working file, survives context loss)
  manifest.json        # ordered holders + closing sections + cover
  dossiers/<slug>.md   # one markdown file per holder, fixed section list
  out/                 # built HTML + PDF
```

**Write `ROSTER.md` progressively.** Long rosters always outlive a context window; the working file
is what lets a resumed session continue instead of restarting the research.

**Narrative order that works for a governance archive:** cover → holders in chronological order →
full roster table → patterns → sources & open questions. Chronological (not verdict-grouped) keeps
the reader's model of the institution intact.

Build with `templates/roster_pdf_builder.py`. Verified stack: `markdown` (extensions `tables`,
`fenced_code`, `sane_lists`) → `weasyprint` `HTML(string=...).write_pdf()` at A4 with `@page`
margins and a page-number footer, then PyMuPDF for the page count and `hashlib.sha256` for the
receipt. A distinct band colour per seat type reads as governance, not as a CV dump.

## 6. Worked example — the seat-architecture trap, with real consequences

A national oil company's chairmanship looked like a clean one-holder-per-period line. It was not:

- The chairman and chief-executive titles were **one seat** for the first fourteen years — so a
  naive "chairmen" table wrongly lists the same four men twice, once as chairman and once as CEO.
- The seats then **split** into non-executive chairman + professional CEO.
- For the next eight years the chair was held **in an acting capacity by the sitting CEO** — so the
  span that a news-only search renders as "no chairman" was in fact two acting holders.
- Only **one** holder of the chair had ever been a politician; every other came from the senior civil
  service or the corporate sector — a fact that reframes every "was this appointment political?"
  question in the archive.
- The early succession was recovered from **one retrospective column** that named all six early
  chairmen in a single paragraph, plus vernacular Wikipedia pages for the civil servants.
- Two items stayed unresolvable: the exact years one mid-career chairman served, and the full name of
  a founding executive director known in the sources only by a short form. Both were published as
  open questions in the archive rather than guessed at.

**The lesson:** seat architecture is the spine of the whole deliverable. Model it before you spend
subagents on people, because a wrong architecture corrupts every profile built on top of it.
