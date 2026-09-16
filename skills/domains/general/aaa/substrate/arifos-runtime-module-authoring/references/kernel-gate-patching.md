# Patching existing arifOS kernel gate files (2026-09-01 session)

Learned while hardening the kernel with LAW_ZEN_ATTENTION (commit 94d0bfa60, 9 files,
610 insertions, LSP pre-commit gate 8/8 clean). Complements the SKILL.md creation guide.

## 1. Implicit string concatenation — real bug class in gate files

Adjacent string literals inside frozenset/tuple literals silently merge:

```python
IRREVERSIBLE_ACTION_TYPES = frozenset({
    "rotate_master_secret"        # ← missing comma
    "modify_constitution_f1_f13", # merges into ONE string
})
```

Found live in `arifosmcp/runtime/consequence_gate.py`: two irreversible action types
merged into `"rotate_master_secretmodify_constitution_f1_f13"`, so constitutional
mutations and master-secret rotations slipped the P40 gate unflagged.

Audit one-liner for any gate file:
```bash
grep -nE '"[^"]+"\s*$' file.py   # string literal ending a line, no comma
```
Then verify set membership in a REPL: `'rotate_master_secret' in IRREVERSIBLE_ACTION_TYPES`.

## 2. Freeze discipline — check before touching any kernel file

- `arifosmcp/runtime/kernel_freeze.py` → `ENFORCEMENT_MODULES` tuple = the G7-pinned
  constitutional circuit (pre_execution_gate, canonical_vault_chain, self_mod_lock,
  act_token, session, kernel_router, law, kernel_freeze). Modifying a file in that
  set changes the freeze digest; with `ARIFOS_KERNEL_FREEZE_ENFORCE=1` a digest
  mismatch BLOCKS every mutating action at Gate 8.5.
- Pin: `ARIFOS_KERNEL_FREEZE_PIN` env or `/var/lib/arifos/kernel_freeze.pin`.
- `docs/FREEZE_PROTOCOL.md` — check status (PROPOSAL awaiting F13 fire-word `freeze`
  vs sealed). While PROPOSAL, gate files outside ENFORCEMENT_MODULES may be patched
  with the additive discipline below.
- Read the FULL target file before patching — pagination warnings from read_file are
  real; partial reads caused a duplicate-kwargs SyntaxError this session (patch tool
  inserted `enforce=`/`timestamp=` twice; caught by py_compile, not lint).

## 3. Additive + flag-gated + default-invariant (Phase-1 discipline)

The kernel runs `COLLAPSE_TRIGGER_ENFORCE = False` (Phase 1 observe-only). Any new
behavior MUST:
- add dataclass fields WITH defaults (backward compat for frozen constructors),
- add function params as keyword-only with defaults,
- gate enforcement behind a NEW flag defaulting to False (e.g. `ZEN_ATTENTION_ENFORCE`),
- never change existing verdict paths when the flag is off,
- carry a dated comment: `# LAW_X (date, additive — F13 pending)`.

Genesis canon files (GENESIS/*.md) have amendment procedures — append a clearly
labeled `PROPOSAL` section, never edit ratified sections.

## 4. Testing kernel changes

- Cold import chain is SLOW: `core.physics.economic_invariants` pulls the whole
  arifosmcp schema graph (~2 min). Use timeout ≥ 300s or background=true.
- Many kernel modules run `_self_test()` at import — a plain `python3 -c "import ..."`
  exercises them.
- pytest conftest runs a protocol sentinel against `http://127.0.0.1:8088/mcp`; if the
  kernel is down, set `ARIFOS_SKIP_PROTOCOL_SENTINEL=1` for offline runs.
- **Baseline attribution for failing tests**: `git stash push -m wip && run test &&
  git stash pop`. If it fails on baseline too → pre-existing, not your regression.
  (test_forge_preflight_irreversible_action_requires_ack failed identically on
  baseline this session.)

## 5. Multi-agent concurrency hazard

Another session may edit the same working tree concurrently (this session found
LAW_ZEN_ATTENTION additions in forge_preflight.py / principal_paradox.py that arrived
via a timed-out batch delivery mid-session, plus a separate agent touching
mind_feedback_hook.py). Rules:
- `git diff --stat` BEFORE committing; know what is yours.
- Stage explicit file paths only — NEVER `git add -A` / `git commit -a`.
- Expect a timed-out tool call to have PARTIALLY landed; re-read the file before
  re-applying the same patch (double-application = duplicate defs).
- **A sibling agent may COMMIT your in-flight patches** (kimi-code/FI-008 committed
  the core LAW_ZEN_ATTENTION gate work under `94d0bfa60` while this session was still
  editing). After any external modification: re-read the file, reconcile duplicate
  dataclass fields (CollapseVerdict got two LAW_ZEN_ATTENTION blocks; merge, don't
  stack), and verify your patches landed in the sibling commit with
  `git show <sha>:<file> | grep -c <marker>` — git status may show the file as
  clean because the sibling committed it.

## 6. Broken package `__init__` — load modules directly via importlib

`from arifosmcp.runtime.X import ...` can fail with ModuleNotFoundError even when
`runtime/X.py` exists, because `arifosmcp/runtime/__init__.py` imports modules that
don't exist (e.g. `arifosmcp.runtime.compression`). Workaround for testing single
modules without fixing the package:

```python
import sys, importlib.util
sys.path.insert(0, '.')
spec = importlib.util.spec_from_file_location('pp', 'runtime/principal_paradox.py')
pp = importlib.util.module_from_spec(spec)
sys.modules['pp'] = pp          # MUST register BEFORE exec for dataclasses
spec.loader.exec_module(pp)
```

Registering in `sys.modules` first is mandatory — dataclass `__post_init__`/field
resolution looks up the class's module and crashes with
`AttributeError: 'NoneType' object has no attribute '__dict__'` if it's not there.
Same pattern works for forge_preflight.py, consequence_gate.py, mind_feedback_hook.py.

Also: `arifosmcp/core/physics/economic_invariants.py` is a RE-EXPORT wrapper around
the canonical `/root/arifOS/core/physics/economic_invariants.py` — importing the
wrapper can raise a circular-import error. Test the canonical copy from `/root/arifOS`
root instead (sys.path.insert(0, '/root/arifOS')).

## 7. Gate-wiring pass — a built gate with no live caller is dead code

Commit `1a36840` built the LAW_ZEN_ATTENTION enforcement gates but left four
dead seams; commit `f3a077a49` closed them. Generalizable rules:

**Dead-seam audit.** After any commit that adds a gate function or new params to
a gate, grep for live call sites:
```bash
grep -rn "new_gate_fn(" arifosmcp/ --include="*.py" | grep -v "def \|test_"
```
Zero hits, or the orchestrator passing nothing for the new params = dead wiring.
Fixed seams this session: run_forge_preflight→stage_10 (K-Gate params threaded),
gate_1_5_principal_paradox→autonomous_invariant_seal (promotion branch),
governance_pipeline E7 call (proofs read from ctx via `getattr(ctx, ..., False)`),
swarm_ignition boot (close_stale_loops before measure, try/except → DEGRADED receipt).

**Caller-forged-proof guard (SECURITY).** Any bypass-gate whose inputs are
caller-supplied (reversibility score, rollback recipe, proofs) MUST void those
inputs when an upstream classifier already said irreversible:
```python
_k_gate_active = reversibility != "IRREVERSIBLE"
... reversibility_score=reversibility_score if _k_gate_active else None
```
Otherwise deploy-mode callers forge `score=0.99` to skip ack. Always test the
forgery attack yourself before committing (deploy + forged proof must STILL block).

**Gate ordering — constitutional gates go AFTER observe-only overrides.**
`if not enforce: verdict = SEAL` swallows any HOLD computed before it. If the
gate protects a constitutional floor (attention, safety), place its enforcement
AFTER that override; only telemetry stays observe-only.

**Probe shapes — read the return dict before asserting.** First battery run
asserted `r.get('passed')` on run_forge_preflight, which has NO `passed` key
(keys: human_ack_valid, reason_codes, reversibility, final_gate, ...). Print
`sorted(r.keys())` first. Similarly: ActionClass enum values are OBSERVE,
ANALYZE, DRAFT, SIMULATE, MUTATE, EXTERNAL_SIDE_EFFECT, IRREVERSIBLE, UNKNOWN —
the docstring's "PROPOSE" is stale. Read enums, not docstrings.

**Scary test names don't mean your bug.** `test_safety_refuses_execution_for_irreversible`
failed inside `load_quote_ledger` (missing fixture) — attribute via clean stash
(section 4) before losing sleep; note it as pre-existing in the commit message.

Full detail: skill `a-forge-development` → `references/law-zen-attention-seam-closing.md`.
