# Trust and Verification — Threat Model, Verification Ladder, Honest Gaps (condensed from report ch. 5–6, dim09, dim10)

Load this file before sealing, redacting, or adjudicating any PDF. Core doctrine (I5): trust is
anchored OUTSIDE the artifact. The file is evidence; the ledger is proof.

## 1. Threat model — why in-file trust is insufficient

| Attack / failure | Evidence | Doctrine consequence |
|---|---|---|
| Shadow attacks on signed PDFs | Mainka, Mladenov & Rohlmann (NDSS 2021, CVE-2020-9592/9596): standard-compliant content hide/replace defeated signature validation in 16 of 29 tested viewers | A viewer's signature checkmark is a claim, not evidence. Never conclude integrity from it |
| Redaction by overlay | Failure record: Manafort (Jan 2019), Kentucky AG v. TikTok (Oct 2024), DOJ Epstein files (Dec 2025) — black rectangles over live text layers | Redaction = content REMOVAL + rasterize-verified re-extraction. Never cosmetics |
| Metadata leakage | ~39–40k PDFs from 75 security agencies / 47 countries mostly leaked hidden data; 1,237 files "sanitized" with exiftool still yielded full metadata — the tool removes the reference, not the object (arXiv:2103.02707) | Metadata sanitization requires object-level removal; treat all internal metadata as claims |
| Internal dates | PDF internal dates are rewritable | Dates inside the file are claims, never evidence. Time comes from RFC 3161 |
| Hallucinated success (agent-side) | Premature termination + skipped verification >14% of observed multi-agent failures (directional, secondary); agents hallucinate tool invocations (Google ADK issue #4173) | Decouple the success signal from the agent that did the work (F9 Anti-Hantu) |

## 2. The anchor protocol (D5)

```
content bytes -> SHA-256 digest -> Merkle leaf -> append to hash-chained DAG (VAULT999)
              -> RFC 3161 qualified timestamp where evidentiary grade is required
```

Reference logic (per report snippet S8):

```python
import hashlib
h = hashlib.sha256(open(path, "rb").read()).hexdigest()
leaf = hashlib.sha256(bytes.fromhex(h)).hexdigest()  # Merkle leaf over file digest
anchor = {"artifact": path, "sha256": h, "merkle_leaf": leaf,
          "ledger": "VAULT999", "status": "SEALED"}  # append to hash-chained DAG
# VOID on any mismatch. RFC 3161 qualified timestamp added where evidentiary
# grade is required; internal PDF dates are claims, never evidence.
```

- Evidentiary grade: PDF/A-4 (ISO 19005-4, on PDF 2.0) for permanence + PAdES-B-LTA with a
  qualified RFC 3161 timestamp. eIDAS Article 41(2) gives qualified timestamps a presumption of
  accurate time and data integrity that reverses the burden of proof — no in-file mechanism does this.
- veraPDF (pinned installer) gates any PDF/A or PDF/UA conformance claim. qpdf does not.
- Redaction events are the one sanctioned irreversibility: content is destroyed, but the EVENT is
  recorded as a new hash-chained VAULT999 entry — provability of what/when without retaining content (F1 Amanah).

## 3. The four-gate verification ladder (D7) — deterministic first, model last

Mismatch at any gate is a hard fail, never "log and continue."

| Gate | Method | Pass criteria | Failure response |
|---|---|---|---|
| G1 Structural integrity | `qpdf --check`; `pdfinfo`; `pdffonts`; veraPDF for PDF/A/UA profiles | qpdf exit 0; page count = expected; every font `emb=yes`; no `uni=no` CID fonts; veraPDF "PASSED" for declared profile | Regenerate from source; rebuild ToUnicode maps; embed fonts; do not ship |
| G2 Rasterized visual QA | `pdftoppm -png` per page; deterministic checks first (blank-page size/luminance heuristic, bbox non-empty); vision model second | Zero blank pages; no clipping; no tofu glyphs; every claimed chart present on its expected page | Re-render with explicit waits (`networkidle0`, `waitForSelector`); `printBackground: true`; provision fonts; regenerate figures |
| G3 Text round-trip | `pdftotext` / PyMuPDF on the RENDERED artifact; sentinel assertions; word-count tolerance vs source | Extraction non-empty; all sentinels found; no CID-garbage sequences | OCR fallback on corrupted layers; regenerate with proper subsetting/ToUnicode |
| G4 Adjudication (model-last) | LLM judge against rubric, only after G1–G3 pass; judge pre-validated | Judge reports chance-corrected kappa; position-swap consistency; 3 runs at temperature 0 | Reject or re-baseline the judge; an unvalidated judge verdict is void |

G4-data (data accuracy): every number printed in the PDF is recomputed from the source data by the
generator script — never hand-typed — and any derived statistic (ratios, projections) must disclose
its computation basis in the artifact or its sidecar; a hand-typed narrative number is FABRIKASI.

G4 discipline: the largest LLM-judge study (21 judges, ~541k judgments) found raw agreement
overstates quality by 33–41 percentage points of kappa deflation; self-family preference reaches
67–82% in high-risk contexts. An unvalidated judge is a NEGATIVE verifier — it manufactures
confidence. `scripts/pdf_verify.sh` implements G1–G3; G4 is human/judge protocol, not a script.

Tool-OK != page-correct: blank pages, missing backgrounds, and tofu all return exit status 0 from
the generator. A zero exit status is evidence that a process completed, not that a page rendered.

## 4. FABRIKASI — the negative capability list (claims VOID until probed)

- Live re-rendering of data inside an opened PDF — render happens at build time; "live" means a
  pre-render snapshot frozen into the artifact.
- Audio embedded in PDF — possible via reportlab, but no verified federation pattern exists.
- Pixel-perfect modern CSS Grid via WeasyPrint — partial support; Chromium headless is the probed
  path for JS-heavy layouts.
- Better-than-95% OCR on heterogeneous real-world scans or handwriting — clean print at 300 DPI is
  98–99%; hand-filled forms stay below 95% document-level; degraded documents fall to 72.7% (wet);
  handwriting belongs to frontier VLMs (1.2–1.5% CER on IAM, capped near 85% on hard medical forms).
- Voice-to-PDF in one step — unbuilt; the chain is speech-to-text -> Markdown -> pandoc, and it is
  doctrine only once probe-verified end-to-end.
- Trustworthy redaction of third-party PDFs without content destruction + rasterize-verified
  re-extraction.
- Any integrity conclusion from a viewer's signature checkmark (shadow attacks, 16/29 viewers).
- Tagged PDF from raw reportlab — output is UNTAGGED PDF 1.4. Closing paths (unprobed): pandoc +
  LuaLaTeX `-V pdfstandard=ua-2` (TeX Live 2025), or Typst >=0.14 (tags by default).
- Symmetric conversion promises: PDF->DOCX fails ~6.2% vs DOCX->PDF ~1.1%.

Any assertion of the above without fresh probe output is FABRIKASI — fabricated until probed — and
VOID under F4 Clarity. Say what the federation cannot do, in writing; that registry is doctrine.
