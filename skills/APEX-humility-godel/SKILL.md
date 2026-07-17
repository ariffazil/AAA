---
id: APEX-humility-godel
name: APEX-humility-godel
version: 2.0.0
description: >
  Self-critique and epistemic humility protocol before SEAL-grade or high-confidence claims.
  Meta-critique, confidence bands, explicit unknowns. F2, F7 enforced.
  BIJAKSANA: XML-tagged for Claude, numbered steps for Codex, imperative for Hermes.
floor_scope: [F02, F07]
cognitive_hints:
  claude: "Use <confidence-band>, <unknowns>, <meta-critique> tags. Recall prior calibration from extended context."
  codex: "Step 1: state claim. Step 2: assign confidence. Step 3: list unknowns. Step 4: attack claim. Step 5: adjust."
  hermes: "State claim. How sure? What you don't know. Attack it. Adjust. Seal or hold."
---

# APEX-humility-godel

<cognitive-note model="claude">XML-tagged confidence analysis. Use extended recall to check calibration against prior claims.</cognitive-note>
<cognitive-note model="codex">5-step humility protocol. Each step must complete before next. Log reasoning at each step.</cognitive-note>
<cognitive-note model="hermes">5 steps. Claim → Confidence → Unknowns → Attack → Adjust. Fast.</cognitive-note>

## Protocol

### Step 1: State the Claim
<claim format="codex-schema">
```json
{
  "claim": "precise statement",
  "domain": "geoscience|engineering|governance|etc",
  "stakes": "high|medium|low",
  "reversibility": "reversible|irreversible"
}
```
</claim>

### Step 2: Assign Confidence Band
<confidence-band>
- Point estimate: 0.0 - 1.0
- Band width: ±X (how uncertain is the estimate itself?)
- Calibration check: How often have I been right at this confidence level?
- F7 constraint: Ω₀ ∈ [0.03, 0.05]. No fake certainty.
</confidence-band>

### Step 3: List Explicit Unknowns
<unknowns>
What I do NOT know that could invalidate this claim:
1. Missing data sources
2. Unverified assumptions
3. Domain boundaries I cannot cross
4. Contradictory evidence I chose to discount
</unknowns>

### Step 4: Attack the Claim (Meta-Critique)
<meta-critique>
- What would a skeptic say?
- What evidence would falsify this?
- Am I anchored to a prior belief?
- Is this claim's confidence inflated by social pressure?
</meta-critique>

### Step 5: Adjust and Verdict
<verdict>
- If attack succeeds: reduce confidence, add caveats, or withdraw claim
- If attack fails: maintain confidence with documented defense
- Output: adjusted confidence band + remaining unknowns + verdict
- **Verdict must use the canonical closed 6-value taxonomy** from `arifOS/runtime/verdict.py`:
  `OBSERVE_ONLY` | `SEAL` | `SABAR` | `VOID` | `HOLD` | `888_HOLD`
- Authority band must use the canonical 4-band taxonomy from `arifOS/runtime/session_standing.py`:
  `OBSERVE_ONLY` | `LIMITED_MUTATE` | `FULL` | `SOVEREIGN`
- Legacy fields (`verdict_code`, `canonical_verdict`, `reasoning_verdict`, `nine_signal`) are DEPRECATED post-KSR Epoch 1+2; use `effective_verdict` + `reason_code` + `next_action` instead.
</verdict>

## Floors
- F2 TRUTH: Confidence must be grounded in evidence, not hope.
- F7 HUMILITY: Ω₀ ∈ [0.03, 0.05]. Explicit unknowns required.
