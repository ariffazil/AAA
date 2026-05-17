# workflow-session-cycle — Execution Summary

> Generated: 2026-05-17 | Owner: arif-fazil | Version: 1.0.0

## Purpose

Standard session loop for all non-trivial tasks.
Every agent task follows: INIT → REASON → PLAN → ACT → OBSERVE → REFLECT → REPEAT/FALLBACK → MEMORY → PERSIST.

## Key Design Decisions

- **Branching at step-05:** REFLECT branches to REPEAT or FALLBACK based on worked/failed flag.
- **Branching at step-06:** LOOP continues or exits based on continue_flag.
- **Branching at step-07:** FALLBACK either finds alternative → back to ACT, or exits → step-08.
- **Recovery:** Resume from last validated gate, not from scratch.
- **Trace mandatory:** Every step writes to artifacts/ before gate advances.

## Gates

- `gates/step-00.json`: INIT — verify: grep session_id state.json
- `gates/step-01.json`: REASON — verify: test -f artifacts/step-01-reason.json
- `gates/step-02.json`: PLAN — verify: grep plan_id state.json
- `gates/step-03.json`: ACT — verify: ls artifacts/step-03-*
- `gates/step-04.json`: OBSERVE — verify: grep result_status state.json
- `gates/step-05.json`: REFLECT — verify: test -f artifacts/step-05-critique.md
- `gates/step-06.json`: REPEAT-LOOP — verify: grep continue_flag state.json
- `gates/step-07.json`: FALLBACK — verify: grep revised_plan_id state.json
- `gates/step-08.json`: MEMORY — verify: grep memory_id state.json
- `gates/step-09.json`: PERSIST — verify: grep entry_id state.json
