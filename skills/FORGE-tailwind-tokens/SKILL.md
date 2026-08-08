---
id: FORGE-tailwind-tokens
name: FORGE-tailwind-tokens
version: 1.0.0-2026.07.17
description: "Tailwind design tokens — Trinity Design System for federation cockpit and web surfaces."
owner: A-FORGE
risk_tier: low
floor_scope: ['F1', 'F4']
autonomy_tier: T1
---
# ⚒️ Tailwind Tokens — Trinity Design System

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Purpose
Maintain Tailwind CSS configuration aligned with Trinity design tokens: federation colour palette, organ-specific accents, dark theme, CSS variable bridge for dynamic theming.

## When to Use
- Setting up or modifying `tailwind.config.{ts,js}` for any federation surface
- Defining colour tokens, spacing scale, typography, breakpoints
- Dark theme implementation — `class` strategy, CSS variable integration
- Organ-specific theming (arifOS amber, GEOX teal, WEALTH gold, WELL violet)

## When NOT to Use
- Component-level styling decisions — use TW utility classes directly
- Animation/keyframe definitions — belong in CSS, not token config
- Runtime theme switching outside the Trinity design seam contract

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Token renames must be staged; deprecated tokens kept as aliases for one cycle |
| F2 TRUTH | Token values in config must match design spec; no drift between figma → config |
| F4 CLARITY | Max 3 grey neutrals, 5 colour steps per hue — no infinite token explosion |
| F6 MARUAH | Colour contrast meets WCAG AA minimum; dignity in readability |
| F13 SOVEREIGN | Brand colours (primary, accent) approved by Arif before deploy |

## Commands & Patterns

```ts
// tailwind.config.ts — Trinity token structure
colors: {
  midnight: { 50: '...', 900: '...' },    // base neutral
  forge:    { 500: '#f59e0b', ... },        // amber — action
  geox:     { 500: '#14b8a6', ... },        // teal — earth
  wealth:   { 500: '#fbbf24', ... },        // gold — capital
  well:     { 500: '#8b5cf6', ... },        // violet — human
  sovereign:{ 500: '#ef4444', ... },        // red — veto
}

// CSS variable bridge for dynamic theming
:root { --color-forge: theme('colors.forge.500'); }

// Dark theme — class strategy
darkMode: 'class',
// Usage: <html class="dark"> or <ThemeToggle />
```

## Refusal Surface
- ❌ Inline styles or `style={}` for anything themable via token
- ❌ Hex values outside the token config (no colour literals in components)
- ❌ Removing deprecated tokens without alias fallback
- ❌ RGB/HSL values that lack WCAG AA contrast verification
