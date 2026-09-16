# jobs.json schema reference (snapshot 2026-08-05)

## Top-level shape

```json
{
  "jobs": [ ... ],
  "updated_at": "2026-08-05T..."
}
```

Top-level fields observed:
- `jobs`: array of job objects
- `updated_at`: ISO timestamp, last write — populated by validator

## Job object fields

| Field | Type | Notes |
|---|---|---|
| `id` | string (12 hex) | Required for patches. Stable across edits. |
| `name` | string | Human-readable, can be Unicode. Not unique. |
| `prompt` | string | Empty for `no_agent=true` jobs. |
| `skills` | array | Attached skill names, loaded by agent loop. |
| `skill` | string/null | Single-skill form (legacy). |
| `model` | string/null | Per-job model override. |
| `provider` | string/null | Per-job provider override. |
| `provider_snapshot` | string/null | Set at creation time. |
| `model_snapshot` | string/null | Set at creation time. |
| `base_url` | string/null | Custom provider URL. |
| `script` | string | **Bare name** resolving under `/root/HERMES/scripts/`. NOT absolute path. |
| `no_agent` | bool | If true, script runs as cron job, no LLM. |
| `context_from` | string/array/null | Job ID(s) whose last output is injected as context. |
| `schedule` | object | `{kind: "cron", expr: "0 7 * * *", display: "0 7 * * *"}` or `{kind: "interval", minutes: N, display: "every Nm"}`. |
| `schedule_display` | string | Cached display string. |
| `repeat` | object | `{times: N | null, completed: N}`. |
| `enabled` | bool | Required, must be boolean. |
| `state` | string | "scheduled", "paused", etc. |
| `paused_at` | string/null | ISO timestamp when paused. |
| `paused_reason` | string/null | Free-text reason. |
| `created_at` | string | ISO timestamp. |
| `next_run_at` | string | ISO timestamp. |
| `last_run_at` | string/null | ISO timestamp, last actual run. |
| `last_status` | string | "completed", "error", "running", "unknown". |
| `last_error` | string/null | Most recent error message. |
| `last_delivery_error` | string/null | Separate from runtime error. |
| `deliver` | string | Where output goes. |
| `origin` | string/null | "tier-3.8-rsi-2026-08-05" — provenance tag. |
| `enabled_toolsets` | array/null | Per-job toolset whitelist. |
| `workdir` | string/null | Per-job cwd. |
| `fire_claim` | string/null | Internal scheduler state. |

## Delivery allow-list (observed)

The validator checks `deliver` against a known set. As of 2026-08-05:

- `local` — write to `/root/.hermes/cron/output/<job_id>/`
- `origin` — back to where the job was created
- `telegram:<chat_id>` — Telegram bot
- `discord:<channel>` — Discord channel
- `slack:<channel>` — Slack channel
- `whatsapp` / `signal` / `matrix` — platform homes
- `all` — fan-out
- Comma-separated: `telegram:267378578,telegram:-1004446358629`

## Provider live-set (snapshot 2026-08-05)

From validator reading `/root/HERMES/config.yaml` and recent jobs.json diffs:

- `qwen-token-plan-individual` (live)
- `qwen-token-plan` (live)
- `null` (inherited, valid)
- `fed` (removed — keep config clean)
- `hermes-asi` (alias unresolved — keep config clean)

If you patch a job to a provider not in the live set, the validator fails at apply-time.

## Common schedule shapes

```json
{"kind": "cron", "expr": "0 7 * * *", "display": "0 7 * * *"}
{"kind": "interval", "minutes": 30, "display": "every 30m"}
{"kind": "interval", "seconds": 7200, "display": "every 7200s"}
```

The validator's cron check parses 5 fields. Expressions with 4 fields fail.

## ID stability

IDs are 12-character hex strings minted at creation. They survive edits, do NOT survive remove+recreate.
**Always patch by `id`, never by `name`** — names can collide.

## Location conventions

- jobs.json: `/root/HERMES/cron/jobs.json`
- Validator: `/root/HERMES/scripts/zen/validate_jobs_json.py`
- Output dir: `/root/.hermes/cron/output/<job_id>/<timestamp>.md`
- Executions DB: `/root/.hermes/cron/executions.db` (separate, not covered here)
- Backup dir: `/root/forge_work/backups/`
- Tick lock: `/root/HERMES/cron/.tick.lock` (DO NOT touch mid-tick)
