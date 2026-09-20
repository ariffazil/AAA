# INIT v2 ROOTS — ONTOLOGY IS REAL IN CODE, ABSENT IN THE LIVE CONTRACT
> 2026-09-20 ~18:20 MYT · KVM8 (forge) · HERMES · read-only · zero mutation
> Trigger: claim that *"the latest arif_init now reports an active init_v2_roots structure with
> TEMPORAL_ROOT, OBJECTIVE_ROOT, NEGATIVE_KNOWLEDGE, and PROVENANCE_ROOT"*

---

## ★ CORRECTION — 2026-09-20 18:42 MYT (re-probe; corrected IN PLACE, not appended)

**The §1 verdict below is now SUPERSEDED. All four roots are LIVE.**

Two commits landed after this report was written:

```
18:24:28  5e5197aa2  fix(init): surface init_v2_roots 4 roots in MCP envelope (last-mile)
18:26:50  4ba65628b  feat(init-v2): ratify roots + repair actor canonicalization + ship schemas
18:29:57  deployed session.py written
18:30:03  kernel restarted
```

Re-measured at 18:41 across all three verbosity modes:

```
verbosity=minimal   init_v2_roots: present · 4 roots · status ACTIVE
verbosity=standard  init_v2_roots: present · 4 roots · status ACTIVE
verbosity=full      init_v2_roots: present · 4 roots · status ACTIVE

NEGATIVE_KNOWLEDGE.unmeasured_scalars = ["G","C_dark","W3","kappa_r"]
```

So the report's §1 finding was **true at 18:14–18:20 and is stale at 18:41.** Recorded, not retracted:
the measurement was correct when taken, and reality moved. **REALITY > MODEL applies to this file too.**

**What did NOT close** — both self-contradictions remain in the live payload after the 18:30 restart:

```
session_birth.actor_cryptographically_verified : False
result.actor_cryptographically_verified        : True     ← same payload, still split

session_authority_state : BOOT_ATTESTATION_FAILED
authority_band          : LIMITED_MUTATE                   ← authority still granted
result.actor_verified   : None                             ← new: null in result
```

Commit `4ba65628b` says *"repair actor canonicalization"*; the cryptographic-verification split is a
different field and is still open. **Two of the three contradictions this session measured survive.**

---

---

## 1. VERDICT — 1 OF 4 IS LIVE

| Root | Builder produces it | In live `arif_init` payload |
|---|---|---|
| TEMPORAL_ROOT | ✅ | ✅ **populated** (`temporal_root`) |
| OBJECTIVE_ROOT | ✅ | ❌ **absent** |
| NEGATIVE_KNOWLEDGE | ✅ | ❌ **absent** |
| PROVENANCE_ROOT | ✅ | ❌ **absent** |

`init_v2_roots` itself does **not appear anywhere** in the live response — searched recursively over
the full payload at `verbosity=full`, after the service restart.

```
result.temporal_root present : True
result.temporal       present : False
result.init_v2_roots  present : False
```

**So the thesis "ignorance and challengeability are becoming first-class state" is not yet true.**
TIME is first-class. IGNORANCE and CHALLENGEABILITY are code, not contract.

---

## 2. THE BUILDERS WORK — PROVEN BY DIRECT INVOCATION

Called inside the deployed venv:

```python
from arifosmcp.tools.session import _build_init_v2_roots
out = _build_init_v2_roots(sid=..., actor_id='arif-fazil', identity_verified=True,
                           mode='init', objective='probe', success_criteria=['x'],
                           verification_requirements=['y'], sess={}, temporal_context={...})
```
→ returns all four roots. Real output, abridged:

```json
{"schema":"arifos.init.v2.roots","version":"2.0.0","ratified":"2026-09-20","status":"ACTIVE",
 "TEMPORAL_ROOT":       {"question":"WHEN am I?","clock_status":"UNKNOWN",
                         "clock_uncertainty_ms":5000,"ntp_drift_ms":null,
                         "falsification":"Any subsequent timestamp contradicts this anchor"},
 "OBJECTIVE_ROOT":      {"question":"WHAT am I trying to accomplish?","task_type":"EXECUTION",
                         "termination_rules":["goal_achieved","budget_exhausted",
                                              "hold_verdict","sovereign_interrupt"],
                         "falsification":"If success_criteria are met but objective is not
                                          achieved, criteria were wrong"},
 "NEGATIVE_KNOWLEDGE":  {"question":"WHAT DON'T I know?","unmeasured_scalars":["G", ...]},
 "PROVENANCE_ROOT":     { ... }}
```

**Every root carries its own `falsification` field.** This is genuinely good work — it is exactly the
computational form of `VOID = R − M_t`: the system enumerating what it is *not* justified in claiming.

Also verified: the builder is robust. It returns 8 keys with `objective=None`, and with
`actor_id=None, identity_verified=False, sess={}`. **No input I tried makes it raise.**

---

## 3. ★ SO WHERE DOES IT GO? THE FIX TARGETED THE WRONG LAYER

The receiving field exists — `schemas/session.py:608`, on `SessionManifest`, next to `temporal_root`:

```python
init_v2_roots: dict[str, Any] | None = Field(default=None, ...)
```

Both call sites are wired, and the code comment shows the drop was already spotted:

```python
# INIT v2 Roots last-mile wire (2026-09-20, additive — 333-AGI).
# The builder was threaded into only 1 of 3 arif_init return branches;
# the mode=init light path took this branch, so the 4 roots were built
# and dropped. Match the ~3980 principal-agent branch pattern.
init_v2_roots=_safe_build(_build_init_v2_roots, ...)
```

And `runtime/verbosity.py` was patched to preserve them — with a comment that names the defect class:

```python
# INIT v2 roots + temporal grounding context (2026-09-20, additive — F11/F9).
# Without these the 4 built roots and the temporal context were silently
# projected OUT of the envelope (built-then-dropped = F2 truth gap).
"temporal",
"init_v2_roots",
```

**But those entries live in `_MINIMAL_KEEP_TOP_LEVEL` and `_MINIMAL_KEEP_RESULT` — the MINIMAL lists.**
My probe ran at `verbosity=full`, where the minimal lists do not apply — and the fields are *still*
absent, alongside `temporal`, which is also absent.

Two independent builders (`_build_temporal_context`, `_build_init_v2_roots`), both verified working
in isolation, both return `None`-equivalent at the payload.

> **The fix was applied to the projection layer, but the values are missing upstream of projection.
> The keep-list cannot preserve a field that was never populated.**

Confirmed timeline:

```
18:13:42  verbosity.py + session.py written (the fix)
18:13:47  kernel restarted
18:14:33  probe: temporal_root ✅   temporal ❌   init_v2_roots ❌
```

The fix is live. It did not take.

---

## 4. WHAT THIS MEANS FOR THE ONTOLOGY

The mapping itself stands — it is not weakened by a wiring fault. Three points worth keeping:

- **`GOEX ≠ universe` is the load-bearing distinction.** REALITY is the universe; GEOX measures one
  physical portion of it. If GEOX is ever let to *be* the universe, the map has eaten the territory.
- **`VOID = R − M_t` is now partly computable, and that is the strongest part of the design.**
  `NEGATIVE_KNOWLEDGE.unmeasured_scalars` literally enumerates the scalars the system cannot yet
  justify. That is `M_t` reporting its own boundary rather than filling it.
- **WEALTH ≠ VOID is correctly separated.** WEALTH is a potential field (resources, scarcity,
  optionality, risk, future claims); VOID is the justified-claim boundary. Different organs.

But: **do not let the schema's existence be read as the capability's existence.** The three absent
roots are precisely the case in point — designed, built, ratified, and not delivered.

And CHRON: `temporal geometry` is the right description of what it orders, but its outcome loop has
still never closed — every verify check to date returned `due_count: 0` (4 of 4), with 19 active
predictions, 0 verified, 0 lessons. Geometry for *ordering* is live; geometry for *outcome* is not.

---

## 5. STATUS

**Zero mutation.** Read-only probes + direct function invocation in the deployed venv + this file.
No federation change. No canon change. No seal. No signature.

**Awaiting Arif:** whether the last-mile wiring of `init_v2_roots` is in scope for the stabilization
epoch — it is a one-layer fix and it is exactly P0 item 3 (INIT state ontology) in the external plan.
