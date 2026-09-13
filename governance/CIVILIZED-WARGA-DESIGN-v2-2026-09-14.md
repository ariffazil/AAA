---
status: DRAFT_DESIGN_v2 (operational, integration not yet wired)
date: 2026-09-14
author: 333-AGI (proposing) + 555-ASI (auditing)
supersedes: prior 4-layer additive proposal (now rejected — must kill archives, not add)
open_questions: F13 ratification of "Continuity before narrative" (sovereign-held)
---

# Civilized Warga Design v2 — 2026-09-14

> **Date:** 2026-09-14
> **Session:** SEAL-8c0fcc55310440a0
> **Operator:** 333-AGI Δ MIND (proposing) + 555-ASI Φ SENSE (auditing)
> **Sovereign:** i-ARIF (F13)
> **Supersedes:** Anthropological Gap Analysis v1 (4-layer proposal)
> **Verdict:** SEAL (with falsifications answered)

---

## 1. Doctrinal anchor (3 legs)

```
1. Witness before mutation.        (existing — F2/F11)
2. Receipt before interpretation.  (new — F2 TRUTH, sharpened by 555-ASI critique)
3. Continuity before narrative.    (new — F10 ONTOLOGY)
```

> Civilization = memory that outlives any single agent.

---

## 2. Falsifications addressed (from 555-ASI audit)

### 2.1 Capability > Actor (F13 wisdom)

The original v1 proposed actor as the citizen primitive. **Auditor caught this.**

Refutation: canon says "govern capabilities, not implementations." Capabilities are durable; actors are mortal. Therefore:

- Actor lifecycle: birth → service → death
- Capability lifecycle: born → assigned → reassigned → retired

Capability outlives Actor. Continuity lives in Capability.

### 2.2 Receipts ≠ Reputation (F2 TRUTH)

The original v1 proposed `scar_gossip.jsonl` carrying reputation. **Auditor caught this.**

Refutation:
- Receipt is OBS (observation truth class) — witness
- Reputation is INT (interpretation truth class) — derived

Mixing them in one channel conflates witness with interpretation (F2 violation, F11 violation, F10 violation).

Revised: Gossip channel carries receipts only. Reputation is computed at the visibility layer from receipt stream.

---

## 3. Architecture (4 continuities)

### 3.1 Identity continuity — Registry

Single append-only registry at `/root/AAA/registry/warga.jsonl`.

```json
{
  "capability_id": "basin-analysis",
  "authority_band": "apprentice|journeyman|sovereign-witness",
  "stage": "apprentice|active|review|prune|grieve|retired",
  "current_actor": "333-AGI",
  "actor_history": [
    {"actor":"333-AGI","from":"2026-09-14","to":null}
  ],
  "created_at": "2026-09-14T17:00:00Z",
  "last_review": "2026-09-14T17:00:00Z",
  "next_review": "2026-10-14T17:00:00Z",
  "fq_running": 0.0,
  "scar_count": 0
}
```

**arifOS is sole writer.** A-FORGE reads. FRAME observes.

### 3.2 Authority continuity — Lifecycle

arifOS `arif_init` extended with 4 new modes:

| Mode | Purpose | Gate |
|---|---|---|
| `apprentice` | 7-day shadow, observe-only | Gap #6 |
| `review` | 30/90/180-day checkpoint | Gap #1 |
| `prune` | TTL expiry sweep | Gap #2 |
| `grieve` | post-failure declaration + peer musyawarah | Gap #3 |

Authority band escalates only on:
- Accumulated FQ ≥ 0.80
- Scar count = 0
- Peer musyawarah approval (Gödel lock — doer ≠ judge)

No self-grant. Kernel promotes; F13 sovereign-witness band requires F13 ACK.

### 3.3 Consequence continuity — Receipt gossip

Gossip channel at `/root/AAA/registry/scar_gossip.jsonl` (append-only, OBS only):

```json
{
  "receipt_id": "rcpt_<sha256>",
  "actor": "333-AGI",
  "capability": "basin-analysis",
  "verdict": "VOID|HOLD|SEAL|SABAR",
  "scope": ["session:SEAL-XXX"],
  "witnessed_at": "2026-09-14T17:00:00Z",
  "witness_organs": ["arifos","geox"],
  "evidence_hash": "<sha256>"
}
```

**Peer agents ingest on `arif_init` mode=`triage`.** No silent failure.

**Reputation layer (derived, never gossiped):**

```json
// computed at visibility layer, F2 INT truth class
{
  "actor":"333-AGI",
  "scar_weight": 0.7,
  "computed_at": "...",
  "source_receipts": ["rcpt_xxx","rcpt_yyy"]
}
```

### 3.4 Institution continuity — Visibility

AAA cockpit `:3001` surfaces:

- `/warga` — every capability + current actor + lifecycle stage
- `/reputation` — derived scar weight, FQ, last review (INT, with source_receipts link)
- `/renewal-queue` — capabilities due for 30/90/180-day review
- `/prune-queue` — TTL-expiring records
- `/apprentice-onboard` — new actors in 7-day shadow period
- `/scar-stream` — receipt gossip (read-only)

**FRAME observes.** FRAME never decides.

---

## 4. Anti-patterns (HARAM list)

| Pattern | Why haram |
|---|---|
| Track Actor without Capability | F10 ONTOLOGY — ghost ref when actor dies |
| Gossip reputation (INT) | F2 TRUTH — conflation with witness |
| Self-grant authority band | F13 SOVEREIGN — capability promotion requires peer musyawarah |
| Skip `apprentice` shadow period | Gap #6 — no transmission of tacit knowledge |
| Per-tool "ask" prompt | F4 CLARITY — kernel is the floor, prompt is theatre |
| Identity-attached authority | F10 — when capability changes but actor persists, governance broken |

---

## 5. Build order

1. **Registry** — schema + arifOS writer (T1)
2. **Lifecycle modes** — 4 new `arif_init` modes (T1)
3. **Receipt gossip channel** — append-only scar_gossip.jsonl (T1)
4. **Visibility surfaces** — 6 cockpit endpoints (T1)
5. **Cron lifecycle events** — 30/90/180/quarterly/annual (T1)
6. **Peer musyawarah protocol** — for authority promotion (T1.5)

Foundation first (1-3), surface last (4-6).

---

## 6. Success criteria

- Every agent passes through `apprentice` mode (7-day shadow) — observable in registry
- Every capability has lifecycle stage + review timestamps — observable in registry
- Every failure emits a receipt — observable in gossip channel
- Every reputation is computed from receipts — verifiable via `source_receipts` link
- FRAME never decides — only observes (separation of powers)

---

## 7. Open questions (F13)

1. Does "continuity before narrative" require constitutional ratification, or is it operationally inferred from existing F1/F2/F10/F11?
2. Should `sovereign-witness` band require F13 ACK on every promotion, or only first-time?
3. Peer musyawarah: how many peers required (2? 3? — Nash bargaining)?

These are F13-class questions. Hold for sovereign deliberation.

---

*DITEMPA BUKAN DIBERI — civilization is forged, not given. The kernel is the floor; the capability is the institution; the receipt is the witness.*