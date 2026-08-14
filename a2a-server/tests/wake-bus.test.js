#!/usr/bin/env node
/**
 * wake-bus.test.js — Contract tests for the AAA Wake Bus (P1 public infrastructure).
 *
 * Self-contained: no network, no Redis, no NATS. The WakeBus runs with an
 * injectable transport so delivery outcomes are deterministic.
 *
 * Covers the Paperclip P1 patterns distilled in
 * doc/plans/2026-08-14-paperclip-semantic-map.md:
 *   1. Enqueue validation (5 event types, semantic reason mandatory)
 *   2. Fingerprint dedup sha256(actor+reason+target) with coalescing
 *   3. 15s first-run grace surface (constant exported; race guard documented)
 *   4. Exponential backoff (5s → 25s → 125s), max 3 attempts
 *   5. SABAR-RETRY: 3 consecutive failures, zero verdict-changing evidence →
 *      HOLD with reason. HOLD ≠ DROP — the wake stays readable.
 *   6. Delivery via A2A card endpoints.baseUrl (registry lookup)
 *   7. Queue snapshot shape (GET /api/wake/queue contract)
 *
 * Run: node tests/wake-bus.test.js
 * Exit code: 0 on success, 1 on any assertion failure.
 */

'use strict';

const path = require('path');
const assert = require('assert/strict');
const {
  WakeBus,
  wakeFingerprint,
  WAKE_EVENTS,
  FIRST_RUN_GRACE_MS,
  MAX_ATTEMPTS,
} = require(path.join('..', 'wake_bus'));

const PASS = '✅ PASS';
const FAIL = '❌ FAIL';
let passed = 0;
let failed = 0;

function record(condition, label, detail) {
  if (condition) {
    console.log(`${PASS} — ${label}`);
    passed += 1;
  } else {
    console.log(`${FAIL} — ${label}${detail ? `\n       ${detail}` : ''}`);
    failed += 1;
  }
}

function newBus(deliverFn, cardRegistry) {
  return new WakeBus({
    redisClient: null,
    cardRegistry: cardRegistry || null,
    deliverFn,
    autoStart: false, // tests drive ticks manually
  });
}

(async function main() {
  // ─── 1. Event taxonomy ───────────────────────────────────────────────

  record(
    WAKE_EVENTS.length === 5
      && WAKE_EVENTS.includes('assignment_created')
      && WAKE_EVENTS.includes('comment_added')
      && WAKE_EVENTS.includes('upstream_complete')
      && WAKE_EVENTS.includes('budget_changed')
      && WAKE_EVENTS.includes('citizen_stalled'),
    'event taxonomy: exactly the 5 canonical wake events',
    JSON.stringify(WAKE_EVENTS),
  );

  // ─── 2. Validation ───────────────────────────────────────────────────

  {
    const bus = newBus(async () => ({ ok: true, status: 200 }));
    const bad = bus.validateEnqueue({ actor: '', event: 'nope', reason: '' });
    record(bad.valid === false && bad.errors.length >= 3, 'validation rejects empty actor/event/reason');

    const stallNoTarget = bus.validateEnqueue({ actor: 'opencode', event: 'citizen_stalled', reason: 'idle 30m' });
    record(
      stallNoTarget.valid === false && stallNoTarget.errors.some((e) => e.includes('citizen_stalled')),
      'citizen_stalled requires a target',
    );

    const good = bus.validateEnqueue({ actor: 'opencode', event: 'comment_added', reason: 'F13 replied on PR 42', target: 'pr-42' });
    record(good.valid === true, 'valid envelope passes');
  }

  // ─── 3. Enqueue + dedup fingerprint ──────────────────────────────────

  {
    const bus = newBus(async () => ({ ok: true, status: 200 }));
    const first = await bus.enqueue({ actor: 'opencode', event: 'comment_added', reason: 'F13 replied', target: 'issue-7' });
    record(first.accepted === true && typeof first.id === 'string' && first.wake.status === 'queued', 'enqueue accepted → queued');

    const dup = await bus.enqueue({ actor: 'opencode', event: 'comment_added', reason: 'F13 replied', target: 'issue-7' });
    record(dup.accepted === true && dup.deduped === true && dup.coalescedId === first.id, 'identical fingerprint dedupes + coalesces');

    const other = await bus.enqueue({ actor: 'opencode', event: 'comment_added', reason: 'F13 replied AGAIN', target: 'issue-7' });
    record(other.accepted === true && other.deduped !== true && other.id !== first.id, 'different reason → new wake (no false dedup)');

    const fp = wakeFingerprint('opencode', 'F13 replied', 'issue-7');
    record(
      fp.startsWith('wake:') && fp.length === 69 && fp === wakeFingerprint('opencode', 'F13 replied', 'issue-7'),
      'fingerprint = sha256(actor+reason+target), deterministic, namespaced',
    );
    record(first.wake.fingerprint === fp, 'enqueued wake carries its fingerprint');

    // target is part of identity: same reason, different target → distinct wake
    const t2 = await bus.enqueue({ actor: 'opencode', event: 'comment_added', reason: 'F13 replied', target: 'issue-8' });
    record(t2.accepted === true && t2.id !== first.id && t2.wake.fingerprint !== fp, 'target is fingerprinted (same actor+reason, other target ≠ dedup)');

    const invalid = await bus.enqueue({ actor: 'x', event: 'bogus', reason: '' });
    record(invalid.accepted === false && Array.isArray(invalid.errors), 'invalid enqueue rejected with error list');
  }

  // ─── 4. Delivery: happy path via A2A card URL ────────────────────────

  {
    const deliveries = [];
    const registry = { get: (id) => (id === 'opencode' ? { endpoints: { baseUrl: 'http://127.0.0.1:19999/' } } : null) };
    const bus = newBus(async (url, body) => {
      deliveries.push({ url, body });
      return { ok: true, status: 200 };
    }, registry);

    const enq = await bus.enqueue({ actor: 'opencode', event: 'assignment_created', reason: 'task routed by AREP', target: 'task-1' });
    const n = await bus.tick();
    record(n === 1, 'tick delivers one due wake');
    record(deliveries[0].url === 'http://127.0.0.1:19999/a2a/message/send', 'delivery URL = peer base + /a2a/message/send');
    const sent = deliveries[0].body;
    record(
      sent.jsonrpc === '2.0' && sent.method === 'message/send' && sent.params?.message?.parts?.length === 2,
      'delivery body is A2A JSON-RPC message/send (text + data parts)',
    );
    const dataPart = (sent.params.message.parts || []).find((p) => p.type === 'data');
    record(
      dataPart && dataPart.data.wake.event === 'assignment_created' && dataPart.data.wake.reason === 'task routed by AREP',
      'data part carries the wake (event + semantic reason + fingerprint)',
    );
    const got = bus.getWake(enq.id);
    record(got.status === 'delivered' && got.attempts === 1 && got.consecutiveFailures === 0, 'delivered on first attempt, failure counter reset');

    // AAA-hosted card (.../a2a/<agent>) routes to the gateway's canonical ingress
    const hostedReg = { get: () => ({ endpoints: { baseUrl: 'https://aaa.arif-fazil.com/a2a/opencode' } }) };
    const hostedDeliveries = [];
    const busHosted2 = new WakeBus({
      redisClient: null,
      cardRegistry: hostedReg,
      deliverFn: async (url) => { hostedDeliveries.push(url); return { ok: true, status: 200 }; },
      autoStart: false,
    });
    await busHosted2.enqueue({ actor: 'opencode', event: 'comment_added', reason: 'F13 replied', target: 'pr-1' });
    await busHosted2.tick();
    record(
      hostedDeliveries[0] === 'https://aaa.arif-fazil.com/a2a/message/send',
      'AAA-hosted card resolves to canonical ingress /a2a/message/send (public host kept when no rewrite fn)',
    );

    // With the production loopback rewrite (server.js wiring), the same card delivers on 127.0.0.1
    const localDeliveries = [];
    const busLocal = new WakeBus({
      redisClient: null,
      cardRegistry: hostedReg,
      deliverFn: async (url) => { localDeliveries.push(url); return { ok: true, status: 200 }; },
      autoStart: false,
      resolveSelfBase: (h) => (h === 'aaa.arif-fazil.com' ? 'http://127.0.0.1:3001' : null),
    });
    await busLocal.enqueue({ actor: 'opencode', event: 'comment_added', reason: 'F13 replied', target: 'pr-1' });
    await busLocal.tick();
    record(
      localDeliveries[0] === 'http://127.0.0.1:3001/a2a/message/send',
      'self-host rewrite: public card host → loopback ingress (loopback-only auth)',
    );

    // Unknown actor → no card → no_delivery_url failure path
    const ghostBus = newBus(async () => ({ ok: false, status: 503, error: 'http_503' }));
    const ghost = await ghostBus.enqueue({ actor: 'ghost-agent', event: 'budget_changed', reason: 'FLAME budget exhausted' });
    await ghostBus.tick();
    const ghostWake = ghostBus.getWake(ghost.id);
    record(ghostWake.status === 'retrying' && /no_delivery_url/.test(ghostWake.lastError || ''), 'missing card → retrying with no_delivery_url (HOLD after 3)');
  }

  // ─── 5. Backoff curve + SABAR-RETRY HOLD ─────────────────────────────

  {
    const bus = newBus(async () => ({ ok: false, status: 503, error: 'http_503' }));
    record(bus.backoffMs(1) === 5_000 && bus.backoffMs(2) === 25_000 && bus.backoffMs(3) === 125_000, 'exponential backoff 5s/25s/125s');

    const enq = await bus.enqueue({ actor: 'qwen-code', event: 'upstream_complete', reason: 'blocker task-0 sealed', target: 'task-2' });
    const wake0 = bus.getWake(enq.id);

    let now = Date.parse(wake0.createdAt);
    await bus.tick(now); // attempt 1
    let w = bus.getWake(enq.id);
    record(w.status === 'retrying' && w.attempts === 1 && w.nextAttemptAt === now + 5_000, 'attempt 1 failure → retrying @ +5s');

    await bus.tick(now + 5_000); // attempt 2
    w = bus.getWake(enq.id);
    record(w.status === 'retrying' && w.attempts === 2 && w.nextAttemptAt === now + 5_000 + 25_000, 'attempt 2 failure → retrying @ +25s');

    await bus.tick(now + 30_000); // attempt 3
    w = bus.getWake(enq.id);
    record(
      w.status === 'held' && w.attempts === 3 && /sabar_retry/.test(w.holdReason || '') && w.consecutiveFailures === 3,
      'attempt 3 failure → SABAR HOLD with reason (not dropped)',
    );

    // Held wake never retried, but stays readable — HOLD ≠ DROP
    const dueAgain = await bus.tick(now + 1_000_000);
    record(dueAgain === 0 && bus.getWake(enq.id).status === 'held', 'held wake is terminal for the bus but still inspectable');

    const view = bus.queueView();
    record(view.counts.held >= 1 && view.queue.some((x) => x.id === enq.id), 'queue view lists held wakes for operator display');
  }

  // ─── 6. Evidence resets SABAR counter ────────────────────────────────

  {
    const bus = newBus(async () => ({ ok: false, status: 500, error: 'http_500' }));
    const enq = await bus.enqueue({ actor: 'kimi-code', event: 'comment_added', reason: 'review requested', target: 'issue-9' });
    const t0 = Date.parse(bus.getWake(enq.id).createdAt);
    await bus.tick(t0); // 1 failure
    bus.recordEvidence(enq.id, 'operator_nudge'); // verdict-changing evidence arrives
    const w = bus.getWake(enq.id);
    record(w.consecutiveFailures === 0, 'operator evidence resets consecutive-failure counter');

    await bus.tick(t0 + 10_000); // attempt 2
    await bus.tick(t0 + 100_000); // attempt 3
    const w3 = bus.getWake(enq.id);
    // evidence reset means SABAR counter never reached 3 in a row before attempts cap — attempts cap (3) still HOLDs
    record(w3.status === 'held' && w3.consecutiveFailures === 2, 'attempts cap (3) still holds even with mid-flight evidence; counter honest');
  }

  // ─── 7. First-run grace constants (Paperclip 15s twin) ───────────────

  record(FIRST_RUN_GRACE_MS === 15_000, 'first-run grace = 15s (Paperclip TASK_WATCHDOG_FIRST_RUN_GRACE_MS twin)');
  record(MAX_ATTEMPTS === 3, 'max delivery attempts = 3 (SABAR-RETRY bound)');

  // ─── 8. Queue view contract (GET /api/wake/queue shape) ──────────────

  {
    const bus = newBus(async () => ({ ok: true, status: 200 }));
    await bus.enqueue({ actor: 'a', event: 'budget_changed', reason: 'r1' });
    await bus.enqueue({ actor: 'b', event: 'comment_added', reason: 'r2', target: 't2' });
    await bus.enqueue({ actor: 'b', event: 'comment_added', reason: 'r2', target: 't2' }); // dedup
    const view = bus.queueView();
    record(view.ok === true && Array.isArray(view.events) && Array.isArray(view.statuses) && typeof view.counts === 'object',
      'queue view: ok + events + statuses + counts');
    record(view.stats.enqueued === 2 && view.stats.deduped === 1, 'stats track enqueued (new only) / deduped');
    record(view.queue.length === 2, 'queue lists live wakes (deduped one coalesced, not duplicated)');
    const filtered = bus.queueView({ actor: 'b' });
    record(filtered.queue.length === 1 && filtered.queue[0].actor === 'b', 'queue filter by actor');
  }

  // ─── 9. Hydration: restart with in-flight wakes ──────────────────────

  {
    const store = new Map(); // fake Redis hSet/hGetAll
    const fakeRedis = {
      isOpen: true,
      async hSet(_k, id, raw) { store.set(id, raw); },
      async hGetAll() { return Object.fromEntries(store); },
      async zAdd() { return 1; },
    };
    const bus = new WakeBus({
      redisClient: fakeRedis,
      deliverFn: async () => ({ ok: false, status: 0, error: 'crash mid-flight simulation' }),
      autoStart: false,
    });
    const enq = await bus.enqueue({ actor: 'claude-code', event: 'upstream_complete', reason: 'forge done', target: 'task-3' });
    await bus.tick(Date.now());
    record(bus.getWake(enq.id).status === 'retrying', 'pre-restart wake persisted as retrying');

    // Simulate restart: fresh bus, same Redis, wake was 'delivering' at death
    store.set(enq.id, JSON.stringify({ ...JSON.parse(store.get(enq.id)), status: 'delivering' }));
    const bus2 = new WakeBus({
      redisClient: fakeRedis,
      deliverFn: async () => ({ ok: true, status: 200 }),
      autoStart: false,
    });
    const restored = await bus2.hydrate();
    const w = bus2.getWake(enq.id);
    record(restored === 1 && w.status === 'queued', 'hydrate restores mid-flight wake as queued');
  }

  // ─── Summary ─────────────────────────────────────────────────────────

  console.log(`\n${passed} passed, ${failed} failed`);
  if (failed > 0) process.exit(1);

})().catch((err) => { console.error(err); process.exit(1); });
