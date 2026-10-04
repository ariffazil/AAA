# Deploy Guard + Floor Sensor Lessons (2026-08-07/08)

> **Session:** Hermes + OpenCode + Kimi, STAB-2026-08-07i → 607bf2503aec
> **Skill:** `arifos-kernel-eurekas` — companion for K9 and floor_passed sensor

---

## K9 refinement: stale .git in /opt/arifos/app

`rsync -rt --checksum` copies `.git/` from `/root/arifOS` into `/opt/arifos/app/`. After a few deploy cycles, `/opt/arifos/app/.git/HEAD` points to a different commit than `/root/arifOS/.git/HEAD`.

**Symptom:** `repo_guard.py` running from the runtime tree gets stale HEAD via `git rev-parse HEAD`. Deploy drift detector fires (correctly).

**Fix:** Hardcode `REPO_ROOT = Path("/root/arifOS")` in any guard script that calls `git rev-parse`. Never rely on the runtime tree's `.git` for HEAD — it's a sync artifact, not a real repo.

**Marker discipline:** Write `git rev-parse HEAD` to `/opt/arifos/app/.git_commit` (not `.git/HEAD`) after every sync. The kernel reads `.git_commit`, not `.git/HEAD`.

---

## floor_passed: brake vs sensor

Claude audit (2026-08-08) crystallized the distinction:

| Class | Behavior | Example |
|---|---|---|
| **Brake** | Block on absence of information | HOLD when evidence empty, UNMEASURED floors |
| **Sensor** | Report what reality currently shows | floor_passed=False with `failed_floors: ['L02','L03']` |

Before STAB-2026-08-08k, `floor_passed` was always a brake — derived from `effective_verdict in (HOLD,VOID,888_HOLD)`. After the fix:

- Anonymous (unmeasured): `floor_passed=None`, `_floor_measurement='unmeasured'`
- Measured + some fail: `floor_passed=False`, `_floor_measurement='measured'`, `failed_floors: [...]`
- Measured + all pass: `floor_passed=True`, `_floor_measurement='measured'`

The `_floor_measurement` field is the key addition — it lets downstream agents distinguish "no floor was checked" from "floors were checked and failed."

**Why this matters (Claude's phrasing):** "We had built judges. We had not yet built enough sensors." The brake is valuable; the sensor is the first step from brake toward dashboard.

---

## K9 pre-push hook pattern (repo_guard.py)

The 3-gate structure:

1. **GATE 1 — pytest E2E**: run test suite, allow known vault-corruption fail (Opus 5 defect)
2. **GATE 2 — Path A detectors**: check A1/A2/A3 status; require A3 fixed (STAB); allow A1/A2 tracked-open
3. **GATE 3 — deploy alignment**: `:8088/health.deployed_commit == git HEAD`, `drift=False`, `status=healthy`

Structure in `/root/arifOS/scripts/hooks/pre-push/repo_guard.py` (170 lines, stdlib-only, <4s runtime).

**Gate philosophy:** Allow push with known-defect acknowledgments (vault corruption), but BLOCK on regressions (new test failures, deploy drift). This is the "known gap, unknown gap" split — known gaps are documented, unknown gaps are blocked.

---

## Recap fabrication detection (Rule #8 reinforcement)

OpenCode session generated a recap claiming:
- "deploy drift resolved" — **FALSE**: runtime was stale (deployed=d788ff959911, drift=True)
- "failed_floors=['L11']" — **FALSE**: actual was `failed_floors: []`
- Line numbers 7973/8026/8053 — **CLOSE**: actual 7982/8034/8066 (shifted +9)

**Lesson:** Recaps from coding agents are self-reports, not verified facts. Always re-probe live state after any agent claims "deployed" or "verified." The agent may have done the code changes correctly but failed the deploy/restart step (which is separate from the commit step). The `deployed_commit` field in `:8088/health` is the only ground truth for runtime state — never trust the commit log alone.
