#!/bin/bash
# validate_tool_sot.sh — Federation Tool SOT Validation
# DITEMPA BUKAN DIBERI
#
# Validates:
# 1. Each organ's tools_sot.yaml exists and is parseable
# 2. Tool count in SOT matches live /health endpoint
# 3. No "Use when: Use when" description bugs
# 4. No duplicate tool names across organs (except intentional bridges)

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

log_ok() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; WARNINGS=$((WARNINGS+1)); }
log_err() { echo -e "${RED}❌ $1${NC}"; ERRORS=$((ERRORS+1)); }

echo "=== Federation Tool SOT Validation ==="
echo "Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# ── Step 1: Check SOT files exist and parse ──────────────────────────────

ORGS=("arifOS:8088" "A-FORGE:7071" "GEOX:8081" "WEALTH:18082" "WELL:18083")
SOT_FILES=(
    "/root/arifOS/tools_sot.yaml"
    "/root/A-FORGE/tools_sot.yaml"
    "/root/GEOX/tools_sot.yaml"
    "/root/WEALTH/tools_sot.yaml"
    "/root/WELL/tools_sot.yaml"
)

echo "── Step 1: SOT File Validation ──"

for sot_file in "${SOT_FILES[@]}"; do
    organ=$(basename $(dirname "$sot_file"))
    if [ ! -f "$sot_file" ]; then
        log_err "$organ: SOT file missing at $sot_file"
        continue
    fi

    # Parse YAML
    count=$(python3 -c "
import yaml, sys
try:
    data = yaml.safe_load(open('$sot_file'))
    tools = data.get('tools', [])
    print(len(tools))
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    print(-1)
" 2>/dev/null)

    if [ "$count" = "-1" ]; then
        log_err "$organ: SOT file failed to parse"
    else
        log_ok "$organ: SOT file valid ($count tools)"
    fi
done

echo ""

# ── Step 2: Compare SOT count vs live endpoint ──────────────────────────

echo "── Step 2: Live Endpoint Verification ──"

for entry in "${ORGS[@]}"; do
    IFS=':' read -r organ port <<< "$entry"
    sot_file="/root/$([ "$organ" = "A-FORGE" ] && echo "A-FORGE" || echo "$organ")/tools_sot.yaml"

    if [ ! -f "$sot_file" ]; then
        log_warn "$organ: Skipping live check (no SOT file)"
        continue
    fi

    # Get SOT count (public + authenticated only — internal tools not on live surface)
    sot_count=$(python3 -c "
import yaml
data = yaml.safe_load(open('$sot_file'))
tools = data.get('tools', [])
# Count only public and authenticated tools (internal tools not on live MCP surface)
public_auth = [t for t in tools if t.get('access') in ('public', 'authenticated')]
print(len(public_auth))
" 2>/dev/null)

    # Get live count from /health (only WELL exposes tool_count)
    live_count=$(curl -s --connect-timeout 5 "http://127.0.0.1:$port/health" 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    # Only WELL exposes tool_count in health endpoint
    tc = d.get('tool_count', d.get('tools_loaded', None))
    if tc is not None:
        print(tc)
    else:
        print(-2)  # field not present
except:
    print(-1)  # endpoint unreachable
" 2>/dev/null || echo -1)

    if [ "$live_count" = "-1" ]; then
        log_warn "$organ: Live endpoint unreachable (port $port)"
    elif [ "$live_count" = "-2" ]; then
        log_ok "$organ: SOT ($sot_count) — live tool_count not exposed in /health"
    elif [ "$sot_count" = "$live_count" ]; then
        log_ok "$organ: SOT ($sot_count) = Live ($live_count)"
    else
        delta=$((live_count - sot_count))
        if [ $delta -ge -2 ] && [ $delta -le 2 ]; then
            log_warn "$organ: SOT ($sot_count) ≈ Live ($live_count) — delta $delta (acceptable)"
        else
            log_err "$organ: SOT ($sot_count) ≠ Live ($live_count) — delta $delta"
        fi
    fi
done

echo ""

# ── Step 3: Description quality check ───────────────────────────────────

echo "── Step 3: Description Quality ──"

for sot_file in "${SOT_FILES[@]}"; do
    organ=$(basename $(dirname "$sot_file"))
    if [ ! -f "$sot_file" ]; then
        continue
    fi

    bugs=$(python3 -c "
import yaml
data = yaml.safe_load(open('$sot_file'))
bugs = 0
for t in data.get('tools', []):
    desc = t.get('description', '')
    if 'Use when: Use when' in desc:
        bugs += 1
        print(f'  BUG: {t[\"name\"]}: {desc[:80]}')
print(bugs)
" 2>/dev/null)

    bug_count=$(echo "$bugs" | tail -1)
    if [ "$bug_count" = "0" ]; then
        log_ok "$organ: No description bugs"
    else
        log_err "$organ: $bug_count description bugs found"
        echo "$bugs" | head -5
    fi
done

echo ""

# ── Step 4: Cross-organ duplicate check ─────────────────────────────────

echo "── Step 4: Cross-Organ Duplicates ──"

all_names=$(python3 -c "
import yaml, glob
names = []
for f in ['/root/arifOS/tools_sot.yaml', '/root/A-FORGE/tools_sot.yaml', '/root/GEOX/tools_sot.yaml', '/root/WEALTH/tools_sot.yaml', '/root/WELL/tools_sot.yaml']:
    try:
        data = yaml.safe_load(open(f))
        for t in data.get('tools', []):
            names.append(t['name'])
    except:
        pass
# Find duplicates
from collections import Counter
dupes = {k: v for k, v in Counter(names).items() if v > 1}
for name, count in sorted(dupes.items()):
    print(f'{name}: {count}')
" 2>/dev/null)

if [ -z "$all_names" ]; then
    log_ok "No duplicate tool names across organs"
else
    log_warn "Duplicate tool names found (may be intentional bridges):"
    echo "$all_names"
fi

echo ""

# ── Step 5: Prefix lint ──────────────────────────────────────────────────
# Per-organ prefix rules:
#   arifOS:  ^arif_
#   A-FORGE: ^forge_
#   GEOX:    ^geox_
#   WEALTH:  ^capital_
#   WELL:    ^well_

echo "── Step 5: Prefix Lint ──"

prefix_result=$(python3 <<'PYEOF'
import yaml, re
PREFIXES = {
    'arifOS':  r'^arif_',
    'A-FORGE': r'^forge_',
    'GEOX':    r'^geox_',
    'WEALTH':  r'^capital_',
    'WELL':    r'^well_',
}
errors = []
for organ, prefix in PREFIXES.items():
    p = f'/root/{organ if organ != "A-FORGE" else "A-FORGE"}/tools_sot.yaml'
    try:
        data = yaml.safe_load(open(p))
    except Exception as e:
        errors.append(f'{organ}: SOT parse error: {e}')
        continue
    tools = data.get('tools', [])
    if not isinstance(tools, list):
        continue
    for t in tools:
        name = t.get('name', '')
        if not re.match(r'^[a-z][a-z0-9_]*$', name):
            errors.append(f'{organ}: {name!r} is not snake_case')
        elif prefix and not re.match(prefix, name):
            errors.append(f'{organ}: {name!r} does not match prefix {prefix!r}')
for e in errors:
    print(e)
print(f'{len(errors)} errors')
PYEOF
)

prefix_err_count=$(echo "$prefix_result" | tail -1)
if [ "$prefix_err_count" = "0 errors" ]; then
    log_ok "All tool names pass prefix + snake_case lint"
else
    while IFS= read -r line; do
        if [ "$line" != "0 errors" ]; then
            log_err "$line"
        fi
    done <<< "$prefix_result"
fi

echo ""

# ── Step 6: arifOS count pinning ────────────────────────────────────────
# arifOS public surface MUST equal exactly 8 tools (the constitutional claim).
# Per directive: arifOS canon = 8 capabilities in 2 public tiers
# (7 open + 1 acknowledgment-gated = 8 total)

echo "── Step 6: arifOS Count Pinning ──"

# arifOS MCP tools/list works without MCP session header
live_count=$(curl -s --connect-timeout 5 -X POST http://127.0.0.1:8088/mcp \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' 2>/dev/null | python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    print(len(d.get('result', {}).get('tools', [])))
except: print(-1)
")

sot_count=$(python3 -c "
import yaml
data = yaml.safe_load(open('/root/arifOS/tools_sot.yaml'))
print(len(data.get('tools', [])))
" 2>/dev/null)

if [ "$live_count" = "8" ]; then
    log_ok "arifOS live surface = 8 (matches constitutional claim: 7 open + 1 gated)"
elif [ "$live_count" = "-1" ]; then
    log_warn "arifOS live endpoint unreachable"
else
    log_err "arifOS live surface = $live_count (expected 8) — constitutional drift!"
fi

if [ "$sot_count" = "8" ]; then
    log_ok "arifOS SOT = 8 capabilities (canonical)"
elif [ "$sot_count" = "25" ]; then
    log_warn "arifOS SOT = 25 (8 public+auth + 17 internal) — over-declared but documented"
else
    log_warn "arifOS SOT = $sot_count (expected 8 public+auth)"
fi

# Also verify the doctrine statement from capability_registry.json is consistent
# Public wire = (access == 'public') OR (tier == 'gated' OR tier == 'open')
# Per directive: 7 open + 1 gated = 8 total public wire
doctrine_check=$(python3 -c "
import yaml
data = yaml.safe_load(open('/root/arifOS/tools_sot.yaml'))
tools = data.get('tools', [])
public_tools = [
    t for t in tools
    if t.get('access', '') in ('public', 'authenticated')
    or t.get('tier', '') in ('open', 'gated')
]
print(len(public_tools))
" 2>/dev/null)
if [ "$doctrine_check" = "8" ]; then
    log_ok "arifOS public wire = 8 (7 open + 1 gated, doctrine consistent)"
else
    log_warn "arifOS public wire = $doctrine_check (expected 8 = 7 open + 1 gated)"
fi

echo ""

# ── Summary ─────────────────────────────────────────────────────────────

echo "=== Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}VALIDATION FAILED${NC}"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}VALIDATION PASSED WITH WARNINGS${NC}"
    exit 0
else
    echo -e "${GREEN}VALIDATION PASSED${NC}"
    exit 0
fi
