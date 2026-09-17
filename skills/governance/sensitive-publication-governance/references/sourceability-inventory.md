# Sourceability inventory — auditing a published corpus

Use when asked to find which sentences in a published body of work could NOT be defended by
pointing at publicly available sources. The deliverable is a **list, not an opinion** — an
inventory of exact quotes with categories, never a verdict on whether to publish.

Also run it as pre-flight discipline on a single new piece: a sentence that would fail this
sweep should not be written in the first place.

---

## 1. Extract bodies first

Never audit from a rendered surface. Dump the text, then read the text.

Run `scripts/extract-makcikgpt-bodies.py --batches 5` — it writes one `.txt` per article, a
`manifest.json`, and round-robin batch directories `batches/b1..b5/`.

**Check the extracted-vs-source count.** The article `.ts` files store the body in two shapes
(`html: \`...\`` as an object property, and `const html = \`...\`` as a module const). An
extractor anchored on one shape drops the rest and still looks like it worked — 30 of 35 files
and ~280k characters, reported as success. A partial corpus yields a confidently incomplete
inventory, which is worse than no inventory.

Scan template literals escape-aware: walk forward honouring `\` escapes, stop at the first
*unescaped* backtick. Splitting on backticks naively truncates any piece containing one.

## 2. Batch and delegate — one reader per batch, mutually blind

Hand each batch to a separate reader with identical instruction text. Keep readers blind to each
other: a reader that sees another's findings converges on them, and the point of the sweep is
independent coverage, not consensus. Give each reader the full category list and severity scale
in its own context — they share no memory.

Task text per batch (fill only the directory):

> READ-ONLY. Do not edit, move, or delete any file; do not run anything that writes to disk.
>
> Context: a pre-publication risk inventory for an opinion writer who is a serving employee of an
> institution he also writes about adversarially. The question: which sentences in his published
> work could NOT be defended by pointing at publicly available sources — i.e. sentences only
> someone on the inside could have written.
>
> Read every `*.txt` in `<dir>` IN FULL — do not sample. Handle any code-switched register.
>
> Flag, per file, sentences in these classes:
> **INSIDER_KNOWLEDGE** — internal meetings, minutes, memos, org detail, staffing/HR matters,
> non-public decisions, unreleased figures.
> **FIRST_PERSON_ORG** — writing as an employee or participant from inside the institution.
> **UNGROUNDED_FACT** — a specific checkable number, date, sum, named event, or named act with no
> citable public source.
> **ATTRIBUTED_INSIDE** — hearsay or unnamed insiders as the basis of a factual claim.
> **MOTIVE_AS_FACT** — a named living person's private motive, character, or hidden intention
> asserted as established fact rather than as opinion or question.
>
> Quote EXACTLY, verbatim, under 300 characters — never paraphrase inside the quote. Do not flag
> rhetorical questions, clearly-labelled opinion, slogans, satire, or facts any reader could look
> up. Be strict: a shorter list of real findings beats a padded one; if a file has nothing, say so
> for that file. Do not judge guilt, legality, or intent — you are cataloguing, not prosecuting.
> Do not speculate about sources.
>
> Severity: HIGH = non-public institutional information, an unreleased figure, or first-person
> employee knowledge of the employer. MED = specific checkable assertion with no public source.
> LOW = insider-sounding phrasing asserting nothing checkable.
>
> Output ONLY a JSON object, no prose wrapper:
> `{"findings": [{"file", "slug", "quote", "category", "why", "severity"}], "files_read":
> [...], "files_with_no_findings": [...]}`.

Require JSON only so batches merge mechanically. If a reader returns prose, ask once for the same
content as JSON.

## 3. A regex pre-filter helps — but never replaces the readers

A quick pass over the extracted text for insider markers (first-person + organisation, "sumber
dalaman", "orang dalam", meeting/minutes vocabulary, "belum diumum", "makcik tahu sebab",
"angka sebenar", staff-as-insider phrasing) is useful for sizing the task and for catching what a
reader skims past. It over-matches liberally — treat its output as candidate pins, never as
findings. Quote-anchored reader output is the deliverable.

## 4. Merge and report

Deduplicate on `(slug, quote)`. Group by severity, HIGH first. Report in this order:

1. **Counts** — files read, findings by category, findings by severity.
2. **The findings** — each with its exact quote, its file, and one clause naming what public
   source would be needed and is absent.
3. **Which files came back clean.** The negative result is half the value: it tells the author
   which pieces are already defensible. Never omit it.
4. **Any file that failed to extract or was not read.**

## 5. Rules for the report

- **No verdicts.** Do not say whether a piece is defamatory, actionable, or safe. The inventory
  is evidence; the legal call is the author's and his counsel's.
- **No speculation about who supplied what.** If a sentence could only come from inside, say it
  needs a non-public source — never name or guess the source.
- **Quote-anchored only.** A finding without a verbatim quote is an opinion.
- **State the negative.** "Swept N files, M findings across K files, J clean." A partial sweep
  reported as complete is the failure mode this procedure exists to prevent.
