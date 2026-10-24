# Observatory audit — 2026-10-24T04:25Z

**Trigger:** sovereign report that the public Observatory page shows `unavailable` / `missing` across most blocks.
**Method:** read the served snapshot (`/api/public-state`), the writer (`scripts/emit_observatory_snapshot.py` + `scripts/build_public_state.py`), the cron entry, the writer log, and the client renderer (`/_shared/observatory.js`). No block was judged from the page alone.

## Pipeline status: ALIVE

```
cron (root)      4-59/10 * * * *  jitu-guard emit_observatory_snapshot && build_public_state.py
last write       2026-10-24T12:14:18+08
snapshot id      obs_20261024_041416.json   signature: signed (ed25519:sha256:698cc1ab26357272)
public-state     92883 bytes · http 200 · schema arifos.public-state.v1
generated_at     2026-10-24T04:14:18Z   (≈4 min old at audit time)
writer EXIT=0
```

The "unavailable" text is mostly the *renderer* not finding a field, not the writer failing.

## D1 — FIXED: Daily Reality Pulse mislabelled every organ

**Symptom:** `arifOS UNKNOWN · A-FORGE UNKNOWN · AAA UNKNOWN · GEOX DOWN · WEALTH UNKNOWN · WELL UNKNOWN`, while the organ cards on the same page all reported `live / http 200`.

**Cause (two bugs in one function, `renderPulse`):**

1. It read `transport, dependency, capability, governance, identity, last_receipt, contract` — five of those seven fields are **not emitted** by `arifos.public-state.v1`. The real organ record has `liveness, readiness, capability, governance`.
2. It fed `governance` into the health aggregator, and the aggregator reads `.value` first. GEOX's governance value is `"HOLD"`, which the semantic mapper classifies as `down` — so a **healthy** organ rendered red because of a **governance verdict**.

**Fix applied** (`/var/www/html/_shared/observatory.js`, backup `.bak-20261024-preaudit`):
pulse = `liveness + readiness` (state field preferred over free text so `"http 200"` and `"27 public tools"` classify correctly); governance moved to the cell tooltip; comment records why.

**Verification** — same aggregator run against the live snapshot:

| organ | before | after |
|---|---|---|
| arifOS | UNKNOWN | HEALTHY |
| A-FORGE | UNKNOWN | HEALTHY |
| AAA | UNKNOWN | HEALTHY |
| GEOX | DOWN | HEALTHY |
| WEALTH | UNKNOWN | HEALTHY |
| WELL | UNKNOWN | HEALTHY |

Served file carries the change (`/_shared/observatory.js`, last-modified 04:22:25Z).

**Residual:** `cache-control: max-age=14400` — a browser that loaded the old file keeps it for up to 4h. Not changed here (Caddy config, T2).

## D2 — OPEN (real, not display): the pipeline's own findings

Emitted by the writer, unprompted:

| id | sev | finding |
|---|---|---|
| F-004 | **HIGH** | `verify=True replay=True chain_verified=False` — chain entries=275, corrupt=0, **gaps=40** |
| F-002 | MED | `proven_live=3/8 tested_fresh=3 invocable=8` — 5 kernel tools untested for 160557s (44.6h) |
| F-005 | MED | identity present **6/8** organs |
| F-006 | MED | transport **11/11**, semantic **0/11** — transport alignment is not federation proof |
| F-008 | LOW | `source=afe27dde3eaf` vs `deployed=e8dd4ab` |
| F-001/003/007/009 | — | RESOLVED |

These are the honest core. The page is right to show 5 open findings.

## D3 — STRUCTURAL GAPS (absent evidence, not failure)

| block | state | cause |
|---|---|---|
| `metabolism` (11 stages) | metrics `unknown` — void_rate, hold_rate, latency, queue_depth, last_error all null | arifFlow per-actor telemetry not wired into the snapshot; only `stage` is populated |
| `evidence` / `authority` top-level | ABSENT | contract emits them under other blocks; the page's `unavailable` is a mapping gap, not a missing probe |
| `organs.<aforge|wealth|well>.governance` | null | collector maps governance only for arifOS/GEOX |
| `organs.aaa.capability` | null | no `tools/list` probe for the control plane |
| `substrate` | `NOT_PROVEN` | by design: "no infrastructure probe in this snapshot; floor counts measure governance, not substrate" |
| P1-5 / P1-6 receipt federation | `CANARY 2026-09-09 — RETEST REQUIRED` | 45 days stale; retest before any GO |

## Verdict

```
renderer          one real defect, FIXED and verified (6/6 organs)
writer            healthy, honest, fresh (4 min), signed
data defects      5 open findings, dominated by chain gaps=40 (HIGH)
structural gaps   6 blocks that carry no evidence yet — labelled as such, not green
surface freshness fresh snapshot, but 4h client cache on the renderer
```

Nothing on this page was made greener than its evidence. The one thing that *was* false was a red: a healthy GEOX shown as DOWN.

## Reproduce

```
curl -s https://arifos.arif-fazil.com/api/public-state | python3 -m json.tool | head
tail -40 /var/log/arifos/observatory.log
grep -n "healthOf" /var/www/html/_shared/observatory.js
```
