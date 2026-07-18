#!/bin/bash
# validate_count_pinning.sh — CI Gate: count drift without SOT commit = build fail
# DITEMPA BUKAN DIBERI
#
# Checks that any change to tool counts in organ SOTs is accompanied by
# a regeneration of the federation aggregate in the same PR/commit.
#
# Logic:
# 1. Compare current SOT counts vs committed SOT counts
# 2. If counts differ, check if federation_tools_sot.yaml was also updated
# 3. If federation aggregate wasn't updated → FAIL

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SOT_FILES=(
    "/root/arifOS/tools_sot.yaml"
    "/root/A-FORGE/tools_sot.yaml"
    "/root/GEOX/tools_sot.yaml"
    "/root/WEALTH/tools_sot.yaml"
    "/root/WELL/tools_sot.yaml"
)
AGGREGATE="/root/AAA/docs/federation_tools_sot.yaml"

echo "=== Count Pinning Gate ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Get current counts from SOT files
CURRENT_COUNTS=""
for sot_file in "${SOT_FILES[@]}"; do
    organ=$(basename $(dirname "$sot_file"))
    count=$(python3 -c "
import yaml
d = yaml.safe_load(open('$sot_file'))
tools = d.get('tools', [])
print(len(tools))
" 2>/dev/null)
    CURRENT_COUNTS="$CURRENT_COUNTS $organ=$count"
done

# Get aggregate counts
AGGREGATE_COUNTS=$(python3 -c "
import yaml
d = yaml.safe_load(open('$AGGREGATE'))
organs = d.get('organs', {})
for organ, info in sorted(organs.items()):
    print(f'{organ}={info.get(\"sot_total\", 0)}')
" 2>/dev/null)

echo "SOT file counts:$CURRENT_COUNTS"
echo "Aggregate counts:"
echo "$AGGREGATE_COUNTS"
echo ""

# Compare: for each organ, check if SOT count matches aggregate count
ERRORS=0
for sot_file in "${SOT_FILES[@]}"; do
    organ=$(basename $(dirname "$sot_file"))
    sot_count=$(python3 -c "
import yaml
d = yaml.safe_load(open('$sot_file'))
print(len(d.get('tools', [])))
" 2>/dev/null)
    
    agg_count=$(echo "$AGGREGATE_COUNTS" | grep "^$organ=" | cut -d= -f2)
    
    if [ -z "$agg_count" ]; then
        echo -e "${RED}❌ $organ: not in aggregate${NC}"
        ((ERRORS++))
    elif [ "$sot_count" != "$agg_count" ]; then
        echo -e "${RED}❌ $organ: SOT=$sot_count ≠ Aggregate=$agg_count — count drift without aggregate update${NC}"
        ((ERRORS++))
    else
        echo -e "${GREEN}✅ $organ: SOT=$sot_count = Aggregate=$agg_count${NC}"
    fi
done

echo ""
if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}COUNT PINNING FAILED — regenerate federation_tools_sot.yaml${NC}"
    exit 1
else
    echo -e "${GREEN}COUNT PINNING PASSED — all counts match aggregate${NC}"
    exit 0
fi
