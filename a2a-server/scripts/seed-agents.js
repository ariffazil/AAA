#!/usr/bin/env node
/**
 * A2A Agent Seed — registers all 8 forge instruments at AAA boot.
 * Called after agent-card-registry auto-loads CIV-33 cards.
 *
 * Lifecycle contract:
 *   - CommonJS export: { AGENTS, seed }
 *   - No import side-effect: importing this file MUST NOT trigger HTTP I/O.
 *     Side-effects only run when invoked as a CLI (require.main === module).
 *   - Configurable port / base URL via seed({ port, baseUrl, timeoutMs, log }).
 *   - Awaits every request; applies an explicit timeout per request.
 *   - Returns accurate { registered, existing, failed, total } counts.
 *   - Idempotent: treats HTTP 409 Conflict (already registered) as "existing".
 *   - Payload contract: { agent_id, agent_role, actor_id: null, policy: { fi_slot, ... } }
 *     FI is stored as policy.fi_slot; actor_id is intentionally null until the
 *     actor binds a session key in arifOS.
 *   - No hardcoded bearer token. If AAA_AUTH_TOKEN env is set, attach it; otherwise
 *     rely on the local-network trust boundary (localhost-only).
 */

'use strict';

const fs = require('fs');
const http = require('http');
const path = require('path');
const { URL } = require('url');
const YAML = require('yaml');

const DEFAULT_PORT = 3001;
const DEFAULT_TIMEOUT_MS = 5000;
const REGISTRY_PATH = path.resolve(__dirname, '../../registries/forge_instruments.yaml');

const AGENT_ID_BY_FI = Object.freeze({
  'FI-001': 'opencode',
  'FI-002': 'claude-code',
  'FI-003': 'qwen-code',
  'FI-004': 'antigravity',
  'FI-005': 'codex-cli',
  'FI-006': 'copilot-cli',
  'FI-007': 'grok-build',
  'FI-008': 'kimi-code',
});
const ROLE_BY_FI = Object.freeze({
  'FI-001': 'orchestrator',
  'FI-002': 'architect',
  'FI-003': 'dormant',
  'FI-004': 'executor',
  'FI-005': 'forge',
  'FI-006': 'forge',
  'FI-007': 'forge',
  'FI-008': 'forge',
});

function loadAgents(registryPath = REGISTRY_PATH) {
  const document = YAML.parse(fs.readFileSync(registryPath, 'utf8'));
  const instruments = Array.isArray(document && document.instruments)
    ? document.instruments
    : [];
  const agents = instruments
    .filter((instrument) => AGENT_ID_BY_FI[instrument.id])
    .map((instrument) => Object.freeze({
      id: AGENT_ID_BY_FI[instrument.id],
      fi: instrument.id,
      model: instrument.model || 'unknown',
      mcp: Array.isArray(instrument.mcp_surface) ? instrument.mcp_surface.length : 0,
      role: ROLE_BY_FI[instrument.id],
    }));
  if (agents.length !== Object.keys(AGENT_ID_BY_FI).length) {
    throw new Error(
      `forge instrument registry mismatch: expected 8 active slots, found ${agents.length}`,
    );
  }
  return Object.freeze(agents);
}

const AGENTS = loadAgents();

/**
 * Build the registration payload for one agent. Mirrors the AAA /api/agents/register
 * contract: actor_id is null until the actor binds a session; FI is stored on
 * policy.fi_slot so the lifecycle manager can locate the slot later.
 */
function buildPayload(agent) {
  return {
    agent_id: agent.id,
    agent_role: agent.role,
    actor_id: null,
    policy: {
      fi_slot: agent.fi,
      model: agent.model,
      mcp_count: agent.mcp,
      citizenship: 'warga-aaa',
    },
  };
}

/**
 * Resolve the base URL we POST to. Honors explicit baseUrl, then port, then env,
 * then the well-known default of 127.0.0.1:3001.
 */
function resolveBaseUrl(opts) {
  if (opts && typeof opts.baseUrl === 'string' && opts.baseUrl.length > 0) {
    return opts.baseUrl.replace(/\/+$/, '');
  }
  const rawPort = (opts && opts.port != null)
    ? opts.port
    : (process.env.A2A_PORT || process.env.AAA_A2A_PORT || DEFAULT_PORT);
  const parsedPort = Number.parseInt(String(rawPort), 10);
  const port = Number.isInteger(parsedPort) && parsedPort > 0 ? parsedPort : DEFAULT_PORT;
  return `http://127.0.0.1:${port}`;
}

function postJson(targetUrl, body, timeoutMs) {
  return new Promise((resolve) => {
    let parsed;
    try {
      parsed = new URL(targetUrl);
    } catch (err) {
      resolve({ ok: false, status: 0, error: `invalid url: ${err.message}`, body: '' });
      return;
    }

    const payload = Buffer.from(JSON.stringify(body), 'utf8');
    const headers = {
      'Content-Type': 'application/json',
      'Content-Length': payload.length,
    };

    // Optional bearer token from env. Never hardcoded.
    if (process.env.AAA_AUTH_TOKEN) {
      headers['Authorization'] = `Bearer ${process.env.AAA_AUTH_TOKEN}`;
    }

    const req = http.request({
      method: 'POST',
      hostname: parsed.hostname,
      port: parsed.port,
      path: `${parsed.pathname.replace(/\/+$/, '')}/api/agents/register`,
      headers,
      timeout: timeoutMs,
    }, (res) => {
      let chunks = '';
      res.setEncoding('utf8');
      res.on('data', (c) => { chunks += c; });
      res.on('end', () => {
        resolve({
          ok: res.statusCode >= 200 && res.statusCode < 300,
          status: res.statusCode,
          body: chunks,
          error: null,
        });
      });
    });

    req.on('timeout', () => {
      req.destroy(new Error(`timeout after ${timeoutMs}ms`));
    });
    req.on('error', (err) => {
      resolve({ ok: false, status: 0, error: err.message, body: '' });
    });
    req.write(payload);
    req.end();
  });
}

/**
 * Seed all 8 agents. Returns a structured counts object that ALWAYS
 * sums to AGENTS.length (registered + existing + failed === total).
 *
 *   registered — new agent was created on this run (HTTP 2xx, not 409)
 *   existing   — agent was already present (HTTP 409 Conflict)
 *   failed     — network error, timeout, or non-2xx/409 response
 */
async function seed(opts) {
  const baseUrl = resolveBaseUrl(opts || {});
  const timeoutMs = (opts && Number.isInteger(opts.timeoutMs)) ? opts.timeoutMs : DEFAULT_TIMEOUT_MS;
  const log = (opts && typeof opts.log === 'function') ? opts.log : () => {};

  const counts = { registered: 0, existing: 0, failed: 0, total: AGENTS.length, baseUrl };

  for (const agent of AGENTS) {
    const payload = buildPayload(agent);
    const result = await postJson(baseUrl, payload, timeoutMs);

    if (result.ok) {
      counts.registered += 1;
      log(`✅ ${agent.id} (${agent.fi}) — ${result.status}`);
    } else if (result.status === 409) {
      counts.existing += 1;
      log(`↻ ${agent.id} (${agent.fi}) — 409 already registered`);
    } else {
      counts.failed += 1;
      const detail = result.error
        ? result.error
        : `HTTP ${result.status} ${result.body ? '· ' + result.body.substring(0, 120) : ''}`;
      log(`❌ ${agent.id} (${agent.fi}) — ${detail}`);
    }
  }

  log(
    `Seed complete. ${counts.registered} registered · ${counts.existing} existing · ` +
    `${counts.failed} failed · ${counts.total} total`,
  );
  return counts;
}

// Side-effect guard: only run when invoked as a CLI, never on require.
if (require.main === module) {
  const argv = process.argv.slice(2);
  let cliPort = DEFAULT_PORT;
  let cliBaseUrl = null;
  let cliTimeoutMs = DEFAULT_TIMEOUT_MS;
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (flag === '--port' && i + 1 < argv.length) {
      const parsed = Number.parseInt(argv[i + 1], 10);
      if (Number.isInteger(parsed)) cliPort = parsed;
      i += 1;
    } else if (flag === '--base-url' && i + 1 < argv.length) {
      cliBaseUrl = argv[i + 1];
      i += 1;
    } else if (flag === '--timeout-ms' && i + 1 < argv.length) {
      const parsed = Number.parseInt(argv[i + 1], 10);
      if (Number.isInteger(parsed)) cliTimeoutMs = parsed;
      i += 1;
    }
  }

  seed({ port: cliPort, baseUrl: cliBaseUrl, timeoutMs: cliTimeoutMs, log: console.log })
    .then((counts) => {
      process.exitCode = counts.failed > 0 ? 1 : 0;
    })
    .catch((err) => {
      console.error('[seed-agents] unexpected failure:', err);
      process.exit(2);
    });
}

module.exports = { AGENTS, seed, buildPayload, loadAgents, resolveBaseUrl };
