# Nasi Lemak Analytics Dashboard Pattern

> Deployed: 2026-08-26 at `https://syedos.arif-fazil.com/nasilemak/analytics.html`

## Tech Stack

- **Self-contained HTML** — Chart.js from CDN, inline CSS/JS, no build step
- **Dark theme** — `#0a0a0f` background, `#f0a500` gold accent, `#12121a` card bg
- **Chart.js 4.4.7** — bar charts for daily volume, line charts for trends
- **Custom CSS bars** — for location/variant breakdown (more control than Chart.js)
- **Mobile responsive** — `grid-template-columns: repeat(2,1fr)` on small screens

## File Structure

```
/var/www/html/syedos/nasilemak/
├── index.html          # Original dashboard (sample data only)
└── analytics.html      # Real analytics dashboard (31 orders)
```

## Deployment

```bash
cp /root/sado/data/nasi_lemak_analytics_v2.html \
   /var/www/html/syedos/nasilemak/analytics.html
```

## Dashboard Sections

### 1. Hero Stats (4 cards)
- Total Units
- Avg / Order
- Est. Monthly Profit (RM9,640)
- Berlauk Risk (RM116/mo @10%)

### 2. Location Rules Box
- Green tags: berlauk-allowed locations
- Red tags: telur-only locations (no berlauk)
- Shows volume breakdown (44% telur-only, 56% berlauk-eligible)

### 3. Variant Economics Table
- All 4 variants with cost/sell/margin/waste risk
- Color-coded waste risk (green = free, red = covers)

### 4. Daily Order Volume Chart
- Bar chart, all 26 orders
- Event days highlighted purple
- X-axis: dates, Y-axis: units

### 5. Location Breakdown + Day-of-Week Pattern
- Side-by-side cards
- Location bars with color coding + ✅/🚫 berlauk indicator
- DOW average bars (Isnin–Ahad)

### 6. Weekly Growth Trend
- Line chart, weekly totals
- Shows business growth trajectory

### 7. Variant Demand Bars
- Estimated split: rebus 53%, mata 18%, dadar 9%, berlauk 9%, other 11%
- Color-coded by variant

### 8. Berlauk Waste Risk Model Table
- Waste % scenarios (5%, 10%, 20%, 30%)
- Loss per day + monthly loss
- Color-coded by severity

### 9. Order History Table
- All 31 orders with date, day, total, est. revenue, est. profit, event tag

### 10. Optimization Insights
- 6 key insights with icons
- Location rules, berlauk cap, event opportunity, etc.

## Chart.js Config Pattern

```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: orders.map(o => o.date.slice(5)),
    datasets: [{
      label: 'Units',
      data: orders.map(o => o.total),
      backgroundColor: orders.map(o => o.ev ? 'rgba(168,85,247,.7)' : 'rgba(240,165,0,.6)'),
      borderColor: orders.map(o => o.ev ? '#a855f7' : '#f0a500'),
      borderWidth: 1, borderRadius: 3
    }]
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: '#6b7280', font: { size: 10 } }, grid: { display: false } },
      y: { ticks: { color: '#6b7280' }, grid: { color: '#1e1e30' } }
    }
  }
});
```

## Custom CSS Bar Pattern

```css
.bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.bar-label { width: 100px; font-size: 11px; text-align: right; flex-shrink: 0; }
.bar-track { flex: 1; height: 20px; background: #1e1e30; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; display: flex; align-items: center; padding-left: 6px; font-size: 10px; color: #fff; font-weight: 600; }
.bar-val { font-size: 11px; width: 50px; text-align: right; flex-shrink: 0; }
```

## Color Palette

| Element | Color | Hex |
|---|---|---|
| Background | Black | `#0a0a0f` |
| Card bg | Dark gray | `#12121a` |
| Border | Dark blue-gray | `#1e1e30` |
| Gold accent | Gold | `#f0a500` |
| Success | Green | `#22c55e` |
| Warning | Orange | `#f59e0b` |
| Error | Red | `#ef4444` |
| Event/Premium | Purple | `#a855f7` |
| Telur-only | Blue | `#3b82f6` |
| LRT locations | Green | `#10b981` |
| EVEN/Events | Pink | `#ec4899` |

## Update Workflow

When new chat data arrives:
1. Extract ZIP → `_chat.txt`
2. Run Python parser → JSON
3. Update `orders` array in HTML
4. Copy to `/var/www/html/syedos/nasilemak/analytics.html`
5. Verify with `curl -sk https://syedos.arif-fazil.com/nasilemak/analytics.html`