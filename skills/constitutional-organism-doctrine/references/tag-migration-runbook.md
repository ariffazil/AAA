# Tag Migration Runbook — Federation-Wide Label Rename

> **Forged:** 2026-08-12 · Case study: `[EXE]` → `[🦾ACT]`
> **Trigger:** Any constitutional tag rename that propagates across multiple tiers

## Pre-Migration Checklist

1. [ ] **Canonical source identified** — where is the tag first defined?
2. [ ] **All files containing the old tag found** — `rg -l 'OLD_TAG' /root/{AAA,HERMES,arifOS,...}`
3. [ ] **Back-compat decision made** — should the gate regex match both old and new?
4. [ ] **Emoji width verified** (if emoji is part of new tag)
5. [ ] **Backup taken** of mutable files before patching

## Migration Steps

### Tier 1: Canonical Fragment
```
/root/AAA/instructions/<fragment-name>.md
```
- Update ALL references to the old tag
- Add **Rename Provenance** section documenting old→new, rationale, and immutability of historical receipts

### Tier 2: Rendered Output
```bash
cd /root && ./scripts/render-agents.sh
```
- Re-renders AGENTS.md + CLAUDE.md from canonical fragments
- Verify output contains new tag: `rg 'NEW_TAG' /root/AGENTS.md`

### Tier 3: SOUL.md (Identity)
```
/root/HERMES/SOUL.md
```
- Line 168+ embeds the receipt mandate
- Update all references

### Tier 4: Gate Code (Physical Enforcement)
```
/root/HERMES/mcp_servers/substrate_output_gate.py
```
- Update regex: `re.compile(r'(\[(?:NEW_TAG|OLD_TAG)(?:-PARTIAL)?\]...)')`
- **CRITICAL:** Keep OLD_TAG in regex for VAULT999 back-compat
- Update self-tests to cover BOTH new and legacy
- Run: `cd /root/HERMES/mcp_servers && python3 substrate_output_gate.py`

### Tier 5: Skills (All References)
```
rg -l 'OLD_TAG' /root/HERMES/skills/ /root/AAA/skills/
```
- Patch each skill that references the old tag
- Add rename provenance note where the tag is discussed in detail

### Tier 6: Memory Notes
```
/root/HERMES/memories/MEMORY.md
/root/HERMES/memories/USER.md
```
- Update persistent references

### Tier 7: Canon JSON (Emoji Mapping)
```
/root/AAA/canon/epistemic-emoji-map.json
```
- Update the EXECUTION section with new tag name and emoji

### Tier 8: Verify
```bash
# Confirm zero stale active references (exclude provenance/history notes)
rg -l 'OLD_TAG' /root/{AAA/instructions,HERMES/SOUL.md,HERMES/mcp_servers,HERMES/skills,HERMES/memories,AGENTS.md} | grep -v 'archive\|seed\|BACKUP'

# Confirm gate passes
cd /root/HERMES/mcp_servers && python3 substrate_output_gate.py

# Confirm render is clean
cd /root && ./scripts/render-agents.sh
```

## Pitfalls

1. **Regex back-compat:** If you remove OLD_TAG from the gate regex, any VAULT999 historical receipt tagged with OLD_TAG will be treated as untagged prose (Rule 3 pass-through). Keep both in the alternation group.

2. **Emoji before gate:** If the emoji REPLACES the ASCII tag before the gate layer, the regex won't match. The agent must emit ASCII tags internally, and the gateway/render layer converts to emoji for human consumption.

3. **Unicode width:** Some emoji are 2-cell wide (East Asian Width `W`), which can break monospace alignment. Test in the target terminal before deploying.

4. **Partial renames:** If you only update tiers 1-3 but skip tier 4 (gate code), the physical enforcement still works with the old tag. This is safe temporarily but creates confusion about which tag is canonical.

5. **Skill reference file renames:** When renaming a reference file (e.g. `exe-receipt-discipline-2026-08-12.md` → `act-receipt-discipline-2026-08-12.md`), update ALL skill references to the file path, not just the content.

## Case Study: [EXE] → [🦾ACT] (2026-08-12)

- **Rationale:** ACT execution actuator alignment with constitutional reflex arc
- **Gate back-compat:** YES — regex matches both `[🦾ACT]` and `[EXE]`
- **Files modified:** 10 across 7 tiers
- **Gate tests:** 4/4 PASS (3 new + 1 legacy back-compat)
- **Render:** AGENTS.md + CLAUDE.md re-rendered clean
- **Emoji:** 🦾 (U+1F9BE, East Asian Width W, 2-cell)
