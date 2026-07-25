# Contributing to AAA

> **SOT:** 2026-07-25 | **DITEMPA BUKAN DIBERI**

AAA is the cockpit and A2A mesh hub of the arifOS Federation. It routes, displays, and registers agents — it never judges or executes.

## Before You Start

1. Read the [README](README.md) — understand what AAA IS and IS NOT
2. Understand the agent lanes: 333-AGI, 555-ASI, 888-APEX, 777-forge
3. Read [CLAUDE.md](CLAUDE.md) — agent doctrine

## Setup

```bash
git clone git@github.com:ariffazil/AAA.git && cd AAA
npm install && npm run build
npm run a2a:server          # dev A2A gateway
```

## Making Changes

1. **Fork → Branch → Edit → Test → PR**
2. Run `npm test` before pushing (lint + build + security + stabilization)
3. Run `npm run validate:aaa` for agent card validation

## Boundaries

- AAA routes and displays — never adjudicates (arifOS does that)
- AAA registers agents — never executes (A-FORGE does that)
- No agent self-authorization
- Respect the Zen 99 skill cap

## Federation

AAA is one of 7 organs. See [ariffazil/ariffazil](https://github.com/ariffazil/ariffazil) for the federation map.

---

*Maintained under F13 SOVEREIGN by Muhammad Arif bin Fazil.*
