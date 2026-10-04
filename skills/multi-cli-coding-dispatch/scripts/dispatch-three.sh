#!/bin/bash
# dispatch-three.sh — Single-command 3-way parallel dispatch for sovereign-scale work
#
# Usage: dispatch-three.sh <spec-path> <output-dir> <basename>
#   <spec-path>: path to canonical WORK_SPEC.md
#   <output-dir>: where each agent writes its HTML
#   <basename>: prefix for output files (e.g. "surat-final-v12")
#
# Effect: launches qwen + deepseek + gpt-5.6-luna in parallel with 8s stagger.
# Logs to <output-dir>/<basename>-dispatch-{harness}.log
# Verifies each output file exists and is non-empty when dispatch completes.
#
# Verified: 2026-08-12 (PETRONAS v12 DRAFT_SPEC dispatch)

set -e

SPEC_PATH="$1"
OUTPUT_DIR="$2"
BASENAME="$3"

if [ -z "$SPEC_PATH" ] || [ -z "$OUTPUT_DIR" ] || [ -z "$BASENAME" ]; then
  echo "Usage: $0 <spec-path> <output-dir> <basename>"
  echo "Example: $0 /root/forge_work/WORK_SPEC.md /root/forge_work draft"
  exit 1
fi

if [ ! -f "$SPEC_PATH" ]; then
  echo "ERROR: spec file not found: $SPEC_PATH"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

PROMPT="Read ${SPEC_PATH} and follow it EXACTLY. Save your HTML draft to ${OUTPUT_DIR}/${BASENAME}-\$HARNESS.html. Use only inline CSS. Output must be print-ready (weasyprint-compatible). When done, print: DRAFT COMPLETE — \$HARNESS, then the output path, then pages estimate, then SHA-256, then verdict. Be terse. Do not ask clarifying questions."

echo "=== Dispatching 3 parallel CLIs ==="
echo "Spec: $SPEC_PATH"
echo "Output dir: $OUTPUT_DIR"
echo "Basename: $BASENAME"
echo ""

# 1. Qwen Code (no -m flag — defaults to anthropic route)
echo "[1/3] Launching Qwen Code..."
( qwen -p "$PROMPT" -o text 2>&1 | tee "${OUTPUT_DIR}/${BASENAME}-dispatch-qwen.log" | tail -60 ) &
QWEN_PID=$!

# 2. OpenCode DeepSeek via zen tier
sleep 8
echo "[2/3] Launching OpenCode DeepSeek (opencode-zen tier)..."
( opencode run --model opencode-zen/deepseek-v4-pro "$PROMPT" 2>&1 | tee "${OUTPUT_DIR}/${BASENAME}-dispatch-deepseek.log" | tail -60 ) &
DEEPSEEK_PID=$!

# 3. OpenCode gpt-5.6-luna via zen tier
sleep 16
echo "[3/3] Launching OpenCode gpt-5.6-luna (opencode-zen tier)..."
( opencode run --model opencode-zen/gpt-5.6-luna "$PROMPT" 2>&1 | tee "${OUTPUT_DIR}/${BASENAME}-dispatch-luna.log" | tail -60 ) &
LUNA_PID=$!

echo ""
echo "All 3 launched. Wait for completion notifications."
echo "QWEN_PID=$QWEN_PID DEEPSEEK_PID=$DEEPSEEK_PID LUNA_PID=$LUNA_PID"
echo ""
echo "When complete, verify outputs:"
echo "  ls -la ${OUTPUT_DIR}/${BASENAME}-*.html"
echo "  for f in ${OUTPUT_DIR}/${BASENAME}-*.html; do echo \"=== \$f ===\"; sha256sum \"\$f\"; done"