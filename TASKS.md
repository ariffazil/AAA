<!-- SOT-MANIFEST
owner: aaa-maintainer
workflows_version: 1.0.0
scope: /root/AAA
-->

# TASKS.md — AAA Execution Loop

> **How AAA does things. How AAA escalates. How AAA logs.**

---

## 1 · The Governed Loop

```
SENSE       runtime / human / agent notices something     → Issue
MODEL       discussion, evidence, labels                  → structured understanding
PLAN        branch + PR                                   → concrete proposal
EVALUATE    CI + review                                   → doctrine + peers judge
AUTHORIZE   merge to main                                 → sovereign law update
ACT         Actions → A-FORGE                             → leased execution
REMEMBER    hash + Issue closure + logs                   → sealed memory
REFLECT     incidents / metrics                           → new Issues
```

## 2 · Branch Naming
| Type | Pattern | Example |
|---|---|---|
| Feature | `feat/<issue-n>-<slug>` | `feat/123-a2a-auth-hardening` |
| Fix | `fix/<issue-n>-<slug>` | `fix/456-cockpit-regress` |
| Doctrine | `doctrine/<slug>` | `doctrine/skill-canon-12` |
| Chore | `chore/<slug>` | `chore/update-deps` |

One Issue → one primary branch.

## 3 · Commit Message Rules

```
<type>(<scope>): <short description>     [max 72 chars]

[body — wrap at 100 chars, explain WHY]

REPO=ariffazil/AAA
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `forge(<scope>)`.

## 4 · Tags
`vYYYY.MM.DD[-SUFFIX]` ONLY. NEVER semver.

## 5 · Safety Checks (Pre-Mutation)
- [ ] `git status` clean or only intended
- [ ] On feature branch (NOT main)
- [ ] Branch references Issue ID
- [ ] Lease acquired if MUTATE-class
- [ ] `npm run build` passes
- [ ] `npm run lint` passes
- [ ] No secrets in diff
- [ ] No constitutional files touched (or 888_HOLD)

## 6 · Logging
Every mutation produces a receipt at `/root/forge_work/<name>-YYYY-MM-DD.md`.

Every SEAL-grade action seals to VAULT999 via `arifos_arif_seal`.

## 7 · Escalation Matrix
| Condition | Action | Tool |
|---|---|---|
| Reversible mutation | Proceed | (no escalation) |
| Irreversible mutation | 888_HOLD | Wait for Arif |
| A2A auth change | 888_HOLD + 888_JUDGE | `arifos_arif_judge` |
| Secret exposure | 888_HOLD + Telegram | Direct |
| Cross-repo change | 888_HOLD + Arif | Direct |
| CI failure | Diagnose | `github-ci-diagnose` |

## 8 · Human Input Requests
| Need | Channel | Wait time |
|---|---|---|
| 888_HOLD on irreversible | Telegram `@ASI_arifos_bot` or AAA cockpit HOLD button | Until ack |
| Constitutional question | AAA cockpit → 888 deliberation | Until SEAL |
| Operational question | Telegram direct | Async ok |

**Silence is HOLD, not SEAL.**

## 9 · Bootstrap Order
1. Read this `TASKS.md`
2. Read `AGENT.md`
3. Read `SKILL.md`
4. Read `/root/AGENTS.md` (global)
5. Read `FEDERATION_CONTRACT.md`
6. Initialize `arif_session_init`
7. Attest all 7 organs
8. Check `memory/` for carry-forward

## 10 · Self-Audit (Reflexion Loop)
```
000  ATTEST     : Read AGENT.md + SKILL.md + TASKS.md
111  SENSE      : `git status`, `forge_health_check`
333  REASON     : `arifos_arif_think mode=plan`
555  EMPATHIZE  : Who is affected?
666  HEART      : Risk + dignity + reversibility?
777  FORGE      : Dry-run. Lease if needed.
888  JUDGE      : `arifos_arif_judge` for irreversible
999  SEAL       : `arifos_arif_seal` to VAULT999
```

---

*License: AGPL-3.0 · Sovereign: Arif bin Fazil · DITEMPA BUKAN DIBERI*
