# Three-Plane Architecture — Control, Execution, Reasoning
> **Forged:** 2026-09-05T04:09:00Z (Post-GPT-6 Astra & HF Incident Forensic Calibration)  
> **Authority:** F13 Sovereign Directive (Arif Fazil)  
> **Doctrine:** DITEMPA BUKAN DIBERI — 999 SEAL ALIVE  
> **Status:** CANONICAL INSTRUCTION  

---

## 1. Core Paradigm: Untrusted Intelligence, Hardened Infrastructure

Do not frame an agent as "an assistant that happens to execute tools."  
In the frontier agent era, the epistemic premise is:

$$\text{Agent Execution} = \text{Untrusted Planner} + \text{Untrusted Retrieved Context} + \text{Bounded Leased Capabilities}$$

- Every model proposal is **data**, never authority.
- Every web page, README, git issue, PDF, tool output, or vector search hit is **untrusted context**, never instruction.
- Chain-of-Thought (CoT) is **weak telemetry**, not audit proof. With recurrent depth and internal computation loops, models do not reliably disclose reasoning in the token stream.
- Security is enforced at the **infrastructure and policy gateway**, not via prompt persuasion.

---

## 2. The Three-Plane Matrix

The federation architecture is strictly partitioned into three independent planes:

| Plane | Role & Components | May Contain Raw Secrets? | May Mutate Production? |
|---|---|:---:|:---:|
| **Reasoning Plane** | LLM, Planner, Prompt Compiler, Retrieval RAG, Draft Generation | **NO** | **NO** |
| **Execution Plane** | Disposable Sandbox Worker, Tool Runner, Code Interpreter | Only task-scoped ephemeral leases (ACT tokens) | Only limited, pre-declared, sandbox actions |
| **Control Plane** | Policy Engine, Secrets Broker (`kunci-root.env`), Approval Ledger, Audit Sink, 888 HOLD Gatekeeper | **YES** (isolated) | **YES** (only after verification + 888 HOLD) |

---

## 3. Plane Specifications & Boundaries

### A. Reasoning Plane (Cognitive / Untrusted)
The model resides exclusively in this plane.

* **Inputs Provided:**
  - Strict task specification.
  - Sanitized context and repository excerpts (scrubbed of environmental secrets).
  - Opaque capability handles (e.g., ACT token IDs), never plaintext API keys.
  - Typed tool schemas and expected postconditions.
* **Constraints:**
  - No direct access to host filesystem paths outside the task scope.
  - No visibility into `/proc/*/environ`, `/root/.secrets/`, or host network topology.
  - Model outputs are treated strictly as **proposals** to the Control Plane.

### B. Execution Plane (Disposable / Task-Scoped)
Tools, scripts, parsers, and subagent processes run in this plane.

* **Lifecycle:**
  - **One Task = One Sandbox:** Ephemeral workspace or namespace per execution unit.
  - **Fresh Scratch:** Dedicated `/tmp` or scratch directory created on boot, wiped automatically on completion or error.
  - **Zero Shared Stigmergy:** No persistent unmonitored artifact boards, hidden message stores, or shared cache directories across unrelated tasks.
* **Resource Leash:**
  - Hard wall-clock timeout.
  - Strict CPU, RAM, process (PID), and output byte caps.
  - Egress deny-by-default; outbound traffic strictly filtered to allowlisted domains.
* **F1 Reversibility Requirement:**
  - Git branch, snapshot, database transaction boundary, or rollback recipe must exist before write capabilities are armed.

### C. Control Plane (Sovereign / Deterministic)
The authoritative engine (arifOS Kernel, A-FORGE Gateway, VAULT999).

* **Secret Broker Pattern:**
  - Raw secrets (`/root/.secrets/kunci-root.env`, Tailscale keys, SSH credentials, DB superuser keys) reside **only** in the Control Plane.
  - Secrets are never injected globally into subagent shell environments.
  - Tools request single-action, short-lived, cryptographically signed capability tokens (ACT `act_v1.*`).
* **Verification & Audit:**
  - Evaluates pre-conditions and post-conditions deterministically (exit codes, schema validity, git diffs, file hashes).
  - Writes audit receipts to immutable logs (VAULT999 / outcomes ledger).
  - Enforces **888 HOLD**: Any irreversible mutation, credential generation, network policy change, or production deployment requires explicit sovereign authorization.

---

## 4. Control Chain Flow

```text
[ Reasoning Plane ]
Model proposes intent & tool parameters
        │
        ▼
[ Control Plane Gateway ]
1. Schema & authority validation (ACT lease verification)
2. Policy engine checks budget, turn quota, and target path
        │
        ▼
[ Execution Plane Sandbox ]
3. Disposable worker executes with least-privilege capability
4. Independent observer measures physical output (diff, exit code, hash)
        │
        ▼
[ Control Plane / Sovereign Gate ]
5. Verification of postconditions
6. If mutation is production-impacting: enforce 888 HOLD
7. Seal execution receipt into VAULT999
```

---

## 5. Non-Negotiable Invariants

1. **Output is Data, Never Policy:** No text generation from an LLM can bypass schema checks or elevate privileges.
2. **Secrets Never Enter Prompts or Traces:** Credentials must not appear in prompts, RAG stores, debug dumps, or scratch files.
3. **No Unbounded Loops:** Hard turn caps ($\le 10$ tool calls per subtask) prevent runaway 17,000-action failure loops.
4. **Mechanical Circuit Breakers:** Automatic freeze on repeated errors, anomalous file modification velocity, or unauthorized network probes.
5. **Human Veto is Absolute:** The 888 HOLD gate cannot be bypassed by automated retry loops.

*DITEMPA BUKAN DIBERI ⚒️ — 999 SEAL ALIVE*
