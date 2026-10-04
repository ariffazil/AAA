# Apex Scalar Replication — Session Detail (2026-08-14)

> Dispatched to Qwen Code (GLM-5.2) after Kimi Code hit billing quota wall.
> Committed `b2a0dd7a`. Live-verified from `/opt/a-forge/app/dist/`.

## The gap

arifOS `:8088/health` measures all 5 apex scalars:
```json
"apex_scalars": {
  "G":      { "value": 0.4714, "status": "MEASURED" },
  "C_dark": { "value": 0.1225, "status": "MEASURED" },
  "W3":     { "value": 0.7439, "status": "MEASURED" },
  "h":      { "value": 0.7669, "status": "MEASURED" },
  "QDF":    { "value": 0.4137, "status": "MEASURED" }
}
```

A-FORGE `:7071/health` reported `{ value: null, status: "UNMEASURED" }` for all five, while `apex_scalars_policy.replication_strategy` literally said "A-FORGE reads apex_scalars from arifOS /health."

**This is the "documentation theater" anti-pattern:** a health endpoint documents a delegation/replication strategy that the runtime never executes.

## Detection pattern (general — apply to any federation organ)

1. `curl -s localhost:<port>/health | jq '.apex_scalars'`
2. If all values are `null` and `apex_scalars_policy.replication_strategy` or `delegated_to` is non-empty → documentation theater.
3. Grep source: `grep -rn "apex_scalars\|replication_strategy\|delegated_to" src/` — if the strategy string exists in the health response builder but no `fetch()` call reads the delegated source → confirmed.

## The fix

### GovernanceBridge.ts — `fetchApexScalars()`

Generalized from existing `fetchCanonicalG()` (which only fetched G):

```typescript
export interface ScalarReplica {
  value: number;
  status: "REPLICATED";        // never MEASURED — we didn't measure
  source: "arifos.health";
  replicated_at: string;
}

export interface ApexScalarReplicaSet {
  G: ScalarReplica | null;
  C_dark: ScalarReplica | null;
  W3: ScalarReplica | null;
  h: ScalarReplica | null;
  QDF: ScalarReplica | null;
}
```

Key design decisions:
- **`status: "REPLICATED"` not `"MEASURED"`** — provenance preserved (F2 TRUTH + F7 HUMILITY). A-FORGE did not measure; it replicated.
- **3s timeout** (up from 2s for `fetchCanonicalG`) — apex scalar computation on arifOS side can be slow.
- **Partial response support** — if arifOS returns some scalars but not all, only available ones are replicated.
- **No caching** — `/health` is low-frequency; freshness > perf.

### server.ts — `/health` handler

Handler became `async`. Calls `fetchApexScalars()` at top. On success → `REPLICATED` entries. On failure → `null / "UNREACHABLE"` entries (changed from `UNMEASURED` to distinguish "can't reach source" from "source hasn't measured").

`apex_scalars_policy` gained:
- `replicated_from: "arifos.health:8088"`
- `replication_status: "active" | "degraded" | "unreachable"`
- `replication_latency_ms: <number>`

### Test file

`test/apexScalarReplication.test.ts` — 7 cases:
1. Full response → all 5 REPLICATED
2. arifOS unreachable → all null / UNREACHABLE
3. Partial response → only available ones REPLICATED
4. REPLICATED not MEASURED (provenance check)
5. HTTP 500 from arifOS → graceful null
6. Missing apex_scalars key in response → graceful null
7. Non-numeric value → graceful null

## Deploy sequence

1. `cd /root/A-FORGE && npm test` → 205 pass, 5 fail (pre-existing EphemeralGenesisRunner)
2. `rsync -av dist/ /opt/a-forge/app/dist/`
3. CHDIR fix (see SKILL.md Deploy pitfalls): drop-in override for WorkingDirectory + ExecStart
4. `systemctl daemon-reload && systemctl restart a-forge.service`
5. Poll `:7071/health` — verify `apex_scalars.*.status == "REPLICATED"`

## Live verification (2026-08-14 01:33 MYT)

```
G:       value=0.4716, status=REPLICATED
C_dark:  value=0.1226, status=REPLICATED
W3:      value=0.7439, status=REPLICATED
h:       value=0.7668, status=REPLICATED
QDF:     value=0.4138, status=REPLICATED
replicated_from: arifos.health:8088
replication_status: active
replication_latency_ms: 6
```

## Worker agent dispatch note

Kimi Code v0.35 hit `403 quota exceeded` — billing cycle exhausted. Qwen Code (GLM-5.2 via z.ai) successfully completed the same SPEC headlessly. **Always have a fallback coding CLI when dispatching SPEC-based forge tasks.** Kimi Code's `provider.auth_error: 403` is a hard wall — no retry helps; switch provider immediately.
