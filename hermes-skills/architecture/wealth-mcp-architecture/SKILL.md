---
name: wealth-mcp-architecture
description: WEALTH MCP physics-inspired redesign — 50 tools to 32 atomic tools + 8 prompts + 20+ resources. Tool/prompt/resource primitive allocation for capital intelligence MCP servers.
trigger: WEALTH MCP tool count or WEALTH refactor or MCP primitives tools prompts resources
category: architecture
tags: [mcp, fastmcp, wealth, capital-intelligence, physics-economics]
---

# WEALTH MCP — Architecture Blueprint

**DITEMPA BUKAN DIBERI — Forged, Not Given**

## The Core Problem

WEALTH MCP exposes 50 tools via @mcp.tool() decorators — everything dumped as tools: atomic calculators, orchestration wrappers, reasoning workflows, and duplicate aliases. MCP has 3 primitives:

| Primitive | Purpose | Should contain |
|---|---|---|
| tool | Atomic actions/computations | Calculate, validate, fetch, write |
| prompt | Reasoning templates | Orchestration rituals, multi-step judgments |
| resource | Readable knowledge/state | Schemas, formulas, policies, ontology |

## Physics-Inspired Naming Convention

```
wealth_<dimension>_<operation>
```

- wealth = MCP namespace
- dimension = physics-inspired abstraction
- operation = economic action

## Complete Rename Table

See the full blueprint at: /root/WEALTH/docs/WEALTH_MCP_ARCHITECTURE.md

## Count Summary

| Category | Before | After |
|---|---|---|
| Tools | 50 | 32 |
| Prompts | 0 | 8 |
| Resources | 7 | 20+ |

## Implementation

Phase 1 (low risk): Rename V2_CANONICAL_MAP keys only
Phase 2 (medium risk): Demote umbrella tools to prompts
Phase 3 (low risk): Register resources
Phase 4: Deploy + verify initialize handshake
