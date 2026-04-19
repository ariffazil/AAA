# OpenClaw Plane

This directory makes OpenClaw a **first-class runtime target** inside AAA.

Rule:

- **AAA authors**
- **OpenClaw consumes**
- **runtime state must round-trip back into AAA inventory**

OpenClaw is the main agentic runtime.
AAA is therefore the **workspace authority** for every OpenClaw-relevant contract:

- agents and bindings
- gateway and channel policy
- ACP host adapters
- MCP catalogs
- plugin policy and pinning
- A2A metadata
- exported runtime bundles

## Canonical shape

```text
openclaw/
├─ agents/      # agent definitions and runtime bindings
├─ gateway/     # gateway, channels, model/provider, security policy
├─ acp/         # ACP host adapters and session templates
├─ mcp/         # MCP runtime catalogs and manifests
├─ plugins/     # approved plugins, pins, marketplace sources
├─ a2a/         # agent cards and discovery metadata
├─ channels/    # message routing and authorization policy
└─ exports/     # generated artifacts consumed by OpenClaw runtime
```

Not all subdirectories exist yet. This file freezes the intended plane.

## Authoring rule

If OpenClaw can:

- run it
- install it
- route to it
- expose it
- emit events about it

then AAA must be able to:

- describe it
- inventory it
- policy-gate it
- export it
- audit it

## Runtime rule

OpenClaw should run from **AAA-derived state**, not hand-edited local drift.

That means:

- YAML source contracts live in AAA
- JSON artifacts are exported from AAA
- runtime inspection should be diffed against AAA desired state
- drift should fail closed for high-risk changes
