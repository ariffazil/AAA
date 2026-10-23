# Scheduler audit — P1 (one-by-one, not a rate)

**measured** 2026-10-23T03:56Z · host forge · read-only

```
jobs 33 · enabled 32 · disabled 1 · last_status=error 1
```

## The one failure — and it is a real finding, not a flake

| field | value |
|---|---|
| name | `🜂 Site drift watch — Caddy config + bundle pointer` |
| id | `a39cfb467193` |
| schedule | every 360m |
| script | `constitutional-drift-watch.py` |
| last_error | `Script exited with code 1` + `DRIFT produced-but-not-served` |

The non-zero exit is the script **doing its job**: it detects drift and exits 1 so the runner
records a failure. The runner treats a detector's positive result as a job failure. That is a
metric-design defect, not a script defect — and it hides a genuine incident.

## The drift it found, verified independently

```
dist/index.html     -> assets/index-RlEEP0al.js     built  2026-10-21 20:19
webroot index.html  -> assets/index-BASIvgqQ.js     live   2026-10-20 21:29
probe https://arif-fazil.com/assets/index-RlEEP0al.js -> HTTP 404
```

**A build from 21 October exists that was never deployed.** The site has been serving a
three-day-old bundle while `dist/` holds a newer one whose entry asset does not resolve. This
is exactly the class the site's own AGENTS.md deploy gate exists to catch, and the only sensor
reporting it is the one marked "error".

## Consequence for the federation's honesty metric

"83 of 86 runs succeeded" describes the fleet's ability to avoid emitting a non-zero exit.
It does not describe whether anything was observed. **The single "failed" job was the only one
that told the truth in that window.** Optimising the success rate would have suppressed it.

## Classification and next step

- Detector-correct, deploy-stale, public-surface → fix is an **L4 deploy** (site bundle).
- **HOLD for ARIF.** Not executed: deploying a 3-day-old untested bundle to a public surface
  without a verified `make verify-pages` pass would be the wrong first move.
- Separable L1 fix (additive, not executed): make a detector's positive result report as
  `DETECTED` rather than `error`, so a working sensor stops looking like a broken one — while
  still surfacing the incident. That is a runner-contract change, not a cron edit.

## Falsifier

If `https://arif-fazil.com/assets/index-RlEEP0al.js` returns 200, or if the webroot index hash
equals the dist index hash, the drift has been deployed and this finding is stale.
