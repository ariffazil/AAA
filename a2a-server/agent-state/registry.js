/**
 * AGENT REGISTRY — Civil Registry of All Agents
 * 
 * "REGISTERED does not mean AUTHORIZED."
 * 
 * Redis-backed. Every agent gets an agent_id. No anonymous agents.
 * No duplicate identities. No "temporary helper" outside the registry.
 * 
 * DITEMPA BUKAN DIBERI
 */

const redis = require('redis');
const { VALID_TRANSITIONS, AGENT_STATES } = require('./schemas');

const REGISTRY_KEY = 'aaa:agent_registry';
const STATE_PREFIX = 'aaa:agent:';

let _client = null;

function getRedis() {
  if (!_client) {
    _client = redis.createClient({ socket: { host: '127.0.0.1', port: 6379 } });
    _client.on('error', (err) => console.warn('Redis agent-registry:', err.message));
    _client.connect().catch(() => {});
  }
  return _client;
}

// ── Agent Registry CRUD ─────────────────────────────────────────────

/**
 * Register a new agent. Agent starts as CLAIMED.
 * @param {Object} params
 * @param {string} params.agent_name
 * @param {string} params.agent_class
 * @param {string} params.sovereign_owner
 * @param {Object} [params.identity]
 * @param {Object} [params.manifest]
 * @returns {Promise<Object>}
 */
async function registerAgent({ agent_name, agent_class, sovereign_owner, identity, manifest }) {
  const r = getRedis();
  const agent_id = `AGENT-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,8)}`;
  
  const agent = {
    agent_id,
    agent_name,
    agent_class,
    sovereign_owner: sovereign_owner || 'ARIF_FAZIL',
    identity: {
      claimed_by: identity?.claimed_by || 'agent manifest',
      verified: identity?.verified || false,
      verification_method: identity?.verification_method || 'none',
    },
    body: identity?.body || { runtime: 'local', model: 'unknown', host: 'af-forge' },
    manifest: manifest || {
      declared_purpose: '',
      declared_capabilities: [],
      declared_tools: [],
      declared_limits: [],
      version: '0.1.0',
      hash: '',
    },
    capability_attestation: {
      status: 'UNATTESTED',
      evidence: [],
      last_checked_at: null,
    },
    context: null,
    lease: null,
    policy: {
      floors_bound: ['F1', 'F2', 'F13'],
      risk_tier: 'low',
      requires_human_ack: false,
    },
    health: { status: 'warming', heartbeat_at: null, error_state: null },
    audit: { vault_chain: 'VAULT999', events: [], last_seal: null },
    termination: { kill_switch: true, revocation_reason: null, postmortem_required: true },
    state: 'REGISTERED',
    created_at: new Date().toISOString(),
    created_by: identity?.claimed_by || 'AAA',
    version: 1,
  };

  const key = STATE_PREFIX + agent_id;
  await r.set(key, JSON.stringify(agent));

  // Add to registry index
  await r.hSet(REGISTRY_KEY, agent_id, JSON.stringify({
    agent_id, agent_name, state: 'REGISTERED', agent_class, created_at: agent.created_at,
  }));

  await _logAuditEvent(agent_id, 'AGENT_REGISTERED', { agent_name, agent_class });
  return agent;
}

/**
 * Get an agent by ID.
 */
async function getAgent(agent_id) {
  const r = getRedis();
  const raw = await r.get(STATE_PREFIX + agent_id);
  if (!raw) return null;
  return JSON.parse(raw);
}

/**
 * List all registered agent IDs.
 */
async function listAgents() {
  const r = getRedis();
  const all = await r.hGetAll(REGISTRY_KEY);
  return Object.values(all).map(v => JSON.parse(v));
}

/**
 * Transition agent state. Validates transition legality.
 */
async function transitionState(agent_id, new_state, metadata = {}) {
  const r = getRedis();
  const raw = await r.get(STATE_PREFIX + agent_id);
  if (!raw) throw new Error(`Agent ${agent_id} not found`);

  const agent = JSON.parse(raw);
  const current = agent.state;

  const allowed = VALID_TRANSITIONS[current] || [];
  if (!allowed.includes(new_state)) {
    throw new Error(`Invalid transition: ${current} → ${new_state}. Allowed: ${allowed.join(', ')}`);
  }

  agent.state = new_state;
  agent.version = (agent.version || 1) + 1;
  agent.updated_at = new Date().toISOString();

  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await r.hSet(REGISTRY_KEY, agent_id, JSON.stringify({
    agent_id, agent_name: agent.agent_name, state: new_state,
    agent_class: agent.agent_class, updated_at: agent.updated_at,
  }));

  // Log the state transition to VAULT999 events
  if (['MANIFESTED', 'ATTESTED', 'LEASED', 'SUSPENDED', 'REVOKED', 'SEALED'].includes(new_state)) {
    const eventType = `AGENT_${new_state === 'LEASED' ? 'LEASED' : new_state === 'SUSPENDED' ? 'SUSPENDED' : 'REGISTERED'}`;
    await _logAuditEvent(agent_id, eventType, { from: current, to: new_state, ...metadata });
  }

  return agent;
}

/**
 * Manifest an agent — declare its purpose, tools, limits.
 */
async function manifestAgent(agent_id, manifest) {
  const agent = await getAgent(agent_id);
  if (!agent) throw new Error(`Agent ${agent_id} not found`);

  agent.manifest = {
    declared_purpose: manifest.purpose || agent.manifest?.declared_purpose || '',
    declared_capabilities: manifest.capabilities || [],
    declared_tools: manifest.tools || [],
    declared_limits: manifest.limits || [],
    version: manifest.version || '0.1.0',
    hash: manifest.hash || '',
  };

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'MANIFEST_SUBMITTED', manifest);

  return transitionState(agent_id, 'MANIFESTED', { manifest_hash: manifest.hash });
}

/**
 * Attest an agent's capabilities.
 */
async function attestAgent(agent_id, attestation) {
  const agent = await getAgent(agent_id);
  if (!agent) throw new Error(`Agent ${agent_id} not found`);

  agent.capability_attestation = {
    status: attestation.status || 'LIVE_ATTESTED',
    evidence: attestation.evidence || [],
    last_checked_at: new Date().toISOString(),
  };

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'CAPABILITY_ATTESTED', attestation);

  return transitionState(agent_id, 'ATTESTED', attestation);
}

/**
 * Bind context to an agent.
 */
async function bindContext(agent_id, context_packet) {
  const agent = await getAgent(agent_id);
  if (!agent) throw new Error(`Agent ${agent_id} not found`);

  agent.context = context_packet;

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'CONTEXT_ATTACHED', { context_id: context_packet.context_id });

  return transitionState(agent_id, 'CONTEXT_BOUND', { context_id: context_packet.context_id });
}

/**
 * Grant a lease to an agent.
 */
async function grantLease(agent_id, lease) {
  const agent = await getAgent(agent_id);
  if (!agent) throw new Error(`Agent ${agent_id} not found`);

  const lease_id = `LEASE-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,6)}`;
  agent.lease = {
    lease_id,
    authority_granter: lease.authority_granter || 'AAA_JUDGE',
    allowed_actions: lease.allowed_actions || ['observe'],
    forbidden_actions: lease.forbidden_actions || [],
    expires_at: lease.expires_at || new Date(Date.now() + 3600000).toISOString(),
    revocable: lease.revocable !== false,
    status: 'active',
  };

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'LEASE_GRANTED', agent.lease);

  return transitionState(agent_id, 'LEASED', { lease_id });
}

/**
 * Revoke an agent's lease.
 */
async function revokeLease(agent_id, reason) {
  const agent = await getAgent(agent_id);
  if (!agent) throw new Error(`Agent ${agent_id} not found`);

  if (agent.lease) {
    agent.lease.status = 'revoked';
    agent.lease.revocation_reason = reason || 'Administrative revocation';
  }

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'LEASE_REVOKED', { reason });

  return agent;
}

/**
 * Suspend an agent — no action allowed.
 */
async function suspendAgent(agent_id, reason) {
  const agent = await transitionState(agent_id, 'SUSPENDED', { reason });
  agent.health = { ...agent.health, status: 'suspended', error_state: reason };
  agent.termination = { ...agent.termination, revocation_reason: reason };

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'AGENT_SUSPENDED', { reason });

  return agent;
}

/**
 * Seal an agent — full audit written to VAULT999.
 */
async function sealAgent(agent_id) {
  const agent = await getAgent(agent_id);
  if (!agent) throw new Error(`Agent ${agent_id} not found`);

  agent.audit = {
    ...agent.audit,
    last_seal: new Date().toISOString(),
    events: [...(agent.audit?.events || []), { type: 'SEALED', at: new Date().toISOString() }],
  };

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'SESSION_SEALED', {});

  return transitionState(agent_id, 'SEALED');
}

/**
 * Update agent heartbeat.
 */
async function heartbeat(agent_id) {
  const agent = await getAgent(agent_id);
  if (!agent) return null;

  agent.health = {
    ...agent.health,
    status: agent.health?.status === 'degraded' ? 'active' : (agent.health?.status || 'active'),
    heartbeat_at: new Date().toISOString(),
    error_state: null,
  };

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  return agent;
}

/**
 * Inspect agent — full state dump.
 */
async function inspectAgent(agent_id) {
  return getAgent(agent_id);
}

// ── Audit ───────────────────────────────────────────────────────────

async function _logAuditEvent(agent_id, event_type, payload = {}) {
  try {
    const r = getRedis();
    const event = {
      agent_id,
      event_type,
      payload,
      timestamp: new Date().toISOString(),
    };
    await r.lPush(`aaa:audit:${agent_id}`, JSON.stringify(event));
    await r.lPush('aaa:audit:global', JSON.stringify(event));
  } catch (e) {
    console.warn('Audit log failed:', e.message);
  }
}

// ── Kill Switch ─────────────────────────────────────────────────────

/**
 * Kill an agent — hard revoke + seal.
 */
async function killAgent(agent_id, reason) {
  await revokeLease(agent_id, reason);
  const agent = await transitionState(agent_id, 'REVOKED', { reason });
  agent.health = { ...agent.health, status: 'dead' };
  agent.termination = {
    kill_switch: true,
    revocation_reason: reason,
    postmortem_required: true,
  };

  const r = getRedis();
  await r.set(STATE_PREFIX + agent_id, JSON.stringify(agent));
  await _logAuditEvent(agent_id, 'AGENT_RETIRED', { reason });

  return sealAgent(agent_id);
}

// ── Exports ─────────────────────────────────────────────────────────

module.exports = {
  registerAgent,
  getAgent,
  listAgents,
  transitionState,
  manifestAgent,
  attestAgent,
  bindContext,
  grantLease,
  revokeLease,
  suspendAgent,
  sealAgent,
  heartbeat,
  inspectAgent,
  killAgent,
};
