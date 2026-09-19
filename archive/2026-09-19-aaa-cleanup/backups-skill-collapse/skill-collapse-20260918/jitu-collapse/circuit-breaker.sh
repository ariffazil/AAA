#!/usr/bin/env bash
# circuit-breaker.sh — Agent loop cap (max 3 retries per task)
# Usage:
#   source circuit-breaker.sh
#   cb_check <task_id>     # returns 0=ok, 1=OPEN (stop)
#   cb_fail <task_id>      # increment failure count
#   cb_reset <task_id>     # reset after success
#   cb_status              # show all open breakers
#
# F1 AMANAH: prevent metabolic runaway. 3 strikes → HOLD.

CB_DIR="/root/.local/share/arifos/circuit-breakers"
CB_MAX_RETRIES=3
mkdir -p "$CB_DIR"

cb_check() {
    local task_id="$1"
    local cb_file="$CB_DIR/$task_id.cb"

    if [[ ! -f "$cb_file" ]]; then
        echo '{"failures":0,"state":"CLOSED","last_failure":null}' > "$cb_file"
        echo "[CB] $task_id → CLOSED (fresh)"
        return 0
    fi

    local state=$(python3 -c "import json; print(json.load(open('$cb_file'))['state'])" 2>/dev/null)
    local failures=$(python3 -c "import json; print(json.load(open('$cb_file'))['failures'])" 2>/dev/null)

    if [[ "$state" == "OPEN" ]]; then
        echo "[CB] $task_id → CIRCUIT_BREAKER_OPEN ($failures failures)"
        echo "[CB] Agent MUST stop. Escalate to 888-APEX or human."
        return 1
    fi

    echo "[CB] $task_id → CLOSED ($failures/$CB_MAX_RETRIES failures)"
    return 0
}

cb_fail() {
    local task_id="$1"
    local cb_file="$CB_DIR/$task_id.cb"

    if [[ ! -f "$cb_file" ]]; then
        echo '{"failures":1,"state":"CLOSED","last_failure":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}' > "$cb_file"
        return 0
    fi

    local failures=$(python3 -c "import json; print(json.load(open('$cb_file'))['failures'])" 2>/dev/null)
    failures=$((failures + 1))

    if [[ $failures -ge $CB_MAX_RETRIES ]]; then
        python3 -c "
import json
data = {'failures': $failures, 'state': 'OPEN', 'last_failure': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'}
json.dump(data, open('$cb_file', 'w'), indent=2)
"
        echo "[CB] $task_id → CIRCUIT_BREAKER_OPEN ($failures failures)"
        echo "[CB] MAX RETRIES HIT. Agent MUST stop and escalate."
    else
        python3 -c "
import json
data = {'failures': $failures, 'state': 'CLOSED', 'last_failure': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'}
json.dump(data, open('$cb_file', 'w'), indent=2)
"
        echo "[CB] $task_id → failure $failures/$CB_MAX_RETRIES"
    fi
}

cb_reset() {
    local task_id="$1"
    local cb_file="$CB_DIR/$task_id.cb"
    echo '{"failures":0,"state":"CLOSED","last_failure":null}' > "$cb_file"
    echo "[CB] $task_id → RESET (closed)"
}

cb_status() {
    echo "=== Circuit Breaker Status ==="
    for f in "$CB_DIR"/*.cb; do
        [[ -f "$f" ]] || continue
        local task=$(basename "$f" .cb)
        local state=$(python3 -c "import json; print(json.load(open('$f'))['state'])" 2>/dev/null)
        local failures=$(python3 -c "import json; print(json.load(open('$f'))['failures'])" 2>/dev/null)
        echo "  $task: $state ($failures failures)"
    done
}
