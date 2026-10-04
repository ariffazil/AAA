# Auditing a Spawned Build Agent's "Runtime-Only" Report (2026-08-09)

Pattern from the grok FED-zen session: a spawned agent (grok/codex/opencode) pasted a change table claiming "I zen'd FED, runtime only — identity untouched." Arif asked me to be manager/auditor/validator. The table was a HYPOTHESIS LIST, not a receipt.

## The 6-step audit

1. **Hash-snapshot BEFORE auditing, and again the moment you suspect edits.**
   ```bash
   md5sum <config> && stat -c '%y' <config>   # baseline
   # ... later ...
   md5sum <config> && stat -c '%y' <config>   # re-check
   ```
   A hash change with an OLD mtime = the agent edited a path you're not looking at. Catches phantom claims and wrong-path edits.

2. **Check BOTH candidate paths for each runtime config.** Repo source vs live runtime are DIFFERENT files:
   - Hermes: `/root/HERMES/config.yaml` (repo, edited 04:09 by agent) vs `/usr/local/lib/hermes-agent/config.yaml` (LIVE runtime, mtime Aug 5 — agent never touched it).
   - OpenClaw: `/root/ariffazil/.openclaw/openclaw.json` (stale) vs `/root/.openclaw/openclaw.json` (LIVE, edited 04:03).
   The agent may have edited the non-live copy — the running runtime still uses the old config. `stat` mtimes disambiguate; report which path is actually live.

3. **Security-scan every file the agent wrote, not just content.** A "fix" that hardcodes a secret can ship world-readable: `hermes-asi-wrapper.sh` had the full `LITELLM_MASTER_KEY` inline at mode 755. Always:
   ```bash
   stat -c '%a' <new/edited file>          # mode check
   grep -n 'sk-...' <script>               # hardcoded key literal
   ```
   5-R protocol: secrets come from `$ENV` (sourced from kunci-mas.env), never inline, never mode >600/700.

4. **Identity integrity = mtime sweep on the card tree.**
   ```bash
   find /root/AAA/a2a-server/agent-cards -type f -newermt '<session start>'   # empty = WHO untouched
   ```
   This is the concrete proof behind "runtime provider contract only." Also sweep `federation-models.json`, `SOUL.md`, `bound_to` files.

5. **Check for doctrine inversion, not just file drift.** An agent told to "zen FED" may flip agents from FED-primary to DIRECT-primary to keep things working while FED was down. That inverts the standing doctrine (FED=primary, direct=fallback). Reversible either way — but the direction is an F13 decision for Arif, not the build agent's call. Flag it explicitly.

6. **Report SOT-vs-live drift as a labeled gap, not identity corruption.** `federation-models.json` may still advertise FED-primary while live opencode.json says direct. Two operational files disagreeing = sync one file, zero card edits. Not a constitutional breach.

## Report shape (what worked)

| File | Change | Contract field | Verified? |
|---|---|---|---|
| haproxy.cfg | /health → /health/liveliness + timeout check 3000 | gateway health (runtime) | ✅ live 200 in 3ms |

Then a discipline table: ✅ agent-cards untouched / ✅ direct providers kept / ⚠️ federation-models.json drift / 🔴 wrapper key hardcoded at 755. Arif reads this format fast.

## The HAProxy 503 root-cause (same session)

`:4000` HAProxy returned 503 while `:4011` litellm-federation was healthy. Two causes, both in the health check:
1. `option httpchk GET /health` runs LiteLLM's FULL upstream sweep — 8.9s with valid auth; `/health/liveliness` answers in 3ms. Default `timeout check` (~1s) kills the slow check → backend marked down. Fix: `GET /health/liveliness` + `timeout check 3000` (`/health/readiness` 9ms also fine).
2. `http-check send hdr Authorization "Bearer <key>"` — if the key is a redacted placeholder, litellm journal shows "Malformed API Key" every check interval. Compare haproxy key with `$LITELLM_MASTER_KEY` live.

Also: `curl -sf` falsely reports litellm ports "down" (401 without auth) — use `ss -tlnp` to verify the listener; and a `PORT` env var in flat.env overrides litellm's `--port` CLI flag (unit launched with `--port 4000` bound 26898 instead).
