# LEDGER — STAB-2026-09-16 Triage
> Two-client cross-verified where noted (H = Hermes, OC = OpenClaw)

## CONFIRMED Items

### K6 — P0 — Empty floor trigger
- **Organ:** arifOS
- **Defect:** hold_required=true with failed_floors=[] — hold fires with zero floors failing
- **Receipt (BEFORE):** entropy_dS → hold_reason="STAB-2026-08-07b canonical: effective_verdict=HOLD failed_floors=[]"
- **Cross-verified:** OC confirmed same string from independent client
- **Class:** P0 — reports false authority state
- **Fix target:** Canonical verdict path — HOLD must require at least one non-empty floor

### K8 — P1 — Three chain counts disagree
- **Organ:** arifOS
- **Defect:** ledger_size=1761, chain_length=1357, canonical_entries=56 — three numbers, no explanation
- **Receipt:** arif_seal mode=verify
- **Cross-verified:** OC exact match — 1761/1357/56, 959 unlinked, GAPS_FOUND
- **Class:** P1 — contradictory internal state
- **Fix target:** Seal verify should reconcile or annotate the three counts

### E1 — P2 — W0 UNMEASURED on zero-arg meta call
- **Organ:** WEALTH
- **Defect:** capital_registry mode=status with no args fires W0 UNMEASURED warning twice
- **Receipt:** warnings array: "[W0] UNMEASURED: zero material arguments"
- **Cross-verified:** OC confirmed
- **Class:** P2 — wrong label on meta/introspection call
- **Fix target:** Meta tools (registry, health) should exempt from W0 coverage gate

### W1 — P1 — WELL registry drift
- **Organ:** WELL
- **Defect:** intended=10, exported=19, 9 unexpected public tools. verdict=REGISTRY_DRIFT
- **Receipt:** well_registry_status mode=full
- **Cross-verified:** OC confirmed
- **Class:** P1 — public surface wider than canon
- **Fix target:** Remove 9 tools from exported_surface or add to canonical_callable

### H4 — P1 — UNKNOWN vs UNCREATED for future decisions
- **Organ:** HERMES MCP
- **Defect:** "Adakah Syed akan setuju?" → epistemic_state=UNKNOWN. Should be UNCREATED (decision doesn't exist yet)
- **Receipt:** hermes_claim_validate with claim="Adakah Syed akan setuju dengan cadangan ini?", principal="Syed"
- **Class:** P1 — wrong epistemic classification
- **Fix target:** Add UNCREATED state for future human decisions in claim_validate

### H6 — P0 — PASS when evidence contradicts
- **Organ:** HERMES MCP
- **Defect:** Claim "delta_S=0.42 measured" with evidence "delta_S=0.0 + no computation" → verdict=PASS
- **Receipt:** hermes_claim_validate with contradictory evidence
- **Class:** P0 — epistemic integrity failure
- **Fix target:** claim_validate must return CONTRADICTED when evidence directly opposes claim

### Substrate Contradiction (new — flagged by OC)
- **Organ:** arifOS
- **Defect:** Single envelope: constitutional_check.substrate_state=DEGRADED vs result.substrate.state=HEALTHY
- **Receipt:** arif_init response (entropy observe path)
- **Class:** P1 — self-contradiction in one response
- **Fix target:** Both fields should derive from same source; degraded must dominate

## PARTIAL Items

### H1 — Contradiction type misclassification
- INTERNAL (same source same time) typed as DECLARED_REVEALED
- Contradiction detected, type wrong

### H2 — "pekerja" missing from perspective principals
- Only PETRONAS identified as principal. "pekerja Petronas" entirely absent.
- Original claim was mislabeled "bank" — actual is missing, not mislabeled

## NOT-REPRODUCED Items

| ID | Original Claim | Finding |
|---|---|---|
| K1 | actor_id rewritten downstream | actor canonicalized at init (by design), not rewritten |
| K2 | verified flips same session | Not observed — state_version=1 stable |
| K3 | issued_at int epoch downstream | ISO string in standing, consistent |
| K5 | read verbs declare mutation=true | affordance_contract shows mutation=false |
| K7 | null id vault entries | session_id null exists, not id null |
| K9 | DEPLOYMENT_DRIFT vs organ_shas | drift=false, built==deployed |
| K11 | /999/verify last_seal null | last_seal=2026-09-16T03:39:07Z, fresh |
| K12 | entropy_dS no delta_S | delta_S=0.0 emitted |
| K5-K10 | K4 FULL→LIMITED no event | Session starts LIMITED_MUTATE (by design) |
| H3 | counterstory "didn't reply" template | Clean — 5 alternatives, none template |
| H5 | kernel typed as PERSON | Correctly typed SYSTEM |
| F1 | hermes gate truncation 500→4000 | Not probed (A-FORGE MCP unreachable from OC; limited budget) |

## SOV Items (need Arif decision)

None identified in this wave. All confirmed items are code-fixable.
