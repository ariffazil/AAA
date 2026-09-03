# BLAST_RADIUS.md — Agentic Action Classification

Before any MCP tool acts, classify its blast radius.

| Radius | Name | Example | Ack Required |
|--------|------|---------|-------------|
| **R0** | Thought | Reasoning, planning, analysis | None |
| **R1** | Draft | Text/code draft, preview, dry-run | None |
| **R2** | Local file | Create/edit artifact, config tweak | Cite/confirm |
| **R3** | Memory write | Persistent memory, state change | Consent gate |
| **R4** | External action | API call, docker restart, compose up | Signed session |
| **R5** | Irreversible | Publish, delete, spend, deploy | 888_ACK |

## Usage

When proposing any action, prefix with radius:

```
[R2] Editing /root/arifOS/core/floors.py
[R4] Restarting docker compose service arifosmcp
[R5] Deploying to production — requires 888_ACK
```

## Mapping to arifOS

| Radius | arifOS Stage | Floor Check |
|--------|-------------|-------------|
| R0-R1 | 111-333 (Mind/Reason) | F4 Clarity |
| R2 | 444 (Kernel/Route) | F1 Amanah |
| R3 | 555 (Memory) | F6 Empathy, F11 Audit |
| R4 | 777 (Ops/Forge) | F8 Genius, F12 Resilience |
| R5 | 888 (Judge) | F13 Sovereign, explicit ACK |

## Thermodynamic Cost

| Radius | Typical Energy Cost | Typical ΔS |
|--------|---------------------|------------|
| R0 | Near zero | Neutral |
| R1 | Low | Slightly positive |
| R2 | Low | Neutral |
| R3 | Medium | Persistent |
| R4 | High | System-visible |
| R5 | Very high | Irreversible |

DITEMPA BUKAN DIBERI
