'use strict';
/**
 * AAA A2A tailnet transport identity — observe-only.
 *
 * The aaa-ingress tsagent node verifies the peer with whois, HMAC-signs the
 * identity, and forwards to AAA on loopback. This middleware verifies the
 * signature and attaches req.tailnetIdentity. It never blocks.
 */
const crypto = require('crypto');
const fs = require('fs');

const KEY_PATH =
  process.env.ARIFOS_TAILNET_INGRESS_KEY_FILE || '/etc/arifos/tailnet-ingress.key';
const HEADER_IDENTITY = 'x-tailnet-identity';
const HEADER_SIGNATURE = 'x-tailnet-signature';
const HEADER_TS = 'x-tailnet-ts';
const HEADER_ACTOR = 'x-arif-actor';
const MAX_SKEW_SECONDS = 120;

let cachedKey = null;
let cachedMtime = 0;

function loadKey() {
  try {
    const st = fs.statSync(KEY_PATH);
    if (!cachedKey || st.mtimeMs !== cachedMtime) {
      cachedKey = fs.readFileSync(KEY_PATH, 'utf8').trim();
      cachedMtime = st.mtimeMs;
    }
    return cachedKey;
  } catch {
    return null;
  }
}

function b64decode(value) {
  const padding = '='.repeat((4 - (value.length % 4)) % 4);
  return Buffer.from(value + padding, 'base64url');
}

function verify(headers) {
  const identityB64 = headers[HEADER_IDENTITY];
  const signature = headers[HEADER_SIGNATURE];
  const ts = headers[HEADER_TS];
  const any = identityB64 || signature || ts;
  const fail = (reason) => {
    if (any) console.warn(`[tailnet_verify] ${reason}`);
    return null;
  };
  if (!identityB64 || !signature || !ts) return fail('missing_header');

  const tsInt = Number(ts);
  if (!Number.isFinite(tsInt)) return fail('bad_ts');
  if (Math.abs(Date.now() / 1000 - tsInt) > MAX_SKEW_SECONDS) return fail('skew');

  const key = loadKey();
  if (!key) return fail('no_key');

  const expected = crypto
    .createHmac('sha256', key)
    .update(`${ts}.${identityB64}`)
    .digest('hex');
  const expectedBuf = Buffer.from(expected);
  const signatureBuf = Buffer.from(String(signature).toLowerCase());
  if (
    expectedBuf.length !== signatureBuf.length ||
    !crypto.timingSafeEqual(expectedBuf, signatureBuf)
  ) {
    return fail('sig_mismatch');
  }

  try {
    const payload = JSON.parse(b64decode(identityB64).toString('utf8'));
    if (!payload.node || !Array.isArray(payload.tags) || typeof payload.caps !== 'object') {
      return fail('bad_payload');
    }
    return payload;
  } catch {
    return fail('decode_error');
  }
}

function matchesActor(identity, actor) {
  const a = String(actor || '').toLowerCase();
  if (!a) return false;
  const node = String(identity.node || '').replace(/\.$/, '').toLowerCase();
  if (a === node || a === node.split('.')[0]) return true;
  for (const tag of identity.tags || []) {
    const suffix = String(tag).replace(/^tag:/, '').toLowerCase();
    if (a === suffix || a.startsWith(`${suffix}-`) || a.endsWith(`-${suffix}`)) return true;
  }
  return false;
}

// A2A task type/tool -> arifOS MCP capability. Deterministic map, observe-only.
// RATIFIED 2026-10-19: write/edit/compose are DRAFTING (arif_think) unless the
// task's action_class says MUTATE/IRREVERSIBLE, or the intent says
// deploy/execute/mutate/forge. Execution is a property of the action, not the verb.
const ACTION_CLASS_CAPABILITY = {
  READ: 'arif_observe',
  OBSERVE: 'arif_observe',
  DRAFT: 'arif_think',
  THINK: 'arif_think',
  ROUTE: 'arif_route',
  MEMORY: 'arif_memory',
  JUDGE: 'arif_judge',
  MUTATE: 'arif_forge',
  IRREVERSIBLE: 'arif_forge',
  SEAL: 'arif_seal',
};

const TASK_KEY_CAPABILITY = [
  { keys: ['seal', 'vault', 'receipt'], cap: 'arif_seal' },
  { keys: ['forge', 'execute', 'mutate', 'deploy', 'irreversible'], cap: 'arif_forge' },
  { keys: ['judge', 'verdict', 'adjudicate', 'evaluate'], cap: 'arif_judge' },
  { keys: ['route', 'dispatch', 'delegate'], cap: 'arif_route' },
  { keys: ['memory', 'recall', 'remember', 'context'], cap: 'arif_memory' },
  {
    keys: ['think', 'reason', 'plan', 'analyze', 'critique', 'review', 'write', 'edit', 'compose', 'draft'],
    cap: 'arif_think',
  },
  { keys: ['observe', 'search', 'query', 'read', 'fetch', 'research', 'sense'], cap: 'arif_observe' },
];

function taskDescriptor(body) {
  const envelope =
    body?.envelope || body?.params?.envelope || body?.task || body?.params?.task || {};
  const actionClass = String(
    envelope.action_class || envelope.actionClass || ''
  ).toUpperCase();
  const intent = String(
    envelope.intent ||
      envelope.tool ||
      envelope.skill ||
      body?.intent ||
      body?.tool ||
      body?.skill ||
      ''
  ).toLowerCase();
  return { actionClass, intent };
}

function requiredCapabilityForTask(body) {
  const { actionClass, intent } = taskDescriptor(body);
  if (actionClass && ACTION_CLASS_CAPABILITY[actionClass]) {
    return { cap: ACTION_CLASS_CAPABILITY[actionClass], descriptor: actionClass };
  }
  for (const rule of TASK_KEY_CAPABILITY) {
    if (rule.keys.some((key) => intent.includes(key))) {
      return { cap: rule.cap, descriptor: intent };
    }
  }
  return null;
}

function hasCapability(identity, cap) {
  const grant = identity?.caps?.['arif-fazil.com/cap/mcp'];
  if (!Array.isArray(grant)) return false;
  return grant.some(
    (entry) => Array.isArray(entry?.tools) && entry.tools.includes(cap)
  );
}

function tailnetIdentityMiddleware(req, _res, next) {
  const present = Boolean(req.headers[HEADER_IDENTITY]);
  const identity = verify(req.headers);
  if (present && !identity) {
    console.warn(`[tailnet_mw] path=${req.path} verify_failed`);
  }
  if (!identity) return next();

  req.tailnetIdentity = identity;
  const declared = req.headers[HEADER_ACTOR] || identity.declared_actor || '';
  if (declared && !matchesActor(identity, declared)) {
    console.warn(
      `[tailnet_actor_binding] mismatch node=${identity.node} tags=${JSON.stringify(
        identity.tags
      )} declared=${declared}`
    );
  } else {
    console.log(
      `[tailnet_identity] node=${identity.node} tags=${JSON.stringify(
        identity.tags
      )} caps=${Object.keys(identity.caps || {}).join(',')} actor=${declared || '-'}`
    );
  }

  // A2A task-level actor binding (observe-only). The body may carry the
  // declared actor in an envelope or in params. Compare it to the verified
  // tailnet node/tags; never block while in observe mode.
  const bodyActor =
    req.body?.envelope?.actor_id ||
    req.body?.params?.envelope?.actor_id ||
    req.body?.actor_id ||
    req.body?.params?.actor_id ||
    '';
  if (bodyActor && !matchesActor(identity, bodyActor)) {
    console.warn(
      `[tailnet_actor_binding] body_mismatch node=${identity.node} tags=${JSON.stringify(
        identity.tags
      )} actor=${bodyActor}`
    );
  } else if (bodyActor) {
    console.log(
      `[tailnet_actor_binding] body_match node=${identity.node} actor=${bodyActor}`
    );
  }

  const required = requiredCapabilityForTask(req.body);
  if (required) {
    if (!hasCapability(identity, required.cap)) {
      console.warn(
        `[tailnet_capability] a2a_missing required=${required.cap} task=${required.descriptor} node=${identity.node}`
      );
    } else {
      console.log(
        `[tailnet_capability] a2a_granted required=${required.cap} task=${required.descriptor} node=${identity.node}`
      );
    }
  }
  next();
}

module.exports = {
  tailnetIdentityMiddleware,
  verify,
  matchesActor,
  requiredCapabilityForTask,
  hasCapability,
};
