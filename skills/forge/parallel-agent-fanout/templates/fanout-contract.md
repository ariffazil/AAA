# FROZEN INTERFACE CONTRACT — <objective name>
> Version: v1 · Frozen <date> · Owner: <parent agent> · Authority: <authority holder>
> **NO AGENT MAY EDIT THIS FILE.** Build to it. If it is wrong, report it — do not silently deviate.

## 0. Why this file exists

<One paragraph: what breaks without a shared contract. State the failure mode the contract prevents.>

## 1. Probe results (build to THESE, not to assumptions)

| Package / component | Status |
|---|---|
| <name> <version> | present |
| **<name>** | **ABSENT — do not import** |

Existing surfaces that MUST be respected (do not modify, do not duplicate):
- `<path>` — <what it is and why it is off-limits>
- `<path>` — <existing engine to reuse rather than reimplement>

## 2. File ownership (disjoint — other agents own the rest)

```
<path/owned_by_you_1>
<path/owned_by_you_2>
<test path owned by you>
```

Files owned by sibling agents — do not create, edit, or delete:
- `<path>`
- anything under `<other package>/`

## 3. The shared envelope — EVERY component returns this

```python
<type definition, written out in full>
```

Invariants (enforced by the type, not by convention):
- <invariant 1>
- <invariant 2>

## 4. Function signatures — FROZEN

```python
def <name>(<args>) -> <return>:
    """<one line>

    <constraints, units, and what UNMEASURED means here>
    """
```

Rules for every function in this file:
- <rule, e.g. "no function may return a probability it invented; emit n_samples / coverage / uncertainty">
- <rule, e.g. "a classification may only be emitted by a named rule whose decision inputs are measured; otherwise UNMEASURED with value null">

## 5. Output bundle

```python
{
  "<key>": <shape>,
  "status": "MEASURED" | "PARTIAL" | "UNMEASURED",
  "local_verdict": "QUALIFIED_CANDIDATE",
  "pending_authority": "<who seals>",
  "preferred_hypothesis": None,   # ALWAYS None — never populated by this layer
}
```

**Forbidden in the bundle:** <list the keys that must never appear — confidence, probability, score, any self-assigned certainty>.

## 6. Doctrine that MUST be preserved through the wire

Numbered, each with its reason. A naive implementation drops these.

1. **<rule>** — <why, and the failure it prevents>
2. **<rule>** — <why>
3. **<rule>** — <why>

## 7. Anti-collision protocol (mandatory for every agent)

Parallel agents overwrite shared directories mid-task. Therefore:
- **Create only the files listed in your brief.** No other file may be created or modified.
- Never edit this contract, the shared engine, or any file outside your brief.
- Do not run mutating version-control commands.
- Run only your own test file; a full-suite run while siblings write measures the race.
- Before finishing, run your own tests and paste **real** command output. A claim without
  pasted tool output is not a deliverable.

DITEMPA BUKAN DIBERI ⚒️
