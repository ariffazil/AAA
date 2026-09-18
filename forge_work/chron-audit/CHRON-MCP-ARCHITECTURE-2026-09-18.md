# CHRON MCP Architecture — Query API to the Temporal Organ

> **Status:** DESIGN — scaffold for next agent session
> **Date:** 2026-09-18
> **Authority:** F13 sovereign analysis
> **Pattern:** CHRON = organ. CHRON MCP = interface. Same as GEOX/GEOX MCP.

---

## 0. Design Principles

1. **CHRON MCP is a query API, not the organ itself.** The organ runs continuously as a materialized consumer over NATS. The MCP exposes what the organ knows.

2. **Read-heavy, write-light.** Most calls are queries. Writes are limited to predictions (which carry verify_at) and observations (which are evidence, not interpretation).

3. **FRAME is independent.** FRAME can query CHRON, challenge CHRON, and say CHRON is wrong — without CHRON's permission.

4. **Bitemporal by default.** Every query supports `as_of` — what did we know at time T?

5. **No self-certification.** CHRON cannot seal its own predictions. arifOS seals. CHRON observes.

---

## 1. Tool Surface

### READ tools (OBSERVE class — no auth required)

| Tool | Purpose | Returns |
|------|---------|---------|
| `chron_query_changed` | What materially changed since T? | List of ChronEpisodes with change classification |
| `chron_query_believed` | What did we believe about X at time T? | Claim chain with supersession lineage |
| `chron_query_predictions` | Show open/verified/failed predictions | Prediction list with status, verify_at, outcome |
| `chron_query_calibration` | What is our prediction accuracy? | Brier score, error class distribution, calibration curve |
| `chron_query_episodes` | List episodes by filter | Episodes with observations, claims, outcomes |
| `chron_query_lessons` | What lessons have been extracted? | Lesson candidates and promoted lessons |
| `chron_query_attention` | What deserves attention now? | Ranked signals with urgency × consequence × actionability |
| `chron_query_lineage` | How did belief about X evolve? | Full supersession chain with timestamps |
| `chron_query_as_of` | Temporal reconstruction at date T | Snapshot of all beliefs, predictions, outcomes at T |
| `chron_query_scars` | What CHRON-specific scars exist? | Prediction failures that became constraints |

### WRITE tools (MUTATE class — requires auth)

| Tool | Purpose | Input | Gate |
|------|---------|-------|------|
| `chron_predict` | Create prediction with verify_at | claim, confidence, horizon, verify_at, assumptions, evidence | Must carry verify_at. No floating predictions. |
| `chron_observe` | Record observation from organ | source, content, truth_class, observed_at | Truth class mandatory (OBS/DER/INT/SPEC) |
| `chron_episode` | Create ChronEpisode | function, question, principal, observations, claims | Append-only. Never rewrite. |
| `chron_verify` | Record verification outcome | prediction_id, expected, observed, error_class | Only after verify_at has passed |
| `chron_learn` | Extract lesson from verified error | prediction_id, lesson_text, evidence | Requires verified incorrect prediction |
| `chron_supersede` | Mark belief as superseded | old_claim_id, new_claim_id, reason | Append-only correction |

### WITNESS tools (for FRAME)

| Tool | Purpose | Returns |
|------|---------|---------|
| `chron_witness_challenge` | FRAME challenges a CHRON claim | Challenge receipt with evidence |
| `chron_witness_verify` | FRAME independently verifies | Verification verdict with evidence |
| `chron_witness_observe` | FRAME observes CHRON's outputs | Observation receipt |

---

## 2. FRAME Integration

FRAME is not inside CHRON. FRAME is the independent witness that can challenge CHRON.

```
REALITY
    │
    ▼
  FRAME ──────────────┐
    │                  │
    ▼                  │ witnesses
  NATS                 │ challenges
    │                  │ verifies
    ▼                  │
  arifFlow             │
    │                  │
    ▼                  │
  CHRON ◄──────────────┘
    │
    ▼
Agentic Memory
```

### FRAME's role with CHRON:

| Action | How |
|--------|-----|
| **Witness** | FRAME observes CHRON's episodes, predictions, verifications |
| **Challenge** | FRAME can call `chron_witness_challenge` with counter-evidence |
| **Verify** | FRAME independently checks CHRON's claims against reality |
| **Drift** | FRAME detects when CHRON's calibration degrades |

### FRAME's tools for CHRON:

```yaml
frame_chron_witness:
  input:
    - chron_episode_id or chron_prediction_id
    - frame_evidence (from FRAME's own probes)
    - frame_verdict (CONFIRMED | CONTRADICTED | UNVERIFIABLE)
  output:
    - witness_receipt (attaches to the episode/prediction)
    - If CONTRADICTED: triggers CHRON review
```

### The key rule:

```
FRAME can say "CHRON is wrong" without asking CHRON.
No control may certify itself.
```

---

## 3. CHRON MCP Data Flow

```
                    NATS
                      │
                      ▼
              CHRON Observer
          (materialized consumer)
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
  Episode Store  Prediction Store  Calibration Store
  (bitemporal)   (with verify_at)  (Brier scores)
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
                 CHRON MCP
              (query interface)
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
  AAA             Agentic Memory      FRAME
  (decision)      (adaptation)        (witness)
```

---

## 4. CHRON MCP Schema (per tool)

### chron_query_changed

```yaml
input:
  since: datetime          # ISO-8601, required
  until: datetime          # optional, defaults to now
  domain: string[]         # optional filter: WORLD, REALITY, CLOCK, etc.
  audience: string         # optional: arif, syed, both
  min_consequence: string  # optional: HIGH, MEDIUM, LOW

output:
  episodes: ChronEpisode[]
  change_count: int
  material_changes: string[]  # human-readable summary
```

### chron_predict

```yaml
input:
  claim: string            # what we expect (required)
  confidence: float        # 0-1 (required)
  horizon: string          # "3d", "1w", "1m" (required)
  verify_at: datetime      # when to check (REQUIRED — no floating predictions)
  assumptions: string[]    # what must hold (required)
  evidence: string[]       # evidence refs (optional)
  principal: string        # arif, syed, federation
  domain: string           # which organ/domain this relates to

output:
  prediction_id: string
  verify_at: datetime
  status: PENDING
  receipt: string
```

### chron_verify

```yaml
input:
  prediction_id: string    # which prediction to verify (required)
  expected: string         # what we predicted (required)
  observed: string         # what actually happened (required)
  error_class: string      # DATA_ERROR, ASSUMPTION_ERROR, MODEL_ERROR, REGIME_CHANGE, UNKNOWN, CORRECT
  evidence: string[]       # evidence refs (required)
  source: string           # where observed data came from (required)

output:
  verification_id: string
  prediction_id: string
  was_correct: boolean
  error_delta: string
  brier_score: float       # computed after verification
  calibration_updated: boolean
  receipt: string
```

### chron_query_as_of

```yaml
input:
  as_of: datetime          # the point in time to reconstruct (required)
  domain: string[]         # optional filter
  include_predictions: boolean  # default true
  include_retracted: boolean    # default false

output:
  snapshot_time: datetime
  active_claims: Claim[]
  active_predictions: Prediction[]
  known_outcomes: Outcome[]
  superseded_claims: Claim[]  # only if include_retracted
```

---

## 5. ChronStore (internal to CHRON organ)

Not exposed via MCP. CHRON owns this.

```
/root/.local/share/chron/
├── episodes/
│   ├── chron-ep-20260918-observe-a1b2c3d4.json
│   ├── chron-ep-20260918-predict-e5f6g7h8.json
│   └── ...
├── predictions/
│   ├── pred-20260918-budget2027-i9j0k1l2.json
│   └── ...
├── calibration/
│   ├── brier-scores.jsonl
│   └── error-classes.jsonl
├── lessons/
│   ├── lesson-candidates.jsonl
│   └── promoted-lessons.jsonl
└── scars/
    └── chron-scars.jsonl
```

---

## 6. NATS Subjects (CHRON subscribes/publishes)

### CHRON subscribes to:

```yaml
governance.>           # arifOS governance events
aforge.execute         # A-FORGE execution traces
aforge.experience      # A-FORGE experience traces
frame.observe          # FRAME observations
frame.drift            # FRAME drift signals
well.signal            # WELL vitality signals
wealth.signal          # WEALTH market signals
geox.signal            # GEOX earth signals
hermes.claim           # HERMES validated claims
```

### CHRON publishes to:

```yaml
chron.episode          # new ChronEpisode created
chron.prediction       # prediction made (with verify_at)
chron.verification     # prediction verified
chron.calibration      # calibration updated
chron.lesson           # lesson candidate extracted
chron.scar             # scar formed
chron.attention        # attention allocation decision
```

---

## 7. Authority Boundaries

| Action | Authority |
|--------|-----------|
| Create episode | CHRON (auto, from NATS events) |
| Create prediction | CHRON (requires verify_at) |
| Verify prediction | CHRON (after verify_at, from evidence) |
| Extract lesson | CHRON (requires verified incorrect prediction) |
| Seal prediction | arifOS only (CHRON cannot self-seal) |
| Challenge claim | FRAME (independent, no CHRON permission needed) |
| Promote lesson to policy | Agentic Memory (requires authority) |
| Change calibration weights | arifOS (constitutional change) |

---

## 8. Compression

> CHRON MCP is the query API to the temporal organ. Read-heavy, write-light. FRAME is independent — can challenge, verify, and say CHRON is wrong. Bitemporal by default. No self-certification.

---

DITEMPA BUKAN DIBERI ⚒️
