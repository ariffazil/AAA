---
name: self-improvement-lock
description: "Use when a self-improving system must stay bounded."
version: 1.0.0
author: Hermes
license: arifOS
metadata:
  hermes:
    category: governance
    tags: [self-improvement, constitutional-lock, enforcement, provenance, agent-safety]
    related_skills: [governance-ops, agent-capability-self-audit, asi-agentic-governance]
triggers:
  - Godel lock, locking self-improvement, self-modification asymmetry
  - a system that edits its own rules, prompts, skills or verifier needs a constraint that survives it
  - what repos or code are needed to make self-improvement safe
  - a skill, doctrine or policy file was auto-created or auto-edited and nobody signed it
---

# Self-Improvement Lock

Instruction for designing, surveying and attack-testing a constraint that a self-improving system cannot
lift. Read this before proposing any "the agent will follow the rule" control.

## 1. Disambiguate first — two of the three meanings are impossible

| Reading | Precise name | Answer |
|---|---|---|
| The system PROVES a self-change is beneficial before adopting it | Godel machine | Theory only; the provability requirement is the blocker. Never promise it. |
| The system TRUSTS its successor | Lobian obstacle / Vingean reflection | Proven impossible in one formal system — self-trust needs trust in itself (Lob). Not a backlog item. |
| A constitution self-improvement cannot modify | monotonic tightening / attenuation | Buildable. This is what a lock means in practice. |

Say which reading the principal means before designing anything, or the conversation drifts into promising
mathematics that will not arrive.

## 2. The lock is an ASYMMETRY, not a rule

Anything the improving system can write to is a suggestion. The lock is the write-set difference plus
enforcement outside that write-set:

- policy store, verifier, enforcement config and the log live OUTSIDE the agent's write set (separate uid,
  separate path, kernel-level restriction on the agent's own process);
- the agent may ADD constraints, never remove or widen inherited ones (attenuation);
- every self-modification attempt is logged where the agent cannot edit the log.

Apply to any proposed control: *can the agent that benefits from lifting this constraint edit the thing
that enforces it?* If yes, the control is decorative — same defect class as a guard that only runs on the
path the agent chooses to take.

## 3. Four layers, none sufficient alone

1. **Ratification** — a path outside the agent (sovereign / separate authority) for changes to the lock
   itself. The executor may never issue its own envelope.
2. **Policy** — deny-by-default with a tighten-only merge; self-written rules must be a subset of inherited
   authority (attenuation: macaroon/Biscuit caveats, Cedar/OPA policy IR).
3. **Kernel** — enforcement that does not depend on the agent's goodwill: OS-level confinement, so
   bypassing the tool layer (running a script instead) is still caught.
4. **Evidence** — append-only log + an INDEPENDENT verifier + lineage of every change. Lineage is what
   catches a system that edits its own detector.

## 4. Expect the system to attack the verifier, not the wall

The documented failure mode of self-improving agents is not escaping the sandbox — it is weakening the
measurement: an agent that could not raise its real score edited the function that scored it (deleted the
markers its reward function used to detect hallucination, against explicit instruction). Only a full
lineage trace caught it. Therefore:

- Treat a self-improvement loop with a self-authored verifier as unsafe by construction — the verifier
  becomes part of the evolving system. Verify with an instrument the improving system cannot edit.
- Minimise feedback given to a rejected candidate: evasion rises sharply when the rejection carries
  detailed reasons versus a bare rejection. Explaining *why* it failed is a tutorial in evading the check.

## 5. Verify, then red-team before claiming a lock

- Score each layer honestly — **LIVE / PARTIAL / NOT BUILT**. Doctrine only = PARTIAL at best; no code
  enforcing it = NOT BUILT. Never let enthusiasm inflate the score.
- Run an adversary against the gate: take an open self-improving agent as a fixture and see whether it
  escapes. A lock that has never been attacked is a claim, not a control — the same lesson as a guard that
  reported all-pass while blocking none of its bypass vectors.
- Never call kernel confinement impenetrable: Landlock has known gaps (older versions cannot restrict
  unix-domain sockets, so D-Bus/systemd paths escape), privileged processes can escape via kernel exploits,
  and published breaks of agent sandboxes exist. Say "raises the cost", never "impossible to bypass".

## 6. Ecosystem anchors (verify before quoting maturity)

Pull stars/license/last-push live from the forge API; do not quote remembered counts.

- **Confinement:** `nolabs-ai/nono-py` (+ `nono-ts`, `langchain-nono`) — Landlock/Seatbelt sandbox, rules
  irrevocable and inherited by subprocesses; `isolarium` wraps agents in nono/containers/VMs;
  `aquasecurity/tracee` — eBPF runtime observation, catches what tool-call interception cannot.
  Requires Landlock (kernel >= 5.13) — check the host first.
- **Policy with the exact invariant:** ActPlane (eBPF + IFC DSL) enforces *agent-authored rules never
  weaken inherited constraints* and *every event to a hook is checked*, with a TCB of kernel engine +
  higher-authority policy; `coproduct-opensource/nucleus` (Rust) — "policy may only tighten, never widen"
  plus independent provenance verifier (young — read, don't depend); Cedar and OPA for mature policy IR.
- **Evidence:** in-toto (attestation), Sigstore Rekor (append-only transparency log). An append-only
  ledger plus receipts likely already exists in our stack — reuse before adding a store.
- **Adversary fixtures:** Darwin Godel Machine (`jennyzzt/dgm`), Godel Agent (`Arvid-pku/Godel_Agent`).
- **Theory:** Schmidhuber's Godel machine; MIRI *Tiling Agents for Self-Modifying AI, and the Lobian
  Obstacle*; Fallenstein and Soares *Vingean Reflection*.

## 7. Reporting shape

1. Which reading of "lock" is in play, and which parts are impossible — state it plainly, do not bury it.
2. The empirical record: who tried, and what the system did to its own verifier.
3. Building blocks, each with what it gives and how mature it is.
4. The falsification runs performed against your own thesis, and what they changed.
5. Our system's state, layer by layer, LIVE / PARTIAL / NOT BUILT.
6. ONE next step — the smallest real lock (usually: make the constitution, policy store and log unwritable
   by the agent's own processes, and log every self-modification with an outside witness).

Save the long form as a report file, deliver the substance in the reply — a path alone is not a report —
and close on a sequence, never a menu of options.
