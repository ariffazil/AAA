---
name: auth-failure-attribution
description: "Use when a 401/403 could belong to any hop in the chain."
version: 1.0.0
tags: [auth, credentials, 401, triage, proxy, gateway, credential-store, attribution]
---

# Auth Failure Attribution

> In a multi-hop chain, **the error class names the symptom, not the owner.** A `401` is equally
> consistent with a dead caller credential, a wrong hop, an empty credential store, and a revoked
> upstream key — four owners, four different fixes.

**Load when:** a caller reports an auth or authorization failure and more than one component sits
between it and the resource — proxy, gateway, a front-end that injects or passes through auth, a
credential store, an upstream provider.

**Do not load for:** a confirmed provider-side quota or billing failure (that is a lane problem, not
an auth-attribution problem), or credential *leak* containment (see `credential-exposure-containment`).
For the opposite direction — proving an inspection did not emit a secret — see
`secret-safe-inspection`.

---

## 1. The differential probe — two paths, same backend

The fastest attribution in any injected-auth topology is to find a path that **bypasses the caller's
credential** and one that **requires it**, then send the identical request down both. A front-end that
injects a service credential commonly sits beside a pass-through front-end that does not.

```
injecting front-end    → overwrites the caller's Authorization with a service credential
pass-through front-end → no injection; the caller MUST present its own valid credential
```

| injecting | pass-through | Owner of the failure | Not the cause |
|---|---|---|---|
| 200 | 401 | the **caller's own credential** (missing, revoked, unregistered) | the resource, the upstream, the proxy, the network |
| 200 | 200 | nothing | — |
| 4xx | 4xx | the **service credential** inside the routing config | the caller's credential |
| 0 / unreachable | 0 / unreachable | transport, or the hop itself | credentials |

This pair of calls outranks every config read, log grep and restart, because it varies exactly one
thing. Do it first.

Corollary: **never treat a result from one front-end as evidence about another.** Front-ends reaching
the same backend can answer with different truths about the same resource, and a working path through
the injecting front-end hides a broken caller credential completely.

## 2. One bad credential, or an empty store?

The answer changes the blast radius by orders of magnitude, and it is one query. Count rows in the
credential table before anything else — do not reason from the single failing caller.

```
rows > 0  → one credential is bad. Owner: that caller.
rows = 0  → every credential of this class is gone. Owner: the store. Every caller presenting its
            own credential is down simultaneously, and most of them will fail silently.
```

## 3. Wipe vs corruption vs single revocation

Separate a store wipe from a damaged store from a routine revocation. Check every signal; any one
alone is ambiguous.

| Signal | Wipe | Corruption | Revocation |
|---|---|---|---|
| store-init marker mtime | at the incident minute | old | old |
| schema-migration history | **all** migrations inside seconds | partial / none | none |
| row history span | one day only | old rows intact | old rows intact |
| container restart count | 0, start time matching the init marker | >0 | 0 |

`restart_count = 0` together with a start time at the init marker means the process was started onto
an **empty** data directory — deliberate re-creation, not a crash. A sibling database surviving in the
same cluster tells you the cluster was re-created rather than damaged, which narrows who or what did
it without naming it.

Report the actor as **UNKNOWN** when it is unknown, and name the probe that would find it. Never
infer an actor from the shape of the damage.

## 4. What the failure disables is not what it looks like

A dead caller credential in a chain that has fallbacks does **not** produce errors. It produces a
**silent substitution**: the caller keeps working, on a different backend, under a different name.

1. **Read who actually served.** Log the resolved backend per call. Without it, a lane's front routes
   can be dead for hours with the only symptom being an unrecorded swap.
2. **Reset the model of "working".** Continuous service is not continuous service of the contracted
   thing. State which name served, not that the request succeeded.
3. **Count the failures that were recorded but never read.** A store emitting `status=failure` rows is
   witnessing correctly; the gap is a *reader*. Another writer does not close it. Report `PRODUCED`
   separately from `OBSERVED` — the recording usually already works.

## 5. Fix selection, and the one fix that is not yours

When the caller's own credential is the casualty:

- **Re-provision** through the owning provisioning script — preferred: auditable, correct scope.
- **Re-register the existing value.** If the store hashes credentials as the bare digest of the
  plaintext with no salt, the same value can be re-registered from the copy already in the caller's
  config, so no secret is redistributed. Reproduce the digest to verify the scheme before relying on
  it — do not assume the salt is absent.
- **Point the caller at the credential-injecting path.** Works immediately, and costs per-caller
  attribution: the traffic is billed and logged under the service identity from then on. State that
  cost rather than presenting the bypass as free.

**Re-minting is not the agent's to take.** When the broken credential is the one the agent itself runs
on, the actor is also the beneficiary of the restored access. Present the options, name the
attribution cost, and hand the choice to the credential owner. This is not caution theatre: a system
that re-issues its own credential when its credential is missing is precisely the pattern credential
governance exists to prevent.

## 6. Reporting shape

1. **Which hop owns it**, from the differential probe — one line, before any narrative.
2. **Blast radius as a count**, not an anecdote: how many credentials of that class exist, and which
   callers present their own. A zero-row store is a fleet event.
3. **The recovery options with their costs**, including the attribution cost of the bypass path.
4. **The reader that was missing**, and where it belongs — as a check, not a new service.

## 7. Re-runnable reader

Probe the four facts above and exit with a verdict (`0` held / `1` broken / `2` backend down,
fail-closed). It writes nothing, mutates nothing, restarts nothing, and reads credentials by *name*
only, printing just a redacted form. Adapt the endpoints and the store query to the stack at hand;
the shape is what matters.

```python
#!/usr/bin/env python3
"""reader for one credential-backed lane: alive? authenticates? who served? how many failures?"""
import json, re, subprocess, sys, urllib.error, urllib.request

BACKEND      = "http://127.0.0.1:4013"        # the service itself
PASS_THROUGH = "http://127.0.0.1:4012/v1"     # requires the caller's own credential
INJECTING    = "http://127.0.0.1:4000/v1"     # injects the service credential
CRED_ENV, CRED_NAME = "/root/.secrets/fed-zen-key.env", "FED_ZEN_KEY"
LANE, WINDOW = "i-arif", 24
STORE = ["docker", "exec", "-i", "postgres", "psql", "-U", "arifos_admin", "-d", "litellm",
         "-t", "-A", "-F", "|", "-c"]


def load_cred(path, name):                 # read by NAME; never return it to an output path
    for line in open(path):
        if line.strip().startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def scrub(s):                              # masks full keys AND the masked tails upstreams echo
    s = re.sub(r"sk-[A-Za-z0-9_\-]{6,}", "sk-<REDACTED>", s)
    return re.sub(r"sk-[.\-_A-Za-z0-9]{1,8}[A-Za-z0-9]{3,4}\b", "sk-<REDACTED>", s)


def call(url, cred=None, payload=None, timeout=15):
    data = json.dumps(payload).encode() if payload else None
    r = urllib.request.Request(url, data=data)
    if cred:  r.add_header("Authorization", f"Bearer {cred}")
    if data:  r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:    return e.code, json.loads(e.read().decode() or "{}")
        except Exception: return e.code, {}
    except Exception as e:                 # unreachable != failed; never report it as failed
        return 0, {"error": f"unreachable: {type(e).__name__}"}


def store(sql):
    try:
        r = subprocess.run(STORE + [sql], capture_output=True, text=True, timeout=30)
        return (r.stdout + r.stderr).strip()
    except Exception as e:                 # store down is a probe result, not a crash
        return f"store_unavailable: {type(e).__name__}"


broken = []
live = call(f"{BACKEND}/health/liveliness", timeout=8)[0] == 200
print(f"[1] backend alive ...................... {'OK' if live else 'DOWN'}")
if not live: broken.append("backend_down")

cred = load_cred(CRED_ENV, CRED_NAME)
print(f"[2] credential present ................. {'yes' if cred else 'MISSING'}")
held = False
if cred and live:
    code, body = call(f"{PASS_THROUGH}/models", cred=cred)
    held = code == 200
    print(f"    credential authenticates ............ {'OK' if held else f'FAIL ({code})'}")
    if not held:
        print(f"    reason: {scrub(str(body.get('error', body)))[:160]}")
        inj = call(f"{INJECTING}/models")[0]
        print(f"    injecting path answers .............. {inj}")
        if inj == 200:
            print("    -> ATTRIBUTION: the caller credential owns this, not upstream, not the proxy")
        broken.append("credential_unauthenticated")
elif not cred:
    broken.append("credential_missing")

if held:
    # generous budget on purpose: reasoning backends emit empty content at low max_tokens
    code, body = call(f"{PASS_THROUGH}/chat/completions", cred=cred,
                      payload={"model": LANE, "messages": [{"role": "user", "content": "ping"}],
                               "max_tokens": 400}, timeout=120)
    served = body.get("model") if code == 200 else None
    print(f"[3] lane reachable .................... {'OK' if code == 200 else f'FAIL ({code})'}")
    print(f"    actually served by ................... {served or 'unknown'}")
    if served and served != LANE:
        print("    -> degraded: the contracted name is NOT the backend that answered")
    if code != 200: broken.append("lane_unreachable")

rows = store('SELECT count(*) FROM "LiteLLM_VerificationToken";').strip().splitlines()[-1]
print(f"[4] credential rows in store ........... {rows}")
if rows == "0":
    print("    -> EMPTY STORE: every caller presenting its own credential is down at once")
    broken.append("store_empty")

fails = store(f'''SELECT count(*) FROM "LiteLLM_SpendLogs" WHERE status='failure'
    AND "startTime" > now() - interval '{WINDOW} hours';''').strip().splitlines()[-1]
print(f"    failures in {WINDOW}h window .............. {fails}")
try:
    if int(fails) > 0 and not held: broken.append("failures_recorded_unread")
except ValueError:
    pass

print("-" * 68)
if not live:
    print("VERDICT: BACKEND DOWN - cannot assess (fail-closed)."); sys.exit(2)
if broken:
    print(f"VERDICT: BROKEN - {', '.join(broken)}"); sys.exit(1)
print("VERDICT: HELD - credential authenticates, lane serves, no auth failures recorded.")
sys.exit(0)
```

## Pitfalls

- **Do not restart anything before the differential probe.** A restart clears the evidence that
distinguishes a store wipe from a stale process, and it fixes neither.
- **Do not conclude "provider key revoked" from a caller-side `401`.** Check the store row count and
the pass-through path first; provider revocation and a missing caller credential produce the same
status code with different owners.
- **Do not echo credential material while proving the failure.** Read credentials by *name*, print
  only a redacted form, and mask the partially-masked tails services echo back (`sk-…` plus a short
  suffix) — a bare full-key pattern will not catch those.
- **Do not treat "the service still answers" as "the credential works".** With fallbacks configured,
  the first is compatible with the second being false for hours.
- **Do not mint a new scheduled job to watch this.** Attach the check to something that already runs,
  or leave it manual and say so.
- **Do not probe a reasoning backend with a tiny `max_tokens` and read the empty `content` as a dead
  lane.** It spends the whole budget on reasoning and returns `200` with no visible text — grade the
  HTTP code and the reasoning-token count, or raise the budget.
