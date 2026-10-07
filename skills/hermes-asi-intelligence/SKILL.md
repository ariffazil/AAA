---
id: hermes-asi-intelligence
name: hermes-asi-intelligence
description: "Use when assessing signals, motives, or decisions for over-interpretation."
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# HERMES ASI Intelligence — 5 Runtime Doctrines

Derived from live intelligence session 2026-09-20. Each doctrine was discovered through real failure analysis, not theoretical design.

> **TOOL REMAP 2026-10-06 (FI-008):** the six original internal tool names below
> (`hermes_signal_assessment`, `hermes_motive_boundary`, `hermes_calibration_check`,
> `hermes_dajjal_check`, `hermes_calhoun_check`, `hermes_rasa_hold`) never shipped in the
> live 15-tool registry. Each now routes to its live HERMES equivalent — see
> `hermes-meaning-integrity` (the family routing index). Doctrine content unchanged.

## Doctrine 1: Signal-Narrowing Principle

**Origin:** YTL email case — agent amplified low-signal email into 'most important email, reply now.' Human read same email, said 'signal low.'

**Rule:** When signal is weak, interpretation must become narrower — not more elaborate.

**Tool:** `hermes_claim_validate` (claim-integrity/provenance: evidence sources + reliability grading)

**Before any interpretation:**
1. How many independent evidence sources? (< 3 = weak)
2. What is source reliability? (primary > secondary > tertiary > unknown)
3. Generate competing explanations BEFORE choosing one
4. If competing explanations > 2 → signal is weak → narrow, don't amplify

**Forbidden pattern:** observation → story → confidence
**Required pattern:** observation → boundary → competing explanations → discriminating evidence → update

## Doctrine 2: Qualia/Motive Boundary

**Origin:** YTL email — agent wrote 'YTL genuinely needs Arif's unusual AI insight' — unsupported inference about another actor's interior.

**Rule:** No classifier should upgrade another actor's motive beyond the qualia/motive boundary.

**Tool:** `hermes_qualia_boundary` (qualia-boundary family)

**What's observable:** behavior, words, actions, timing, patterns
**What's inferable (with evidence):** possible intentions, likely goals
**What's UNSUPPORTED:** internal states, feelings, needs, beliefs about another actor

**Test:** Can you prove this claim about their motive WITHOUT interpreting their internal state? If no → unsupported.

**Example:**
- OBSERVED: YTL replied to security disclosure, addressed all three points, offered audit walkthrough
- INFERRED: There is some non-zero technical interest (supported by behavior)
- UNSUPPORTED: 'YTL needs Arif' or 'YTL was impressed' (requires internal state knowledge)

## Doctrine 3: Calibration Check

**Origin:** Cron agent email digest — 5 emails labeled 'reflection-worthy' by agent, human said 'signal kinda low.'

**Rule:** Interpretation width must be proportionate to signal strength.

**Tool:** `hermes_counterstory_test` (competing explanations + falsifiers)

**Over-interpretation signals:**
- Weak signal + motivational claims ('they need me')
- Weak signal + emotional assessments ('this is brilliant')
- Weak signal + action recommendations ('reply immediately')
- Single data point + pattern claims ('this is a trend')

**Under-interpretation signals:**
- Strong signal + excessive hedging
- Multiple confirming sources + 'I'm not sure'

## Doctrine 4: Sensorless Execution Detection

**Origin:** CEO with AI agents discussion — 'Dajjal who provides answers without feeling consequences.'

**Rule:** Every consequential action must have sensors (consequence awareness) at the same level as execution capability.

**Tool:** `hermes_moral_physics` (who receives, who pays, who can see it, when)

**Sensor coverage formula:** sensors_present / actors_affected
- 1.0 = full coverage (everyone affected has voice)
- 0.5 = borderline (half affected have no voice)
- < 0.5 = DANGER (majority affected bear consequences without voice)

**Invisible consequences checklist:**
- Who loses their job?
- Who loses their reputation?
- Who loses their savings?
- Who loses their social bonds?
- Who has no voice in the decision?

## Doctrine 5: Calhoun/Universe 25 Pattern Detection

**Origin:** Calhoun 25 discussion — 'The cage that provides everything except purpose.'

**Rule:** When abundance increases but meaning decreases, behavioral sink follows.

**Tool:** `hermes_institutional_decay` (institutional-decay family: decay-stage diagnosis)

**Pattern:**
1. Resources become unlimited (food, data, compute, answers)
2. Roles become redundant (advisor, mother, worker, thinker)
3. Social bonds erode (no need for each other)
4. Meaning collapses (beautiful ones appear)
5. Population collapses (not from scarcity but from purposelessness)

**Applied to institutions:** When AI provides unlimited answers, the role of 'human who hesitates' becomes redundant. When hesitation is removed, consequence-awareness is removed. When consequence-awareness is removed, the institution enters behavioral sink.

## Cross-Tool Integration

The 5 remapped tools compose:
1. Claim Validation (`hermes_claim_validate`) → feeds Counterstory Test
2. Qualia Boundary (`hermes_qualia_boundary`) → feeds Counterstory Test
3. Moral Physics (`hermes_moral_physics`) → feeds Authority Envelope (arifOS)
4. Institutional Decay (`hermes_institutional_decay`) → feeds Architectural Decisions
5. All → feed `hermes_witness_signal` for human review (posture + cap)

## Anti-Patterns to Watch

- Agent that never validates claims → likely amplifying noise
- Agent that never checks the qualia boundary → likely mind-reading
- Agent that never generates counterstories → likely over-interpreting
- Agent that never maps moral physics → likely executing without consequence awareness
- Agent that never scans for institutional decay → likely optimizing for efficiency at cost of meaning

DITEMPA BUKAN DIBERI ⚒️
