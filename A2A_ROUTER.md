# A2A ROUTER — Where to go for what

> Written 2026-10-01 by FI-008. 4 sibling A2A paths exist in this repo. They are NOT redundant. Each has one job. This doc maps intent → path.

## TL;DR

| If you want to… | Go to |
|---|---|
| **Run** the production agent card endpoint + task router | `/root/AAA/a2a-server/` (Node.js · port 3001) |
| **Read** the A2A protocol specs, treaties, agent cards, peer contracts, mesh topology | `/root/AAA/a2a/` (docs/spec layer, not runtime) |
| **Use** the Python constitutional wrapper around the official `a2a-sdk` (alpha — F1-F13 enforcement) | `/root/AAA/aaa-a2a/` (Python ≥ 3.13 · v0.1.0a2 · wraps port 3001) |
| **Read** the constitutional role definitions for the 3 numeric tiers (333-AGI Composer, 555-ASI Auditor, 888-APEX Governor) | `/root/AAA/aaa/{333,555,888}/ROLE.md` |

## Layer map

```
┌─────────────────────────────────────────────────────────────┐
│  /root/AAA/a2a/                DOCS / SPECS LAYER           │
│  ├── A2A_ALIGNMENT_SPEC.md                                  │
│  ├── AAA_TREATY.md                                          │
│  ├── APEX-ZEN-A2A-MASTER-SPEC.md                            │
│  ├── agent-card.json · agent-cards/                         │
│  ├── peer-contracts/ · policies/                            │
│  ├── mesh-topology-static.json                              │
│  └── convergence_receipt_2026-09-13.json                   │
└─────────────────────────────────────────────────────────────┘
                              ↑ spec consumed by ↓
┌─────────────────────────────────────────────────────────────┐
│  /root/AAA/a2a-server/        PRODUCTION RUNTIME            │
│  Express server · port 3001                                 │
│  Serves https://aaa.arif-fazil.com agent card endpoint      │
│  Implements task routing + live protocol                    │
└─────────────────────────────────────────────────────────────┘
                              ↑ wraps with F1-F13 ↓
┌─────────────────────────────────────────────────────────────┐
│  /root/AAA/aaa-a2a/           PYTHON CONSTITUTIONAL WRAPPER  │
│  alpha · v0.1.0a2 · Python ≥ 3.13                           │
│  Wraps official a2a-sdk with floor enforcement              │
│  Not yet production. Read `aaa-a2a/README.md` before use.  │
└─────────────────────────────────────────────────────────────┘

      Orthogonal to all 3 (constitutional role definitions):
┌─────────────────────────────────────────────────────────────┐
│  /root/AAA/aaa/333/ROLE.md      333-AGI  — Composer         │
│  /root/AAA/aaa/555/ROLE.md      555-ASI  — Auditor          │
│  /root/AAA/aaa/888/ROLE.md      888-APEX — Governor         │
└─────────────────────────────────────────────────────────────┘
```

## Common pitfalls (read first)

- **Don't import from `a2a-server/` in Python code** — it's Node.js. Use `aaa-a2a/` if you need Python.
- **Don't treat `a2a/` agent-card.json as the live agent card** — `a2a-server/` serves the live one. `a2a/agent-card.json` is the spec/contract source.
- **Don't edit `a2a-server/server.js` without reading `a2a/AAA_TREATY.md` first** — the spec layer defines invariants the runtime must honor.
- **`aaa-a2a/` is alpha** — F1-F13 enforcement may not be complete. Cross-check with `a2a-server/` behavior before relying on it for production paths.

## Status of each path (2026-10-01)

| Path | Status | Owner |
|---|---|---|
| `a2a-server/` | Production · live | HERMES lane |
| `a2a/` | Spec source · mostly frozen | Constitutional |
| `aaa-a2a/` | Alpha · not production | Constitutional port effort |
| `aaa/{333,555,888}/` | Ratified role defs · frozen | Constitutional |

## When this router is wrong

If you find that two of these paths actually do the same job, this doc is wrong. Edit it. The fact that there are 4 paths is a feature if their roles are clean, a bug if they're redundant. The bar is: every path has a distinct job, no path is dead.