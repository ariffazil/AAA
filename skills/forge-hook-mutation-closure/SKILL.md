---
name: forge-hook-mutation-closure
id: forge-hook-mutation-closure
version: 1.0.0
owner: AAA
autonomy_tier: T2
description: "Use when mutating federation runtime hook infrastructure."
risk_tier: high
floor_scope: [F1, F2, F13]
triggers:
  - "edit hermes-nudges.yaml"
  - "edit hermes-nudge-injector.py"
  - "add or modify a Hermes plugin pre_llm_call hook"
  - "wire a new capability into nudge-injector or probe-first-reflex"
  - "two handlers trigger on the same hook event"
  - "patch doubles up a function the plugin already does"
tags: [forge, federation, hook, plugin, nudge, capability-split, interference-test, transcript-replay]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# FORGE Hook Mutation Closure

The class of work: mutate federation runtime hook infrastructure (nudge engine yaml, engine python, plugin registration in `~/.hermes/profiles/<profile>/plugins/<name>/`) without producing doubled/zero/conflicting handlers. Covers pre_llm_call, post_llm_call, pre_tool_call, post_tool_call, gateway_dispatch hooks.

The session that produced this skill showed the failure mode: two handlers triggering on the same hook event from different mechanisms (YAML engine + plugin Python) both firing on entity-name detection. Doubled nudge injection = token waste + confusing LLM context. Single handler triple of `(hook, event, condition)` is the goal.

## When to use

- Editing `hermes-nudges.yaml` to add/modify/remove a nudge.
- Editing `hermes-nudge-injector.py` to add new condition keys or process_*_llm logic.
- Adding a new Hermes plugin with `pre_llm_call` / `post_llm_call` / `pre_tool_call` hooks.
- Two mechanisms (yaml rule + plugin guard) seem to detect the same trigger.
- Someone reports "agent confession-before-probe" or "double nudge" or "zero nudge where expected".

## Procedure

```
1. INVENTORY HOOKS      → list every handler registered for the hook event you'll touch
2. CAPABILITY MAP       → for each handler, what condition(s) trigger it, what does it emit
3. CHOOSE LANE          → if your trigger already has a handler, you have three options:
                          a) Capability split (recommended): divide trigger space by signal
                          b) Take over: remove the other handler, fully own this trigger
                          c) Skip: the other handler already covers this signal
4. MUTATE               → make the minimum patch needed for your chosen lane
5. UNIT TEST            → run synthetic message lists through both handlers; verify each
                          alone still passes its own tests, AND verify together they don't
                          double-fire on the same input
6. INTERFERENCE REPLAY  → load real transcript messages from state.db for the hook event
                          and replay them through both handlers; count fires per hook
7. RECEIPT              → write state sebenar + path + verified count + "belum habis" jujur
```

### 1. Inventory hooks

```bash
# Find every plugin registered for the profile
ls /root/.hermes/profiles/<profile>/plugins/*/__init__.py

# Find every pre_llm_call / pre_tool_call / post_llm_call function in plugins
grep -rn "def pre_llm_call\|def pre_tool_call\|def post_llm_call" \
  /root/.hermes/profiles/<profile>/plugins/

# Find every nudge in the engine yaml
grep -A1 "^- id:" /root/AAA/federation/protocols/hermes-nudges.yaml
```

For each handler record: (hook_event, condition_keys, what_it_injects, what_it_strips).

### 2. Capability map

A capability = (signal_class, action). Signal classes that commonly collide in this federation:

| Signal class | Engine nudge typical owner | Plugin typical owner |
|---|---|---|
| First turn | `is_first_turn` | none — usually plugin via `_needs_probe_first` |
| Entity-name (person / file / system) | `any_keyword` + entity list | regex pattern + entity list |
| Consequential action (rm, DROP, payment, health) | `regex` blocklist | plugin-specific |
| Mode (CONVERSE / EXPLAIN / INSPECT) | `collapse` post_llm strip | firewall script (presentation_firewall.py) |
| Boundary (forward/paste artifact) | not engine territory | plugin guard |

When two handlers claim the same signal class, **capability split is the default**. Pick which signal the engine owns (typically framework / generic / reloadable) and which the plugin owns (typically specific / stateful / testable). Do not duplicate.

### 3. Choose lane

Reversible rule: **the one with more existing tests wins the signal**. Sealed artifacts (with RECEIPT.md + tests passing) stay sealed unless their lane explicitly overlaps. Engine yaml is framework — easy to reload, easy to delete a rule. Plugin Python is logic — has unit tests, has boundary contract.

Default for federation hook mutations:
- New generic / framework rule → engine YAML (`hermes-nudges.yaml`)
- New specific / stateful logic → plugin
- Trigger already owned by plugin → keep plugin, don't add engine rule
- Trigger already owned by engine → keep engine, don't add plugin guard

### 4. Mutate minimum

- One file at a time. If you're mutating engine yaml AND engine python AND plugin, stop — that's three mutable surfaces and the interference matrix grows fast.
- Re-read the file you're about to patch with offset/limit before patching (patch tool enforces this).
- Preserve every other rule/guard. Don't reorder priority unless you have a test for it.

### 5. Unit test the lane in isolation

Each handler must still pass its own synthetic test cases AFTER your change. The engine has a testable Python entry point — write a quick `python3 -c "..."` snippet that calls `process_pre_llm(...)` with a synthetic message list and asserts which `nudges_applied` are returned.

For a plugin: same pattern, call `plugin.pre_llm_call(user_message=..., conversation_history=..., is_first_turn=...)` and assert the returned context shape.

### 6. Interference replay (mandatory when >1 handler for the hook)

Load real transcript messages from `~/.hermes/state.db` for the hook event being tested. Replay each turn through BOTH handlers. Count fires per handler per turn.

```python
import sqlite3, importlib.util, pathlib, sys

# Load real messages
con = sqlite3.connect('/root/.hermes/state.db')
rows = con.execute("""
  SELECT id, role, substr(content,1,150), timestamp FROM messages
  WHERE session_id=? AND role IN ('user','assistant')
  ORDER BY timestamp LIMIT 12
""", (session_id,)).fetchall()
con.close()

# Load both handlers
spec_a = importlib.util.spec_from_file_location('h_a', '/path/to/plugin_a/__init__.py')
mod_a = importlib.util.module_from_spec(spec_a); spec_a.loader.exec_module(mod_a)
# ... similarly for handler_b

# Replay each turn through both
for i, row in enumerate(rows):
    msgs = [{'role':'system','content':'sys'}] + [
        {'role': r[1], 'content': r[2]} for r in rows[:i+1]
    ]
    a_fired = bool(mod_a.pre_llm_call(...))
    b_fired = bool(mod_b.pre_llm_call(...))
    doubled = a_fired and b_fired
    # doubled > 0 is a regression; log every doubled case
```

The test passes iff: zero doubled fires across the replayed transcript, every previously-passing synthetic test still passes, and the handler that was supposed to own each signal class does fire (not zero-fire on inputs that should trigger).

### 7. Receipt

Format that worked this session (Arif endorsed):

```
**Verified fact:** (3-5 lines of WHAT the test/replay actually showed, not a description of what you intended)

**Status:**
- file A — what changed, line range, verified count
- file B — what changed, line range, verified count
- interference replay — N turns, X doubled, Y zero-fired-where-expected
- open debt — explicit "belum habis" if any
```

Don't write the receipt before the test passes.

## Pitfalls

1. **Mechanism split is a smell, not a goal.** Two handlers with the same condition on the same hook event is duplicate machinery — token waste + confusing output. Always check for it before declaring "done." The cheapest detection: list every plugin's `pre_*` functions and grep their condition patterns against your new condition.

2. **Asking "X or Y?" when defaulting is reversible = attention leak.** The membrane: technical questions route to musyawarah, not F13. Default-rule: pick the reversible lane, execute, report. If you don't know which lane is reversible, probe both lanes' test pass counts first — that's data, not a question.

3. **Don't add first-turn handling to a handler that requires entity-name.** Plugin guards that conditionalize on entity-name will not fire on "Wei Arif, fair question" with no entity. The user's confession-before-probe defect happens both with and without entity — split the trigger space accordingly, don't try to make one handler cover both.

4. **Engine support left after deleting a rule is forward-compatible, not dead code.** When you remove a YAML rule but keep the engine python supporting its condition key (e.g. `is_first_turn`), leave it. Future rule may use the same key. Removing it is double-mutation for no current benefit.

5. **Replay-test against a transcript you produced yourself hides bugs.** Always replay against `state.db` from a real session — the synthetic version of your own session will have the same defects as the production version. Use the user's session_id, not your own test fixture.

6. **"Hook infra is wired" requires a call site, not just a file.** A script or rule that exists at canonical path but is not invoked by any plugin = theatre, not wiring. `grep -rn` for the script path inside plugin code paths. Zero hits = unwired.

7. **Status report format that the user endorsed is a standing rule.** When the user says "report state sebenar, path, verified count, belum habis jujur" — that becomes the standing format for this class of work, not a one-time ask. Memory captures "who the user is"; the skill captures "how to report."

8. **Plugin signature mismatch breaks daemon silent.** When you change a plugin's `__init__.py` signature, the daemon that loads plugins may not pick up the change until restart. Verify with a subprocess invocation (engine runs via subprocess — fail-closed is the default, so missing-import returns the original content unchanged, NOT an error).

9. **Don't propose more than 3 options to F13.** A/B/C menu is fine. A/B/C/D/E is choice paralysis. If you have 4+ options, recommend one with a one-line justification and let the human override — don't list them.

10. **"Belum habis" is a label, not a confession.** When you cannot complete a step in this session, write "belum habis: <what's missing>" in the receipt. Don't fold unfinished work back to the user as a question. Don't pretend it's done.

## References

| Reference | What it covers |
|---|---|
| `references/capability-matrix.md` | Decision table: which signal class belongs in engine yaml vs plugin, with examples |

## Verification checklist before reporting done

- [ ] Every handler for the hook event is listed and its condition keys recorded
- [ ] No two handlers trigger on the same (hook_event, signal_class) — if there is overlap, capability split has been done
- [ ] Each handler passes its own synthetic unit tests
- [ ] Interference replay against real `state.db` transcript: zero doubled, zero-zero-fired-where-expected
- [ ] Receipt written in state-sebenar + path + verified count + belum-habis format
- [ ] Reversibility path documented (which file to delete/revert to undo)

DITEMPA BUKAN DIBEI ⚒