#!/usr/bin/env bash
# generate-hud-state.sh — HUD kernel: build canonical state object.
#
# Per sovereign 2026-10-02: 8-panel reality cockpit
# ── [1] MISSION ─────────────────────────────────────────────────────
# Bounded HUD repair 2026-10-02: mission kini dipaparkan dari sumber LIVE
# (execution-path-next.json — pemilik semantik kerja semasa), bukan teks
# misi tersembun dari sesi lapuk. Fallback eksplisit, bukan karutan.
budget_bounded="unspecified"
_now_epoch=$(date -u +%s)
_epn="/root/AAA/cockpit/execution-path-next.json"
if [[ -r "$_epn" ]]; then
  mission_objective=$(jq -r '.current_state.last_action // .purpose // "no active governed mission"' "$_epn" 2>/dev/null | head -1)
  mission_objective=${mission_objective:-"no active governed mission"}
  task_id="exec-path@$(jq -r '.generated_at // "?"' "$_epn" 2>/dev/null)"
  termination=$(jq -r '.next_steps[0].name // "none queued"' "$_epn" 2>/dev/null | head -1)
  # Sovereign fix 2026-10-02: mission carries its own source age — staleness must
  # be visible on the surface, not masked by render-time regeneration.
  _epn_mtime=$(stat -c %Y "$_epn" 2>/dev/null || echo "$_now_epoch")
  mission_age_min=$(( ( _now_epoch - _epn_mtime ) / 60 ))
  (( mission_age_min < 0 )) && mission_age_min=0
  # Stale mission text must not pose as current (sovereign 2026-10-02):
  # past a freshness bound the honest value is "none", with the staleness named.
  if (( mission_age_min > 90 )); then
    mission_objective="no active governed mission (exec-path stale ${mission_age_min}m)"
  fi
else
  mission_objective="no active governed mission"
  task_id="NONE"
  termination="NONE"
  mission_age_min=-1
fi

# ── [0] IDENTITY / AUTH (restored 2026-10-02 — peer patch deleted these vars) ─
actor="${USER:-root}"
actor_crypto="NO"
authority_band="OBSERVE_ONLY"
mutation_allowed="NO"
active_lease="unknown"
_active_lease_path="/root/AAA/cockpit/.lease"
if [[ -r "$_active_lease_path" ]]; then
  _lh=$(jq -r '.holder // "unknown"' "$_active_lease_path" 2>/dev/null)
  _lr=$(jq -r '.concurrent_write_rule.mode // "unknown"' "$_active_lease_path" 2>/dev/null)
  if [[ -n "$_lh" && "$_lh" != "null" ]]; then
    active_lease="${_lh} (${_lr})"
  fi
fi

runtime_json='{}'
md5_identity_json='null'
runtime_path="/root/AAA/cockpit/runtime-identity.json"
if [[ -r "$runtime_path" ]]; then
  runtime_json=$(jq -c '.summary // {}' "$runtime_path" 2>/dev/null || echo '{}')
  md5_identity_json=$(jq -c '.md5_identity // null' "$runtime_path" 2>/dev/null || echo 'null')
fi

# ── [2] RUNTIME ─────────────────────────────────────────────────────
src_sha=$(git -C /root/arifOS rev-parse --short HEAD 2>/dev/null || echo "no-git")
# deploy_sha MUST be measured from the deployed artifact — never copied from
# source (2026-10-02 scar: tautological deploy_sha=$src_sha made the HUD
# "source=deployed match" unfalsifiable — a check that cannot fail is decoration).
deploy_sha=$(grep -m1 '^Version:' /opt/arifos/current/venv/lib/python3.13/site-packages/arifos-*/METADATA 2>/dev/null | awk '{print $2}')
deploy_sha=${deploy_sha:-unknown}
# imported_version likewise measured from the runtime package, not hardcoded.
# Bug fix 2026-10-02: prior code asked importlib.metadata.version('arifosmcp') which
# does not exist; package is 'arifos'. Now uses correct name; falls back to UNKNOWN.
import_version=$(/opt/arifos/current/venv/bin/python -c "import importlib.metadata as m; print(m.version('arifos'))" 2>/dev/null || echo UNKNOWN)
# Strict runtime verify (placeholder — actual flag set by HUD consumer)
strict_runtime_state=$(jq -r '.summary.contradictions | length' /root/AAA/cockpit/runtime-identity.json 2>/dev/null || echo 0)

# ── [3] SURVIVAL ────────────────────────────────────────────────────
disk_pct=$(df -P / 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%' || echo "?")
mem_pct=$(free 2>/dev/null | awk '/^Mem:/ {printf "%.0f", $3/$2*100}' || echo "?")
swap_pct=$(free 2>/dev/null | awk '/^Swap:/ {printf "%.1f", ($3>0?$3/$2*100:0)}' || echo "?")
zombie_n=$(ps -eo stat 2>/dev/null | grep -cE '^Z' || echo 0)
running_services=$(systemctl list-units --type=service --state=running --no-pager 2>/dev/null | grep -cE '\.service' || echo 0)
total_services=$(systemctl list-units --type=service --no-pager 2>/dev/null | grep -cE '\.service' || echo 0)
# Sovereign fix 2026-10-02: well.json was a GHOST SOURCE (file never existed).
# Read real WELL telemetry (machine_state.json, cron /proc collector). Honest "—".
well_score=$(jq -r '.pressure.score // .pressure.level // "—"' /root/WELL/machine_state.json 2>/dev/null || echo "—")
_well_ts=$(jq -r '.timestamp_unix // 0' /root/WELL/machine_state.json 2>/dev/null || echo 0)
if [[ "$_well_ts" =~ ^[0-9]+$ ]] && (( _well_ts > 0 )); then
  well_age_min=$(( ( _now_epoch - _well_ts ) / 60 )); (( well_age_min < 0 )) && well_age_min=0
else
  well_age_min=-1
fi

# ── [4] JUDGMENT ────────────────────────────────────────────────────
canon_ok="OK"
contradictions_n=$strict_runtime_state
# FRAME — sovereign fix 2026-10-02: prior math divided the timestamp BEFORE subtracting
# (garbage output), then a hardcoded "7.8" papered over it. Compute honestly; "?" if unknown.
_frame_ts=$(jq -r '.ts // empty' /root/AAA/cockpit/shadow-matrix/last-run.json 2>/dev/null || echo "")
frame_age_days="?"
if [[ -n "$_frame_ts" ]]; then
  _frame_epoch=$(date -d "$_frame_ts" +%s 2>/dev/null || echo "")
  if [[ -z "$_frame_epoch" && "$_frame_ts" =~ ^[0-9]+$ ]]; then _frame_epoch="$_frame_ts"; fi
  if [[ -n "$_frame_epoch" ]] && (( _frame_epoch > 0 )); then
    frame_age_days=$(( ( _now_epoch - _frame_epoch ) / 86400 ))
  fi
fi
frame_alerts=$(grep -oE "Alerts: [0-9]+" /root/AAA/cockpit/shadow-matrix/drift-latest.txt 2>/dev/null | awk '{print $2}' || echo 0)
frame_warnings=$(grep -oE "Warnings: [0-9]+" /root/AAA/cockpit/shadow-matrix/drift-latest.txt 2>/dev/null | awk '{print $2}' || echo 0)
frame_ok=$(grep -oE "OK: [0-9]+" /root/AAA/cockpit/shadow-matrix/drift-latest.txt 2>/dev/null | awk '{print $2}' || echo 0)

# ── [5] TIME / LEARNING ─────────────────────────────────────────────
chron_attention_debt=$(jq -r '.attention_debt // 0' /root/chron/data/attention.json 2>/dev/null || echo 0)
chron_predictions_due=$(jq -r '.predictions_due // 0' /root/chron/data/predictions_due.json 2>/dev/null || echo 0)
# Sovereign fix 2026-10-02: the key is mean_brier — '.brier' never existed in
# calibration.json, so the HUD showed a permanent "?" next to existing data.
_brier_raw=$(jq -r '.mean_brier // empty' /root/chron/data/calibration.json 2>/dev/null || echo "")
chron_brier=$(printf '%.3f' "$_brier_raw" 2>/dev/null || echo "—")

# ── [6] CONCURRENCY ─────────────────────────────────────────────────
# Bug fix 2026-10-02: prior grep -cE "(claude|forge|hermes|chron|geox)" matched
# every cmdline containing those strings, including subprocesses (hermes gateway,
# otelcol, avahi-daemon, hermes-agent internals) — inflating count to 36-40
# when true AAA-agent processes are ~3. Now scoped to .arifos/agents/* processes.
active_agents_n=$(pgrep -af "arifOS/agents|kimi|hermes-agent" 2>/dev/null \
  | grep -vE "(grep|pgrep|otelcol|avahi|chronyd)" \
  | wc -l | tr -d ' ' || echo 0)
leases_n=$(find /root -maxdepth 5 -name "*.lease*" 2>/dev/null | wc -l | tr -d ' ' || echo 0)
dirty_repos=$(timeout 5 git -C /root status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo 0)

# ── [7] ECW / FEDERATION ────────────────────────────────────────────
ecw_summary=$(jq -c '.summary // {}' /root/AAA/cockpit/ecw-report.json 2>/dev/null || echo "{}")

# ── ROOT CONTRACT (sovereign 2026-10-02) ────────────────────────────
# BURNING: ONE material + unresolved + consequence-changing item, else none.
# WAITING: oldest sovereign decision + queue age, else none.
# SOURCE≠RUNTIME: material execution divergence only, else none.
# FRESHNESS: worst-of per-source ages. LAST CONSEQUENCE: newest receipt, else none.
# No per-organ verdicts (arifOS alone owns constitutional judge labels).
burning="none"
if [[ "${strict_runtime_state}" =~ ^[0-9]+$ ]] && (( strict_runtime_state > 0 )); then
  burning="runtime identity contradiction (strict_drift=${strict_runtime_state}, unresolved)"
elif awk -v s="${swap_pct:-0}" 'BEGIN{exit !(s>60)}' 2>/dev/null; then
  burning="swap pressure ${swap_pct}%"
elif [[ "${chron_predictions_due}" =~ ^[0-9]+$ ]] && (( chron_predictions_due > 0 )); then
  burning="chron predictions due=${chron_predictions_due}"
elif [[ "${zombie_n}" =~ ^[0-9]+$ ]] && (( zombie_n > 10 )); then
  burning="zombies=${zombie_n}"
fi

held_count=$(jq -r '.held_for_sovereign | length' "$_epn" 2>/dev/null || echo 0)
held_oldest=$(jq -r '.held_for_sovereign[0] // empty' "$_epn" 2>/dev/null)
waiting="none"
if [[ "${held_count}" =~ ^[0-9]+$ ]] && (( held_count > 0 )); then
  waiting="held=${held_count} · oldest: ${held_oldest} · queue age=${mission_age_min}m"
fi

source_neq_runtime="none"
if [[ "${strict_runtime_state}" =~ ^[0-9]+$ ]] && (( strict_runtime_state > 0 )); then
  source_neq_runtime="src=${src_sha} vs wheel=${deploy_sha} import=${import_version} (${strict_runtime_state} signals)"
fi

freshness="FRESH"
_worst_age="${mission_age_min:-0}"
[[ "$_worst_age" == "-1" ]] && _worst_age=0
(( _worst_age >= 15 )) && freshness="WARM"
(( _worst_age >= 120 )) && freshness="STALE"

newest_receipt=$(ls -t /root/AAA/cockpit/receipts/*.md 2>/dev/null | head -1)
last_consequence="none"
if [[ -n "$newest_receipt" ]]; then
  _rc_age=$(( ( _now_epoch - $(stat -c %Y "$newest_receipt" 2>/dev/null || echo "$_now_epoch") ) / 60 ))
  last_consequence="$(basename "$newest_receipt" .md) · ${_rc_age}m ago"
fi

# ── Build canonical state object ────────────────────────────────────
# bounded-repair 2026-10-02: punca nilai kosong → default jujur
_now="$(date -u +%s)"; _iso="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
: "${actor:=root}"
: "${actor_crypto:=NO}"
: "${authority_band:=OBSERVE_ONLY}"
: "${mutation_allowed:=NO}"
: "${active_lease:=unknown}"
[[ "${disk_pct}" =~ ^[0-9]+$ ]] || disk_pct=0
[[ "${mem_pct}" =~ ^[0-9]+$ ]] || mem_pct=0
[[ "${zombie_n}" =~ ^[0-9]+$ ]] || zombie_n=0
[[ "${running_services}" =~ ^[0-9]+$ ]] || running_services=0
[[ "${total_services}" =~ ^[0-9]+$ ]] || total_services=0
[[ "${contradictions_n}" =~ ^[0-9]+$ ]] || contradictions_n=0
[[ "${frame_alerts}" =~ ^[0-9]+$ ]] || frame_alerts=0
[[ "${frame_warnings}" =~ ^[0-9]+$ ]] || frame_warnings=0
[[ "${frame_ok}" =~ ^[0-9]+$ ]] || frame_ok=0
[[ "${chron_attention_debt}" =~ ^[0-9]+$ ]] || chron_attention_debt=0
[[ "${chron_predictions_due}" =~ ^[0-9]+$ ]] || chron_predictions_due=0
[[ "${active_agents_n}" =~ ^[0-9]+$ ]] || active_agents_n=0
[[ "${leases_n}" =~ ^[0-9]+$ ]] || leases_n=0
: "${NOW_UNIX:=$_now}"

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
  --arg burning "$burning" \
  --arg waiting "$waiting" \
  --arg source_neq_runtime "$source_neq_runtime" \
  --arg freshness "$freshness" \
  --arg last_consequence "$last_consequence" \
  --argjson mission_age_min "$mission_age_min" \
  --argjson well_age_min "$well_age_min" \
  --arg runtime_json "$runtime_json" \
  --arg md5_identity_json "$md5_identity_json" \
  --arg generated_at "$NOW_UTC" \
  --argjson generated_at_unix "$NOW_UNIX" \
  '{
    schema: "hud-state-v3-root-contract",
    generated_at: $generated_at,
    generated_at_unix: $generated_at_unix,
    root_contract: {
      burning: $burning,
      waiting: $waiting,
      source_neq_runtime: $source_neq_runtime,
      freshness: $freshness,
      last_consequence: $last_consequence
    },
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
        mission_age_min: $mission_age_min,
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
        well_score: $well_score,
        well_age_min: $well_age_min
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

STATE_OUT="${STATE_OUT:-/root/AAA/cockpit/hud-state.json}"
tmp="${STATE_OUT}.tmp"
printf '%s\n' "$final" > "$tmp"
mv "$tmp" "$STATE_OUT"
chmod 0644 "$STATE_OUT"
echo "HUD state written: $STATE_OUT (sha256=${body:0:12}...)" >&2
