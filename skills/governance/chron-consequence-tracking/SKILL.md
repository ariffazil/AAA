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

Three daily oneshots do the work: reconciliation (~06:50), **prediction verifier (~07:00)**, and the loop
closer (~07:15, which also runs the briefing). The `.service` units commonly read `disabled` while
`.timer` units read `enabled` — that is the normal timer+oneshot shape. **Judge liveness from the timer,
not `systemctl is-active <name>.service`**, which is `inactive` for any oneshot not currently mid-run.

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

## Output shape

After a registration, reply with the event id, target date, prediction ids with their one-line claims and
confidences, and the verification date — compact, no ceremony. After a *review*, lead with calibration:
how many predictions closed, how many were wrong, and which stage of the loop is dead. The principal cares
whether the institution learns, not how many rows the store holds.
