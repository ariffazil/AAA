/**
 * Auto-register federation organs on AAA startup.
 * Called after server.listen() — probes each organ's health, then registers.
 *
 * Lifecycle contract:
 *   - CommonJS export: { autoRegisterOrgans, ORGANS }
 *   - autoRegisterOrgans awaits seed({ port }) from ./scripts/seed-agents.
 *   - seed import is side-effect free: no I/O fires on require alone.
 *   - No hardcoded bearer token. Organ registration trusts the localhost
 *     boundary; if AAA_AUTH_TOKEN env is set, it is forwarded (set inside
 *     seed-agents, never here).
 *   - Returns structured counts { organs: { registered, existing, failed, total },
 *     agents: { registered, existing, failed, total }, ok, startedAt, finishedAt }.
 */

'use strict';

const { AGENTS, seed } = require('./scripts/seed-agents');

const ORGANS = Object.freeze([
  Object.freeze({
    identity: Object.freeze({ organId: 'arifos', name: 'arifOS Constitutional Kernel', role: 'governance' }),
    endpoints: Object.freeze({ healthUrl: 'http://127.0.0.1:8088/health', mcpUrl: 'http://127.0.0.1:8088/mcp' }),
    skills: Object.freeze([
      Object.freeze({ id: 'session_init', name: 'Session Init', description: 'Constitutional session binding' }),
      Object.freeze({ id: 'judge', name: 'Judge', description: 'Constitutional verdict' }),
      Object.freeze({ id: 'vault_seal', name: 'Vault Seal', description: 'Immutable ledger append' }),
      Object.freeze({ id: 'route', name: 'Route', description: 'Intent routing to organs' }),
    ]),
  }),
  Object.freeze({
    identity: Object.freeze({ organId: 'aforge', name: 'A-FORGE Execution Shell', role: 'execution' }),
    endpoints: Object.freeze({ healthUrl: 'http://127.0.0.1:7071/health', mcpUrl: 'http://127.0.0.1:7072/mcp' }),
    skills: Object.freeze([
      Object.freeze({ id: 'forge_execute', name: 'Forge Execute', description: 'Code execution' }),
      Object.freeze({ id: 'forge_shell', name: 'Forge Shell', description: 'Governed shell' }),
      Object.freeze({ id: 'forge_git', name: 'Forge Git', description: 'Git operations' }),
    ]),
  }),
  Object.freeze({
    identity: Object.freeze({ organId: 'geox', name: 'GEOX Earth Intelligence', role: 'evidence' }),
    endpoints: Object.freeze({ healthUrl: 'http://127.0.0.1:8081/health', mcpUrl: 'http://127.0.0.1:8081/mcp/' }),
    skills: Object.freeze([
      Object.freeze({ id: 'basin_resolve', name: 'Basin Resolve', description: 'Basin analysis' }),
      Object.freeze({ id: 'seismic_compute', name: 'Seismic Compute', description: 'Seismic physics' }),
      Object.freeze({ id: 'petrophysics', name: 'Petrophysics', description: 'Well log analysis' }),
    ]),
  }),
  Object.freeze({
    identity: Object.freeze({ organId: 'wealth', name: 'WEALTH Capital Intelligence', role: 'capital' }),
    endpoints: Object.freeze({ healthUrl: 'http://127.0.0.1:18082/health', mcpUrl: 'http://127.0.0.1:18082/mcp' }),
    skills: Object.freeze([
      Object.freeze({ id: 'emv', name: 'EMV', description: 'Expected monetary value' }),
      Object.freeze({ id: 'monte_carlo', name: 'Monte Carlo', description: 'Simulation' }),
      Object.freeze({ id: 'conservation', name: 'Conservation', description: 'Capital conservation' }),
    ]),
  }),
  Object.freeze({
    identity: Object.freeze({ organId: 'well', name: 'WELL Human Readiness', role: 'vitality' }),
    endpoints: Object.freeze({ healthUrl: 'http://127.0.0.1:18083/health', mcpUrl: 'http://127.0.0.1:18083/mcp' }),
    skills: Object.freeze([
      Object.freeze({ id: 'readiness', name: 'Readiness', description: 'Human readiness check' }),
      Object.freeze({ id: 'vitality', name: 'Vitality', description: 'Vitality validation' }),
      Object.freeze({ id: 'dignity', name: 'Dignity', description: 'Dignity guard' }),
    ]),
  }),
  Object.freeze({
    identity: Object.freeze({ organId: 'openclaw', name: 'OpenClaw Agentic Coder', role: 'orchestration' }),
    endpoints: Object.freeze({ healthUrl: 'http://127.0.0.1:18789/health', mcpUrl: 'ws://127.0.0.1:18789' }),
    skills: Object.freeze([
      Object.freeze({ id: 'agent_spawn', name: 'Agent Spawn', description: 'Spawn coding agents' }),
      Object.freeze({ id: 'cron', name: 'Cron', description: 'Scheduled tasks' }),
      Object.freeze({ id: 'telegram', name: 'Telegram', description: 'Messaging channel' }),
    ]),
  }),
]);

async function registerOneOrgan(baseUrl, organ, timeoutMs) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const resp = await fetch(`${baseUrl}/federation/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(organ),
      signal: ctrl.signal,
    });
    const text = await resp.text();
    let result = {};
    try {
      result = text ? JSON.parse(text) : {};
    } catch (_parseErr) {
      result = { ok: false, error: 'invalid_json', detail: text.slice(0, 200) };
    }
    return {
      status: resp.status,
      ok: resp.ok || result.ok === true || result.status === 'EXISTING',
      existing: result.status === 'EXISTING' || resp.status === 409,
      error: result.error || null,
      detail: result.detail || null,
    };
  } catch (err) {
    const aborted = err && err.name === 'AbortError';
    return {
      status: 0,
      ok: false,
      existing: false,
      error: aborted ? `timeout after ${timeoutMs}ms` : err.message,
      detail: null,
    };
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Bounded readiness probe — GETs an organ's /health with timeout.
 * Returns `{ reachable, latencyMs, status, error }`.  Never throws.
 *
 * Used before registerOneOrgan so a half-up organ doesn't waste a
 * registration attempt.  Bounded with AbortController + bounded
 * timeoutMs; no request-path retry here (handled at caller layer).
 */
async function probeReadiness(healthUrl, timeoutMs) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  const started = Date.now();
  try {
    const resp = await fetch(healthUrl, { signal: ctrl.signal });
    return {
      reachable: resp.ok,
      latencyMs: Date.now() - started,
      status: resp.status,
      error: null,
    };
  } catch (err) {
    const aborted = err && err.name === 'AbortError';
    return {
      reachable: false,
      latencyMs: Date.now() - started,
      status: 0,
      error: aborted ? `timeout after ${timeoutMs}ms` : err.message,
    };
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Bounded retry loop for the readiness probe.  Uses linear backoff so a
 * slow-boot organ still gets a fair chance without stretching the boot
 * budget.  Caps total attempts; returns the LAST probe result.
 */
async function probeReadinessWithRetry(healthUrl, timeoutMs, opts) {
  const maxAttempts = (opts && Number.isInteger(opts.maxAttempts)) ? opts.maxAttempts : 3;
  const backoffMs = (opts && Number.isInteger(opts.backoffMs)) ? opts.backoffMs : 500;
  let last = { reachable: false, status: 0, latencyMs: 0, error: 'no-attempt' };
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    last = await probeReadiness(healthUrl, timeoutMs);
    if (last.reachable) {
      last.attempts = attempt;
      return last;
    }
    if (attempt < maxAttempts) {
      await new Promise((resolve) => setTimeout(resolve, backoffMs * attempt));
    }
  }
  last.attempts = maxAttempts;
  return last;
}

/**
 * Probe each organ, register it, then seed the 8 forge instruments.
 * Always returns a structured counts object — never throws to the caller.
 *
 * Readiness is bounded: each /health probe uses an AbortController with
 * `timeoutMs`, and the probe retries at most `readinessMaxAttempts`
 * times with linear backoff before registering.  Registration itself
 * uses the same per-call timeout.  All timeouts are explicit; no
 * unbounded waits.
 */
async function autoRegisterOrgans(port = 3001, opts) {
  const parsedPort = Number.parseInt(String(port), 10);
  const normalizedPort = Number.isInteger(parsedPort) && parsedPort > 0 ? parsedPort : 3001;
  const baseUrl = `http://127.0.0.1:${normalizedPort}`;
  const timeoutMs = (opts && Number.isInteger(opts.timeoutMs)) ? opts.timeoutMs : 5000;
  const readinessMaxAttempts = (opts && Number.isInteger(opts.readinessMaxAttempts))
    ? opts.readinessMaxAttempts
    : 3;
  const readinessBackoffMs = (opts && Number.isInteger(opts.readinessBackoffMs))
    ? opts.readinessBackoffMs
    : 500;
  // Allow tests / power-users to inject a custom ORGANS list.
  const organsToRegister = (opts && Array.isArray(opts.organs)) ? opts.organs : ORGANS;
  const startedAt = new Date().toISOString();
  const log = (opts && typeof opts.log === 'function') ? opts.log : () => {};

  const organCounts = { registered: 0, existing: 0, failed: 0, total: organsToRegister.length };

  for (const organ of organsToRegister) {
    // Bounded readiness probe (timeout + bounded retry + backoff).
    const readiness = await probeReadinessWithRetry(
      organ.endpoints.healthUrl,
      timeoutMs,
      { maxAttempts: readinessMaxAttempts, backoffMs: readinessBackoffMs },
    );
    if (!readiness.reachable) {
      organCounts.failed += 1;
      log(
        `[auto-register] ❌ ${organ.identity.organId}: readiness probe failed ` +
        `(attempts=${readiness.attempts}, ${readiness.error || `HTTP ${readiness.status}`})`,
      );
      continue;
    }
    const result = await registerOneOrgan(baseUrl, organ, timeoutMs);
    if (result.ok && result.existing) {
      organCounts.existing += 1;
      log(`[auto-register] ↻ ${organ.identity.organId} — already registered`);
    } else if (result.ok) {
      organCounts.registered += 1;
      log(`[auto-register] ✅ ${organ.identity.organId} — registered`);
    } else {
      organCounts.failed += 1;
      const detail = result.detail ? ` — ${result.detail}` : '';
      log(`[auto-register] ❌ ${organ.identity.organId}: ${result.error || `HTTP ${result.status}`}${detail}`);
    }
  }

  log(
    `[auto-register] organs: ${organCounts.registered} registered · ` +
    `${organCounts.existing} existing · ${organCounts.failed} failed · ` +
    `${organCounts.total} total`,
  );

  // Seed 8 forge instruments into agent lifecycle manager.
  // Explicitly await seed({ port }) so caller observes completion.
  let agentCounts = {
    registered: 0,
    existing: 0,
    failed: AGENTS.length,
    total: AGENTS.length,
  };
  let seedError = null;
  try {
    agentCounts = await seed({ port: normalizedPort, timeoutMs, log });
  } catch (err) {
    seedError = err.message;
    log(`[auto-register] forge agent seeding failed: ${seedError}`);
  }

  const finishedAt = new Date().toISOString();
  return {
    organs: organCounts,
    agents: agentCounts,
    ok: seedError === null && organCounts.failed === 0 && agentCounts.failed === 0,
    startedAt,
    finishedAt,
    seedError,
  };
}

// Side-effect guard: only run when invoked as a CLI, never on require.
if (require.main === module) {
  const argv = process.argv.slice(2);
  let cliPort = 3001;
  let cliTimeoutMs = 5000;
  let cliReadinessMaxAttempts = 3;
  let cliReadinessBackoffMs = 500;
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (flag === '--port' && i + 1 < argv.length) {
      const parsed = Number.parseInt(argv[i + 1], 10);
      if (Number.isInteger(parsed)) cliPort = parsed;
      i += 1;
    } else if (flag === '--timeout-ms' && i + 1 < argv.length) {
      const parsed = Number.parseInt(argv[i + 1], 10);
      if (Number.isInteger(parsed)) cliTimeoutMs = parsed;
      i += 1;
    } else if (flag === '--readiness-max-attempts' && i + 1 < argv.length) {
      const parsed = Number.parseInt(argv[i + 1], 10);
      if (Number.isInteger(parsed)) cliReadinessMaxAttempts = parsed;
      i += 1;
    } else if (flag === '--readiness-backoff-ms' && i + 1 < argv.length) {
      const parsed = Number.parseInt(argv[i + 1], 10);
      if (Number.isInteger(parsed)) cliReadinessBackoffMs = parsed;
      i += 1;
    }
  }

  autoRegisterOrgans(cliPort, {
    timeoutMs: cliTimeoutMs,
    readinessMaxAttempts: cliReadinessMaxAttempts,
    readinessBackoffMs: cliReadinessBackoffMs,
    log: console.log,
  })
    .then((summary) => {
      process.exitCode = summary.ok ? 0 : 1;
    })
    .catch((err) => {
      console.error('[auto-register] unexpected failure:', err);
      process.exit(2);
    });
}

module.exports = {
  autoRegisterOrgans,
  ORGANS,
  probeReadiness,
  probeReadinessWithRetry,
};
