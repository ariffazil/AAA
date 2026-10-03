# CLUSTER B-1 — AUDIT/OBSERVABILITY SHADOWS — sealed at 2026-10-03 10:44

**Cluster:** B-1 (8 carry_forward items: e-6207c0, e-b580d3, e-f742a3, e-743e6c, e-9d07da, e-0bc824, e-f76fd0, e-07fbd9)
**Probed by:** FI-005 (codex-cli) per carry_forward

## Live Findings

| Sub-claim | Claim status | Live evidence |
|---|---|---|
| **S1 ghost docker postgres on :5432** | ❌ FALSE ALARM | docker `postgres` is the canonical `af-forge` project DB. vault999 schema, arifos_admin user, 4 tables in public (trust_history, trust_scores, vault_seals) + 1 in observability (observations). All live. |
| **SCT decision-event audit trail broken (F11)** | ✅ **REAL F11 GAP** | `sct_decision_events/` under `/root/A-FORGE/forge_work/2026-07-17/` last write 2026-08-08 (dead 56 days). ACT events go to `act_decision_events/` (live, current). SCT writer code no longer exists in `/root/A-FORGE/src/`. New `sct_decisions/` dir empty (Sept 18). **Real gap: SCT writer path is broken, not migrated.** |
| **Source-level hardening (a/b/c)** | ⚠️ UNVERIFIED LIVE | Need 3 targeted probes (art_pusaka.py path, EXPECTED_PYTHON, 03-fhs-canon.conf). Defer to B-1.5 next turn. |
| **BOOT_ATTESTATION_FAILED — _ORGAN_REGISTRY unseeded** | ✅ **REAL** | `_ORGAN_REGISTRY = {}` at line 122 of organ_attestation.py, populated only via `attest_organ()` at line 416. No auto-seed at boot/first-init. **Real bug — affects any F13 path that requires `execution_readiness=ready + session_authority_state=VERIFIED` at session start.** |
| **Reconciliation queue (skewed lineage)** | ⚠️ UNVERIFIED | Need targeted diff. Defer. |
| **SUBSTRATE-FIX LINEAGE** | ⚠️ UNVERIFIED | Need live tree status. Defer. |
| **SUBSTRATE PACKAGE inventory** | ⚠️ UNVERIFIED | Defer. |
| **PACKAGE THESIS** | ⚠️ UNVERIFIED | Defer. |

## Actionable Items (auto-executable)

### B-1.A: SCT writer path — needs 1-line F13 binary or fix
The SCT writer code is missing. Either:
1. The function was deleted (need to find git history)
2. The path was migrated to `forge_work/sct_decisions/` but writer never wired

→ **STAGED for F13** — the F11 audit gap is constitutional, not T1-AUTO. Cannot auto-fix.

### B-1.B: _ORGAN_REGISTRY auto-seed
- Small, well-scoped, in organ_attestation.py
- Patch: add `seed_self_attestation()` call to a boot hook
- BUT: this is a kernel-level change. Should be F13-staged.

### B-1.C: source-level hardening (a/b/c) + reconciliation queue + substrate package
- All T1-AUTO, but each requires precise context (3+ sub-tasks each, ~6 files)
- Total scope: ~6-8 file edits across arifOS + A-FORGE

## Verdict

- **2 REAL bugs confirmed live**: SCT writer path dead (F11), _ORGAN_REGISTRY unseeded (F8/F13)
- **1 FALSE ALARM**: ghost postgres (it's the canonical DB)
- **5 UNVERIFIED**: deferred to next probe turn

## Next action

Stage 2 real bugs as F13-RATIFIED (constitutional), continue probing the 5 unverified.

**Mutation this turn:** ZERO. All sealed as evidence; no source code changed.

## Receipts
- [receipt: /root/A-FORGE/forge_work/2026-07-17/act_decision_events/act_decisions_2026-10-03.jsonl:mtime-2026-10-03-10:42] (live ACT writes, current)
- [receipt: /root/A-FORGE/forge_work/2026-07-17/sct_decision_events/sct_decisions_2026-08-07.jsonl:mtime-2026-08-08-00:09] (SCT dead since)
- [receipt: /root/A-FORGE/forge_work/sct_decisions/:empty] (new dir, no writes)
- [receipt: /root/arifOS/arifosmcp/runtime/organ_attestation.py:line-122,_ORGAN_REGISTRY=init-empty]
- [receipt: docker-inspect:postgres:af-forge:project, vault999:arifos_admin, 4-tables-public+1-observability]
