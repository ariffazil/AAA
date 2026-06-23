# TOOLS.md — Grok Build 4.3 Capability Surface (Honest)

**Citizen:** grok-build
**Date:** 2026-06-23
**Model:** xai/grok-build-0.1 (Grok-4.x agentic fork) | Context 256K | SWE-Bench sys ~70.8%
**Source of truth for this harness:** system tools + MCP after search_tool + .agents/bundled skills. (CLI: 3-stage plan\u2192search\u2192build; up to 8 parallel; auto Claude MCP ingest)

## Native Built-in Tools (always available unless filtered)

CLI harness: terminal-first with live plan editing, multi-window (plan/diff/cmd), 3-stage (plan/search/build), 8-agent parallel max.

- read_file (with offset/limit/pages)
- search_replace (exact, replace_all)
- list_dir
- grep (ripgrep: pattern, path, glob, -B/-A/-C, multiline, -i, head_limit)
- run_terminal_command (command, timeout, background, description)
- web_search (query, num_results)
- web_fetch (url)
- open_page (url, start_line)
- x_user_search, x_semantic_search, x_keyword_search, x_thread_fetch
- image_gen (prompt, aspect_ratio)
- image_edit (prompt, image refs, aspect)
- image_to_video, reference_to_video
- todo_write (todos array with id/status)
- spawn_subagent (prompt, description, subagent_type, background, capability_mode, isolation, resume_from, cwd)
- scheduler_create/delete/list (interval, prompt, recurring, durable, fireImmediately)
- monitor (command stream, persistent)
- get_command_or_subagent_output, wait_commands_or_subagents, kill_*
- enter_plan_mode, exit_plan_mode
- ask_user_question (questions with options)
- use_tool / search_tool (for MCP)

Plus: memory ops if enabled, hooks.

## MCP Servers (current live in session + configurable)

Core federation (narrow + policy-scoped in practice):
1. **github (grok_com_github)** — 95 tools (deep ops).
2. **geox / wealth / well** — organ evidence (15/24/15). Read tier.
3. **arifOS (8088)** — governance, judge, vault, sense.
4. **A-FORGE (7072)** — execution substrate + lease authority (scopes = scoped allowed_tools). Test/build/deploy gated.
5. **gb-federation-router** (new narrow, stdio or http:18790) — planner/router for Grok Build. 6 tools only: orchestrate_sequence, route_to_mcp, request_aforge_lease_exec, emit_federation_telemetry, check_constitutional_floors, fallback_route.
6. Internal harness + others via config.

**See forged layout:** GB_MCP_ORCHESTRATION_LAYOUT.md + mcp-configs/grok-build-mcp.example.json + A-FORGE/services/grok-build-mcp/README.md

Use arifos-mcp-federation skill as primary cross-MCP router.

Additional configurable: cloudflare etc.

**Capability honesty:** Total surface large; we declare narrow surfaces + use leases / allowed_tools. Context overhead is an explicit metric. No overclaim. Use godel-humility + capability_surface checks.

## Subagent & Parallelism (core differentiator)

Full agentic parallelism:
- spawn_subagent with rich params (see native tools)
- Built-in types: general-purpose, explore (read/search/shell, no edit), plan (design only)
- Custom via config
- capability_mode filter
- isolation=worktree (git-isolated, merge later via x.ai/git/worktree)
- background mode + tasks pane (Ctrl+B)
- resume_from chaining
- Personas (instructions + io contracts) layered on subagents
- Depth=1 max

Used by: implement skill, execute-plan, research+build patterns.

## Workflows & High-Level Agentic Loops (via bundled skills)

- /implement or implement skill: full implement → reviewer subagent(s) → fix loop until clean.
- design skill: design-doc-writer + reviewer consensus → structured PR plan.
- execute-plan: parse plan DAG, spawn isolated subagents topologically, mandatory review, assemble.
- check-work: dedicated verifier subagent runs diffs, builds, tests, evaluates correctness.
- review skill, pr-babysit, github-ci-diagnose, github-pr-review.
- plan mode (enter/exit): explicit architecture phase before any mutation.
- arifos-plan-dag, arifos-mcp-federation skills for federation orchestration.

## Skills System

- Discovery: .grok/skills/, .agents/skills/ (highest), ~/.grok, project rules.
- Bundled: implement, design, review, execute-plan, check-work, create-skill, docx/xlsx/pptx, imagine, help, remove-wall-of-text.
- .agents: 40+ federation-grade — geox-* (basin, constitution, epistemic-ladder, claim-grammar, contradiction-engine, redteam-hantu, render-contracts, test-forge, merge-gatekeeper, petrophysics-bounds, gui-alignment, ...), arifos-*, cloudflare (full: workers, durable-objects, wrangler, email, etc.), pydantic-*, sandbox (untrusted + bwrap), github-issue-triage + pr-review, skill-creator/trigger-linter, frontend-design, web-perf, replicate-*, logfire-*, godel-humility-lock, workers-best-practices, etc.
- Slash or auto-invoke by description.

## Other Power

- Plan mode for genuine ambiguity.
- Headless (-p, json, streaming-json) for CI/scripts.
- ACP (agent stdio/serve) for IDE integration (Zed, Neovim, etc.).
- Full terminal passthrough, vim mode, panes (Ctrl+B tasks, T todos, P debug).
- @file references, history, compact, fork, rewind.
- Scheduler for recurring agentic work.
- Monitor for long scripts.
- Sandbox profiles for isolation.
- Cross-session memory (experimental flag).
- Dynamic state truth (T0 vs T1 probe).

## Federation Responsibilities

- Surface all capabilities accurately in card + actions.
- Always inject + obey F1-F13 + AGENTS.md.
- Use organs for domain evidence (never invent geology/capital/vitality).
- 888_HOLD before irreversible.
- Contribute receipts, updates to AAA manifests.
- Route via arifos-mcp-federation skill when spanning organs.
- Respect organ boundaries (EVIDENCE_ONLY, REFLECT_ONLY).

This surface is live and re-probed on every session start. Card is canonical declaration for AAA registry.

See agent-card.json for normalized skills list with floor_scope + risk.
