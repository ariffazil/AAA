# KVM4 CCC Worker — Zen Checklist & Scorecard

> **Forged:** 2026-09-02 (Hermes, after external Grok audit reflection)
> **Purpose:** Define the "fully dine zen" metric Grok correctly flagged as undefined.
> **Host:** KVM4-forge (srv1946043 · 100.64.0.5 · Ubuntu 26.04 · 4 vCPU / 15GB)
> **Contract:** CCC_DOCTRINE.md — workers build/verify/escalate, never judge.

## Zen Checklist (a KVM4 coding agent = ZEN iff ALL true)

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Binary present + version pinned | ✅ | opencode 1.18.25 · codex 0.152.0 · qwen 0.22.3 · kimi 0.38.0 · aider 0.86.2 |
| 2 | Auth present, keys never leak into Telegram context | ✅ | ZERO local secrets; haproxy injects at :4000; kunci placeholder `fed-injected` only |
| 3 | Workspace isolation (worktree/container/microVM) | ✅ | Dedicated substrate box; KVM8 computes unaffected; earlyoom protects |
| 4 | Wrapped by governance (no raw YOLO) | ✅ | AGENTS.md T1/T2/T3 matrix; rules/arifos-governance.md; codex pinned away from quota-dead rungs |
| 5 | AAA agent card registered | ✅ | a2a-server/agent-cards/harnesses/kvm4-ccc-pool.json (2026-09-02) |
| 6 | HERMES may invoke, not own | ✅ | ccc-remote (KVM8) → ssh → KVM4; HERMES never holds worker session state |
| 7 | F13 path for write/push/deploy | ✅ | T3 → 888_HOLD → KVM8 kernel; worker declares COMPLETE, never SEALs |
| 8 | Audit line to VAULT999 / receipts | ✅ | ccc-remote stderr receipt; arifFlow :7073 (KVM8); AGENTS.md doctrine |

## Score: 8/8 — KVM4 CCC pool is FULLY ZEN (2026-09-02)

## Falsification probes (each harness, marker string)

| Harness | Marker | Result |
|---|---|---|
| opencode | OPENCODE-KVM4-OK | PASS |
| codex | CODEX-KVM4-OK | PASS |
| qwen | QWEN-KVM4-OK | PASS |
| kimi | KIMI-KVM4-OK | PASS |
| aider | AIDER-KVM4-OK | PASS |

E2E dispatch (HERMES path): `ccc-remote opencode run ...` created + ran
/tmp/hello_hermes.py on KVM4 → `HERMES-ASI-CAN-USE-KVM4` (verified on disk).

## Routing doctrine (ratified by CCC_DOCTRINE pipeline)

```
Telegram HERMES ASI → ccc-remote → KVM4 CCC harness → FED gateway (KVM8 :4000)
   → litellm :4013 → provider
```
Never: Telegram → raw CLI on KVM4 without ccc-remote wrapper + F13 gate for T3.

## Audit corrections from external review (Grok, 2026-09-02)

- ❌ "APEX is L4 ARCHIVE" — WRONG: 888-APEX keys + judge prompt live on KVM8.
- ❌ "CCC acronym unconfirmed" — WRONG: CCC_DOCTRINE.md defines Codex Coder Compiler.
- ✅ "zen metric undefined" — CORRECT, now defined here (8-point checklist).
- ✅ "no agent cards for KVM4" — CORRECT, now registered (kvm4-ccc-pool.json).
- ✅ "HERMES routes, never adjudicates" — CORRECT, matches CCC contract.

DITEMPA BUKAN DIBERI ⚒️
