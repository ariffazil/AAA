# arifOS `/tools/list` endpoint quirk — verified 2026-08-06

## The bug shape

`curl http://127.0.0.1:8088/tools/list` returns:

```
Method Not Allowed
```

with HTTP 405. The route is not registered at that path on arifOS kernel. The sibling/script that probed it would naturally conclude the kernel exposes no tools — a wrong conclusion that masks federation health.

## The right paths

Three routes return the tools list (verified working 2026-08-06):

| Path | Content | Notes |
|---|---|---|
| `GET /tools` | Full JSON tool schema list | Primary route; returns `service`, `tools[]`, `count`, `version`, `release_name`, `git_commit`, `source_of_truth` |
| `GET /tools.json` | Same as `/tools` | Alternate route |
| `GET /tools/list` | **405 Method Not Allowed** | Do NOT use |

The kernel's own `source_of_truth` field in the response states:

```
"source_of_truth": "public_tool_names() == tools/list == /tools == /tools.json"
```

So `tools/list` is referenced as a canonical name in the kernel's source of truth, but the HTTP route exposes it under `/tools` (and `/tools.json`). Confusing — the route name and the canonical name disagree.

## What `/tools` returns

A JSON object like:

```json
{
  "service": "ARIFOS MCP",
  "tools": [
    {
      "name": "arif_init",
      "canonical": "arif_init",
      "description": "KERNEL 000 · Session ignition...",
      "stage": "000",
      "lane": "AGI",
      "access": "public",
      "inputSchema": {...},
      "outputSchema": {...}
    },
    ... 7 more kernel tools (arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal)
  ],
  "count": 8,
  "version": "kanon-f2aee35",
  "release_name": "v2026.08.01",
  "git_commit": "f2aee35",
  "source_of_truth": "public_tool_names() == tools/list == /tools == /tools.json"
}
```

Useful fields for audit:
- `count` — should match `len(tools)`; if mismatch, malformed response
- `version` / `git_commit` — kernel version fingerprint for drift detection
- `access` — `public`, `internal_only`, `authenticated` (corresponds to F1 AMANAH bands)
- `lane` — `AGI`, `ASI`, `APEX` (agent lane classification)

## Recipe (no piping to avoid tirith flag)

```bash
# Save first
curl -s http://127.0.0.1:8088/tools > /tmp/arifos-tools.json

# Then parse
python3 -c "
import json
d = json.load(open('/tmp/arifos-tools.json'))
print(f\"count={d['count']} version={d.get('version')} commit={d.get('git_commit')}\")
print('Tools:')
for t in d.get('tools', []):
    print(f\"  {t['name']:20s} stage={t.get('stage','?'):6s} lane={t.get('lane','?'):5s} access={t.get('access','?')}\")
"
```

## Probe for fabricated tool families

When a sibling or subagent report describes a tool family that should exist, grep the tools list:

```bash
# Example: verify "megamemory_*" tools claimed by a sibling
python3 -c "
import json
d = json.load(open('/tmp/arifos-tools.json'))
matches = [t['name'] for t in d.get('tools',[]) if 'megamemory' in t['name'].lower()]
print(f'megamemory matches: {len(matches)}', matches if matches else 'NONE — fabrication confirmed')
"
```

If `0 matches`, the tool family is fabricated. Verified 2026-08-06: a sibling report claimed `megamemory_understand`, `megamemory_create_concept`, `megamemory_link` exist as OpenCode tools — none of them exist in the arifOS `/tools` response, nor in A-FORGE's `/tools` response, nor anywhere in `/root/arifOS/arifosmcp/`. The only `megamemory` mention in any skill/codebase is a regex in a deny-list (`/root/HERMES/skills/devops/vps-operations/SKILL.md`).

## Wider lesson — what's actually in arifOS tools

The 8 canonical arifOS kernel tools (verified live 2026-08-06):

| Tool | Stage | Lane | Access |
|---|---|---|---|
| `arif_init` | 000 | AGI | public |
| `arif_observe` | 111 | AGI | public |
| `arif_think` | 333 | AGI | public |
| `arif_route` | 555 | AGI | public |
| `arif_memory` | 555m | AGI | internal_only |
| `arif_judge` | 888 | ASI | authenticated |
| `arif_forge` | 010 | AGI | internal_only |
| `arif_seal` | 999 | APEX | authenticated |

**No `megamemory_*`, no `atlas_*` as a separate tool, no `eureka_*` as a separate tool.** ATLAS333 and EUREKA777 live as:
- ATLAS333: `arifos://atlas333/*` MCP resources (read-only knowledge map) + `arif_observe(mode='atlas')` mode + `arif_think(mode='atlas')` mode (latter is NOT in the live `/tools` schemas — `arif_think` modes are `reason | reflect | verify | axioms | plan | plan_review | plan_approve | refactor_plan | metabolize | simulate | wonder | atlas` per the registry JSON, but the `arif_think` schema in `/tools` only declares `mode: 'reason'` as the default — the registry JSON is the more complete source)
- EUREKA777: a cognition pattern documented in `/root/arifOS/okf/eureka777/` and `/root/arifOS/GENESIS/059_FQ_SEAL_GAUGE_AMC.md`, not an exposed tool

If a report describes ATLAS333 / EUREKA777 as MCP-callable tools with their own `tools/list` entries, that's wrong — they're either resources (`arifos://atlas333/*`) or kernel modes (`arif_observe(mode='atlas')`, `arif_think(mode='atlas')`), not standalone tools.

## Pitfalls

- **`/tools/list` returns 405 — the route does not exist despite the field name `source_of_truth` claiming it does.** Use `/tools` (no trailing `.list`) or `/tools.json`.
- **Don't pipe `curl | python3` directly** — tirith flags schemeless URLs to pipe-to-interpreter. Save to `/tmp/` first, then parse.
- **Mode names in `/tools` schemas vs mode names in `arifosmcp/schemas/arifos_tool_registry.json` can diverge.** The schemas show the minimum surface area exposed by FastMCP; the registry JSON is the full internal mode set. When verifying "does mode X exist on tool Y", grep both. E.g. `arif_think` schema says `default: "reason"`; registry JSON lists `reason | reflect | verify | axioms | plan | plan_review | plan_approve | refactor_plan | metabolize | simulate | wonder | atlas`. The exposed surface (what an MCP client can actually invoke) is the schema's enum, not the registry.
- **Siblings fabricating tool families is a recurring pattern** — when a report describes a tool family with believable prefixes (`megamemory_*`, `atlas_*`, `eureka_*`, `forge_*`) that don't appear in `/tools`, it's a fabrication. The 8 canonical kernel tools above are exhaustive.