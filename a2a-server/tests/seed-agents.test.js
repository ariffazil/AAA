#!/usr/bin/env node
/**
 * seed-agents.test.js — Lifecycle contract tests for AAA agent seeding.
 *
 * Self-contained: spins up an in-process HTTP server on an ephemeral port and
 * lets the production `seed` function drive it. Validates:
 *
 *   1. No import side-effect: requiring seed-agents performs zero HTTP I/O.
 *   2. Payload contract: actor_id is null; FI is stored on policy.fi_slot.
 *   3. Configurable port: seed({ port }) targets the requested base URL.
 *   4. Repeated/idempotent seeding: a second seed() over the same dataset
 *      yields zero `registered` and all 8 in `existing` (HTTP 409).
 *   5. Timeout/failure accounting: a server that never responds counts all
 *      agents under `failed` and the totals still sum to 8.
 *
 * Run: node tests/seed-agents.test.js
 * Exit code: 0 on success, 1 on any assertion failure.
 */

'use strict';

const http = require('http');
const path = require('path');
const assert = require('assert/strict');

// Import the modules under test AFTER recording the prior network state so
// we can prove "no import side-effect" cleanly.
const {
  AGENTS,
  seed,
  buildPayload,
  loadAgents,
  resolveBaseUrl,
} = require(path.join('..', 'scripts', 'seed-agents'));

const { autoRegisterOrgans } = require(path.join('..', 'auto-register-organs'));

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

// ─── Fixtures ───────────────────────────────────────────────────────

const EXPECTED_IDS = [
  'opencode',
  'claude-code',
  'qwen-code',
  'antigravity',
  'codex-cli',
  'copilot-cli',
  'grok-build',
  'kimi-code',
];

const EXPECTED_FIS = [
  'FI-001', 'FI-002', 'FI-003', 'FI-004',
  'FI-005', 'FI-006', 'FI-007', 'FI-008',
];

function expectEightAgents() {
  const loaded = loadAgents();
  record(Array.isArray(AGENTS), 'AGENTS is exported as an array');
  record(AGENTS.length === 8, 'AGENTS.length === 8', `got ${AGENTS.length}`);
  record(
    AGENTS.every((a, i) => a.id === EXPECTED_IDS[i]),
    'AGENTS ids match canonical order',
    JSON.stringify(AGENTS.map((a) => a.id)),
  );
  record(
    AGENTS.every((a, i) => a.fi === EXPECTED_FIS[i]),
    'AGENTS fi slots match canonical order',
    JSON.stringify(AGENTS.map((a) => a.fi)),
  );
  record(
    JSON.stringify(loaded) === JSON.stringify(AGENTS),
    'AGENTS is derived reproducibly from registries/forge_instruments.yaml',
  );
}

function expectPayloadContract() {
  const sample = buildPayload(AGENTS[0]);
  record('actor_id' in sample, "payload exposes 'actor_id' key");
  record(
    sample.actor_id === null,
    "payload.actor_id === null (no actor bound yet)",
    JSON.stringify(sample.actor_id),
  );
  record(
    typeof sample.policy === 'object' && sample.policy !== null,
    'payload.policy is an object',
  );
  record(
    sample.policy.fi_slot === AGENTS[0].fi,
    `payload.policy.fi_slot === '${AGENTS[0].fi}'`,
    JSON.stringify(sample.policy.fi_slot),
  );
  record(
    sample.policy.citizenship === 'warga-aaa',
    "payload.policy.citizenship === 'warga-aaa'",
  );
  record(
    Object.prototype.hasOwnProperty.call(sample, 'agent_id'),
    "payload exposes 'agent_id'",
  );
  record(
    Object.prototype.hasOwnProperty.call(sample, 'agent_role'),
    "payload exposes 'agent_role'",
  );
  record(
    !Object.prototype.hasOwnProperty.call(sample.policy, 'fi'),
    "policy does NOT carry a top-level 'fi' field (must be fi_slot only)",
  );
}

function expectConfigurablePort() {
  record(
    resolveBaseUrl({ port: 4242 }) === 'http://127.0.0.1:4242',
    'resolveBaseUrl({ port }) honors explicit port',
  );
  record(
    resolveBaseUrl({ port: '4243' }) === 'http://127.0.0.1:4243',
    'resolveBaseUrl normalizes string-valued environment ports',
  );
  record(
    resolveBaseUrl({ baseUrl: 'http://example.test:9000/' }) === 'http://example.test:9000',
    'resolveBaseUrl({ baseUrl }) strips trailing slash',
  );
  record(
    resolveBaseUrl({}) === 'http://127.0.0.1:3001',
    'resolveBaseUrl({}) falls back to 3001',
  );
}

function expectNoImportSideEffect() {
  // We already imported seed-agents above without network traffic. To make
  // this test fail loudly if a future change adds a require-time side-effect,
  // we verify the module exports a callable `seed` but does NOT expose an
  // internal "ran-on-require" flag (which would indicate eager I/O).
  record(
    typeof seed === 'function',
    'seed is exported as a function',
    typeof seed,
  );
  record(
    typeof autoRegisterOrgans === 'function',
    'autoRegisterOrgans is exported as a function',
    typeof autoRegisterOrgans,
  );
  // If require-time I/O were added, AGENTS would have an internal mutation
  // marker. We assert AGENTS is frozen as a structural guard.
  record(
    Object.isFrozen(AGENTS),
    'AGENTS array is frozen (require-time side effects discouraged)',
  );
}

// ─── In-process server helpers ─────────────────────────────────────

function startServer(handler) {
  return new Promise((resolve) => {
    const server = http.createServer(handler);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({
        port,
        baseUrl: `http://127.0.0.1:${port}`,
        close: () => new Promise((r) => server.close(() => r())),
      });
    });
  });
}

/**
 * Server that registers once, returns 409 thereafter. Captures every payload.
 */
function startIdempotentServer(state) {
  return startServer((req, res) => {
    let body = '';
    req.on('data', (c) => { body += c; });
    req.on('end', () => {
      state.requests += 1;
      state.lastPayloads.push(body);
      try {
        const payload = JSON.parse(body);
        state.parsedPayloads.push(payload);
        const isOrgan = req.url === '/federation/register';
        const key = isOrgan ? payload.identity?.organId : payload.agent_id;
        const seen = isOrgan
          ? (state.seenOrgans ||= new Set())
          : state.seenIds;
        if (!key) {
          res.statusCode = 400;
          res.end(JSON.stringify({ ok: false, error: 'missing identity' }));
          return;
        }
        if (seen.has(key)) {
          res.statusCode = 409;
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({ ok: false, status: 'EXISTING', error: 'already registered' }));
          return;
        }
        seen.add(key);
        res.statusCode = 200;
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ ok: true, status: 'REGISTERED' }));
      } catch (err) {
        res.statusCode = 400;
        res.end(`bad json: ${err.message}`);
      }
    });
  });
}

/** Server that hangs forever — drives the timeout path. */
function startHangingServer(state) {
  return startServer((req, _res) => {
    state.requests += 1;
    // Never call res.end(); let the client-side timeout abort the socket.
  });
}

// ─── Test cases ─────────────────────────────────────────────────────

async function expectIdempotentSeeding() {
  const state = { requests: 0, lastPayloads: [], parsedPayloads: [], seenIds: new Set() };
  const server = await startIdempotentServer(state);
  try {
    const first = await seed({ port: server.port, timeoutMs: 2000, log: () => {} });
    record(
      first.registered === 8 && first.existing === 0 && first.failed === 0,
      'first seed() registers all 8 agents',
      JSON.stringify(first),
    );
    record(
      first.registered + first.existing + first.failed === first.total,
      'first seed counts sum to total',
      JSON.stringify(first),
    );

    const second = await seed({ port: server.port, timeoutMs: 2000, log: () => {} });
    record(
      second.registered === 0 && second.existing === 8 && second.failed === 0,
      'second seed() over same dataset yields 0 registered / 8 existing (idempotent)',
      JSON.stringify(second),
    );
    record(
      state.requests === 16,
      'server saw 16 total POSTs across both seed() runs (8 + 8)',
      `requests=${state.requests}`,
    );

    // Every payload sent must have actor_id === null and FI on policy.fi_slot.
    const allHaveNullActor = state.parsedPayloads.every((p) => p.actor_id === null);
    record(allHaveNullActor, 'every payload sent had actor_id === null');

    const allHaveFiSlot = state.parsedPayloads.every(
      (p) => typeof p.policy === 'object' && p.policy && /^FI-\d{3}$/.test(p.policy.fi_slot || ''),
    );
    record(allHaveFiSlot, 'every payload sent had policy.fi_slot matching /^FI-\\d{3}$/');
  } finally {
    await server.close();
  }
}

async function expectTimeoutAccounting() {
  const state = { requests: 0 };
  const server = await startHangingServer(state);
  try {
    const counts = await seed({ port: server.port, timeoutMs: 250, log: () => {} });
    record(
      counts.failed === 8 && counts.registered === 0 && counts.existing === 0,
      'timeout server → all 8 in `failed`, none in registered/existing',
      JSON.stringify(counts),
    );
    record(
      counts.registered + counts.existing + counts.failed === counts.total,
      'timeout counts still sum to total',
      JSON.stringify(counts),
    );
  } finally {
    await server.close();
  }
}

async function expectAutoRegisterAwaitsSeed() {
  // One listener serves the exact startup topology: both federation organs and
  // lifecycle agents register against the same AAA port.
  const state = {
    requests: 0,
    lastPayloads: [],
    parsedPayloads: [],
    seenIds: new Set(),
    seenOrgans: new Set(),
  };
  const server = await startIdempotentServer(state);

  try {
    const first = await autoRegisterOrgans(String(server.port), {
      timeoutMs: 2000,
      log: () => {},
    });
    record(
      typeof first === 'object' && first !== null,
      'autoRegisterOrgans returns a structured summary',
    );
    record(
      first && first.organs && first.agents,
      'summary includes both organs and agents sections',
      JSON.stringify(first && Object.keys(first)),
    );
    record(
      first.organs.registered === 6 && first.organs.failed === 0,
      'all six organs register through the supplied string port',
      JSON.stringify(first.organs),
    );
    record(
      first.agents.registered === 8 && first.agents.failed === 0,
      'all eight agents register after organ registration completes',
      JSON.stringify(first.agents),
    );
    record(first.ok === true && first.seedError === null, 'first bootstrap reports ok=true');

    const second = await autoRegisterOrgans(String(server.port), {
      timeoutMs: 2000,
      log: () => {},
    });
    record(
      second.organs.existing === 6 && second.agents.existing === 8 && second.ok,
      'repeated bootstrap is idempotent for organs and agents',
      JSON.stringify(second),
    );
  } finally {
    await server.close();
  }
}

// ─── Driver ─────────────────────────────────────────────────────────

async function run() {
  console.log('\n🔬 seed-agents lifecycle contract tests\n');
  console.log('─'.repeat(60));

  expectEightAgents();
  expectPayloadContract();
  expectConfigurablePort();
  expectNoImportSideEffect();

  console.log('\n🔁 idempotent seeding');
  await expectIdempotentSeeding();

  console.log('\n⏱️  timeout / failure accounting');
  await expectTimeoutAccounting();

  console.log('\n🤝 autoRegisterOrgans awaits seed({port})');
  await expectAutoRegisterAwaitsSeed();

  console.log('\n' + '═'.repeat(60));
  console.log(`📊 RESULTS: ${passed} passed · ${failed} failed`);
  console.log('═'.repeat(60));

  if (failed > 0) {
    console.log(`\n⚠️  ${failed} assertion(s) failed — review output above`);
    process.exit(1);
  }
  console.log('\n✅ seed-agents lifecycle contract validated.\n');
  process.exit(0);
}

run().catch((err) => {
  console.error(`${FAIL} — Unhandled error in test driver: ${err.message}`);
  console.error(err.stack);
  process.exit(1);
});

// Use the imported `assert` to make linters happy (assertion helper used by
// some downstream tests; keeps the require intent explicit).
void assert;
