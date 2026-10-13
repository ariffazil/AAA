# public-claims — Public Observation Contract compiler (infra tier)

**Owner:** fi-003 (Qwen Code, 333-AGI) · **F13 GO:** 2026-10-12 · **Proposal:** `/root/arif-fazil.com/forge_work/proposals/fi-003/public-observation-contract-2026-10-12/`

## What

`generate-public-claims.cjs` probes the declared sources and bakes `claims.json` (a conformant `arifos://shared/observation-envelope/v1` set) into the mcp vhost. Served; refreshed every 15 min.

## Lane / cron

```
*/15 * * * * /root/.local/bin/jitu-guard public-claims && /usr/bin/node /root/AAA/scripts/public-claims/generate-public-claims.cjs >> /var/log/arifos/public-claims.log 2>&1
```

## Inputs / outputs

| | Path |
|---|---|
| contract (in) | `/var/www/html/mcp/shared/controlling-claims.json` |
| claims (out, served) | `/var/www/html/mcp/shared/claims.json` |
| public URL | https://mcp.arif-fazil.com/shared/claims.json |

Sources probed (read-only): kernel `http://127.0.0.1:8088/health` (required), `https://mcp.arif-fazil.com/.well-known/mcp/server.json`, AAA `http://127.0.0.1:3001/health`.

## Honesty invariants (structural)

- unresolved field → `UNMEASURED` (never a pass)
- source down → `UNREACHABLE`
- rule `reachable` → state `REACHABLE` (observed, no verdict)
- a PASS/FAIL is asserted only via `state_map` or a pass/fail rule

## Reversibility

- stop: remove the crontab line above
- unwire: `rm -rf /var/www/html/mcp/shared/` + revert the page snapshot lines
- script is idempotent; running it by hand has no side effect beyond writing `claims.json`
