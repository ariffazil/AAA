# AUTH Protocol — Canonical Home

> **This is the protocol definition.**
> **The execution engine lives in A-FORGE:** `/root/A-FORGE/src/domain/auth/pipeline.ts`
> **AAA owns the protocol. A-FORGE owns the execution.**

## Files

| File | Purpose |
|------|---------|
| `DOCTRINE.md` | Canonical protocol definition — the five questions, three laws, jurisdiction boundary |
| `task_contract.ts` | TypeScript schema — TaskContract, EvidenceBundle, PipelineStatus, PipelineStage |
| `task_contract_v1.yaml` | Human-readable contract template |
| `sample_contract.json` | Example contract for testing |

## Execution

The `auth_pipeline` MCP tool is registered on A-FORGE (:7072). It chains:

```
DECLARE → LEASE → LOCK → EXECUTE → EVIDENCE → VERIFY → JUDGE → MERGE → SEAL → INGEST
```

Each stage delegates to existing A-FORGE + arifOS tools.

## Architecture

```
AAA (Wisdom + Process)
├── 333-AGI — "What should we do?"
├── 555-ASI — "Is the evidence sound?"
├── 888-APEX — "Is this constitutional?"
└── AUTH — "Was the process followed?"

A-FORGE — "What is executed?"
VAULT999 — "What is proven?"
arifFLOW — "What happened?"
```
