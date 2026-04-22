/**
 * A2A Server Tests
 * 
 * Tests for the AAA A2A server implementation.
 * Run with: npx tsx src/lib/a2a/test.ts
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import { createApp } from './server.js';

const BASE_URL = 'http://localhost:3001';

async function wait(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function test(name: string, fn: () => Promise<void>): Promise<void> {
  try {
    await fn();
    console.log(`✅ ${name}`);
  } catch (error) {
    console.error(`❌ ${name}:`, error);
    process.exitCode = 1;
  }
}

async function expectEqual<T>(actual: T, expected: T, message?: string): Promise<void> {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(`${message || 'Assertion failed'}\nExpected: ${JSON.stringify(expected)}\nActual: ${JSON.stringify(actual)}`);
  }
}

async function expectContains(actual: string, expected: string, message?: string): Promise<void> {
  if (!actual.includes(expected)) {
    throw new Error(`${message || 'Contains assertion failed'}\nExpected to contain: ${expected}\nActual: ${actual}`);
  }
}

async function expectStatus(actual: number, expected: number, message?: string): Promise<void> {
  if (actual !== expected) {
    throw new Error(`${message || 'Status assertion failed'}\nExpected: ${expected}\nActual: ${actual}`);
  }
}

async function runTests(): Promise<void> {
  console.log('🧪 Starting A2A Server Tests\n');

  // Start test server
  const app = createApp();
  const server = app.listen(3001, () => {
    console.log('📍 Test server running on port 3001\n');
  });
  
  await wait(500);

  // ── Test 1: Health Check ────────────────────────────────────────────────
  await test('Health check endpoint', async () => {
    const response = await fetch(`${BASE_URL}/health`);
    await expectStatus(response.status, 200);
    
    const data = await response.json() as any;
    await expectEqual(data.status, 'healthy');
    await expectEqual(data.protocol, 'A2A');
    await expectContains(data.motto, 'Ditempa');
  });

  // ── Test 2: Agent Card Discovery ───────────────────────────────────────
  await test('Agent Card at /.well-known/agent.json', async () => {
    const response = await fetch(`${BASE_URL}/.well-known/agent.json`);
    await expectStatus(response.status, 200);
    
    const data = await response.json() as any;
    await expectEqual(data.id, 'aaa-gateway');
    await expectEqual(data.name, 'AAA Gateway');
    await expectContains(data.url, 'aaa.arif-fazil.com');
    await expectEqual(data.capabilities.streaming, true);
  });

  // ── Test 3: Agent Card also at /agent.json ──────────────────────────────
  await test('Agent Card at /agent.json', async () => {
    const response = await fetch(`${BASE_URL}/agent.json`);
    await expectStatus(response.status, 200);
    
    const data = await response.json() as any;
    await expectEqual(data.id, 'aaa-gateway');
  });

  // ── Test 4: Message Send - Basic Task ──────────────────────────────────
  await test('Message/send - basic task', async () => {
    const response = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'Hello A2A agent' }],
            messageId: 'test-msg-001'
          }
        }
      })
    });
    
    await expectStatus(response.status, 200);
    
    const data = await response.json() as any;
    await expectEqual(data.jsonrpc, '2.0');
    await expectContains(data.result.id, 'aaa-');
    await expectEqual(data.result.kind, 'task');
    await expectEqual(data.result.status.state, 'completed');
  });

  // ── Test 5: Message Send - Agent Dispatch Skill ─────────────────────────
  await test('Message/send - agent-dispatch skill', async () => {
    const response = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 2,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'dispatch a task to the planner' }],
            messageId: 'test-msg-002'
          }
        }
      })
    });
    
    await expectStatus(response.status, 200);
    
    const data = await response.json() as any;
    await expectEqual(data.result.status.state, 'completed');
    await expectContains(
      data.result.status.message?.parts[0]?.text || '', 
      'dispatched'
    );
  });

  // ── Test 6: Message Send - Agent Handoff Skill ────────────────────────
  await test('Message/send - agent-handoff skill', async () => {
    const response = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 3,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'handoff to mobility agent' }],
            messageId: 'test-msg-003'
          }
        }
      })
    });
    
    await expectStatus(response.status, 200);
    
    const data = await response.json() as any;
    await expectContains(
      data.result.status.message?.parts[0]?.text || '', 
      'handoff'
    );
  });

  // ── Test 7: Message Send - Status Query Skill ──────────────────────────
  await test('Message/send - status-query skill', async () => {
    const response = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 4,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'check task status' }],
            messageId: 'test-msg-004'
          }
        }
      })
    });
    
    await expectStatus(response.status, 200);
    
    const data = await response.json() as any;
    await expectContains(
      data.result.status.message?.parts[0]?.text || '', 
      'Status query'
    );
  });

  // ── Test 8: Get Task ────────────────────────────────────────────────────
  await test('Get task by ID', async () => {
    // First create a task
    const createResponse = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 5,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'create test task' }],
            messageId: 'test-msg-005'
          }
        }
      })
    });
    
    const createData = await createResponse.json() as any;
    const taskId = createData.result.id;
    
    // Then get it
    const getResponse = await fetch(`${BASE_URL}/tasks/${taskId}`);
    await expectStatus(getResponse.status, 200);
    
    const getData = await getResponse.json() as any;
    await expectEqual(getData.result.id, taskId);
    await expectEqual(getData.result.kind, 'task');
  });

  // ── Test 9: Get Task - Not Found ───────────────────────────────────────
  await test('Get task - not found', async () => {
    const response = await fetch(`${BASE_URL}/tasks/nonexistent-task-id`);
    await expectStatus(response.status, 404);
    
    const data = await response.json() as any;
    await expectEqual(data.error.code, -32001); // TASK_NOT_FOUND
  });

  // ── Test 10: Cancel Task ────────────────────────────────────────────────
  await test('Cancel task', async () => {
    // Create a task
    const createResponse = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 6,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'task to cancel' }],
            messageId: 'test-msg-006'
          }
        }
      })
    });
    
    const createData = await createResponse.json() as any;
    const taskId = createData.result.id;
    
    // Cancel it
    const cancelResponse = await fetch(`${BASE_URL}/tasks/${taskId}/cancel`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 7,
        method: 'tasks/cancel',
        params: {}
      })
    });
    
    await expectStatus(cancelResponse.status, 200);
    
    const cancelData = await cancelResponse.json() as any;
    await expectEqual(cancelData.result.success, true);
  });

  // ── Test 11: Invalid JSON-RPC Version ─────────────────────────────────
  await test('Invalid JSON-RPC version', async () => {
    const response = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '1.0', // Invalid version
        id: 1,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'test' }],
            messageId: 'test-msg-007'
          }
        }
      })
    });
    
    await expectStatus(response.status, 400);
    
    const data = await response.json() as any;
    await expectEqual(data.error.code, -32600); // INVALID_REQUEST
  });

  // ── Test 12: Skills in Agent Card ──────────────────────────────────────
  await test('Agent card has correct skills', async () => {
    const response = await fetch(`${BASE_URL}/.well-known/agent.json`);
    const data = await response.json() as any;
    
    const skills = data.skills as Array<{ id: string; name: string }>;
    await expectContains(skills.map(s => s.id), 'agent-dispatch');
    await expectContains(skills.map(s => s.id), 'agent-handoff');
    await expectContains(skills.map(s => s.id), 'status-query');
  });

  // ── Test 13: Context ID Propagation ────────────────────────────────────
  await test('Context ID is propagated', async () => {
    const customContextId = 'test-context-123';
    
    const response = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 8,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'test context' }],
            messageId: 'test-msg-008'
          },
          contextId: customContextId
        }
      })
    });
    
    const data = await response.json() as any;
    await expectEqual(data.result.contextId, customContextId);
  });

  // ── Test 14: Task ID Reuse ─────────────────────────────────────────────
  await test('Task ID can be provided by client', async () => {
    const customTaskId = 'custom-task-id-abc123';
    
    const response = await fetch(`${BASE_URL}/message/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 9,
        method: 'message/send',
        params: {
          message: {
            role: 'user',
            parts: [{ kind: 'text', text: 'test custom task id' }],
            messageId: 'test-msg-009'
          },
          taskId: customTaskId
        }
      })
    });
    
    const data = await response.json() as any;
    await expectEqual(data.result.id, customTaskId);
  });

  console.log('\n🏁 Tests completed');
  
  server.close(() => {
    console.log('📭 Test server stopped');
    process.exit(process.exitCode || 0);
  });
}

runTests().catch(console.error);