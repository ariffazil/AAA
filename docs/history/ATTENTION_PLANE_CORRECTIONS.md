# Attention Plane — correction history
> **Moved verbatim from README.md** during the AGENTIC-README-DOCTRINE v1 restructure
> (2026-10-16). This is audit history: valuable, but not landing-page prose. The public
> README now states the current definition directly. Source archive:
> `docs/archive/README-2026-10-16-pre-doctrine.md`.

## P2 correction — what arifFlow actually is (2026-09-21)

Earlier README called `arifFlow — Witness Plane`. **Correction:**

| Component | Role | NOT |
|---|---|---|
| FRAME | independent witness | not ledger, not telemetry |
| VAULT999 | immutable ledger | not witness, not telemetry |
| arifFlow | metabolism / FQ / receipts | not witness, not ledger |

`Witness ≠ Telemetry ≠ Ledger`. Three distinct roles.

## P2 correction — state reconciliation, not verification (2026-09-21)

Earlier README said AAA "verifies" federated state. **Correction:**

AAA establishes `ObservedState_A ?= ObservedState_B`. It does NOT establish `Claim = AbsoluteTruth`. The term for this discipline is **state reconciliation** (or **consistency verification**), not **verification**.

Every `organ.status = DOWN` carries:
- `observed_at`
- `source`
- `source_age`
- `confidence`
- `probe_method`
- `failure_reason`

because `organ.status = DOWN` doesn't necessarily mean `organ is dead` — it may mean probe timed out, auth failed, or network path failed. AAA preserves that distinction.

## F13 2026-09-25 — ActionRisk gate (replaces double-counted irreversibility floor)

`Reversibility` is no longer folded into EvidenceQuality — it was double-counted here and in the floor override. Reversibility now lives in the separate **ActionRisk** gate: a strongly-evidenced irreversible action still routes to Arif; evidence strength never manufactures reversibility. The `irreversibility_floor: P ≥ 0.85` override was replaced by `action_risk_gate` (see README hard-overrides table).
