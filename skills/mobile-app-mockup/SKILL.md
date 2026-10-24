---
name: mobile-app-mockup
description: Mock up mobile app screens as PNG from HTML.
version: 1.0.0
---

# Mobile App Mockup (HTML -> PNG)

Produce a phone-screen mockup image for app concepts (device status, reports, dashboards) without a design tool.

## Procedure

1. Write one self-contained HTML file in `/tmp/`. No external fonts or CDNs - headless Chrome must render it offline.
2. Render:
   ```bash
   google-chrome --headless=new --disable-gpu --no-sandbox --screenshot=out.png \
     --window-size=430,900 --hide-scrollbars file:///tmp/out.html
   ```
   The dbus/UPower warning on stderr is noise; success is the `NNNN bytes written to file` line.
3. Check size (`ls -la out.png`) and `vision_analyze` the PNG for clipping, overlap, or a half-rendered frame before sending.
4. Deliver with `MEDIA:/tmp/out.png`.

## Phone frame that renders correctly

- Body: dark page background (`#1a1a2e`), flex centre, `min-height: 100vh`, `padding: 20px`.
- Frame: `width: 390px`, `background: #0f0f1f`, `border-radius: 42px`, `padding: 14px`, soft drop shadow.
- Screen: `background: #f5f6fa`, `border-radius: 30px`, `overflow: hidden`.
- Status bar: time on the left, `🔋 NN%` on the right, 13px semibold.
- Header band: gradient (`linear-gradient(135deg, #15803d, #16a34a)` for operational, `#0c4a6e -> #0284c7` for reporting), white text, greeting + title + subtitle.
- Cards: white, `border-radius: 18px`, `box-shadow: 0 4px 16px rgba(0,0,0,0.06)`.
- Metric rows: icon chip (34x34 rounded), label 13px grey, value 16px bold.

## Content conventions

- Keep one value per row: Date, Time, Location, then the highlighted metric in its own tinted banner.
- A **live status screen** shows a snapshot (one date, one time, one reading). A date RANGE with a single reading is incoherent: "18 Sep - 30 Sep, 6°C" implies the machine held one value for 13 days with no timestamp. Range belongs in a **history/report** screen, where the reading is min/max/avg over the period.
- For a temperature report, a healthy machine holds its set point: draw a **flat line at the set point**, not a wobble inside the safe band. Showing fluctuation inside 2-8°C reads as "the machine is misbehaving", which is the opposite of the intent.
- Bottom nav icons are usually unwanted - the user has asked for them removed. Omit unless requested.

## Iteration

Edits are almost always small text or date swaps. Use `sed -i` on the HTML then re-render, rather than rewriting the file:

```bash
sed -i 's/5:00 PM/7:00 PM/g; s/92%/82%/g; s/18 Sep 2026/1 Oct 2026/g' /tmp/out.html
```

When the range changes, the x-axis day labels must change with it - a sed on the date text alone leaves the old day numbers in the SVG.

## Inline SVG charts

For a small chart inside a phone card, an inline `<svg viewBox="0 0 320 180">` with hand-placed `<line>`/`<circle>` beats embedding an image: it scales crisply and stays editable via sed. Keep grid lines light (`#e2e8f0`), axis labels 8-9px `#64748b`.
