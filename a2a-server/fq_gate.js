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

// ── Safe parsing + pure decision (fail-closed) ───────────────────────
// FQ-v1.1.0: missing/unparseable quotient is UNMEASURABLE, never a pass.
// A legitimate quotient of 0 must stay 0 (HOLD) — parseFloat()||0.5 masked it.

function readQuotient(v) {
    const n = typeof v === 'number' ? v : parseFloat(v);
    return Number.isFinite(n) ? n : null;
}

function gateDecide(fq) {
    const q = readQuotient(fq.quotient);
    const unmeasurable = q === null;
    const verdictHot = fq.verdict === 'BURNING' || fq.verdict === 'OVERHEAT';
    // Docstring contract (header, line 12): BURNING/OVERHEAT HOLD regardless of quotient.
    const passes = !unmeasurable && !verdictHot && q >= FQ_HOLD_THRESHOLD;
    let reason = '';
    if (!passes) {
        if (unmeasurable) {
            reason = 'FQ UNMEASURABLE: no readable quotient (fail-closed). MUTATE blocked until FQ observable.';
        } else if (fq.verdict === 'BURNING') {
            reason = `FQ CRITICAL: verdict=BURNING. Execute outruns verify by dangerous margin. All MUTATE blocked.`;
        } else if (fq.verdict === 'OVERHEAT') {
            reason = `FQ HIGH: verdict=OVERHEAT. Reduce execute, increase verify. MUTATE blocked.`;
        } else {
            reason = `FQ STUCK: quotient=${q.toFixed(3)} below threshold ${FQ_HOLD_THRESHOLD}. Verify before executing. MUTATE blocked.`;
        }
    }
    return { pass: passes, reason };
}

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
                        quotient: readQuotient(fq.quotient ?? fq.legacy_quotient),
                        verdict: fq.verdict || fq.legacy_verdict || 'UNKNOWN',
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
            quotient: readQuotient(data.fq ?? data.quotient ?? data.legacy_quotient),
            verdict: data.verdict || data.legacy_verdict || 'UNKNOWN',
            execute_count: data.execute_count || 0,
            verify_count: data.verify_count || 0,
            source: 'flow_state.json (cache)',
            live: false,
        };
    } catch {
        return {
            quotient: null,  // fail-closed: no source = UNMEASURABLE, never a pass
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

    const decision = gateDecide(fq);

    return {
        pass: decision.pass,
        fq,
        reason: decision.reason,
        threshold: FQ_HOLD_THRESHOLD,
        gate_version: 'FQ-v1.1.0-failclosed',
    };
}

/**
 * Synchronous FQ check using cache only (for middleware).
 */
function fqGateSync() {
    const fq = fallbackFQ();
    const decision = gateDecide(fq);
    return {
        pass: decision.pass,
        fq,
        reason: decision.reason,
        threshold: FQ_HOLD_THRESHOLD,
        gate_version: 'FQ-v1.1.0-failclosed',
    };
}

module.exports = { fqGate, fqGateSync, probeLiveFQ, gateDecide, readQuotient, FQ_HOLD_THRESHOLD };
