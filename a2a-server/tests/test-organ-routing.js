#!/usr/bin/env node
/**
 * test-organ-routing.js — Unit Tests for Organ Dispatch Routing
 *
 * Validates resolveOrgan(), dispatchToOrgan(), and explicit metadata routing
 * in server.js without requiring live organs.
 *
 * Run: node tests/test-organ-routing.js
 * Requires: Node 22+, working directory /root/AAA
 *
 * DITEMPA BUKAN DIBERI — Forged 2026-07-20
 */

// Mock the federation gateway BEFORE loading server module
const mockMcpCall = async (organ, method, params) => {
  if (organ === 'fake') throw new Error('connection refused');
  return {
    ok: true,
    result: { status: 'healthy', organ, tool: params?.name, args: params?.arguments },
  };
};

// Inject mock for mcpCall
const federationGateway = require('../federation_gateway');
const originalMcpCall = federationGateway.mcpCall;
federationGateway.mcpCall = mockMcpCall;

const { resolveOrgan, dispatchToOrgan, ORGAN_ROUTING_MAP } = require('../server');

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
  console.log('\n🔬 Testing Organ Dispatch Routing...');
  console.log('─'.repeat(60));

  // ── resolveOrgan tests ──────────────────────────────────────────
  console.log('\n📡 1. resolveOrgan — Keyword Matching\n');

  assert(resolveOrgan('evaluate prospect Alpha') === 'geox', 'prospect → geox');
  assert(resolveOrgan('run basin analysis') === 'geox', 'basin → geox');
  assert(resolveOrgan('seismic inversion') === 'geox', 'seismic → geox');
  assert(resolveOrgan('petrophysics analysis') === 'geox', 'petrophysics → geox');
  assert(resolveOrgan('compute NPV of project') === 'wealth', 'NPV → wealth');
  assert(resolveOrgan('assess capital allocation') === 'wealth', 'capital → wealth');
  assert(resolveOrgan('check portfolio risk') === 'wealth', 'portfolio → wealth');
  assert(resolveOrgan('validate operator vitality') === 'well', 'vitality → well');
  assert(resolveOrgan('assess fatigue levels') === 'well', 'fatigue → well');
  assert(resolveOrgan('guard dignity boundary') === 'well', 'dignity → well');
  assert(resolveOrgan('build and deploy service') === 'aforge', 'build/deploy → aforge');
  assert(resolveOrgan('judge this verdict') === 'arifos', 'judge → arifos');

  // ── Explicit metadata routing ──────────────────────────────────
  console.log('\n📡 2. resolveOrgan — Explicit Metadata Routing\n');

  assert(
    resolveOrgan('generic text', { metadata: { routing: 'geox', tool: 'geox_prospect', args: { prospect_ref: 'X' } } }) === 'geox',
    'metadata routing: geox explicit'
  );
  assert(
    resolveOrgan('generic text', { metadata: { routing: 'wealth', tool: 'capital_health', args: { mode: 'runway' } } }) === 'wealth',
    'metadata routing: wealth explicit'
  );
  assert(
    resolveOrgan('generic text', { metadata: { routing: 'well', tool: 'well_validate_vitality', args: { mode: 'readiness' } } }) === 'well',
    'metadata routing: well explicit'
  );

  // ── Empty params / no match ─────────────────────────────────────
  console.log('\n📡 3. resolveOrgan — Edge Cases\n');

  assert(resolveOrgan('hello world') === 'arifos', 'no keyword match → arifos default');
  assert(resolveOrgan('') === 'arifos', 'empty string → arifos default');
  assert(
    resolveOrgan('generic', { metadata: { routing: 'unknown' } }) === 'arifos',
    'unknown organ key → arifos default'
  );

  // ── dispatchToOrgan ─────────────────────────────────────────────
  console.log('\n📡 4. dispatchToOrgan — Explicit Metadata Dispatch\n');

  const explicitResult = await dispatchToOrgan(
    'test-geox-1',
    { parts: [{ type: 'text', text: 'evaluate prospect Alpha' }] },
    'prospect.evaluate',
    { metadata: { routing: 'geox', tool: 'geox_prospect', args: { prospect_ref: 'Alpha', mode: 'screen' } } }
  );
  assert(explicitResult?.organ === 'geox', 'dispatched to geox');
  assert(explicitResult?.error === undefined, 'no error');

  // ── dispatch with no metadata → keyword fallback ─────────────────
  const keywordResult = await dispatchToOrgan(
    'test-well-1',
    { parts: [{ type: 'text', text: 'check operator readiness' }] },
    'readiness.check',
    {}
  );
  assert(keywordResult?.organ === 'well', 'keyword → well');
  assert(keywordResult?.error === undefined, 'no error');

  // ── Unmatched free text → arifos default (always matches) ─────
  const defaultResult = await dispatchToOrgan(
    'test-unknown-1',
    { parts: [{ type: 'text', text: 'random words' }] },
    'unknown.skill',
    {}
  );
  assert(defaultResult?.organ === 'arifos', 'unmatched free text → arifos default dispatch');

  // ── Summary ─────────────────────────────────────────────────────
  console.log('\n' + '═'.repeat(60));
  console.log(`📊 RESULTS: ${passed} passed · ${failed} failed · ${passed + failed} total`);
  console.log('═'.repeat(60));

  // Restore mcpCall
  federationGateway.mcpCall = originalMcpCall;

  if (failed > 0) {
    console.log(`\n⚠️  ${failed} test(s) FAILED — review output above`);
    process.exit(1);
  }
  console.log('\n✅ Organ dispatch routing validated.\n');
  process.exit(0);
}

run().catch((err) => {
  console.error(`${FAIL} — Unhandled error: ${err.message}`);
  console.error(err.stack);
  process.exit(1);
});
