---
name: empirical-audit-pdf
description: Audit PDF, every claim probes live.
---

# Empirical Audit PDF — probe-grounded, single-script

Class-level skill. Trigger: the user asks for a research/audit/capability-map/stack-inventory PDF and emphasises *ground truth*, *attention*, or *unified view* of a system's actual state. Examples: "map all X tools and capabilities", "give me the real state", "audit the stack", "prove what works". Trigger phrases: "map all", "audit", "real state", "ground truth", "what can actually do".

This is NOT a markdown-to-PDF task (use `forge-pdf-delivery`). It is a probe → live-data → chart → assemble pipeline where every figure in the document traces back to a terminal command or API call.

## The one rule

**Every claim in the PDF backs to a probe or live API response captured during the same script run.** No "as documented" claims. No screenshot-of-a-prior-session charts. No skill-catalog recital. The artifact's evidence density is its credibility.

## Pipeline — one Python script, four phases

1. **Probe binaries + Python libs.** `subprocess.run` for every binary the audit touches (`pandoc --version`, `weasyprint --version`, etc.), plus `python3 -c "import lib; print(lib.__version__)"` for every Python lib. Two-column table in the PDF. This is the empirical ground.

2. **Live data via API.** `urllib.request.urlopen` to the federation's own endpoints (gold ticker, macro snapshot, well registry, etc.) or to any external URL the audit depends on. One data fetch, multiple charts derived from it. NEVER use stale data.

3. **Charts as PNG via matplotlib.** Dark theme (`#0d1117` background, `#e6edf3` text, `#f0a500` gold accent). Save PNGs to a scratch dir. Prefer line / bar / candlestick / imshow heatmap — whichever the data shape fits. Each chart gets a one-line caption naming the source.

4. **Assemble into PDF via reportlab.** Embed the PNGs with `reportlab.platypus.Image`. Build the same dark theme via `HexColor` constants and `ParagraphStyle`. Tables for probe results, snippets, gaps, decision matrix. `PageBreak` between major sections.

5. **Verify.** `pdfinfo` for page count, `pdftotext -layout` for text-layer presence. For dark-theme pages, ink-coverage sweep is unreliable (whole page is dark); use per-page char count via `pdftotext -f N -l N file.pdf - | wc -c` — designed pages carry 800+ chars, spill pages < 300.

## Structure — cognitive-attention-first (default 4 pages)

| Page | Content | Why |
|---|---|---|
| Cover | Title, subtitle, date, mode, source, goal (4-line table) | Reader knows what they're holding in 5s |
| 1 | Live numbers table + 1 chart (live-fed, captioned with source) | First signal in <30s |
| 2 | Installed-inventory table + capability heatmap chart | Empirical ground |
| 3 | Snippets (4–6 copy-paste-ready code blocks) + 2-min decision matrix | Reader can act |

Total: 4 pages A4, ~200KB, single Python file end-to-end. The 2-min decision matrix is the payoff — reader picks up `if you want X, use Y, because Z` and walks away.

## Procedure rules (always-on)

- **Probe before claim.** Never say "weasyprint supports X" without running it in the same script. The probe output is in the artifact's first table — the reader verifies the audit verified itself.
- **Live data, not screenshots.** Charts are generated from a live API in the same script run. The artifact loses value the moment the data is stale. If the API is down, write `API DOWN @ <time>` into the table — do not fabricate.
- **Snippets must run.** Every code block must execute when pasted into a Python 3 REPL on this VPS. Pseudo-code is fabrication.
- **No skill-catalog recital.** When the user says "map all skills", they mean the resulting capability surface, not a 200-skill table. Compress into the heatmap + gaps table. Catalog names that don't add to the decision matrix don't belong.
- **One Python file.** Probe + chart + assembly all in `build_audit.py`. Don't split into separate scripts — the user wants one place to read and modify.
- **Dark theme by default.** Empirical audits read as "research product"; the dark theme signals to the reader that the principal has live infrastructure, not static documentation. Light theme only if the user explicitly asks for plain-text.
- **Honest gaps section is required.** A "What is NOT here" table that names what the stack cannot do today, and an honest-move column for each. Without this, the audit reads as marketing. With this, it reads as engineering.

## Pitfalls (read before authoring)

- **`plt.Rectangle` is NOT exported from `matplotlib.pyplot`.** Use `from matplotlib.patches import Rectangle` then `ax.add_patch(Rectangle(...))`. Pyright/lint catches it; runtime AttributeError is silent until the figure renders empty. Same for `Circle`, `Polygon`, `Wedge`.
- **Set `MPLCONFIGDIR=/tmp/.mpl` and `matplotlib.use('Agg')` BEFORE `import matplotlib.pyplot`.** Without Agg, headless servers fail on first `plt.show`; without `MPLCONFIGDIR`, pyrolite user config emits a non-fatal `legend.bbox_to_anchor` warning every call. Both cheap to set up-front, expensive to forget.
- **Dark-theme pages break ink-coverage blank-page detection.** Every page reads ~98–100% regardless of content. Use per-page char count (`pdftotext -f N -l N file.pdf - | wc -c`) instead: designed pages carry 800+ chars, spill pages < 300.
- **`matplotlib.patches` text + `set_aspect('equal')` = silently-vanishing labels.** Drop `set_aspect('equal')` for infographic-style charts; place text and patches in DATA coords matching `set_xlim`/`set_ylim`. Save WITHOUT `bbox_inches='tight'`. Gate every figure: `(np.array(Image.open(f).convert('RGB')).mean(axis=2) > 200).sum()` must exceed zero.
- **Live API responses are dict-shaped, not always list-shaped.** Probe the shape first (`type(d).__name__` and `list(d.keys())[:10]` for dicts, `len(arr)` for lists) before indexing. A `mat[i][j]` crash on the wrong shape costs more than a 3-line probe.
- **`subprocess.run` for `--version` calls may emit to stderr.** Capture both: `out = subprocess.run(cmd, capture_output=True, text=True, timeout=5); first = (out.stdout or out.stderr).strip().split('\n')[0]`. Empty stdout on a tool that only writes stderr is normal.

## Templates

- `templates/analytics-audit-pdf.py` — copy-paste scaffold. Probe + 2 chart funcs + 4-page assembly + verify. Replace the probe list, the live API call, the chart definitions, and the decision-matrix table — keep everything else.

## Companion skills

- `forge-pdf-delivery` — markdown-to-PDF pipeline (different task: prose-heavy documents, no probes). Load it for CSS skeletons, but the empirical-audit pattern is its own pipeline.
- `forge-artifact-publisher` — EMD output reflex arc; defines the artifact types but expects the data already shaped. Use this skill when data shaping is trivial; load `empirical-audit-pdf` when every claim needs a probe.
- `forge-document-intelligence` — INPUT direction (PDF → structured data). Different class of work.