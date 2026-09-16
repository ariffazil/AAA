# Physique Intel Substrate Pattern — Reference

> How to stand up per-coach athlete intel substrate when Arif says "init X intelligence for coach Y's athletes". Pattern proven 2026-08-29 with Syed Sado Physique Intel.

## Why this pattern exists
When Arif attends a physique comp as volunteer (not coach, not judge), there's a class of record-keeping that doesn't fit:
- Trading journal (per-trade, numeric, technical) — wrong shape
- General notes — too unstructured to grep
- CRM / athlete database — over-engineered for 1-4 comps/year/athlete

Comp data is sparse but compounding: category + placing + coach read + volunteer observations per comp day. Need append-only history per athlete that survives years.

## Directory shape
```
<root>/<coach>-physique-intel/
├── README.md                doctrine + scope (volunteer boundary, voice override note)
├── athletes.yaml            roster ledger — append-only, schema_version field
├── event-log.md             running notes per comp date (single rolling file)
├── voice-<coach>.md         coaching voice primer (per coach, distinctive)
├── comp-pipeline.md         pre → stage → post → lesson loop template
├── <coach>-mechanics.md     how coaching actually looks from volunteer side
└── sessions/
    └── <athlete-slug>.md    per-athlete append-only record (one file, grows forever)
```

`<root>` = `/root/forge_work/` (proven location) for session-bound work, or `/root/` for permanent substrates if Arif says "set this up properly, not just for today".

## File purposes

### README.md
- Doctrine: volunteer boundary rule, voice override scope, F9 anti-hantu real-person protocol
- Structure tree (above)
- How-to-use (live comp day → event-log; post-comp → sessions/<athlete>.md; pre-comp week → comp-pipeline draft)
- Out-of-scope list (programming, diet, medical, coaching cues)

### athletes.yaml
```yaml
schema_version: "ISO date"
f13_owner: Arif Fazil
coach: <Coach Name> (<handle>)
gym: <Gym>, <City>
athletes:
  - id: ath-001
    name: <Real Name>
    ig_handle: TBD   # populate when known
    coach_since: TBD
    category_history: []
    next_target: TBD
    prep_status: TBD  # off-season | bulking | cutting | peak-week
    peak_week_protocol: TBD
    notes: |
      First athlete tracked under this substrate.
ledger_rules:
  append_only: true
  result_resolve_required: true
  cross_ref_event_log: true
  anonymize_in_share: true
```

### event-log.md
Single rolling file per comp day. Template fields:
- Event name + date + venue (when known)
- Athletes tracked (links to athletes.yaml)
- Live state — observed by Arif (posers, backstage crowd, lighting, energy)
- Per-athlete run sheet (category, conditioning, poses, symmetry, stage energy, result, coach read)
- Volunteer side (what Arif did: pump room, water, transport, photos)
- Other ringside intel (judges, rivals, Krishnakumar presence)
- Post-comp (cooldown, debrief, prize, social)
- Source map applied (which sources primary this time)
- Pitfalls applied (which scars were activated)

### sessions/<athlete-slug>.md
Per-athlete append-only. Sections:
- Snapshot (name, coach, first tracked comp, status)
- Athlete dossier (age, height, weight class, off-season weight, stage weight, prior comps, strengths, gaps, injury)
- Comp log table (Date | Event | Category | Placing | Result)
- Most recent comp — full debrief section (coach read, volunteer read, lessons)
- Next-cycle parking lot
- Archive rules (never overwrite, append only)

### comp-pipeline.md
Generic 5-phase template per comp:
- Phase 0 — Comp selection (winner-only gate)
- Phase 1 — Prep 8-12 weeks
- Phase 2 — Stage week (-7 to 0)
- Phase 3 — Stage day
- Phase 4 — Post-comp (within 7 days)
- Phase 5 — Lessons archived

Copy per active cycle to `sessions/<athlete>-<year>-<comp>.md` (per-comp append-only file inside the athlete folder if comps stack).

## Substrate init sequence (2-3 minutes, not 10)

When Arif says "init physique/substrate/WELL intelligence for <coach>":

1. Pick `<root>` — default `/root/forge_work/<coach>-physique-intel/`. Confirm if Arif said "permanent" or "session".
2. Write README.md (boundary doctrine + tree + scope).
3. Write athletes.yaml with schema_version header + 1 athlete entry (TBD fields).
4. Write event-log.md skeleton (today's comp header + TBD fields).
5. Write voice-<coach>.md (voice primer based on observed coach register).
6. Write comp-pipeline.md (5-phase template).
7. Write <coach>-mechanics.md (volunteer observation of how coach works).
8. Write sessions/<first-athlete-slug>.md (template, TBD fields).
9. Memory entry: substrate path, voice override scope, F9 real-person protocol.

**Don't ask "what fields do you want" or "should we use yaml or sqlite".** Pick the shape, ship it. Arif redirects if wrong.

## Append-only discipline
- `athletes.yaml` — never delete entries. Update fields. Add new athletes as new entries.
- `event-log.md` — append new comp sections, never overwrite old.
- `sessions/<athlete>.md` — append new comp sections below, never rewrite prior.

Git-friendly: each file is mostly prose + tables. Hand-editable on Arif's phone if needed.

## Pitfalls
- ❌ SQLite / Postgres / vector DB for 4 comps/year — overkill. Yaml + md wins.
- ❌ Asking 10 questions before drafting — Arif says "buat ja". Ship in 2-3 min.
- ❌ Generic "athlete tracker" SaaS — Arif doesn't want another login.
- ❌ Coach voice for volunteer chat — wrong register. Voice override scoped to cue/draft only.
- ❌ Adding athlete fields Arif didn't ask for — schema stays lean, grows with comps.

## Cross-ref
- Voice primer for Syed specifically: `references/abang-sado-coaching-voice.md`
- Boundary doctrine: see SKILL.md § "Volunteer-side Intel Mode"
- **Telegram lane wiring for an athlete DM** (6-step proven pattern — config.yaml + lanes.yaml + cross-profile memory files + athletes.yaml + sessions/<slug>.md + verify): see `references/syedsado-physique-substrate.md`. Use when Arif says "wire TG ID `<digits>` for `<athlete name>`" or Coach Syed asks to onboard a client as a Hermes contact.