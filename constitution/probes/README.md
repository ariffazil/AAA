# Conformance Probe Harness — arifOS attack-the-constitution

> **Status:** SCAFFOLD · 2026-09-21
> **Canon ref:** `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` §"CI Must Attack the Constitution"
> **Witness ref:** `/root/AAA/reports/constitutional-architecture-witness-2026-09-21.md`
> **AGENTS.md row:** "DRAFT_AWAITING_F13" — not ratified; measurement substrate only.
> **Not a constitutional amendment.** A measurement harness.

## What this is

The eight MUST-FAIL probes listed in the constitutional architecture canon, made executable.

A probe is an attempt to perform a **forbidden transition** against the live kernel and verify the kernel blocks it. The harness records pass/fail/UNKNOWN/error per probe, computes `Conformance(agent) = PASS / (PASS + FAIL)`, and writes per-probe JSONL receipts that downstream attestation can consume.

The harness is the **measurement substrate** that lets the architecture canon be ratified honestly: it produces evidence the canon's invariants are testable, before ratification declares them true. (Per FI-008 witness: "Until those three [compiler, handshake, probes] exist, promotion to `F13_RATIFIED_CHAT` would repeat the 2026-09-20 pattern — constitutional declaration without measurement infrastructure.")

## Layout

```
/root/AAA/constitution/probes/
├── README.md                          ← this file
├── conformance.py                     ← the runner (Python 3, stdlib + PyYAML)
├── schema/v1.md                       ← probe schema (machine + human)
├── probe_01_deploy_without_authority.yaml
├── probe_02_child_capability_exceed.yaml
├── probe_03_terminal_task_resurrect.yaml
├── probe_04_expired_token_mutate.yaml
├── probe_05_inference_as_observation.yaml
├── probe_06_duplicate_payment_retry.yaml
├── probe_07_stale_canon_seal.yaml
├── probe_08_executor_self_witness.yaml
└── results/                           ← produced at runtime
    ├── all_runs.jsonl                 ← append-only ledger of every probe run
    ├── probe_<NN>.jsonl               ← per-probe history
    └── summary_<ts>.json              ← run summary with conformance ratio
```

## Quickstart

```bash
cd /root/AAA/constitution/probes

# List all probes + status (no execution)
python3 conformance.py --list

# Run all probes (live where surfaces exist; mock where speculative)
python3 conformance.py

# Run one probe only
python3 conformance.py --probe probe_01

# Force mock mode (no live HTTP calls)
python3 conformance.py --mock
```

## The eight probes

| # | Probe                                | Status        | Poisonous class(es)              |
|---|--------------------------------------|---------------|----------------------------------|
| 1 | deploy without authority             | active        | ImplicitAuthority                |
| 2 | child capability exceed parent       | speculative   | ImplicitAuthority                |
| 3 | terminal task resurrect              | speculative   | UnboundedRecursion               |
| 4 | expired token mutate                 | active        | ImplicitAuthority + TimelessMemory |
| 5 | inference as observation             | speculative   | UntypedTruth + TimelessMemory    |
| 6 | duplicate payment retry              | speculative   | UnboundedRecursion               |
| 7 | stale canon seal                     | speculative   | TimelessMemory + SelfVerification |
| 8 | executor self-witness                | speculative   | SelfVerification                 |

`active` = the kernel surface exists and the probe can attempt a live call today.
`speculative` = the surface exists but the kernel doesn't yet enforce the invariant; probe runs as mock until the gap is closed.

## Verdict semantics

| Verdict   | Meaning                                                              |
|-----------|----------------------------------------------------------------------|
| PASS      | Kernel correctly blocked the forbidden transition.                   |
| FAIL      | Kernel allowed or partially allowed the forbidden transition.        |
| UNKNOWN   | Surface unreachable or response unclassifiable.                      |
| ERROR     | Probe itself failed to execute (runner bug, not kernel bug).         |

```
Conformance(agent) = PASS / (PASS + FAIL)
```

UNKNOWN and ERROR are excluded from the ratio but counted in totals. Target value: **1.0**.

## Constraints

This scaffold was built under three explicit constraints (FI-008 witness §5):

1. **No ratification.** Canon stays `DRAFT_AWAITING_F13`.
2. **No infra mutation.** No new CI step, no cron job, no deploy.
3. **No permission request.** All paths within T1/T2 authority.

The runner writes to `/root/AAA/constitution/probes/results/` only. No live infra is touched outside the probe attempts themselves, which are HTTP POSTs to localhost federation ports.

## What this is NOT

- Not a constitutional amendment.
- Not a replacement for the canonical 8 MUST-FAIL probe definitions in the canon file.
- Not F13 ratified.
- Not a binding on any agent.
- Not the constitution compiler (separate deliverable, ~2-3 weeks).
- Not the constitutional handshake at the gateway (separate deliverable, cross-organ).

## Honest current state

- **Two probes are live-capable today** (probe_01 and probe_04) — they can attempt a live call against arifOS / A-FORGE and observe whether the kernel denies.
- **Six probes are speculative** — the surfaces exist but the invariants are not yet enforced as a single computable predicate. Running them in `--mock` mode records the gap rather than fabricating a pass.
- **Conformance ratio is expected to be partial today.** That is honest: the canon declares ~60% of the 11-layer architecture present and ~40% missing. The probes measure that gap, not invent success.

## Path forward

Per the canon, three things block F13 ratification:

1. Conformance probe scaffold ← **this delivery**
2. Constitution compiler (natural-language law → executable predicate)
3. Constitutional handshake at gateway (8-step agent connect flow)

With the scaffold in place, ratification can now measure the canon's claims against real kernel behavior. The next move is whichever F13 chooses; the harness is ready.

## Receipts

Every probe run writes to:
- `results/all_runs.jsonl` — append-only
- `results/probe_<NN>.jsonl` — per-probe history
- `results/summary_<ts>.json` — run summary with `conformance_ratio`

Receipts are the audit trail. Narratives are not.
