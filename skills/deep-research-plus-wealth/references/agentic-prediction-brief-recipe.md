# Agentic Prediction Brief — Plain-Track Recipe

When the user asks for a 1–5 year prediction on a state-linked institution (NOC, GLC, central bank, sovereign wealth, large listed company with government nexus) and wants to read the deliverable themselves, this is the working recipe. Proven 2026-10-05 (PETRONAS 2026–2028, 12 pages, 310KB, plain track, delivered as PDF via MEDIA:).

## When to use plain track vs dark dossier

| Track | Trigger | When |
|---|---|---|
| **Plain** (this recipe) | "PDF untuk aku baca" / "literature grade" / no fancy visual / the institution is the user's own employer (F7 insider bias) | User reads alone |
| **Dark dossier** | "PDF mode" / "create a dossier" / "brief [named third party]" / impress a counterparty | Recipient looks at the artifact |

If unclear, default to plain for self-reads. The user has corrected this: dark theme reads as theatre when the audience is the user themselves.

## End-to-end pipeline (proven, ~10 minutes wall)

```
1. Probe live state (parallel):
   - zai_search entity + 1 event + 1 forecast (3 calls, serial — see pitfall)
   - yfinance live via urllib (Brent, KLCI, USD/MYR, US10Y) — proven one-liner
   - Internal atlas/router if entity is known (PETRONAS → /root/AAA/canon/PETRONAS/ATLAS.md)
2. Draft 8-layer structure (see deep-research-plus-wealth SKILL.md §3-Year Forecast Variant)
3. Build matplotlib chart pack (4 charts, see "Chart pack" below)
4. Write single-file HTML with embedded CSS (see "Plain-track CSS" below)
5. Render: weasyprint brief.html brief.pdf  (5-15s)
6. Verify: pdfinfo brief.pdf | grep Pages  (target 12-15 pages)
7. Visual QA: pdftoppm -r 100 -f 1 -l 2 brief.pdf qa -png  →  vision_analyze on the PNGs
8. Deliver: MEDIA: <absolute path>  + 10-line chat summary (verdict + scenarios + key tripwires)
```

## Chart pack (4 charts, all matplotlib, light theme)

Use a shared `rcParams` block: ivory background, Times family, navy `#1a2744` / gold `#b8860b` / red `#a33` / green `#2e7d32` / grey `#777`. White axis face, no top/right spines, grid `#eee`. Width `8.6 in`, height `4.2 in`, DPI 160.

| # | Chart | Recipe | Why it works |
|---|---|---|---|
| 1 | **Revenue & PAT bars** (grouped, FY-by-FY) | Two `ax.bar(x-w/2)` and `ax.bar(x+w/2)`, one NAVY, one GOLD, value labels above each | Surfaces the YoY narrative in one glance; trends visible across 4-5 years |
| 2 | **Physical vs price twin-axis** (the single highest-value chart) | `ax.bar(...)` for the volume series (RED, left axis) + `ax2.plot(...)` for the price series (NAVY, right axis). `ax2.grid(False)`, combined legend | Breaks the "high oil = high revenue" myth; matches the user's physical-vs-price rule (see weekly-sovereign-brief-2026.md) |
| 3 | **Subsidy paradox** (grouped bars, two series) | `ax.bar(x-w/2)` green = dividend; `ax.bar(x+w/2)` red = subsidy bill | Mandatory for any NOC analysis. Crosses when subsidy > dividend. From subsidy-paradox skill |
| 4 | **Production / output trend** (bars, aspirational grey) | Bars in NAVY for past, lighter shade for forecast horizon. Value labels above | Shows decline-as-baseline; forecast is clearly different from history |

Always include `chart_n_name.png` reference in HTML via `<img src="...">` relative path. Caption underneath in italic grey, with [OBS]/[DER] tag and source.

## Plain-track CSS (sovereign reading, no theatre)

Palette:
- Background `#fcfaf3` (ivory, never pure white — pure white reads as Word doc)
- Primary text `#1a2744` (navy)
- Accent gold `#b8860b` for rules, h3 subheaders, one verdict box border
- Secondary muted `#555` for metadata, captions, footer
- Tag pill colors: OBS=navy, DER=gold, INT=dark red, UNK=grey, all white text 8.5pt bold

Type:
- Body: `'Times', 'Liberation Serif', serif`, 11pt, line-height 1.45
- H1 (section): 15pt bold navy, `border-bottom: 0.6pt solid gold`, `padding-bottom: 2pt`
- H2 (page-break section): same + `page-break-before: always`
- H3 (sub): 12pt bold gold
- Caption: 9.5pt italic grey
- Verdict box: ivory background `#f7f3e8`, `border-left: 3pt solid gold`, 8/10pt padding, bold body
- Footer: @page rules for left "Project · Plain Track" + right "Muka N" + bottom gold rule

Do not include: dark backgrounds, sans-serif, emoji icons, dashboards/gauges/thermometers, animated anything. The plain track is "literature grade" — read like a book chapter, not a briefing slide.

## Section order (the user's reading shape)

1. Cover (title + subtitle + meta + 1 verdict callout + skop paragraph)
2. §1 — State of reality, what mainstream media misses (3-5 numbered sub-findings)
3. §2 — Structure / 3-5 drivers (each with trajectory + bracket)
4. §3 — Scenarios (3-4 weighted, table form, P% + trigger + 2027 indicator + risk)
5. §4 — Mainstream myths (5 ranked, claim / what it sounds like / what's actually true)
6. §5 — Tripwires (6-8, table form, ambang + trigger + severity TINGGI/SEDERHANA/KRITIKAL)
7. §6 — Reading for the user (work, macro, portfolio) + Omega question + Self-falsification block
8. §7 — Appendix: primary sources, secondary sources, numbers bank, void analysis

The Omega question is one italic blockquote with a single line the user could repeat to a third party. The self-falsification block is 4-6 ranked items, each = "what would change my mind + direction + new central value".

## Search routing pitfall (zai_search entity queries)

`mcp__zai_search__web_search_prime` with `location=my`, `content_size=high` is the right tool for Malaysia/entity research. But generic entity queries can return off-topic ads (Maxis, insurance, etc.) as the top 5 results. **Fix shape:**

```
"INSTITUTION" "PERSON FULL NAME" YEAR ROLE  (quotes around org + person)
```

Example that failed: `PETRONAS Tengku Taufik 2026 contract` → Maxis ads. Shape that worked: `"PETRONAS" "Tengku Muhammad Taufik" 2026 PCEO` → 5/5 on-target. If still drifts, drop `content_size=high` (returns shorter summaries, same page list).

The failure is a query-shape problem, not a tool failure. A 5-bullet `web: []` or 5-bullet ad block is a sign to rephrase, not to abandon the search.

## Visual QA gate (mandatory)

Before sending the PDF:

```bash
pdftoppm -r 100 -f 1 -l 2 brief.pdf qa -png
```

Then `vision_analyze` on the PNGs asking:
- (1) Is the title readable and the cover clean?
- (2) Do the h3 subheaders render correctly under h1?
- (3) Any text overflow off the page?
- (4) Are the charts present and uncropped?

If the chart captions run off, the chart is too tall — drop height from 80mm to 65mm or split into 2 pages. If the verdict box overflows, split the verdict into 2 sentences and reduce padding. The user will catch chart axis-label overflow in 1 line; pay it before sending.

## Insider bias disclosure (F7)

When the institution is the user's own employer, the brief must include one line: "Insider bias disclosed — user is [role] at [institution]." Place in the Skop paragraph or the §7 void analysis. The bias is acknowledged so the reader can discount accordingly. Do not hide the affiliation to seem neutral; the user has caught this kind of laundering before.

## What "agentic prediction" means in this lane

The deliverable is **a scenario tree with calibrated probabilities + falsifiers**, not a point forecast. Every main thesis carries:
- a bracket (e.g. "PAT RM45-60B by FY2028")
- a central value (e.g. "central RM52B")
- a probability (e.g. "60%")
- a falsifier (e.g. "Brent <USD 65 sustained 6+ months → bear case")

A point forecast is theatre. A bracket is honest. The probability is INT, not OBS — label it. The falsifier is the load-bearing claim: it tells the future session *when* to re-cast the central case.

## Proven numbers (do not re-derive; just confirm with one fresh probe)

- Brent live: `urllib` Yahoo Finance `BZ=F` (5d), `[meta]['regularMarketPrice']`
- KLCI: `^KLSE` ticker
- USD/MYR: `MYR=X` ticker
- US10Y: `^TNX` ticker (proxy for MGS regime; no direct MGS in Yahoo)
- PETRONAS IFR H1/FY numbers: from `petronas_vitals.py` or `/root/AAA/canon/PETRONAS/ATLAS.md` table (refresh one per session, do not trust cached >30 days)
- Subsidy bill: from `references/weekly-sovereign-brief-2026.md` anchor bank if the brief is within 14 days of the weekly brief

If any number drifts >5% from the cached value, re-probe live and label as DER (re-probed). Cite the source body, not the aggregator.

## Common failure modes to avoid

- **One-number forecast** with no bracket or falsifier. The user reads it as a guess.
- **5+ scenarios** without a clear central case. The user reads it as covering bases.
- **10+ tripwires** with overlapping triggers. The user reads it as unfocused.
- **Mainstream-myths section** that restates the myth without naming the *specific* mainstream source ("media often says X" is lazy; name the outlet).
- **Void analysis** that lists things the agent does not know about the institution. The user wants *what the institution's own release omits* — the deliberate silences, not the unknown unknowns.
- **No self-falsification block.** The user has caught fact errors at 1-bar speed. Visible self-audit signals the brief is a working draft, not a sealed artifact.
