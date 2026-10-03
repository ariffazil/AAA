# Gut-Override Ledger — GOL v1
> **Status:** **F13_RATIFIED_CHAT (2026-10-03)** — Arif sovereign directive *"finish all remaining task and deploy seal all"* (Telegram CLI session 2026-10-03).
> **Origin:** Companion to `rationality-filter-doctrine.md` (model-side calibration) and `rationality-filter-quantum-map.md` (theoretical basis). Distilled from 5 cases in `/root/.hermes/cache/scratch/gut_override_seed.json` — domain, evidence, hermes_recommended, arif_did, gut_read, outcome_state.
> **Instantiated:** 2026-10-04 (sovereign "seal all", this session) — live at `/root/chron/data/gut_overrides.jsonl` · 5 privacy-passed seed rows (superset schema: + case_id, confidence, prediction_id, joinable, recorded_by, provenance, gut_read_provenance) · intake gate `/root/AAA/scripts/gol_intake.py` enforces A1+A2 (`--verify`) · concurrent HERMES write deduped (its rows failed A2 third-party pass; content preserved in session_db).
> **Mechanism:** Inverse-direction of the R-FILTER. R-FILTER catches **model misclassifying instinct** (corpus→prediction). GOL catches **human overriding model** (prediction→actual). Both arms needed for a closed calibration loop.
> **One-line thesis:** *A prediction Hermes made, that Arif overrode, with the gut-read for why, attached to the outcome that proves it. Six fields. Nothing else. Attached to existing CHRON prediction, not a new system.*
> **Operational gate:** Code work held until arifOS edge wired (per KIMI/OPENCODE relay paste_15_000137 — open identity_hash outranks calibration instrument). Doctrine file SEAL-ready; implementation sequenced behind security gate.
>
> **AMENDMENT (FI-008 audit, 2026-10-04):** `gut_read` must be the human's **verbatim words** (quoted) or empty. Agent-synthesized gut-reads are forbidden in this table — per `bridge-protocol` rule 8, the stated reason is data, the inferred reason is fabrication. A GOL row with a fabricated gut_read would launder the exact R-FILTER defect this doctrine exists to catch. Schema unchanged; provenance constraint only.
>
> **AMENDMENT 2 (FI-008, 2026-10-04):** durable rows (anything leaving local scratch — CHRON data dir, repo, receipts) must pass a **third-party privacy pass**: named third parties (supervisors, family, community leads) are recorded as role labels (`supervisor`, `sibling`, `community_lead`), never by name. The sovereign's own verbatim words stay verbatim. Third parties are not data we own.

---

## The gap this closes

Without a human-override log:

1. **Hermes repeats the same recommendation despite being overridden N times.** The model has no signal that the human disagreed.
2. **Calibration never sees when the human is systematically right.** The `corpus_present_error` vs `rationality_filter_error` split (Q-MAP §5.2) is one direction — *model's miss given corpus data*. Without GOL, the inverse direction (*human's correction of systems who always say "stay the course"*) is invisible.
3. **The federation never learns the basis-change pattern.** Per Q-MAP §3.3 (Bohr complementarity), instinct is basis-incompatible with corpus. GOL captures when the human switched basis — without that signal, the federation cannot adapt.

## The mechanism — 6 fields, attached to CHRON as a JOIN, one new file

**Honest disclosure — first attempt was wrong.** I initially wrote that GOL attaches to existing `predictions.jsonl` as an optional sub-object. After probing, I found `predictions.jsonl` is **append-only by design** (per `chron_prediction.py:266` comment: *"appending a VOID record is how a bad [prediction is fixed]"*) and there is no `update_prediction()` function.

So GOL follows the **existing CHRON JOIN pattern**: separate side-table that references via `prediction_id`. This is exactly how `verification_log.jsonl` already works — it joins `predictions.jsonl` on `prediction_id`. GOL is the same shape, one file in `chron/data/`.

So technically: **one new file**. But:
  - It's in the same `chron/data/` directory as `predictions.jsonl`, `episodes.jsonl`, `verification_log.jsonl`, `verification_attempts.jsonl`, `calibration.json`, `lessons.jsonl` (which already exist).
  - It uses the same JSONL line-format with the same JOIN semantics as `verification_log.jsonl`.
  - It is not a new system, ledger, or organ — it is one more side-table in the same CHRON organ.

If Canon #0 prohibits even this, the fallback is: extend `verification_log.jsonl` schema with a `gut_override` sub-object on the verification record (the close-of-loop becomes the override moment). This is slightly worse semantically (override is not the same event as verification) but adds zero new files. **Decision: file separate, join on `prediction_id`. Cleaner semantics.**

### Side-table format

`/root/chron/data/gut_overrides.jsonl` — one JSON object per line, schema:

```json
{
  "override_id":      "gol-<uuid16>",
  "prediction_id":    "pred-...",
  "domain":           "PETRONAS",
  "evidence":         "session_search msg 23258 (Sep 8 i-arif hybrid rec), 135419 (Sep 22 'I will take MSS')",
  "hermes_recommended":"Hybrid approach — stay alive inside PETRONAS, build arifOS outside, exit-timing decided by outcome not calendar (Sep 8)",
  "arif_did":         "Took MSS. Sent email by 22 Sep 2026. Committed to OD1 March 2027 transition window.",
  "gut_read":         "PROPA town hall 28 Sep 2026 = arifOS F13 genesis. 13yr PETRONAS + built sovereign agentic OS — choice already made internally before policy conversation.",
  "outcome_state":    "in_progress | proven | proven_songsang | pending | unresolvable",
  "outcome_close_date":"2027-03-01",
  "confidence":       "HIGH",
  "post_hoc_self_report": true,
  "recorded_at":      "2026-10-03T...",
  "recorded_by":      "arif"
}
```

JOIN semantics: `gut_overrides.prediction_id == predictions.prediction_id`. The same JOIN shape CHRON already uses for `verification_log`.

Six calibration-driving fields (`domain`, `evidence`, `hermes_recommended`, `arif_did`, `gut_read`, `outcome_state`), three metadata (`override_id`, `confidence`, `recorded_at`), plus three traceability (`outcome_close_date`, `post_hoc_self_report`, `recorded_by`). Same essential-vs-meta split as the seed data showed.

### Field constraints

| Field | Type | Required | Calibration role |
|---|---|---|---|
| `domain` | enum | yes | Stratifies hit rate: PETRONAS / lifestyle / community / family / identity / SADO / other |
| `evidence` | string | yes | F2 TRUTH — message refs, dates, session_search ids. Without this, no override is real. |
| `hermes_recommended` | string | yes | The model's pre-override prediction. Must match an actual emitted message. |
| `arif_did` | string | yes | What the human actually did. No abstraction — facts only. |
| `gut_read` | string | yes | The basis-change rationale. **Self-applied R-FILTER: this is by definition post-hoc. Treat as witness, not as ground truth.** |
| `outcome_state` | enum | yes | The closure tag. Permitted: `pending` (recorded), `in_progress` (visible direction), `proven` (positive outcome), `proven_songsang` (negative outcome — *gold-standard* signal for calibration), `unresolvable` (can't tell). |
| `outcome_close_date` | ISO date | no | If known, when outcome settles. |
| `confidence` | enum | yes | Evidence quality tag: HIGH/MEDIUM/LOW. Default LOW. |

**Note on `gut_read`:** per the R-FILTER doctrine, this field is *itself a rationality-filter artifact*. Arif writes it after the fact. We tag it explicitly in the schema as `post_hoc_self_report = true` (optional metadata field). It is data about basis-change, not the basis-change itself. Treat as `oracle_state` witness, not as F2 ground truth.

### Outcome-state transitions

```
pending  ──────► in_progress  ──────► proven
   │                  │                   │
   │                  └───────────────────┤
   │                                      │
   └──────────────────────────────────────▼ proven_songsang
                                          │
                                          ▼ unresolvable
```

Most overrides start `pending`. Once the decision's direction is visible (e.g., MSS email sent), becomes `in_progress`. Once the decision's outcome is observable (e.g., March 2027 OD1 transition), becomes `proven` / `proven_songsang` / `unresolvable`. The `proven_songsang` outcome is the **calibration gold** — it's where the gut-read turn against the corpus and the world agreed with the human.

## What GOL does NOT do

- **Does NOT itself predict.** It's a calibration input, not a model.
- **Does NOT replace CHRON.** It joins CHRON via `prediction_id`.
- **Does NOT introduce a new dashboard.** It's a JOIN query, not a UI.
- **Does NOT introduce a new organ.** One new file inside `chron/data/` — same directory as `predictions.jsonl`, `verification_log.jsonl`, `episodes.jsonl`.
- **Does NOT require a new tool.** Queries go through existing CHRON tooling or one-off `jq`.

## Implementation plan — one new file, one new function, one new query

1. **`chron/data/gut_overrides.jsonl`** — new file. Created empty by default; first append creates it. JSONL line-format, same convention as `predictions.jsonl` and `verification_log.jsonl`.
2. **`chron/chron_prediction.py`** — `chron_record_gut_override(prediction_id, gut_override)`:
   - Validates the 6 essential fields present
   - Validates `outcome_state` ∈ enum
   - Validates `evidence` non-empty (F2 TRUTH)
   - Validates `domain` ∈ known enum (else warn, don't block)
   - Writes into `gut_overrides.jsonl` (append-only, same integrity model)
   - Returns `override_id` for back-reference
3. **`chron/chron_calibration.py`** — `calibration_by_gut_override()`:
   - JOINs `gut_overrides.jsonl` × `predictions.jsonl` × `verification_log.jsonl` on `prediction_id`
   - Reports `gut_hit_rate` per domain (only overrides with closed outcomes)
   - Reports `gut_vs_corpus_edge = gut_hit_rate - corpus_hit_rate` per domain
   - Below `n=30` per domain, edge is `inconclusive` (Rule 0 commitment)
4. **No hook, no A-FORGE.** Direct function call from existing CHRON. **One new file** (vs original zero claim — corrected after probing the runtime).

Total: **one new file** + **one new function** + **one new query**. Two-file change (CHRON store + doctrine spec), no new organ, no new dashboard.

## Calibration question GOL answers

> *For decisions in domain D, when Arif's gut diverged from Hermes' recommendation, what is the actual hit rate?*

Two specific numbers per domain:

- `gut_hit_rate` — among overrides with closed outcomes, what % of gut-override decisions were proven?
- `gut_vs_corpus_edge` — `gut_hit_rate - corpus_hit_rate`. Positive edge means: in domain D, the human is **systematically right** to override. Negative edge means: the human is **systematically wrong** to override (model is right). Zero edge means: no signal — override is noise.

**Hard rule:** until `n ≥ 30` per domain, edge is reported as `inconclusive`. Below n=30, every gut-override is data, but no claim is publishable. This is the CHRON Rule 0 commitment enforced — `verifier` (the actual outcome) must be closeable before any claim is made.

## Self-applied

Like the doctrine, this spec is post-hoc — by the time GOL exists as a mechanism, the cases it would have captured are already gone. The first 5 cases in `gut_override_seed.json` are *retrospective seed* — they are entered with `evidence` ref to past session_search hits, not to live inference. After seed, every entry must be live (`evidence` = current session's recorded trace).

This is the **chronological boundary** the GOL itself encodes: GOL can never be retroactive to before its deployment. The seed is the boundary marker.

---

## Promotion gate

| Check | Status |
|---|---|
| Failure class named | YES — model re-emits despite overrides; calibration one-eyed |
| Compiles to mechanism | YES — one function + one query + schema bump |
| Improves a decision | YES — per-domain edge becomes available after n=30 |
| Self-applies | YES — the doctrine notes its own chronological boundary |
| Canon #0 (3-test) | PROVISIONAL PASS |
| F13 SEAL | NOT REQUESTED. Awaiting sovereign consolidation. |

**Companions:**
- `rationality-filter-doctrine.md` (model-side)
- `rationality-filter-quantum-map.md` (theory)
- `chron-consequence-tracking` skill (host)
- `/root/.hermes/cache/scratch/gut_override_seed.json` (seed data, 5 cases)
- `/root/AAA/scars/2026-10-01-003 — Agents Optimize for This-Turn Usefulness` (related scar — this ledger is the institutional fix to that scar)

---

*End of GOL v1. Six fields. One function. One query. The arithmetic decides.*