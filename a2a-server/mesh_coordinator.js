/**
 * AAA Mesh Coordinator — Loop Detector & Gradient Computer
 * ═══════════════════════════════════════════════════════════
 *
 * Subscribes to governance events and organ heartbeats on NATS.
 * Detects compound patterns, computes gradient signals, and
 * publishes feedback into the mesh for AAA cockpit display.
 *
 * Forged: 2026-06-14 — P3 dynamic flow wiring
 * DITEMPA BUKAN DIBERI
 */

const NATS_URL = 'nats://127.0.0.1:4222';

// ── Configuration ──────────────────────────────────────────────────────────

const CONFIG = {
  /** How often to compute and publish gradient signals (seconds) */
  GRADIENT_INTERVAL_S: 30,
  /** Maximum age of organ heartbeat before marking stale (seconds) */
  ORGAN_STALE_THRESHOLD_S: 120,
  /** Maximum age of organ heartbeat before marking dead (seconds) */
  ORGAN_DEAD_THRESHOLD_S: 300,
  /** How many recent governance events to keep in memory */
  GOVERNANCE_WINDOW: 200,
  /** Repeated HOLD threshold — if same tool gets HOLD this many times in window, escalate */
  HOLD_REPEAT_THRESHOLD: 5,
  /** Floor breach burst threshold — if this many breaches in window, freeze agent */
  BREACH_BURST_THRESHOLD: 3,
};

// ── In-Memory State ────────────────────────────────────────────────────────

/** @type {Map<string, {status: string, lastSeen: number, toolCount: number}>} */
const organState = new Map();

/** @type {Array<{timestamp: number, subject: string, verdict: string, tool: string, session: string}>} */
const governanceEvents = [];

/** @type {Map<string, number>} — tool → HOLD count in current window */
const holdCounts = new Map();

/** @type {Map<string, number>} — floor → breach count in current window */
const breachCounts = new Map();

/** @type {Array<{timestamp: number, type: string, severity: string, message: string}>} */
const alerts = [];

/** @type {number} */
let gradientScore = 50; // 0-100. 50 = nominal. Higher = more urgent/unstable.

// ── NATS Helpers ───────────────────────────────────────────────────────────

/**
 * Connect to NATS and start all subscriptions.
 * @param {object} [existingNc] — optional existing NATS connection to reuse
 * @returns {Promise<object>} nats connection
 */
async function startMeshCoordinator(existingNc) {
  let nc;
  if (existingNc) {
    nc = existingNc;
    console.log('[mesh-coord] Reusing existing NATS connection');
  } else {
    const { connect } = require('nats');
    nc = await connect({ servers: NATS_URL });
    console.log('[mesh-coord] NATS connected');
  }

  const sc = require('nats').StringCodec();

  // ── Subscribe: Governance events ──────────────────────────────────────
  const govSub = nc.subscribe('arifos.gate.>');
  console.log('[mesh-coord] Subscribed: arifos.gate.>');

  (async () => {
    for await (const msg of govSub) {
      try {
        const data = JSON.parse(sc.decode(msg.data));
        const timestamp = Date.now();
        governanceEvents.push({
          timestamp,
          subject: msg.subject,
          verdict: data.verdict,
          tool: data.tool_name,
          session: data.session_id,
        });
        // Trim window
        while (governanceEvents.length > CONFIG.GOVERNANCE_WINDOW) {
          governanceEvents.shift();
        }

        // Track HOLD counts
        if (data.verdict === 'HOLD') {
          const tool = data.tool_name || 'unknown';
          holdCounts.set(tool, (holdCounts.get(tool) || 0) + 1);

          if (holdCounts.get(tool) >= CONFIG.HOLD_REPEAT_THRESHOLD) {
            const alert = {
              type: 'REPEATED_HOLD',
              severity: 'warn',
              message: `Tool ${tool} has ${holdCounts.get(tool)} HOLDs in recent window`,
              timestamp,
            };
            alerts.push(alert);
            if (alerts.length > 100) alerts.shift();
            await publishAlert(nc, alert);
          }
        }

        // Track floor breaches
        if (data.violated_laws && data.violated_laws.length > 0) {
          for (const law of data.violated_laws) {
            breachCounts.set(law, (breachCounts.get(law) || 0) + 1);
          }
          const totalBreaches = Array.from(breachCounts.values()).reduce((a, b) => a + b, 0);
          if (totalBreaches >= CONFIG.BREACH_BURST_THRESHOLD) {
            const alert = {
              type: 'BREACH_BURST',
              severity: 'critical',
              message: `${totalBreaches} floor breaches in window. Violated: ${[...breachCounts.keys()].join(', ')}`,
              timestamp,
            };
            alerts.push(alert);
            if (alerts.length > 100) alerts.shift();
            await publishAlert(nc, alert);
          }
        }
      } catch (_) {
        // Malformed message — skip
      }
    }
  })();

  // ── Subscribe: Organ heartbeats ───────────────────────────────────────
  const orgSub = nc.subscribe('arifos.organ.>');
  console.log('[mesh-coord] Subscribed: arifos.organ.>');

  (async () => {
    for await (const msg of orgSub) {
      try {
        const data = JSON.parse(sc.decode(msg.data));
        const organId = data.organ || msg.subject.split('.').pop();
        organState.set(organId, {
          status: data.status || 'UNKNOWN',
          lastSeen: Date.now(),
          toolCount: data.tool_count || (data.health ? data.health.tools_loaded : 0),
        });
      } catch (_) {
        // Malformed heartbeat — skip
      }
    }
  })();

  // ── Gradient Computer (periodic) ──────────────────────────────────────
  setInterval(() => {
    computeAndPublishGradient(nc);
  }, CONFIG.GRADIENT_INTERVAL_S * 1000);

  // ── Mesh Status (periodic) ────────────────────────────────────────────
  setInterval(() => {
    publishMeshStatus(nc);
  }, 60_000);

  console.log('[mesh-coord] Loop coordinator active');
  return nc;
}

// ── Gradient Computer ──────────────────────────────────────────────────────

function computeAndPublishGradient(nc) {
  const now = Date.now();
  let score = 50; // baseline

  // Factor 1: Stale organs (each stale organ +10, each dead +20)
  let staleCount = 0;
  let deadCount = 0;
  for (const [organ, state] of organState) {
    const age = now - state.lastSeen;
    if (age > CONFIG.ORGAN_DEAD_THRESHOLD_S * 1000) {
      deadCount++;
      score += 20;
    } else if (age > CONFIG.ORGAN_STALE_THRESHOLD_S * 1000) {
      staleCount++;
      score += 10;
    }
  }

  // Factor 2: Recent HOLD density (each HOLD +2, cap +30)
  const recentWindow = CONFIG.GRADIENT_INTERVAL_S * 1000 * 2;
  const recentHolds = governanceEvents.filter(
    e => e.verdict === 'HOLD' && (now - e.timestamp) < recentWindow
  ).length;
  score += Math.min(recentHolds * 2, 30);

  // Factor 3: Breach density (each breach +5, cap +25)
  const totalBreaches = Array.from(breachCounts.values()).reduce((a, b) => a + b, 0);
  score += Math.min(totalBreaches * 5, 25);

  // Clamp
  gradientScore = Math.max(0, Math.min(100, score));

  // Determine gradient class
  let gradientClass = 'NOMINAL'; // 0-30
  if (gradientScore > 70) gradientClass = 'CRITICAL';
  else if (gradientScore > 50) gradientClass = 'ELEVATED';
  else if (gradientScore > 30) gradientClass = 'WATCH';

  // Publish gradient signal
  const payload = JSON.stringify({
    event: 'GRADIENT',
    score: gradientScore,
    class: gradientClass,
    factors: {
      stale_organs: staleCount,
      dead_organs: deadCount,
      recent_holds: recentHolds,
      total_breaches: totalBreaches,
    },
    organ_status: Object.fromEntries(
      Array.from(organState.entries()).map(([id, s]) => [
        id,
        { status: s.status, age_s: Math.round((now - s.lastSeen) / 1000) },
      ])
    ),
    timestamp: new Date().toISOString(),
  });

  try {
    nc.publish('arifos.mesh.gradient', JSON.stringify(payload));
    // Also publish a deduplicated one
    nc.publish(`arifos.mesh.gradient.${gradientClass.toLowerCase()}`, JSON.stringify(payload));
  } catch (_) {
    // Fire and forget
  }

  // Reset breach counts after computing gradient
  breachCounts.clear();
}

// ── Mesh Status Publisher ──────────────────────────────────────────────────

function publishMeshStatus(nc) {
  const now = Date.now();
  const organList = Array.from(organState.entries()).map(([id, s]) => ({
    organ: id,
    status: s.status,
    age_s: Math.round((now - s.lastSeen) / 1000),
  }));

  const payload = JSON.stringify({
    event: 'MESH_STATUS',
    gradient_score: gradientScore,
    governance_events_24h: governanceEvents.length,
    active_organs: organList.filter(o => o.age_s < CONFIG.ORGAN_STALE_THRESHOLD_S).length,
    total_organs: organList.length,
    organs: organList,
    recent_alerts: alerts.slice(-5),
    timestamp: new Date().toISOString(),
  });

  try {
    nc.publish('arifos.mesh.status', JSON.stringify(payload));
  } catch (_) {
    // Fire and forget
  }
}

// ── Alert Publisher ─────────────────────────────────────────────────────────

async function publishAlert(nc, alert) {
  const payload = JSON.stringify({
    event: 'MESH_ALERT',
    ...alert,
  });
  try {
    // Publish to governance stream so it's persistent
    await nc.publish('arifos.mesh.alert', JSON.stringify(payload));
  } catch (_) {
    // Fire and forget
  }
}

// ── Query API (for AAA cockpit) ────────────────────────────────────────────

function getMeshState() {
  const now = Date.now();
  return {
    gradient_score: gradientScore,
    governance_events: governanceEvents.slice(-20),
    hold_counts: Object.fromEntries(holdCounts),
    breach_counts: Object.fromEntries(breachCounts),
    organ_status: Array.from(organState.entries()).map(([id, s]) => ({
      organ: id,
      status: s.status,
      age_s: Math.round((now - s.lastSeen) / 1000),
    })),
    recent_alerts: alerts.slice(-10),
  };
}

// ── Exports ────────────────────────────────────────────────────────────────

module.exports = {
  startMeshCoordinator,
  getMeshState,
  CONFIG,
};
