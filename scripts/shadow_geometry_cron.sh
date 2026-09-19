#!/bin/bash
# Shadow geometry + behavioral drift + mechanical checks — 6h cadence
# Forged 2026-09-19 by 333-AGI (F13 "finish near term"). Output → cockpit/shadow-matrix/.
set -euo pipefail
OUT=/root/AAA/cockpit/shadow-matrix
mkdir -p "$OUT"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 /root/arifOS/arifosmcp/tools/shadow_geometry_comparison.py > "$OUT/geometry-latest.txt" 2>&1
python3 /root/arifOS/arifosmcp/tools/frame_behavioral_drift.py > "$OUT/drift-latest.txt" 2>&1
echo "{\"ts\":\"$TS\",\"geometry\":\"$OUT/geometry-latest.txt\",\"drift\":\"$OUT/drift-latest.txt\"}" > "$OUT/last-run.json"
