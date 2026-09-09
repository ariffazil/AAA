#!/bin/bash
# latency_report_hook.sh — Loop 3 Closer
# ════════════════════════════════════════
# Source this after every harness API call to report latency to FED.
# Gives reality authority over routing via latency data.
#
# Usage: source /root/AAA/scripts/latency_report_hook.sh
#        report_latency "provider" "model" latency_ms [status_code] [tokens_in] [tokens_out] [agent_id]
#
# ZEN_KERNEL: Reality must have authority over future behavior.
# DITEMPA BUKAN DIBERI.

FED_URL="${FED_URL:-http://127.0.0.1:7074}"
FED_DB="${FED_DB:-/root/.local/share/arifos/fed_state.db}"
LATENCY_LOG="/root/AAA/scripts/logs/latency_report.log"

report_latency() {
	local provider="$1"
	local model="$2"
	local latency_ms="$3"
	local status_code="${4:-200}"
	local tokens_in="${5:-0}"
	local tokens_out="${6:-0}"
	local agent_id="${7:-unknown}"
	local timestamp
	timestamp="$(date -u +%Y-%m-%dT%H:%M:%S%z)"

	# Log locally first
	mkdir -p "$(dirname "$LATENCY_LOG")"
	echo "[$timestamp] $provider/$model latency=${latency_ms}ms status=$status_code agent=$agent_id" >>"$LATENCY_LOG"

	# Try FED MCP endpoint (primary)
	local response
	response=$(curl -sf --max-time 5 -X POST "$FED_URL/mcp" \
		-H "Content-Type: application/json" \
		-H "Accept: application/json, text/event-stream" \
		-d "{
            \"jsonrpc\": \"2.0\",
            \"method\": \"tools/call\",
            \"params\": {
                \"name\": \"fed_report_latency\",
                \"arguments\": {
                    \"provider\": \"$provider\",
                    \"model\": \"$model\",
                    \"latency_ms\": $latency_ms,
                    \"status_code\": $status_code,
                    \"tokens_in\": $tokens_in,
                    \"tokens_out\": $tokens_out,
                    \"agent_id\": \"$agent_id\"
                }
            },
            \"id\": 1
        }" 2>/dev/null)

	if [ $? -ne 0 ] || [ -z "$response" ]; then
		# Fallback: write directly to SQLite
		if [ -f "$FED_DB" ]; then
			sqlite3 "$FED_DB" "INSERT OR REPLACE INTO route_latency 
                (provider_name, model_id, p50_ms, p95_ms, sample_count, last_sample)
                VALUES ('$provider', '$model', $latency_ms, $latency_ms, 1, '$timestamp');" 2>/dev/null
		fi
	fi

	# Emit to arifFlow witness
	curl -sf --max-time 3 -X POST "http://127.0.0.1:7073/ingest" \
		-H "Content-Type: application/json" \
		-d "{
            \"actor_id\": \"latency_report_hook\",
            \"session_id\": \"latency-$provider-$model\",
            \"step_type\": \"Verify\",
            \"epistemic_label\": \"Observation\",
            \"floor_verdict\": \"Pass\",
            \"payload\": {
                \"event\": \"latency_report\",
                \"provider\": \"$provider\",
                \"model\": \"$model\",
                \"latency_ms\": $latency_ms,
                \"status_code\": $status_code,
                \"agent_id\": \"$agent_id\",
                \"source\": \"latency_report_hook_loop3\"
            }
        }" >/dev/null 2>&1
}

# Export function for use in other scripts
export -f report_latency
export FED_URL FED_DB LATENCY_LOG
