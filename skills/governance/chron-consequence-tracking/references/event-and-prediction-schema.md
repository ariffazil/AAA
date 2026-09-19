# CHRON store shapes

Copyable shapes for both stores. Field lists are what the writers actually emit; treat them as the
contract for any consumer you build.

## Event store — `<AAA>/scripts/chron_events.json`

```json
{
  "_updated": "YYYY-MM-DD",
  "events": [
    {
      "id": "kebab-case-unique-id",
      "title": "Human-readable event description",
      "target_date": "2026-09-28",
      "timezone": "Asia/Kuala_Lumpur",
      "audience": "arif",
      "kind": "OBSERVATION",
      "source": "live probe <timestamp> <host>; map: <path to the artifact>",
      "confidence": "CONFIRMED",
      "consequence": "HIGH",
      "actionability": "PREPARE",
      "note": "The finding, with the measured numbers inline.",
      "predictions": [
        {
          "claim": "<falsifiable statement>",
          "expected_value": "0 new packets",
          "threshold": 0,
          "unit": "packets",
          "verifier": "ls -t <dir> — baseline N files, newest <ts>; count files newer than <ts>",
          "falsifier": "any <artifact> with mtime after <ts>",
          "confidence": 0.75
        }
      ]
    }
  ]
}
```

Allowed values:

| Field | Values |
|---|---|
| `kind` | FISCAL · MARKET_EVENT · REGULATORY_WINDOW · PERSONAL_SAFE · MACRO_INDICATOR · OBSERVATION |
| `audience` | arif · syed · both |
| `confidence` | CONFIRMED · LIKELY · ANNOUNCED · PREDICTED · TENTATIVE |
| `consequence` | HIGH · MEDIUM · LOW |
| `actionability` | PREPARE · WATCH · MONITOR |

`id` must be unique — the writer refuses a collision. `target_date` must be `YYYY-MM-DD`.

## Prediction entry (input, inside the event)

`claim`, `expected_value`, `threshold`, `unit`, `verifier`, `falsifier`, `confidence`.

A useful verifier is a **command plus its baseline**: state what the value is *right now* so the future
reader can tell a change from a constant. "Count files newer than X" is checkable; "check the output" is
not.

## Prediction record (output — `chron/data/predictions.jsonl`, one object per line)

```json
{
  "prediction_id": "pred-<12 hex>",
  "claim": "<copied from the event entry>",
  "expected_outcome": "<expected_value>",
  "confidence": 0.6,
  "verify_at": "2026-09-28T23:59:59+08:00",
  "horizon": "3w",
  "assumptions": [],
  "evidence": [],
  "source": "chron_events",
  "source_id": "<event id>",
  "principal": "arif",
  "status": "ACTIVE",
  "created_at": "<ISO 8601 Z>",
  "observed_outcome": null,
  "error": null,
  "error_type": null,
  "verified_at": null,
  "brier_score": null,
  "supersedes": null,
  "falsifier": "<copied>",
  "verifier_method": "<copied from verifier>",
  "threshold": 0,
  "threshold_low": null,
  "threshold_high": null,
  "unit": "packets",
  "audience": "arif"
}
```

Derived at generation time: `prediction_id`, `verify_at` (from `target_date`, end of day MYT), `horizon`
(`Nd` ≤ 7, `Nw` ≤ 30, else `Nm`), `status=ACTIVE`, `created_at`, `principal`, `audience`. Deduplication
key is `source_id||claim`, so regenerating is idempotent.

`horizon` is computed from **days remaining at generation**, not from the event kind — two predictions on
the same event always share a horizon, and regenerating later does not rewrite it.

## Status values observed

`ACTIVE` → (verification) → outcome recorded with `correct: true|false`. `RETRACTED` / `SUPERSEDED` are
the terminal states for a claim withdrawn or replaced before its date. A prediction whose claim changed
gets superseded, never silently edited — `supersedes` chains it.

## CLI surface

```
status · episodes · predictions [status] · verify [--dry-run] · learn · generate · calibration · tools · call <tool>
```

Run as `cd /root && PYTHONPATH=/root python3 -m chron <cmd>`.
