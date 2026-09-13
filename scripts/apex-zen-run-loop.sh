#!/bin/bash
# APEX-ZEN Runtime Loop — runs all 3 sources + reality binder + router
# Cron entry: see /root/AAA/scripts/apex-zen-cron.txt
set -e

LOG="/root/VAULT999/apex-zen-loop.log"
mkdir -p "$(dirname "$LOG")"

echo "[$(date -Iseconds)] APEX-ZEN loop start" >> "$LOG"

# Phase 1a: collect telemetry from session wire.jsonl
python3 /root/AAA/scripts/apex-zen-session-collector.py --since 1h >> "$LOG" 2>&1 || \
    echo "[$(date -Iseconds)] session-collector failed" >> "$LOG"

# Phase 1b: pull telemetry from arifFlow :7073 (real artifact source)
python3 /root/AAA/scripts/apex-zen-ariflow-source.py >> "$LOG" 2>&1 || \
    echo "[$(date -Iseconds)] ariflow-source failed" >> "$LOG"

# Phase 1c: bind Reality — L1/L2/L3/L4 witness objects
python3 /root/AAA/scripts/apex-zen-reality-binder.py --latest 5 >> "$LOG" 2>&1 || \
    echo "[$(date -Iseconds)] reality-binder failed" >> "$LOG"

# Phase 2: route consequences
python3 /root/AAA/scripts/apex-zen-consequence-router.py >> "$LOG" 2>&1 || \
    echo "[$(date -Iseconds)] router failed" >> "$LOG"

echo "[$(date -Iseconds)] APEX-ZEN loop end" >> "$LOG"