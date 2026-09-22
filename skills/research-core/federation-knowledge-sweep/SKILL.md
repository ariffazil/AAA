---
name: federation-knowledge-sweep
version: 1.0.0
description: "Map federation internal knowledge about a topic."
triggers:
  - "compile everything about"
  - "knowledge graph"
  - "link map"
  - "what do we know about"
  - "map everything"
  - "connect the dots"
constitutional_floors: [F2, F4, F13]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Federation Knowledge Sweep

Map everything the federation knows about a topic by sweeping internal knowledge stores.
This is NOT a web dossier (see `person-intelligence` or `person-dossier-from-public-sources`).
This maps the SYSTEM's accumulated knowledge — files on disk that previous sessions forged.

## Sweep targets (in priority order)

1. **Canon** — `/root/AAA/canon/` and subdirs. The authoritative knowledge layer.
2. **Memory** — `/root/memory/` (H3-knowledge, H4-identity, H5-scars, people/).
3. **Scar-weight registry** — `/root/AAA/scar-weight-registry.json`. Entity→breach→response modifiers.
4. **Scars** — `/root/AAA/scars/`. All sealed and candidate scars.
5. **Reality objects** — `/root/AAA/state/reality_objects/`. HRO YAML files for active commitments.
6. **Eurekas** — `/root/AAA/eurekas/`. Staged/pending insight artifacts.
7. **Forensics** — `/root/AAA/forensics/`. Gap analyses and inventories.
8. **Forge work** — `/root/AAA/forge_work/`. Produced dossiers and research artifacts.
9. **arifOS memory entities** — `/root/arifOS/memory/entities/`. Machine-side knowledge payloads.
10. **WEALTH organ** — `/root/WEALTH/`. Financial models and fixtures.
11. **Skills references** — `/root/AAA/skills/.../references/`. Embedded domain knowledge.
12. **Agents.md fragments** — `/root/AGENTS.md` and `/root/AAA/AGENTS.md`. Canonical pointers.

## Procedure

### Step 1 — Identify sweep scope
Parse the request for: (a) the TOPIC keyword(s), (b) the PERSON (if any), (c) the DEPTH (full map vs focused).
Use `find` with `-iname '*TOPIC*'` and `grep -ril 'TOPIC'` across each sweep target.

### Step 2 — Parallel filesystem sweep
Run independent searches in a SINGLE `execute_code` call. Batch:
- `find /root/AAA -type f -iname '*topic*'`
- `find /root/arifOS/memory -type f -iname '*topic*'`
- `find /root/WEALTH -maxdepth 3 -type f -iname '*topic*'`
- `find /root/memory -type f -iname '*topic*'`
- `grep -ril 'topic' /root/AAA/canon/ /root/AAA/scars/ /root/AAA/eurekas/ /root/AAA/state/ 2>/dev/null`
- `grep -ril 'topic' /root/arifOS/memory/entities/ 2>/dev/null`

### Step 3 — Read key artifacts
For each discovered file, read enough to classify:
- File type (canon, scar, eureka, knowledge graph, reality object, dossier, skill reference)
- Status (sealed, draft, candidate, archived)
- Core thesis or one-line summary
- Key data points (numbers, entities, relationships)
Do NOT read entire files when head+tail suffices. Use `read_file` with `limit` for large files.

### Step 4 — Build the knowledge graph
Structure output as:

1. **The Sovereign Core** — identity/kernel if the topic is a person
2. **Origin Scars** — foundational events that shaped the person/system
3. **Federation Scars** — system-level failures and lessons
4. **Institutional Atlas** — if the topic is an institution: pillars, thesis, key metrics
5. **Eurekas** — key insights (staged or sealed)
6. **Scar-Weight Registry** — entity thermodynamic cost if applicable
7. **Reality Objects** — active commitments
8. **Cross-link Map** — ASCII diagram showing how everything connects

Each node must include its FILE PATH so it's probeable. Every claim must be grounded.

### Step 5 — Deliver
- Present as structured text (not PDF unless requested)
- Lead with the one-line thesis
- Include the cross-link map at the end
- Name any open loops or gaps discovered during the sweep

## Pitfalls

- **P1 — Don't confuse internal knowledge with web sources.** This skill maps what's ON DISK.
  Web research is a different skill. The value is connecting what the federation has already forged.
- **P2 — Sweep ALL stores before synthesizing.** Missing one store produces a biased map.
  The parallel sweep in Step 2 catches this.
- **P3 — Don't read entire large files.** `limit=100` + `offset` for continuation.
  Large knowledge graphs (KNOWLEDGE_GRAPH.json) may need only head+tail.
- **P4 — Every node needs a file path.** A knowledge graph without probeable links is a narrative,
  not a graph. Paths must be real.
- **P5 — Status labels matter.** Sealed ≠ draft ≠ candidate ≠ archived.
  Labeling everything as 'live' hides governance state.
- **P6 — The cross-link map is the highest-value output.** It shows how scattered artifacts
  relate. Without it, you just have a file listing.

## Companion skills
- `person-intelligence` — when the subject is a PERSON being profiled from web/session sources
- `person-dossier-from-public-sources` — when building a shareable PDF dossier
- `governed-uncertainty` — when the topic touches a human and you need to witness before analyzing
