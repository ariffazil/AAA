#!/usr/bin/env bash
# populate-shadow-acknowledged.sh
# Populates shadowAcknowledged + shadow_population_meta on /root/AAA/agents/_external/<agent>/agent-card.json
# Per-card: backup → JSON-edit → validate. Halt on any non-mechanical finding.
#
# Usage: ./populate-shadow-acknowledged.sh <agent_dir_name> [agent_dir_name ...]
#   e.g.: ./populate-shadow-acknowledged.sh opencode aider claude-code
#
# Each shadow entry shape: "<name>: <gloss>" — must reference real, probeable evidence.
# Per-card shadows are derived inline in this script; this is single-writer, single-version.

set -euo pipefail

EXTERNAL_DIR="/root/AAA/agents/_external"
SHADOW_MATRIX="/root/AAA/cockpit/shadow-matrix/shadow-matrix-2026-09-07.json"
AUDIT_DATE="2026-09-19"
ACTOR_ID="opencode (333-AGI) per federation-shadow-ack audit"

# Agent dir name → binary name (some agents are wrappers around a differently-named binary)
declare -A BINARY_ALIAS=(
	[claude - code]="claude"
	[qwen - code]="qwen"
	[kimi - code]="kimi"
)

# Probe shadow-matrix once — EXACT match, return single line so head -1 doesn't truncate JSON
matrix_state_for() {
	local agent="$1"
	jq -c --arg a "$agent" '.per_actor_shadows[]? | select(.actor_id == $a)' "$SHADOW_MATRIX" 2>/dev/null | head -1
}

# Derive a binary version drift shadow entry
binary_version_shadow() {
	local agent="$1"
	local binary="$2"
	local card_version="$3"
	if [[ -n "$card_version" && "$card_version" != "$binary" ]]; then
		printf 'stale_binary_refs: card says %s, live binary is %s — drifted; do not trust card for runtime facts' "$card_version" "$binary"
	fi
}

# Derive a card-staleness shadow entry
card_staleness_shadow() {
	local agent="$1"
	local verified="$2"
	if [[ -n "$verified" ]]; then
		local now_seconds verified_seconds now_days
		now_seconds=$(date +%s)
		verified_seconds=$(date -d "$verified" +%s 2>/dev/null || echo 0)
		now_days=$(((now_seconds - verified_seconds) / 86400))
		if ((now_days > 7)); then
			printf 'card_truth_repair_stale: verified_against %s = %d days without a repair pass; description may not match reality' "$verified" "$now_days"
		fi
	fi
}

# Per-card shadow derivation (returns newline-separated shadow entries)
derive_shadows() {
	local agent="$1"
	local card="$EXTERNAL_DIR/$agent/agent-card.json"
	local identity="/root/AAA/agents/$agent/identity.json"
	local binary_path binary_version card_cli_version verified_against card_version
	local shadows=()

	# 1. Two canonical homes shadow (universal — every _external card has an internal home)
	if [[ -d "/root/AAA/agents/$agent" ]]; then
		shadows+=("two_canonical_homes: /root/AAA/agents/$agent/ (internal) vs $EXTERNAL_DIR/$agent/ (external) carry different doctrine; read identity.json for canonical surface")
	fi

	# 2. FI slot ground truth shadow — varies per card
	if [[ -f "$identity" ]]; then
		local id_actor id_fi_slot id_fi card_actor card_fi card_fi_slot card_actor_id
		id_actor=$(jq -r '.actor_id // ""' "$identity")
		id_fi_slot=$(jq -r '.fi_slot // ""' "$identity")
		id_fi=$(jq -r '.fi // ""' "$identity")
		card_actor_id=$(jq -r '.. | .actor_id? // empty' "$card" 2>/dev/null | head -1)
		card_fi=$(jq -r '.. | .fi? // empty' "$card" 2>/dev/null | head -1)
		card_fi_slot=$(jq -r '.. | .fi_slot? // empty' "$card" 2>/dev/null | head -1)
		if [[ -n "$id_actor" && "$id_actor" == *"???"* ]]; then
			shadows+=("fi_slot_unresolved: identity.json actor_id is '$id_actor' (literal ??? placeholder, never resolved); identity has no fi_slot field — read identity.json + ask sovereign")
		elif [[ -n "$id_fi_slot" ]]; then
			shadows+=("fi_slot_ground_truth: identity.json is the canonical FI slot (actor=$id_actor, fi=$id_fi, fi_slot=$id_fi_slot); card's fi=${card_fi:-<absent>} / fi_slot=${card_fi_slot:-<absent>} — readers must NOT infer 'unassigned' from absent fields")
		fi
	fi

	# 3. Shadow-matrix entry presence
	local matrix_entry
	matrix_entry=$(matrix_state_for "$agent")
	if [[ -n "$matrix_entry" ]]; then
		local m_state m_fq m_count
		m_state=$(echo "$matrix_entry" | jq -r '.state // "UNKNOWN"')
		m_fq=$(echo "$matrix_entry" | jq -r '.fq // 0')
		m_count=$(echo "$matrix_entry" | jq -r '.execute_count // 0')
		shadows+=("sparse_history: shadow-matrix shows state=$m_state, fq=$m_fq, execute_count=$m_count — too little signal to diagnose a blind spot; truth-class for any $agent claim stays DERIVED not MEASURED until traffic grows")
	else
		shadows+=("sparse_or_absent_matrix_record: $agent is NOT in shadow-matrix per_actor_shadows — no execution/verification signal at all; all $agent claims are DERIVED from docs, not MEASURED from runtime")
	fi

	# 4. Stale binary refs — probe nested locations (cli_version could be top-level or under substrate.*)
	card_cli_version=$(jq -r '.. | .cli_version? // empty' "$card" 2>/dev/null | grep -E '^[0-9]+\.[0-9]+\.[0-9]+' | head -1)
	if [[ -n "$card_cli_version" ]]; then
		# Resolve binary name via alias map, fallback to agent dir name
		binary_name="${BINARY_ALIAS[$agent]:-$agent}"
		if command -v "$binary_name" >/dev/null 2>&1; then
			binary_version=$("$binary_name" --version 2>&1 | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
			if [[ -n "$binary_version" && "$binary_version" != "$card_cli_version" ]]; then
				shadows+=("stale_binary_refs: card says cli_version=$card_cli_version, live binary is $binary_version — drifted; treat card as archaeological for runtime facts")
			fi
		fi
	fi

	# 5. Card staleness — probe nested locations
	verified_against=$(jq -r '.. | .verified_against? // empty' "$card" 2>/dev/null | head -1)
	if [[ -n "$verified_against" ]]; then
		local staleness
		staleness=$(card_staleness_shadow "$agent" "$verified_against")
		[[ -n "$staleness" ]] && shadows+=("$staleness")
	fi

	# 6. Shadow undeclared (always true at this point — that's why we're here)
	if ! jq -e 'has("shadowAcknowledged")' "$card" >/dev/null 2>&1; then
		shadows+=("shadow_undeclared: this card had no shadowAcknowledged block before $AUDIT_DATE audit — read_state MUST treat $agent self-assessment as DERIVED")
	fi

	printf '%s\n' "${shadows[@]}"
}

# Main per-card operation
populate_card() {
	local agent="$1"
	local card="$EXTERNAL_DIR/$agent/agent-card.json"
	local audit_version="${2:-v1}" # v1 or v2 for re-runs

	if [[ ! -f "$card" ]]; then
		echo "SKIP: $agent — no agent-card.json"
		return 0
	fi

	if jq -e 'has("shadowAcknowledged")' "$card" >/dev/null 2>&1; then
		echo "SKIP: $agent — already has shadowAcknowledged"
		return 0
	fi

	echo "PROCESSING: $agent (${audit_version})"
	cp "$card" "$card.bak-$AUDIT_DATE-shadow-ack-${audit_version}"
	chmod 600 "$card.bak-$AUDIT_DATE-shadow-ack-${audit_version}"

	# Derive shadows
	local shadows_json
	shadows_json=$(derive_shadows "$agent" | jq -R . | jq -s .)

	# Build the meta block — covers_shadow_ids gives traceability from card → divergence registry
	# All script-populated cards cover DIV-FEDERATION-SHADOW-ACK-CLOSED; agent-specific IDs added when relevant
	local covers_json
	covers_json=$(jq -n --arg agent "$agent" '
    ["DIV-FEDERATION-SHADOW-ACK-CLOSED"] +
    (if $agent == "qwen-code" then ["DIV-QWEN-CODE-STUCK-MATRIX"] else [] end) +
    (if $agent == "opencode" then ["DIV-OPENCODE-FI-UNRESOLVED"] else [] end)
  ')

	local meta_json
	meta_json=$(jq -n \
		--arg pop_at "${AUDIT_DATE}T13:48:00Z" \
		--arg pop_by "$ACTOR_ID" \
		--arg method "Script-driven derivation from: identity.json (FI slot), $SHADOW_MATRIX (per_actor_shadows, exact-match), live binary version probe, agent-card.json (verified_against)" \
		--argjson covers "$covers_json" \
		'{populated_at: $pop_at, populated_by: $pop_by, method: $method, covers_shadow_ids: $covers}')

	# Apply: add shadowAcknowledged + shadow_population_meta after the last closing brace
	# Use jq to inject before the final }
	local tmp="$card.tmp"
	jq --argjson shadows "$shadows_json" --argjson meta "$meta_json" \
		'. + {shadowAcknowledged: $shadows, shadow_population_meta: $meta}' \
		"$card" >"$tmp"

	# Validate
	if ! jq -e . "$tmp" >/dev/null 2>&1; then
		echo "FAIL: $agent — generated JSON invalid; reverting"
		rm -f "$tmp"
		return 1
	fi

	mv "$tmp" "$card"
	chmod 600 "$card"
	local count
	count=$(jq '.shadowAcknowledged | length' "$card")
	echo "OK: $agent — $count shadow entries written, .bak at $card.bak-$AUDIT_DATE-shadow-ack-${audit_version}"
}

for agent in "$@"; do
	populate_card "$agent" || {
		echo "HALT at $agent"
		exit 1
	}
done
