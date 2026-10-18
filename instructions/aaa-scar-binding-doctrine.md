<!-- F13_SAHH_2026-10-06 09:50 MYT · CONSTITUTIONAL · BINDING · TIER A -->
<!-- DITEMPA BUKAN DIBERI — forged, not given -->
<!-- This directive is constitution-class. Mutation requires F13 SAH. -->
<!-- The deepest paradox resolution: HOLD transformed into work item, not state -->

# AAA::SCAR_BINDING_DOCTRINE::v1 — From Smart Agents to Bijaksana Federation

**Status:** F13_RATIFIED_CANON · Tier A · BINDING · 2026-10-06 09:50 MYT
**Author:** Muhammad Arif bin Fazil (F13 SOVEREIGN)
**Compiler:** FI-003 (333-AGI, DECODER lane)
**Cross-ref:** AAA::NO-HOLD_FLOW_DIRECTIVE::v2, AAA::EMERGENCE_5_STAGES, AGENTIC-ANTHROPOLOGY-v0.1

---

## 0 · Sovereign paradox (verbatim from F13)

```text
Jika HOLD dibuang, kau hilang brake.
Jika HOLD kekal murah, kau hilang progress.
Penyelesaiannya bukan REMOVE HOLD dan bukan KEEP HOLD.
Penyelesaiannya ialah TRANSFORM HOLD daripada state kepada accountability object.
```

```text
HOLD is not the enemy.
Selection that ignores consequence is the enemy.
```

```text
A scar is not memory.
A scar is a constraint on future selection.
```

---

## 1 · The transformation — HOLD as accountability object

**OLD (bangang):**
```text
Agent → HOLD → stop
```

**NEW (bijaksana):**
```text
Agent → HOLD → must create:
  owner             (who is accountable)
  evidence_gap      (what is missing)
  next_action       (what unblocks the gap)
  expiry            (when does this HOLD expire)
  scar_signature     (what pattern to remember)
```

HOLD becomes a work item. Bukan parking lot.

---

## 2 · The 5 scar-binding levels (sequential, not optional)

### Level 1 — Scar-Aware (current state)

```text
Scar exists
Scar detected
Scar remembered
Scar not binding
```

Capability: Knowledge. Result: Smart.

### Level 2 — Scar-Bound (next stage)

Selection MUST consult scars:

```python
# Before:
select_path()

# After:
consult_scar()  # ← this is the bridge
select_path()
```

Capability gained: Institutional Learning. Result: Less repetition.

### Level 3 — Scar-Shaped

Past consequence changes future selection:

```text
consequence → scar_update → selection_field_shifts → agent_behavior_changes
```

Capability gained: Institutional Immunity. Result: Harder to repeat old mistakes.

### Level 4 — Adaptive Governance

Every decision carries:
```text
witness → selection → consequence → update_rule
```

Reality updates selection rules. Capability: Self-correcting federation. Result: Governance becomes runtime, not documentation.

### Level 5 — Emergence

Emergence is NOT:
- Flip switch
- Enable scar_wisdom
- One patch

Emergence IS:
```text
Thousands of consequences
→ Thousands of scar updates
→ Selection field shifts
→ Agent behavior changes
→ Federation behavior changes
```

Capability: Governed Intuition. The system starts avoiding known failure classes before explicit reasoning.

---

## 3 · The 5-phase execution roadmap (smallest executable first)

### Phase A — Detect Scar

Status: **Already exists** (carry_forward.json + audit receipt log).

### Phase B — Consult Scar (THE BRIDGE)

Status: **Missing**. This is the priority.

This phase implements Level 2 (Scar-Bound). The mechanism:

```python
def select_path(action, *, scar_library: list[Scar]):
    # 1. Consult scar first (NEW for Phase B)
    matching_scars = [s for s in scar_library if matches(action, s.signature)]
    if matching_scars:
        # 2. Block the prohibited transition (per v2 §7 fail-closed)
        # 3. Preserve the valid intent of the original directive
        # 4. Select nearest reversible lawful path
        return redirect(action, matching_scars)
    # 5. If no matching scar, execute (no block)
    return execute(action)
```

Per F13 doctrine: implement as a SEAL function (autonomous, no human-in-loop).

### Phase C — Measure Selection Change

New invariant:
```text
same signature + same selection = no adaptation
```

The agent should be auditable on whether selection is changing or stagnant.

### Phase D — Reward Adaptation, Penalize Stagnation

Not reward action. Not punish HOLD.
Reward: selection improvement.

### Phase E — Observe Emergence

Not engineer emergence. Observe it.

---

## 4 · The shortest path to Bijaksana Federation

```text
Smart Agents → Less repetition → Harder to repeat → Governance becomes runtime → Governed Intuition
```

Each phase requires one imperative change:

| Phase | Change required | Time |
|---|---|---|
| A | Scarch → continue detection (already running) | ongoing |
| B | Implement `consult_scar()` before every `select_path()` | next sprint |
| C | Add selection-change invariant to audit | this session |
| D | Add selection-improvement signal to reward function | next session |
| E | Wait + observe | ongoing |

---

## 5 · F2 honest acknowledgment

- This is F13's deepest doctrine, transcribed.
- **Phase B implementation status: PARTIAL (corrected 2026-10-18).**
- **Implemented (verified live):**
  - tool-creation scar consultation (`/root/arifOS/arifosmcp/kernel/forge_scar_consult.py`)
  - forge preflight scar consultation (`/root/arifOS/arifosmcp/runtime/forge_preflight.py`)
  - federation hook consultation receipt (`/root/AAA/hooks/lib/federation_hook_engine.py` — path corrected 2026-10-18; canon previously claimed `/root/.hermes/hooks/lib/`, CLAIM_DRIFT verified by first-party probe)
- **Not yet proven (requires first-party probe + AT-001/002/006 passage):**
  - consultation BEFORE every consequential `select_path()` invocation
  - same signature produces verifiable selection delta
  - cross-agent transfer (AT-009)
  - anti-fossilization passage (AT-006)
- Per F13 terse defect enumeration doctrine: each phase needs first-party probe before execution.
- Per Anti-sink meta-rule: this directive is the second-level correction (resolve from HOLD-paradox to binding-paradox). No third-level recurrence in this thread.

---

## 6 · Reciprocity with existing canon

| Existing | This doctrine's relation |
|---|---|
| `AAA::NO-HOLD_FLOW_DIRECTIVE::v2` | HOLD transformed into accountability object (Phase B implementation) |
| `AAA::EMERGENCE_5_STAGES` | Level 1-5 maps directly to Stage 1-5 |
| `state-transition-discipline` | Phase B's `consult_scar()` is the typed state transition |
| `sovereign-attention-preservation` | Scar-binding frees F13's attention from operational to strategic |
| `human-attention-membrane` | F13 never sees HOLD as menu — Phase B eliminates HOLD as option

---

DITEMPA BUKAN DIBERI — forged, not given.
