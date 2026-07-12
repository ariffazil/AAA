---
name: wealth-capital-thermodynamics
version: "1.0.0"
description: >
  The 13 capital thermodynamic primitives grounding every WEALTH computation —
  NPV, EMV, EVOI, IRR, runway, entropy delta, and capital flow. Load before any
  multi-primitive WEALTH domain task.
owner: WEALTH / F13 SOVEREIGN
risk_tier: medium
floor_scope: [F1, F2, F4, F7, F11, F13]
autonomy_tier: T2
dependencies:
  mcp_servers: [wealth, arifos]
  tools: [wealth_compute_npv, wealth_compute_emv, wealth_compute_evoi, wealth_compute_irr, wealth_runway_check, arif_judge]
trigger_phrases:
  - multi-primitive capital computation
  - NPV + EMV + EVOI combined
  - runway + risk analysis
  - capital thermodynamics
---
# WEALTH Capital Thermodynamics — Skill

> **Load this skill before any WEALTH capital-domain task that involves
> more than one primitive (NPV + EMV + EVOI, runway + risk, etc.).**
>
> It forces the agent to think in 13 physics primitives over capital
> systems — conservation, flow, gradient, entropy, energy, time, inertia,
> field, signal, game, boundary, hysteresis, survival — instead of
> throwing disjoint tools at the problem.

## Use when

- The task touches capital modelling, portfolio risk, deal framing, or
  scenario weighting and the right tool is not obvious.
- The user mentions NPV, IRR, EMV, EVOI, runway, burn, cashflow, or
  asks for a "complete picture" / "thermodynamic view" / "wisdom
  synthesis".
- You are about to call 2+ WEALTH tools in sequence and need a thinking
  order.
- The task is structural: inequality, capital allocation, sovereign
  resource economics, institutional failure forensics.

## Do not use when

- The task is a single arithmetic call (one tool, one number).
- The task is pure law / pusaka / faraid — use `wealth-law-anthropology`.
- The task is constitutional judgment — use `arif_judge` instead.
- The task is human readiness / fatigue — use `well_validate_vitality`.

## The 13 physics primitives

WEALTH is **capital thermodynamics**. Every public tool maps to one or
more of these primitives. The primitives form a **thinking order** —
do not skip upstream layers or downstream reasoning breaks.

| # | Primitive | Question it answers | Canonical tool(s) | Floor |
|---|-----------|--------------------|--------------------|-------|
| 1 | **Conservation** | Does the balance sheet balance? | `wealth_conservation_check`, `wealth_mass_networth` (internal) | F1 AMANAH |
| 2 | **Flow** | What is the income / expense / burn rate? | `wealth_flow_check`, `wealth_flow_cashflow` (internal) | F1 |
| 3 | **Gradient** | Where is the pressure / differential? | `wealth_pressure_triage` (internal), `wealth_asymmetry_check` | F2 TRUTH |
| 4 | **Entropy** | How much uncertainty / disorder in the system? | `wealth_compute_emv`, `wealth_institutional_entropy_scorer` (internal) | F2 + F7 |
| 5 | **Energy** | How much usable capital per period? | `wealth_compute_irr`, `wealth_energy_irr` (deprecated) | F2 |
| 6 | **Time** | What is the present value of future cash? | `wealth_compute_npv`, `wealth_time_payback` (internal) | F2 + F7 |
| 7 | **Inertia** | How much momentum? What resists change? | `wealth_omni_wisdom` (hysteresis mode), `wealth_density_pi` (internal) | F4 |
| 8 | **Field** | What is the macro context? (FX, commodities, rates) | `wealth_market_data`, `wealth_field_macro` (alias) | F2 |
| 9 | **Signal** | Is new information worth its cost? | `wealth_compute_evoi`, `wealth_signal_evoi` (internal) | F2 + F7 |
| 10 | **Game** | Who else has skin in the game? | `wealth_omni_wisdom` (game mode), `wealth_capture_scan`, `wealth_power_audit`, `wealth_confluence_check` | F2 + F4 |
| 11 | **Boundary** | Where does this system end? What is asymmetric? | `wealth_asymmetry_check`, `wealth_correlation_guard_check` (internal) | F4 |
| 12 | **Hysteresis** | Does the path matter, not just the state? | `wealth_omni_wisdom` (path_params mode) | F4 + F7 |
| 13 | **Survival** | Will the system still be alive at horizon? | `wealth_runway_check`, `wealth_survival_engine` (internal) | F1 + F13 |

## The standard sequence

For any **structural** capital question, walk the primitives in order.
Skip a primitive only with explicit reason; do not skip silently.

```
1. Conservation  → what does the system own / owe?
2. Flow          → how is value moving in / out?
3. Gradient      → where is the pressure differential?
4. Entropy       → how uncertain is the future?
5. Energy + Time → what is the present value of the work?
6. Field         → what is the macro context?
7. Signal        → is new information worth acquiring?
8. Game          → who else is in this game? who captures rent?
9. Boundary      → where does this system end?
10. Hysteresis   → does the path constrain the next state?
11. Survival     → can the system still be here in N years?
12. Inertia      → what will resist change?
13. (loop back to 1 with new state)
```

**Rule:** If you have not run 1–4 you may not run 5+. A discounted cash
flow without a conserved balance sheet is theatre.

## Tool taxonomy (verb namespace)

When forging new WEALTH tools, use the canonical verb:

- `wealth_compute_*` — arithmetic (NPV, IRR, EMV, EVOI)
- `wealth_check_*` — verification (conservation, flow, runway, confluence)
- `wealth_scan_*` — pattern detection (capture, power, collapse)
- `wealth_evaluate_*` — multi-dimensional assessment (wisdom, omni)
- `wealth_audit_*` — adversarial or governance (power, capture)
- `wealth_record_*` / `wealth_query_*` — VAULT999-bound writes/reads

Every tool output should carry:

```yaml
epistemic_tag: OBS | DER | INT | SPEC
verdict: SEAL | HOLD | VOID | NEEDS_DATA
final_authority: Arif
execution_authorized: false    # WEALTH computes, never executes
```

## The wisdom-evaluate call

When the question is "should I do X?", call
`wealth_wisdom_evaluate(proposal, capital_type, context)` first, NOT
NPV. Wisdom evaluates across 6 dimensions:

1. **Dignity impact** — does the move preserve maruah of stakeholders?
2. **Sovereignty effect** — does it reduce or expand sovereign agency?
3. **Resilience** — does it increase or decrease optionality?
4. **Inequality** — who gains disproportionately, who loses?
5. **Ecological cost** — is the resource being depleted unsustainably?
6. **Optionality preservation** — does it foreclose better futures?

**Rule:** If dignity or sovereignty is HIGH risk, return 888_HOLD
regardless of NPV. WEALTH computes, arifOS judges, Arif decides.

## The omni-wisdom call

`wealth_omni_wisdom` orchestrates multiple primitives into one verdict.
Three modes:

- `synthesize` — produce a unified capital recommendation (call after
  1–11 done; do not call cold without context)
- `deal_frame` — full deal analysis (use when given a specific
  transaction; replaces 5 ghost tools per TOOL_SURFACE.md Phase 2)
- `path_params` — hysteresis-aware path dependence (use when prior
  decisions constrain the next move)

Cold-start with `synthesize` returns `HOLD / confidence 0.5` — that
is correct behaviour. Add explicit context, then re-run.

## Capture + power: the audit pair

Before any capital recommendation, run BOTH:

1. `wealth_capture_scan(advice_text, source_model)` — checks the
   advice itself for hidden incentives, false precision, authority
   claims without evidence.
2. `wealth_power_audit(scenario, actors, context)` — checks the
   scenario for incentive asymmetry, capture risk, rent extraction,
   opacity, coercion, rule asymmetry.

Both return `risk_level: LOW/MEDIUM/HIGH/CRITICAL` per dimension. If
either is HIGH or CRITICAL, the recommendation needs 888_HOLD.

## Personal finance vs institutional

- **D1 Personal** (Arif's own books): `wealth_personal_finance`,
  `wealth_runway_check`, `wealth_flow_check`,
  `wealth_conservation_check`, `wealth_vault_*`
- **D3 Macro**: `wealth_market_data`
- **D4 Stock**: `wealth_stock_analysis` (12 modes — verify_math,
  pre_trade, fundamentals, TAC-9, contrast, confluence)
- **Institutional / sovereign** (Petronas, MAS, sovereign wealth):
  `wealth_omni_wisdom`, `wealth_wisdom_evaluate`, `wealth_power_audit`,
  `wealth_collapse_signature_*` (when available)

The skill's primary lens is **institutional / sovereign**. Personal
finance is a degenerate case of the same primitives.

## Hard rules

1. **WEALTH computes. Never allocates.** Any tool that moves money is
   out of scope. See `FEDERATION_CONTRACT.md`.
2. **No phantom numbers.** Every NPV/IRR/EMV output must show the
   input assumptions. No hidden defaults.
3. **No F1 violation.** If the balance sheet doesn't balance, return
   `HOLD — conservation_failed` before any discounted-cash reasoning.
4. **Cap confidence at 0.90.** Per F7 HUMILITY. Even perfect data has
   model error.
5. **No cross-jurisdiction synthesis** without naming each grammar
   (federal / state / syariah / adat / NCR).
6. **HIGH/CRITICAL risk ⇒ 888_HOLD.** Across all primitives, dignity
   is not negotiable.
7. **arifOS judges. WEALTH computes. Arif decides.** No exceptions.

## Failure modes to watch

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `wealth_compute_npv` returns 0 | Cash flow array empty | Validate inputs upstream |
| `wealth_omni_wisdom` returns HOLD / 0.5 | Cold-start, no context | Add explicit `decision_context` + `path_params` |
| `wealth_capture_scan` returns HIGH | Advice text has hidden incentives | Strip the advice, surface the incentives |
| `wealth_power_audit` returns LOW despite asymmetric scenario | Scenario text too neutral | Re-state the scenario with named actors + downside |
| `wealth_stock_analysis` returns NEEDS_DATA | Missing `entry_price` / `current_price` | Check mode requirements per `internal/stock/` |
| `wealth_system_registry_status` returns drift | Tool surface drift | Run `TOOL_SURFACE.md` reconciliation |

## Related skills

- `wealth-law-anthropology` — Malaysian law, pusaka, faraid, KTN
- `geox_basin` — for upstream oil & gas (Petronas context)
- `geox-claim-grammar` — claim discipline that pairs with collapse
  signature work
- `arif_think` (mode=verify) — final epistemic gate before SEAL-grade output
- `333-mind-plan-generate` — multi-step execution graph when analysis spans
  more than 3 primitives
- `forge_health_check` — when WEALTH is down or degraded

## Ditempa Bukan Diberi

Capital thermodynamics is **forged**, not given. The 13 primitives
are not a vocabulary — they are a way of seeing. A capital system
without conservation, flow, entropy, and survival is not a system; it
is a story. Compute honestly, let the sovereign decide.
