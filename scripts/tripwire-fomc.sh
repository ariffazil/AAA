#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# FOMC MACRO TRIPWIRE — 2026-07-31 ~18:00 UTC
# ═══════════════════════════════════════════════════════════════════════════════
# Enforces FQ gates during volatility window. Tripwire fires at T-1h.
# Forged: 2026-07-28 by OpenCode (FI-001) under F13 directive
# Doctrine: DITEMPA BUKAN DIBERI
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

TRIPWIRE_DIR="/root/.local/share/arifos/sessions/fomc-tripwire-2026-07-31"
TRIPWIRE_JSON="$TRIPWIRE_DIR/tripwire.json"
STATE_FILE="$TRIPWIRE_DIR/state.json"
NOW_UTC=$(date -u +%s)
FOMC_UTC=$(date -u -d "2026-07-31 18:00:00" +%s 2>/dev/null || echo "0")
HOURS_LEFT=$(( (FOMC_UTC - NOW_UTC) / 3600 ))

mkdir -p "$TRIPWIRE_DIR"

# ─── Status check ─────────────────────────────────────────────────
status_check() {
    echo "════════════════════════════════════════"
    echo "FOMC MACRO TRIPWIRE STATUS"
    echo "════════════════════════════════════════"
    echo "Event:     FOMC + GDP + Core PCE"
    echo "Window:    2026-07-31 ~18:00 UTC"
    echo "Now:       $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "Time left: ${HOURS_LEFT}h"

    if [ "$HOURS_LEFT" -lt 0 ]; then
        echo "STATUS:    ⚠️  EVENT HAS PASSED — tripwire EXPIRED"
    elif [ "$HOURS_LEFT" -le 24 ]; then
        echo "STATUS:    🔴 ACTIVE WINDOW — FQ gates ENFORCED"
    elif [ "$HOURS_LEFT" -le 72 ]; then
        echo "STATUS:    🟡 APPROACHING — FQ elevated monitoring"
    else
        echo "STATUS:    🟢 NOMINAL — standard FQ gates"
    fi

    # Check FQ
    FQ=$(curl -sf http://localhost:7073/health 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('fq', 'unknown'))" 2>/dev/null || echo "unknown")
    echo "FQ:        $FQ"

    # Gold signal
    if command -v wealth &>/dev/null || curl -sf http://localhost:18082/health >/dev/null 2>&1; then
        echo "Gold RSI:  probe via wealth_capital_market(mode=signal, commodity=xauusd)"
    fi
    echo "════════════════════════════════════════"
}

# ─── Gate check ───────────────────────────────────────────────────
gate_check() {
    # During active window (T-24h to T+2h), enforce strict gates
    if [ "$HOURS_LEFT" -le 24 ] && [ "$HOURS_LEFT" -gt -2 ]; then
        echo "TRIPWIRE:ACTIVE"
        # Read current FQ — if < 0.5, HOLD all forge ops
        FQ=$(curl -sf http://localhost:7073/health 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('fq', 0.5))" 2>/dev/null || echo "0.5")
        FQ_FLOAT=$(python3 -c "print(float($FQ))" 2>/dev/null || echo "0.5")
        if python3 -c "exit(0 if float('$FQ_FLOAT') < 0.5 else 1)" 2>/dev/null; then
            echo "GATE:FQ_HOLD — FQ below 0.5 during FOMC window"
            return 1
        fi
        echo "GATE:PASS — FQ=$FQ during FOMC window"
    else
        echo "GATE:NOMINAL"
    fi
    return 0
}

# ─── Main ─────────────────────────────────────────────────────────
case "${1:-status}" in
    status) status_check ;;
    gate)   gate_check ;;
    *)
        echo "Usage: $0 {status|gate}"
        echo ""
        echo "  status  — Show tripwire status and time remaining"
        echo "  gate    — Run FQ gate check (exit 0=pass, 1=HOLD)"
        ;;
esac
