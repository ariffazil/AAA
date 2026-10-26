# QUANTUM-PATHS.md — Rigorous Evaluation of Advanced & "Quantum" Horizons
**Standard:** Empirical Falsifiability · **Zero Tolerance for Metaphorical Pseudoscience**
**Document ID:** `QP-2026-10-25-RATIFIED`

---

## 1. Epistemic Demarcation & Excluded Scope

To maintain engineering integrity, we enforce three strict prohibitions:
1. **No Metaphorical Quantum Claims:** Agent consensus, tool combinations, or subjective feelings are *never* described as "quantum entanglement," "superposition," or "wavefunction collapse." Exploring alternative trajectories is termed **scenario exploration** or **multiverse tree search**.
2. **Simulator $\neq$ Quantum Advantage:** Running a state-vector simulator on classical x86 CPUs does not provide quantum speedup. It incurs exponential classical simulation overhead ($O(2^n)$).
3. **Emergence Must Be Measured Operationally:** "Emergence" is defined strictly as: *Higher held-out task completion rate and autonomous recovery, achieved with equal or lower human intervention and equal or lower cost, with zero unauthorized mutations.*

### Excluded Scope List
- Physical quantum hardware execution for natural language processing or tool orchestration (hardware noise, I/O latency, and state-preparation bottlenecks make this unviable).
- Machine consciousness or subjective qualia claims.
- Cryptographic post-quantum key exchange as a mechanism for agent intelligence (PQC is purely a threat-mitigation primitive, not a reasoning capability).

---

## 2. Bounded Opportunity Map

| Path Identifier | Operational Meaning | Bottleneck Addressed | Status | Primary Classical Baseline |
|---|---|---|---|---|
| **P-01: Specialist Routing** | Hierarchical intent decomposition with strict capability matching | LLM context pollution and wrong-tool selection | **NOW** | Single large prompt with full tool index |
| **P-02: Bitemporal Memory** | Valid-time and known-at indexed retrieval with contradiction invalidation | Hallucinated facts and stale context persistence | **NOW** | Flat vector similarity search (RAG) |
| **P-03: Sandbox World Models** | Predictive dry-run of tool side-effects before real-world execution | High rollback costs and irreversible mutation risk | **NEXT** | Direct speculative execution with rollback scripts |
| **P-04: Causal Intervention** | Do-calculus / Pearlian counterfactual evaluation of federation actions | Spurious correlations in agent error attribution | **NEXT** | Correlation / regression error logs |
| **P-05: Formal Verification** | Model-checking small state machines (ACT grants, lease lifecycles) | Edge-case race conditions in distributed execution | **NEXT** | Unit and property-based fuzz tests |
| **P-06: Verifier-Gated RL** | GRPO / RLVR fine-tuning on deterministic verification signals | Suboptimal multi-step reasoning trajectories | **RESEARCH** | Few-shot in-context learning + DSPy prompts |
| **P-07: Quantum-Inspired Classical** | Tensor networks / simulated annealing for combinatorial tool dispatch | NP-hard multi-agent scheduling under resource constraints | **RESEARCH** | Integer Linear Programming (CBC / GLPK) |
| **P-08: Physical Quantum QAOA/QML** | Mapping execution graphs to NISQ QPUs or quantum annealers | Massive discrete portfolio optimization | **REJECT** | Classical branch-and-bound / Simulated Annealing |
| **P-09: Post-Quantum Cryptography** | Ed25519 $\rightarrow$ ML-DSA (Dilithium) migration for VAULT999 signatures | Future Shor's algorithm signature forgery threat | **RESEARCH** (Security Track) | Ed25519 + HMAC-SHA256 |

---

## 3. Detailed Path Evaluations

### Path P-01: Hierarchical Specialist Decomposition & Routing
- **Operational Meaning:** Decompose sovereign tasks into orthogonal sub-tasks routed strictly to specialized organs (GEOX, WEALTH, WELL, KERNEL) rather than a single monolithic model prompt.
- **Bottleneck Addressed:** Context saturation, tool argument collision, and hallucinated capabilities.
- **Current Evidence:** Live probe demonstrated 118 tools on A-FORGE; presenting all 118 tools to a single LLM degrades instruction-following accuracy.
- **Smallest Experiment:** Run 20 synthetic multi-domain queries through a 2-tier classifier vs flat single-agent prompt; measure tool selection accuracy.
- **Cost Cap:** $0.50 USD in API tokens.
- **Falsifier:** If 2-tier routing adds >500ms latency without increasing tool selection accuracy by $\ge 15\%$.
- **Status:** **NOW** (Production implementation underway via AAA Router).

### Path P-02: Bitemporal Retrieval with Provenance & Expiry
- **Operational Meaning:** Every retrieved context item carries two independent timestamps: `valid_time` (when the fact was true in reality) and `known_at` (when the system observed it).
- **Bottleneck Addressed:** Agents citing superseded policies, stale URLs, or deprecated credentials.
- **Current Evidence:** CHRON store (`/root/chron/data/episodes.jsonl`) already implements bitemporal indexing with `store_generation`.
- **Classical Baseline:** Flat semantic vector search (e.g. standard Qdrant embeddings).
- **Smallest Experiment:** Query past policies with temporal boundaries; confirm that superseded policies are never injected into active reasoning contexts.
- **Status:** **NOW** (Standardizing across AAA and arifOS).

### Path P-03: Sandbox World Modeling & Scenario Exploration
- **Operational Meaning:** Branching disposable workspaces (bwrap / overlayfs) where agents simulate complex tool chains to observe state deltas before requesting sovereign authorization.
- **Bottleneck Addressed:** Irreversible operational errors and fear-based operator hesitation.
- **Current Evidence:** A-FORGE ephemeral genesis engine currently spins up bwrap containers in <200ms.
- **Classical Baseline:** Blind execution with manual rollback recipes.
- **Smallest Experiment:** Run 10 multi-file refactoring tasks in disposable bwrap worktrees; verify that failed runs leave zero host side-effects.
- **Status:** **NEXT**.

### Path P-04: Causal Inference over Intervention Logs
- **Operational Meaning:** Apply PyWhy / Do-calculus to agent execution logs to evaluate whether tool $A$ *caused* task success, or merely correlated with benign tasks.
- **Bottleneck Addressed:** Erroneous attribution of system stability to unnecessary safety bureaucracy.
- **Current Evidence:** `causal555-pywhy` skill exists in AAA catalog; requires structured intervention datasets.
- **Smallest Experiment:** Fit a directed acyclic graph (DAG) to 200 execution logs and test the conditional independence of tool retries given agent model.
- **Status:** **NEXT**.

### Path P-05: Formal Verification of Authority State Machines
- **Operational Meaning:** Express the 7-step Reality Loop and ACT capability token state transitions in TLA+ or Alloy to mathematically prove the absence of deadlock, unhandled timeout states, and privilege escalation.
- **Bottleneck Addressed:** Race conditions in distributed lease acquisition and crash recovery.
- **Smallest Experiment:** Model the `KernelAuthValidator` and `LeaseManager` protocol (under 100 lines of TLA+); run TLC model checker to verify safety invariant: $\forall s \in \text{States}: \text{Mutating}(s) \implies \text{Authorized}(s) \land \text{LeaseHeld}(s)$.
- **Cost Cap:** 0 USD (local open-source tools).
- **Falsifier:** Discovery of a deadlock or state explosion rendering model checking uncomputable.
- **Status:** **NEXT**.

### Path P-06: Verifier-Gated Reinforcement Learning (RLVR / GRPO)
- **Operational Meaning:** Train local small language models (e.g. Qwen-2.5-Coder-7B) using Group Relative Policy Optimization (GRPO), rewarded strictly by deterministic unit test and effect verifiers.
- **Bottleneck Addressed:** High API costs and rate limits of frontier proprietary models for routine code refactoring.
- **Hard Safety Gates:**
  1. Verifiers must be completely deterministic and run in isolated read-only environments.
  2. Reward model must not be an LLM (prevents sycophancy and reward gaming).
  3. Minimum 500 validated task-verifier pairs required before training ignition.
- **Status:** **RESEARCH** (Pending verifier dataset curation).

### Path P-07: Quantum-Inspired Classical Optimization (Tensor Networks / Annealing)
- **Operational Meaning:** Use simulated annealing or tensor-network contractions on classical GPUs to solve high-dimensional asset allocation or multi-agent scheduling problems.
- **Bottleneck Addressed:** Combinatorial explosion in WEALTH portfolio balancing or 50+ agent schedule optimization.
- **Classical Baseline:** Open-source Mixed Integer Linear Programming (HiGHS / SciPy linprog).
- **Stopping Condition:** If classical HiGHS solver finds the global optimum in <100ms, terminate quantum-inspired exploration immediately.
- **Status:** **RESEARCH**.

### Path P-08: Physical Quantum Computing (NISQ / QPUs)
- **Operational Meaning:** Offloading reasoning or optimization to IBM Quantum, D-Wave, or Rigetti QPUs via cloud APIs.
- **Rigorous Bottleneck Analysis:**
  - Data transfer latency to cloud QPUs: 200–2,000ms.
  - Queue waiting times on public QPUs: minutes to hours.
  - State preparation (input encoding): $O(N)$ overhead completely destroys theoretical $O(\sqrt{N})$ Grover speedup for database search.
  - Physical qubit error rates ($10^{-3}$ to $10^{-4}$) require hundreds of physical qubits per logical qubit, unavailable today.
- **Definitive Verdict:** **REJECT**. No demonstrated quantum advantage exists for agent tool selection, reasoning, or federation orchestration. Classical algorithms running on modern CPUs/GPUs outperform NISQ QPUs by orders of magnitude at zero extra cost.

### Path P-09: Post-Quantum Cryptography (PQC) Security Track
- **Operational Meaning:** Transitioning VAULT999 signature verification from Ed25519 to NIST-standardized Post-Quantum algorithms (ML-DSA / FIPS 204).
- **Bottleneck Addressed:** Long-term archival integrity against "harvest now, decrypt/forge later" attacks.
- **Implementation Reality:** Larger signature sizes (ML-DSA-44 is 2,420 bytes vs Ed25519's 64 bytes). Increases receipt payload sizes 38x.
- **Status:** **RESEARCH (Dedicated Security Track)** — Do not deploy until receipt storage architecture is optimized.
