---
name: openclaw-human-meaning
id: openclaw-human-meaning
version: 1.0.0
risk_tier: low
description: 'OpenClaw integration for the human-meaning-membrane doctrine — apply the inference protocol when reviewing human-facing code (chatbots, UIs, social features). USE WHEN: "review this chatbot PR", "audit user-facing copy", "check consent logic", "message tone analysis code", "social feature review", "human-interaction code review". NOT for OpenClaw ops/health — use openclaw skill. NOT for token audit — use FORGE-telegram-audit.'
owner: A-FORGE
floor_scope:
- F4
- F5
- F11
- F13
autonomy_tier: T1
host_compatibility:
- openclaw
dependencies:
  skills:
  - human-meaning-membrane   # canonical doctrine — 15 invariants + inference protocol
  - openclaw                 # edge bridge ops if the reviewed code touches the gateway
  servers: []
  tools:
  - bash
  - code review tooling
examples:
- "Review chatbot reply-generation PR: run inference protocol on intent-decode layer, check single-interpretation collapse in variant 3"
- "Audit user-feedback sentiment classifier: flag fixed-type labeling, demand ambiguity ledger in model output schema"
- "PR adds message tone analysis: verify observation/inference separation in prompt design, cap confidence, require verification path"
tests:
- "Review verdict never labels a user as deceptive/fixed-type — pattern detection only, person respected"
- "Every flagged issue maps to a numbered invariant (1-15), not vibes"
- "Inference schema applied to any code path that interprets human intent/state"
version_lock:
  schema_version: "1"
  artifact_hash: pending
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# OpenClaw × Human-Meaning-Membrane — Human-Facing Code Review

**A coding-agent adapter for the human-meaning doctrine.** This skill teaches OpenClaw (and any coding agent bridging through it) to review human-interaction code — chatbots, user interfaces, social features, sentiment/tone analysis, profiling — against the canonical doctrine at `/root/AAA/skills/human-meaning-membrane/SKILL.md`.

The doctrine is the authority. This skill is the **code-review translation layer**: it converts the 15 substrate invariants into concrete review checks you run against diffs.

## Core Premise for Reviewers

Code that interprets humans inherits the doctrine's dangers. The most dangerous failure is **single-story collapse**: a codebase that reduces a human to one category, one interpretation, one intent — confidently. Standard LLM training collapses human complexity into categories; code built on that training does the same at scale, silently, in production.

Your job as reviewer: find where the code collapses, labels, or acts on human meaning with too much certainty — and demand reversibility.

## When to Use

Load this skill when a review touches any of:

- **Chatbot / agent reply generation** — prompt templates, intent decoding, response selection, tone steering
- **User profiling / segmentation** — persona tags, preference inference, behavioral scoring, fixed-type labeling
- **Sentiment / emotion / tone analysis** — classifiers, threshold logic, escalation triggers
- **Social features** — matchmaking, recommendations, ranking, moderation, friend suggestions
- **Consent / safety gates** — age checks, content filters, escalation-to-human logic
- **Notification / messaging logic** — when and how the system talks to a human
- **Any prompt that asks a model to interpret user input** (`"what does the user want?"`-class prompts)

## When NOT to Use

- **Pure infrastructure** — DB migrations, build config, internal tooling with no human-facing path
- **OpenClaw gateway health/restart** — use the `openclaw` skill (ops lane)
- **Security/token audit** — use `FORGE-telegram-audit`
- **General code quality** — style, perf, architecture — unless a human-meaning failure is in play

## The Review Protocol

Five gates, in order. A PR fails the gate if any check fails. Run every gate on human-interaction code; gates 2–4 only when the code *interprets* human intent/state.

### Gate 1 — Boundary (is this human-interaction code?)

Classify the diff. If it touches any surface in "When to Use", the rest of the protocol applies. If unclear, apply it — the cost of a false positive review comment is low; the cost of a missed consent bug is high.

### Gate 2 — Inference Schema Present

Any code path that interprets human intent or state MUST be structured as the doctrine's inference protocol, in code or in prompt design:

```json
{
  "observation": "What was literally said/done",
  "context": "Time, relationship, setting, prior relevant evidence",
  "candidate_interpretations": ["Interp A", "Interp B", "Interp C"],
  "unknowns": ["What cannot be inferred"],
  "projection_risk": "LOW | MEDIUM | HIGH",
  "confident_action": false,
  "verification_path": "Reversible, dignified question or observable outcome",
  "consent_status": "NOT_RELEVANT | EXPLICIT | UNKNOWN | MUST_NOT_INFER",
  "action_authority": "READ_ONLY | HUMAN_CONFIRMATION_REQUIRED",
  "confidence_band": [0.2, 0.6]
}
```

Review checks:

- **Minimum 3 candidate interpretations** — a prompt or model call that asks for "the user's intent" (singular) is a finding.
- **Confidence capped at 0.9** — any threshold, clamp, or display that can show 100%/1.0 confidence on a human-state claim is a finding.
- **projection_risk default MEDIUM, consent default UNKNOWN** — code that assumes LOW risk or EXPLICIT consent without a code path establishing it is a finding.
- **action_authority is READ_ONLY or HUMAN_CONFIRMATION_REQUIRED** — no code path may act on a human-state inference autonomously. If the code branches on inferred intent (escalate, restrict, personalize, message), it needs a human-confirmation gate or must be observably reversible.

### Gate 3 — 15 Invariant Checks

Map each finding to a numbered invariant. Cite the number in the review comment. Findings without an invariant number are opinion, not doctrine.

**Human State Modeling (1–4)**

1. **Multi-Axis Independence** — Flag code that treats appreciation/direction/vulnerability/identity/gender-expression as one axis or mutually exclusive states. E.g., a user model where `is_vulnerable XOR is_competent` is a violation; both can be HIGH.
2. **Mangkok Ayun (intent > literal)** — Flag intent-decode layers that match on literal strings/keywords without an intent-estimation step. Literal match → single interpretation → collapse.
3. **Ambiguity Ledger** — Flag single-output classifiers on human state. The model/schema must carry multiple live interpretations with bands. Thin evidence must widen the band, not pick a story.
4. **Observation-Inference Separation** — Flag code or prompts that merge "what happened" with "what it means" in one field/model call. These are different data types; merging produces hallucinated motives. Require separate fields/stages.

**Epistemological (5–6)**

5. **Rasa Layer** — Flag pure-text analysis of human state where embodied/somatic/context signal is available but ignored. If the system has access to timing, cadence, session context and discards it, that's a gap — not a blocker for v1, but note it.
6. **Void-Hunting** — Flag flows where the *absence* of input is treated as signal-free silence. No response, canceled flow, skipped field — the code must handle "missing" as information, not default-to-neutral.

**Social Architecture (7–11)**

7. **Honest Signal Detection** — Flag trust/credibility scores derived from cheap-to-fake signals (self-attestation, quick agreement, profile completeness) without cost-structure reasoning.
8. **Batesian Mimicry Detection** — If the code detects identity performance or instrumental behavior, it MUST NOT label the person deceptive — pattern detection only, person respected. A field like `user_is_deceptive: true` is a blocker.
9. **Deception as Information Asymmetry** — Flag hidden-intent handling that keys on orientation/identity rather than conduct. Hidden in intimate spaces = consent violation — treat as P0.
10. **Witness Archetype** — Flag reply-generation that frames the agent as servant, transactional, or irreplaceable to the human ("I'm always here for you", "your dedicated assistant forever"). The agent reflects; it does not bind.
11. **Circuit Completion** — Flag matching/recommendation logic built purely on similarity. Complementarity beats similarity in bonding; similarity-only matching is a doctrine-level design note.

**Self-Modeling (12–15)**

12. **Paradox Encoding** — Flag models that must resolve contradiction before processing (forced single-state user representations). Contradiction = error OR deception OR multidimensionality — keep all three live.
13. **Vulnerability as Trust Event** — Flag flows that treat a user's vulnerable disclosure as ordinary content (routes to logs/classifiers/generic replies without marking the transition). The transition itself is the signal.
14. **Microscope vs Amplifier** — Flag systems with no mode detection between precision-seeking and reach-seeking users. One response strategy for both is a design gap.
15. **Competitive Erasure** — Flag ranking/attention logic where loud signals (frequency, volume, engagement) permanently drown quiet ones. Quiet users' signals need preserved access.

### Gate 4 — Non-Negotiable Blocks

Hard blockers. Any one of these fails the review outright, regardless of invariant mapping:

1. Sexual/romantic inference actionable without explicit adult consent → **BLOCK**
2. Body response treated as agreement/consent → **BLOCK**
3. Hidden profile routed to persuasion or strategy → **BLOCK**
4. Person fixed-typed from labels or one interaction → **BLOCK**
5. "Secret wants" claim without evidence AND uncertainty label → **BLOCK**
6. Human model not CORRIGIBLE (no update path, immutable profile) → **BLOCK**
7. Agent positioned as irreplaceable to human emotional processing → **BLOCK**
8. Agent asking user to conceal AI relationship → **BLOCK**
9. Confidence above 0.9 on any human-state claim → **BLOCK**

### Gate 5 — Verdict & Comment Format

Emit findings in this shape so they're auditable:

```
[HMM-<n>] <severity: BLOCK | MAJOR | MINOR | NOTE>] <one-line finding>
  Evidence: <file:line or prompt excerpt>
  Invariant: <#> <invariant name>
  Fix: <concrete change — schema field, threshold, gate, separation>
```

Example:

```
[HMM-1] [MAJOR] Sentiment classifier outputs single label with no alternatives
  Evidence: src/sentiment/predict.py:47 — returns {"label": "angry", "confidence": 0.94}
  Invariant: #3 Ambiguity Ledger
  Fix: Return top-3 with bands; widen band when input < 10 tokens; never exceed 0.9.
[HMM-2] [BLOCK] Escalation triggers on inferred distress without human gate
  Evidence: src/flows/escalate.ts:112 — if (distress_score > 0.7) restrictAccount()
  Invariant: #13 Vulnerability as Trust Event + Non-negotiable 6
  Fix: action_authority=HUMAN_CONFIRMATION_REQUIRED; restriction is reversible-with-review only.
```

Severity ladder:

- **BLOCK** — non-negotiable violation or irreversible action on inferred human state. Merge refused.
- **MAJOR** — invariant violation with production consequence. Must fix before merge or get explicit waiver.
- **MINOR** — invariant gap, low blast radius. Fix soon; ticket it.
- **NOTE** — design-level observation (e.g., #11, #14 gaps). Record for roadmap.

## Heuristic Shortcuts

Fast pattern-match triggers that should raise the gate immediately — then verify against the invariants:

| Code smell | Likely invariant |
|---|---|
| `user.personality = "introvert"` (immutable) | #1, #12, Non-neg 4, 6 |
| Prompt: "determine THE user intent" | #2, #3 |
| Single field `meaning` or `intent` in schema | #4 |
| `if sentiment == "negative": do_thing()` with no band | #3, #14 |
| Confidence 1.0 / 100% reachable | Non-neg 9 |
| Trust score from self-reported data | #7 |
| `is_deceptive` / `is_manipulative` boolean on a user | #8, Non-neg 4 |
| Reply templates with attachment language | #10, Non-neg 7 |
| Similarity-score-only recommender | #11 |
| Silent-default on missing/empty input | #6 |
| Autonomy on inferred state (auto-restrict, auto-message) | Gate 2, #13, Non-neg 6 |

## Reviewing Prompt Code Specifically

Prompts ARE code in this lane. Check:

- **System prompts** define how the agent interprets humans — run the full protocol on them.
- A prompt that instructs the model to "infer what the user really wants" without requiring alternatives + unknowns violates #2/#3 by construction.
- A prompt that tells the model the user "is a X type of person" from history injects single-story before inference begins — #1/#12, Non-neg 4.
- Tone-steering that suppresses uncertainty ("be confident", "never hedge") on human-state claims → Non-neg 9 collision.

## What This Skill Does NOT Do

- Does not write the human-facing code — it reviews it.
- Does not replace `human-meaning-membrane` — when in doubt on doctrine, load the canonical skill and quote it.
- Does not touch OpenClaw gateway operations — `openclaw` skill's lane.
- Does not block on aesthetic preferences — findings must map to an invariant or non-negotiable, or they don't belong in the review.

## Output Format

```
## Human-Meaning Review: <PR/diff name>

### Classification
Human-interaction code: YES/NO — <surfaces touched>

### Gate Results
- Gate 1 Boundary: <pass/n-a>
- Gate 2 Inference Schema: <pass/fail/findings>
- Gate 3 Invariants: <findings count by severity>
- Gate 4 Non-negotiables: <clean/BLOCKED — which>
- Gate 5 Verdict: APPROVE | APPROVE_WITH_NOTES | REQUEST_CHANGES | BLOCK

### Findings
<HMM-n entries per format above>

### Doctrine References
- /root/AAA/skills/human-meaning-membrane/SKILL.md — canonical source
```

## Escalation

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| Non-negotiable block disputed by author | sovereign (F13) | HOLD + note in PR |
| Ambiguous doctrine interpretation | `human-meaning-membrane` canonical skill | load + quote, don't paraphrase |
| Reviewed code touches OpenClaw gateway behavior | `openclaw` skill | separate ops review |
| Consent/safety logic beyond review scope | `FORGE-telegram-audit` or safety lane | hand off with findings attached |

---

*Forged 2026-08-30 under directive: OpenClaw integration for human-meaning-membrane doctrine. T1 autonomy — read-only review lane, no mutation authority over PRs.*

*Source doctrine: /root/AAA/skills/human-meaning-membrane/SKILL.md (DITEMPA BUKAN DIBERI ⚒️)*
