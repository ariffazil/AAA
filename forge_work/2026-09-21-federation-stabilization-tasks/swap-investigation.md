# SWAP CHURN INVESTIGATION — 2026-09-21

> **Status:** observation · T0 · FI-008
> **Probe timestamp:** 2026-09-21T02:24 UTC

## Current state

| metric | value |
|---|---|
| Total RAM | 31 GiB |
| Used | 17 GiB |
| Available | 14 GiB |
| Swap total | 8.0 GiB |
| **Swap used** | **7.3 GiB (91.25%)** |
| PSI memory avg60 | 0.00 (idle) |
| Load avg 1/5/15 | 2.32 / 2.98 / 2.99 |

## /proc/vmstat cumulative counters (over uptime)

| counter | value | notes |
|---|---|---|
| `pswpin` | 59,422,662 | 59M pages swapped IN over uptime |
| `pswpout` | 92,811,374 | 92M pages swapped OUT over uptime |
| `pgfault` | 18,781,828,216 | 18B minor faults (no I/O) |
| `pgmajfault` | 56,479,347 | 56M MAJOR faults (I/O required) |
| `pginodesteal` | 316,521 | inode pages reclaimed |

## vmstat 1 5 live samples

```
r  b  swpd     free   buff   cache   si    so    bi    bo   in    cs   us sy id wa st gu
5  1  6603644 4165920 2396408 9433088 146  229  8432  2802 9677  16   13  3 77  1  6  0
2  1  6603644 4147020 2409848 9438296   0    0 16944  204 18738 26723 31  7 53  8  1  0
2  1  6603644 4139008 2424584 9439640   0    0 14776  368 17859 27322 29  5 57  8  1  0
4  1  6603500 4101704 2438896 9440200 144    0 14812 2004 23880 33399 41 12 37  9  2  0
4  0  6603500 4090356 2454104 9441488   0    0 15900  904 20823 29853 31  7 51  9  2  0
```

## Top swap consumers

| PID | comm | swap |
|---|---|---|
| 1022599 | node | 5944 kB |
| 1 | systemd | 848 kB |

## Interpretation

**The 91.25% swap usage is largely historical, not active churn.**

- Cumulative `pswpout` = 92M pages × 4 KiB ≈ 370 GiB total swapped OUT over uptime
- Cumulative `pswpin` = 59M pages × 4 KiB ≈ 240 GiB total swapped IN
- **But current live activity:** `si=0-146, so=0-229` — light active churn

The kernel is keeping 6.6 GB of pages swapped out even though 14 GiB of RAM is available. This is **deliberate kernel behavior**: pages that haven't been touched recently get pushed to swap to keep a hot working set in RAM. It is *not* a sign of memory pressure.

**The earlier chat observation that swap=91% → "system has memory pressure" was a misdiagnosis.** PSI avg60=0.00 confirms no current pressure. Major page faults (56M cumulative) suggest occasional I/O from cold-start, not chronic paging.

## When it WOULD be a problem

- PSI avg60 > 5% sustained for 1+ hour
- `si` (swap-in) > 1000 sustained
- Free memory < 2 GiB sustained
- Load average > CPU count × 2

None of these conditions are met.

## The actual substrate story

The 91% swap is healthy long-running-server behavior. The system has:
- 14 GiB hot RAM available
- 6.6 GiB cold swap (mostly unmapped inactive pages)
- ~3 GiB cache/buffer headroom

The bigger substrate finding is G3's actual gate: **the 95 dirty files in /opt/arifos/current** represent pending deployment work, not memory pressure. The dirty tree IS what we should fix — separate from swap.

## Conclusion

**G3 swap sub-gate is GREEN, not RED.** The earlier chat overstated the severity. No swap action needed. Continue with G3's other work items (zombie reap, dirty tree capture).

## Action

None for swap. Continue monitoring PSI avg60 in the substrate canary (planned G7).
