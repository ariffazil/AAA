---
name: forge
description: "Forge — bare /forge alias for the 333-forge spine. Build the smallest executable unit now; receipt > narrative."
triggers:
  - "/forge"
relationships:
  - target: hermes-forge
    type: alternative_to
    confidence: 1.00
  - target: opencode-forge
    type: alternative_to
    confidence: 1.00
---

# /forge

Bare alias for `/333_forge`.

1. Read `/root/AAA/skills/333-forge/SKILL.md`.
2. Take the smallest unit that can run now; finish it or name the blocker.
3. Receipt: `flow_ingest(step_type=Execute, payload={"zen":"333","artifact":<path|blocker>})`.

Do not open a large task without explicit intent.
