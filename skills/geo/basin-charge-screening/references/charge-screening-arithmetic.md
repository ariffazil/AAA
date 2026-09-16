# Charge Screening — Arithmetic and Decision Table

Companion to `basin-charge-screening`. Use when you have section thickness and gradient and need the verdict
fast, or when you need to sanity-check an optimistic prospectivity claim.

## Constants

| Quantity | Value |
|---|---|
| Seabed temperature, deep water | 2–4 °C |
| Seabed temperature, tropical shallow platform | 25–28 °C |
| Oil onset | 60–65 °C |
| Peak oil | 90–110 °C |
| Wet gas | 110–150 °C |
| Dry gas | >150 °C |
| Gradient, carbonate-dominated section | 23–25 °C/km |
| Gradient, typical clastic basin | 25–35 °C/km |
| Thermal conductivity, carbonate | ~2.8 W/mK |
| Thermal conductivity, shale | ~1.8 W/mK |
| Crust thickness: oceanic / thinned continental / normal continental | ~7 / 25–30 / 35–40 km |

**Carbonate sections run a *lower* gradient than shale-equivalent sections** because carbonate conducts heat
away from the source interval. Higher conductivity means faster heat loss, so a carbonate section that is the
same thickness as a shale section is *cooler*, not hotter. This is a common inversion — check which way you
applied it before reporting.

## Worked case — thick carbonate platform over thinned continental crust

Archetype: an isolated carbonate platform province built on a microcontinental fragment, one deep exploration
well penetrating a few kilometres of carbonate to volcanic basement, no proven source rock.

```
Inputs
  Section thickness (deepest well, to basement)   2.0–2.5 km
  Crust, from isostasy / geophysical inversion     25–30 km        -> thinned continental
  Gradient                                         23–25 °C/km     -> carbonate-dominated
  Seabed (tropical, shallow platform)              ~28 °C

Base-of-section temperature
  T = 28 + (2.5 km × 23 °C/km) = 28 + 57.5      = ~85 °C

Kitchen depths for this gradient and seabed
  Oil onset    (60 - 28) / 23  = 1.4 km
  Peak oil     (90 - 28) / 23  = 2.7 km
  Peak oil     (110 - 28) / 23 = 3.6 km

Verdict
  Base of section 85 °C  vs  peak oil 90–110 °C  ->  BELOW the kitchen
  Substantial source rock would need ~1 km of section that does not exist:
  below the base there is nothing but volcanic basement.
```

Two independent failures, both present:

1. **No generative section.** Shallow-water oxygenated platform carbonate; organic matter not preserved.
   Periplatform drift present but Neogene — too young to have matured.
2. **No burial.** 2.0–2.5 km is the entire section; basement is both the sediment floor and the thermal floor.
   The one well that penetrated it bottomed in basement, which caps total thickness rather than merely
   under-sampling it.

Observed corroboration: a large number of dry wells on the same ridge trend, reaching multi-kilometre depths
with zero commercial discovery. Treat that as thermodynamic evidence.

## Decision table

| Section to basement | Crust | Gradient | Expected base temp | Verdict |
|---|---|---|---|---|
| <2 km | 25–40 km continental | 23–25 °C/km | <80 °C | Cannot cook — no burial |
| 2–3 km | thinned continental 25–30 km | 23–25 °C/km | 80–100 °C | Marginal at best; depends entirely on source rock and whether the generative facies sits at the hot base |
| 3–5 km | normal continental | 25–30 °C/km | 100–150 °C | Can cook *if* a source rock exists; timing becomes the question |
| 2–3 km | oceanic 7 km + high heat flow | 35–50 °C/km | 100–150 °C | Can cook — thin crust and high heat flow substitute for thickness |
| any | any | any | any | **Zero identified source rock overrides every row above.** Compute the rest only after charge is plausible. |

## Failure modes to avoid

- **Defaulting seabed temperature to 0 °C.** On a tropical shallow platform this loses ~28 °C — a whole
  maturity zone.
- **Treating a thick section as automatically prospective.** Section thickness says nothing about source rock.
  A carbonate platform is thick sediment with no generative interval.
- **Reading thick crust as a positive.** It reduces subsidence. Thick crust plus thin section is the definitive
  negative combination.
- **Extrapolating a source rock at depths no well reached.** State it as speculation if you must mention it.
- **Borrowing a producing analog from the same ocean.** Verify its crust and heat-flow setting first; a
  rift-margin analog and a platform-on-microcontinent analog share no petroleum-system mechanics.
