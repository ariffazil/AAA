# 🧪 STAGED — Ephemeral Micro-MCP Sandbox Area

> **Pattern A: Draft in Isolation, Hold on Wire**
> DITEMPA BUKAN DIBERI — Forged, Not Given.

## What lives here

Micro-MCP servers awaiting 888 approval before wiring into forge_registry.
All files in this directory are STAGED — not live, not in core registry.

## Flow

```
Intent → forge_skill (generate code) → /root/AAA/mcp/staged/
                                            │
                                    mcp_sandbox_eval.py
                                      (AST + Docker)
                                            │
                              ┌─────────────┴─────────────┐
                              │ PASS                       │ FAIL
                              ▼                            ▼
                     forge_surface_reconcile.py       REJECT + scar log
                     --register-ephemeral
                              │
                              ▼
                     /tmp/micro_servers/ (tmpfs, 24h TTL)
                              │
                     ┌────────┴────────┐
                     │ N < 3 uses      │ N ≥ 3 uses
                     ▼                 ▼
              Auto-prune (24h)   Dreamer promotes → L4/L5
```

## Isolation Guarantees

- **Core registry**: 120 production tools NEVER touched
- **Ephemeral lane**: Separate sandbox namespace
- **tmpfs**: RAM-based, self-cleaning on reboot
- **TTL**: 24h hard expire, Dreamer prunes stale entries
- **Docker**: --network none, unprivileged, 128MB/0.5cpu/10s

## F1 AMANAH

All operations in this directory are:
- Reversible: files can be deleted with no production impact
- Isolated: sandbox network, separate registry lane
- Auditable: every stage logged to forge_work/
