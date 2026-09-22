# CHRON Observability — Reconciliation Repair (Task 0)

> **Date:** 2026-09-21 (MYT) · **Host:** KVM8 (forge) · **Author:** subagent (repair lane)
> **Scope:** `/root/scripts/chron_personal/task0_reconciliation.py` (owned), new test + probe files (owned), `/root/.hermes/cron/state/chron_personal/task0_latest.json` (owned)
> **Not touched:** anything under `/root/chron/` or `/root/AAA/scripts/` (other agents own those). The FQ surface was read only.
> **Doctrine:** the pessimist's rule — two independent observers who disagree are INFORMATION. The bug was the silence, not the difference.

---

## 0. STATUS

| Item | State |
|---|---|
| False positive (B) | **FIXED** — schedule-aware classification; only `MISSED` is an alarm |
| Undeclared detection (C) | **FIXED** — windowed, scheduler-dispatched, tombstone-aware; verdict on `39c828068dab` below |
| Silent contradiction (A) | **FIXED** — `surface_reconciliation` block + `SURFACE_DISAGREEMENT` finding class; peer never rewritten |
| Alarm removed? | **NO.** No alarm class was deleted. `INERTIA` still fires — now only when a job was genuinely due and did not run, at **HIGH** (was INFO) |
| Service exit | `ExecMainStatus=0` after manual run (proof e) |
| Tests | `python3 test_task0_classifier.py` → **Ran 40 tests … OK** (exit 0) |
| Probe | `python3 probe_task0_reconciliation.py` → **11/11 checks passed** (exit 0) |

---

## 1. CORRECTIONS TO THE BRIEF (measured, not assumed)

The brief was right on (A) and (B). Two of its premises on (C) do not survive measurement:

1. **"whether 'fired' means 'has an output file'"** — it did **not**. The pre-fix detector read `executions.db`, never the output directory:
   `fired_not_declared = executed_ids - all_declared_ids`, where `executed_ids` came from `SELECT … FROM executions WHERE claimed_at >= ?`.
   The real defect was **timezone-blind window arithmetic**, not artifact-existence. Proven in §3.
2. **"39c828068dab … is either a genuinely undeclared job or a stale output directory"** — it is neither of those two options as posed. It is a **genuinely undeclared job (`amin-acl-weekly-checkin`) that really executed — on 2026-09-20 at 20:00 MYT, the previous day**, i.e. outside the window under test. The output directory was a red herring; the execution row is the evidence. Verdict in §4.

Also worth recording: the pre-fix `executions_today=17` at 06:50 was **inflated**: 17 = **6 leaked previous-evening rows + 11 true in-window rows** (measured, §3).

---

## 2. HOW THE CLASSIFIER WORKED — BEFORE vs AFTER

### 2.1 BEFORE (pre-fix, verbatim from the backed-up source)

```python
def today_start_utc() -> str:
    midnight_myt = now_myt().replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight_myt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
...
cutoff = today_start_utc()          # '2026-09-20T16:00:00Z'
rows = conn.execute("... WHERE claimed_at >= ? ...", (cutoff,))
...
fired_not_declared  = executed_ids - all_declared_ids
declared_not_fired  = declared_ids - executed_ids        # ← the whole defect
```

Plainly stated, the three computations were:

- **'fired'** = a row exists in `executions.db` whose `claimed_at` is `>=` the cutoff **as a lexicographic string comparison**, where stored values carry a `+08:00` offset and the cutoff carries `Z`.
- **'declared'** = `id` present in `jobs.json` under `jobs` (enabled or disabled).
- **'did not fire'** = `declared_enabled_ids − executed_today_ids`. It asked *"has it fired today"* and **never asked "was it due to fire yet"**.

Three consequences, all measured today:

| # | Mechanism | Effect |
|---|---|---|
| 1 | `'2026-09-20T20:00:11+08:00' >= '2026-09-20T16:00:00Z'` → `True` at character 11 (`'2' > '1'`) | yesterday's 16:00–23:59 MYT runs counted as *today*; `executions_today` inflated 11 → 17 |
| 2 | membership test with no schedule awareness | every daily job scheduled **after** the 06:50 run reported "did not fire", every day, forever |
| 3 | no cross-check against the FQ surface | two surfaces could hold opposite verdicts, silently |

### 2.2 AFTER (v0.2.0) — what the classifier now is

- **Window** — `day_start_myt(now)` … `now`, compared as **aware `datetime`s** (`parse_ts` → `datetime.fromisoformat`, offset-aware). Raw SQL is pre-filtered only with an offset-agnostic date floor `today−2d` (can over-include, never under-include); precision is applied in Python. `reconcile()` **re-enforces the invariant** on whatever list it is handed and reports `executions_outside_window_ignored`.
- **'fired'** — a row with `source='builtin'` (scheduler-dispatched) and `claimed_at` inside the window. `source='direct'` on-demand runs are reported separately as `ON_DEMAND_EXECUTIONS` (INFO) and never reconciled against `jobs.json`.
- **Per-job schedule state** (each job against **its own** schedule, 5-field cron parsed in-module, no new dependency):
  `FIRED` · `MISSED` (due time passed + 30 min grace, nothing ran — **the only alarm**) · `PENDING_TODAY` (due later today) · `NOT_DUE_TODAY` (schedule excludes today) · `PENDING_NEXT` (interval job, `next_run_at` in the future) · `UNKNOWN_SCHEDULE` (unprovable → its own HIGH finding, never silently "missing").
  Grace is 30 min because real dispatch lag was observed (docforge `0 6 * * *` fired 06:18 today).
- **'did not fire'** — only `MISSED`. Legacy key `summary.declared_not_fired` is retained but now equals the corrected `MISSED` set; the probe asserts the two agree so a stale consumer cannot read the old meaning back.
- **Independent witnesses kept separate** — output directories are reported as `output_dir_without_execution` with the note *"An output directory persists forever and is NOT evidence that the job executed in the window under test."* Nothing in the alarm path reads a directory.
- **Schedule witness** — the parsed cron expression is cross-checked against the scheduler's own `next_run_at`; disagreement → `SCHEDULE_WITNESS_DRIFT` (INFO), `next_run_at` in the past → `SCHEDULE_OVERDUE` (HIGH).

---

## 3. PROOF (a) — BEFORE / AFTER, false positives reclassified

**BEFORE**, today's real service runs (journal, verbatim):

```
Sep 21 06:50:22 forge python3[1624260]: CHRON Task 0 — 2026-09-21
Sep 21 06:50:22 forge python3[1624260]:   Executions today: 17
Sep 21 06:50:22 forge python3[1624260]:   Severity: CRITICAL
Sep 21 06:50:22 forge python3[1624260]:   [CRITICAL] Jobs fired but absent from jobs.json: {'39c828068dab'}
Sep 21 06:50:22 forge python3[1624260]:   [INFO] Enabled jobs that did not fire today (may be weekly/monthly): {'canary-iron-radar', 'b7943df5bad1', '0a40f4cc66fe', '3e40c50f0ca2', '8313453a73a7'}
```
```
Sep 21 11:21:21 forge python3[2013044]:   Executions today: 26
Sep 21 11:21:21 forge python3[2013044]:   Severity: CRITICAL
Sep 21 11:21:21 forge python3[2013044]:   [CRITICAL] Jobs fired but absent from jobs.json: {'08ef9da87d09', '39c828068dab'}
Sep 21 11:21:21 forge python3[2013044]:   [INFO] Enabled jobs that did not fire today (may be weekly/monthly): {'b7943df5bad1', '3e40c50f0ca2', 'canary-iron-radar'}
```
(Note the second run only minutes later: three of the "missing" jobs had fired in the meantime and the *remaining* "missing" set simply changed shape. An alarm whose output is a function of the clock is not an alarm.)

**The old window, quantified** (measurement of the leak):

```
at 06:50 the OLD filter reported executions_today=17
  OLD-filter rows at 06:50 : 17
  of those, truly outside  : 6
  true in-window at 06:50  : 11
  identity 17 = 6 leaked + 11 real -> CONSISTENT
```
The 6 leaked rows were yesterday-evening MYT runs: `a39cfb467193 19:16`, `b1ee87971b9f 20:00`, `39c828068dab 20:00`, `161c0d5e0d0c 21:15`, `canary-arifflow-governance-digest 22:00`, `99659c39430c 23:45`.

**AFTER** — same five jobs, same instant (06:50:22 MYT), repaired classifier (probe P4, verbatim):

```
canary-iron-radar '0 12 * * 5' at 06:50 -> NOT_DUE_TODAY (due_today=[])
b7943df5bad1 '17 3 * * 0' at 06:50 -> NOT_DUE_TODAY (due_today=[])
0a40f4cc66fe '0 9 * * 1' at 06:50 -> PENDING_TODAY (due_today=['09:00'])
3e40c50f0ca2 '0 14 * * *' at 06:50 -> PENDING_TODAY (due_today=['14:00'])
8313453a73a7 '15 7 * * *' at 06:50 -> PENDING_TODAY (due_today=['07:15'])
```
```
[PASS] P4b replay at 06:50: no false MISSED, no false DRIFT
        missed=[] fired_not_declared=[] pending=['161c0d5e0d0c','3e40c50f0ca2','99659c39430c']
        not_due=['b7943df5bad1','canary-arifflow-governance-digest','canary-iron-radar']
```
Two of the five were never due today at all (Friday and Sunday schedules, seen on a Monday); three had fire times **after** the run. None is `MISSED`.

**Live run of the repaired script / service** (2026-09-21 11:30:31 MYT, verbatim):

```
CHRON Task 0 — 2026-09-21 (v0.2.0)
  Window: 2026-09-21T00:00:00+08:00 -> 2026-09-21T11:30:31.090223+08:00
  Declared enabled: 15
  Executions today: 19 (on-demand: 1)
  Completed: 9
  Failed: 0
  Delivered: 14
  Fired but not declared: []
  MISSED (due today, did not fire): []
  PENDING_TODAY (due later today): ['161c0d5e0d0c', '3e40c50f0ca2', '99659c39430c']
  PENDING_NEXT (interval, future): []
  NOT_DUE_TODAY (schedule excludes today): ['b7943df5bad1', 'canary-arifflow-governance-digest', 'canary-iron-radar']
  UNKNOWN_SCHEDULE: []
  Severity: INFO
  RECONCILIATION task0=INFO vs fq=OPTIMAL (fq=1.5675675675675675, age=1.1 min) -> AGREE
  [INFO] ON_DEMAND_EXECUTIONS: 1 in-window executions were on-demand (source != 'builtin'); they are not scheduled fires and are not reconciled against jobs.json
```

`08ef9da87d09` — reported CRITICAL by the pre-fix 11:21 run — is `source='direct'`, `scheduled_instant=NULL`, no output directory: an **on-demand** execution with no schedule to reconcile. It is now INFO, not drift. That is a second false positive in the same alarm, found while fixing the first.

## 3b. PROOF (b) — the two required test cases

`python3 /root/scripts/chron_personal/test_task0_classifier.py` → `Ran 40 tests in 0.250s / OK`

```python
def test_T1_job_at_2300_is_not_flagged(self):
    """A job due at 23:00 is PENDING_TODAY at 06:50, never MISSED."""
    j = job("attention-closure", "attention-closure", "45 23 * * *")
    state, ev = T0.classify_job(j, [], self.NOW_0650)
    self.assertEqual(state, "PENDING_TODAY", ev)
    self.assertNotEqual(state, "MISSED")
    self.assertEqual(ev["due_times_today_myt"], ["23:45"])
    self.assertIn("window still OPEN", ev["equations"])

def test_T2_job_at_0200_that_did_not_fire_is_flagged(self):
    """A job due at 02:00 with no execution is MISSED (window closed)."""
    j = job("vps-backup", "VPS Backup", "0 2 * * *")
    state, ev = T0.classify_job(j, [], self.NOW_0650)
    self.assertEqual(state, "MISSED", ev)
    self.assertIn("window CLOSED with no fire", ev["equations"])
```
Plus: `PENDING_TODAY` at 06:50 for a 06:45 job (grace), `NOT_DUE_TODAY` for `0 12 * * 5` on a Monday and `17 3 * * 0` on a Monday, `PENDING_TODAY` for `0 9 * * 1` on a Monday 06:50, live `MISSED` → `INERTIA` at HIGH (asserted not removed), the timezone seam test against a real temp SQLite DB, the disagreement-grading tests, and the job-shape contract test.

## 4. PROOF (c) — VERDICT ON `39c828068dab`

**VERDICT: a genuinely undeclared job that really executed — but NOT inside the window under test.** Both halves are independently established; neither is a guess.

The execution row that decides it (quoted from `executions.db`, re-derived by probe P10):

```
exec id      : 4bf4e08a52a44296a0dc2c13c9d64ba2
job_id       : 39c828068dab
source       : builtin                      ← scheduler-dispatched, not on-demand
status       : completed
claimed_at   : 2026-09-20T20:00:11.157385+08:00   ← 2026-09-20 20:00 MYT (YESTERDAY)
started_at   : 2026-09-20T20:00:11.765903+08:00
finished_at  : 2026-09-20T20:03:06.240692+08:00
delivery_outcome : failed
scheduled_instant: 2026-09-20T12:00:00+00:00       ← = 20:00 MYT schedule
```
```
[PASS] P10 verdict on 39c828068dab
        verdict=UNDECLARED_NOT_FIRED_IN_WINDOW
        in jobs.json: NO | tombstoned: NO | executions=1 | in window(2026-09-21T00:00:00+08:00): 0
```

Identity of the job (from `/root/.hermes/cron/output/39c828068dab/2026-09-20_20-02-21.md`):
`# Cron Job: amin-acl-weekly-checkin`, schedule `0 20 * * 0` ("every sunday 8pm"), `deliver=telegram:8798431893`. It was **declared when it ran** — sessions on 2026-09-18/19 dump its full record from `jobs.json`. It is absent from `jobs.json` today (35 jobs, `grep -c` = 0), absent from **every** `jobs.json*` backup on disk, and **absent from `tombstones.jsonl`** — i.e. it was removed without a tombstone row, which is the exact failure that record exists to prevent. The scheduler itself agrees it is gone: `"Job with ID or name '39c828068dab' not found."`

So the honest answer to the brief's question:

- **undeclared?** YES — real, and it is a **deletion-hygiene finding** (silent removal, no tombstone), not a today-fire finding.
- **executed in the window under test?** NO — its only execution is 2026-09-20 20:00 MYT, 4 h *before* the window (which starts 2026-09-21 00:00 MYT / `2026-09-20T16:00Z`). It was swept in by the lexicographic compare (§2.1 defect 1). Its output directory is likewise a stale artifact, now reported only as `output_dir_without_execution`.
- **what this classifier now does with it:** it appears under `undeclared_historical` (last fire predates the window) as INFO with the row attached, and it will raise CRITICAL **only** if it fires again inside a window. If a tombstone is written for it, it moves to `fired_declared_then_removed`. Nothing about it is dropped or hidden.

## 5. PROOF (d) — the contradiction is now surfaced, not silent

**The silence, measured:** `grep -c 'fq_last_state\|global_fq\|global_verdict' task0_reconciliation.py.bak-20260921T112601` → **0**. And the peer never read task0 either: `grep -c 'task0' /root/chron/chron_ariflow_bridge.py` → **0**. Two observers, mutually blind, no disagreement field anywhere.

**Real inputs through the repaired path** (probe P8, verbatim):

```
[PASS] P8 contradiction is now surfaced (and was silent before)
        pre-fix episode: task0_latest.json.bak-20260921T112601 severity='CRITICAL' observed_at=2026-09-21T03:23:45.187209Z
        live peer: verdict='OPTIMAL' fq=1.5675675675675675 updated_at=2026-09-21T03:29:23.205474Z
        compare_surfaces -> DISAGREE gap=2
        raise -> [('SURFACE_DISAGREEMENT', 'CRITICAL')] overall=CRITICAL
        the pre-fix file contains the string 'fq'? NO (no field referenced the peer surface)
```

**The live, agreeing case** (current state, probe P7):

```
[PASS] P7 surface block present; peer surface never written by task0
        agreement='AGREE' task0='INFO' peer='OPTIMAL' fq=1.5675675675675675
        peer_state_age_minutes=0.6
        peer sha256 6bc5fee803734889... -> 6bc5fee803734889... (unchanged)
        peer keys=['actors', 'global_fq', 'global_verdict', 'updated_at']
        policy=Both surfaces are independent observers. Neither is rewritten to agree with the other;
               a disagreement is raised as its own finding class (SURFACE_DISAGREEMENT) so it can never be silent.
```

Design of the fix (doctrine: do not destroy the independent witness):
- task0 now **reads** `/root/chron/data/fq_last_state.json` and **never writes** it (probe hashes it before/after a run; it also asserts the peer file has only the bridge's four keys).
- Every report carries a `surface_reconciliation` block (also `observations[1]` and a `claims` row: *"this reconciliation agrees with the independent FQ surface"* → `VERIFIED` / `CONTRADICTED` / `UNKNOWN`).
- Disagreement becomes its **own severity class** `SURFACE_DISAGREEMENT`, graded by distance: gap 2 (one side all-clear, the other CRITICAL/FAILED) → CRITICAL; gap 1 (clean vs elevated) → HIGH. Both agree-not-ok (e.g. HIGH vs DEGRADED) is `AGREE` — same side of the line, no class raised. Noise control, not alarm deletion.
- Unreadable peer → `SURFACE_UNREADABLE` (HIGH), never a pass. Peer state older than 6 h → `PEER_STALE` (INFO): a stale witness is reported as *no comparison asserted*, not as agreement.
- **No verdict was edited to match the other.** The FQ surface is untouched; task0's severity is computed from task0's own evidence.

## 6. PROOF (e) — service exit status after a manual run

```
# systemctl show -p ExecMainStatus -p ExecMainStartTimestamp -p ExecMainExitTimestamp chron-task0-reconciliation.service
Type=oneshot
ExecMainStartTimestamp=Mon 2026-09-21 11:30:30 +08
ExecMainExitTimestamp=Mon 2026-09-21 11:30:31 +08
ExecMainStatus=0

# systemctl show -p ExecMainStatus --value chron-task0-reconciliation.service
0
```
`main()` returns 0 unconditionally; a bad `--at` is reported and still exits 0; the prediction-store step stays best-effort. The probe's P1 re-checks this on every run.

---

## 7. FILES

| File | Action |
|---|---|
| `/root/scripts/chron_personal/task0_reconciliation.py` | **modified** v0.1.0 → v0.2.0 (backup `…py.bak-20260921T112601`) |
| `/root/scripts/chron_personal/test_task0_classifier.py` | **new** — 40 tests, exit 0 |
| `/root/scripts/chron_personal/probe_task0_reconciliation.py` | **new** — 11 independent checks, exit 0 |
| `/root/.hermes/cron/state/chron_personal/task0_latest.json` | regenerated by the repaired script (backup `…json.bak-20260921T112601`, kept) |

Backups are timestamped and were not deleted. Run order for a re-check: `python3 test_task0_classifier.py` → `python3 probe_task0_reconciliation.py`.

---

## 8. WHAT I COULD NOT DO

1. **Prove that `39c828068dab` was deleted *by anyone in particular*, or when.** No `jobs.json*` backup on disk ever contained it, and `tombstones.jsonl` has no row for it, so the deletion is undated and unattributed. What is proven: it was declared when it ran (2026-09-18/19 session dumps), it ran 2026-09-20 20:00 MYT, and it is undeclared and un-tombstoned now.
2. **Write the tombstone.** `tombstones.jsonl` is outside my ownership (`/root/.hermes/cron/` scheduler surface — not in my file list), so the silent-deletion defect is *surfaced* (it now shows up as `undeclared_historical`) but **not remediated**. Writing the row is a one-line append for whoever owns the tombstone record.
3. **Fix the emitting surfaces.** I did not touch `/root/chron/` (the FQ writer) or any other surface that reads `task0_latest.json`. The reconciliation is now *carried in the report*; whether a downstream consumer acts on `SURFACE_DISAGREEMENT` (e.g. the 06:50 timer's delivery path) is unverified — I did not test alert delivery, only classification.
4. **Reconstruct the 06:50 episode exactly.** The 06:50 write of `task0_latest.json` was overwritten **at 11:23:45, before I took my backup — by a writer I could not attribute** (the service itself last ran 11:21:20; no cron job or timer invokes task0 other than the 06:50 timer, so the 11:23:45 write most likely came from an interactive agent session running the script by hand). What I have of the 06:50 episode is the journal output, quoted verbatim below and matching the brief's own quote. My 06:50 replay uses today's `jobs.json` + `executions.db` restricted to the 06:50 window: window membership is historical-real, the schedule fields (`next_run_at`/`last_run_at`) are current. Classification of the five jobs is unaffected (all are cron jobs, parsed from their expressions).
5. **Measure the FQ surface's variance.** In my three observations today its `global_verdict` was `OPTIMAL` (fq 1.214 → 1.4359 → 1.5676); `loop_log.jsonl` carries no `global_verdict` history, so I cannot say whether that verdict ever varies. If it is effectively single-valued, disagreement can only ever be raised *by task0's side* — a property of the peer witness, not of my fix, and worth someone else's probe.
6. **Establish `UNKNOWN_SCHEDULE` behaviour on real input.** No enabled job currently has an unparsable expression, so that branch is covered by unit test only, not by live data.
7. **Not verified:** that `INERTIA`→HIGH (raised from INFO) will not be delivered as noise by whatever consumes this report. The severity change is deliberate — a job that was due and did not run is a real signal — but downstream routing was not in scope and I did not test it.

One more honest note: the 11:21 and 11:23 pre-fix runs today are **not** two observers disagreeing — they are the same observer re-run. The genuine disagreement is task0 vs FQ, and its two live readings (07:15 `OPTIMAL` / 1.214 vs the 06:50 `CRITICAL`) are 24 m 49 s apart. Both files are preserved as they were found; neither was edited.
