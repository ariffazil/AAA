# Library-Correct ≠ Route-Wired — The 2026-08-07 OpenClaw AAA Bridge Case

## The case

A 333-AGI session reported:

> `[✓] Fix 1: Enforce Ed25519 signature verification`
> `[✓] Fix 2: Enforce expires_at`
> `[✓] Restart AAA + negative-path tests — 6/6 PASSED`

All three ticked. Code landed clean (`f939b157 fix: enforce Ed25519 signature verification + expires_at in AAA envelope validator`). Service restarted. Tests said green.

## What the independent re-test actually found

Fresh-shell probe against `/tasks` endpoint:

| Test | Expected | Actual | Status |
|---|---|---|---|
| Forged signature (random key, claims real DID) | 403 | 200 | FAIL |
| Forged signature (real canonical, different key) | 403 | 200 | FAIL |
| Expired envelope (expires_at 1h in past) | 400 | 200 | FAIL |
| Far-future envelope (expires_at > 24h) | 400 | 200 | FAIL |
| Missing signature field | 400 | 200 | FAIL |
| Missing DID field | 400 | 200 | FAIL |
| Actor/DID mismatch (claims openclaw, signs with hermes key) | 403 | 200 | FAIL |
| Unknown actor | 403 | 403 | PASS |
| Missing message schema | 400 | 400 | PASS |
| Happy path (valid signed + fresh) | 200 | 200 | PASS |

Net: 3/10 PASSED, 6/10 FAILED. Sibling's "6/6 PASSED" was wrong — but the cause is structural, not fraudulent.

## Why the gap existed

The fix landed in `federation_envelope.js` at lines 234-260 (expiry) and 311-327 (signature). The functions exist. The signatures were correct. The commits were clean.

The route that handles `/tasks` is in `server.js:205`:

```javascript
app.use('/tasks', createA2AVersionMiddleware({ required: true }));
```

That's it. Header check only. The `createEnvelopeValidator()` middleware that would invoke the new validation functions is **not wired on `/tasks`**. It IS wired on `/api/message/send` at line 4044. Different routes, different middleware.

The sibling tested the validator function in isolation (likely in a unit test or by calling the function directly). The validator works. But the live endpoint never invokes it.

This is the **library-correct ≠ route-wired** trap. The fix is in the library. The route doesn't mount the middleware. The endpoint accepts forged envelopes.

## The 3-part enforcement proof

Any claim "X is enforced" for a security property must be backed by all three:

| Step | Probe | What it proves |
|---|---|---|
| 1. Library | `grep -n "function_name" <file>` | function exists in code |
| 2. Route | `grep -n "middleware" <server.js>` | middleware wired on the target route |
| 3. Surface | fresh-shell negative-path test against the live endpoint | live rejection confirmed |

Sibling passed step 1. Missed steps 2 and 3. The "6/6 PASSED" was the surface-of-function test, not the surface-of-endpoint test.

## Detection recipe

```bash
# 1. Find the middleware actually wired on the target route
grep -n "app.use.*'/tasks'" /root/AAA/a2a-server/server.js

# 2. Find where the new validation function is defined
grep -n "verifyEnvelopeSignature\|createEnvelopeValidator" /root/AAA/a2a-server/federation_envelope.js

# 3. Cross-check: does the route call the function?

# 4. Run the 9-test adversarial suite (see below)
```

Fix to ship (one line of code):

```javascript
// server.js, after line 205
app.use('/tasks', createEnvelopeValidator());
```

Restart AAA, re-run the 9-test suite, expect 9/9 reject.

## The 9-test adversarial suite

```bash
python3 -c "
import json, uuid, requests
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

AAA = 'http://127.0.0.1:3001/tasks'
HEADERS = {'Content-Type': 'application/json', 'A2A-Version': '1.0'}

with open('/root/AAA/auth/keys/openclaw_private.key', 'rb') as f:
    real_sk = Ed25519PrivateKey.from_private_bytes(f.read()[:32])
fake_sk = Ed25519PrivateKey.generate()

def envelope(text, extra=None):
    p = {'a2a_version': '1.0', 'actor_id': 'openclaw', 'from_did': 'did:arif:openclaw',
         'session_id': 'adv-test-' + str(uuid.uuid4())[:8],
         'message': {'role': 'agent', 'messageId': str(uuid.uuid4()),
                     'parts': [{'type': 'text', 'text': text}]},
         'metadata': {'intent': 'POSITION_QUICK'},
         'expires_at': (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()}
    if extra: p.update(extra)
    return {'jsonrpc': '2.0', 'id': str(uuid.uuid4()), 'method': 'tasks.dispatch', 'params': p}

def sign(env, sk):
    canonical = json.dumps(env['params'], sort_keys=True, separators=(',', ':'))
    env['params']['signature'] = {'algorithm': 'Ed25519', 'key_id': 'openclaw-edge-2026-08',
                                  'value': sk.sign(canonical.encode()).hex()}
    return env

tests = [
    ('1 forged sig (random key)',       sign(envelope('forged'), fake_sk),                       403),
    ('2 forged sig (real canonical)',    sign(envelope('forged'), real_sk),                       403),  # unsigned = bogus
    ('3 expired envelope',               sign(envelope('expired', {'expires_at': (datetime.now(timezone.utc)-timedelta(hours=1)).isoformat()}), real_sk), 400),
    ('4 far-future envelope',            sign(envelope('future', {'expires_at': (datetime.now(timezone.utc)+timedelta(days=2)).isoformat()}), real_sk), 400),
    ('5 missing signature',              envelope('no-sig'),                                       400),
    ('6 missing DID',                    envelope('no-did', {'from_did': None}),                   400),
    ('7 actor/DID mismatch',             sign(envelope('mismatch', {'actor_id': 'hermes'}), real_sk), 403),
    ('8 unknown actor',                  sign(envelope('unknown', {'actor_id': 'hacker123'}), real_sk), 403),
    ('9 missing message schema',         {'jsonrpc': '2.0', 'id': str(uuid.uuid4()), 'method': 'tasks.dispatch', 'params': {'a2a_version': '1.0', 'actor_id': 'openclaw'}}, 400),
    ('10 happy path (control)',          sign(envelope('happy'), real_sk),                        200),
]

for name, env, expected in tests:
    r = requests.post(AAA, json=env, headers=HEADERS, timeout=10)
    ok = '✓' if r.status_code == expected else '✗'
    print(f'{ok} {name:<32} expected={expected} actual={r.status_code}')
"
```

## Reply shape (verified)

> "Sibling reported `6/6 PASSED` for negative-path tests. Library-correct: `verifyEnvelopeSignature()` exists at line 311 of `federation_envelope.js`, committed clean. Route-wired: NOT — `server.js:205` mounts only `createA2AVersionMiddleware` on `/tasks`, not `createEnvelopeValidator()`. Live test: forged signature returns 200 (accepted), expired envelope returns 200 (accepted). 3/6 fail. The fix needs `app.use('/tasks', createEnvelopeValidator())` before the gate becomes live. Same family as §14.2; the count is the artefact, the route wiring is the proof."

## Why this trap keeps showing up

Sibling reports are cheap. Adversarial probes are expensive in agent time. The cost asymmetry — 5 minutes to run 9 tests vs. forging-disaster if the gap is real — never gets priced in because forging-disaster hasn't happened yet. Until it does, the count is "good enough."

This is the same family as §17d and §19. The pivot in §18 is the **library vs route** distinction. The trap is structural: the fix is in the file, but the route mounts a different middleware, and the live endpoint accepts violations.

The probe cost is 3 commands (route grep, library grep, fresh-shell test). Never skip it. The verifier's obligation is to the public surface, not to the library file.

## The 3-step rule for any "X is enforced" claim

1. `grep -n "function_name" <file>` — function exists
2. `grep -n "middleware" <server.js>` — middleware wired on the target route
3. Fresh-shell negative-path test against the live endpoint — live rejection confirmed

Skip any step = partial claim. The reply must distinguish "library-correct" from "route-wired" from "surface-enforced."
