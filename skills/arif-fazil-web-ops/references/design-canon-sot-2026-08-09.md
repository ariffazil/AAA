# Design Canon SOT — arif-fazil.com (verified 2026-08-09)

Condensed from the zero-context survivability audit + SOT receipt verification.
Use BEFORE any design change to the hub pages. Hierarchy (verified against files):

```
atlas.yaml (SEALED F13 2026-08-01)  → route + ring authority
federation.json (organs section)    → organ + port + posture authority (8 organs)
SITE_IDENTITY.md §5                 → sacred palette authority
world-model.yaml (DRAFT — NOT ratified) → vocabulary overlay, Phase A incomplete
llms.txt                            → INCOMPLETE surface summary (lists 5 organs only)
```

## The sacred palette (SITE_IDENTITY §5)

`paper #0A0B0D` · `ink #EDEAE2` · `ink-soft #9AA0A8` · `ember #E4572E` · `gold #C9A227`
Gold/ember = value + warning. **Ember is NOT a door accent — it is the warning accent.**

## atlas.yaml rings (SEALED) — `data-ring` personalities

| Ring | tokens | plane | Primary hex (tokens.css) | Pages |
|---|---|---|---|---|
| SOUL | red | narrative | `#8B1A1A` / `#B33030` (+ gold accent `#E8B84B`) | / (home), /000, /doctrine, /writing, /essays, /politics/shadow |
| MIND | cyan | proof | `#00D4AA` | /999, /mcp, /missions, /verify, /canon |
| BODY | gold | organ | gold family `#C9A227`/`#D4A24C`/`#E8B84B` | /world, /wealth, /economics, /well, /vitals, /forge, /malaysia, /oil, /gas, /gold, /politics/* |
| ORGAN | violet | domain | violet family | /earth, /geox |

## tokens.css organ colors (Trinity §color.organ)

arifOS `#E8B84B` gold · AAA `#7C9CFF` blue · GEOX `#6BD3B4` teal · WEALTH `#D4A24C` amber · WELL `#E58CC1` pink · A-FORGE `#B487F5` violet

## Verified live-door mapping (5-lane nav: HOME EARTH WORDS WORLD WORK)

| Live door | atlas route | Ring | Canon accent | My first pass (WRONG) |
|---|---|---|---|---|
| HOME (/) | / | SOUL | red family + gold accent | gold only |
| EARTH (/earth) | /earth | ORGAN · GEOX | teal `#6BD3B4` | cyan `#4FC3F7` (close but not canon) |
| WORDS | /doctrine /writing (SOUL) | SOUL | red family | amber `#D4A24C` |
| WORLD (/world) | /world | BODY | **gold** | ember `#E4572E` (wrong — world=capital=gold) |
| WORK | /forge /well /vitals | BODY | gold family (or A-FORGE violet) | green `#3DDC97` (wrong) |

Note: `words` and `work` are NOT atlas routes — mapping them is reconstruction, not citation.
The 9-domain accent map in world-model.yaml (earth=teal, capital=yellow, voice=purple, work=amber,
human=red, origin=gold, proof/law=void-blue) is DRAFT — do not treat as canonical until F13.

## Divergence findings (2026-08-09)

- Live 5-door nav ≠ world-model.yaml 9-domain nav (earth/capital/voice/work/law/proof/origin + signal/human) — DRAFT, Phase A incomplete (`phase_a_complete: false`).
- atlas.yaml routes have NO /words or /work — live doors are legacy names.
- `/trust/` 404 and `/observatory/` 404 (moved to /arifos/ without redirect) despite SITE_CONSTITUTION RULE 2 promising ≤3-click access.
- llms.txt "five constitutional organs" omits A-FORGE, arifFLOW, HERMES — federation.json `organs` array has all 8 with ports/postures/MCP endpoints.
- `/root/arif-fazil.com/FEDERATION.md` is a dead symlink.

## Status

Per-door accent implementation (tokens.css `--accent-*` + hub badges) is deployed to origin but
held at Cloudflare edge (4h TTL, purge token lacks permission). Alignment to canon colors:
**HOLD — awaiting F13 ruling** (design identity is Arif's call).
