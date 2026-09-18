# CHRON TEMPORAL SUBSTRATE — CANONICAL ARCHITECTURE REFERENCE

> **Status:** DESIGN REFERENCE — NOT RATIFIED, NOT BUILT, NOT SEALED
> **Source:** external architectural analysis relayed by F13, 2026-09-18
> **Distilled by:** i-ARIF (auditor/validator role)
> **Home:** `/root/AAA/forge_work/chron-audit/` — the canonical governance tree is
> `chattr +i` immutable (correctly), so this reference lives in the CHRON work area.
> **Evidence discipline:** every checkable claim in the source re-derived from disk.
> Two refuted, two findings the source missed. See
> `DISTILLATE-EXTERNAL-TEMPORAL-SUBSTRATE-2026-09-18.json` alongside this file.
> **CHRON_STATE: EXPERIMENTAL** — 0 of 3 ALPHA-ZEN jobs have fired. This describes
> where CHRON should go AFTER the runtime chain is witnessed. Not a licence to build.

---

## 0. The distinction that matters

| Thing | Answers |
|---|---|
| **Reality Graph** | what the institution thinks exists, and how things relate |
| **World Memory** | what it chooses to retain about what happened |
| **World Model** | what it expects will happen next |
| **CHRON** | the temporal layer that reconciles all three |

CHRON is not another cron system, not another infographic generator, and not
"memory". It is the reconciliation layer.

**Closed loop:**
`Reality → Observation → Attention → Expectation → Decision → Action → Outcome → Memory → Calibration → Better Attention`

---

## 1. The maturity ladder

| Stage | Name | Meaning |
|---|---|---|
| 0 | SCHEDULED | tasks exist |
| 1 | WITNESSED | natural runtime causal chains proven |
| 2 | EPISODIC | canonical ChronEpisode exists |
| 3 | GRAPHED | episodes create reality relationships |
| 4 | TEMPORAL | as-of reasoning + supersession works |
| 5 | CALIBRATED | prediction → outcome verification |
| 6 | LEARNING | shadow agent improves ranking under supervision |
| 7 | INSTITUTIONAL | multiple agents share governed world memory |
| 8 | ADAPTIVE | system changes behaviour from measured experience |
| 9 | REFLEXIVE | system understands its own uncertainty and learning quality |

**CHRON sits at Stage 0 → 1.** Mature isolated components do NOT make the
institution mature.

---

## 2. Stage 0 — the arrow protocol (where we are now)

Do not build learning. Prove the runtime chain:

```
SCHEDULED → FIRED → PROCESS_STARTED → INPUTS_COLLECTED → G11_APPLIED
→ HERMES_GATE_APPLIED → ARTIFACT_CREATED → TARGET_RESOLVED → SEND_ATTEMPTED
→ TELEGRAM_ACCEPTED → RECEIPT_MATCHED
```

**Every arrow becomes an Observation. No arrow inherits truth from its neighbour.**

---

## 3. Stage 1 — ChronEpisode (the canonical object)

Every cycle produces one, WITHOUT changing delivery:

```
ChronEpisode {
  episode_id, cycle_id, principal, audience
  valid_time, observed_at, known_at, expires_at
  observations[], claims[], selected_signals[], rejected_signals[]
  predictions[], decisions[], actions[], outcomes[]
  privacy_scope, provenance[], receipts[]
  parent_episode_ids[]
}
```

**The Telegram output is DERIVED from this object — not the other way around.**
PNG, PDF, voice, text, silence are all just renderers.

---

## 4. Stage 2 — Human Reality Edge

```
OIL_PRICE_CHANGE --relevant_to--> ARIF
OIL_PRICE_CHANGE --observed_by--> CHRON
CHRON_SIGNAL --delivered_to--> ARIF
ARIF --self_reported--> DECISION
DECISION --resulted_in--> ACTION
ACTION --followed_by--> OUTCOME
```

**NEVER create `ARIF --feels--> anxious` unless Arif explicitly reported it.**
Instead: `STATEMENT --reported_by--> ARIF` / `STATEMENT --claims--> anxious`.
HERMES protects perspective sovereignty at the graph level.

---

## 5. Ontology (compact — do not graph everything)

**Reality nodes:** PERSON · AGENT · ORGANIZATION · SYSTEM · PLACE · ASSET · EVENT ·
OBSERVATION · CLAIM · SOURCE · DEADLINE · DECISION · ACTION · OUTCOME

**Cognitive nodes:** ATTENTION_EVENT · CHRON_EPISODE · MEMORY · HYPOTHESIS ·
PREDICTION · EUREKA · LESSON · SCAR · POLICY_CANDIDATE

**Edges:** OBSERVED_FROM · REPORTED_BY · SUPPORTED_BY · CONTRADICTS · SUPERSEDES ·
HAPPENED_AT · KNOWN_AT · EXPIRES_AT · RELEVANT_TO · SELECTED_FOR · REJECTED_FOR ·
DELIVERED_TO · ATTENDED_TO · PREDICTED · ACTED_ON · RESULTED_IN · COMPARED_WITH ·
REMEMBERED_AS · DISTILLED_INTO · SCARRED_AS

**Be extremely conservative with `CAUSED`.** Start chains as `PRECEDED`,
`ASSOCIATED_WITH`, `POSSIBLY_INFLUENCED` until causality is demonstrated.

---

## 6. The four clocks

| Clock | Meaning |
|---|---|
| **EVENT_TIME** | when reality happened |
| **OBSERVED_TIME** | when the sensor saw it |
| **KNOWLEDGE_TIME** | when the institution accepted it |
| **RELEVANCE_TIME** | when it mattered to this principal |

One event. Happened Monday, discovered Wednesday, relevant Friday. **Three
different realities.** Requires bitemporal storage (`valid_time`,
`transaction_time`) plus principal relevance intervals.

Unlocks: *"What did we know on Tuesday?"* — instead of answering with information
discovered Thursday.

---

## 7. World Memory — three layers, NOT one database

**A. Immutable event ledger** — append-only. Never rewrite yesterday. Corrections
use `SUPERSEDES` / `CORRECTS` / `RETRACTS`.

**B. Reality Graph** — a *projection* of the ledger, not the canonical store.
If corrupted, rebuild it.

**C. Semantic memory** — distilled things likely to matter again. Not *"today
Arif saw oil at X"* but maybe *"energy signals frequently affect Arif's work
attention"* — and even that preserves evidence and validity.

---

## 8. Memory metabolism

```
RAW OBSERVATION → EPISODE → LESSON_CANDIDATE → LESSON → POLICY_CANDIDATE → POLICY
FAILURE → ERROR → SCAR_CANDIDATE → SCAR → CONSTRAINT
```

**Most observations should die. Forgetting is essential.** Otherwise you build a
permanent graph of temporary noise.

---

## 9. Uncertainty lives inside memory

Never `06:00 docforge goes to DM`. Always:

```
claim · truth_state(VERIFIED|REPORTED|INFERRED|CONTESTED|RETRACTED)
confidence · observed_at · evidence_refs · valid_from · valid_to · supersedes
```

Agents then remember *what they believed, why, when, and what corrected them.*

---

## 10. Retrieval — hybrid, never embeddings alone

```
query + principal + time + truth state + graph neighbourhood
      + semantic similarity + provenance quality + freshness
```

Order: temporal filter → principal/privacy → truth-state → graph traversal →
semantic expansion → provenance ranking → contradiction check → return.

*"Why did we change the CHRON delivery architecture?"* must follow
`current config ← SUPERSEDES → older config ← CAUSED_BY → audit findings ←
SUPPORTED_BY → receipts`.

**Every retrieval supports AS OF:** now / yesterday / a date / what changed / what
was retracted.

---

## 11. Prediction is a first-class node

```
prediction_id, created_at, claim, confidence, horizon,
verification_at, assumptions[], evidence[], principal
```

At verification: `expected / observed / error`, classified `DATA_ERROR ·
ASSUMPTION_ERROR · MODEL_ERROR · REGIME_CHANGE · UNKNOWN`.

**Never delete failed predictions. Failed predictions are more valuable than
correct ones for learning.**

---

## 12. Attention becomes learnable

Not *"what is relevant?"* but *"which signals deserve interruption?"*

Score: truth · consequence · urgency · personal relevance · novelty · uncertainty ·
**attention_cost**. Output: `FULL | PULSE | SILENT`.

**SILENT is an intelligent action.**

---

## 13. Negative-space learning

Keep fingerprints of rejected candidates:
`candidate_id, domain, rank_band, rejection_reason, timestamp`

Then ask: *which rejected things became consequential?*
Yields `LOW_RANK_YESTERDAY → HIGH_REAL_WORLD_IMPACT_TODAY`.
Teaches **attention**, not preferences.

---

## 14. Three speeds — never mix

| Speed | Timescale | Scope |
|---|---|---|
| **FAST** | minutes / per cycle | staleness, dedupe, fallback |
| **SLOW** | days / weeks | source reliability, ranking priors, calibration |
| **RARE** | weeks / months | ontology, authority, privacy, governance |

**If mixed, the system oscillates. A weird Tuesday must not rewrite policy.**

---

## 15. Semantic immune system

Every control-like thing must prove `NAME · CALL_PATH · MEASURED_EFFECT ·
BYPASS_RESISTANCE · EVIDENCE`.

Maturity: `DECLARED → PARTIAL → ENFORCED → VERIFIED → CONTRADICTED`

```
RAW OBSERVATION > MEASURED FACT > DERIVED STATE > REASON CODE > NARRATIVE LABEL
```

**Fix this before learning loops are allowed to trust those labels.**

---

## 16. No self-certification

```
CHRON observes → agent proposes → independent auditor falsifies → arifOS grants
authority → A-FORGE implements → FRAME observes outcome → Reality corrects
```

**No actor evaluates, promotes and seals its own change.**

---

## 17. The four cores

**arifOS** = authority and truth-transition kernel. Not memory, not the world
model, not the renderer. Answers: who acts, what authority exists, what claim
state is this, what transition is allowed.

**HERMES** = semantic membrane. Protects `self-report ≠ inference`,
`statement ≠ belief`, `behaviour ≠ motive`, `representation ≠ referent`.

**FRAME** = independent witness. If arifOS says HEALTHY, FRAME asks *what was
measured?* If CHRON says DELIVERED, FRAME checks *message_id? destination?*

**A-FORGE** = experience-generating actuation:
`INTENT → EXPECTATION → EXECUTION → RESULT → DELTA → TRACE`

---

## 18. The proving query

> "Show me everything we believed about X at time T, why we believed it, what
> contradicted it, what we did because of it, what happened afterward, and what
> changed our belief."

**That single query proves institutional world memory exists.**

---

## 19. What NOT to build yet

No giant graph database · no automatic self-modification · no RL loop · no
policy-learning engine · no hundreds of ontology types · no autonomous memory
promotion.

**Twenty excellent Expectation→Outcome chains beat 20,000 context snippets.**

---

## 20. Marching order

1. Witness 14:00 and 21:15 naturally.
2. Build no new producer during freeze.
3. Produce causal arrow evidence per run.
4. Reconcile the representation > measurement kernel inversion.
5. Identify which desired functions existing lanes already satisfy.
6. Define ChronEpisode ONLY after observing real payloads.
7. Store first episodes append-only.
8. Add supersession/retraction semantics.
9. Build graph projection over episodes.
10. Only after enough outcome pairs: prediction calibration.
11. Only after calibration: shadow learning.
12. Only after independent validation: promotion.

---

## 21. Corrections to the source (audit trail)

**Refuted:**
- *"live init shows drift:false yet becomes DEPLOYMENT_DRIFT"* — NOT reproducible.
  `arif_init` returned `drift=false`, `reason_code=NEEDS_REVIEW`, `state=HEALTHY`.
- *"the DEPLOYMENT_DRIFT label overrode a false value"* — FALSE for the observed
  instance. The 09:12 receipt records drift verified independently (source
  `a027b74676ba` vs deployed `174c76c82eff`; `/health` `release.drift=True`).
  That label was correct. Acting on the claim would patch correct code.

**Still real, wider than the source said:** `tools.py` has FOUR drift triggers.
Two measured (lines 143, 150). Two not: line 140 accepts `substrate.state ==
"DEGRADED"` as proof; line 153 accepts the substring "drift" in a prose list.

**Confirmed:** the memory temporal surface already exists — `temporal_as_of`
(tools.py:24343), `include_contested` (:24341), `supersedes_memory_id` (:24322),
enforced in `tool_13_arif_memory.py:428`.

**Found, missed by the source:** A-FORGE `world-model-lite.jsonl` STOPPED WRITING
2026-08-27 (22 days). 792 records, 792 distinct ids, 5 distinct actions. The
source praised this layer and proposed feeding CHRON into it — **the consumer is
dead.** Same class as the 5-minute APEX-ZEN loop.
