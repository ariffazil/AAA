---
name: geox-temporal-intelligence
description: "Operate GEOX temporal intelligence — decline curves, RRR, basin lifecycle, dynamical systems (Takens/EDM), and the shared temporal primitive bridging GEOX state reconstruction to WEALTH market intelligence. Use for production forecasts, reserve depletion, basin maturity, regime detection, attractor reconstruction, and any point-in-time→temporal upgrade."
version: 2.0.0
triggers:
  - Production decline curve or forecast
  - Reserve replacement ratio calculation
  - Basin lifecycle or maturity assessment
  - Exploration cadence or pipeline lag
  - Petronas temporal analysis
  - Dynamical systems or Takens embedding or EDM
  - State-space reconstruction from time series
  - Regime detection or attractor reconstruction
  - Temporal intelligence architecture across GEOX and WEALTH
  - Point-in-time to temporal upgrade
  - Awesome-Agentic-Time-Series research mapping
related_skills:
  - wealth-mcp-ops
  - financial-chart-analysis
---

# GEOX Temporal Intelligence

Two layers of temporal capability on GEOX `:8081`:

**Layer 1 — Domain tools** (earth.temporal): 4 pure-computation tools. No network, no mutable state, OBSERVE-class only.

**Layer 2 — Dynamical systems** (`geox_dynamical_systems`): State-space reconstruction primitives. Takens embedding, mutual information, false nearest neighbors, EDM kernel. These are the SHARED TEMPORAL PRIMITIVE that bridges GEOX Earth-state reconstruction to WEALTH market-state reconstruction.

**Architecture** (Arif, 2026-08-09):
```
                ┌─ Temporal Embedding ─┐
                │ (Takens / EDM /      │
                │  foundation model)    │
                └─────────┬────────────┘
                          │
             ┌────────────┼────────────┐
             ▼                         ▼
        GEOX domain              WEALTH domain
        ───────────              ────────────
        • Decline curves         • Regime detection
        • 4D seismic             • Volatility forecasting
        • Basin subsidence       • Multi-horizon price
        • Thermal history        • Anomaly detection
             │                         │
             ▼                         ▼
        Earth state vector       Market state vector
```

**Zen principle:** Don't add new tools. Harden what exists. `capital_indicator` trajectory mode (WEALTH) and `geox_dynamical_systems` (GEOX) share the same mathematical foundation — attractor reconstruction from temporal data. The same Takens embedding that reconstructs a basin's subsidence history can reconstruct gold's price regime.

**Point-in-time vs temporal** (the gap):

| Domain | Point-in-time (now) | Temporal (missing) |
|--------|-------------------|-------------------|
| GEOX | Porosity = 18%, Vsh = 25% | How does porosity decline with depth? Did thermal maturity peak 5Ma or 50Ma ago? |
| WEALTH | RSI = 63.5, ATR = $19.87 | Did RSI cross 70→60? Is ATR expanding or contracting? Regime CHANGE or CONTINUATION? |

Foundation models for time series (Chronos, Timer, TiRex) could close this gap — zero-shot forecasting, regime detection, multi-horizon prediction. Research context: [Awesome-Agentic-Time-Series](https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series).

| Tool | What it does |
|------|-------------|
| `geox_temporal_decline` | Exponential decline curve fit + forecast |
| `geox_temporal_rrr` | Reserve replacement ratio tracking |
| `geox_temporal_basin_lifecycle` | Basin maturity stage classification |
| `geox_temporal_cadence` | Exploration-to-production pipeline analysis |

## geox_temporal_decline

Fit exponential decline: Q(t) = Q0 * exp(-D*t)

**Input:** `production_data` (list of {year, bpd}), `forecast_years`, `threshold_bpd`
**Output:** `trend` (growth/stable/decline), `decline_rate_pct_annual`, `forecast` (list of {year, bpd}), `years_to_threshold`

```python
# Malaysia production decline
geox_temporal_decline(
    production_data=[
        {"year": 2020, "bpd": 550000},
        {"year": 2023, "bpd": 454000},
        {"year": 2025, "bpd": 380000}
    ],
    forecast_years=5,
    threshold_bpd=350000
)
# → years_to_threshold = when production can't meet refinery needs
```

## geox_temporal_rrr

**Input:** `reserves_start_mmbbl`, `additions_mmbbl`, `production_mmbbl`
**Output:** `rrr_ratio`, `interpretation` (replacing/partial/consuming), `reserves_end_mmbbl`, `years_at_current_rate`

RRR >= 1.0 = replacing. RRR < 1.0 = consuming.

```python
geox_temporal_rrr(5000.0, 200.0, 400.0)
# → rrr_ratio=0.5, interpretation="consuming"
```

## geox_temporal_basin_lifecycle

**Input:** `basin_name`, `peak_production_bpd`, `current_production_bpd`, `discovery_year`, `peak_year`
**Output:** `stage` (growth/plateau/decline/mature), `remaining_potential_pct`, `decline_rate_pct`

```python
geox_temporal_basin_lifecycle("Malay Basin", 500000.0, 250000.0, 1969, 2004)
# → stage="decline", remaining=50%
```

## geox_temporal_cadence

**Input:** `blocks_offered`, `blocks_awarded`, `years_span`, `average_cycle_time_years`
**Output:** `award_rate_pct`, `pipeline_lag_years`, `production_impact_year`, `capacity_gap_assessment`

```python
geox_temporal_cadence(20, 12, 3, 4.5)
# → production_impact_year = current + 4.5 years
```

## Dynamical Systems (geox_dynamical_systems)

State-space reconstruction primitives — the bridge to WEALTH temporal intelligence.

| Tool | What it does | Reference |
|------|-------------|-----------|
| `geox_mutual_information` | Find optimal delay τ for Takens embedding (Fraser & Swinney 1986) | First local minimum of I(τ) |
| `geox_false_nearest_neighbors` | Find optimal embedding dimension E | FNN ratio < threshold |
| `geox_takens_embed` | Build delay-coordinate library + targets | Takens (1981) embedding |
| `geox_edm_kernel` | Kernel-weighted local dynamics prediction | Sugihara & May (1990) EDM |

**Federation contract:**
- GEOX: reconstructs state-space (this module)
- WEALTH: interprets the geometry economically
- WELL: judges readiness to act on dynamical regimes
- arifOS: governs the authority to act on the forecast

**Key insight:** These primitives accept arbitrary univariate time series — not just Earth data. Gold prices, production rates, basin subsidence — all can be embedded into state space. The same Takens embedding that reconstructs a basin's subsidence history can reconstruct gold's price regime. This is the SHARED TEMPORAL PRIMITIVE.

**Limitations:** EDM is a local method — it works well near the attractor but degrades far from observed states. Reconstruction quality depends on series length (need 10^E points minimum for reliable embedding). Noise in the input series propagates through embedding — denoise first.

## Pitfalls

- Decline curve assumes exponential. Real fields may follow hyperbolic/harmonic. Exponential is conservative.
- RRR uses proved reserves only. Probable/possible not included.
- Basin lifecycle is relative. "Decline" = current vs peak, doesn't account for EOR.
- Cadence assumes linear pipeline. Real exploration has binary outcomes (dry holes).
- EDM requires sufficient data length: 10^E points minimum for reliable embedding (E = embedding dimension from FNN). Short series → unreliable reconstruction.
- Takens embedding assumes deterministic dynamics. Stochastic series (random walk) produce spurious attractors — test for determinism before embedding.
- `geox_dynamical_systems` does NOT forecast. It reconstructs state-space geometry. Forecasting is a CONSUMER of the reconstructed geometry (via EDM kernel prediction), not the purpose of the module itself.
- Foundation models (Chronos, Timer, TiRex) could enhance temporal intelligence but require either local GPU or API integration — not yet wired. See [Awesome-Agentic-Time-Series](https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series) for the research landscape.

## Research context

The temporal intelligence gap is mapped in [Awesome-Agentic-Time-Series](https://github.com/TROUBADOUR000/Awesome-Agentic-Time-Series) (151 stars, MIT, June 2026). Key streams relevant to GEOX+WEALTH:
- **Foundation models** (Chronos, TimeGPT, Moirai, Timer) — zero-shot forecasting without training
- **LLM4TS** — translating between time series and natural language for root-cause analysis
- **Agentic TS** — closed-loop forecasting agents with memory and world models
- **Benchmarks** (TemporalBench, TimeSage-MT) — evaluating temporal reasoning quality

Current GEOX position: Layer 1 (domain tools) is production-ready. Layer 2 (dynamical systems) is the primitive. Missing: foundation model consumption, world-model interface, temporal memory persistence.
