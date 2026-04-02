# core/kernel — arifOS Kernel Loop

> **DITEMPA BUKAN DIBERI** — *Forged, not given.*

```
Location: /root/waw/core/kernel/
Role: Kernel loop implementation (QueryEngine pattern from Claude Code leak analysis)
Status: DRAFT — needs wiring to arifOS MCP at localhost:8080
Version: 2026-04-01
```

## What This Is

Implementation of a Claude Code-style agent loop patterned after the 2026-03-31 leak analysis.
The leak confirmed the "right" pattern for coding agents:
- One master loop engine (QueryEngine = this kernel)
- Permissioned tools with a policy firewall between LLM and execution
- Multi-agent orchestration with restricted tool scopes
- Layered memory
- Feature-flagged autonomy

## Files

| File | Purpose | Status |
|------|---------|--------|
| `kernel_loop_v1.json` | Architecture spec — full design document | ✅ Complete |
| `kernel_loop_interface.py` | Python interface — Runnable skeleton | ⚠️ Needs wiring |

## How It Maps to arifOS Architecture

Per `arifOS/README.md`:

| README Layer | This Directory | What It Does |
|-------------|----------------|--------------|
| `core/kernel/` (evaluator.py, consensus.py) | `kernel_loop_interface.py` | `KernelLoop` class — owns LLM calls, tool invocation, retries, budgets |
| `core/shared/floors.py` | `kernel_loop_interface.py::ConstitutionalHooks` | F1-F13 pre/post loop hooks |
| `arifosmcp/runtime/` | Wire `_execute_tool()` to MCP client | Execute tools via arifOS MCP at localhost:8080 |
| Agent spec | Not yet implemented | `CoordinatorAgent` pattern — spawn children with constrained scopes |

## How to Wire It

1. **Implement `_execute_tool()`** in `KernelLoop` — call your MCP client at port 8080
2. **Register existing tools** from MCP server into `ToolRegistry` with `risk_tier` and `permission_tier`
3. **Bootstrap `ToolPolicyEngine`** in your MCP server startup
4. **Wire `888_JUDGE`** as the `auditor_handle` — constitutional compliance checking
5. **Add mode switching** — `internal` / `external_open` / `external_undercover` via `KernelConfig`

## Trinity Alignment

```
Architect (Δ) = KernelLoop — controls routing, budgets, pipeline
Auditor (Ω)  = 888_JUDGE — constitutional compliance, trace validation
Agent (Ψ)    = MCP tool hosts — execute, stateless
```

## Relationship to Claude Code Leak

| Claude Code (Leaked) | arifOS Kernel (This) |
|---------------------|---------------------|
| QueryEngine.ts (~46K LoC) | `KernelLoop` class |
| Tool.ts (~29K LoC) | `ToolRegistry` + `ToolPolicyEngine` |
| bashSecurity.ts (23 checks) | `ConstitutionalHooks.post_git_check()` + add bashSecurity equivalent |
| Commands (~80-85 commands) | arifOS ~40 MCP tools |
| KAIROS background agents | `BackgroundScheduler` (not yet implemented) |
| BUDDY companion agent | `BuddyAgent` (not yet implemented) |
| Undercover Mode | Mode system: `internal` / `external_open` / `external_undercover` |

## Next Steps

- [ ] Wire `KernelLoop._execute_tool()` to MCP client at localhost:8080
- [ ] Register all 40 MCP tools into `ToolRegistry` with risk tiers
- [ ] Implement bashSecurity 23-point check equivalent
- [ ] Add `BackgroundScheduler` for KAIROS/BUDDY patterns
- [ ] Write automated tests for kernel loop (Claude Code's biggest failure)

## Reference

- arifOS README: `/root/waw/arifOS/README.md`
- Claude Code leak analysis: `/root/waw/skills/arifos-deploy/references/` (archived sources)
- Kernel hash: `ΔΩΨ-ARIF-888`
