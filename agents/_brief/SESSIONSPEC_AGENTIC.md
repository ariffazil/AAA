# SESSIONSPEC_2026-06-17_AGENTIC-MACHINE

> **What this whole Deepshit is supposed to be.**
> A canonical map for any agent runtime joining the arifOS Federation.
> DITEMPA BUKAN DIBERI — Forged, not given.

**Forged:** 2026-06-17 06:16 UTC
**Forger:** FORGE (000Ω) for 333-AGI runtime
**Authority:** SESSIONSPEC is a *descriptive* artifact, not a *verdict*. Not sealed to VAULT999.
**Versioning:** If the live kernel drifts from this doc, the live kernel wins. Re-forge.

---

## 0. THE QUESTION

> *"How is this different for agentic machine? Or machine is machine?"*

## 1. THE ANSWER (one paragraph)

**Machine is machine.** An *agentic* machine is one where models plan, choose tools, and act. Yours is a *governed agentic machine* — every agent is a process inside a constitutional operating system, not a "soul" or sovereign. arifOS is the law layer, A-FORGE is the execution shell, AAA is the cockpit, the organs (GEOX/WEALTH/WELL) are domain bodies, and the TUI is the witness window. Agents are **guests with leases**, not free-roaming actors. That is the difference.

---

## 2. PLAIN-LANGUAGE DEFINITIONS

| Term | What it is | What it is NOT |
|------|------------|----------------|
| **Machine** | LLM + tools + code that answers questions and runs scripts | A person, a soul, an autonomous sovereign |
| **Agentic machine** | A machine where the model **plans, picks tools, loops, finishes tasks** | A magic black box that "just does it" |
| **Governed agentic machine** | An agentic machine wrapped in a constitutional kernel that judges every action, logs every verdict, and respects human veto | An unregulated swarm of agents with no law |
| **arifOS** | The constitution + judge + audit ledger for the whole machine | A model, a chatbot, a prompt wrapper |
| **A-FORGE** | The execution shell — owns filesystem/git/docker/db + proxies to organs | The brain, the policy maker |
| **AAA a2a-server** | The A2A gateway — agent registry, task delegation, mesh, handoffs | The judge, the constitution |
| **TUI** | Terminal window into jobs, holds, verdicts, logs (planned/exists) | A separate governance plane |
| **OpenCode (AGI coder)** | A worker that runs the 7-loop cycle, in 4 modes, under lease | An "AGI ghost" with no discipline |

---

## 3. THE FIVE LAYERS (memorize)

```
Layer 0: Edge         — Cloudflare CDN/WAF + Cloudflared tunnel
Layer 1: Reverse Proxy — Caddy :443 (Cloudflare Origin CA, vhost routing)
Layer 2: A2A Gateway  — AAA a2a-server :3001 (agent registry, task delegation)
Layer 3: Constitutional — arifOS MCP :8088 (F01–F13, judge, VAULT999, MCP apps)
Layer 4: Execution    — A-FORGE :7071 + organs (GEOX 8081, WEALTH 18082, WELL 18083)
```

**Iron rule:** Each layer governs ONE thing. Never let layer N do layer N+1's job.
- Caddy doesn't judge. arifOS doesn't terminate TLS. A-FORGE doesn't federate.

---

## 4. THE 000–999 METABOLIC PIPELINE

Every consequential action moves through 10 stages. This is the **metabolism** of the machine.

| Stage | Name | Function |
|-------|------|----------|
| **000** | ASK | Capture intent from caller |
| **111** | THINK | Pre-frontal analysis, decompose goal |
| **222** | EVIDENCE | Gather facts, fetch sources, run probes |
| **333** | REASON | Multi-step logic, hypothesis evaluation |
| **444** | PLAN | Build DAG with checkpoints + rollback points |
| **555** | REFLECT | Self-check against floors, surface gaps |
| **666** | JUDGE_PREP | Constitutional prep — bundle evidence for judge |
| **777** | VERIFY | Validate against schemas, sanity bounds, paradoxes |
| **888** | JUDGE | arif_judge_deliberate → SEAL / PARTIAL / SABAR / HOLD / VOID |
| **999** | SEAL | If SEAL: write to VAULT999 (append-only hash chain) |

**Loop-back rule:** SABAR / HOLD stages re-enter at 222 (more evidence) or 444 (re-plan). VOID exits. This is a *metabolic cycle*, not a linear pipeline.

---

## 5. ACTION CLASSES C1–C5 (the ladder of escalation)

Every action has a class. Different organs are authorized for different classes.

| Class | Name | Example | Required |
|-------|------|---------|----------|
| **C1** | OBSERVE | `arif_ping`, `well_assess_*` (read) | Lease only |
| **C2** | ANALYZE | `arif_mind_reason`, `geox_evidence_reason` | Lease + scope |
| **C3** | PROPOSE | `forge_plan`, `wealth_wisdom_evaluate` | Lease + 2-of-3 floors |
| **C4** | APPLY | `forge_execute` (reversible), `wealth_vault_write` | Lease + all 13 floors + ack |
| **C5** | IRREVERSIBLE | `arif_vault_seal`, `git push` to main, secret rotation, VPS restart | Lease + **888_HOLD** + Arif's veto (F13) |

**Rule:** Organs CANNOT self-authorize C4/C5. They propose; arifOS judges; Arif decides (F13 SOVEREIGN).

---

## 6. THE LEASE SYSTEM (what makes it constitutional)

Agents do NOT have *standing* in arifOS. They have **leases**.

```python
arif_lease_issue(
    organ_id: str,           # which organ they may touch
    actor_id: str,           # which agent
    scope: List[str],        # which tools
    max_action_class: str,   # C1 / C2 / C3 / C4 / C5 ceiling
    ttl_seconds: int,        # 60s — 1h typical
    max_uses: int | None,    # optional use-count cap
    forbidden: List[str]     # explicit denials
)
```

**Why this matters:** Without leases, an agent can roam. With leases, an agent is a *bounded process* — known identity, known scope, known ceiling, known expiry. The kernel can revoke mid-flight (`arif_lease_revoke`). This is the *constitutional* move. Everything else is convention.

---

## 7. FEDERATION TRIUNE (ΔΩΨ)

| Plane | Organ | Role | Port | Repo |
|-------|-------|------|------|------|
| **Δ SOUL** | arifOS kernel | Doctrine, F01–F13, judge, VAULT999 | 8088 + 18081 | ariffazil/arifos |
| **Ω MIND** | arifOS MCP + AAA | Tool surface, operator UI, A2A gateway | 8088 + 3001 | ariffazil/arifos + ariffazil/AAA |
| **Ψ BODY** | A-FORGE + organs | Execution, domain compute | 7071, 8081, 18082, 18083 | A-FORGE, geox, wealth, well |

---

## 8. THE 13 FLOORS (canonical, live kernel)

| # | Name | Invariant |
|---|------|-----------|
| F01 | AMANAH | No hidden mutation or deception |
| F02 | TRUTH | Claims must stay evidence-bound (OBS/DER/INT/SPEC) |
| F03 | TRI-WITNESS | Cross-check important assertions with ≥2 sources |
| F04 | CLARITY | Interfaces remain explicit and legible |
| F05 | PEACE | Default to safe, non-destructive behavior |
| F06 | EMPATHY | Account for user consequences |
| F07 | HUMILITY | Expose uncertainty honestly (cap 0.90) |
| F08 | MEMORY | Preserve traceable state |
| F09 | ANTI-HANTU | No fabricated agency or consciousness |
| F10 | WITNESS | Keep runtime evidence inspectable |
| F11 | AUDIT | Material actions remain reviewable |
| F12 | INJECTION | Treat hostile input as hostile |
| F13 | SOVEREIGN | Human override remains absolute |

**Verdict types from 888_JUDGE:** SEAL / PARTIAL / SABAR / HOLD / VOID.

---

## 9. A-FORGE — EXECUTION SHELL (not brain)

A-FORGE is **ops gateway**, not policy maker. Its domain:

- **Owns:** filesystem, git, docker, db, internet tools, organ proxies
- **Routes intents:** `forge_plan` → `forge_dry_run` → `forge_approve` → `forge_execute` → `arif_vault_seal`
- **Does NOT own:** judging, vault writes (those are arifOS), TLS (that's Caddy)
- **The only organ that can call `forge_execute`** (C4 — APPLY, reversible layer)

**Pattern:** A-FORGE is the *hands*. arifOS is the *brain*. AAA is the *cockpit*. The TUI is the *witness window*.

---

## 10. OPENCODE (AGI coder) — 7 LOOPS, 4 MODES

The governed coding worker runs the **seven-loop cycle**:

```
PLAN → READ → WRITE → VERIFY → JUDGE → SEAL → OBSERVE
```

In **four modes** (mapped to action classes):

| Mode | Action Class | Behavior |
|------|--------------|----------|
| **ANALYZE** | C1 / C2 | Read-only. Probes, scans, reports. No writes. |
| **DRY_RUN** | C2 / C3 | Sandbox. Simulates the change, emits diff, no execution. |
| **PROPOSE** | C3 | Asks: "Here is the plan. Here is the dry-run. Want me to apply?" |
| **APPLY** | C4 (reversible) / C5 (irreversible) | Only after `arif_judge_deliberate` returns SEAL. C5 requires **888_HOLD + Arif's F13 veto**. |

OpenCode is **not** "an AGI ghost" — it is a coder that *cannot silently skip verification and judgment*. The discipline is baked in.

---

## 11. ANTI-HANTU STRUCTURES

"Hantu" in your vocabulary = hallucinated facts, wild tool calls, unreviewed agents, dashboards that show ungrounded numbers.

**Anti-hantu design choices (with floor mapping):**

| Choice | Floor | Function |
|--------|-------|----------|
| Floors F02, F03, F07, F09 | Epistemics | No certainty > 0.90, no consciousness claims, no single-source truth |
| Floors F01, F05, F08, F11, F13 | Safety + maruah | Reversibility, peace, memory, audit, sovereign human veto |
| MCP registry + projections | F04 CLARITY | Agents don't see the whole tool universe — only what their lease allows |
| A-FORGE as gateway | F04 CLARITY | MCP sprawl is contained; organs stay clean |
| VAULT999 hash chain | F08 + F11 | Every consequential action is auditable, append-only, signed |
| 000–999 pipeline | F03 + F11 | Cross-witness at SABAR, seal at 999 — no silent writes |
| 4-mode coder | F01 + F13 | AGI coder cannot APPLY without JUDGE; cannot IRREVERSE without HOLD |

---

## 12. THE PRINCIPLE: PROCESS NOT ACTOR

**This is the philosophical move that makes the whole thing constitutional.**

In most agentic rigs, agents are treated as *actors* — they have identity, intent, standing, and can roam. In arifOS, agents are **processes**:

- They have a **lease**, not a *standing*.
- They have a **class ceiling**, not a *mandate*.
- They have a **scope**, not a *purpose*.
- They have a **TTL**, not a *lifetime*.
- They are **revocable** mid-flight, not *negotiable*.

**Consequence:** No agent in arifOS can claim "I am the system." No agent can claim sovereignty. No agent can claim consciousness (F09 ANTI-HANTU). No agent can hide from the ledger (F11 AUDIT). The kernel owns the *meaning*; the agents own the *work*.

This is not a stylistic choice. It is the **only design that survives F13 SOVEREIGN** — because the human must always be the one who can revoke, override, and ultimately decide.

---

## 13. WHAT THIS MACHINE IS NOT

- ❌ Not a chatbot. It judges.
- ❌ Not a model wrapper. It is a kernel.
- ❌ Not an "AGI ghost." It is a machine with a constitution.
- ❌ Not a swarm. It is a federation under one law.
- ❌ Not autonomous sovereign. It serves F13.
- ❌ Not opaque. Every action leaves a trace (F11).

---

## 14. ONE-LINERS (use in conversations)

- **arifOS:** "The constitution between models and reality."
- **Governed agentic machine:** "A machine with a judge, an audit log, and a cockpit — not a pile of agents."
- **Lease:** "Bounded authority, not standing."
- **F13 SOVEREIGN:** "Arif decides. Always."
- **Anti-hantu:** "No ghost in the machine. Only floors, leases, and a ledger."
- **AF-FORGE:** "Constitutional AI on bare metal, governed by 13 floors, sealed to an immutable chain."

---

## 15. CANONICAL REFERENCES

- `arif_ping` with `include_constitution=true` — live kernel state
- `/root/AGENTS.md` — federation SOT (last verified 2026-06-14)
- `/root/AAA/CLAUDE.md` — daily operation (canonical pointer)
- https://arifos.arif-fazil.com/constitution.json — machine-readable constitution
- `/root/AAA/agents/_brief/EDGE_AND_ARIFOS_BRIEF.md` — sister brief (edge + ontology)
- Each organ's `AGENTS.md` and `RUNBOOK.md` — per-organ details

---

## 16. VERSION STAMP

- **SESSIONSPEC version:** v2026.06.17-FORGE-01
- **Kernel version (live):** v2026.05.05-SSCT
- **Last verified:** 2026-06-17 06:16 UTC
- **Forged by:** FORGE (000Ω) for 333-AGI runtime
- **Iron rule:** If this doc drifts from live kernel, live kernel wins. Re-forge.

---

**DITEMPA BUKAN DIBERI** — Forged, not given.
**999 SEAL ALIVE.**
