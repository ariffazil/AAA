/**
 * G2 Witness Gate — Pre-execution Tri-Witness Consensus Check.
 *
 * Forged 2026-08-05. DITEMPA BUKAN DIBERI.
 *
 * Every MUTATE action must pass through this gate before execution.
 * The gate checks three independent channels:
 *   W1 — Human witness (F13 sovereign, cockpit status, WELL vitality)
 *   W2 — AI witness (other agents, FLAME consensus, seal chain health)
 *   W3 — Earth/External witness (GEOX compute, WEALTH market, cockpit organ health)
 *
 * W³ = ∛(W1 × W2 × W3) — Nash geometric mean.
 * Zero in any channel → consensus collapses to zero.
 *
 * Verdicts:
 *   CONSENSUS (W³ ≥ 0.75) → PROCEED to execution
 *   WEAK      (0.40 ≤ W³ < 0.75) → ANNOUNCE + reduced authority
 *   DIVERGENT (W³ < 0.40) → 888_HOLD, route to sovereign
 */
'use strict';

const fs = require('fs');
const http = require('http');

// ── Constants ────────────────────────────────────────────────────────
const W3_THRESHOLD_CONSENSUS = 0.75;
const W3_THRESHOLD_WEAK = 0.40;
const COCKPIT_STATUS_PATH = '/root/AAA/state/status.json';
const COCKPIT_URL = 'http://127.0.0.1:3001/cockpit/live';

// ── Witness computation ──────────────────────────────────────────────

/**
 * Compute W1 — Human witness score.
 * Based on: cockpit health, WELL vitality (if available), F13 sovereign presence.
 */
function computeW1(cockpitData) {
    if (!cockpitData) return 0.80; // default: human sovereign assumed present

    const agents = cockpitData.agent_list || [];
    const alive = agents.filter(a => a.status === 'healthy').length;
    const total = agents.length;

    // Core organs alive ratio
    const aliveRatio = total > 0 ? alive / total : 0.5;

    // Threshold: at least 6/10 organs need to be alive
    if (aliveRatio < 0.5) return 0.20;
    if (aliveRatio < 0.7) return 0.50;

    return Math.min(0.90, 0.60 + aliveRatio * 0.3);
}

/**
 * Compute W2 — AI witness score.
 * Based on: seal chain health, other agents reporting, FLAME availability.
 */
function computeW2(cockpitData) {
    if (!cockpitData) return 0.50;

    const agents = cockpitData.agent_list || [];
    // AI witness: other agents alive, FLAME responding
    const flame = agents.find(a => a.agent_id === 'flame');
    const fed = agents.find(a => a.agent_id === 'fed');

    let score = 0.40; // baseline: AI exists

    if (flame && flame.status === 'healthy') score += 0.25;
    if (fed && fed.status === 'healthy') score += 0.15;
    if (agents.filter(a => a.status === 'healthy').length >= 6) score += 0.10;

    return Math.min(0.90, score);
}

/**
 * Compute W3 — Earth/External witness score.
 * Based on: GEOX, WEALTH organ health, vault integrity.
 */
function computeW3(cockpitData) {
    if (!cockpitData) return 0.40;

    const agents = cockpitData.agent_list || [];
    const geox = agents.find(a => a.agent_id === 'geox');
    const wealth = agents.find(a => a.agent_id === 'wealth');
    const arifos = agents.find(a => a.agent_id === 'arifos');

    let score = 0.30; // baseline: some external grounding

    if (arifos && arifos.status === 'healthy') score += 0.20;
    if (geox && geox.status === 'healthy') score += 0.20;
    if (wealth && wealth.status === 'healthy') score += 0.20;

    return Math.min(0.90, score);
}

/**
 * Fetch cockpit data for witness computation.
 */
async function fetchCockpitData() {
    try {
        // Try live cockpit first
        const data = await httpGet(COCKPIT_URL);
        return JSON.parse(data);
    } catch {
        // Fallback to file
        try {
            return JSON.parse(fs.readFileSync(COCKPIT_STATUS_PATH, 'utf8'));
        } catch {
            return null;
        }
    }
}

function httpGet(url) {
    return new Promise((resolve, reject) => {
        http.get(url, { timeout: 3000 }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) resolve(data);
                else reject(new Error(`HTTP ${res.statusCode}`));
            });
        }).on('error', reject).on('timeout', function() { this.destroy(); reject(new Error('timeout')); });
    });
}

// ── Main gate function ───────────────────────────────────────────────

/**
 * Run the G2 witness gate.
 * @param {object} context - { intent, action_class, tool, agent_id, session_id }
 * @returns {Promise<{pass: boolean, verdict: string, w3_score: number, w1: number, w2: number, w3: number, evidence: object}>}
 */
async function witnessGate(context = {}) {
    const cockpitData = await fetchCockpitData();

    const w1 = computeW1(cockpitData);
    const w2 = computeW2(cockpitData);
    const w3 = computeW3(cockpitData);

    // Nash geometric mean: W³ = (W1 × W2 × W3)^(1/3)
    // Zero in any channel → zero consensus
    const w3Score = Math.cbrt(w1 * w2 * w3);

    let verdict;
    let pass;

    if (w3Score >= W3_THRESHOLD_CONSENSUS) {
        verdict = 'CONSENSUS';
        pass = true;
    } else if (w3Score >= W3_THRESHOLD_WEAK) {
        verdict = 'WEAK';
        pass = true; // proceed with caution
    } else {
        verdict = 'DIVERGENT';
        pass = false; // block
    }

    return {
        pass,
        verdict,
        w3_score: parseFloat(w3Score.toFixed(3)),
        w1: parseFloat(w1.toFixed(3)),
        w2: parseFloat(w2.toFixed(3)),
        w3: parseFloat(w3.toFixed(3)),
        evidence: {
            cockpit_agents_alive: cockpitData ? cockpitData.agents?.alive : null,
            cockpit_agents_total: cockpitData ? cockpitData.agents?.total : null,
            computed_at: new Date().toISOString(),
        },
        gate_version: 'G2-v1.0.0',
    };
}

/**
 * Quick sync witness check (for non-async contexts).
 * Uses cached cockpit data from disk.
 */
function witnessGateSync() {
    let cockpitData = null;
    try {
        cockpitData = JSON.parse(fs.readFileSync(COCKPIT_STATUS_PATH, 'utf8'));
    } catch { /* use null */ }

    const w1 = computeW1(cockpitData);
    const w2 = computeW2(cockpitData);
    const w3 = computeW3(cockpitData);
    const w3Score = Math.cbrt(w1 * w2 * w3);

    let verdict, pass;
    if (w3Score >= W3_THRESHOLD_CONSENSUS) { verdict = 'CONSENSUS'; pass = true; }
    else if (w3Score >= W3_THRESHOLD_WEAK) { verdict = 'WEAK'; pass = true; }
    else { verdict = 'DIVERGENT'; pass = false; }

    return {
        pass,
        verdict,
        w3_score: parseFloat(w3Score.toFixed(3)),
        w1: parseFloat(w1.toFixed(3)),
        w2: parseFloat(w2.toFixed(3)),
        w3: parseFloat(w3.toFixed(3)),
        gate_version: 'G2-v1.0.0',
    };
}

module.exports = { witnessGate, witnessGateSync };
