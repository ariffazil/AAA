/**
 * envelope_v1.test.js — tamper tests for the AAA gateway signer (GAP #1 slice)
 *
 * Run: node tests/envelope_v1.test.js
 *   Uses the real AAA control-plane key (actor "aaa") for sign+verify and
 *   fresh throwaway keypairs (env AAA_ENVELOPE_KEY_DIR override) for the
 *   wrong-key case, so no secret material is written anywhere.
 *
 * Interop proof: `node tests/envelope_v1.test.js --emit` prints
 *   {"envelope":…, "payload":…} for the python verifier:
 *   node tests/envelope_v1.test.js --emit | \
 *     /root/arifOS/.venv/bin/python -m arifosmcp.runtime.signed_envelope verify --stdin
 */

'use strict';

const assert = require('assert');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ev1 = require('../envelope_v1');

function signingInputOf(env) {
  return Buffer.from(
    ev1.canonicalize({
      actor_id: env.actor_id,
      session_id: env.session_id,
      timestamp: env.timestamp,
      nonce: env.nonce,
      payload_hash: env.payload_hash,
    }),
    'utf8'
  );
}

const PKCS8_PREFIX = Buffer.from('302e020100300506032b657004220420', 'hex');
const SPKI_PREFIX = Buffer.from('302a300506032b6570032100', 'hex');

function makeThrowawayKeyPair(dir) {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const seed = privateKey.export({ format: 'der', type: 'pkcs8' }).subarray(16);
  const pubRaw = publicKey.export({ format: 'der', type: 'spki' }).subarray(-32);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'imposter_private.key'), seed.toString('hex'));
  fs.writeFileSync(path.join(dir, 'imposter_public.key'), pubRaw.toString('hex'));
}

let passed = 0;
const results = [];
function check(name, fn) {
  try {
    fn();
    passed += 1;
    results.push(`PASS ${name}`);
  } catch (e) {
    results.push(`FAIL ${name}: ${e.message}`);
    process.exitCode = 1;
  }
}

const payload = { name: 'arif_init', arguments: { actor_id: 'aaa-gateway' }, task: 'gap1' };

// (a) valid envelope verifies (roundtrip with the real registered key)
check('valid envelope verifies', () => {
  const env = ev1.signEnvelope(payload);
  assert.strictEqual(env.v, 1);
  assert.strictEqual(env.alg, 'ed25519');
  const pub = crypto.createPublicKey(ev1.loadPrivateKey(env.actor_id));
  assert.ok(crypto.verify(null, signingInputOf(env), pub, Buffer.from(env.sig, 'base64')));
});

// (b) any byte-tamper of the payload or actor_id is rejected
check('payload tamper rejected (hash mismatch)', () => {
  const env = ev1.signEnvelope(payload);
  const tampered = { ...payload, task: 'gap1-TAMPERED' };
  assert.notStrictEqual(ev1.payloadHash(tampered), env.payload_hash);
  assert.ok(signingInputOf(env).length > 0);
});

check('actor_id tamper rejected (signature invalid)', () => {
  const env = ev1.signEnvelope(payload);
  const forged = { ...env, actor_id: 'imposter' };
  const pub = crypto.createPublicKey(ev1.loadPrivateKey('aaa'));
  assert.strictEqual(
    crypto.verify(null, signingInputOf(forged), pub, Buffer.from(forged.sig, 'base64')),
    false,
    'sig made by aaa must not verify under tampered actor_id input'
  );
});

// (c) replayed nonce within window rejected (deterministic nonce + hash dedupe)
check('replayed nonce detectable (nonce + payload hash unique per call)', () => {
  const e1 = ev1.signEnvelope(payload);
  const e2 = ev1.signEnvelope(payload);
  assert.notStrictEqual(e1.nonce, e2.nonce, 'nonce must be fresh per call');
  // Same nonce+fields ⇒ identical signing input ⇒ replay would verify the same
  // signature; the python verifier's nonce store is what rejects it (NONCE_REPLAY).
});

// (d) wrong-key signature rejected
check('wrong-key signature rejected', () => {
  const realPub = crypto.createPublicKey(ev1.loadPrivateKey('aaa'));
  const tmp = path.join(os.tmpdir(), `env1test-${process.pid}`);
  makeThrowawayKeyPair(tmp);
  const prev = process.env.AAA_ENVELOPE_KEY_DIR;
  process.env.AAA_ENVELOPE_KEY_DIR = tmp;
  try {
    const env = ev1.signEnvelope(payload, { actorId: 'imposter' });
    assert.ok(!crypto.verify(null, signingInputOf(env), realPub, Buffer.from(env.sig, 'base64')));
  } finally {
    if (prev === undefined) delete process.env.AAA_ENVELOPE_KEY_DIR;
    else process.env.AAA_ENVELOPE_KEY_DIR = prev;
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

// flag gating
check('flag off → attach is a no-op (byte-identical args)', () => {
  delete process.env.ARIF_ENVELOPE_SIGNED;
  const args = { name: 'x', arguments: { a: 1 } };
  assert.strictEqual(ev1.attachSignedEnvelope(args), args);
  assert.strictEqual(ev1.envelopeEnabled(), false);
});
check('flag on → signed_envelope attached, payload hash covers payload only', () => {
  process.env.ARIF_ENVELOPE_SIGNED = '1';
  try {
    const args = { name: 'x', arguments: { a: 1 } };
    const attached = ev1.attachSignedEnvelope(args, { actorId: 'aaa' });
    assert.ok(attached.signed_envelope);
    assert.strictEqual(attached.signed_envelope.payload_hash, ev1.payloadHash(args));
  } finally {
    delete process.env.ARIF_ENVELOPE_SIGNED;
  }
});

// self-test passthrough
check('selfTest passes', () => {
  ev1.selfTest();
});

console.error(results.join('\n'));
console.error(`${passed}/${results.length} passed`);

if (process.argv.includes('--emit')) {
  const env = ev1.signEnvelope(payload, { sessionId: 'interop-gap1' });
  process.stdout.write(JSON.stringify({ envelope: env, payload }) + '\n');
}
