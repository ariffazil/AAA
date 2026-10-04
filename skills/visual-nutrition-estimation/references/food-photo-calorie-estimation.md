# Food Photo Calorie Estimation — Dessert Cups

Status: field-tested (2026-08-13)

## Policy
- Do not identify people in images. Describe food neutrally.
- Keep epistemic labels in reasoning trail: [OBS]/[DER]/[SPEC].
- Deliver the result with a [🦾ACT] receipt.

## Quick Method
1. Scale from common objects
   - Teaspoon bowl ≈ 4–5 cm diameter; handle ≈ 13–14 cm.
   - Small, low glass: ≈ 7–8 cm diameter, ≈ 6–7 cm tall.
2. Portion mass estimate
   - Cream desserts ~1 g/ml. 160–220 ml → 150–230 g.
3. kcal bands (per 100 g)
   - Tiramisu-in-cup: 240–330 kcal
   - Chocolate mousse: 300–360 kcal
4. Compute range
   - kcal_low = mass_g × band_low / 100
   - kcal_high = mass_g × band_high / 100
5. Report + one narrowing question
   - Midpoint at 180 g.
   - Ask: coffee/mascarpone vs pure chocolate? Cup volume if known?

## Examples (180 g)
- Tiramisu: 432–594 kcal (mid ≈ 513)
- Mousse: 540–648 kcal (mid ≈ 594)

## Notes
- Biscuit/ladyfinger base: add +20–60 kcal depending thickness.
- Whipped cream above rim: add 10–15% volume.
- Prefer stated cup volume over utensil scaling when available.
