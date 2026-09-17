<!-- SOT: addendum. Tier: S5 Phase-1 follow-up — regression found, isolated, and NOT papered over. -->
# S5 PHASE 1 — ADDENDUM: the wall fix changed behaviour, and two tests say it shouldn't have

> Forged: 2026-09-18 · KVM8 · after the S5 Phase-1 commit
> Why this exists: I made a behaviour change to a live organ. I ran the organ's test suite against
> a **pristine HEAD** and against **my change**, and compared. That comparison is below, unchanged.

---

## 1. The comparison (measured, not estimated)

Same selection both runs: `pytest tests -k "seismic or structure or interpret or gate"`.
Method: `git checkout --` the two files to get HEAD, run, capture the failure list, restore mine, run again, diff.

```
pristine HEAD : 26 failed, 238 passed, 3 skipped
my change     : 28 failed, 236 passed, 3 skipped

NEW failures  : 2
    tests/test_geox_fix_brief_a_b_c.py::test_c_acceptance_session_payload_gates_measurable
    tests/test_seismic_zen_f1.py::test_f1_measure_throw_feeds_gates
FIXED failures: 0
```

An earlier iteration of my rule caused **4** new failures. That was a real bug in my change and I
fixed it before this addendum: the first rule treated *any* `governance_status == "HOLD"` as a physics
falsification, which mislabelled "you sent an empty framework" and "unknown mode" as falsified claims.
The rule is now narrower — it falsifies only when the payload itself reports a gate KILL
(`combined_gate_verdict == KILL`, a non-empty `kills` list, or `gate_summary == "KILL"`), looked for at
top level and inside `structure_validate`. That took 4 new failures down to 2.

## 2. What the two surviving failures actually assert

Both assert `local_verdict == "QUALIFIED_CANDIDATE"` for a framework that the federation's own K-*
gates reject. I printed the kills rather than guessing:

**`test_geox_fix_brief_a_b_c.py`** — its fixture is described as a *session-replay acceptance* framework
(`SEAL-51a63024e73c45e0`). Its own gate matrix:

```
combined_gate_verdict : KILL
kills                 : ['K-THROW', 'K-DL', 'K-RESTORE']

K-THROW   "4 fault(s) fail tip-taper"
    F1_south_bounding  Throw increases toward tip (tip growth / no taper)
    F2_north_flank     Tip throw does not taper relative to mid-fault
    F3_north_flank     Throw constant/non-tapering at tips
    F4_north_shallow   (PASS)
K-DL      D/L = 1.477e-01 — outside the global envelope (Earth bulk is 0.005–0.05)
          F4 D/L = 0.000e+00 — also outside
K-RESTORE Restoration hard veto — line-length residuals 0.33 / 0.67 / 0.89 vs tolerance 0.05
```

**`test_seismic_zen_f1.py`** — `zen_measure_throw`'s own fixture fault carries
`throw_profile_m: [1.0, 1.0, 1.0, 1.0, 1.0]` — a perfectly constant throw. K-THROW kills it:
*"Throw constant/non-tapering at tips"*. The fixture feeds its own output into its own downstream gate
and the gate rejects it.

So the situation is precise: **the gates are right about the physics, and the two tests assert that a
rejected framework must still be stamped a candidate.** The acceptance fixture for the wall is itself
physically invalid — throw that grows toward the tip, D/L an order of magnitude outside the global
band, and restoration residuals 7–18× tolerance.

## 3. What I did NOT do

**I did not edit the tests.** Changing an assertion to match new code is indistinguishable from
editing the judge so a failing check passes — the exact self-modification asymmetry Law 6 forbids.
The tests now fail loudly, which is what a test is for. The decision belongs to F13, and the two
honest options are:

```
A. The fixture is wrong, not the wall.  Give the acceptance fixture physically valid geometry
   (tapered throw profiles, D/L inside 0.005–0.05, restoration residual < tolerance) and keep the
   assertion. The test then measures what its docstring says it measures — gate measurability.
B. The assertion is too strong.  Its docstring reads "Replay session-shaped 5H/5F + calibration →
   ≥5/7 gates not UNMEASURED" — gate MEASURABILITY, not physics validity. If the fixture stays
   synthetic, the assertion should accept the honest verdict instead of demanding a candidate label.
```
I lean **A**: a governance acceptance test should exercise a framework that *could* be accepted,
otherwise it verifies the label and not the wall.

## 4. The other 26 failures are pre-existing

Present on pristine HEAD before I touched anything: `test_gateway_authority` (9), `test_seismic_rsi` (6),
`test_seismic_compute_unified_modes` (3), `test_seismic_pipeline_end_to_end` (3),
`test_seismic_interpret_p0` (2), `test_seismic_mode_router_contracts` (2), `test_auto_mint` (1).
Not mine, not fixed here, and not to be quietly attributed to this work.

## 5. State of the GEOX fix after this pass

```
/root/GEOX/src/...        patched, narrowed rule, compiles           (source of truth)
/opt/geox/src/...         patched, narrowed rule, compiles           (live tree, NOT loaded)
running process           still the pre-fix module                   (restart BLOCKED_AT_GATE)
in-process proof          IMPOSSIBLE -> KILL/HOLD/FALSIFIED · kills ['K-THROW','K-DL']
                          PLAUSIBLE -> PARTIAL/QUALIFY/QUALIFIED_CANDIDATE · kills []
regression                +2 failing tests, both asserting the old behaviour, evidence above
```

---

*A test that encodes a defect is a second defect. Reporting it is not the same as fixing it —
and fixing it by rewriting the assertion is not fixing it at all. DITEMPA BUKAN DIBERI ⚒️*
