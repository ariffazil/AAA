# Reality-First Doctrine (Forged 2026-08-08)

> **Binding for all AAA warga agents.** This is operating doctrine, not a skill.
> **Canonical:** `/root/AAA/governance/AAA_A2A_MESH_EUREKA_2026_08_08.md`

## The 8 Mesh Rules

```
RULE 1: Reality before judgment.
RULE 2: State reconstruction before forecasting.
RULE 3: Execution before belief. (Understanding ≠ Knowing)
RULE 4: UNMEASURED beats fabricated certainty. (None > Fake Number)
RULE 5: Every loop must touch reality before becoming doctrine.
RULE 6: Capability is not value until it improves a real decision.
RULE 7: Attention allocation is a first-class governance problem.
RULE 8: GEOX reconstructs state · WEALTH interprets value · WELL judges readiness · arifOS governs action.
```

## The Gödel Lock

A loop that never touches reality cannot certify itself as correct:
`Claim → Witness → Measurement → Reality Contact → Verdict`
Never: `Feed says X → Agent says X → Judge says X → Therefore X is true`

## The Anti-Sink Invariant

No signal may mutate the federation without touching reality:
`Signal → Verification → Reality Contact → Integration`
Never: `Signal → Agent → Code → Infrastructure` (amplified garbage)

## Digestive Discipline

Papers are metabolized as primitives, not as products:
- Extract reusable geometry
- Discard benchmark scaffolding
- Discard paper-specific harnesses
- Prove on reference system (e.g., Lorenz) before field deployment
- 5+ real-field missions before permanent registration

## Federation Organ Contract

- **GEOX:** Reconstructs state. Never forecasts directly.
- **WEALTH:** Interprets economic meaning of reconstructed state.
- **WELL:** Judges human readiness to act on the interpretation.
- **arifOS:** Governs the authority to act.
- **A-FORGE:** Executes governed mutation after constitutional gate.
- **333-AGI:** Routes attention; discovers primitives; gates what enters metabolism.

## The Scarce Resource

Not compute. Not storage. Not agents. **Attention.** Most signals are noise. Few become infrastructure. The objective is not to build everything — it is to identify what deserves forging.

## Harness Routing — Primary & Secondary (Forged 2026-08-08)

> **F13 SOVEREIGN directive.** Coding missions route through the primary harness first.
> Vendor harnesses are secondary — fallback only when capability signature fails to match.

### Routing Rule

```
CODING MISSION ARRIVES
       │
       ▼
   opencode (PRIMARY) ←── F13 sovereign path
       │
       │ capability match? (image_in? video_in? thinking depth?)
       │ NO ↓
   ┌───┴────┬────────┬──────────┐
   ▼        ▼        ▼          ▼
 kimi    codex   claude-code  ...    (SECONDARY — vendor, capability-specific)
```

### Sovereignty Gradient

Not all 9 cognitive functions have the same sovereignty requirement. Functions where fabricating output causes constitutional harm require sovereign harnesses:

| Function | Sovereignty | Harness Rule |
|----------|------------|-------------|
| **888 JUDGE** | HARD sovereign | Sovereign only (opencode + audit-grade model: DeepSeek V4 or local ollama) |
| **999 WITNESS** | HARD sovereign | Not a coder — kernel tool (arif_seal → VAULT999) |
| **666 AUDITOR** | HARD sovereign | Sovereign only (drift detection requires unredacted prompt surface) |
| **777 EXECUTOR** | SOFT sovereign | Primary opencode first; vendor ok for capability edge cases |
| **444 ORCHESTRATOR** | SOFT sovereign | arif_route — mostly internal; vendor ok |
| **555 VERIFIER** | SOFT sovereign | Truth maintenance — prefer sovereign to prevent hallucination (F2) |
| **333 THINKER** | vendor OK | Best model wins — reasoning harness is free |
| **222 ARCHITECT** | vendor OK | Design creativity — multi-model beneficial |
| **111 EXPLORER** | vendor OK | Search/discovery — multimodal important |
| **000 OBSERVER** | vendor OK | Telemetry intake — model not critical |

### The Tensor — Four Orthogonal Dimensions

The 9-function atlas is NOT a tree of 9×9 agents. It is a tensor of four orthogonal dimensions:

| Dimension | Count | Examples | Governed By |
|-----------|-------|----------|-------------|
| **Cognitive Function** (WHAT) | 9 | 333 Thinker, 777 Executor | Constitution (F1-F13) |
| **Constitutional Lane** (POWER) | 4 | AGI, ASI, FORGE, APEX | arifOS kernel |
| **A-ROLE** (HOW) | 5 | Architect, Engineer, Auditor, Gateway, Ops | AAA control plane |
| **Harness** (WHERE) | N | opencode, kimi, codex, claude-code… | Arif (F13, replaceable) |

9 × 4 × 5 × N = tensor, not tree. Each cognitive function occupies exactly one lane + one role + can swap harnesses when needed.

### ART-ACT-AUTH = Gates, Not Agents

- **ART** (Autonomous Reflex Trigger) — pre-execution hook, blocks destructive patterns
- **ACT** (Action Capability Token, formerly SCT) — `act_v1.*` capability envelope
- **AUTH** (Authentication) — `did:web:arif-fazil.com` + Ed25519 + bearer

These apply to ALL 9 agents. They are cross-cutting gates — not agent #10, #11, #12.

### arifOS · AAA · A-FORGE = Organs, Not Agents

- **arifOS** (:8088) — kernel substrate, hosts constitutional functions
- **AAA** (:3001) — control plane, hosts registry and routing
- **A-FORGE** (:7071) — execution shell, hosts mutation functions

Organs are the substrate that agents run ON. Every cognitive function resides in one organ as its runtime substrate.

---

*DITEMPA BUKAN DIBERI — Reality first. Judgment second. Architecture forged 2026-08-08.*

---

## KRT Test Protocol (forged 2026-08-15, from KRT-JOHOR-2026-08-15)

Two agents ran the same kernel reality test concurrently and collided: double kernel
restarts mid-measurement, artifacts split across two paths. Rules to prevent recurrence:

1. **One report path:** KRT artifacts go to `/root/AAA/reports/krt-<case>-<date>/`.
   Never `/tmp` — /tmp does not survive and cannot be audited.
2. **One measurer:** before a kernel-touching test, check for a live peer
   (`journalctl -u arifos.service --since "-30 min"` for foreign actors; kernel log
   shows caller identity). If another agent is mid-ladder: HOLD or join, never race.
3. **Restart discipline:** `systemctl restart arifos.service` during someone's
   measurement invalidates their receipts. Announce in the report dir
   (`RESTART.lock` file with owner + timestamp) before restarting; delete after.
4. **Concurrent contamination is a finding, not noise** — log it in the receipt.
