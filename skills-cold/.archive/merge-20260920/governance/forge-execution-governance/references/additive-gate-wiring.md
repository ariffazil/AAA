# Wiring an Additive Governance Gate

The build-side counterpart of `forge-execution-governance` §7. Use when adding a new guard to an
existing governed service — an explanatory-class gate, an evidence-type gate, a provenance gate —
where the contract must be extended without breaking existing records or the existing state machine.

## 0. Find the live object before editing anything

A service usually has the same surface implemented in several layers: a typed model, a mode
dispatcher, a tool/server registration, and a store. Determine **which one holds the live object and
the transition guard** before choosing an edit site. Read all candidates, then answer concretely:

- where is the record actually persisted, and by which function?
- which function is the transition guard (the one that runs the pre-conditions)?
- which layer is registered as the public tool?

Editing the model layer when the live object is a plain `dict` in a store is the common mis-take: the
`dict` never passes through the model, so nothing validates.

## 1. The three resolutions — prove all three, or the gate cannot fire

### 1a. Module identity

```bash
# from the interpreter AND cwd the service and the test suite actually use
python -c "import <pkg>.<mod> as m; print(m.__file__)"
```

If a duplicate tree exists (a stale top-level copy beside `src/`), which one wins depends on
`sys.path` order, and the test runner's order can differ from the service's. Print the resolved file
from both contexts.

### 1b. Published surface

For a mode-dispatched MCP tool, the input schema comes from the **registered wrapper signature**, not
the implementation. A parameter added to the impl alone is invisible (and `additionalProperties:
false` means the caller is refused, not merely ignored).

```bash
grep -n '<tool_name>' <wiring_module>.py      # find every wrapper signature
# then, at runtime:
tools/list -> <tool>.parameters.properties     # does the new parameter appear?
```

Patch the impl, the dispatcher, **and** the wiring signature. An integration test that asserts the
parameter is present in the published schema keeps this from regressing silently.

### 1c. Store / path

```bash
readlink -f <reader_path>; readlink -f <writer_path>   # compare resolved, not literal
ls -la <both parents>                                  # does the wrong parent exist (shadow create)?
```

Two paths differing only in case, or one symlink vs one direct path, are the usual split. If the wrong
parent directory exists, a file-backed store will create a second store there and the reader will
keep reporting the first one's numbers forever.

**Consequence to state plainly:** with a split store, a correct guard never fires. Test count > 0,
production count = 0. Say that in the report rather than presenting the passing tests as sufficiency.

## 2. Editing across duplicate package trees

When a duplicate tree shadows the real one, mirror the *additive* change into both so the behaviour is
identical whichever resolves — then **report the duplication as a pre-existing hazard**. Do not
silently normalise one tree into the other (that is a much larger, unrequested mutation), and do not
leave the axis half-applied (a field present in one copy only is worse than absent, because which
copy resolves is not obvious from the source).

## 3. Contract and code must be assertable against each other

When the rule lives in a YAML/JSON contract *and* in code, write the test that reads the contract and
compares it to the code's own vocabulary and rules:

- the contract's class/enum list == the module's exported list
- the contract's guarded transitions == the guard function's guarded targets
- the original error codes are all still present (assert the **original set** survives, not just that
  new ones exist)
- JSON schemas: the new field is **not** added to `required`, so pre-existing records stay valid

This turns "the contract documents the rule" into "the contract cannot drift from the rule".

## 4. Test shape that proves the guard actually stops something

Cover, at minimum:

1. the refused case for **each** guarded target, asserting the **error code** (not just a falsy return)
2. the fallback the contract recommends for the worst class (e.g. transition to a terminal reject)
3. the declared-but-contradicted case — declaring a strong class over text that does not support it
   must still be refused; otherwise a declaration is a bypass
4. a record from **before** the field existed (key absent) reads as the fail-closed default
5. unknown/junk values are never promoted into an allowed class
6. **every unguarded transition still passes for every class** — this is the "did not break the
   existing machine" test and it is the one most often skipped
7. the live path: drive the real guard function with a stub store and a dead upstream, asserting the
   new error code, that legacy gates still win their own legacy code, and that unrelated verdicts are
   untouched
8. the field is reachable from the published surface (§1b)

## 5. Running the repo's suite

- **Use the repo's own virtualenv**, not the agent runtime interpreter. A collection failure is far
  more often a wrong-interpreter problem (missing `fastmcp`, `pytest-asyncio`) than a broken suite;
  check for `.venv/` and run `.venv/bin/python -m pytest`. Report which interpreter produced which
  result, and do not report a wrong-interpreter failure as a suite defect.
- **Record the baseline BEFORE editing**: full-suite run to a file, capturing the `FAILED <nodeid>`
  list.
- **Diff the failure SET, not the count.** Suites that regenerate their own export artifacts mid-run
  flip unrelated tests between runs; a count change is not attributable to you. `set(after) -
  set(before)` empty is the claim worth making, and name the tests that flipped for unrelated reasons.
- An isolated run of the new test file is **valid evidence** for the new code when the wider suite is
  blocked. State plainly which of the two you achieved.
- Do not import the service's server/bootstrap module in the new test file unless you must; keeping it
  import-free means it collects and runs even when the wider suite cannot.

## 6. Concurrent writers

Run `git status` **at the end, not only at the start**. In a busy federation, files change under you:
untracked scripts appear, another writer edits the test file you are working in, and suites rewrite
tracked generated artifacts (`.well-known/*.json`, `llms.txt`, tool manifests).

- restore generated artifacts you did not intend to change before reporting
- verify the lines you are about to claim are actually yours, and report foreign edits as foreign —
  do not fold them into your change report, and do not silently "fix" them
- a schema entry another writer added while you worked still needs verifying before you cite it as
  working; correct-but-foreign is a different statement from your own edit
