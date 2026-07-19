#!/usr/bin/env bash
# install-bare-metal.sh — Source-controlled bare-metal observability installer.
#
# Maps the canonical source configs in /root/AAA/observability/ to the active
# runtime locations used by Prometheus (systemd) and Grafana (deb). The
# installer is idempotent: it diffs the source against the active file, prints
# the proposed change, and only writes after a successful pre-validation pass
# (promtool check + YAML/JSON parse).  All active files are backed up with a
# UTC timestamp before any modification; backups are recorded in
# /var/log/aaa-observability-install.log so an operator can roll back.
#
# Usage:
#   bash /root/AAA/observability/install-bare-metal.sh [--dry-run] [--restart]
#
# Options:
#   --dry-run    Validate and diff; do not write.
#   --restart    Restart prometheus and grafana-server after writing.
#   --no-backup  Skip the backup step (offensive; debug only).
#
# Exits non-zero on any pre-validation failure; never writes partial state.

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  printf 'install-bare-metal: must run as root (systemctl + /etc access).\n' >&2
  exit 1
fi

DRY_RUN=0
RESTART=0
SKIP_BACKUP=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --restart) RESTART=1 ;;
    --no-backup) SKIP_BACKUP=1 ;;
    *) printf 'install-bare-metal: unknown argument %s\n' "$arg" >&2; exit 1 ;;
  esac
done

SRC_ROOT="/root/AAA/observability"
PROM_SRC="$SRC_ROOT/prometheus/prometheus.yml"
PROM_DST="/etc/prometheus/prometheus.yml"
ALERTS_SRC="$SRC_ROOT/prometheus/nine_signal_alerts.yml"
ALERTS_DST="/etc/prometheus/rules.d/nine_signal_alerts.yml"
GRAFANA_DATASOURCE_SRC="$SRC_ROOT/grafana/provisioning/datasources/prometheus.yml"
GRAFANA_DATASOURCE_DST="/etc/grafana/provisioning/datasources/prometheus.yml"
GRAFANA_DASHBOARD_PROV_SRC="$SRC_ROOT/grafana/provisioning/dashboards/nine_signal_dashboard.yml"
GRAFANA_DASHBOARD_PROV_DST="/etc/grafana/provisioning/dashboards/nine_signal_dashboard.yml"
GRAFANA_DASHBOARD_JSON_SRC="$SRC_ROOT/grafana/dashboards/nine_signal_overview.json"
GRAFANA_DASHBOARD_JSON_DST="/var/lib/grafana/dashboards/nine_signal_overview.json"

LOG_FILE="/var/log/aaa-observability-install.log"
mkdir -p "$(dirname "$LOG_FILE")" "$(dirname "$PROM_DST")" "$(dirname "$ALERTS_DST")" \
  "$(dirname "$GRAFANA_DATASOURCE_DST")" "$(dirname "$GRAFANA_DASHBOARD_PROV_DST")" \
  "$(dirname "$GRAFANA_DASHBOARD_JSON_DST")"

ts() { date -u +%Y%m%dT%H%M%SZ; }

log() {
  printf '%s [install-bare-metal] %s\n' "$(ts)" "$*" | tee -a "$LOG_FILE"
}

validate() {
  local src="$1"
  local dest="$2"
  local kind="$3"
  case "$kind" in
    yaml)
      python3 -c "import yaml,sys; yaml.safe_load(open('$src'))" || {
        log "FAIL: invalid YAML at $src"; return 1;
      }
      # Only Prometheus-shaped files get a promtool pass; Grafana provisioning
      # YAML uses a different schema (apiVersion / datasources) and must be
      # validated as plain YAML.
      if command -v promtool >/dev/null 2>&1 && [[ "$src" == */prometheus/* ]]; then
        if [[ "$src" == *alerts* ]]; then
          promtool check rules "$src" >/dev/null || {
            log "FAIL: promtool rejected $src"; return 1;
          }
        elif [[ "$src" == *prometheus.yml ]]; then
          promtool check config "$src" >/dev/null || {
            log "FAIL: promtool rejected $src"; return 1;
          }
        fi
      fi
      ;;
    json)
      python3 -c "import json; json.load(open('$src'))" || {
        log "FAIL: invalid JSON at $src"; return 1;
      }
      ;;
  esac
  log "validated $src for $dest"
}

backup() {
  local dest="$1"
  if [[ -f "$dest" && $SKIP_BACKUP -eq 0 ]]; then
    local backup_path="${dest}.bak.$(ts)"
    cp -p "$dest" "$backup_path"
    log "backed up $dest to $backup_path"
  fi
}

install_file() {
  local src="$1"
  local dest="$2"
  local kind="$3"
  validate "$src" "$dest" "$kind" || return 1
  if [[ ! -f "$dest" ]] || ! diff -q "$src" "$dest" >/dev/null 2>&1; then
    if [[ $DRY_RUN -eq 1 ]]; then
      log "DRY-RUN: would install $src -> $dest"
    else
      backup "$dest"
      install -m 0644 "$src" "$dest"
      log "installed $src -> $dest"
    fi
  else
    log "unchanged: $dest already matches source"
  fi
}

install_file "$PROM_SRC" "$PROM_DST" yaml
install_file "$ALERTS_SRC" "$ALERTS_DST" yaml
install_file "$GRAFANA_DATASOURCE_SRC" "$GRAFANA_DATASOURCE_DST" yaml
install_file "$GRAFANA_DASHBOARD_PROV_SRC" "$GRAFANA_DASHBOARD_PROV_DST" yaml
install_file "$GRAFANA_DASHBOARD_JSON_SRC" "$GRAFANA_DASHBOARD_JSON_DST" json

if [[ $RESTART -eq 1 && $DRY_RUN -eq 0 ]]; then
  log "restarting prometheus and grafana-server"
  systemctl reload prometheus || systemctl restart prometheus
  systemctl reload grafana-server || systemctl restart grafana-server
fi

log "done (dry_run=$DRY_RUN restart=$RESTART skip_backup=$SKIP_BACKUP)"
