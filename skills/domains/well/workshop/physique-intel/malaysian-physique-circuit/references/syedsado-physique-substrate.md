# SyedSado Physique Substrate — Pattern + Scaffold

> Class reference for the `/root/forge_work/syedsado-physique-intel/` live substrate.
> Read when: Arif, Coach Syed, or an athlete DM references a new athlete, a new comp cycle, a coach-side intel request, or any volunteer-side observation from a bodybuilding event.
> Owner: Arif Fazil (F13). Substrate forged 2026-08-29 alongside `malaysian-physique-circuit` skill.

## What this substrate IS
- A persistent append-only ledger for Syed-coached athletes — identity, comp history, prep status, visual intel, next-cycle questions, coach verbatim reads.
- The **bridge** between the federation (Hermes, voice, lanes, memory) and the **real-world coach/volunteer/athlete triangle** at Malaysian BB events.
- F13 record. Bodies NEVER merge. Each athlete is its own row, its own dossier.

## What this substrate is NOT
- A coaching platform. Programming, peaking, macros, posing cues → Coach Syed owns.
- A public archive. Athlete handles, results, photo identity — opt-in only (F9 anti-hantu).
- A diagnostic tool. Visual intel = honest observe; never prescribe.

## Substrate layout (proven 2026-08-29)

```
syedsado-physique-intel/
├── README.md                    doctrine + scope + "what we don't do"
├── athletes.yaml                F13 ledger — one entry per athlete, append-only
├── event-log.md                 active comp run sheet (TBD rows until Arif captures)
├── voice-abangsado.md           coaching voice primer (BM Penang gritty, Abang Sado register)
├── comp-pipeline.md             pre → stage → post → lesson loop (template)
├── coach-syed-mechanics.md      how coaching actually looks from volunteer side
└── sessions/
    └── <athlete-slug>.md        per-athlete dossier (one file, append per comp)
```

## Roster discipline (athletes.yaml)

```yaml
schema_version: "YYYY-MM-DD"
f13_owner: Arif Fazil
coach: Syed Khairuddin Morktarudin (@rico_ricaldo_33)
gym: D'Popye Gym, KL

athletes:
  - id: ath-NNN            # sequential, never reuse
    name: "<full name>"
    telegram_id: '<digits>'  # only if wired (see Onboarding below)
    ig_handle: TBD | '@handle'
    coach_since: <YYYY> | TBD
    category_history: []   # filled from event logs as they accumulate
    next_target: TBD | '<event name>, <date>'
    prep_status: off-season | bulking | cutting | peak-week
    peak_week_protocol: TBD | '<custom rule>'
    notes: |
      Multi-line, append-only. Never delete — superseded means edit next-line down.
```

**Append-only rule.** Never delete a row. To "retire" an athlete: set `prep_status: retired` and add a new row in `notes` with date. The historical record stays.

## Onboarding an athlete (Tele lane wiring pattern)

When Arif says "wire TG ID `<digits>` for `<athlete name>`" (or Coach Syed asks to onboard someone as a Hermes contact):

1. **`config.yaml`** — add `<digits>` as string in TWO lists (YAML roundtrip via `execute_code` because `patch` tool refuses this file):
   - `telegram.allowed_chats` (gate open)
   - `telegram.free_response_chats` (no `@mention` required for DM-style reply)
   - **Verify with `grep -c "<digits>"` — must equal 2.** This is the double-inject rule (see skill pitfalls).
2. **`lanes.yaml`** — append a new lane after `faqwan:` block, before `guest:`. Copy the Faqwan schema; swap identifiers; add `skills: [..., "malaysian-physique-circuit"]` and `canonical_refs: [..., "/root/forge_work/syedsado-physique-intel/README.md", ...]` and `doctrines: { ..., diagnose_dont_prescribe: true, coach_syed_owns_calls: true }`.
3. **Cross-profile memory files** — forge in `/root/HERMES/profiles/aaa-hermes/memories/`:
   - `USER-<slug>.md` — identity table, athlete dossier, comp history (TBD rows), comm preferences, permissions.
   - `SOUL-<slug>.md` — voice register (pending first 3-5 DMs), what-I-AM-allowed, what-NEVER-allowed (coaching cues, macros, medical, public naming without consent).
   - `MEMORY-<slug>.md` — rolling memory lane.
   - **MUST use `cross_profile=true` flag on `write_file`** — tool defaults to refuse any cross-profile write. Verified 2026-08-29.
4. **`athletes.yaml`** — append entry as above.
5. **`sessions/<slug>.md`** — forge the dossier with all known fields filled, photo evidence path, and pending fills block.
6. **Verify (parallel)**: grep config.yaml + grep lanes.yaml + `ls USER/SOUL/MEMORY files` → must all show the new ID. Then announce.

## Visual intel — adding an athlete photo

1. Save path (e.g. `/root/.hermes/cache/images/img_<hash>.jpg`) — don't move, just reference.
2. Call `vision_analyze` with the **explicit guardrail prompt** (see Pitfalls in `malaysian-physique-circuit/SKILL.md`) — verbatim instruction block: "Don't name the person. Don't assign placing. Don't fabricate category."
3. Log in `sessions/<slug>.md` under a `## Visual intel — YYYY-MM-DD (location)` heading.
4. Always append: "**Caveat:** [backstage gym light / daytime outdoor / hotel ballroom] ≠ stage verdict under spot lights."

## Active-comp live observation pattern

When Arif (or another volunteer) is physically at a venue:

1. Open `event-log.md`; remove the placeholder TBD rows as data comes in.
2. Capture the **competitor number** from the plate on trunks → update `athletes.yaml` and `sessions/<slug>.md`.
3. Capture **category** (printed banner, MC announce, score sheet — primary source only; never guess).
4. Capture **placing** (post-comp MC announce; verify with Daily Express Sabah / Molek / Tegaptv Malaysia the next morning, cite source URL).
5. Capture **Coach Syed's verbatim read** if he gives one — quote, don't paraphrase.
6. Capture **volunteer observations** — pump room, posing, stage energy, audience response, lighting. Honest, structured.
7. **Never fabricate.** If you didn't see it, write TBD.

## Post-comp (within 7 days)

1. Refresh `athletes.yaml` row with `category_history: [..., {date, event, category, placing}]`
2. Add dated entry under `## Comp log` in `sessions/<slug>.md`
3. Capture next-cycle question (parked)
4. Optional: cross-link if Coach Syed's read differs from volunteer's read — file both, no synthesis

## What NEVER goes in this substrate
- Workout prescriptions (sets × reps × tempo)
- Macros / calories / food timing
- Peaking protocols authored by anyone but Coach Syed
- Health/medical interpretation
- Public photo/name references for non-consenting athletes
- Predictions of placing before the announcement

## Source files cross-reference
- `malaysian-physique-circuit` skill → MSIA comp source map + winner-only doctrine + photo-analysis pitfalls
- `syedos` skill → Coach Syed persona + Abang Sado voice register + DM behaviour patterns
- `BIOHACK-PEPTIDES` skill (separate) → if Syed pitches peptide protocols to a client, route there — never into athlete substrate.
