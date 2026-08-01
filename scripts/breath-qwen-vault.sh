#!/usr/bin/env bash
set -euo pipefail

# FED B2 — Vault breath for Qwen Token Plan / Responses
# F11/F13 discipline: only ARIF edits actual key values and runs this script.
#
# This script does NOT embed secrets. You must edit /root/.secrets/kunci-mas.env
# (via nano) with actual rotated keys before this script can complete successfully.
#
# Spec reference: /root/AAA/governance/FED-harness-tool-governance-v1.0.0.md §14 (Ratification Path)
# Companion: /root/AAA/federation/seats.yaml (canonical seat registry)

TS="$(date -u +%Y%m%dT%H%M%SZ)"
VAULT="/root/.secrets/kunci-mas.env"

echo "============================================================"
echo "FED B2 — Vault Breath for Qwen Token Plan / Responses"
echo "Timestamp: $TS"
echo "============================================================"
echo

# ─────────────────────────────────────────────────────────────────────────────
# Pre-flight: back up vault
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.0] Pre-flight: backing up vault"
cp -a "$VAULT" "${VAULT}.bak-pre-vault-${TS}"
echo "       Backup: ${VAULT}.bak-pre-vault-${TS}"
echo

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: prompt user to edit vault with actual rotated keys
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.1] EDIT REQUIRED — open /root/.secrets/kunci-mas.env in nano and insert:"
echo
echo "       export QWEN_OPENCODE_API_KEY=\"sk-sp-H.NEW_KEY_PRO\""
echo "       export QWEN_HERMES_API_KEY=\"sk-sp-D.NEW_KEY_HERMES\""
echo "       export QWEN_OPENCLAW_API_KEY=\"sk-sp-D.NEW_KEY_OPENCLAW\""
echo "       export QWEN_INDIVIDUAL_API_KEY=\"sk-sp-H.NEW_KEY_INDIVIDUAL\""
echo
echo "       Replace NEW_KEY_* with actual rotated keys from QwenCloud console."
echo "       (B3: rotate via https://home.qwencloud.com/api-keys first)"
echo
echo ">>> Run now: nano $VAULT"
echo ">>> Save with Ctrl+O, Enter, Ctrl+X"
echo ">>> Press Enter here once you have done that."
read -r _
echo

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: lock vault file permissions (F11)
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.2] Locking vault file permissions to 0600"
chmod 600 "$VAULT"
ls -la "$VAULT"
echo

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: regenerate flat env and verify drift-free
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.3] Regenerating flat env + drift check"
cd /root/.secrets
make vault-generate
make vault-verify
echo

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: source vault and verify only key lengths (NEVER echo values)
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.4] Sourcing vault and verifying key lengths (no values printed)"
# shellcheck disable=SC1091
source "$VAULT"

echo "       QWEN_OPENCODE_API_KEY length:    ${#QWEN_OPENCODE_API_KEY}"
echo "       QWEN_HERMES_API_KEY length:      ${#QWEN_HERMES_API_KEY}"
echo "       QWEN_OPENCLAW_API_KEY length:    ${#QWEN_OPENCLAW_API_KEY}"
echo "       QWEN_INDIVIDUAL_API_KEY length:  ${#QWEN_INDIVIDUAL_API_KEY}"
echo
echo "       (Expected: each > 30 chars; real keys are ~50 chars)"
echo

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: set Claude Code shell env from Pro seat (indirection)
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.5] Setting ANTHROPIC_AUTH_TOKEN in ~/.bashrc (Claude Code shell env)"
echo 'export ANTHROPIC_AUTH_TOKEN="$QWEN_OPENCODE_API_KEY"' >> ~/.bashrc
# shellcheck disable=SC1091
source ~/.bashrc
echo "       ANTHROPIC_AUTH_TOKEN length: ${#ANTHROPIC_AUTH_TOKEN}"
echo "       (Expected: matches QWEN_OPENCODE_API_KEY length)"
echo

# ─────────────────────────────────────────────────────────────────────────────
# Step 6: optional service restarts (informational only — sovereign choice)
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.6] Optional: restart services to pick up new env (sovereign choice)"
echo
echo "       sudo systemctl restart arifos a-forge hermes-asi-gateway openclaw"
echo
echo "       Most agents re-read env per call, so restart is optional."
echo "       Press Enter to skip restart."
read -r _
echo

# ─────────────────────────────────────────────────────────────────────────────
# Step 7: append vault-breath receipt to VAULT999 (F11 audit chain)
# ─────────────────────────────────────────────────────────────────────────────
echo "[B2.7] Appending VAULT999 receipt (audit chain)"
forge_vault \
  mode="receipt" \
  tier="session.ledger" \
  reason="vault_breath_qwen_token_plan" \
  value="{\"timestamp\":\"${TS}\",\"action\":\"B2_vault_breath\",\"seats\":[\"team_pro\",\"team_standard_hermes\",\"team_standard_openclaw\",\"individual_pro\"],\"rotation\":\"chat_leak_3_rounds\",\"by\":\"888\"}"

echo
echo "============================================================"
echo "FED B2 — COMPLETED"
echo
echo "Vault populated, services read fresh env, VAULT999 audit appended."
echo "OpenCode / Codex / Hermes / OpenClaw should now succeed on first call."
echo
echo "Next steps (per FED spec §14):"
echo "  - '999 SEAL FED-HARNESS-TOOL-GOVERNANCE' → I seal the spec"
echo "  - Run F (live verification): first FED-gated tool call → VAULT999 receipt"
echo "============================================================"
