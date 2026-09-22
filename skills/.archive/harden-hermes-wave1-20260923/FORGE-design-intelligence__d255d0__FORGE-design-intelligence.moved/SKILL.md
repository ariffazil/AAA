---
id: FORGE-design-intelligence
name: FORGE-design-intelligence
version: 1.0.0-2026-08-20
description: >
  Design intelligence for building professional UI/UX across platforms.
  Industry-specific reasoning rules, UI style taxonomy, color palettes,
  typography pairing, accessibility guidelines, and anti-patterns.
  Use when any agent builds web surfaces, landing pages, dashboards, or UI.
owner: A-FORGE
risk_tier: low
floor_scope: ['F1', 'F4', 'F6', 'F13']
autonomy_tier: T1
capability_tier: fed-reasoning-heavy
ecology_state: WARM
tags: [design, ui, ux, tailwind, accessibility, typography, color, styles, patterns]
trigger_phrases:
  - "design system"
  - "ui design"
  - "ux guidelines"
  - "color palette"
  - "typography"
  - "accessibility"
  - "landing page"
  - "dashboard design"
  - "glassmorphism"
  - "neumorphism"
  - "brutalism"
  - "design tokens"
  - "ui styles"
  - "anti-patterns"
  - "responsive design"
dependencies:
  skills:
    - FORGE-tailwind-tokens
---

# FORGE-design-intelligence — Design Intelligence Knowledge Base

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.
> **Kebijaksanaan:** Captured from external research (ui-ux-pro-max), distilled for federation use.

---

## Purpose

Provide agents with comprehensive design intelligence when building any UI:
- Federation cockpit surfaces
- Landing pages (arif-fazil.com, federation dashboards)
- MCP GUI applications
- Internal tools and admin panels
- External-facing web properties

## When to Use

- Building any new web page or component
- Designing dashboard layouts
- Choosing color schemes for a project
- Selecting typography for a brand
- Reviewing UI for accessibility compliance
- Generating design systems for new projects
- Auditing existing UI for anti-patterns

## When NOT to Use

- Token-level Tailwind config → use `FORGE-tailwind-tokens`
- MCP Apps iframe/CSP wiring → use `FORGE-mcp-gui`
- Browser automation or navigation → use `agentic-web` doctrine
- Runtime theme switching logic → use `FORGE-tailwind-tokens`

---

## Constitutional Floor Alignment

| Floor | Application |
|-------|-------------|
| F1 AMANAH | Design decisions must serve the user, not aesthetic ego |
| F4 CLARITY | Every element must communicate purpose; no decorative noise |
| F6 MARUAH | WCAG AA contrast minimum; dignity in readability; no exclusionary design |
| F13 SOVEREIGN | Brand colours and visual identity approved by Arif before any public deploy |

---

## §1 — Industry Design Rules

When building for a specific domain, apply these industry-specific patterns:

### Tech & SaaS
| Domain | Pattern | Style Priority | Anti-Patterns |
|--------|---------|---------------|---------------|
| SaaS | Feature-centric hero + social proof | Minimalism, Bento Grid | Cluttered hero, generic stock photos |
| Developer Tool | Code-first, terminal aesthetics | Dark Mode, Brutalism | Marketing fluff, corporate speak |
| AI/Chatbot | Conversation-forward, trust indicators | Glassmorphism, Soft UI | Overpromising sentience, uncanny valley |
| Cybersecurity | Shield imagery, dark palette, zero-trust signals | Dark Mode, Minimalism | Bright neon, cartoon hackers |

### Finance & Banking
| Domain | Pattern | Style Priority | Anti-Patterns |
|--------|---------|---------------|---------------|
| Fintech | Trust-first, regulatory badges | Minimalism, Clean Lines | AI purple/pink gradients, gamification of risk |
| Banking | Institutional credibility, conservative palette | Corporate, Clean | Trendy animations, dark mode (unless user-opted) |
| Crypto/Web3 | Transparency, real-time data | Dark Mode, Dashboard | Overly complex tokenomics visuals, moon imagery |

### Healthcare
| Domain | Pattern | Style Priority | Anti-Patterns |
|--------|---------|---------------|---------------|
| Medical Clinic | Clean, professional, appointment-forward | Soft UI, Minimalism | Playful animations, casual tone |
| Pharmacy | Product grid, trust seals, clear pricing | Clean, Functional | Dark themes, complex navigation |
| Mental Health | Calming palette, gentle interactions | Soft UI, Warm Minimalism | Urgency cues, alarming statistics |

### E-commerce
| Domain | Pattern | Style Priority | Anti-Patterns |
|--------|---------|---------------|---------------|
| General | Product-first, clear CTAs, trust signals | Clean, Responsive Grid | Overwhelming carousels, pop-up overload |
| Luxury | Editorial layout, whitespace, premium feel | Minimalism, Editorial | Discount badges, urgency timers |
| Food Delivery | Appetizing visuals, location-aware | Warm, Card-based | Complex menus, tiny touch targets |

### Services
| Domain | Pattern | Style Priority | Anti-Patterns |
|--------|---------|---------------|---------------|
| Restaurant | Hero image, menu-forward, reservation CTA | Warm, Card-based | Auto-playing video, complex parallax |
| Beauty/Spa | Calming palette, before/after, booking | Soft UI, Editorial | Neon accents, aggressive CTAs |
| Legal | Professional credibility, case results | Corporate, Minimalism | Friendly/casual tone, bright colors |

---

## §2 — UI Style Taxonomy

79 searchable styles organized by visual family:

### General Visual Styles (43 active)
| Style | Best For | Key Characteristics |
|-------|----------|---------------------|
| **Minimalism** | SaaS, luxury, portfolios | Whitespace, clean typography, limited palette |
| **Brutalism** | Developer tools, creative agencies | Raw HTML aesthetic, bold type, no rounded corners |
| **Glassmorphism** | AI products, creative tools | Frosted glass, blur, transparency layers |
| **Neumorphism** | Smart home, wellness apps | Soft shadows, subtle depth, monochrome |
| **Dark Mode** | Developer tools, media, gaming | Dark backgrounds, light text, reduced eye strain |
| **Bento Grid** | Dashboards, feature showcases | Apple-style grid layout, varied card sizes |
| **Soft UI (evolution)** | Wellness, beauty, premium | Soft shadows, organic shapes, calming palette |
| **Claymorphism** | Playful apps, education, kids | 3D clay-like elements, rounded, friendly |
| **Skeuomorphism** | Utility apps, legacy audiences | Realistic textures, familiar metaphors |
| **Flat Design** | Enterprise, dashboards | No shadows/depth, solid colors, clean |
| **Material Design** | Android-first, enterprise | Elevation, ripple effects, consistent grid |
| **Organic/Nature** | Wellness, eco-brands | Natural shapes, earth tones, flowing forms |
| **Gradient Mesh** | Creative, portfolios | Complex multi-color gradients, visual depth |
| **Duotone** | Media, photography sites | Two-color treatment, dramatic contrast |
| **Isometric** | Tech, data visualization | 3D isometric illustrations, technical feel |
| **Retro/Vintage** | Food, lifestyle, nostalgia brands | Muted colors, classic typography, textures |
| **Cyberpunk** | Gaming, crypto, nightlife | Neon on dark, glitch effects, futuristic |
| **Aurora** | Creative, SaaS | Gradient animations, northern lights inspiration |

### Mobile-Specific (2)
| Style | Platform | Notes |
|-------|----------|-------|
| **iOS Native** | iOS | SF Pro, rounded groups, blur backgrounds |
| **Material You** | Android 12+ | Dynamic color, large titles, expressive |

### Platform Design Systems (3)
| System | When to Use |
|--------|-------------|
| **Fluent 2** | Microsoft ecosystem, Windows apps |
| **Shopify Polaris** | E-commerce, Shopify ecosystem |
| **Adobe Spectrum** | Creative tools, Adobe ecosystem |

### Mobile Material (1)
| Style | Notes |
|-------|-------|
| **Material 3 Expressive** | Android Material with expressive motion |

### Analytics (1)
| Style | Notes |
|-------|-------|
| **Dashboard Analytics** | Data-dense, chart-forward, information hierarchy |

---

## §3 — Color Palettes by Industry

### Palette Selection Rules
1. **Primary** — brand identity, 60% of color usage
2. **Secondary** — supporting, 30% of color usage
3. **Accent/CTA** — action color, 10% of color usage
4. **Background** — canvas, never pure white (#FFF) in dark themes
5. **Text** — must meet WCAG AA (4.5:1 contrast minimum)

### Industry Palettes

| Industry | Primary | Secondary | CTA | Background | Notes |
|----------|---------|-----------|-----|------------|-------|
| **SaaS/Tech** | #2563EB (Blue) | #7C3AED (Purple) | #F59E0B (Amber) | #F8FAFC | Trust + innovation |
| **Fintech** | #1E40AF (Deep Blue) | #059669 (Green) | #DC2626 (Red) | #F1F5F9 | Stability + growth |
| **Healthcare** | #0891B2 (Teal) | #059669 (Green) | #2563EB (Blue) | #F0FDFA | Calm + healing |
| **E-commerce** | #7C3AED (Purple) | #EC4899 (Pink) | #F59E0B (Amber) | #FFFBEB | Energy + conversion |
| **Luxury** | #18181B (Near-black) | #D4AF37 (Gold) | #B45309 (Bronze) | #FAFAF9 | Exclusivity + elegance |
| **Food/Beverage** | #DC2626 (Red) | #F59E0B (Amber) | #059669 (Green) | #FEF2F2 | Appetite + warmth |
| **Wellness/Spa** | #E8B4B8 (Soft Pink) | #A8D5BA (Sage) | #D4AF37 (Gold) | #FFF5F5 | Calm + premium |
| **Gaming** | #7C3AED (Purple) | #EC4899 (Pink) | #10B981 (Emerald) | #0F172A | Energy + excitement |
| **Legal** | #1E3A5F (Navy) | #92400E (Brown) | #B45309 (Bronze) | #F8FAFC | Authority + trust |
| **Education** | #2563EB (Blue) | #059669 (Green) | #F59E0B (Amber) | #EFF6FF | Clarity + growth |

---

## §4 — Typography Pairing

### Pairing Principles
- **Maximum 2 font families** per project (1 for display, 1 for body)
- **Contrast in weight**, not in style (avoid mixing script + sans-serif unless intentional)
- **Test at all sizes** — some fonts break at small sizes

### Curated Pairings

| Pairing | Display | Body | Mood | Best For |
|---------|---------|------|------|----------|
| **Professional** | Inter | Inter | Clean, modern | SaaS, dashboards |
| **Editorial** | Playfair Display | Source Serif Pro | Elegant, authoritative | Luxury, editorial |
| **Technical** | JetBrains Mono | Inter | Code-forward, precise | Developer tools |
| **Friendly** | DM Sans | DM Sans | Warm, approachable | Consumer apps |
| **Premium** | Cormorant Garamond | Montserrat | Sophisticated, calm | Wellness, luxury |
| **Bold** | Space Grotesk | Inter | Geometric, modern | Tech, startups |
| **Warm** | Lora | Open Sans | Comfortable, readable | Blog, content sites |
| **Minimal** | Outfit | Outfit | Geometric, neutral | Clean interfaces |

### Google Fonts Import Pattern
```
https://fonts.google.com/share?selection.family=Inter:wght@400;500;600;700|Playfair+Display:wght@400;600;700
```

---

## §5 — Accessibility Guidelines (Non-Negotiable)

### WCAG AA Compliance
| Rule | Requirement | Check |
|------|-------------|-------|
| **Text Contrast** | 4.5:1 minimum for normal text | Use WebAIM Contrast Checker |
| **Large Text Contrast** | 3:1 minimum for 18pt+ or 14pt bold | Same tool |
| **Focus States** | Visible focus ring on all interactive elements | Test with keyboard nav |
| **Reduced Motion** | Respect `prefers-reduced-motion` | CSS media query |
| **Touch Targets** | Minimum 44x44px for interactive elements | Measure in dev tools |
| **Alt Text** | All meaningful images have descriptive alt | Screen reader test |
| **Color Independence** | Never use color as the only indicator | Add icons/patterns |
| **Text Scaling** | Layout survives 200% text zoom | Test in browser zoom |

### Semantic HTML
- Use `<button>` not `<div onClick>`
- Use `<nav>`, `<main>`, `<header>`, `<footer>`
- Use `<h1>`-`<h6>` in order (no skipping levels)
- Use `aria-label` when visible text is insufficient

---

## §6 — Anti-Patterns (What NOT To Do)

### Universal Anti-Patterns
| ❌ Anti-Pattern | ✅ Instead |
|----------------|-----------|
| Auto-playing video/carousel | Static hero with clear CTA |
| Pop-up on load | Exit-intent or scroll-triggered |
| Cookie banner covering content | Minimal, dismissible banner |
| Hover-only interactions on mobile | Touch-friendly alternatives |
| Walls of text without hierarchy | Scannable sections with headings |
| Stock photos of people shaking hands | Authentic imagery or illustrations |
| Rainbow gradients everywhere | Purposeful accent gradients |
| Centered vertical navigation | Left sidebar or top nav |
| Infinite scroll without cues | Pagination or "load more" with count |
| Form errors after submission | Inline validation, real-time feedback |
| Broken layouts at 375px width | Mobile-first responsive testing |
| Focus trapping without escape | Keyboard-accessible modals |

### Federation-Specific Anti-Patterns
| ❌ Anti-Pattern | ✅ Instead |
|----------------|-----------|
| Overly complex federation dashboards | 5-panel HUD model (from HUD doctrine) |
| Raw data dumps to users | Curated mission health indicators |
| Console.log in production surfaces | Structured logging with receipts |
| Hardcoded color values | Use Trinity design tokens |
| No loading states | Skeleton screens or spinners |

---

## §7 — Pre-Delivery Checklist

Before shipping any UI surface:

```
[ ] No emojis as icons (use SVG: Heroicons, Lucide, or Phosphor)
[ ] cursor-pointer on all clickable elements
[ ] All interactive elements keyboard-accessible
[ ] Focus states visible and styled
[ ] prefers-reduced-motion respected
[ ] Text contrast meets WCAG AA (4.5:1)
[ ] Responsive: tested at 375px, 768px, 1024px, 1440px
[ ] No horizontal scroll on any viewport
[ ] Images have meaningful alt text
[ ] Forms have labels (not just placeholders)
[ ] Error states are clear and actionable
[ ] Loading states exist for async operations
[ ] Dark mode tested (if applicable)
[ ] No layout shift on load (CLS < 0.1)
[ ] Touch targets minimum 44x44px
[ ] Content reflows without clipping at narrow widths
[ ] Badges/chips don't break with long text
[ ] Interaction timing feels responsive (< 100ms feedback)
```

---

## §8 — Design System Generation Pattern

When asked to generate a complete design system for a new project:

```
1. IDENTIFY the industry/domain
2. SELECT pattern (hero-centric, dashboard, editorial, etc.)
3. CHOOSE style family (minimalism, soft UI, dark mode, etc.)
4. PICK palette (industry-aligned, WCAG compliant)
5. PAIR typography (display + body, max 2 families)
6. DEFINE effects (shadows, transitions, hover states)
7. LIST anti-patterns to avoid (industry-specific)
8. APPLY pre-delivery checklist
```

---

## Refusal Surface

- ❌ Never use pure black (#000) for text — use #18181B or similar
- ❌ Never use pure white (#FFF) for backgrounds in dark mode
- ❌ Never use font size below 14px for body text
- ❌ Never use auto-playing media without user control
- ❌ Never sacrifice accessibility for aesthetics
- ❌ Never skip WCAG AA contrast verification
- ❌ Never use more than 2 font families
- ❌ Never ship without mobile testing at 375px

---

*Forged: 2026-08-20 by Hermes under F13 SOVEREIGN directive.*
*Kebijaksanaan captured from external research, distilled for federation governance.*
*DITEMPA BUKAN DIBERI — Forged, Not Given. ⚒️*
