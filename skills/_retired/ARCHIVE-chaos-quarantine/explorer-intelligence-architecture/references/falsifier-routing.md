# Falsifier Routing

One-line summary:
Every falsifier in a `falsification_packet` must be routed either to OpenClaw for cognitive attack or to A-FORGE for physical/runtime execution.

## 1. Purpose

Use this contract when Hermes or OpenCode hands a falsification packet forward and the system must decide:

- which falsifiers OpenClaw can do directly
- which falsifiers require A-FORGE substrate
- which cross-domain tools can be called in-place vs via forge execution

## 2. Input and Output

Input:

- `falsification_packet` from Hermes, directly or via OpenCode

Output:

- `tests[]` filled with routed falsifier tasks
- `next_route` set to `openclaw`, `aforge`, mixed, or return path

## 3. Decision Law

### Route to OpenClaw

Use OpenClaw when the falsifier is primarily cognitive:

- contradiction detection
- reasoning attack
- evidence comparison
- claim grammar checking
- domain-law synthesis
- cheap direct tool call with no build/run/deploy substrate

Examples:

- compare conflicting evidence
- run `geox_contrast_detect` if it is direct and bounded
- run `wealth_asymmetry_check` if it is direct and bounded
- synthesize which hypothesis is weakest under current evidence

### Route to A-FORGE

Use A-FORGE when the falsifier is primarily physical/runtime:

- computing heavy jobs
- running code
- build/test/deploy
- sandbox execution
- tool mutation
- environment-dependent verification

Examples:

- `forge_execute`
- `forge_sandbox_run`
- large simulation
- test suite execution
- build artifact generation

## 4. Cross-Domain Tool Rule

Cross-domain falsifiers are not automatically forge work.

Use this split:

- if the tool is directly callable, bounded, and returns evidence without substrate work -> OpenClaw can dispatch it
- if the tool needs runtime scaffolding, code execution, sandboxing, or artifact production -> A-FORGE owns it

Examples:

- `geox_contrast_detect` -> OpenClaw direct unless it needs extra runtime substrate
- `wealth_asymmetry_check` -> OpenClaw direct unless it expands into simulation or code execution
- Monte Carlo portfolio run -> A-FORGE
- synthetic seismic modelling batch -> A-FORGE if runtime-heavy

## 5. Test Entry Shape

Each routed falsifier should become a `tests[]` entry like:

```yaml
- test_id: test-001
  falsifier_id: fals-001
  route_owner: openclaw | aforge
  tool: ""
  test_type: cognitive | physical
  hypothesis_id: ""
  passed: null
  notes: ""
```

## 6. Mixed Routing

One packet may split.

If some falsifiers are cognitive and some are physical:

- OpenClaw owns the packet
- packet is partitioned into `tests[]`
- physical subset is forwarded to A-FORGE
- cognitive subset is handled locally
- result is reassembled into one packet before verify stage

## 7. Return Conditions

After falsifier routing:

- all tests inconclusive -> return to OpenCode or Hermes for stronger hypotheses or more observation
- one or more contradictions survive -> escalate using `next_route`
- physical execution blocked -> route to AAA/arifOS if lease, authority, or floor issue appears

## 8. Law

If the falsifier needs thought, OpenClaw can own it.
If the falsifier needs substrate, A-FORGE must own it.
If the falsifier changes authority or irreversibility, arifOS must see it.
