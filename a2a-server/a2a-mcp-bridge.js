#!/usr/bin/env node
/**
 * a2a-mcp-bridge.js — A2A Task → MCP Tool Call → A2A Response + VAULT999 Receipt
 *
 * The clean adapter that closes Gap 1 of the AAA-A2A architectural pivot:
 * External agents send A2A tasks, AAA routes to the correct MCP organ,
 * returns the result wrapped in A2A format with a VAULT999 receipt.
 *
 * ORGAN MAP:
 *   arifOS   :8088 — constitutional kernel (judge, seal, lease)
 *   A-FORGE  :7072 — execution shell (shell, git, docker, code)
 *   GEOX     :8081 — earth intelligence (seismic, basin, petrophysics)
 *   WEALTH   :18082 — capital intelligence (NPV, risk, conservation)
 *   WELL     :18083 — human readiness (vitality, fatigue, dignity)
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const { writeSeal } = require('./vault');
const HTTP = require('http');
const HTTPS = require('https');

// ── Canonical Organ Map ──────────────────────────────────────────────
const ORGAN_MAP = {
  arifos:  { name: 'arifOS',  port: 8088,  host: '127.0.0.1', protocol: 'http' },
  aforge:  { name: 'A-FORGE', port: 7072,  host: '127.0.0.1', protocol: 'http' },
  geox:    { name: 'GEOX',    port: 8081,  host: '127.0.0.1', protocol: 'http' },
  wealth:  { name: 'WEALTH',  port: 18082, host: '127.0.0.1', protocol: 'http' },
  well:    { name: 'WELL',    port: 18083, host: '127.0.0.1', protocol: 'http' },
};

const A2A_STATUS_MAP = {
  completed: 'COMPLETED',
  failed:    'FAILED',
  working:   'WORKING',
  held:      'INPUT_REQUIRED',
};

// ── MCP Client ──────────────────────────────────────────────────────

/**
 * Call an MCP tool on a federation organ via HTTP POST.
 *
 * @param {string} organKey — key in ORGAN_MAP (e.g. 'arifos', 'aforge')
 * @param {string} toolName — MCP tool name (e.g. 'arif_judge', 'forge_shell')
 * @param {object} args — tool arguments
 * @param {number} [timeoutMs=15000] — request timeout
 * @returns {Promise<{ok: boolean, result?: any, error?: string}>}
 */
async function callMCPTool(organKey, toolName, args, timeoutMs = 15000) {
  const organ = ORGAN_MAP[organKey];
  if (!organ) {
    return { ok: false, error: `Unknown organ: ${organKey}. Valid: ${Object.keys(ORGAN_MAP).join(', ')}` };
  }

  const payload = JSON.stringify({
    jsonrpc: '2.0',
    method: 'tools/call',
    params: { name: toolName, arguments: args || {} },
    id: `bridge-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
  });

  return new Promise((resolve) => {
    const options = {
      hostname: organ.host,
      port: organ.port,
      path: '/mcp',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'User-Agent': 'AAA-A2A-Bridge/1.0',
      },
      timeout: timeoutMs,
    };

    const lib = organ.protocol === 'https' ? HTTPS : HTTP;
    const req = lib.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);

          // MCP error response
          if (parsed.error) {
            return resolve({
              ok: false,
              error: parsed.error.message || 'MCP error',
              code: parsed.error.code,
              data: parsed.error.data,
            });
          }

          // MCP success response
          return resolve({
            ok: true,
            result: parsed.result,
            mcpId: parsed.id,
          });
        } catch (parseErr) {
          return resolve({
            ok: false,
            error: `Failed to parse MCP response: ${parseErr.message}`,
            raw: data.slice(0, 1000),
          });
        }
      });
    });

    req.on('error', (err) => {
      resolve({ ok: false, error: `MCP request failed: ${err.message}` });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({ ok: false, error: `MCP request timed out after ${timeoutMs}ms` });
    });

    req.write(payload);
    req.end();
  });
}

// ── A2A Bridge ──────────────────────────────────────────────────────

/**
 * Bridge an A2A task to an MCP tool call and return an A2A response.
 *
 * Expected A2A task structure:
 *   params.metadata = {
 *     skill: 'forge.delegate' | 'governance.check' | etc.,
 *     routing: 'aforge' | 'arifos' | 'geox' | 'wealth' | 'well',
 *     tool: 'tool_name'         // MCP tool to call
 *   }
 *   params.message.parts[].text  // or params.metadata.args for structured args
 *
 * @param {object} task — A2A task object (from message/send or tasks/send)
 * @param {object} [options] — override options
 * @param {string} [options.organ] — override routing organ
 * @param {string} [options.tool] — override tool name
 * @param {object} [options.args] — override arguments
 * @returns {Promise<object>} A2A-compatible response
 */
async function bridgeTask(task, options = {}) {
  const params = task.params || task;
  const metadata = params.metadata || {};
  const message = params.message || {};

  // Resolve routing: explicit options > metadata > default
  const organKey = (options.organ || metadata.routing || '').toLowerCase();
  const toolName = options.tool || metadata.tool || '';
  const skillId = metadata.skill || 'unknown';

  // If no organ specified, try to infer from skill
  const resolvedOrgan = organKey || inferOrganFromSkill(skillId);

  if (!resolvedOrgan || !toolName) {
    return buildA2AResponse(task, {
      status: 'FAILED',
      error: {
        code: -32602,
        message: 'Missing routing information',
        data: { hint: 'Specify metadata.routing (organ) and metadata.tool in the A2A task' },
      },
    });
  }

  // Extract arguments from message text or metadata.args
  let args = options.args || metadata.args || {};
  if (Object.keys(args).length === 0 && message.parts) {
    // Fallback: try to parse text as arguments
    const textParts = message.parts.filter((p) => p.type === 'text');
    if (textParts.length > 0 && !args.command && !args.query) {
      args = { input: textParts[0].text };
    }
  }

  // Mark as WORKING in task store
  const taskId = params.id || `bridge-${Date.now()}`;

  // Call the MCP tool
  const mcpResult = await callMCPTool(resolvedOrgan, toolName, args);

  if (!mcpResult.ok) {
    // Write a VOID receipt on failure
    try {
      await writeSeal(
        { id: taskId, contextId: params.contextId || taskId, status: { state: 'FAILED' }, metadata },
        'aaa-bridge',
        `mcp.call.${resolvedOrgan}.${toolName}.fail`,
        { error: mcpResult.error, organ: resolvedOrgan, tool: toolName }
      );
    } catch { /* best effort */ }

    return buildA2AResponse(task, {
      status: 'FAILED',
      error: {
        code: -32000,
        message: `MCP tool call failed: ${mcpResult.error}`,
        data: { organ: resolvedOrgan, tool: toolName, mcpError: mcpResult },
      },
    });
  }

  // Write a VAULT999 receipt on success
  let receiptId = null;
  try {
    const sealResult = await writeSeal(
      { id: taskId, contextId: params.contextId || taskId, status: { state: 'COMPLETED' }, metadata },
      'aaa-bridge',
      `mcp.call.${resolvedOrgan}.${toolName}.ok`,
      { organ: resolvedOrgan, tool: toolName, resultSummary: truncate(JSON.stringify(mcpResult.result), 200) }
    );
    if (sealResult.ok) {
      receiptId = sealResult.data?.id || sealResult.data?.receipt_id || `seal-${Date.now()}`;
    }
  } catch { /* receipt best effort */ }

  return buildA2AResponse(task, {
    status: 'COMPLETED',
    result: {
      mcp: mcpResult.result,
      receipt_id: receiptId,
      organ: resolvedOrgan,
      tool: toolName,
    },
  });
}

// ── Helpers ──────────────────────────────────────────────────────────

/**
 * Infer organ from A2A skill ID.
 */
function inferOrganFromSkill(skillId) {
  const SKILL_ORGAN_MAP = {
    'forge.delegate':          'aforge',
    'forge.execute':           'aforge',
    'hold.request':            'arifos',
    'governance.check':        'arifos',
    'constitutional.deliberation': 'arifos',
    'judge.deliberate':        'arifos',
    'vault.seal':              'arifos',
    'vault.receipt':           'arifos',
    'lease.issue':             'arifos',
    'agent.discover':          'arifos',
    'session.identity':        'arifos',
    'basin.resolve':           'geox',
    'seismic.compute':         'geox',
    'petrophysics.compute':    'geox',
    'prospect.evaluate':       'geox',
    'earth.evidence':          'geox',
    'capital.compute':         'wealth',
    'risk.assess':             'wealth',
    'conservation.check':      'wealth',
    'flow.check':              'wealth',
    'wellness.assess':         'well',
    'vitality.validate':       'well',
    'homeostasis.assess':      'well',
    'dignity.guard':           'well',
  };
  return SKILL_ORGAN_MAP[skillId] || null;
}

/**
 * Build an A2A-compatible response object.
 */
function buildA2AResponse(task, outcome) {
  const params = task.params || task;
  const taskId = params.id || `bridge-${Date.now()}`;

  const status = outcome.status || 'COMPLETED';
  const a2aStatus = A2A_STATUS_MAP[status] || status;

  const response = {
    id: taskId,
    jsonrpc: '2.0',
    result: {
      id: taskId,
      status: {
        state: a2aStatus,
        timestamp: new Date().toISOString(),
      },
    },
  };

  if (outcome.result) {
    response.result.artifact = {
      parts: [
        {
          type: 'text',
          text: typeof outcome.result === 'string'
            ? outcome.result
            : JSON.stringify(outcome.result, null, 2),
        },
      ],
      metadata: outcome.result.mcp?.metadata || outcome.result.metadata || {},
    };
  }

  if (outcome.error) {
    response.result.status.error = outcome.error;
    response.result.status.state = 'FAILED';
  }

  // Surface VAULT999 receipt if present
  if (outcome.result?.receipt_id) {
    response.result.metadata = {
      ...response.result.metadata,
      receipt_id: outcome.result.receipt_id,
    };
  }

  return response;
}

function truncate(str, maxLen) {
  if (!str || str.length <= maxLen) return str;
  return str.slice(0, maxLen) + '...';
}

/**
 * Get the organ map (for discovery/validation).
 */
function getOrganMap() {
  return Object.entries(ORGAN_MAP).map(([key, val]) => ({
    key,
    name: val.name,
    port: val.port,
  }));
}

/**
 * Health check: verify all organs are reachable.
 * Returns { ok, organs: [{ key, name, port, alive }] }
 */
async function bridgeHealth() {
  const results = [];
  let allOk = true;

  for (const [key, organ] of Object.entries(ORGAN_MAP)) {
    try {
      const alive = await new Promise((resolve) => {
        const req = HTTP.get(
          `http://${organ.host}:${organ.port}/health`,
          { timeout: 3000 },
          (res) => { resolve(res.statusCode >= 200 && res.statusCode < 400); }
        );
        req.on('error', () => resolve(false));
        req.on('timeout', () => { req.destroy(); resolve(false); });
      });
      if (!alive) allOk = false;
      results.push({ key, name: organ.name, port: organ.port, alive });
    } catch {
      allOk = false;
      results.push({ key, name: organ.name, port: organ.port, alive: false });
    }
  }

  return { ok: allOk, organs: results };
}

module.exports = {
  bridgeTask,
  callMCPTool,
  bridgeHealth,
  getOrganMap,
  ORGAN_MAP,
};
