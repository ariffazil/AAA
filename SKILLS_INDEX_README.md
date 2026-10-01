# SKILLS INDEX — Source-of-Truth Map

> Written 2026-10-01 by FI-008 during distraction cleanup.
> Three files look similar. They are NOT redundant. Each has one job.

## The 3 files

| File | Schema | Role | Generator | Reader |
|---|---|---|---|---|
| `skills_index.federation.json` | `arifos.skills.federation.v1` | **INPUT MANIFEST** — defines which organ roots contribute + dedup priority | `scripts/skills_index_gen.py --federation` | `skills_index_gen.py` itself (next stage) |
| `skills_index.json` | `1.1.0-federation` | **OUTPUT CATALOG** — the federated skill catalog after dedup | `scripts/skills_index_gen.py` (default) | `scripts/compass.py`, `QWEN_INIT_PROMPT.md`, `TREE777` |
| `skills/SKILLS_INDEX.json` | `arifos.skills_index.v2` | **INTERNAL v2 INDEX** — the v2 skill mesh (different schema, different generator, internal to `skills/` tree) | `skill-index-generator.py` (separate process) | internal v2 mesh consumers |

## Flow

```
skills_index_gen.py --federation
        ↓ (writes)
skills_index.federation.json       ← INPUT MANIFEST (organ roots + priority)
        ↓ (reads)
skills_index_gen.py --out
        ↓ (writes)
skills_index.json                  ← OUTPUT CATALOG (what compass / TREE777 read)
```

Separately:

```
skill-index-generator.py           ← INTERNAL v2 tool
        ↓ (writes)
skills/SKILLS_INDEX.json            ← INTERNAL v2 INDEX (lives inside skills/ tree)
```

## What to edit

- **Adding a new organ** → edit `skills_index.federation.json`'s `roots` + `priority`, then regenerate `skills_index.json`.
- **Adding a new skill** → just put it under the right path; the catalog regenerator finds it.
- **Never hand-edit any of the three.** All three carry `do_not_hand_edit` or are generator outputs.

## Why both v1 and v2 exist

v1 is the federated-wide catalog (cross-organ, 754 unique skills after dedup).
v2 is the skills/-internal index (richer mesh: harnesses, alias_paths, depth metrics, 654 skills).

The AAA cockpit and QWEN init read v1.
The v2 mesh internally reads v2.

Both pipelines are live. Don't unify them — different purposes.