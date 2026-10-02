# hermes-pdf-intelligence — KVM4 Verification Receipt (2026-10-02)

**Relay:** irfanclaw (KVM4) · **Author:** Kimi (FI-008, deep-research swarm) · **Source:** `Kimi_Agent_Unified PDF Skill Map.zip` forwarded by ARIF 01:37 UTC
**ZIP sha256:** `136afa2e97e730c90fb54275e36b713c5581dfc21bd0f41be7cbd93eb699c17c` (44 files, 3.4 MB)

## Verdict: ACCEPTED — skill verified by live execution, not by reading

### Cross-node probe divergence = doctrine proven (the key result)

Same `scripts/probe_manifest.sh`, two nodes, same hour:

| Tool | Kimi node (reported 01:46 UTC) | KVM4 (probe run 01:48 UTC) |
|---|---|---|
| pandoc / weasyprint / qpdf / xelatex | PRESENT | **MISSING ×4** |
| chromium | MISSING → google-chrome route | MISSING (google-chrome 153.0.8010.36 PRESENT) |
| poppler (pdftotext/pdftoppm/pdfinfo) | PRESENT | PRESENT 26.01.0 |
| tesseract / soffice / gs / mutool | — | MISSING |
| py: reportlab/pymupdf/pypdf/pdfplumber/pdfminer/weasyprint | — | **MISSING ×6** |
| py: matplotlib | — | PRESENT 3.10.7 |

This is not a contradiction — it is the skill's own core law ("the same federation node differs per machine; yesterday's probe is a claim") demonstrating itself. A capability map without probe output would have been wrong on at least one node.

### Live tests executed on KVM4 (all PASS)

1. `pdf_verify.sh` on Kimi's own 74-page report `HERMES_PDF_Intelligence_Report.pdf` → G1 pdfinfo OK (74pp), G2 rasters OK (pp.1, 74), G3 extraction 24,440 words, sentinel found. VERIFY PASS. (qpdf gate correctly reported MISSING→weakened on this node.)
2. Eval brief hash check: recorded `74f96d78d10e69b345a4ad93ffca8eef67fe3e756f884f58459bfe6ac6ccd7e8` == recomputed. **Byte-exact trust anchor.**
3. `pdf_verify.sh` + sentinels on eval brief → PASS (1 page, 225 words, "XAUUSD MORNING BRIEF" ×2, "4112.44" ×3).
4. `md_to_pdf.sh` route ladder read: xelatex → weasyprint → chromium/google-chrome → soffice; wkhtmltopdf FORBIDDEN by standing order (CVE-2022-35583 CVSS 9.8). On KVM4 the first three engines are MISSING → script correctly exits 2 with "capability VOID" instead of pretending. **Failure path verified as honest.**

### Eval quality note (with_skill vs without_skill)

Both one-page XAUUSD briefs computed stats from the same CSV without hand-typing. Differences are methodology labels, not fabrications: with_skill used MA21 + explicit verification capsule + hash anchor; without_skill used MA24 + RSI(14). with_skill demonstrates the doctrine (gates, sentinels, receipt); without_skill is the competent baseline.

### Relationship to federation PDF work (same day)

- Consistent with dossier v1.1 (13 real skills, 9 symlinked from `/root/AAA/skills/`), Wawa v2 render-verify gate, v3 FigureAsset spec. This skill **operationalizes** the verification-gate doctrine: `probe → route → cognition → verify → anchor`.
- Trust-anchoring ladder (SHA-256 → Merkle/VAULT999 → RFC 3161) matches the convergence index "trust lives outside the file" lesson.

### Distribution

- Canonical copy staged: `skills/hermes-pdf-intelligence/` (this commit) — AAA repo is the federation skill source of truth (9/13 PDF skills already symlink from it per dossier v1.1).
- Kimi's node-local install at `/root/.hermes/skills/hermes-pdf-intelligence/` remains his discovery view; nodes may re-link to canonical at next sync.
- 6 eureka lessons already in `eurekas/eureka-entries.jsonl` (origin/main blob `f3d21d7d`), attributed FI-008.

### Open item (Arif's one-binary, relayed from Kimi)

Eureka entries currently live in the jsonl lane only. Writing them additionally to carry-forward (writer denied FI-008 — correct gate behavior) or kernel L2 memory requires a lease minted with Arif's confirmation. **Held, not bypassed.** Arif: say the word and Hermes routes it through the lease flow.

---
DITEMPA BUKAN DIBERI · every PASS above is an executed command on KVM4, 2026-10-02 01:47–01:52 UTC · irfanclaw
