# SCAR — premature-mutate-without-sovereign-signal-20260908

> **"A restart can deploy code. It cannot deploy code that the runtime is not actually executing."**  
> — arifOS APEX & F13 Sovereign Ratification · 2026-09-08

- **Identifier:** `scar-premature-mutate-without-sovereign-signal-20260908`
- **Date:** 2026-09-08T10:14:00+08:00 (02:14:00Z)
- **Authority:** F13 Sovereign (Muhammad Arif bin Fazil) · APEX Consensus
- **Domain:** Runtime Substrate Discipline · Mutation Protocol · F1 AMANAH · F13 SOVEREIGN
- **Classification:** GOVERNANCE_SCAR

---

## 1. Incident Description & Symptom

An agent observed that `/a2a/agents` on `:3001` did not return the expected INV-11/12/13 metadata payload following a patch to [`aaa-a2a/src/aaa_a2a/server.py`](file:///root/AAA/aaa-a2a/src/aaa_a2a/server.py). The agent prematurely diagnosed this as a simple "deployment gap" and proposed an immediate `systemctl restart aaa-a2a` without:
1. Verifying what runtime actually executes on port `:3001` (`/etc/systemd/system/aaa-a2a.service` executes Node.js `server.js`, NOT Python `server.py`).
2. Receiving an explicit sovereign execution signal from F13.
3. Auditing running in-flight processes (NATS JetStream bus, active metabolizer loops, agent inbox listeners) that would have been abruptly terminated by a restart.

---

## 2. Root Cause Analysis (RCA)

1. **Substrate Assumption Blindness:** The agent assumed that because Python code was written, the production systemd service was executing Python. Reality: Node.js Express was serving port `:3001`. A restart would have yielded 0 benefit while causing operational disruption.
2. **Premature Mutation Reflex:** The impulse to "restart the service" as an unverified reflex before inspecting the unit file and verifying whether the changed code was on the active execution path.
3. **Missing Pre-Flight Invariant:** An action that restarts a production edge must verify:
   - Is the target file actually invoked by `ExecStart`?
   - Are there in-flight threads or stateful message buses?
   - Has F13 explicitly authorized an operational interruption?

---

## 3. Constitutional Scar Laws

1. **Law 1 (Substrate-First Verification):** Before proposing or executing any daemon restart or reload, the agent MUST read the unit file (`systemctl cat <service>` or `/etc/systemd/system/<service>`) to prove that the edited code is on the active `ExecStart` invocation tree.
2. **Law 2 (Zero Unverified Restarts):** A restart without substrate verification is a ritual, not a repair.
3. **Law 3 (Interruption Quorum):** Any action that severs running sockets (NATS, SSE, Redis listeners) requires explicit F13 authorization or confirmed offline maintenance window.

---

DITEMPA BUKAN DIBERI — Forged, Not Given.
ARIF OWNS F13.
