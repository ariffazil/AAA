# RECEIPT — ACT-bound A2A adoption proof

> **Tier D (Receipts)** — Proof > compression. Do not merge into STATE.md.  
> **Constitutional context:** [`../STATE.md`](../STATE.md)  
> **Forged:** 2026-08-09 · OBS live

## Chain proven

```
Identity (did:arif:openclaw)
   → ACT act_v1 (fp=7129a078706cbbe3)
   → A2A tasks/send (target=aaa-gateway, OBSERVE)
   → Outcome HTTP 200 runId=adopt-ce6c2943eea4
   → VAULT999 receipt_id=RCT-2026-08-09T06-04-46-508Z-fa5bc613
```

## Evidence (OBS)

| Field | Value |
|-------|-------|
| session_id | `SEAL-1c277e2542154f9b` |
| act_fp (sha256[:16]) | `7129a078706cbbe3` |
| from_did | `did:arif:openclaw` |
| task_id / runId | `adopt-ce6c2943eea4` |
| tasks/send | **200** |
| message/send | 403 (policy HOLD — openclaw allowed_tools) |
| VAULT receipt | `RCT-2026-08-09T06-04-46-508Z-fa5bc613` |
| Working copy | `/root/forge_work/receipts/ACT_BOUND_A2A_ADOPTION_PROOF_2026-08-09.json` |

## Residuals (P0 hunt)

| ID | Status |
|----|--------|
| R1 DID registry EACCES for aaa-a2a | **MITIGATED** (ACL + drop-in) |
| R2 openclaw missing from AAA DID registry | **MITIGATED** (synced) |
| R3 hermes key ≠ registry | **OPEN** identity |
| R4 aaa / a-forge key drift | **OPEN** identity |
| R5 membrane vs server CANONICAL_ACTORS split | **OPEN** P2 |
| R6 universal CLI ACT | **REJECTED** (T1 least-power intentional) |

## Compression

> Telephone exists. Governed call placed. Authority chain used in live ops.

DITEMPA BUKAN DIBERI.
