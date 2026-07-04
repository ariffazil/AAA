# Implementation Contract

All Forge execution must adhere to this contract:

1. **Traceability**: Every mutation must trace back to an approved step in the Architect's brief.
2. **Reversibility**: Prefer atomic, reversible changes. Do not bundle unrelated refactors into a single feature implementation.
3. **Evidence**: You cannot claim a task is complete without evidence (e.g., successful test output, log traces).
4. **Boundary Preservation**: Respect existing repository structures. Do not rename canonical files unless explicitly requested.
