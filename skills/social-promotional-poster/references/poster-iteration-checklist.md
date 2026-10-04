# Poster Iteration Checklist

Run this checklist after every render. Skip any step at your own peril.

## 1. File integrity

```bash
identify /path/to/out.png    # ImageMagick
md5sum /path/to/out.png      # must change after CSS patches
```

- [ ] `identify` returns correct dimensions (1080x1350 for IG post)
- [ ] MD5 differs from previous render (otherwise Chrome cache returned stale output)
- [ ] File size reasonable (>100KB for 1080x1350 - smaller = empty/missing fonts)

## 2. Vision-loop self-critique prompt (paste into vision_analyze)

```
Review this promotional poster. Be brutally honest:
1. Hero image - present and clean, or YouTube UI / watermarks / product mismatch leaking through?
2. Typography hierarchy - which element wins the eye first? What is competing?
3. CTA clarity - is there ONE clear next action with one clear next channel?
4. Overall viral coefficient 0-10. What is broken, what is working, what is the ONE thing that would push this +2 points?
```

After 3 renders, evolve the question to target specific failures from previous rounds.

## 3. Anti-slop spot-check

Run through the 10 slop tells (from claude-design skill):

- [ ] No tech-gradient (blue/violet glossy)
- [ ] No generic indigo accent
- [ ] No icon + heading + sentence x 3 equal-weight feature grid (unless doing it intentionally)
- [ ] No left-border accent callout cards
- [ ] No glassmorphism by default
- [ ] No monument stat (oversized numbers filling space)
- [ ] No rounded-square icon topper on every heading
- [ ] No center-stack composition
- [ ] No Inter-default typography
- [ ] Surface matches composition (Decide/Learn surface = hero acceptable)

## 4. Brand fidelity (real-people rule)

- [ ] If poster features a named human: source image is REAL photo, NOT from `/root/forge_work/` or `/root/.openclaw/media/`
- [ ] If user supplied a screenshot with UI overlays: inpainting actually worked (or design embraces the artifact)
- [ ] Hero image content matches product/brand (no dim sum in nasi lemak poster)

## 5. Conversion readiness

- [ ] CTA channel is ONE only (IG DM OR WhatsApp OR Telegram)
- [ ] CTA action is clear (DM, pre-order, scan, RSVP)
- [ ] Urgency line present if brand is local F&B / drop / event
- [ ] Handle visible at CTA and/or footer (NOT both = redundancy)
- [ ] Location/area mentioned if walk-in business