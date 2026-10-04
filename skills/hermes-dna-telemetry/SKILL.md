---
name: hermes-dna-telemetry
description: "Operate the HERMES DNA constitutional telemetry subsystem — unified institutional ledger, MAP/ATLAS/ECHO metrics engine, and the :7080 telemetry sidecar. Use when asked to check institutional health, refresh MAP/ATLAS/ECHO, inspect the institutional ledger, query the telemetry sidecar, or reason about the FREEZE phase (observation-only, no coupling)."
version: "1.0.0"
tags:
  - telemetry
  - map-atlas-echo
  - institutional-ledger
  - freeze
  - hermes-dna
  - governance
---

# HERMES DNA Telemetry

Constitutional telemetry for the arifOS federation: **MAP sees · ATLAS governs · ECHO witnesses**. Built 2026-08-09. The double-helix framing: right strand = ECHO (agent learning, L1-L6), left strand = SCAR (human meaning, H1-H6), hydrogen bonds = ATLAS (law over capability), reading mechanism = MAP.

## THE FREEZE — binding constitutional ruling (2026-08-09)

**Observation only. NO coupling to behavior.** Do NOT wire metrics → geometry, Kabarkan→PG→behavior, or SCAR→behavior short-circuit. The metrics EXIST to measure; they do NOT drive anything yet. Reason: coupling before the noise floor is known turns signal+noise into reactivity. Exit criteria (all must pass before coupling): variance < threshold per signal, no unexplained trend, ≥3 sample points per signal, F13 review.

Binding ruling: `/root/forge_work/2026-08-09/INSTITUTIONAL-ZEN-FREEZE.md`

## Components

| Component | Path | Role |
|---|---|---|
| Institutional Ledger | `/root/.local/share/arifos/institutional_ledger.jsonl` | Unified receipts from 4 streams, SHA-256 dedup, idempotent |
| Ledger Collector | `/root/scripts/ledger_unify.py` | Reads output_gate + apex + hook + vault receipts → unified entries |
| Metrics Engine | `/root/scripts/institution_metrics.py` | Computes MAP/ATLAS/ECHO → `/root/AAA/state/institution_metrics.json` |
| Telemetry Sidecar | `/root/scripts/institution_telemetry.py` → **:7080** | Serves FQ (arifFlow live) + MAP/ATLAS/ECHO |
| Refresh Cron | `hermes-dna-metrics-refresh` (every 15m, no_agent) | Runs ledger_unify + metrics, prints summary |

## The 3 metrics

- **MAP** (Model Alignment Potential) — understanding quality. Proxy: plan/action success rate ÷ reasoning complexity (action types).
- **ATLAS** (Authority-To-Landscape) — governance leverage. Proxy: governed actions ÷ governance artifacts (13 floors + 2×2 matrix + 8 lanes = 25).
- **ECHO** (Epistemic Continuity Through Honest Observation) — learning honesty. Proxy: retained improvements ÷ honest observations (failures + near misses + anomalies + drift + unexpected successes). Denominator MUST include honest observations, not just failures — an institution that sees nothing is blind, not healthy.

## Usage

```bash
# Query sidecar
curl http://127.0.0.1:7080/health    # FQ + MAP + ATLAS + ECHO merged
curl http://127.0.0.1:7080/metrics   # full telemetry JSON
curl http://127.0.0.1:7080/ledger    # ledger entry count

# Manual refresh (cron does this every 15m)
/usr/local/lib/hermes-agent/profiles/aaa-hermes/scripts/hermes-dna-refresh.sh
# or directly:
python3 /root/scripts/ledger_unify.py && python3 /root/scripts/institution_metrics.py
```

## Reading the numbers (baseline 2026-08-09 first read)

- MAP 0.06 CALIBRATING — ledger is mostly vault commit receipts, not "plans"; expect this to recalibrate
- ATLAS 1176 STABLE — 29k+ governed actions ÷ 25 artifacts; high governance leverage
- ECHO 0.001 CALIBRATING — 41 retained ÷ 29k+ observations; VAULT is observation-heavy, retained improvements still few. **This is the freeze's job to characterize.**
- SCAR continuity 1.0 — 6/6 scars verified (`/root/memory/H5-scars/H5_SCAR_REGISTRY.json`, key is `stats.total_scars`)

## Pitfalls

- **Scar registry stats key is `total_scars`, not `total`** — `H5_SCAR_REGISTRY.json` uses `stats.total_scars/verified/stale`.
- **Veo/imagen are NOT part of this subsystem** — media gen lives in `gemini-media-gen`; telemetry just counts their receipts.
- **arifFlow :7073 is a Rust daemon — never touch it to add telemetry.** The sidecar :7080 exists precisely so FQ (metabolism) and MAP/ATLAS/ECHO (constitutional) stay separate planes.
- **Sidecar is a foreground server** — start via `terminal(background=true)`, log to `/root/AAA/state/institution_telemetry.log`.
- **Freeze is a constitutional ruling, not a suggestion** — a future session that "helpfully" wires metrics→geometry violates F4 (reduces clarity) and the F13 ruling. Do not.

## Doctrine references

- `/root/forge_work/2026-08-09/INSTITUTIONAL-ZEN-FREEZE.md` — the binding freeze ruling
- `/root/memory/H5-scars/H5_SCAR_REGISTRY.json` — left strand (human scars, sovereign gate: index reads OK, scar content needs `scar:<id>`)
- `/root/memory/H6-constitution/H6_SCAR_ROOTS.md` — scar→lesson→law→floor lineage

DITEMPA BUKAN DIBERI.
