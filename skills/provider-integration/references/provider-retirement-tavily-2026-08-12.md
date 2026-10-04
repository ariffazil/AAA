# Provider Retirement — Tavily Cleanup (2026-08-12)

## Context

Tavily dev plan exhausted (HTTP 432 quota). Sovereign replacement = SearXNG (:8080, self-hosted, $0).
Session task: clean up all Tavily references across the federation.

## Discovery sweep results

| # | Location | Type | Action taken |
|---|---|---|---|
| 1 | `/root/.hermes/skills/devops/deep-research-deployment/SKILL.md` line 92 | Provider table | Marked retired (strikethrough + RETIRED tag) |
| 2 | `/root/HERMES/skills/devops/external-mcp-integration/references/deep-research.md` line 85 | Enum value list | Annotated: `(~~tavily~~ retired 2026-08-12)` |
| 3 | `/root/arifOS/arifosmcp/runtime/tavily_bridge.py` | Active code module | LEFT — arifOS internal, not in active runtime path for Hermes search |
| 4 | `/root/arifOS/tests/runtime/test_tavily_bridge.py` | Test file | LEFT — tests for arifOS internal module |
| 5 | `/root/hermes-agent-dev/plugins/web/tavily/` | Plugin source | LEFT — Hermes upstream plugin, not installed in active profile |
| 6 | VAULT999 historical receipts | Immutable truth | **NEVER touched** |

## Key findings

1. **30 files matched `tavily` across `/root`** — but only 3 were in active Hermes skill/doc paths. The rest were arifOS internals, upstream plugin source, archived backups, and test fixtures.
2. **No live runtime processes** reference Tavily. `ps auxw | grep tavily` → empty.
3. **No active env config** — `TAVILY_API_KEY` not in `kunci-mas.env` golden vault.
4. **No litellm routing** — Tavily was never a litellm model_list entry; it was a search backend, not an LLM provider.
5. **No cron job references** — `jobs.json` clean.

## The marking convention applied

### Provider table (SKILL.md)
```
| ~~Tavily~~ | ~~`TAVILY_API_KEY`~~ | **RETIRED 2026-08-12** — dev plan exhausted (HTTP 432). SearXNG is sovereign primary. |
```

### Enum value list (reference doc)
```
| `MCP_SEARCH_PROVIDER` | Search backend for MCP mode | `searxng`, `model`, `brave` (~~tavily~~ retired 2026-08-12) |
```

## What was NOT touched and why

- **arifOS internal modules** (`tavily_bridge.py`, tests): These are arifOS kernel internals, not Hermes skill territory. If arifOS retires them, it's a separate code mutation through A-FORGE.
- **Hermes upstream plugin source** (`/root/hermes-agent-dev/plugins/web/tavily/`): This is the Nous Research upstream codebase, not the active Hermes profile. Editing upstream fork code is out of scope for a skill cleanup.
- **VAULT999 receipts**: Immutable historical evidence. The fact that Tavily was once used is sealed truth.

## Sovereign replacement verification

```bash
curl -sf http://127.0.0.1:8080/healthz
# → 200 (0.004748s)
```

SearXNG confirmed as sovereign primary search backbone. Web search fallback chain:
SearXNG (primary) → Brave → MiniMax → DDG (last resort).

## Generalization

This pattern applies to ANY provider retirement:
1. Sweep all surfaces (secrets, configs, skills, docs, cron, runtime processes)
2. Classify each hit (active config vs reference doc vs enum vs immutable)
3. Mark retired entries with strikethrough + date + reason + replacement
4. Leave reference docs describing option space untouched (they educate, not configure)
5. Leave historical receipts untouched (immutable truth)
6. Verify sovereign replacement is healthy
7. Verify no live runtime references remain
