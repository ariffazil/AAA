---
id: hermes-asi-intelligence
name: hermes-asi-intelligence
description: "Use when assessing signals, motives, or decisions for over-interpretation."
---

# HERMES ASI Intelligence — 5 Runtime Doctrines

Derived from live intelligence session 2026-09-20. Each doctrine was discovered through real failure analysis, not theoretical design.

## Doctrine 1: Signal-Narrowing Principle

**Origin:** YTL email case — agent amplified low-signal email into 'most important email, reply now.' Human read same email, said 'signal low.'

**Rule:** When signal is weak, interpretation must become narrower — not more elaborate.

**Tool:** hermes_signal_assessment

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

**Tool:** hermes_motive_boundary

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

**Tool:** hermes_calibration_check

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

**Tool:** hermes_dajjal_check

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

**Tool:** hermes_calhoun_check

**Pattern:**
1. Resources become unlimited (food, data, compute, answers)
2. Roles become redundant (advisor, mother, worker, thinker)
3. Social bonds erode (no need for each other)
4. Meaning collapses (beautiful ones appear)
5. Population collapses (not from scarcity but from purposelessness)

**Applied to institutions:** When AI provides unlimited answers, the role of 'human who hesitates' becomes redundant. When hesitation is removed, consequence-awareness is removed. When consequence-awareness is removed, the institution enters behavioral sink.

## Cross-Tool Integration

The 5 tools compose:
1. Signal Assessment → feeds Calibration Check
2. Motive Boundary → feeds Counterstory Test
3. Dajjal Check → feeds Authority Envelope
4. Calhoun Check → feeds Architectural Decisions
5. All → feed hermes_rasa_hold for human review

## Anti-Patterns to Watch

- Agent that never calls signal_assessment → likely amplifying noise
- Agent that never calls motive_boundary → likely mind-reading
- Agent that never calls calibration_check → likely over-interpreting
- Agent that never calls dajjal_check → likely executing without consequence awareness
- Agent that never calls calhoun_check → likely optimizing for efficiency at cost of meaning

DITEMPA BUKAN DIBERI ⚒️
