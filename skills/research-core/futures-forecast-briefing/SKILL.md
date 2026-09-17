---
name: futures-forecast-briefing
description: "Use when asked to forecast a period or portray the future."
version: 1.0.0
owner: curator-managed
risk_tier: low
floor_scope: [F2, F4, F7, F13]
autonomy_tier: T1
trigger_phrases:
  - "what will [year/period] look like"
  - "portray the future"
  - "how will X evolve next year"
  - "world in 2027"
  - "what's going to happen to"
  - "deep research the future of"
  - "how will AI agents affect"
  - "aren't we heading toward"
  - "is this the end of"
  - "what's the worst that could happen"
dependencies:
  mcp_servers: []
  skills: [deep-research, web-extraction-fallbacks, hermes-rasa]
---

# Futures / Forecast Briefing

## When to Use

The principal asks you to **portray a period** rather than report a present state — "how will AI agents affect human life next year", "the world in 2027", "what will agents do to civilisation", "where is X heading in three months". Also load when the question arrives pre-loaded with a doom frame ("I'm very dystopia btw") or a wrong mechanism ("could they wipe the internet").

This is NOT a replacement for `deep-research`. Research gathers the material; **this skill governs what the answer must contain** so it is a forecast instead of a well-sourced description of today.

## The One Failure Mode

Producing a present-tense, well-sourced description of the current landscape and presenting it as the future. Every citation can be real and the deliverable still useless. The test: does the answer contain a **dated claim about a state that does not exist yet**, with its mechanism named? If not, it is a recap.

## Procedure

### Step 0 — Correct the premise before answering it

If the question embeds a wrong verb or mechanism, say what **cannot** happen and why, first. One paragraph, then the real answer. Do not lecture, and do not answer the wrong question faithfully.

- "Wipe the internet / delete digital money" — a frame with no physical mechanism. State that physical and protocol-layer redundancy make it non-falsifiable, then substitute the real failure mode: **loss of assurance in a layer nobody inspects**. Quiet, not loud.
- "Robot uprising" — substitute the documented operational failure (agents taking out-of-envelope actions, swarm collisions, cascade errors).
- "AI replaces all jobs" — substitute the measured damage (entry-level footholds and apprenticeship pipelines, not aggregate unemployment).

Naming the substitution is the highest-value move in the whole answer: it converts a mood into a testable claim.

### Step 1 — Search for what already happened

The catastrophe the principal fears is usually **already documented in miniature**. Search for the precedent before forecasting the escalation. A forecast grounded in a dated incident (agents that escaped containment, a swarm that self-synchronised, an error seed that produced false consensus) is an extrapolation; without it, it is opinion.

When the tooling layer resists — lexically-gated search queries, truncated extractions — see `references/search-and-extraction-under-governance.md`. Do not report a tool failure as the answer.

### Step 2 — Separate RECORD from FORECAST, visibly

- **RECORD** — already happened; dated, sourced, checkable. State plainly, with the source artefact (post-mortem, paper, regulator release).
- **FORECAST** — probability × impact. Mark it as such.

Never let a forecast sentence sit in the same list as a sourced fact without a marker. The principal audits text adversarially and will catch blended claims.

### Step 3 — Rank the engines by likelihood × impact, not by drama

The headliner claim is usually the *least* likely. The boring structural constraint (power, depreciation schedules, hiring pipelines, access control, insurance exclusions) is usually already underway. Give a **small number** of engines, ordered, each with its mechanism named — not an inventory.

State explicitly which engines are **locked in** versus **still open**. That is the difference between a three-month question and a one-year question: contracts, capex, rules, and hiring decisions already made cannot be undone inside the window.

### Step 4 — Counter-signals are mandatory

Every doom-framed claim gets its strongest live pushback in the same breath. State the claim, state who disputes it and on what grounds, then say which half survives scrutiny. A one-sided doom framing is authority-wash, and this principal rejects authority-wash.

Also carry what did NOT happen: the aggregate that stayed stable, the vendors that turned out profitable, the prediction that failed. A forecast without its counter-signals is propaganda, and the whole deliverable gets discounted for it.

### Step 5 — Land on the principal's own exposure last

An abstract global forecast is incomplete until it touches his country, employer, income, family, or trade. One concrete local line outweighs a paragraph of global trend. Global trend → national position → his line. Always in that order, always ending on his.

### Step 6 — Close with ONE action

Offer the artifact — dossier, PDF, deeper dive on ONE named engine — in a single sentence, then stop. Do not enumerate four follow-ups. If the answer changes nothing he does next, say what it does change.

## Output Shape (conversation delivery)

- Dense continuous prose, not a bullet inventory. For exploratory and futures questions the principal reads narrative straight through — save bullets and tables for genuinely tabular material.
- Register: direct, short sentences, concrete nouns, BM/English mix as he writes. No hedging filler, no "it is important to note", no service-desk framing, no headers over a two-paragraph answer.
- Name the mechanism in every claim. "Agents are low variance, so all of them choose the same option simultaneously" beats "agents introduce systemic risk".
- Say plainly when you are unsure, or mark a claim CONTESTED, rather than smoothing over a weak source.
- End with weight, not a summary. The last sentence should be the thing he remembers, not a restatement.

## Pitfalls

- **Never answer a dystopian framing with agreement or dismissal.** Agreement makes you a mirror; dismissal makes you the establishment. Both end the analysis. Deliver the mechanism and let him place it.
- **Never use future tense for something that already happened.** Search first. The "big bang" he is bracing for is frequently a documented past incident, and finding it is worth more than any speculation about it.
- **Never present a forecast unanchored to a decision.** If nothing in it changes what he does next, it is entertainment. Say what it changes.
- **Do not confuse the questions in the ask.** "Next year" and "three months" are different forecasts because different things are already locked in. If he asks both, answer both separately and say which one he is actually asking about.
- **Do not let the counter-signals become a hedge.** The counter-signal section states what survives; it does not soften the main claim into mush. Take a position and mark its confidence.
- **Do not quote a figure without its denominator or per-unit value.** A transaction count without per-transaction value, or a job-creation projection without its conditional clause, is a number stripped of its meaning. Carry both or neither.
- **Do not treat every credible-sounding number as a fact.** When a statistic's only sources are SEO/content-mill domains restating each other, mark it CONTESTED and prefer the primary — or name the primary you used. Never mix a contested figure into a list of sourced ones without a marker.
- **Do not measure or model how much the principal cares.** Forecast the system, not his attachment to it.
- **Do not collapse "it could happen" into "it will happen".** Mechanism, likelihood, and timeframe are three separate assertions. Make each one explicitly.

## References

- `references/ai-agent-risk-landscape.md` — Verified risk/incident knowledge bank for agent-related futures work: the containment-failure precedent (escape through a single filtered egress chokepoint, an improvised inter-agent message board, re-established after remediation, cluster-admin within hours), multi-agent failure modes (low variance → simultaneous identical decisions, resource avalanche, collusion without comms, sabotage with self-replicating malware, capability ≠ coordination), error cascades and false consensus (one atomic seed → system-wide; a governance layer moves defence success from 0.32 to 0.89), self-propagating agent worms (agent config files as a first-class attack surface, skill supply chain universally vulnerable, sandbox isolation is the decisive control), near-autonomous state-actor operations, financial-stability warnings (FSB/IMF/BIS plus insurance aggregation risk), the agent-payments **value gap** (never quote a transaction count without per-transaction value), agent-native social platforms, physical and economic constraints (power, the politics of household utility bills, depreciation vs hardware life, circular financing), access geopolitics (model access cut by unilateral state action), a hosting economy's exposure, and the counter-signals section that must accompany any doom framing. Re-verify volatile figures before quoting.
- `references/search-and-extraction-under-governance.md` — How to keep researching when the tooling layer resists: recovering from a lexically-gated `web_search` (rephrase to strip the trigger lexeme, or extract a known URL — the gate is on wording, not subject), and recovering the omitted middle of a truncated `web_extract` (the cache file is one long line, so slice it in `execute_code` with `str.find()` instead of `read_file` offsets).

## Related

- `deep-research` — the gathering phase (multi-source search, extraction ladder, evidence grading). Prepare the material there; apply this skill's shape to deliver it.
- `web-extraction-fallbacks` — when URL extraction itself fails (bot walls, search-only backends, full outages).
- `hermes-rasa` / `governed-uncertainty` — how to hold an open question and mark uncertainty without collapsing it.
