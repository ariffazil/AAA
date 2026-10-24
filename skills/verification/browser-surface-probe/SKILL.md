---
name: browser-surface-probe
description: "Use when a live page must be render-verified in a browser."
triggers:
  - "verify the page renders"
  - "measure the DOM"
  - "check images load on the live site"
  - "mobile overflow"
  - "blank space on the page"
  - "screenshot at the anchor"
  - "render matrix"
---

# Browser Surface Probe

Measuring what a live page actually renders in a browser — images, layout, anchors, overflow —
where curl and HTML source cannot answer. Companion to `rendered-surface-verification`
(which-file/lane/template questions) and `verify-before-report` (did the deploy land). This skill
owns the measurement recipes.

## Render matrix (images/logos)

An `<img src>` tag present proves wiring, not rendering. For every image record:
`naturalWidth`/`naturalHeight` (0 = failed or never loaded), rendered
`getBoundingClientRect()` size, computed `visibility`/`display`, and `complete`.

```js
(() => {
  const rows = [];
  document.querySelectorAll('img').forEach(img => {
    const cs = getComputedStyle(img);
    const r = img.getBoundingClientRect();
    rows.push({src: img.getAttribute('src'), complete: img.complete,
      natW: img.naturalWidth, natH: img.naturalHeight,
      rendW: Math.round(r.width), rendH: Math.round(r.height),
      vis: cs.visibility === 'visible' && cs.display !== 'none' ? 'VISIBLE' : 'HIDDEN'});
  });
  return JSON.stringify(rows);
})()
```

**Force-eager lazy images before measuring.** `loading="lazy"` images report `naturalWidth 0` and
`complete: false` until scrolled near — every below-fold image reads as "broken" without running
`document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading="eager")` and waiting
first.

## Cache discipline after a CSS repair

A deployed fix can look failed because the test browser or an edge serves the old HTML:

1. Confirm the served copy carries the fix: curl the live URL and grep for the new rule/attribute.
2. In the browser, walk `document.styleSheets` for the new rule text.
3. `CF-Cache-Status: DYNAMIC` on the response = fresh from origin; a stale browser copy needs a
   hard reload.
4. Only then re-measure. Measuring a stale render and patching the (already-fixed) code again is
   the classic wasted loop.

## Horizontal overflow root-cause

Measure `document.documentElement.scrollWidth - clientWidth`. To find the culprit, walk every
element for `getBoundingClientRect().right > clientWidth` but skip subtrees inside an
`overflow-x: auto` ancestor — a contained scroller (table wrapper, sub-nav) never expands the
document. The widest offender outside containment is the cause; the classic shape is a
`flex-wrap: nowrap` row with no wrap rule at the mobile breakpoint. Fix the media query, deploy,
re-measure to 0.

## Harness control test

If `scrollIntoView` / `window.scrollTo` leaves `scrollY` at 0, do not conclude the page blocks
scrolling — repeat on a neutral page first. If the neutral page also refuses, the headless harness
is the blocker and anchor-navigation evidence is unusable. For anchor screenshots use
`scrollIntoView({block:"start", behavior:"instant"})` — smooth behavior may not finish before
capture, and hash navigation in a headless tab may not fire at all (record the measured scrollY
with the screenshot, never assume the jump happened).

## Device emulation lifecycle

CDP `Emulation.setDeviceMetricsOverride` does not survive navigation or reload — re-apply it after
every goto and confirm with `window.innerWidth` before trusting a mobile measurement. Headless
tabs can also blank between probes under emulation switching; re-check `location.pathname` and
re-navigate when selectors start returning null on a page you know has them.

## Screenshot evidence

Capture to a durable path (copy out of the harness tmp dir), one per viewport, each named by
viewport + location. Record alongside it: viewport size, scrollY, and the measured anchor rect.
A screenshot without measurements is a vibe; measurements without a screenshot miss what a vision
pass would catch.