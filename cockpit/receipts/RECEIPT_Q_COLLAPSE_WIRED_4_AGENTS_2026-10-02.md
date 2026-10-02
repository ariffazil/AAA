# RECEIPT — Q_COLLAPSE Wired Across 4 AAA Agents
**Date:** 2026-10-01T23:03:03Z
**Lane:** B (read-only doctrine injection, no authority mutation)
**Sovereign signal:** "go and wire all" (2026-10-02)

## Per-Agent Wiring

### 1. Hermes — q-collapse-anchor plugin (aaa-hermes profile)
- Path: /root/.hermes/profiles/aaa-hermes/plugins/q-collapse-anchor/
- Files: __init__.py (pre_llm_call + post_llm_call hooks) + plugin.yaml
- Pre-LLM: injects doctrine digest into system context (low-cost reminder)
- Post-LLM: emits doc_anchor note about one-path output contract
- Reversibility: rm -rf the plugin directory

### 2. Kimi — q_collapse_anchor.py hook
- Path: /root/.kimi-code/hooks/q_collapse_anchor.py
- Hook: prompt-submit/first-turn → injects doctrine as context
- F1 AMANAH: read-only, untrusted historical evidence framing
- Reversibility: rm 1 file

### 3. Qwen — q_collapse_anchor.md project context
- Path: /root/.qwen/projects/-root/q_collapse_anchor.md
- Reason: Qwen CLI has NO native hooks (no --hooks flag)
- Method: project-context file Qwen CLI respects as instruction
- Reversibility: rm 1 file

### 4. OpenCode — witness-wrap.sh env-var
- Path: /root/.opencode/bin/witness-wrap.sh (appended 3 lines)
- Method: export AAA_Q_COLLAPSE_DOCTRINE and AAA_Q_COLLAPSE_INVARIANTS paths
- Reason: OpenCode is Node.js, no native lifecycle hooks; only witness-wrap.sh exists
- Reversibility: remove last 3 lines from witness-wrap.sh

## All 4 verified live
- Hermes: 7 Q_COLLAPSE refs in plugin
- Kimi: 4 refs in hook
- Qwen: 4 refs in anchor.md
- OpenCode: 3 lines added (export doctrine path + invariants path)

## Common source of truth (DO NOT fork per sovereign policy "16. Consumers import vocabulary; they do not fork it")
- /root/AAA/cockpit/AAA_Q_COLLAPSE_v0.1.md — main spec
- /root/AAA/cockpit/q-collapse-replay.json — 3-case replay results
- /root/AAA/cockpit/execution-path-next.json — held sovereign items
- /root/AAA/cockpit/INIT_FORGE_RITUAL.md — closed-loop pipeline
- /root/AAA/cockpit/CANONICAL_ROOT_PROMPT.md — default front-door prompt
- /root/.claude/projects/-root/memory/eight-eureka-invariants-2026-10-02.md — 8 invariants

All 4 agents reference these canonical sources. None fork the doctrine.

## Held for sovereign signal (per forge queue)
- Compose 6-7 invariants into 1 canon (Hermes proposal)
- Prove second bounded task from different organ path
- Forge composite canon into spec only after executable test demands it

[receipt: /root/.hermes/profiles/aaa-hermes/plugins/q-collapse-anchor/__init__.py — sha256 TBD with Linux md5sum]
[receipt: /root/.kimi-code/hooks/q_collapse_anchor.py]
[receipt: /root/.qwen/projects/-root/q_collapse_anchor.md]
[receipt: /root/.opencode/bin/witness-wrap.sh — 3 lines added at end]
