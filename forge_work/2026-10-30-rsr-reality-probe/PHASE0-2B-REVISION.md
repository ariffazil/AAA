# PHASE0-2B-REVISION.md — corrections to inspection plan (receipts-only)
2026-10-30. Per directive: reconcile matrix to exactly 12, config provenance,
independence claims narrowed, F6 windows preserved, N2/N4/N5 remain proposals.

## 1. Independence claim NARROWED (replaces "FAILED federation-wide")

OLD (wrong): "independent verification antara 333/555/888 FAILED pada tahap model."
REVISED: configured model pools OVERLAP (333∩888=4, 333∩555=3, 555∩888=3 shared
underlying identifiers). What this establishes: NO guarantee of model-disjoint
verification from config. What it does NOT establish: that any specific review
actually used a shared model (per-call assignment unaudited), that actor separation
exists or fails (unaudited), or that evidence-lineage separation exists (unaudited).

independence:
  configured_model_disjointness: failed_if_required   # requirement itself undecided
  per_call_model_separation: not_established          # needs x-litellm receipts per call
  actor_separation: not_established                   # same actor produced and checked this session
  evidence_lineage_separation: not_established
  independent_observation: not_performed
  human_authority_role: separately_declared           # 888 gate is authority, NOT an independent witness

## 2. Config provenance (MEASURED this session)

- config_ref: /root/A-FORGE/litellm-config.yaml
- config_sha256: 74c3e2f5eca84e75065bc0b7fb8c1f8227a2b3ae3bad090cf25788d3c2c15b71
- config_mtime: 2026-10-29 15:00:57 +0800
- RUNNING PROCESS USES THIS EXACT FILE: docker container litellm-federation
  (started 2026-10-29 15:01:24 +0800, 27s after config mtime) bind-mounts
  /root/A-FORGE/litellm-config.yaml -> /app/config.yaml, litellm on port 4013.
  process_uses_this_config: ESTABLISHED (bind-mount + start-time adjacency).
  Note: bind mount = live file; edits after container start WOULD be picked up on
  config reload — mtime predates container start, so observed content = what we hashed.
- FED :7074 (fed_router.py) and haproxy :4000 are SEPARATE processes; whether they
  read this same config: NOT established (not inspected).
- resolved_call_overlap: not_assessed (no inference permitted).

## 3. Matrix reconciled to exactly 12 (one primary status per pattern)

| P# | primary status | evidence | failing/untested subcriterion |
|---|---|---|---|
| P01 | SUPPORTED_BY_INSPECTION | zero-overlap stores §2 | parallel path unexercised |
| P02 | TESTED_WITHIN_FIXTURE_SCOPE | F5 schema validation | production nodes unexercised |
| P03 | SUPPORTED_BY_INSPECTION | TEMPORAL-CONTRACT mapping | adapter wiring pending |
| P04 | DESIGN_INTENT_ONLY | shapes defined in plan | never executed |
| P05 | DESIGN_INTENT_ONLY | join semantics written | not run |
| P06 | NOT_ASSESSED | tool advertised only | routing table unexamined |
| P07 | FAILED_AT_CONFIG_LEVEL (scoped: configured disjointness only) | chain overlap §2 of plan | per-call + actor + lineage unaudited |
| P08 | TESTED_WITHIN_FIXTURE_SCOPE | F6 single interruption point | see §4 windows |
| P09 | SUPPORTED_BY_INSPECTION | hard stops present | no live loop |
| P10 | TESTED_WITHIN_FIXTURE_SCOPE | F5/F6b | concurrent failure untested |
| P11 | NOT_ASSESSED | cost trivially low in Phase 0 | no cost model |
| P12 | NOT_ASSESSED | deferred by F9 | deliberate |

Sum = 12. Prior "4+4+2+1+3=14" was a miscount (P07 counted twice: partial+fail);
this table supersedes it.

## 4. F6 untested windows (explicit, preserved)

tested: interruption AFTER ledger append, BEFORE projection re-read.
untested: validation→write window; partial write; disk-full; concurrent writers;
replay after lost acknowledgement.

## 5. N2 scope note (per directive)

N2 grep finds implementation evidence only. Falsifiers demanding actual behaviour,
or absence-over-a-window, CANNOT be closed by grep — such predictions get
per-criterion verdict: needs-live-test or UNVERIFIABLE-by-inspection.

## 6. Join output contract (per directive, adopted verbatim shape)

{"branches": {"N2": {"status":"...", "evidence_refs":[]},
  "N4": {"status":"...", "reason": null},
  "N5": {"status":"...", "evidence_refs":[]}},
 "coverage": "partial|full",
 "authorizes_next_action": false}
"completed" = inspection operation finished, NOT proof of the underlying claim.

## 7. Policy decisions required from 888 (questions, not changes)

Q1. Does federation policy REQUIRE model-disjoint producer/verifier pools,
    or only per-task different-reviewer assignment (with per-call receipts)?
Q2. If per-task separation: accept dispatcher constraint + receipt as the
    enforcement point? (candidate change — NOT authorized by this document)
Q3. Are the 4 seal-chain historical link breaks (RECEIPT-CHAIN-RECON.md)
    within the bound EPOCH_ATTESTATION gap set? (digest join pending approval)
No routing changes proposed or made.
