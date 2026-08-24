#!/usr/bin/env bash
# grok-multimodal.sh — any AAA agent spawns Grok Build Imagine
# Native tools live ONLY on the Grok Build harness (FI-007):
#   image_gen · image_edit · image_to_video · reference_to_video
# Other agents cannot call those tools in-process. They spawn grok CLI.
#
# Usage:
#   grok-multimodal.sh image "prompt" [--out DIR] [--ratio 9:16]
#   grok-multimodal.sh edit  /path.jpg "prompt" [--out DIR] [--ratio 9:16]
#   grok-multimodal.sh video /path.jpg "prompt" [--out DIR] [--seconds 6]
#
# Auth: Grok OIDC on this VPS. No FED seat. Do not add grok to litellm.
# DITEMPA BUKAN DIBERI — 2026-08-25 FI-007

set -euo pipefail

MODE="${1:-}"
shift || true
OUTDIR="${GROK_MM_OUT:-/root/forge_work/grok-mm}"
RATIO="9:16"
SECONDS=6
IMAGE=""
PROMPT=""

usage() {
  sed -n '2,16p' "$0" | sed 's/^# //;s/^#//'
  exit 1
}

[[ -z "$MODE" ]] && usage

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUTDIR="$2"; shift 2 ;;
    --ratio) RATIO="$2"; shift 2 ;;
    --seconds) SECONDS="$2"; shift 2 ;;
    --image) IMAGE="$2"; shift 2 ;;
    -h|--help) usage ;;
    *)
      if [[ -z "$PROMPT" && -f "$1" && "$MODE" != "image" && -z "$IMAGE" ]]; then
        IMAGE="$1"; shift
      else
        PROMPT="${PROMPT:+$PROMPT }$1"; shift
      fi
      ;;
  esac
done

GROK_BIN="${GROK_BIN:-$(command -v grok || true)}"
[[ -x "$GROK_BIN" ]] || GROK_BIN=/root/.local/bin/grok
[[ -x "$GROK_BIN" ]] || { echo '{"ok":false,"error":"grok CLI not found"}' >&2; exit 2; }

mkdir -p "$OUTDIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TASK_ID="grok-mm-${STAMP}-$$"

case "$MODE" in
  image)
    [[ -n "$PROMPT" ]] || usage
    INSTR="Use the image_gen tool. Prompt: ${PROMPT}. aspect_ratio=${RATIO}. After generation, copy the file into ${OUTDIR}/${TASK_ID}.jpg. Reply with JSON only: {\"ok\":true,\"path\":\"...\",\"tool\":\"image_gen\"}."
    ;;
  edit)
    [[ -n "$IMAGE" && -f "$IMAGE" && -n "$PROMPT" ]] || usage
    INSTR="Use the image_edit tool. Source image (absolute path): ${IMAGE}. Prompt: ${PROMPT}. aspect_ratio=${RATIO}. Copy result into ${OUTDIR}/${TASK_ID}.jpg. Reply with JSON only: {\"ok\":true,\"path\":\"...\",\"tool\":\"image_edit\"}."
    ;;
  video)
    [[ -n "$IMAGE" && -f "$IMAGE" && -n "$PROMPT" ]] || usage
    INSTR="Use the image_to_video tool. Source image (absolute path): ${IMAGE}. Prompt: ${PROMPT}. duration=${SECONDS}. resolution_name=720p. Copy result into ${OUTDIR}/${TASK_ID}.mp4. Reply with JSON only: {\"ok\":true,\"path\":\"...\",\"tool\":\"image_to_video\"}."
    ;;
  *)
    echo '{"ok":false,"error":"mode must be image|edit|video"}' >&2
    exit 1
    ;;
esac

exec "$GROK_BIN" -p "$INSTR" --always-approve --output-format json
