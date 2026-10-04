# arifFLOW L0→L4 Case Study
## First application of the Cascade Doctrine
### Date: 2026-08-10

---

## Context

arifFLOW (Rust daemon, port 7073) — the arifOS Federation's metabolism plane. 6,200 lines Rust, 560 lines Python. Produces FQ (flow quotient), ingests receipts, gates execution.

Original audit found 5/7 assumptions FALSIFIED. This was the first L0→L4 verification cycle.

## Results

| Phase | Scope | Verdict |
|-------|-------|---------|
| L1↔L2 | Code → Binary | SUPPORTED (byte-identical SHA-256) |
| L2↔L3 | Binary → Behaviour | SUPPORTED (6/6 live tests) |
| L3↔L4 | Behaviour → Reality | SUPPORTED (VAULT999 grew, actor state governs, FQ visible) |

## Transition Matrix

| Finding | Before | After |
|---------|--------|-------|
| V1 Fail-closed | FALSIFIED | WEAKENED (env override exists) |
| V2 FQ consistency | FALSIFIED | WEAKENED (two fields, one enforced) |
| V3 Auto-enforce | FALSIFIED | SUPPORTED |
| V4 Chain validation | FALSIFIED | WEAKENED |
| V5 /release auth | WEAKENED | SUPPORTED |
| V6 VAULT999 | FALSIFIED | SUPPORTED |

## Key Learnings

### 1. Sibling Agent Concurrency

A sibling opencode agent was concurrently editing the same files. Impact:
- Binary built by subagent may be stale relative to sibling's commit
- Mitigation: always `ps aux | grep opencode` before deploy, verify binary hash

### 2. UUID Strictness

arifFlow requires strict UUID v4 for receipt_id/session_id. Custom strings rejected. Use `python3 -c "import uuid; print(uuid.uuid4())"`.

### 3. vault999.rs API

`Vault999Sealer::seal()` takes `checkpoint_hash: [u8; 32]`, not `&FlowReceipt`. Must: `receipt.hash()` → `hex::decode()` → `[u8; 32]` → `sealer.seal(checkpoint)`.

### 4. Missing Required Fields

`cooling_decision` is required in /ingest JSON. Omitting returns 400.

### 5. Deployment Verification

Always `sha256sum` built vs deployed binary. Stale binaries = L1↔L2 gap.

## Verdict: PARTIAL

All 6 claims reach L4 with evidence. 2 claims carry residual architectural debt (WEAKENED). No forced SEAL.

---

*Case study from ARIFOS::L0_L4_CASCADE::v1.0 first application.*
