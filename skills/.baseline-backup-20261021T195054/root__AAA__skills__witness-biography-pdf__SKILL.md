---
name: witness-biography-pdf
description: Triggered by realiti hidup or cover to cover.
---

# Witness Biography PDF — 20-30 min reading artifact

Arif commissions these as **personal library reading material** — a single PDF that captures the *arc* of a famous human's life so he can feel they've been met, not skimmed. Two reference productions on file: Demis Hassabis (Oct 2026) and Elon Musk (Oct 2026). The grammar is consistent; the subject varies.

## What this artifact IS, and IS NOT

**IS:**
- A witness artifact about one real human.
- Sourced entirely from public records — authorised biography excerpts the publisher made available, Wikipedia, major outlets (Guardian, NYT, Bloomberg, Reuters, BBC, Forbes, AP), and first-person interviews (TED, Lex Fridman, podcasts, magazine essays).
- 20-30 minutes reading time (around 14 pages typst at 10.5pt).
- BM Penang-kampung register; plain; chapters short; naratif bergerak laju.
- Witness-first: facts over legend, scars over mythology.

**IS NOT:**
- A Wikipedia chronology, a company history, a fanboy piece, or an anti-piece.
- A verbatim extraction from a copyrighted book (publisher excerpt ≠ fair-use cover-to-cover reproduction). Repeating the same author quote to source 4+ facts is the boundary; reproducing copyrighted text paragraph-by-paragraph is not.
- A psychoanalysis or diagnosis. Never diagnose a living person. Quote what they said and what observers said about them.
- A victory lap or a takedown. End with an open question, not a verdict.

## Chapter grammar (13 bab skeleton)

Proven across Demis and Elon productions. Use this unless Arif specifies another structure.

1. **Akar / Roots** — family, birthplace, the scar that shaped the scar.
2. **Scar pertama / First turning point** — the formative wound (family, school, war, exile).
3. **Kod / First craft** — earliest skill that became identity.
4. **Wang tidak selesaikan apa-apa / Money did not solve it** — first fortune, what it opened, what it did not.
5. **Semua orang kata mustahil / Everyone said impossible** — the long-shot bet.
6. **The fall / Tahun gelap** — the year everything almost ended.
7. **Production hell / operating mode** — the famous crisis.
8. **Operating style / how the person runs** — patterns, not events.
9. **Public war / latest public fight** — the thing people argue about.
10. **Apa yang dia percaya / What they believe** — the worldview.
11. **Kos yang tidak nampak / Hidden cost** — relationships, body, reputation, sleep.
12. **Bayangan / Shadows** — enemies, critics, ex-allies.
13. **Soalan terbuka / Open questions** — end on a question. Never on a verdict.

Every chapter answers three questions silently, in this order: *What happened. Why it mattered. What pattern keeps repeating.*

## Cover and ending

- **Cover:** name · subtitle (Realiti Hidup, dari X ke Y) · two-column vital-stat block · one pull-quote. No emoji, no stock-photo. Always set `Disusun dari sumber awam — bukan petikan lengkap <book title>` if a book is the primary inspiration.
- **Ending:** never `X adalah genius`. Never `X adalah masalah`. End with the open question Arif actually feels: usually the tension between *what they built* and *what it cost*. One closing italic paragraph in the same register (`Ini bukan cerita X. Ini cerita seorang manusia yang...`). Always include `DITEMPA BUKAN DIBERI` or equivalent lineage mark at the foot.

## Source priority

1. **Authorised biography publisher excerpts** — Walter Isaacson, Ashlee Vance, etc. publishers release selected chapters and these are quotable. Use for structure and direct quotes; do NOT attempt to reproduce paragraphs verbatim.
2. **Authorised magazine essays by or about the subject** — Justine Musk (Marie Claire, 2010), Vivian Wilson (NBC, Teen Vogue, 2024–25), etc. Quoting the subject's own written words is fair use; build the spine around them.
3. **Major outlets** — Wikipedia business-career and personal-life articles, Guardian, NYT, Bloomberg, BBC, AP, Reuters, Forbes, Washington Post, Atlantic, Sky.
4. **First-person interviews** — TED, Lex Fridman, Joe Rogan, podcasts, conference Q&A. Use the subject's verbatim quotes sparingly — pick 4–8 distributed across the artifact, not clustered.
5. **Company histories / public filings** — founder bio pages, SEC filings (10-K Item 1), IPO prospectuses.

Cross-audit each candidate claim against at least two of the above before it goes into the artifact. The artifact ships as honest narrative; if you can only find one source for a fact, downgrade it (according to, by her account, as reported in Isaacson).

## Research workflow

Research runs *before* any writing. Do not start the .typ until you have at minimum 8 verified, attributable facts per chapter × 13 chapters ≈ 100 facts.

```python
exa.web_search_exa(query=f"{subject} {angle} facts biography authoritative interview", numResults=8)
for angle in ["childhood family", "first career", "pivotal failure", "current state"]

exa.web_fetch_exa(urls=[publisher_excerpt_url, mariclaire_url, nbc_url, ...], maxCharacters=6000)
```

## Typst mechanics — read this before drafting

Two traps bit previous productions in this lane:

### Trap 1 — asterisks-as-profanity in book quotes

Walter Isaacson, Ashlee Vance and other authorised biographers use ASCII asterisks to redact profanity (`f***`, `s***`). Typst treats `*word*` as italic, `**word**` as bold, `***word***` as both, and any unmatched sequence of asterisks at the end of a phrase (like `f***`) opens a strong-emphasis markup that never closes — compile fails with `unclosed delimiter` pointing at the asterisks. `\*` does **not** escape this; the typst markup parser does not honour the backslash for emph.

**Fix:** before writing any .typ source, scan the drafted prose for run-on asterisks in quoted speech. Replace each with one of:
- a hyphenated separator (`f---`, `s---`) — preserves the redaction beat
- the literal English word (`fuck`, `shit`) — these are valid in private-DM artifacts for the sovereign's own reading
- a euphemism (`[profanity]`, `foul language`) — when the source quote is non-essential

Do the replacement **at draft time, in the prose**, not as a sed pass on the .typ — sed chains against a file full of `\n`, `#`, and quotes produce escaping errors that look like typst errors.

### Trap 2 — `$` opening math mode inside narrative

Any `$` in a typst source immediately enters math mode. This bites even when escaped:

```
\$10^170\$     # compiles to $10^170$ → math mode → broken unless you balance math markup
\$300\,000      # ALSO fails — the comma + caret breaks the math parse
```

For numbers like exponents, large integers, or monetary amounts in narrative:
- Write `10^170` (no dollar signs) for exponentiated large numbers.
- Write `USD 44 bilion` or `\$44 bilion` (which compiles fine as text) for money in BM.
- If a math expression **must** render as math (e.g., an actual formula), close with another `$` and balance the contents — but for biographical prose this is almost never needed.

The escape `\$` is correct for *currency* in running text. Do not also escape surrounding digits; `\$10^170\$` opens math between the dollars even though both are escaped.

### Trap 3 — long body degenerates into filler

Cap the body BEFORE writing the source. Budget per chapter: ~500–700 words target, hard stop at 900 words. Demis production hit 18 KB of source for 14 pages; Musk hit 28 KB. Both fit, but if the source grows past ~32 KB it means one chapter is monopolising the document and the others are getting stubs — that's a sign to re-draft the long chapter, not just to chop lines.

When the budget fires: discard the offending draft, redraft short. Trimming a degenerate draft ships the texture of the filler.

## Production procedure

1. **Probe reality first.** Read the existing /root/AAA/skills/typst-pdf-report/SKILL.md for the canonical typst escape rules; *do not patch it* (it is in an external skills dir, read-only). This skill is the **content** companion — typst-pdf-report is the **mechanics** companion.
2. **Wire research tools.** For an authoritative biography subject, the minimum research kit is one wide web search per public-chapter angle + one web_fetch pass over the publisher excerpt + the subject's own magazine essays + Wikipedia. Exa MCP or firecrawl; web_search is too noisy for biographical claims.
3. **Outline to 13 chapters** in a temporary scratch file. List the 4–8 facts per chapter with source attribution.
4. **Draft cover + chapters in BM**, target 500–700 words/chapter.
5. **Sanitise asterisks** at draft time — see Trap 1.
6. **Sanitise `$`** at draft time — see Trap 2.
7. **Write the .typ** in **one write_file call** (not a shell pipeline, see typst-pdf-report pitfall 8).
8. **Compile, then verify:**
   ```bash
   typst compile subject.typ subject.pdf
   pdfinfo subject.pdf | grep -E "Pages|File size"
   pdftotext subject.pdf - | head -40     # text integrity
   pdftotext subject.pdf - | tail -40     # last page readability
   ```
   Pages target: 12–16. File size 60–100 KB. If pages < 10, expansion is too thin; if > 18, content is too wide.
9. **Deliver** `MEDIA:/abs/path/subject.pdf` plus a one-paragraph receipt listing chapters and a short note on asterisks/$-escapes you had to handle (so Arif knows what was sanitised).

## Pitfall register (cumulative, distilled)

- **You already had this skill from prior runs** when you write `f***` into a typst source verbatim — check Trap 1 first.
- **Subject's own quotes become the artifact's spine** when available — Justine Musk's *Marie Claire* essay for Musk, Isaacson excerpts for Demis. Lean on first-person sources over secondary narration.
- **Public-figure brutal facts stay public** even when painful — Vivian Wilson's interview about Elon, the 10% presence figure, the ketamine disclosure. Quote the published statement, not the agent's gloss.
- **Family scars need attribution, not analysis.** Quote what Isaacson and Kimbal Musk said about Errol Musk's tirades; do not infer absent-father syndrome in your own voice.
- **End on an open question** that frames what the reader will keep thinking after they put the PDF down. Demis: "Bolehkah Einstein dan Ender dalam satu hayat?" Musk: "Adakah ia bukti kehebatan manusia, atau amaran tentang harga?" The question must be one that the artifact itself did not pre-answer.

## Reference productions on file

- **Demis Hassabis** — Realiti Hidup, dari Catur ke Nobel. 14 pages. Sources: Wikipedia, Guardian (3 years), MIT Tech Review, FT, NobelPrize.org, Penguin Random House publisher excerpt, Probinism book-review summary, LessWrong, Fortune, Time, 9to5Google. Primary framework: Ender → AI scientist → Oppenheimer problem.
- **Elon Musk** — Realiti Hidup, dari Pretoria ke Starship. 14 pages. Sources: Walter Isaacson *Elon Musk* (2023) publisher excerpt, Ashlee Vance (2015), Justine Musk *Marie Claire* (2010), Vivian Wilson NBC + Teen Vogue (2024-25), Wikipedia, BBC, Bloomberg, NYT, Guardian, Forbes, Reuters, Washington Post, Atlantic, AP. Primary framework: scar → capacity → cost.

When a new request in this lane arrives, read both production .typ files in `/tmp/` if they survive, otherwise re-summarise from the delivered PDFs in chat history. They are templates — not to copy, but to remember the rhythm.

## Related skills

- `typst-pdf-report` — the mechanics companion; load it before producing any typst source.
- `pdf-federation` — the cross-engine PDF front door (weasyprint, xelatex, pandoc fallbacks) if typst fails for any reason.
- `person-dossier-from-public-sources` — when the deliverable is a *short* dossier, not a 20-30 min artifact. Use that instead.
- `walter-isaacson-biography` — narrow trigger (Walter Isaacson register, any subject). When the artifact is specifically *in the style of Isaacson*, use that one as the lens; otherwise use this skill.
- `observed-ground` — for fact-checking discipline; every claim must be source-attributed.

## Anti-patterns (do not)

- Reproduce paragraphs verbatim from copyrighted books. Even when the publisher excerpt is publicly available, sustained verbatim reproduction is not what Arif means by "cover to cover" — he means *cover the full arc*, not *include the full cover text*.
- End with a verdict ("X adalah hebat / teruk / bermasalah"). Verdicts kill re-reads; questions preserve them.
- Insert your own moral framing ("Despite his flaws...", "However one cannot deny..."). Quote an observer instead.
- Use "Schelling point" / "predictive" / "shadow" arifOS vocabulary in the PDF body. The artifact is for human reading, not system narration — keep doctrine out.
- Apologise for what the subject did. Name the cost; let the reader hold the rest.
