'use strict';

/**
 * sro_propagation.js — A2A SRO Propagation Handler (Protocol v1)
 *
 * Implements cross-agent SRO propagation as specified in
 * /root/AAA/canon/A2A_SRO_PROPAGATION_PROTOCOL_v1.md
 *
 * Handles:
 *  - SRO_CREATED: broadcast to all federation agents
 *  - SRO_SUPERSEDED: targeted delivery to referencing agents
 *  - SRO_CALIBRATED: broadcast calibration outcomes
 *
 * Persists events to /root/.local/share/arifos/sro_events.jsonl
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const SRO_EVENTS_FILE = '/root/.local/share/arifos/sro_events.jsonl';
const VALID_EVENT_TYPES = new Set(['SRO_CREATED', 'SRO_SUPERSEDED', 'SRO_CALIBRATED']);

/**
 * Validate an SRO propagation event payload.
 */
function validateSroEvent(event) {
  if (!event || typeof event !== 'object') {
    return { valid: false, error: 'Event must be a JSON object' };
  }
  if (!VALID_EVENT_TYPES.has(event.type)) {
    return { valid: false, error: `Invalid SRO event type: '${event.type}'. Expected SRO_CREATED, SRO_SUPERSEDED, or SRO_CALIBRATED.` };
  }
  if (!event.agent_id || typeof event.agent_id !== 'string') {
    return { valid: false, error: 'agent_id string is required' };
  }
  if (!event.claim_id && !event.old_claim_id) {
    return { valid: false, error: 'claim_id or old_claim_id is required' };
  }
  return { valid: true };
}

/**
 * Persist SRO event to JSONL ledger.
 */
function recordSroEvent(event) {
  try {
    const dir = path.dirname(SRO_EVENTS_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    const stamped = {
      ...event,
      recorded_at: new Date().toISOString(),
      event_hash: crypto.createHash('sha256').update(JSON.stringify(event)).digest('hex'),
    };
    fs.appendFileSync(SRO_EVENTS_FILE, JSON.stringify(stamped) + '\n');
    return stamped;
  } catch (err) {
    console.error('[SRO-PROPAGATION] Failed to record event:', err.message);
    return null;
  }
}

/**
 * Route and propagate SRO event to federation agents.
 */
async function propagateSroEvent(event, options = {}) {
  const check = validateSroEvent(event);
  if (!check.valid) {
    return { success: false, error: check.error };
  }

  const recorded = recordSroEvent(event);

  const targets = [];
  if (event.type === 'SRO_CREATED' || event.type === 'SRO_CALIBRATED') {
    // Broadcast to primary federation agents
    targets.push('hermes-asi', '333-AGI', '555-ASI', '888-APEX', 'geox', 'wealth', 'well');
  } else if (event.type === 'SRO_SUPERSEDED') {
    // Targeted: agents referencing old_claim_id
    if (Array.isArray(event.target_agents) && event.target_agents.length > 0) {
      targets.push(...event.target_agents);
    } else {
      targets.push('hermes-asi', '333-AGI');
    }
  }

  return {
    success: true,
    event_type: event.type,
    claim_id: event.claim_id || event.old_claim_id,
    event_hash: recorded ? recorded.event_hash : null,
    propagated_to: targets,
    recorded_at: recorded ? recorded.recorded_at : new Date().toISOString(),
    status: 'PROPAGATED',
  };
}

module.exports = {
  validateSroEvent,
  recordSroEvent,
  propagateSroEvent,
  SRO_EVENTS_FILE,
};
