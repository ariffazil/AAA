// Demis Hassabis — Realiti Hidup
// Ditempa bukan diberi
// Source-base: exa research (Wikipedia, Guardian, MIT Tech Review, FT, Nobel Prize,
// American Academy, Penguin Random House, Probinism, Guardian, LessWrong, Fortune,
// Time, 9to5Google). Bukan petikan lengkap buku; bentuk realiti terkumpul dari
// sumber awam verifiable. Compiled 2026-10-21.

#set page(
  paper: "a4",
  margin: (x: 2.4cm, y: 2.2cm),
  numbering: "1",
)

#set text(
  font: "DejaVu Serif",
  size: 10.5pt,
  lang: "ms",
)

#set par(justify: true, leading: 0.65em, first-line-indent: 0pt)

#set heading(numbering: none)

#let sect(title) = {
  v(0.8em)
  block(
    fill: luma(232),
    inset: (x: 10pt, y: 6pt),
    radius: 2pt,
    width: 100%,
  )[#text(size: 12pt, weight: "bold")[#title]]
  v(0.4em)
}

// ============================================================
// COVER
// ============================================================
#align(center)[
  #v(1.2cm)
  #text(size: 22pt, weight: "bold")[Demis Hassabis]\
  #v(0.3em)
  #text(size: 14pt)[Realiti Hidup, dari Catur ke Nobel]
  #v(0.8em)
  #text(size: 10pt, style: "italic")[Disusun dari sumber awam — bukan petikan lengkap buku]
]

#v(1.5cm)

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  [
    *Lahir:* Julai 1976, Finchley, London Utara\
    *Ibu:* Singapura-Cina, kerja sebagai pembantu jualan di John Lewis, ibu tunggal yang menjaga anak-anak\
    *Bapa:* Greek-Cypriot, pemuzik, jual mainan dari van merah Volkswagen\
    *Nama asal:* Hassapis — tukar kepada Hassabis
  ],
  [
    *Gelaran:* CBE 2018, Knighted 2024\
    *Anugerah:* Nobel Kimia 2024 (AlphaFold) bersama John Jumper\
    *Jawatan:* CEO Google DeepMind; pengasas Isomorphic Labs\
    *Pasangan & keluarga:* Isteri + dua anak, menetap London
  ],
)

#v(0.8em)

#align(center)[
  #text(size: 9pt, style: "italic")[
    "There is no 50 percent mode in Demis. There is not even a 99 percent mode in Demis. There is only 100 percent." — Shane Legg
  ]
]

#v(1cm)

// ============================================================
// BAB 1 — AKAR
// ============================================================
#sect[Bab 1 — Akar: catur, kemiskinan, dan disiplin seorang ayah]

Ibu Demis membesar dalam kemiskinan di Singapura — sebahagian masa sebagai yatim di jalan raya, sebelum ditemui saudara mara yang membawanya ke London untuk belajar kejururawatan. Apabila Demis kecil, dia kerja shift di John Lewis sebagai pembantu jualan, ambil kerja tambahan sebagai pencuci. Bapa dia Greek-Cypriot, family's first university graduate, tetapi tak tahan office work — lebih suka jadi penyanyi-penulis lagu, jual mainan dari van Volkswagen merah yang dah buruk.

Dalam latar keluarga yang camni, bakat Demis muncul awal dan tajam:

- Umur 4 — belajar catur dengan menonton bapa bermain dengan bapa saudara. Dalam beberapa minggu, dah boleh kalahkan orang dewasa.
- Umur 5 — mula bertanding. Duduk di atas buku telefon di atas dua kerusi bertindan supaya kepalanya nampak di atas meja. Kerap kalahkan kanak-kanak lebih tua.
- Umur 6 — layak bermain dalam Kejuaraan Bawah 14 Britain. Menang dua perlawanan sebelum tertidur di atas meja sebab permainan masuk lewat malam, jauh lepas waktu tidur.

Leonard Barden — pak catur Inggeris — mendekati bapa Demis dengan satu ayat: "Your son is the best six-year-old I've ever seen." Respons bapa: terima ayat tu sebagai wahyu dari Tuhan. Hujung minggu selepas hujung minggu, dia masukkan Demis ke dalam van merah Volkswagen, bawakan ke dewan gereja yang daif di merata tempat — tinggalkan isteri dengan dua anak kecil. Kadang tidur dalam sleeping bag atas enjin belakang van; kadang hostel murah, sebilik satu katil dua orang. Kalau Demis menang, hadiahnya cukup untuk bayar hostel. Ibu tetap runsing tentang kos.

Demis menghabiskan A-level dua tahun awal, pada umur 16. Catur bukan sekadar permainan — dia alat beliau membentuk minda. Sebelum games, semasa games, dan selepas games, fikirannya dilatih untuk menghadapi masalah dengan cara yang terancang.

#pagebreak()

// ============================================================
// BAB 2 — KOMPUTER DAN BULLET GAMES
// ============================================================
#sect[Bab 2 — Komputer, permainan, dan pembentukan kerjaya]

Pada 1984, dengan wang kemenangan catur, Demis beli komputer pertama: ZX Spectrum 48K. Belajar pengaturcaraan sendiri dari buku. Tulis atur cara AI pertama di Commodore Amiga untuk bermain reversi.

1994 — berusia 17 tahun — dia bekerja di Bullfrog Productions dengan Peter Molyneux, mereka dan mengetua pembangunan *Theme Park* (1994). Permainan jual jutaan salinan, menang Golden Joystick.

Dalam tempoh Bullfrog, Demis membuat satu pemerhatian penting: watak digital boleh belajar dari tindakan seperti tepuk dan pukulan — bentuk primitif *reinforcement learning*. Konsep ini akan kekal dalam kepalanya hampir dua dekad.

Dari Cambridge (Double First dalam Sains Komputer), Demis asaskan Elixir Studios pada 1998 — syarikat permainan sendiri. Berjaya secara komersial. Tetapi matlamat sebenar dia bukan permainan. Dia mahukan intelligence sebagai subjek utama.

Quote yang kekal: "I thought it was time to do something that focused on intelligence as a primary thing."

#pagebreak()

// ============================================================
// BAB 3 — NEUROSAINS: MEMORI DAN MASA HADAPAN
// ============================================================
#sect[Bab 3 — Neurosains: hippocampus, masa lampau, dan masa hadapan]

2005 — berhenti Elixir, mula PhD neurosains kognitif di UCL. Tiada background biologi sekolah menengah, tetapi memilih hippocampus — kawasan otak yang masih kurang difahami algoritma.

Pada 2007, satu kajian yang dipilih jurnal *Science* sebagai salah satu daripada 10 "Breakthrough of the Year": Demis menunjukkan lima pesakit amnesia (rosak hippocampus) tidak boleh membayangkan peristiwa masa hadapan dengan baik. Implikasinya: bahagian otak yang dianggap untuk masa lampau juga kritikal untuk perancangan masa depan.

Penemuan ini — *memori dan perancangan masa hadapan saling berkait* — akan jadi benih falsafah di sebalik DeepMind: sistem yang bukan hanya mengingat, tetapi merancang.

2009/2010 — berhenti postdoc, kembali sains komputer dengan Shane Legg (seorang lagi postdoc UCL yang mereka cipta istilah "artificial general intelligence") dan Mustafa Suleyman (aktivis sosial yang mahu jadi "force multiplier" untuk kebaikan).

#pagebreak()

// ============================================================
// BAB 4 — GANG OF THREE DAN DEEPMIND
// ============================================================
#sect[Bab 4 — Gang of Three dan penubuhan DeepMind]

Pelan perniagaan 2010 ditolak hampir semua pelabur. "Enlightenment" bukan model bisnes yang meyakinkan.

Pitch demi pitch:

- Singularity Summit after-party — cuba meyakinkan Peter Thiel.
- David Gammon — pelabur religius yang meminta mereka pitch kepada anak lelakinya yang berumur 14 tahun.
- Founders Fund akhirnya selamatkan mereka.

Thiel selesa melabur 2010 (lawan arus). Menjelang akhir 2012, dia berhenti melabur lagi — "terlalu mahal dan terlalu arus perdana". Pada 2014, DeepMind tetap perlu duit besar. Facebook tawar lebih, tetapi Zuckerberg tak nampak AI lebih penting dari VR atau 3D printing. Google — £400 juta (sekitar \$650 juta ketika itu).

Tiga pengasas — Gang of Three:

- #text(weight: "bold")[Demis Hassabis] — visioner, neurosaintis-pemprogram. Peranan: mission control.
- #text(weight: "bold")[Shane Legg] — New Zealander; mereka cipta istilah AGI. Peranan: rangka matematik untuk mengukur AGI.
- #text(weight: "bold")[Mustafa Suleyman] — aktivis jalanan, mahu gunakan tech untuk kebaikan. Peranan: pendorong etika & governans.

David Silver — kawan rapat Demis sejak zaman Cambridge — orang yang akan mengarah *AlphaGo*.

*Velocity of execution:* sehingga 2026, DeepMind sudah terbitkan lebih 1,000 kertas saintifik — lebih sedozen dalam *Nature* dan *Science*.

#pagebreak()

// ============================================================
// BAB 5 — ATARI: MESIN BELAJAR SENDIRI
// ============================================================
#sect[Bab 5 — Atari: mesin yang belajar dari piksel tulen]

2013 — DeepMind umum DQN (Deep-Q Network) yang mengajar dirinya bermain Atari classics dari awal: Pong, Breakout, Space Invaders — hanya dari piksel mentah dan signal skor.

Teknik: gabungan *reinforcement learning* dengan "memory replay buffer" yang meniru cara hippocampus manusia bermain dengan memori.

David Silver, ketika itu: "People were just blown away. It was a turning point."

Demonstrasi teknologi ini yang meyakinkan Larry Page bayar £400 juta.

#pagebreak()

// ============================================================
// BAB 6 — ALPHAGO: MOVE 37
// ============================================================
#sect[Bab 6 — AlphaGo, Move 37, dan kekejaman Seoul]

Mac 2016, Four Seasons Seoul. Lee Sedol (kedua tertinggi dunia, pernah juara dunia) lwn AlphaGo.

Bilangan kemungkinan state dalam Go dianggar sekurang-kurangnya $10^(170)$ — jauh lebih banyak daripada atom dalam alam semesta yang boleh diamati. Tak boleh brute force.

David Silver dan pasukannya latih neural network bukan untuk mengira, tetapi untuk meniru pakar. Hasilnya: *Move 37* dalam Game 2. Begitu aneh dan tiada precedent, Michael Redmond (pemain Go terbaik dunia, komentator) pada awalnya keluarkan batu itu dari papan, "No, that can't be right."

Ternyata — stroke of creative genius. Mesin boleh jadi intuitif, malah cantik.

Selepas kalah, Lee Sedol — yang masih shock — mohon maaf: "I, Lee Sedol, lost, but mankind did not." Thore Graepel, dalam nada lain: "At first, it looks harmless. Then it's just completely dominating. We don't understand the mechanics... We just know that it is in control."

#pagebreak()

// ============================================================
// BAB 7 — KEJAYAAN GANJAR DAN PECAH DALAMAN
// ============================================================
#sect[Bab 7 — Project Mario, kesihatan yang pecah, dan Suleyman]

DeepMind Health dilancar — kemudian torpedoed oleh satu tajuk Daily Mail: "GOOGLE HANDED PATIENTS' FILES." Walaupun misleading, ia dedahkan distrust awam terhadap big tech.

Project Mario — inisiatif Mustafa Suleyman untuk spin out DeepMind dari Google dengan lembaga etika bebas. Perjuangan dalaman panjang. Gagal.

Klimaks peribadi: ouster Suleyman selepas siasatan buli. Perpecahan rumah tangga yang highlightkan Dilema Demis — keseimbangan antara kesetiaan kawan dan tuntutan keras kepimpinan.

BetaAlpha: AlphaZero — belajar catur dan shogi dari kosong, tanpa data manusia. Menang 100-0 lwn AlphaGo dalam sparring match.

2022, Julai: AlphaFold menghasilkan struktur 200 juta protein dalam satu pelepasan tunggal.

#pagebreak()

// ============================================================
// BAB 8 — CHATGPT SHOCK
// ============================================================
#sect[Bab 8 — ChatGPT Shock: tanks di atas rumput]

Demis sudah lama ketawa bahasa sebagai "ungrounded symbols". Kecerdasan sebenar, katanya, mesti bermain dalam simulasi dunia (Gaia) atau kuasai games.

Meanwhile — di seberang teluk, Ilya Sutskever baca kertas 2017 "Attention Is All You Need" — bangun dari kerusi.

OpenAI, tanpa beban purism saintifik DeepMind dan caution korporat Google, *scale* GPT-3 (175 bilion parameter) dan lepas ChatGPT pada 30 November 2022.

Lima bulan kemudian, Demis kepada Mallaby: "This is wartime. OpenAI and Microsoft have literally parked the tanks on the lawn."

Mallaby tinggalkan kita dengan soalan menghantui: dalam perlumbaan superintelligence, akan kalahkah yang baik — yang dipandu sains dan keselamatan — kepada accelerationists?

#pagebreak()

// ============================================================
// BAB 9 — GEMINI DAN SETERUSNYA
// ============================================================
#sect[Bab 9 — Gemini, Nobel, dan cita-cita yang belum selesai]

Demis gabung Google Brain dengan DeepMind — bina Gemini. Garis pertempuran dilukis: titan lama RL-based versus upstart transformer.

Oktober 2024: Nobel Kimia bersama John Jumper untuk AlphaFold — struktur protein jangka hayat yang dianggap mustahil.

2025-2026, fokus sekarang:

- Project Astra — pembantu digital universal. Ingat butiran perbualan sebelumnya. Personalization. Demo pada smart glasses.
- Gemini Robotics — robot dikawal Gemini. Bawa dulang, main tic-tac-toe, sediakan makan tengah hari.
- Project Mariner — ejen yang bukan hanya mendedah dunia tetapi *bertindak* di dalamnya: tempah tiket, belanja online.
- Isomorphic Labs — startup untuk selesaikan penyakit dengan AI.

Hassabis masih meramal AGI dalam 5-10 tahun, dengan kebarangkalian bahagian bawah. Test pilihannya sendiri: adakah sistem boleh terbitkan relativity umum hanya dari maklumat yang Einstein ada? Atau hipotesis matematik baru?

Bekerja shift kedua, 10pm-4am: "I come alive at about 1 a.m." Tidur enam jam. Office hari penuh, back-to-back, tiada jeda. Hampir tiada hobi selain bola sepak — Liverpool.

#pagebreak()

// ============================================================
// BAB 10 — SUARA PALING DALAM
// ============================================================
#sect[Bab 10 — Suara paling dalam: apa yang Demis percaya]

*Mengenai sains vs kejuruteraan.* "I identify myself as a scientist first and foremost." OpenAI, kontrasnya, "revered engineers." Saham jangka panjang: mungkin DeepMind memandang rendah *brute force scaling laws* — dan mahal untuknya.

*Mengenai kekhuatiran.* "What keeps me up at night? The question of international standards and cooperation — not just between countries, but also between companies and researchers — as we get towards the final steps of AGI."

*Mengenai consciousness.* "I don't think any of today's systems to me feel self-aware or conscious in any way... obviously, everyone needs to make their own decisions by interacting with these chatbots. I think theoretically it's possible." Dan: "These systems might acquire some feeling of self-awareness. That is possible."

*Mengenai cita-cita.* Mengatasi Newton dan Einstein dalam memahami *fabric of reality itself*.

*Mengenai dirinya sendiri.* Ender's Game — budak genius yang dikurung, dibuli, dimanipulasi dewasa — menyelamatkan manusia dengan kos peribadi yang besar. Dia minta isterinya baca buku tu. Isteri rasa kasihan pada watak utama. Demis rasa identified "powerfully". "Like Ender, Hassabis had dedicated every fiber of his being to the accomplishment of a mission."

#pagebreak()

// ============================================================
// BAB 11 — BAYANGAN YANG IKUT
// ============================================================
#sect[Bab 11 — Bayangan yang ikut: Musk, OpenAI, dan mereka yang menentang]

Elon Musk bermain peran penting — tetapi sarat dengan kontradiksi mengganggu.

Bragging kepada Larry Page tentang pelaburannya dalam DeepMind kononnya membantu促成 pengambilalihan Google. Selepas ditolak untuk membeli DeepMind 2014 (lebih suka Google), Musk tukar benci Hassabis — label dia "evil genius" dengan bukti bahawa Demis pernah kerja dalam permainan yang betul-betul bernama *Evil Genius*.

Musk dan Reid Hoffman — dijemput mesyuarat lembaga keselamatan DeepMind, mendengar pelan dalaman, kemudian gunakan apa yang didengar untuk asas OpenAI. Demis, dalam nota Mallaby, "Hassabis, ever practical, was also angry in a simpler way. Musk and Hoffman had been invited to the SpaceX gathering in good faith. They had sat through the meeting, listened to DeepMind's plans, and then used what they had heard to double-cross him."

Karakter lain dari pergerakan ini:

- Geoffrey Hinton — "There aren't any examples of more intelligent things being controlled by less intelligent things." Ditanya mengapa teruskan: "I could give you the usual arguments... but the truth is that the prospect of discovery is too sweet."
- Ilya Sutskever — saintis OpenAI, baca transformer 2017 dan bangun dari kerusi.
- Mustafa Suleyman — akhirnya di Microsoft, dengan kecenderungan untuk beri amaran tentang risiko pekerjaan berganda AI.
- Shane Legg — masih di DeepMind, percaya *singleton* adalah pertaruhan terbaik untuk AI selamat.

#pagebreak()

// ============================================================
// BAB 12 — STRUKTUR YANG DEMIS BANGUN
// ============================================================
#sect[Bab 12 — Struktur yang Demis bina (atau tak berjaya bina)]

*Manhattan Project untuk AI.* Demis pernah bayangkan kumpulkan saintis terbaik dunia di satu pusat terpencil, fokus tunggal pada superintelligence selamat. Gabungan stesen angkasa *Ender* + perkemahan rahsia Manhattan Project di New Mexico. Episode *Out of Eden* Mallaby: "But to believers in the singleton vision, OpenAI's founding represented the Fall."

*Singleton + Egos.* Singleton tidak bertahan pertemuan dengan egonya yang ditarik oleh AI.

*Race, bukan cooperation.* Perang US-China menjadikan cooperation sukar, walaupun dalam US sendiri. Nuklear non-proliferation treaties — bukti bahawa cooperation antara pihak yang lebih bermusuhan daripada AS-China adalah mungkin — tidak dikutip serius.

*Implications for governance.* Capability ≠ authority. Siapa yang paling bijak bukan siapa yang patut kawal sistem selepas ia cukup berkuasa. Tokoh yang sama — Demis, Altman, Musk — semua push acceleration sambil bimbangkan acceleration.

#pagebreak()

// ============================================================
// BAB 13 — HUJUNG (BELUM)
// ============================================================
#sect[Bab 13 — Hujung (belum)]

Buku Mallaby bukan victory lap. Ia satu race.

Beberapa soalan yang ditinggal terbuka:

- Bolehkah Demis jadi Einstein *dan* Ender dalam satu hayat? Atau perlu dia pilih?
- Adakah saintis selamat itu illusion — orang yang paling hampir dengan AGI bakal juga orang paling berkepentingan untuk capainya?
- Siapa yang sebenarnya akan jadi Oppenheimer untuk AI — yang bertanya kebenaran selepas ciptaan?

Demis sendiri, dalam Mid-40s, duduk di satu restoran London dengan Mallaby, teringat cerita bapa: "Your best" bukan pepatah generik — dia ambil literal, "try literally to the point of destroying yourself, go absolutely, completely 100 percent."

#align(center)[
  #v(0.4cm)
  #text(size: 10pt, style: "italic")[#quote(block: true)[
    *Aku nak hang buat satu pdf aku boleh baca untuk tau pasai realiti hidup dia.*\
    #v(0.4em)
    Ini bukan cerita DeepMind. Ini bukan biografi pengasas Google DeepMind.\
    Ini soal seorang manusia yang memutuskan tak tidur cukup sehinggalah dia boleh \
    berdiri di antara Newton dan apa yang datang selepas Einstein.
  ]]
]

#v(1cm)

#align(center)[
  #text(size: 8pt, style: "italic")[
    Disusun 2026-10-21 · Sumber: Wikipedia, Guardian (2024, 2025, 2026), MIT Technology Review, \
    FT, American Academy of Arts & Sciences, NobelPrize.org, Penguin Random House, \
    Probinism, LessWrong, Fortune, Time, 9to5Google.\
    BUKAN petikan verbatim Sebastian Mallaby, *The Infinity Machine* (2026).\
    DITEMPA BUKAN DIBERI.
  ]
]
