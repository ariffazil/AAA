// IG STORY / TIKTOK — 1080x1920, single vertical post
#let gold = rgb("#e0c264")
#let gold-lite = rgb("#f0d68a")

#set page(width: 1080pt, height: 1920pt, margin: 0pt, fill: black)
#set text(font: "Cormorant Garamond", fill: white, lang: "ms")

#let diamond-row(n: 6, s: 10pt, gap: 9pt, col: gold) = {
  let span = (n - 1) * (s + gap)
  box(width: span, height: s, {
    for i in range(n) {
      place(dx: i * (s + gap), dy: 0pt, rotate(45deg, origin: center, square(size: s, fill: col)))
    }
  })
}

#block(width: 100%, height: 100%, fill: black)[
  // full-bleed background image
  #place(top + left, image("ig-hero-0.jpg", width: 1080pt, height: 1920pt, fit: "cover"))
  // scrim top for title legibility
  #place(top + left, rect(width: 1080pt, height: 760pt, fill: rgb("#0a0c16a0")))
  // scrim bottom for date legibility
  #place(bottom + left, rect(width: 1080pt, height: 300pt, fill: rgb("#0a0c16b0")))

  // ── Top: eyebrow ──
  #place(top + center, dy: 48pt)[
    #align(center)[
      #diamond-row(n: 6, s: 10pt, gap: 9pt, col: gold)
      #v(0.9em)
      #text(font: "Cormorant Garamond", size: 22pt, tracking: 0.35em, fill: gold)[SATU RENUNGAN]
    ]
  ]

  // ── Title ──
  #place(center + horizon, dy: -80pt)[
    #align(center)[
      #text(font: "Playfair Display", size: 78pt, weight: "bold", fill: white)[GEMA]
      #v(0.05em)
      #text(font: "Playfair Display", size: 78pt, weight: "bold", fill: white)[BUMANTARA]
      #v(0.6em)
      #text(font: "Cormorant Garamond", size: 30pt, style: "italic", fill: gold-lite)[
        Bukan nostalgia. Denyut yang tak pernah berhenti.
      ]
    ]
  ]

  // ── Bottom: date / venue ──
  #place(bottom + center, dy: 150pt)[
    #align(center)[
      #text(font: "Lato", size: 20pt, tracking: 0.12em, fill: white)[
        17 OKTOBER 2026 · STADIUM NASIONAL BUKIT JALIL
      ]
      #v(0.5em)
      #text(font: "Cormorant Garamond", size: 18pt, fill: gold)[
        Dato' Sri Siti Nurhaliza · Gema Bumantara
      ]
    ]
  ]
]
