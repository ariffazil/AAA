# Runtime-zen change report audit — WHO/WHICH split verification (2026-08-09)

When a sibling (grok / codex / kimi / opencode) pastes a "I zen'd FED / I fixed routing /
I cleaned configs" report with a change table, verify it as an **auditor, not a reader** —
and specifically verify the identity-vs-runtime split held.

Worked example: grok-build "zen FED for opencode/openclaw/hermes" report audited live 2026-08-09.
Report table claimed 7 files changed; every row verified against live probes; 3 findings surfaced
(hardcoded key in wrapper, SOT drift, doctrine reversal question). Verdict: runtime clean,
identity intact, 2 cleanup items + 1 F13 decision.

## Verification checklist

1. **Hash-snapshot BEFORE and AFTER.** `md5sum` + `stat -c '%y'` every file the report claims
   to touch (haproxy.cfg, opencode.json, openclaw.json, HERMES/config.yaml, wrapper scripts)
   at audit start; re-run after the sibling finishes. The report's "changed" list must match
   actual mtime/hash deltas. A report claiming a file changed when the hash is identical =
   the report is describing intent, not reality.

2. **Verify identity tree untouched.** `find /root/AAA/a2a-server/agent-cards -type f -newermt '<session-start>'`
   must be EMPTY. Also check `AAA/agents/`, `SOUL.md`, `bound_to`, `class`, `species` — the WHO
   layer. A runtime-zen run may touch `model` / `base_url` / `apiKey` / `order` (WHICH) but NEVER cards.

3. **Probe the front door with auth, not curl -sf.** `curl -sf` lies on litellm (401 without
   key looks like "down"). Use `curl -w '%{http_code} %{time_total}s'` with
   `Authorization: Bearer $LITELLM_MASTER_KEY`, and `ss -tlnp` for listening truth.

4. **Beware the "fixed it" that breaks a different rule.** A sibling fixing "keys being unset"
   may hardcode the secret into a world-readable wrapper script (mode 755 + literal `sk-...`
   = 5-R violation: never hardcode, never > mode 600). Always `stat -c '%a'` any script the
   report claims to have modified, and grep for literal key material.

5. **Watch for silent doctrine reversal.** "Zen" that flips primary → direct (or FED → direct)
   contradicts the FED=primary/direct=fallback doctrine if unstated. The report may claim
   "order only, 0 providers removed" — verify `enabled_providers` / provider counts unchanged
   AND the primary didn't silently flip lanes. If it did flip, that's an F13 decision, not a
   sibling decision.

6. **Check SOT drift.** If the sibling edited live configs but not `/root/.config/federation-models.json`
   (the declared SOT), flag it as runtime drift — not identity corruption, but a consistency debt.
   Fix later by aligning the SOT only; still zero card writes.

## Verdict shape

```
table: claim → live-probe result (✅ verified / ⚠️ nuance / ❌ wrong)
+ security findings (hardcoded secrets, mode violations)
+ one open F13 decision if the change reversed a doctrine
```

Then EXECUTE the cleanup within authority tier instead of bouncing options back.

## Live evidence from the 2026-08-09 audit (reference)

- HAProxy health check: `option httpchk GET /health/liveliness` + `timeout check 3000` → front
  door :4000 back to 200 in 2.9ms (was 503; `/health` full sweep = 8.9s killed the 1s check).
- litellm-proxy (3rd stack) parked: `systemctl disable --now` + drop-in `parked-20260809.conf`.
- litellm-escape `no-db.conf`: `UnsetEnvironment=DATABASE_URL POSTGRES_URL ARIFOS_MEMORY_POSTGRES_URL VAULT999_DB` + `Environment=PORT=` guard.
- Wrapper finding: `/usr/local/bin/hermes-asi-wrapper.sh` mode 755 with literal `sk-lit-91ae...` key.
- SOT drift: federation-models.json still said opencode primary=`litellm-federation/opencode` while
  live opencode.json primary=`deepseek/deepseek-v4-pro`.
