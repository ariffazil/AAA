---
name: flow-gap-sweep
version: 1.0.0
description: "Use when probing flow or hunting federation gaps and flaws."
owner: HERMES
risk_tier: low
autonomy_tier: T1
tags: [federation, flow, health, floors, arifflow, niat, gap-analysis]
triggers:
  - "probe current flow"
  - "gaps to seal"
  - "flaws to fix"
  - "flow health"
  - "federation gap sweep"
  - "identify flaws"
capability_tier: fed-agent-subagent
---

# Flow-Gap Sweep — transport green ≠ flow healthy

A sweep that stops at "all ports return 200" answers a question nobody asked.
All organs up proves nothing about code age, floor semantics, per-actor flow
discipline, or autonomous loops. Run four checks IN THIS ORDER — each finds a
defect class the previous one misses. Transport health gets ONE line in the
report, never the headline.

## Step 0 — Transport (one command, one line of report)

```bash
for url in 8088 7071 7072 7073 7074 7075 8081 18082 18083 18087 18097 18099 18075 18094 18101; do
  curl -s -o /dev/null -w "%{http_code} :$url\n" --max-time 5 http://localhost:$url/health
done
systemctl --failed --no-pager
```

Do NOT trust any port list as exhaustive; extend as organs are added.

## Step 1 — Deploy drift (fix this FIRST if found)

```bash
cd /root/arifOS && git fetch origin main -q    # never count on stale remote-tracking refs
git rev-parse HEAD                             # source
git -C /opt/arifos/current rev-parse HEAD      # deployed
git rev-list --count $(git -C /opt/arifos/current rev-parse HEAD)..HEAD
```

Pitfall: `/health` says nothing about code age. A deployed SHA that is an
ancestor of source HEAD by a large count means many floor/semantic fixes may
already exist in source — diagnose drift before diagnosing any downstream
"bug", or you will root-cause problems already fixed.

## Step 2 — Kernel floors: read PROVENANCE, not pass/fail

```bash
curl -s http://localhost:8088/health \
  | jq '.layer_health.constitutional | {failing: .floors_failing, agg: .floors_aggregate, prov: .floors_provenance}'
```

- One payload can contradict ITSELF: `floors_detail` says `fail` while
  `floors_measurement_status` says `unmeasured` for the same floor. When
  `floors_provenance` says `governance_kernel_alias` or `unmeasured_default`,
  the value arrived through an alias key (e.g. F6 via `kappa_r`) fed by a
  structural placeholder, not an instrument — treat the floor as UNMEASURED,
  never report it as a real failure.
- `floor_passed=true` only when ALL floors are measured AND passing.
  `floors_pass: 10/13` is a count of measured-passes, never a score.
- An F1 failure usually traces OUTSIDE the kernel — F1 is fed by the arifFlow
  FQ probe and the failing number is often one specific actor's quotient
  (check per-actor before touching kernel code).
- Floors are non-deterministic across reads (13/13 → 7 pass within an hour
  has been measured); never quote a floor number without a timestamp.

## Step 3 — arifFlow per-actor FQ

```bash
curl -s http://localhost:7073/health \
  | jq '{constellation: .vector.diagnosis.constellation, actors: .fq.per_actor}'
```

Read per actor: `quotient`, `diagnosis`, `held`.

- `held: true` = execution-dominance hold (executes without mechanical
  verify). The cure is running verifies for the held actor — never loosen the hold.
- Actors with `quotient: null` are UNMEASURED and drag the constellation
  toward SIMULATION. Unmeasured is not neutral — it IS the pathology. Either
  instrument the actor or remove it from tracking.
- `legacy_verdict`/`legacy_diagnosis` (FLOWING/BALANCED/OPTIMAL) and scalar FQ
  are fossils — quote the vector diagnosis, never the scalar.

## Step 4 — Autonomous loops (silent death)

```bash
systemctl is-active arifos-niat-executor
journalctl -u arifos-niat-executor -n 30 --no-pager | grep -E "DONE|Verdict"
tail -3 /root/.local/share/arifos/niat_execution_log.jsonl
```

- A failed niat run is NOT a crash: `DONE: 0 completed, 0 blocked, N errors`
  with `Verdict: UNKNOWN` per proposal means the kernel judge returned UNKNOWN
  for every proposal and the executor exits 1 on the count. Loop items stay
  open silently — a run that failed days ago can hold an open safety item
  nobody sees. Always read what the loop items SAY, not just that it failed.
- Ledger schema can rot silently: check the last log lines for null
  timestamp/niat_id/status fields before trusting any aggregate over it.

## Step 5 — Resource pressure

`df -h /` (flag ≥82%, diagnose before 85%), `free -h`, `uptime` load.
Then the docker-fleet probes (stats, system df, Caddy scan) belong to
`federation-health` — run them only if Step 0 or this step flagged something.

## Report shape (to the sovereign, BM, no jargon)

Findings ranked: deploy drift → failing floors with provenance → held +
unmeasured actors → dead/stuck loops → resource pressure. Good news (clean
false-DOWN checks, recovered services) gets one line. Close with ONE proposed
execution order and ask which to run — not a menu of options.
