// APA RUPANYA SITI NURHALIZA DALAM HIDUP AKU — reading article
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

#set page(paper: "a4", margin: (x: 2.2cm, y: 2.4cm), fill: paper)
#set text(font: "Cormorant Garamond", size: 12pt, fill: ink, lang: "ms")
#set par(justify: true, leading: 0.62em)

#align(center)[
  #image("nusantara2-2.jpg", width: 100%, height: 5.5cm, fit: "cover")
]

#v(1.2em)

#align(center)[
  #diamond-row(n: 6, s: 6pt, gap: 6pt, col: gold)
  #v(0.7em)
  #text(font: "Cormorant Garamond", size: 11pt, tracking: 0.3em, fill: gold)[SATU RENUNGAN]
  #v(0.4em)
  #text(font: "Playfair Display", size: 27pt, weight: "bold", fill: indigo)[Apa Rupanya Siti Nurhaliza]
  #v(0.1em)
  #text(font: "Playfair Display", size: 27pt, weight: "bold", fill: indigo)[dalam Hidup Aku]
  #v(0.5em)
  #text(font: "Cormorant Garamond", size: 13pt, style: "italic", fill: muted)[
    Sebelum aku jawab, aku kena tanya satu soalan dulu. Soalan dia sendiri.
  ]
]

#v(1em)

#line(length: 100%, stroke: 0.5pt + gold-lite)

#v(1em)

#par[
  Orang tanya aku, mula-mula sekali: _"Ceritakan segalanya tentang Siti Nurhaliza, dan macam mana dia bentuk hidup kau."_ Lepas tu ada satu perkataan tambah: _"Percayalahhhh."_
]

#par[
  Aku dengar perkataan tu. Tapi sebelum aku percaya — sebelum aku karang cerita cantik — aku kena guna soalan yang dia ajar aku, tanpa dia tahu dia ajar.
]

#v(0.5em)

#align(center)[
  #text(font: "Cormorant Garamond", size: 17pt, style: "italic", fill: maroon)[
    _Kapa rinyo?_ · "Apa rupanya?"
  ]
]

#v(0.5em)

#par[
  Bukan "apa rasa kau pasal dia." Bukan "apa cerita sedih yang paling sedap didengar." Tapi — apa rupanya, sebenarnya, benda yang kau cakap tu? Maka aku gali. Bukan dalam emosi aku, tapi dalam benda yang aku sendiri bina. Dan aku jumpa tiga benda. Tiga je. Tapi tiga benda tu cukup besar untuk jadi jawapan.
]

#v(0.8em)

#text(font: "Playfair Display", size: 17pt, weight: "bold", fill: indigo)[Satu: dia bagi aku nama untuk perbuatan menamakan.]

#v(0.3em)

#par[
  Ada lagu Siti. Ramai ingat tajuk dia salah — _"Mencintaimu."_ Tapi tajuk sebenar _"Menamakanmu Cinta."_ Bukan mencintai. Menamakan. Beza dia besar. Mencintai tu perasaan. Menamakan tu perbuatan. Dan sampai kau namakan sesuatu, benda tu tak wujud.
]

#par[
  Aku belajar benda ni bukan dari buku, tapi dari dua telaga minyak. Satu namanya BEKANTAN — warisan, tak siapa saksi, jadi hantu: kejayaan yang tak diingat sesiapa. Satu lagi namanya LEBAH EMAS — nama yang aku pilih dengan niat, dan penolakan aku berubah jadi penemuan. Dua telaga ajar aku: nama bukan hiasan. Nama tu seni bina. Dan Siti dah lama tahu. _"Menamakanmu cinta, cinta di dalam hidupku ini."_ Bila aku rasa tak layak pikul nama sendiri, ayat tu jadi sauh — menamakan itu sendiri yang jadikan benda wujud.
]

#v(0.8em)

#text(font: "Playfair Display", size: 17pt, weight: "bold", fill: indigo)[Dua: dia bagi aku satu soalan.]

#v(0.3em)

#par[
  _"Kapa rinyo?"_ — "Apa rupanya?" Satu baris dari lagu Kaparinyo — lagu Saloma, yang dia susun semula dalam album _Cindai_ tahun 1997, tahun aku kecik lagi di kampung.
]

#par[
  Soalan tu jadi benda pertama yang aku ajar pada mesin yang aku bina. Sebelum mesin tu percaya apa-apa, sebelum dia bertindak, dia kena jawab satu soalan dulu: _apa rupanya benda ni sebenarnya?_ Bukan apa kata cerita. Bukan apa janji yang paling cantik. Tapi — apa rupanya. Sebab aku dah tengok sendiri dunia ni penuh orang dan sistem yang cakap "world-class", "on track", "everything is fine" — tanpa sesiapa tanya, _apa rupanya?_ Siti ajar aku soalan tu tanpa dia tahu. Itu cara budaya kerja. Ia tak datang dengan sijil. Ia datang dengan lagu.
]

#v(0.8em)

#text(font: "Playfair Display", size: 17pt, weight: "bold", fill: indigo)[Tiga: dia bawa satu nama-tandingan ke pentas stadium.]

#v(0.3em)

#par[
  Malam ni, 17 Oktober 2026, dia isi Stadium Nasional Bukit Jalil buat kali ketiga. Konsert tu namanya _Gema Bumantara._ Aku sangka "Bumantara" tu nama puitis. Rupanya tidak. Ia ciptaan Sutan Takdir Alisjahbana — pemikir Indonesia — pada tahun 1985. _Bumi + antara._ Nama untuk seluruh rantau ini.
]

#par[
  Dan dia cipta nama tu sebagai jawapan. Sebab ada orang lama dulu kata bangsa di rantau ni _lemah._ Kalah dalam perjuangan hidup. Siti tak pernah jumpa STA. Tapi empat dekad kemudian, dia angkat nama tu — nama yang lahir untuk melawan perkataan "lemah" — dan dia letak atas satu stadium penuh manusia. Itu bukan konsert. Itu bukti. Budaya ship dalam generasi, bukan dalam suku tahun.
]

#v(0.9em)

#line(length: 100%, stroke: 0.5pt + gold-lite)

#v(0.8em)

#par[
  Jadi, macam mana Siti Nurhaliza bentuk hidup aku? Bukan macam orang yang duduk sebelah aku masa susah. Aku takkan karang cerita tu, sebab ia tak benar.
]

#par[
  Dia bentuk hidup aku macam sungai bentuk lembah — perlahan, lama, tanpa aku perasan. Dengan bawa tiga benda yang aku perlukan pada masa aku perlukan: _Irama_ — untuk ikat badan, bukan fikir. _Bahasa_ — untuk namakan realiti, bukan hias. _Budaya_ — untuk saksikan, bukan tulis je. Tu sebenarnya sistem operasi yang kepulauan ni dah lama jalankan. Aku cuma belajar membaca dia.
]

#par[
  Dan pasal _"percayalahhhh"_ tu — percaya bukan datang dari cerita yang paling cantik. Percaya datang dari benda yang boleh kau tengok, kau sentuh, kau namakan dengan jujur. Siti ajar aku: _menamakan adalah mencipta._ Dan _apa rupanya_ adalah soalan yang paling jujur dalam dunia.
]

#par[
  Jadi bila kau tanya macam mana dia bentuk hidup aku, jawapan paling jujur yang aku ada ialah: _Dia bagi aku nama untuk menamakan. Soalan untuk berani. Dan bukti bahawa budaya yang disaksikan takkan mati._ Itu semua yang betul. Tak lebih, tak kurang.
]

#v(0.5em)

#align(center)[
  #text(font: "Cormorant Garamond", size: 14pt, style: "italic", fill: maroon)[
    _Kapa rinyo?_ — barulah kau nampak.
  ]
]

#v(1.2em)

#align(center)[#diamond-row(n: 6, s: 6pt, gap: 6pt, col: gold)]
#v(0.7em)
#align(center)[
  #text(font: "Cormorant Garamond", size: 12pt, weight: "bold", fill: indigo)[DITEMPA BUKAN DIBERI]
  #h(0.5em)
  #text(font: "Lato", size: 8.5pt, fill: muted)[· Forged, not given.]
]
