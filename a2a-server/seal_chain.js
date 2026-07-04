#!/usr/bin/env node
/**
 * seal_chain.js — Canonical local hash-chain seal writer for VAULT999.
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
 * Each entry:
 *   {
 *     "seq":        42,
 *     "prev_hash":  "sha256:..." | "sha256:0" (genesis),
 *     "this_hash":  "sha256:...",
 *     "payload":    { ... canonical seal ... },
 *     "epoch":      ISO-8601 UTC timestamp,
 *     "actor":      agent_id,
 *     "verdict":    SEAL | HOLD | VOID,
 *   }
 *
 *   this_hash = sha256(prev_hash || canonical_json(payload) || seq || epoch)
 *
 * Hash rule: chained — prev_hash is included in the hash. Tampering with any
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

// Optional remote mirror (vault999-writer) — best-effort, never blocks local chain
const REMOTE_URL = process.env.VAULT_WRITER_URL || null;
const REMOTE_TOKEN = process.env.VAULT_WRITER_TOKEN || '';

// ── Canonical JSON (deterministic byte sequence) ──────────────────────────

function canonicalJson(obj) {
  // Match JSON.stringify semantics: null, undefined, primitives
  if (obj === null || typeof obj !== 'object') {
    return JSON.stringify(obj);
  }
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalJson).join(',') + ']';
  }
  // Object: include own enumerable keys, but skip undefined values
  // (matches JSON.stringify which strips undefined). This guarantees
  // canonicalJson(x) === canonicalJson(JSON.parse(JSON.stringify(x))).
  const keys = Object.keys(obj).filter((k) => obj[k] !== undefined).sort();
  const parts = keys.map((k) => JSON.stringify(k) + ':' + canonicalJson(obj[k]));
  return '{' + parts.join(',') + '}';
}

// ── Hash function ────────────────────────────────────────────────────────

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
  // fsync per write — power-loss durability
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

function verifyChain() {
  const entries = readLedger();
  let expectedPrev = GENESIS_HASH;
  for (let i = 0; i < entries.length; i++) {
    const e = entries[i];
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
    expectedPrev = e.this_hash;
  }
  return {
    ok: true,
    length: entries.length,
    head: entries.length > 0 ? entries[entries.length - 1].this_hash : GENESIS_HASH,
  };
}

// ── Public: write a seal ─────────────────────────────────────────────────

async function writeSeal(payload) {
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

  const entry = {
    seq,
    prev_hash: prevHash,
    this_hash: thisHash,
    payload,
    epoch,
    actor: payload.agent_id || 'unknown',
    verdict: payload.verdict || 'SEAL',
  };

  // Persist atomically: ledger first, then head
  appendLedger(entry);
  writeHead({ seq, hash: thisHash, epoch, actor: entry.actor, verdict: entry.verdict });

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
    prev_hash: prevHash,
    epoch,
    chain_head: thisHash,
  };
}

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
    console.log('Usage: seal_chain.js {verify|head|recent N|length|write JSON}');
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
  hashSeal,
  canonicalJson,
  GENESIS_HASH,
  LEDGER_PATH,
  HEAD_PATH,
  VAULT_DIR,
};