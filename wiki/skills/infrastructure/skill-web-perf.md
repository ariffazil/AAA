---
title: "Skill: Web Performance Audit"
created: 2026-05-17
updated: 2026-05-17
version: 1.0.0
type: skill
category: infrastructure
tags: [web-perf, lighthouse, core-web-vitals, lcp, inp, cls, fcp, tbt, chrome-devtools, audit]
confidence: high
contested: false
floors: [F7, F8]
risk_band: LOW
sources: [/root/.agents/skills/web-perf/SKILL.md]
---

# Skill: Web Performance Audit

> **Source:** `/root/.agents/skills/web-perf/SKILL.md`
> **Agent:** OpenCode / Kimi
> **Forged:** 2026-05-17

---

## Trigger Conditions

Load this skill when the task involves:
- Auditing page load performance
- Debugging Lighthouse scores
- Optimizing Core Web Vitals
- Identifying render-blocking resources or layout shifts
- Keywords: performance, lighthouse, lcp, cls, inp, audit, speed, web-vitals

---

## Doctrine

Performance is user experience. A slow site is a broken site.

---

## Core Web Vitals Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| FCP (First Contentful Paint) | ≤ 1.8s | ≤ 3.0s | > 3.0s |
| TBT (Total Blocking Time) | ≤ 200ms | ≤ 600ms | > 600ms |

---

## Common Fixes

| Problem | Fix |
|---------|-----|
| Render-blocking CSS | Inline critical CSS, defer non-critical |
| Large JS bundles | Code split, tree-shake, use dynamic imports |
| Unoptimized images | WebP/AVIF, responsive images, lazy load |
| Layout shifts | Set explicit width/height on images, ads |
| Slow server response | Edge caching, CDN, optimize TTFB |

---

## Related

- [[skill-frontend-design]] — UI/UX construction
- [[skill-cloudflare]] — Edge caching and optimization

---

*DITEMPA BUKAN DIBERI — Performance is a feature, not an optimization.*
