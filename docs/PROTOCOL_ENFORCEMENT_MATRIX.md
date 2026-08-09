# Protocol Enforcement Matrix — L0–L6

> **Forged:** 2026-08-09  
> **Doctrine:** Protocols coordinate. Governance decides.  
> **Probe:** `/root/AAA/scripts/protocol-enforce.sh`  
> **Lightweight:** `state-probe.sh` §7  

## Authority flow (enforced)

```text
L6 VAULT999     → Can it be proven?
L5 ACT + DID    → Who may act?
L4 arifOS       → Should it be done?
L3 A2A          → Who is talking? (transport)
L2 MCP          → How is work executed? (transport)
L1 CALL_MAP     → Where do I send requests?
L0 STATE_READY  → Is the system standing?
```

## Live enforcement map (OBS)

| Layer | Mechanism | Fail-closed behavior | Probe |
|-------|-----------|----------------------|--------|
| **L0** | `state-probe.sh` | exit 1 DEGRADED / 2 DOWN | §1–6 |
| **L1** | CALL_MAP + 3-layer registry | docs missing → probe fail; bad cards skipped | §1 + catalog |
| **L2** | Streamable HTTP MCP initialize | organ down → hard fail in `protocol-enforce` | MCP POST /mcp |
| **L3** | `A2A-Version: 1.0` middleware | missing → **400** | curl without header |
| **L3** | EMD tri-witness gate | anonymous low-W³ → **403 EMD_VALIDATION_BLOCKED** | curl anonymous task |
| **L3** | DISPLAY_ONLY ceiling | AAA health requires ceiling; envelope blocks mutation | health + federation_envelope |
| **L4** | Holy 8 MCP tools | missing arif_judge → fail | tools/list |
| **L5** | ART gate `act_v1.*` / `sct_v1.*` | invalid token format rejected | art_gate.js |
| **L5** | DID registry + organ keys | sparse keys → soft/hard in probe | filesystem |
| **L6** | VAULT999 `outcomes.jsonl` | missing/empty → hard fail | file size + AAA vault CONNECTED |

## What is **not** yet hard-enforced (honest)

| Gap | Risk | Next |
|-----|------|------|
| Every MCP mutate requires live ACT validation | Some local CLI paths trust process identity | Keep T3 HOLD; tighten forge_sct on mutate |
| Hermes A2A :18089 agent-card | Incomplete peer discovery | Publish card or AAA pointer |
| MCP protocolVersion skew (03-26 vs 11-25) | Client fragility | Negotiate only; document |
| Full OTel | Observability | later |
| Multi-hop ACT chain | Deferred by naming SEAL | after telephone proven |

## Operator commands

```bash
# Daily / CI
/root/AAA/scripts/state-probe.sh          # L0 + lightweight L4/L6
/root/AAA/scripts/protocol-enforce.sh     # full L0–L6 matrix

# Expect
# STATE_READY warn=0
# PROTOCOL_ENFORCED warn=0
```

## One-sentence SEAL

> **MCP tells how to use tools, A2A how to talk, ACT/did:web who may act, arifOS what is allowed, VAULT999 what can be proven — and probes fail closed when those gates are missing.**

DITEMPA BUKAN DIBERI.

## Authority layer detail

[`ACT_AUTHORITY_LAYER.md`](./ACT_AUTHORITY_LAYER.md) — did:web = who · ACT = what office · F1–F13 = should · VAULT = prove.
