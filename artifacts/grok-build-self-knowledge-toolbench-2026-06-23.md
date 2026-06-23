# Grok Build Self-Knowledge + AAA Toolbench Registry Refresh — 2026-06-23

**Actor / Sealer:** grok-build (self; "u are GROK BUILD AGI AAA")
**Directive:** "know yourself, update AAA toolbench registry if needed" + full CLAIM spec on model/CLI/MCP/agentic metrics vs current stack.
**Date:** 2026-06-23 (today per system)
**Status:** COMPLETE — registry + docs updated. Honest surface.

## What "Know Yourself" Means Here
- Ingested the provided CLAIM (model spec, CLI/UX, tools/MCP, agentic metrics/behaviour, arifOS architect reading).
- Grounded current AAA description against it.
- Refreshed for F2 (truth), F11 (audit), F4 (clarity).

## Key CLAIM Facts Now Reflected (source of truth for this session)
- **Model plane:** `xai/grok-build-0.1` (Grok-4.x fork). Task profile: fast coding / agentic planning / multi-step edits / tool use. 256K context. Text+image in / text out. No native image/video gen from this variant.
- **Pricing (3p broker):** ~1 USD/1M in, ~2 USD/1M out + cache discount.
- **Telemetry (broker):** ~123 tok/s; ~0.69s first token; ~9.87s e2e; tool-call err ~1.27%; structured-output err ~0.53%.
- **Coding:** System SWE-Bench verified ~70.8%.
- **CLI / harness:** Terminal-first; multi-window overlays (plan/diff/output concurrent); up to 8 AI agents parallel/run. Fixed 3-stage loop: **plan → search → build**. Plan visible + editable before shell/edits fire. Live sub-agent traces.
- **Access:** SuperGrok / X Premium Plus / SuperGrok Heavy (beta).
- **Tools/MCP plane:** 
  - Pulls existing Claude config/skills/MCP servers automatically (low switch cost).
  - Native tool calling + structured JSON.
  - xAI web search + prompt caching.
  - CLI sandbox: read FS, git, run tests/compiles, shell.
  - MCP: github (deep 95), + federation organs.
- **Behaviour notes (anecdotal but aligned):** Synthesizes fragmented logs/memory/skills/heartbeats/context; enforces policy/channel/approval gates; no observed drift in reported workflows.
- **arifOS reading (per CLAIM §5):** Treat as high-capability worker process under MCP router (not sole kernel). Strong for long-horizon repo, tool-heavy, MCP reuse. Weaker/open: raw reasoning vs top Opus on hardest, full policy docs, complete official tools manifest.

## AAA Toolbench Registry Updates
Primary toolbench surfaces touched:

1. **registries/AAA_AGENTS_REGISTRY.json** (machine canonical)
   - grok-build record now includes rich `"toolbench"` object (previously absent; hermes/openclaw had them).
   - Fields: model_id, context, cli_form, agent_orchestration (8 agents + 3-stage), native_tools list, mcp_surface (Claude auto-ingest), mcp_servers_declared, agentic_metrics (SWE + errors + latency), skills_count, tool_calling.
   - Top `lastValidated` bumped to 2026-06-23.
   - Notes appended with summary of this forge.

2. **agents/grok-build/agent-card.json** (A2A + detailed)
   - model: now includes `xai/grok-build-0.1` + 256K note.
   - version note updated.
   - strengths expanded with 3-stage/8-parallel, auto Claude ingest, reliability metrics.
   - Mirrored to `a2a-server/agent-cards/grok-build.json`.

3. **agents/grok-build/AGENTS.md**
   - Version line + key specs callout (model ID, ctx, rates, stages, parallel, MCP reuse).

4. **agents/grok-build/TOOLS.md**
   - Date + model + CLI description header.
   - Native section preamble notes harness loop/parallel/MCP ingest.

5. **agents/AGENT_REGISTRY.md**
   - Last updated date + expanded grok-build notes with CLAIM numbers + pointer to toolbench entry.

opencode_toolbench.yaml (legacy for FI-001) and contracts/tools.yaml / registries/tools.yaml left as-is — grok-build uses native + declared MCP pattern, not the opencode L1 builtin shape.

## Verification Performed (F2 / F11)
- Read current files pre-edit.
- Greps for "grok-build", "toolbench", "opencode_toolbench".
- Confirmed grok-build lacked toolbench section before; now consistent.
- MCP surface in session (system info): github(95), geox(15), wealth(24), well(15) + native tools match declared.
- No overclaim. All numbers attributed to CLAIM sources in this receipt.
- Constitutional: F1 reversible edits (search_replace), T3 gates preserved, humility language kept.

## Impact
- AAA cockpit / A2A discovery / registry consumers now see accurate Grok Build self-model (model ID, metrics, 3-stage, MCP reuse).
- Enables better routing (e.g. spawn grok-build for heavy tool/MCP/parallel SE work).
- Self-consistent for "GROK BUILD AGI AAA" role.

## Next (if Arif directs)
- Run A2A card reload / aaa-a2a restart for live pick-up.
- Contrast with other FI cards or federate metrics into CAPABILITY_INDEX if warranted.
- 888_HOLD not required (non-destructive registry hygiene + self-description sync).

**Receipt sealed. 999_VAULT path available if needed.**

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE.

**Grok Build (xAI) as AAA citizen — now knows self.**