---
name: walter-isaacson-biography
description: "Use for biography PDF in Walter Isaacson register."
version: 1.0.0
owner: curator
risk_tier: high
triggers:
  - "write biography in Walter Isaacson style"
  - "biography pdf"
  - "novel nonfiction"
  - "tell the story of X and Y"
  - "real story of us"
  - "biographical narrative"
floors: [F2, F5, F6, F9, F11, F13]
tags: [biography, narrative, nonfiction, walter-isaacson, pdf, anonymization, real-person, story]
capability_tier: fed-long-context
ecology_state: WARM
---

# Walter Isaacson-Style Biography Artifact

Governs the case where the principal asks for a **biography-style artifact** — Walter Isaacson register (Jobs, Einstein, Musk, da Vinci): prose narrative where facts are interleaved with insight, time is a character, the biographer's voice organizes but does not invent. The subject is a real living person or persons. Sources may be the principal's own data (chat exports, journals) or public records.

**Not this skill:**
- Long-form analysis addressed to the principal for his own decision-making → `principal-analysis-artifact`
- A wisdom letter or nasihat for a loved one → `wisdom-letter-for-loved-ones`
- A third-party advisory document for a real-world decision → `third-party-advisory-doc`
- A personal README / voice piece → `human-voice-writing`
- A forensic audit of a real institution → `audit-repo-reality` / `institution-entropy-audit`

## The Anonymization Gate (F5, applies before any reading)

Before opening any source that contains a **third party's** private data (WhatsApp exports, DMs, voice notes, journals, photographs), authorize one of three modes. **Never read third-party private data without explicit choice between these three.**

**Mode A — Full Boundary (no read of source).**
Author the biography entirely from MAP-class sources: `MEMORY.md`, `USER.md`, `carry_forward.json`, SCAR files, public canon, public records. Source is silent on intimate chronology. Length is bounded because intimate detail is not available. Safest.

**Mode B — STORY → MAP quarantine (extract facts only).**
Open the source. Extract only: dates, names of places and roles, observable events, time-anchored facts. **Sumback** any quoted dialogue, private interpretation, intimate narrative. Author biography from extracted facts plus MAP. Verifiable but loses texture.

**Mode C — Full authorize (explicit F13-class ratification).**
Principal states explicitly: "I authorize Hermes to read this [export] for biography purposes, accepting the intimate narrative becomes agent output." Required for biography that retains quoted dialogue, intimate details, narrative reconstruction from private exchanges. This is the only mode that produces Walter Isaacson register with full source texture.

**Pitfall — Default to Mode A if principal does not pick.** If the principal says "guna apa ada" or is ambiguous, **default to A and ASK which mode they want**. Do not infer "C" from "guna apa ada" — the principal may have meant A. Inference here is the failure mode that turns a working session into an F5 violation.

**Pitfall — Anonymization ≠ just removing the name.** When the principal asks for "no real name", they mean:
- Pseudonymize proper personal names ("Arif Fazil" → "lelaki pertama"; "Syed Kudin" → "lelaki kedua")
- Keep company/institution names ("PETRONAS") only if they are not themselves the private matter
- Keep city/location names ("Kuala Lumpur", "Ampang") unless location is itself the disclosure
- Keep generic relational nouns ("abang", "adik", "pakcik", "makcik")
- Keep relationship nicknames that are part of the dynamic's texture ("Abang Sado") if they survive anonymization
- **Never** replace with single-letter placeholders ("A", "B", "S") — those lose the two-person texture the biography is built on. Use descriptor phrases.

## The Register (Walter Isaacson, applied to BM Penang context)

Isaacson's register has five moves. Apply all five.

1. **Prose first, never bullets.** The deliverable is a sequence of paragraphs. Bullets are for index pages and chapter lists, not for body. If the body has a bulleted section, the section is not yet a biography.

2. **Fact + insight interleaved.** Never state a fact without then connecting it to what the fact means for the human. Pattern: "It is five-thirty in the morning. The order form has 292 units. The cap is nineteen portions. The cap is also, by the end of this book, the number that holds the friendship in place." — that is the move.

3. **Time as character.** Treat days, not events, as the unit of structure. Open chapters with the hour. Let the reader feel the day accumulating. The chronology matters more than the incidents.

4. **Quotation from source verbatim.** When the source has a quote ("Sometimes I feel I'm gay sebab I cannot handle women's emotions"), use the quote. Do not paraphrase into cleaner English. The dialect is the texture. The BM Penang, the broken English, the emoji that closes the sentence — all of it survives into the prose. Cleaning the quote into BBC English is the failure that turns biography into PR.

5. **The biographer's voice at the edges.** **A note on the form** at the start. **An epilogue** at the end that names what the biographer could not see. The body is the subject's. The edges are the biographer's. This is the contract.

## The Structure (default — overridable)

```
Cover page (image + title)
Title page (typography only, dedication, author)
Prologue (a note on the form — what was read, what was not, the limits)
Body (chapters in chronological order, by day or by cluster of days)
Epilogue (what the biographer could not see, the cap that held)
```

**Chronological beats thematic.** "Write a biography" without further direction → chronological. If the principal says "start from the sister", "lead with the wallet", etc., that is a thematic override — apply but document the override in the prologue.

**Chapter length 1500-3000 words.** Shorter than 1000 is a magazine piece. Longer than 4000 is a thesis and loses reader. Default 2000.

**Total length 5000-8000 words for a single-subject biography. Up to 12000 for a two-subject biography where the relationship is the subject.** Length discipline matters because the deliverable must be read in one sitting.

## The Pipeline (build → verify → deliver → archive)

### Step 1 — Author the markdown body first, do NOT render directly.

```
/tmp/biography_<TITLE>.md
```

Build chapter by chapter. **Append, do not overwrite.** If the principal asks for an iteration, save the previous as a backup `_v<n-1>.md` only at the explicit request — default is overwrite. Accumulating `.md` files clutters `/tmp`.

### Step 2 — Choose cover visual BEFORE rendering the PDF.

Three options, ordered by safety:

1. **SVG line art programmatic** (default for biographies of living subjects). Two silhouettes, no faces. City skyline as background. Author in SVG, convert via `rsvg-convert -w 1500 -h 2000 /tmp/cover.svg -o /tmp/cover.png`. No data dependency, fully reproducible, looks like a literary fiction cover (Walter Isaacson's *Steve Jobs* paperback cover is silhouette, not photo).

2. **AI-generated image via `mmx image generate`** (when principal accepts AI-illustrated style). Use prompt-optimizer; aspect 3:4; specify "no faces visible", the color palette, and the mood. ~25 seconds.

3. **Real photograph** (only when principal supplies the photograph AND the subject has consented AND any third party in frame is also consented). Fetching public photos of living subjects from LinkedIn or social media **without explicit principal authorization** is F5 territory.

**Default:** option 1.

### Step 3 — Render with proper book margins and typography.

Use `reportlab` with the following parameters (calibrated for hardcover-style paperback):

```
LEFT_MARGIN = 2.8cm        (binding edge)
RIGHT_MARGIN = 2.2cm
TOP_MARGIN = 3cm
BOTTOM_MARGIN = 2.8cm
```

Body: Times Roman 11pt, leading 17, justified, first-line indent 18.
Chapter title: Times Roman 20pt, leading 26.
Source citations: Times Italic 9pt, color `#888888`.
Page numbers: centered footer, Times Italic 9pt, color `#888888`.
Cover page: NO page number (use `onFirstPage` callback).

### Step 4 — Verify the file is a real PDF.

```
file /root/.hermes/cache/documents/doc_biography_<TITLE>.pdf
```

Must say `PDF document, version 1.7+`. A text file with `.pdf` extension is the most common defect and the most embarrassing.

### Step 5 — Archive previous iteration BEFORE writing the new one.

When the principal asks for an iteration (e.g. "use my reality", "redo chronological", "no real name"):

```bash
ls /root/.hermes/cache/documents/doc_biography_*.pdf
```

If there is a previous version, **delete it** — do not keep `_v1`, `_v2`, `_v3` lying around. The principal does not want their final iteration named after `_FINAL_v3_REVISED`. One PDF in `documents/`, named by content (`doc_biography_ALPHA_ZEN.pdf`), is the contract. The intermediate `.md` files in `/tmp/` can stay (they're not surfaced) but the PDF does not accumulate.

### Step 6 — Deliver via `MEDIA:` path.

```
MEDIA:/root/.hermes/cache/documents/doc_biography_<TITLE>.pdf
```

## Pitfalls

### "Telling the story" ≠ "writing the story"

When the principal says "tell our story", they do not mean write it in first person as the principal. They mean: use the biographer's voice. The biographer is the agent. The subject is the principal. The narrative voice belongs to the agent; the subject's voice comes through in quoted dialogue from the source.

### Walter Isaacson register without Isaacson's discipline

The principal may say "Walter Isaacson style" because they want it to *read* like Isaacson — narrative momentum, prose density, biographical insight. They are NOT asking for Isaacson's research discipline (interviews, primary documents, fact-checking against three sources). Apply the *register*. Do not pretend the biography was researched the way Isaacson researches; the source is the WhatsApp export, not three years of interviews. **Say so in the prologue.** The prologue is where the limits live; the body never lies about its provenance.

### Iteration churn

The principal will iterate ("B" instead of "A", "redo from chronological", "no real name"). Each iteration is a new PDF. Do not let the count grow past 4 in `documents/`; if it does, the principal has lost track of which one they wanted and the pipeline has failed.

### Mixing register modes

Walter Isaacson ≠ agent receipt block. The biography does NOT carry `[OBS]/[DER]/[INT]/[SPEC]` tags, does NOT carry ΔS, does NOT carry source IDs in the body. Citation is *prose attribution*: "the export states", "the WhatsApp thread records", "on the twenty-ninth of August". If a tag slips in, it is a register failure and the paragraph must be rewritten.

### Confusing "deep research" with "more data"

Principal says "do deep research, reality context of both of us" — this is NOT an instruction to fetch external public records. It is an instruction to draw on ALL available internal sources: MEMORY.md, USER.md, carry_forward.json, SCAR files, chat exports, canon files, public canon where relevant. External public-record fetching (LinkedIn profiles, public photos) is a separate authorization step. When in doubt, draw on what is already in the federation; ask before fetching.

### The cap that holds

Every biography has a number that holds. Isaacson's *Steve Jobs* has the year. *Einstein* has 1905. A biography of two men and a federation has the cap — nineteen portions, or the order form, or the peptide dose. Find the number early. It is the frame.

## Reference pattern — chapter opening

A Walter Isaacson biography opens chapters with three moves in sequence:

1. **The day, named precisely.** "It is twenty-seven minutes past eight on a Wednesday evening in late August, the kind of evening in Kuala Lumpur where the heat has broken but the humidity has not."

2. **The fact on the day.** "Arif types a single sentence into a WhatsApp thread."

3. **The frame the fact fits.** "The thread will, in twenty-eight days, become a book."

This three-beat opening works because it gives the reader a place to stand, a thing to see, and a hint of why the thing matters. Apply it on every chapter that is not a continuation chapter.

## Reference pattern — the prose fact/insight pair

When stating a fact, immediately connect it to meaning:

> ❌ "Syed was divorced. He had children."
> ✅ "Syed was divorced. The children live with their mother. The marriage had ended, but the way the marriage ended — the ex-wife using the children as leverage — is the body of experience that Syed now carries into every conversation Arif has about family."

The second version is harder to write and easier to read. Apply it throughout.

## Reference pattern — the epilogue

The epilogue is where the biographer names what they could not see. Apply this template:

```
The book ends where the [source] ends. [Source] ends on [date]. [What was not captured].

What the book can contain is the shape of what was said.

It is, in places, almost unbearably [adjective 1]. It is, in places, almost unbearingly [adjective 2]. It is, in places, almost unbearingly [adjective 3]. It is the kind of record that [subject class] make when [condition].

The [biographer's role] has rules about [subject matter]. The rules are [origin]. They are not the same rules as the [subjects'] rules. The biographer can [capability 1]. The biographer can [capability 2]. The biographer can [capability 3]. The biographer cannot, however, [the one thing that matters].

The biographer is, by design, a [noun phrase that names the limitation].

What is there, between [subject 1] and [subject 2], is [the number that holds].
```

The pattern works because it (a) closes the chronology, (b) names the unsaid, (c) names the biographer's limit, and (d) returns to the cap.

## Quality check before delivering

1. Could a reader who has never seen the federation tooling read this end to end without a glossary?
2. Is every quoted line verbatim from source — including dialect, broken English, emoji?
3. Are proper personal names anonymized to descriptor phrases, not single letters?
4. Is the chronology clear (chapter opens with day and hour)?
5. Does the biographer's voice appear at the edges (prologue + epilogue) and disappear in the body?
6. Is the file actually a PDF, version 1.7+?
7. Is there exactly ONE `doc_biography_*.pdf` in the documents directory, named by content not version?
8. Was the principal's mode authorization (A/B/C) explicit before any third-party data was read?

If any answer is wrong, fix before delivering.