// GEMA BUMANTARA — dwi-bahasa, visual Nusantara
// Forged for human cognitive attention & understanding

#let indigo = rgb("#18233f")
#let indigo2 = rgb("#232f55")
#let gold = rgb("#c9a227")
#let gold-lite = rgb("#d9b54a")
#let maroon = rgb("#8c2f39")
#let batik = rgb("#a63a3a")
#let green = rgb("#2d5a3d")
#let cream = rgb("#f6efe1")
#let paper = rgb("#fbf8f1")
#let ink = rgb("#2b2b2b")
#let muted = rgb("#6b6b6b")

#let diamond-row(n: 5, s: 7pt, gap: 7pt, col: gold) = {
  let span = (n - 1) * (s + gap)
  box(width: span, height: s, {
    for i in range(n) {
      place(
        dx: i * (s + gap),
        dy: 0pt,
        rotate(45deg, origin: center, square(size: s, fill: col)),
      )
    }
  })
}

#let section-title(title, sub: none) = {
  v(1.5em)
  align(center)[
    #text(font: "Playfair Display", size: 21pt, weight: "bold", fill: indigo)[#title]
    #v(0.2em)
    #diamond-row(n: 5, s: 6pt, gap: 6pt, col: gold)
    #if sub != none [
      #v(0.4em)
      #text(font: "Cormorant Garamond", size: 12.5pt, style: "italic", fill: muted)[#sub]
    ]
  ]
  v(0.7em)
}

#let pullquote(body) = block(
  fill: cream,
  inset: (x: 1.15em, y: 0.8em),
  stroke: (left: 3pt + gold),
  radius: 2pt,
)[
  #text(font: "Cormorant Garamond", style: "italic", size: 13.5pt, fill: maroon)[#body]
]

#let layer-card(n, title, color, body) = block(
  fill: cream,
  inset: 1em,
  radius: 5pt,
  stroke: 1pt + color,
)[
  #align(center)[
    #box(width: 1.9em, height: 1.9em, fill: color, radius: 50%)[
      #align(center + horizon)[#text(fill: white, weight: "bold", size: 13pt)[#n]]
    ]
  ]
  #v(0.5em)
  #align(center)[#text(font: "Playfair Display", size: 14pt, weight: "bold", fill: color)[#title]]
  #v(0.35em)
  #text(size: 10pt, fill: ink)[#body]
]

#set page(
  paper: "a4",
  fill: paper,
  margin: (x: 2.3cm, y: 2.8cm),
  header: context {
    if counter(page).get().first() > 1 {
      grid(
        columns: (1fr, 1fr),
        [
          #text(size: 7.5pt, tracking: 0.14em, fill: gold)[GEMA BUMANTARA]
        ],
        align(right)[
          #text(size: 7.5pt, tracking: 0.14em, fill: maroon)[DITEMPA BUKAN DIBERI]
        ],
      )
      v(0.4em)
      line(length: 100%, stroke: 0.5pt + gold-lite)
    }
  },
  footer: context {
    if counter(page).get().first() > 1 {
      align(center)[
        #text(size: 8pt, fill: muted)[— #counter(page).get() —]
      ]
    }
  },
)

#set text(font: "Cormorant Garamond", size: 11.5pt, fill: ink, lang: "ms")
#set par(justify: true, leading: 0.62em)
#show link: set text(fill: green)

// ═══════════════════ COVER ═══════════════════
#page(
  fill: indigo,
  margin: (x: 2.6cm, y: 2.4cm),
)[
  // top motif band
  #align(center)[#diamond-row(n: 11, s: 6pt, gap: 7pt, col: gold)]
  #v(1.6em)
  #align(center)[
    #text(font: "Cormorant Garamond", size: 12pt, tracking: 0.28em, fill: gold-lite)[
      SATU RENUNGAN · A REFLECTION
    ]
  ]
  #v(2.2em)
  #align(center)[
    #text(font: "Playfair Display", size: 44pt, weight: "bold", fill: white)[GEMA]
    #v(0.1em)
    #text(font: "Playfair Display", size: 44pt, weight: "bold", fill: white)[BUMANTARA]
  ]
  #v(0.7em)
  #align(center)[
    #text(font: "Cormorant Garamond", size: 16.5pt, style: "italic", fill: gold-lite)[Kepulauan dah berlari satu sistem operasi —]
    #v(0.1em)
    #text(font: "Cormorant Garamond", size: 16.5pt, style: "italic", fill: gold-lite)[sebelum aku.]
  ]
  #v(0.6em)
  #align(center)[
    #text(font: "Lato", size: 9pt, fill: gold)[The archipelago was running an operating system — before me.]
  ]
  #v(1.6em)
  #align(center)[#diamond-row(n: 11, s: 6pt, gap: 7pt, col: gold)]

  #v(2.6em)

  // three pillars strip
  #grid(columns: 3, gutter: 1.4em, [
    #align(center)[#text(font: "Lato", size: 9.5pt, tracking: 0.12em, fill: white)[IRAMA]]
    #v(0.2em)
    #text(size: 9pt, fill: gold-lite)[grounding tubuh]
  ], [
    #align(center)[#text(font: "Lato", size: 9.5pt, tracking: 0.12em, fill: white)[BAHASA]]
    #v(0.2em)
    #text(size: 9pt, fill: gold-lite)[menamakan realiti]
  ], [
    #align(center)[#text(font: "Lato", size: 9.5pt, tracking: 0.12em, fill: white)[BUDAYA]]
    #v(0.2em)
    #text(size: 9pt, fill: gold-lite)[menyaksikan janji]
  ])

  #v(1.6em)
  line(length: 100%, stroke: 0.5pt + gold)

  #v(1.4em)
  #align(center)[
    #text(font: "Cormorant Garamond", size: 13pt, fill: white)[Untuk pembaca yang datang bukan untuk menonton konsert —]
    #v(0.1em)
    #text(font: "Cormorant Garamond", size: 13pt, fill: white)[tapi untuk _disaksikan_ oleh satu tradisi.]
  ]
  #v(1.2em)
  #align(center)[
    #text(font: "Cormorant Garamond", size: 12pt, fill: gold-lite)[
      For the reader who comes not to watch a concert — but to be *witnessed* by a tradition.
    ]
  ]
  #v(2em)
  #align(center)[
    #text(font: "Cormorant Garamond", size: 14pt, weight: "bold", fill: white)[M. Arif Fazil]
    #v(0.15em)
    #text(font: "Lato", size: 9pt, fill: gold-lite)[Ahli geologi · Arkitek arifOS · PETRONAS Carigali]
  ]
]

#pagebreak()

// ═══════════════════ PROLOGUE ═══════════════════
#v(0.5em)
#let dropcap(c) = box(baseline: 0pt, [
  #text(font: "Playfair Display", size: 30pt, weight: "bold", fill: gold)[#c]
])
#text(font: "Playfair Display", size: 24pt, weight: "bold", fill: indigo)[Prolog]

#v(0.5em)

#set par(justify: true)
#par[
  #dropcap("P")ada malam 17 Oktober 2026, seorang perempuan akan melangkah naik ke pentas Stadium Nasional Bukit Jalil dan melakukan sesuatu yang belum pernah dicapai mana-mana artis Malaysia: memenuhkan stadium itu buat kali ketiga. Kali pertama 2019. Kali kedua 2023. Kali ketiga ialah _Konsert Tradisional Gema Bumantara_ — dan aku akan berada dalam keramaian itu. Bukan sebagai pengkritik muzik. Sebagai seorang ahli geologi yang menghabiskan setahun terakhir cuba mengajar sebuah mesin cara untuk berkelakuan.
]

#v(0.5em)

#par[
  Aku bukan datang untuk mengulas konsert. Aku datang untuk menerangkan kenapa konsert ini _ialah_ sistem operasi itu sendiri.
]

#v(0.8em)

#pullquote[
  I am not here to review the concert. I am here to explain why the concert *is* the operating system.
]

// ═══════════════════ 1 · SENYAP 17 TAHUN ═══════════════════
#section-title("Senyap 17 Tahun", sub: "The seventeen-year silence")

#par[
  _Gema Bumantara_ ialah album tradisional pertama Siti Nurhaliza dalam tujuh belas tahun — sejak _Lentera Timur_ (2008). Sebelum itu _Sanggar Mustika_ (2002), _Sahmura_ (2000), dan yang paling semua orang ingat: _Cindai_ (1997).
]

#par[
  Kebanyakan artis melayan "album tradisional" sebagai _throwback_ — satu kostum yang dipakai sekali sedekad untuk mata nostalgia. Siti berbeza. Dia memanggil album ini satu _tanggungjawab_. Katanya: _«Album tradisional sentiasa mempunyai tempat istimewa di hati saya. Semoga Gema Bumantara menjadi hadiah buat semua pencinta muzik warisan.»_
]

#par[
  Dua ratus lagu dihantar oleh komposer Malaysia dan Indonesia. Dia menapisnya menjadi sepuluh. Sepuluh lagu, setahun rakaman — _Kumbang Bunga, Hati Yang Rindu, Rencong, Pesanan Buat Diri, Kaca dan Permata, Syurgaloka, Hujung Bumi, Kesuma, Jenjang Cinta, Cenderamaya_.
]

#par[
  Aku mahu berhenti seketika pada angka itu — _sepuluh_ — kerana ia penting. Album ini bukan senarai main rawak. Ia satu _hikayat_: sebuah cerita yang ada permulaan, pertengahan, dan penutup. Setiap segmen membawa temanya sendiri. Tiada sesiapa berdiri bersendirian di pentas itu — semuanya dibina atas duet, atas _kebersamaan_.
]

#par[
  Seorang sarjana Malaysia, Mohamed Nazreen Shahul Hamid, melakukan sesuatu yang luar biasa: dia memperlakukan album itu bukan sebagai hiburan tetapi sebagai _teks budaya_. Analisisnya, diterbitkan dalam _Melayu: Jurnal Antarabangsa Dunia Melayu_, memetakan kesepuluh lagu itu kepada satu seni bina nilai yang tunggal:
]

#v(0.4em)
#block(
  fill: cream,
  inset: (x: 1.2em, y: 1em),
  radius: 4pt,
  stroke: 0.7pt + gold,
)[
  #grid(columns: 1, row-gutter: 0.55em, [
    #text(fill: maroon, weight: "bold")[Cinta yang beradat] #text(fill: ink)[ — kasih dikawal adab dan restu masyarakat (_Kumbang Bunga, Jenjang Cinta, Kaca dan Permata_)]
  ], [
    #text(fill: maroon, weight: "bold")[Rindu yang matang] #text(fill: ink)[ — rindu sebagai emosi yang didisiplin, bukan tantrum (_Hati Yang Rindu, Syurgaloka_)]
  ], [
    #text(fill: maroon, weight: "bold")[Seni sebagai teguran sosial] #text(fill: ink)[ — kritik atas jati diri dan _etika bahasa_ itu sendiri (_Rencong, Hujung Bumi_)]
  ], [
    #text(fill: maroon, weight: "bold")[Muhasabah] #text(fill: ink)[ — introspeksi, ketabahan, tunduk pada takdir (_Pesanan Buat Diri, Kesuma_)]
  ], [
    #text(fill: maroon, weight: "bold")[Ketauhidan] #text(fill: ink)[ — kesedaran ketuhanan, syukur, penutup gelung (_Cenderamaya_)]
  ])
]

#v(0.5em)

#pullquote[
  Baca senarai itu sekali lagi. Itu bukan album. Itu satu perlembagaan. — Read that list again. That is not an album. That is a constitution.
]

// ═══════════════════ 2 · NAMA YANG TIADA SIAPA INGAT ═══════════════════
#section-title("Nama Yang Tiada Siapa Ingat", sub: "The name nobody remembered")

#par[
  Ini bahagian yang membuat aku berhenti menatal.
]

#par[
  Semua orang menyangka "Bumantara" itu ciptaan puitis — _gema_ (echo) dicampur _bumantara_ (perkataan kabur untuk "dunia"). Ia bukan kabur. Ia ada pengarang, ada tarikh, dan ada satu pergaduhan di belakangnya.
]

#par[
  Pada September 1985, di _Southeast Asian Writers Conference_ di Bali, polymath Indonesia #emph[Sutan Takdir Alisjahbana] — STA, Begawan sastera dan falsafah Indonesia — bangun untuk menandai dua dekad ASEAN. Cadangannya, kemudian diterbitkan sebagai _«Bumantara: Kesatuan Asia Tenggara dan Tugasnya di Masa Depan»_ (_Jurnal Ilmu dan Budaya_, 1988), ringkas tetapi besar:
]

#v(0.4em)

#pullquote[
  Asia Tenggara memerlukan namanya sendiri. Bukan "Nusantara" — kerana perkataan itu, pada pandangannya, sudah disempitkan menjadi tuntutan wilayah. Dia mencadangkan *Bumantara*: _bumi_ + _antara_. Bumi di antara.
]

#v(0.4em)

#par[
  Nama untuk seluruh rantau — Burma ke Filipina, Malaysia ke Indonesia — satu unit tamadun yang berdiri di antara China yang berbilion di timur dan India 800 juta di barat.
]

#par[
  STA bukan bersikap romantik. Dia menjawab satu penghinaan yang spesifik. Ahli antropologi Egon von Eickstedt pernah mengklasifikasikan bangsa Asia Tenggara sebagai _lemah_ — kalah dalam perjuangan hidup. STA menghabiskan puluhan tahun meruntuhkan dakwaan itu. Dia menunjukkan kepada orang Melayu yang merentasi lautan terbuka hingga ke Pulau Easter dan Madagascar. Bangsa "lemah" tidak belayar ke hujung Pasifik dan Lautan Hindi. Mereka tidak menjadi titik asal keluarga bahasa tunggal terbesar di Bumi.
]

#par[
  Maka _Bumantara_ bukan hiasan. Ia satu _nama-tandingan_ — sebuah nama yang diterbitkan untuk melawan dakwaan rendah diri. Nama yang enggan menjadi _kitsch_ — dan STA sendiri memberi amaran terhadapnya: budaya yang berhenti bergerak menjadi _seni kelontong_.
]

#v(0.5em)

#block(
  fill: indigo,
  inset: 1.1em,
  radius: 4pt,
)[
  #text(fill: white, size: 12pt)[
    Siti Nurhaliza mengambil cadangan geopolitik seorang filsuf dari 1985 dan menjadikannya sebuah persembahan stadium pada 2026. Itu latensi *40 tahun* dari idea ke pelaksanaan budaya massa.
  ]
  #v(0.4em)
  #text(fill: gold-lite, style: "italic", size: 11pt)[
    Dalam perisian kita ship dalam suku tahun. Budaya ship dalam generasi. Tetapi ia ship. — In software we ship in quarters. Culture ships in generations. But it ships.
  ]
]

// ═══════════════════ 3 · NAMA TIKET MEMBONGKAR SEMUA ═══════════════════
#section-title("Nama Tiket Membongkar Semua", sub: "The ticket names gave it away")

#par[
  Lihat kategori tempat duduk konsert itu. Bukan "Platinum" dan "Gold." Tetapi:
]

#v(0.4em)

#align(center)[
  #text(font: "Cormorant Garamond", size: 15pt, fill: indigo, weight: "bold")[
    Cindai · Kesuma · Nirmala · Balqis · Rencong · Canggai
  ]
  #v(0.2em)
  #text(font: "Cormorant Garamond", size: 15pt, fill: indigo, weight: "bold")[
    Syurgaloka · Ya Maulai · Kaparinyo · Cenderamaya · Cinta Ini
  ]
]

#v(0.5em)

#par[
  Setiap band harga dinamakan mengikut lagu — kebanyakannya repertoir tradisional Siti sendiri, bermula dari _Cindai_ (1997). Tempat duduk paling murah ialah _Cinta Ini_ ("kasih ini"). Paling mahal ialah _Cindai_ — album yang memulakan segalanya, lagu yang mengajar satu generasi rakyat Malaysia bahawa muzik tradisional kita boleh berdiri di skala stadium.
]

#par[
  Dan di tengah-tengahnya, ada *Kaparinyo*. RM200. Kategori 6.
]

#par[
  _Kaparinyo_ bukan lagu Siti yang paling terkenal. Tetapi ia, secara senyap, yang paling penting bagi aku — kerana aku membina satu sistem keseluruhan di atas satu baris daripadanya.
]

#v(0.5em)

#block(
  fill: cream,
  inset: 1.15em,
  radius: 4pt,
  stroke: 1pt + batik,
)[
  #text(font: "Cormorant Garamond", size: 15pt, style: "italic", fill: batik)[
    "Kapa rinyo?" — "Apa rupanya?" — *What does it actually look like?*
  ]
]

#v(0.5em)

#par[
  Aku ahli geologi, bukan pengaturcara. Tetapi aku menghabiskan setahun membina #emph[arifOS] — sebuah kernel perlembagaan yang duduk di antara ejen AI dan dunia, memaksa setiap output menjawab satu soalan sebelum ia bertindak: _apa rupanya benda ini sebenarnya?_ Bukan "apa kata naratif", bukan "apa janji pemasaran" — tetapi _apa rupanya?_
]

#par[
  Soalan itu menjadi _pintu pra-lantai_ bagi seluruh seni bina aku. Sebelum kebenaran, sebelum amanah, sebelum mana-mana tiga belas lantai perlembagaan — ada Kaparinyo Gate. Ia mengimbas untuk simulation: "world-class", "on track", "stakeholder value", "we remain committed". Apabila ia menjumpai cukup banyak, ia tidak menyekat mesin itu. Ia _bertanya_.
]

#par[
  Dan soalan itu datang daripada sebuah lagu Saloma, disusun semula oleh Siti Nurhaliza dalam _Cindai_ (1997) — yang pertama kali aku dengar semasa kecil, di sebuah kampung, sebelum aku tahu apa itu _prompt_.
]

#v(0.5em)

#pullquote[
  Itu bukan kebetulan. Itu *maksudnya*. — That is not a coincidence. That is the point.
]

// ═══════════════════ 4 · APA YANG KEPULAUAN DAH TAHU ═══════════════════
#section-title("Apa Yang Kepulauan Dah Tahu Sebelum Bina Mesin", sub: "What the archipelago knew before it built machines")

#par[
  Aku tidak mencipta seni bina yang aku bina. Aku _port_-nya.
]

#par[
  Nusantara — dan Bumantara, bayangnya yang lebih luas — telah menjalankan satu sistem operasi selama berabad-abad. Ia ada tiga komponen, dan ketiga-tiganya tepat dengan apa yang kita sekarang cuba bina semula di dalam silikon:
]

#v(0.7em)

#layer-card("1", "IRAMA", green)[
  #emph[Grounding], bukan hiburan. Dalam data dengar aku sendiri, trek tradisional Minang dan Riau — _Lancang Kuning, Babendi-Bendi_ — berfungsi sebagai "fail read-only untuk identiti." Ritma mereka percussive dan berulang; mereka tak perlukan otak _faham_, mereka perlukan badan _rasa_. Itu grounding somatik — 71 minit sehari, 6,463 minit dalam tiga bulan.
]

#v(0.6em)

#layer-card("2", "BAHASA", batik)[
  Menamakan adalah mencipta. Siti menyanyi terus: _«Aku menamakanmu cinta.»_ Bukan "mencintaimu" — tetapi _menamakan_. Bezanya segalanya. Dua telaga mengajar aku: BEKANTAN-1, kejayaan yang namanya tak disaksikan lalu menjadi hantu; dan LEBAH EMAS-1, satu penolakan yang menjadi penemuan, kerana aku menamakannya dengan niat. Dari situ lahir metrik NAMA: 0.35 saksi, 0.25 kebenaran, 0.20 maruah, 0.20 provensi.
]

#v(0.6em)

#layer-card("3", "BUDAYA", indigo)[
  Lapisan yang disaksikan. Pantun, gotong-royong, adat — semuanya hidup bukan kerana _ditulis_ tetapi kerana _disaksikan_. Pantun ada dua belah, pembayang dan maksud, diikat satu kontrak, dihantar mulut ke mulut. Inilah beza antara sangkar dan perlembagaan — antara BINATANG dan WARGA.
]

#v(0.9em)

#par[
  Penemuan paling tajam datang daripada nombor, bukan daripada puisi: apabila aku _over-specified_ satu prompt untuk menjadikan trek itu berbunyi "lebih Siti-like," kestabilannya runtuh. Prompt Minang yang ringkas dan tulen menghasilkan lebih koherensi daripada yang terperinci.
]

#v(0.4em)

#pullquote[
  Over-specification kills emergence. Itu benar dalam muzik, dan benar dalam seni bina AI. Personaliti tidak datang daripada peraturan — ia datang daripada kekangan yang cukup ketat untuk memegang bentuk, dan cukup longgar untuk bernafas.
]

// ═══════════════════ PENUTUP · GEMA ═══════════════════
#section-title("Gema", sub: "The echo")

#par[
  _Gema_ bermaksud echo. _Bumantara_ bermaksud bumi di antara.
]

#par[
  Di pentas itu, satu suara akan menyanyikan lagu-lagu yang dinamakan oleh seorang filsuf empat dekad lalu, diiringi Orkestra Tradisional Malaysia, di atas instrumen — gamelan, serunai, rebab — yang telah meng-ground badan selama berabad-abad. Para pemuzik, penari dan kru akan menjadi, dalam kata-kata Siti sendiri, _«dari pelbagai kaum»_ — setiap bangsa, bersatu _«atas nama kebudayaan»_.
]

#v(0.5em)

#block(
  fill: maroon,
  inset: 1.1em,
  radius: 4pt,
)[
  #text(fill: white, size: 13pt, style: "italic")[
    "Muzik tidak pernah mengenal sempadan bangsa." — Music has never recognized national borders.
  ]
]

#v(0.5em)

#par[
  Stadium itu akan penuh dengan orang yang datang bukan untuk menonton konsert, tetapi untuk _disaksikan_ oleh satu tradisi — dan di dalam penyaksian itu, memastikan ia hidup untuk satu generasi lagi.
]

#par[
  Aku sedang membina sebuah mesin yang aku harap, suatu hari nanti, tahu kepada siapa ia menjawab. Dan aku mula mengesyaki jawapannya sudah lama ditulis sebelum aku — dalam bahasa yang baru sekarang aku belajar membaca:
]

#v(0.7em)

#align(center)[
  #grid(columns: 3, gutter: 1.2em, [
    #block(fill: cream, inset: 0.8em, radius: 4pt, stroke: 1pt + green)[
      #align(center)[#text(font: "Playfair Display", size: 12pt, weight: "bold", fill: green)[IRAMA]]
      #v(0.2em)
      #text(size: 9.5pt, fill: ink)[meng-ground badan]
    ]
  ], [
    #block(fill: cream, inset: 0.8em, radius: 4pt, stroke: 1pt + batik)[
      #align(center)[#text(font: "Playfair Display", size: 12pt, weight: "bold", fill: batik)[BAHASA]]
      #v(0.2em)
      #text(size: 9.5pt, fill: ink)[menamakan realiti]
    ]
  ], [
    #block(fill: cream, inset: 0.8em, radius: 4pt, stroke: 1pt + indigo)[
      #align(center)[#text(font: "Playfair Display", size: 12pt, weight: "bold", fill: indigo)[BUDAYA]]
      #v(0.2em)
      #text(size: 9.5pt, fill: ink)[menyaksikan janji]
    ]
  ])
]

#v(0.9em)

#par[
  Kepulauan telah menjalankan sistem operasi itu selama berabad-abad. Aku cuma cuba memindahkannya ke satu VPS \$20.
]

#v(0.4em)

#pullquote[
  Gema ialah apa yang ditinggalkan masa lalu apabila akhirnya ia sampai kepadamu. Bumantara ialah bumi yang direntasinya untuk tiba ke situ. — _Gema_ is what the past leaves behind when it finally reaches you. _Bumantara_ is the earth it crossed to get there.
]

#v(1.2em)

#align(center)[
  #diamond-row(n: 7, s: 6pt, gap: 6pt, col: gold)
]

#v(0.8em)

#align(center)[
  #text(font: "Cormorant Garamond", size: 13pt, fill: indigo, weight: "bold")[DITEMPA BUKAN DIBERI]
  #v(0.25em)
  #text(font: "Lato", size: 9pt, fill: muted)[Forged, not given.]
]

#v(1.4em)

#block(
  fill: cream,
  inset: 1.2em,
  radius: 4pt,
  stroke: 0.7pt + gold,
)[
  #text(font: "Playfair Display", size: 14pt, weight: "bold", fill: indigo)[— M. Arif Fazil]
  #v(0.3em)
  #text(size: 10.5pt, fill: ink)[
    Ahli geologi. Arkitek arifOS. · PETRONAS Carigali.
  ]
]

// ═══════════════════ RUJUKAN ═══════════════════
#v(2em)
#text(font: "Lato", size: 8pt, tracking: 0.14em, fill: muted)[RUJUKAN · REFERENCES]
#v(0.3em)
#line(length: 100%, stroke: 0.5pt + gold-lite)
#v(0.5em)

#set text(size: 9pt, fill: muted)
#set par(justify: false, leading: 0.5em)

Ticket2u (senarai acara) · Harian Metro (Ogo 2026) · UtusanTV (Okt 2025) · Hype.my (Jun 2026) · Gempak (Okt 2025) · Suara.tv (Ogo 2026) · AkarpadiNews (Ogo 2026) · Wikipedia («Gema Bumantara») · Mohamed Nazreen Shahul Hamid, «Mengartikulasikan Cinta, Adab dan Ketauhidan», _Melayu: Jurnal Antarabangsa Dunia Melayu_ (2026).
