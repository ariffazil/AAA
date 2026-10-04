# Agent → Memory Wiring Map (2026-08-09)

Session: Arif asked *"Is my Hermes agent and other agent wired to the double helix memory?"* — answered by probing every harness's live config (no skill loaded; pure read-only recon).

## The two artifacts named "double helix"

1. **Memory double helix** = the two axes in `/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md` (sealed 2026-08-08):
   - **L-axis (L0–L6)** — agent operational memory, classified by function: Redis (L1/L2), Qdrant (L3), Supabase (L4), FalkorDB/Graphiti (L5), VAULT999 (L6).
   - **H-axis (H1–H6)** — human survival memory, classified by survival value: H1 Capture → H2 Experience → H3 Knowledge → H4 Identity → H5 Scars → H6 Constitution.
   - Constitutional boundary: the federation may **reference** H-axis, never **own** it. H5 scars read only on explicit `scar:<id>` invocation. No vectorization/embedding of scars without F13 keyword.
   - Doctrine's H↔L mapping: H1↔L1–L2 Redis+Conversation↔**HERMES** (sovereignty gate at ingestion) · H2↔L2 Session+L6 Receipts↔**A-FORGE** · H3↔L3 Qdrant+L4 Supabase↔**GEOX/WEALTH** · H4↔L4 agent cards↔**AAA** · H5↔L6 VAULT999↔**arifOS+WELL** · H6↔L6↔**arifOS**.

2. **Governance reflection** = `/root/forge_work/DOUBLE_HELIX_2026-08-08.md`: Floors (identity strand) + Flow (metabolism strand), Laws as hydrogen bonds, VAULT999 = currency exchange between inner (intelligence) and outer (civilization) loops. Header says pointer-only, NOT a floor/law/GENESIS. **Not a memory architecture** — don't answer memory questions from it.

## Per-harness config map (probed 2026-08-09)

### Hermes — L wired + H reference
- Config: `/root/.hermes/config.yaml` (1472 lines). Relevant blocks: `memory:` (memory_enabled: true, provider: **honcho**, char limits), `mcp_servers:` (arifos :8088, aforge :7072, fed :7074, geox :8081, wealth :18082, well :18083, hermes :18901, github, minimax, hound, mage, notebooklm, deep-research disabled).
- H-axis: `notebooklm` MCP description literally says *"Use for /root/memory/H5-scars and any sovereign memory that needs cited lineage."*
- **Trap:** active profile dir `~/.hermes/profiles/aaa-hermes/` holds memories/ + skills/ + hooks/ but **no config.yaml** — profile-level config lives in the main config. (aaa-hermes memories: lane-syed.json, SOUL-syed.md, USER-syed.md, MEMORY-syed.md.)

### Claude Code — L wired + H reference
- Config: `/root/.claude/settings.json` — the `permissions.allow` list IS the wiring manifest: `mcp__arifos__arif_init/observe/think/route/compose/memory/judge/forge/seal`, `mcp__memory__*`, `mcp__postgres__*`, `mcp__graphiti-mcp__*`, `mcp__geox__*`, `mcp__wealth__*`, `mcp__well__*`, `mcp__aforge__*` (incl. forge_vault).
- Agent card: `/root/AAA/registries/agents.yaml` → `claude-code` entry, `mcp_surface:` lists 20 servers (a-forge, arifOS, brave-search, chrome-devtools, docker, exa, filesystem, geox, git, memory, meyhem, minimax-coding-plan, playwright, postgres, sequential-thinking, supabase, tavily, time, wealth, well).

### Kimi FI-008 — L wired
- Config: `/root/.arifos/agents/kimi/config.toml`. MCP authoritative list = `/root/.kimi-code/mcp.json` (**8 servers as of 2026-08-07** — don't enumerate from prose, read mcp.json). Own memory: `/root/.arifos/agents/kimi/state.db`. extra_skill_dirs = AAA skills + ~/.agents/skills.

### OpenCode — partial
- Config: `.opencode.json` (project root or `~/.config/opencode/`). `mcp:` block: `arifOS-Kernel` (local, `arifosmcp.runtime` stdio) **enabled**; `arifOS-Intelligence`, `arifOS-Public`, `arifOS-WELL`, `arifOS-WEALTH` often **enabled: false**. Context7 enabled. Also carries `arifOS_contract` with floors_enforced.
- §4c of SKILL.md already covers the model-alias bug class for opencode.json.

### OpenClaw — NOT wired at store level (the gap)
- Runtime config: `/root/arifOS/config/openclaw/openclaw.json` — top keys: meta/logging/agents/tools/commands/session/channels/gateway. **0 hits** for mcp/memory/vault/plugin/redis/qdrant. Tools block only (profile/elevated/exec/fs).
- Memory = file-based: `/root/.openclaw/workspace/MEMORY.md` (+ .bak-driftguard-2026-08-06 snapshots), `/root/.openclaw/workspace/hermes-memories/MEMORY.md`, `/root/.openclaw/media/MEMORY.md`.
- Agents dir: `/root/.openclaw/agents/{333-agi,claude,codex,kimi,main,opencode}/`; extensions: art-governor, governed-tool-gate.
- Wired at **doctrine level only** (workspace AGENTS.md → /root/AGENTS.md pointers). Per EMD 2026-08-08, OpenClaw = SENSE/observational lane — the gap may be intentional.

## Verdict table delivered

| Agent | L-axis | H-axis |
|---|---|---|
| Hermes | ✅ full (arif_memory, forge_vault, honcho) | ✅ read-only ref (notebooklm→H5-scars) |
| Claude Code | ✅ full (arif_memory, memory, postgres, graphiti, aforge) | 🟡 ref via AGENTS.md + filesystem |
| Kimi | ✅ good (8 MCP + state.db) | 🟡 doctrine pointers |
| OpenCode | 🟡 partial (kernel only) | 🟡 AGENTS.md overlay |
| OpenClaw | ❌ none (file-based own memory) | ❌ |

## Next step offered (not executed)
Wire OpenClaw via arifos MCP (T2: snapshot config → add server → restart → rollback ready) — or leave as-is since SENSE lane may not need store memory. Arif hadn't answered at session end.

## Reusable probe technique
```bash
# For any harness, the wiring signal is: does its config name a memory store?
for f in /root/.hermes/config.yaml /root/.claude/settings.json \
         /root/.arifos/agents/kimi/config.toml /root/arifOS/config/openclaw/openclaw.json; do
  echo "== $f"; grep -ioE 'arif_memory|forge_vault|graphiti|postgres|redis|qdrant|vault|notebooklm|memory' "$f" | sort | uniq -c | sort -rn | head -5
done
```
Zero hits + a workspace file (`MEMORY.md`) = doctrine-wired, store-unwired (OpenClaw pattern).
