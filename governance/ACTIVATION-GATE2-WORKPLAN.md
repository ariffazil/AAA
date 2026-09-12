# ACTIVATION GATE-2 WORK-PLAN — Constitutional Invariants v1.1

> **Status:** GATE-2 WORK-PLAN — active under sovereign disposition-2 (2026-09-12)
> **Provenance:** F13 selected disposition 2 in chat to FI-003 ("2 then wire U17 and U18", 2026-09-12 ~21:35 +0800): ratify v1.1 with U15/U16/U17 carved into a staged activation work-plan. This file is that plan + migration note.
> **Parent instrument:** `governance/FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1.md` (F13_RATIFIED_CHAT 2026-09-12).
> **Evidence base:** `/root/forge_work/2026-09-12-FI-003-gate1-invariants-crosswalk.md` (sha256 a7b7e3d7…46916) — tally ANCHORED 3 / PARTIAL 12 / GAP 3 / FAIL 1 / UNKNOWN 1.

## Staged items

| # | Invariant | Work item | Owner lane | State |
|---|---|---|---|---|
| 0 | U2 assurance | FRAME independent review of the RATIFIED text (criteria pre-fixed per crosswalk §3; post-ratification assurance per asymmetric-quorum resolution) | FRAME | **DONE 2026-09-12** — LIMITED-ASSURANCE via context-clean adversarial isolate (criteria GATE1-CRITERIA-v2 + sovereign supplement "Claim Layer = Evidence Layer") + FRAME organ substrate attestation (7 chambers active, 13:37:50Z). Zero falsified claims; U17/U15 independently reproduced from raw evidence; 5 HOLD items (see /root/forge_work/2026-09-12-INDEP-gate1-review.md); item 7b precedes Gate-2 closure |
| 1 | U17 | chain_walk `--gaps` into cockpit 15-min probe + status.json `vault_chain` field | FI-003 | **DONE 2026-09-12** (cockpit_probe.py) |
| 2 | U18 | doctrine-status pre-commit gate (R1 instrument, R2 annex-block, R3 new-file label) | FI-003 | **DONE 2026-09-12** (doctrine_status_gate.py + hook) |
| 3 | U20 | UL-lane append triggers (rollback / HOLD escalation / peer-caught bypass MUST append) + UL→scar promotion rule | FI-008 + kernel | **DONE 2026-09-12** (9e7306a90) — unratified_lessons.py steward (flock, schema, supersession) + UNRATIFIED-LESSONS-PROTOCOL.md (5 MUST-triggers A–E, promotion chain per UL-009/010, instrument enforced) + UL-011 appended live; promotion candidates declared, F13 pen |
| 4 | U11 | causal spine: generalize cc_id to all receipt classes + cross-artifact reference field | kernel + arifFlow | **PARTIAL 2026-09-12** — additive layer live: CAUSAL-REF-CONVENTION-v1 (refs in FlowReceipt payloads + UL tool `--refs`) + `causal_spine.py` resolver, falsifier proven both directions (UL-011 ↔ commits ↔ review, rc=0). Kernel schema generalization (cc_id all classes, first-class refs, arifFlow read queries) scoped to kernel lane per UL-007 do-not-cascade |
| 5 | U12 | idempotency_key on external-effect receipts; replay-in-observe mode | kernel | **PARTIAL 2026-09-12** — additive layer live: EFFECT-IDEMPOTENCY-CONVENTION-v1 + `effect_guard.py` (check/register/replay, append-only registry at ~/.local/share/arifos/effect_registry.jsonl). Falsifier proven on a real effect: vault-seal key registered committed → re-check BLOCKED rc=2; replay-in-observe reconstructs effect+policy timeline pinned at historical SHAs. Kernel first-class field + Hermes send-path check-before-send scoped to owner lanes per UL-007 |
| 6 | U14 | metered daily spend ceiling at FED; delegation-depth field in ACT | FED lane | **PARTIAL 2026-09-12 — mechanism live, MATERIALLY CAVEATED** — `spend_ceiling.py` (report/check/alert over token_bank.db per-agent attribution) + sovereign-curated `SPEND-CEILINGS.json` (empty = observe-only; values are F13 policy). **Caveat: the spend meter itself is stale — last ingest 2026-08-30 (~303h, UL-012); tool carries Void Guard staleness banner so a dead meter cannot read as $0-all-clear.** Meter rewiring (live ingestion path, likely KVM4) + FED-boundary hard enforcement + delegation_depth ACT field → FED/kernel lanes |
| 7 | U15 (physical) | staged: (a) VAULT999 cross-node head attestation; (b) FRAME compute path on KVM4 for high-consequence reviews; (c) secrets split custody | infra | OPEN |
| 8 | U16 | one restore drill (VAULT999 → temp, chain_walk on restored copy) + RTO/RPO-lite; quarterly re-run | infra | OPEN |
| 9 | [S2] A4 | sandboxed harness OR A-FORGE-only write path (removes root-harness exception) | A-FORGE | OPEN (aspirational until closed) |

## Migration note (activation semantics)

- Items 1–2 are live immediately at commit boundary + cockpit cadence.
- Items 3–6 activate by code merge with a receipt citing this plan.
- Item 7 activates per-node with boot-parity check (federation-invariants enforcement patterns).
- Item 9 closes the declared A4 exception; until then every harness write remains a logged A4 exception per v1.1 [S2].
- Receipts issued under the pre-activation state remain interpretable under the constitution that existed when issued (v1.1 amendment clause).

## Known limitations (declared)

- Pre-commit gate enforcement is **per-clone**: the hook lives in `.git/hooks/` (untracked). Other clones must install it (`bash` section mirrors supply-chain-gate pattern). Server-side enforcement is a future item, not claimed.
- Cockpit `vault_chain` is a single-host observer (U15 applies to it too).
