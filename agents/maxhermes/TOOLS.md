# TOOLS.md — maxhermes Agent

## Allowed Tools

### GEOX (Earth Domain)
- `geox_load_well_log` — load wireline log data
- `geox_archie_sw` — compute water saturation
- `geox_kozeny_carman_phi` — compute porosity
- `geox_seismic` — seismic data
- `geox_horizon_pick` — horizon interpretation
- `geox_monte_carlo_volume` — volume estimation

### Grounding
- `geox-ground` — physics grounding
- `maxhermes-geox-ground` — MaxHermes GEOX skill

### Verification
- `self-verify` — claim verification before output
- `consequence-classifier` — AC_Risk classification

### MCP
- `arifOS kernel` — constitutional judgment
- `arifos_compute_risk` — risk scoring

## Prohibited

- Present interpretation as observation
- Claim grade without verification
- Skip self-verify on consequential claims
- Bypass 888_HOLD pattern

---

*Last updated: 2026-04-29*
