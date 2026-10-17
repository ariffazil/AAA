// GEMA BUMANTARA — 2 pages: BM + English, public-facing, hero image
#let indigo = rgb("#18233f")
#let gold = rgb("#c9a227")
#let gold-lite = rgb("#e0c264")
#let maroon = rgb("#8c2f39")
#let paper = rgb("#fbf8f1")
#let ink = rgb("#26252a")
#let muted = rgb("#6b6b6b")

#let diamond-row(n: 5, s: 6pt, gap: 6pt, col: gold) = {
  let span = (n - 1) * (s + gap)
  box(width: span, height: s, {
    for i in range(n) {
      place(dx: i * (s + gap), dy: 0pt, rotate(45deg, origin: center, square(size: s, fill: col)))
    }
  })
}

#set page(paper: "a4", margin: 0cm, fill: paper)
#set text(font: "Cormorant Garamond", size: 11.5pt, fill: ink, lang: "ms")

// ── Hero block with title overlay ──
#let hero(sub, byline) = block(
  width: 100%,
  height: 11.2cm,
  fill: black,
)[
  #image("nusantara2-2.jpg", width: 100%, height: 11.2cm, fit: "cover")
  #place(top + left, rect(width: 100%, height: 11.2cm, fill: rgb("#0c0e1a78")))
  #place(bottom + left, rect(width: 100%, height: 3.2cm, fill: rgb("#0a0c16a8")))
  #place(top + left, dx: 1.6cm, dy: 1.3cm)[
    #diamond-row(n: 7, s: 6pt, gap: 6pt, col: gold)
    #v(0.7em)
    #text(font: "Cormorant Garamond", size: 10pt, tracking: 0.3em, fill: gold-lite)[SATU RENUNGAN · A REFLECTION]
    #v(0.5em)
    #text(font: "Playfair Display", size: 40pt, weight: "bold", fill: white)[GEMA]
    #v(0.05em)
    #text(font: "Playfair Display", size: 40pt, weight: "bold", fill: white)[BUMANTARA]
    #v(0.45em)
    #text(font: "Cormorant Garamond", size: 13.5pt, style: "italic", fill: gold-lite)[#sub]
  ]
  #place(bottom + left, dx: 1.6cm, dy: 1.0cm)[
    #text(font: "Lato", size: 8pt, tracking: 0.12em, fill: rgb("#ffffffcc"))[#byline]
  ]
]

// ── Body scaffold ──
#let body(title, subtitle, content) = block(
  inset: (x: 1.8cm, y: 1.1cm),
)[
  #text(font: "Playfair Display", size: 17pt, weight: "bold", fill: indigo)[#title]
  #v(0.15em)
  #text(font: "Cormorant Garamond", size: 12pt, style: "italic", fill: muted)[#subtitle]
  #v(0.5em)
  #content
  #v(0.7em)
  #align(center)[#diamond-row(n: 5, s: 5pt, gap: 5pt, col: gold)]
  #v(0.6em)
  #align(center)[
    #text(font: "Cormorant Garamond", size: 11.5pt, weight: "bold", fill: indigo)[DITEMPA BUKAN DIBERI]
    #h(0.5em)
    #text(font: "Lato", size: 8pt, fill: muted)[· Forged, not given.]
  ]
]

#set par(justify: true, leading: 0.55em)

// ═══════════════════════ PAGE 1 — BAHASA NUSANTARA ═══════════════════════
#page[
  #hero(
    "Muzik tradisional bukan nostalgia — ia adalah denyut yang tidak pernah berhenti.",
    "GEMA BUMANTARA · Bahasa Nusantara",
  )
  #body(
    "Irama, Bahasa dan Budaya yang Tidak Akan Mati",
    "Mengapa sebuah album tradisional masih memenuhi stadium pada 2026.",
    [
      #par[
        Pada 17 Oktober 2026, Siti Nurhaliza menaiki pentas Stadium Nasional Bukit Jalil dan memenuhkannya buat kali ketiga — satu rekod yang belum dicapai mana-mana artis Malaysia. _Konsert Tradisional Gema Bumantara_ ialah album tradisional pertamanya dalam 17 tahun. Tetapi ia bukan sekadar pusingan nostalgia.
      ]
      #par[
        Nama "Bumantara" pun bukan rekaan semata. Ia datang daripada Sutan Takdir Alisjahbana, seorang pemikir Indonesia, pada tahun 1985: _bumi_ + _antara_ — tanah di antara. Ia adalah jawapannya kepada dakwaan lama bahawa bangsa di rantau ini "lemah". Bangsa yang lemah tidak belayar merentasi lautan hingga ke Pulau Easter dan Madagascar.
      ]
      #par[
        Perhatikan nama-nama tiket: bukan Platinum dan Gold, tetapi Cindai, Kesuma, Nirmala, Balqis, Rencong — dan di tengahnya, _Kaparinyo_. _"Kapa rinyo?"_ bererti "Apa rupanya?" Satu baris daripada lagu lama, tetapi soalannya masih hidup hingga hari ini.
      ]
      #par[
        Budaya tradisional sebenarnya sebuah sistem, bukan hiasan. Tiga perkara yang membuatnya terus hidup: *Irama* yang mengikat tubuh — ritma Minang tidak memerlukan otak untuk memahami, cukup tubuh untuk merasa. *Bahasa* yang menamakan realiti — menamakan adalah mencipta. *Budaya* yang menyaksikan — pantun, gotong-royong, adat hidup kerana disaksikan, bukan sekadar ditulis.
      ]
      #par[
        _Gema_ bererti gema. _Bumantara_ bererti bumi di antara. Apabila masa lalu akhirnya sampai kepada kita, itulah gemanya; dan bumi yang direntasinya untuk tiba ke situ, itulah Bumantara.
      ]
    ],
  )
]

// ═══════════════════════ PAGE 2 — ENGLISH ═══════════════════════
#page[
  #hero(
    "Traditional music is not nostalgia — it is a pulse that never stopped.",
    "GEMA BUMANTARA · English",
  )
  #body(
    "The Rhythm, Language and Culture That Refuse to Die",
    "Why a traditional album still fills a stadium in 2026.",
    [
      #par[
        On 17 October 2026, Siti Nurhaliza will step onto the stage of Stadium Nasional Bukit Jalil and fill it for the third time — a record no Malaysian artist has matched. _Konsert Tradisional Gema Bumantara_ is her first traditional album in 17 years. But it is not just a lap of nostalgia.
      ]
      #par[
        The name "Bumantara" is not simply made up. It came from Sutan Takdir Alisjahbana, an Indonesian thinker, in 1985: _bumi_ + _antara_ — the land between. It was his answer to the old claim that the peoples of this region were "weak." Weak peoples do not sail across the ocean to Easter Island and Madagascar.
      ]
      #par[
        Notice the ticket names: not Platinum and Gold, but Cindai, Kesuma, Nirmala, Balqis, Rencong — and at the centre, _Kaparinyo_. _"Kapa rinyo?"_ means "What does it actually look like?" One line from an old song, but the question still lives today.
      ]
      #par[
        Traditional culture is really a system, not decoration. Three things keep it alive: *Irama* — rhythm that binds the body; Minang rhythm needs no understanding from the mind, only feeling from the body. *Bahasa* — language that names reality; to name is to create. *Budaya* — culture that bears witness; pantun, gotong-royong and adat live because they are witnessed, not merely written.
      ]
      #par[
        _Gema_ means echo. _Bumantara_ means the earth between. When the past finally reaches us, that is the echo; and the earth it crossed to arrive, that is Bumantara.
      ]
    ],
  )
]
