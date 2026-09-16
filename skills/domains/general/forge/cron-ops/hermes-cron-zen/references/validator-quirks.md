# Validator quirks — what it does and doesn't catch

## What the validator DOES check (apply-time)

The validator at `/root/HERMES/scripts/zen/validate_jobs_json.py` runs these checks on the patch JSON
before writing:

1. **Duplicate IDs** — two jobs with the same id → fail.
2. **Provider in live set** — `provider` field must be in the live set from `config.yaml` or `null`.
3. **Cron expression 5-field** — `0 7 * * *` ✓, `0 7 * *` ✗.
4. **Enabled is bool** — must be `true` or `false`, not anything else.
5. **Delivery in allow-list** — see jobs-json-shape reference.

If any check fails, the validator prints errors, preserves the existing backup, and exits 1.

## What the validator does NOT check

- **Script path resolution** — the validator accepts any value in `script` field. The runtime
  resolver is what rejects absolute paths outside `/root/HERMES/scripts/`. So a patch can pass
  validator apply and then immediately fail at runtime.
- **Script existence** — the validator doesn't check if the script file exists. It'll accept a patch
  pointing at a non-existent script.
- **Idempotency** — running apply twice with the same patch can change the same job twice. There's
  no "if value already X, skip" logic.
- **Cross-references** — if a job has `context_from: "abc123"`, the validator doesn't check that
  `abc123` exists.
- **Schedule semantics** — `0 7 * * 8` (Aug + Sunday) parses but may not be what you intended.
  Validator doesn't warn.

## Runtime-only errors you'll see after a clean validator apply

These are the failures that pass validator but fail at runtime. Probe with `last_error` and
`last_delivery_error`:

| Symbol | Class | Fix |
|---|---|---|
| `Script not found: /root/HERMES/scripts/<name>.sh` | path | Move/symlink the script to `/root/HERMES/scripts/`. |
| `Blocked: script path resolves outside the scripts directory` | path-resolution | Set `script` field to bare name; move script to `/root/HERMES/scripts/`. |
| `delivery error: Telegram send failed: You must pass the token` | env-strip | Downgrade deliver to `local`, OR set `no_agent: false`. |
| `Provider 'X' not in live set` | validator-actually-rejects | Use a live provider. |
| `Script exited with code N` | script-runtime | Read the script's stdout/stderr in `/root/.hermes/cron/output/<id>/`. |
| `Cron expression parse error: ...` | validator-actually-rejects | 5-field cron expression. |

## Common validator pitfalls

### "Patch passed but job still erroring"

The validator says "OK ✅" but the next cron tick still shows the same `last_error`. Cause:
- The runtime issues are not in the validator's scope. Run a probe with `last_error` to see
  the new failure.

### "apply said backup at /root/forge_work/backups/jobs.json.bak-<ts> but the file is missing"

The validator logs `backup = BACKUP_DIR / f'jobs.json.bak-{stamp}'` but the backup file is only
written if the directory exists. If `BACKUP_DIR.mkdir(parents=True, exist_ok=True)` fails
(permissions, disk full), the apply aborts before writing the backup. The receipt path is also
handed out but not written. Don't trust the printed path — verify the file exists.

### "Receipt exists but the patch content doesn't match what I sent"

The validator's `update` step does a string-comparison-or-set per field. If the field already has
the exact value in the patch, it's still overwritten. The receipt shows the full final state, not
the diff. **Always diff jobs.json before vs after** with `diff <backup> <current>` to verify what
actually changed.

### Apply form edge cases

```bash
# Standard
python3 /root/HERMES/scripts/zen/validate_jobs_json.py apply /path/to/PATCH.json

# Check-only (no write)
python3 /root/HERMES/scripts/zen/validate_jobs_json.py check /path/to/jobs.json
```

The `check` mode is **read-only** — useful for dry-run before any T2 patch.

## When the validator itself is the wrong tool

If you need to:
- Add a no_agent job with a new script that doesn't exist yet → write the script first, then patch.
- Move many jobs to a new schedule → use the patch's `updates` array, NOT direct edit.
- Remove a job permanently → use `hermes cron remove <id>` (CLI), not direct JSON delete (the CLI
  also handles cleanup of output dirs).

## Receipt inspection

The receipt JSON at `/root/forge_work/backups/jobs.json.receipt-<ts>.json` contains:

```json
{
  "patch_source": "/path/to/PATCH.json",
  "applied_at": "2026-08-05T18:11:45Z",
  "patched_jobs": ["84e6752c7b7f", "..."],
  "reversible": true,
  "backup": "/root/forge_work/backups/jobs.json.bak-20260805-181145"
}
```

Read the receipt alongside the patch JSON to verify what was actually applied matches what was
proposed.
