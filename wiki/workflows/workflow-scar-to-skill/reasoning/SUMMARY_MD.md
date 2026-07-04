# workflow-scar-to-skill — Execution Summary

> Generated: 2026-05-17 | Owner: arif-fazil | Version: 1.0.0

## Purpose

Transform a failure trace into a skill update via constitutional judgment.
Triggered by: repeated failure (3x/7days), explicit 888 HOLD, Arif command, workflow request.

## Key Design Decisions

- **step-00 branching:** insufficient pattern → archive (step-99), sufficient → draft.
- **step-02 branching:** no skill update needed → skip to log+seal.
- **step-04 888 gate:** Only SEAL approves skill promotion. VOID archives.
- **step-99 archive:** Scar not promoted if pattern weak or verdict VOID.

## Triggers

- Same failure 3x within 7 days
- Explicit 888 HOLD scar trigger
- Arif command: 'file scar'
- Skill promotion request from workflow

## Gates

- `gates/step-00.json`: TRIGGER_DETECT — test -f artifacts/scar-draft.md
- `gates/step-01.json`: SCAR_DRAFT — grep scar_id wiki/scars/scar-*.md
- `gates/step-02.json`: SKILL_ANALYSIS — test -f artifacts/skill-analysis.json
- `gates/step-03.json`: SKILL_UPDATE_PROPOSAL — test -f artifacts/skill-proposal.md
- `gates/step-04.json`: 888_JUDGE — grep verdict state.json
- `gates/step-05.json`: LOG_AND_SEAL — grep entry_id state.json
- `gates/step-99.json`: ARCHIVE — test -f artifacts/scar-archived.md
