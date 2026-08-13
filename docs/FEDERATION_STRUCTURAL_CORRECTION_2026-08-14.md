# FEDERATION STRUCTURAL CORRECTION — 2026-08-14

**Authority:** ARIF (F13 SOVEREIGN)
**Issued:** 2026-08-14T06:00Z
**Priority:** IMMEDIATE — all CCC coding agents

## STRUCTURAL TRUTH

FED, FLAME, and FRAME are NOT independent GitHub repos.
They are organs of AAA. Their canonical home is:

- **FED** → `/root/AAA/scripts/fed_router.py` (already here, live service uses this path)
- **FLAME** → `/root/FLAME/` (temporary, should migrate to AAA governance)
- **FRAME** → `/root/FRAME/` (GitHub private repo, keep as-is for now)

### What this means for CCC coders:

1. **DO NOT create new repos** for FED, FLAME, or FRAME
2. **DO NOT push to** `ariffazil/FED.git` or `ariffazil/FLAME.git` — they don't exist on GitHub
3. **FED code lives in AAA** — `/root/AAA/scripts/`
4. **FLAME code lives at** `/root/FLAME/` — systemd service `flame-api.service` runs from here
5. **FRAME** — private GitHub repo, push access available

### Orphaned local clones (DO NOT USE):
- `/root/FED/` — dead clone, runtime uses AAA/scripts instead
- `/root/FLAME/` — live runtime, but no GitHub remote
- `/root/.openclaw/workspace-*` — agent scratch dirs, no remote
- `/root/.openclaw/workspace` — stale AAA feature branch clone

### Canonical repo map (updated):
| Organ | GitHub | Local | Status |
|---|---|---|---|
| AAA | ariffazil/AAA | /root/AAA | Canonical root |
| arifOS | ariffazil/arifOS | /root/arifOS | OK |
| A-FORGE | ariffazil/A-FORGE | /root/A-FORGE | OK |
| HERMES | ariffazil/HERMES | /root/HERMES | OK |
| GEOX | ariffazil/GEOX | /root/GEOX | OK |
| WEALTH | ariffazil/WEALTH | /root/WEALTH | OK |
| WELL | ariffazil/WELL | /root/WELL | OK |
| arifFlow | ariffazil/arifFlow | /root/arifFlow | OK |
| FRAME | ariffazil/FRAME | /root/FRAME | OK (private) |
| FED | NONE | /root/AAA/scripts | In AAA |
| FLAME | NONE | /root/FLAME | needs AAA migration |

DITEMPA BUKAN DIBERI
