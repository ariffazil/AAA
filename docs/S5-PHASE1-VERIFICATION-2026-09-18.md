<!-- SOT: execution record + verification. Tier: AWAITING F13 SIGN-OFF. -->
# S5 PHASE 1 — VERIFICATION, NOT CONSTRUCTION
> Forged: 2026-09-18 · KVM8 · Hermes ASI session
> Directive received: *"Bungkus JITU (Circuit Breaker) dan GEOX Physical Gates (K-DIP/K-SCALE/K-TAPER)
> dahulu… JITU mesti diangkat sebagai satu-satunya circuit breaker mutlak, dan GEOX physical gates
> mesti bertukar dari spesifikasi dokumen menjadi actuator berfungsi."*
> **Result: both already exist as working code. Neither is a document. The real gap is wiring.**
> Data: `reports/s5-phase1-verification-20260918.json`

---

## 1. GEOX physical gates — LIVE, not a spec

`/root/GEOX/src/geox_mcp/tools/structure_gates/` holds running code, not prose:

```
k_dip.py 13,720 b   k_dl.py 6,855 b   k_throw.py 7,549 b   restore.py 9,018 b
topology.py 7,490 b velocity.py 4,325 b growth.py 4,138 b   witness.py 3,533 b
calibration_derive.py 21,463 b   cutoff.py 12,992 b   geometry_adapt.py 7,699 b   normalize.py 4,264 b
```

Registered and callable: `geox_structure_validate` (present in `tools_manifest.yaml`) →
`run_all_structure_gates`, returning `PASS | KILL | INCONCLUSIVE`, plus `UNMEASURED` when scale/V is
missing, and explicitly **"Never local SEAL"**.

Naming correction: the two gates named as missing exist under the kernel's own vocabulary —
**K-TAPER = K-THROW** ("throw tapers to elliptical tip-line", Barnett 1987) and **K-SCALE = K-DL**
(displacement/length scaling, 10⁻³–10⁻¹ global; Earth bulk 0.005–0.05). The spec header carries
**"Status: LIVE PRODUCT"** and has since it was written.

**Verdict: PHANTOM ABSENCE.** The claim "specification document, not a functioning actuator" is the
failure mode our own doctrine names — a capability declared down without an inventory sweep. Both
audits committed it: the external one claimed the gates were missing; *I* claimed "no capability owns
instant-override" from a `SKILL.md`-only grep. Both were wrong for the same reason: **we searched text
where the thing is code.**

## 2. JITU / circuit breaker — THREE implementations, ZERO callers

```
/core/arifOS/core/paradox/circuit_breakers.py      CB1 Godellock (Ω₀<0.03) · CB2 Single-Witness ·
                                                    CB3 Cheap Truth · CB4 Recursive Stack ·
                                                    CB5 Confidence Cascade        [+ tests, 227 b]
/root/scripts/governance/circuit-breaker.sh        3-strikes task-loop cap, state in
                                                    ~/.local/share/arifos/circuit-breakers/*.cb
/root/arifOS/scripts/wire/arif-circuit-breaker     anti-infinite-RSI lock, MAX_ENTROPY_DELTA=0.15,
                                                    state in /var/run/arifos_circuit_breaker.json
/root/AAA/governance/wawabot-circuit-breaker-spec.md
/root/AAA/instructions/autonomous-substrate-kernel.md:44   "the emergency circuit breaker keyword
                                                            \"JITU\" is explicitly invoked"
```

Wiring measured:

| Check | Result |
|---|---|
| callers of `circuit-breaker.sh` | **1 — its own doctrine doc.** No runtime caller. |
| callers of `arif-circuit-breaker` | **1 — its own Makefile/README.** No runtime caller. |
| importers of `circuit_breakers.py` | **0 in live code** (only generated docs + dist wheels) |
| cron entries mentioning circuit | **0** |
| systemd units mentioning circuit | **0** |
| `/var/run/arifos_circuit_breaker.json` | **does not exist** |
| `.cb` state dir | **one entry, `test-task.cb`, 2026-08-15** |

**Verdict: BUILT, NEVER WIRED.** It has not tripped — not because nothing needed stopping, but because
nothing calls it. Three implementations, no single authority, no live trigger. Under F1 that is not a
missing floor; it is an **unconnected** one.

## 3. Why I did not build a fourth

F13's own instruction this session: *"no safety theatre at all in my skills… safety is emergence
attributes, should be in kernel."* Writing a new skill that describes a circuit breaker would be
exactly the decoration it refuses. And a fourth implementation of a mechanism that already exists three
times is the duplication defect S0–S3 exist to remove. So Phase 1 produced **a wire spec**, not code.

## 4. Wire spec — one authority, one trigger, one receipt (for sign-off)

```
AUTHORITY   One breaker. The other two become callers of it, or are retired with a tombstone.
            Candidate: circuit_breakers.py (it is the only one with tests and a doctrine anchor).
TRIGGER     JITU is a THING, not a word in a prompt. A word can only be obeyed by something that
            reads it. Concretely: a trip file with the full authority tuple
              { tripped_at, by, scope, reason, until, trace_id }
            and every automated lane consults it BEFORE its first side effect.
ENFORCEMENT A refused-with-receipt path, not a warning. An automated lane that cannot show it
            checked the trip file must not run. (Precedent exists in this repo: a pre-commit gate
            already blocks on pattern match — the mechanism is proven, only the subject is wrong.)
RECEIPT     Trip and reset both write to the causal ledger with trace_id. A halt nobody can prove
            happened is indistinguishable from no halt.
SCOPE       Named explicitly, because "stop everything" that cannot say what it stopped is theatre:
            which lanes, which crons, which escalations. Unknown scope = HOLD.
IMMUTABILITY F13 trips and F13 resets. Nothing automated may reset it — otherwise the loudest
            failure mode (a loop that clears its own breaker) is one line of code away.
```

## 5. Held

- JITU wire — awaiting sign-off. Touching the enforcement path of every automated lane is an
  authority change, not a bug fix.
- GEOX — **nothing to build.** Optional follow-up only: an agent-facing entry point already exists as
  `geox_seismic_interpret` / `geox_structure_validate`; the `geox-intel` address minted in S2 now makes
  that capability set visible in the mesh for the first time.

---

*Built is not wired. Spec is not actuator. Doctrine without a kill is decoration —
and a breaker nobody calls is a kill switch with no current. DITEMPA BUKAN DIBERI ⚒️*
