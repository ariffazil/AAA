# SCAR-003 — telemetry_confidence_exceeds_reality
Class: governance · Severity: HIGH · Promoted 2026-09-22

**Pattern:** Displayed telemetry (balance, confidence, health_score) contradicts
spend-gated reality, and the ranker trusts the display. High-confidence wrong
ranks are worse than low-confidence ones.

**First observed:** mulerouter balance_usd=49.925 confidence=0.99 while chat
returned 402 insufficient_balance (actual -0.7476 credits), 2026-09-22.
Sibling: mimo health UNREACHABLE rows from fake-000 key-pool bug (confidence
absent but status wrong).

**Immunity:** witness fields on health; chat canaries for spend-gated lanes;
balance display never outranks witnessed chat evidence in tie-breaks.

**Floors:** F1_AMANAH cost_hold · F2_TRUTH · F11_AUDIT
