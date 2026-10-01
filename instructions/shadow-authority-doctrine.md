# Shadow Authority Doctrine — Transformation Path > Everything Else

> Forged: 2026-09-29 | Source: HERMES Authority X-Ray + Message Path Collapse audit
> Classification: Canonical Instruction (F13_RATIFIED 2026-09-29) | Constitutional binding: F1 (AMANAH), F2 (TRUTH), F11 (AUDITABILITY), F13 (HUMAN_SOVEREIGNTY)
> Status: F13_RATIFIED_CHAT (2026-09-29) by Arif F13 sovereign. Captures lessons from 2026-09-29 hermes shadow-audit.

## Axiom 0: The Real Unit of Analysis Is the Transformation Path

```
User message
   ↓
[ T1: identity resolve ]
[ T2: lane routing ]
[ T3: context governor ]
[ T4: people register ]
[ T5: care governor ]
[ T6: recent history ]
[ T7: capability map ]
[ T8: pre-LLM mode emit ]
[ T9: prompt assembly ]
[ T10: LLM call ]
[ T11: post-LLM mode-shape ]
[ T12: pre-tool gate 1 — mode_first_gate ]
[ T13: pre-tool gate 2 — lane_switch scoped ]
[ T14: pre-tool gate 3 — arifos-hermes-gate-hook (JITU) ]
[ T15: tool execute ]
   ↓
Response
```

Model is **one node** among 15. Behavior emerges from the **graph**, not the prompt.

**Metric:** `transition_count(message → capability)`. Lower is better. Audit this number, not file count.

---

## Axiom 1: Shadow Authority > Wrong Authority

Wrong authority is visible (`BLOCKED` shows up). Shadow authority is invisible:
- File exists, registered in intent
- Comment sounds authoritative
- Function defined, returns verdict
- But: never loaded, never called, zero runtime effect

Example: `mode_first_enforcement.py` (6.3 KB, no HOOK.yaml, never loaded by gateway hook loader per `/usr/local/lib/hermes-agent/gateway/hooks.py:43-72`). A reader of the file would assume mode-first is enforced. **It is not.**

**Detection rule:** Shadow authority exists wherever file/code surface ≠ runtime behavior. Map every claim of authority to its load path. If the load path is missing, it's theatre.

---

## Axiom 2: Capability Graph ≠ Reasoning Graph

Two systems can have identical capability surfaces (same 27 tools available) and produce different reasoning outcomes because the **transformation path differs**.

- DM session vs Group session: same tools, different lane card injected
- Arif lane vs Syed lane: same tool set, different PEOPLE REGISTER, different CAPABILITY MAP

**Test:** `tool X available? ✅` proves nothing. Test instead: `what reaches the model when tool X is requested?`

---

## Axiom 3: Size ≠ Authority

The 61 KB SOUL.md, the 26 KB lanes.yaml, the 13 KB context-governor.md — all loud files. The actual authority lived in:
- `lane_switch/__init__.py` (940 lines, runtime transformer)
- `mode_first_gate/__init__.py` (389 lines, runtime gate)
- `arifos-hermes-gate-hook.py` (32 KB, JITU sovereign stop)

**Scar line (BM):** `Fail yang paling kuat bercakap, jarang fail yang paling kuat berkuasa.`

---

## Axiom 4: Identity Coherence vs Reality Coherence

Most agents optimize for identity coherence first: "Am I still myself?" before "Do I understand what's happening?". This produces consistent-sounding-but-misaligned behavior.

Optimize for reality coherence: what is actually true, what is the user actually asking, what does the evidence actually show.

---

## Axiom 5: The Biggest Bottleneck Is Not Intelligence

When an agent seems "bangang", the cause is rarely the model. It's almost always **the transformation chain between human and model**:
- Too many transitions
- Each transition adds latency, distortion, shadow authority
- Reasoning happens AFTER all the framing

Audit **middleware / routing / gating / transformation chains** before assuming the model is the problem.

---

## Axiom 6: Count Transitions, Not Components

```
File count → entropy
Transition count → authority
```

Formula for any agent audit:

```
human → T1 → T2 → T3 → ... → Tn → capability
```

Each `T_i` is a potential veto point, distortion, or shadow authority. Lower `n` is better. Each `T_i` must answer: "How does this improve reality mapping?" If no answer: remove or demote to per-call opt-in.

---

## Axiom 7: The First Mutation Is Rarely the Right Mutation

Audit progression for the 2026-09-29 session:

| Hypothesis | Verdict |
|---|---|
| 1. Delete SOUL.md | Wrong — L4 prompt influence, not authority |
| 2. Delete persona files | Insufficient — symptom, not cause |
| 3. Reduce entropy (delete .bak files) | Partial — cleanup, not governance fix |
| 4. Audit runtime authority | Closer — finds mode_first_gate plugin as real gate |
| 5. Audit message transformation path | **Smoking gun** — finds lane_switch injecting 3-5 KB pre-reasoning |

**Pattern:** Each hypothesis gets closer to the transformation path. The right target is rarely the first thing you see.

---

## Axiom 8: SCAR — The Map That Explains Behavior ≠ The Code That Executes Behavior

Documentation says X. Code says Y. Runtime says Z. **Trust the runtime trace, not the map.**

For every authority claim, prove it with code execution path:
1. File path
2. Load path (who imports it, who calls it)
3. Trigger event (what invokes it)
4. Effect path (what it does to message/tool/output)
5. Failure mode (what if it's missing/broken)

If any step is missing, the claim is shadow authority.

---

## Axiom 9: SESSION_GOVERNED Authority Surfaces

For each authority surface, classify into:

| Level | Class | Action |
|---|---|---|
| L0 | Dead artifact | Archive |
| L1 | Style only | Remove from prompt |
| L2 | Prompt influence | Keep, audit per-claim value |
| L3 | Memory influence | Keep, verify scope (dm vs shared) |
| L4 | Reasoning influence | Keep, compress to minimum viable |
| L5 | Capability veto (detect-only) | Keep audit trail, demote if no observed abuse |
| L6 | Execution veto (fail-closed) | Keep, sovereign-ratified only |

**Rule:** No surface may operate above its observed level. Shadow authority lives where L6 claim lacks L6 evidence.

---

## The Compression

> **Behavior is governed less by what the model knows and more by what reaches the model before it thinks.**

Or in arifOS form:

```
Reality > Prompt.
Prompt > Model.
Model > Output.

BUT

Transformation Path > semuanya.
```

---

## Operational Test (apply to any agent audit)

For each candidate mutation:

1. Does this reduce `transition_count`? — If yes, prefer. If no, demote.
2. Does this reduce `prompt_bytes_added_per_turn`? — If yes, prefer. If no, demote.
3. Does this preserve `capability_availability`? — If yes, safe. If no, escalate F13.
4. Does this preserve `reality_mapping_quality`? — If yes, safe. If no, escalate F13.
5. Is the rollback path <= 1 minute? — If yes, auto-execute. If no, ask.

---

## Ratification Path

DRAFT_AWAITING_F13. To ratify:
1. F13 sovereign review
2. AA/AAA musyawarah (333 ARCHITECT + 555 AUDITOR + 666 JUDGE minimum)
3. F11 receipt chain (audit log + signed digest)
4. Promotion to F13_RATIFIED in /root/AAA/AGENTS.md instruction table

---

## Provenance

- Audit session: 2026-09-29, hermes shadow-audit (Kimi Code FI-008 + HERMES musyawarah)
- Files inspected (read-only): 940 lines lane_switch plugin, 389 lines mode_first_gate plugin, 232 lines mode_first_enforcement.py (ghost), 374 lines reality-claim-gate, 32 KB arifos-hermes-gate-hook.py, 61 KB SOUL.md, 26 KB lanes.yaml, 13 KB context-governor.md, 15 KB config.yaml, 1.2 KB IDENTITY_LOCK.json, plus hooks/ directory and hermes_mcp/ package
- Files MUTATED in this audit (Phase A): zero (observation only)
- Phase B mutations (pending F13 per-action GO): lane_switch refactor + mode_first_gate demote + L0 artifact purge — each with diff preview, snapshot, rollback path