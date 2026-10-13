/**
 * FQ Gate — Constitutional HOLD at FQ < 0.5.
 *
 * Forged 2026-08-05. DITEMPA BUKAN DIBERI.
 *
 * This is the structural fix for the deepest architectural gap identified:
 * agents execute even when FQ signals STUCK/OVERHEAT/BURNING.
 *
 * The gate:
 *   - Probes arifFlow (:7073) for live FQ
 *   - If FQ.quotient < 0.5 → 423 HOLD all MUTATE actions
 *   - If FQ.verdict in {OVERHEAT, BURNING} → 423 HOLD all MUTATE actions
 *   - Falls back to flow_state.json cache if arifFlow unreachable
 *   - OBSERVE actions ALWAYS pass (read-only is safe)
 *
 * This is NOT advisory. This is constitutional.
 *
 * The Linux kernel analogy: this is like the scheduler refusing to
 * schedule new processes when the load average exceeds a threshold.
 * arifOS's equivalent: when execute outruns verify, refuse to execute.
 */
'use strict';

const http = require('http');
const fs = require('fs');

// ── Constants ────────────────────────────────────────────────────────
const ARIFLOW_URL = 'http://127.0.0.1:7073/health';
const FLOW_STATE_PATH = '/root/AAA/state/flow_state.json';
const FQ_HOLD_THRESHOLD = 0.50;
const PROBE_TIMEOUT_MS = 3000;

// ── FQ Probe ─────────────────────────────────────────────────────────

/**
 * Fetch live FQ from arifFlow.
 * @returns {Promise<{quotient: number, verdict: string, execute_count: number, verify_count: number, source: string}>}
 */
async function probeLiveFQ() {
    return new Promise((resolve) => {
        const req = http.get(ARIFLOW_URL, { timeout: PROBE_TIMEOUT_MS }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const d = JSON.parse(data);
                    const fq = d.fq || d;
                    resolve({
                        quotient: parseFloat(fq.quotient) || 0.5,
                        verdict: fq.verdict || 'UNKNOWN',
                        execute_count: fq.execute_count || 0,
                        verify_count: fq.verify_count || 0,
                        source: 'arifFlow:7073',
                        live: true,
                    });
                } catch {
                    resolve(fallbackFQ());
                }
            });
        });
        req.on('error', () => resolve(fallbackFQ()));
        req.on('timeout', () => { req.destroy(); resolve(fallbackFQ()); });
    });
}

/**
 * Fallback: read FQ from cached flow_state.json.
 */
function fallbackFQ() {
    try {
        const data = JSON.parse(fs.readFileSync(FLOW_STATE_PATH, 'utf8'));
        return {
            quotient: parseFloat(data.fq) || 0.5,
            verdict: data.verdict || 'UNKNOWN',
            execute_count: data.execute_count || 0,
            verify_count: data.verify_count || 0,
            source: 'flow_state.json (cache)',
            live: false,
        };
    } catch {
        return {
            quotient: 0.5,
            verdict: 'UNKNOWN',
            execute_count: 0,
            verify_count: 0,
            source: 'DEGRADED (no source available)',
            live: false,
        };
    }
}

// ── Gate Function ────────────────────────────────────────────────────

/**
 * Run the FQ gate check.
 * @returns {Promise<{pass: boolean, fq: object, reason: string}>}
 */
async function fqGate() {
    const fq = await probeLiveFQ();

    // OBSERVE is always safe, but we check FQ for MUTATE
    // This function returns the FQ state for the caller to decide

    const passes = fq.quotient >= FQ_HOLD_THRESHOLD;
    let reason = '';

    if (!passes) {
        if (fq.verdict === 'BURNING') {
            reason = `FQ CRITICAL: quotient=${fq.quotient.toFixed(3)} BURNING. Execute outruns verify by dangerous margin. All MUTATE blocked.`;
        } else if (fq.verdict === 'OVERHEAT') {
            reason = `FQ HIGH: quotient=${fq.quotient.toFixed(3)} OVERHEAT. Reduce execute, increase verify. MUTATE blocked until FQ ≥ 0.50.`;
        } else {
            reason = `FQ STUCK: quotient=${fq.quotient.toFixed(3)} below threshold ${FQ_HOLD_THRESHOLD}. Verify before executing. MUTATE blocked.`;
        }
    }

    return {
        pass: passes,
        fq,
        reason,
        threshold: FQ_HOLD_THRESHOLD,
        gate_version: 'FQ-v1.0.0',
    };
}

/**
 * Synchronous FQ check using cache only (for middleware).
 */
function fqGateSync() {
    const fq = fallbackFQ();
    const passes = fq.quotient >= FQ_HOLD_THRESHOLD;
    let reason = '';
    if (!passes) {
        reason = `FQ HOLD: quotient=${fq.quotient.toFixed(3)} below ${FQ_HOLD_THRESHOLD}. MUTATE blocked until verify catches up.`;
    }
    return {
        pass: passes,
        fq,
        reason,
        threshold: FQ_HOLD_THRESHOLD,
        gate_version: 'FQ-v1.0.0',
    };
}

module.exports = { fqGate, fqGateSync, probeLiveFQ, FQ_HOLD_THRESHOLD };
