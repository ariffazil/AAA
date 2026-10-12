# HOLD NOTICE — Person-File v1.1 Artefacts (2026-10-06)

> **Status:** HELD per F13 verdict review, 2026-10-06
> **Reason:** v1.1 architecture (`/root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.1.md`) is SUPERSEDED by the v1.2 amendments diff at `/root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.2-AMENDMENTS.md`.
> **Authoritative action (per F13):** "AMEND, jangan migrate lagi. Preserve 15-block design but add claims as block 16. Recast person.v1.yaml from 'single source of truth' to 'canonical materialized projection.' Raw evidence and HumanStateClaim records remain independently authoritative."

## What is HELD

| Path | Status | Reason |
|---|---|---|
| `/root/AAA/scripts/person_validate/person_validate.py` | HELD | Built against v1.1 SOT-claim architecture. Needs v1.2 AMEND 13 changes before re-use. |
| `/root/AAA/scripts/person_pilot/migrate.py` | HELD | Built against v1.1 refactor model. Per F13, do NOT run on a real person tree. Synthetic fixture only. |
| `/root/AAA/cockpit/musyawarah/2026-10-06-person-file-design/README.md` | HELD | References v1.1 sections. Re-index into v1.2 after Step 1. |

The originals remain in place (not deleted) because they may still be useful for reading code review by the musyawawah. They are NOT to be re-run on production data.

## What was MOVED out of production

The pilot migration output — `/root/memory/people/SYED/person.v1.yaml` (653 lines, v1.1-era) — was moved to:

`/root/.hermes/cache/scratch/pilot_S01/person.v1.yaml.v1.1-era`

Reason: F13 verdict said "do not overwrite" and "do not migrate" yet. The v1.1 pilot YAML was placed in the production Syed tree by the subagent before the verdict was read. Relocated to scratch as a comparison fixture, renamed to mark its v1.1-era provenance. The original Syed 15-file production tree is intact.

## What is the next step

Per v1.2 AMEND 14:

1. **Musyawawah 333-AGI → 555-ASI → 888-APEX** on the v1.2 diff. 333 reviews schema, 555 audits against existing substrate (Supabase, Drive, AAA, hermes state.db), 888 adjudicates constitutional claims (F5 privacy, F8 consent, F13 sovereignty).
2. After 555 audit passes, 888 considers ratification path (DRAFT_AWAITING_F13 → DRAFT_AWAITING_F13 with shadow comparison → F13_SEAL).
3. After ratification, the full v1.2 design doc is produced (v1.1 + this diff + claim-substrate walkthrough).
4. Then re-align the 3 held artefacts to v1.2.
5. Then dry-run Syed-as-pilot as a *shadow projection comparison* in `/root/.hermes/cache/scratch/pilot_S01/` only — no F5 content migrated, no production write, until 555 audit sign-off.

## What is the canonical entry point for the design now

- **v1.1 design doc** — `/root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.1.md` (SUPERSEDED, kept for diff history)
- **v1.2 amendments diff** — `/root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.2-AMENDMENTS.md` (current, DRAFT_AWAITING_F13)
- **v1.1 artefacts (held)** — `/root/AAA/scripts/person_validate/person_validate.py`, `/root/AAA/scripts/person_pilot/migrate.py`, `/root/AAA/cockpit/musyawarah/2026-10-06-person-file-design/README.md`
- **Pilot comparison fixture** — `/root/.hermes/cache/scratch/pilot_S01/person.v1.yaml.v1.1-era` (was previously at `/root/memory/people/SYED/person.v1.yaml`; moved here per F13 "do not migrate" directive)

---

*Filed 2026-10-06 by HERMES under F13 verdict review. No mutation to production state. No canonization. DRAFT_AWAITING_F13.*
*DITEMPA BUKAN DIBERI ⚒️*
