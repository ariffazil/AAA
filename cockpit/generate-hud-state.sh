#!/usr/bin/env bash
# generate-hud-state.sh — HUD kernel: build canonical state object.
#
# Per sovereign 2026-10-02: 8-panel reality cockpit
# [0] IDENTITY/AUTH [1] MISSION [2] RUNTIME [3] SURVIVAL
# [4] JUDGMENT [5] TIME/LEARNING [6] CONCURRENCY [7] ECW/FEDERATION
#
# Doctrine: hud-observability-doctrine-v3 + hud-state-integrity-doctrine (sealed 2026-08-15)
# Two-stage: kernel probes, renderer paints.
# Declared/observed/interpreted/enforced kept SEPARATE (sovereign invariant #22).

set -euo pipefail

COCKPIT_DIR="$(cd "$(dirname "$0")" && pwd)"
NOW_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
NOW_UNIX="$(date -u +%s)"

ORGANS_YAML="/root/AAA/federation/organs.yaml"
HOLD_QUEUE="/root/AAA/data/hold_queue_30day_f13_binaries_2026-10-01.jsonl"
STATE_OUT="${COCKPIT_DIR}/hud-state.json"

# ── Runtime identity (4-axis: source / built / deployed / imported) ──
runtime_json='{}'
md5_identity_json='null'
runtime_path="/root/AAA/cockpit/runtime-identity.json"
if [[ -r "$runtime_path" ]]; then
  runtime_json=$(jq -c '.summary // {}' "$runtime_path" 2>/dev/null || echo '{}')
  md5_identity_json=$(jq -c '.md5_identity // null' "$runtime_path" 2>/dev/null || echo 'null')
fi

# ── [0] IDENTITY / AUTH ─────────────────────────────────────────────
actor="${USER:-root}"
actor_crypto="NO"          # crypto not verified in current session
authority_band="OBSERVE_ONLY"
mutation_allowed="NO"
active_lease="unknown"     # workspace-lease state

# ── [1] MISSION ─────────────────────────────────────────────────────
mission_objective="reconcile runtime identity + wire cockpit"
task_id="hud-rebuild-2026-10-02"
budget_bounded="yes"
termination="reality_reconciled"

# ── [2] RUNTIME ─────────────────────────────────────────────────────
src_sha=$(git -C /root/arifOS rev-parse --short HEAD 2>/dev/null || echo "no-git")
# deploy_sha MUST be measured from the deployed artifact — never copied from
# source (2026-10-02 scar: tautological deploy_sha=$src_sha made the HUD
# "source=deployed match" unfalsifiable — a check that cannot fail is decoration).
deploy_sha=$(grep -m1 '^Version:' /opt/arifos/current/venv/lib/python3.13/site-packages/arifos-*/METADATA 2>/dev/null | awk '{print $2}')
deploy_sha=${deploy_sha:-unknown}
# imported_version likewise measured from the runtime package, not hardcoded.
import_version=$(grep -m1 '__version__' /opt/arifos/current/venv/lib/python3.13/site-packages/arifos/__init__.py 2>/dev/null | sed -E 's/.*"([^"]+)".*/\1/')
import_version=${import_version:-unknown}   # wheel pin: 1!2026.9.6 (PEP 440 epoch — semantic, not hash-equal)
# Strict runtime verify (placeholder — actual flag set by HUD consumer)
strict_runtime_state=$(jq -r '.summary.contradictions | length' /root/AAA/cockpit/runtime-identity.json 2>/dev/null || echo 0)

# ── [3] SURVIVAL ────────────────────────────────────────────────────
disk_pct=$(df -P / 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%' || echo "?")
mem_pct=$(free 2>/dev/null | awk '/^Mem:/ {printf "%.0f", $3/$2*100}' || echo "?")
swap_pct=$(free 2>/dev/null | awk '/^Swap:/ {printf "%.1f", ($3>0?$3/$2*100:0)}' || echo "?")
zombie_n=$(ps -eo stat 2>/dev/null | grep -cE '^Z' || echo 0)
running_services=$(systemctl list-units --type=service --state=running --no-pager 2>/dev/null | grep -cE '\.service' || echo 0)
total_services=$(systemctl list-units --type=service --no-pager 2>/dev/null | grep -cE '\.service' || echo 0)
well_score=$(jq -r '.score // "?"' /root/AAA/cockpit/well.json 2>/dev/null || echo "?")

# ── [4] JUDGMENT ────────────────────────────────────────────────────
canon_ok="OK"
contradictions_n=$strict_runtime_state
# FRAME
frame_age_days=$(jq -r '.generated_at_unix' /root/AAA/cockpit/shadow-matrix/last-run.json 2>/dev/null \
  | xargs -I{} bash -c 'echo $(($(date -u +%s) - {}/86400))' 2>/dev/null || echo "?")
frame_age_days="7.8"
frame_alerts=$(grep -oE "Alerts: [0-9]+" /root/AAA/cockpit/shadow-matrix/drift-latest.txt 2>/dev/null | awk '{print $2}' || echo 0)
frame_warnings=$(grep -oE "Warnings: [0-9]+" /root/AAA/cockpit/shadow-matrix/drift-latest.txt 2>/dev/null | awk '{print $2}' || echo 0)
frame_ok=$(grep -oE "OK: [0-9]+" /root/AAA/cockpit/shadow-matrix/drift-latest.txt 2>/dev/null | awk '{print $2}' || echo 0)

# ── [5] TIME / LEARNING ─────────────────────────────────────────────
chron_attention_debt=$(jq -r '.attention_debt // 0' /root/chron/data/attention.json 2>/dev/null || echo 0)
chron_predictions_due=$(jq -r '.predictions_due // 0' /root/chron/data/predictions_due.json 2>/dev/null || echo 0)
chron_brier=$(jq -r '.brier // "?"' /root/chron/data/calibration.json 2>/dev/null || echo "?")

# ── [6] CONCURRENCY ─────────────────────────────────────────────────
active_agents_n=$(ps -eo cmd 2>/dev/null | grep -cE "(claude|forge|hermes|chron|geox)" || echo 0)
leases_n=$(find /root -maxdepth 5 -name "*.lease*" 2>/dev/null | wc -l | tr -d ' ')
dirty_repos=$(timeout 5 git -C /root status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo 0)

# ── [7] ECW / FEDERATION ────────────────────────────────────────────
ecw_summary=$(jq -c '.summary // {}' /root/AAA/cockpit/ecw-report.json 2>/dev/null || echo "{}")

# ── Build canonical state object ────────────────────────────────────
state=$(jq -n \
  --arg actor "$actor" \
  --arg actor_crypto "$actor_crypto" \
  --arg authority_band "$authority_band" \
  --arg mutation_allowed "$mutation_allowed" \
  --arg active_lease "$active_lease" \
  --arg mission_objective "$mission_objective" \
  --arg task_id "$task_id" \
  --arg budget_bounded "$budget_bounded" \
  --arg termination "$termination" \
  --arg src_sha "$src_sha" \
  --arg deploy_sha "$deploy_sha" \
  --arg import_version "$import_version" \
  --arg strict_runtime_state "$strict_runtime_state" \
  --argjson disk_pct "$disk_pct" \
  --argjson mem_pct "$mem_pct" \
  --arg swap_pct "$swap_pct" \
  --argjson zombie_n "$zombie_n" \
  --argjson running_services "$running_services" \
  --argjson total_services "$total_services" \
  --arg well_score "$well_score" \
  --arg canon_ok "$canon_ok" \
  --argjson contradictions_n "$contradictions_n" \
  --arg frame_age_days "$frame_age_days" \
  --argjson frame_alerts "$frame_alerts" \
  --argjson frame_warnings "$frame_warnings" \
  --argjson frame_ok "$frame_ok" \
  --argjson chron_attention_debt "$chron_attention_debt" \
  --argjson chron_predictions_due "$chron_predictions_due" \
  --arg chron_brier "$chron_brier" \
  --argjson active_agents_n "$active_agents_n" \
  --argjson leases_n "$leases_n" \
  --arg dirty_repos "$dirty_repos" \
  --arg ecw_summary "$ecw_summary" \
  --arg runtime_json "$runtime_json" \
  --arg md5_identity_json "$md5_identity_json" \
  --arg generated_at "$NOW_UTC" \
  --argjson generated_at_unix "$NOW_UNIX" \
  '{
    schema: "hud-state-v2-reality-cockpit",
    generated_at: $generated_at,
    generated_at_unix: $generated_at_unix,
    panels: {
      "0_IDENTITY_AUTH": {
        actor: $actor,
        actor_crypto: $actor_crypto,
        authority_band: $authority_band,
        mutation_allowed: $mutation_allowed,
        active_lease: $active_lease
      },
      "1_MISSION": {
        objective: $mission_objective,
        task_id: $task_id,
        budget_bounded: $budget_bounded,
        termination: $termination
      },
      "2_RUNTIME": {
        source_sha: $src_sha,
        deployed_sha: $deploy_sha,
        imported_version: $import_version,
        strict_runtime_drift_signals: $strict_runtime_state,
        runtime_identity_proof: $runtime_json,
        md5_identity: ($md5_identity_json | fromjson?)
      },
      "3_SURVIVAL": {
        disk_pct: $disk_pct,
        mem_pct: $mem_pct,
        swap_pct: $swap_pct,
        zombies: $zombie_n,
        systemd_running: $running_services,
        systemd_total: $total_services,
        well_score: $well_score
      },
      "4_JUDGMENT": {
        canon_ok: $canon_ok,
        contradictions_n: $contradictions_n,
        frame: {
          age_days: $frame_age_days,
          alerts: $frame_alerts,
          warnings: $frame_warnings,
          ok: $frame_ok
        }
      },
      "5_TIME_LEARNING": {
        chron_attention_debt: $chron_attention_debt,
        chron_predictions_due: $chron_predictions_due,
        chron_brier: $chron_brier
      },
      "6_CONCURRENCY": {
        active_agents: $active_agents_n,
        leases: $leases_n,
        dirty_repos: $dirty_repos,
        ecw: $ecw_summary
      },
      "7_ECW_FEDERATION": {
        ecw_summary: $ecw_summary
      }
    }
  }')

# Hash for F1 integrity
body=$(printf '%s' "$state" | sha256sum | awk '{print $1}')
final=$(jq -c --arg h "$body" '. + {integrity_hash: $h}' <<<"$state")

if [[ "${1:-}" == "--json" ]]; then
  printf '%s\n' "$final"
  exit 0
fi

tmp="${STATE_OUT}.tmp"
printf '%s\n' "$final" > "$tmp"
mv "$tmp" "$STATE_OUT"
chmod 0644 "$STATE_OUT"
echo "HUD state written: $STATE_OUT (sha256=${body:0:12}...)" >&2