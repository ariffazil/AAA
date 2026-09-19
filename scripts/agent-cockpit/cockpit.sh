#!/bin/bash
# Agent cockpit — one-shot check. Run from cron or by hand.
# Output: BM, 3 sections (brief / signal / stuck). Arif nampak dalam 5 saat.
set -e
DIR="/root/AAA/scripts/agent-cockpit"
echo "════════════════════════════════════════"
echo "📡 AGENT COCKPIT — $(date -u '+%Y-%m-%d %H:%M UTC')"
echo "════════════════════════════════════════"
echo ""
echo "── Morning brief ──"
python3 "$DIR/morning_brief.py"
echo ""
echo "── Attention signal ──"
python3 "$DIR/attention_signal.py"
echo ""
echo "── Stuck-agent ──"
python3 "$DIR/stuck_detector.py"
echo ""
