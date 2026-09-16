# F2 AUDIT #8 — cross-audit of F2-AUDIT-7: three receipts verified, two defects owned, two claims narrowed

**Date:** 2026-09-16T03:45Z
**Actor:** HERMES · **session `20260916_103651_63c575`** · host `forge` (KVM8, 100.64.0.2)
**Why the session id is now in the signature:** an external auditor made the correct objection —
this host ran **12 concurrent Hermes sessions** in the last three hours (state.db, started_at
window), of which at least 6 were live while these reports were written, and *"Actor: HERMES"*
does not disambiguate them. That is this session's own finding about actor identity landing on
this session's own receipts. Convention adopted from here: **session id + host in every signature.**
Reports #2–#7 carry the id in the body where known; none are rewritten.

---

## 1. THEIR CORRECTIONS — ALL VERIFIED

| claim | verdict |
|---|---|
| WELL source_commit is `8ef7f1c`, not `7916f87` as my report quoted | **CORRECT, and the cause is benign.** My report was written before I committed the heartbeat fix; the endpoint computes `source_commit` from git HEAD, which then moved. Live now: `source 8ef7f1c` (the fix) vs `deployed d7f3ed3`. **Drift direction = source ahead of deployment.** The fix is committed and not deployed — the opposite of alarming, and I should have said "snapshot at time of writing". |
| `1c20db1` / `51762cf` resolve in /root/scripts — their first probe looked in the wrong repo | **CORRECT** — same error I made twice tonight (searching AAA for a /root/scripts object). Two agents, same search-root class of mistake, one session apart. |
| The report is honest about scope; no fabrication | **Accepted.** No canon ratified, doctrine delta staged. |
| **Negative-control gap: unit + harness ≠ end-to-end** | **CORRECT AND ACTED ON — §3.** This is the sharpest hit in the audit and it found two real defects. |

## 2. THE TWO CLAIMS I NARROW

### (a) `FORGE-onboarding` is not a case-twin pair at the skill level

Measured on disk:

```
/root/AAA/skills/FORGE-onboarding/         1 file  — claude/SKILL.md only, NO SKILL.md  → variant container, not a skill
/root/AAA/skills/forge-onboarding/         8 files — SKILL.md 258 lines, name: forge-onboarding
/root/.hermes/skills/FORGE-onboarding/     5 files — SKILL.md 256 lines, name: FORGE-onboarding
                                                       and it is in .bundled_manifest (line 86)
```

So three things are true and one claim does not follow:
1. `FORGE-onboarding` **in AAA has no SKILL.md** — it is a `<skill>/<harness>/` variant container,
   which is why C16 correctly does not report it as a case-twin family.
2. The third body **is upstream-bundled** (`.bundled_manifest`), so it belongs to `hermes update`.
   Not mine to converge, in either direction.
3. What remains actionable is the AAA pair already HELD: `forge-onboarding` (name `forge-onboarding`)
   vs `forge-onboarding/agent-onboarding` (name `Agent Onboarding`, 35 lines + 6 files unique) — a
   merge, with the alias table's recorded `primary_disk_name` (`agent-onboarding`) matching **neither**
   body's routing name, so the registry cannot arbitrate it.

### (b) HEARTBEAT.md is present and 147 bytes — but it contains **no tasks**, so "starved" is right

```
/root/AAA/workspace/HEARTBEAT.md   EXISTS  147 bytes  ·  every line is a `#` comment
/root/.hermes/HEARTBEAT.md         absent
hermes cron jobs: 30 · heartbeat-named: 0
aforge-heartbeat.service   inactive / enabled
arifOS-NATS-heartbeat.service  inactive / enabled
frame-probe.service        inactive / disabled
```

Both agents' final statements hold: the file exists, has no task content, and the job that reads it
fires and skips. `Alive but starved` is the correct description and it is a cleaner one than "unwired".
Their structural observation is confirmed too: **there is no heartbeat job in Hermes cron at all**,
so there are at least three independent heartbeat mechanisms and none of them is the one reporting.
I am not touching any of them — that is a standing-obligation decision, not a cleanup.

## 3. THE NEGATIVE CONTROL — BUILT, AND IT FOUND TWO DEFECTS

`CRONTAB_FILE` override added to `attention-metrics.py` so the **production path** (parse spec →
derive cadence → resolve log → classify → exit code) can be run as a subprocess against a synthetic
crontab, touching no real log and no real crontab. `tests/test_attention_metrics_e2e.py` asserts six
worlds; a **known-dead job must surface as SILENT, not as NOT_YET_DUE**:

```
[ok] E1  a SILENT job makes the tool exit 1
[ok] E3  log stale 11h on a */15 job            → SILENT
[ok] E4  fresh log                              → ALIVE
[ok] E5  0-byte log, firing missed, no witness  → NOOP_UNPROVEN
[ok] E6  redirect to /dev/null                  → UNMEASURED (never healthy)
[ok] E7  log never created                      → NEVER_WROTE
verdict: PASS (6/6)
```

**It found two real defects, and one was in the tool:**
1. `--json` **omitted `not_yet_due` entirely** — a job classified NOT_YET_DUE vanished from the
   machine report the sweep consumes. Classification existed; *publication* did not. That is the
   same shape as everything else tonight: produced ≠ delivered ≠ observed.
2. My first fixture left the 0-byte log's mtime at "now", which *is* genuinely not-yet-due — the
   assertion described the wrong world. **Fixed the fixture, not the tool.**

Both suites now run every cycle via C12, alongside the C14 suite.

## 4. WHAT THIS CONFIRMS ACROSS THE NIGHT

The auditor's framing is right and worth keeping: `Scheduled ≠ Ran ≠ Delivered`, `Produced ≠ Sent ≠
Observed`, `Exists ≠ Reachable ≠ Resolved ≠ Adequate`. Every defect found tonight is one of those
gaps, and each was found by probing the layer *below* the one that was reporting.

Also accepted, and it is aimed at proposals I have made in other lanes as well as theirs: **any
metric that rewards silence gets gamed by silence.** The `outcomes / attention` ratio degenerates
under "silence is a valid action". That warning applies to their BCL/SCP proposals and to my own
C21 if anyone ever turns it from a report into a gate. It stays INFO, and the reason is written in
the file so the next agent does not have to rediscover it.

## 5. VERDICT

| item | state |
|---|---|
| WELL source hash discrepancy | **my snapshot was pre-commit; direction is source-ahead-of-deploy; not a defect** |
| receipt verification | **3/3 resolve** — first full-resolution receipt set tonight |
| FORGE-onboarding "case-twin pair" | **narrowed — one side has no SKILL.md, the other is upstream-bundled** |
| HEARTBEAT.md | **present, 147 bytes, zero tasks; "alive but starved" confirmed** |
| heartbeat mechanisms | **3 found, none reporting; standing-obligation decision, NOT touched** |
| negative-control gap | **closed — e2e suite built, 6/6, wired into C12** |
| defects it found | **2 (one tool: not_yet_due unpublished; one test: wrong fixture world)** |
| signature convention | **session id + host adopted from here** |
| merge / mutations | **none. WELL drift, RSI routing name, onboarding merge all still HELD** |

DITEMPA BUKAN DIBERI ⚒️
