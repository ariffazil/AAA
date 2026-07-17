---
name: region-contract
description: Archived monolith-edit region contract retained for audit provenance. Do not use as the active editing workflow; use the current spatial or visual verification skill for region-preserving page changes.
---

# REGION-CONTRACT — Monolith Edit Guard

> **DITEMPA BUKAN DIBERI** — Forged, not given.

## Purpose
Prevent monolith rewrites that destroy regions. Every page with 3+ sections MUST declare `data-region` attributes. Edits touch ONE region only.

## The Law

### Every page with 3+ sections declares regions:
```html
<div data-region="header">...</div>
<div data-region="chart">...</div>
<div data-region="decision">...</div>
<div data-region="nav">...</div>
<div data-region="footer">...</div>
```

### Before ANY edit:
1. **Inventory**: List all `data-region` attributes in the target file
2. **Identify**: Which region(s) does this edit touch?
3. **Protect**: All OTHER regions must remain byte-identical
4. **Verify**: After edit, confirm all regions still present

### After ANY edit:
```bash
# Region presence test — must pass or deploy is VOID
for region in header chart decision nav footer; do
  grep -q "data-region=\"$region\"" target.html || echo "❌ REGION $region MISSING — DEPLOY VOID"
done
```

### Forbidden patterns:
- ❌ `write entire_file.html` when only one region changes
- ❌ `cat > file.html << 'EOF'` (heredoc = monolith rewrite)
- ❌ Any edit that changes more than one `data-region` block

### Required patterns:
- ✅ `edit` tool targeting specific region content
- ✅ `patch` with exact old_string → new_string for one region
- ✅ Diff output showing only ONE region changed

## Gold Chart Regions (canonical)
| Region | data-region | Content |
|--------|-------------|---------|
| Header | `header` | Topbar, price, RSI, EMA, signal badge |
| Chart | `chart` | Candlestick + RSI strip |
| Decision | `decision` | R:R bar, Context narrative, Support/Resistance/Confluence |
| Timeframe | `timeframe` | 1H/4H/1D/1W/1M buttons |
| Footer | `footer` | Federation nav + copyright |

## Wealth Dashboard Regions (canonical)
| Region | data-region | Content |
|--------|-------------|---------|
| Topbar | `topbar` | Brand, nav links |
| Ticker | `ticker` | 7-asset price bar |
| Detail | `detail` | Asset info, signal, chart link |
| Sidebar | `sidebar` | Briefing, stats, federation links |
| Footer | `footer` | Federation + ecosystem links |

## Enforcement
- CI gate: `grep -c 'data-region=' page.html` must equal expected count
- Deploy gate: all expected regions present
- Any missing region → VOID verdict, no deploy
