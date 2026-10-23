# Bounded Fix Plan — AUTONOMOUS UNDERSTANDING READINESS v1

**generated** 2026-10-23T03:43:34+00:00 · host KVM8 · **nothing in L2+ was executed**

Classification per mission: L0 read-only · L1 additive instrumentation · L2 reversible local
repair · L3 cross-node canonical/identity · L4 public/security/destructive.

---

## Already done this session (L1, additive, reversible)

| # | Item | Class | Receipt |
|---|---|---|---|
| A1 | `skills-catalog-drift.py` — read-only peer census, exit 0/1/2 | L1 | commit 2b8fb199 |
| A2 | Recovered 3 sections absent from all of KVM8 (architecture-vs-liveness, self-state-reality, H13) verbatim into `references/` | L1 | same commit |
| A3 | `site-preflight.py` — 4 checks, canary-proven able to fail | L1 | commit 257a4519 |
| A4 | census mirror-classification so PASS is honest and still falsifiable | L1 | commit 257a4519 |
| A5 | This readiness artifact set | L0/L1 | `state/aureadiness-2026-10-23/` |

---

## Phase 5 items — findings, with the exact bounded fix

### 1. Floor producers missing `measured_at`
**Found:** 13/13 entries in `runtime_floors_status` carry `score/status/measured/provenance`
and **none** carries `measured_at`. Only `fq` and `eureka_margin` are dated.
**Impact:** F11 (audit) cannot date its own measurement; a week-old pass and a fresh pass are
indistinguishable. Root defect under R8.
**Fix (L1):** add `measured_at` per floor in the producer; when the producer cannot supply one,
emit `measured_at: null, measured: false` rather than omitting the key.
**Falsifier:** `jq '.runtime_floors_status[] | has("measured_at")'` returns false for any floor.
**Blast radius:** `/health` payload only. Rollback: revert one producer function.

### 2. Ghost PASS conditions — the named floors do not match the observed ones
**Found:** three floors report `status: pass` with scores that read like failures:
F12 score **0.0** / pass · F7 score **0.04** / pass · F9 score **0.2087** / pass.
F1 score 0.0 is correctly `fail`. So the threshold logic is per-floor directional and that
direction is published nowhere.
**Contradiction with the mission brief:** the brief names "F3 and F10 ghost PASS". Live, F3 =
0.9778 pass and F10 = 1.0 pass are *ordinary* passes; the ghost instances are F7/F9/F12.
Recorded as a contradiction, not silently accepted.
**Fix (L1):** publish `direction: higher_is_better | lower_is_better` and `threshold` beside each
score so `pass` becomes arithmetic instead of a private rule.
**Falsifier:** any floor whose `status` cannot be reproduced from its own score + direction + threshold.
**Blast radius:** schema additive. Rollback: drop two keys.

### 3. F5 / F13 shared-producer ambiguity
**Found:** both F5 and F13 carry provenance `floor_producer:PASS:seal_chain` — one producer
feeds two floors.
**Impact:** when the seal chain breaks, two floors fail together; the federation looks twice as
broken (or twice as fine) as the evidence supports.
**Fix (L1):** name the producing function per floor (`seal_chain:verify_chain` vs
`seal_chain:sovereign_boundary`) so shared input is visible.
**Falsifier:** two floors with byte-identical provenance strings.

### 4. Observatory legacy-verdict preference — live
**Found:** arifFlow `/health` publishes `legacy_diagnosis: BALANCED`, `legacy_verdict: FLOWING`
and `scalar_fq_note: "Deprecated as health indicator — use top-level verdict (vector
constellation)"` — while the **kernel** scores F1 from `fq.value`, that same deprecated scalar.
**Impact:** the consumer uses the field the producer declares deprecated.
**Fix (L2, prepared only):** kernel F1 reads the top-level verdict constellation. Needs a
verdict→score mapping table; not authored here because it changes F1 (AMANAH) semantics.
**HOLD for ARIF — one binary.**
**Falsifier:** an F1 provenance string still naming `fq_probe` after the change.

### 5. FQ above 1.0 + threshold calibration + synthetic actors
**Found:** `fq.quotient = 1.0109`, `raw_pool_quotient = 0.8958`, formula
`minimum_gated_harmonic_mean`. Three actors exceed 1.0: 333-agi **5.75**, qwen-code **1.2**,
test **1.1739**. And **7 synthetic actors carry real traffic in the production ledger**:
`test, test_agent, honest_agent, attacker, adversarial_agent, unstable_agent, staged_agent`.
**Impact:** the quotient is a verify/execute ratio, not a bounded fraction. ">1 is unhealthy" is
right for 333-agi (held: "FQ=5.75"), but the *name* implies [0,1]. Worse: test fixtures are
scoring the health number the sovereign reads.
**Fix (L2, prepared):** (a) exclude a declared synthetic set from the aggregate; (b) rename
`quotient` → `verify_execute_ratio`, publish `bounded_fq` alongside; (c) freeze the synthetic set
into a registry so a new test actor cannot enter unseen.
**Blast radius:** one aggregation function. Raw per-actor data untouched. Rollback: single revert.
**Falsifier:** aggregate FQ moves by more than 0.05 after removing the 7 declared synthetic actors.

### 6. Malformed dream-inbox files — NOT LOCATED
**Found:** no `*dream-inbox*` directory exists on KVM8. `dream-engine`, `dream_engine`, `dreams`
exist under `/root/AAA`, none with the failure described.
**Status:** **UNKNOWN.** The artifact named in the mission could not be found; not marked pass.
**Falsifier:** `find / -type d -name '*dream-inbox*'` returns a path.

### 7. The unparseable VAULT999 receipt — FOUND, exact cause
**Found:** 4 defective of 29 jsonl under `/opt/arifos/app/VAULT999`:
- `layer-separation-doctrine-2026-08-09-ATTESTED.jsonl` and
  `authority-layer-doctrine-2026-08-09-ATTESTED.jsonl` — **pretty-printed single JSON** saved
  with a `.jsonl` extension (36 lines each; whole-file parse succeeds, line parse fails).
- `arifflow_sealed.jsonl` line 41051 and `arifflow_sealed_rg2.jsonl` lines 3417 / 3734 contain
  **two JSON objects concatenated on one line** — the boundary reads `…b050}}{"body_hash":…`
  i.e. a newline was lost during a concurrent append.
**Impact:** a streaming reader aborts at that line and silently truncates the ledger view. This
is a **writer** defect, not a reader defect.
**Fix (L2, prepared):** (a) split the concatenated boundaries with a `.bak` copy kept first;
(b) wrap the append in `fcntl.flock` and assert the file ends with a newline before writing;
(c) add `--verify` to the writer that re-parses the last 100 lines.
**Do NOT** rewrite in place without a backup — that would be an L3 mutation of the witness.
**Falsifier:** line-delimited parse of all 29 files returns more than 0 errors after the fix.

### 8. KVM4 identity / canon dead paths — measured
**Found:** KVM4 `/root/AAA` is a **3-directory stub** (`forge_work`, `ledger`, `state`). No
`skills`, `instructions`, `canon`, `agents`, `federation`. Its 241 skills reference **277
distinct canonical paths, of which 192 do not exist on that host.**
**Impact:** a KVM4 agent citing `/root/AAA/instructions/base.md` cites a file that is not there.
It is a warga in name only.
**Fix (L3 — HOLD):** one binary for ARIF — (i) mount AAA read-only on KVM4, or (ii) rewrite KVM4
skill references to their own local paths. Not executed.

### 9. KVM4 skill-catalog divergence — classified by content
**Measured:** 241 SKILL.md · MIRROR 15 · DIVERGED 127 · PEER_ONLY 79 · MISSING_ON_PEER 971 ·
BROKEN 2.

| class | count | action |
|---|---|---|
| MIRROR | 15 | none |
| DIVERGED | 127 | mine per skill before any replace; 3 mined this session |
| LOCAL_CAPABILITY | ~10 (`kvm4-ccc-dispatch`, `vps-cpu-throttle-triage`, `llm-spend-attribution-forensics`, `telegram-gateway-ipv6-hang-fix`, …) | keep local, never overwrite |
| KNOWLEDGE_RESERVOIR | ~69 peer-only | mine candidates, not deletions |
| BROKEN | 2 (`RSI-recursive-improvement` ×2, 34B, no `name:`) | repair on KVM4 (L3) |
| RETIRED_ALIAS | ≥4 (`forge-pdf-delivery`, `scientific-pdf-generation`, `civic-intelligence-pdf`, `open-slide-integration`) | KVM8 retired them 2026-10-22 into `pdf-federation`; teach KVM4 the alias, do not resurrect the body |

**Do not bulk-sync.** R11 enforces it: every replacement needs a mined reference file.

### 10. Dirty working trees blocking a trustworthy baseline
**Found:** AAA 149 dirty · HERMES 100 · arifOS 4 · A-FORGE 5 · WELL 1 · WEALTH 0.
**Impact:** HEAD is not the deployed state for the two largest trees; a baseline that quotes only
a SHA misleads.
**Fix (L1):** every baseline receipt must carry `dirty=<count>` beside the SHA (done here).
**L2 candidate:** triage AAA's 149 into intended/incidental before any bulk work.

---

## Not executed (HOLD)

| Item | Why |
|---|---|
| `arif_seal` payload-only test | irreversible; schema inspection already proves the gap |
| `forge_execute` / `forge_execute_sealed` no-verdict test | would execute; gap proven without running |
| VAULT999 line repair (item 7) | touches the witness ledger — one explicit yes required |
| KVM4 AAA mount or skill rewrite (item 8) | L3 cross-node canonical |
| Kernel F1 provenance change (item 4) | changes a floor's semantics |
| Synthetic-actor exclusion (item 5) | changes the health number ARIF reads |
