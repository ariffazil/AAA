---
id: mcp-smoke-test
name: FORGE-mcp-smoke-test
version: 1.0.0
description: Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.
owner: AAA
risk_tier: low
host_compatibility:
  - claude-code
  - codex
  - opencode
  - kimi
  - kimi-code
version_lock: pending
trinitarian:
  - Ω
functional_tags:
  - Ops
  - Audit
layer: RUNTIME
autonomy_tier: T1
floor_scope:
  - F2
  - F4
  - F11
---

# MCP Server Smoke Test

Validate that MCP servers respond correctly to health probes and basic tool calls. Detect down servers, mismatched schemas, and transport errors.

## Usage

Run smoke tests against all federation MCP endpoints to verify liveness and schema compliance.

## Targets

- arifOS :8088
- A-FORGE :7071
- GEOX :8081
- WEALTH :18082
- WELL :18083
