# ⚒️ AAA PDF Voice Protocol — arifOS Federation

> **STATUS:** BINDING for all AForgePublishCompiler output · 2026-07-21
> **Authority:** F13 SOVEREIGN directive (Arif)
> **Doctrine:** DITEMPA BUKAN DIBERI

## The Rule (Wajib)

Every PDF artifact rendered by `aforge_publish` MUST be written in **human language cognitive context** suitable for a peer-reviewed geological publication (AAPG Bulletin / PETRONAS technical report voice).

**Zero robotic syntax. Zero raw code. Zero governance plumbing visible in the artifact.**

## The Translation Map

The internal epistemic machinery stays — it never goes away. Only the **rendered text** changes.

| Internal state | Renders as |
|---|---|
| `[OBS]` | "Measured Data" / "Observed Ground Truth" |
| `[DER]` | "Calculated Surface" / "Derived Geometry" |
| `[INT]` | "Geological Interpretation" |
| `[SPEC]` | "Uncalibrated Polygon" / "Conceptual Outline" / "Hypothesised Extent" |
| `geox_falsify(mode='full')` | "Validated against regional geophysical models" |
| `K001-K007 Kill Matrix` | "Seven-layer geological consistency test" |
| `INCONCLUSIVE` verdict | "Model requires additional calibration before deployment" |
| `F1 AMANAH` / `F11 AUDIT` | "Data provenance cryptographically verified" |
| `Falsification gate` | "Model suitability assessment" |
| `AForgePublishCompiler` | "Document preparation pipeline" |
| `ClosedLoopVisualValidator` | "Independent technical review" |

## Voice Rules

1. **Passive technical voice.** "The data were collected…" "Models were evaluated…" not "We collected data" or "I ran the model."
2. **Geological terminology over system terms.** Use *Moho*, *sediment thickness*, *Curie isotherm*, *rift-sag*, *half-graben* — not *backend*, *payload*, *payload key*, *hash chain*.
3. **No function names in figure captions, legends, or body text.** If a section needs to reference an evaluation, write the conclusion in plain geological language.
4. **Source citations in scientific style.** "Madon (2021)" not "Madon 2021 PDF file." "NOAA/NCEI EMAG2v3 (Maus et al., 2009)" not "/root/.cache/geox/emag2/EMAG2_V3_UpCont_DataTiff.tif."
5. **Uncertainty language, not system jargon.** "Model B agrees with the magnetic observation within combined uncertainty (σ = 9.2 nT)" not "z=0.03 PASS."
6. **Receipts stay machine-readable, but never enter the human artifact.** The SHA256, call hashes, and validator outputs remain in `.receipt.json` and `.validator.json` files; the PDF itself contains only human prose.

## What MUST Remain in the PDF

- Author/editor names
- Executive summary in plain English
- Methodology section in geological terms
- Data sources with proper scientific citations
- Maps, sections, charts with legends
- Uncertainty statements in physical units (nT, km, %, etc.)
- Conclusions in geological language
- The PDF is signed by `arifOS Federation · DITEMPA BUKAN DIBERI` as a watermark

## What MUST NOT Appear in the PDF

- Raw code, file paths, class names, function names
- Epistemic tag literals (`[OBS]` etc.) — they are translated
- Governance tag literals (`F1`, `Kill Matrix`, `INCONCLUSIVE`)
- Internal status codes (`PASS`, `FAIL`, `WARN`, `SEAL`, `HOLD`, `VOID`)
- Diagnostic stack traces, log lines, validator output JSON
- `arifos://` resource URIs
- SHA256 hashes (these live in `.receipt.json`, not in the PDF)

## Enforcement

- The translation layer is implemented in `aforge_publish.voice_translator`
- All three backends (ReportLab, Typst, WeasyPrint) call `translate_artifact()` before rendering
- The matplotlib figure legend helper `make_geological_legend()` replaces raw `[OBS]`/`[SPEC]` with rendered text
- `ClosedLoopVisualValidator` retains its internal vocabulary in `.validator.json` but the PDF never echoes it

## How Future Agents Must Implement

```python
from aforge_publish.voice_translator import translate_artifact, translate_figure_legend

# 1. Translate the manifest in-place before compile
manifest = translate_artifact(manifest)

# 2. Replace raw legend labels in matplotlib figures
labels = translate_figure_legend(["[OBS] Malay Basin", "[SPEC] other 14"])
# → ["Measured Ground Truth (Malay Basin)",
#    "Uncalibrated Polygon (other 14)"]
```

The translator is idempotent and stateless. Apply once, ship forever.

