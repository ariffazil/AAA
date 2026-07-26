# FEDERATION_MAP.md — AAA

```yaml
layer: L1
role: GOVERNANCE
function: Surface
status: ACTIVE
canon: arif-fazil.com/aaa/

identity:
  repository: ariffazil/AAA
  organ: AAA Control Plane
  floor_range: F1–F13 (via arifOS)

function: |
  AAA is the Agent Surface Layer of the arifOS Federation.
  It owns: operator cockpit, A2A gateway, federation state display,
  agent identity cards, and the human-facing control surface.

  AAA routes and displays. It does NOT adjudicate.
  Judgment belongs to arifOS (L0) and APEX (L1).

upstream:
  - ariffazil/arifos       # L0 — constitutional kernel

downstream:
  - ariffazil/arifFlow     # L1 — coordination
  - ariffazil/A-FORGE      # L1 — execution

federation_surface: https://arif-fazil.com/aaa/
```

**DITEMPA BUKAN DIBERI — Forged, Not Given.**
