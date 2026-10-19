---
name: arxiv-preprint-pipeline
description: "Use when preparing a paper for arXiv or arif-fazil.com."
version: "1.0.0"
metadata:
  hermes:
    tags: [arxiv, preprint, latex, manuscript, research-paper, site-publish, words-writing]
---

# arXiv Preprint Pipeline

Turn a draft paper (any format) into: (a) an arXiv-uploadable TeX package with
companion data files and metadata, and optionally (b) a live paper page on
arif-fazil.com under `/words/writing/<slug>/`. Class of task: "is this
arXiv-ready?" / "publish this paper" / "prepare for arXiv".

## Scope boundary with essay-publish-pipeline

Personal/reflective/civic content → `essay-publish-pipeline` (Medium register
or MakcikGPT register). Academic manuscript with abstract, sections,
figures/tables, bibliography, falsifiable claims → this skill. When mirroring
the paper to the site, follow essay-publish-pipeline's static-shell + landing
card + index.json/llms.txt recipe but use the PAPER register (mono kicker
`WORDS · PAPER · <domain> · ENGLISH`, no `Narrative · Ψ SOUL` label, no
italic-uppercase hero), and add `citation_*` meta tags plus a PDF button.
See `references/site-mirror-paper-page.md` for the full shell pattern.

## Procedure (order matters)

### 1. Locate source artifacts BEFORE rebuilding anything

```bash
find /root/forge_work /root/worktrees /root/arifOS -newermt "<paper date>" \\
  \( -name '*.tex' -o -name '*.typ' -o -name '*.bib' -o -name '*.bbl' \)
```
Search by paper title string (`rg -l '<exact title>'`) across forge_work,
worktrees, /root/AAA before assuming the source is missing. A Typst draft may
coexist with the final LaTeX build — check BOTH; they often differ in title
and maturity (an earlier Typst draft is NOT the submission artifact).
If only a PDF exists (metadata: Creator=LaTeX/xdvipdfmx ⇒ built from TeX
somewhere; Creator=Typst ⇒ Typst source): rebuild the TeX from the PDF text —
see step 2.

**Rebuild trigger:** if no .tex for the PDF exists anywhere, reconstruct it
(see step 2). Do not hand Arif a Typst-drafted package and call it arXiv-ready
— arXiv wants TeX source, and a Typst draft with a different title is the
wrong artifact.

### 2. Reconstruct TeX from a PDF-only draft (pymupdf + manual layout)

- Extract text with `pymupdf` (`page.get_text("text", sort=True)`), preserving
  page markers, headings, tables (via `page.find_tables()` when available,
  else read column layout), figures (re-draw as TikZ: flow diagrams, ladders,
  bar charts — vector, no raster), equations (re-typeset amsmath).
- Normalize ligatures (ﬁ→fi, ﬂ→fl, etc.) before diffing.
- Base packages that always work: geometry(1in margins,10pt), lmodern,
  booktabs, tabularx, ragged2e, enumitem, hyperref(hidelinks), tikz+
  arrows.meta+positioning.
- Compile twice with pdflatex for cross-refs; fix Overfull hboxes (tighten
  TikZ `text width` / node distance) and use \raggedright or narrower
  columns for tables with mid-word hyphenation.
- **Fidelity check:** `difflib.SequenceMatcher` on whitespace-normalized,
  de-hyphenated, de-ligatured text of original vs rebuilt PDF. Word-level
  ratio ≥ ~0.92 is a good bar; residual diffs should be explained (bibliography
  citation formatting, hyphenation) — list them, don't hide them.

### 3. Verify every cited arXiv ID actually exists (anti-hallucinated-reference)

```python
import urllib.request, xml.etree.ElementTree as ET
ids = "2606.09498,2603.28052,..."  # comma-joined from the manuscript
x = urllib.request.urlopen(
    f"http://export.arxiv.org/api/query?id_list={ids}&max_results=20",
    timeout=30).read().decode()
# parse <entry><title>, <id>, authors — compare title strings to the citation list
```
Every ID must return a matching title + author list. Any mismatch = citation
contamination: fix or flag before packaging. (AI-drafted manuscripts carry
plausible-but-fake references at nontrivial rates — this check is mandatory,
not optional.)

### 4. Audit orphan bibliography entries

For every \bibitem{key}, grep the .tex body (outside the bibliography
block) for `\cite{...key...}`. An uncited bibitem = dead reference — remove it
or add a real in-text citation. Numeric-style \bibitem{key} (no
\bibitem[key]{key}) is correct LaTeX — don't be confused by pdftotext showing
[author-name] where the compiled PDF shows [n].

### 5. Companion data files the paper's text promises

If §Data Availability / §Implementation says "the companion package includes
X and Y" (e.g., two small CSVs), those files MUST exist in the package or the
paper is shipping a false statement about itself. Build them from the numbers
actually disclosed in the paper (aggregate snapshot CSV with
metric,count,as_of,source,interpretation_limit columns; claim-status ledger
CSV with claim,status,required_upgrade_path columns). Keep the "this is
telemetry, not accuracy" framing in the CSV itself.

### 6. arXiv metadata (pre-fill, don't improvise at upload time)

Write `arxiv_metadata.txt` beside the tex:
- Title (exact), Author, Affiliation (as printed on paper)
- Primary category (cs.AI for governance/runtime papers), cross-lists
  (cs.SE, cs.CY where apt)
- Comments: page/table/figure count + document type (position paper) + any
  honesty line ("proposed experiments have not been run")
- License recommendation: CC BY 4.0
- Abstract plain text: **arXiv web form caps at 1920 characters** — count it
  (`len(abstract)`) and trim if needed. Abstract must be plain text (no LaTeX
  markup) for the form field.

### 7. Package and verify a clean-room compile

```bash
tar -czf paper-arxiv-source.tar.gz -C arxiv/ paper.tex companions...  # NO .pdf/.aux/.log
mkdir /tmp/arxiv-clean && tar -xzf paper-arxiv-source.tar.gz -C /tmp/arxiv-clean
cd /tmp/arxiv-clean && pdflatex paper.tex && pdflatex paper.tex  # must reproduce the same page count
```
If the clean-room compile fails or page-count differs, the package is not
uploadable — fix before delivering.

### 8. State the endorsement/account gate honestly (F2)

First submission to a category (e.g., cs.AI) requires **endorsement**: either
an institutional email meeting arXiv's criteria, or one positive endorsement
from an established arXiv author in the endorsement domain. Corporate email
does not substitute. Tell Arif exactly this — do not say "arXiv ready" without
qualifying that endorsement + account + license choice remain human steps.
How to find an endorser: open a cited paper's abs page → "Which authors of
this paper are endorsers?" → contact 1-2 (never mass-email).

### 9. Optional: mirror to arif-fazil.com

Follow `essay-publish-pipeline` Steps 1-5 (site module + registries + landing
card + static shell + markdown mirror) with the PAPER register, and drop the
verified PDF into `public/words/writing/<slug>/<slug-short>.pdf`. Add citation
meta:
```html
<meta name="citation_title" content="..." />
<meta name="citation_author" content="Fazil, Muhammad Arif bin" />
<meta name="citation_publication_date" content="2026/10/19" />
<meta name="citation_pdf_url" content="https://arif-fazil.com/words/writing/<slug>/<file>.pdf" />
```
Deploy the PDF + shell to BOTH roots (`/var/www/html/words/...` and
`/var/www/html/arif/words/...`) per the Caddy /words/* root split, then run
the 5-gate verification (page, PDF content-type, landing count, index.json,
index.md).

## Pitfalls

- **Typst draft ≠ final artifact.** An arXiv-targeted Typst draft with a
  different, older title may sit in forge_work next to the real PDF-only
  final. Always check PDF Creator metadata and title match before choosing a
  source tree.
- **Vision hallucination on rendered figure pages.** When QA'ing compiled
  figures via page-render + vision_analyze, the model may invent box labels
  that don't exist in the source (e.g., reporting "RECEIPT" for a
  GROUND-TRUTH box). Cross-check any reported label against the .tex source
  or `pdftotext` output before acting on a vision-reported defect. Prefer
  coordinate checks (pymupdf word bboxes vs margin box) for overflow claims.
- **Abstract over limit.** arXiv's web form hard-caps the abstract at 1920
  characters; long position-paper abstracts blow past it. Count before
  delivery.
- **Orphan bibitems ship dead references** — reviewers/moderators notice
  instantly; audit \cite usage per key (step 4).
- **Citations hallucinated by drafting AI** — always verify each arXiv ID via
  the export API (step 3); plausible IDs that resolve to different papers are
  worse than missing ones.
- **Package bloat.** Never include .aux/.log/.pdf in the source tarball; only
  .tex + companion data + figures (as pdf/png for pdfLaTeX mode). Hidden files
  are auto-deleted by arXiv anyway.
- **Endorsement is not optional** — don't report "arXiv ready" without stating
  the endorsement/account step; corporate email usually doesn't qualify.
- **Vision-based PDF QA is corroborating, not primary.** Primary fidelity
  check = text diff (pymupdf) + clean-room compile. Vision can confirm layout
  sanity on a page but its label-level claims must be source-checked.