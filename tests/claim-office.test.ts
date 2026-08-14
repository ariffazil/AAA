/**
 * Claim Office — unit tests
 * 
 * Tests:
 *   1. Single claim succeeds
 *   2. Two concurrent claims → exactly one wins (409 teaching denial)
 *   3. Expired TTL → reclaimable
 *   4. Release by owner succeeds
 *   5. Release by non-owner fails
 *   6. getClaimStatus returns correct state
 */

import { ClaimOffice } from '../src/gateway/claim_office.js';
import { mkdtempSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

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

function sleep(ms: number): void {
  const end = Date.now() + ms;
  while (Date.now() < end) { /* sync spin */ }
}

function makeTempOffice(): ClaimOffice {
  const tmpDir = mkdtempSync(join(tmpdir(), 'claim-office-test-'));
  return new ClaimOffice(tmpDir);
}

async function testSingleClaim(): Promise<void> {
  console.log('\n[TEST 1] Single claim succeeds');
  const office = makeTempOffice();

  const result = office.claimWork('work-001', 'agent-alpha', 300);
  assert(result.claimed === true, 'claimed=true');
  assert(result.owner === 'agent-alpha', 'owner = agent-alpha');
  assert(result.claim_id !== undefined, 'claim_id present');
  assert(result.expires_at !== undefined, 'expires_at present');
}

async function testDoubleClaim(): Promise<void> {
  console.log('\n[TEST 2] Double claim → exactly one wins (teaching denial)');
  const office = makeTempOffice();

  const first = office.claimWork('work-002', 'agent-alpha', 300);
  assert(first.claimed === true, 'first claim succeeds');

  const second = office.claimWork('work-002', 'agent-beta', 300);
  assert(second.claimed === false, 'second claim denied');
  assert(second.owner === 'agent-alpha', 'denial shows current owner');
  assert(second.teaching !== undefined, 'teaching denial present');
  assert(second.teaching?.current_owner === 'agent-alpha', 'teaching shows owner');
  assert(second.teaching?.wait_seconds > 0, 'teaching shows wait_seconds');
  assert(second.teaching?.hint.includes('agent-alpha'), 'teaching hint mentions owner');
}

async function testExpiredReclaim(): Promise<void> {
  console.log('\n[TEST 3] Expired TTL → reclaimable');
  const office = makeTempOffice();

  // Claim with 1-second TTL
  const first = office.claimWork('work-003', 'agent-alpha', 1);
  assert(first.claimed === true, 'initial claim succeeds');

  // Wait for expiry
  sleep(1200);

  // Now claim again
  const second = office.claimWork('work-003', 'agent-beta', 300);
  assert(second.claimed === true, 're-claim after expiry succeeds');
  assert(second.owner === 'agent-beta', 'new owner = agent-beta');
}

async function testReleaseByOwner(): Promise<void> {
  console.log('\n[TEST 4] Release by owner succeeds');
  const office = makeTempOffice();

  office.claimWork('work-004', 'agent-alpha', 300);
  const released = office.releaseClaim('work-004', 'agent-alpha');
  assert(released === true, 'release returns true');

  const status = office.getClaimStatus('work-004');
  assert(status === null, 'no active claim after release');
}

async function testReleaseByNonOwner(): Promise<void> {
  console.log('\n[TEST 5] Release by non-owner fails');
  const office = makeTempOffice();

  office.claimWork('work-005', 'agent-alpha', 300);
  const released = office.releaseClaim('work-005', 'agent-beta');
  assert(released === false, 'non-owner release returns false');

  // Claim still active
  const status = office.getClaimStatus('work-005');
  assert(status !== null, 'claim still active');
  assert(status?.owner === 'agent-alpha', 'owner unchanged');
}

async function testGetClaimStatus(): Promise<void> {
  console.log('\n[TEST 6] getClaimStatus returns correct state');
  const office = makeTempOffice();

  const before = office.getClaimStatus('work-006');
  assert(before === null, 'null before any claim');

  office.claimWork('work-006', 'agent-alpha', 300);
  const during = office.getClaimStatus('work-006');
  assert(during !== null, 'non-null after claim');
  assert(during?.owner === 'agent-alpha', 'correct owner');
  assert(during?.claimed === true, 'claimed=true');

  office.releaseClaim('work-006', 'agent-alpha');
  const after = office.getClaimStatus('work-006');
  assert(after === null, 'null after release');
}

async function main(): Promise<void> {
  console.log('=== Claim Office Tests ===\n');

  try {
    await testSingleClaim();
    await testDoubleClaim();
    await testExpiredReclaim();
    await testReleaseByOwner();
    await testReleaseByNonOwner();
    await testGetClaimStatus();
  } catch (err) {
    console.error('\n[ERROR]', err);
    failed++;
  }

  console.log(`\n=== RESULTS: ${passed} passed, ${failed} failed ===`);
  process.exit(failed > 0 ? 1 : 0);
}

main();
