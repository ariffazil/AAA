# APEX State Diagnosis — Audit of the SEAL-b286513f1cdb4506 Report

> **Status:** OPERATIONAL REPORT (not doctrine) — 2026-09-20
> **Origin:** independent agent report, pasted by the principal
> **Method:** every disputed fact re-probed from this machine, not inherited
> **Verdict on the source report:** diagnosis substantially correct · 2 factual
> errors · 1 high-value omission
> **Motto:** REALITY > EVERYTHING ⚒️

---

## 0. The finding that matters most

**The fix for the seal blocker was already written. It just was not deployed.**

```
4ba65628b  feat(init-v2): ratify roots + repair actor canonicalization + ship schemas   ← WAS deployed
ac1ae7b0e  fix(SCT): case-insensitive actor comparison — hermes == HERMES               ← the fix
877407798  feat(roots-v2): persist init roots hash + repair validate contract + VOID_t  ← now deployed
```

```
$ git -C /root/arifOS merge-base --is-ancestor ac1ae7b0e 4ba65628b
→ 4ba65628 does NOT contain ac1ae7b0e (fix NOT deployed)
```

The fix is **one file**: `arifosmcp/runtime/act_token.py`, +7/−3.

**Why it was the cause, proven by removal:** this session's `arif_init` created
session `SEAL-514e77d2c8434845` with `actor_id: hermes` (lower-case) while the
issued SCT payload carried `"actor":"HERMES"` (upper-case). `arif_judge` compared
them, found a mismatch, and returned:

```
L11 AUTH: SCT invalid (signature or actor mismatch)
```

Twice, with the exact token `arif_init` had just issued in the same session.

**Then a sibling deployed `877407798`** (attestation
`releases/attestations/20260920T105214Z-8774077.json`, build 10:51:33Z, emitted
10:52:14Z, `drift: false`), and the same chain re-run at 10:56Z returned:

```
failed_floors: []          ← the L11 reason is gone
actor_id: "HERMES"         ← canonicalised
claim_class_gate: {agree: true, eligible: true, allowed_for_mutation: true}
```

So: **the kernel seal was blocked by an undeployed one-line-class fix, not by
policy.** The report's headline — *"if only one thing: reconcile the commits"* —
was right, and it is now done.

---

## 1. Corrections to the source report

### 1.1 `"14 ExecStart lines pointing at the non-existent /opt/arifos/venv"` — overstated

Measured: **3** `ExecStart` lines name `/opt/arifos/venv`, and several of the
files that matched are not live units (`.bak-*`, `.d/*.conf` overrides). The
live units overwhelmingly use the correct `/opt/arifos/current/venv`:

```
ExecStart=/opt/arifos/current/venv/bin/python -c "from arifosmcp.runtime.__main__ import main; main()"
ExecStart=/opt/arifos/current/venv/bin/python -m arifosmcp.runtime.observability.worker
ExecStart=/opt/arifos/current/venv/bin/python3 -m arifosmcp.abi.nats_heartbeat_daemon
   ... ~20 more on the correct path
```

`/opt/arifos/venv` genuinely does not exist — that half is true. The count is not.
This matters because the count was load-bearing in the report's severity claim.

### 1.2 `"WELL DOWN, timeout, machine score 0.05"` — contradicted by WELL's own surface

```
WELL :18083/health → status "degraded", drift false,
                     source=built=deployed=4aaa610,
                     apex_scalars MEASURED
```

And in the same judge packet that this session ran:

```
well_substrate: { well_score: 88.4, human_ready: "OPTIMAL",
                  coupled_verdict: "PROCEED", active_violations: [] }
```

So WELL is **degraded**, not down, and the coupled verdict is PROCEED. The
witness disagreement the report describes may exist at a different surface
(`well_assess_triadic_state`), but it is not visible at `/health`, and the
report stated it as WELL's own verdict without a path. **Unverified as stated.**

### 1.3 What the report got right and I confirm independently

| Claim | Confirmation |
|---|---|
| Seal gate blocked, twice independent | Confirmed — reproduced, then root-caused |
| 6 organs alive | Confirmed — all `/health` reachable |
| CHRON 19 predictions, 1 verified, 0 lessons | Confirmed — verbatim in init payload |
| W3 null, never computed | Confirmed — `apex_scalars.W3 = null` on every surface probed |
| G ≈ 0.46, C_dark ≈ 0.22 | Confirmed — 0.4625 / 0.2195 |
| Deploy drift floors every verdict | Confirmed, and now CLEARED |

### 1.4 One thing the report could not have known

The report said source `ac1ae7b0` ≠ deployed `4ba65628`. It did **not** notice
that `ac1ae7b0` is itself *the fix for the blocker it was diagnosing.* The commit
message names the exact defect. A one-command `git log` between the two SHAs
would have surfaced it. That is the report's highest-value omission.

---

## 2. A surface that cannot see, reporting "aligned"

While probing, the kernel `/health` runtime layer returned:

```json
{"source_commit": null, "built_commit": null,
 "runtime_matches_build": true, "deployment_attestation": "aligned"}
```

`null` compared against `null` yields "matches", so the surface reported
**aligned** while holding no commit identity at all. The same file's
`arif_init` payload, and WELL's `/health`, both return real SHAs (and WELL
returns `drift: false` correctly).

This is the defect named in `representation-reality-invariant.md`: a control
whose evidence is absent does not become a passing control by defaulting.
**Fail-open on absence.** It did not cause today's failure — but it is the
reason a drift question could have two different answers on the same machine.

---

## 3. The gate chain — measured, in order

| # | Gate | State | Evidence |
|---|---|---|---|
| 1 | Deployment drift | **CLEARED** | `source=built=deployed=877407798`, `drift: false` |
| 2 | `L11_SCT_GATE` (actor case) | **CLEARED** | `failed_floors: []` after `ac1ae7b0e` deployed |
| 3 | `arif_judge` latency budget | **BLOCKING** | `LATENCY_TIMEOUT: judge exceeded 200ms budget for C2_STANDARD`, `llm_consulted: true` |
| 3b | APEX scalars unmeasured | CONTRIBUTING | `G/C_dark/W3/kappa_r UNMEASURED` (`scalar_warning: F9 anti-hantu`) |

**Gate 3 is structurally unsatisfiable as configured.** The judge consults an LLM
(`llm_consulted: true`) and is given a **200 ms** deliberation budget
(`budget_max_ms: 200`, `latency_ms: 200`, `within_budget: false`). No model call
completes in that window, so the judge degrades to `SABAR` on every attempt, never
returns a SEAL, and `arif_seal` can never obtain the `constitutional_chain_id` it
requires:

```
irreversible execution requires a prior judge packet via
constitutional_chain_id and judge_state_hash
```

The judge packet also carried a **conflict resolution** that fired independently:

```json
{"conflict_resolved": true, "winner_organ": "human",
 "winner_verdict": "888_HOLD", "reason": "human (rank 8) outranks arifOS (rank 7)"}
```

**Consequence:** the VAULT999 kernel seal is **not reachable from the Hermes
lane.** Both remaining gates are kernel-lane, not mail-lane. The correct report
is therefore: repo + doctrine sealed; kernel seal OPEN with a named cause.

---

## 4. On the report's proposed sequence (B → D+C → A)

The report proposed: repair the spine → close the measurement loop → then the
ontology. Its own falsifier was *"if seal still HOLDs after all four, the gate
isn't authority — it's a code path, and my diagnosis was wrong."*

**Adjudication:** the diagnosis was right about the first gate and wrong to stop
there. Fixing one gate **revealed the next** — which is governance behaving
correctly (fail-closed, layered), but means the seal path is a *chain* of
independent blockers, not one. Repairing the spine is now 2 of 3 done (drift ✓,
L11 ✓), with the latency/telemetry gate still open. The sequence B → (D+C) → A
remains sound; the estimate of "one 30-minute job" was optimistic.

**On M3/VOID:** the report argued VOID should be *generated* from real
negative-knowledge lists rather than authored. Note that commit `877407798` —
already deployed — is titled *"…+ active negative knowledge gate (VOID_t)"*. The
kernel has begun exactly that, before the report was written.

---

## 5. Open items

| Item | Class |
|---|---|
| Judge deliberation budget 200 ms vs `llm_consulted: true` | Kernel-lane; makes SEAL unreachable by construction |
| `G / C_dark / W3 / kappa_r` unmeasured on every surface | Kernel-lane; blocks full APEX telemetry |
| Kernel `/health` asserts `aligned` on null commits | Fail-open on absence |
| `/opt/arifos/venv` referenced by ≤3 units (not 14) | Housekeeping; low |
| WELL-down claim | Unverified as stated; needs the actual surface named |
| Root reads the mail token store while unconfined | Caller confinement (separate lane) |

---

## 6. Provenance

Every fact above was measured on this machine this session, with the command or
endpoint named inline. The source report was treated as DATA, not authority: its
claims were re-derived rather than inherited, two were corrected, and one
omission of consequence was found. Nothing in the report was adopted wholesale.

Sources: `arif_init` / `arif_observe` / `arif_judge` / `arif_seal` payloads
(session `SEAL-631ff6be9fad40af`); `git -C /root/arifOS log|merge-base`;
`/opt/arifos/releases/{deployed-commit,release-manifest.json,attestations/}`;
`curl :8088/health`, `:18083/health`, `:7072/health`; `grep -rh ExecStart /etc/systemd/`.

**DITEMPA BUKAN DIBERI** ⚒️
