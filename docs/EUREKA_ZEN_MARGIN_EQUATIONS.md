# EUREKA·ZEN Margin — Full Equation Metrics

> **Kernel × QQQQ × Agent — how the numbers couple.**
> **GENESIS 022 · Forged 2026-07-18 · F13 SOVEREIGN**
> **Iron line: Zen is not the last 2%. Zen is the first 10% of every full tank.**

**Sealed SOT (do not fork prose):**  
`/root/A-FORGE/forge_work/2026-07-18/EUREKA-ZEN-METRICS-FRAMEWORK.md`  
VAULT999 seq 26 · `326b0439a41d8b59bed1d3a453c81d23d020b6eef78df65f42cb854946757b6c`

Code (implements sealed equations — no second doctrine):
- `arifOS/arifosmcp/geometry/eureka_zen.py` — U_eureka/U_zen, ROI, G, C_dark, W³, tank
- `arifOS/arifosmcp/runtime/qqqq_metrics.py` — QQQQ + I_total coupling
- Doctrine: `arifOS/GENESIS/022_EUREKA_ZEN_MARGIN.md`

---

## 0. Short answer (coded)

```
U_eureka(tank=0.80) >> U_zen(tank=0.80)   → eureka wins (abundance)
U_zen(tank=0.03)   >> U_eureka(tank=0.03)  → zen wins (margin)

ROI_zen(50%) > ROI_zen(3%)   # full choice set beats constrained

The margin is not where zen belongs.
The margin is where zen is finally allowed.
```

```python
from arifosmcp.geometry import u_eureka, u_zen
print(f"Abundance: E={u_eureka(0.8):.2f} Z={u_zen(0.8):.2f}")
print(f"Margin:    E={u_eureka(0.03):.2f} Z={u_zen(0.03):.2f}")
```

---

## 1. Why zen sits at the margin (not abundance)

| Phase  | Mode | Feels like | Physics |
|--------|------|------------|---------|
| Eureka | Open, multiply paths | Abundance | Entropy **injection** \(J\) |
| Zen    | Close, compress, seal | Scarcity | Entropy **export** \(X\) |

Abundance rewards expansion. Zen is negative work. Negative work is deferred until the budget forces export. The margin is not where zen *belongs* — it is where zen is finally *allowed*.

---

## 2. Tank

\[
T = \frac{B_{\text{remaining}}}{B_{\max}} \in [0,1]
\]

| Symbol | Default | Meaning |
|--------|---------|---------|
| \(T_{\text{critical}}\) | 0.02 | Expansion illegal; only compression pays |
| \(T_{\text{margin}}\) | 0.03 | First honest audit (reflex zen) |
| \(T_{\text{abundance}}\) | 0.50 | Forced export before next eureka |
| \(Z_{\text{first}}\) | 0.10 | First 10% of full tank is zen work |

```python
from arifosmcp.geometry import compute_eureka_zen, EntropyFlux
m = compute_eureka_zen(0.9, EntropyFlux(inject=5, export=0), proposing_eureka=True)
# m.gate_label == ZEN_BEFORE_EUREKA
```

---

## 3. Entropy flux & F4

\[
\Delta S_{\text{session}} = J - X \leq 0 \quad \text{(F4 CLARITY)}
\]

\[
M = \frac{X}{J + \varepsilon}, \quad \varepsilon = 10^{-6}
\]

- \(M \ge 1\): export ≥ inject — healthy metabolism  
- \(M < 1\) under abundance: metabolic debt  
- \(M \to 0\): pure eureka debt → margin zen inevitable  

---

## 4. Phase machine

```
T ≤ 0.02                     → MARGIN_ZEN          (export only)
0.02 < T ≤ 0.03              → MARGIN_REFLEX
T ≥ 0.50 ∧ ¬export_done      → ABUNDANCE_MUST_ZEN  → label ZEN_BEFORE_EUREKA
T ≥ 0.50 ∧ export_done       → ABUNDANCE_EUREKA_OK
else                         → NORMAL_DUAL
```

**Iron rule (label, not silent block):**

\[
T \ge T_{\text{abundance}} \land \neg\text{export} \land \text{proposing eureka}
\;\Rightarrow\; \texttt{ZEN\_BEFORE\_EUREKA}
\]

---

## 5. QQQQ (four layers)

| Q | Name | Floor | Gate |
|---|------|-------|------|
| Q1 | Qualitative ≥5 paths + NULL + INVERSE | F2 | option-space honesty |
| Q2 | BR, REV, time, conf, PA | F4 | measured trade-offs |
| Q3 | precedent, interference, superposition, observer | F7 | second-order |
| Q4 | Zen export block | F4 + metabolism | forced export at abundance |

Q4 envelope:

```yaml
q4_export:
  export_actions: [dirty_trees_to_zero, kill_false_restart]
  delta_s_claim: -0.3    # must be ≤ 0
  tank_at_export: 0.9
  deferred_to_margin: false
  completed: true
```

Verdicts: `QQQQ_COMPLETE` · `INADMISSIBLE-Q1..Q4`

```python
from arifosmcp.runtime.qqqq_metrics import validate_qqqq, gate_qqqq
check = validate_qqqq(envelope, intent_class="RECOMMENDATION", tank=0.9)
```

---

## 6. Agentic Intelligence

\[
\mathrm{AI} = C \times G_{\mathrm{nd}} \times \mathrm{Auth} \times \mathrm{Cont} \times \mathrm{Acc} \times \mathrm{Met}
\]

| Factor | Zero means |
|--------|------------|
| \(C\) Capability | passive assistant |
| \(G_{nd}\) Grounding | hallucinating agent |
| Auth | rogue action |
| Cont | amnesiac tool |
| Acc | untraceable machine |
| Met | repeating system (eureka debt) |

\[
\mathrm{Met} = \mathrm{clamp}\!\left(\frac{X}{J+\varepsilon},\,0,\,1\right)
\]

Idle session (\(J=X=0\)): Met = 1 (neutral, does not collapse AI).

---

## 7. F8 Genius & Ψ Vitality (kernel)

\[
G = (A \times P \times X_{\mathrm{exec}} \times E^{2})\times(1-h) \ge 0.80
\]

\[
\Psi = \frac{|\Delta S|\cdot\mathrm{Peace}^{2}\cdot\kappa_{r}\cdot\mathrm{RASA}\cdot\mathrm{Amanah}}{\mathrm{Entropy}+\mathrm{Shadow}+\varepsilon}
\]

\(\Psi \ge 1\): homeostatic candidate for SEAL.

---

## 8. Coupling (one admissible predicate)

\[
\mathrm{admissible} =
  \mathrm{kernel\_floors\_pass}
  \land \mathrm{qqqq\_COMPLETE}
  \land \mathrm{AI} > 0
  \land \Delta S_{\mathrm{session}} \le 0
\]

```python
from arifosmcp.runtime.qqqq_metrics import compute_kernel_agent_qqqq

full = compute_kernel_agent_qqqq(
    tank=0.9,
    inject=1.0,
    export=2.0,
    envelope=envelope,           # Q1–Q3 + q4_export
    intent_class="RECOMMENDATION",
    capability=0.9,
    grounding=0.9,
    authority=1.0,
    continuity=0.8,
    accountability=0.9,
    kernel_floors_pass=True,
)
print("\n".join(full.summary_lines()))
# full.coupling["should_force_zen"]
# full.agentic.agentic_intelligence
# full.eureka_zen.phase / .gate_label / .metabolic_balance
```

---

## 9. Agent loop (where metrics sit)

```
human intent
  → identity bind (arif_init)
  → authority + lease
  → intelligence proposes (paths = Q1)
  → QQQQ metrics (Q1–Q4) + EUREKA·ZEN tank probe
  → kernel floors F1–F13 + 16-gate chain
  → SEAL | HOLD | VOID
  → A-FORGE execute (only after SEAL + lease)
  → verify → memory revise → VAULT999 seal
  → COOL = zen export (must not wait for 2%)
```

Cooling **is** zen. Cooling only at margin = metabolic imbalance.

---

## 10. SALAM one-liner

```
│ Zen is not the last 2%. Zen is the first 10% of every full tank.
```

---

*DITEMPA BUKAN DIBERI — equations over folklore.*
