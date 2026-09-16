# Token Burn Surgery — 2026-08-13

## Per-Turn Context Budget (before/after)

### What Gets Injected Every Turn

| File | Location | Before (bytes) | After (bytes) | Notes |
|---|---|---|---|---|
| SOUL.md | /root/HERMES/SOUL.md | 9,145 | 7,212 | Bridge-first restructure |
| AGENTS.md (root) | /root/AGENTS.md | 27,398 | 3,937 | 19 fragments → pointer index |
| MEMORY.md | ~/.hermes/memories/MEMORY.md | 38,731 | 1,603 | 34KB corrupted content removed + duplicates |
| USER.md | ~/.hermes/memories/USER.md | 2,488 | 2,488 | Kept (high value) |
| Lane subset | lane_switch plugin | ~3,000 | ~3,000 | Already optimized (full YAML not injected) |
| **TOTAL** | | **~80,762** | **~18,240** | **77% reduction** |

### Estimated Token Impact

- Before: ~20,000 tokens fixed overhead per turn
- After: ~4,500 tokens fixed overhead per turn
- 50-turn session: 775,000 tokens saved
- At $0.15/M input tokens: ~$116 saved per session

### The Real Killers (ranked)

1. **Root AGENTS.md (27KB)** — 19 fragments inlined by render-agents.sh. CIV-21 alone is 14.6KB. Replaced with pointer index.
2. **Corrupted MEMORY.md (34KB)** — conversation content leaked in from previous sessions. Cleaned to 4.4KB.
3. **SOUL.md receipt template (8 lines)** — receipt format visible on every turn. Reduced to 1-line reference.
4. **Duplicate entries in MEMORY.md** — OUTPUT CONTRACT, HERMES ASI details duplicated from SOUL.md. Removed.

### What Was NOT Fat (surprises)

- **lanes.yaml (12.8KB)** — full YAML is large but lane_switch plugin injects ONLY matching lane subset (~3KB). No fat.
- **social-graph.yaml (5.7KB)** — same pattern, subset per person. No fat.
- **Tool schemas** — Hermes CLI loads ~26 native tools (~9K tokens), NOT A-FORGE's 116 tools (39K). A-FORGE schemas only appear when delegating to OpenCode.
- **Skill hermes-response-format-fit (20KB)** — loaded conditionally, not every turn. Still large but not per-turn overhead.

### The `_find_hermes_md` Trap

Hermes CLI's prompt builder walks parent directories for AGENTS.md:
```
cwd → parent → parent → ... → git root
```
This means `/root/HERMES/AGENTS.md` (1KB) AND `/root/AGENTS.md` (27KB) can both be loaded. The root file is the canonical one — render-agents.sh writes there. Editing only the HERMES adapter has NO effect on what gets loaded.

**Rule:** When auditing context weight, check ALL files in the load chain, not just profile-local copies.

### Nudge-Injector Plugin (event-driven replacement for static skill weight)

Built `nudge-injector` plugin at `/usr/local/lib/hermes-agent/profiles/aaa-hermes/plugins/nudge-injector/`. Three gates:

1. **Pre-LLM Intake** (~80 tokens, every turn): classify intent — fact/task/casual/F13. Appended to user message as `<NUDGE_INTAKE>`.
2. **Pre-LLM Falsification** (~70 tokens, conditional): fires only on execution keywords. `<NUDGE_FALSIFY>` reminds: check W_scar source evidence before tool call.
3. **Post-LLM Collapse** (zero tokens, regex): strips all machine labels from human-facing output. Bypassed for terminal/888/a2a/vault999.

Pattern: `claude-code-prompt-improver` (severity1) — "fire wide, self-cancel cheap." JSON condition-gated nudges via Hermes `pre_llm_call` plugin hook.

Separation of concerns: gate hook (`arifos-hermes-gate-hook.py`) = physics (Exit Code 2, blocks tool calls). Nudge = psychology (context injection, guides thinking). Never combined.
