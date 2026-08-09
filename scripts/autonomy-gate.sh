#!/bin/bash
# T0: print CONTINUE|PARTIAL|HOLD from live probes + known contradiction classes
# Does NOT authorize T2/T3. Judgment aid only. GENESIS/061 · STATE §18
set -euo pipefail
STATE_OK=0
PROTO_OK=0
/root/AAA/scripts/state-probe.sh >/tmp/ag_state.txt 2>&1 && STATE_OK=1 || STATE_OK=0
/root/AAA/scripts/protocol-enforce.sh >/tmp/ag_proto.txt 2>&1 && PROTO_OK=1 || PROTO_OK=0
ARIFOS=$(curl -sf --max-time 3 http://127.0.0.1:8088/health 2>/dev/null || echo '{}')
DRIFT=$(python3 -c "import json,sys; d=json.loads(sys.argv[1] or '{}'); print(d.get('deployment_drift_status') or d.get('status') or 'unknown')" "$ARIFOS" 2>/dev/null || echo unknown)
STATUS=$(python3 -c "import json,sys; d=json.loads(sys.argv[1] or '{}'); print(d.get('status','unknown'))" "$ARIFOS" 2>/dev/null || echo unknown)
CONTRA=0
[[ "$DRIFT" == "drift_detected" ]] && CONTRA=1
[[ "$STATUS" == "degraded" ]] && CONTRA=1
echo "OBS state_ready=$STATE_OK protocol_enforced=$PROTO_OK arifos_status=$STATUS drift=$DRIFT contradictions_flag=$CONTRA"
if [[ $STATE_OK -eq 1 && $PROTO_OK -eq 1 && $CONTRA -eq 0 ]]; then
  echo "GATE=SEAL_EXECUTE  # still requires tier check for T2/T3"
elif [[ $STATE_OK -eq 1 && $PROTO_OK -eq 1 && $CONTRA -eq 1 ]]; then
  echo "GATE=PARTIAL_EXECUTE  # T0/T1 only; acknowledge contradictions; no full deploy SEAL"
else
  echo "GATE=HOLD"
fi
