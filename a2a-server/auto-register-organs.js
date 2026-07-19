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
 * Probe each organ, register it, then seed the 8 forge instruments.
 * Always returns a structured counts object — never throws to the caller.
 */
async function autoRegisterOrgans(port = 3001, opts) {
  const parsedPort = Number.parseInt(String(port), 10);
  const normalizedPort = Number.isInteger(parsedPort) && parsedPort > 0 ? parsedPort : 3001;
  const baseUrl = `http://127.0.0.1:${normalizedPort}`;
  const timeoutMs = (opts && Number.isInteger(opts.timeoutMs)) ? opts.timeoutMs : 5000;
  const startedAt = new Date().toISOString();
  const log = (opts && typeof opts.log === 'function') ? opts.log : () => {};

  const organCounts = { registered: 0, existing: 0, failed: 0, total: ORGANS.length };

  for (const organ of ORGANS) {
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
    }
  }

  autoRegisterOrgans(cliPort, { timeoutMs: cliTimeoutMs, log: console.log })
    .then((summary) => {
      process.exitCode = summary.ok ? 0 : 1;
    })
    .catch((err) => {
      console.error('[auto-register] unexpected failure:', err);
      process.exit(2);
    });
}

module.exports = { autoRegisterOrgans, ORGANS };
