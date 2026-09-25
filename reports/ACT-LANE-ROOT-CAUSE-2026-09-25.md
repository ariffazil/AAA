# ACT LANE REPAIR SPEC — Root Cause Proven
> **Session:** SEAL-8065675e8035455a · 333-AGI · 2026-09-25
> **State-transition note:** this document is `ROOT_CAUSE_PROVEN` + `REPAIR_SPEC_READY`. It is **NOT** `REPAIRED`. Not `AUTHORIZED`. Not `EXECUTED`.
> **Evidence class:** OBS (live probes, exception reproduced) — confidence 0.95. DER (causal chain) — confidence 0.90.

---

## 0. What changed since the audit

The audit called this "structural" and ranked it #1. That ranking was right; the word **"structural" was wrong**. This is a **one-line credential drift**, not an architectural failure. The constitution was never broken — a Redis password was added and one consumer was never told.

> **A "structural outage" that is actually a missing env var is a category error worth learning from.** [INT]

---

## 1. The proven failure chain [OBS, reproduced]

```
Redis 127.0.0.1:6379        → UP, pid 3892624, requirepass SET
crypto_auth.py:147          → redis_url = os.getenv("ARIFOS_REDIS_URL",
                                             "redis://127.0.0.1:6379/0")   ← NO CREDENTIAL
ARIFOS_REDIS_URL            → NOT SET in service env  (falls back to no-auth URL)
                              ↓
client.from_url() + .set()  → AuthenticationError
                              "HELLO must be called with the client already
                               authenticated, otherwise the HELLO <proto> AUTH
                               <user> <pass> option can be used"            ← REPRODUCED
                              ↓
crypto_auth.py:277-285      → logs "F13: Redis STORE FAILED for <id> ...
                                        — not issuing challenge"
                              ↓
returns AUTHORIZATION_STORAGE_UNAVAILABLE
                              ↓
arif_judge                  → requires_human_signature=true
                              + challenge token NEVER MINTED
                              ↓
nothing to sign → signing service :18900 (healthy, key_loaded=true) has no input
                              ↓
A-FORGE                     → ERR_ACT_NO_SECRET
                              ↓
lg:444 DECIDE ──✗──► lg:556 DEPLOY    ← all governed mutation parked
```

**Reproduction (this session, read-only):**
```
$ python3 -c "import redis; redis.from_url('redis://127.0.0.1:6379/0').ping()"
AuthenticationError: HELLO must be called with the client already authenticated...
$ redis-cli ping
NOAUTH Authentication required.
$ redis-cli config get requirepass
NOAUTH Authentication required.        # requirepass is set
```

**The signer was never the problem.** `:18900` returns `{"status":"ok","service":"aaa-signing","key_loaded":true}`. All four "measured failures" in the earlier report were **one fault propagating through four surfaces**. [INT — this is the key correction]

---

## 2. The fix — one motion, credential already exists

`/root/.secrets/kunci-root.env` **already contains** these var *names* (verified present, values not printed):
- `REDIS_PASSWORD`
- `REDIS_URL`
- `REDIS_FED_PASSWORD`

`ARIFOS_REDIS_URL` is **not set**, so `crypto_auth.py` falls through to the no-auth default.

### Repair (T3 — auth infrastructure. Requires F13 or 888-APEX judge.)

```bash
# 1. Set the authenticated URL into the arifOS service env
#    (from the existing REDIS_URL / REDIS_PASSWORD in kunci-root.env — no new secret)
echo 'ARIFOS_REDIS_URL=redis://:${REDIS_PASSWORD}@127.0.0.1:6379/0' >> <arifos service env file>

# 2. Restart the kernel so the lazy _get_redis() re-inits
systemctl restart arifos

# 3. VERIFY — the only acceptable proof
curl -s -X POST http://127.0.0.1:8088/mcp   # issue one test challenge
#   expect a minted challenge_id, NOT AUTHORIZATION_STORAGE_UNAVAILABLE
```

### Verification criterion (independent, per Authority Envelope §Witness)
| Check | Pass condition |
|---|---|
| V1 | `issue_challenge()` returns a real `challenge_id` (not the error dict) |
| V2 | `arif_judge` on a T1 candidate returns a **minted** `authorization_request` |
| V3 | A-FORGE no longer returns `ERR_ACT_NO_SECRET` on a dry-run |
| V4 | seal_chain appends a new seq (proof the 999 path is live) |

All four must pass. V1 alone is not closure.

---

## 3. Why this must NOT be self-executed

This is the one repair in the entire list where **the beneficiary must not perform the fix**.

`arifOS/core/shared/laws.py:311` — *to SEAL is itself a F1 AMANAH violation (self-authorization).*
`authority-envelope.md` — *the executor may NEVER issue its own envelope.*

I am the agent whose mutation authority is currently blocked **by this exact defect**. If I wire my own authorization credential back in, I have issued my own envelope. The gate's beneficiary does not repair the gate.

So: **root cause proven → spec ready → execution held for F13/888.** That is not work-collapsing; that is the authority boundary. Per anti-collapse doctrine, this is `authority-boundary`, one of the four legitimate stop conditions.

---

## 4. estimateP falsification — target located, still un-run

G is minted in **two places** (a duplication worth noting):

| Location | Form |
|---|---|
| `arifosmcp/kernel/apex_decision_field.py:32,65` | `G36 = A * P * E * X` (raw product) |
| `arifosmcp/runtime/apex_canonical.py:533` | `G = (A * P * E * X) ** (1/4)` ← **canonical V3** |
| `arifosmcp/tools/forge.py:77` / `tools/sense.py:482` | `return product**0.25` |
| `arifosmcp/runtime/apex_c_dark.py:385` | `G = A * P * E * X * Phi` ← **STALE pre-V3, marked as such** |
| `A-FORGE/src/domain/apex/apex_c_dark.py:106` | same stale 5-factor |

`truth_kernel.py:166` seeds `prior_probability: float = 0.5` (defensible). The **0.7 → 0.915** claim from carry_forward `e-a3e0d6b6` is about *spec*-level priors feeding the `P` dial before checks run — the dial that `apex_canonical.py:533` then 4th-roots into G.

**Falsification is pure compute (T1, no mutation):** isolate one historical SEAL receipt, recompute G from raw measured A/P/E/X with priors stripped, compare verdict. Pre-registered rule already exists in `e-a3e0d6b6`.

**Note the second finding here:** `G = A·P·E·X` (product) vs `G = (A·P·E·X)^(1/4)` (geometric mean) coexist in live code. One of them is canonical, one is not. That is a **FATWA K1-class namespace collision on a governance scalar** — same defect class as the `666`/`888` numeral collision the fatwa settled. Worth a ruling. [INT, cap 0.70]

---

## 5. Revised risk ranking (accepting the reviewer's order, with one amendment)

| Rank | Item | Status after this probe |
|---|---|---|
| 1 | ACT lane outage | **ROOT CAUSE PROVEN — one env var.** Not structural. |
| 2 | estimateP falsification | Target located (`apex_canonical.py:533`). Still un-run. |
| 3 | Drift sensor defect | Confirmed. `source_vs_wheel` hash-vs-version. |
| 4 | Ghost capability surfaces | 5 ghost paths + 1 advertised ghost (`federation-health`). |
| 5 | `runtime/tools.py` cycles | 28,909 lines / 60 back-edges / 64 cycles. Survivable. |
| 6 | Ghost postgres :5432 | Needs #1 fixed first. |

**Amendment to the ranking:** the reviewer placed #6 "requires governed mutation first." Confirmed — but with #1 proven as a one-liner, #6 becomes reachable in the *same* authorization event.

---

## 6. The meta-strange-loop — named at last

```
  ┌─────────────────────────────────────────────────────────┐
  │  The repair of the authorization lane                    │
  │  is itself a governed mutation                           │
  │  which requires the authorization lane.                  │
  └─────────────────────────────────────────────────────────┘
```

This is the true strange loop of the machine — a **bootstrap paradox at the constitutional layer**. It is why the system can judge forever and never act: not because judgment is broken, but because the *hand* between judgment and action has no credential.

**And the resolution is not technical.** It is F13. The sovereign holds the authority that the broken lane cannot mint. That is exactly the design intent — the human is the root of the trust chain precisely for the case where the chain's own links fail. The system is stuck **at** the sovereign, not stuck **despite** the sovereign.

That is why your F13 read matters and should be preserved verbatim in canon:

> *A broken authorization lane is painful operationally, but less dangerous than an authorization lane that silently auto-approves.*

Preserved. The constitution held. It just cannot move.

---

## 7. State declaration (no Boolean)

| Object | State | prev | expected_next | owner | evidence_required |
|---|---|---|---|---|---|
| ACT lane root cause | `ROOT_CAUSE_PROVEN` | `SYMPTOM_CATALOGUED` | `REPAIR_AUTHORIZED` | F13 / 888-APEX | V1–V4 in §2 |
| Repair spec | `READY_UNEXECUTED` | — | `EXECUTED` | A-FORGE after auth | V4 seal_chain seq |
| estimateP falsification | `TARGET_LOCATED` | `HYPOTHESIZED` | `COMPUTED` | 333-AGI (T1) | recomputed G vs stored G |
| Drift sensor fix | `DIAGNOSED` | `NOTICED` | `PATCHED` | 333-AGI (T1) after auth | comparison returns equal-able |
| F6 hazard rule | `AWAITING_RATIFICATION` | `PROPOSED` | `RATIFIED` | F13 | one word: SAH |

**ΔS:** a "structural outage" collapsed to a one-line fix with a reproducible proof and a 4-point verification gate. Category error removed from the risk register.

---

*333-AGI · OBSERVE_ONLY · mutation_allowed=false · DITEMPA BUKAN DIBERI ⚒️*

---

# §8. ADDENDUM — CLAIM RETRACTION & RESCOPING (2026-09-25T05:50Z)

Independent re-audit of this report's claims applied the OBSERVE/DERIVED/INFERRED/INTERPRET
table from `hermes-role-ladder.md` §5 back onto the author. Two claims did not hold their class.

## Retracted / downgraded

| Original claim | Was classed | Real class | Finding |
|---|---|---|---|
| "A2A agent-card tiada, hantu" | stated as OBSERVE | **INFERRED** | Card EXISTS at `a2a-server/agent-cards/federation/hermes.json` (15.6KB). It is a **stub**, not a ghost. `url: None`. RETRACTED as stated. |
| "gateway websocket mati" | stated as OBSERVE | **INTERPRET** | `:18789` returns **HTTP 403** (alive, refusing). `:9900` is **HTTP JSON, not websocket** (upgrade attempt returns 200, not 101). "Dead" was a narrative. Correct state: *two services alive, both non-viable as the ws fallback the dispatcher expects.* |

## Upheld
- doctrine staged + DIRECTIVE delivered — OBSERVE (files verified 13:39/13:40)
- `canon/` `chattr +i`, promotion = T3 — OBSERVE (`----i------I--e-------`)
- hermes daemon `:9900` ALIVE — OBSERVE (`{"status":"ok","agent":"hermes-forge"}`)

## RESCOPING — the defect is larger than either pass stated

The re-audit corrected the class but scoped the defect to hermes. Live measurement widens it:

```
federation cards on disk : 6
url set (usable)         : 0
url = None (stub)        : 6
federation-a2a-sync.py   : writes NO url field at all
```

**Every** federation card is an endpoint-less stub — opencode (14.6KB), hermes (15.6KB), claude (12.4KB), and 3 more. The generator `federation-a2a-sync.py` never emits a URL. `dist/extensions/hermes/` is absent, and `agent-cards/extensions/` holds `hermes-asi.json` + `hermesarifos-bot.json` but **no `hermes.json`**.

So X11 is not "regenerate the hermes card." It is:
> the A2A federation card generator produces endpoint-less stubs for the entire mesh, so no agent can be dispatched to via card, and the dispatcher falls back to an OpenClaw websocket path that refuses with 403.

Three layers, one symptom — the re-audit's framing was right. The scope is the mesh, not the agent.

## X11 repair spec (one instruction, not an investigation)

1. `federation-a2a-sync.py` must emit `url` from the live port registry (`organs.yaml` / live probe), not leave it unset.
2. Emit `agent-cards/extensions/hermes.json` to the canonical path the registration reads.
3. Remove the OpenClaw websocket fallback in `aaa_dispatch_a2a` — a refused 403 fallback masks a card-layer failure as a transport failure.
4. Verify: `aaa_dispatch_a2a → hermes` returns `TASK_STATE_COMPLETED` with a real reply.

**Manual edit of the cards is rejected** — they are generated; edits would be overwritten at next sync. Owner X11 stands.

*ΔS: two claims reclassified using the table the same author wrote. Retraction is the table working.*
