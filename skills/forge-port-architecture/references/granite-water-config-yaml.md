# GRANITE vs WATER — Config YAML Annotation Doctrine

Pattern for governance-class config files in the arifOS federation. Emerged 2026-08-12
during cognitive-params.yaml authoring.

## The Doctrine

Every numeric/structural parameter in a federation config file must carry an explicit
**GRANITE** or **WATER** annotation. The two states encode the change authority:

| Tag | Meaning | Authority to change | Audit |
|-----|---------|---------------------|-------|
| 🪨 **GRANITE** | Constitutional — F7 HUMILITY floor, F13 SOVEREIGN bound. | Only F13 SOVEREIGN consent. Locked by design. | VAULT999-sealed on every reference |
| 💧 **WATER** | Empirical / tuned. Runtime calibration expected. | forge_witness W³ feedback loop, C_dark, agent sanity. | Regular drift probe |

## When to apply

- Any YAML file that feeds runtime thresholds (drift caps, memory tiers, decay constants)
- Any config block that the cognitive layer reads at boot
- Anywhere a Python module-level constant is being moved to YAML for self-healing loops

## Concrete markers

```yaml
# 🪨 GRANITE — Epistemic floor: constitutional ceiling. Do NOT change.
confidence_cap: 0.90

# 💧 WATER — Inertia coefficient. Calibrate with runtime feedback.
eta_inertia: 0.50
```

Marker convention: place the emoji + tag in a comment on the **line preceding** the value,
not inline (inline breaks YAML parsers and linters).

## Bootstrap rule

The Python constants stay authoritative until the YAML loader lands. Mirror the YAML into
the Python file's module-level constants so drift between code and config is impossible.
Run a parity check at CI time:

```python
# Python:  CONFIDENCE_CAP: float = 0.90
# YAML:    confidence_cap: 0.90
# Rule:    abs(float(yaml[key]) - python_const) < 1e-9  → pass
```

## Pitfalls

1. **Don't tag something WATER that the F7 floor enforces.** Confidence caps, ceiling
   thresholds, and constitutional floors are always GRANITE — even if "we tuned them once".
2. **Don't tag something GRANITE that has no enforcement path.** A value with no F-floor
   backing it is just WATER with extra ceremony.
3. **Inline tags break parsers.** Keep them in a preceding comment line.
4. **YAML 1.1 vs 1.2 schema_version.** Pin it explicitly. New floor YAMLs use `1.0.1` or later.

## Reference impl

- `/root/HERMES/config/cognitive-params.yaml` — canonical example (F7 HUMILITY domain)
- Loaded by: `/root/HERMES/cognitive/config.py` at boot
- 7 GRANITE tags, 9 WATER tags across 6 threshold params + 2 dict blocks
