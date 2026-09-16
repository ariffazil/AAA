# RFC F1-MCP-Governance-Wrapper — Decisions Summary

> Sealed: 2026-08-28 by 888 Sovereign (Arif Fazil)

## Locked Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Interceptor Language: **Rust** | Memory safety, zero GC pause, zero overhead, small binary. |
| 2 | Policy Format: **TOML** | Superior readability for hand-audit. YAML rejected (ambiguous). |
| 3 | DEV_KEY Scope: **impact_radius ≤ 1 AND is_reversible = true ONLY** | Zero delegation for mutation ops. |
| 4 | Domain Expansion: **Pilot FED + GEOX first** | 1-week clean audit → expand to WEALTH, WELL, media. |
| 5 | Hermes Integration: **UDS Proxy Shim** | Interceptor below Hermes execution layer. Silent filtering. |

## Architecture

```
LLM (max 5 tools) → MCP Reversibility Wrapper → Deterministic Interceptor (Rust) → MCP Servers
                    ↑ Intent Router (deterministic, zero-LLM)
```

## Phase Roadmap

- Phase 1 (Week 1): Policy schema + audit chain
- Phase 2 (Week 2): MCP Reversibility Wrapper
- Phase 3 (Week 3): Deterministic Interceptor (Rust binary)
- Phase 4 (Week 3-4): Zero-LLM Intent Router
- Phase 5 (Week 4): Per-Agent Role ACL
- Phase 6 (Week 5): Constitutional integration

## Full RFC

`/root/AAA/governance/RFC-F1-MCP-Governance-Wrapper.md`

## Crate

`/root/AAA/mcp-governance-interceptor/` (652 lines, 8 source files, Rust)
