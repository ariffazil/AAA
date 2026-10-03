# MCP Lifecycle Corrected Audit — 2026-10-03 15:25

**Status**: Arif caught me. I made the same epistemic error twice (single-measurement → narrative).

## What I claimed (WRONG)

| Claim | Reality | Live proof |
|---|---|---|
| "wealth dead" (masked unit) | **ALIVE** on port 18082, owned by `tailscaled` (PID 246852) | ss -tlnp shows 18082 LISTEN |
| "well dead" | **ALIVE** on 18083, owned by tailscaled | ss -tlnp shows 18083 LISTEN |
| "hermes-mcp stdio spawned by codex" | **ALIVE** on 18420, owned by python process (hermes-rasa/server.py, PID 3992521) | ps shows actual command, parent=systemd |
| "fed: no service file" | **fed-router.service EXISTS and is running** | systemctl list-units shows it active |
| "frame: no service file" | **frame-mcp.service AND frame-organ.service EXIST and running** | systemctl list-units shows both |
| "firecrawl-mcp stdio" | **stdio can't listen TCP**; port 8931 is owned by playwright-mcp (node process) | ps shows node command |
| "6 dead MCPs" | **0 dead MCPs** | All 6 ports respond, just different supervisors |

## What I did right

- **Live probe L0 (PID), L1 (port)**: both true.
- **FAILED on L2 (MCP ready)**: my probe called `tools/list` without `initialize` first, got Bad Request.
- **FAILED on L4 (recovery)**: I didn't walk parent chain.

## Per Arif's audit doctrine: HEALTHY MCP ≈ L3 + L4

- L0 (PID): 10/10 alive
- L1 (port): 10/10 alive
- L2 (MCP ready): need to test with `initialize` first
- L3 (tools/list): blocked by L2
- L4 (recoverable): unmeasured

**So I claimed "all 6/6 alive therefore OK" — wrong. L0+L1 are true, but L2+L3+L4 are unmeasured.**

## What I'll do (no mutasi, this turn)

1. Write 1 spec (MCP Lifecycle Registry v1) per your audit framework
2. Add to carry_forward as F13-stash: build the registry
3. Update audit receipt (this one) replacing the wrong claims
4. NO new code, NO new hooks, NO new mutasi

## What I will NOT do (per Law 10)

- ❌ Tweak wealth/well/fed/frame unit files (irreversible)
- ❌ Add new systemd units (overkill for audit fix)
- ❌ Make more claims without multi-axis measurement

## Reversibility

`rm /root/AAA/docs/audit-receipts/MCP-LIFECYCLE-CORRECTED-AUDIT-2026-10-03.md` (1 command)
`rm /root/AAA/docs/blueprints/MCP-LIFECYCLE-REGISTRY-SPEC-v1.md` (1 command)

