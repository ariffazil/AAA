#!/usr/bin/env bash
# display-hud.sh — HUD renderer (dumb). Sovereign 8-panel reality cockpit.
#
# Per sovereign 2026-10-02:
# - NORMAL → one line, WARN → expand one level, HOLD → evidence + next action
# - No menus. No 200 tools. Just enough.

set -euo pipefail

COCKPIT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_FILE="${COCKPIT_DIR}/hud-state.json"
GENERATOR="${COCKPIT_DIR}/generate-hud-state.sh"
EXEC_PATH="${COCKPIT_DIR}/execution-path-next.json"

REGEN=1
RAW=0
for arg in "$@"; do
  case "$arg" in
    --no-regen) REGEN=0 ;;
    --raw) RAW=1 ;;
    *) echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if [[ $REGEN -eq 1 ]]; then
  env -i HOME=/root PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    bash "$GENERATOR" >/dev/null
fi

[[ -r "$STATE_FILE" ]] || { echo "no state file" >&2; exit 2; }

# F1 integrity
state_no_hash=$(jq 'del(.integrity_hash)' "$STATE_FILE" 2>/dev/null || echo "{}")
expected=$(jq -r '.integrity_hash // ""' "$STATE_FILE" 2>/dev/null)
actual=$(printf '%s' "$state_no_hash" | sha256sum | awk '{print $1}')
if [[ -n "$expected" && "$expected" != "$actual" ]]; then
  echo "TAMPERED state file" >&2; exit 3
fi

# Auto-detect TTY
if [[ ! -t 1 ]]; then RESET=""; BOLD=""; DIM=""; RED=""; YEL=""; GRN=""; CYN=""
else
  RESET="\033[0m"; BOLD="\033[1m"; DIM="\033[2m"; RED="\033[1;31m"
  YEL="\033[1;33m"; GRN="\033[1;32m"; CYN="\033[1;36m"
fi

# Pull panel values
s() { jq -r "($1) // \"?\"" "$STATE_FILE" 2>/dev/null | head -1; }

# [0] IDENTITY_AUTH
actor=$(s '.panels["0_IDENTITY_AUTH"].actor')
actor_crypto=$(s '.panels["0_IDENTITY_AUTH"].actor_crypto')
authority_band=$(s '.panels["0_IDENTITY_AUTH"].authority_band')
mutation_allowed=$(s '.panels["0_IDENTITY_AUTH"].mutation_allowed')
active_lease=$(s '.panels["0_IDENTITY_AUTH"].active_lease')

# [1] MISSION
objective=$(s '.panels["1_MISSION"].objective')
objective="${objective:0:70}"
task_id=$(s '.panels["1_MISSION"].task_id')
mission_age_min=$(s '.panels["1_MISSION"].mission_age_min')
termination=$(s '.panels["1_MISSION"].termination')
# Stale queue: the honest value already says "none" — don't double-label or
# parade stale termination items as if they were current.
if [[ "$objective" == "no active governed mission"* ]]; then
  mission_line="${objective}"
  term_disp=""
else
  mission_line="${objective} (${task_id} · src age=${mission_age_min}m)"
  term_disp="→ ${termination}"
fi

# [2] RUNTIME
src_sha=$(s '.panels["2_RUNTIME"].source_sha')
deployed_sha=$(s '.panels["2_RUNTIME"].deployed_sha')
imported_version=$(s '.panels["2_RUNTIME"].imported_version')
strict_drift=$(s '.panels["2_RUNTIME"].strict_runtime_drift_signals')

# [3] SURVIVAL
disk_pct=$(s '.panels["3_SURVIVAL"].disk_pct')
mem_pct=$(s '.panels["3_SURVIVAL"].mem_pct')
swap_pct=$(s '.panels["3_SURVIVAL"].swap_pct')
zombies=$(s '.panels["3_SURVIVAL"].zombies')
sys_run=$(s '.panels["3_SURVIVAL"].systemd_running')
sys_tot=$(s '.panels["3_SURVIVAL"].systemd_total')
well_score=$(s '.panels["3_SURVIVAL"].well_score')

# [4] JUDGMENT
canon_ok=$(s '.panels["4_JUDGMENT"].canon_ok')
contradictions=$(s '.panels["4_JUDGMENT"].contradictions_n')
frame_alerts=$(s '.panels["4_JUDGMENT"].frame.alerts')
frame_warn=$(s '.panels["4_JUDGMENT"].frame.warnings')
frame_ok=$(s '.panels["4_JUDGMENT"].frame.ok')
frame_age=$(s '.panels["4_JUDGMENT"].frame.age_days')

# [5] TIME_LEARNING
attention_debt=$(s '.panels["5_TIME_LEARNING"].chron_attention_debt')
predictions_due=$(s '.panels["5_TIME_LEARNING"].chron_predictions_due')
brier=$(s '.panels["5_TIME_LEARNING"].chron_brier')

# [6] CONCURRENCY
active_agents=$(s '.panels["6_CONCURRENCY"].active_agents')
leases=$(s '.panels["6_CONCURRENCY"].leases')
dirty=$(s '.panels["6_CONCURRENCY"].dirty_repos')

# [7] ECW_FEDERATION (summary is string-serialized in state)
ecw_str=$(s '.panels["7_ECW_FEDERATION"].ecw_summary')
ecw_total=$(jq -r '.total_probed // "?"' <<<"$ecw_str" 2>/dev/null || echo "?")
ecw_transport=$(jq -r '.transport_up // "?"' <<<"$ecw_str" 2>/dev/null || echo "?")
ecw_sem=$(jq -r '.semantic_clean // "?"' <<<"$ecw_str" 2>/dev/null || echo "?")

# bounded-repair: koersi numerik (tiada placeholder dalam -gt)
[[ "$strict_drift" =~ ^[0-9]+$ ]] || strict_drift=0
[[ "$contradictions" =~ ^[0-9]+$ ]] || contradictions=0

# Conditional formatting
mut_color=$GRN
[[ "$mutation_allowed" == "NO" ]] && mut_color=$YEL
strict_color=$GRN
drift_note=""
[[ "$strict_drift" -gt 0 ]] && drift_note=" (CONTRADICTION)"
[[ "$strict_drift" -gt 0 ]] && strict_color=$RED
# Bug fix 2026-10-02: canon and contradictions are SEPARATE dimensions.
# canon=OK means canonical files intact (proven).
# contradictions=N means N observed divergences (also legitimate, may coexist).
# Per spec §6.7: contradiction is evidence, not pathology.
# Only elevate to RED when contradiction count breaches a threshold.
canon_color=$GRN
contradictions_color=$GRN
[[ "$contradictions" -gt 0 ]] && contradictions_color=$YEL
[[ "$contradictions" -gt 3 ]] && contradictions_color=$RED

# Banner
if [[ $RAW -eq 0 ]]; then
  printf '%s╔══════════════════════════════════════════════════════════════════════╗%s\n' "$BOLD" "$RESET"
  printf '%s║ ARIF / AAA REALITY COCKPIT%s             %s%s%s\n' "$BOLD" "$RESET" "$DIM" "$(date -u +'%Y-%m-%d %H:%MZ')" "$RESET"
  printf '%s╠══════════════════════════════════════════════════════════════════════╣%s\n' "$BOLD" "$RESET"
fi

cat <<EOF
${BOLD}[0] IDENTITY${RESET}  ${actor} claimed | crypto:${actor_crypto} | AUTH:${authority_band} | MUTATE:${mut_color}${mutation_allowed}${RESET} | lease=${active_lease}
${BOLD}[1] MISSION${RESET}     ${mission_line}${term_disp:+ ${term_disp}}
${BOLD}[2] RUNTIME${RESET}     src=${src_sha} wheel=${deployed_sha} import=${imported_version}
                       strict_drift_signals=${strict_color}${strict_drift}${RESET}${drift_note}
${BOLD}  ↳ MD5${RESET}         arifos=$(jq -r 'if .panels["2_RUNTIME"].md5_identity.arifos.md5_match == true then "MATCH" elif .panels["2_RUNTIME"].md5_identity.arifos.md5_match == false then "DRIFT" else "UNKNOWN" end' "$STATE_FILE" 2>/dev/null) aforge=$(jq -r 'if .panels["2_RUNTIME"].md5_identity.aforge.md5_match == true then "MATCH" elif .panels["2_RUNTIME"].md5_identity.aforge.md5_match == false then "DRIFT" else "UNKNOWN" end' "$STATE_FILE" 2>/dev/null) frame=$(jq -r 'if .panels["2_RUNTIME"].md5_identity.frame.md5_match == true then "MATCH" elif .panels["2_RUNTIME"].md5_identity.frame.md5_match == false then "DRIFT" else "UNKNOWN" end' "$STATE_FILE" 2>/dev/null)
${BOLD}[3] SURVIVAL${RESET}    DISK=${disk_pct}% MEM=${mem_pct}% SWAP=${swap_pct}% ZOMB=${zombies}  svc=${sys_run}/${sys_tot}  WELL=${well_score}
${BOLD}[4] JUDGMENT${RESET}    canon_integrity=${canon_color}${canon_ok}${RESET} | contradictions_observed=${contradictions_color}${contradictions}${RESET} | FRAME 🔴${frame_alerts} 🟡${frame_warn} 🟢${frame_ok} age=${frame_age}d
${BOLD}[5] TIME${RESET}        chron attention_debt=${attention_debt} | due=${predictions_due} | brier=${brier}
${BOLD}[6] CONCURRENCY${RESET} agents=${active_agents} leases=${leases} dirty=${dirty}
${BOLD}[7] ECW${RESET}         probed=${ecw_total} transport=${ecw_transport} semantic_clean=${ecw_sem} SURFACE_DRIFT=$(jq -r '.drift_classes_hit.SURFACE_DRIFT // 0' <<<"$ecw_str" 2>/dev/null || echo "?")
EOF

# ── ROOT CONTRACT (sovereign 2026-10-02): decision pressures only.
# Sensors, organ states, and diagnosis live behind drill-down, not here.
# arifOS alone owns constitutional judge labels — organs never render as voters.
burning=$(s '.root_contract.burning')
waiting=$(s '.root_contract.waiting')
src_neq_rt=$(s '.root_contract.source_neq_runtime')
last_cons=$(s '.root_contract.last_consequence')
burn_color=$RESET; [[ "$burning" != "none" ]] && burn_color=$RED
echo
printf '%sBURNING%s        %s%s%s\n' "$BOLD" "$RESET" "$burn_color" "$burning" "$RESET"
printf '%sWAITING%s         %s\n' "$BOLD" "$RESET" "$waiting"
printf '%sSOURCE≠RUNTIME%s  %s\n' "$BOLD" "$RESET" "$src_neq_rt"
printf '%sLAST CONSEQ.%s    %s\n' "$BOLD" "$RESET" "$last_cons"

# NEXT — read first 3 from execution-path-next.json
if [[ -r "$EXEC_PATH" ]]; then
  epn_age_min=$(( ( $(date -u +%s) - $(stat -c %Y "$EXEC_PATH" 2>/dev/null || date -u +%s) ) / 60 ))
  echo
  printf '%sNEXT%s         ' "$BOLD" "$RESET"
  jq -r --argjson age "$epn_age_min" '"\(.generated_at) | queue age=\($age)m | held=\(.held_for_sovereign | length)\n"' "$EXEC_PATH" 2>/dev/null | head -1
  jq -r '.next_steps[:3] | .[] | "  → \(.name)\n"' "$EXEC_PATH" 2>/dev/null
fi

# FRESHNESS — per-source worst (per sovereign 2026-10-02): render freshness must
# not mask source staleness. state=render age; exec-path=queue source age.
state_age=$(( $(date -u +%s) - $(jq -r '.generated_at_unix' "$STATE_FILE" 2>/dev/null || echo 0) ))
fresh_status=$(s '.root_contract.freshness')
[[ "$fresh_status" == "?" || -z "$fresh_status" ]] && fresh_status="UNKNOWN"
epn_disp="?"
[[ -n "${epn_age_min:-}" ]] && epn_disp="${epn_age_min}m"
fresh_color=$GRN
[[ "$fresh_status" == "WARM" ]] && fresh_color=$YEL
[[ "$fresh_status" == "STALE" || "$fresh_status" == "TAMPER" ]] && fresh_color=$RED

echo
printf '%sFRESHNESS%s       %s%s%s  (state=%ss · exec-path=%s)\n' "$BOLD" "$RESET" "$fresh_color" "$fresh_status" "$RESET" "$state_age" "$epn_disp"

# F1 receipt trail
echo
printf '%sreceipt: [receipt: /root/AAA/cockpit/hud-state.json]%s\n' "$DIM" "$RESET"

exit 0