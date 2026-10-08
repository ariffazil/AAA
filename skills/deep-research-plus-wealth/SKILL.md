---
name: deep-research-plus-wealth
description: "Seven-layer institutional intelligence artifact for F13 SOVEREIGN. NOT a report — a judgment container. Load when producing analysis that must change the quality of judgment, not the quantity of information."
tags: [research, wealth, intelligence, arif-standard, institutional-artifact]
version: "2026-08-06-v2"
ratified: "2026-08-06 by F13 SOVEREIGN — evolved from 4-layer to 7-layer specification"
---

# INSTITUTIONAL INTELLIGENCE ARTIFACT

> "Do not write a report. Build an artifact that helps a human make a better irreversible decision."

## What this is

NOT: Report, Memo, Dashboard, Research Paper.

YES: Institutional Intelligence Artifact.

Purpose: change the quality of judgment. Every page must justify its existence. Every chart must answer one question. Every conclusion must have a falsification path. Every verdict must have a control set.

## The 7-Layer Architecture

### Layer 1 — Reality (OBS only)
What happened? Evidence. Sources. Facts. No opinions. Timeline, Financials, Governance structure, Projects, Partnerships. Every claim must survive deletion of all opinions.

### Layer 2 — Structure (DER only)
How does the system work? Dependencies, Networks, Power, Capital flows. Explain how the system works, not whether it is good or bad.

### Layer 3 — Computation (WEALTH tools)
What do the models say? NPV, Monte Carlo, Scenarios, Sensitivity, Stress tests, Governance Capacity, Veto Concentration, Beautiful Mouse, Stress Index, Responsibility Ledger. For every tool: Input, Output, Coverage, Known defects. VERDICT_CONFLICT if tool contradicts evidence — do not resolve.

### Layer 4 — Governance
Who decides? Board composition, Control, Vetoes, Independence, Conflicts, Dual roles, Published charters.

### Layer 5 — Incentives
Who benefits? Reward, Fear, Constraint, Exposure. Career incentives. Capital incentives. What must be true for each actor to behave as claimed.

### Layer 6 — Cognitive Layer
What is everyone pretending not to see? Blind spots, Unknowns, Contradictions, Stale data, Rhetoric vs substance. The artifact must attack itself here.

### Layer 7 — Omega Layer
What is the one uncomfortable question? The artifact collapses to one sentence. That sentence is usually the most valuable thing in the document.

### Visual Doctrine — Live Models Over Static Charts (ARIF'S OVERRIDE)

**Arif's explicit doctrine (2026-08-06):** "Why so many static graphs? Bake that into the model slider. Use ExxonMobil modeling toolkit. Make interactive live model with full human clarity."

**Arif's second doctrine (same session):** *"Are u sure your graph is correctly put?"* — the model must pass a calibration check BEFORE you trust its visual output. The user will inspect the numbers, not the pretty curve. If the curve looks right but the readout at the headline value is wrong (e.g. PETRONAS dividend RM 260B at $95 — 6× the real RM 45.4B PAT), the chart is theatre, not analysis. Always surface a numeric readout next to the chart and prove it against a known anchor.

Static PNGs are decoration. Live sliders with real-time canvas rendering are instruments. Every variable becomes a slider. Every output becomes a readout. Every model lives in the browser, not in a PDF.

### When to use each:

| Approach | When | Why |
|---|---|---|
| **Live canvas + sliders** (PREFERRED) | User wants to "play" with the model, explore scenarios, ask "what if" | Arif builds for agents and humans who interact, not passively read |
| **Static chart** (backup) | Deliverable must be a non-interactive PDF for offline/attachment | PDF cannot run JS — use matplotlib PNG, embed in HTML |
| **Both** | PDF deliverable + live web page | Build the engine first (HTML/JS), then screenshot static for PDF |

### Live engine architecture (proven on arif-fazil.com):
1. **One script block, all functions in scope.** Shared constants at top. Each engine (panel) in its own IIFE. Cross-references use global functions, not repeated calculations.
2. **Canvas > SVG for this use case.** Canvas renders at 180 DPI, no DOM overhead, clean for dark themes.
3. **Readouts are one signal per element.** No duplicate cards, no redundant badges, no "probe lines" that repeat what the cards say.
4. **Cross-link panels bidirectionally.** "→ see sovereign side" on panel 1, "← corporate side" on panel 2.
5. **Calibrate from reported data, not from assumptions.** See `subsidy-paradox-calibration` skill for the PETRONAS precedent: calibrate from MoF reported bill ÷ known per-unit gap, not from total national consumption.

### Critical calibration pattern (lesson learned):
```
WRONG constant: assume total pool × assumed per-unit gap
RIGHT constant: actual pool = reported total bill ÷ known per-unit gap
```
The PETRONAS subsidy model was wrong by 2x when calibrated to total national fuel consumption (38B L/yr). Correct pool: 17B L/yr, derived from RM 42B/yr reported ÷ RM 2.46/L gap.

### Visual vocabulary (when static charts are needed):
Line charts, bar charts, waterfalls, sensitivity matrices, Monte Carlo fans. Answer: "What happened?"

### Cognitive Visuals (primary — prefer live versions):
Power Map — who controls whom
Veto Map — who can stop decisions
Incentive Map — who benefits
Risk Topology — where collapse begins
Governance Geometry — where authority concentrates

Gentari's governance geometry chart is stronger than 20 pages of prose. But a live version with sliders is stronger still.

## Mandatory Sections

### What We Know (OBS)
### What We Think (DER)
### What We Cannot Prove (UNKNOWN)
### What Would Falsify This Artifact
### Control Set — Compared to whom? Peer distribution → Percentile → Verdict. No comparison = no verdict.
### Binding Constraint — ONE load-bearing variable. Why every other risk flows through this one.
### Omega Question — The one uncomfortable question that survives after all numbers are removed.

## Language Style

Short. Declarative. Dense.

Bad: "Gentari appears to have potentially significant growth prospects which may result in..."
Good: "9.1 GW is real. Governance is the constraint. The question is who controls the upside."

### Override signal — "So what?" / "stop narrating"

When Arif says **"So what?"** after an audit, review, or meta-analysis, the meaning is:
*ship the corrected artifact, not a meta-narrative about the critique*. The expected output
of "audit this artifact" is **the corrected artifact**. The v2 audit workflow:

1. Identify the gaps from the audit (claim IDs, semantic grammar, countercase, operator matrix, falsifier).
2. Build the corrected v2 in one pass — claim IDs inline, semantic chart palette, verification ledger as appendix.
3. Ship the v2 with a 5-line delta summary, not a 15-line analysis of the critique.

A session that produced a self-audit before being asked to "ship it" earned "So what?" — the
user wants the artifact, not the analysis-of-the-analysis. The v2 deliverable should take
roughly the same wall-clock time as the v1 because the corrections are scoped, not invented.

### Sibling audits hallucinate too — verify before folding

When a sibling/delegated agent produces an audit or any artifact that you intend to fold
into a v2, its claims are **inputs, not truths**. Verified 2026-08-07 on a sibling Apex
audit of the weekly brief: it shipped 3 factual errors that survived two reads.

| Error class | Example | Live correction |
|---|---|---|
| Date drift | "Warsh takes over September" | Warsh sworn in May 22, 2026; he already chaired the Jul 29 hold |
| Invented magnitude | "JPM target set when oil was $122" | Brent never hit $122 in 2026; causal anchor was fabricated |
| Fabricated quote | "Morningstar: odds of rate cut vanished" | No such quote locatable; attribution was unverified |

Discipline: live-verify every temporal claim, magnitude claim, and attributed quote in a
sibling artifact against one primary source before writing it into the v2. Output a
verification ledger (claim ID / gate / verdict / source) as a mandatory appendix. The
`apex-fact-check-pass` skill encodes the three gates (DATE / MAGNITUDE / QUOTE) and is the
pre-seal verification layer for any Apex/WEALTH PDF render.

### Cross-bot verification rule (2026-08-08) — gates on infrastructure liveness

When a sibling audit makes claims about infrastructure being "down/off/dead", the verification ledger MUST include a live probe per service before endorsing. Verified 2026-08-08 on OpenClaw's L5/FalkorDB audit:

| OpenClaw claim | Live probe | Truth |
|---|---|---|
| "Ollama NOT RUNNING" | `curl :11434/api/tags` → returned `bge-m3:latest` + `qwen2.5:3b` | ❌ FALSE — Ollama healthy with models loaded |
| "Graphiti MCP :8000 returns nothing" | `curl :8000/health` → `{"status":"healthy"}` | ❌ FALSE — MCP responding |
| "Qdrant offline" | `curl :6333/collections` → 7 collections including `arif_evidence` | ❌ FALSE — Qdrant has real data |
| "L5 pipeline dead at every link" | Infrastructure alive end-to-end; only `graphiti_semantic_floor` flag = `disabled` | ⚠️ PARTIAL — infrastructure alive, semantic floor disabled |
| "0 kernel log calls" | confirmed | ✅ TRUE |
| "Nothing depends on L5 today" | confirmed (`graphiti_semantic_floor: disabled`) | ✅ TRUE |

OpenClaw's narrative frame ("dead pipeline") was wrong; the actual finding was "infrastructure alive but floor disabled". Three of four "down" claims were false. **The audit was high-confidence wrong.** This is a separate failure mode from the 2026-08-07 Apex case (3 factual errors, otherwise sound architecture): this one **mistook a disabled feature flag for missing infrastructure**.

Gate rule: every claim of the form "X is OFFLINE/DEAD/MISSING" requires a live probe (`curl :PORT/health`, `docker ps`, `systemctl status`) with the exact command recorded in the ledger. Narrative state descriptions ("dead pipeline", "no traffic", "silent") are NOT infrastructure probes.

### The audit-of-the-audit pattern (2026-08-07)

When Arif pastes a sibling SEAL/Apex report and asks **"audit and validate this"**, the
deliverable is a **verification ledger of the audited artifact**, not a meta-analysis of
the critique. Two failure modes to avoid:

- **Confident agreement** — endorsing the audit's claims without re-probing. The 333-AGI
  SEAL-9e3e38d3adb3459b report (Aug 7) claimed "no unexpected exposure" on UFW, but live
  `ss -tlnp` showed `hermes pid=3015207` listening on `0.0.0.0:8444` with no UFW rule.
  Endorsing that line would have left a public listener unreported.
- **Confident dismissal** — rejecting the audit wholesale because some claims look
  suspicious. The same report's *architecture* (DID registration, DISPLAY_ONLY ceiling,
  OpenClaw as EDGE warga) was correct; the *fact layer* was wrong. Reject the bad claims,
  keep the good ones.

Workflow:

1. Build a verification ledger table: **Claim (with C-ID) × Live-shell evidence ×
   Verdict** (✅ TRUE / ⚠️ PARTIAL / ❌ FALSE / ❓ UNVERIFIABLE). One row per consequential
   claim. Each row references the exact live command that proved or disproved it
   (`ls -la /root/AAA/auth/keys/openclaw_private.key`, `find /root/.openclaw -name
   "*bridge*"`, `wc -l /root/arifOS/VAULT999/outcomes.jsonl`).
2. For each ❌ row, show the live counter-evidence with the matching command. For the
   333-AGI report: the DID key exists (✅), the registry entry exists (✅), but the "bridge
   skill on disk" is not findable (❌), and FQ=1.11 is outside the designed 0–1 range (❌).
3. Report self-assessment: "Trust the report at ~70%." Numbers, not vibes.
4. If real gaps exist, ship the corrected v2. If not, verify the existing v1 stands.

Cost of getting it wrong: a meta-analysis of the audit without a verification ledger is
worthless to Arif. He reads the verification table, not the prose. Bullet items must
reference the exact live command that proved or disproved them.

## When Arif Pastes an External Audit of Your Own Session

Distinct from auditing siblings (above) — here the audit is OF YOU, delivered as a chat paste. The instinct is to defend, agree without grounding, or pivot to the next task. All three fail.

**Procedure:**
1. **Acknowledge each finding separately** with the verb pattern: "fair / true / I missed that / partially agree / disagree because X". Do not bundle into a single paragraph of acknowledgment — the user reads the row-level mapping, not the prose.
2. **Classify the defect** (in your own work, not the auditor's taxonomy) into one of:
   - L1 — symptom→verdict shortcut ("X rosak" without raw evidence)
   - L2 — misread of a documented constraint (tool capability vs workaround)
   - L3 — missing coverage / stopping-rule without criteria
   - L4 — receipt-less action or unverified retry
   State which L each finding maps to, briefly. This is your self-audit ledger, not theatre.
3. **Distinguish "in my lane" from "not in my lane."** Production config drift, model transport integrity, MCP federation health, A-FORGE actuator auth, service restart — these are upstream of mouth. Acknowledge and route; do not claim authority to fix.
4. **Default L0 memory save** (defect pattern + remedy) WITHOUT asking the user. The user will compress to "consolidate, save as one compact entry" if needed — but the act of asking "should I save this?" is itself a friction pattern (CLARIFICATION TOLERANCE = zero).
5. **Cluster F13 binaries by risk**, then ask ONE short binary per cluster. Never batch "all of B/C/D/E" into one approval — that is menu-dump at the audit-response layer, same defect class as the original audit found.
6. **State enforcement status honestly** — "operating rule only, not fully enforced until Phase 0 validates" — not "fully fixed". The audit found a discipline gap; saving the lesson is not the same as closing the gap.

**Pitfall: defense-via-classification.** A clean L1/L2/L3/L4 grid can become a way to *reframe* the failure rather than own it. Write the acknowledgment in plain BM first, then attach the grid as a ledger. The grid is a record; the prose is the receipt.

**Pitfall: routing the lesson to the wrong target.** Mouth saves its own operational memory; engineering lane saves config/transporter/MCP work. Do not let mouth save "need to pin web.search_backend" — that is upstream work and gets lost if the mouth session ends.

**Pitfall: turning one approved action into four "while we're at it" follow-ons.** The user approved *A* (memory save). A/B/C/D/E are five more, not one. Each gets its own binary.

## Research Session Discipline — Terminal States & Evidence Ledger

A research session is not "done when the answer feels done." It is done when one of four terminal statuses can be honestly emitted, with an evidence ledger that a future session can re-probe.

**State machine (apply to every deep-research turn, not just the headline brief):**

```
SCOPE → PLAN_AXES → SEARCH → EXTRACT → EVIDENCE_LEDGER
      → GAP_ANALYSIS → COUNTEREVIDENCE → SYNTHESIS → VERIFY → DELIVER
```

Each transition emits a receipt: inputs, provider, URLs, evidence hashes, errors, cost, duration, next state. Synthesis is GATED by the prior five — never by the model's confidence.

**Terminal statuses (mandatory, exactly one per session):**

- **COMPLETE** — all material axes covered, key claims cross-checked against ≥2 independent sources, citation verification passed, counterevidence searched.
- **PARTIAL** — useful evidence exists, named gaps remain, list them explicitly. The user reads the gap list, not the prose.
- **BLOCKED** — retrieval, authorization, or provider failure prevents a defensible answer. Name the failure class (provider quality / dispatch drift / tool-call transport / agent policy).
- **REFUSED** — request violates a policy, legal, or safety boundary. Not "I don't want to."

**Pitfall: "Aku ada cukup" as a stopping rule.** The model finishing its evidence search is not the user accepting the answer. Always emit one of the four statuses. The 4-class taxonomy is the *receipt*, not the *feeling*.

**Pitfall: collapsing symptom to verdict.** "Web search is broken" without raw evidence is L1 — same defect class the audit caught this session. State the constraint, distinguish 4 root classes, then propose the smallest reversible probe. "Search returned unrelated results" is a probe-able observation; "search is broken" is a verdict.

**Pitfall: 1 round = enough.** A single `web_search` call rarely covers a research axis. Plan axes first (≥3 typical), execute parallel where the tool allows, sequence where the tool doesn't. Single-round coverage is a self-deception pattern, not a coverage claim.

**Pitfall: documented constraint vs improvisation.** `web_search` documented as single-query. `web_extract` accepts ≤5 URLs. `execute_code` is the designed orchestration path for 3+ tool calls. State the constraint, then use the designed path. Do not label a documented constraint as a tool defect because the first attempt returned noise.

**Pitfall: synthesis-from-incomplete-retrieval.** If the search returned unrelated results, the next step is *not* "synthesize from the one good result and proceed." It is "declare PARTIAL, name the gap, ask the user whether to retry with a different query shape or proceed with the partial base." The synthesis step does not absorb retrieval failures; it consumes their output.

**Tool-specific fallbacks (commit to memory as standing rule, not per-session discovery):**

| Tool | Documented constraint | Designed workaround |
|---|---|---|
| `web_search` (hermes `hermes_tools.web_search`) | single-query per call | `execute_code` loop for 3+ queries; alternate providers (exa / firecrawl / brave) via separate `tool_call` |
| `web_extract` (hermes `hermes_tools.web_extract`) | ≤5 URLs per call | `execute_code` loop for 6+ URLs |
| `mcp__exa__web_search_exa` (connector) | tool_call rejects multiple connector entries in one batch | one `tool_call` per search; use `execute_code` wrapper for loops |
| `mcp__brave_search__brave_web_search` | tool_call rejects multiple connector entries in one batch | one `tool_call` per search |
| `mcp__zai_search__web_search_prime` | first-result trap on commercial-intent queries | rephrase with quoted institution + year anchor; drop `content_size=high` if drift persists |
| PDF generation | default `pandoc -o out.pdf` produces duplicate title when H1 is also document title | keep H1 in source; let pandoc use the YAML `title:` field for the header |
| PDF delivery via MEDIA: | first attempt may not land; gateway may swallow the path | verify (path/size/magic/hash) before retry; on retry failure, switch route (re-attach with `MEDIA:` re-emit, or save to `~/.hermes/cron/output/` and send via `local` delivery), never repeat the same directive without a state change |

**Counterevidence is mandatory, not optional.** For any non-trivial claim (especially a Big-Four-style empirical claim, a "men want/need" generalization, a market forecast, an attribution), the search plan must include at least one query shaped to DISCONFIRM the headline. A clean confirmation set with no disconfirmation probe is F2 risk.

**Evidence ledger shape (compact, write once at session close):**

```
research_ledger:
  axes_planned: N
  axes_covered: M (with N-M named as gaps)
  sources_total: K
  sources_independent: ≥2 for each headline claim
  counterevidence_probed: yes/no
  terminal_status: COMPLETE | PARTIAL | BLOCKED | REFUSED
  falsifiers_named: list
  open_questions: list
```

**The synthetic-essay variant carries this too.** When the ask is a reflective-essay (per the variant above), the same state machine applies but EXTRACT and COUNTEREVIDENCE shapes differ — sources are philosophical/textual, not empirical. Counterevidence there = opposing schools of thought, not opposing datasets.

## Rendering Doctrine — Human Language, Frameworks Invisible

The 7 layers and any named frameworks (Acemoglu, Calhoun, Gödel/Hofstadter, Ostrom, "strange loops", "principal-agent voids") are **thinking scaffolding**. They inform the analysis; they must NOT appear in the deliverable unless Arif explicitly asks for them by name. Verified correction 2026-08-06 (PETRONAS collapse brief): Arif said *"I want full human language and focus on PETRONAS. No need to mention mouse godel lock etc"* after the framing pass named frameworks. Lesson: propose the frame once at kickoff, drop it on first pushback, never re-introduce. The "7-layer" label may appear on the cover badge only — not in chapter prose.

**The subsidy paradox is mandatory for ANY NOC / national-oil-company analysis (2026-08-06).** High oil is NOT a bull case for the nation. The paradox: rising Brent → rising PETRONAS dividend → BUT rising fuel subsidy bill that moves faster. At Brent above ~$95/bbl, Malaysia spends MORE on fuel subsidies than it receives from petroleum revenue. This inverted the entire "high oil = windfall" frame that the original PETRONAS collapse analysis missed. The lesson for all future NOC analyses:
- ALWAYS model the sovereign side alongside the corporate side — they are one machine, not two.
- ALWAYS include the subsidy bill curve as a live slider, not a static chart (for live-site deliverables).
- ALWAYS check whether the net position (petroleum revenue − subsidy bill) flips negative at any point in the Brent range.
- ALWAYS cross-link corporate and sovereign pages bidirectionally at `#subsidy-paradox` anchors.
See `pdf-report-generation` skill `references/petronas-subsidy-paradox-2026.md` for the numbers bank, and `arif-fazil-site-ops` skill for the live-site interactive engine pattern.

**Calibrate constants against reported data, not assumptions (2026-08-06, learned the hard way).** First version of the subsidy model used 38B L/yr (total national fuel consumption). At $85 Brent + RM 1.99/L BUDI95 cap, the model output subsidy = 38B × RM 2.46 = RM 93.5B/yr — but the *actually reported* steady-state is RM 3.5B/month ≈ RM 42B/yr (not the April RM 7.5B/month war-spike). The model was off by 2.2×. The fix: derive the constant from the reported figure, not the assumption. Formula: `actual_pool_L = reported_total_bill ÷ per_unit_gap`. Always cross-check: if the model's "headline value" number at a known anchor disagrees with a published value, the model is wrong, not the chart. Show the user the numeric readout before any chart.

For "when will X collapse / is it titanic / net debt / ranges and tripwires" requests, the output shape is:
- **Verdict-first plain prose.** No layer labels, no epistemic jargon in the narrative. Epistemic tags (OBS/DER/INT) live in table cells and chart captions only.
- **Scenario table with probabilities** (e.g. Soft landing / Structural squeeze / Full squeeze — 45/30/15%, plus base/tail/renewal as needed).
- **Tripwire dashboard:** 6-7 tripwires, each with threshold + trigger + severity (SEVERE / ELEVATED / WATCH).
- **Monte Carlo** on the load-bearing P&L variable (report median + P10/P90, never just mean).
- **Sensitivity tornado** (oil price dominates for any oil major — verify, don't assume).
- **"Where I'm wrong"** ranked by magnitude of swing, upside AND downside, ranked separately.
- **Honor the asker's stated bias** ("It's titanic now, but I'm bias") — acknowledge it, label INT, then test the bias against the bull case at equal rigour. **Do not collapse to the user's stated certainty.**
- **Page floor:** ≥13 pages for PDF deliverables of this class; all raw data tables → appendix with epistemic tag column.
- **Adversarial balance & scenario weights (Apex v2, 2026-08-07):** every main thesis carries a countercase block (steelman + one disconfirming datapoint + "what would make this wrong by next week"); no countercase → F2 violation risk. Replace single-path directional language with weighted 3-scenario branching (Base/Upside/Failure, e.g. 40/25/35), each with trigger + falsifier threshold — a scenario without a falsifier is decoration. Render contract (claim blocks C-IDs, source index S-IDs, decision packet, semantic-role chart palette): see `pdf-report-generation` → `references/apex-deliverable-protocol.md`.

## The reflective-essay variant (personal-reflection deep research — proven 2026-08-07)

When Arif pastes a personal/philosophical note (often Malay: attraction, identity, human nature) and asks "deep research on this" or similar:

- **Register switch.** "Full human language" for reflection = ESSAY register: warm, conversational, first-person, Malay voice kept ("aku/kau"), friend-thinking-out-loud. NOT the terse institutional register — "Short. Declarative. Dense." applies to intelligence artifacts only. If the first pass lands dense, expect "give me in full human language. I want to read for my understanding." — re-do in essay form, not just soften the same text.
- **Silent scaffolding applies here too.** He may name a theory ("relate to Jung human shadow") — integrate the CONCEPT throughout, never label sections with theory names. Jung/Bowlby/Damasio stay invisible in section headings; the thinking shapes the narrative without owning it. Same doctrine as PETRONAS v2: "No need to mention X by name."
- **The stated curiosity is the real question.** "I am still intrigued by X" outranks the original text. Center the essay on X (e.g. "how abang sado jadi sado" became a full chapter, not a side note). Follow the human question, not the source text.
- **Arc that landed:** (1) quote the original text verbatim as anchor → (2) unpack it line by line → (3) answer the curiosity in depth → (4) one human verdict → (5) three things he can carry. Body = pure narrative; sources → appendix ledger with epistemic tags (OBS/DER/INT/UNK).
- **PDF follow-up is standard.** He often follows with "PDF" — hand off to `pdf-report-generation` with the conceptual-diagram chart pack (matplotlib patches on dark navy, no data charts). See that skill's "conceptual chart pack" section.
- **Output format:** prose response first; the prose IS the artifact. PDF is the physical vessel, not a separate deliverable shape.

## Margin Doctrine

Left margin: Narrative (human reading path)
Right margin: Epistemic markers (OBS / DER / INT / UNK) — like military intelligence products

## Final Verdict Format

NEVER output: BUY / SELL / SEAL.

Output:
- OBS — what is proven
- DER — what is computed
- INT — what is interpreted
- UNKNOWN — what remains unverifiable
- BINDING CONSTRAINT — the one load-bearing variable
- FALSIFICATION TEST — what would prove this wrong
- OMEGA QUESTION — the uncomfortable one

## Agent Workflow (for delegated production)

| Agent | Produces | Layer |
|-------|----------|-------|
| Reality Agent | Timeline, Evidence, Facts | Layer 1 |
| Research Agent | Industry map, Peers, Benchmarks | Layer 2 |
| WEALTH Agent | NPV, Stress, Scenarios, Governance | Layer 3 |
| Adversarial Agent | "Why is this artifact wrong?" — mandatory | Layer 6 |
| Visualization Agent | Charts, Power maps, Dependency maps, Risk matrices | All |
| Editorial Agent | Turns all outputs into human story | Layer 7 |

## Quick Article Metabolism — Light variant (PROVEN 2026-08-09)

When Arif drops a URL expecting analysis (not a full 7-layer artifact):

1. **Extract** via `web_extract` first (fast, may get chrome). If chrome-heavy, fall back to `browser_navigate` pre-cookie snapshot.
2. **X-ray:** extract key findings, statistics, claims. Label every claim [OBS] or [INT].
3. **Map to federation:** for each finding, identify which arifOS organ/floor/weapon already addresses the problem. This is the "why does this matter to us" layer.
4. **Meta-observation:** one INT paragraph on what the article reveals about the industry's gap vs arifOS's position.
5. **Output:** compact structured analysis (table + bullets), NOT 7-layer artifact. ΔS negative = article metabolized.

Trigger: Arif drops a URL with no explicit ask ("init the session. <URL>"). Default = metabolize through arifOS lens, deliver X-ray. If he wants deeper analysis, he'll say so.

**Pitfall: TNS extraction.** thenewstack.io returns ~90% navigation chrome via `web_extract`. Post-cookie browser DOM is blank (headless detection). Best partial path: grab the initial browser snapshot BEFORE accepting cookies. Known site-specific extraction quirks — see `anti-bot-web-extraction` for Shopee/Lazada patterns.

**Pitfall: article ≠ institutional communication.** Industry journalism (The New Stack, TechCrunch, etc.) is NOT the same class as CEO interviews / earnings calls / government announcements. Do NOT load `institutional-communication-audit` for tech journalism — the 7-Layer Incentive Stack and Physical Constraint Questions don't apply to editorial content. Use this lighter pattern instead.

**Pitfall: forwarded session results.** Arif may forward a previous session's closing output as context. Treat as input data, not a new request. Acknowledge the forwarded result, then proceed with the actual new request (the URL). Do not re-analyze the forwarded content unless asked.

## Weekly Sovereign Brief — Recurring Pattern (PROVEN 2026-08-07)

When the ask is "what's happening this week / what do I need to know / weekly brief", load `references/weekly-sovereign-brief-2026.md`. It contains:
- **Search recipe** — 4 parallel rounds, ~20 queries, "August 2026 / this week" dated filters, Malaysia-specific sources (BNM, paultan.org, Bursa Malaysia)
- **6-chart pack pattern** — one matplotlib batch script, shared rcParams + NAVY/GOLD/RED/GREEN/BLUE/ORANGE palette: week-moves bar, gold 6-week OHLC, **twin-axis physical-vs-price** (the week's most valuable chart), subsidy paradox, Fed regime timeline, KLCI sector tape
- **State-of-world anchor bank** — re-probe before reuse; values shift week to week
- **Physical-vs-price verification rule** (Kpler lesson, 2026-08-05): WTI collapsed to $75.64 on "draft deal" headlines while Kpler showed only 5 tanker transits vs 20+ pre-war baseline the same morning. ALWAYS quote the physical number next to the price for any geopolitics-driven move (port throughput, cargo manifests, inventory draws, border crossings). The physical number is the F2 anchor; the price is a hypothesis.

This extends the "calibrate against reported data, not assumptions" discipline — same root pattern, applied to live news rather than static models.

### Malaysia macro-statistics — DOSM source map & numbers bank (2026-08-08)

When the ask is "GDP Malaysia ok ka", "industri macam mana", "statistik ni betul ke", "I don't believe that number", or any DOSM/BNM/MoF macro claim about Malaysia, load `references/malaysia-macro-statistics-2026.md`. It carries: the DOSM release cadence (advance vs final GDP dates — Q2 2026 final is 14 Aug), a verified Q1/Q2 2026 numbers bank with epistemic tags, the **7-holes framework** ("how correct statistics deceive": advance-vs-final psychology, per-capita vs median, re-export transfer pricing, subsidy-inflated GDP via G, deflator choice, informal economy ~30%, Penang/Johor concentration, each with Malaysia example + falsification test), and the **WEALTH :18082 capability boundary** (8 tools, 555_COMPUTE_ONLY, no national-stats tool — probe /health before claiming the organ computed anything; deliver macro audits from primary sources instead). Catches the "nombor betul boleh menipu" frame that landed for Arif: GDP says 5.6%, his wallet says otherwise — both are right; one is the country, one is him.

## 3-Year Forecast Variant — calibrated predictions for institutional / GLC horizons (proven 2026-10-05, PETRONAS)

When the ask is a multi-year forecast ("3-year prediction", "where is X in 2028", "next cycle outlook") for a state-linked institution (NOC, GLC, central bank, sovereign wealth), use a 8-layer variant that adds the **horizon-uncertainty discipline** the 7-layer collapse-brief shape doesn't carry.

### Why 8 layers, not 7

Collapse questions answer "when" with a tripwire dashboard. Multi-year forecasts answer "what range" with **calibrated probability bands + explicit falsifiers**. The cognitive layer collapses to a single omega *number* (e.g. "RM55B PAT is the new normal, not the floor") — not a question. The structural difference forces 2 new layers:

- **Layer 0 — State of reality right now** (audited + interim, with date stamps on every figure)
- **Layer 8 — One-line so-what** (single number/claim that survives all numbers being removed)

### Structure

| Layer | Content | What makes it different from 7-layer collapse |
|---|---|---|
| 0 | State of reality (audited FY + latest interim, dated) | Every figure has a date stamp; "H1 2026" not "this year" |
| 1 | Mainstream media narrative vs reality gap | Table format: claim / what it sounds like / what's actually true |
| 2 | Real drivers (typically 3-5) | Each driver gets a 12-36 month trajectory with bracket, not a point |
| 3 | Calibrated predictions | Probability bands (e.g. 60% / central, 25% bear, 15% bull) + falsifier + horizon for every prediction |
| 4 | Mainstream media reality check (ranked) | Top 5 things mainstream gets wrong, each ranked by impact |
| 5 | What this means for the user (if user is positioned) | Only fire if user has a position; labelled "not financial advice" |
| 6 | Unknown / what I cannot tell you | Mandatory; ranked by how much each unknown would flip the predictions |
| 7 | Falsifiers to track monthly | 2-4 monthly trackable signals that would force re-cast |
| 8 | One-line so-what | Single number, the load-bearing claim in one sentence |

### Identity-probe-first gate (mandatory for entity research)

Before framing any hypothesis about a person, organization, or institution with semi-specified identity (partial name, role assumption, "the current CEO of X"), **probe the identity with one search before writing a single hypothesis**. Verified failure mode 2026-10-05 (PETRONAS, also Tengku Taufik case from earlier sessions): "Tengku Taufik" or "SapuraOMV under PETRONAS" framed as expectation analysis, both premises wrong, all downstream H1-H8 false. Pattern is class-level: when memory contains a partial anchor + role assumption, parametric slot-fill generates plausible-but-wrong facts.

**Gate:** `zai_search` query = `full name + current role + organization`. Read first 3 results. Confirm current post, name spelling, career start. THEN frame hypotheses. The probe costs 1 tool call, ~20 seconds. Premise-mismatch costs the entire brief and a sovereign correction.

### Tool-call shape pitfall (verified 2026-10-05)

`mcp__claim_ledger__claim_record` and most local MCP tools **require** `calls[].name` as a top-level field, NOT inside `arguments`. The shape is:

```python
# CORRECT
tool_call(calls=[{"name": "mcp__claim_ledger__claim_record", "arguments": {...}}])

# WRONG — silently fails with "name required"
tool_call(calls=[{"mcp__claim_ledger__claim_record": {"arguments": {...}}}])
```

If `tool_call` returns "calls[0] requires a 'name'", the fix is the field position, not the argument shape. Retry once with corrected shape; if it still fails, skip the ledger and write claims to a local file as receipts. Don't loop.

### zai_search batch limit (verified 2026-10-05)

`tool_call` with multiple `mcp__zai_search__web_search_prime` entries in one `calls[]` array is **rejected** with "tool_call takes exactly one entry for local tools; you sent N". Serial per query, not batched. The error message is literal. Each search = one tool_call. For 5-6 queries, budget 5-6 tool_calls, ~30-60s wall.

### Plain-track vs dark-theme PDF (proven 2026-10-05, PETRONAS brief)

The "sovereign theme" colors in the PDF pipeline above are the dark dossier track. When the user reads the PDF *for themselves* (not for a third party to look at), use the **plain track** instead. The trigger words in the request: "PDF untuk aku baca", "literature grade", "no fancy visual", or no clarification + the deliverable is a forecast of *their own* institution (insider bias disclosed, F7). Plain track recipe lives in `references/agentic-prediction-brief-recipe.md` — ivory background, Times serif, gold rules, no boxy callouts other than one verdict box, charts use the same palette as the dark track but on white, and the visual QA gate (`pdftoppm` → `vision_analyze` for chart-bearing pages) is mandatory before sending.

### zai_search for entity queries — first-result trap (verified 2026-10-05)

`mcp__zai_search__web_search_prime` with `location=my` and `content_size=high` is the right tool for Malaysia/entity research, but a query like `"PETRONAS Tengku Taufik 2026 contract"` can return Maxis/insurance ads as the top 1-5 results if the routing backend reroutes on commercial-intent signals. Symptom: 5 results, none mention the named entity. **Fix:** rephrase with the institutional org as a quoted term and include a year or event anchor: `"PETRONAS" "Tengku Muhammad Taufik" 2026 PCEO` — quoted institution raises the precision. If the first rephrase still drifts, drop `content_size=high` (returns less summary text per result, but the page list is the same). Do not let a 5-bullet "web: []" block convince you the tool is broken — it is a query-shape failure, not a tool failure.

### Self-falsification block — required at end of every prediction brief (added 2026-10-05)

The "di mana aku mungkin salah" / "where I'm wrong" block is not optional decoration. It is the single section that makes the brief legible to a future session and to the user re-reading it after a year. Format: 4-6 ranked items, each = (a) what would change your mind, (b) which direction it would move the central case, (c) the new central value if it fires. The user has caught Arif-side fact errors in 1 line before; a visible self-falsification block reduces sovereign-attention cost on re-reads and signals epistemic honesty.

### Calibration doctrine — bracket not point

Multi-year forecasts fail when they give a point ("PETRONAS PAT 2028 will be RM60B"). They survive when they give a **bracket with calibrated probability + falsifier + horizon**:

```
P1: FY2026 PAT RM60-75B (probability 70%, central RM65B)
    Falsifier: Brent sub-$65 sustained 6+ months, or Petros negative ruling 2026
P2: FY2027 PAT RM48-65B (probability 60%, central RM55B)
    Falsifier: geopolitical oil spike (Iran-Israel, Hormuz, Russia-Ukraine)
```

Bracket is honest. Point is theatre. Central + range + probability + falsifier = a claim a future session can grade.

### PDF pipeline (proven, 44KB output, 2026-10-05)

For SOVEREIGN-grade deliverables where Arif will read in Telegram, render to PDF:

```bash
# 1. Write the .md
# 2. Write the .html with embedded CSS (sovereign theme: navy #0b3d2e, gold #c9a227)
# 3. Render
python3 -c "from weasyprint import HTML; HTML('brief.html').write_pdf('brief.pdf')"
# 4. Send via MEDIA: path in response
```

`weasyprint ≥ 70.0` is the proven engine. `pandoc` and `google-chrome` are also available but weasyprint is fastest for the sovereign HTML style. Output ~44KB for 7-page brief, ~5-15s render time.

The HTML must be self-contained: `<style>` in head, no external CSS/JS, no web fonts (weasyprint will fetch-blocking). Use system fonts. Tables for media-narrative-gap data; semantic chart grammar colors (see artifact-rendering-doctrine.md).

### Critical of mainstream media — required, not optional

For institutional / GLC / NOC analysis, build a **media-narrative-vs-reality table** in Layer 1. For each mainstream claim, write 3 columns: (1) what mainstream says, (2) what it sounds like, (3) what's actually true. Verified value: every column the user has read is downstream of (a) institution's comms, (b) PMO/government comms, (c) bank research. None of these are incentivized to surface negative scenarios. The table forces the artifact to surface what mainstream won't.

**Counter-evidence suppression** is the most common failure mode. Watch for: framing language ("stable", "managed", "smooth", "aligned with"), absence of unit-error corrections (24.5 mmboe "reserves" was actually daily production equivalent), and PM-speak treated as evidence.

### Memory correction discipline

When a probe contradicts a memory entry (SapuraOMV = TotalEnergies, not PETRONAS; "24.5 mmboe reserves" is daily production rate), **state the correction explicitly in the brief** before proceeding. The user catches these at 1-bar speed. Corrections acknowledged in the brief = less sovereign attention cost than corrections caught by the user.

## Knowledge banks (load on trigger)

| Ask pattern | Reference |
|---|---|
| "What are the darkest things AI agents can do?" / dark mirrors / scheming / agentic risk | `references/ai-dark-mirror-research-2026.md` |
| "What's happening this week" / weekly brief | `references/weekly-sovereign-brief-2026.md` |
| "GDP Malaysia ok ka" / DOSM/BNM macro claims | `references/malaysia-macro-statistics-2026.md` |
| "I'm still intrigued by X" / personal-philosophical reflection | `references/attraction-love-shadow-research-2026.md` |
| "3-year prediction on [NOC/GLC]" / institutional multi-year forecast | This skill's "3-Year Forecast Variant" section above + `references/agentic-prediction-brief-recipe.md` (plain-track CSS, chart pack, HTML pipeline, search routing). PETRONAS canon: `/root/AAA/canon/PETRONAS/ATLAS.md` (router: `PETRONAS-intelligence-router`) |

## Source-Discovery Fallback

When planning any research run, assume `web_search`/`web_extract` may be unavailable (Tavily backend HTTP 432). Have the direct-curl arxiv fallback ready: `references/arxiv-fallback.md` documents the API base URL, query syntax (avoid `AND`/`OR` keywords; use `all:term1+term2` for implicit OR; `id_list=` for known IDs), proven query templates by domain, and the ~8-query rate limit. Use this before assuming web tools will work — a pip install or apt-get isn't needed; curl + grep is the universal fallback.

## Reference Architecture

v1 (2026-08-06): Asked "What is Gentari?" → got 9.1 GW narrative
v2 (2026-08-06): Asked "What is the geometry?" → got governance_capacity 0.2883/3.0
v3 (2026-08-06): Asked "What is everyone pretending not to see?" → layered 7-layer artifact with falsification paths, control set, omega question
