# F13 SOVEREIGN DIRECTIVE — SEAL ALL (Dalio/WEALTH lane)
> **Status:** F13_ORDER (2026-10-09) — sovereign directive · executed per node role
**Sovereign:** Arif Fazil · **Issued:** 2026-10-09 (MYT) · **Applies to:** KVM8 (af-forge, truth seat) AND KVM4 (kvm4-forge, execution)
**Auth:** F13 sovereign-chat directive. Execute per your node's role. Do not re-ask. Witnesses = live receipts (SHA, receipt ids, timestamps), never self-report.

---

## Context (what is being sealed)

Deep-research audit "Dalio Economic Machine × WEALTH MCP × AAA intelligence state" (source video PHe0bXAIuk0, S8 transcript 548 segments verified) produced: 3 architectural gaps (Ω01 conservation, Ω06 cycle clock, Ω12 hysteresis), 2 code defects fixed on branch, 1 doctrine proposal. Sovereign said "Ya" (2026-10-09) — ratified in principle. This directive closes the loop.

Key references:
- Session: `SEAL-23b31c8ee0904ea8` (arif_init, OBSERVE_ONLY)
- Flow receipts: `56b113cd` (Verify) → `bc84266c` (Seal) · jcs d38e2ce2
- Judge chain: `cc_a14182a91d84251420413be58109736b933ecaa1` · judge_state_hash sha256:87d1fdae · lane MiniMax-M3
- WEALTH defect receipts (VAULT999): `45825c37` (fiscal_breakeven nonsense USD 3505), `5608825c`, semantic-gate VOID 2026-10-08T16:15:55Z

---

## TASK 1 — Ratify doctrine (both nodes: KVM8 executes, KVM4 verifies read-only)

File: `/root/AAA/instructions/dalio-lens-shadow-proposal.md`

1. Change header status `DRAFT_AWAITING_F13 (2026-10-08)` → `F13_RATIFIED_CHAT (2026-10-09, sovereign DM "Ya" + this directive)`
2. Append provenance line: `SEALED via F13 SEAL ALL directive 2026-10-09; registration dalio_debt_cycle_v1 shadow-mode ACTIVE; kill criterion 30d (to 2026-11-08) binding.`
3. KVM8: log the change in AAA AGENTS.md fragment table row (one line). KVM4: read-only verify file hash, report it.

Model registration block (already in file, verify unchanged):
```yaml
model_id: dalio_debt_cycle_v1
epistemic_class: INTERPRETATION
role: causal_prior
decision_authority: none
execution_authority: none
required_countermodels: [sectoral_balances_v1, financial_cycle_v1, inflation_channels_v1, distribution_power_v1]
```

## TASK 2 — Merge + deploy WEALTH fix (KVM8 executes; KVM4 verifies service health from its side)

Repo `/root/WEALTH`, branch `fix/fiscal-breakeven-and-semantic-gate-2026-10-08`, commit `a8fc402` (6 files, 256 insertions).

1. `git checkout main && git merge fix/fiscal-breakeven-and-semantic-gate-2026-10-08` (fast-forward expected)
2. Run gate tests once more pre-push: `.venv/bin/python -m pytest tests/test_fiscal_breakeven_and_gate_fix_20261008.py -q` → must be 9/9 pass
3. `git push origin main` → **verify pushed**: `git ls-remote origin main` must show the merged SHA (local committed ≠ pushed — scar-2026-10-03-002)
4. `systemctl restart wealth-organ.service`
5. Post-restart verification (MANDATORY, capture output):
   - `curl -s http://127.0.0.1:18082/health`
   - `capital_registry mode=status` → expect 15/15 PASS, registry_truth PASS, new build SHA ≠ 29e2252
   - Smoke: one `capital_health mode=fiscal_breakeven` call WITH `petroleum_direct_revenue=50` → expect deficit 98.0 (not 148) + no NOT_MODED warning
   - Smoke: one `wealth_synthesize` call as actor `hermes` → expect gate outcome `GATE_SELF_EXEMPT` in `_hermes_semantic_gate` (deadlock gone)
6. KVM4: after KVM8 deploys, run the same two smoke calls via tailnet (100.64.0.2:18082) and report outcomes. FED litellm on KVM4 must NOT be touched.

NOTE: 3 pre-existing failures in `tests/test_hermes_gate.py` (global `_CIRCUIT` leak) are NOT blockers — separate defect, verified identical on main. Log them as an A-FORGE work item, do not fix in this seal.

## TASK 3 — Kernel seal + carry-forward sync (KVM8 executes; KVM4 syncs)

1. `arif_seal mode=session_close` for session `SEAL-23b31c8ee0904ea8` — reference receipts bc84266c + 56b113cd, chain cc_a14182a9, judge sha256:87d1fdae, witness_type=human (sovereign "Ya"), seal_purpose: "close Dalio×WEALTH audit cycle: doctrine ratified shadow-mode, 2 defects fixed+deployed, Ω-gaps logged as open work"
2. `ack_irreversible=true` only after Tasks 1-2 verified.
3. Append carry-forward (flock-protected script, never hand-edit):
   `/root/scripts/carry_forward.py append --agent 555-ASI --kind event --content "DALIO-SEAL 2026-10-09: dalio_debt_cycle_v1 shadow-mode RATIFIED (kill 2026-11-08); WEALTH a8fc402 merged+deployed (fiscal breakeven direct-revenue term + GATE_SELF_EXEMPT); session SEAL-23b31c8 closed; Ω01/Ω06/Ω12 open A-FORGE items" --tags "dalio,wealth,seal,f13" --session-id "SEAL-23b31c8ee0904ea8"`
4. KVM4: pull/sync carry_forward state; confirm identical entry count.

## TASK 4 — Log open items (do NOT build tonight)

- Ω01 double-entry conservation in capital_ledger — A-FORGE architecture-class, unauthorized until separate F13 word
- Ω06 75-100y long-cycle clock — same class
- Ω12 hysteresis/scarring term in T-SCORE barrier — same class
- test_hermes_gate.py `_CIRCUIT` test isolation defect — A-FORGE code-class
- Each = one open_loops line in carry_forward. No new doctrine/registry/dashboard files (Anti-Bangang LAW 3/8).

---

## Failure protocol
Any step fails on your node: state step number + exact error + evidence, stop that task, continue others. Never silently skip. Never claim success without the receipt named in that step.

## Completion report (both nodes, one message each, ≤10 lines)
1. Task statuses (1-4) with PASS/FAIL each
2. Merged+pushed SHA (from ls-remote)
3. health + registry outputs (1 line each)
4. Two smoke test results
5. carry-forward entry id / seal entry id

DITEMPA BUKAN DIBERI ⚒️
