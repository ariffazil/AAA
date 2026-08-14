/**
 * Wake Bus — unit tests (publish/subscribe round-trip via real NATS)
 * 
 * Tests:
 *   1. publishWake() publishes to NATS
 *   2. subscribeWakes() receives matching wakes
 *   3. subscribeWakes() ignores non-matching agents
 *   4. getWakeStreamDepth() returns non-negative
 * 
 * Requires: NATS server at nats://localhost:4222
 */

import { publishWake, subscribeWakes, getWakeStreamDepth, WakeReason } from '../src/gateway/wake_bus.js';
import type { WakePayload } from '../src/gateway/wake_bus.js';

const PASSED = '✅';
const FAILED = '❌';
let passed = 0;
let failed = 0;

function assert(condition: boolean, msg: string): void {
  if (condition) {
    console.log(`  ${PASSED} ${msg}`);
    passed++;
  } else {
    console.error(`  ${FAILED} ${msg}`);
    failed++;
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function testPublishAndSubscribe(): Promise<void> {
  console.log('\n[TEST 1] publishWake + subscribeWakes round-trip');

  const received: WakePayload[] = [];
  const unsub = await subscribeWakes('test-agent-1', (wake) => {
    received.push(wake);
  });

  // Publish 2 wakes for this agent
  await publishWake('test-agent-1', WakeReason.ASSIGNMENT_CREATED, { issue: 42 }, 'test-source');
  await publishWake('test-agent-1', WakeReason.COMMENT_ADDED, { comment: 'hello' }, 'test-source');

  // Wait for delivery
  await sleep(2000);

  assert(received.length === 2, `received 2 wakes (got ${received.length})`);
  if (received.length >= 1) {
    assert(received[0].reason === WakeReason.ASSIGNMENT_CREATED, 'first wake reason = assignment_created');
    assert(received[0].target_agent === 'test-agent-1', 'target_agent correct');
    assert(received[0].payload?.issue === 42, 'payload preserved');
  }
  if (received.length >= 2) {
    assert(received[1].reason === WakeReason.COMMENT_ADDED, 'second wake reason = comment_added');
  }

  unsub();
}

async function testIsolationBetweenAgents(): Promise<void> {
  console.log('\n[TEST 2] Agent isolation — wrong agent gets nothing');

  const receivedA: WakePayload[] = [];
  const receivedB: WakePayload[] = [];

  const unsubA = await subscribeWakes('agent-alpha', (w) => receivedA.push(w));
  const unsubB = await subscribeWakes('agent-beta', (w) => receivedB.push(w));

  // Publish to alpha only
  await publishWake('agent-alpha', WakeReason.SOVEREIGN_SUMMONS, {}, 'test');
  await sleep(1500);

  assert(receivedA.length === 1, `alpha received 1 (got ${receivedA.length})`);
  assert(receivedB.length === 0, `beta received 0 (got ${receivedB.length})`);

  unsubA();
  unsubB();
}

async function testStreamDepth(): Promise<void> {
  console.log('\n[TEST 3] getWakeStreamDepth()');

  const depth = await getWakeStreamDepth();
  assert(depth.message_count >= 0, `message_count >= 0 (got ${depth.message_count})`);
  assert(depth.byte_size >= 0, `byte_size >= 0 (got ${depth.byte_size})`);
  assert(typeof depth.last_message_at === 'string' || depth.last_message_at === null,
    `last_message_at is string or null`);
}

async function testAllWakeReasons(): Promise<void> {
  console.log('\n[TEST 4] All wake reasons publish successfully');

  const reasons = Object.values(WakeReason);
  const received: WakePayload[] = [];
  const unsub = await subscribeWakes('test-all-reasons', (w) => received.push(w));

  for (const reason of reasons) {
    await publishWake('test-all-reasons', reason, { reason_test: true }, 'test');
  }

  await sleep(3000);
  assert(received.length === reasons.length, `received all ${reasons.length} reasons (got ${received.length})`);

  unsub();
}

async function main(): Promise<void> {
  console.log('=== Wake Bus Tests (live NATS) ===\n');

  try {
    await testPublishAndSubscribe();
    await testIsolationBetweenAgents();
    await testStreamDepth();
    await testAllWakeReasons();
  } catch (err) {
    console.error('\n[ERROR]', err);
    failed++;
  }

  console.log(`\n=== RESULTS: ${passed} passed, ${failed} failed ===`);
  process.exit(failed > 0 ? 1 : 0);
}

main();
