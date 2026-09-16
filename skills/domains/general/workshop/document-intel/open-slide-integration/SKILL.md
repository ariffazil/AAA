---
name: open-slide-integration
description: "Agentic slide/PDF authoring patterns from open-slide."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [open-slide, agentic-authoring, presentations, design-system, staged-reveals, scoping-protocol]
    category: creative
    related_skills: [powerpoint, scientific-pdf-generation, civic-intelligence-pdf]
---

# Open-Slide Integration — Agentic Authoring Runtime

> **DITEMPA BUKAN DIBERI** — Extracted from open-slide framework (github.com/1weiho/open-slide).
> **Source:** 2026-08-25 repo ingest, 593 files, React/Vite/TypeScript stack.

Use when: generating presentations, PDFs, dashboards, or any visual artifact. Six distillation patterns from a production agent-native slide framework.

## When to Use

- Generating any visual artifact (PDF, slides, dashboard) from structured content.
- Designing agent-authored presentations where the agent writes the source.
- Building artifacts that need live-tweakable design tokens or budget discipline.
- Wiring async agent edits via in-source markers.
- NOT for reading/extracting from existing PDFs (use `ocr-and-documents`).

## The 6 Eurekas

### Eureka 1 — Skills as Package Artifacts

open-slide ships skills inside the npm package (`packages/core/skills/`), declared in `"files"` so skills travel with the package. Consumer installs, skills auto-available.

**Pattern for arifOS:** Domain packages bundle their own skills. `geox-seismic-ingest` ships with `@geox/core`, `wealth-ledger-write` with `@wealth/ledger`. Install package, skills follow. No centralized registry clone needed.

### Eureka 2 — Inspector Comment Markers (Async Agent Edits)

User clicks element in browser, attaches comment, persisted as in-source markers:

```jsx
{/* @slide-comment id="c-a1b2c3" ts="2026-08-25T12:00:00Z" text="base64url(JSON)" */}
```

Agent later parses markers, applies edits, deletes markers. No external task tracker.

**Pattern for arifOS — `@agent-task` markers:**
```
{/* @agent-task id="t-xxx" text="base64url(JSON{task, priority, context})" */}
```
Agent scans, finds, executes, deletes. Apply in reverse line order so line numbers stay valid.

```python
import base64, json, re
MARKER_RE = r'\{/\*\s*@agent-task\s+id="(t-[a-f0-9]+)"\s+text="([A-Za-z0-9_-]+={0,2})"\s*\*/\}'

def parse_task_markers(source):
    tasks = []
    for m in re.finditer(MARKER_RE, source):
        task_id, b64 = m.groups()
        payload = json.loads(base64.b64decode(b64.replace('-', '+').replace('_', '/') + '=' * (-len(b64) % 4)))
        tasks.append({'id': task_id, **payload})
    return tasks
```

### Eureka 3 — Design System with CSS Variables (Live Tweaking)

```tsx
export const design = {
  palette: { bg: '#0f172a', text: '#f8fafc', accent: '#fbbf24' },
  typeScale: { hero: 180, body: 40 },
  radius: 12,
};
// Consumption: style={{ background: 'var(--osd-bg)' }}
```

Design panel writes CSS vars live during slider drag; file commit happens on save. Two surfaces: `var(--osd-X)` for live CSS, `design.X` for JS arithmetic.

**Pattern for arifOS:** Any UI-heavy artifact exposes tweakable tokens as CSS vars. User adjusts, agent reads back, persists.

### Eureka 4 — Fixed Canvas Discipline

Fixed 1920x1080 canvas. No scroll. Cropped content is gone. The vertical budget is calculated BEFORE writing:

```
Usable height = 1080 - 2*padding
Element height = font_size * line_height * lines
Sum(elements + gaps) <= usable
```

**Rules:** one idea per page. Max ~40 words. Near budget = split page, never shrink type below scale floor. No `overflow` escape hatch.

**Pattern for arifOS:** All artifact generation calculates budget first. PDF: max ~2000 chars/page. Slide: max ~40 words/slide.

```python
def check_budget(elements, canvas_h=1080, padding=120):
    usable = canvas_h - 2 * padding
    total = sum(e['font'] * e['lh'] * e['lines'] + e.get('gap', 0) for e in elements)
    return total <= usable, usable - total
```

### Eureka 5 — Steps + Morph Primitives (Staged Reveals)

**Steps:** wrap deferred parts in `<Step>`, group in `<Steps>`. Each navigation beat reveals next. Use when order of ideas is the point — not reflexively.

**Morph:** same element `id` on two adjacent pages + `morph` on transition = Magic Move interpolation. For state continuity only, never decoration.

**Hard rules:** `<Step>` must be direct child of `<Steps>` (silent fail otherwise). Page must read complete when jumped to. One motion DNA per deck, 140-280ms, under 12px/3% magnitude.

**Pattern for arifOS:** Extend `powerpoint` skill with reveal declarations. python-pptx can add entrance animations via `animation` XML. Or export to open-slide React format for full fidelity.

### Eureka 6 — Agent-Native Scoping Protocol (4 Questions)

Before writing ANY code, lock 4 decisions:

1. **Aesthetic direction** — 3 topic-tailored options, not generic presets. Each option = vibe word + concrete visual cue. Mark one "(Recommended)".
2. **Page count** — 3-5 short / 6-10 standard / 11-20 deep.
3. **Text density** — minimal / light / standard / dense. Drives type scale and layout.
4. **Motion** — static / subtle / rich.

Rules: ask all before writing. Skip only when already answered — restate assumption. Don't pad with follow-ups already answered. Thin prompt = ask topic FIRST.

**Scope map for arifOS:**

| Skill | Questions |
|-------|-----------|
| powerpoint | aesthetic, page_count, text_density, motion |
| scientific-pdf | mode (A/B/C/D/E), page_count, figure_count, epistemic strictness |
| civic-intelligence-pdf | color_scheme, signal_density, epistemic, audience |
| xlsx | structure, formula_depth, chart_count, delivery_format |

## Integration Checklist

Every visual artifact (PDF, slides, dashboard):

1. **Scope first** — 4-question protocol before writing code.
2. **Budget check** — calculate content fit before rendering. Near budget = split.
3. **Design tokens** — expose tweakable values as CSS variables where possible.
4. **Staged reveals** — use Steps/Morph when order matters. Never reflexively.
5. **Task markers** — leave `@agent-task` markers for async follow-up edits.
6. **Component not map** — visually repeated elements are explicit instances, not `array.map`. Inspector/agent must target each individually.

## Self-Review Before Finishing

- [ ] Scoped via 4-question protocol (or restated assumptions)
- [ ] Budget calculated, every page fits
- [ ] One coherent visual direction across all pages
- [ ] One idea per page, max ~40 words per slide
- [ ] Repeated elements are explicit instances, not data maps
- [ ] All assets exist on disk
- [ ] No overflow escape hatches

## Constitutional Assessment

| arifOS organ | Eureka |
|-------|--------|
| 111 SENSE | Skills as package artifacts = distributed perception |
| 333 THINK | Scoping protocol = structured reasoning before action |
| 555 VERIFY | Budget discipline = falsification before render |
| 777 FORGE | In-source markers = execution primitive |
| 888 JUDGE | CSS variables = user authority over aesthetics |
| 999 WITNESS | Design system = provenance trail for visual decisions |

## Pitfalls

- open-slide requires Node 18+ and pnpm. Hermes VPS may not have these. Check `node --version` before attempting live open-slide runs. The PATTERNS are portable; the RUNTIME may not be installed.
- The skills in this repo are Claude Code skills (`.claude/skills/` format). The principles apply to Hermes skills; the trigger/description format differs.
- Morph transitions in open-slide have 7 hard rules (opacity-only enter/exit, deterministic geometry, no transform on morph node, useIsActivePage gating). Violating any produces visibly broken morphs. Apply all 7 before implementing.
- PowerPoint (python-pptx) animation XML is verbose and error-prone. For simple staggered reveals, exporting to open-slide React format is cleaner. For PowerPoint-only delivery, use LibreOffice render to verify animations look right.

## References

- open-slide: https://github.com/1weiho/open-slide (MIT, Yiwei Ho)
- Local clone: /tmp/open-slide-audit/open-slide (2026-08-25, shallow)
- Core skills: packages/core/skills/{create-slide,slide-authoring,apply-comments,current-slide,create-theme}
- Design system ref: packages/core/skills/slide-authoring/references/design-system.md

---

*Forged: 2026-08-25 from open-slide repo ingest (593 files)*
*DITEMPA BUKAN DIBERI — Agentic authoring runtime patterns*
