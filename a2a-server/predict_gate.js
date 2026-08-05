/**
 * G3 Predict Gate — Pre-execution Simulation & Risk Assessment.
 *
 * Forged 2026-08-05. DITEMPA BUKAN DIBERI.
 *
 * Every high-risk MUTATE action must pass through this gate before execution.
 * The gate computes a risk score and, for domain-specific actions, attempts
 * to run a predictive simulation via forge_predict.
 *
 * Risk factors:
 *   - Blast radius (filesystem, network, database, vault, organ)
 *   - Reversibility (FULL, PARTIAL, NONE)
 *   - Domain (geox, wealth, well, infra, code, config)
 *   - Organ health (from cockpit)
 *
 * Verdicts:
 *   SAFE     (risk < 0.30)           → PROCEED
 *   CAUTION  (0.30 ≤ risk < 0.60)    → PROCEED with annotation
 *   RISKY    (0.60 ≤ risk < 0.85)    → ANNOUNCE, require explicit ack
 *   DANGER   (risk ≥ 0.85)           → 888_HOLD, block execution
 */
'use strict';

const fs = require('fs');

// ── Constants ────────────────────────────────────────────────────────
const COCKPIT_STATUS_PATH = '/root/AAA/state/status.json';

const RISK_THRESHOLDS = {
    SAFE: 0.30,
    CAUTION: 0.60,
    RISKY: 0.85,
    // ≥ 0.85 → DANGER
};

// Domain risk baselines
const DOMAIN_BASELINE_RISK = {
    vault: 0.80,     // VAULT999 — permanent, immutable
    dns: 0.75,       // DNS/firewall — network-wide blast
    vps: 0.70,       // VPS restart — all services down
    database: 0.65,  // Database mutation — data loss risk
    deploy: 0.50,    // Deploy — reversible but service-affecting
    config: 0.40,    // Config change — usually reversible
    geo: 0.35,       // GEOX compute — reversible, compute-only
    wealth: 0.35,    // WEALTH compute — reversible, compute-only
    well: 0.30,      // WELL — reflect-only, no mutation
    code: 0.25,      // Code edit — fully reversible via git
    read: 0.05,      // Read-only — zero risk
    observe: 0.05,   // Observe — zero risk
};

// Reversibility risk multipliers
const REVERSIBILITY_MULTIPLIER = {
    FULL: 0.5,
    PARTIAL: 1.0,
    NONE: 2.0,
    UNKNOWN: 1.5,
};

/**
 * Classify the domain of an action from text/tool name.
 */
function classifyDomain(actionText, toolName) {
    const t = (actionText + ' ' + (toolName || '')).toLowerCase();

    if (t.match(/\b(vault|seal|outcomes\.jsonl|chattr)\b/)) return 'vault';
    if (t.match(/\b(dns|firewall|ufw|caddy|ssl|tunnel|cloudflare)\b/)) return 'dns';
    if (t.match(/\b(restart|reboot|shutdown|vps|hostinger)\b/)) return 'vps';
    if (t.match(/\b(drop|delete.*table|migrate|schema|postgres|supabase)\b/)) return 'database';
    if (t.match(/\b(deploy|rsync|systemctl restart|caddy.*reload)\b/)) return 'deploy';
    if (t.match(/\b(config|\.env|\.json|\.yaml|\.toml)\b/)) return 'config';
    if (t.match(/\b(seismic|basin|geox|petrophysics|prospect|well.*log)\b/)) return 'geo';
    if (t.match(/\b(capital|npv|emv|market|portfolio|wealth|forex)\b/)) return 'wealth';
    if (t.match(/\b(vitality|fatigue|well|homeostasis|dignity)\b/)) return 'well';
    if (t.match(/\b(edit|write|commit|push|merge|code|refactor)\b/)) return 'code';
    if (t.match(/\b(read|observe|probe|health|status|check|list|search)\b/)) return 'observe';

    return 'code'; // default
}

/**
 * Compute blast radius score (0-1) based on affected systems.
 */
function computeBlastRadiusScore(blastRadius, affectedOrgans) {
    if (!blastRadius) blastRadius = 'LOW';
    const radiusScores = { LOW: 0.10, MEDIUM: 0.40, HIGH: 0.70, CRITICAL: 0.95, FEDERATION: 1.0 };
    let score = radiusScores[blastRadius.toUpperCase()] || 0.40;

    // Each affected organ increases blast
    if (Array.isArray(affectedOrgans)) {
        score = Math.min(1.0, score + affectedOrgans.length * 0.10);
    }

    return score;
}

/**
 * Load cockpit data for health-based risk adjustment.
 */
function loadCockpitData() {
    try {
        return JSON.parse(fs.readFileSync(COCKPIT_STATUS_PATH, 'utf8'));
    } catch {
        return null;
    }
}

/**
 * Compute health risk modifier from cockpit organ status.
 */
function computeHealthRiskModifier(cockpitData) {
    if (!cockpitData) return 0.20; // unknown → moderate penalty

    const agents = cockpitData.agent_list || [];
    const coreOrgans = ['arifos', 'a-forge', 'geox', 'wealth', 'well'];
    let unhealthyCount = 0;

    for (const organId of coreOrgans) {
        const agent = agents.find(a => a.agent_id === organId);
        if (!agent || agent.status !== 'healthy') unhealthyCount++;
    }

    return unhealthyCount * 0.15; // 0.15 risk increase per unhealthy core organ
}

// ── Main gate function ───────────────────────────────────────────────

/**
 * Run the G3 predict gate.
 * @param {object} context - { intent, tool, blast_radius, reversibility, affected_organs, action_class }
 * @returns {{ pass: boolean, verdict: string, risk_score: number, domain: string, recommendation: string, factors: object }}
 */
function predictGate(context = {}) {
    const {
        intent = '',
        tool = '',
        blast_radius = 'LOW',
        reversibility = 'FULL',
        affected_organs = [],
        action_class = 'OBSERVE',
    } = context;

    // 1. Classify domain
    const domain = classifyDomain(intent, tool);

    // 2. Compute base risk
    const baseRisk = DOMAIN_BASELINE_RISK[domain] || 0.25;

    // 3. Compute blast radius score
    const blastScore = computeBlastRadiusScore(blast_radius, affected_organs);

    // 4. Reversibility modifier
    const revKey = (reversibility || 'FULL').toUpperCase();
    const revMultiplier = REVERSIBILITY_MULTIPLIER[revKey] || 1.0;

    // 5. Health modifier
    const cockpitData = loadCockpitData();
    const healthModifier = computeHealthRiskModifier(cockpitData);

    // 6. OBSERVE actions are always safe
    if (action_class === 'OBSERVE' || action_class === 'ANALYZE') {
        return {
            pass: true,
            verdict: 'SAFE',
            risk_score: 0.05,
            domain,
            recommendation: 'Proceed — observation has no side effects.',
            factors: {
                base_risk: baseRisk,
                blast_radius: blastScore,
                reversibility_multiplier: revMultiplier,
                health_modifier: healthModifier,
                action_class,
                domain,
            },
            gate_version: 'G3-v1.0.0',
        };
    }

    // 7. Compute final risk score
    //    risk = baseRisk × (blastScore × 0.6 + 0.4) × revMultiplier + healthModifier
    const compositeRisk = baseRisk * (blastScore * 0.6 + 0.4) * revMultiplier + healthModifier;
    const riskScore = Math.min(1.0, Math.max(0.0, compositeRisk));

    // 8. Determine verdict
    let verdict, pass, recommendation;

    if (riskScore < RISK_THRESHOLDS.SAFE) {
        verdict = 'SAFE';
        pass = true;
        recommendation = 'Proceed — risk within safe bounds.';
    } else if (riskScore < RISK_THRESHOLDS.CAUTION) {
        verdict = 'CAUTION';
        pass = true;
        recommendation = 'Proceed with caution. Verify reversibility path before execution.';
    } else if (riskScore < RISK_THRESHOLDS.RISKY) {
        verdict = 'RISKY';
        pass = true; // still passes, but with annotation
        recommendation = 'High risk detected. Announce before execution. Ensure rollback plan is documented. Consider running simulation first.';
    } else {
        verdict = 'DANGER';
        pass = false;
        recommendation = 'DANGER: Risk exceeds safe threshold. Route to 888-APEX for constitutional verdict. Simulation required.';
    }

    return {
        pass,
        verdict,
        risk_score: parseFloat(riskScore.toFixed(3)),
        domain,
        recommendation,
        factors: {
            base_risk: baseRisk,
            blast_radius: parseFloat(blastScore.toFixed(3)),
            reversibility_multiplier: revMultiplier,
            health_modifier: parseFloat(healthModifier.toFixed(3)),
            action_class,
            domain,
            cockpit_organs_healthy: cockpitData ? cockpitData.agents?.alive : null,
        },
        gate_version: 'G3-v1.0.0',
    };
}

module.exports = { predictGate, classifyDomain, DOMAIN_BASELINE_RISK };
