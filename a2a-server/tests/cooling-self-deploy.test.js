#!/usr/bin/env node
/**
 * cooling-self-deploy.test.js — COOLING_RECEIPT_SPEC_v1 §4 ingress gate.
 *
 * Ships the spec §9 checklist items:
 *   - Register COOLING_RECEIPT as valid VAULT999 envelope type (classifier)
 *   - Add governance.self_deploy: false constraint to ingress gate (INV-C5)
 *   - Test: cooling receipt cannot self-deploy (reject, no append)
 *   - Test: cooling receipt routes correctly through governance (INV-C4 intact)
 *
 * Isolation: VAULT_DIR → mkdtemp BEFORE require (paths computed at load).
 * VAULT_WRITER_URL cleared so no mirror fires. No real vault mutation —
 * the negative paths must prove NO append; the positive paths write only
 * to the temp ledger.
 *
 * Run: node tests/cooling-self-deploy.test.js
 * Exit 0 = all assertions pass, 1 = any failure.
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

// ── Isolation (MUST precede require — module reads env at load) ──────────
const TMP_VAULT = fs.mkdtempSync(path.join(os.tmpdir(), 'cooling-gate-vault-'));
process.env.VAULT_DIR = TMP_VAULT;
delete process.env.VAULT_WRITER_URL;
delete process.env.TSA_URL;
delete process.env.TSA_USERNAME;
delete process.env.TSA_PASSWORD;

const sc = require('../seal_chain.js');

const LEDGER = path.join(TMP_VAULT, 'seal_chain.jsonl');

let failures = 0;
function check(name, cond, detail) {
  if (cond) {
    console.log(`  ok   ${name}`);
  } else {
    failures += 1;
    console.log(`  FAIL ${name}${detail ? ` — ${detail}` : ''}`);
  }
}

function ledgerLines() {
  if (!fs.existsSync(LEDGER)) return 0;
  return fs.readFileSync(LEDGER, 'utf-8').trim().split('\n').filter(Boolean).length;
}

function readEntries() {
  if (!fs.existsSync(LEDGER)) return [];
  return fs.readFileSync(LEDGER, 'utf-8').trim().split('\n').filter(Boolean).map(JSON.parse);
}

// A-FORGE coolingVerbs craftCoolingReceipt envelope shape (flat, event_type,
// no `action`, governance_path but NO governance block) — the live emitter.
function aforgeEnvelope(extra = {}) {
  return {
    seal_version: 3,
    event_type: 'cooling.receipt',
    epoch: new Date().toISOString(),
    action_class: 'OBSERVE',
    caller: 'hermes-prime',
    actor: 'hermes-prime',
    session_id: 'sess-cooling-test-001',
    context_id: 'ctx-cooling-test-001',
    original_seal_seq: 40,
    original_verdict: { verdict: 'SEAL', judge_hash: 'sha256:deadbeef', judge_summary: 'test' },
    drift_detected: { present: true, observations: [{ dimension: 'test', delta: 'n/a', epistemic_label: 'OBS', severity: 'INFO' }] },
    proposed_improvement: { hypothesis: 'gate test', evidence: 'unit', epistemic_label: 'INT' },
    governance_path: { target_organ: 'arifOS', target_floor: 'F13', required_authority: '888_HOLD', judge_required: true, reason: 'test' },
    supersedes: { seal_seq: 40, type: 'COLD_LINK', note: 'lineage only' },
    witness: { human: null, ai: 'hermes-prime', external: null },
    metadata: {},
    ...extra,
  };
}

async function main() {
  console.log(`temp vault: ${TMP_VAULT}`);

  // ── 1. Classifier: declared event_type wins for cooling ────────────────
  console.log('\n[1] classifier recognizes A-FORGE cooling envelope');
  const cls = sc.classifyEventType(aforgeEnvelope());
  check('A-FORGE envelope → cooling.receipt', cls === 'cooling.receipt', `got ${cls}`);
  const clsAction = sc.classifyEventType({ action: 'a2a.tasks.send' });
  check('a2a action path unchanged', clsAction === 'a2a.dispatch', `got ${clsAction}`);
  const clsCoolAction = sc.classifyEventType({ action: 'cooling.receipt' });
  check('legacy action-field cooling still cooling', clsCoolAction === 'cooling.receipt', `got ${clsCoolAction}`);

  // ── 2. validateCooling INV-C5: self_deploy truthy → rejected ───────────
  console.log('\n[2] INV-C5 rejects self-deploy declarations');
  const vTrue = sc.validateCooling(aforgeEnvelope({ governance: { self_deploy: true } }), {});
  check('self_deploy:true → rejected', vTrue.rejected === true, JSON.stringify(vTrue.violations));
  check('INV-C5 named in violations', vTrue.violations.some(v => v.invariant === 'INV-C5_SELF_DEPLOY'));
  const vStr = sc.validateCooling(aforgeEnvelope({ governance: { self_deploy: 'true' } }), {});
  check("self_deploy:'true' (string) → rejected", vStr.rejected === true);
  const vFalse = sc.validateCooling(aforgeEnvelope({ governance: { self_deploy: false } }), {});
  check('self_deploy:false → accepted', vFalse.rejected === false);
  const vAbsent = sc.validateCooling(aforgeEnvelope(), {});
  check('governance absent → accepted (emitters may omit; ingress stamps)', vAbsent.rejected === false);
  const vNested = sc.validateCooling({ event_type: 'cooling.receipt', action_class: 'OBSERVE', caller: 'x', payload: { governance: { self_deploy: true } } }, {});
  check('nested payload.governance.self_deploy:true → rejected', vNested.rejected === true);

  // ── 3. INV-C4 preserved (routes through governance) ────────────────────
  console.log('\n[3] INV-C4 governance routing intact');
  const vGov = sc.validateCooling(
    aforgeEnvelope({ governance_path: { required_authority: '888_HOLD', judge_required: false } }),
    {}
  );
  check('judge_required:false + 888_HOLD → INV-C4 fires', vGov.violations.some(v => v.invariant === 'INV-C4_GOVERNANCE_PATH'));

  // ── 4. writeSeal REJECT: throws before ANY ledger work ─────────────────
  console.log('\n[4] writeSeal rejects self_deploy:true with zero append');
  const before = ledgerLines();
  let threw = false;
  let errMsg = '';
  try {
    await sc.writeSeal(aforgeEnvelope({ governance: { self_deploy: true } }));
  } catch (e) {
    threw = true;
    errMsg = String(e.message);
  }
  check('writeSeal throws', threw, 'resolved instead of throwing');
  check('error names INV-C5_SELF_DEPLOY', errMsg.includes('INV-C5_SELF_DEPLOY'), errMsg.slice(0, 200));
  check('ledger line count unchanged', ledgerLines() === before, `before=${before} after=${ledgerLines()}`);

  // ── 5. writeSeal ACCEPT: lands stamped, classified, validated ───────────
  console.log('\n[5] writeSeal accepts live A-FORGE envelope shape');
  const r = await sc.writeSeal(aforgeEnvelope());
  check('writeSeal ok', r.ok === true, JSON.stringify(r).slice(0, 300));
  check('cooling validated', r.cooling_validated === true);
  check('not downgraded', r.cooling_downgraded === false, JSON.stringify(r.cooling_violations));
  const entries = readEntries();
  const e = entries[entries.length - 1];
  check('entry event_type = cooling.receipt', e.event_type === 'cooling.receipt', `got ${e.event_type}`);
  check('entry payload.governance.self_deploy stamped false', e.payload && e.payload.governance && e.payload.governance.self_deploy === false, JSON.stringify(e.payload && e.payload.governance));
  check('entry governance_path preserved (routing intact)', e.payload && e.payload.governance_path && e.payload.governance_path.judge_required === true);
  check('entry action_class preserved OBSERVE', e.payload && e.payload.action_class === 'OBSERVE');

  // ── 6. Explicit self_deploy:false accepted, unchanged ──────────────────
  console.log('\n[6] explicit self_deploy:false accepted');
  const r2 = await sc.writeSeal(aforgeEnvelope({ governance: { self_deploy: false, routed_to_judge: false } }));
  check('writeSeal ok', r2.ok === true);
  const e2 = readEntries()[ledgerLines() - 1];
  check('self_deploy stays false', e2.payload.governance.self_deploy === false);

  // ── 7. INV-C1 downgrade semantics preserved (not rejected) ─────────────
  console.log('\n[7] INV-C1 action_class=MUTATE downgrades, does NOT throw');
  let threw7 = false;
  try {
    await sc.writeSeal(aforgeEnvelope({ action_class: 'MUTATE' }));
  } catch (e7) {
    threw7 = true;
  }
  check('MUTATE-class cooling still lands (downgrade, ratified semantics)', threw7 === false);
  const e3 = readEntries()[ledgerLines() - 1];
  check('INV-C1 violation recorded on entry',
    Array.isArray(e3.invariants_violated) && e3.invariants_violated.some(v => String(v.invariant).startsWith('INV-C1')),
    JSON.stringify(e3.invariants_violated));

  // ── 8. Non-cooling path regression ─────────────────────────────────────
  console.log('\n[8] non-cooling seal path unchanged');
  const r8 = await sc.writeSeal({ action: 'a2a.tasks.send', agent_id: 'aaa-gateway', session_id: 'sess-8', context_id: 'ctx-8', verdict: 'SEAL', witness: { human: 'w', ai: null, external: null } });
  check('a2a write ok', r8.ok === true);
  const e8 = readEntries()[ledgerLines() - 1];
  check('a2a entry event_type a2a.dispatch', e8.event_type === 'a2a.dispatch', `got ${e8.event_type}`);
  check('no governance stamp on non-cooling', !(e8.payload && e8.payload.governance && 'self_deploy' in e8.payload.governance));

  // ── Summary ────────────────────────────────────────────────────────────
  console.log(`\n${failures === 0 ? 'ALL PASS' : `${failures} FAILURE(S)`} — temp vault: ${TMP_VAULT}`);
  process.exit(failures === 0 ? 0 : 1);
}

main().catch(e => {
  console.error('FATAL:', e);
  process.exit(1);
});
