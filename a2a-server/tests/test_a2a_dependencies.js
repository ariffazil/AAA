#!/usr/bin/env node
/**
 * test_a2a_dependencies.js — Unit Test for A2A Dependency Enforcement
 */

const { bridgeTask, validateExplorerDependencies } = require('../a2a-mcp-bridge');
const { validateExplorerDependencies: validateEnvelopeDependencies } = require('../federation_envelope');

const PASS = '✅ PASS';
const FAIL = '❌ FAIL';
let passed = 0;
let failed = 0;

function assert(condition, label, detail) {
  if (condition) {
    console.log(`${PASS} — ${label}`);
    passed++;
  } else {
    console.log(`${FAIL} — ${label}${detail ? `\n       ${detail}` : ''}`);
    failed++;
  }
}

async function run() {
  console.log('\n🔬 Testing A2A Dependency Enforcement...');

  // Test 1: wealth_compute_npv without parent_seal_hash (Should fail)
  const taskNoHash = {
    params: {
      id: 'test-dep-no-hash',
      metadata: {
        skill: 'capital.compute',
        routing: 'wealth',
        tool: 'wealth_compute_npv',
        args: {
          cash_flows: [-1000, 200, 300, 400, 500],
          discount_rate: 0.1
        }
      }
    }
  };

  const resNoHash = await bridgeTask(taskNoHash);
  assert(
    resNoHash.result.status.state === 'FAILED',
    'Reject wealth_compute_npv without parent_seal_hash'
  );
  assert(
    resNoHash.result.status.error.message.includes('Dependency violation'),
    'Error message matches dependency violation description',
    resNoHash.result.status.error.message
  );

  // Test 2: wealth_compute_npv WITH parent_seal_hash (Should bypass dependency check)
  const taskWithHash = {
    params: {
      id: 'test-dep-with-hash',
      metadata: {
        skill: 'capital.compute',
        routing: 'wealth',
        tool: 'wealth_compute_npv',
        args: {
          cash_flows: [-1000, 200, 300, 400, 500],
          discount_rate: 0.1,
          provenance: {
            parent_seal_hash: 'seal-1234567890abcdef'
          }
        }
      }
    }
  };

  const resWithHash = await bridgeTask(taskWithHash);
  // It will bypass the dependency check and either succeed (if organ is up) or fail due to network/refusal,
  // but it should NOT fail with "Dependency violation".
  assert(
    resWithHash.result.status.state !== 'FAILED' || !resWithHash.result.status.error.message.includes('Dependency violation'),
    'Bypass dependency violation block when parent_seal_hash is present',
    resWithHash.result.status.error?.message
  );

  // Test 3: arif_forge_execute with judge_state_hash should not be blocked by explorer dependency gate
  const forgeDepCheck = validateExplorerDependencies('arifos', 'arif_forge_execute', {
    judge_state_hash: 'sha256:abcd1234'
  });
  assert(
    forgeDepCheck.ok === true,
    'Allow arif_forge_execute with judge_state_hash',
    forgeDepCheck.error
  );

  // Test 4: mapped concrete explorer tools must still validate through federation envelope rules
  const envelopeDepCheck = validateEnvelopeDependencies('wealth_compute_npv', { receipts: {} });
  assert(
    envelopeDepCheck.ok === false && envelopeDepCheck.reason.includes('EXPLORER_DEPENDENCY_HOLD'),
    'Reject mapped concrete explorer tool without upstream sealed receipts',
    envelopeDepCheck.reason
  );

  console.log(`\n📊 RESULTS: ${passed} passed · ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
