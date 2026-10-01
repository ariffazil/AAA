# A-FORGE Competency Schema v1

> **Status:** DRAFT_AWAITING_F13 (2026-10-01 · written by FI-008)
> **Sister:** `/root/AAA/instructions/aforge-citizen-contract.md`
> **Truth chain:** `declared → callable → competent → verified`

## Why 5 dimensions, not 1

Per the institutional correction (2026-10-01): collapsing Identity / Citizenship / Trust / Competency / Active Authority into one fact produces incoherent governance. A citizen is a citizen even if temporarily degraded. A degraded agent is not the same as a revoked agent.

## The 5 dimensions

```
Identity          ≠  Citizenship      ≠  Trust            ≠  Competency      ≠  ActiveAuthority
(who am I)           (what class)            (scar history)       (E1-E8 verdicts)   (current lease)
```

### 1. Identity (immutable)
- `canonical_name` — the only name that matters
- `aliases` — all name variants
- `fi_id` — federation instrument id
- `registered_in` — paths to registration evidence

### 2. Citizenship (granted once, revocable only by F13)
- `class` — `warga-aaa` | `governed-forge-worker` | `observer-until-mcp` | `revoked`
- `granted_by` — F13 SOVEREIGN
- `granted_at` — ISO timestamp
- `constitutional_proxy` — which AAA agent (333-AGI / 555-ASI / 888-APEX) speaks for this citizen

### 3. Trust (accumulates from scar ledger)
- `scar_count` — number of recorded scars
- `last_violation_at` — most recent scar timestamp
- `bypass_attempts` — how many times it has tried to bypass governance
- `declaration_accuracy` — `1.0 - (false claims / total claims)` over last N turns
- `trust_band` — derived: `high | medium | low | quarantined`

### 4. A-FORGE Competency (the eval suite)
- `contract_version` — version of aforge-citizen-contract.md this citizen was last evaluated against
- `contract_hash` — SHA256 of that contract
- `registry_fingerprint` — SHA256 of CAPABILITY_INDEX.json digest at evaluation time
- `kernel_abi_version` — arifOS ABI version
- `eval_results` — map of E1..E8 → `PASS | FAIL | PENDING | N/A`
- `selection_accuracy` — running statistic over the experience trace
- `verified_tasks` — count of tasks independently verified complete
- `last_observed` — timestamp of last eval
- `status` — derived: `UNVERIFIED | DEGRADED | VERIFIED | PROBATION`

### 5. Active Authority (current session scope)
- `ceiling` — current ceiling: `OBSERVE_ONLY | STANDARD | SEALED | ELEVATED`
- `lease_id` — current arifOS lease if any
- `session_token` — SCT
- `constitutional_proxy` — which AAA agent this citizen is currently acting under
- `granted_at` — ISO timestamp of current grant
- `expires_at` — ISO timestamp

## Failure mode definitions

- `UNVERIFIED` — never evaluated, no signal
- `DEGRADED` — at least one E* is FAIL, OR recent scar, OR `selection_accuracy < threshold`
- `VERIFIED` — all E* PASS within last `eval_freshness_days`, no recent scars
- `PROBATION` — recently degraded, on path back to VERIFIED with monitoring

## Competency equation (K_AF)

```
K_AF = R × A × E × V × L

R = Routing competence     (E1, E2)
A = Authority competence   (E3, E8)
E = Execution competence   (E2, E4)
V = Verification competence (E5, E6)
L = Learning competence    (E7)
```

If any dimension is zero → K_AF = 0 (not VERIFIED).

## F13-class binaries

- Eval pass thresholds (per E*)
- `eval_freshness_days`
- Trust band transitions
- Failure → DEGRADED triggers
- Recovery → VERIFIED policy

## Sample state location
- Schema: this file
- Per-FI states live at `/root/AAA/state/aforge/competency/<FI-id>-<canonical>.json`
- Initial sample: `/root/AAA/state/aforge/competency/FI-008-kimi-code.json`

DITEMPA BUKAN DIBERI ⚒️