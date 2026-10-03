---
name: skills-cold-storage-ops
description: Thaw or freeze skills. Use when a skill is missing.
version: 1.0.0
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Skills Cold Storage Ops

## When to Use

- A skill/slash command is missing or fails to load → it may be in cold storage; thaw it.
- User asks to freeze/clean/prune skills, or "where did skill X go".
- Monthly zen maintenance (freeze untouched >60d).

## The System (forged 2026-08-24, F13 green-light)

- LIVE index: `/root/.hermes/skills/` — ~179 skills, ~23K tokens of frontmatter per session.
- COLD storage: `/root/.hermes/skills-cold/` — 328+ skills, mv only (never rm), reversible.
- Receipts: `/root/.hermes/backups/zen-20260824T180658Z/` (move_receipt.json, cold_list.json, full_inventory.json, symlink_map.json, config.yaml.bak). `THAW_MANIFEST.json` in skills-cold root.
- MCP filters: `mcp_servers.*.tools.include` in config.yaml — aforge 21, well 5, firecrawl 4; github/hermes/notebooklm/deep-research/hound/openrouter disabled (0 calls/90d). Thaw = remove filter or enabled:true + `/reload_mcp`.

## Procedure

### Thaw
1. `find /root/.hermes/skills-cold -maxdepth 3 -name SKILL.md | grep -i <term>`
2. `mv /root/.hermes/skills-cold/<rel> /root/.hermes/skills/<rel>`
3. `/reload_skills` (no gateway restart)
4. Organ-linked entry (target under /root/AAA, /root/WELL, /root/GEOX, /root/WEALTH, /root/.agents): recreate the symlink in skills/, do NOT mv organ content.

### Freeze
1. Verify unused 60+ days via state.db `messages.tool_name='skill_view'` name match.
2. `mv` dir from skills/ to skills-cold/ (NEVER rm).
3. Append entry to a dated receipt under /root/.hermes/backups/.
4. `/reload_skills`.

## Pitfalls

- `.hub`/`.curator_backups` were deleted 2026-08-24 (scar in move_receipt.json); hub state regenerates — don't rely on `hermes skills update` provenance for cold skills.
- Many entries in skills/ are SYMLINKS to organ repos — move only the link, never the target.
- Category dir sharing a name with a skill (`knowledge/`) crashes naive mv — handle merge collisions explicitly.
- Bundled skills re-seed on `hermes update` without `.no-bundled-skills` marker; re-freeze reappeared ones.
- token-plan-image had 3 copies — canonical at top level, extras cold.

## Verification

- Live: `find /root/.hermes/skills -name SKILL.md | wc -l` (~179)
- Cold: `find /root/.hermes/skills-cold -name SKILL.md | wc -l` (~328)
- Frontmatter names in live tree must be unique.
