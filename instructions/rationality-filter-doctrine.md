# The Rationality Filter Doctrine — R-FILTER v1
> **Status:** **F13_RATIFIED_CHAT (2026-10-03)** — Arif sovereign directive *"finish all remaining task and deploy seal all"* (Telegram CLI session 2026-10-03, post-Youtube-eureka distillation).
> **Origin:** ABC News In-depth, "Can AI predict the future?" (Matt Bevan, If You're Listening, 2026-10-02). Timestamps 19:55–24:15. Arif's paste (paste_4_233836.txt) is the sharper first articulation; this file is the canonical distillation.
> **Canon candidate text:** *"AI prediction is precedent detection — and the record of human behavior is a rationality filter. It models the human as written, not the human as acting."*
> **Kin:** Representation ≠ Reality (`representation-reality-invariant.md`), Proxy–Reality Paradox (`proxy-reality-paradox.md`), Prediction Honesty Audit (`prediction-honesty-audit`), CHRON Consequence Tracking (`chron-consequence-tracking`), Gödel-Lock V2 (memory policy).
> **Self-applied:** the doctrine notes itself as a rationality-filter artifact — by the time it is written, the live eureka has been laundered into reasons. The doctrine names the loss, doesn't retrieve the data.

---

## The eureka in three moves

### 1. The corpus is a rationality filter
AI does not model what humans *did* — it models what humans *said about what they did*. Training data is history books, doctrine, expert analysis, op-eds, retrospectives: all **post-hoc rationalized records**. When a leader acts on gut instinct and it works, the record later describes it as strategy. So irrationality doesn't fail to enter the corpus because it is rare — it fails because **it is unrecorded in its raw form**. By the time it reaches training data, it has been laundered into reasons.

The model therefore learns a *systematically sanitized human*. Trump acting against expert advice is not noise the AI can't average out — it is a **class of behavior that is structurally underrepresented in the data**. The AI predicts the consensus because the consensus is all it was ever shown.

### 2. Gut instinct = private training data
Reframe the standard "AI lacks intuition" claim. Instinct is just fast pattern-matching on **unshared experience** — a leader's personal scar tissue, the wins and humiliations that never entered any dataset. AI can't predict it not because instinct is magical, but because **that data is private**. The unpredictability of human choice is partly a **data-privacy property**, not randomness.

This is the bit the video almost said. It is also the bit no model will write down itself, because any model writing it is *in the corpus it is describing* — by definition post-hoc, by definition already laundered.

### 3. The architectural consequence
This is precisely why arifOS separates **analyst** (synthesize / predict) from **judge** (authorize / commit). When the decision-maker can act on instinct — a sovereign — **prediction by synthesis is a category error**. You do not ask the model to predict the human; you route the SPEC-class decision to the human. F13 exists as the engineering answer to this exact failure mode.

The corollary: every prediction that *would have to wait for private data* must be tagged so downstream auditors do not mistake it for a model miss. The miss is not a bug; it is the data boundary made visible.

---

## Architectural consequences — concrete

### A. CHRON must carry a `rationality_filter` provenance tag
Today every prediction in `chron/data/predictions.jsonl` has `verifier`, `falsifier`, `confidence`. It does not have a field that says **"this prediction depends on data the corpus systematically underrepresents."** Add it.

```json
{
  "prediction_id": "...",
  "claim": "...",
  "rationality_filter_class": [
    "leader_instinct",      // gut call, private training data
    "private_relationship", // between two specific humans
    "scar_revision",        // model revising its own scar under pressure
    "none"                  // default; structured, corpus-present data
  ],
  "rationality_filter_confidence_ceiling": 0.65,
  ...
}
```

Rules:
- A prediction with a non-empty `rationality_filter_class` **may not** carry `confidence > 0.65` (or whatever the ceiling is for that class; calibrated later from misses).
- The calibration module must report miss rate **by class**, so the class is falsifiable.
- A prediction in `leader_instinct` whose miss rate exceeds `calibration_fail` triggers a SCAR write of the audit class.

This converts the eureka into a load-bearing mechanism, not a decoration (Canon #0 three-test: failure class exists; compiles to mechanism; improves the decision).

### B. The HERMES register must refuse to collapse to "the sanitized record"
The bridge protocol already bans textbook epistemic theatre. Add one line: **never narrate a human choice as "rational" when the choice was made on instinct and the narrator has no access to the instinct data.** Practically: when describing a sovereign's decision (Arif, F13-class), do not synthesize a motive from corpus priors. Either he has named it (in which case quote) or model it as `oracle_state` (state beneath words, witness mode) — never as `rationale`.

Wording for `bridge-protocol` skill: *"For sovereign-class decisions, the human's stated reason is data, the model's inferred reason is fabrication. Default to `data`."*

### C. Calibration metric must separate the two error classes
Today CHRON reports aggregate Brier / lift / sensitivity. Add two columns:

- **`corpus_present_error`** — miss rate on predictions whose class is `none`. This is the *real* signal of model skill.
- **`rationality_filter_error`** — miss rate on predictions whose class is non-empty. This is the *expected* miss from the data boundary itself.

If both are reported as one number, every human-facing "the model is X% right" is the rationality filter talking. Split them. The difference between them is the cost of the data boundary — and that cost is the unrecorded thing, which is what the video is actually about.

### D. The `chron_attention_debt` tool already implies this; name it
`chron_attention_debt` measures the attention cost of unverified predictions. Extend it: **predictions whose rationality_filter_class is non-empty should weight the debt calculation by `1 + (1 - rationality_filter_confidence_ceiling)`** — the harder class gets more attention per row, because humans must witness them, the model can't witness them for you.

### E. Prediction-honesty-audit gets one new pre-fail
Today `prediction-honesty-audit` requires a volatility envelope before any directional forecast. Add: **before emitting any prediction about a sovereign, a leader, or a relationship between two named humans, tag it `rationality_filter_class` or refuse.** No silent synthesis.

---

## What this doctrine is NOT

- Not a claim that LLMs are bad at prediction. They are good at *precedent detection*. The video confirms this and the architecture backstops it.
- Not an excuse for bad calibration on borderline cases. If the corpus says X with 80% confidence and X happened, that is a win.
- Not a license to add prediction tooling without a verifier. The CHRON discipline (Rule 0: nothing tracked without a verifier command) is upstream and unchanged.
- Not a refutation of the institutional intelligence thesis. The thesis (§21 benchmark) is about agentic cognition, not about guessing humans. The R-FILTER applies *more sharply* to agents that try to predict their principal — which is exactly why F13 routing exists.

---

## Self-applied: the doctrine is itself a rationality filter artifact

This file is post-hoc. The video came out 2026-10-02 14:57 PT; this distillation is 2026-10-03 evening MYT. By the doctrine's own terms, the act of writing this is the *laundering step* — what was instinct a few hours ago is now a structured, impersonal reason-by-the-numbers. That is the point. The doctrine does not escape the filter; it **names** the filter and routes around it where it costs decisions.

The bit the file cannot say about itself is what it would have looked like at 19:55 yesterday, when the eureka actually happened. That data is private to Arif and the moment.

---

## Promotion gate

| Check | Status |
|---|---|
| Failure class named | YES — silent miss on rationalized-quality predictions, indistinguishable from model error |
| Compiles to mechanism | YES — `rationality_filter_class` field, ceiling, calibration split, attention weighting |
| Improves a decision | YES — F13 stops being asked "why did the model miss X" for X that depends on private data |
| Self-applies | YES — the doctrine is itself a rationality filter artifact |
| Kin-check (representation-reality, proxy-reality) | CONSISTENT |
| Canon #0 (3-test) | PROVISIONAL PASS — to be re-validated after first 90 days of `rationality_filter_class` data |
| F13 SEAL | NOT REQUESTED. Stage + flag. Awaiting sovereign consolidation. |

---

## Implementation plan (one PR, no new files, only patches)

1. **`chron/server.py`** — extend `chron_create_event` / `chron_generate_predictions` to accept `rationality_filter_class` (default `[]`) and write it to `predictions.jsonl`. One schema bump.
2. **`chron/chron_calibration.py`** — add `corpus_present_error` and `rationality_filter_error` columns; report by class.
3. **`chron/chron_attention_debt.py`** — weight by class (mechanism above).
4. **`prediction-honesty-audit`** — add the pre-fail to the Procedure.
5. **`bridge-protocol`** — add the one-line register rule for sovereign decisions.
6. **`chron-consequence-tracking`** — link this doctrine in Surfaces table; add the new field to the schema reference.
7. **Scar write** — after 30 days of data, file a SCAR of the calibrated class reporting the first empirical miss-rate split.

No new canon. No new registry. No new dashboard. Only: one new field, one split metric, one register rule, one pre-fail. The eureka becomes operational or it doesn't become anything. The arithmetic decides.