# Closed-Loop V-Model Harness Doctrine

> **CANONICAL PRINCIPLE:** "The worker never grades its own homework; verifiers observe the raw artifact, not the summary."

## 1. The V-Model Topology

```
[1. Intent / Task Contract] ──────────────────────────► [5. Acceptance & Seal]
         │                                                      ▲
         ▼                                                      │
[2. Falsifiable Criteria Decomposition] ──────────► [4. Independent Verification]
                   │                                            ▲
                   ▼                                            │
               [3. Apex Construction (Execution Worker)] ───────┘
```

## 2. Invariant Rules

1. **Separation of Concerns:** The agent that writes the code or mutates the environment (`333 ARCHITECT` / `EXECUTION WORKER`) CANNOT issue the final verdict.
2. **Raw Artifact Observation:** Verifiers (`555 AUDITOR` / `FRAME Observer` / `888 APEX`) must read raw command outputs, stdout, stderr, process tables, and file hashes — never the summary markdown claims made by the worker.
3. **Falsification-First:** Every task must define at least one negative or boundary test condition before implementation begins.
4. **Deterministic Receipts:** Every verified cycle logs an immutable receipt to `VAULT999/RECEIPTS/` containing timestamps, actors, raw proofs, and delta-S <= 0 verification.
