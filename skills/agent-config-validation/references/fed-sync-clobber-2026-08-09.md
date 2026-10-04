# fed-sync clobber — worked case 2026-08-09

The second layer of the opencode deepseek-restore saga (first layer:
`opencode-enabled-providers-gating-2026-08-09.md`). After restoring
`deepseek` + `qwen-token-plan-individual` to `enabled_providers`, the restore
was REVERTED ~4 minutes later by an automated sync, and the config was broken
again with a NEW schema error.

## Timeline

- 10:11Z — manual restore applied (deepseek + qwen-token-plan-individual back in
  `enabled_providers`, models added to 333-AGI allowlist). Verified valid.
- 10:15:24Z — `fed-sync.timer` fires. Script snapshots the file (backup contains
  the FIXED state — looks innocent), then rewrites `enabled_providers` from its
  DB verdicts, dropping both providers ("mutations: 2"), and appends:
  ```json
  "_fed_sync": {"last_sync": "...", "source": "FED token_bank.db", "mutations": 2}
  ```
- Symptom: `opencode run` → `Configuration is invalid at .../opencode.json ↳ Unrecognized key: _fed_sync`.
- 10:30Z — next tick: a concurrent sibling edit had re-restored the providers
  and removed `_fed_sync` by hand; the timer ran again.

## Root causes (two independent bugs in the sync design)

1. **Schema violation:** metadata written INLINE into a strict-schema config.
   Any `_`-prefixed audit key is fatal (`additionalProperties: false`).
2. **Stale verdicts:** the sync's source of truth (SQLite `token_bank.db`)
   had deepseek `DEPLETED` — `balance_usd=0.0`, `confidence=0.3`, probed
   `03:17Z`. A live balance API probe at 10:05Z showed `is_available:true`,
   `$16.66`. The provider was topped up between the DB probe and the sync run;
   the DB was never refreshed.

## Fixes applied

- `fed-sync.py`:
  - `PROTECTED_PROVIDERS = {"deepseek", "qwen-token-plan-individual"}` — apply_diff
    skips DISABLE verdicts for these (sovereign-managed, never auto-disabled).
  - `_fed_sync` moved to sidecar: `opencode.json.fed-sync.meta.json`
    (`OPENCODE_JSON.replace(".json", ".fed-sync.meta.json")`).
- `token_bank.db`: deepseek row updated to `balance_usd=16.66`,
  `confidence_score=0.9`, notes `TOP-UP VERIFIED 2026-08-09T10:05Z`.
- Post-sync verification: deepseek still enabled, `_fed_sync` absent, JSON valid.

## Durable checklist for ANY auto-sync writing a strict-schema config

1. `systemctl list-timers` + `systemctl cat <unit>` — find every writer.
2. Grep the writer for the config path + `json.dump` — confirm it rewrites the file.
3. Decide: sidecar metadata OR no metadata. Never inline.
4. Decide: which entries are sovereign-protected from auto-disable.
5. Live-probe providers before trusting DISABLE verdicts; update the DB with evidence.
6. After the next timer tick, re-verify (parse + enabled set + `_fed_sync` absent).

## Concurrent-sibling-commit note

Later in the same session the sibling committed a sweep that included MY
uncommitted edits (git tree showed clean, but `git show HEAD:instructions/autonomy.md`
contained my markers). A "0 dirty" tree does not mean "your changes are committed
under your message" — verify content with `git show HEAD:<path> | grep <marker>`
before assuming a commit succeeded or failed.
