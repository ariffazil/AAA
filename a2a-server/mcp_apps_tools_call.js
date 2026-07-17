/**
 * mcp_apps_tools_call.js — Host-mediated tools/call for SEP-1865 MCP Apps
 *
 * Browser guest (connect-src 'none') never hits organs.
 * AAA host → this proxy → GEOX/arifOS with session lifecycle.
 *
 * OBSERVE allowlist: execute on organ after AAA gate.
 * MUTATE / unknown: 888 HOLD (no blind mutation from UI).
 *
 * DITEMPA BUKAN DIBERI
 */

const HTTP = require('http');
const HTTPS = require('https');

const ORGAN_MAP = {
  arifos: { name: 'arifOS', port: 8088, host: '127.0.0.1', protocol: 'http' },
  geox: { name: 'GEOX', port: 8081, host: '127.0.0.1', protocol: 'http' },
  wealth: { name: 'WEALTH', port: 18082, host: '127.0.0.1', protocol: 'http' },
  well: { name: 'WELL', port: 18083, host: '127.0.0.1', protocol: 'http' },
  aforge: { name: 'A-FORGE', port: 7072, host: '127.0.0.1', protocol: 'http' },
};

/** Stateful MCP organs that mint Mcp-Session-Id */
const STATEFUL_ORGANS = new Set(['geox']);

/**
 * App id → default organ for tools/call routing.
 * Guest only knows tool name; host binds app → organ.
 */
const APP_ORGAN = {
  'well-desk': 'geox',
  'earth-volume': 'geox',
  'judge-console': 'geox',
  'aforge-preview': 'aforge',
  'wealth-portfolio': 'wealth',
};

/**
 * OBSERVE allowlist — UI may call these without arifOS lease.
 * Mutations stay HOLD until full lease/gate path.
 */
const OBSERVE_ALLOWLIST = new Set([
  // Well-desk P0
  'geox_well_desk_open',
  'geox_surface_status',
  'geox_render_well_panel',
  'geox_well_qc',
  // Common GEOX read surfaces (host-mediated only)
  'geox_atlas',
  'geox_basin',
  'geox_deep_time_state',
  'geox_earthquake_catalog',
  'geox_registry',
  'geox_health',
  // WEALTH read surfaces (portfolio dashboard)
  'capital_health',
  'capital_primitive',
  'capital_diagnose',
  'capital_market',
  'capital_wisdom',
]);

/** Explicit mutate / seal — always HOLD from UI path */
const MUTATE_DENYLIST = new Set([
  'geox_well_desk_publish',
  'geox_well_ingest',
  'geox_claim_create',
  'geox_claim_seal',
  'geox_segy_export_tool',
]);

const MUTATE_NAME_RE =
  /(publish|ingest|seal|write|delete|drop|export|mutate|create|update|commit|deploy)/i;

const MCP_ACCEPT = 'application/json, text/event-stream';
const SESSION_TTL_MS = 5 * 60 * 1000;

/** @type {Map<string, { id: string, expires: number }>} */
const sessions = new Map();

function headerGet(headers, name) {
  if (!headers) return undefined;
  const want = name.toLowerCase();
  for (const [k, v] of Object.entries(headers)) {
    if (k.toLowerCase() === want) return Array.isArray(v) ? v[0] : v;
  }
  return undefined;
}

function parseJsonOrSse(raw) {
  const text = (raw || '').trim();
  if (!text) return null;
  if (text.startsWith('{') || text.startsWith('[')) {
    return JSON.parse(text);
  }
  // SSE: take last data: line with JSON
  const lines = text.split(/\r?\n/);
  let last = null;
  for (const line of lines) {
    if (line.startsWith('data:')) {
      const payload = line.slice(5).trim();
      if (payload && payload !== '[DONE]') {
        try {
          last = JSON.parse(payload);
        } catch {
          /* skip */
        }
      }
    }
  }
  if (last) return last;
  throw new Error(`Unparseable MCP body: ${text.slice(0, 200)}`);
}

/**
 * Low-level HTTP POST to organ /mcp.
 * @returns {Promise<{ status: number, headers: object, body: string }>}
 */
function mcpHttp(organKey, { body, sessionId, timeoutMs = 20000 }) {
  const organ = ORGAN_MAP[organKey];
  if (!organ) {
    return Promise.reject(new Error(`Unknown organ: ${organKey}`));
  }

  const payload = typeof body === 'string' ? body : JSON.stringify(body);
  const headers = {
    'Content-Type': 'application/json',
    Accept: MCP_ACCEPT,
    'Content-Length': Buffer.byteLength(payload),
    'User-Agent': 'AAA-MCP-Apps-Host/1.0',
  };
  if (sessionId) headers['Mcp-Session-Id'] = sessionId;

  return new Promise((resolve, reject) => {
    const lib = organ.protocol === 'https' ? HTTPS : HTTP;
    const req = lib.request(
      {
        hostname: organ.host,
        port: organ.port,
        path: '/mcp',
        method: 'POST',
        headers,
        timeout: timeoutMs,
      },
      (res) => {
        let data = '';
        res.on('data', (c) => {
          data += c;
        });
        res.on('end', () => {
          resolve({ status: res.statusCode || 0, headers: res.headers, body: data });
        });
      }
    );
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error(`MCP timeout after ${timeoutMs}ms`));
    });
    req.write(payload);
    req.end();
  });
}

async function ensureSession(organKey) {
  if (!STATEFUL_ORGANS.has(organKey)) return null;

  const existing = sessions.get(organKey);
  if (existing && existing.expires > Date.now()) return existing.id;

  const initBody = {
    jsonrpc: '2.0',
    id: `mcp-apps-init-${Date.now()}`,
    method: 'initialize',
    params: {
      protocolVersion: '2025-03-26',
      capabilities: {},
      clientInfo: { name: 'aaa-mcp-apps-host', version: '1.0.0' },
    },
  };

  const res = await mcpHttp(organKey, { body: initBody });
  const sid = headerGet(res.headers, 'mcp-session-id');
  if (!sid) {
    // Stateless fallback
    return null;
  }

  try {
    await mcpHttp(organKey, {
      body: { jsonrpc: '2.0', method: 'notifications/initialized' },
      sessionId: sid,
    });
  } catch {
    // non-fatal
  }

  sessions.set(organKey, { id: sid, expires: Date.now() + SESSION_TTL_MS });
  return sid;
}

function invalidateSession(organKey) {
  sessions.delete(organKey);
}

function classifyTool(toolName) {
  if (!toolName || typeof toolName !== 'string') {
    return { action: 'hold', reason: 'missing tool name' };
  }
  if (MUTATE_DENYLIST.has(toolName)) {
    return {
      action: 'hold',
      reason: `tool ${toolName} is mutate/seal — requires arifOS lease/gate (not UI OBSERVE)`,
    };
  }
  if (OBSERVE_ALLOWLIST.has(toolName)) {
    return { action: 'observe', reason: 'allowlisted OBSERVE' };
  }
  if (MUTATE_NAME_RE.test(toolName)) {
    return {
      action: 'hold',
      reason: `tool name suggests mutation (${toolName}) — HOLD for arifOS`,
    };
  }
  // Unknown non-mutate: hold closed (least privilege)
  return {
    action: 'hold',
    reason: `tool ${toolName} not on MCP Apps OBSERVE allowlist`,
  };
}

function resolveOrgan(appId, organHint) {
  if (organHint && ORGAN_MAP[organHint]) return organHint;
  if (appId && APP_ORGAN[appId]) return APP_ORGAN[appId];
  // Infer from tool prefix
  return null;
}

function organFromTool(toolName) {
  if (!toolName) return null;
  if (toolName.startsWith('geox_')) return 'geox';
  if (toolName.startsWith('wealth_') || toolName.startsWith('capital_')) return 'wealth';
  if (toolName.startsWith('well_')) return 'well';
  if (toolName.startsWith('arif_') || toolName.startsWith('forge_judge')) return 'arifos';
  if (toolName.startsWith('forge_')) return 'aforge';
  return null;
}

/**
 * Execute a host-mediated tools/call.
 *
 * @param {{ appId?: string, tool: string, arguments?: object, organ?: string, timeoutMs?: number }} input
 * @returns {Promise<object>} guest-safe result envelope
 */
async function handleToolsCall(input = {}) {
  const appId = input.appId || input.app_id || null;
  const toolName = input.tool || input.name || input.toolName;
  const args = input.arguments || input.args || {};
  const timeoutMs = input.timeoutMs || 20000;

  const started = Date.now();
  const classif = classifyTool(toolName);

  const organKey =
    resolveOrgan(appId, input.organ) || organFromTool(toolName) || 'geox';

  const logBase = {
    event: 'mcp_apps_tools_call',
    appId,
    tool: toolName,
    organ: organKey,
    class: classif.action,
    ts: new Date().toISOString(),
  };

  if (classif.action === 'hold') {
    console.info('mcp-apps-tools-call', { ...logBase, status: 'HOLD', reason: classif.reason });
    return {
      ok: false,
      isError: true,
      hold: true,
      policyState: 'hold',
      message: classif.reason,
      tool: toolName,
      appId,
      organ: organKey,
      path: 'aaa-host→arifOS-gate-required',
      ms: Date.now() - started,
    };
  }

  if (!ORGAN_MAP[organKey]) {
    return {
      ok: false,
      isError: true,
      message: `Unknown organ: ${organKey}`,
      tool: toolName,
    };
  }

  try {
    let sessionId = await ensureSession(organKey);

    const callBody = {
      jsonrpc: '2.0',
      id: `mcp-apps-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      method: 'tools/call',
      params: { name: toolName, arguments: args || {} },
    };

    let res = await mcpHttp(organKey, { body: callBody, sessionId, timeoutMs });

    // Session expired / missing → re-init once
    if (
      STATEFUL_ORGANS.has(organKey) &&
      (res.status === 400 || res.status === 404 || /session/i.test(res.body || ''))
    ) {
      invalidateSession(organKey);
      sessionId = await ensureSession(organKey);
      res = await mcpHttp(organKey, { body: callBody, sessionId, timeoutMs });
    }

    let parsed;
    try {
      parsed = parseJsonOrSse(res.body);
    } catch (e) {
      console.info('mcp-apps-tools-call', {
        ...logBase,
        status: 'PARSE_ERROR',
        http: res.status,
        err: e.message,
      });
      return {
        ok: false,
        isError: true,
        message: e.message,
        tool: toolName,
        raw: (res.body || '').slice(0, 500),
        ms: Date.now() - started,
      };
    }

    if (parsed?.error) {
      console.info('mcp-apps-tools-call', {
        ...logBase,
        status: 'MCP_ERROR',
        error: parsed.error.message,
      });
      return {
        ok: false,
        isError: true,
        message: parsed.error.message || 'MCP error',
        code: parsed.error.code,
        data: parsed.error.data,
        tool: toolName,
        organ: organKey,
        ms: Date.now() - started,
      };
    }

    const result = parsed?.result ?? parsed;
    console.info('mcp-apps-tools-call', {
      ...logBase,
      status: 'OK',
      ms: Date.now() - started,
      hasStructured: !!(result && result.structuredContent),
    });

    // Return MCP tools/call result shape so guest applyResult works
    return {
      ok: true,
      isError: !!(result && result.isError),
      policyState: 'observe',
      tool: toolName,
      appId,
      organ: organKey,
      path: 'aaa-host→geox-observe',
      ms: Date.now() - started,
      // Full MCP result for guest
      content: result?.content,
      structuredContent: result?.structuredContent,
      // Flatten structured for convenience (p0-viz uses both)
      ...(result?.structuredContent && typeof result.structuredContent === 'object'
        ? result.structuredContent
        : {}),
      _meta: {
        host: 'aaa-mcp-apps',
        action_class: 'OBSERVE',
        session_bound: !!sessionId,
      },
    };
  } catch (err) {
    console.info('mcp-apps-tools-call', {
      ...logBase,
      status: 'ERROR',
      err: err.message,
    });
    return {
      ok: false,
      isError: true,
      message: err.message || 'tools/call failed',
      tool: toolName,
      organ: organKey,
      ms: Date.now() - started,
    };
  }
}

/**
 * Express mount: POST /api/mcp-apps/tools/call
 * Body: { appId, tool|name, arguments, organ? }
 */
function mountMcpAppsToolsCall(app) {
  app.post('/api/mcp-apps/tools/call', async (req, res) => {
    try {
      const body = req.body || {};
      const result = await handleToolsCall(body);
      // HOLD = policy 403; organ/proxy failure = 502; success = 200
      const httpStatus = result.hold ? 403 : result.ok === false ? 502 : 200;
      res.status(httpStatus).json(result);
    } catch (err) {
      console.error('mcp-apps-tools-call-route', err);
      res.status(500).json({
        ok: false,
        isError: true,
        message: err.message || 'internal error',
      });
    }
  });

  // Discovery / health for the wire
  app.get('/api/mcp-apps/tools/call', (_req, res) => {
    res.json({
      ok: true,
      method: 'POST',
      path: '/api/mcp-apps/tools/call',
      body: { appId: 'well-desk', tool: 'geox_well_desk_open', arguments: { well_id: 'DEMO-01', mode: 'summary' } },
      observe_allowlist: [...OBSERVE_ALLOWLIST],
      mutate_denylist: [...MUTATE_DENYLIST],
      doctrine: 'guest→host→AAA proxy→organ; connect-src none on guest',
    });
  });
}

module.exports = {
  handleToolsCall,
  mountMcpAppsToolsCall,
  classifyTool,
  OBSERVE_ALLOWLIST,
  MUTATE_DENYLIST,
  APP_ORGAN,
};
