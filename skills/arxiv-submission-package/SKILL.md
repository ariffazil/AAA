---
name: arxiv-submission-package
description: "Use when a paper must be checked or packaged for arXiv."
version: 1.0.0
owner: HERMES
capability_tier: fed-reasoning-heavy
ecology_state: WARM
when_to_use: arXiv upload, 'is this paper arXiv ready', building submission tarball, checking a manuscript for submission gates.
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# arXiv Submission Package

Prepare a manuscript for arXiv upload and give a two-part verdict: technical gates
(agent-closed, fail-closed) and human gates (only the author can close them). Every
gate below is a command that produces output — never a claim you repeat from memory.

## Verdict shape (always)

```
TECHNICAL: PASS/FAIL  — each gate, one line, with its command output
HUMAN:     n open     — endorsement / license / category / account / submit click
VERDICT:   ready to upload | blocked on <gate> | not convertible (no TeX source)
```

Never collapse technical PASS into "ready to submit" — a byte-perfect package still
dies at endorsement for a first-time submitter.

## Gate 1 — source format (the Typst/Word trap)

arXiv accepts, in preference order: (La)TeX, AMS(La)TeX, PDFLaTeX, then PDF/HTML for
non-TeX documents. **A PDF with no TeX source behind it cannot be submitted as a TeX
paper**, and a PDF-from-TeX-source is not accepted as a substitute for that source.

```bash
python3 -c "import pymupdf; print(pymupdf.open('paper.pdf').metadata)"
```

- `creator: LaTeX with hyperref` → a TeX tree exists somewhere; find it.
- `Typst` / `Microsoft` / blank → the manuscript must be converted to LaTeX first.
  Conversion is a rewrite, not an export: after converting, compile, then diff the text
  against the original (`difflib.SequenceMatcher` over whitespace- and ligature-normalized
  text; ratio >0.89 is normal for re-typeset copies — the residual is line-breaking).

## Gate 2 — cold-extract compile

arXiv recompiles in THEIR TeX Live, from the uploaded tarball. Build state in your
working directory masks missing files, so the tarball is the only thing that matters.

```bash
rm -rf /tmp/arx_cold && mkdir /tmp/arx_cold
tar -xzf submission.tar.gz -C /tmp/arx_cold && cd /tmp/arx_cold
xelatex -interaction=nonstopmode main.tex >c1.log 2>&1   # pdflatex if the doc needs it
xelatex -interaction=nonstopmode main.tex >c2.log 2>&1
grep -icE '^!' c2.log                                          # want 0
grep -ciE 'undefined (reference|citation)|multiply defined' c2.log   # want 0
```

Run scripts/check-arxiv-package.sh to run every gate in one pass.

Underfull/Overfull `\hbox` warnings are cosmetic (narrow tabularx cells produce them
routinely) and do not block acceptance; `^!` errors and undefined references do.

## Gate 3 — package layout

```
submission.tar.gz
├── main.tex            ← top level, contains \documentclass (arXiv auto-detects it)
├── figure1.pdf         ← figures match ONE engine: .pdf/.jpg/.png for PDFLaTeX, .ps/.eps for LaTeX
└── anc/
    ├── data.csv        ← ancillary data/code ONLY
    └── results.json
```

- Ancillary files go in `anc/` at the tarball root. **No `.tex` inside `anc/`**, and the
  source must not `\input` from it — links break at announcement, and full text in `anc/`
  is not indexed.
- Filename charset: `a-z A-Z 0-9 _ + - . , =`, case-sensitive. Verify:
  `tar -tzf f.tar.gz | grep -P '[^a-zA-Z0-9_+\-.=]'` → want empty.
- No embedded JavaScript in the submission PDF (hard fail at upload).

## Gate 4 — PDF property audit

```bash
python3 - <<'EOF'
import pymupdf, re
raw = open('submission.pdf','rb').read()
d = pymupdf.open('submission.pdf')
print("embedded JS:", len(re.findall(rb'/JS\b|/JavaScript', raw)))          # want 0
fonts = {f[3] for p in d for f in p.get_fonts(full=True)}
print("unsubset fonts:", [n for n in fonts if '+' not in n])                # want []
print("low-text pages:", [i+1 for i,p in enumerate(d) if len(p.get_text().strip()) < 50])  # want []
EOF
```

Embedded JS fails the upload; un-embedded fonts break portability; a page with no
extractable text is invisible to indexing and to every LLM/crawler reader.

## Gate 5 — human gates (report, cannot close)

| Gate | Fact |
|---|---|
| **Endorsement** | First submission in a category needs ≥1 endorsement from an established arXiv author in that category. Institutional email + claimed authorship of prior papers can waive it; personal email cannot. |
| Endorser hunting | On any arXiv abs page, "Which authors of this paper are endorsers?" links the endorsable authors — authors with no link cannot endorse. Seek candidates from the papers you cite, one at a time; mass-mailing is against policy. |
| Account + license | Register as author, pick the license (CC BY 4.0 typical). |
| Category + metadata | Primary + cross-lists, comments (`9 pages, 4 tables, 4 figures`), plain-text abstract. Wrong category = moderation delay. |
| Self-submit | Third-party submission is allowed only under limited conditions — you cannot submit "for" the author. |

## Gate 6 — hash-manifest verification

When the package is described by a `sha256sum` manifest (agent-built or relayed from
another machine):

1. **A hash with no object on this host is a claim, not a receipt.** Search the usual
   roots first; if the file is absent, report UNVERIFIED — never restate the digest.
2. Recompute each digest after the file lands, compare full 64 hex, never a prefix.
3. **A matching digest proves identity, not correctness.** Then reconcile contents:
   parts sum to the stated total, every number cross-checks against the manuscript,
   and the file the manifest names is the file you actually read.

## Pitfalls

- **Build dir ≠ tarball.** Compiling in the working directory passes while the tarball
  fails, because `.aux`/`.bbl`/local figure copies paper over missing inputs. Always
  cold-extract first.
- **Cosmetic warnings ≠ blockers.** Report `^!` errors, undefined refs, JS, missing
  fonts; do not pad the verdict with underfull-hbox noise or the author cannot tell
  what actually blocks them.
- **Technical PASS ≠ submittable.** Say the two gate classes on separate lines.
- **Don't claim an action you did not run.** If you said you replaced a file in the
  package, the digest you quote must come from a probe of that file *after* the write —
  a digest quoted from the plan rather than the disk is fabrication.
