---
name: public-figure-dossier
description: "Use when building a sourced dossier on a named person."
version: 1.0.0
triggers:
  - "make a pdf about <person>"
  - "list everything X did"
  - "dossier on a public figure"
  - "report on <named person> with photos"
  - "expose / rekod on a politician"
capability_tier: fed-long-context
ecology_state: WARM
---

# Public-Figure Dossier

A document about a real, named person — especially an adversarial or "list their failures" framing —
is a credibility object, not a rant. It survives only if every line is traceable, every image is
licensed, and the limits are declared. This is the procedure.

## When to Use

Any deliverable whose subject is a specific named living person, especially when the brief is
negative ("what dumb things did X do", "expose Y", "rekod Z"). Also use it when the brief is
laudatory — the same discipline applies in both directions.

## Step 1 — Fix the frame before collecting

The brief is usually a verdict ("benda bangang"). Convert it to a **record**, and say so on the
page:

- Title it as a record with a date, not as a judgement.
- State the coverage window explicitly and warn that it is incomplete.
- State the source class: public reporting only, no internal documents, no leaks.
- Add a line that the document is not a finding of wrongdoing and not legal advice.

An adversarial document that includes the subject's **own recorded statements** — taken from the
same reporting — is stronger than one that only quotes critics. Include them. A reader who sees
the subject's defence trusts the rest more, and you cannot be accused of selective framing.

## Step 2 — Source discipline

- Trace every item to at least one **accessible public report** (wire service, national outlet,
  court reporting). Where two agree, prefer the more widely verified figure.
- **No claim survives without a checkable source.** Speculation, social-media claims, and
  unattributed summaries are excluded, and the page says they are excluded.
- Carry the source inline per item (short list: outlet names). Keep the full list on a sources page.
- Corroborate anything that carries a number or a quote in two places before it ships.

## Step 3 — Imagery: real photos only, licensed and attributed

**Never text-to-image a named real person.** A diffusion prior produces a person-like image, not
the person; shipping one in a document about that person is fabrication.

Source portraits from Wikimedia Commons via the API — one call returns the licence, author, date
and URL together, which is faster and more reliable than scraping category HTML:

```python
import json, urllib.request, urllib.parse
UA = "<agent-name>/1.0 (educational; contact <email>)"
url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
    "action": "query", "titles": "|".join(FILES),
    "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime", "format": "json"})
# read extmetadata keys: LicenseShortName, UsageTerms, Artist, DateTimeOriginal, ImageDescription
```

Then download and **verify the bytes**:

```bash
curl -sL -A "$UA" -o cand.jpg \
  "https://commons.wikimedia.org/wiki/Special:FilePath/<exact_file_name_with_underscores>"
file cand.jpg   # expect "JPEG image data". "HTML document" means the request failed.
```

`Special:FilePath/` is the reliable delivery route; hand-built thumbnail URLs return HTTP 400 for
unlisted sizes.

Every embedded photo needs the **attribution triple** — source, author, licence — because CC
licences require it. Label every image; an unattributed photo beside attributed ones is itself a
fabrication signal. Add an explicit integrity note stating that no AI-generated image was used.

## Step 4 — Build

- **Light theme by default.** White ground, dark text, one accent rule. Dark decks are for screens.
- WeasyPrint may not be importable from the default interpreter. Locate one that has it before
  concluding it is missing:

```bash
for p in /usr/local/lib/hermes-agent/venv/bin/python /opt/*/current/venv/bin/python; do
  [ -x "$p" ] && "$p" -c "import weasyprint; print(p, weasyprint.__version__)"
done
```

- Embed images as `data:image/jpeg;base64,...` so the PDF is self-contained and does not depend on
  the build directory at render time.

## Step 5 — QA gates before delivery

Run all four. Never ship on the generator's clean exit code — a generator that writes a failure
document also exits 0.

```bash
head -c 8 out.pdf                      # expect %PDF-
pdfinfo out.pdf | grep -E "^Pages|^File size"
pdftotext out.pdf - | wc -w            # a near-empty layer means a failed render
pdftotext out.pdf - | grep -cE "/(root|home|usr|tmp|opt)/"   # must be 0
```

Ink density per page catches the two failure shapes — a stranded fragment (near-empty page) and a
blown-out page. `numpy` is often absent from the default interpreter, so use PIL alone:

```python
from PIL import Image
im = Image.open(png).convert('L'); w, h = im.size; px = im.load()
dark = n = 0
for y in range(0, h, 2):
    for x in range(0, w, 2):
        n += 1
        if px[x, y] < 200: dark += 1
ink = 100.0 * dark / n        # every page should clear ~3%; a page far below its
                              # neighbours is a stranded fragment, not design
```

A forced page break before each section is the usual cause of a near-empty page. Remove the break
and let the engine paginate rather than adding filler.

## Step 6 — Report which gate you could NOT run

If the vision route is unavailable, you cannot eyeball the render. Say so plainly in the delivery
message: name the gates that passed numerically (page count, ink, text layer, path leak) and state
that no visual pass was performed. Then offer to run it. **Do not present a structural QA as a
visual QA** — that is the same defect class as shipping a fabricated figure.

## Pitfalls

- **Do not attribute a pre-existing fault to your own action.** Before reporting "my change broke
  X", count the same error before the change. `journalctl --since ... --until <pre-change-time>`
  and compare counts; an error present for hours beforehand is not caused by the edit.
- **Do not write to the canonical config to fix an unrelated outage.** Separate the resolver/gate
  check from model/provider health, or you will mis-attribute the cause.
- **Declare a cut-off date.** A "this year" document written mid-year is incomplete by
  construction; say the window out loud rather than implying completeness.
- **Keep the artefact hash and the content hash distinct.** A file cannot contain the hash of its
  own bytes; record both so a later session can tell a rebuild from a re-delivery.

## Related

- Pipeline doctrine, engine matrix and layout ownership: the externally owned `document-pipeline`
  skill. That one routes; this one is the procedure for a named-person subject.
- Licensed-photo sourcing rules also live in the externally owned real-person reference-photo
  skill. Where that skill and this one differ on the download route, the API recipe above was
  verified against live Wikimedia responses.
