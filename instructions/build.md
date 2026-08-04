# Build, test, deploy

## Tech stack

| Layer | Stack |
|---|---|
| **Python (arifOS)** | Python ≥ 3.12, < 3.15. Ruff (line 100), mypy strict, absolute imports, `pyproject.toml` driven. Pydantic 2, FastMCP 3.4.4, Streamable-HTTP MCP. `uv` for venv. |
| **Python (GEOX)** | Python ≥ 3.11. Ruff (line 130). Geoscience stack: `numpy`, `scipy`, `lasio`, `welly`, `segpy`, `obspy`, `bruges`, `pylops`, `scikit-learn`. |
| **Python (WEALTH)** | Python ≥ 3.12. Capital stack: `numpy-financial`, `pydantic-ai`, `langgraph`, `psycopg`, `polars`, `duckdb`, `pyportfolioopt`, `quantlib`, `riskfolio-lib`, `yfinance`. |
| **Python (WELL)** | Python ≥ 3.12. Minimal surface: FastMCP, Pydantic, httpx. |
| **TypeScript / Node (A-FORGE)** | Node ≥ 22, TypeScript 6.0+, ESLint 10, ESM (`"type": "module"`), NodeNext ESM with explicit `.js` extensions, Zod ~3.25. |
| **TypeScript / Node (AAA)** | Node ≥ 22, Vite 8, React 19, Tailwind 4, Radix UI, shadcn/ui. |
| **Docker** | Organs run **bare-metal systemd**. Supporting services run in Docker. **Do NOT containerize core organs.** |
| **Reverse proxy** | Caddy on 80/443; Cloudflare Tunnel as the only public ingress. |

## Per-organ commands

| Organ | Source | Runtime | Install | Test | Deploy |
|---|---|---|---|---|---|
| **arifOS** | `/root/arifOS` | `/opt/arifos/app` | `uv sync --frozen` | `pytest tests/ -q --tb=short` | `make deploy-local` |
| **A-FORGE** | `/root/A-FORGE` | `/opt/a-forge/app` | `npm install && npm run build` | `npm test` | `make deploy` |
| **AAA** | `/root/AAA` | process | `npm install && npm run build` | `npm run lint && npm test` | `systemctl restart aaa-a2a` |
| **GEOX** | `/root/GEOX` | process | `pip install -e ".[dev]"` | `PYTHONPATH=src pytest tests/ -q` | `systemctl restart geox-mcp` |
| **WEALTH** | `/root/WEALTH` | process | `pip install -e ".[dev]"` | `pytest tests/ -q` | `systemctl restart wealth-organ` |
| **WELL** | `/root/WELL` | process | `pip install -e .` | `pytest tests/ -q` | `systemctl restart well` |

## Root aggregator

```bash
make prove             # full proof pack (per-organ)
make health            # port sweep (per-organ)
make sot-check         # source-of-truth drift
make security-audit    # per-organ security scanners
make vault999-verify   # VAULT999 chain integrity
make scorecard         # federation scorecard
```

## Commit / branch / tag discipline

- **Commits:** Conventional (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`).
- **Branches:** `main` is production. Feature branches. Git-first deploy.
- **Tags:** `vYYYY.MM.DD` ONLY (Iron Rule). The forge date is the version.
- **SOT-MANIFEST:** every pointer doc carries the SOT block; `make forge` bumps it.

## Code style

- **Python (arifOS):** Ruff (line 100), mypy strict, absolute imports. Python ≥ 3.12, < 3.15.
- **Python (GEOX):** Ruff (line 130). Python ≥ 3.11.
- **TypeScript / Node:** ESLint 10, Node ≥ 22, ES modules, NodeNext ESM with explicit `.js` extensions.
- **Epistemic tags:** `CLAIM` · `PLAUSIBLE` · `HYPOTHESIS` · `ESTIMATE` · `UNKNOWN` mandatory on substantive claims. F2 binding.
- **Dynamic-State:** T₀ observation is evidence only for T₀. Re-probe at T₁ before any irreversible action.
- **F6 dual-register:** kernel/audit surfaces emit **MARUAH**; public/UI surfaces emit **EMPATHY**.
- **F2 dual-register:** kernel evidence keeps label form (`OBS`/`DER`/`INT`/`SPEC`); briefing chips render band form.

## Health & recovery

```bash
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083 arifflow:7073; do
  curl -sf "http://localhost:${svc##*:}/health" >/dev/null 2>&1 \
    && echo "✅ ${svc%%:*}" || echo "❌ ${svc%%:*}"
done
```

Restart policy: T1 single service · T2 multi-service · T3 federation restart requires **888_HOLD**.

**Unified doctor:** `/root/scripts/doctor.sh` — single-command federation health dashboard.
