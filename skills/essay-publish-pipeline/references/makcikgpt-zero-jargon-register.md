# MakcikGPT Writing Register — Zero Jargon Rule

## Core Rule (Arif 2026-08-14, enforced)

**ZERO jargon in MakcikGPT articles.** If a word would not exist in a kampung conversation between two makcik at a nasi lemak stall, it is jargon.

### Forbidden words (non-exhaustive)
FQ, arifOS, AI, proxy, KPI, governance, token, metric, federation, constitutional, entropy, thermodynamic, capability, agent, scalar, vector, measurement, organ, sovereign, seal, forge, apex, quantum, drift, confident, bullshit, model (in tech context)

### Exception
Words the **user explicitly wrote** in their own text are OK (e.g. "KPI boleh main" in context). Those are narrative references, not framework usage.

### Why this exists
Arif explicitly rejected all technical framing in MakcikGPT articles. Even the word "drift" was removed from "Kenapa Love Mati" article. The register is **makcik kampung** — pure human experience.

### Writing technique
- Start with a concrete object (nasi lemak, timbangan, cermin)
- One concept per section
- Blockquotes for emphasis (max 2 sentences)
- Tables for comparison
- HR between sections
- No bullet points for main content (save for lists)
- Closing = one memorable line, not summary

### Template structure
```html
Title: [concept in Malay]
Subtitle: "Versi Makcik Kampung · [date]"
Body: concrete → abstract → personal → conclusion
Footer: "DITEMPA BUKAN DIBERI"
```

### Verification
After writing, scan with: `grep -oinE '\b(FQ|arifOS|AI|proxy|KPI|drift|federation|constitutional|entropy|thermodynamic|capability|agent|token|scalar|vector|metric|measurement|organ|governance|sovereign|seal|forge|apex|quantum)\b' FILE | grep -v 'font-family\|tokens.css\|link rel'`
If output is non-empty, remove jargon before publishing.
