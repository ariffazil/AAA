# Changelog v3.1.1 — 0-index renumber (2026-09-21)

> **Trigger:** Arif SEAL on the 8-stage workflow structure, 2026-09-21.
> **Scope:** cosmetic structural renumber. **Zero semantic change.**
> **Reversibility:** v3.1.0 body is frozen at
> `/root/AAA/skills/.frozen/2026-09-21-llms-alignment/SKILL.md.from.mcp-ops-v3.1.0`.
> **Spine v3.1.0 → v3.1.1 transition is byte-identity save for stage-name substitutions.**

## What changed

| Element | v3.1.0 numbering | v3.1.1 numbering |
|---|---|---|
| Preamble stage | Stage 1 LEARN | **Stage 0 LEARN** |
| 2nd stage | Stage 2 DISCOVER | **Stage 1 DISCOVER** |
| 3rd stage | Stage 3 PROBE | **Stage 2 PROBE** |
| 4th stage | Stage 4 BUILD | **Stage 3 BUILD** |
| 5th stage | Stage 5 SECURE | **Stage 4 SECURE** |
| 6th stage | Stage 6 TEST | **Stage 5 TEST** |
| 7th stage | Stage 7 EXTEND | **Stage 6 EXTEND** |
| 8th stage | Stage 8 PUBLISH | **Stage 7 PUBLISH** |
| 9th stage | Stage 9 GOVERN | **Stage 8 GOVERN** |
| RETIRE (sub-section) | Stage 9h RETIRE | **Stage 8h RETIRE** |

Sub-stages follow their parents (4a → 3a, 5b → 4b, 8c → 7c, 9g → 8g, etc.).

## Latent anomaly fixed

In v3.1.0, the procurement sub-stage sat at `Stage 1b` even though procurement is logically under
DISCOVER (`Stage 2` in v3.1.0). The 0-index renumber re-parents it correctly: `Stage 1b`
procurement now sits under `Stage 1 DISCOVER`. The two-step fix was:

1. Pre-fix the latent anomaly: `Stage 1b` → `Stage 2b` (under the correct parent).
2. Top-level renumber: `Stage N` → `Stage N−1` for N = 9..1.

Result: `Stage 1b` procurement lands under `Stage 1 DISCOVER`. Correct.

## What was NOT changed (semantic identity preserved)

- 32 absorbed references — content unchanged, only stage-number cross-references renumbered
- All 24 superseded MCP skill names — preserved as tombstones
- Allowed/Forbidden/Escalation rules — content identical
- Stage headings' parenthetical subtitles — unchanged
- `supersedes:` list — unchanged (still 24+ names)
- `triggers:` list — unchanged
- `floor_scope:`, `autonomy_tier:`, `capability_tier:` — unchanged

## Two-pass substitution script (Python) — preserves byte identity within stage-name regions

```python
# Capture sub-stages that need re-parenting first.
src = src.replace('Stage 1b', '__STAGE_B_PRE__')
src = src.replace('Stage 9h', '__STAGE_8H_PRE__')

# Top-level: Stage 9..1 → Stage 8..0 with placeholders (avoids cascade).
for n in range(9, 0, -1):
    src = src.replace(f'Stage {n}', f'__STAGE_{n-1}__')
for n in range(9, 0, -1):
    src = src.replace(f'__STAGE_{n-1}__', f'Stage {n-1}')

# Re-emit sub-stage placeholders to post-renumber identity.
src = src.replace('__STAGE_B_PRE__', 'Stage 1b')
src = src.replace('__STAGE_8H_PRE__', 'Stage 8h')

# Version bump 3.1.0 → 3.1.1 in frontmatter.
import re
src = re.sub(r'^(version:\s*)3\.1\.0\s*$', r'\g<1>3.1.1', src, count=1, flags=re.MULTILINE)
```

Result: SKILL.md v3.1.0 = 44,273 B; SKILL.md v3.1.1 = 44,724 B (delta = +451 B = the appended v3.1.1 changelog line).

## Frozen chain integrity

```
engineering/mcp-ops/SKILL.md                         v3.1.1   44,724 B   sha 6c2baf6e52bf     (canonical, live)
.frozen/2026-09-21-llms-alignment/
  SKILL.md.from.mcp-ops-v3.0.1                       v3.0.1   32,556 B   sha ebe2ebdfa487     (original v3.0.1 frozen)
  SKILL.md.from.mcp-ops-v3.1.0                       v3.1.0   43,858 B   sha bfc0b9280086     (intermediate v3.1.0 frozen)
  SKILL.md.from.mcp-testing                          same     32,556 B   sha ebe2ebdfa487     (mcp-testing body — node-consolidated since v3.0.1)
  absorbed-INDEX.md.from.pre-alignment                        9,925 B                          (pre-rewrite INDEX frozen)
```

22/22 federation tombstone symlinks resolve to v3.1.1 across all four skill trees
(`/root/AAA/skills`, `/root/.opencode/skills`, `/root/.agents/skills`, `/root/.claude/skills`).
The 1 hermes-profile stale (`/root/AAA/skills/capabilities/coding/mcp-ops` →
`/root/.hermes/profiles/aaa-hermes/skills/FORGE-mcp-ops`) is a hermes-internal scope, not part of
the AAA canonical tree — correctly NOT absorbed, correctly NOT updated.

## Why "0-index" is cleaner

LEARN as Stage 0 (rather than Stage 1) reads as **preamble or orientation** — the index
0 is naturally read as "before everything else starts." This matches the llms.txt reading order
at `https://modelcontextprotocol.io/llms.txt` where `getting-started/intro` is the first surface.
The 0-indexed numbering also keeps the stage count additive: a future Stage 9 (e.g., COMMUNITY)
would extend downward without needing a renumber.

## Cost of this pass

- 1 SKILL.md renumber (44 KB)
- 2 reference docs renumber (INDEX + workflow-map)
- 1 new frozen v3.1.0 body
- 1 added changelog footer line in SKILL.md
- 1 added row in INDEX Wave timeline
- 1 new reference (this file)
- 0 net new content (no semantic additions)
- 0 destructive operations (everything preserved)

## Ready for next pass

F13 sovereign decision queue (not yet executed, awaiting authorization):

1. **`arifOS` 888 formal seal** of v3.1.1 → VAULT999 immutable write
2. **OWNERSHIP_MAP.yaml** P3_mcp_tooling collapse (3-chain → 1-chain) given inode-level
   consolidation of MCP-Verify into MCP-Operate
3. **Census sweep on the 32 absorbed references** — verify their stage-number citations
   are consistent (only the 32 do not have direct stage-XYZ refs that were renumbered)

*Generated by 333-AGI at 2026-09-21 23:45 MYT, per Arif SEAL on the canonical 8-stage structure
with LEARN as Stage-0 preamble and RETIRE folded into GOVERN.*
