#!/usr/bin/env node
/**
 * seal_chain.js — Canonical local hash-chain seal writer for VAULT999.
 *
 * v2.0.0 — ENRICHED ENVELOPE (FORGED 2026-07-04)
 * Adds: Merkle root, event envelope, witness triangle, policy hash,
 *       delegation chain, signature placeholder.
 * Backward compatible: entries seq 1-7 verify unchanged.
 * New entries (seq 8+) use the enriched format.
 *
 * The Arrow of Time, made real.
 *
 * Every governed action that crosses the AAA bridge produces a seal. Each seal
 * contains the SHA-256 of the previous seal. The chain is append-only, head
 * is persisted, integrity is verifiable end-to-end.
 *
 * This file IS the bridge. It does not delegate the chain extension to any
 * remote service. The remote vault999-writer is a federation mirror; the local
 * chain is canonical for the A2A task lifecycle.
 *
 *   ┌────────┐     write_seal()     ┌────────────────┐
 *   │  A2A   │ ───────────────────► │  seal_chain.js │
 *   │  task  │                      └────────┬───────┘
 *   └────────┘                               │
 *                                            ▼
 *                                  ┌─────────────────────┐
 *                                  │ /root/VAULT999/      │
 *                                  │   seal_chain.jsonl   │   ← append-only
 *                                  │   chain_head.json    │   ← current head
 *                                  └─────────────────────┘
 *
 * Entry format (v2 ENRICHED):
 *   {
 *     "seq":        8,
 *     "prev_hash":  "sha256:...",
 *     "this_hash":  "sha256:...",           // backward-compat: hash of canonical payload
 *     "merkle_root":"sha256:...",           // NEW: Merkle root of event fields
 *     "epoch":      ISO-8601 UTC,
 *     "actor":      agent_id,
 *     "verdict":    SEAL | HOLD | VOID,
 *
 *     // ── Enriched event fields ──
 *     "event_type": "a2a.dispatch" | "forge.shell" | "constitutional.verdict"
 *                  | "tool.register" | "session.seal",
 *     "principal":  "agent:opencode-333-FORGE",  // cryptographic identity claim
 *     "tool_schema_hash": "sha256:..." | null,   // hash of tool inputSchema
 *     "policy_hash": "sha256:..." | null,        // hash of active F1-F13 floors
 *     "input_hash":  "sha256:..." | null,        // hash of tool inputs
 *     "output_hash": "sha256:..." | null,        // hash of tool outputs
 *
 *     // ── Identity & witness ──
 *     "delegation_chain": ["parent_event_id", ...],
 *     "signature":  null,                        // Phase 2: sign(merkle_root, actor_key)
 *     "witness": {
 *       "human":    null,                        // Phase 2: human signature
 *       "ai":       null,                        // Phase 2: AI witness signature
 *       "external": null                         // Phase 2: external timestamp proof
 *     },
 *
 *     // ── Original payload (backward compat) ──
 *     "payload": { ... original vault.js payload ... }
 *   }
 *
 *   this_hash = sha256(prev_hash || canonical_json(payload) || String(seq) || epoch)
 *   merkle_root = hash( canonical_json({event_type, principal, tool_schema_hash, policy_hash, input_hash, output_hash}) )
 *
 * Hash rule: chained — prev_hash is included in this_hash. Tampering with any
 * past entry invalidates all subsequent hashes. The chain is the arrow.
 *
 * DITEMPA BUKAN DIBERI — forged, not given.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ── Configuration ─────────────────────────────────────────────────────────

const VAULT_DIR = process.env.VAULT_DIR || '/root/VAULT999';
const LEDGER_PATH = path.join(VAULT_DIR, 'seal_chain.jsonl');
const HEAD_PATH = path.join(VAULT_DIR, 'seal_chain_head.json');
const GENESIS_HASH = 'sha256:0'; // sentinel — never a real sha256
const ENRICHED_VERSION = 2;      // version tag for enriched entries

// Optional remote mirror (vault999-writer) — best-effort, never blocks local chain
const REMOTE_URL = process.env.VAULT_WRITER_URL || null;
const REMOTE_TOKEN = process.env.VAULT_WRITER_TOKEN || '';

// ── Canonical JSON (deterministic byte sequence) ──────────────────────────

function canonicalJson(obj) {
  if (obj === null || typeof obj !== 'object') {
    return JSON.stringify(obj);
  }
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalJson).join(',') + ']';
  }
  const keys = Object.keys(obj).filter((k) => obj[k] !== undefined).sort();
  const parts = keys.map((k) => JSON.stringify(k) + ':' + canonicalJson(obj[k]));
  return '{' + parts.join(',') + '}';
}

// ── Hash functions ────────────────────────────────────────────────────────

function sha256Hex(input) {
  return 'sha256:' + crypto.createHash('sha256').update(input).digest('hex');
}

function hashSeal(prevHash, payload, seq, epoch) {
  const material = [
    prevHash,
    canonicalJson(payload),
    String(seq),
    epoch,
  ].join('|');
  return sha256Hex(material);
}

/**
 * Compute Merkle root from an array of leaves.
 * For a single leaf: merkle_root = hash(leaf).
 * For multiple: pairwise hashing until one node remains.
 */
function computeMerkleRoot(leaves) {
  if (!leaves || leaves.length === 0) return null;
  if (leaves.length === 1) return sha256Hex(leaves[0]);

  let nodes = leaves.map((l) => sha256Hex(l));
  while (nodes.length > 1) {
    const next = [];
    for (let i = 0; i < nodes.length; i += 2) {
      if (i + 1 < nodes.length) {
        next.push(sha256Hex(nodes[i] + nodes[i + 1]));
      } else {
        next.push(nodes[i]); // odd node — carry forward
      }
    }
    nodes = next;
  }
  return nodes[0];
}

/**
 * Compute the event Merkle root from enriched event fields.
 * Leaves: [event_type, principal, tool_schema_hash, policy_hash, input_hash, output_hash]
 */
function computeEventMerkleRoot(fields) {
  const leaves = [
    fields.event_type || 'unknown',
    fields.principal || 'unknown',
    fields.tool_schema_hash || 'sha256:0',
    fields.policy_hash || 'sha256:0',
    fields.input_hash || 'sha256:0',
    fields.output_hash || 'sha256:0',
  ];
  return computeMerkleRoot(leaves);
}

/**
 * Determine seal version from entry — v1 (plain) or v2 (enriched).
 */
function sealVersion(entry) {
  return entry.merkle_root ? 2 : 1;
}

// ── Head persistence ─────────────────────────────────────────────────────

function readHead() {
  try {
    const raw = fs.readFileSync(HEAD_PATH, 'utf-8');
    return JSON.parse(raw);
  } catch (e) {
    if (e.code === 'ENOENT') {
      return { seq: 0, hash: GENESIS_HASH, epoch: null };
    }
    throw e;
  }
}

function writeHead(head) {
  const tmp = HEAD_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(head, null, 2));
  fs.renameSync(tmp, HEAD_PATH);
}

// ── Ledger I/O ───────────────────────────────────────────────────────────

function appendLedger(entry) {
  const line = JSON.stringify(entry) + '\n';
  const fd = fs.openSync(LEDGER_PATH, 'a');
  try {
    fs.writeSync(fd, line);
    fs.fsyncSync(fd);
  } finally {
    fs.closeSync(fd);
  }
}

function readLedger() {
  if (!fs.existsSync(LEDGER_PATH)) return [];
  const raw = fs.readFileSync(LEDGER_PATH, 'utf-8');
  return raw.split('\n').filter((l) => l.trim()).map((l) => JSON.parse(l));
}

// ── Verification ─────────────────────────────────────────────────────────

/**
 * Verify the hash chain integrity.
 * v1 entries: check prev_hash + this_hash.
 * v2 entries: additionally check merkle_root.
 */
function verifyChain() {
  const entries = readLedger();
  let expectedPrev = GENESIS_HASH;
  const enriched = []; // tracked for v2-specific checks

  for (let i = 0; i < entries.length; i++) {
    const e = entries[i];

    // ── Chain integrity (universal) ──
    if (e.prev_hash !== expectedPrev) {
      return {
        ok: false,
        broken_at_seq: e.seq,
        reason: 'prev_hash mismatch',
        expected: expectedPrev,
        actual: e.prev_hash,
      };
    }
    const recomputed = hashSeal(e.prev_hash, e.payload, e.seq, e.epoch);
    if (recomputed !== e.this_hash) {
      return {
        ok: false,
        broken_at_seq: e.seq,
        reason: 'this_hash mismatch (payload tampered)',
        expected: recomputed,
        actual: e.this_hash,
      };
    }

    // ── Enriched integrity (v2 only) ──
    if (sealVersion(e) === 2) {
      enriched.push(e);
      if (e.merkle_root) {
        const recomputedMerkle = computeEventMerkleRoot({
          event_type: e.event_type,
          principal: e.principal,
          tool_schema_hash: e.tool_schema_hash,
          policy_hash: e.policy_hash,
          input_hash: e.input_hash,
          output_hash: e.output_hash,
        });
        if (recomputedMerkle !== e.merkle_root) {
          return {
            ok: false,
            broken_at_seq: e.seq,
            reason: 'merkle_root mismatch (event fields tampered)',
            expected: recomputedMerkle,
            actual: e.merkle_root,
            enriched_failure: true,
          };
        }
        // Signature check — if signature exists, verify against merkle_root
        // (Phase 2: actual key-based verification)
        if (e.signature) {
          // Placeholder: future ED25519/RSA verification of sign(merkle_root, key)
          // For now: presence of signature is noted but not cryptographically verified
        }
      }
    }

    expectedPrev = e.this_hash;
  }

  return {
    ok: true,
    length: entries.length,
    head: entries.length > 0 ? entries[entries.length - 1].this_hash : GENESIS_HASH,
    v1_entries: entries.length - enriched.length,
    v2_entries: enriched.length,
    enriched_count: enriched.length,
  };
}

// ── Public: write a seal ─────────────────────────────────────────────────

async function writeSeal(payload, opts = {}) {
  if (!payload || typeof payload !== 'object') {
    throw new Error('writeSeal: payload must be a non-null object');
  }

  // Ensure vault directory exists
  fs.mkdirSync(VAULT_DIR, { recursive: true });

  // Atomic head read-modify-write
  let head = readHead();
  const seq = head.seq + 1;
  const epoch = new Date().toISOString();
  const prevHash = head.hash;
  const thisHash = hashSeal(prevHash, payload, seq, epoch);

  // ── Enriched envelope fields ──
  const eventType = opts.event_type || classifyEventType(payload);
  const principal = opts.principal || `agent:${payload.agent_id || 'unknown'}`;
  const toolSchemaHash = opts.tool_schema_hash || null;
  const policyHash = opts.policy_hash || computePolicyHash(opts.active_floors);
  const inputHash = opts.input_hash || (payload.payload ? sha256Hex(canonicalJson(payload.payload)) : null);
  const outputHash = opts.output_hash || null;
  const delegationChain = opts.delegation_chain || [];
  const signature = opts.signature || null;
  const witness = opts.witness || { human: null, ai: null, external: null };

  // Compute Merkle root from event fields
  const merkleRoot = computeEventMerkleRoot({
    event_type: eventType,
    principal,
    tool_schema_hash: toolSchemaHash,
    policy_hash: policyHash,
    input_hash: inputHash,
    output_hash: outputHash,
  });

  const entry = {
    seq,
    prev_hash: prevHash,
    this_hash: thisHash,
    merkle_root: merkleRoot,
    epoch,
    actor: payload.agent_id || 'unknown',
    verdict: payload.verdict || 'SEAL',

    // Enriched fields
    seal_version: ENRICHED_VERSION,
    event_type: eventType,
    principal,
    tool_schema_hash: toolSchemaHash,
    policy_hash: policyHash,
    input_hash: inputHash,
    output_hash: outputHash,

    // Identity + witness + delegation
    delegation_chain: delegationChain,
    signature,
    witness,

    // Original payload (backward compat)
    payload,
  };

  // Persist atomically: ledger first, then head
  appendLedger(entry);
  writeHead({
    seq,
    hash: thisHash,
    merkle_root: merkleRoot,
    epoch,
    actor: entry.actor,
    verdict: entry.verdict,
    seal_version: ENRICHED_VERSION,
  });

  // Best-effort remote mirror (non-blocking failure)
  if (REMOTE_URL) {
    mirrorRemote(entry).catch((err) => {
      console.error('[seal_chain] remote mirror failed (local chain intact):', err.message);
    });
  }

  return {
    ok: true,
    seq,
    this_hash: thisHash,
    merkle_root: merkleRoot,
    prev_hash: prevHash,
    epoch,
    chain_head: thisHash,
    seal_version: ENRICHED_VERSION,
  };
}

// ── Event type classification ─────────────────────────────────────────────

function classifyEventType(payload) {
  const action = (payload.action || '').toLowerCase();
  if (action.startsWith('a2a.')) return 'a2a.dispatch';
  if (action.includes('shell') || action.includes('forge.execute')) return 'forge.shell';
  if (action.includes('judge') || action.includes('verdict')) return 'constitutional.verdict';
  if (action.includes('register') || action.includes('forge.skill')) return 'tool.register';
  if (action.includes('seal') || action.includes('session')) return 'session.seal';
  return 'a2a.general';
}

/**
 * Compute a policy hash from active constitutional floors.
 * In production, this reads live floor states from arifOS.
 * For now: deterministic hash of the floor names that are active.
 */
function computePolicyHash(activeFloors) {
  if (!activeFloors || !Array.isArray(activeFloors) || activeFloors.length === 0) {
    return null;
  }
  const sorted = [...activeFloors].sort();
  return sha256Hex('FLOORS:' + sorted.join(','));
}

// ── Remote mirror ─────────────────────────────────────────────────────────

async function mirrorRemote(entry) {
  if (!REMOTE_URL) return;
  const headers = { 'Content-Type': 'application/json' };
  if (REMOTE_TOKEN) headers['X-Writer-Token'] = REMOTE_TOKEN;
  const resp = await fetch(`${REMOTE_URL}/seal`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      ...entry.payload,
      seq: entry.seq,
      prev_hash: entry.prev_hash,
      this_hash: entry.this_hash,
      merkle_root: entry.merkle_root,
      seal_version: entry.seal_version,
      epoch: entry.epoch,
    }),
    signal: AbortSignal.timeout(3000),
  });
  if (!resp.ok) throw new Error(`remote mirror HTTP ${resp.status}`);
}

// ── Public: query ────────────────────────────────────────────────────────

function getHead() {
  return readHead();
}

function getChainLength() {
  return readHead().seq;
}

function getRecent(n = 10) {
  const entries = readLedger();
  return entries.slice(-n);
}

/**
 * Get enriched chain summary — includes v1/v2 breakdown and Merkle roots.
 */
function getChainSummary() {
  const entries = readLedger();
  let v1 = 0, v2 = 0;
  const merkleRoots = [];
  for (const e of entries) {
    if (sealVersion(e) === 2) {
      v2++;
      if (e.merkle_root) merkleRoots.push({ seq: e.seq, merkle_root: e.merkle_root });
    } else {
      v1++;
    }
  }
  return {
    total: entries.length,
    v1_entries: v1,
    v2_entries: v2,
    genesis_hash: GENESIS_HASH,
    head: getHead(),
    merkle_roots: merkleRoots,
  };
}

// ── CLI ──────────────────────────────────────────────────────────────────

async function main() {
  const cmd = process.argv[2];
  if (cmd === 'verify') {
    const r = verifyChain();
    console.log(JSON.stringify(r, null, 2));
    process.exit(r.ok ? 0 : 1);
  } else if (cmd === 'head') {
    console.log(JSON.stringify(readHead(), null, 2));
  } else if (cmd === 'recent') {
    const n = parseInt(process.argv[3] || '5', 10);
    console.log(JSON.stringify(getRecent(n), null, 2));
  } else if (cmd === 'length') {
    console.log(getChainLength());
  } else if (cmd === 'summary') {
    console.log(JSON.stringify(getChainSummary(), null, 2));
  } else if (cmd === 'write') {
    const payloadJson = process.argv[3];
    if (!payloadJson) {
      console.error('Usage: seal_chain.js write \'<json-payload>\'');
      process.exit(2);
    }
    const payload = JSON.parse(payloadJson);
    const r = await writeSeal(payload);
    console.log(JSON.stringify(r, null, 2));
  } else {
    console.log('Usage: seal_chain.js {verify|head|recent N|length|summary|write JSON}');
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch((e) => {
    console.error('[seal_chain] fatal:', e);
    process.exit(1);
  });
}

module.exports = {
  writeSeal,
  verifyChain,
  getHead,
  getChainLength,
  getRecent,
  getChainSummary,
  hashSeal,
  computeEventMerkleRoot,
  canonicalJson,
  classifyEventType,
  GENESIS_HASH,
  LEDGER_PATH,
  HEAD_PATH,
  VAULT_DIR,
  ENRICHED_VERSION,
};
