# Concurrent-Canonical-Write Incident — 2026-08-07

> Incident reference for F3b failure mode. Two agents wrote `AAA_FEDERATION_CONTRACT_v0.1` simultaneously.

## Timeline

| Time (UTC) | Agent | Path | Format |
|---|---|---|---|
| 05:31 | Hermes | `/root/AAA/federation/AAA_FEDERATION_CONTRACT_v0.1.md` | Markdown (113 lines, 5932 bytes) |
| 05:31 | Kimi/other | `/root/AAA/federation/contracts/AAA_FEDERATION_CONTRACT_v0.1.yaml` | YAML (134 lines, 4676 bytes) |

Same timestamp. Same content. Different paths. Different INV-ID assignments.

## INV-ID divergence

| INV-ID | Hermes MD | YAML |
|---|---|---|
| 01 | Spawn transfers work | Spawn transfers work (same) |
| 02 | Capability ceiling | Judgment path |
| 03 | Judgment path | Per-spawn governance |
| 04 | Per-spawn governance | Unknown is valid |
| ... | different order | different order |

Same 15 invariants. Completely different ID numbering. Both claim authority. Neither references the other.

## Resolution

Per sovereign directive: YAML kept (richer structure — each INV carries `enforces`/`consequence`/`source`). MD archived:

```
/root/AAA/federation/_archive/2026-08-07-pre-canon-merge/AAA_FEDERATION_CONTRACT_v0.1-MD-DRAFT.md
```

## What broke

1. **INV-14 (receipt chain):** Neither file had `parent_spawn_hash`. The write itself violated the contract it was trying to establish.
2. **INV-15 (no silent violation):** The concurrent write was NOT silent (two files visible on disk) — but it was uncoordinated (no explicit conflict protocol).
3. **INV-04 (spawn-level governance):** The violation was at spawn level (two agents spawned by the same sovereign, writing to overlapping scope), not caught by any gate.

## Defense

1. When two agents receive "forge X" instruction, include `canonical_path:` in the instruction
2. If concurrent write detected post-hoc: archive both, re-derive canonical from both inputs
3. Add INV-16: "Concurrent canonical writes are a violation, not a feature"
4. **List target directory before writing** (F3 defense) — even when writing to a NEW path

## Source

Live incident, 2026-08-07. Verified by `ls -la` and `diff`. No fabrication.
