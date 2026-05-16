# agents/apex/

> APEX agent runtime-memory mirror — control-plane restore point.

## What this is

This directory is the git-backed mirror of `/root/.apex/` on the VPS runtime.
It exists so Apex can be restored from a clean workspace clone if needed.

## Relationship to AAA constitutional files

| File in AAA root | Role |
|------------------|------|
| `USER.md` | AAA's own constitutional operator file (F13 sovereign identity) |
| `memory/MEMORY.md` | AAA's own constitutional memory |

| File here | Role |
|-----------|------|
| `agents/apex/USER.md` | APEX-specific operator profile (mirrors `/root/.apex/USER.md`) |
| `agents/apex/MEMORY.md` | APEX runtime memory: VPS state, conventions, active holds |
| `agents/apex/SOUL.md` | APEX agent identity and character |
| `agents/apex/AGENTS.md` | Federation workspace orientation |
| `agents/apex/BOOTSTRAP.md` | Startup sequence |
| `agents/apex/IDENTITY.md` | Identity claims and epistemic tags |
| `agents/apex/FLOORS_BRIEF.md` | F1–F13 quick reference |

## Update rule

- Update `USER.md` / `MEMORY.md` here when VPS ground-truth materially changes
- Add `Observed: YYYY-MM-DD by Hermes` on every volatile section
- Keep facts dated and scoped — no vague generalisations

## Live source

During active execution, Apex reads from `/root/.apex/` on the VPS.
Git repo is the **restore point**, not the live source.

## Authority

- Repo home: `AAA/agents/apex/`
- Live path: `/root/.apex/`
- Owner: Muhammad Arif bin Fazil
- Authority: F13 SOVEREIGN — human veto is absolute

Last reviewed: 2026-05-05
