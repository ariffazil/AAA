#!/usr/bin/env node
/**
 * auto-register-organs.test.js — Bounded readiness fetch contract tests
 *
 * Self-contained: spins up an in-process HTTP server on an ephemeral port
 * and validates that probeReadiness + probeReadinessWithRetry honour:
 *
 *   1. explicit timeout (AbortController) — never hangs
 *   2. linear retry/backoff — bounded number of attempts
 *   3. structured result — { reachable, latencyMs, status, error, attempts }
 *   4. autoRegisterOrgans skips register when readiness probe fails
 *
 * Run: node tests/auto-register-organs.test.js
 * Exit code: 0 on success, 1 on any assertion failure.
 */

'use strict';

const http = require('http');
const path = require('path');
const assert = require('assert/strict');

const {
  probeReadiness,
  probeReadinessWithRetry,
  autoRegisterOrgans,
  ORGANS,
} = require(path.join('..', 'auto-register-organs'));

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

// ─── In-process fixture HTTP server ─────────────────────────────────

function startFixture(handler) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => handler(req, res));
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, port });
    });
  });
}

function stopFixture(server) {
  return new Promise((resolve) => server.close(resolve));
}

// ─── 1. probeReadiness — explicit timeout ──────────────────────────

async function testProbeTimeout() {
  // Server that NEVER responds.
  const { server, port } = await startFixture((req, res) => {
    // hold the socket open forever
  });
  try {
    const result = await probeReadiness(`http://127.0.0.1:${port}/health`, 200);
    record(
      result.reachable === false && /timeout after 200ms/.test(result.error || ''),
      'probeReadiness: times out within 200ms and returns reachable=false',
      JSON.stringify(result),
    );
    record(
      result.latencyMs >= 200 && result.latencyMs < 500,
      'probeReadiness: latencyMs roughly matches timeout (not blocked forever)',
      `latencyMs=${result.latencyMs}`,
    );
  } finally {
    await stopFixture(server);
  }
}

// ─── 2. probeReadiness — reachable path ─────────────────────────────

async function testProbeSuccess() {
  const { server, port } = await startFixture((req, res) => {
    res.statusCode = 200;
    res.setHeader('content-type', 'application/json');
    res.end('{"status":"green"}');
  });
  try {
    const result = await probeReadiness(`http://127.0.0.1:${port}/health`, 1000);
    record(
      result.reachable === true && result.status === 200,
      'probeReadiness: 200 OK → reachable=true, status=200',
      JSON.stringify(result),
    );
    record(
      typeof result.latencyMs === 'number' && result.latencyMs >= 0,
      'probeReadiness: latencyMs is a non-negative number',
      `latencyMs=${result.latencyMs}`,
    );
  } finally {
    await stopFixture(server);
  }
}

// ─── 3. probeReadinessWithRetry — bounded retries + backoff ─────────

async function testRetryBounded() {
  // Always-down server (responds 500 — fetch treats that as !ok).
  const { server, port } = await startFixture((req, res) => {
    res.statusCode = 500;
    res.end('down');
  });
  try {
    const started = Date.now();
    const result = await probeReadinessWithRetry(
      `http://127.0.0.1:${port}/health`,
      100, // tight timeout per attempt
      { maxAttempts: 3, backoffMs: 50 },
    );
    const elapsed = Date.now() - started;
    record(
      result.reachable === false && result.attempts === 3,
      'probeReadinessWithRetry: stops after maxAttempts and reports attempts=3',
      JSON.stringify(result),
    );
    // 3 attempts, each responds immediately with 500, plus linear backoff
    // (50ms + 100ms).  Total expected: ~150-300ms; cap generously at 5s.
    record(
      elapsed >= 100 && elapsed < 5000,
      `probeReadinessWithRetry: total elapsed (${elapsed}ms) honours the bounded budget`,
      `elapsed=${elapsed}ms`,
    );
  } finally {
    await stopFixture(server);
  }
}

// ─── 4. probeReadinessWithRetry — eventually reachable ──────────────

async function testRetryEventualSuccess() {
  let hits = 0;
  const { server, port } = await startFixture((req, res) => {
    hits += 1;
    if (hits < 2) {
      res.statusCode = 503;
      res.end('warming');
    } else {
      res.statusCode = 200;
      res.end('{"status":"green"}');
    }
  });
  try {
    const result = await probeReadinessWithRetry(
      `http://127.0.0.1:${port}/health`,
      500,
      { maxAttempts: 5, backoffMs: 50 },
    );
    record(
      result.reachable === true && result.attempts === 2,
      'probeReadinessWithRetry: succeeds on 2nd attempt and reports attempts=2',
      JSON.stringify(result),
    );
  } finally {
    await stopFixture(server);
  }
}

// ─── 5. autoRegisterOrgans — readiness failure skips register ───────

async function testAutoRegisterSkipsOnUnreachableOrgan() {
  // AAA endpoint accepts registrations; /health probes always fail.
  // We inject a custom ORGANS list that targets the fixture port so we
  // don't accidentally hit the live federation organs on this VPS.
  const { server, port } = await startFixture((req, res) => {
    if (req.method === 'POST' && req.url === '/federation/register') {
      // Count registration attempts — should be ZERO for unreachable organ.
      let body = '';
      req.on('data', (chunk) => { body += chunk; });
      req.on('end', () => {
        // Try to recognise an organ JSON for nicer test output.
        let parsed = {};
        try { parsed = JSON.parse(body); } catch (_e) { /* ignore */ }
        globalThis.__registerHits = (globalThis.__registerHits || 0) + 1;
        globalThis.__registerLog = (globalThis.__registerLog || []).concat(
          [parsed && parsed.identity && parsed.identity.organId],
        );
        res.statusCode = 200;
        res.setHeader('content-type', 'application/json');
        res.end(JSON.stringify({ ok: true, handshake: { stage: 'REGISTERED', stages: [] } }));
      });
      return;
    }
    // All /health probes fail.
    res.statusCode = 502;
    res.end('bad gateway');
  });
  globalThis.__registerHits = 0;
  globalThis.__registerLog = [];
  // Build a stub ORGANS list that targets THIS fixture for both /health and /register.
  const stubOrgans = [
    Object.freeze({
      identity: Object.freeze({ organId: 'fixture-a', name: 'Fixture A', role: 'execution' }),
      endpoints: Object.freeze({
        healthUrl: `http://127.0.0.1:${port}/health`,
        mcpUrl: `http://127.0.0.1:${port}/mcp`,
      }),
      skills: Object.freeze([
        Object.freeze({ id: 'noop', name: 'Noop', description: 'noop' }),
      ]),
    }),
    Object.freeze({
      identity: Object.freeze({ organId: 'fixture-b', name: 'Fixture B', role: 'execution' }),
      endpoints: Object.freeze({
        healthUrl: `http://127.0.0.1:${port}/health`,
        mcpUrl: `http://127.0.0.1:${port}/mcp`,
      }),
      skills: Object.freeze([
        Object.freeze({ id: 'noop', name: 'Noop', description: 'noop' }),
      ]),
    }),
  ];
  try {
    const summary = await autoRegisterOrgans(port, {
      timeoutMs: 150,
      readinessMaxAttempts: 2,
      readinessBackoffMs: 25,
      organs: stubOrgans,
      log: () => {}, // silent
    });
    record(
      summary.organs.failed === stubOrgans.length,
      `autoRegisterOrgans: every organ marked failed when readiness is unreachable (${summary.organs.failed}/${stubOrgans.length})`,
      JSON.stringify(summary.organs),
    );
    record(
      globalThis.__registerHits === 0,
      'autoRegisterOrgans: NO /federation/register calls were issued when readiness probe failed',
      `register hits=${globalThis.__registerHits}`,
    );
  } finally {
    await stopFixture(server);
  }
}

// ─── 6. autoRegisterOrgans — bounded time budget ────────────────────

async function testAutoRegisterTotalBudgetBounded() {
  // Slow organ: /health responds after 400ms (just above the tight timeout).
  const { server, port } = await startFixture((req, res) => {
    if (req.url === '/federation/register') {
      let body = '';
      req.on('data', (chunk) => { body += chunk; });
      req.on('end', () => {
        res.statusCode = 409;
        res.end(JSON.stringify({ status: 'EXISTING' }));
      });
      return;
    }
    setTimeout(() => {
      res.statusCode = 200;
      res.end('{"status":"green"}');
    }, 400);
  });
  const stubOrgans = [
    Object.freeze({
      identity: Object.freeze({ organId: 'slow-a', name: 'Slow A', role: 'execution' }),
      endpoints: Object.freeze({
        healthUrl: `http://127.0.0.1:${port}/health`,
        mcpUrl: `http://127.0.0.1:${port}/mcp`,
      }),
      skills: Object.freeze([Object.freeze({ id: 'noop', name: 'Noop', description: 'noop' })]),
    }),
    Object.freeze({
      identity: Object.freeze({ organId: 'slow-b', name: 'Slow B', role: 'execution' }),
      endpoints: Object.freeze({
        healthUrl: `http://127.0.0.1:${port}/health`,
        mcpUrl: `http://127.0.0.1:${port}/mcp`,
      }),
      skills: Object.freeze([Object.freeze({ id: 'noop', name: 'Noop', description: 'noop' })]),
    }),
  ];
  try {
    const started = Date.now();
    const summary = await autoRegisterOrgans(port, {
      timeoutMs: 150,
      readinessMaxAttempts: 1,
      readinessBackoffMs: 25,
      organs: stubOrgans,
      log: () => {},
    });
    const elapsed = Date.now() - started;
    record(
      elapsed < 10_000,
      `autoRegisterOrgans: total elapsed (${elapsed}ms) stays within bounded budget`,
      `elapsed=${elapsed}ms`,
    );
    // With readinessMaxAttempts=1 and timeout=150ms, /health returns 200 after 400ms
    // → first attempt times out → readiness fails → organ marked failed.
    // (Fixture POST returns 409 only when reached, but readiness failed first.)
    record(
      summary.organs.failed === stubOrgans.length,
      'autoRegisterOrgans: slow /health forces every organ to fail (bounded timeout honored)',
      JSON.stringify(summary.organs),
    );
  } finally {
    await stopFixture(server);
  }
}

// ─── Runner ─────────────────────────────────────────────────────────

(async () => {
  try {
    await testProbeTimeout();
    await testProbeSuccess();
    await testRetryBounded();
    await testRetryEventualSuccess();
    await testAutoRegisterSkipsOnUnreachableOrgan();
    await testAutoRegisterTotalBudgetBounded();
  } catch (err) {
    record(false, 'runner', err.stack || err.message);
  }
  console.log(`\n${passed} passed, ${failed} failed`);
  process.exit(failed === 0 ? 0 : 1);
})();
