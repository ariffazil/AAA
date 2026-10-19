---
name: entity-dossier-sourcing
description: "Use when a deep dossier on a named entity is asked for."
version: 1.0.0
owner: curator
risk_tier: medium
triggers:
  - "tell me everything about <company>"
  - "deep research internal and external"
  - "what is really going on with <entity>"
  - "buat dossier untuk <syarikat>"
  - "cari dalam GDrive pasal <entity>"
floors: [F2, F4, F7, F13]
tags: [research, dossier, corporate, drive, evidence, pdf]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
owned_by: curator
authority_of: AAA
---

# Entity Dossier Sourcing

Governs "tell me everything about X" where X is a **named entity** — a company, a subsidiary, a state-linked arm,
an agency, a person-in-institution. The deliverable is a source-graded dossier, not a news summary and not a
model's recollection.

**Related, not duplicated:** `principal-analysis-artifact` owns the shape and register of a long-form artifact
(structure, counter-case, length discipline). `typst-pdf-report` owns the general Typst build/escape pipeline.
This skill owns the **sourcing sweep** — the part where a dossier gets its numbers — and the render defects
specific to a multi-section dossier.

## The sweep is three layers, in evidence order

All three before writing. The order is ranked: each earlier layer outranks the next, and reading the first-party
record early changes what the web layer has to answer.

**1. Internal archive.** Grep the federation trees, then open the canon index for the entity family instead of
guessing paths.

```bash
grep -ril '<entity>' /root/AAA /root/arifOS/memory /root/HERMES/lanes /root/.hermes/lanes 2>/dev/null | head -40
grep -ril '<entity>' /root/GE* /root/A-FORGE /root/WEALTH /root/arifOS 2>/dev/null | head -30
```

For the Malaysian NOC family the ATLAS and its knowledge graph own the routing rule; modelled artifacts
(trajectory models, tripwires, scenario weights) sit under `arifOS/memory/entities/`. Read for prior theses and
prior estimates — then quote and grade them, never restate an internal model as measured fact.

**2. The principal's Google Drive — the layer most often skipped, and the one carrying first-party financials.**
Direct OAuth REST, no wrapper. Token at `/root/.secrets/google_token.json`.

```python
import json, urllib.request, urllib.parse
tok = json.load(open('/root/.secrets/google_token.json'))
data = urllib.parse.urlencode({'client_id': tok['client_id'], 'client_secret': tok['client_secret'],
                               'refresh_token': tok['refresh_token'],
                               'grant_type': 'refresh_token'}).encode()
at = json.load(urllib.request.urlopen(
    urllib.request.Request('https://oauth2.googleapis.com/token', data=data)))['access_token']

def drive(q, n=50):
    url = 'https://www.googleapis.com/drive/v3/files?' + urllib.parse.urlencode({
        'q': q, 'pageSize': n,
        'fields': 'files(id,name,mimeType,modifiedTime,size,owners(displayName),webViewLink)',
        'orderBy': 'modifiedTime desc',
        'includeItemsFromAllDrives': 'true', 'supportsAllDrives': 'true'})
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers={'Authorization': 'Bearer ' + at}))).get('files', [])
```

Run **both** queries — `fullText contains '<entity>'` searches document *bodies* and is the high-value one
(registry extracts and prior dossiers whose filenames say nothing), and `name contains '<Entity>'` catches
title-named reports. Download with `files/<id>?alt=media` and the same Bearer header, then `pdftotext -layout`
for financial tables and two-column registry extracts (plain `pdftotext` only for prose).

What lives there: company-registry credit extracts (registration number, every former name, paid-up capital,
directors with appointment dates, shareholder list, five years of balance sheet and P&L, gearing and return
ratios), audited statement summaries, earlier investigative dossiers. A registry extract is a first-party record
of what was filed; an article about the company is not.

**3. External web.** `mcp__exa__web_search_exa` with a natural-language description of the ideal page, not
keywords — strategy/capacity, acquisitions, CEO interview and 2030 target, profit-loss and segment, and always
the *divestment / stake sale / criticism* angle beside the growth angle (a company in a selling cycle announces
it in the trade press first). One search per `tool_call`: local tools take a single entry and a multi-entry
batch is rejected. Bulk-fetch annual reports and IR PDFs with `mcp__exa__web_fetch_exa` (URL list, ~14000 chars)
and prefer the issuer's own PDF over any write-up describing it.

## Grade every figure, in plain words, not tags

| Grade | What it is | Example |
|---|---|---|
| **UKUR** (measured) | registry extract, audited statement, filing | paid-up capital, PAT, director list |
| **DILAPOR** (reported) | institution's own release / IR / news of one | "9.1GW installed and under construction" |
| **TERBIT** (derived) | your arithmetic over the two above | capacity share of a total |
| **ANDAI** (interpreted) | thesis, pattern read, scenario weight | "the arm is an ESG façade" |

Without the DILAPOR rung, second-hand figures get filed as measured and the document upgrades hearsay to fact.
Every TERBIT figure names its denominator in the sentence; every ANDAI sentence says it is a reading.

## Arithmetic traps that produce wrong numbers

- **A holding company's zero revenue in a pre-consolidation year is not "no business".** Consolidation begins on
a specific year and the earlier column stays empty; quoting the pair as growth produces a narrative that is
purely an artefact of the accounting boundary. Check the consolidated-accounts flag per year first.
- **A group segment is not a subsidiary.** Where the entity is bundled with property or treasury, the segment
revenue belongs to the segment. Give the entity's own line if one exists and say the segment figure cannot size
it.
- **A minority stake's ticket size is not a valuation.** Read which noun the number attaches to — stake offered,
enterprise value, or equity value. With heavy debt these differ by multiples; conflating them misstates the
company by billions.
- **Headline capacity is usually not wholly owned**, and reported capacity ≠ operating capacity. Take both and
label them; the gap is a finding about delivery.
- **Trend claims need three years of the same basis.** A series that crosses a consolidation change, a disposal or
a currency change is not a trend.
- **The registration number is the identity, not the brand.** A recently launched brand is often a renamed legacy
company with a decades-old incorporation date and several former names — get both before writing the history.

## Rendering a multi-section dossier

Cover plus numbered body, a boxed side-by-side comparison, a timeline, a grading close. These defects compile
cleanly and ship wrong:

- **`#set page(numbering: "muka 1")` does not prefix the word.** The string is a numbering *pattern* where `1` is
substituted per page, so the literal word prints and the digit becomes the page glyph (`mukb 8`). Use
`numbering: "1"`. For an unnumbered cover: `numbering: none` at the top, then re-issue
`#set page(numbering: "1")` right after the `#pagebreak()` that ends the cover.
- **0.13.x has no closure numbering** — `numbering: n => "muka " + str(n)` fails with `error: unexpected
argument`. Use the pattern string or a `footer` block.
- **`#grid` children must be positional arguments, not a content block.** `#grid(columns: (1fr, 1fr))[ #block(...)[A] #block(...)[B] ]` compiles with no warning and stacks both boxes in one cell. Write
`#grid(columns: (1fr, 1fr), gutter: 10pt, block(...)[A], block(...)[B],)`.
- **`#pagebreak(weak: true)` before a heading** stops it being stranded at the page foot, and only fires when the
heading would actually be orphaned. Apply it where the defect appears, not to every heading.
- **Verify geometry with `pdftotext -bbox file.pdf -`** — side-by-side boxes share a `yMin` with different
`xMin`; stacked boxes share `xMin` and differ in `yMin`. Judge all names, figures and wording from
`pdftotext` alone. A `vision_analyze` pass reliably catches gross layout ("the boxes are stacked") but invents
names and paraphrases bullets — never accept a content claim from it and never use it as the only check.
- **Before delivery:** page count, plus a page-tail sweep — a tail that is a section heading means a break did not
take; a tail that is only a footer means a near-empty final page (fix the closing block's top spacing, not the
body).

## Close and deliver

The dossier ends on a grading section, not a summary: one block per rung naming which figures sit there, then one
sentence the principal can carry — the consequence, in his register. No recap. Register is BM Penang, short and
direct, zero machine vocabulary in the prose. Emit `MEDIA:/abs/path/file.pdf`; never cite a scratch path.
