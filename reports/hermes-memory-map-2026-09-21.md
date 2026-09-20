# HERMES MEMORY — MAP & APEX-ZEN CLASSIFICATION
**Measured:** 2026-09-21 01:25 MYT · host forge (KVM8)
**Trajectory:** assistant-turn classification, not a rewrite.

## 1. WHAT THIS MEMORY IS

Not a diary. A block injected into EVERY turn. Hard caps enforced by the tool.

| file | chars | cap | fill |
|---|---|---|---|
| memories/MEMORY.md | 2,147 | 2,200 | 97% |
| memories/USER.md | 1,372 | 1,375 | 99% |
| **live total** | **3,519** | — | — |

Everything else (session history, VAULT999, Qdrant, carry_forward) is RETRIEVAL, not memory.
Retrieval is unbounded. Memory is scarce by design. A fact belongs here only if it must
shape EVERY turn.

## 2. LIVE MEMORY — CLASSIFICATION (20 entries)

### KEEP — load-bearing, shapes every reply (17)
- MEMORY header: tag schema + human-memory-compartmentalization pointer
- [POLICY] MUTATE · K-02
- [POLICY] HUMAN OUTPUT GATE = bridge-protocol v3
- [POLICY] CONDUCT (no gotcha-replay, heavy→Syed, LIGHT theme)
- [POLICY] TRADING (commodity chart = signal; Syed accounting bg)
- [POLICY] KERNEL SEAL L11/L13 — no agent finishes a seal
- [MAP] ECHO LOOP — still live, observed again 2026-09-21
- [MAP] write_file FOLLOWS SYMLINKS
- [MAP] A-FORGE-MCP :7072 cold/warm
- [MAP] TELEGRAM-SEAL (no seal in TG; carry_forward carries human_state)
- SCAR-001 rules (1)(2)(3)
- USER: BAHASA/pronoun ban · 'init to seal' · geoscience-minda+Syed-recovery · deepest want ·
  intimate/Wisconsin boundary · CROSS-AI AUDIT · non-coder · bapak 4 Mac 2024

### REFACTOR — durable principle, stale instance (2)
- [MAP] TG MIRROR — keep "user= ≠ speaker"; the Amin example (8798431893) is superseded
  (Amin lane removed 2026-09-20; sovereign: "penat aku nak suruh org mesej").
- [MAP] MUSIC-SOMATIC — the finding is real; the detail belongs in a skill, not the
  always-on block. Zero reuse outside that lane.

### WATCH — volatile, will need revision (2)
- [MAP] SYED — half is MAP (recipient-never-subject, domain). Half is a living human plan
  (nasi lemak sidekick). Plans change; MAP does not.
- USER "Kerja: exec geoscience PETRONAS Carigali" — thinnest entry, and the most likely to move.

### LAW DECLARED, NOT APPLIED (defect)
Header states: "Durable claims carry state(VERIFIED|REPORTED|UNKNOWN|SUPERSEDED)+evidence_ref+observed_at".
Measured: 3 of 20 entries carry a state tag; 2 carry observed_at/evidence_ref.
Same family as kernel `L02: 0.960 >= 0.99` and `deployed=UNKNOWN` printed as OK:
a rule is written at the top of the file and not enforced on the body.

## 3. THE PENDING QUEUE (123 records) — WHAT IT ACTUALLY IS

Window: 2026-09-18 00:28 → 2026-09-21 01:21 (3.0 days)
Records: 123 · Operations: 323 {'remove': 17, 'add': 63, 'replace': 243}
Distinct anchors: 147 · anchors re-queued >1x: 57
Proposed new text volume: 63,453 chars

**It is 18.1x the size of the entire live memory.** Live total 3,519 chars; MEMORY.md cap 2,200.
The queue is STRUCTURALLY INADMISSIBLE — it can never be applied as a batch. Nothing expires;
oldest record is 3.0 days old. It accumulates.

### Why it must not be approved

1. **It proposes wrong facts as correct.** e.g. USER.md "Kerja: exec geoscience PETRONAS
   Carigali" → "writes code & deploys directly (not just directive-giver)". That contradicts
   the standing non-coder rule. Approved, every future session inherits it.

2. **It oscillates.** Anchor `[POLICY] TRADING…` has SEVEN competing versions in 3 days.
   `[MAP] CHRON :18102` has 6. `[MAP] ECHO LOOP` has 6. This is not learning; it is the same
   sentence rewritten repeatedly.

3. **It cross-contaminates.** An MSS separation-package payload (RM418k, tax detail) was
   attached under the TRADING anchor at 2026-09-20 03:07. Wrong content, wrong anchor.

4. **It is stale before approval.** Queue claims "CHRON CALIBRATION BROKEN: 0 verified,
   accuracy 0.0 (n=4)". Measured 2026-09-21: verified=2, accuracy=0.5, predictions=20.
   Approving it would write a retracted state into always-on memory.

5. **STORY-class content in bulk.** 47 Syed references, financial details, health, family.
   Per the compartmentalization doctrine this repo already seals: STORY stays with the human;
   agents hold MAP only.

### Root cause
`write_approval: false` — the gate HOLDS correctly. But no queue depth limit, no expiry, no
supersession. A correct gate in front of an unbounded accumulator still produces an
unusable queue. The gate is not the defect; the missing TTL is.

## 4. VERDICT

Live memory: **healthy and tight** — 17/20 keep. Not the problem.
Pending queue: **dead accumulation** — 0/123 should be applied as written.
The defect is not memory content. It is that background-review proposals have no expiry and
no supersession, so 3 days of them pile up as 18x inadmissible text with no terminal state.

## 5. NEXT MACHINE ACTION (reversible)
- Quarantine the 123 records (move, not delete) with a manifest. Original path documented.
- Do NOT apply any record. Do NOT rewrite live memory in the same motion.
- Add TTL + supersession to the propose path (lane owner: memory subsystem).

Receipt: this file. `trace_id=trc-memory-map-20260921`
