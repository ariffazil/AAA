#!/usr/bin/env node
/**
 * safety-proxy/test.js — Constitutional Test Suite
 * =================================================
 * Tests the hermes_safety_proxy middleware, policy engine, and JITU tokens.
 *
 * Run: node safety-proxy/test.js
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

'use strict';

const { classifyAction, isReadOnlyMode, TIERS } = require('./policy');
const { createJituToken, validateJituToken, hashPayload } = require('./jitu_token');

let passed = 0;
let failed = 0;
let total = 0;

function assert(condition, name) {
  total++;
  if (condition) {
    passed++;
    console.log(`  ✅ ${name}`);
  } else {
    failed++;
    console.error(`  ❌ ${name}`);
  }
}

function assertEqual(actual, expected, name) {
  assert(actual === expected, `${name} (got: ${actual}, expected: ${expected})`);
}

// ── Policy Engine Tests ───────────────────────────────────────────────────

console.log('\n═══ POLICY ENGINE ═══');

// AUTO_PASS: read-only tools
console.log('\n── AUTO_PASS (read-only tools) ──');
assertEqual(classifyAction({ tool_name: 'forge_probe' }).tier, TIERS.AUTO_PASS, 'forge_probe → AUTO_PASS');
assertEqual(classifyAction({ tool_name: 'forge_health_check' }).tier, TIERS.AUTO_PASS, 'forge_health_check → AUTO_PASS');
assertEqual(classifyAction({ tool_name: 'forge_registry_status' }).tier, TIERS.AUTO_PASS, 'forge_registry_status → AUTO_PASS');
assertEqual(classifyAction({ tool_name: 'forge_search' }).tier, TIERS.AUTO_PASS, 'forge_search → AUTO_PASS');
assertEqual(classifyAction({ tool_name: 'forge_fetch' }).tier, TIERS.AUTO_PASS, 'forge_fetch → AUTO_PASS');
assertEqual(classifyAction({ tool_name: 'forge_memory' }).tier, TIERS.AUTO_PASS, 'forge_memory → AUTO_PASS');
assertEqual(classifyAction({ tool_name: 'forge_shell_dryrun' }).tier, TIERS.AUTO_PASS, 'forge_shell_dryrun → AUTO_PASS');
assertEqual(classifyAction({ tool_name: 'forge_chart' }).tier, TIERS.AUTO_PASS, 'forge_chart → AUTO_PASS');

// JITU_REQUIRED: write/execute tools
console.log('\n── JITU_REQUIRED (write/execute tools) ──');
assertEqual(classifyAction({ tool_name: 'forge_shell' }).tier, TIERS.JITU_REQUIRED, 'forge_shell → JITU_REQUIRED');
assertEqual(classifyAction({ tool_name: 'forge_execute' }).tier, TIERS.JITU_REQUIRED, 'forge_execute → JITU_REQUIRED');
assertEqual(classifyAction({ tool_name: 'forge_pipeline_run' }).tier, TIERS.JITU_REQUIRED, 'forge_pipeline_run → JITU_REQUIRED');
assertEqual(classifyAction({ tool_name: 'forge_register' }).tier, TIERS.JITU_REQUIRED, 'forge_register → JITU_REQUIRED');
assertEqual(classifyAction({ tool_name: 'forge_skill' }).tier, TIERS.JITU_REQUIRED, 'forge_skill → JITU_REQUIRED');
assertEqual(classifyAction({ tool_name: 'forge_seal' }).tier, TIERS.JITU_REQUIRED, 'forge_seal → JITU_REQUIRED');
assertEqual(classifyAction({ tool_name: 'forge_github_create_issue' }).tier, TIERS.JITU_REQUIRED, 'forge_github_create_issue → JITU_REQUIRED');

// DENY: blocked tools
console.log('\n── DENY (blocked tools) ──');
assertEqual(classifyAction({ tool_name: 'forge_approve' }).tier, TIERS.DENY, 'forge_approve → DENY (cannot self-authorize)');

// DENY: destructive commands
console.log('\n── DENY (destructive commands) ──');
assertEqual(classifyAction({ command: 'rm -rf /var/data' }).tier, TIERS.DENY, 'rm -rf /var/data → DENY');
assertEqual(classifyAction({ command: 'DROP DATABASE production' }).tier, TIERS.DENY, 'DROP DATABASE → DENY');
assertEqual(classifyAction({ command: 'chmod 777 /etc/passwd' }).tier, TIERS.DENY, 'chmod 777 → DENY');
assertEqual(classifyAction({ command: 'iptables -F' }).tier, TIERS.DENY, 'iptables -F → DENY');
assertEqual(classifyAction({ command: 'ufw disable' }).tier, TIERS.DENY, 'ufw disable → DENY');

// FORCE_DENY: even with JITU, blocked
console.log('\n── FORCE_DENY (irreversible) ──');
assertEqual(classifyAction({ command: 'git push --force origin main' }).tier, TIERS.DENY, 'force push main → DENY');
assertEqual(classifyAction({ command: 'shutdown now' }).tier, TIERS.DENY, 'shutdown → DENY');
assertEqual(classifyAction({ command: 'reboot' }).tier, TIERS.DENY, 'reboot → DENY');
assertEqual(classifyAction({ command: 'mkfs.ext4 /dev/sda' }).tier, TIERS.DENY, 'mkfs → DENY');

// JITU_REQUIRED: write commands
console.log('\n── JITU_REQUIRED (write commands) ──');
assertEqual(classifyAction({ command: 'git push origin main' }).tier, TIERS.JITU_REQUIRED, 'git push → JITU_REQUIRED');
assertEqual(classifyAction({ command: 'systemctl restart nginx' }).tier, TIERS.JITU_REQUIRED, 'systemctl restart → JITU_REQUIRED');
assertEqual(classifyAction({ command: 'docker rm container1' }).tier, TIERS.JITU_REQUIRED, 'docker rm → JITU_REQUIRED');
assertEqual(classifyAction({ command: 'npm install express' }).tier, TIERS.JITU_REQUIRED, 'npm install → JITU_REQUIRED');
assertEqual(classifyAction({ command: 'apt-get install nginx' }).tier, TIERS.JITU_REQUIRED, 'apt install → JITU_REQUIRED');

// Action class-based classification
console.log('\n── Action class classification ──');
assertEqual(classifyAction({ action_class: 'OBSERVE' }).tier, TIERS.AUTO_PASS, 'OBSERVE → AUTO_PASS');
assertEqual(classifyAction({ action_class: 'SEARCH' }).tier, TIERS.AUTO_PASS, 'SEARCH → AUTO_PASS');
assertEqual(classifyAction({ action_class: 'MUTATE' }).tier, TIERS.JITU_REQUIRED, 'MUTATE → JITU_REQUIRED');
assertEqual(classifyAction({ action_class: 'EXECUTE' }).tier, TIERS.JITU_REQUIRED, 'EXECUTE → JITU_REQUIRED');
assertEqual(classifyAction({ action_class: 'IRREVERSIBLE' }).tier, TIERS.DENY, 'IRREVERSIBLE → DENY');

// Safe default for unknown
console.log('\n── Safe default ──');
assertEqual(classifyAction({ tool_name: 'unknown_tool_xyz' }).tier, TIERS.JITU_REQUIRED, 'Unknown tool → JITU_REQUIRED (safe default)');

// Read-only mode detection
console.log('\n── Read-only mode detection ──');
assert(isReadOnlyMode('forge_filesystem', { mode: 'read' }), 'forge_filesystem read → read-only');
assert(!isReadOnlyMode('forge_filesystem', { mode: 'write' }), 'forge_filesystem write → NOT read-only');
assert(isReadOnlyMode('forge_git', { mode: 'status' }), 'forge_git status → read-only');
assert(isReadOnlyMode('forge_git', { mode: 'diff' }), 'forge_git diff → read-only');
assert(!isReadOnlyMode('forge_git', { mode: 'commit' }), 'forge_git commit → NOT read-only');
assert(isReadOnlyMode('forge_docker', { mode: 'ps' }), 'forge_docker ps → read-only');
assert(!isReadOnlyMode('forge_docker', { mode: 'exec' }), 'forge_docker exec → NOT read-only');
assert(isReadOnlyMode('forge_postgres', { mode: 'query', mutate: false }), 'forge_postgres query(!mutate) → read-only');
assert(!isReadOnlyMode('forge_postgres', { mode: 'query', mutate: true }), 'forge_postgres query(mutate) → NOT read-only');
assert(isReadOnlyMode('forge_vault', { mode: 'read' }), 'forge_vault read → read-only');
assert(!isReadOnlyMode('forge_vault', { mode: 'write' }), 'forge_vault write → NOT read-only');

// ── JITU Token Tests ──────────────────────────────────────────────────────

console.log('\n═══ JITU TOKENS ═══');

// Create and validate
console.log('\n── Create & Validate ──');
const payload = { tool_name: 'forge_shell', actor_id: 'opencode-333', arguments: { command: 'ls -la' } };
const payloadHash = hashPayload(payload.arguments);

const { token, expires_at } = createJituToken({
  tool_name: payload.tool_name,
  actor_id: payload.actor_id,
  payload_hash: payloadHash,
  approval_type: 'AUTO_JITU',
});

assert(typeof token === 'string' && token.startsWith('jitu_v1.'), 'Token format is jitu_v1.*');
assert(new Date(expires_at) > new Date(), 'Token expires in the future');

const validation = validateJituToken(token, {
  tool_name: payload.tool_name,
  actor_id: payload.actor_id,
  payload_hash: payloadHash,
});
assert(validation.valid, 'Token validates with correct context');
assertEqual(validation.payload.tool, 'forge_shell', 'Token payload contains tool name');
assertEqual(validation.payload.actor, 'opencode-333', 'Token payload contains actor');

// Tool mismatch
console.log('\n── Binding checks ──');
const mismatch1 = validateJituToken(token, { tool_name: 'forge_execute' });
assert(!mismatch1.valid, 'Rejects on tool mismatch');
assertEqual(mismatch1.error, 'TOOL_MISMATCH', 'Error is TOOL_MISMATCH');

const mismatch2 = validateJituToken(token, { actor_id: 'different-agent' });
assert(!mismatch2.valid, 'Rejects on actor mismatch');
assertEqual(mismatch2.error, 'ACTOR_MISMATCH', 'Error is ACTOR_MISMATCH');

// Invalid token
console.log('\n── Invalid tokens ──');
assert(!validateJituToken(null).valid, 'null token → invalid');
assert(!validateJituToken('').valid, 'empty token → invalid');
assert(!validateJituToken('garbage').valid, 'garbage token → invalid');
assert(!validateJituToken('jitu_v1.dGVzdA.bad_sig').valid, 'bad signature → invalid');

// Sovereign token
console.log('\n── Sovereign token ──');
const { token: sovToken } = createJituToken({
  tool_name: 'forge_shell',
  actor_id: 'arif-sovereign',
  payload_hash: payloadHash,
  approval_type: 'SOVEREIGN_JITU',
  sovereign_id: '888',
  seal_id: 'seal-123',
});
const sovValidation = validateJituToken(sovToken);
assert(sovValidation.valid, 'Sovereign token validates');
assertEqual(sovValidation.payload.type, 'SOVEREIGN_JITU', 'Sovereign token type is SOVEREIGN_JITU');
assertEqual(sovValidation.payload.iss, '888', 'Sovereign issuer is 888');
assertEqual(sovValidation.payload.seal, 'seal-123', 'Sovereign token has seal ID');

// ── Summary ───────────────────────────────────────────────────────────────

console.log('\n═══════════════════════════════════════');
console.log(`  Total: ${total} | Passed: ${passed} | Failed: ${failed}`);
console.log('═══════════════════════════════════════');

if (failed > 0) {
  console.error('\n  ⚠️  SOME TESTS FAILED — review before deploying.\n');
  process.exit(1);
} else {
  console.log('\n  ✅ ALL TESTS PASSED — safety proxy ready.\n');
  process.exit(0);
}
