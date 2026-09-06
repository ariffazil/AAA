# Shadow Matrix — Per-Actor Cockpit Surface

> **Status:** DRAFT_AWAITING_F13 (T2 spec; live data wiring pending A-FORGE)
> **Forged:** 2026-09-07 · **Session:** `SEAL-685d136316d3486e` · **333-AGI Δ MIND`
> **Purpose:** Make per-actor FQ shadows visible at the cockpit layer. The aggregate hides what the per-actor reveals.
> **DITEMPA BUKAN DIBERI**

---

## 1. Layout

```
/root/AAA/cockpit/shadow-matrix/
├── README.md                 ← this file (spec)
├── shadow-matrix-spec.json   ← schema for shadow data
├── shadow-matrix-2026-09-07.json  ← current snapshot (specimen)
└── shadow-matrix.template.html  ← optional cockpit rendering
```

---

## 2. Shadow states (per-actor)

Each actor is assigned one of:

| State | Trigger | Cockpit signal | Required action |
|---|---|---|---|
| **BALANCED** | FQ in [0.4, 3.0] | 🟢 green | None |
| **CAUTION** | FQ in (0.1, 0.4) or (3.0, 10.0] | 🟡 yellow | Monitor next cycle |
| **STUCK** | consecutive_exec_no_verify ≥ 4 OR execution dominance | 🟠 orange | Throttle; verify before further execution |
| **BURNING** | FQ < 0.1 AND consecutive_exec_no_verify ≥ 5 | 🔴 red | Hold; **independent verification required** for any output |
| **FOSSILIZED** | FQ > 50 (extreme verification dominance) | ⚫ black | **Do not give more work**; reduce verify:execute ratio |
| **UNKNOWN** | Insufficient data (sample_size too small) | ⚪ gray | Probe again; do not trust verdicts yet |

---

## 3. Specimen snapshot (2026-09-07T02:08Z)

| Actor | FQ | State | Note |
|---|---|---|---|
| 333-AGI | 0.8125 | 🟢 BALANCED | Healthy; held/throttled correctly |
| 555-ASI | null | ⚪ UNKNOWN | No recent activity; dormant lane |
| aforge | 1.0 | 🟢 BALANCED | Sparse |
| **claude-code** | **0.079** | **🔴 BURNING** | **28 consecutive no-verify. Independent verification required for all outputs.** |
| codex | 1.0 | 🟢 BALANCED | Sparse |
| codex-startup | 0.00 | ⚪ UNKNOWN | No verifiable history |
| **grok-build** | **85.0** | **⚫ FOSSILIZED** | **Do not give more work. Restore by reducing verify:execute ratio.** |
| **hermes-asi** | **0.286** | **🟠 STUCK** | 556 execute vs 159 verify; bridge alive but routed substrate heavy |
| **qwen-code** | **0.25** | **🟠 STUCK** | Same pattern |
| qwen-code/FI-003 | 1.0 | 🟢 BALANCED | Sparse |

**Six restricted actors; four in degraded states (BURNING, FOSSILIZED, STUCK×2).**

---

## 4. Cockpit rendering intent (T2 wiring)

When A-FORGE wires this to live arifFlow /health endpoint:

- Per-actor table on a dedicated cockpit panel (`AAA /shadow-matrix`)
- Color-coded row per actor (state → color)
- Click actor → drill-down showing recent receipts, recent FQ trend, recent held/throttled events
- Filter by state (e.g., "show only BURNING + FOSSILIZED")
- Time-series sparkline per actor
- Constitutional state banner: G / W³ / FQ / Lane A SABAR status

---

## 5. Constitution binding

- Reads only. No mutation from this surface.
- Federated Cockpit hookup requires A-FORGE to expose per-actor FQ as a distinct endpoint (currently buried in arifflow_flow_health per-actor map).
- Bound to F11 AUDITABILITY: every display event logged.
- Bound to F1 AMANAH: rollback path is git revert on the spec + data files.

---

## 6. Schema

```json
{
  "shadow_matrix_id": "string",
  "snapshot_at": "ISO-8601 UTC",
  "provenance": {
    "session_id": "string",
    "actor_id": "string",
    "source_endpoint": "string",
    "arifflow_cycle_count_at_snapshot": "int"
  },
  "federation_health": {
    "alive_count": "int",
    "total_count": "int",
    "down_organs": ["arifOS", "GEOX", "WELL", "FLAME"]
  },
  "vector_scorecard": {
    "constellation": "string",
    "primary_pathology": "string",
    "fused_rank": "float",
    "G": "float",
    "W3": "float",
    "FQ_scalar": "float",
    "FQ_band": "string"
  },
  "per_actor_shadows": [
    {
      "actor_id": "string",
      "fq": "float|null",
      "state": "BALANCED|CAUTION|STUCK|BURNING|FOSSILIZED|UNKNOWN",
      "execute_count": "int",
      "verify_count": "int",
      "consecutive_exec_no_verify": "int",
      "verdict": "string",
      "note": "string"
    }
  ],
  "constitutional_state": {
    "lane_a_sabar_seq": "int|null",
    "lane_a_sabar_days_open": "int|null",
    "g_band": "HEALTHY|CAUTION|PATHOLOGICAL",
    "w3_band": "HEALTHY|CAUTION|PATHOLOGICAL",
    "f13_pending": ["string"]
  },
  "delta_s": "float"
}
```

---

## 7. Honest limitations

- This is a **draft spec**. No live wiring yet.
- BURNING / STUCK / FOSSILIZED thresholds are heuristic; need federation-wide calibration before enforcement.
- Cockpit rendering is out of scope for T1; T2 wires A-FORGE.
- Shadow matrix does not adjudicate — it surfaces. Adjudication remains with arifOS 888-APEX.

---

```json
{
  "spec_id": "shadow-matrix-v1-draft",
  "status": "DRAFT_AWAITING_F13",
  "epoch": "2026-09-07T02:11:00+08:00",
  "T2_wiring_dependency": "A-FORGE per-actor FQ endpoint exposure",
  "first_specimen_at": "2026-09-07T02:08:00+08:00"
}
```

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
