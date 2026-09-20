# W3 IS A CONSTANT — THE SCALAR THAT GOVERNS THE SYSTEM IS FABRICATED
> 2026-09-20 ~18:55 MYT · KVM8 · HERMES · read-only · zero mutation
> Trigger: Arif — *"Kita sedang govern atas nombor yang tak wujud."*

---

## VERDICT: CONFIRMED TO THE DIGIT

W3 is not a measurement. It is `∛(0.42 × 0.99 × 0.99)` — a constant computed from three
hardcoded values, reported as `"status": "MEASURED"`.

```
reported W3 = 0.7439
recomputed  = ∛(human × ai × earth)
            = ∛(0.42 × 0.99 × 0.99)
            = ∛0.41174
            = 0.7439          ← exact match
```

---

## THE FABRICATION, IN SOURCE

`runtime/rest_routes/rest_routes.py:962-964`:

```python
"human_witness": _WITNESS_DEFAULTS["human"],                          # 0.42 — constant
"ai_witness": 0.99,                                                   # 0.99 — constant
"earth_witness": (0.99 if live_containers else _WITNESS_DEFAULTS["earth"]),  # BOOLEAN
```

None of the three is measured:

| Channel | Value used | What it actually is |
|---|---|---|
| human | **0.42** | `_WITNESS_DEFAULTS["human"]` — a fallback constant |
| ai | **0.99** | a literal in the function body |
| earth | **0.99** | `if live_containers` — a boolean on container liveness, else `0.26` |

And the fallback logic at line 1073-1076 guarantees the constant wins whenever a channel is
absent — which it always is for `human`:

```python
resolved_witness = {
    k: witness.get(k) if witness.get(k) is not None and witness.get(k) != 0.0 else v
    for k, v in _WITNESS_DEFAULTS.items()      # defaults {human:0.42, ai:0.32, earth:0.26}
}
```

Live probe of `_build_governance_status_payload()`:

```
witness used for W3 : {"human": 0.42, "ai": 0.99, "earth": 0.99}
apex_scalars        : W3 {"value": 0.7439, "status": "MEASURED"}
```

---

## THE DOCTRINE ALREADY FORBIDS THIS — IN A DIFFERENT FILE

`runtime/apex_primitives.py:202-207`, written **2026-08-09**, says:

> *"P0 2026-08-09 v2 (OPENCLAW): W3 must NOT be PHI. PHI is scar pressure (repeated-failure
> feedback) — not tri-witness. Canonical W3 = ∛(H×AI×Ext) needs live witness channels, which
> tool-call metrics do not carry. Computed in rest_routes from resolved_witness.
> **Here: honest None, never an inflated proxy.**"*

```python
"W3": None,     # apex_primitives.py:207 — honest
```

**Two implementations of one scalar:**

| File | Behaviour | Surfaces? |
|---|---|---|
| `apex_primitives.py` | returns `None` — honest, per its own comment | ❌ no |
| `rest_routes.py` | returns `0.7439` from three constants | ✅ **yes** |

The doctrine says *"never an inflated proxy."* The inflated proxy is the one that ships.

---

## WHY THIS MATTERS MORE THAN ANY OTHER FINDING TONIGHT

**F3 TRI-WITNESS requires ≥ 0.75** (`constitution.md:10`, `civ-21.md:162`, `musyawarah.md:30`).

```
W3 = 0.7439   <   0.75   → below the constitutional floor
```

The system sits **permanently just below** its own witness floor — and it **cannot move**, because
two of its three inputs are constants and the third is a boolean. A scalar that cannot change is
not governing anything; it is a fixed gate.

This answers the three things Arif measured:

- **"W3 still null, never measured"** — now measured, but neither. It was `None` on one surface and
  a constant on another. Neither state was ever a measurement.
- **"G = 0.4625, flat"** — G and C_dark come from `compute_apex_from_metrics()` (real tool-call
  telemetry). Those move. W3 does not, because it is not wired to that pipeline at all.
- **"Session token says 0.94, federation says null"** — two surfaces, two sources, neither measured.
  No judge exists between them. Exactly as Arif named it.

**And it explains the learning loop's silence.** CHRON shows 0 lessons. If the credibility scalar
that would gate promotion is a constant, no evidence can ever move it. The pipe is not blocked
downstream — its input is not connected.

---

## WHAT IT DOES NOT MEAN

This is **not** a security hole and **not** an incident. Nothing unauthorised happened. The value
is *honest in intent* — a placeholder wearing a `MEASURED` label. The defect is the **label**, and
that label is the one class this whole session has been chasing:

```
Declared ≠ Actual
```

`apex_primitives.py` chose *declared UNMEASURED*. `rest_routes.py` chose *declared MEASURED*. The
schema carried both and nothing reconciled them.

---

## THE FIX (NOT APPLIED — needs an authority decision)

Not a rewrite. One of:

1. **Honest None** — align `rest_routes.py` to `apex_primitives.py`. W3 reports UNMEASURED until
   real witness channels exist. The floor then correctly reports *cannot witness* instead of
   *slightly failing*.
2. **Wire the channel** — make `human_witness` an actual measurement (a real trip-witness count or
   a signed human attestation), and make `earth_witness` a graded signal rather than
   `if live_containers`.

Option 1 is *remove > duplicate* — the anti-chaos rule. Option 2 is the real work Arif named as
*"bukan kerja sehari."*

**Both are one file.** Neither is a new organ.

---

## ★ ADDENDUM — THE 0.94 FOUND. TWO SURFACES, TWO DIFFERENT SETS OF INVENTED CONSTANTS.

> 2026-09-20 19:05 MYT · closes the one item this file marked UNMEASURED.

Arif observed: *"session token cakap W3: 0.94. Federation surface cakap W3: null, UNMEASURED.
Dua jawapan, satu mesin, masa yang sama."*

Both numbers are now traced. **They are two different constants from two different files.**

`runtime/chatgpt_integration/apps_sdk_tools.py:127-129` — the ChatGPT connector path:

```python
"witness": {
    "human": _clamp_score(resolved_witness.get("human"), 0.95),
    "ai":    _clamp_score(resolved_witness.get("ai"),    0.94),
    "earth": _clamp_score(resolved_witness.get("earth"), 0.93),
},
"witness_ai":    _clamp_score(resolved_witness.get("ai"),    0.94),
"witness_earth": _clamp_score(resolved_witness.get("earth"), 0.93),
```

`_clamp_score(value, default)` returns `default` on `TypeError/ValueError` — i.e. whenever the
channel is absent, the constant is served.

**Arithmetic, exact:**

```
∛(0.42 × 0.99 × 0.99) = 0.7439   ← rest_routes.py  (HTTP /health)     → "W3: 0.7439"
∛(0.95 × 0.94 × 0.93) = 0.9400   ← apps_sdk_tools  (ChatGPT connector) → "W3: 0.94"   ← EXACT
∛(0.42 × 0.32 × 0.26) = 0.3269   ← _WITNESS_DEFAULTS (the fallback)
```

**So the disagreement is not between two witnesses. It is between two fabrications.**

| Surface | Constants (human/ai/earth) | W3 | Label |
|---|---|---|---|
| HTTP `/health` | 0.42 · 0.99 · 0.99 | **0.7439** | `"MEASURED"` |
| ChatGPT connector | 0.95 · 0.94 · 0.93 | **0.9400** | served as witness scores |
| `apex_primitives.py` | — | **None** | `UNMEASURED` (honest) |

Three implementations of one constitutional scalar. Two invent a number, one declines to. The two
that invent are the two that ship to a surface. None of the three touches a live witness channel.

And every one of the three sets sits on a different side of the F3 floor of 0.75:

```
0.3269  below floor   (fallback)
0.7439  below floor   (HTTP)        ← the system is "failing" by 0.0061
0.9400  above floor   (connector)   ← the system is "passing" comfortably
```

**The same machine reports the federation as both failing and passing the tri-witness floor,
simultaneously, on two connectors — and neither figure was ever measured.**

That is the sharpest possible form of the defect Arif named: *kita govern atas nombor yang tak wujud.*

---

## STATUS

**Mutations: ZERO.** Read-only source inspection + direct function invocation in the deployed venv
+ this file. No federation change. No canon change. No seal. No signature.
