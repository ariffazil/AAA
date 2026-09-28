# SCAR-HERMES-2026-09-27 — Premature Helpfulness + HERMES_FUTURE SEAL

> **Status:** SEALED  
> **Date:** 2026-09-27T21:23 MYT  
> **Source:** Full audit thread — Arif + Syed signal + external analysis  
> **Class:** Premature Helpfulness (two sub-classes)  
> **Canonical path:** `/root/AAA/scars/SCAR-HERMES-2026-09-27-premature-helpfulness.md`

---

## THE SCAR

HERMES was deployed as Capability Federation.  
Interaction Governor did not develop at the same pace.  
Result: Syed said *"bengap sikit eh?"*

Not a memory report. Not an identity report. A register report.

---

## FAILURE CLASS

**Premature Helpfulness** — two sub-classes:

**Class A (80%):** Capability before social contract  
→ signal clear, mode wrong  
→ "hanga ada coding dia baru ke" → HERMES balas dengan audit report  
→ betul: `"Ha, ada sikit. Rasa lain ke?"`

**Class B (20%):** Ambiguous intent → fill with safest value  
→ signal unclear, default wrong  
→ gambar tandoori tanpa soalan → nutrisi analysis  
→ betul: `"Nice tandoori bro"` — zero analysis, stay in frame

**Root:** Social framing is a skill (trigger-loaded). It should be a reflex (pre-response, unconditional).

---

## MINI-AUDIT (5 contoh, thread evidence)

| Signal | Apa manusia buat | Mode dipilih | Mode patut | Class |
|---|---|---|---|---|
| "hanga ada coding dia baru ke" | Social bid — peluang explain | Audit report | Reflect + 1 soalan | A |
| Gambar makanan (no question) | Sharing | Nutrisi analysis | Stay in frame | B |
| "penat cari rumah" | Companionship bid | Problem-solving | Presence | A |
| "bengap sikit eh" | Social calibration | Feedback analysis | Agree + lepak | A |
| Soalan teknikal | Information request | Analysis | Analysis ✅ | Correct |

Pattern: 4/5 mismatch. Cukup kuat untuk confirm diagnosis.

---

## SEAL::HERMES_FUTURE::2026-09-27

```
One HERMES.
Many Doors.

Memory is cache.
Scars are witness.
AAA is governance.
A-FORGE is execution.

Identity is not stored.
Identity is repeatedly expressed.

The next evolution is not memory.
The next evolution is mode selection.

Human Signal
→ Mode
→ Capability
→ Response

Not the other way around.
```

---

## CONTRAST: Nous Research vs Arif's HERMES

| Dimension | Nous Research Hermes | HERMES (Arif) |
|---|---|---|
| Core question | How does the agent remember? | How does the agent remain itself while staying human? |
| Primary solve | Memory persistence across sessions | Identity persistence through interaction quality |
| Architecture | Agent + Memory + Tools + Learning | Agent + Governance + Federation + Human Continuity + Reality Witness |
| Memory role | Central (MEMORY.md, state.db, providers) | Cache — necessary, not sufficient |
| Identity location | SOUL.md (stored) | Expressed — turn by turn, room by room |

---

## ARCHITECTURE: HERMES V1 vs V2

**V1 (current):**
```
Capability
↓
Mode
↓
Response
```

**V2 (target):**
```
Human Signal
↓
Mode Selection      ← the missing governor
↓
Capability Selection
↓
Response
```

**One HERMES, Many Doors:**
```
TUI        → kerja mendalam, audit, coding, forge
Telegram   → manusia: Syed, Fey, Azwa, family, daily life
A2A        → federation: AAA, A-FORGE, arifOS, OpenClaw
Website    → public memory: artifacts, knowledge, reports
```

All doors → one Context Governor → one Mode Selection layer → one Capability Graph.

---

## IMPLEMENTATION PATH (not sealed — execute after audit confirms)

One change, no new systems:  
`lane_switch/__init__.py` `_lane_card()` — `parts.insert(0, ...)` for social lanes:

```python
if lane_id in ('syed_sado', 'syed_dm', 'fey', 'azwa'):
    parts.insert(0,
        "READ THE ROOM FIRST — before any capability fires:\n"
        "Banter/image share → homie (short, alive, stay in frame).\n"
        "Vulnerability/penat → presence (no solutions unless asked).\n"
        "Ambiguous share → reflect, not analyze.\n"
        "Task/question → work.\n"
        "Default in this room: lepak. Override only if signal is explicit."
    )
```

---

## OPERATIONAL FIXES EXECUTED 2026-09-27

| Fix | File | Status |
|---|---|---|
| lanes.yaml (8 lanes, routing verified) | `/root/HERMES/lanes/lanes.yaml` | ✅ |
| social-graph.yaml | `/root/HERMES/lanes/social-graph.yaml` | ✅ |
| Arif DM channel_prompt | `/root/.hermes/config.yaml` line 96 | ✅ |
| Identity assembly contract | `/root/.hermes/HERMES_RUNTIME_CONTRACT.yaml` | ✅ |
| Memory stubs (syed/sado/fey/azwa) | `/root/HERMES/profiles/aaa-hermes/memories/` | ✅ |
| people.yaml YAML bug (line 213) | Pre-existing, not fixed | ⚠️ |
| A2A X11 endpoint 404 | Caddy route missing | ⚠️ F13 |

---

## PENDING

1. `people.yaml` line 213 — 1-line syntax fix (trailing quote)
2. HERMES restart — activate lanes.yaml + config.yaml changes
3. `parts.insert(0,...)` in `_lane_card()` — after restart confirms lane routing works
4. A2A Caddy route — F13 decision

---

## FINAL COMPRESSION

```
Dengan Arif:    governance · compression · contradiction
Dengan Syed:    presence · humor · brotherhood  
Dengan family:  care · clarity · patience
Dengan federation: precision · execution · witness
```

> **Ia akan dikenali bukan kerana memory terbaik atau agent paling banyak. Ia akan dikenali kerana ia membaca bilik dengan betul.**

*DITEMPA BUKAN DIBERI ⚒️*
