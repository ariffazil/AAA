// GEMA BUMANTARA — 2 pages: BM + English, hero image, condensed
#let indigo = rgb("#18233f")
#let gold = rgb("#c9a227")
#let gold-lite = rgb("#e0c264")
#let maroon = rgb("#8c2f39")
#let batik = rgb("#a63a3a")
#let green = rgb("#2d5a3d")
#let cream = rgb("#f6efe1")
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
#set text(font: "Cormorant Garamond", size: 11pt, fill: ink, lang: "ms")

// ── Hero block with title overlay ──
#let hero(sub, byline) = block(
  width: 100%,
  height: 11.2cm,
  fill: black,
)[
  #image("nusantara2-2.jpg", width: 100%, height: 11.2cm, fit: "cover")
  // scrim for readability
  #place(top + left, rect(width: 100%, height: 11.2cm, fill: rgb("#0c0e1a78")))
  // darker bottom band behind the tagline
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

#set par(justify: true, leading: 0.52em)

// ═══════════════════════ PAGE 1 — BAHASA NUSANTARA ═══════════════════════
#page[
  #hero(
    "Kepulauan dah berlari satu sistem operasi — sebelum aku.",
    "GEMA BUMANTARA · Bahasa Nusantara",
  )
  #body(
    "Kepulauan Dah Berlari Satu Sistem Operasi",
    "The archipelago was already running an operating system — before me.",
    [
      #par[
        Pada 17 Oktober 2026, Siti Nurhaliza menaiki pentas Stadium Nasional Bukit Jalil dan memenuhkannya buat kali ketiga — rekod yang belum dicapai mana-mana artis Malaysia. _Konsert Tradisional Gema Bumantara._ Aku hadir bukan sebagai pengkritik muzik, tetapi sebagai ahli geologi yang setahun ini cuba mengajar sebuah mesin cara untuk berkelakuan — kerana aku mula percaya konsert ini _ialah_ sistem operasi itu sendiri.
      ]
      #par[
        Nama "Bumantara" bukan rekaan puitis. Ia lahir daripada Sutan Takdir Alisjahbana, sasterawan-filsuf Indonesia, pada 1985: _bumi + antara_ — tanah di antara China yang berbilion dan India 800 juta. Ia satu _nama-tandingan_: jawapan kepada dakwaan lama bahawa bangsa Nusantara itu "lemah". Bangsa "lemah" tidak belayar ke Pulau Easter dan Madagascar. Empat dekad kemudian, Siti membawa cadangan seorang filsuf itu ke pentas stadium. Budaya ship dalam generasi, bukan suku tahun.
      ]
      #par[
        Lihat nama tiket: bukan Platinum dan Gold, tetapi Cindai, Kesuma, Nirmala, Balqis, Rencong — dan di tengahnya, _Kaparinyo_. _"Kapa rinyo?"_ — "Apa rupanya?" Daripada satu baris lagu itu aku bina pintu pertama arifOS: sebelum kebenaran, sebelum amanah, mesin mesti menjawab _apa rupanya benda ini sebenarnya_ — bukan apa kata naratif, bukan apa janji pemasaran.
      ]
      #par[
        Aku tidak mencipta apa-apa. Aku _port_-nya. Kepulauan dah lama jalankan satu sistem operasi: *Irama* yang meng-ground badan — ritma Minang tak perlukan otak faham, cukup badan rasa. *Bahasa* yang menamakan realiti — menamakan adalah mencipta. *Budaya* yang menyaksikan janji — pantun, gotong-royong, adat hidup bukan kerana ditulis, tetapi kerana disaksikan. Aku cuma memindahkannya ke satu VPS \$20.
      ]
      #par[
        _Gema_ ialah apa yang ditinggalkan masa lalu apabila akhirnya ia sampai kepadamu. _Bumantara_ ialah bumi yang direntasinya untuk tiba ke situ.
      ]
    ],
  )
]

// ═══════════════════════ PAGE 2 — ENGLISH ═══════════════════════
#page[
  #hero(
    "The archipelago was running an operating system — before me.",
    "GEMA BUMANTARA · English",
  )
  #body(
    "The Archipelago Was Running an Operating System",
    "Kepulauan dah berlari satu sistem operasi — sebelum aku.",
    [
      #par[
        On 17 October 2026, Siti Nurhaliza will step onto the stage of Stadium Nasional Bukit Jalil and fill it for the third time — a record no Malaysian artist has matched. _Konsert Tradisional Gema Bumantara._ I will be there not as a music critic, but as a geologist who spent a year teaching a machine how to behave — because I have come to believe this concert _is_ the operating system.
      ]
      #par[
        "Bumantara" is not a poetic coinage. It came from Sutan Takdir Alisjahbana, the Indonesian writer-philosopher, in 1985: _bumi + antara_ — the earth between a billion-strong China and an 800-million India. It is a _counter-name_: an answer to the old claim that the peoples of the archipelago were "weak." Weak peoples do not sail to Easter Island and Madagascar. Four decades later, Siti carried a philosopher's proposal onto a stadium stage. Culture ships in generations, not quarters.
      ]
      #par[
        Look at the ticket names: not Platinum and Gold, but Cindai, Kesuma, Nirmala, Balqis, Rencong — and at their centre, _Kaparinyo_. _"Kapa rinyo?"_ — "What does it actually look like?" From that single line I built the first gate of arifOS: before truth, before trust, the machine must answer _what this thing actually looks like_ — not what the narrative says, not what the marketing promises.
      ]
      #par[
        I invented nothing. I _ported_ it. The archipelago has long run an operating system: *Irama* grounding the body — Minang rhythm needs no understanding from the brain, only feeling from the body. *Bahasa* naming reality — to name is to create. *Budaya* witnessing the covenant — pantun, gotong-royong, adat live not because they were written, but because they were witnessed. I am only porting it to a \$20 VPS.
      ]
      #par[
        _Gema_ is what the past leaves behind when it finally reaches you. _Bumantara_ is the earth it crossed to get there.
      ]
    ],
  )
]
