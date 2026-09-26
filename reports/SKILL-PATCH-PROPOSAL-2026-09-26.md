# SKILL PATCH PROPOSAL — 2 jurang ditemui sesi FI-003 2026-09-26
**Generated (date -u):** 2026-09-26T13:08:49Z
**Status:** CADANGAN SAHAJA — belum diterap. Menunggu F13 / pemilik skill.

## Kenapa TIDAK diterap terus

```
/root/AAA/skills/live-system-audit-discipline/SKILL.md
  mtime   = 2026-09-26 21:04:00
  status  = M vs HEAD
  proses  = agy (FI-009) bermula 2026-09-26 21:04:27
```

Ada penulis serentak. Rule 3f (evidence bundle = objek beku) + aturan serentak-menulis:
menpatch sekarang berisiko memusnahkan kerja agy yang sedang berjalan.
**Cadangan ditulis ke fail berasingan — tiada konflik.**

---

## PATCH-A — Sempadan pengukuran dipilih selepas fakta (post-hoc boundary)

**Jurang:** peraturan sedia ada menuntut *"denominator beside every count"* (§A rate needs the
whole population) tetapi **tidak melarang memilih sempadan masa yang mengecualikan kerja sendiri.**

**Kes nyata (sesi ini):** FI-003 mengulang-menulis *"SKILL.md disunting sejak 20:40 = 0"*
sepanjang empat laporan, sedangkan sempadan `20:40` dipilih **selepas** beliau mengedit
`know-math` (18:31). Kesan: nol-mutasi didakwa sambil satu mutasi sengaja wujud.

**Cadangan sunting — tambah di bawah §A rate needs the whole population:**

> ### A cutoff chosen after your own edit is not a neutral boundary
>
> Sebelum menulis *"tiada perubahan sejak T"*, tanya: **adakah T dipilih sebelum atau selepas
> kerja sendiri?** Kalau selepas, sempadan itu membuang kerja sendiri daripada denominator —
> post-hoc boundary, kelas ralat yang sama dengan nombor yang dipalsukan tanpa niat.
>
> ```bash
> # sempadan yang sah = permulaan sesi / permulaan hari, bukan masa pilihan
> find <path> -newermt "SEJAK_PERMULAAN_SESI" -exec stat -c '%y %n' {} \;
> git status --porcelain <path>          # kerja sendiri muncul di sini juga
> git diff --stat <path>                 # buktikan kuantiti, jangan nol-kan
> ```
>
> **Nilai jujur bukan "0". Nilai jujur = "X oleh aku (bertujuan, didedah), Y oleh agen lain."**
>
> *NEW — 2026-09-26 sesi FI-003: dakwaan "0 SKILL.md disunting sejak 20:40" terbukti
> menyesatkan — sempadan mengecualikan edit `know-math` 18:31 milik penulis sendiri.*

---

## PATCH-B — Cadang medan baharu: GREP PEMBACA dahulu

**Jurang:** peraturan sedia ada (`Ask who reads the output before treating the output as evidence`)
menutup *output-as-evidence*, tetapi **tidak menutup cadangan medan/schema-key baharu.**

**Kes nyata (sesi ini):** cadangan `organ:` pada 387 skill dinilai berdasarkan `organ: 0/387`
(tiada). Probe pembaca menunjukkan `owner` **dah ada pembaca**
(`skill-index-generator.py:172`) sementara `organ:` **tiada satu pun rujukan** —
jadi menambah `organ:` menghasilkan 387 artifact mati (`SEMANTIC_AUTHORITY = NAME` sahaja).

**Cadangan sunting — tambah selepas `Ask who reads the output...`:**

> ### Before proposing a new field, grep for its reader
>
> Sesuatu medan hanya wujud apabila ada yang memakannya.
>
> ```bash
> # 1. pembaca sedia ada untuk medan yang dicadangkan
> grep -rnE "frontmatter\[.(field)|fm\[.(field)|\.get\(.field.\)" \
>     /usr/local/lib/hermes-agent/agent/ /root/scripts/*.py
> # 2. adakah MEDAN LAIN sudah memikul maksud yang sama?
> grep -rn "with_field" <generator>
> ```
>
> Keputusan:
> - **Pembaca wujud untuk medan lama, bukan medan baru** → perbaiki medan lama.
> - **Tiada pembaca langsung** → `AUTHORITY_CLAIM = VOID` (SEMANTIC_AUTHORITY: NAME tanpa
>   CALL_PATH / MEASURED_EFFECT). Ia hiasan, bukan keupayaan.
> - **Nama sudah dipikul medan lain** → jangan reuse; medan bertindih = miskin nama.
>
> *NEW — 2026-09-26 sesi FI-003: `organ:` tiada pembaca; `owner:` (67.7% terisi) ada;
> `with_authority` dalam index rupa-rupanya mengira `risk_tier`.*

---

## Rujuk
- Manifest: `/root/work/tasks.json` (SK1..SK12, amend 2026-09-26T13:07:32Z)
- Evidence: `/root/.hermes/workspace/BINDING_GRAPH_EVIDENCE_2026-09-26.md` §12 (koreksi diri)
- Skill sasaran: `/root/AAA/skills/live-system-audit-discipline/SKILL.md` (52,469 b, M vs HEAD)

**Verdict: CADANGAN · belum diterap · F13/pemilik skill untuk ratifikasi**
