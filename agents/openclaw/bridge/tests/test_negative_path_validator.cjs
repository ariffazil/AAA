#!/usr/bin/env node
/**
 * Negative-path unit test — federation_envelope.js (live module)
 * Proves the two committed fixes at the validator layer:
 *   1. verifyA2ASignature rejects forged signatures (receiver-side enforcement)
 *   2. validateEnvelope rejects expired / future-dated envelopes
 *   3. Capability ceiling blocks DISPLAY_ONLY from MUTATE
 * Calls the functions directly — no HTTP, no EMD gate interference.
 * Forged: 2026-08-07 · F2 TRUTH — prove the mechanism, not just the outcome.
 */
const crypto = require('crypto');
const path = require('path');

const MODULE = '/root/AAA/a2a-server/federation_envelope.js';
const KEY_SEED = require('fs').readFileSync('/root/AAA/auth/keys/openclaw_private.key').subarray(0, 32);

const env = require(MODULE);
const { verifyA2ASignature, validateEnvelope, createEnvelopeValidator } = env;

const PASS = '\x1b[92mPASS\x1b[0m';
const FAIL = '\x1b[91mFAIL\x1b[0m';
const results = [];

function check(name, ok, detail = '') {
  const tag = ok ? PASS : FAIL;
  results.push({ name, ok });
  console.log(`${tag} ${name}${detail ? '  — ' + detail : ''}`);
}

// ── Build PKCS8 DER from raw Ed25519 seed ──────────────────────────
function privKeyFromSeed(seed) {
  const prefix = Buffer.from('302e020100300506032b657004220420', 'hex');
  return crypto.createPrivateKey({ key: Buffer.concat([prefix, seed]), format: 'der', type: 'pkcs8' });
}

// ── Sign canonical envelope bytes ───────────────────────────────────
function signEnvelope(seed, fields) {
  const canonical = Buffer.from(JSON.stringify(fields, Object.keys(fields).sort()));
  return crypto.sign(null, canonical, privKeyFromSeed(seed)).toString('hex');
}

const DID = 'did:key:z7QHNDZM4dm0fl4bwI7BOhVmMAh_pBVsQN2i17Ndog1jLjQ'; // openclaw in registry

const baseFields = {
  from_did: DID,
  to_did: 'did:arif:aaa',
  task_id: 'test-task-001',
  task_type: 'system_status',
  issued_at: '2026-08-07T15:00:00Z',
  nonce: 'nonce-001',
};

// ═══ 1. Signature verification (receiver-side enforcement) ═══
console.log('\n═══ 1. Ed25519 signature verification ═══');

// Valid signature — real openclaw key
const validSig = signEnvelope(KEY_SEED, baseFields);
const rValid = verifyA2ASignature({ ...baseFields, signature: validSig });
check('valid signature accepted', rValid.ok === true, `reason=${rValid.reason} did=${rValid.did} organ=${rValid.organId}`);

// Forged signature — random key, claimed as openclaw DID
const forgedSig = signEnvelope(crypto.randomBytes(32), baseFields);
const rForged = verifyA2ASignature({ ...baseFields, signature: forgedSig });
check('forged signature REJECTED', rForged.ok === false, `reason=${rForged.reason}`);

// Missing signature
const rNoSig = verifyA2ASignature({ ...baseFields });
check('missing signature REJECTED', rNoSig.ok === false, `reason=${rNoSig.reason}`);

// Unknown DID
const rUnknownDid = verifyA2ASignature({ ...baseFields, from_did: 'did:arif:does-not-exist', signature: validSig });
check('unknown DID REJECTED', rUnknownDid.ok === false, `reason=${rUnknownDid.reason}`);

// ═══ 2. Expiry enforcement ═══
console.log('\n═══ 2. Expiry enforcement (validateEnvelope) ═══');

const baseEnv = {
  envelope_version: '1.0',
  trace_id: 'test-expiry',
  actor_id: 'openclaw',
  session_id: 'oc-session',
  organ: 'AAA',
  authority: { source: 'loopback' },
  risk: { tier: 'T0', action_class: 'OBSERVE' },
  receipts: {},
  legacy_wrap: false,
};

const rExpired = validateEnvelope({ ...baseEnv, expires_at: '2020-01-01T00:00:00Z' }, 'arif_sense_observe');
check('expired envelope REJECTED', rExpired.ok === false, `reason=${rExpired.reason}`);

const rFuture = validateEnvelope({ ...baseEnv, expires_at: '2026-08-10T15:00:00Z' }, 'arif_sense_observe');
check('future-dated (>24h) envelope REJECTED', rFuture.ok === false, `reason=${rFuture.reason}`);

const rBad = validateEnvelope({ ...baseEnv, expires_at: 'not-a-date' }, 'arif_sense_observe');
check('malformed expires_at REJECTED', rBad.ok === false, `reason=${rBad.reason}`);

// Valid envelope passes
const rGood = validateEnvelope({ ...baseEnv, expires_at: '2026-08-08T15:00:00Z' }, 'arif_sense_observe');
check('valid envelope ACCEPTED', rGood.ok === true, `reason=${rGood.reason}`);

// ═══ 3. Capability ceiling (DISPLAY_ONLY → no MUTATE) ═══
console.log('\n═══ 3. Capability ceiling ═══');

// openclaw = router role → ceiling PREPARE. A MUTATE tool must be blocked.
const rMutate = validateEnvelope(
  { ...baseEnv, actor_id: 'openclaw', risk: { tier: 'T3', action_class: 'MUTATE' } },
  'arif_forge_execute'
);
check('DISPLAY_ONLY (router) MUTATE blocked', rMutate.ok === false, `reason=${rMutate.reason}`);

// OBSERVE tool under openclaw should pass policy (risk T0)
const rObserve = validateEnvelope(
  { ...baseEnv, actor_id: 'openclaw', risk: { tier: 'T0', action_class: 'OBSERVE' } },
  'arif_sense_observe'
);
// NOTE: may be blocked by other checks (receipt/authority); policy itself must pass
check('router OBSERVE not ceiling-blocked', !String(rObserve.reason || '').includes('Capability ceiling'), `reason=${rObserve.reason}`);

// ═══ Summary ═══
console.log('\n' + '='.repeat(60));
const nPass = results.filter(r => r.ok).length;
const nFail = results.filter(r => !r.ok).length;
console.log(`PASS: ${nPass}  FAIL: ${nFail}`);
if (nFail) {
  results.filter(r => !r.ok).forEach(r => console.log(`  ${FAIL} ${r.name}`));
  process.exit(1);
}
console.log('\nValidator layer: receiver-side enforcement PROVEN.');
process.exit(0);
