# TWO CORRECTIONS + P0 IDENTITY BINDING GAP
> 2026-09-18 05:11 +0800 · read-only

---

## PART 1 — CORRECTION: the timeline is 40 minutes, not 16 hours

OpenClaw claimed T2 deployed *"16 jam sebelum session audit ni bermula."* Measured:

```
file mtime : 2026-09-18 04:29:40 +0800
restart    : 2026-09-18 04:30:02 +0800      ← 22 seconds after mtime
commit     : 2026-09-18 04:31:45 +0800      ← 2 min after restart
NOW        : 2026-09-18 05:11:02 +0800      ← T2 is 40 minutes old
```

**T2 deployed 40 minutes ago, live, during this session.** I observed it in real time
(ACTION-LEDGER §0.2 records my discovery at ~04:45). It was not a pre-existing 16-hour-old state,
and it is not outside the session's scope. The deploy window and the audit window **overlap**.

---

## PART 2 — CORRECTION: T2 did not break production signing. It was already dead.

OpenClaw: *"Fail-closed deployed, AAA_PAM_USER tak set, lane menolak semua tandatangan sekarang.
Production signing = mati."* — **The causal claim is wrong.**

Two independent paths exist:

| Path | State BEFORE T2 | State AFTER T2 |
|---|---|---|
| **Main** (challenge_id → verify → sign) | **ALREADY BROKEN** — challenge store unreachable | still broken |
| **Legacy** (canonical_json, no challenge) | **worked** (warn-then-sign) | **closed** |

Evidence the main path was already dead:
```
redis-cli -n 0 PING                        → NOAUTH Authentication required
http://127.0.0.1:8088/challenge/x         → 404
04:30:22 journal: "Challenge verification failed: Cannot retrieve challenge
                   (http + redis fallback failed): HTTP Error 404" → 403
```

`_load_challenge_from_redis` uses `redis://127.0.0.1:6379/0` (no password) against a Redis
requiring AUTH, and the HTTP fallback 404s. **No challenge could be retrieved → no signing could
occur on the main path — before T2 existed.**

**What T2 actually changed:** the main path's error moved from **403** (challenge unreachable) to
**401** (no credential). It did not disable a working lane. It *did* close the legacy unsigned
path — which was working, and was the insecure-by-design backdoor.

**So: production signing was not working before tonight. T2 neither broke it nor fixed it. It
relabelled the failure and closed one insecure door.**

---

## PART 3 — CORRECTION: "governance breach" is not established

OpenClaw asks whether the deploying seat had F13 authority. Facts:

```
commit e66b2643f | 333-AGI | 2026-09-18 04:31:45 | security(signing): fail-closed…
ACTION-LEDGER (FI-003's own edit): "DONE … FI-003 under F13 'teruskan T2'"
```

I searched for a primary source of that F13 directive:
```
grep "teruskan T2" across /root/AAA + /root/arifOS
→ ONLY hit: ACTION-LEDGER.md:179 — the ledger citing itself
```

**No primary record of the F13 "teruskan T2" directive was found.** That is a finding, but it is
not proof of breach:

- **Not established:** that the act was unauthorised.
- **Not established:** that it was authorised.
- **What is established:** an agent-authored ledger asserts F13 authorisation, and **the
  authorisation claim has no traceable source.** Under this session's own rules — *no receipt, no
  claim* — that claim is **UNVERIFIED**.

**Correct framing:** an **unverified authorisation claim in a governance record** — not a
confirmed breach. The distinction matters; asserting breach without evidence would be the same
defect class this session has been cataloguing.

---

## PART 4 — ★ P0: identity verification has NO public-key → actor registry binding

Found while tracing the identity path (interrupted mid-trace; completed now).

`runtime/tools.py:24811–24815` (the Ed25519 verify path):

```python
effective_actor_id = (
    actor_id.strip()
    if isinstance(actor_id, str) and actor_id.strip()
    else f"anon:{hashlib.sha256(bytes.fromhex(pubkey_hex)).hexdigest()[:16]}"
)

payload = f"{effective_actor_id}:{challenge}".encode()
pubkey.verify(sig_raw, payload)
```

And confirmed by grep:
```
grep "resolve_actor_public_key\|is_registered_actor" runtime/tools.py  → EMPTY
```

**The verify path never resolves `actor_id` → registered public key.** It verifies the signature
against the **caller-supplied** key, and derives/accepts the actor identity from the **caller's own
claim**. There is no step that asks *"does this public key belong to this actor?"*

### Why this matters

| Function | Binding |
|---|---|
| `issue_actor_challenge` (mint) | ✅ checks `is_registered_actor` … **but 5 identities bypass via `_ALWAYS_CHALLENGEABLE`** (`arif`, `888`, `ariffazil`, `kimi-code`, `kimi-code/fi-008`) |
| `_consume_actor_challenge` | ✅ checks `challenge.actor_id == claimed actor_id` |
| **Ed25519 verify (line 24811)** | ❌ **NO binding to registry — trusts supplied key + claimed actor** |

Consequence in principle: a caller who possesses **any** Ed25519 keypair, claims
`actor_id = "ARIF"`, and holds a valid outstanding challenge issued to `ARIF`, satisfies every
check — because the actor claim is self-declared and the key is self-supplied.

### Gating (what limits it today)

- `arif_challenge` is **not** on the public 8-tool MCP surface (probe: `Unknown tool`).
- `arif_verify` is **not** on the public surface (probe: `Unknown tool`).
- `POST /kernel/arif_verify` → **403** on localhost (route exists, blocked); **404** on public.
- `arif_challenge` **defaults `actor_id="ARIF"`** — so minting a challenge bound to ARIF requires
  no impersonation effort *if the path is reachable*.

**Status: NOT EXPLOITED, NOT TESTED.** No challenge minted, no signature attempted — doing so
would forge sovereign identity.

### The finding stated precisely

**The guard on the identity path is reachability (which surfaces are mounted), not cryptographic
binding.** The verification logic itself would accept a self-asserted identity with a self-supplied
key. That is the same shape as the genesis-minter finding: *individual links look correct; the
composition relies on an assumption nothing enforces.*

**Contrast with the signing lane, which DOES bind:** `_verify_ed25519_proof` derives the sovereign
public key from the signer (governance_identity.py, B1 2026-07-27). The identity path does not.

### Recommended fix (P1, small)

In the verify path, after parsing `pubkey_hex`, resolve the claimed actor's registered key and
require equality:
```python
registered = resolve_actor_public_key(effective_actor_id)
if registered is None or registered.lower() != pubkey_hex:
    return _verify_fail_response(..., reason="pubkey_not_registered_to_actor")
```
Plus: remove the `actor_id="ARIF"` default (it is a forge-identity default, per OpenClaw #59328),
or require an explicit actor with no fallback.

---

## SUMMARY FOR ARIF

| Item | Status |
|---|---|
| T2 deployed 16 hours before session | ❌ **FALSE — 40 minutes, during the session** |
| T2 broke production signing | ❌ **FALSE — main path already dead (challenge store unreachable)** |
| T2 closed the legacy unsigned path | ✅ **TRUE — that path worked, and was the insecure one** |
| Unauthorised deploy / governance breach | ⚠️ **NOT ESTABLISHED** — ledger asserts F13 "teruskan T2", no primary source found → **unverified authorisation claim** |
| Identity verify binds key→actor | ❌ **P0 CONFIRMED — no registry binding** |
| P0 exploited | ❌ No — gated by surface reachability only |

**Nothing was mutated by this session. No challenge minted, no signature attempted, no revert performed.**

**Three signing-lane blockers remain** (unchanged): `AAA_PAM_USER`, `python-pam`, **redis
credentials for the challenge store**. Provisioning any two still leaves it dead.
