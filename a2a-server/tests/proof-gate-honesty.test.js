#!/usr/bin/env node
/**
 * proof-gate-honesty.test.js — D1 regression guard (FI-003, 2026-09-29).
 *
 * SCAR: on 2026-09-29 a live probe found the A2A wire emitting
 *   proof: { pass: true, score: 0.85, detail: 'ZKPC_OBSERVATION' }
 * as a hardcoded literal in every response, on a host with zero ZK circuitry
 * (circom/halo2/gnark absent, no .circom/.r1cs/.zkey on disk). Foreign
 * federation agents consumed that score as a proof assertion.
 * That is a REPRESENTATION failure, not a capability gap: a system that lacks
 * a capability and a system that claims one it lacks are different failures.
 * See /root/AAA/docs/ZKPC-CANONICAL-DOCTRINE.md "What ZKPC Cannot Prove" and
 * /root/AAA/instructions/recovery-reality-cache.md §7 (disk reality over
 * nominal claims).
 *
 * Invariants enforced here (scoped to the D1 ask — misleading ZKPC labels):
 *   I1  No gate may pair pass:true with a ZKPC_* label unless attested:true.
 *   I2  Every proof gate must carry an explicit attestation field.
 *   I3  The ZKPC_* vocabulary must not reappear hardcoded on this wire.
 *   I4  Honesty must not be reached by deleting the proof gate.
 *
 * DELIBERATELY NOT asserted here: the other nine gates are also hardcoded
 * (presence:"LIVE", energy:"default cost", sovereign:"no F13 halt"). That is a
 * real finding — registered as D6 — but relabelling nine gates is a wider wire
 * contract change than D1 authorised, so it is reported, not silently patched.
 *
 * Method: server.js exposes no module boundary (5.7k-line monolith), so the
 * gate literals are extracted from source and evaluated — locking the shipped
 * wire shape without importing the whole server.
 *
 * Run: node tests/proof-gate-honesty.test.js   (exit 0 = pass, 1 = fail)
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const SERVER = path.join(__dirname, '..', 'server.js');
const src = fs.readFileSync(SERVER, 'utf8');

let failures = 0;
const ok = (m) => console.log(`  PASS  ${m}`);
const bad = (m) => { console.log(`  FAIL  ${m}`); failures++; };

// ── extract every `const apexGates = { ... };` literal ──────────────────────
const blocks = [];
const marker = 'const apexGates = {';
let i = 0;
while ((i = src.indexOf(marker, i)) !== -1) {
  const start = i + marker.length - 1;
  let depth = 0;
  let j = start;
  for (; j < src.length; j++) {
    if (src[j] === '{') depth++;
    else if (src[j] === '}') { depth--; if (depth === 0) break; }
  }
  blocks.push(src.slice(start, j + 1));
  i = j + 1;
}

if (blocks.length === 0) bad('no `const apexGates = {` block found in server.js');
else ok(`found ${blocks.length} apexGates literal block(s)`);

const parsed = [];
// Block #0 interpolates a computed runtime value (detail: invariant.reason), so
// the sandbox supplies an opaque marker instead of throwing ReferenceError.
const SANDBOX = { invariant: { reason: '<COMPUTED_AT_RUNTIME>' } };
for (const [n, b] of blocks.entries()) {
  try {
    parsed.push({ n, gates: vm.runInNewContext(`(${b})`, SANDBOX) });
  } catch (e) {
    bad(`block #${n} is not an evaluable object literal: ${e.message}`);
  }
}

// ── I1 / I2 ─────────────────────────────────────────────────────────────────
for (const { n, gates } of parsed) {
  for (const [name, g] of Object.entries(gates)) {
    const label = String(g.detail ?? '');
    const zkClaim = /ZKPC/i.test(label);
    const assertsPass = g.pass === true;

    if (zkClaim && assertsPass && g.attested !== true) {
      bad(`block #${n} gate "${name}": asserts pass:true under a ZKPC label `
        + `(detail="${label}") while attested=${JSON.stringify(g.attested)} `
        + '— claims a proof the host cannot compute');
    } else if (name === 'proof' && g.attested === undefined) {
      bad(`block #${n} proof gate carries no "attested" field — the wire must `
        + 'state whether the value was measured');
    } else if (zkClaim && g.attested !== true) {
      bad(`block #${n} gate "${name}": ZKPC label present without attested:true`);
    } else {
      ok(`block #${n} gate "${name}": pass=${JSON.stringify(assertsPass)} `
        + `attested=${JSON.stringify(g.attested)} label="${label.slice(0, 44)}"`);
    }
  }
}

// ── I3 ──────────────────────────────────────────────────────────────────────
const zkHits = (src.match(/ZKPC_OBSERVATION|ZKPC_AUDIT|ZKPC_CERTAINTY|ZKPC_NONE/g) || []);
if (zkHits.length > 0) {
  bad(`ZKPC_* vocabulary still hardcoded on this wire (${zkHits.length} occurrence(s))`);
} else {
  ok('no ZKPC_* literal remains in server.js');
}

// ── guard: the honesty must not be achieved by deleting the gate ────────────
for (const { n, gates } of parsed) {
  if (!('proof' in gates)) {
    bad(`block #${n} has no proof gate at all — honesty was reached by `
      + 'silently dropping the gate, which hides the gap instead of declaring it');
  } else {
    ok(`block #${n} still declares a proof gate (gap visible, not hidden)`);
  }
}

console.log(`\nproof-gate-honesty: ${failures === 0 ? 'PASS' : 'FAIL'} (${failures} failure(s))`);
process.exit(failures === 0 ? 0 : 1);
