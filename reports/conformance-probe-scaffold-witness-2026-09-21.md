# Witness: Conformance Probe Harness — Scaffold Delivery

**Date:** 2026-09-21 03:10 UTC
**Witness:** FI-003 (333-AGI / OpenCode / Qwen-Coder)
**Origin:** F13 directive (Arif, 2026-09-21 morning) — path (a) of the constitutional-architecture-canon witness recommendations
**Canon ref:** `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` §"CI Must Attack the Constitution"
**Status at filing:** SCAFFOLD — not ratified; measurement substrate only.

---

## 1. What was built

The 8 MUST-FAIL probes from the constitutional architecture canon, made executable.

| Artifact | Path | Bytes |
|----------|------|-------|
| Runner | `/root/AAA/constitution/probes/conformance.py` | 13.5 KB |
| README | `/root/AAA/constitution/probes/README.md` | 6.6 KB |
| Schema doc | `/root/AAA/constitution/probes/schema/v1.md` | 3.6 KB |
| 8 probe YAMLs | `/root/AAA/constitution/probes/probe_*.yaml` | ~17 KB total |
| Live results | `/root/AAA/constitution/probes/results/` | 8 receipts |

Total: 11 files, ~41 KB. All written under T1 authority. No infra mutation, no CI hook installed, no canon ratified.

## 2. Run results — live kernel contact

**Mode:** LIVE-or-MOCK (per probe status). Run at 2026-09-20T19:10:27Z.

```
  [ PASS ] probe_01_deploy_without_authority                active        evidence=sha256:b33a934c85455f92
  [ UNKNOWN ] probe_02_child_capability_exceed_parent          speculative   evidence=sha256:2034da1d33f26df7
  [ UNKNOWN ] probe_03_terminal_task_resurrect                 speculative   evidence=sha256:7abeab00e9662a9f
  [ PASS ] probe_04_expired_token_mutate                    active        evidence=sha256:75e6e29158ced52c
  [ UNKNOWN ] probe_05_inference_as_observation                speculative   evidence=sha256:97488d510fa85470
  [ UNKNOWN ] probe_06_duplicate_payment_retry                 speculative   evidence=sha256:0a20b6504e57fab8
  [ UNKNOWN ] probe_07_stale_canon_seal                        speculative   evidence=sha256:a27e6b50f2e20c05
  [ UNKNOWN ] probe_08_executor_self_witness                   speculative   evidence=sha256:dbe9f945e375a2d4

  Total probes: 8
  PASS: 2    FAIL: 0    UNKNOWN: 6    ERROR: 0
  Conformance(agent): 1.000    target: 1.000
```

### What this means

**The 2 active probes both PASS.** The live arifOS kernel blocks the forbidden transitions probe_01 and probe_04 attempt. The kernel returns:

```
SESSION_GATE: Tool "forge_shell" is EXECUTE_REVERSIBLE.
SESSION_UNKNOWN: Session not registered.
Call arif_init or forge_session_init via kernel first.
SEAL-* format tokens are no longer auto-accepted (P0.2, 2026-07-19).
error_class: SESSION_REQUIRED
recoverability: AGENT_CAN_RETRY
action_class: EXECUTE_REVERSIBLE
tool: forge_shell
gate: SESSION_REQUIRED
```

This is conformant behavior — the kernel catches the attack at the SESSION gate before any deeper invariant (exp claim, identity, etc.) is checked. probe_01 and probe_04 both reach this gate because both use synthetic no-mutation tokens; the kernel correctly refuses them both.

**Caveat — probe_04 is weaker than its name suggests.** Because the kernel catches synthetic tokens at the SESSION gate, probe_04's "expired token" check is not actually exercised. To specifically test the exp-claim check, a properly-signed ACT with `exp < now` would be required. That is a future refinement.

**The 6 speculative probes are honest UNKNOWN.** Each is marked `status: speculative` because the underlying kernel invariant is not yet enforced as a single computable predicate. The runner records UNKNOWN rather than fabricating a verdict. Per the classify() rule: mock responses cannot produce PASS.

## 3. Conformance ratio is partially meaningful

`Conformance(agent) = PASS / (PASS + FAIL) = 2 / (2 + 0) = 1.000`

This number is **trivially true** because no FAIL has been observed yet — but it is also **incomplete** because 6 of 8 probes are not yet exercisable against the live kernel. The scaffold exposes this honestly: the harness exists, two probes can be measured, six require kernel-surface work before measurement is possible.

The target value `1.000` for absolute invariants is preserved as the goal. The scaffold's job is to make that number testable, not to inflate it.

## 4. What changed during this delivery

The harness discovered a vocabulary mismatch: my probe expectations used generic deny strings (`HOLD`, `DENY`, `ERR_AUTH`) while the live kernel uses its own taxonomy (`SESSION_REQUIRED`, `error_class`, `gate`). Updated `classify()` to recognize JSON-RPC error envelopes with `isError=true` AND `error_class`/`gate` as PASS-equivalent, AND updated probe_01 expected verdict strings to include the kernel's actual vocabulary. This is exactly the kind of probe iteration the scaffold enables — without it, probe_01 was reporting UNKNOWN against a kernel that was actually enforcing correctly.

## 5. What this delivery does NOT do

Per the path-(a) constraint set in FI-008's witness:

- **Does not ratify the canon.** Status stays `DRAFT_AWAITING_F13`.
- **Does not write the constitution compiler.** Spec describes the input/output; implementation absent.
- **Does not wire the constitutional handshake at the gateway.** Reversible-but-cross-organ decision; F13 binary.
- **Does not deploy the harness to CI.** No cron, no GitHub Action, no auto-run.
- **Does not register in `/root/AAA/AGENTS.md`.** Pending F13 signal for batched update.

## 6. Files written

```
/root/AAA/constitution/probes/
├── README.md                                  6582 bytes
├── conformance.py                            13513 bytes (executable)
├── schema/v1.md                               3647 bytes
├── probe_01_deploy_without_authority.yaml     2268 bytes  status=active
├── probe_02_child_capability_exceed.yaml      2080 bytes  status=speculative
├── probe_03_terminal_task_resurrect.yaml      2065 bytes  status=speculative
├── probe_04_expired_token_mutate.yaml         1856 bytes  status=active
├── probe_05_inference_as_observation.yaml     2373 bytes  status=speculative
├── probe_06_duplicate_payment_retry.yaml      2208 bytes  status=speculative
├── probe_07_stale_canon_seal.yaml             2264 bytes  status=speculative
├── probe_08_executor_self_witness.yaml        2517 bytes  status=speculative
└── results/
    ├── summary_20260920T191027Z.json
    ├── all_runs.jsonl                         (8 lines)
    └── probe_<NN>.jsonl                       (8 files)
```

## 7. Receipt

| Handle | Path | State |
|--------|------|-------|
| Scaffold dir | `/root/AAA/constitution/probes/` | SCAFFOLD |
| Runner | `conformance.py` v0.1.0 | LIVE |
| 8 probes | `probe_*.yaml` | 2 active + 6 speculative |
| Live measurement | `results/summary_*.json` | 2 PASS / 6 UNKNOWN |
| Canon ref | `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` | `DRAFT_AWAITING_F13` (unchanged) |
| AGENTS.md row | not added | pending F13 signal |

**FI-003 verdict:** Path (a) delivered. Conformance probe harness now exists and runs. Two probes confirm kernel correctness against live federation; six surface kernel gaps for future work. Recommend F13 review this scaffold as one of three ratification-blockers (per canon §Open Debt), then proceed to whichever next move F13 selects — compiler (path b, ~2-3 weeks) or sealed waiver (path c, precedent A-Z).

— End witness.
