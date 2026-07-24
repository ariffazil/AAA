---
id: APEX-fff-loop-protocol
name: APEX-fff-loop-protocol
version: 2.0.0
description: '5-pass recursive audit sequence: Blue (diagnose) → Red (attack) → Blue
  (forge) → Yellow (verify) → Gold (seal). Emits skill artifacts + MEMORY line + drift
  signal. BIJAKSANA: XML-tagged for Claude, numbered steps for Codex, imperative for
  Hermes.

  '
floor_scope:
- F01
- F04
- F08
- F11
cognitive_hints:
  claude: Use <pass-blue>, <pass-red>, <pass-gold> tags. Extended recall for cross-pass
    state.
  codex: '5 sequential passes. Each pass: input from prior → process → output to next.
    Strict chaining.'
  hermes: 5 passes. Diagnose. Attack. Forge. Verify. Seal. Run them.
owner: AAA
---
# APEX-fff-loop-protocol

<cognitive-note model="claude">XML-tagged audit passes. Maintain cross-pass state in extended context.</cognitive-note>
<cognitive-note model="codex">5 sequential passes. Each has explicit input/output. Chain-of-thought at each pass boundary.</cognitive-note>
<cognitive-note model="hermes">5 passes. Run in order. Each feeds the next. Seal at end.</cognitive-note>

## The 5 Passes

<passes>
| Pass | Color | Name | Action | Output |
|------|-------|------|--------|--------|
| 1 | Blue | Diagnose | Identify the problem | Problem statement + scope |
| 2 | Red | Attack | Adversarial critique | Weaknesses + failure modes |
| 3 | Blue | Forge | Build the fix | Solution + implementation |
| 4 | Yellow | Verify | Validate the fix | Test results + regression check |
| 5 | Gold | Seal | Finalize and seal | Verdict + vault entry |
</passes>

## Pass Details

<pass id="1" color="blue" name="diagnose">
- Input: Target artifact (code, skill, architecture)
- Process: Analyze structure, identify issues, scope blast radius
- Output: Problem statement with severity classification
</pass>

<pass id="2" color="red" name="attack">
- Input: Problem statement from Pass 1
- Process: Adversarial critique. Try to break it. Find edge cases. Red-team.
- Output: List of weaknesses, each with exploitation scenario
</pass>

<pass id="3" color="blue" name="forge">
- Input: Weaknesses from Pass 2
- Process: Build fix for each weakness. Prefer surgical patches over rewrites.
- Output: Fix implementation with rollback plan
</pass>

<pass id="4" color="yellow" name="verify">
- Input: Fix from Pass 3
- Process: Run tests, check for regressions, verify floor compliance
- Output: Test results, regression report, floor checklist
</pass>

<pass id="5" color="gold" name="seal">
- Input: Verified fix from Pass 4
- Process: Final review, emit verdict, write to VAULT999
- Output: SEAL verdict + vault entry + MEMORY line
</pass>

## Floors
- F1 AMANAH: Each pass is reversible until Pass 5 (seal).
- F4 CLARITY: Each pass must produce clearer output than its input.
- F8 GENIUS: Systemic health maintained across all 5 passes.
- F11 AUDITABILITY: Full 5-pass trace logged.
