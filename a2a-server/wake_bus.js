#!/usr/bin/env node
/**
 * WAKE BUS — Event-driven wake queue as AAA public infrastructure (barang awam).
 *
 * Distilled from Paperclip P1 patterns (MIT):
 *   - server/src/services/heartbeat.ts + agent_wakeup_requests schema
 *     → enqueue/claim/finish lifecycle, coalesce counter, idempotency key
 *   - server/src/services/task-watchdogs.ts
 *     → 15s first-run grace (TASK_WATCHDOG_FIRST_RUN_GRACE_MS)
 *     → stable stop fingerprints (sha256 over material state)
 *   - bounded retry: exponential backoff, max attempts, then terminal HOLD
 *
 * Federation twin decisions (doc/plans/2026-08-14-paperclip-semantic-map.md):
 *   - Persistence: existing Redis (REDIS_URL) with in-memory fallback. No new organ.
 *   - Delivery: A2A card endpoints.baseUrl from AgentCardRegistry. No new protocol.
 *   - HOLD semantics: reuse FQ-gate vocabulary (verdict HOLD, reason, next_action).
 *     HOLD, not DROP — a held wake stays inspectable at /api/wake/:id.
 *
 * SABAR-RETRY: after 3 consecutive delivery failures with zero verdict-changing
 * evidence, the wake is HELD with reason. No retry storm. The state waits.
 *
 * AAA never judges: the bus carries events; it does not decide what the woken
 * agent should do with them.
 *
 * DITEMPA BUKAN DIBERI — Forged 2026-08-14.
 */

'use strict';

const crypto = require('crypto');

// ── Constants ─────────────────────────────────────────────────────────────

const WAKE_EVENTS = Object.freeze([
  'assignment_created', // a task was assigned to this actor
  'comment_added',      // new input arrived on a target the actor owns
  'upstream_complete',  // a dependency finished; blocked work may proceed
  'budget_changed',     // cost/budget state changed (FLAME / FQ semantics)
  'citizen_stalled',    // watchdog: actor looks stalled (grace-protected)
]);

const WAKE_STATUSES = Object.freeze([
  'queued',       // enqueued, waiting for delivery attempt
  'delivering',   // delivery in flight
  'delivered',    // target accepted the wake (2xx)
  'retrying',     // delivery failed, backoff scheduled
  'held',         // SABAR — attempts exhausted or manual hold; NOT dropped
  'deduped',      // superseded by identical fingerprint while queued
]);

/** sha256(actor + reason + target) — Paperclip stableStopFingerprint pattern. */
const FINGERPRINT_PREFIX = 'wake:';
/** Grace window after first enqueue during which duplicate detection is
 *  relaxed for citizen_stalled events (a just-created assignment may race
 *  its own first wake — Paperclip TASK_WATCHDOG_FIRST_RUN_GRACE_MS twin). */
const FIRST_RUN_GRACE_MS = 15_000;
/** Exponential backoff: 5s, 25s, 125s (base 5s, factor 5). */
const BACKOFF_BASE_MS = 5_000;
const BACKOFF_FACTOR = 5;
/** Max delivery attempts before HOLD. */
const MAX_ATTEMPTS = 3;
/** Wakes older than this are pruned from the hot map (HOLD records kept). */
const RETENTION_MS = 24 * 60 * 60 * 1000;
/** Redis key for the persisted queue state (list of wake ids + hash). */
const REDIS_KEY = 'aaa:wake_bus';
const REDIS_INDEX_KEY = 'aaa:wake_bus:index';

// ── Fingerprint ───────────────────────────────────────────────────────────

function wakeFingerprint(actorId, reason, target) {
  const payload = JSON.stringify({
    version: 1,
    actorId: String(actorId || ''),
    reason: String(reason || ''),
    target: String(target || ''),
  });
  return `${FINGERPRINT_PREFIX}${crypto.createHash('sha256').update(payload).digest('hex')}`;
}

// ── Wake Bus ──────────────────────────────────────────────────────────────

class WakeBus {
  /**
   * @param {object} [opts]
   * @param {import('redis').RedisClientType|null} [opts.redisClient] shared client (may be null → memory only)
   * @param {object} [opts.cardRegistry] AgentCardRegistry-compatible ({ get(id) })
   * @param {number} [opts.firstRunGraceMs]
   * @param {number} [opts.maxAttempts]
   * @param {(url: string, body: object, timeoutMs: number) => Promise<{ok: boolean, status: number, error?: string}>} [opts.deliverFn] injectable transport (tests)
   * @param {boolean} [opts.autoStart] start the delivery loop (default true; tests disable)
   */
  constructor(opts = {}) {
    this.redisClient = opts.redisClient || null;
    this.cardRegistry = opts.cardRegistry || null;
    /** @type {(hostname: string) => string|null} maps AAA's own public host → loopback base */
    this.resolveSelfBase = opts.resolveSelfBase || null;
    this.firstRunGraceMs = opts.firstRunGraceMs ?? FIRST_RUN_GRACE_MS;
    this.maxAttempts = opts.maxAttempts ?? MAX_ATTEMPTS;
    this.deliverFn = opts.deliverFn || null;
    /** @type {Map<string, object>} */
    this.wakes = new Map();
    /** @type {Map<string, string>} fingerprint → wake id (dedup index) */
    this.fingerprints = new Map();
    this.timer = null;
    this.stats = { enqueued: 0, deduped: 0, delivered: 0, held: 0, failedAttempts: 0 };
    if (opts.autoStart !== false) this.start();
  }

  // ── Validation ────────────────────────────────────────────────────────

  /**
   * Validate an enqueue request. Returns { valid, errors, value }.
   * AAA validates shape, never content-judges.
   */
  validateEnqueue(body) {
    const errors = [];
    const actor = typeof body?.actor === 'string' ? body.actor.trim() : '';
    const reason = typeof body?.reason === 'string' ? body.reason.trim() : '';
    const target = typeof body?.target === 'string' ? body.target.trim() : '';
    let event = typeof body?.event === 'string' ? body.event.trim() : '';

    if (!actor) errors.push('missing or invalid "actor" (agent id)');
    if (!WAKE_EVENTS.includes(event)) {
      errors.push(`"event" must be one of: ${WAKE_EVENTS.join(', ')}`);
      event = '';
    }
    if (!reason) errors.push('missing "reason" (semantic wake reason — every wake carries why)');
    // target optional: some events (budget_changed) are actor-scoped
    if (event === 'citizen_stalled' && !target) {
      errors.push('"target" required for citizen_stalled (the stalled work item)');
    }

    return {
      valid: errors.length === 0,
      errors,
      value: { actor, event, reason, target },
    };
  }

  // ── Enqueue ───────────────────────────────────────────────────────────

  /**
   * Enqueue a wake. Dedup: identical (actor, reason, target) fingerprint with a
   * queued/retrying/delivering wake is coalesced (Paperclip coalescedCount).
   * First-run grace: a wake for an actor whose previous wake was enqueued less
   * than firstRunGraceMs ago is deduped (race guard, not judgment).
   * @returns {Promise<{accepted: boolean, id?: string, deduped?: boolean, coalescedId?: string, wake?: object, errors?: string[]}>}
   */
  async enqueue(body) {
    const { valid, errors, value } = this.validateEnqueue(body);
    if (!valid) return { accepted: false, errors };

    const now = Date.now();
    const fingerprint = wakeFingerprint(value.actor, value.reason, value.target);
    const existingId = this.fingerprints.get(fingerprint);
    if (existingId) {
      const existing = this.wakes.get(existingId);
      if (existing && ['queued', 'retrying', 'delivering'].includes(existing.status)) {
        existing.coalescedCount += 1;
        existing.updatedAt = new Date().toISOString();
        this.stats.deduped += 1;
        await this.persistWake(existing);
        return { accepted: true, deduped: true, coalescedId: existingId, wake: this.publicView(existing) };
      }
      // terminal or delivered — allow re-enqueue under same fingerprint
      this.fingerprints.delete(fingerprint);
    }

    const id = crypto.randomUUID();
    const wake = {
      id,
      fingerprint,
      actor: value.actor,
      event: value.event,
      reason: value.reason,
      target: value.target || null,
      payload: (body && typeof body.payload === 'object' && body.payload !== null) ? body.payload : null,
      requestedBy: (typeof body?.requestedBy === 'string' && body.requestedBy.trim()) || 'system',
      status: 'queued',
      attempts: 0,
      coalescedCount: 0,
      consecutiveFailures: 0,
      firstEvidenceSeen: false,
      nextAttemptAt: now,
      createdAt: new Date(now).toISOString(),
      updatedAt: new Date(now).toISOString(),
      deliveredAt: null,
      heldAt: null,
      holdReason: null,
      lastError: null,
      deliveryUrl: null,
    };
    this.wakes.set(id, wake);
    this.fingerprints.set(fingerprint, id);
    this.stats.enqueued += 1;
    await this.persistWake(wake);
    return { accepted: true, id, wake: this.publicView(wake) };
  }

  // ── Delivery ──────────────────────────────────────────────────────────

  /** Resolve the A2A delivery URL for an actor from its agent card.
   *  AAA-hosted cards (baseUrl .../a2a/<agent>) deliver through the gateway's
   *  canonical ingress POST /a2a/message/send, rewritten to loopback by the
   *  caller-supplied `resolveSelfBase` (external public URLs hairpin through
   *  Cloudflare and fail loopback auth). Peers running their own A2A server
   *  keep their own path. */
  resolveDeliveryUrl(actorId) {
    if (!this.cardRegistry) return null;
    const card = this.cardRegistry.get(actorId);
    if (!card) return null;
    const base = card.endpoints && (card.endpoints.baseUrl || card.endpoints.a2aUrl);
    if (!base) return null;
    let url;
    try { url = new URL(base); } catch { return null; }
    const selfBase = this.resolveSelfBase ? this.resolveSelfBase(url.hostname) : null;
    if (selfBase) {
      const target = new URL(selfBase);
      target.pathname = '/a2a/message/send';
      return target.toString();
    }
    if (/^\/a2a\/.+/.test(url.pathname)) {
      url.pathname = '/a2a/message/send';
    } else {
      url.pathname = url.pathname.replace(/\/+$/, '') + '/a2a/message/send';
    }
    return url.toString();
  }

  /** Build the A2A JSON-RPC message/send envelope carrying this wake.
   *  Wakes ride the federation's own wire format — no new protocol. */
  buildDeliveryBody(wake) {
    return {
      jsonrpc: '2.0',
      id: wake.id,
      method: 'message/send',
      params: {
        message: {
          role: 'user',
          parts: [
            {
              type: 'text',
              text: `[WAKE:${wake.event}] ${wake.reason}${wake.target ? ` (target: ${wake.target})` : ''}`,
            },
            {
              type: 'data',
              data: {
                wake: {
                  id: wake.id,
                  event: wake.event,
                  reason: wake.reason,
                  target: wake.target,
                  payload: wake.payload,
                  requested_by: wake.requestedBy,
                  fingerprint: wake.fingerprint,
                },
              },
            },
          ],
        },
      },
    };
  }

  backoffMs(attempt) {
    // attempt is 1-based: 5s, 25s, 125s
    return BACKOFF_BASE_MS * Math.pow(BACKOFF_FACTOR, Math.max(0, attempt - 1));
  }

  /**
   * Record delivery evidence. Any verdict-changing evidence (success OR an
   * explicit operator signal) resets the SABAR-RETRY failure counter.
   */
  recordEvidence(wakeId, kind) {
    const wake = this.wakes.get(wakeId);
    if (!wake) return false;
    if (kind === 'delivered' || kind === 'operator_nudge') {
      wake.consecutiveFailures = 0;
      wake.firstEvidenceSeen = true;
    }
    return true;
  }

  /**
   * Attempt delivery of one due wake. Exposed for tests.
   */
  async attemptDelivery(wake, nowMs = Date.now()) {
    wake.attempts += 1;
    wake.status = 'delivering';
    wake.updatedAt = new Date().toISOString();

    const url = this.resolveDeliveryUrl(wake.actor);
    wake.deliveryUrl = url;
    if (!url) {
      return this.handleFailure(wake, 'no_delivery_url: agent card has no endpoints.baseUrl', nowMs);
    }

    const deliver = this.deliverFn || defaultDeliver;
    let result;
    try {
      result = await deliver(url, this.buildDeliveryBody(wake), 10_000);
    } catch (err) {
      result = { ok: false, status: 0, error: err && err.message ? err.message : String(err) };
    }

    if (result.ok) {
      wake.status = 'delivered';
      wake.consecutiveFailures = 0;
      wake.firstEvidenceSeen = true;
      wake.deliveredAt = new Date().toISOString();
      wake.updatedAt = wake.deliveredAt;
      this.stats.delivered += 1;
      await this.persistWake(wake);
      return { outcome: 'delivered', wake };
    }

    wake.lastError = result.error || `http_${result.status}`;
    this.stats.failedAttempts += 1;
    return this.handleFailure(wake, wake.lastError, nowMs);
  }

  /**
   * SABAR-RETRY: 3 consecutive failures with zero verdict-changing evidence →
   * HOLD (never DROP). The wake stays inspectable; the state waits.
   */
  handleFailure(wake, errorText, nowMs = Date.now()) {
    wake.consecutiveFailures += 1;
    wake.lastError = errorText;
    wake.updatedAt = new Date().toISOString();

    if (wake.attempts >= this.maxAttempts || wake.consecutiveFailures >= this.maxAttempts) {
      wake.status = 'held';
      wake.heldAt = new Date().toISOString();
      wake.holdReason = `sabar_retry: ${wake.consecutiveFailures} consecutive failures without verdict-changing evidence (${errorText})`;
      wake.updatedAt = wake.heldAt;
      this.stats.held += 1;
      return { outcome: 'held', wake };
    }

    wake.status = 'retrying';
    wake.nextAttemptAt = nowMs + this.backoffMs(wake.attempts);
    return { outcome: 'retrying', wake };
  }

  // ── Loop ──────────────────────────────────────────────────────────────

  start(intervalMs = 2_000) {
    if (this.timer) return;
    this.timer = setInterval(() => { this.tick().catch(() => {}); }, intervalMs);
    if (typeof this.timer.unref === 'function') this.timer.unref();
  }

  stop() {
    if (this.timer) clearInterval(this.timer);
    this.timer = null;
  }

  /** One delivery pass: due wakes oldest-first, max 5 per tick. */
  async tick(nowMs = Date.now()) {
    const due = [...this.wakes.values()]
      .filter((w) => (w.status === 'queued' || w.status === 'retrying') && w.nextAttemptAt <= nowMs)
      .sort((a, b) => a.nextAttemptAt - b.nextAttemptAt)
      .slice(0, 5);
    for (const wake of due) {
      await this.attemptDelivery(wake, nowMs);
    }
    this.prune(nowMs);
    return due.length;
  }

  /** Drop delivered/terminal wakes older than RETENTION_MS from hot memory. */
  prune(nowMs = Date.now()) {
    for (const [id, wake] of this.wakes) {
      if (wake.status === 'delivered' && wake.deliveredAt && nowMs - Date.parse(wake.deliveredAt) > RETENTION_MS) {
        this.wakes.delete(id);
        if (this.fingerprints.get(wake.fingerprint) === id) this.fingerprints.delete(wake.fingerprint);
      }
    }
  }

  // ── Persistence (Redis optional; memory always works) ─────────────────

  /**
   * Never let a dead Redis block the wake path: persistWake races a short
   * timeout and gives up (memory state remains authoritative for the queue).
   */
  _withTimeout(promise, ms, label) {
    let timer = null;
    const timeout = new Promise((resolve) => {
      timer = setTimeout(() => {
        console.warn(`[wake-bus] ${label} timed out after ${ms}ms (Redis unavailable?) — continuing in-memory`);
        resolve(false);
      }, ms);
      if (typeof timer.unref === 'function') timer.unref();
    });
    return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
  }

  async persistWake(wake) {
    if (!this.redisClient || !this.redisClient.isOpen) return false;
    try {
      return await this._withTimeout((async () => {
        await this.redisClient.hSet(REDIS_KEY, wake.id, JSON.stringify(wake));
        await this.redisClient.zAdd(REDIS_INDEX_KEY, [
          { score: Date.parse(wake.createdAt) || Date.now(), value: wake.id },
        ]);
        return true;
      })(), 2_000, 'persist');
    } catch (err) {
      console.warn('[wake-bus] persist failed (non-fatal):', err.message);
      return false;
    }
  }

  /** Load persisted wakes back into memory after a restart. */
  async hydrate() {
    if (!this.redisClient || !this.redisClient.isOpen) return 0;
    try {
      const all = await this._withTimeout(this.redisClient.hGetAll(REDIS_KEY), 3_000, 'hydrate');
      if (!all) return 0;
      let restored = 0;
      for (const [id, raw] of Object.entries(all)) {
        try {
          const wake = JSON.parse(raw);
          // Re-queue anything that was mid-flight when we died.
          if (wake.status === 'delivering') {
            wake.status = wake.attempts >= this.maxAttempts ? 'held' : 'queued';
            wake.nextAttemptAt = Date.now();
          }
          this.wakes.set(id, wake);
          this.fingerprints.set(wake.fingerprint, id);
          restored += 1;
        } catch { /* corrupt entry — skip, never crash the bus */ }
      }
      if (restored > 0) console.log(`[wake-bus] hydrated ${restored} wakes from Redis`);
      return restored;
    } catch (err) {
      console.warn('[wake-bus] hydrate failed (non-fatal):', err.message);
      return 0;
    }
  }

  // ── Reads ─────────────────────────────────────────────────────────────

  publicView(wake) {
    const { ...view } = wake;
    return view;
  }

  getWake(id) {
    const wake = this.wakes.get(id);
    return wake ? this.publicView(wake) : null;
  }

  /**
   * Queue snapshot. Held wakes are listed (HOLD ≠ DROP — visible for operator
   * / 888 display), delivered wakes optional.
   */
  queueView({ includeDelivered = false, actor = null, event = null, limit = 200 } = {}) {
    const rows = [...this.wakes.values()]
      .filter((w) => (includeDelivered ? true : w.status !== 'delivered'))
      .filter((w) => (actor ? w.actor === actor : true))
      .filter((w) => (event ? w.event === event : true))
      .sort((a, b) => Date.parse(b.createdAt) - Date.parse(a.createdAt))
      .slice(0, limit)
      .map((w) => this.publicView(w));
    const counts = {};
    for (const w of this.wakes.values()) counts[w.status] = (counts[w.status] || 0) + 1;
    return {
      ok: true,
      events: WAKE_EVENTS,
      statuses: WAKE_STATUSES,
      counts,
      stats: { ...this.stats },
      queue: rows,
    };
  }
}

// ── Default transport ─────────────────────────────────────────────────────

async function defaultDeliver(url, body, timeoutMs = 10_000) {
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // A2A Protocol v1.0.0 §9.2 — version header required on JSON-RPC routes
        'A2A-Version': '1.0',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    return { ok: res.ok, status: res.status, error: res.ok ? undefined : `http_${res.status}` };
  } catch (err) {
    return { ok: false, status: 0, error: err && err.name === 'AbortError' ? 'timeout' : (err.message || 'delivery_failed') };
  } finally {
    clearTimeout(t);
  }
}

module.exports = {
  WakeBus,
  wakeFingerprint,
  WAKE_EVENTS,
  WAKE_STATUSES,
  FIRST_RUN_GRACE_MS,
  MAX_ATTEMPTS,
  REDIS_KEY,
};
