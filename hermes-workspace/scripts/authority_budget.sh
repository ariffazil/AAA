#!/bin/bash
# authority_budget.sh — scar_authority_contraction_v1 runtime scorer
# Usage: ./authority_budget.sh <clarity> <evidence> <mandate> <risk> <reversibility>
# Scores are 0.0–1.0 floats

CLARITY="${1:-0.5}"
EVIDENCE="${2:-0.5}"
MANDATE="${3:-0.5}"
RISK="${4:-0.5}"
REVERSIBILITY="${5:-0.5}"

# Weights from policy
W_CLARITY=0.30
W_EVIDENCE=0.35
W_MANDATE=0.20
W_RISK=-0.35
W_REVERSIBILITY=0.10

# Compute weighted budget
BUDGET=$(python3 -c "
weights = [$W_CLARITY, $W_EVIDENCE, $W_MANDATE, $W_RISK, $W_REVERSIBILITY]
scores  = [$CLARITY,   $EVIDENCE,   $MANDATE,   $RISK,   $REVERSIBILITY]
budget  = sum(w * s for w, s in zip(weights, scores))
budget  = min(budget, $EVIDENCE)
budget  = max(0.0, min(1.0, budget))
print(round(budget, 3))
")

# Determine mode
if (( $(echo "$BUDGET >= 0.75" | bc -l) )); then
  MODE="answer"
elif (( $(echo "$BUDGET >= 0.50" | bc -l) )); then
  MODE="advise"
elif (( $(echo "$BUDGET >= 0.30" | bc -l) )); then
  MODE="clarify"
else
  MODE="pause"
fi

echo "{\"budget\": $BUDGET, \"mode\": \"$MODE\"}"
