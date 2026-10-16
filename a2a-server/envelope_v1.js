/**
 * envelope_v1.js — SIGNED-ENVELOPE v1 signer (AAA gateway side)
 *
 * GAP #1 slice: "Verified actor binding end-to-end".
 * Spec: /root/arifOS/arifosmcp/docs/SIGNED-ENVELOPE-v1.md
 * Python verifier: /root/arifOS/arifosmcp/runtime/signed_envelope.py
 *
 * Flag: ARIF_ENVELOPE_SIGNED=1. Flag off → attachSignedEnvelope is a no-op and
 * outbound tool calls are byte-identical to before.
 *
 * Key: /root/AAA/auth/keys/{actor}_private.key — 32-byte Ed25519 seed, hex
 * (0600, gitignored). Default actor: "aaa" (AAA control-plane DID,
 * did:arif:aaa — "signs ingress capsules" per /root/AAA/auth/did_registry.yaml).
 *
 * Zero npm dependencies (node:crypto only).
 */

'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const ENVELOPE_VERSION = 1;
const ENVELOPE_ALG = 'ed25519';
const ENVELOPE_FIELD = 'signed_envelope';

// PKCS8 DER prefix for an Ed25519 private key (RFC 8410): the 32-byte seed is
// appended raw, so a hex seed file becomes a real KeyObject with no deps.
const PKCS8_ED25519_PREFIX = Buffer.from('302e020100300506032b657004220420', 'hex');

function keyDir() {
  return process.env.AAA_ENVELOPE_KEY_DIR || '/root/AAA/auth/keys';
}

function envelopeEnabled() {
  return process.env.ARIF_ENVELOPE_SIGNED === '1';
}

function defaultActor() {
  return process.env.ARIF_ENVELOPE_ACTOR || 'aaa';
}

/** CANON: UTF-8 JSON, recursively sorted keys, compact separators (spec §3). */
function canonicalize(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(',')}]`;
  if (value !== null && typeof value === 'object') {
    const keys = Object.keys(value).sort();
    return `{${keys.map((k) => `${JSON.stringify(k)}:${canonicalize(value[k])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function payloadHash(payload) {
  return crypto.createHash('sha256').update(Buffer.from(canonicalize(payload), 'utf8')).digest('hex');
}

function loadPrivateKey(actorId) {
  const file = path.join(keyDir(), `${actorId}_private.key`);
  const hex = fs.readFileSync(file, 'utf8').trim();
  const seed = Buffer.from(hex, 'hex');
  if (seed.length !== 32) {
    throw new Error(`envelope_v1: ${file} is not a 32-byte hex seed`);
  }
  const der = Buffer.concat([PKCS8_ED25519_PREFIX, seed]);
  return crypto.createPrivateKey({ key: der, format: 'der', type: 'pkcs8' });
}

/**
 * Build a complete SIGNED-ENVELOPE v1 for `payload`.
 * Options: actorId (default env ARIF_ENVELOPE_ACTOR || 'aaa'), sessionId.
 */
function signEnvelope(payload, { actorId, sessionId } = {}) {
  const actor_id = actorId || defaultActor();
  const session_id = sessionId == null ? '' : String(sessionId);
  const timestamp = Math.floor(Date.now() / 1000);
  const nonce = crypto.randomBytes(16).toString('hex');
  const pHash = payloadHash(payload);
  const signingInput = Buffer.from(
    canonicalize({ actor_id, session_id, timestamp, nonce, payload_hash: pHash }),
    'utf8'
  );
  const sig = crypto.sign(null, signingInput, loadPrivateKey(actor_id));
  return {
    v: ENVELOPE_VERSION,
    alg: ENVELOPE_ALG,
    actor_id,
    session_id,
    timestamp,
    nonce,
    payload_hash: pHash,
    sig: sig.toString('base64'),
  };
}

/**
 * Flag-gated attach for outbound tools/call arguments. Returns the SAME
 * arguments object with `signed_envelope` added when the flag is on;
 * unchanged when off.
 */
function attachSignedEnvelope(toolArgs, opts = {}) {
  if (!envelopeEnabled()) return toolArgs;
  if (!toolArgs || typeof toolArgs !== 'object') return toolArgs;
  const payload = { ...toolArgs };
  delete payload[ENVELOPE_FIELD];
  const envelope = signEnvelope(payload, opts);
  return { ...toolArgs, [ENVELOPE_FIELD]: envelope };
}

/** Self-test (node tests/envelope_v1.test.js): sign → local verify roundtrip. */
function selfTest() {
  const payload = { prompt: 'apa khabar', n: 3, nested: { b: 2, a: 1 } };
  const env = signEnvelope(payload, { actorId: process.env.ARIF_ENVELOPE_ACTOR || 'aaa' });
  const signingInput = Buffer.from(
    canonicalize({
      actor_id: env.actor_id,
      session_id: env.session_id,
      timestamp: env.timestamp,
      nonce: env.nonce,
      payload_hash: env.payload_hash,
    }),
    'utf8'
  );
  const pub = crypto.createPublicKey(loadPrivateKey(env.actor_id));
  const ok = crypto.verify(null, signingInput, pub, Buffer.from(env.sig, 'base64'));
  if (!ok) throw new Error('selfTest: signature did not verify');
  // CANON determinism: sorted keys survive re-serialization.
  const a = canonicalize({ b: 2, a: 1, c: { z: 1, y: [2, 1] } });
  const b = canonicalize({ c: { y: [2, 1], z: 1 }, a: 2 - 1, b: 1 + 1 });
  if (a !== b) throw new Error('selfTest: canonicalize not deterministic');
  if (payloadHash(payload) !== payloadHash({ nested: { a: 1, b: 2 }, n: 3, prompt: 'apa khabar' })) {
    throw new Error('selfTest: payload hash not order-insensitive');
  }
  return env;
}

module.exports = {
  ENVELOPE_FIELD,
  ENVELOPE_VERSION,
  attachSignedEnvelope,
  canonicalize,
  envelopeEnabled,
  loadPrivateKey,
  payloadHash,
  selfTest,
  signEnvelope,
};
