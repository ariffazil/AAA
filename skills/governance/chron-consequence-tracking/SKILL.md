---
name: chron-consequence-tracking
description: "Track a claim to its verification date: chron it."
version: 1.0.0
floors: [F2, F7, F11]
triggers:
  - "chron it"
  - "register this in chron"
  - "track this prediction"
  - "when will we know"
  - "is this prediction due"
  - "chron status"
  - "prediction verified"
  - "calibration"
  - "temporal commitment"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# CHRON — Temporal Consequence Tracking

CHRON answers four questions and nothing else: *what did we think · what happened · were we wrong ·
what changed because of it.* It is the organ that turns a statement into a dated, checkable commitment.

Use it whenever a conclusion has a future moment at which reality will settle it. Writing the
conclusion into a report is not tracking it; the report has no verification date and no verifier, so
nothing will ever come back and say the analysis was wrong.

## Rule 0 — nothing is tracked until it has a verifier command

Every prediction must carry, in the store itself:

- **`verifier` / `verifier_method`** — the *exact* command, endpoint, or source that closes it. Not "check
  the news" but `ls -t <dir>` / `curl <api>` / `grep <field> <ledger>`. The next session must be able to
  run it without re-deriving intent.
- **`falsifier`** — the observation that would prove it wrong, stated as an observation, not a negation.
- **`verify_at`** — derived from the event's `target_date`. Set the date; do not hand-write the timestamp.
- **`confidence`** — a number, so calibration is computable later.

If you cannot write the closing command, the claim is not ready to be tracked. A prediction whose
verifier is missing is decoration: it will appear in the due-queue, cost attention, and settle nothing.

**NEW — 2026-09-20 bind-before-attention:** `create_prediction` mints `UNBOUND` (not `ACTIVE`) unless
`probe_id` is set or `audience=arif` (HUMAN_WITNESS). A text `verifier_method` that the scanner cannot
run is still unbound. Scanner: `python3 /root/chron/chron_early_falsifier_scan.py` →
`data/binding_scan.json`. Hooked into the existing loop closer. No new cron. Do not rewrite birth
records to add `probe_id`; wire a probe function instead. `EARLY_FALSIFIER_SATISFIED != FALSIFIED`.

## Rule 0.5 — reconcile ledger intent against live store before trusting either

Whenever a session opens with a "refine the chron task" directive, the first move is to diff the
designed/claimed state against the live state — both can be wrong, and the *gap* is the work. The
canonical check:

```python
import json
# live counts
preds = [json.loads(l) for l in open('/root/chron/data/predictions.jsonl')]
sc = {}
for p in preds: sc[p.get('status','?')] = sc.get(p.get('status','?'),0)+1
print(sc)  # ACTIVE / VERIFIED / CORRECT / INCORRECT / UNBOUND / SUPERSEDED / VOIDED_SECTION_12
```

If a doctrine file (e.g. `CHRON-FINAL-TASK-LEDGER-2026-09-18.md`) says "T3 UNBUILT" but the store has
88 predictions, the doctrine is stale — append a `## N. RECONCILIATION NOTE` block recording the
diff (date, live counts, re-classification), do not silently rewrite the doctrine. The ledger remains
the design intent; the reconciliation block carries the truth.

The same pattern applies to `lessons.jsonl`: if entries read "Unknown error type 'UNKNOWN' seen N
times. Investigate root cause." with no basis, those are placeholder emissions from a classifier
that cannot represent a positive class — they are **not** lessons. Replace with real lessons derived
from VERIFIED predictions, each carrying `prediction_id`, observed value, brier, and the conclusion
the evidence supports. Placeholders without basis are CLASS A anti-patterns.

## When the principal says "chron it"

He means: take the finding you just produced and register it as a **dated commitment with falsifiable
predictions that carry verifiers** — not "write it up in a report". Then report back, in one short
block: the event id, its target date, the prediction ids, and the date they verify. Register each
consequence-bearing claim as its own prediction so the store can score them independently; one event
with four checkable claims beats one event with a vague summary.

## Procedure

### 1. Confirm the organ before writing

```bash
systemctl is-active chron-mcp                     # the server (FastMCP, 127.0.0.1:18102/mcp)
ss -ltnp | grep 18102                             # something owns the port
cd /root && PYTHONPATH=/root python3 -m chron status
```

`status` returns the store census — episodes by function, predictions by state, lesson count. Read it
before adding to the store; it is also the health read (see Pitfalls).

### 2. Register the event

The event store is `<AAA>/scripts/chron_events.json`:
`{"events": [...], "_updated": "YYYY-MM-DD"}`.

Write through the function, not by editing the file — it enforces the duplicate-id check and date
validation, and it bumps `_updated`:

```bash
cd /root && PYTHONPATH=/root python3 - <<'PY'
from chron.server import chron_create_event
r = chron_create_event(
    event_id="kebab-case-unique-id",
    title="Human-readable event",
    target_date="YYYY-MM-DD",
    kind="OBSERVATION",          # FISCAL | MARKET_EVENT | REGULATORY_WINDOW |
                                 # PERSONAL_SAFE | MACRO_INDICATOR | OBSERVATION
    audience="arif",             # arif | syed | both  -- controls which lane may surface it
    source="<provenance: the probe, file or URL that grounds this>",
    note="<the finding, with the measured numbers>",
    confidence="CONFIRMED",      # CONFIRMED | LIKELY | ANNOUNCED | PREDICTED | TENTATIVE
    consequence="HIGH",          # HIGH | MEDIUM | LOW
    actionability="PREPARE",     # PREPARE | WATCH | MONITOR
)
print(r)
PY
```

Returns `{"created": true, "event_id": ..., "total_events": N}`. A duplicate id or a malformed date
comes back as `{"error": ...}` — treat that as a refusal, do not retry with a coerced date.

`source` is the provenance field: name the command, file or URL that grounds the event. An event with no
provenance is an opinion with a date attached.

### 3. Attach predictions (the designed path)

Add a `predictions[]` array to the event, then let the generator expand it. Each entry carries `claim`,
`expected_value`, `threshold`, `unit`, `verifier`, `falsifier`, `confidence`:

```bash
cd /root && PYTHONPATH=/root python3 - <<'PY'
import json
from pathlib import Path
p = Path('<AAA>/scripts/chron_events.json')
d = json.loads(p.read_text())
for e in d['events']:
    if e['id'] == 'kebab-case-unique-id':
        e['predictions'] = [{
            "claim": "<falsifiable statement>",
            "expected_value": "<=8",
            "threshold": 8,
            "unit": "tasks",
            "verifier": "<exact command that closes it>",
            "falsifier": "<observation that proves it wrong>",
            "confidence": 0.65,
        }]
d['_updated'] = "YYYY-MM-DD"
p.write_text(json.dumps(d, indent=2, default=str) + "\n")

from chron.chron_prediction import generate_from_chron_events
print("generated:", len(generate_from_chron_events()))
PY
```

The generator mints `prediction_id`, derives `verify_at` from `target_date` (end of day, MYT), computes
`horizon` from days-until, sets `status=ACTIVE`, and de-duplicates on `source_id||claim` — so re-running
it is safe. An event with no `predictions[]` falls back to a trivial *"the event will occur"* claim,
which is barely falsifiable; always supply the array for anything that matters.

### 4. Let the schedulers close the loop

```bash
systemctl list-timers chron-* --all --no-pager
```

**CHRON has FOUR cron layers, not one. Probe all four before declaring the organ dead.**

| Layer | Path | Use case |
|---|---|---|
| `jobs.json` | `/root/HERMES/cron/jobs.json` | agent-invoked jobs (A-Z pulses, etc.) — has `no_agent` + `lane=human\|machine` |
| System crontab | `crontab -l` | one-off shell jobs, mostly legacy |
| `/etc/cron.d/chron*` | `ls /etc/cron.d/ | grep chron` | low-level organ crons (bl02 calibration, bridge_flow) — run every 5 min or daily |
| systemd timers | `systemctl list-timers chron-*` | the daily loop (reconciliation 06:50, verifier 07:00, loop-closer 07:15, edge-midday 12:30, reality-impact-attestor 09:45) |

A "missing CHRON cron" report that only checked `jobs.json` is wrong by construction — three more
layers exist and any of them can be live. The canonical live check is:

```bash
# 1) jobs.json
python3 -c "import json; d=json.load(open('/root/HERMES/cron/jobs.json')); print(sum(1 for j in d['jobs'] if 'chron' in (j.get('name','') or '').lower()))"
# 2) crontab
crontab -l 2>/dev/null | grep -iE 'chron|temporal'
# 3) /etc/cron.d/
ls /etc/cron.d/ | grep -iE 'chron'
# 4) systemd timers
systemctl list-timers --all | grep -iE 'chron'
# 5) data freshness (the real liveness signal)
ls -la /root/chron/data/{episodes,predictions,lessons,calibration,verification_log}.jsonl
```

Three daily oneshots do the metabolic work: reconciliation (~06:50), **prediction verifier (~07:00)**,
and the loop closer (~07:15, which also runs the briefing). The `.service` units commonly read
`disabled` while `.timer` units read `enabled` — that is the normal timer+oneshot shape. **Judge
liveness from the timer, not `systemctl is-active <name>.service`**, which is `inactive` for any
oneshot not currently mid-run. The proof of life is `LastTriggerUSecRealtime` recent AND the
service stdout in `journalctl -u <name> --since '7 days ago'`.

**JITU-guard wrapper for cron cron.d entries.** Legacy `/etc/cron.d/chron*` lines invoke
`/root/.local/bin/jitu-guard <lane> && /usr/bin/python3 <script>` — the `jitu-guard` shim is the
correct entrypoint, not a bare `python3`. Skipping it skips the policy gate that defines what
the cron is allowed to do. When writing a new cron.d entry, copy the guard form from
`/etc/cron.d/chron-bl02-calibration`.

### 5. Close an outcome by hand when the verifier cannot

```
chron_record_verification(prediction_id, observed_outcome, correct)
```

This is the write surface that completes the arrow of time. Record `correct: false` without flinching — a
store that only contains confirmations has no calibration value, and the `error_type` field exists so
misses can be classified rather than hidden.

### 6. Read it back

```bash
cd /root && PYTHONPATH=/root python3 -m chron status        # store census
cd /root && PYTHONPATH=/root python3 -m chron predictions   # [ACTIVE|VERIFIED|all]
cd /root && PYTHONPATH=/root python3 -m chron calibration
cd /root && PYTHONPATH=/root python3 -m chron verify --dry-run
cd /root && PYTHONPATH=/root python3 -m chron call <tool>   # any MCP tool
```

## 7. Close the loop — write a verify cycle when none exists

`chron verify --dry-run` is a single-shot read; sustained T4 closure needs a *cycle*: a script
that runs the verifiers, scores the results, updates prediction statuses, appends lessons, and
appends to `verification_log.jsonl`. Build it as a standalone Python script (script mode, not
package mode — see Pitfalls), then call it from a cron. **No new cron without F13 binary**: write
a proposal to `/root/AAA/cockpit/proposals/CHRON-VERIFY-CYCLE-CRON-<date>.md` listing the schedule
options (A: daily fixed, B: post-pulse, C: event-driven hook, D: hold manual, E: defer), and let
F13 pick one.

### Three-class dispatcher (the pattern that actually scores)

Every prediction in the store falls into one of three verification classes. A cycle that does not
classify before probing emits a flood of `NO_LIVE_DATA` for the cases that should have scored and
no score for the cases that should have been flagged.

| Class | Match | Probe | Verdict emitted when | Verdict refused when |
|---|---|---|---|---|
| **A — Filesystem** | `verifier_method` starts with `grep ` or contains `ExecStart` | `subprocess.run(verifier, shell=True, timeout=15)`; parse int from stdout | result matches claim's expected count/state | destructive command detected (refuse `rm`, `mv`, `chmod`, redirect to `/`) — log as `PROBE_ERROR` |
| **B — Market threshold** | claim contains XAUUSD / Brent / WTI / OIL / GAS / USDMYR / KLCI / RON95 | call WEALTH MCP `capital_market` with mode=commodity / mode=fx / mode=stock; use 6h cache | structured `threshold` or `threshold_low/high` field present, live value resolves, op matches | `gold_spot` is not a valid commodity id — use `gold`. **Silver is not gold** — never substitute as proxy. RON95 is Malaysian-domestic, no federated lane carries the live price — log `UNOBSERVABLE_FROM_LANES` |
| **C — Event / state** | none of the above | manual review queue | human verdict recorded via `chron_record_verification` | auto-emit nothing; surface as `EVENT_PREDICTION` in verification_log so it appears in the next review |

### Threshold parser — read the structured fields first

`predictions.jsonl` rows carry `threshold`, `threshold_low`, `threshold_high`, and `op` (sometimes).
Read those before regex-parsing the claim string — the structured field is the source of truth, and
regex-on-claim conflates different claim forms (`"holds < 4.40"`, `"XAUUSD closes > 4500"`,
`"Brent 65-75"`) into one brittle matcher.

```python
def parse_threshold(claim, p):
    if p.get("threshold_low") is not None and p.get("threshold_high") is not None:
        return {"low": float(p["threshold_low"]), "high": float(p["threshold_high"]), "kind": "range"}
    if p.get("threshold") is not None:
        op = "<" if "<" in claim or "holds" in claim.lower() else ">"
        # "up"/"climb"/"higher" → ">", "holds"/"below"/"<" → "<"
        if any(s in claim.lower() for s in [">", "atas", "above", "up", "climb", "higher"]):
            op = ">"
        return {"threshold": float(p["threshold"]), "op": op, "kind": "threshold"}
    # fall back to regex only if both fields missing
    ...
```

### Brier + verdict + lesson in one write

For every score the cycle produces, do three writes atomically: update the prediction row
(status → VERIFIED or INCORRECT, verdict, verified_at, observed_outcome, brier_score), append
to `verification_log.jsonl`, and append a lesson to `lessons.jsonl` carrying
`source_prediction_id` + brier + observed value + one-sentence conclusion. The lesson is the
"what does this mean" line that the next session will read. A cycle that scores but does not
emit lessons is calibration without learning.

**Backup before any write that mutates the prediction store.** Use a timestamped
`predictions.jsonl.bak-verify-<ts>` next to the live file; the cycle should refuse to write if
the backup step fails.

### Calibration reporting

After every cycle, recompute the headline number and surface the change:

```python
correct = sum(1 for p in preds if p.get("verdict") == "CORRECT")
total = sum(1 for p in preds if p.get("verdict") in ("CORRECT","INCORRECT"))
brier_mean = sum(p.get("brier_score",0) for p in preds if p.get("brier_score") is not None) / total
```

Honest numbers drop when a cycle runs — the previous "optimistic" accuracy was a smaller sample.
A drop is information, not failure. The principal cares whether the institution learns, not
whether the score goes up.

## Surfaces

| What | Where |
|---|---|
| Event store | `<AAA>/scripts/chron_events.json` |
| Predictions | `chron/data/predictions.jsonl` (one JSON object per line) |
| Episodes / index | `chron/data/episodes.jsonl`, `index.json` |
| Verification outcomes | `chron/data/verification_log.jsonl` (keyed by `prediction_id`) |
| Loop log / calibration | `chron/data/loop_log.jsonl`, `calibration.json` |
| Lessons | `chron/data/lessons.jsonl` |
| Server | `chron-mcp.service`, FastMCP streamable HTTP at `127.0.0.1:18102/mcp` |
| Write functions | `chron_create_event` in `chron/server.py`; `generate_from_chron_events` in `chron/chron_prediction.py` |

MCP tool names are prefixed `chron_` — `chron_create_event`, `chron_generate_predictions`,
`chron_record_verification`, `chron_active_events`, `chron_active_predictions`, `chron_predictions_due`,
`chron_store_stats`, `chron_temporal_briefing`, `chron_attention_debt`.
JSON shapes for both stores: `references/event-and-prediction-schema.md`.

**Time-dimensions vocabulary:** Chronos (sequential), Kairos (opportune), Aion (deep-time),
Telos (terminal) — each maps onto a CHRON construct; do not collapse them. See
`references/four-time-dimensions.md` for the lens and the four-check gate
(`Chronos ∧ Kairos ∧ Aion ∧ Telos` → legitimate; any failing → HOLD).

## Pitfalls

- **Run the CLI as a module from the repo root, with `PYTHONPATH` set.** The package imports itself
  absolutely (`from chron.chron_store import get_store`), so `python3 <pkg>/__main__.py …` or running
  from inside the package directory fails with `ModuleNotFoundError: No module named 'chron'`. Use
  `cd /root && PYTHONPATH=/root python3 -m chron <cmd>` — the environment the systemd units declare.
- **An MCP session error is a transport requirement, not an outage.** A hand-rolled JSON-RPC POST to the
  HTTP MCP port returns `-32600 Bad Request: Missing session ID` because FastMCP streamable HTTP needs an
  initialised session. Do not report the organ as down on that response — use the MCP tool lane, or the
  importable function, and keep raw curl out of the loop.
- **Absence of lessons is the loudest health read.** Compare the episode counts *by function* rather than
  the total: `observe` in the tens of thousands against single-digit `predict`/`verify` and a 0-byte
  `lessons.jsonl` means the loop records but never closes. Report the ratio across observe → predict →
  verify → learn; a large observation total with zero lessons is a bigger finding than the throughput.
- **CHRON is a consequence tracker, not a clock.** Never answer "what time is it" / "is it morning" from
  it. Current-time claims come from `date`, the public time endpoint, or the carry-forward temporal root.
  A store full of dated predictions is not a time source.
- **Date a prediction when you make it, not when you remember it.** A commitment registered after the
  event it predicts has no falsification value, and the store cannot tell a lucky guess from a forecast
  except by `created_at` vs `target_date` — so check those two fields when auditing a track record.
- **Scope the audience at write time.** `audience: arif|syed|both` gates which lane may surface the event.
  A commitment about a person's health, or a personal safe-date, belongs to that person's audience; do not
  file it as general.
- **Reading verdicts means JOINing.** Outcomes land in `verification_log.jsonl` keyed by `prediction_id`;
  the proposition lives in `predictions.jsonl`. Reading either alone yields a score with no claim attached
  — join them before reporting calibration.
- **Do not file a stream of trivia.** Every event costs attention on its target date. Register what has an
  owner and a date; a due-queue diluted with uncheckable entries gets ignored, and an ignored due-queue is
  worse than none.
- **Verify the digest that consumes this is actually scheduled.** CHRON-backed weekly packets are a
  classic designed-but-never-wired ritual: the producer script works, the output directory exists, and
  nothing invokes it on cadence. Before promising the principal a recurring digest, list the output
  directory newest-first and compare the newest artifact against the declared slot.
- **VAULT999 receipts do not carry the tool result.** Reading `/root/VAULT999/wealth/receipts.jsonl`
  to recover a `capital_market` call's price returns nothing — the receipts store arguments, status,
  and verdict fields, not the nested `result`. To get live market state, call the WEALTH MCP tool
  fresh, or write a sibling probe script that does and caches the snapshot to a JSON file with a
  `captured_at` timestamp. Refuse any cache older than 6 hours — a cycle that scores on stale
  data is worse than one that scores nothing.
- **The WEALTH supported-commodity list is small and exact.** `gold` is the id, not `gold_spot`.
  `natgas` is not supported. The full list at last probe: `brent_crude`, `lng_asia`, `coal_api2`,
  `gold`, `malaysia_rsd`. Anything else returns `UNSUPPORTED`. A verify cycle that calls the
  wrong id will think it has no live data when the truth is that the lane does not carry the
  instrument — log the lane's response verbatim so the next session does not retry the same call.
- **Never substitute a proxy for the claimed instrument.** Silver is not gold; Brent is not WTI
  (the commodity engine returned Brent when WTI was requested and the answer was silently branded
  XBRENT). If the live lane cannot produce the exact instrument, emit `NO_LIVE_DATA` and stop.
  A verdict on a proxy is a verdict on a different claim, and the calibration it produces is
  calibration for the wrong thing.
- **No new cron without F13 binary.** Wiring a verify cycle to fire automatically requires
  appending a job to `/root/HERMES/cron/jobs.json`; per `base.md:15` "new capability fires on a
  trigger, not a polling timer; no new cron without explicit F13 approval." Build the cycle,
  prove it works on `--dry-run`, then write an F13 proposal listing the schedule options. Do
  not silently wire the cron. The cycle itself is reversible (a script with no cron); the cron
  is the irreversible addition.
- **The first lesson emission is rarely the right one.** A verify cycle that scores correctly
  but emits a generic placeholder lesson ("Unknown error type 'UNKNOWN' seen N times") is
  learning nothing. The classifier that produced the placeholder is a defect: it cannot
  represent "state already correct" as a positive class, so it loops. The fix is in the
  cycle, not in the store — emit a lesson that names the prediction, the brier, the observed
  value, and the one-sentence conclusion. If you cannot write that line, do not write anything;
  the absence is more useful than a placeholder.

- **The T5 chain requires `error_type` in BOTH `predictions.jsonl` AND `verification_log.jsonl`.**
  `chron.chron_prediction.get_verified()` JOINs the two stores and prefers `error_type` from
  `verification_log.jsonl`. A cycle that writes `status=INCORRECT` and `verdict=INCORRECT` but
  never sets `error_type` produces a row that `chron_learn.extract_lessons()` refuses —
  it routes the outcome to `insufficient_data.jsonl` ("error class names no cause") instead of
  `lessons.jsonl`. The classifier is strict on purpose (defends against the loop promoting its
  own blindness), so the fix lives upstream: a verify cycle that scores an INCORRECT verdict
  MUST also classify the failure to a known class (`RANGE_STALE_AT_MINT`, `MODEL_ERROR`,
  `ASSUMPTION_ERROR`, `DATA_ERROR`, `REGIME_CHANGE`, `AWAITING_EVIDENCE`) and write the
  classification into BOTH stores atomically. After any verify cycle, the next step is
  `python3 /root/chron/chron_learn.py` — if it reports `extracted 0 lessons` against a
  non-empty `verification_log.jsonl`, the cycle forgot to classify.

- **The T5 recovery: classify-then-rerun, not regenerate.** When a verify cycle that scored
  N verdicts leaves `lessons.jsonl` empty, the wrong move is to add new lessons by hand; the right
  move is to backfill `error_type` on the existing INCORRECT rows and re-run `chron_learn`.
  Procedure:
  1. Open `verification_log.jsonl`; for every entry where `outcome == "INCORRECT"` and
     `error_type` is null/missing, classify using one of the six named classes above
     (with provenance: what the observed value proves about the failure).
  2. Mirror the same `error_type` + `error` string into the matching `predictions.jsonl` row by
     `prediction_id` — `get_verified()` reads the verification-log field first but the prediction
     row is the persistent record.
  3. Re-run `python3 /root/chron/chron_learn.py`. Expect `extracted N lessons` for N
     distinct (error_type, prediction_id) pairs.
  4. If still 0, the classification itself is wrong — `error_type=UNKNOWN` is not in
     `INTERPRETABLE_ERROR_TYPES` and routes to `insufficient_data.jsonl` instead. Re-pick from
     the six named classes; if none fit, leave it as UNKNOWN and accept the gap (the design
     refuses to promote its own blindness).

- **The "converged morning CHRON" pattern — do not re-run cron-scheduled jobs manually.** A
  session that invokes `chron.py`, `bridge_flow`, `chron_briefing`, `chron_attention_debt`, and
  `chron_attribution` as separate calls duplicates what the four cron layers already produced.
  Replace the five-call dance with one read-only aggregator (`/root/AAA/scripts/chron_morning.py`,
  BM Penang default, MD or `--json` output) that reads from the same stores the cron just
  updated and emits a single brief. The aggregator is a *consumer* — it does not mutate, does
  not probe WEALTH fresh, does not re-run any subsystem. The cron schedule is the producer;
  the morning script is the dashboard. Building both halves is the work; calling them
  serially in a session is the chaos the principal called out as "redundants jaaaa".
  Read the cron-layers reference (`references/chron-cron-layers.md`) before adding any new
  manual probe; the schedule table there is the source of truth for "what fired when".

- **PYTHONPATH=/root is required for every `chron` package script.** The package imports itself
  absolutely (`from chron.chron_store import get_store`), so a bare `python3 /root/chron/<file>.py`
  fails with `ModuleNotFoundError: No module named 'chron'`. The systemd units declare
  `Environment=PYTHONPATH=/root`; replicate that env in any hand-run probe, or run from
  `cd /root && PYTHONPATH=/root python3 -m chron <cmd>`. A session that runs each subsystem
  manually and gets `ModuleNotFoundError` is also a signal the manual rerun was the wrong shape —
  use the aggregator, not a re-implementation.

## Output shape

After a registration, reply with the event id, target date, prediction ids with their one-line claims and
confidences, and the verification date — compact, no ceremony. After a *review*, lead with calibration:
how many predictions closed, how many were wrong, and which stage of the loop is dead. The principal cares
whether the institution learns, not how many rows the store holds.
