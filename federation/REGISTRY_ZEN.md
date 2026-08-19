# Registry Zen — One Source, Many Views

## The Problem (2026-08-19)

Six overlapping registries, each partially correct, none canonical:
`mcp-catalog.yaml` + `agents.yaml` + `call_map.yaml` + `organs.yaml` + `skills.yaml` + `CAPABILITY_INDEX.json`

Result: 48/62/8 drift, 78 orphan skills, arifFlow in SIMULATION (can't read coherent anatomy).

## The Cut

**ONE source (the whole):** `federation.yaml` — R∉S, the reference frame
**ONE pen:** `federation-generate.py`
**EIGHT selves (generated A2A cards):** `agents/<name>/agent.yaml`
**FOUR views (generated):** `out/` directory

```
federation.yaml          ← THE WHOLE. Singular. You edit only this. (R∉S)
agents/
  opencode/agent.yaml    ← THE SELF. A2A card. Generated. Opaque surface.
  qwen/agent.yaml        ← 8 selves, each a card, none can drift from the whole.
  ...
out/
  organ-view.yaml        ← organ-tier only
  capability-index.json  ← capability → servers
  call-view.yaml         ← role → servers
  drift-report.txt       ← all counts from one source
```

**A2A ontology:** `agent.yaml` = Agent Card (self, what one agent declares). `federation.yaml` = discovery layer (whole, who exists and who may talk to whom). The self cannot define the federation. The federation defines what each self may expose. R∉S at the protocol boundary.

## Design Decisions

1. **Surface is a field, not a count.** Each server carries `surface: public|internal|private`. Drift becomes structurally impossible.
2. **Bindings are derived, not hand-wired.** `agent → role → capability → server`. Change a role once, every agent updates.
3. **Owner is required on every skill.** `owner: null` = orphan, auto-flagged.

## How to Use

```bash
# Edit the one source
vim federation.yaml

# Regenerate all views
python3 federation-generate.py

# Check drift report
cat out/drift-report.txt
```

## Generated Views

| Output | Replaces |
|--------|----------|
| `out/agent-surface.yaml` | `agents.yaml` (agent → MCP servers) |
| `out/organ-view.yaml` | `organs.yaml` (organ-tier only) |
| `out/capability-index.json` | `CAPABILITY_INDEX.json` |
| `out/call-view.yaml` | `call_map.yaml` (role → servers) |
| `out/drift-report.txt` | Observatory drift numbers |

## Old Files (now deprecated)

These files are READ-ONLY. Do not edit them. They will be archived after F13 seal.

| Old file | Replaced by | Status |
|----------|-------------|--------|
| `mcp-catalog.yaml` | `federation.yaml` server section | deprecated |
| `agents.yaml` | `agents/<name>/agent.yaml` (A2A cards) | deprecated |
| `call_map.yaml` | `out/call-view.yaml` | deprecated |
| `organs.yaml` | `out/organ-view.yaml` | deprecated |
| `skills.yaml` (registries/) | `federation.yaml` skill section | deprecated |
| `CAPABILITY_INDEX.json` (registries/) | `out/capability-index.json` | deprecated |

## Seal Path

1. ✅ Schema designed + generator built
2. ✅ Generator runs clean (exit 0, all invariants pass)
3. ⬜ Populate with live VPS values (replace sample data)
4. ⬜ Point agent loaders at generated views
5. ⬜ Symlink or delete old files
6. ⬜ F13-seal `sealed_by` field

DITEMPA BUKAN DIBERI ⚒️
