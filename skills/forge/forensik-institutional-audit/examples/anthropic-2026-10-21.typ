// Dario & Daniela Amodei -- Anthropic Institutional Reality Audit
// Constitutional audit, bukan biografi keluarga.
// Compile 2026-10-21

#set page(paper: "a4", margin: (x: 2.2cm, y: 2cm), numbering: "1")
#set text(font: "DejaVu Serif", size: 10pt, lang: "ms")
#set par(justify: true, leading: 0.6em, first-line-indent: 0pt)

#let sect(title) = {
  v(0.7em)
  block(fill: luma(232), inset: (x: 10pt, y: 6pt), radius: 2pt)[
    #text(size: 11.5pt, weight: "bold")[#title]
  ]
  v(0.3em)
}

#let sm(it) = text(size: 9pt)[#it]

#align(center)[
  #v(0.6cm)
  #text(size: 18pt, weight: "bold")[DARIO AND DANIELA AMODEI]
  #v(0.2em)
  #text(size: 12pt)[The Duo of Intelligence, Their Shadow, Their Scars, and the Anthropic Paradox]
  #v(0.4em)
  #text(size: 10pt, style: "italic")[Siapa yang bina institusi, siapa pegang autoriti, sama ada keselamatan survive scaling]
  #v(0.6em)
  #text(size: 9pt)[Compiled 2026-10-21 -- Verdict: HOLD pending F13 review]
]

#v(0.5cm)

#align(center)[
  #block(fill: luma(245), inset: 10pt, radius: 3pt, width: 92%)[
    #text(size: 9pt)[
      *Soalan utama*: Adakah institusi yang diasaskan sebagai correction
      terhadap tekanan organisasi lama boleh kekalkan misinya apabila modal,
      compute, dan tekanan IPO mengepunginya? Anthropic ialah alternasi constitution
      ke OpenAI -- atau hanya ekpresi berbeza sistem scaling yang sama? Falsifiable.
    ]
  ]
]

#pagebreak()

#sect[00. Executive judgment]

*PROVEN* (disokong dokumen primer):

1. Anthropic ditubuhkan Januari 2021 oleh *tujuh* pengasas bersama, bukan dua. Per TIME (Perrigo 30 Mei 2024) dan Wikipedia: Dario Amodei (CEO, bekas VP Research OpenAI), Daniela Amodei (President, bekas VP Safety and Policy), Tom Brown (CCO, ex-GPT-3 lead), Jack Clark (head of policy), Jared Kaplan (Chief Scientist, lead author Scaling Laws), Sam McCandlish (co-author Scaling Laws), Chris Olah (interpretability).
2. Anthropic ialah Public Benefit Corporation (Delaware), dengan Long-Term Benefit Trust pegang Class T stock.
3. Constitutional AI (arXiv 2212.08073, Dec 2022) ditulis oleh Yuntao Bai dan Jared Kaplan sebagai corresponding authors -- bukan oleh Amodei. 49 senarai penulis.
4. IPO November 2026 dirancang; nilai sasaran lebih dari 2 trilion dollar. Founder LLC berkongsi 50.1% undi; LTBT mesti pilih majoriti lembaga.

*CONTESTED*:

- "Anthropic lebih selamat" -- FALSIFIABLE. Sendiri mengakui safety capability dari luar (Schulman, Leike).
- "Safety survive scaling" -- rekod kosong. Tidak nampak keputusan LTBT menentang CEO secara terbuka.
- "Sibling coordination" -- Daniela sendiri memanggil model CEO-President piawai Silicon Valley.

*UNKNOWN*:

- Trust Agreement penuh (tidak diterbitkan).
- Apa yang sebenar-benar berlaku dalaman OpenAI 2019-2020 hingga tujuh orang ini keluar.
- Senarai penuh outgoing safety personnel Anthropic 2025-2026 (tidak lengkap).

#pagebreak()

#sect[01. Epistemic limits dan had sumber]

Bukti yang digunakan, diberi kelas:

*Primer* (Tier 1):
- anthropic.com/news/the-long-term-benefit-trust (19 Sept 2023)
- anthropic.com/responsible-scaling-policy (v3.4 berkuat kuasa Julai 2026)
- arXiv 2212.08073 "Constitutional AI: Harmlessness from AI Feedback" (Bai et al. 2022)
- arXiv 2001.08361 "Scaling Laws for Neural Language Models" (Kaplan et al. 2020)
- Stanford eCorner transcript Daniela Amodei (Feb 2024)
- Harvard Law Forum: "Anthropic Long-Term Benefit Trust" (Morley/Berger/Simmerman, Okt 2023)
- TIME excerpt, Billy Perrigo (30 Mei 2024)
- Lex Fridman interview transcript (Nov 2024)
- CBS News Dario interview (Feb 2026)
- Anthropic statement on Department of War (26 Feb 2026)

*Bukan primer tapi berguna*:
- Wikipedia (semakan silang)
- Reuters, AP, NPR, CNBC, TIME, Fortune, Verge
- 9to5AI "Anthropic LTBT: who picks the board" (20 Okt 2026)
- Robert Eccles "Anthropic Before the Prospectus" (Okt 2026)

*Tidak boleh pakai*:
- Memo orang dalam, tweet tanpa nama, naratif retroaktif
- sam_altman.pdf sebagai autoriti untuk Anthropic

#pagebreak()

#sect[02. Siapa sebenarnya yang asaskan Anthropic]

Sumber primer: TIME (Perrigo 30 Mei 2024): "Anthropic's seven co-founders all previously worked at OpenAI." Wikipedia dan Anthropic company page senarai tujuh; Ben Mann ditambah oleh sesetengah sumber sebagai lapan.

Tujuh pengasas rasmi:

- Dario Amodei -- CEO, Italian-American, computational biophysicist (PhD Princeton), VP Research OpenAI 2016-2020, helped lead GPT-2 and GPT-3 effort.
- Daniela Amodei -- President, BA UC Santa Cruz (English lit, politik, muzik), OpenAI VP Safety and Policy; led people plus research engineering teams; early Stripe.
- Tom Brown -- Chief Compute Officer; lead engineer GPT-3 (OpenAI).
- Jared Kaplan -- Chief Scientist; lead author Scaling Laws (Kaplan et al. 2020); Johns Hopkins faculty on leave.
- Sam McCandlish -- senior research; co-author Scaling Laws; theoretical physics (Stanford).
- Jack Clark -- co-founder, head of policy; former OpenAI Policy Director; author of Import AI Newsletter.
- Chris Olah -- co-founder, interpretability research; founder distill.pub.

*Pemerhatian kritikal*: Naratif "hanya Amodei bersaudara" merendahkan sumbangan lima nama lain. Pengasas yang bukan adik-beradik Amodei *secara terbuka* orang yang:
- Tulis *scaling laws* yang memberi Anthropic strategi model.
- Reka arsitektur latihan model Claude (Tom Brown, GPT-3 lineage).
- Asas program interpretability (Chris Olah).
- Pimpin hal ehwal negara dan dasar awam (Jack Clark).

#pagebreak()

#sect[03. Founder-role decomposition]

Amodei kedua-duanya berbeza, tapi *complementarity*, bukan dichotomized 'Dario mind/Daniela hands'. Daniela sendiri menolak framing itu (Stanford 2024): dia "much more sort of practical kind of the business oriented side," bukan "non-intellectual."

*Dario* memimpin:
- Halatuju saintifik lima tahun (5-year arc generative AI).
- Risiko existential -- penaungan di UN Security Council (Sept 2026).
- "Pace the frontier" -- panggilan moratorium kelajuan.
- Penulis "Machines of Loving Grace" (2024), "The Adolesce of Technology."
- CEO, board director, Founding LLC member.
- 18j dolar personal compensation 2025.

*Daniela* memimpin:
- "Manage the senior leadership team" (Stanford eCorner Feb 2024).
- Operations, orang, risiko, strategik komersial.
- Board Chair (per CNBC IPO prospectus Sept 2026).
- President -- gelaran industri piawai Silicon Valley COO.
- 16.4j dolar compensation 2025.

*Lima nama lain tidak boleh disingkirkan*:
- *Tom Brown* -- Chief Compute Officer. Tanpa dia, model tidak boleh dilatih.
- *Jared Kaplan* -- bekas Chief Scientist; author scaling laws. Tanpa tesis ini, founder strategy hilang.
- *Sam McCandlish* -- teori scaling exponent.
- *Jack Clark* -- Head of Policy. Orang yang manages naratif diplomatik awam Anthropic.
- *Chris Olah* -- interpretability research lead. Scientific distinctiveness of Anthropic rests on this.

*Berlawan sam_altman.pdf*: dokumen sebelum ini nyatakan John Schulman dan Jan Leike "perpindahan kapabiliti" OpenAI ke Anthropic. Itu betul -- Schulman dan Leike ialah joined personnel, *bukan* pengasas. Kapabiliti OpenAI yang *paling penting* (GPT lineage) datang dengan Kaplan, McCandlish, Brown *sebelum* Schulman dan Leike.

#pagebreak()

#sect[04. OpenAI lineage dan keluar institusi]

*Tarikh*: Akhir 2020 -- awal 2021, tujuh orang keluar OpenAI beramai-ramai. Anthropic ditubuhkan Januari 2021, diumumkan Mei 2021 dengan 124j dolar Series A.

*Mengapa keluar (dengan bukti)*:
- Dario Amodei (CFR 11 Mac 2025): "we left at the end of 2020... scaling laws... if you take more computation and more data to train AI systems with relatively simple algorithms, they get better at all kinds of cognitive tasks across the board." Satu set percaya lebih awal berbanding majoriti OpenAI.
- Lex Fridman (Nov 2024): "It is incredibly unproductive to try and argue with someone else's vision." Penolakannya *bukan* Microsoft deal, *bukan* teknikal. *Vision*.
- Anthropic founding thesis: "the same organisation should be at the frontier and be focused on safety, because safety research needed the most capable models to study, and because someone at the frontier had to be."

*Bukti lineage dari OpenAI*:
- Ilya Sutskever -- GPT lineage -- Anthropic via Kaplan dan McCandlish (Scaling Laws).
- John Schulman (post-training PPO) -- Anthropic Ogos 2024 -- Thinking Machines Feb 2025.
- Jan Leike (Superalignment co-lead) -- Anthropic Mei 2024 (kini kepala alignment).
- Andrea Vallone (OpenAI model policy lead) -- Anthropic Jan 2026.
- *Tidak*: Sutskever (SSI), Mira Murati (Thinking Machines).

#pagebreak()

#sect[05. Dario Amodei: sumbangan dan autoriti yang disahkan]

*Latar belakang*:
- Caltech -- Stanford (BS physics) -- Princeton (PhD biophysics) -- Stanford Medicine postdoc -- Baidu -- Google Brain (senior research scientist) -- OpenAI VP Research (2016-2020) -- Anthropic CEO (2021-).

*Sumbangan saintifik yang disahkan*:
- Pemimpin usaha GPT-2, GPT-3, dan sebahagian besar safety research di OpenAI (Lex Fridman; CFR transcript).
- Mengarang majoriti OpenAI charter (TIME Perrigo, 30 Mei 2024).
- Penulis "Machines of Loving Grace" (2024) -- visi beneficial AI.
- Penulis "The Adolescence of Technology."
- Panggilan ke UN Security Council (Sept 2026).

*Fungsi autoriti hari ini*:
- CEO plus board director plus Founding LLC member.
- Chairman signatory pada Department of War statement (Feb 2026).
- Komunikasi dengan Three-letter agencies plus Pentagon.
- 18j dolar personal compensation 2025.

*Pemerhatian*: Dario's authority ialah *vocal dan scientific* plus commercial-execution-mediated. *Belum* ditunjukkan pada rekod keputusan yang *membatalkan* keputusan eksekutif terhadap CEO/desakan dolar. Documented exercised power: ASL-3 deployment (Mei 2025), refusal terhadap Pentagon fully-autonomous term (Feb 2026).

#pagebreak()

#sect[06. Daniela Amodei: sumbangan dan autoriti yang disahkan]

*Latar belakang*:
- BA UC Santa Cruz (English lit, politik, muzik).
- International development, congressional staffer, campaign work.
- Stripe awal (40 orang) -- recruiting -- risk operations.
- OpenAI 2018 -- VP Safety and Policy plus led People team and Research Engineering.
- Anthropic 2020 -- President and board chair.

*Fungsi autoriti*:
- Board Chair (pengumuman CNBC IPO prospectus Sept 2026).
- President (operasional harian, komersial, asas eksekutif).
- 16.4j dolar compensation 2025.

*Apa dia tidak*:
- Bukan "COO" secara tajuk -- "President" adalah jawatan umum Silicon Valley.
- Bukan *scientific director* -- itu fungsi Jared Kaplan (dahulu), masa depan tidak jelas.

*Test pasal "Dario mind / Daniela hands"*:
Daniela di Stanford (Feb 2024): "much more sort of practical kind of the business oriented side." Tapi dia BA humanities -- bukan "non-intellectual."

*Practical influence vs formal authority*:
- Formally: high (Board Chair and President).
- Practically: tinggi -- dia sehari-hari hold staff plus commercial plus board agenda.
- Boleh dia override Dario? Tiada bukti; IPO structuring (Founding LLC), Department of War letter -- co-signed.
- Boleh Dario override dia? Tiada rekod public.

#pagebreak()

#sect[07. Scar Ledger]

Definisi: SCAR ialah peristiwa institusi *yang disaksikan* dan *mengubah selection constraints masa depan*.

*SCAR-2021-FOUNDING*: 7 ex-OpenAI keluar awal 2021, membentuk Anthropic dengan thesis safety-first di frontier. *Behavior change*: ditubuhkan Public Benefit Corp dari hari pertama. *Verified*: ya. *Owner*: tujuh pengasas. *Status*: ACTIVE.

*SCAR-2022-CAI*: Constitutional AI paper (Bai et al., Dis 2022). *Behavior change*: Anthropic telah buat CAI-as-foundational-model-training siri. *Verified*: ya -- Claude model menggunakan constitution; updated untuk Claude 4/4.5. *Owner*: Yuntao Bai, Jared Kaplan dengan seluruh contributing authors.

*SCAR-2023-LTBT-LAUNCH*: Long-Term Benefit Trust ditubuhkan Sept 2023 dengan lima trustees. *Behavior change*: Trust appoints board majority sekarang (April 2026). *Verified*: ya. *Owner*: Neil Buddy Shah (chair), Matheny, Bahl, Christiano, Robinson awalnya.

*SCAR-2023-RSP-V1*: RSP keluar pada hari yang sama (Sept 2023). *Behavior change*: ASL-1..4 framework jadi operatif; ASL-3 activated (Mei 2025) dengan Claude Opus 4. *Owner*: Responsible Scaling Officer.

*SCAR-2024-LEIKE*: Jan Leike pindah ke Anthropic (Mei 2024). *Behavior change*: fokus alignment Anthropic bertambah. *Owner*: head of alignment team.

*SCAR-2024-WILMERHALE-TRUSTED-AUTHORITY*: Melalui sam_altman.pdf, lepas OpenAI Nov 2023 crisis, Anthropic governance design *didokumentasi* oleh Morley/Berger/Simmerman (HLS Forum 2023). *Behavior change*: rujukan untuk founder-LLC design di IPO.

*SCAR-2026-LTBT-LOSS-VACANCY*: Tino Cuellar pindah ke Anthropic Chief Global Affairs Officer Ogos 2026. *Behavior change*: Trust governing jadi 3 (designed 5). *Verified*: ya.

*SCAR-2026-PENTAGON*: Feb 2026, Anthropic tolak Pentagon demands. *Behavior change*: Dario's personal authority naik; bid prices stable tidak jatuh. *Verified*: ya.

*SCAR-2026-BARTZ*: 1.5b dolar copyright settlement (Julai 2026). *Behavior change*: largest copyright case settlement didokumentasi; 450j dolar bayaran terakhir belum selesai (per Eccles). *Verified*: ya.

*ARCHIVE-MURATI-COMPLAINT*: Testimoni Murati Mei 2026 tentang Dario -- behavior change *belum* dikesan.

*ARCHIVE-LATE-DEPARTURES-2025-2026*: 17 dilaporkan keluar, banyak dengan cyber-time window (Mac-Okt 2026), belum jelas sama ada ganti atau bocor keluar.

#pagebreak()

#sect[08. Shadow Register]

Definisi: SHADOW = kapabiliti/akibat/insentif yang *kurang kelihatan* oleh narrative pilihan institusi.

*SHAD-1: Safety branding vs frontier scaling*. Branding safety-first; scaling frontier model. ASL-3 only activated, ASL-4 threshold belum dilewati. Claude 5.5 dan Mythos ada. Cuaca teduh: scaling perimeter membesar lebih cepat dari ASL schedules.

*SHAD-2: Constitutional models vs mutable corporate authority*. Constitution: list of values integrated into training. Corporate authority: boleh amend constitution. *Tiada siapa* Amir dalam Anthropic yang secara langsung dapat *amend* constitution *between* model releases.

*SHAD-3: Public benefit vs private capital*. PBC, Foundation remain 26%. Cap table effect: 518b dolar compute obligations, ~80% non-cancelable (Reuters Sept 2026). Tension: beneficiary = shareholders in exits.

*SHAD-4: Interpretability claims vs limited legibility*. Chris Olah's programme *mendakwa*, ditiru oleh DeepMind, OpenAI. *Belum* : published proof full legibility.

*SHAD-5: Enterprise reliability vs autonomous-agent risk*. Anthropic sells Claude Code, Cowork, agentic products. Wildness dalam autonomous agents (Dario's own CFR framing) *kontra* "enterprise reliability."

*SHAD-6: Sibling coordination vs independent dissent*. 7 pengasas kekal muncul IPO dokumen (Sept 2026) *mengesahkan* coordinated posture, *bukan* independent challenge ke Dario/Daniela dari Founder LLC members.

*SHAD-7: Compute partnerships vs strategic dependence*. 221b dolar Google+Amazon commitments. Google 14% (capped 15%) plus Amazon 42.2b convertible + 32b preferred. Dua pelabur utama adalah juga vendor compute dan pesaing langsung.

*SHAD-8: Safety refusal vs national-security incentive*. Feb 2026 Anthropic held ground pada Pentagon. *Credible*, *documented*. *Bayangan*: apa jika UK, Israel, atau China membuat permintaan sama?

*SHAD-9: Mission preservation vs liquidity*. 7 pengasas "pledged 80% of personal Anthropic equity to charitable causes" (CNBC IPO prospectus). *Bayan*, *bukan* dikuatkuasakan.

*SHAD-10: Model constitution vs upstream provenance*. 1.5b dolar Bartz settlement Ogos 2026. *Real* failure: training data source disclosed. *Real* frictions: upstream constitutionalisation *tidak* menyelesaikan data provenance.

#pagebreak()

#sect[09. Lapan Paradox Tests]

*P1 Safety-Origin Paradox* (institusi sebagai correction jadi accelerator frontier). Anthropic scaling frontier Opus 5.5; ASL-3 akt. ASL-4 belum. Scaling law Kaplan-McCandlish co-authors memberi thesis. *Verdict*: PARTIAL.

*P2 Sibling-Governance Paradox* (trust increases coordination, weakens independent challenge). 7 pengasas kekal terkumpul ke IPO; cross-signature pada Pentagon dan IPO. Muatan terpisah unknown. *Verdict*: UNKNOWN.

*P3 Scaling Paradox* (knowledge enables scaling). publicly-verifiable. *Verdict*: PARTIAL.

*P4 Constitutional AI Paradox* (models governed by constitutions whose authors governed by corporate authority). CAI disusun internally; boleh amend constitution tanpa external disclosure otomatis. *Verdict*: CONTESTED.

*P5 Exit-to-Authority Paradox* (dissenters exit, become new authority). 7 OpenAI anti-commercial leakers plus Schuman, Leike ke Anthropic. Dario governing new firm. *Verdict*: PROVEN.

*P6 Safety-Capital Paradox* (safety requires compute; compute requires capital). 518b dolar obligation; customer concentration. Investor class AWS+GOOG is also vendor+competitor. *Verdict*: CONTESTED.

*P7 Interpretability Paradox* (lead interpretability research while deploying belum fully interpretable systems). *Verdict*: PARTIAL.

*P8 Public-Benefit Paradox* (PBC consider benefit tapi tidak prove benefit prevails). Tino quit trust->CGO. 4.6b dolar revenue 2025. 8b dolar operating loss. LTBT enforcement belum documented. *Verdict*: CONTESTED.

#pagebreak()

#sect[10. Constitutional AI -- siapa yang tulis constitution?]

Kertas asal (arXiv 2212.08073):
- *Corresponding authors*: Yuntao Bai, Jared Kaplan.
- *Co-authors*: 49 nama.
- *Method*: SL and RL with AI-generated critiques against principles.
- *Founding principle*: human supervision = list of rules.

*Siapa boleh amend constitution?*:
- Tiada external authority.
- Anthropic memutuskan bila update, tanpa public review otomatis.
- Claude's constitution (anthropic.com/research/claudes-constitution) sering di-amend antara rilis.

*Banding dengan dokumen undang-undang*:
- *Role*: constitution for *model behavior*, not for *organization*.
- *Sama siapa yang govern?*: Anthropic executive team.
- *Siapa boleh amend?*: Anthropic.
- *External disclose?*: untuk rilis besar, ya. Untuk tweak kecil, tak.

*Soalan*: apakah "constitutional AI" memberi organisasi democratic legitimacy? Tidak. Apakah ia restrains kelakuan model? *Sebahagian* -- model behaviour boleh diganggu dari training-quality issues (CAI paper acknowledges) -- unsolvable by constitution alone.

#pagebreak()

#sect[11. Long-Term Benefit Trust]

Sumber primer:
- anthropic.com/news/the-long-term-benefit-trust (Sept 2023)
- Harvard Law Forum (Morley/Berger/Simmerman, Okt 2023)
- 9to5AI (20 Okt 2026) -- Trust komposisi terkini.

*Struktur*:
- Class T stock.
- 5 trustees, *bertugas tahunan*, *independen* dari shareholders.
- Directors phased in: 1 hingga 3 (majoriti daripada 5) mengikut masa dan funding milestones.
- Protective provisions: notice (bukan veto) untuk "certain actions."

*Pemerhatian terkini (per 9to5AI Okt 2026)*:
- April 14 2026 -- Trust-selected directors majority.
- Ogos 4 2026 -- Tino Cuellar quit Trust untuk menjadi CGO. *Trust sekarang 3* (designed for 5).
- October 20 2026 -- Anthropic site lists Shah, Fontaine, Bernanke.

*Yang dipunyai oleh LTBT* (dokumen terbuka):
- Board appointment and removal (phased).
- "Approve pilihan of external reviewers" untuk RSP (per RSP v3.2).
- Consultation pada RSP changes (RSP v3.4).

*Yang dipunyai belum dikuatkuasakan*:
- Veto pada board decisions.
- Veto pada model release.
- Independent enforcement.

*Yang TIDAK dipunyai*:
- Public filing requirement.
- Penerimaan petition dari pekerja.
- Veto ke atas investment decisions.
- Override ke atas CEO dalam commercial conflicts.

*Falsifier*: jika Trust *pernah* elevate a board decision menentang CEO atau commercial pressure, itu *real* exercised power. *Belum berlaku*.

#pagebreak()

#sect[12. Board dan Executive authority]

Per IPO prospectus (Reuters plus CNBC):
- 6 board directors dari stok dan Trust election.
- Daniela: Board Chair (per CNBC).
- Trust: now elects majority (April 2026).
- Founders LLC: 50.1% undi (Class F share, satu saham).

Perkomposisi exact (Anthropic company page Okt 2026): Dario, Daniela, Yasmin Razavi, Reed Hastings, Chris Liddell, Vas Narasimhan.

*Tempoh fasa pasca-IPO yang kritikal*:
- 2 trilion dolar valuation menjadikan governance errors costly.
- Trust now independent, financial beneficiary 0%, akan menahan lebih banyak.

#pagebreak()

#sect[13. Capital dan Compute -- kebergantungan]

*IPO prospectus (Sept 2026)*:
- 518b dolar AI buildout over decade.
- 80% non-cancelable.
- 111b dolar ke Google, 110b dolar ke Amazon, 31.4b dolar ke Microsoft.
- 417b dolar total long-term commitments end 2025.
- 54.6b dolar non-cancellable hosting end 2025.

*Pelaburan dalam*:
- Amazon: 42.2b dolar convertible plus 32b dolar preferred.
- Google: ~14% straight equity (capped 15%).
- Microsoft: 5b dolar.
- Nvidia: 10b dolar.
- AMD equity alongside accelerator supply.

*Risiko structurally*:
- Vendor 1 (Google) = shareholder 14%.
- Vendor 2 (Amazon) = preferred plus convertible plus Bedrock distribution.
- 47% of revenue thru AWS Bedrock.

*Q3 2026 (per Reuters 14 Okt)*:
- Revenue 16.8b dolar, plus 45% QoQ.
- Q1 4.7b dolar, Q2 11.6b dolar.
- Annualised ~110b dolar EOY estimates.
- Operationally profitable on adjusted basis.

*Risiko*: Concentration in two vendors who are juga competitor dan investor. Customer concentration: 2 customers = 23%+ revenue (per FT analysis).

#pagebreak()

#sect[14. Authority Graph]

Laluan autoriti:
- *Shareholders* (majority public setelah IPO) lantik board.
- *Board of 6* -- Daniela (Chair, board director), Dario (CEO, board director), Trust-appointed (4 dari 6).
- *Long-Term Benefit Trust* (3 daripada 5 sekarang) -- Shah (Chair) plus Fontaine plus Bernanke. Cuellar (quit 8/4). 2 vacancies.
- *Founders LLC* (7 orang, bukan 2) -- 50.1% undi through Class F.
- *Researchers* (alignment, safety, capabilities) -- operational influence.
- *Compute partners* (AWS, GCP, Microsoft) -- vendor dependency.
- *Customers* (~47% via partner clouds) -- concentration.

#pagebreak()

#sect[15. Consequence Ledger]

- *Jan 2021 founding* -- Exit threatens "fresh start" -- Owner: 7 co-founders.
- *CAI paper Dec 2022* -- Methodology became foundational -- 49 co-authors.
- *LTBT launch Sept 2023* -- Institutional differentiator -- Initial Trustees.
- *Schulman joins Aug 2024* -- Capability inflow.
- *RSP v2 release Okt 2024* -- Policy structure evolve -- RSO.
- *Leike joins Mei 2024* -- Alignment strength -- Hiring plus Leike.
- *ASL-3 activation Mei 2025* -- Cybers plus CBRN context -- RSP deployment.
- *Tino joins trust Jan 2026* -- Governance refreshed -- Trust selection.
- *Tino->CGO Ogos 2026* -- Trust emptied to 3 -- Trust chair.
- *Dept of War refusal Feb 2026* -- Public commitment -- CEO statement.
- *DPA statement Mar 2026* -- Legal challenge -- CGO plus CEO.
- *1.5b dolar Bartz settlement Julai 2026* -- Largest copyright settlement -- Legal team.
- *IPO prospectus Sept 2026* -- Governance design tested -- Founders LLC.
- *Q3 2026 revenue 16.8b dolar* -- Sustainable scaling -- Operations.

#pagebreak()

#sect[16. OpenAI vs Anthropic]

*Founding governance*: OpenAI -- Nonprofit->PBC; Microsoft 27%; Foundation 26%. Anthropic -- PBC from day 1; Founder LLC 50.1%; LTBT picks majority.

*CEO authority*: OpenAI -- Bret Taylor chair board plus Altman CEO plus Murati CTO (after reshuffles). Anthropic -- Daniela board chair plus Dario CEO.

*Safety organs*: OpenAI -- Safety Committee di Foundation (Kolter SSC). Anthropic -- Responsible Scaling Officer plus LTBT advisory.

*Documented departures*: OpenAI -- Sutskever, Leike, Schulman, Murati, Zoph, McGrew, Vallone. Anthropic -- Schulman->TMM, Pobar+Bakhtin->Meta Superintelligence, Mrinank Sharma (Feb 2026).

*Compete on*: OpenAI -- Consumer ChatGPT plus Microsoft distribution; Agentic GPT-6 Astra. Anthropic -- Enterprise coding (Claude Code) plus agentic; Cowork; Mythos.

*Compute dependency*: OpenAI -- Azure (Microsoft); Stargate JV (stalled). Anthropic -- AWS plus Azure plus GCP; ~80% non-cancellable.

#pagebreak()

#sect[17. Cross-audit sam_altman.pdf]

Hipotesis ujian: "A corporation loses every safety mechanism when the people who built early alignment leave" (sam_altman.pdf).

*Diterapkan kepada Anthropic*:
- Capability keluar versus relocated? Relocated (Schulman, Leike, Vallone).
- Relocation preserve capability? Bercampur -- Schulman tak permanence (5 bulan), Mrinank Sharma keluar Feb 2026.
- Preserve authority? Tidak jelas -- Schulman tidak appointed at level matching original; Leike ialah contribution alignment.
- Anthropic institutionalize that capability? Ya -- safety research team plus RSP plus ASL framework.
- Mechanisms person-dependent or role-persistent? Role-persistent pada dokumen; person-dependent pada actually working team.
- Succession demonstrated? Tidak sepenuhnya.
- Trust can act if safety leaders depart? Tidak dapat diuji -- belum activated.

*VERDICT*: PARTIAL. Bukti: Institutional persistence mechanisms exist. Personnel persistence belum proven. Trust acting against founder pressure never tested.

#pagebreak()

#sect[18. Kontradiksi dikekalkan]

1. *Dario mind/Daniela hands* versus *Daniela BA humanities and 7-years operational*. Daniela secara eksplisit menolak dichotomized framing.
2. *Anthropic safer* versus *Anthropic ships frontier*. Dept of War refusal adalah satu kes.
3. *Trust sebagai checks-and-balances* versus *Tino->CGO* dan *7 founder kekal bersama* (Founder LLC 50.1%).
4. *Mission governance melalui PBC plus Trust* versus *518b dolar obligations plus 80% equity pledged charitable*.
5. *Citing Sept 2026 essay on UN Security Council* versus *training data settlement 1.5b dolar*. Same person yang witness existential risk.
6. *Constitutional AI comprehensive transparency* versus *corporate authority to amend without external comment*.

#pagebreak()

#sect[19. Falsification Queue]

Bilakah "Anthropic safer" hypothesis *akan* refutated:
- LTBT menentang secara terbuka Amodei keputusan komersial.
- 10% kes Claude produce outer harm.
- ASL-4 triggered *dan* Dario tolak release (atau, sebaliknya, release).
- Depart of War case filed against Trust.
- 2 customer concentration surpasses 35% revenue.
- Vendor basis (AWS/Google) recall capacity *dan* Anthropic reveal escalation.

Bilakah akan *diyakinkan*:
- Independent third-party evaluator reports full model legibility for Opus 5.5 dalam 18 bulan akan datang.
- Customers lebih 50% revenue direct (keluar dari partner-cloud concentration).
- Board chair Daniela consult Trust on non-aligned decision secara terbuka.

#pagebreak()

#sect[20. Constitutional Findings]

*CF-1*: "Amodei bersaudara saja yang founded Anthropic" -- *FALSE*. Tujuh pengasas.
*CF-2*: "Anthropic = safe option" -- *CONTESTED*. Struktural design *real*; enforced governance *belum exhibited*.
*CF-3*: "Trust 5 independent" -- *CONTESTED*. Design 5, currently 3. Cuellar->CGO transition. Quarterly integrity *currently degraded*.
*CF-4*: "Sibling dynamics produce trust" -- *PARTIAL*. Complementarity *real*, separation of power *belum* tested.
*CF-5*: "Capability lineage inherited dari OpenAI" -- *PROVEN*. Scaling laws plus 7 founding ex-OpenAI.
*CF-6*: "Constitutional AI restrains corporate authority" -- *CONTESTED*. Constitution governs model output, not corporate decisions.
*CF-7*: "Mission preservation through capital pressure" -- *CONTESTED*. Capital pressure real. Mission preservation mechanical through nonprofit plus Trust plus 80% pledge.
*CF-8*: "Anthropic stability pre-IPO versus post-IPO" -- *UNKNOWN*. November 2026 akan issuance some evidence.
*CF-9*: "Dario charisma plus Daniela operational = effective leadership" -- *PARTIAL*. Berkuat kuasa pada commercial scaling; *belum* pada conflict beyond exit.
*CF-10*: "De-facto two-person dominance" -- *CONTESTED*. Founder LLC ensures 7-vote minimum.

#pagebreak()

#sect[21. Open Questions]

1. Apakah Trust boleh menang IPO pre-IPO ini jika Founder LLC plus board majority founders menolak ASk?
2. Boleh LTBT memanggil external review dalam RSP v3.4 kalau Anthropic refuses?
3. Adakah Tino CGO pernah mempertahankan Trust *vs* Anthropic management pada apa-apa pun?
4. Apakah isi Founder LLC operating agreement? Adakah founder-veto manufacturer lain?
5. Dalam 2027, berapa percent Anthropic revenue akan Adobe, CDC, federal customer? Lurus atau tidak lurus dengan mission?
6. Adakah Anthropic akan jual Mistral, Cohere, atau bermitra dengan DeepSeek untuk kurangkan dependency ke AWS+Google?
7. Dalam kes ASL-4, adakah Anthropic akan release or Dario tak release?

#pagebreak()

#sect[22. Source manifest (retrieval 21 Okt 2026)]

*Primer*:
- anthropic.com/news/the-long-term-benefit-trust (2023-09-19)
- anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback (2022-12-15)
- anthropic.com/research/claudes-constitution (2023-05-09)
- anthropic.com/responsible-scaling-policy (latest v3.4)
- anthropic.com/company/leadership
- anthropic.com/news/activating-asl3-protections (2025-05-22)
- anthropic.com/news/announcing-our-updated-responsible-scaling-policy (2024-10-15)
- anthropic.com/news/statement-department-of-war (2026-02-26)
- anthropic.com/news/where-stand-department-war (2026-03-05)
- anthropic.com/news/ben-bernanke (2026-07-09)
- anthropic.com/news/national-security-expert-richard-fontaine (2025-06-07)
- arXiv 2212.08073 -- Constitutional AI (Bai et al. 2022)
- arXiv 2001.08361 -- Scaling Laws (Kaplan et al. 2020)

*Harvard Law / Lawyer analysis*:
- corpgov.law.harvard.edu/2023/10/28/anthropic-long-term-benefit-trust/ (Morley/Berger/Simmerman)
- harvardlawreview.org/print/vol-138/amoral-drift-in-ai-corporate-governance/

*Profil / biografi*:
- TIME (Perrigo, 2024-05-30): "How Anthropic Designed Itself to Avoid OpenAI's Mistakes"
- TechCrunch (2024-05-28): Anthropic hires Jan Leike
- Lex Fridman (#452 Dario Amodei, 2024-11-11)
- Stanford eCorner (Daniela, Feb 14, 2024)
- CFR CEO Speaker Series (Dario, 2025-03-11)
- CBS News (Dario interview, 2026-02-28)
- Fortune (2023-09-26, 2026-06-04)
- CNBC (2026-09-29): Founder LLC, Bernanke

*Laporan*:
- Reuters (2026-02-26 ... 2026-10-15)
- CNBC (2026-01-20, 2026-04-24, 2026-09-29)
- NPR (Pentagon standoff)
- AP (Pentagon standoff)
- NYT (Pentagon standoff)
- The Verge (2026-04-08, 2026-09-29)
- The Decoder (2026-10-15)
- Fortune (2026-09-29 IPO losses)
- TechCrunch (joint eval Aug 2025; Vallone Jan 2026)

*Safety ledger*:
- OpenAI+Anthropic joint safety evaluation (2025-08-27)
- Berkeley CLTC (2026-04) GPAI Profile assessment
- 9to5AI (2026-10-20): LTBT komposisi terkini
- AIwiki LTBT analysis
- Robert Eccles "Anthropic Before the Prospectus" (Okt 2026)

*Departures*:
- Business Insider plus CNN (Feb 2026) -- Mrinank Sharma
- freed.tools/en/pages/anthropic-resignations (Sept 2026)
- The Verge plus TechCrunch -- Leike (May 2024), Vallone (Jan 2026), Schulman (Feb 2025)

#pagebreak()

#sect[Satu pelajaran boleh guna semula]

Dari corak dokumen yang kekal selepas audit:

#align(center)[
  #block(fill: luma(245), inset: 12pt, radius: 3pt, width: 90%)[
    #text(size: 10.5pt)[
      Pelajaran: *Governance architecture diuji berdasarkan apa yang dipaksakan
      olehnya, bukan apa yang dijanjikannya. Anthropic's Long-Term Benefit
      Trust plus Founder LLC plus PBC plus 80% equity pledge plus ASL-3 RSP
      activation plus Department of War refusal = structural design that
      *might* constrain founder authority. Struktur hanya belajar apabila
      *digunakan* terhadap commercialization pressure yang sebenarnya. Saat
      itu belum tiba. Serta "moral philosophy" of governance hanya boleh
      dibuktikan pada saat *membebankan konsensus founder* yang terbuka.*
    ]
  ]
]

#v(0.6cm)

#align(center)[
  #text(size: 9pt, style: "italic")[
    Verdict HOLD -- pendirian F13 menunggu pengajian manusia lanjut.
    Dokumen ini ialah rekod bukti yang bersedia untuk dibaca dengan
    mata terbuka, bukan bicara atau keputusan yang memutuskan apa
    Anthropic ialah atau tidak.
  ]
]
