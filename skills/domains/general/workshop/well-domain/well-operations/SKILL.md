---
name: well-operations
description: "Diagnose and operate the WELL organ (port 18083) — freshness monitoring, state.json corruption detection, biometric injection, and DEGRADED/HOLD alert resolution."
category: devops
forged: 2026-07-26
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# WELL Operations — arifOS Federation

> **WELL = Human readiness mirror. REFLECT_ONLY — never diagnose.**
> **Port:** 18083 | **Unit:** `well.service` | **Role:** Somatic intelligence / Body readiness

## BINDING — 2026-10-13 — never invent biometrics

The historical inject recipes (delta_s 0.3, peace2 0.7, well_score 73, clarity 7, previously documented in this skill) are the failure this session closed and have been removed. Any mention of `biometric_inject.sh` or injection flag-packs in `references/` is strictly historical context and explicitly overridden by this doctrine. Do not call `biometric_inject.sh`, `well_inject_biometric`, or POST `/ready` with numbers Arif did not say himself. A null score and an honest MOCK/EXPIRED human substrate is the correct reading. Live state is `WELL_STATE_PATH` (`/var/lib/well/state.json`). `/root/WELL/state.json` is a decoy. Keepalive writes liveness only.

## When to Use This Skill

- WELL freshness DEGRADED or HOLD alerts appearing
- WELL state.json found with `environment: TEST` or `reason: "Mocked healthy state"`
- Need to understand why WELL shows RED/YELLOW vs green. A null score is the honest reading. Do not inject numbers.
- Distinguishing "WELL service is down" from "WELL lacks sovereign biometric data"

## WELL Freshness Bands (from /health → freshness)

| Age | Status | Color | Meaning |
|-----|--------|-------|---------|
| < 1h | `fresh` | GREEN | Recent data, trust as current |
| 1h – 4h | `fresh` (past max) | YELLOW | Data exists but ageing. DEGRADED alerts start. |
| 4h – 24h | `stale` | RED / ORANGE | State expired. `sovereign_state_unknown`. |
| > 24h | `expired` | RED / HOLD | No usable biometric signal. WELL_HOLD. |

## Diagnosis Flow

When a WELL freshness alert fires:

```
1. PROBE live health
   curl -s http://127.0.0.1:18083/health | python3 -m json.tool

2. CHECK key fields:
   - freshness.status → fresh / stale / expired
   - state_age_hours → how old
   - owner_summary.color → GREEN / YELLOW / RED
   - owner_summary.reasons → array of root causes
   - well_score → numeric (or null)
   - truth_status → INSUFFICIENT_DATA / BEHAVIORAL / OPERATOR_REPORTED
   - honesty_banner → the real story
   - source_type → BEHAVIORAL_TELEMETRY vs OPERATOR_REPORTED

3. READ the live state file, not the decoy
   The service reads WELL_STATE_PATH (`/var/lib/well/state.json`).
   `/root/WELL/state.json` is a decoy. Do not treat it as live, and do not write it.

   CRITICAL CHECK — test/mock contamination:
   - environment == "TEST" && reason matches "Mocked" → BAD. Test file overwrote prod.
   - reason == "Mocked healthy state for test session" → state.json is corrupted.
   - source_type == "OPERATOR_REPORTED" → good (sovereign inject)
   - source_type == "BEHAVIORAL_TELEMETRY" → acceptable but LOW confidence

4. READ machine_state.json (machine health — separate from biometrics)
   cat /root/WELL/machine_state.json | head -20
   
   This reports CPU, memory, uptime — machine OK ≠ human data fresh.

5. CLASSIFY the root cause:
```

### Root Cause Table

| Pattern | Cause | Resolution |
|---------|-------|------------|
| `sovereign_state_unknown` | No self-report on file | Leave it. Do not invent one. |
| `biometric_state_fresh_but_insufficient` | Behavioral telemetry only, no sovereign data | Leave insufficient. Do not invent a self-report. |
| `biometric_state_expired_168h_ceiling` | State is old | Accept expired. Do not inject. |
| `environment: TEST` + `Mocked healthy state` | A test file is on a state path | Do not overwrite it with made-up numbers. Confirm which path the process reads. |
| `well_score: null` | No valid biometric data | Correct. Leave null. |
| Machine OK (Uptime, CPU, Memory all normal) | Service is up, human side has no fresh measure | Honest RED. Do not inject. |
| Machine NOT OK (service unreachable) | WELL process or service down | `systemctl restart well` |

## State Contamination Recovery

When state.json is overwritten with test/mock data:

1. **Diagnose:** Read state.json. If it contains `"environment": "TEST"` or `"reason": "Mocked healthy state for test session"`, it's a test file that was written to the production path.

2. **Do not fix this by writing numbers.** The old recipe that passed fixed delta/peace/kappa/amanah values was the failure. A mock banner and a null score stay until Arif himself states his own numbers in the same message. This file does not store those numbers.

3. **Verify:**
   ```bash
   curl -s http://127.0.0.1:18083/health | python3 -c "
   import sys, json
   d = json.load(sys.stdin)
   age = d.get('freshness',{}).get('age_seconds',0)
   ws = d.get('well_score')
   os_ = d.get('owner_summary',{}).get('color')
   ts = d.get('truth_status')
   print(f'Age: {age}s | Score: {ws} | Status: {os_} | Truth: {ts}')
   "
   ```

## The Automated Keepalive Quarantine Cycle

The system crontab runs `well_auto_keepalive.py` every 6 hours (`0 */6 * * *`). This script:

1. Reads `/root/WELL/state.json`
2. If `environment == "TEST"` or `truth_status` is `TEST`/`VOID`/`UNVERIFIED`:
   - **Quarantines** the TEST state to `/root/WELL/state.test.json` (preserved as evidence)
   - **Writes MINIMAL_PROD_SHELL** with `truth_status: INSUFFICIENT_DATA`,
     `test_contamination: QUARANTINED`, `well_score: None`, `freshness: STALE`
   - **Restarts** `well.service` to load the new state
3. If PROD environment & truth not in quarantine list:
   - Refreshes timestamps only — no vitals invented
   - Restarts well.service

### The Cycle Pattern

When state.json contains TEST/MOCK data, the keepalive creates a loop:
```
TEST state → keepalive quarantines → MINIMAL_PROD_SHELL →
restart WELL → timestamp refresh → TEST reappears → ...
```

Check the keepalive log at `/var/log/well-biometric-keepalive.log` for alternating `QUARANTINE` ↔ `timestamp-refresh`.

The MINIMAL_PROD_SHELL has no `biometric` field → computed score ~39 (F2-honest — no valid data).

**Do not break the cycle by inventing a biometric block.** A null score is the correct reading. The removed writer below used to paint a fresh score onto the decoy file. That writer is gone from this skill on purpose (2026-10-13). Do not recreate it. Do not restart WELL to load invented numbers.

### Multiple Freshness Monitoring Layers

| Layer | Mechanism | Schedule | Staleness Threshold |
|-------|-----------|----------|---------------------|
| System crontab | `well_auto_keepalive.py` | Every 6h | auto-quarantine on TEST, refresh on PROD |
| Hermes cron | `well_auto_feed.py` | 08:00, 20:00 MYT | 12h trigger for agent prompt |
| OpenClaw cron | WELL freshness 12h | Every 12h | reports DEGRADED/HOLD |
| WELL service | `/health` endpoint | On request | fresh <1h, stale 4-24h, expired >24h |

An alert from one layer may show different staleness/duration — always probe `/health` for ground truth.

## Biometric injection — forbidden in this skill

No sample command lives here. Do not call the inject script, do not POST `/ready`, and do not write a score. Numbers exist only if Arif says them himself, in that message. Invented sleep, water, steps, or a score are the failure this section used to teach.

## Key Files

| Path | Purpose |
|------|---------|
| `/var/lib/well/state.json` | **THE LIVE state file the running service reads.** Set by `WELL_STATE_PATH` in `/etc/well/well.env`, consumed at `server.py:182`. Always probe the running pid's env, never assume. |
| `/root/WELL/state.json` | **DECOY — not read by the service.** TEST/mock fixture, rewritten by a phantom writer + (pre-2026-09-15) the mis-pathed keepalive. |
| `/opt/well/state.json` | **DECOY — not read by the service.** rsync copy of the `/root/WELL` decoy made by `deploy-to-runtime.sh`. |
| `/root/WELL/machine_state.json` | Machine health metrics (CPU, memory, uptime) — separate concern |
| `/root/WELL/scripts/biometric_inject.sh` | On disk. Do not run it to paint a score. |
| `/root/WELL/scripts/well_auto_keepalive.py` | Substrate observability keepalive — liveness timestamps only, never vitals |
| `/root/WELL/scripts/well_ingest.py` | Intake-queue → live state merger (P1 pipeline) |
| `/root/WELL/scripts/google_fit_bridge.py` | Xiaomi→Google Fit→WELL bridge (autonomous feed) |
| `/root/WELL/google_fit_creds.json` | OAuth creds for the bridge — MISSING unless Arif sets up GCP Fitness API |
| Port 18083 `/health` | Live WELL health endpoint |

### Which state.json does the running service actually read? (PROVEN 2026-09-15)

The repo working dir is `/opt/well` but that is **not** the state path. The one canonical answer:

```bash
tr '\0' '\n' < /proc/$(systemctl show well.service -p MainPID --value)/environ | grep WELL_STATE_PATH
grep WELL_STATE_PATH /etc/well/well.env
sed -n '182p' /root/WELL/server.py   # STATE_PATH = Path(_os.environ.get("WELL_STATE_PATH", "/root/WELL/state.json"))
```

Answer as of 2026-09-15: **`/var/lib/well/state.json`** — neither of the two decoy copies. `/health` reads it fresh on every request via `_load_state()` (`server.py:2565`), so **no restart is needed** after editing it.

## Google Fit Bridge — the "wire the cron" trap (PROVEN 2026-08-01)

A sweep/audit often names `google_fit_bridge.py` as the fix for `H_WELL: CRITICAL — no biometric data`, reporting it "removed from live crontab" and asking to wire it. Two checks BEFORE wiring:

1. **Creds prerequisite:** the bridge reads `/root/WELL/google_fit_creds.json` (Google Cloud project → Fitness API → OAuth client → refresh token via `google_fit_auth_helper.py`). `ls /root/WELL/google_fit_creds.json` — if MISSING, wiring cron = dead cron (every run fails, dirties logs, no data). The bridge CANNOT run until Arif does the ~15 min GCP setup.
2. **Verify the crontab claim yourself:** `crontab -l | grep -i fit` — script present ≠ wired. Sweeps may be correct; probe anyway (F2).

**Present the honest three-option choice when asked "trigger fresh biometric feed?":**
- (a) **Do not invent a self-report.** This file stores no sample values. Only numbers Arif says himself, in that message, are his.
- (b) **Google Fit bridge later** — needs his GCP OAuth consent; note his stated skepticism of wearable optical HR (chest strap only is the preference). Frame accordingly, never push.
- (c) **Leave as-is** — `INSUFFICIENT_DATA` + `honesty: "MOCK / TEST"` banner is F2/F9-honest; WELL stays RED until real data exists.

**Never invent biometrics to green the score** — `well_score: None` with an explicit MOCK/TEST honesty banner is the CORRECT honest state until real data arrives (F9 ANTI-HANTU: fake live = hantu).

## Pitfalls

- **"WELL freshness STALE but a fresh state.json exists on disk" = STATE-PATH DIVERGENCE (PROVEN 2026-09-15).** Three writers targeted three paths: `well_auto_keepalive.py` hardcoded `/root/WELL/state.json`, `well_ingest.py` used `WELL_STATE_PATH`, `biometric_inject.sh` used `$WELL_DIR`. The service reads `WELL_STATE_PATH=/var/lib/well/state.json`, so the keepalive — the ONE job whose purpose is keeping live state fresh — stamped a decoy file every 6h, printed `"state_refreshed": true`, and the live timestamp froze for 11 days (269h, `expired`). Symptom to recognise: **a writer that reports success while `/proc/<pid>/environ` says the service reads a different file.** Fix: resolve the env var in every writer — `Path(os.environ.get("WELL_STATE_PATH", "/var/lib/well/state.json"))` — never hardcode. Rule: any writer's success receipt must echo the `state_path` it actually wrote.
- **Keepalive cadence must be < `max_fresh_age_seconds`.** The gate's `max_fresh_age_seconds` is 3600 (1h). A `0 */6 * * *` keepalive leaves the gate STALE for 5 of every 6 hours. Run the heartbeat at `*/30 * * * *`.
- **`well_ingest.py` was a silent no-op.** `if not intake_files: sys.exit(0)` logged nothing, so 48 runs/day looked identical to a healthy writer while `/var/lib/well/state.json` went unwritten. Also note `merge_into_state()` advances only `last_successful_read`/`last_successful_write` — `timestamp` (the field the gate keys on) is set ONLY in `process_intake_file()`. Void Guard: an empty queue must print a `NO_INTAKE` receipt, never silence.
- **The freshness gate keys on `state["timestamp"]`, not on the human payload age.** By the pipeline's own convention (`server.py:1147` `_get_freshness_band`, `well_ingest.py:170`) `timestamp` = *record write time*; the human-data origin lives in `payload_ts`/`signals_meta.injection_ts`. So a corrected heartbeat can report `freshness: fresh` on an old self-report. **Always read `payload_ts` + `honesty.is_sensor_verified` + `truth_status` together** — `fresh` must never be read as "live biometrics".

- **SCT event write failures (`Errno 30: Read-only file system` on `/root/A-FORGE/forge_work/.../sct_decision_events/`)** — WELL's systemd unit hardens with `ProtectHome=read-only` + `ReadWritePaths=/root/WELL`, so anything outside `/root/WELL` is read-only. `sct_decision_event.py` (line ~37) defaults its event dir to `/root/A-FORGE/forge_work/<date>/sct_decision_events`, which is OUTSIDE the write whitelist → every SCT decision append fails with Errno 30. This does NOT crash the service, but spams journal warnings and silently drops decision audit events. Fix: add the path to `ReadWritePaths` in `/etc/systemd/system/well.service`, then `systemctl daemon-reload && systemctl restart well`:
  ```ini
  ReadWritePaths=/root/WELL /root/A-FORGE/forge_work
  ```
  Verify: `journalctl -u well --no-pager -n 20 | grep -i "read.only\|errno 30"` → empty. Same pattern applies to ANY organ with `ProtectHome=read-only` writing outside its `ReadWritePaths` — when you see Errno 30 from an otherwise-healthy service, check `systemctl cat <unit>` for the hardening block first.

- **state.json keeps reverting to TEST/MOCK after quarantine.** The keepalive log at `/var/log/well-biometric-keepalive.log` may show alternating `QUARANTINE` ↔ `timestamp-refresh` cycles. Something (unknown process) may be re-writing the TEST state. Setting `environment: PROD` AND `truth_status: OPERATOR_REPORTED` AND including a `biometric` block prevents re-quarantine.

- **/health used to crash on `well_score: None`.** That was a missing guard. The fix is the guard, not a painted score. On 2026-10-13 the live health returned HTTP 200 with a null score and an honest MOCK/EXPIRED human substrate. Do not invent a number to turn that green.

- **Mock/test contamination is invisible to auto-keepalive.** The `well_auto_keepalive.py` script writes behavioral telemetry with timestamps, but does NOT guard against a pre-existing test/mock state.json. A test script that writes to `/root/WELL/state.json` can overwrite production data silently — always verify `environment` and `reason` fields.
- **Diagnostic recipe: "cron runs but data is stale" — read the script (PROVEN 2026-08-04).** When a WELL freshness alert fires AND the cron schedule looks correct AND the bridge script exists at the expected path, the most common cause is a **stub bridge** — the script exists and runs but its body is just a status-print stub, not actual data collection. Inspect the script body: if it ends with `print(json.dumps({"status": "restored"}))` or `awaiting OAuth`, the cron fires but never produces data. Fix: complete a real data path, or leave the score null. Do not call the inject script with made-up numbers. Don't waste time debugging a cron that is doing exactly what it was told.

- **machine_state.json is NOT biometric.** Fresh machine metrics (CPU, uptime) do NOT mean WELL has human data. Always check `state.json` `source_type` and `truth_status` separately.
- **state.json can be 87 days stale.** WELL's `stale_after_seconds` is 14400 (4h). Once past 168h (7 days), it gets `biometric_state_expired_168h_ceiling`. Without sovereign injection, WELL stays on behavioral inference forever.
- **`freshness: fresh` with age > 4h is a contradiction — trust the age + honesty_banner, not the status word (PROVEN 2026-08-01).** The `/health` endpoint can report `freshness: fresh` while `age_seconds` is 8.7h and `honesty_banner` says `MOCK / TEST -- not live biometrics`. The quarantine loop writes a MINIMAL_PROD_SHELL whose freshness field lies: `environment: PROD` + `freshness: FRESH` on a shell with NO biometric block. Read the trio together: `freshness.age_seconds` + `honesty_banner` + `truth_status` are the ground truth; `freshness.status` and `environment` are cosmetic on the shell. A sweep reporting "WELL fresh" from the status word alone is wrong — the real state is `INSUFFICIENT_DATA` with no biometrics.
- **Sovereign injection requires the script to restart well.service.** If restart fails (e.g. systemd not available in container), state.json is written but WELL may not pick it up. Verify with health endpoint after injection.
- **Import-chain failure from arifOS source conflicts.** When `systemctl restart well` fails with `SyntaxError: invalid decimal literal` but state.json is clean, the root cause may be git merge conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`) in the arifOS Python source. WELL imports from `/root/arifOS/` via `PYTHONPATH` — the import chain is:
  `server.py → arifosmcp.rama.state_classifier → arifosmcp.__init__ → core modules`
  If any module in this chain has unresolved conflict markers, Python throws SyntaxError and WELL won't start. To diagnose: `journalctl -u well --no-pager -n 30 | grep 'File.*\.py'` to find the exact file + line. To bulk-fix all Python files in arifOS:
  ```bash
  python3 -c "
  import re, os
  root = '/root/arifOS/arifosmcp'
  for dirpath, _, fns in os.walk(root):
      for fn in fns:
          if not fn.endswith('.py'): continue
          fpath = os.path.join(dirpath, fn)
          with open(fpath) as f: content = f.read()
          if '<<<<<<<' not in content and '>>>>>' not in content: continue
          content = re.sub(r'^>>>>>>> .*$\n?', '', content, flags=re.MULTILINE)
          content = re.sub(r'^=======$\n?', '', content, flags=re.MULTILINE)
          content = re.sub(r'^<<<<<<< HEAD\n?', '', content, flags=re.MULTILINE)
          with open(fpath, 'w') as f: f.write(content)
          print(f'Fixed: {fpath}')
  "
  ```
  After bulk-clear, also check for syntax errors that were **masked** by the conflicts (duplicate lines where HEAD and THEIR versions both ended up in the file) — `grep -n 'default=.*default='` can catch one common pattern.

- **`well_machine_diagnose` tool fails with `name 'os' is not defined`.** The function at `server.py` L10448 imports `json` and `pathlib` but does NOT import `os` — yet L10502 calls `os.cpu_count()`. Fix: add `import os as _os_md` inside the function body, and change the call to `_os_md.cpu_count()`. See `references/code-patches-2026-08-01.md` for both patches.

- **`well_machine_diagnose` fails with `_omega_well_output() missing 1 required positional argument: 'mode'`.** After the `os` fix, the tool still fails because all three `_omega_well_output()` calls inside the function are missing the required `mode` parameter (function signature has no default). Add `mode="M_DIAGNOSE"` after each `lane="AGI"` line. Exact patches in `references/code-patches-2026-08-01.md`.

- **The phantom TEST writer also corrupts CODE, not just state.json (PROVEN 2026-08-02).** The recurring phantom that rewrites `state.json` with TEST/mock data can ALSO append broken code to `server.py` — in one incident it injected a new `well_system_pulse` `@mcp.tool()` function whose tail was an orphaned `except Exception: pass return envelope` block that broke the enclosing `try:`. Result: `SyntaxError` → crash loop → WELL DOWN + 503 from AAA. This is a DIFFERENT root cause than the merge-conflict SyntaxError above: here the working tree is "clean" of conflict markers but has an injected broken function with extra dedented lines. Diagnostic signature: `python3 -m py_compile server.py` (or `ast.parse`) errors at a `@mcp.tool()` decorator line with `SyntaxError: expected 'except' or 'finally' block` = an enclosing `try:` had its block mangled by a trailing orphaned `except`. Recovery:
  ```bash
  # 1. Backup the corrupt file for forensics
  cp server.py /tmp/server.py.broken-phantom
  # 2. Restore the committed (known-good) version — git working tree crosses state AND code
  git checkout -- server.py src/server.py
  # 3. Verify it parses BEFORE restarting (one change, one verify — serial discipline)
  python3 -c "import ast; ast.parse(open('server.py').read()); print('PARSES OK')"
  # 4. Restart and confirm health + AAA registration (was UNREACHABLE->503 in the crash)
  systemctl restart well.service && curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18083/health
  journalctl -u well.service --no-pager -n 8 | grep -i registered   # expect REGISTERED with AAA
  ```
  Verify the file mtime/size for rapid changes before patching — a sibling/agent write can race your edit (`file modified by sibling subagent` warning, size delta). See `references/phantom-writer-code-corruption-2026-08-02.md`.
  To catch the phantom **writer** with PID + cmdline, deploy the dual-layer /proc poller + inotify watcher — see `references/ghost-watcher-pid-capture.md`. Use `nohup` to decouple from agent session lifetime.
