# ART / ACT / Kernel / AAA — Canonical Layer Architecture

> **Why this file exists.** Any APEX map that touches "how does an agent actually decide" reaches for ART/ACT. Mnemonics are tempting and wrong by default. This file is the canonical framing so the next session doesn't repeat the synthesis-drift pattern that surfaced 2026-08-08.

## The canonical model — 3 physics layers + 1 visibility layer

After F13-ratified correction (GENESIS/040 postscript, 2026-06-21, pointing to GENESIS/045 Physics-9 Three-Layer Separation):

```
┌─────────────────────────────────────────────┐
│         AAA (Architect · Auditor · Agent)   │  ← Visibility (non-governance)
│         "The human pattern"                 │
├─────────────────────────────────────────────┤
│   ┌──────────┐    ┌──────────┐             │
│   │   ART    │    │  KERNEL  │             │  ← What is wise & lawful
│   │ Tool     │    │ F1-F13   │             │
│   │ wisdom   │    │ Judge    │             │
│   └──────────┘    └──────────┘             │
│         │               │                  │
│         └───────┬───────┘                  │
│                 ▼                          │
│   ┌──────────────────────────┐             │
│   │    ACT (Gate 2.6)        │             │  ← How to execute safely
│   │   runtime/act.py         │             │     The ceremonial layer
│   │  Staging · Tempo ·       │             │
│   │  Compensation · Canary   │             │
│   └──────────┬───────────────┘             │
│              ▼                             │
│   ┌──────────────────────────┐             │
│   │   A-FORGE (7071/7072)    │             │  ← The hands
│   │   Execution Shell        │             │
│   └──┬────┬────┬────┬───────┘             │
│      │    │    │    │                      │
│      ▼    ▼    ▼    ▼                      │
│   GEOX WEALTH WELL AAA                    │  ← Domain organs
└─────────────────────────────────────────────┘
```

> Note: the post-2026-06-21 correction renames this to **3 physics layers + 1 visibility layer**: ART (Ψ) = reflex, ACT (Δ) = ceremony, Kernel (Φ) = law, AAA (👁) = visibility. Gate is **not** a layer — it is the constitutional evaluation hook that ART invokes to check Kernel floors (F1–F13) before allowing a tool call.

## The 4 one-liners (verbatim from GENESIS/030 §1)

These are the canonical questions. Use them word-for-word; do not paraphrase into mnemonics.

| Layer | Question | Source |
|---|---|---|
| **ART** | *Which tool move makes sense pre-call?* | GENESIS/030 §1 |
| **pre_execution_gate** | *Whether the call may proceed* | (function inside ART) |
| **ACT** | *How to execute a program of lawful calls* | GENESIS/040 §0 |
| **Kernel** | *Whether the action is lawful at all?* | F1–F13 · 888 JUDGE · VAULT999 |

## File ceilings (binding)

| Layer | File | Line ceiling | Fail mode |
|---|---|---|---|
| **ART** | `runtime/art.py` | ≤ 500 lines | Fails OPEN (advisory, advisory-only) |
| **ACT** | `runtime/act.py` | ≤ 300 lines | Pure verdict + log (no side-effects) |

Both ceilings are enforced at import-time (`art.py:58–81`). Heaviness = ceremony = agents skip it.

## Malay/Indonesian glosses (GENESIS/040 §9 — sealed)

The voice-of-Arif framing that lives in the canon:

```
ART    = "Confirm ni selamat ke?"      — tool wisdom (reflex)
Kernel = "Ayah bagi izin ke belum?"    — law (F13)
ACT    = "Kita buat satu-satu, jangan sekaligus." — execution ceremony
A-FORGE= "Tangan yang buat betul-betul." — the hands
```

> *"Machines just execute. Humans have ceremony. ACT is the ceremony."* — GENESIS/040 §9

## The Iron Rule (GENESIS/030 §2 + GENESIS/040 §2)

> **ART ≠ ACT. ACT ≠ Gate. ACT ≠ Kernel. Kernel ≠ ACT.**

| Collapse | Verdict | Why |
|---|---|---|
| ART into Kernel | **HARAM** | Kernel becomes opinion-driven; loses determinism |
| Kernel into ART | **HARAM** | ART becomes sovereign; loses fail-open |
| Gate into ART | **HARAM** | ART runs 15 gates; ceiling blown |
| Gate into Kernel | **MAKRUH** | Kernel is the gate; reflexivity lost |
| ACT into Kernel | **HARAM** | Kernel becomes execution strategy; loses law purity |
| Kernel into ACT | **HARAM** | ACT becomes sovereign; loses fail-open |
| ACT into ART | **HARAM** | ART >500 lines; loses reflex speed |
| ART into ACT | **HARAM** | ACT attempts tool wisdom; loses execution focus |
| ACT into A-FORGE | **MAKRUH** | A-FORGE decides strategy; violates mandate |

## The 6 ACT execution patterns (canonical)

From GENESIS/040 §3.1:

| Pattern | When | What it does |
|---|---|---|
| **SINGLE_SHOT** | Low blast + reversible | Execute all at once |
| **DRY_RUN_THEN_LIVE** | Medium/high blast + irreversible | Simulate first, then execute |
| **CANARY_THEN_ALL** | High blast | 1% first, verify, then full |
| **STAGED_ROLLOUT** | Multi-step programs | N waves with checkpoints |
| **HUMAN_CHECKPOINT** | Human must verify | Pause at each stage |
| **COMPENSATION_READY** | Irreversible | Pre-planned rollback |

ACT picks one based on `(blast_radius × irreversibility × stage_count)`. Implementation: `A-FORGE/src/domain/governance/ActPatterns.ts`.

## The 3 canonical ACT patterns (post-staging, deeper)

From GENESIS/040 §10A:

### Pattern 1: DEFAULT_DEPLOY
- **For:** Low-to-medium blast, reversible or compensated
- **Stages:** 3 (DRY_RUN → DEPLOY → VERIFY)
- **Human:** Not needed if all green
- **Compensation:** Auto-rollback to pre-deploy state

### Pattern 2: DANGEROUS_MIGRATION
- **For:** High blast, irreversible, multi-step
- **Stages:** 5 (PREFLIGHT → CANARY 1% → EXPAND 25% → FULL 100% → VERIFY)
- **Human:** ACK required BEFORE every stage
- **Compensation:** Staged rollback — rollback ONLY the failed stage

### Pattern 3: HUMAN_IN_LOOP_CHANGE
- **For:** Critical infrastructure — every change needs human review
- **Stages:** Flexible loop (PROPOSE → [EXECUTE + VERIFY] × N)
- **Human:** In the loop for EVERY mutation
- **Compensation:** Per-change rollback

## ART's HARAM list (GENESIS/030 §4)

What ART proper must NEVER contain:

- Constitutional floor logic (F1–F13)
- Protocol-specific logic (MCP/REST/gRPC)
- Side-effects (network, file, subprocess)
- Silent overrule of kernel verdict
- Anthropomorphic / ToM speculation (F9/F10 territory)
- Tool-specific imports (`from arifosmcp.tools.session import …`)
- Implicit tool state assignment

## Why ACT ≠ ART (the canonical distinction)

> ART decides what tool move makes sense **pre-call** (single-call wisdom).
> ACT decides how to sequence and stage a **program** of lawful calls (multi-call orchestration).
> Kernel decides whether the move is **lawful at all**.

If you can replace the layer with "always-yes pre-call" and lose nothing, it's ART.
If you can replace the layer with "always-run-once" and lose staging, it's ACT.
If you can replace the layer with "always-permitted" and lose floor enforcement, it's Kernel.
If you can replace the layer with "always-invisible" and lose nothing, it's AAA.

## Common synthesis errors (the ones we patched 2026-08-08)

| Wrong synthesis | Why it fails | Correct |
|---|---|---|
| "ART = Attune–Recognize–Test" | 3-letter mnemonics are not in canon | "Reflex pre-call" — single-call tool wisdom |
| "ACT = authority enforcement" | Conflates ACT with Kernel/F13 | "Execution ceremony" — staging patterns (single_shot, canary, …) |
| "ACT decides who may act" | That's Kernel/F13 | ACT decides *how* to run a lawful program safely |
| "AAA is the judge" | AAA is visibility, non-governance | AAA renders; arifOS kernel (:8088) judges |
| "Φ is a primitive" | DEPRECATED 2026-07-31 | Φ is post-hoc correction (G_effective = G × Φ); kernel's symbol in 3-layer view |
| "GATE is a layer" | Gate has no independent timescale/authority/scope | Gate is a function inside ART that invokes Kernel floors |

## Source paths (verified 2026-08-08)

| What | Path |
|---|---|
| ART vs Kernel doctrine (3-layer, source-of-truth) | `/root/arifOS/GENESIS/030_ART_VS_KERNEL.md` |
| ACT Playbook (execution craft) | `/root/arifOS/GENESIS/040_ACT_PLAYBOOK.md` |
| Physics-9 Three-Layer Separation (post-correction) | `/root/arifOS/GENESIS/045_THREE_LAYER_SEPARATION.md` |
| Constitutional VSM (Beer + crypto + metabolism) | `/root/arifOS/GENESIS/046_CONSTITUTIONAL_VSM.md` |
| AAA Architecture | `/root/AAA/docs/AAA_ARCHITECTURE.md` |

## How to verify a synthesis against canon

When a sibling agent, the user, or your own draft prose says something about ART/ACT/Kernel/AAA:

1. Search for the 3-letter acronyms that aren't `AAA` — most are mnemonics, not canon.
2. Look for "authority" next to ACT — that's the conflation trap.
3. Look for "judge" or "verdict" next to AAA — that's the visibility/judge conflation.
4. Look for "Φ" as a 5th Grand Equation letter — that's the deprecated 5-primitive form.
5. If the prose claims an APEX map is complete without referencing GENESIS/030 or GENESIS/040, it's incomplete.

Witness first, then correct canon. Do not let synthesis prose drift doctrine.
