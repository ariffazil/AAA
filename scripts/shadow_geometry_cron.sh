#!/bin/bash
# Shadow geometry + behavioral drift + mechanical checks — 6h cadence
# Forged 2026-09-19 by 333-AGI (F13 "finish near term"). Output → cockpit/shadow-matrix/.
set -euo pipefail
OUT=/root/AAA/cockpit/shadow-matrix
mkdir -p "$OUT"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 /root/arifOS/arifosmcp/tools/shadow_geometry_comparison.py > "$OUT/geometry-latest.txt" 2>&1
python3 /root/arifOS/arifosmcp/tools/frame_behavioral_drift.py > "$OUT/drift-latest.txt" 2>&1

# Evidence gate (D4, 2026-10-03 FI-003) — enforces the N>=5 promotion rule that
# was prose-only in MODEL_SHADOWS.md from 2026-08-26 until now. Its exit 1 means
# "over-claim present", which is a FINDING, not a crash: capture it so `set -e`
# cannot abort the cycle before last-run.json is written. A cycle that dies
# silently is exactly how the 9-day / 37-run dead-cron gap stayed invisible.
set +e
python3 /root/AAA/scripts/shadow_evidence_gate.py > "$OUT/evidence-gate-latest.txt" 2>&1
GATE_RC=$?
set -e

echo "{\"ts\":\"$TS\",\"geometry\":\"$OUT/geometry-latest.txt\",\"drift\":\"$OUT/drift-latest.txt\",\"evidence_gate\":\"$OUT/evidence-gate-latest.txt\",\"evidence_gate_rc\":$GATE_RC}" > "$OUT/last-run.json"
