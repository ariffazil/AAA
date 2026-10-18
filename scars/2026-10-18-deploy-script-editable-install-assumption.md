# SCAR-2026-10-18-004 — Deploy Script Editable-Install Assumption

**Filed:** 2026-10-18 by AGY CLI (Deploy Closeout)
**Weight:** w_scar = 0.9
**Class:** DEPLOYMENT_TOPOLOGY + SILENT_STALE_CODE
**Commit:** arifOS `09ad880fb`

## What happened

`scripts/deploy-to-runtime.sh` previously assumed an editable install at `/root/arifOS` (or rsynced solely into `/opt/arifos/app`), but the live production service imports directly from Python `site-packages` (`/opt/arifos/venv/lib/python3.13/site-packages/arifosmcp`).

Because the deploy script updated only `/opt/arifos/app` while leaving `site-packages` untouched, the service restarted cleanly with status 200/healthy, but continued running old bytecode from `site-packages`. This created the most hazardous class of failure: a deploy that reports complete success while running stale code.

## Why the gate missed it

The pre-push drift check queried `/health` and verified that git HEAD matched the recorded deployment tag/commit in metadata, but never probed the actual physical on-disk file path imported by the live runtime process. Metadata parity masked runtime bytecode drift.

## Fix landed

A content-parity gate was implemented in `scripts/deploy-to-runtime.sh`:
1. Re-resolves the live import path after sync via Python `importlib.util.find_spec('arifosmcp')` and refuses deployment if the package location moved or vanished.
2. Executes strict `diff -rq` (excluding `__pycache__` and `*.pyc`) comparing the source tree against BOTH trees (`/opt/arifos/app/arifosmcp` and `$LIVE_PKG`).
3. Enforces SHA-256 byte parity on core module files (e.g. `__init__.py` SHA `aeccda388d45...`).

## Binding rule (this scar)

- A deploy is unverified until the live process's active `__file__` path is confirmed to be byte-identical to the source repository.
- Never assert deploy success from `/health` or HTTP 200 alone without content-parity verification of the active import tree.
