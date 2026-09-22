# SCAR-001 — liveness_without_witness
Class: observability · Severity: HIGH · Promoted 2026-09-22

**Pattern:** A provider reports liveness on one surface while the capability
surface the ranker's callers actually need is dead.
GET /models = 200 while POST /chat/completions = 402/429/401.

**First observed:** deepseek 2026-09-22 — health board LIVE, judge seat 402
Insufficient Balance; three seal attempts failed before chat canary exposed it.

**Immunity:** health rows require a witness (witness_type + evidence + receipt).
Liveness checks must ride the capability surface (chat_completion), not
metadata endpoints. Enforced by fed_health_set.py fail-closed + probe witness columns.

**Floors:** F2_TRUTH strict_grounding · F11_AUDIT chat_canary_required
