# SURFACE TRUTH CENSUS + STABILIZATION EPOCH PLAN
> 2026-09-20 ~18:20 MYT · KVM8 (forge) · HERMES · read-only · **no mutation**
> Sovereign directive: *"No — jangan mutate federation-wide yet."*

---

## 1. THE PLAN — ACCEPTED

The external analysis proposes a **stabilization epoch** before any federation-wide mutation:
freeze constitutional change → reconcile surface truth, runtime truth, authority continuity and
machine substrate → close one temporal outcome loop → then shadow-run INIT vNext.

**Accepted.** The nine-step order is sound and the destination is correctly stated:

```
ONE GOVERNED GATEWAY  +  MANY INDEPENDENT ORGANS / WITNESSES
```
— not "one MCP that owns everything". Independence is preserved; agent attention is reduced.

**Canonical new invariant (adopt verbatim):**

```
Declared ≠ Registered ≠ Reachable ≠ Callable ≠ Authorized ≠ Verified
```

---

## 2. ★ THREE OF ITS P0 FINDINGS ARE METHOD ERRORS — VERIFIED AGAINST LIVE

The analysis read a **protocol handshake gap as a capability failure.** All three organs use the
standard MCP session handshake (`initialize` → `Mcp-Session-Id` header → `notifications/initialized`).
Raw HTTP calls skip it and receive `SESSION_MISSING` — which is *correct server behaviour*, not a
broken contract.

### 2a. "WEALTH: SESSION_REQUIRED — the contract is impossible to satisfy through this surface"

**FALSE.** With a proper handshake the tool works:

```
initialize → Mcp-Session-Id: ed53d848ba984e97945d8654937d62a0
tools/call capital_registry
→ receipt_id 928101bc-c6df-4cf0-aae7-3b288dd71687
  path /root/VAULT999/wealth/receipts.jsonl
  call_status: DEGRADED          ← real signal, and callable
```

The session is supplied by the **MCP `initialize` response header**, not by a tool parameter — so no
schema field is missing. The contract is satisfiable. *(P0 item 4 rests on this false premise.)*

### 2b. "GEOX: runtime blocks them through RT1_GUARD"

**FALSE.** The actual errors were `Missing session ID`, then:

```
MCP_LIFECYCLE: tools/call rejected until client sends
notifications/initialized after initialize
```

A handshake step, not a guard. GEOX exposes **27 tools** once the lifecycle is completed.

### 2c. "WELL: advertised `well_system_registry_status` itself returns Unknown tool"

**FALSE — and it is a name error, not a surface defect.** That string does not appear in WELL's
advertised list at all (`grep -c` = **0**). The real name is **`well_registry_status`**, and it IS
advertised. The "Unknown tool" response is correct for a tool that was never declared.

---

## 3. WHAT IS CONFIRMED — MEASURED, NOT INHERITED

### 3a. ★ A-FORGE attestation scope mismatch — CONFIRMED, and worse than described

The analysis called it "two witnesses measuring different runtimes". Measured, it is stronger:

```
arifOS attests      : /opt/arifos/current/venv/.../arifosmcp           EXISTS
A-FORGE verifier reads: /usr/local/lib/python3.13/dist-packages/arifosmcp   ABSENT
```

What actually sits at A-FORGE's path:

```
arifosmcp-deprecated/          ← only a src/ dir (stub), Jul 25
arifos-1!2026.8.2.dist-info/   ← an EDITABLE install of a DIFFERENT package
```

**A-FORGE's verifier is not reading a different runtime — it is reading a path where the package does
not exist.** Any DRIFT verdict from that witness is measuring an empty target. This is the first
thing to fix, and the fix is to make both witnesses read one attestation packet naming
`import path + venv root + PID + manifest hash`, not to reconcile two independent guesses.

### 3b. arifOS — deployment parity genuinely closed

```
source  = built = deployed = 4f470929a36a5f75e11d1c55973fbbf35725c855
drift   = False
canon   = 3/3 files verified
```
The earlier `faf0e1a / c85becc` split is gone. One drift class genuinely closed.

### 3c. ★ But arifOS contradicts itself inside ONE payload

```json
"session_birth.actor_cryptographically_verified": false   ← here
"result.actor_cryptographically_verified":         true   ← and here, same response

"session_authority_state": "BOOT_ATTESTATION_FAILED"
"authority_band":          "LIMITED_MUTATE"   ← authority granted despite failed attestation
```

Same actor, same question, two answers — and **mutation authority is granted while the session's own
attestation is marked FAILED.** This is the P0 state-ontology item, and it is demonstrable in a single
call rather than inferred.

### 3d. WELL — deployment drift still open

```
source_commit   2e66d2b
deployed_commit 1baef3b
built_commit    1baef3b
drift           true
status          degraded
authority       REFLECT_ONLY
```
40 tools declared, 40 reachable via session.

### 3e. CHRON — the temporal loop has never actually run

```
episodes     54,100   (54,078 observe · 5 verify · 1 learn · 16 predict)
predictions  19 active · 0 verified
calibration  total_verified 0 · accuracy null · mean_brier null
```

And the verify log is decisive — **every single check found nothing due**:

```
{"event":"check","due_count":0,"next_verify":"2026-09-23T23:59:59+08:00","logged_at":"2026-09-19T01:34:26"}
{"event":"check","due_count":0,"next_verify":"2026-09-23T23:59:59+08:00","logged_at":"2026-09-19T01:36:12"}
{"event":"check","due_count":0,"next_verify":"2026-09-23T23:59:59+08:00","logged_at":"2026-09-19T15:30:01"}
{"event":"check","due_count":0,"next_verify":"2026-09-21T15:13:00+08:00","logged_at":"2026-09-20T15:30:02"}
```

`due_count: 0` four times, and `next_verify` moved **23 Sep → 21 Sep**. So: no prediction has ever
been verified, no lesson has ever been extracted — and the next due date has moved *earlier* by two
days. CHRON should **witness** the migration, not govern it. Agreed with the analysis.

---

## 4. DECLARED vs CALLABLE — THE FIRST MEASUREMENT

| Organ | Declared (REST /tools) | Via MCP session | Callable tested | Result |
|---|---|---|---|---|
| arifOS | 8 | **8** | — | consistent |
| GEOX | 25 | **27** | `geox_surface_status` | ⇒ needs `notifications/initialized` |
| WEALTH | 14 | **14** | `capital_registry` | ✅ callable (DEGRADED) |
| WELL | 40 | **40** | `well_system_registry_status` | ✗ **never advertised** — real name `well_registry_status` |
| A-FORGE | not probed (different transport) | — | — | **UNMEASURED** |
| FLOW | not probed (MCP 404) | — | — | **UNMEASURED** |

**GEOX 25 → 27 is a real discrepancy** worth a look: two tools appear through the session that the
REST surface does not list.

---

## 5. NOT VERIFIED BY ME (do not repeat as fact)

- A-FORGE "131 tools vs 127 affordances, 4 drifts, `block_execution=true`" — I measured
  `ok:true, tool_count:121, tools_loaded:121`. Different probe; **UNMEASURED**.
- WELL "callable 10 / 9 unexpected public" — **UNMEASURED**.
- HERMES "11 canonical tools vs fewer exposed" — **UNMEASURED**.
- WELL "swap 72%, flux 0.775, zombies" — **UNMEASURED** on this pass.

---

## 6. THE PATTERN, STATED PLAINLY

Tonight's session found the same defect class at every layer — and this analysis adds one more
instance, this time from outside:

```
A protocol handshake not performed
  → SESSION_MISSING returned (correct)
  → read as "contract impossible to satisfy"
  → escalated to a P0 remediation item
```

That is **a measurement error reported as a system defect** — the identical shape as the
`C15/C16` canon collision, the `953 genesis anchors` headline, the hand-counted skill tree, and the
prune ledger that claimed three archives and performed one.

**The correction does not weaken the plan.** Four of its P0 items stand on their own evidence
(A-FORGE attestation scope, INIT state ontology, arifOS self-contradiction, CHRON temporal loop).
Two of them should be re-scoped before anyone builds against them.

---

## 7. STATUS

**Mutations this pass: ZERO.** Read-only probes, one report file.
No federation-wide change. No canon change. No seal. No signature.

`arif_seal verify` not invoked. **NO SESSION SEALED.**

**Awaiting Arif:** whether to open the stabilization epoch as a lane, and if so, whether P0 item 1
(Surface Truth invariant) is scoped as a measurement first — which is what this file begins.
