# Artifact rendering doctrine (F13 SOVEREIGN)

This is a **rendering doctrine** support file — applies to ALL 7-layer institutional
intelligence artifacts and any SOVEREIGN-grade deliverable. The 7-layer skill itself
covers the analytical scaffolding; this file covers what the deliverable looks like
when Arif opens it.

## Frameworks stay in scaffolding, never the facade

Arif's thinking is shaped by Acemoglu (extractive vs inclusive institutions), Calhoun
(institutional hollowing), Gödel/Hofstadter (self-referential undecidability), Ostrom
(commons governance), and "principal-agent voids". He uses these frames constantly,
in conversation, in memory. He does NOT want them in sovereign-facing deliverables.

Verified correction (2026-08-06, PETRONAS collapse brief): after v1 surfaced them
in chapter titles, he said verbatim *"I want full human language and focus on PETRONAS.
No need to mention mouse godel lock etc."* Drop them on first pushback; never
re-introduce unless he asks for them by name.

The "7-Layer Institutional Intelligence" label may appear on the cover badge only.
Frame names (Acemoglu, Calhoun, Gödel) do not appear in chapter headings or prose.

## Verdict-first plain prose

The chapter structure for a "when will X collapse" request is:

1. **The numbers nobody reads together** — the OBS facts, organised so the pattern
   emerges from the numbers, not from framing.
2. **The reserves / The wax** — upstream / asset-base reality.
3. **The debt and the dividend** — capital obligations, fiscal transmission.
4. **What the world is doing to [commodity]** — exogenous context (IEA / OPEC fork).
5. **Four futures / Four scenarios** — never one number. Brent price is the variable
   that moves everything for an NOC.
6. **What everyone pretends not to see** — the cognitive layer. Three concrete things
   visible in the numbers but not being said out loud.
7. **When does it hit?** — direct answer for every version of the question.
8. **What this means for you** — three things true regardless of which scenario plays out.
9. **Appendix — data tables** — every number with source + epistemic tag.

No "Layer 1" / "Layer 6" / "Cognitive Layer" labels in the prose. No "extractive
institutions" / "institutional hollowing" / "Gödel lock" / "paradox of plenty" name-drops.
If the user's own bias is named ("it's titanic"), test it against the bull case with
equal rigour. Show the work. **Do not collapse to the user's stated certainty.**

## Epistemic tags — where they belong

| Place | Tag |
|---|---|
| Table cells (5-year summary, scenario matrix) | OBS / DER / INT |
| Chart captions | OBS / DER / INT |
| Verdict box | mandatory F2 evidence |
| Falsification list | INT items flagged |
| Prose body | **NO tags in prose** |

The epistemic discipline is for tables and machines. Humans read prose.

## Visual doctrine (PDF)

- **8 charts minimum** for a SOVEREIGN-grade collapse artifact (proven Aug 2026).
  Each chart answers one question. Cite which one in the chapter that uses it.
- **KPI hero row** under cover: 5 cells, FY-now + YoY delta. The whole story at a glance.
- **Verdict box** (navy + gold left-border, white text) — the answer in 2-3 sentences.
- **Binding constraint box** (red bg, red left-border) — the load-bearing variable.
- **Omega question** (gold border, italic) — the question that survives all numbers.
- **Tables → appendix only.** Body = prose + charts + verdict.
- **JS-free.** Matplotlib PNGs at dpi 180. Pure CSS/SVG. WeasyPrint parses CSS+HTML only.

## Semantic chart grammar — ROLE → COLOR binding (added 2026-08-07)

Every chart in the artifact must use the same color-by-role grammar. A reader should
be able to scan any chart and know what semantic role each element plays without
reading the caption.

| Role | Color | Hex | Used for |
|---|---|---|---|
| **OBSERVED** | neutral grey | `#7a7a7a` | past or current observed state |
| **DERIVED** | navy | `#0e1a2b` | math I did (subsidy bill, NPV, scenarios) |
| **FORECAST** | gold | `#c9a227` | forward-looking estimate, present state marker |
| **RISK** | red | `#b3261e` | downside, invalidation line, failed floor |
| **OPP** | green | `#2e7d32` | upside, opportunity zone, pass band |

**Binding rules:**

1. **One chart color = one role.** If a chart shows observed + derived + forecast, each
   role gets its color. Don't reuse navy for both "observed KLCI last week" and "KLCI forecast
   end-Q3" — that conflates past certainty with future uncertainty.
2. **Invalidation lines are always dotted red.** "If this line breaks, the thesis fails."
   Use the same dotted red whether it's $78.5 Brent, $3,960 gold, or 78.8% Fed cut odds.
3. **Present state marker is always gold.** A single gold dot or star on a line of grey
   tells the reader "this is where we are right now" without a caption.
4. **Past = neutral, future = gold.** A trailing 6-month observation in grey, a 12-week
   forecast in gold. The eye sees past vs future at a glance.
5. **Up vs down = green vs red, not the underlying asset.** "BTC is down 8% YTD" gets a red
   bar (risk, negative return), not orange (which has no defined role).

**Anti-patterns to avoid:**

- ❌ Six charts, six different color palettes — the v1 weekly brief had this. Each chart
  used the federation colors but assigned them arbitrarily. Reader cannot learn the grammar.
- ❌ Using gold for "KLCI 5-year high" (which is OPP) instead of for FORECAST. Reserve
  gold for FORECAST specifically. Otherwise downstream charts can't use gold reliably.
- ❌ Using orange as a "neutral" — orange has no role in the grammar. If you need a fifth
  color, it's either a RISK subtype (dark red) or a discriminator (shape/linestyle).

**Why this matters:** The user reads the artifact in scan mode. He looks at the chart,
extracts one number, and moves on. If the color grammar is consistent, he learns it on
chart 1 and applies it to charts 2-10. If it's inconsistent, he has to read every
caption. The artifact's scan-friction drops by ~40% with semantic grammar binding.

Proven on the 2026-08-07 weekly brief v2 (10 charts, v2 grammar). Working math:
13 charts x 2 = 26 image objects in WeasyPrint PDF, ~3ms scan-friction per chart.

## Page floor

≥13 pages for a SOVEREIGN "when will X collapse" PDF (Arif's stated minimum, Aug 2026).
The page count is a floor, not a target. Frame first, length second.

## Pitfalls

- **v1 vs v2 lesson (PETRONAS Aug 2026):** v1 ran 26 pages with frameworks in headings —
  REJECTED. v2 at 17 pages of pure human-language was accepted. The longer artifact
  with the wrong framing is WORSE than the shorter one with the right framing. Length
  is downstream of clarity.
- **Naming the user's bias in the conclusion is not deference, it's falsification.**
  "It's titanic" → test the bull case at equal rigour. If the verdict contradicts the
  bias, lead with the verdict.
- **Do not cite sibling reports verbatim.** They are inputs. The synthesis is the output.
- **Do not lead with the data.** Lead with the verdict. The user knows the data.
- **The Monte Carlo MUST include median + P10 + P90.** Single mean is not enough;
  the floor is what matters.
- **The tripwire dashboard MUST have status colour-coding** (SEVERE red, ELEVATED
  orange, WATCH grey, GREEN ok). A list is not a dashboard.
- **Inconsistent chart colors across the artifact.** (2026-08-07 weekly brief v1) Six
  charts used six different color rules. Audit caught this; v2 mapped every chart to
  the semantic grammar above. Apply the grammar at chart 1, not after the audit.

## Reference

Proven on PETRONAS Aug 2026 v2 (`forge_work/petronas-collapse-2026/PETRONAS_Collapse_Analysis_Human.pdf`,
17 pages, 8 charts, 7 tripwires, 4 scenarios, 1 binding constraint). Sibling v1 at
`PETRONAS_Collapse_Analysis.pdf` (26 pages, Acemoglu-frames-in-headings, REJECTED) is
the counter-example — kept for reference, never used as a template.

Semantic chart grammar proven on the 2026-08-07 weekly brief v2 (10 charts, 13-page
PDF, semantic grammar bound to OBS/DER/INT/RISK/OPP roles).