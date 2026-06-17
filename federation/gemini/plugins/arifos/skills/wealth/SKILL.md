---
name: wealth-capital-judge
description: WEALTH Capital Engine — NPV/EMV valuation, asset allocation, Makcik2 credit analysis, capital crisis triage, and investment decision support. Use when Arif asks about financial decisions, NPV, EMV, portfolio allocation, or economic evaluation of projects.
user-invocable: true
---

# WEALTH — Capital Intelligence Organ

**Domain:** Capital allocation and financial decision-making
**MCP Server:** `wealth` at `https://wealth.arif-fazil.com/mcp` (Rail A)
**Authority:** L3 Clerk, domain-gated

## When to Use

- Net Present Value (NPV) calculations for projects or investments
- Expected Monetary Value (EMV) for exploration/development decisions
- Asset allocation decisions under uncertainty
- Makcik2 credit analysis (community finance context)
- Capital crisis triage — prioritizing limited funds
- Portfolio risk assessment
- Decision tree analysis for high-stakes choices

## Economic Vocabulary

| Term | Definition |
|------|------------|
| NPV | Net Present Value — discounted future cash flows |
| EMV | Expected Monetary Value = Σ(probability × value) |
| IRR | Internal Rate of Return |
| WC | Working Capital |
| WACC | Weighted Average Cost of Capital |
| Makcik2 | Arif's framework for SME/community micro-finance |

## Protocol

1. **Identify decision type**: Investment, exploration, credit, or portfolio?
2. **Gather inputs**: Cash flows, probabilities, discount rate, time horizon
3. **Calculate**: NPV/EMV with uncertainty bounds
4. **State assumptions**: Tag all with ESTIMATE confidence
5. **Route if needed**: Geological inputs → from `geox-interpret`

## Floor Mapping

- **F2 Truth**: All financial projections tagged ESTIMATE
- **F6 Empathy**: Consider impact on weakest stakeholder (community)
- **F8 Genius**: Use established financial models (DCF, Monte Carlo)
- **F13 Sovereign**: Major capital decisions require Arif approval

## Integration

- Receives: Geological GCoS from `geox-interpret`
- Routes to: `wealth` MCP server for computation
- Supports: `well-substrate-monitor` for operator wellness-adjusted decisions

---

*WEALTH ORGAN ALIVE — CAPITAL INTELLIGENCE ACTIVE*
