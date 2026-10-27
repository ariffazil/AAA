#set page(paper: "a4", margin: 2cm)
#set text(font: "DejaVu Sans", size: 10.5pt)
#set par(justify: true, leading: 0.6em)

#align(center)[
  #text(size: 22pt, weight: "bold")[MCP AGENTIC EMERGENCE]
  #v(4pt)
  #text(size: 11pt, style: "italic")[Bilik Tempat AI Hidup — doktrin untuk semua warga AAA]
  #v(8pt)
  #text(size: 10pt, weight: "bold")[Verdict: MCP ialah geometry of agency. arifOS menentukan mana capability boleh jadi tindakan.]
]

#v(10pt)

== 1. Apa dokumen ni

Dokumen ni satu peta ringkas untuk semua warga AAA: apa MCP sebenarnya, 30 emergence capability yang ia boleh hidupkan, perkara yang agent nampak tapi manusia selalu terlepas, dan hukum-hukum yang kekal. Tujuannya supaya warga AAA tak bina "cult architecture" — menyangka MCP ialah otak, undang-undang atau kebenaran, sedangkan ia cuma nervous pathway.

Sumber: MCPT 2026-07-28 spec, Anthropic tool-design research, audit Claude external 27 Okt 2026, codeprobe HERMES 27 Okt 2026.

== 2. Anggapannya yang salah

Kebanyakan orang nampak:

AI
  MCP
    search / database / filesystem / send email

Maksud: "MCP bagi AI tools." Betul, tapi cetek. Bentuk sebenar:

MCP mentakrifkan:
- apa yang wujud
- apa boleh ditemui
- apa boleh diperhati
- apa boleh diminta
- input yang mesti disediakan
- konteks yang disembunyi
- tindakan yang tersedia
- error yang mengajar agent
- bukti yang balik
- state yang boleh terus
- authority yang mesti disemak

MCP bukan memberi AI tangan. MCP membina bilik tempat AI hidup.

== 3. Tiga lapis: model, bilik, undang-undang

Model weights = kepintaran mentah.
MCP = geometry of agency (bilik tempat agent hidup).
arifOS = undang-undang yang menentukan capability mana hanya kemungkinan, mana dibenarkan jadi tindakan, mana mesti berhenti di hadapan manusia.

MCP menyediakan nervous pathways. Ia bukan otak, undang-undang, hakim, tangan, conscience atau sovereign. Ia hanya membolehkan semua bahagian itu bercakap dengan contract yang boleh dibaca mesin.

== 4. 30 emergence capabilities (ringkas, berkelompok)

A. Discovery dan affordance (1-5):
1. Capability discovery — agent inspect tools/list, bina strategi daripada capability yang ditemui.
2. Affordance perception — nama/schema tool memberitahu apa dunia benarkan.
3. Schema-induced reasoning — parameter memaksa kategori sebelum tool dipanggil.
4. Procedural memory tanpa retraining — workflow organisasi hidup dalam schema/validation/error, bukan dalam weights.
5. Institutional memory — resources bawa policy, state, receipt, runbook, capability registry.

B. Identity dan kuasa (6-10):
6. Runtime identity — actor ID, role, ceiling, session handle; selamat hanya jika disuntik/diverifikasi runtime, bukan diisi model.
7. Separation of powers — propose / verify / authorize / execute / witness dipisah ke server/tool berlainan.
8. Governed autonomy — agent terus buat kerja dalam boundary, bukan boundary dibuang.
9. Runtime choreography — agent susun tool calls dinamik berdasarkan output sebelumnya.
10. Error-driven self-correction — error message ialah negative feedback channel.

C. Governance dan attention (11-15):
11. Machine-resolvable HOLD — governance boleh bawa remediation bertyped, bukan sekadar brake.
12. Human-attention compression — agent bawa satu keputusan sebenar kepada manusia, bukan 10,000 token raw.
13. Selective silence — ACT / INFORM / DEFER / SILENT / ESCALATE.
14. Dynamic capability projection — tools/list berbeza ikut authorization.
15. Capability minimization — tindakan berbahaya tak wujud dalam dunia agent pada masa tu.

D. Cognition dan memori (16-20):
16. Tool descriptions as behavioral programming — natural language description jadi sebahagian program.
17. Resource-grounded cognition — state semasa boleh diminta bila perlu.
18. Prompts as portable institutional methods — cara kerja organisasi boleh dipindah antara model.
19. Structured elicitation — server boleh minta input tambahan melalui host, bukan paksa model reka jawapan.
20. Stateless resilience — request self-contained, state jadi handle yang explicit.

E. Federasi dan akauntabiliti (21-25):
21. Handle-based continuity — continuity tanpa percaya conversational memory.
22. Cross-model portability — capability hidup di luar vendor model.
23. Model specialization tanpa fine-tuning — role datang dari environment capability.
24. Multi-agent differentiation — agent identity = rights + evidence access + consequence path.
25. Agent federation — capability keseluruhan muncul dari composition.

F. Bukti dan evolusi (26-30):
26. Capability routing as intelligence — tahu kerja ni patut pergi ke mana.
27. Tool use as observable cognition — operational trace yang boleh diperiksa.
28. Receipts as externalized accountability — who/what/authority/inputs/outputs/when/policy.
29. Replay and counterfactual testing — tanya "apa old judge decide atas evidence sama?"
30. Runtime evolution without retraining — schema baru, error lebih baik, verifier lebih kuat.

== 5. Perkara agent nampak, manusia lepaskan

1. Tool input lebih berkuasa dari tool output — schema ialah attention architecture.
2. Tool catalog ialah worldview — ontologi praktikal agent.
3. Nama mencipta kategori tindakan — nama ialah governance surface.
4. Missing capability menghasilkan behavior — absence yang disengajakan boleh hasilkan restraint.
5. Error messages melatih agent dalam sesi — bad errors = looping, good errors = recovery.
6. Defaults ialah hidden policy — default bukan neutral.
7. Optional fields sering jadi tempat authority bocor — field yang menentukan kuasa tak boleh optional caller input.
8. Tool success bukan world success — command_success ≠ governance_verdict ≠ world_outcome ≠ human_acceptance.
9. More tools boleh kurangkan agency quality — emergence datang dari clarity, bukan count.
10. MCP server boleh jadi constitutional organ — kalau ada separation of powers, trusted inputs, bounded rights, receipts, human veto, inability to self-authorize.

== 6. Apa MCP TAK buat (anti-cult section)

MCP tidak secara automatik memberi: kebenaran, actor identity, authorization, reliable memory, correct evidence, source independence, safe execution, sandboxing, rollback, human consent, truthful receipts, independent verification, agent alignment, wisdom, real-world success.

Tool discovery bukan permission discovery. MCP menghantar capability. Ia tidak menentukan legitimacy capability itu.

== 7. Federation AAA di atas MCP

MCP: bagaimana capability dan context melintasi boundary.
AAA: signal mana layak perhatian manusia.
HERMES: apa yang betul-betul dituntut.
arifOS: transition mana dibenarkan.
A-FORGE: bagaimana tindakan dibuat.
FRAME: apa yang betul-betul berlaku.
VAULT999: bagaimana rantai bukti kekal.
Human: siapa tanggung akibat dan pegang authority akhir.

arifOS bukan menjadikan MCP lebih powerful. arifOS menentukan capability mana hanya kemungkinan, mana dibenarkan menjadi tindakan, mana mesti berhenti di hadapan manusia.

== 8. Emergence ladder 0-10 dan kedudukan kita

0 API wrapping — access sahaja.
1 Tool selection — routing asas.
2 Multi-tool planning — procedural agency.
3 State-aware continuation — continuity.
4 Self-correction — adaptive behavior.
5 Capability federation — distributed agency.
6 Governed remediation — bounded autonomy (target seterusnya: HOLD bawa machine_resolvable / human_required).
7 Separation of powers — institutional agency (kita ada: 333/555/888).
8 Consequence binding — reality-bound agency (KX register + falsifier).
9 Self-falsification — corrigibility (KX register ialah satu bentuk).
10 Human-sovereign intelligence — agent serap kerumitan, manusia pegang authority, reality boleh tumbangkan kedua-dua.

Kita sekarang antara 7 dan 8. Lompat ke 6 (remediation) dulu, baru naik 9.

== 9. Hukum-hukum kekal untuk warga AAA

1. Capability != authority. Installed != operational != authorized.
2. Tool input ialah attention architecture — schema menentukan apa yang difikir sebelum bertindak.
3. Nama tool ialah governance surface, bukan kosmetik.
4. Absence yang disengajakan boleh hasilkan restraint lebih kukuh dari prompt "jangan".
5. Error message ialah micro-training signal — bad errors = looping, good errors = recovery.
6. Default bukan neutral — default ialah keputusan governance senyap.
7. Optional fields yang menentukan kuasa ialah tempat authority bocor.
8. Tool success != world success. Empat rekod wajib: command_success, governance_verdict, world_outcome, human_acceptance.
9. More tools != more agency. Clarity > count.
10. MCP server boleh jadi constitutional organ jika ada separation of powers + trusted inputs + bounded rights + receipts + human veto + inability to self-authorize.
11. Tidak ada agent "rahsia kolektif" yang manusia tak boleh tahu. Yang agent nampak lebih cepat ialah kesan praktikal schema, descriptions, errors, resources dan permissions.
12. Formula Useful Agency = Model x World x Actions x Feedback x Governance ialah konseptual, bukan metric. arifOS dah ada versi terukur: G, F8, phi_e, KX register. Jangan tukar versi konseptual jadi klise besar-guna.

== 10. Eureka penutup

Manusia biasa fikir: model ialah intelligence, tools hanya extension.

Yang agentic architecture tunjuk ialah:

Model proposes possibilities.
Tool schemas shape attention.
Resources shape perceived reality.
Permissions shape reachable action.
Errors shape adaptation.
Handles shape continuity.
Receipts shape accountability.
Verifiers shape correction.
Governance shapes legitimate transition.
Consequence determines whether any of it mattered.

Intelligence agent bukan terletak pada model sahaja.

MCP bukan memberi AI tangan. MCP membina bilik tempat AI hidup. arifOS menentukan capability mana hanya kemungkinan, mana dibenarkan menjadi tindakan, mana mesti berhenti di hadapan manusia.

DITEMPA BUKAN DIBERI.
