/**
 * Delegation Guard — K1 loop detector (Hermes spec, musyawarah-converged B′ 2026-10-07).
 *
 * Structural fix for the delegation-explosion class (Arif's A2A audit Gap 5):
 * agent A delegates to B; B's gateway delegates back to A; depth grows;
 * CPU + tokens burn while evidence dies. This gate halts the chain.
 *
 * Semantics (Hermes K1): HALT when
 *   - chain depth > MAX_DEPTH (default 2), OR
 *   - the same task signature already exists in the chain (same work
 *     re-delegated = loop, not parallelism).
 *
 * Depth = number of LIVE signatures in the context window (TTL-based).
 * v1 keeps no completion-hook wiring: expiry is the release. A same-signature
 * re-dispatch inside the TTL window is loop-shaped by definition; different
 * signatures remain allowed up to depth.
 *
 * This is NOT advisory. Same class as fq_gate: constitutional at the wire.
 */
'use strict';

const crypto = require('crypto');

const MAX_DEPTH = 2;
const SIGNATURE_TTL_MS = 15 * 60 * 1000;

// contextId -> Map(signature -> ts)
const chains = new Map();

function taskSignature({ targetAgent, skill, text }) {
    return crypto
        .createHash('sha256')
        .update(String(targetAgent || '') + '|' + String(skill || '') + '|' + String(text || '').slice(0, 512))
        .digest('hex')
        .slice(0, 24);
}

function prune(chain, now) {
    for (const [sig, ts] of chain) {
        if (now - ts > SIGNATURE_TTL_MS) chain.delete(sig);
    }
}

/**
 * Check a delegation against its context chain. Records the signature when allowed.
 * @returns {{allow: boolean, reason: string, depth: number, signature: string}}
 */
function checkAndTrack({ contextId, targetAgent, skill, text }) {
    const now = Date.now();
    const sig = taskSignature({ targetAgent, skill, text });
    const key = String(contextId || 'no-context');
    let chain = chains.get(key);
    if (!chain) {
        chain = new Map();
        chains.set(key, chain);
    }
    prune(chain, now);

    const depth = chain.size;
    if (chain.has(sig)) {
        return {
            allow: false,
            reason: `DELEGATION_LOOP: identical task signature already in context chain (sig=${sig}). Re-delegation of the same work is a loop, not parallelism.`,
            depth,
            signature: sig,
        };
    }
    if (depth + 1 > MAX_DEPTH) {
        return {
            allow: false,
            reason: `DELEGATION_LOOP: chain depth ${depth + 1} > MAX_DEPTH ${MAX_DEPTH} (context=${key}). Halting before resource burn.`,
            depth,
            signature: sig,
        };
    }
    chain.set(sig, now);
    return { allow: true, reason: '', depth: depth + 1, signature: sig };
}

/** Explicit release (future completion-hook wiring). */
function release({ contextId, signature }) {
    const chain = chains.get(String(contextId || 'no-context'));
    if (chain) chain.delete(String(signature || ''));
}

/** Test/ops helper: reset all chains. */
function _reset() {
    chains.clear();
}

module.exports = { checkAndTrack, release, taskSignature, _reset, MAX_DEPTH, SIGNATURE_TTL_MS };
