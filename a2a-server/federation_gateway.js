#!/usr/bin/env node
/**
 * Federation Gateway — Cross-Organ Resource Proxy + Pipeline Orchestration
 * ═══════════════════════════════════════════════════════════════════════
 *
 * Closes the MCP federation gap: MCP is multi-server but not federated.
 * This gateway makes organs cross-readable and chainable.
 *
 * Three capabilities:
 *   1. RESOURCE PROXY — `wealth://capabilities` actually resolves via MCP
 *   2. PIPELINE ORCHESTRATION — chain prompts across organs (A→B→C)
 *   3. FEDERATION STATUS — live cross-organ resource/tool/prompt census
 *
 * MCP spec reference: multi-server = client assembles context.
 * Federation = the control plane (AAA) assembles and orchestrates.
 *
 * DITEMPA BUKAN DIBERI — Federation is forged, not given.
 */

'use strict';

const HTTP = require('http');

// ── Organ Map — canonical ports + MCP endpoints ──────────────────────
const ORGANS = {
  arifos: { name: 'arifOS',  port: 8088,  host: '127.0.0.1', desc: 'Constitutional kernel' },
  geox:   { name: 'GEOX',    port: 8081,  host: '127.0.0.1', desc: 'Earth intelligence' },
  wealth: { name: 'WEALTH',  port: 18082, host: '127.0.0.1', desc: 'Capital intelligence' },
  well:   { name: 'WELL',    port: 18083, host: '127.0.0.1', desc: 'Human readiness' },
  aforge: { name: 'A-FORGE', port: 7072,  host: '127.0.0.1', desc: 'Execution shell' },
};

// ── Resource URI Scheme Map — which organ handles which scheme ────────
const SCHEME_MAP = {
  'arifos':  'arifos',
  'geox':    'geox',
  'wealth':  'wealth',
  'well':    'well',
  'aforge':  'aforge',
  'forge':   'aforge',
};

// ── MCP Call Helper ───────────────────────────────────────────────────
async function mcpCall(organKey, method, params = {}, timeoutMs = 10000, identity = {}) {
  const organ = ORGANS[organKey];
  if (!organ) return { ok: false, error: `Unknown organ: ${organKey}` };

  const payload = JSON.stringify({
    jsonrpc: '2.0',
    method,
    params,
    id: `fgw-${Date.now()}-${Math.random().toString(36).slice(2,6)}`,
  });

  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Content-Length': Buffer.byteLength(payload),
  };
  if (identity.actor_id) headers['X-Actor-Id'] = identity.actor_id;
  if (identity.session_id) headers['X-Session-Id'] = identity.session_id;

  return new Promise((resolve) => {
    const req = HTTP.request({
      hostname: organ.host, port: organ.port, path: '/mcp',
      method: 'POST',
      headers,
      timeout: timeoutMs,
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            resolve({ ok: false, error: json.error.message || JSON.stringify(json.error) });
          } else {
            resolve({ ok: true, result: json.result });
          }
        } catch (e) {
          resolve({ ok: false, error: `Parse error: ${e.message}`, raw: data.slice(0, 500) });
        }
      });
    });
    req.on('error', (e) => resolve({ ok: false, error: `Connection error: ${e.message}` }));
    req.on('timeout', () => { req.destroy(); resolve({ ok: false, error: 'Timeout' }); });
    req.write(payload);
    req.end();
  });
}

// ── 1. RESOURCE PROXY ─────────────────────────────────────────────────
/**
 * Resolve a cross-organ resource URI.
 * e.g. "wealth://capabilities" → calls WEALTH tools/list → returns tool catalog
 *      "arifos://constitution/floors" → calls arifOS internal resource
 *      "well://state/current" → calls WELL readiness
 *
 * @param {string} uri — e.g. "wealth://capabilities", "arifos://constitution/floors"
 * @returns {{ ok: boolean, uri: string, organ: string, content?: any, error?: string }}
 */
async function resolveResource(uri) {
  // Parse scheme from URI
  const match = uri.match(/^(\w+):\/\/(.+)/);
  if (!match) {
    return { ok: false, uri, error: `Invalid URI scheme: ${uri}. Expected organ://path` };
  }

  const scheme = match[1];
  const path = match[2];
  const organKey = SCHEME_MAP[scheme];

  if (!organKey) {
    return { ok: false, uri, error: `Unknown scheme: ${scheme}. Valid: ${Object.keys(SCHEME_MAP).join(', ')}` };
  }

  // Strategy: use tools/list to get the organ's capability surface
  // This is the most reliable cross-organ resource resolution
  const toolsResult = await mcpCall(organKey, 'tools/list');
  if (!toolsResult.ok) {
    // Fallback: try resources/list
    const resResult = await mcpCall(organKey, 'resources/list');
    if (!resResult.ok) {
      return { ok: false, uri, organ: organKey, error: `Cannot reach ${organKey}: ${toolsResult.error}` };
    }
    return { ok: true, uri, organ: organKey, content: { resources: resResult.result } };
  }

  // Also try prompts/list for full surface
  const promptsResult = await mcpCall(organKey, 'prompts/list');

  // Build a rich capability snapshot
  const content = {
    organ: ORGANS[organKey].name,
    port: ORGANS[organKey].port,
    resolved_at: new Date().toISOString(),
    tools: toolsResult.result?.tools?.length || 0,
    tool_names: (toolsResult.result?.tools || []).map(t => t.name),
    prompts: promptsResult.ok ? (promptsResult.result?.prompts?.length || 0) : 'unavailable',
    prompt_names: promptsResult.ok ? (promptsResult.result?.prompts || []).map(p => p.name) : [],
  };

  return { ok: true, uri, organ: organKey, content };
}

// ── 2. PIPELINE ORCHESTRATION ─────────────────────────────────────────
/**
 * Execute a pipeline of organ steps sequentially.
 *
 * Pipeline format:
 * [
 *   { organ: "wealth", tool: "wealth_compute_npv", args: { cash_flows: [..], discount_rate: 0.1 } },
 *   { organ: "arifos", tool: "arif_judge", args: { intent: "...", ... } },
 *   { organ: "arifos", tool: "arif_seal", args: { payload: "...", ... } },
 * ]
 *
 * Each step receives the previous step's output as `pipeline_context`.
 * Stops on first failure.
 *
 * @param {Array} pipeline — array of {organ, tool, args} steps
 * @returns {{ ok: boolean, steps: Array, sealed?: boolean }}
 */
async function orchestratePipeline(pipeline, options = {}) {
  const steps = [];
  let pipelineContext = {};

  for (let i = 0; i < pipeline.length; i++) {
    const step = pipeline[i];
    const stepStart = Date.now();

    // Merge pipeline_context into args
    const args = {
      ...(step.args || {}),
      ...(options.passContext !== false ? { _pipeline_context: pipelineContext } : {}),
    };

    const result = await mcpCall(step.organ, 'tools/call', {
      name: step.tool,
      arguments: args,
    }, options.timeoutMs || 15000);

    const stepResult = {
      step: i + 1,
      organ: step.organ,
      tool: step.tool,
      ok: result.ok,
      duration_ms: Date.now() - stepStart,
      output: result.ok ? result.result : undefined,
      error: result.ok ? undefined : result.error,
    };

    steps.push(stepResult);

    if (!result.ok) {
      return {
        ok: false,
        steps,
        error: `Pipeline failed at step ${i + 1}: ${step.organ}/${step.tool} — ${result.error}`,
      };
    }

    // Feed output forward
    pipelineContext[`step_${i + 1}_${step.tool}`] = result.result;
    pipelineContext.last_step = i + 1;
    pipelineContext.last_organ = step.organ;
  }

  return { ok: true, steps };
}

// ── 3. FEDERATION STATUS ──────────────────────────────────────────────
/**
 * Live cross-organ census: tools, prompts, resources per organ.
 */
async function federationStatus() {
  const organs = {};
  const probes = [];

  for (const [key, organ] of Object.entries(ORGANS)) {
    const start = Date.now();
    const [toolsRes, promptsRes, healthRes] = await Promise.all([
      mcpCall(key, 'tools/list', {}, 5000),
      mcpCall(key, 'prompts/list', {}, 5000),
      new Promise((resolve) => {
        HTTP.get(`http://${organ.host}:${organ.port}/health`, (res) => {
          let d = '';
          res.on('data', c => d += c);
          res.on('end', () => {
            try { resolve({ ok: true, status: JSON.parse(d).status || 'alive' }); }
            catch { resolve({ ok: true, status: 'alive' }); }
          });
        }).on('error', () => resolve({ ok: false }));
      }),
    ]);

    organs[key] = {
      name: organ.name,
      port: organ.port,
      health: healthRes.ok ? healthRes.status : 'down',
      latency_ms: Date.now() - start,
      tools: toolsRes.ok ? (toolsRes.result?.tools?.length || 0) : 0,
      prompts: promptsRes.ok ? (promptsRes.result?.prompts?.length || 0) : 0,
      tool_names: toolsRes.ok ? (toolsRes.result?.tools || []).map(t => t.name).slice(0, 10) : [],
      prompt_names: promptsRes.ok ? (promptsRes.result?.prompts || []).map(p => p.name) : [],
      status: toolsRes.ok ? 'online' : 'degraded',
    };
  }

  const aliveCount = Object.values(organs).filter(o => o.status === 'online').length;
  const total = Object.keys(organs).length;

  return {
    ok: true,
    timestamp: new Date().toISOString(),
    summary: `${aliveCount}/${total} organs online`,
    organs,
    cross_organ_schemes: Object.keys(SCHEME_MAP),
    resource_gateway: 'active',
    pipeline_orchestrator: 'active',
  };
}

// ── Express Route Handlers ────────────────────────────────────────────

/**
 * Mount federation routes on Express app.
 * @param {import('express').Express} app
 */
function mountFederationRoutes(app) {
  // ── Auth Middleware ──────────────────────────────────────────────────
  // FIX 2026-07-10: Gateway had zero-auth — any client reaching AAA:3001 could
  // probe all organs' MCP interfaces and chain pipelines without credentials.
  // Token sourced from vault.flat.env → process.env.A2A_TOKEN (loaded by systemd).
  const FEDERATION_TOKEN = process.env.A2A_TOKEN;
  if (!FEDERATION_TOKEN) {
    console.error('[federation_gateway] FATAL: A2A_TOKEN env var not set — refusing to mount routes');
    return;
  }

  function authMiddleware(req, res, next) {
    const token = req.headers['x-arifos-token'];
    if (!token || token !== FEDERATION_TOKEN) {
      return res.status(401).json({
        ok: false,
        error: 'Unauthorized',
        detail: 'Missing or invalid x-arifos-token header',
      });
    }
    next();
  }

  // ── Federated Routes — all auth-gated ───────────────────────────────

  // POST /federation/resource — Resolve cross-organ resource URI
  app.post('/federation/resource', authMiddleware, async (req, res) => {
    const { uri } = req.body || {};
    if (!uri) {
      return res.status(400).json({ ok: false, error: 'Missing "uri" in request body' });
    }
    const result = await resolveResource(uri);
    res.status(result.ok ? 200 : 404).json(result);
  });

  // GET /federation/resource/:scheme/* — URL-encoded resource resolution
  app.get('/federation/resource/:scheme/*', authMiddleware, async (req, res) => {
    const uri = `${req.params.scheme}://${req.params[0] || ''}`;
    const result = await resolveResource(uri);
    res.status(result.ok ? 200 : 404).json(result);
  });

  // POST /federation/pipeline — Execute a cross-organ pipeline
  app.post('/federation/pipeline', authMiddleware, async (req, res) => {
    const { pipeline, options } = req.body || {};
    if (!pipeline || !Array.isArray(pipeline) || pipeline.length === 0) {
      return res.status(400).json({ ok: false, error: 'Missing or empty "pipeline" array in request body' });
    }
    const result = await orchestratePipeline(pipeline, options || {});
    res.status(result.ok ? 200 : 422).json(result);
  });

  // GET /federation/status — Live cross-organ census
  app.get('/federation/status', authMiddleware, async (req, res) => {
    const result = await federationStatus();
    res.status(200).json(result);
  });

  // GET /federation/capabilities — What the federation gateway can do
  app.get('/federation/capabilities', authMiddleware, (req, res) => {
    res.json({
      ok: true,
      gateway: 'Federation Gateway v1.0.0 — 2026-07-10',
      endpoints: {
        'POST /federation/resource': 'Resolve cross-organ resource URI (wealth://, arifos://, well://)',
        'GET /federation/resource/:scheme/*': 'URL-encoded resource resolution',
        'POST /federation/pipeline': 'Execute cross-organ pipeline [step1, step2, ...]',
        'GET /federation/status': 'Live census of all organs (tools, prompts, health)',
        'GET /federation/capabilities': 'This page',
      },
      organ_schemes: SCHEME_MAP,
      organs: Object.fromEntries(
        Object.entries(ORGANS).map(([k, v]) => [k, { name: v.name, port: v.port, desc: v.desc }])
      ),
    });
  });

  console.log('[federation_gateway] Routes mounted with A2A_TOKEN auth: /federation/resource, /federation/pipeline, /federation/status, /federation/capabilities');
}

// ── Exports ───────────────────────────────────────────────────────────
module.exports = {
  ORGANS,
  SCHEME_MAP,
  resolveResource,
  orchestratePipeline,
  federationStatus,
  mountFederationRoutes,
  mcpCall,
};
