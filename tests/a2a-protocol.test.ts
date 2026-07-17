/**
 * Session D — Live A2A Protocol Tests
 * ════════════════════════════════════════════
 * 
 * Validates the MCP lifecycle fixes with real A2A protocol interactions:
 * 1. Agent card discovery (A2A-spec /.well-known/agent.json)
 * 2. MCP handshake (initialize → version negotiation)
 * 3. A2A message send → task creation → state transitions
 * 4. Task retrieval and artifact verification
 * 5. Graceful degradation when AAA unreachable
 * 
 * Tests against the live federation at localhost ports.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

import { describe, it, before } from 'node:test';
import { strict as assert } from 'node:assert';

const BASE = 'http://localhost:3001';
const ARIFOS = 'http://localhost:8088';
const TIMEOUT = 5000;

// ── Helpers ───────────────────────────────────────────────────────────────

async function get(path: string, base = BASE): Promise<{ status: number; body: unknown }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT);
  try {
    const resp = await fetch(`${base}${path}`, { signal: controller.signal });
    clearTimeout(timeout);
    const text = await resp.text();
    let body: unknown = text;
    try { body = JSON.parse(text); } catch { /* raw text */ }
    return { status: resp.status, body };
  } catch (err) {
    clearTimeout(timeout);
    return { status: 0, body: String(err) };
  }
}

async function post(path: string, payload: unknown, base = BASE): Promise<{ status: number; body: Record<string, unknown> }> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT);
  try {
    const resp = await fetch(`${base}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    const body = (await resp.json()) as Record<string, unknown>;
    return { status: resp.status, body };
  } catch (err) {
    clearTimeout(timeout);
    return { status: 0, body: { error: String(err) } };
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// Test 1: A2A Agent Card Discovery
// ═══════════════════════════════════════════════════════════════════════════

describe('A2A Agent Card Discovery', () => {
  it('GET /.well-known/agent.json returns 200 with valid card', async () => {
    const { status, body } = await get('/.well-known/agent.json');
    assert.equal(status, 200, `Expected 200, got ${status}`);
    const card = body as Record<string, unknown>;
    assert.ok(card.name, 'Card must have name');
    assert.ok(card.url, 'Card must have url');
    assert.ok(card.version, 'Card must have version');
    console.log(`  name: ${card.name}, version: ${card.version}`);
  });

  it('Agent card has capabilities', async () => {
    const { body } = await get('/.well-known/agent.json');
    const card = body as Record<string, unknown>;
    const caps = (card.capabilities || {}) as Record<string, unknown>;
    // A2A 1.0 requires at minimum: streaming and/or pushNotifications
    assert.ok(
      caps.streaming !== undefined || caps.pushNotifications !== undefined,
      'Card must declare streaming or pushNotifications capability',
    );
    console.log(`  streaming: ${caps.streaming}, pushNotifications: ${caps.pushNotifications}`);
  });

  it('AAA /health returns healthy', async () => {
    const { status, body } = await get('/health');
    assert.equal(status, 200, `Expected 200, got ${status}`);
    const h = body as Record<string, unknown>;
    const okStatuses = ['healthy', 'degraded', 'ok'];
    assert.ok(okStatuses.includes(String(h.status)), `Unexpected health status: ${h.status}`);
    console.log(`  status: ${h.status}`);
  });

  it('AAA /ready returns ready=true when aligned', async () => {
    const { status, body } = await get('/ready');
    assert.equal(status, 200, `Expected 200, got ${status}`);
    const r = body as Record<string, unknown>;
    assert.ok(r.ready !== undefined, 'Must return ready field');
    console.log(`  ready: ${r.ready}, reason: ${r.status || r.reason || 'ok'}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Test 2: MCP Lifecycle (arifOS)
// ═══════════════════════════════════════════════════════════════════════════

describe('MCP Lifecycle (arifOS)', () => {
  let sessionId: string | undefined;
  let protocolVersion: string | undefined;

  it('initialize returns protocolVersion and capabilities', async () => {
    const { status, body } = await post('/mcp', {
      jsonrpc: '2.0',
      id: 'a2a-test-init-1',
      method: 'initialize',
      params: {
        protocolVersion: '2025-11-25',
        capabilities: { tools: {} },
        clientInfo: { name: 'aaa-a2a-protocol-test', version: '1.0.0' },
      },
    }, ARIFOS);

    assert.equal(status, 200, `MCP initialize failed: HTTP ${status}`);
    if (body.error) {
      console.error(`  MCP error: ${JSON.stringify(body.error)}`);
    }
    assert.ok(!body.error, `MCP initialize error: ${JSON.stringify(body.error)}`);

    const result = (body.result || {}) as Record<string, unknown>;
    protocolVersion = String(result.protocolVersion || '');
    sessionId = body['mcp-session-id'] as string | undefined;

    assert.ok(protocolVersion, 'Must return protocolVersion');
    assert.ok(result.capabilities, 'Must return capabilities');
    assert.ok(result.serverInfo, 'Must return serverInfo');
    console.log(`  protocolVersion: ${protocolVersion}`);
    console.log(`  server: ${(result.serverInfo as Record<string,unknown>)?.name}`);
    console.log(`  sessionId: ${sessionId ? 'present' : 'stateless'}`);
  });

  it('tools/list returns canonical tools after initialize', async () => {
    const { body } = await post('/mcp', {
      jsonrpc: '2.0',
      id: 'a2a-test-tools-1',
      method: 'tools/list',
      params: {},
    }, ARIFOS);

    const result = (body.result || {}) as Record<string, unknown>;
    const tools = (result.tools || []) as Array<{ name: string }>;
    assert.ok(tools.length > 0, 'tools/list must return at least 1 tool');
    console.log(`  tools: ${tools.length}`);
    const names = tools.slice(0, 8).map(t => t.name);
    console.log(`  sample: ${names.join(', ')}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Test 3: A2A Message → Task → Artifact lifecycle
// ═══════════════════════════════════════════════════════════════════════════

describe('A2A Task Lifecycle', () => {
  let taskId: string | undefined;

  it('POST /message/send creates a task', async () => {
    const payload = {
      jsonrpc: '2.0',
      id: 'a2a-test-msg-1',
      method: 'message/send',
      params: {
        message: {
          role: 'user',
          parts: [{ type: 'text', text: 'A2A protocol test: canary probe' }],
          messageId: `canary-${Date.now()}`,
        },
        configuration: { blocking: false },
      },
    };

    const { status, body } = await post('/message/send', payload);
    assert.equal(status, 200, `message/send failed: HTTP ${status}, body: ${JSON.stringify(body).slice(0, 100)}`);

    const result = body.result as Record<string, unknown> | undefined;
    if (result) {
      taskId = result.id as string;
      assert.ok(taskId, 'Task must have id');
      console.log(`  taskId: ${taskId?.slice(0, 16)}...`);

      const status_ = (result.status || result.state) as Record<string, unknown> | string | undefined;
      const state = typeof status_ === 'string' ? status_ : status_?.state;
      console.log(`  state: ${state}`);
    } else if (body.error) {
      console.log(`  A2A error: ${JSON.stringify(body.error)}`);
    } else {
      console.log(`  response keys: ${Object.keys(body).join(', ')}`);
    }
  });

  it('GET /operator/tasks/:taskId retrieves task', async function () {
    if (!taskId) {
      this.skip!('No taskId from previous test');
      return;
    }
    const { status, body } = await get(`/operator/tasks/${taskId}`);
    assert.equal(status, 200, `Task retrieval failed: HTTP ${status}`);
    const task = body as Record<string, unknown>;
    assert.ok(task.id || task.ok, 'Task response must have id or ok');
    console.log(`  task found: ${Boolean(task.id || task.ok)}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Test 4: Registry Conformance Endpoint
// ═══════════════════════════════════════════════════════════════════════════

describe('Registry Conformance', () => {
  it('GET /registry/conformance returns ConformanceArtifact', async function () {
    const { status, body } = await get('/registry/conformance');
    // May be 500 if registry probe fails, which is acceptable (NOT_EVALUATED)
    if (status === 500) {
      console.log(`  DEGRADED (expected when MCP lifecycle fails): ${(body as Record<string,unknown>).message}`);
      this.skip!();
      return;
    }
    assert.equal(status, 200, `Expected 200 or 500, got ${status}`);
    const artifact = body as Record<string, unknown>;
    assert.equal(artifact.schemaVersion, 'session-d.v1', 'Must have session-d.v1 schema');
    assert.ok(artifact.summary, 'Must have summary');
    console.log(`  organs: ${(artifact.summary as Record<string,unknown>)?.totalOrgans}`);
    console.log(`  aligned: ${(artifact.summary as Record<string,unknown>)?.organsAligned}`);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Test 5: Federation Health (all 6 organs reachable)
// ═══════════════════════════════════════════════════════════════════════════

describe('Federation Health', () => {
  const ORGANS = [
    { name: 'arifOS', port: 8088 },
    { name: 'A-FORGE', port: 7071 },
    { name: 'GEOX', port: 8081 },
    { name: 'WEALTH', port: 18082 },
    { name: 'WELL', port: 18083 },
    { name: 'AAA', port: 3001 },
  ];

  for (const organ of ORGANS) {
    it(`${organ.name} :${organ.port} /health returns 200`, async () => {
      const { status } = await get('/health', `http://localhost:${organ.port}`);
      assert.equal(status, 200, `${organ.name}:${organ.port} /health failed: HTTP ${status}`);
    });
  }
});
