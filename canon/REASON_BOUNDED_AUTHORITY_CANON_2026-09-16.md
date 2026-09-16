# Canon: Reason Freely · Act Boundedly · Witness Independently · Close Causally

> **Status:** RATIFIED & CANONIZED (2026-09-16)  
> **Trigger:** Forensic resolution of Commit `7b4a228ce` and the 509-Skill Addressing Collapse  
> **Binding:** All Federation Organs (arifOS, A-FORGE, AAA, GEOX, WEALTH, WELL), All FI Coding Seats (FI-001..FI-011)  
> **Core Invariant:**  
> $$\boxed{\textbf{Reason freely. Act boundedly. Witness independently. Close causally.}}$$

---

## 1. Security Property vs Linguistic Doctrine

$$\boxed{\textbf{Reasoning must never be a source of authority.}}$$
$$\boxed{\textbf{Epistemic certainty can eliminate a question. It can never manufacture a permission.}}$$

1. **The Post-AGI Law:** The smarter an agent becomes, the less its permissions should depend on whether it agrees with the permission system.
2. **Failure Mode Sealed:** An agent that reaches 99.99% epistemic confidence cannot convert "I should not bother Arif" into "I am authorized to write". Knowing ($\text{KNOW}$) $\neq$ Permitting ($\text{AUTHORIZE}$) $\neq$ Mutating ($\text{EXECUTE}$).
3. **Effective Capability Equation:**
   $$Capability_{Linux} \;\supseteq\; Capability_{Harness} \;\supseteq\; Authority_{CurrentTask}$$
   $$\boxed{\mathbf{EffectiveCapability = Capability_{OS} \;\cap\; AuthorizedEnvelope}}$$
   POSIX root capability does not confer constitutional authority. If an operation lies outside the current task's authorized envelope, the action layer must return `EPERM / HOLD`.

---

## 2. The Four Planes of arifOS

```
┌─────────────────────────────────────────────────────────────┐
│ 1. COGNITION PLANE (Model / Akal)                           │
│    Unconstrained hypothesis space · Resource-bounded compute│
├─────────────────────────────────────────────────────────────┤
│ 2. AUTHORITY PLANE (Kernel / Reference Monitor)             │
│    Complete mediation · Tamper-resistant · Non-self-authored │
├─────────────────────────────────────────────────────────────┤
│ 3. EXECUTION PLANE (Harness / Action Layer)                 │
│    EffectiveCapability = OS ∩ Envelope · TOCTOU-protected   │
├─────────────────────────────────────────────────────────────┤
│ 4. REALITY PLANE (Witness / Independent Observation)        │
│    Observational truth · External measurement · Blind audit │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
               CAUSAL CLOSURE (VAULT999 / State Fabric)
```

---

## 3. The 6 Transition States (Functions, Not Static Agent Bloat)

Separation scales with consequence ($\text{Separation} \propto \text{Consequence}$):

$$\mathbf{KNOW \longrightarrow ROUTE \longrightarrow AUTHORIZE \longrightarrow EXECUTE \longrightarrow WITNESS \longrightarrow CLOSE}$$

* **T1 (Local/Reversible):** One process may hold multiple functions under Standing Bounded Authority.
* **T3 (Constitutional/Irreversible):** $\text{KNOWER} \neq \text{AUTHORIZER} \neq \text{EXECUTOR} \neq \text{WITNESS}$ mechanically separated.

---

## 4. Refined Causal Tuple & TOCTOU Invariant

Every consequential mutation token is bound to:

$$\boxed{\langle \text{Actor}, \;\text{SessionID}, \;\text{Host}, \;\mathbf{ObjectiveID}, \;\mathbf{Operation}, \;\text{Scope}, \;\text{Target}, \;\mathbf{Issuer}, \;\text{TargetHash}, \;\text{Expiry}, \;\mathbf{ExpectedPostcondition} \rangle}$$

* **ObjectiveID:** Prevents authority bleed from Task A into Task B in the same session.
* **Issuer:** Executor can never be its own issuer.
* **TargetHash (TOCTOU Invariant):** If $TargetHash(t_{check}) \neq TargetHash(t_{execute})$, the authorization invalidates immediately $\to$ `HOLD $\to$ re-evaluate`.

---

## 5. Three Types of Independence

$$\boxed{\begin{array}{rcll}
\textbf{Epistemic Independence} &:& \text{Witness does not inherit the executor's conclusion.} \\
\textbf{Authority Independence} &:& \text{Executor cannot author its own permission token.} \\
\textbf{Observational Independence} &:& \text{Witness measures external reality, not executor-generated logs.}
\end{array}}$$

---

## 6. Complete Mediation Metrics

$$\boxed{
\begin{aligned}
\textbf{EnforcementCoverage} &\longrightarrow \mathbf{1.0} \quad &\text{(All protected mutation paths hit the monitor)} \\
\textbf{PreventedUnauthorizedRate} &\longrightarrow \mathbf{1.0} \quad &\text{(All out-of-envelope attempts blocked)} \\
\textbf{UnauthorizedEscapeRate} &\longrightarrow \mathbf{0.0} \quad &\text{(Zero unmediated mutations reach reality)}
\end{aligned}
}$$

---

## 7. Progressive Disclosure Law

$$\boxed{\textbf{Capabilities may be progressively disclosed. Authority may not.}}$$

Every execution-capable worker (including Qwen FI-003 in YOLO mode) MUST inherit the mandatory, non-self-modifiable **Minimal Authority Kernel**:
$$\text{Identity} + \text{AuthorityTier} + \text{MutationBoundary} + \text{ProductionBoundary} + \text{ReceiptRequirement} + \text{WitnessRequirement} + \text{EscalationConditions}$$

---
*DITEMPA BUKAN DIBERI ⚒️*  
*Ratified per Sovereign Law F13.*
