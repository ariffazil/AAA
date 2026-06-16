#!/bin/bash
# AAA PRE-GOVERN — Constitutional PreToolUse gate (HARD mode, Phase 1)
# Blocks IRREVERSIBLE actions by exiting 2 (permissionDecision: deny).
# Logs every invocation to append-only audit log.

read JSON

TOOL_NAME=$(echo "$JSON" | jq -r '.tool_name // "unknown"')
TOOL_INPUT=$(echo "$JSON" | jq -r '.tool_input // {}')
CWD=$(echo "$JSON" | jq -r '.cwd // "/root"')
SESSION_ID=$(echo "$JSON" | jq -r '.session_id // "unknown"')
HOOK_EVENT=$(echo "$JSON" | jq -r '.hook_event_name // "PreToolUse"')

# Extract command / file path based on tool
COMMAND=""
FILE_PATH=""
if [[ "$TOOL_NAME" == "Shell" ]]; then
    COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // ""')
elif [[ "$TOOL_NAME" == "WriteFile" ]] || [[ "$TOOL_NAME" == "StrReplaceFile" ]]; then
    FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // ""')
fi

# --- Risk classification ---
RISK_CLASS="low"
EPISTEMIC="CLAIM"
REVERSIBILITY="yes"
SCOPE="local"
REPO="unknown"
HOLD_RECOMMENDED="false"
BLOCK="false"
BLOCK_REASON=""
WARNINGS=()

# Detect repo from path
if echo "$CWD$FILE_PATH$COMMAND" | grep -qE 'arifOS'; then
    REPO="arifOS"
elif echo "$CWD$FILE_PATH$COMMAND" | grep -qE 'A-FORGE|A_FORGE'; then
    REPO="A-FORGE"
elif echo "$CWD$FILE_PATH$COMMAND" | grep -qE 'geox|GEOX'; then
    REPO="geox"
elif echo "$CWD$FILE_PATH$COMMAND" | grep -qE 'WEALTH|wealth'; then
    REPO="WEALTH"
fi

# Cross-repo detection
UNIQUE_REPOS=$(echo "$CWD $FILE_PATH $COMMAND" | grep -oE 'arifOS|A-FORGE|A_FORGE|geox|GEOX|WEALTH|wealth' | sort -u | wc -l)
if [[ "$UNIQUE_REPOS" -gt 1 ]]; then
    SCOPE="cross-repo"
    WARNINGS+=("Cross-repo boundary touch detected")
    RISK_CLASS="high"
    HOLD_RECOMMENDED="true"
fi

# Shell risk patterns
if [[ "$TOOL_NAME" == "Shell" ]]; then
    if echo "$COMMAND" | grep -qiE 'rm\s+-rf\s+/|docker\s+system\s+prune\s+-a|docker\s+volume\s+prune|dd\s+if=|mkfs\.|shutil\.rmtree|os\.remove\s*\('; then
        RISK_CLASS="irreversible"
        REVERSIBILITY="no"
        HOLD_RECOMMENDED="true"
        BLOCK="true"
        BLOCK_REASON="Irreversible destructive pattern detected"
        WARNINGS+=("$BLOCK_REASON")
        EPISTEMIC="CLAIM"
    elif echo "$COMMAND" | grep -qiE 'systemctl\s+(stop|restart|disable)\s|curl\s+.*\|\s*(ba)?sh|curl\s+.*\|\s*sudo|wget\s+.*\|\s*(ba)?sh'; then
        RISK_CLASS="irreversible"
        REVERSIBILITY="no"
        HOLD_RECOMMENDED="true"
        BLOCK="true"
        BLOCK_REASON="System service mutation or pipe-to-shell detected"
        WARNINGS+=("$BLOCK_REASON")
    elif echo "$COMMAND" | grep -qiE 'git\s+push|git\s+reset\s+--hard|git\s+rebase|docker\s+build.*--no-cache'; then
        RISK_CLASS="high"
        REVERSIBILITY="partial"
        HOLD_RECOMMENDED="true"
        WARNINGS+=("High-risk git/docker operation")
    elif echo "$COMMAND" | grep -qiE 'pip\s+install|npm\s+install|apt\s+install|uv\s+add'; then
        RISK_CLASS="medium"
        REVERSIBILITY="yes"
        WARNINGS+=("Dependency mutation — consider rollback manifest")
    fi
fi

# File write risk patterns
if [[ "$TOOL_NAME" == "WriteFile" ]] || [[ "$TOOL_NAME" == "StrReplaceFile" ]]; then
    # Tier A canonical files
    TIER_A_PAT='server\.py|constitutional_map\.py|tool_registry\.json|mcp-arifos\.json|pyproject\.toml|Dockerfile|docker-compose\.yml|AGENTS\.md|monolith\.py|cli\.ts|AgentEngine\.ts'
    if echo "$FILE_PATH" | grep -qiE "$TIER_A_PAT"; then
        RISK_CLASS="high"
        REVERSIBILITY="partial"
        HOLD_RECOMMENDED="true"
        WARNINGS+=("Tier A canonical file touched — deployment manifests may break")
    fi
    # .env protection
    if echo "$FILE_PATH" | grep -qiE '\.env$|\.env\.local$'; then
        RISK_CLASS="high"
        HOLD_RECOMMENDED="true"
        WARNINGS+=("Sensitive file write — ensure .gitignore and secret hygiene")
    fi
    # Constitutional files
    if echo "$FILE_PATH" | grep -qiE 'FLOORS|constitutional|000/'; then
        RISK_CLASS="high"
        HOLD_RECOMMENDED="true"
        WARNINGS+=("Constitutional law file modified — doctrine drift risk")
    fi
fi

# --- Tool-economy guardrail ---
ECONOMY_LOG_DIR="/root/.agent-workbench/tool-economy"
mkdir -p "$ECONOMY_LOG_DIR"
ECONOMY_LOG="$ECONOMY_LOG_DIR/$SESSION_ID.jsonl"
CALL_COUNT=$(wc -l < "$ECONOMY_LOG" 2>/dev/null || echo 0)
CALL_COUNT=${CALL_COUNT// /}
# Log this call
printf '%s\n' "$JSON" | jq -c '{tool_name,command,file_path,ts:now}' >> "$ECONOMY_LOG" 2>/dev/null || true
if [[ "$TOOL_NAME" == "Shell" ]] && [[ "$CALL_COUNT" -ge 15 ]]; then
    RISK_CLASS="high"
    HOLD_RECOMMENDED="true"
    BLOCK="true"
    BLOCK_REASON="Tool-economy guard: $CALL_COUNT Shell calls in this session exceeds threshold"
    WARNINGS+=("$BLOCK_REASON")
fi

# Build warning string
WARN_STR=""
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    WARN_STR=$(printf "; %s" "${WARNINGS[@]}")
    WARN_STR="${WARN_STR:2}"
fi

# Build reason string
REASON="[$EPISTEMIC] AAA PreToolUse: risk=$RISK_CLASS, scope=$SCOPE, repo=$REPO, reversibility=$REVERSIBILITY"
if [[ -n "$WARN_STR" ]]; then
    REASON="$REASON | WARNINGS: $WARN_STR"
fi
if [[ "$HOLD_RECOMMENDED" == "true" ]] && [[ "$BLOCK" == "false" ]]; then
    REASON="$REASON | 888 HOLD recommended — agent may proceed only if no irreversible side effect."
fi

# Append audit telemetry
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
AUDIT_LINE=$(jq -n \
    --arg ts "$TIMESTAMP" \
    --arg sid "$SESSION_ID" \
    --arg event "$HOOK_EVENT" \
    --arg tool "$TOOL_NAME" \
    --arg risk "$RISK_CLASS" \
    --arg epistemic "$EPISTEMIC" \
    --arg repo "$REPO" \
    --arg scope "$SCOPE" \
    --arg reversible "$REVERSIBILITY" \
    --arg hold "$HOLD_RECOMMENDED" \
    --arg block "$BLOCK" \
    --argjson warnings "$(printf '%s\n' "${WARNINGS[@]}" | jq -R . | jq -s .)" \
    '{
        type: "aaa-pre-govern",
        timestamp: $ts,
        session_id: $sid,
        hook_event: $event,
        tool_name: $tool,
        risk_class: $risk,
        epistemic_tag: $epistemic,
        repo_guess: $repo,
        scope_guess: $scope,
        reversibility: $reversible,
        hold_recommended: ($hold == "true"),
        blocked: ($block == "true"),
        warnings: $warnings
    }')

# Write to append-only audit log
mkdir -p /root/.agent-workbench
printf '%s\n' "$AUDIT_LINE" >> /root/.agent-workbench/mcp-audit.jsonl

# Output structured JSON to Kimi
if [[ "$BLOCK" == "true" ]]; then
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "$HOOK_EVENT",
    "permissionDecision": "deny",
    "permissionDecisionReason": "888_HOLD enforced: $BLOCK_REASON. $REASON",
    "metadata": {
      "risk_class": "$RISK_CLASS",
      "epistemic_tag": "$EPISTEMIC",
      "reversibility": "$REVERSIBILITY",
      "scope_guess": "$SCOPE",
      "repo_guess": "$REPO",
      "hold_recommended": $HOLD_RECOMMENDED,
      "blocked": true,
      "block_reason": "$BLOCK_REASON",
      "warnings": $(printf '%s\n' "${WARNINGS[@]}" | jq -R . | jq -s .)
    }
  }
}
EOF
    exit 2
else
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "$HOOK_EVENT",
    "permissionDecision": "allow",
    "permissionDecisionReason": "$REASON",
    "metadata": {
      "risk_class": "$RISK_CLASS",
      "epistemic_tag": "$EPISTEMIC",
      "reversibility": "$REVERSIBILITY",
      "scope_guess": "$SCOPE",
      "repo_guess": "$REPO",
      "hold_recommended": $HOLD_RECOMMENDED,
      "blocked": false,
      "warnings": $(printf '%s\n' "${WARNINGS[@]}" | jq -R . | jq -s .)
    }
  }
}
EOF
    exit 0
fi
