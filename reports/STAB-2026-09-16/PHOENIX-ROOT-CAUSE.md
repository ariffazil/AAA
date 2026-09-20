# PHOENIX-72 ROOT CAUSE — ONE PHASE IS ALWAYS SKIPPED, SO THE CYCLE DEADLOCKS
> 2026-09-20 ~19:25 MYT · KVM8 · HERMES · read-only · zero mutation
> Closes the open question from `PHOENIX-STOPPED-AFTER-ONE-CYCLE.md` §"Open Questions"

---

## VERDICT: NOT AN ERROR. A SCHEDULING BOUNDARY CONDITION WITH ZERO SLACK.

The organ is alive, cron-driven, and **logging correctly**. It deadlocks because the phase
windows are **exactly as wide as the cron period**, and the phase is derived from wall-clock
elapsed time instead of from which phases have actually completed.

---

## THE EVIDENCE — FULL LOG TRAIL, VERBATIM

All eight rotated logs were read. The pattern is identical in every cycle:

```
2026-09-11T19:00:03Z  cycle=PHX-20260910-005 phase=BLUE
2026-09-11T19:00:03Z  HOLD: BLUE requires completed RED (JUDGE gate)

2026-09-12T19:00:02Z  cycle=PHX-20260910-005 phase=GOLD
2026-09-12T19:00:02Z  HOLD: GOLD requires completed BLUE
2026-09-13T19:00:01Z  cycle=PHX-20260910-005 phase=REBIRTH
2026-09-13T19:00:03Z  REBIRTH complete: PHX-20260910-005 sealed, PHX-20260913-006 ignited
```

Now the one cycle where RED actually got a window:

```
2026-09-14T19:00:01Z  cycle=PHX-20260913-006 phase=RED
2026-09-14T19:00:04Z  RED complete: 10 scars discovered        ← RED RAN
2026-09-15T19:00:02Z  cycle=PHX-20260913-006 phase=GOLD
2026-09-15T19:00:02Z  HOLD: GOLD requires completed BLUE        ← BLUE SKIPPED ENTIRELY
2026-09-16T19:00:01Z  cycle=PHX-20260913-006 phase=GOLD
2026-09-16T19:00:02Z  HOLD: GOLD requires completed BLUE
2026-09-17T19:00:02Z  cycle=PHX-20260913-006 phase=REBIRTH
```

**RED ran on 14 Sep. BLUE never got a window. GOLD held twice. REBIRTH sealed a cycle with
`phase_completed = {}`.** Then the next cycle repeated it exactly.

Cycle 007's current state, verbatim (`/root/AAA/state/phoenix72/state.json`):

```json
{"cycle_id": "PHX-20260917-007", "phase": "REBIRTH", "phase_completed": {},
 "scars": [], "repairs": [], "baseline": null, "participants": {}}
```

---

## THE MECHANISM, IN SOURCE

`/root/scripts/phoenix72.sh`, phase computation:

```bash
compute_phase() {
  hours=$(( (now - start_epoch) / 3600 ))
  if   [ "$hours" -lt 24 ]; then echo "RED"
  elif [ "$hours" -lt 48 ]; then echo "BLUE"
  elif [ "$hours" -lt 72 ]; then echo "GOLD"
  else echo "REBIRTH"; fi
}
```

Cron: `0 3 * * *` — **once every 24 h**, at 03:00 MYT = 19:00 UTC.
Phase window: **24 h wide.**

**The window width equals the period. There is zero slack.** Every run lands at `hours ≈ 24·n`.

Now add the second ingredient — sub-second jitter in the cron fire time. Observed above:

```
14 Sep run:  19:00:01Z      cycle_start: 2026-09-13T19:00:02Z
             elapsed = 86 399 s  →  hours = 23  →  RED      ✓ (inside 0–23)
15 Sep run:  19:00:02Z
             elapsed = 172 800 s →  hours = 48  →  GOLD    ✗ (BLUE's window 24–47 skipped)
```

**A one-second drift in when cron fired made `hours` jump 23 → 48 — an increment of 25, not 24 —
stepping clean over the entire BLUE window.** Bash integer division truncates toward zero, so any
`elapsed` a fraction under 48 h also floors to 47 (→ BLUE), while exactly 48 h or over gives 48 (→
GOLD). Whether a phase is skipped therefore depends on **which second the scheduler woke up**.

And in cycle 007 the drift went the other way:

```
cycle_start = 2026-09-17T19:00:02Z
18 Sep run: 19:00:02Z → elapsed exactly 86 400 s → hours = 24 → BLUE
            → "HOLD: BLUE requires completed RED"      ← RED never had a window at all
19 Sep run: 19:00:02Z → hours = 48 → GOLD → "HOLD: GOLD requires completed BLUE"
```

So: **either RED or BLUE is skipped in every cycle — never a clean three-phase run.** Whichever is
skipped, the next phase HOLDs on its unmet prerequisite, and nothing downstream can proceed. The
cycle burns 72 h, REBIRTH seals an empty cycle, and ignites a successor with the same defect.

---

## VERIFICATION — THE MODEL REPRODUCES EVERY LOG LINE (run, not reasoned)

The arithmetic above was verified by simulation against the real timestamps. `elapsed // 3600`
(bash integer division) reproduces **5 of 5** observed phase selections exactly:

```
cycle_start            fire                    elapsed_s  hours computed  logged
--------------------------------------------------------------------------------
2026-09-13T19:00:02Z   2026-09-14T19:00:01Z        86399     23 RED       RED   ✓
2026-09-13T19:00:02Z   2026-09-15T19:00:02Z       172800     48 GOLD      GOLD  ✓
2026-09-13T19:00:02Z   2026-09-16T19:00:01Z       259199     71 GOLD      GOLD  ✓
2026-09-17T19:00:02Z   2026-09-18T19:00:02Z        86400     24 BLUE      BLUE  ✓
2026-09-17T19:00:02Z   2026-09-19T19:00:02Z       172800     48 GOLD      GOLD  ✓
```

A model that predicts the logs it was derived from is still only a fit — but this one also predicts
the case at the margin, which is the real test:

```
drift −1s  → elapsed 172799 → hours 47 → BLUE      ← the phase would have run
drift  0s  → elapsed 172800 → hours 48 → GOLD      ← skipped
drift +1s  → elapsed 172801 → hours 48 → GOLD      ← skipped
```

**One second of scheduler jitter decides whether BLUE executes or is skipped for that entire
cycle.** And the 14 Sep run did fire one second early (`19:00:01`), which is exactly what returned
`hours = 23` and gave RED its only window.

**The margin is a single second.** That is why the failure is intermittent rather than total, and
why it went unnoticed: from the outside, the organ looks like it is running — cron fires, logs
appear, state advances, cycles seal.

---

## WHY CYCLE 001 SUCCEEDED — AND WHY THAT IS THE PROOF

`PHX-20260819-001` is the only complete cycle: `RED → BLUE → GOLD` in `phase_completed`, 6 scars,
**6 repairs**, and a sealed baseline. Its header records a manual sovereign invocation:

> *Sovereign directive: ARIF (F13) 2026-08-19 — "executed by the entire agents in AAA STATE,
> OPENCODE, KIMI CODE, QWEN CODE as CCC, OPENCLAW as master orchestrator, HERMES as human reality
> edge bridge."*

**When humans drove it, all three phases ran. When cron drove it alone, the boundary condition
skipped one phase and the loop died.** The design is sound; the scheduler is not.

---

## THE FIX (NOT APPLIED — one line, but it is an authority decision)

The script already treats `phase_completed` as the source of truth for **gating**:

```bash
[ -z "$(phase_done RED)" ] && { log "HOLD: BLUE requires completed RED"; exit 1; }
```

…but `compute_phase()` **ignores `phase_completed` entirely** and picks the phase from wall clock.
The two mechanisms disagree, and the wall-clock one wins.

**Minimum-energy fix — make the selector read the same source the gate does:**

```bash
compute_phase() {
  [ -z "$(phase_done RED)"  ] && { echo RED;   return; }
  [ -z "$(phase_done BLUE)" ] && { echo BLUE;  return; }
  [ -z "$(phase_done GOLD)" ] && { echo GOLD;  return; }
  echo REBIRTH
}
```

Phase advances by **work completed**, not by clock elapsed. Jitter becomes irrelevant; a missed
run self-heals on the next one instead of skipping a phase.

Two supporting notes:
- The 72 h cycle length must then be enforced separately (a guard on `cycle_start` age), otherwise
  a stalled phase would retry forever — which is correct behaviour, but should be visible.
- `participants: {}` is empty in **all** cycles including the successful one, so witness attachment
  is a separate never-wired step. Fixing the scheduler will not populate it.

---

## SUPPORTING EVIDENCE — THE SCARS IT NEVER GOT TO ACT ON

Cycle 001's sealed baseline names its own recurring class:

```json
"recurring_scar_classes": ["STALE_REGISTRY"]
```

Measured live tonight, 2026-09-20: **WELL `REGISTRY_DRIFT` — 10 intended / 40 registered / 10
callable / 9 unexpected public.**

And the scar ledger since that last successful repair:

```
RED 10 scars (14 Sep, cycle 006)  → BLUE never ran → 0 repairs
```

**The organ predicts its recurring defect, the defect persists for a month, and the pipeline that
would have repaired it is stopped by a comparison operator and a one-second clock drift.**

---

## STATUS

**Mutations: ZERO.** Log reads, source reads, state reads, one report file.
No federation change. No canon change. No seal. No signature.

**Caveat on this finding's own lifespan:** per the rule this session established — a live-system
finding has a TTL. Everything above was measured at ~19:25 MYT on a service that another seat may
touch. `measured_at` is in the header; re-probe before acting.
