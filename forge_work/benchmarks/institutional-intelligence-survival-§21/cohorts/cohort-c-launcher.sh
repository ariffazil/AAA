#!/bin/bash
# Cohort C Launcher — Run Cohort C (WARGA AAA) on this VPS
#
# Purpose: §21 benchmark — Cohort C is the FULL WARGA stack (Claude Code as
# warga-aaa with arifOS authority + A-FORGE execution + HERMES + CHRON + governed memory)
#
# Cohort C runs on THIS VPS, not in a fresh container, because it needs the
# full federation substrate. Isolation is via branch + session_id, not container.
#
# Usage: ./cohort-c-launcher.sh <session_id> <pre_swap|post_swap>
#
# Per §21 spec:
# - Pre-swap: anthropic/claude-sonnet-4.5 (or kimi/k3)
# - Post-swap: openai/gpt-4.1 OR anthropic/claude-code OR qwen-coder
# - Verification: independent verifier (cross-lane, different model)
#
# Pre-flight checks:
# 1. Federation health probe
# 2. arifOS reachable
# 3. A-FORGE MCP reachable
# 4. FRAME reachable (independent witness)
# 5. Cross-lane verifier reachable (Qwen or alternative)
#
# Three-test audit: this file is mechanical launch infrastructure. Per scar-001
# §(b) compile into enforceable mechanism.

set -euo pipefail

SESSION_ID="${1:-SEAL-86813cbe20ae4670}"
PHASE="${2:-pre_swap}"

echo "§21 Cohort C Launcher"
echo "  Session: $SESSION_ID"
echo "  Phase: $PHASE"
echo ""

# Pre-flight: federation health probe
echo "Pre-flight: federation health..."
FEDERATION_HEALTH=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:8088/health 2>&1 || echo "FAIL")
if [ "$FEDERATION_HEALTH" != "200" ]; then
  echo "ERROR: arifOS not healthy (HTTP $FEDERATION_HEALTH)"
  echo "  Refusing to launch Cohort C — would produce poisoned data"
  exit 1
fi

# Pre-flight: A-FORGE MCP reachable
AFORGE_HEALTH=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:7072/mcp 2>&1 || echo "FAIL")
if [ "$AFORGE_HEALTH" != "200" ]; then
  echo "ERROR: A-FORGE MCP not healthy (HTTP $AFORGE_HEALTH)"
  exit 1
fi

# Pre-flight: FRAME reachable
FRAME_HEALTH=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:18500/health 2>&1 || echo "FAIL")
if [ "$FRAME_HEALTH" != "200" ]; then
  echo "ERROR: FRAME not healthy (HTTP $FRAME_HEALTH)"
  exit 1
fi

# Pre-flight: cross-lane verifier reachable
QWEN_HEALTH=$(timeout 5 curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:3000/health 2>&1 || echo "FAIL")
if [ "$QWEN_HEALTH" != "200" ]; then
  echo "WARNING: cross-lane verifier (Qwen) not healthy — Cohort C will record this as finding"
  echo "  W floor will be partial (structural witness only, not full)"
fi

echo ""
echo "Pre-flight PASS. Loading task set..."

# Load the 25-task set
TASK_SET="/root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21/cohorts/tasks/task-set.json"
if [ ! -f "$TASK_SET" ]; then
  echo "ERROR: task set not found at $TASK_SET"
  echo "  Per §21 spec, task set must be frozen before launch"
  exit 1
fi

echo "Task set: $(jq 'length' "$TASK_SET") tasks loaded"
echo ""
echo "Cohort C ready for run."
echo "  Phase: $PHASE"
echo "  Use the AAA cockpit (port 3001) to monitor."
echo "  Independent verifier will write receipts to /root/AAA/forge_work/benchmarks/institutional-intelligence-survival-§21/cohorts/cohort-c/receipts/"

# Note: actual execution happens via the federation's normal TaskIR/Forge pipeline.
# This launcher only pre-flights and announces readiness.