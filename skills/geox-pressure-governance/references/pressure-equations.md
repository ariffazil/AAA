# Pressure Equations Reference — GEOX Engine
# DITEMPA BUKAN DIBERI

## Eaton Method (1969)

```
Pp = Sv - (Sv - Ph) * (Δtn / Δto)^n
```

Where:
- `Pp` = pore pressure (MPa)
- `Sv` = overburden pressure (MPa)
- `Ph` = hydrostatic pressure (MPa)
- `Δtn` = normal compaction slowness (μs/m)
- `Δto` = observed slowness from sonic log (μs/m)
- `n` = Eaton exponent (typically 1.2–3.0 for shale)

**Normal compaction trend (NCT):**
```
Vnc = V0 + k * z
Δtn = 1e6 / Vnc
```

Where:
- `V0` = velocity at zero effective stress (Malay Basin: ~1500 m/s)
- `k` = velocity gradient (Malay Basin: ~0.55 m/s per m)

**Eaton exponent calibration:**
- n=1.2: underpressured or very young sediments
- n=3.0: standard shale (default — but MUST be calibrated with RFT)
- n=6.0: highly overpressured unloading

**Malay Basin note:** Madon 2006 shows top of overpressure at basin center is 1900-2000m, controlled by Group F regional seal. Eaton exponent should be calibrated against at least 3 RFT points below Group F.

## Bowers Method (1995)

**Virgin compaction:**
```
σ = ((V - A) / B)^4
Pp = Sv - σ
```

**Unloading (fluid expansion):**
```
V = A + B * σmax * (σ / σmax)^D
```

Where:
- `A` = velocity at zero effective stress (Malay Basin: ~1500 m/s)
- `B` = compaction constant (~0.5)
- `C` or `D` = unloading coefficient (basin-specific)
- `σmax` = maximum past effective stress

**When to use Bowers over Eaton:**
- When fluid expansion (thermal/diagenetic) is suspected as overpressure mechanism
- When sonic velocity shows "reversal" or "kink" below the normal compaction trend
- When RFT/MDT shows pressures above the Eaton prediction (unloading signature)

## Phillips Fracture Gradient (1972)

```
FG = Pp + C * (Sv - Pp)
```

Where:
- `C` = Phillips coefficient (typically 0.6–0.9)
- `C=0.85` is common for Malay Basin shales (UNCALIBRATED — needs LOT)

**Calibration:** LOT/XLOT at casing shoes. Each LOT point provides one FG measurement at that depth.

## Hydrostatic Gradient — Malay Basin

```
Ph = z * 10.5 kPa/m
```

(1.05 SG brine, typical for Malay Basin. Can range 1.0-1.1 SG depending on salinity.)

## Overburden — Malay Basin (Madon 1997)

```
Sv = ∫ ρ(z) * g * dz
```

Where:
- `ρ(surface)` ≈ 1800 kg/m³ (unconsolidated)
- `ρ(4000m)` ≈ 2400 kg/m³ (compacted)
- Basin center β (stretching factor) ≈ 4.0
- Basin flank β ≈ 1.2

**Heat flow:** 33-42 mW/m² (Madon 1997). Basin still undergoing thermal subsidence (~35 Ma).

## Malay Basin Compartment Model (Madon 2006)

| Compartment | Top Depth | Seal | Mechanism |
|---|---|---|---|
| Basin center | 1900-2000m | Group F shale | Compaction disequilibrium |
| Basin margin | 2600-3000m | Group L shale | Lateral transfer, secondary |

**Group F role:** Regional transgressive shale. Acts as top seal for overpressure in the central Malay Basin. "Soft" overpressure transition above Group F, "hard" overpressure below.

**Group L role:** Caps separate overpressure compartment at basin margins (2600-3000m). Controlling seal for the secondary compartment.

## Sanity Fuses

1. **FG > Sv** → unphysical → 888_HOLD (fracture gradient cannot exceed overburden)
2. **Pp > Sv** → physically impossible (rock would fail) → 888_HOLD
3. **Pp < Ph** → underpressured → flag, check for depletion or uplift
4. **Confidence > 0.85 without calibration** → F7 violation → clamp to 0.72

## References

- Eaton, B.A., 1969. Graphical method predicts geopressures worldwide. *World Oil* 168(6):51-56.
- Bowers, G.L., 1995. Pore pressure prediction from seismic data. *SPE Formation Evaluation* 10(4):249-257.
- Phillips, H.N., 1972. Fracture gradient analysis — new approach to an old problem. *SPE* 4137.
- Matthews, W.R. & Kelly, J., 1967. How to predict formation pressure and fracture gradient from electric and sonic logs. *Oil & Gas Journal* 65(8):92-106.
- Madon, M., 2006. Overpressure history of the Malay Basin. *GSM Bull.* 49:135-144.
- Madon, M., 1997. Analysis of tectonic subsidence and heat flow in the Malay Basin. *GSM Bull.* 41:95-108.
