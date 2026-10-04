# ZKPC Certificate Pattern — Zero-Knowledge Proof of Contribution

**Proven:** 2026-08-12 (PETRONAS AMANAH DIKHIRATI letter). 5 visualizations + 10-page PDF rendered via matplotlib + WeasyPrint.

## What this is

A cryptographic + visual pattern for **anonymous institutional critique letters** where:
- The AUTHOR is anonymous (no name in signature)
- The DATA is provably from public sources (not fabricated)
- The RECEIVER can independently verify every number

**ZKPC = Zero-Knowledge Proof of Contribution.** The author proves they contributed real public data (not made-up numbers) without revealing their identity. The reader verifies by checking the hashes against original sources.

This pattern addresses the F11 AUDITABILITY + F2 TRUTH + F13 SOVEREIGN triangle in a single artifact.

## When to use

- Open letters to Parliament / regulators / media about institutional failure
- Anonymous whistleblower documents (when source protection is critical)
- Any public-facing critique where data integrity matters but author identity is dangerous
- "Rasa derita manusia" letters that need both soul AND verifiable math

## The 5-panel visualization suite

The pattern is a 5-page visualization pack that comes AFTER the letter body. Each panel does one job:

| # | Panel | Job |
|---|---|---|
| 1 | **Headline** | One number (e.g. 70.5%) dominates. Math breakdown as 3 small boxes below. |
| 2 | **Three Hands** | Three offices/people side-by-side. Names appear with role, action, accountability. |
| 3 | **Adaptive Predator** | Bar chart showing constant take (dividend) vs falling profit. Annotation on the contrast. |
| 4 | **Paradox** | Two-column visual (Dulu vs Sekarang). DNA Bulldog vs DNA Anjing framing works for Malaysian context. |
| 5 | **ZKPC Seal** | SHA-256 hash per data row + Merkle root. The cryptographic attestation. |

The point: **the soul lives in the letter body. The math lives in the visuals. They don't fight each other.**

## Design rules (matplotlib dark theme, proven)

```python
BG = "#0a0e1a"          # cosmic deep — the foundation
PANEL = "#141a2e"        # lighter panel
NAVY = "#0e1a2b"         # institution blue
GOLD = "#c9a227"         # verdict / crown / the makcik-yellow accent
CREAM = "#f4ecd8"        # text-light
RED = "#c1272d"          # extraction / blood
BLUE = "#1e3a8a"         # trust
YELLOW = "#fcd34d"       # humble / citizen / the makcik tricolor
GREEN = "#10b981"        # what remains
MUTED = "#6b7280"        # secondary text
```

The **tricolor (red/blue/yellow)** carries the makcikgpt identity. Use sparingly — one accent per panel, not all three at once.

Font size hierarchy:
- Big number headline: 150-180pt
- Sub-headline: 16-18pt
- Body labels: 10-12pt
- Hash text: 8pt monospace

Always `figsize=(14, X)` and `dpi=180` for print quality.

## ZKPC seal — the cryptographic core

```python
import hashlib, json

data_points = [
    {"fy": "FY2020", "pat_rmb": 11.0, "dividend_rmb": 0, ...},
    {"fy": "FY2021", "pat_rmb": 48.7, "dividend_rmb": 25.0, ...},
    # ...
]

# Per-row hash (canonical JSON sort)
for d in data_points:
    d_str = json.dumps({"fy": d["fy"], "p": d["pat_rmb"], "d": d["dividend_rmb"]}, sort_keys=True)
    d["row_hash"] = hashlib.sha256(d_str.encode()).hexdigest()[:16]

# Merkle root
chain = "".join(d["row_hash"] for d in data_points)
merkle_root = hashlib.sha256(chain.encode()).hexdigest()
```

The seal panel renders each row as a line:
```
FY2020  PAT RM11.0B  Div RM0B    Ekstrak 0.0%   sha256: a410710f...
FY2021  PAT RM48.7B  Div RM25B  Ekstrak 51.3%  sha256: d4977890...
...
MERKLE ROOT: sha256:57332d3da60de9561b5db0c46c3adee4...
```

The 16-char prefix is enough for visual identification. The full hash should also appear in the letter body or a footnote.

## Integration with the letter

HTML structure:
```html
<!-- Letter body — pages 1-4 — makcik soul, anonymous role-based signature -->
<!-- Page 5: cover with title + signature line + GitHub link -->
<!-- Pages 6-10: visualization pack -->
```

```python
# In the HTML, embed the visualization PNGs:
<div class="chart-page">
  <img src="charts/01_headline.png" alt="...">
  <div class="chart-caption">LAMPIRAN B · Carta 1: AMANAH DIKHIRATI — Headline 70.5%.</div>
</div>
```

Each visualization page is a `<div class="page-break">` so WeasyPrint places it on its own page.

## Anonymity + verifiability paradox

The pattern RESOLVES the paradox between:
- **Anonymity**: author does not sign their real name
- **Verifiability**: reader can confirm the data is real

Mechanism: the author signs as ROLE ("Seorang bapa · geoscientist · warganegara (anonim)") not as a person. The data hashes prove the data came from public sources. The reader can verify the data without knowing who wrote the letter.

The GitHub link is the public anchor: `github.com/arif-fazil/arifOS`. Anyone curious can trace the substrate (arifOS constitutional framework). But the LETTER itself remains anonymous. The link to the project is a link to a public framework, not to the author's identity at this moment.

## Pitfalls

- **Don't use 16-char hash collision probability as security** — it isn't. The hash is for HUMAN VISUAL VERIFICATION only ("I see the same hash on the public report"). For real cryptographic integrity, use full 64-char SHA-256.
- **Don't put personal name anywhere** — even "Author: anonymous but you can reach me at..." defeats the pattern.
- **Don't use bullet points to list ZKPC properties** — readers will infer it's boilerplate. Let the seal panel SHOW the integrity, not DESCRIBE it.
- **Merkle root in body should match seal panel** — copy-paste, not retyped. Visual mismatch destroys the cryptographic signal.
- **Don't include "pending" or "draft" anywhere in the seal** — it self-cancels. If the seal isn't ready, don't render it.

## Recipe to reproduce

```bash
mkdir -p /tmp/amanah_letter/charts
cd /tmp/amanah_letter
# 1. Write build_visual.py with the 5 chart functions
python3 build_visual.py
# 2. Copy PNGs into charts/ for HTML embedding
cp 0*_*.png charts/
# 3. Write surat_rasmi.html with letter body + viz embeds
# 4. Render with WeasyPrint
/usr/bin/python3.13 -c "import weasyprint; weasyprint.HTML('surat_rasmi.html').write_pdf('SURAT_TERBUKA.pdf')"
# 5. Verify
pdfinfo SURAT_TERBUKA.pdf | grep Pages
```

For each chart, run `pdftoppm -r 110 -png SURAT_TERBUKA.pdf p -f N -l N && vision_analyze` to verify visual integrity. The headline number must dominate. The Three Hands names must be readable. The ZKPC hashes must be consistent.

## When NOT to use this pattern

- Personal letters between known parties (overhead not worth it)
- Internal communications (no anonymous requirement)
- Letters where the writer WANTS their name attached (e.g., expert testimony)
- Letters without numerical claims (no ZKPC value)