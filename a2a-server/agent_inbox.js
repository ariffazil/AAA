#!/usr/bin/env node
/**
 * Agent Inbox — NATS JetStream-backed inter-agent message bus.
 *
 * Each agent gets a persistent inbox via NATS JetStream Key-Value store.
 * Messages follow the SIAL (Structured Inter-Agent Language) protocol.
 *
 * Architecture:
 *   Agent A ──send──▶ NATS KV agent.inbox.{B} ──poll──▶ Agent B
 *                         │
 *                   JetStream (persistent, 24h TTL)
 *                         │
 *                   AAA /inbox API (REST facade)
 *
 * DITEMPA BUKAN DIBERI — Forged 2026-08-05.
 */

const { connect, StringCodec, consumerOpts, AckPolicy, DeliverPolicy } = require('nats');
const crypto = require('crypto');

// ── SIAL Schema v1.0 ─────────────────────────────────────────────────────
// Structured Inter-Agent Language — lossless A2A messaging

const SIAL_VERSION = '1.0.0';

/**
 * Validate a SIAL message envelope.
 * @param {object} msg
 * @returns {{ valid: boolean, errors: string[] }}
 */
function validateSIAL(msg) {
    const errors = [];
    if (!msg) { errors.push('message is null/undefined'); return { valid: false, errors }; }
    if (!msg.from || typeof msg.from !== 'string') errors.push('missing or invalid "from"');
    if (!msg.to || typeof msg.to !== 'string') errors.push('missing or invalid "to"');
    if (!msg.intent || typeof msg.intent !== 'string') errors.push('missing or invalid "intent"');
    if (msg.evidence !== undefined && typeof msg.evidence !== 'object') errors.push('"evidence" must be an object if present');
    if (msg.constraints !== undefined && typeof msg.constraints !== 'object') errors.push('"constraints" must be an object if present');
    if (msg.expected_output_schema !== undefined && typeof msg.expected_output_schema !== 'object')
        errors.push('"expected_output_schema" must be an object if present');
    return { valid: errors.length === 0, errors };
}

/**
 * Create a SIAL envelope.
 * @param {string} from - Sending agent ID
 * @param {string} to - Receiving agent ID
 * @param {string} intent - Natural language intent
 * @param {object} [evidence] - { OBS: [], DER: [], INT: [] }
 * @param {object} [constraints] - { reversibility, max_cost, deadline }
 * @param {object} [expected_output_schema] - JSON Schema for expected response
 * @returns {object} SIAL envelope
 */
function createSIAL(from, to, intent, evidence, constraints, expected_output_schema) {
    return {
        sial_version: SIAL_VERSION,
        msg_id: crypto.randomUUID(),
        from,
        to,
        intent,
        evidence: evidence || { OBS: [], DER: [], INT: [] },
        constraints: constraints || { reversibility: 'reversible' },
        expected_output_schema: expected_output_schema || null,
        timestamp: new Date().toISOString(),
        ttl_seconds: 86400, // 24h
    };
}

// ── Agent Inbox ──────────────────────────────────────────────────────────

const INBOX_KV_BUCKET = 'agent_inbox';
const MAX_MSGS_PER_AGENT = 1000;

class AgentInbox {
    constructor() {
        /** @type {import('nats').NatsConnection|null} */
        this.nc = null;
        /** @type {import('nats').KV|null} */
        this.kv = null;
        this.sc = StringCodec();
        this._connected = false;
    }

    /**
     * Connect to NATS and initialize KV store.
     * @param {string} natsUrl
     */
    async connect(natsUrl = 'nats://127.0.0.1:4222') {
        try {
            this.nc = await connect({ servers: natsUrl, reconnect: true, maxReconnectAttempts: -1 });
            const jsm = await this.nc.jetstreamManager();
            const js = this.nc.jetstream();

            // Create KV bucket if not exists
            try {
                this.kv = await js.views.kv(INBOX_KV_BUCKET);
                console.log(`[inbox] KV bucket '${INBOX_KV_BUCKET}' exists`);
            } catch {
                this.kv = await js.views.kv(INBOX_KV_BUCKET, { history: 5, maxBucketSize: 100 * 1024 * 1024 }); // 100MB
                console.log(`[inbox] KV bucket '${INBOX_KV_BUCKET}' created`);
            }

            this._connected = true;
            console.log('[inbox] Agent Inbox connected to NATS');
            return true;
        } catch (e) {
            console.error('[inbox] NATS connection failed:', e.message);
            this._connected = false;
            return false;
        }
    }

    get connected() { return this._connected; }

    /**
     * Format the KV key for an agent's inbox message.
     * @param {string} agentId
     * @param {string} msgId
     * @returns {string}
     */
    _key(agentId, msgId) {
        return `${agentId}.${msgId}`;
    }

    /**
     * Send a message to an agent's inbox.
     * @param {object} sialEnvelope - SIAL message (validated)
     * @returns {Promise<{ok: boolean, msg_id: string, error?: string}>}
     */
    async send(sialEnvelope) {
        if (!this._connected || !this.kv) {
            return { ok: false, error: 'inbox not connected' };
        }

        const validation = validateSIAL(sialEnvelope);
        if (!validation.valid) {
            return { ok: false, error: `SIAL validation failed: ${validation.errors.join('; ')}` };
        }

        // Ensure msg_id exists
        if (!sialEnvelope.msg_id) {
            sialEnvelope.msg_id = crypto.randomUUID();
        }
        sialEnvelope.sial_version = SIAL_VERSION;
        sialEnvelope.timestamp = sialEnvelope.timestamp || new Date().toISOString();

        const key = this._key(sialEnvelope.to, sialEnvelope.msg_id);
        const value = this.sc.encode(JSON.stringify(sialEnvelope));

        try {
            await this.kv.put(key, value);
            console.log(`[inbox] ${sialEnvelope.from} → ${sialEnvelope.to}: ${sialEnvelope.intent.substring(0, 60)}`);

            // Also publish on a realtime subject for push-based consumers
            if (this.nc) {
                this.nc.publish(`agent.inbox.${sialEnvelope.to}`, value);
            }

            return { ok: true, msg_id: sialEnvelope.msg_id, to: sialEnvelope.to };
        } catch (e) {
            console.error(`[inbox] send failed: ${e.message}`);
            return { ok: false, error: e.message };
        }
    }

    /**
     * Poll messages for an agent from its inbox.
     * @param {string} agentId
     * @param {object} [opts] - { limit, markRead, since }
     * @returns {Promise<{ok: boolean, messages: object[], count: number, error?: string}>}
     */
    async poll(agentId, opts = {}) {
        if (!this._connected || !this.kv) {
            return { ok: false, messages: [], count: 0, error: 'inbox not connected' };
        }

        const limit = opts.limit || 20;
        const prefix = `${agentId}.`;

        try {
            const keysIterable = await this.kv.keys();
            const allKeys = [];
            for await (const k of keysIterable) {
                allKeys.push(k);
            }
            const agentKeys = allKeys.filter(k => k.startsWith(prefix));

            if (agentKeys.length === 0) {
                return { ok: true, messages: [], count: 0 };
            }

            // Sort by timestamp (most recent first, then limit)
            const messages = [];
            for (const key of agentKeys.slice(-limit)) {
                try {
                    const entry = await this.kv.get(key);
                    if (entry) {
                        const msg = JSON.parse(this.sc.decode(entry.value));
                        msg._kv_key = key;
                        msg._kv_revision = entry.revision;
                        msg._created = entry.created;
                        messages.push(msg);
                    }
                } catch (_) {
                    // Skip corrupted entries
                }
            }

            // Sort by timestamp descending
            messages.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

            return { ok: true, messages: messages.slice(0, limit), count: messages.length };
        } catch (e) {
            console.error(`[inbox] poll failed for ${agentId}: ${e.message}`);
            return { ok: false, messages: [], count: 0, error: e.message };
        }
    }

    /**
     * Get a specific message by ID.
     * @param {string} agentId
     * @param {string} msgId
     * @returns {Promise<{ok: boolean, message?: object, error?: string}>}
     */
    async get(agentId, msgId) {
        if (!this._connected || !this.kv) {
            return { ok: false, error: 'inbox not connected' };
        }

        const key = this._key(agentId, msgId);
        try {
            const entry = await this.kv.get(key);
            if (!entry) {
                return { ok: false, error: 'message not found' };
            }
            const msg = JSON.parse(this.sc.decode(entry.value));
            msg._kv_key = key;
            msg._kv_revision = entry.revision;
            msg._created = entry.created;
            return { ok: true, message: msg };
        } catch (e) {
            return { ok: false, error: e.message };
        }
    }

    /**
     * Delete a message from an agent's inbox (mark as read).
     * @param {string} agentId
     * @param {string} msgId
     * @returns {Promise<{ok: boolean, error?: string}>}
     */
    async delete(agentId, msgId) {
        if (!this._connected || !this.kv) {
            return { ok: false, error: 'inbox not connected' };
        }

        const key = this._key(agentId, msgId);
        try {
            await this.kv.delete(key);
            return { ok: true };
        } catch (e) {
            return { ok: false, error: e.message };
        }
    }

    /**
     * Subscribe to realtime inbox notifications for an agent.
     * @param {string} agentId
     * @param {function} callback - receives parsed SIAL message
     * @returns {Promise<import('nats').Sub>}
     */
    async subscribe(agentId, callback) {
        if (!this._connected || !this.nc) {
            throw new Error('inbox not connected');
        }
        const sub = this.nc.subscribe(`agent.inbox.${agentId}`);
        (async () => {
            for await (const msg of sub) {
                try {
                    const sial = JSON.parse(this.sc.decode(msg.data));
                    callback(sial);
                } catch (e) {
                    console.error(`[inbox] callback error for ${agentId}: ${e.message}`);
                }
            }
        })();
        console.log(`[inbox] subscribed to agent.inbox.${agentId}`);
        return sub;
    }

    /**
     * Get inbox statistics for all agents.
     * @returns {Promise<{ok: boolean, stats: object, error?: string}>}
     */
    async stats() {
        if (!this._connected || !this.kv) {
            return { ok: false, error: 'inbox not connected' };
        }

        try {
            const keysIterable = await this.kv.keys();
            const allKeys = [];
            for await (const k of keysIterable) {
                allKeys.push(k);
            }
            const agentCounts = {};
            for (const key of allKeys) {
                const agentId = key.split('.')[0];
                agentCounts[agentId] = (agentCounts[agentId] || 0) + 1;
            }

            const status = await this.kv.status();
            return {
                ok: true,
                stats: {
                    total_messages: allKeys.length,
                    agents_with_mail: Object.keys(agentCounts).length,
                    per_agent: agentCounts,
                    bucket: status ? { bytes: status.backingStore ? 'JetStream' : 'memory', entries: status.values } : null,
                },
            };
        } catch (e) {
            return { ok: false, error: e.message };
        }
    }

    /**
     * Graceful shutdown.
     */
    async close() {
        if (this.nc) {
            await this.nc.drain();
            console.log('[inbox] NATS connection drained');
        }
        this._connected = false;
    }
}

// ── Singleton ────────────────────────────────────────────────────────────

let _inbox = null;

async function getInbox(natsUrl) {
    if (!_inbox) {
        _inbox = new AgentInbox();
        await _inbox.connect(natsUrl);
    }
    return _inbox;
}

module.exports = {
    AgentInbox,
    getInbox,
    validateSIAL,
    createSIAL,
    SIAL_VERSION,
};
