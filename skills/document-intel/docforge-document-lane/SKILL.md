---
name: docforge-document-lane
description: Use when building a verifiable document pipeline.
capability_tier: fed-long-context
ecology_state: WARM
---

# docforge document lane

Class-level skill. Trigger: any recurring or templated document — daily brief, weekly report, dossier, deck, invoice — where the same artifact must be produced repeatedly and proven intact. Also trigger when PDF generation has become a pile of one-off scripts.

Code: `/root/AAA/scripts/docforge/` · suites: `test_docforge.py`, `test_state_delta.py`

## The one rule

**Order is the control: compose → render → GATE → seal.** Sealing is unreachable when a gate fails, so a broken artifact cannot enter the permanent record. If your pipeline seals first and checks after, it launders defects into the record and the seal becomes a liability.

## Six axes, one contract

```
SOURCE   .md | .html | .typ | .py(builder)
TEMPLATE base-a4 | deck-16x9        templates/registry.json
THEME    light | dark | print | accessible
ENGINE   weasyprint | chromium | typst | reportlab
GATES    print-light | screen-dark | accessible
SEAL     content hash + artifact hash + chain ledger
```

A new document type is a new combination, not a new script. Add a row to `registry.json` instead of forking a builder.

```bash
python3 -m docforge engines --selftest      # probe every engine NOW, render a real PDF
python3 -m docforge gates out.pdf --profile print-light --expect-pages 4
python3 -m docforge build spec.json          # compose -> render -> gate -> seal
python3 -m docforge verify docforge-ledger.jsonl
```

## Engine selection — by axis, not by preference

No engine is best; they are different. Decide by which capability you need:

- **CSS Paged Media** (running headers, page counters, footnotes, cross-refs) → WeasyPrint or Prince/Typst. **Headless Chromium does NOT have it.**
- **JavaScript / canvas / SPA** → headless Chromium only.
- **Programmatic canvas** (no HTML at all) → ReportLab.
- **Scripted typesetting, fast** → Typst.
- **Gotenberg** is the microservice wrapper when several services in several languages need PDF and you want Chromium deployed once.

Always pass `--no-pdf-header-footer` to Chromium. Without it the render date, document title and the raw `file:///` source path print on **every page** — an internal filesystem path in a third-party deliverable.

Probe availability, never assume: `docforge engines` reports `available/version/reason` for each, and `--selftest` renders through each and checks the `%PDF-` magic bytes. Which lane produced an artifact is part of that artifact's provenance.

## Gate chain (each answers a different question)

| gate | question |
|---|---|
| `pdf_real` | did a real PDF come out? magic bytes, not extension |
| `geometry` | page count + paper size as designed |
| `ink_present` | is any page blank / orphaned |
| `theme_light` | light-background page, or a toner-eating dark fill |
| `text_layer` | did text arrive in order, no internal path leaked |
| `figures` | do embedded images exist where captions claim |

"It opens" answers none of them.

## The two-hash seal (and what it does NOT prove)

A file **cannot** contain its own hash. So:

- `content_sha256` — over the canonical SOURCE, computed **before** substitution, therefore embeddable. Proves the words were not edited after sealing.
- `artifact_sha256` — over the rendered bytes, computed **after** render, therefore delivered in a sidecar (`sha256sum -c` format).

A tool printing "SHA256: …" inside the PDF it is hashing prints a number that proves nothing. Say in the document where the artifact hash lives, and say plainly that **a hash proves integrity, never accuracy**.

C2PA/Content Credentials adds signed provenance and an X.509 trust chain — that needs a signing identity this lane does not hold. Record the field as `not_signed` rather than omitting it, so a reader can tell "unsigned" from "no provenance mechanism".

## Gran Loop — a briefing with no memory is a newspaper

Track each claim with an **explicit lifecycle**, not free prose:

```
NEW -> OPEN -> MOVED -> SETTLED
CONTESTED -> (CONTESTED | SETTLED | RETRACTED)
```

Then the delta is a **set operation over recorded state**, not a prose diff. Prose is rewritten daily even when the underlying fact has not budged; a text diff flags a reworded sentence and misses a CONTESTED claim going OPEN.

- SQLite is the authority for **exact** recall ("what did I record for item X"). Vectors are for **semantic** recall ("find things LIKE this"). Conflating them gives you a vector store that cannot answer a yes/no question.
- Report the semantic mirror as a **status**, never a silent fallback. "No semantic recall" and "semantic recall unavailable" are different facts.
- **Absent ≠ resolved.** An item live yesterday and missing today is reported as `dropped without resolution`, not retired.
- **`open_items` must be latest-known-state PER ITEM**, not the latest edition's subset — otherwise a claim nobody re-mentioned silently falls out of the register.
- Separate `UNRESOLVED` (knowable, not yet known — a hearing date) from `WITHDRAWN` (cannot be resolved from open sources — a figure with no filing behind it). Collapsing them makes a permanent limit look like tomorrow's research gap.

## Pitfalls (each cost a build cycle)

- **Dark-fill detection by horizontal run length is wrong.** A 2px rule under a table header and a 26px filled block produce the SAME run length. Measure **thickness**, and measure `dark_frac` (fraction of dark pixels) as the primary signal: light page ~0.03-0.10, dark page ~0.5-0.9.
- **Blank-page thresholds must be CALIBRATED, not chosen.** Inherited or guessed numbers fail both ways: too high refuses a legitimately short page, too low misses a blank one. Measure your renderer. At 110dpi: blank A4 = 0.00-0.01% ink, heading-only = 0.06%, real short page = 0.17%. Also use a **relative** test (page under ~25% of the document's median ink) so an orphan page in an otherwise dense document is caught.
- **A fixed-size slide div + non-zero `@page` margin = every slide splits into two pages**, silently. `@page { margin: 0 }` and let the slide supply padding.
- **Name your geometry honestly.** A template called `deck-16x9` sized `297x210mm` is A4 landscape, not 16:9. 16:9 = `338.67 x 190.5 mm` = `960 x 540 pt`.
- **Do not gate on substrings of a number.** Asserting `"842" in page_size` fails against a real reading of `841.92`. Parse and compare numerically with a tolerance.
- **A test that cannot fail is not a test.** `assert x or True` and a gate that always passes are the same defect.
- **Never embed raw internal paths.** `file:///`, `/root/`, `/tmp/` in a text layer is a leak; gate on it.
- **Batch a multi-file commit deliberately.** A directory `git add` stages `__pycache__`; add it to `.gitignore` and `git rm --cached` it.

## Deliver to a VERIFIED destination, or do not deliver

A scheduled document that silently stops arriving looks identical to a quiet
week. Real incident (gateway log, three occurrences in one day):

    Queued-lane final send to 8410138119 failed:
    Forbidden: the bot can't send messages to the bot

8410138119 was the bot's OWN id, stored as `origin.chat_id` on a cron job while
`origin.user_id` held the human's id. `deliver: origin` resolved to the bot.

- **Never trust `origin` when the stored origin id could be the bot.** Resolve to
  an explicit `platform:id` and verify it.
- **Three verdicts, not two:** ALLOW / HOLD / DEGRADED. "I could not verify" is
  not "it is fine" — fail CLOSED when the identity source is unreadable.
- **Read the allowed set from the identity source, never hardcode it.** A
  hardcoded id makes the gate stale the moment a human's id changes, and a stale
  gate that cannot be checked is worse than none.
- **Verify before the transport is touched**, so a refused send costs nothing.
- **Sweep the whole scheduler**, don't just fix the one job: enumerate every job
  and flag any whose origin/deliver resolves to a bot or an unknown id.
- **Prove the sweep can FAIL.** Feed it a synthetic bad job and assert it is
  caught. A sweep that always returns nothing is decoration.
- Record refusals in a table. A declined instruction is information.

## A feedback loop that closes

A briefing that ignores what the reader said about yesterday's is scheduled, not
stateful. But do NOT auto-rewrite prompts from chat:

- Keep `raw_text` **verbatim** and derive the `rule` beside it. The derived rule
  is reviewable and reversible; the raw text is the evidence it came from.
- **Store the DIRECTION.** `buang X` and `fokus X` reduce to the same keyword and
  mean opposite things. A store that keeps only the token applies the wrong one.
- **Retirement requires a reason.** An unexplained retirement is
  indistinguishable from a bug.
- **Never delete.** `status` goes ACTIVE -> RETIRED; the row stays.
- **Count applications.** A rule with a high count and no visible effect is a
  candidate for retirement; without the count it becomes eternal.
- Print the standing rules **inside the document** so they cannot govern
  invisibly.
- **Inject them via a per-tick script, not prose in the prompt.** Rules baked
  into a prompt go stale the first time one is added. The script must print an
  explicit "none standing" — silence is indistinguishable from a failed script.

## Two lanes, one table: schema collision

If `CREATE TABLE IF NOT EXISTS` does not change an existing table, and a parallel
agent already created that table with different columns, your code fails with
`no such column`. Before writing any module that owns a table:

1. Read the live schema: `PRAGMA table_info(<table>)` and `sqlite_master`.
2. If it already exists with a different shape, **adapt your code to the table,
   do not migrate the table to your code.** Their columns may be better (extra
   provenance fields), and rewriting destroys evidence for no gain.
3. Bridge the differences in ONE place — a row-mapping function that returns both
   the live column names and your aliases — so existing callers keep working.
4. Add columns additively (`ALTER TABLE ... ADD COLUMN ... DEFAULT`), never
   destructively.

## A governance record is a claim that must be checked BEFORE you delete

A tombstone said a retired job's unique sections had been "folded into" the
surviving job. A grep found 0 occurrences. Deleting on that record would have
removed the capability while the record said it survived.

Before retiring anything on the strength of "the capability moved": grep the
survivor for the actual content. Then, if the claim was false, **append a
correction row — never edit the original.** A governance record that rewrites
itself is worth nothing. A correlated defect: the retired job referenced a script
that no longer existed, so it was already partly broken.

## Verifying a claim about a document

When someone (or another AI) reports a defect in a rendered document, verify the specific claim before acting — including when the claim is about YOUR output. Real example: a report claimed page 8 measured 1.40% ink and was corrected to 7.75%. Re-measured: no page was 1.40%, and page 8 was 9.31%. The correction had never happened. Re-measure, then report the numbers.

## Pipeline receipt

Each run writes `<EDITION>.receipt.json` recording every stage's **real** outcome: validate, state, build, seal, mirror, dispatch. On a gate refusal, state the true position — the artifact is on disk, **no seal was produced**, and no delivery occurred. Report transitions, not booleans: `PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED`.
