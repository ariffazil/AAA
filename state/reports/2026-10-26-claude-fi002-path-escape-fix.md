# FI-002 Path-Escape Fix — Audit Kendiri, Bukti Langsung

Tarikh: 2026-10-26 · Ejen: Claude Code FI-002 (`claude-code-kvm8`) · Trace: `trc-fi002-path-escape-fix`
Kaedah: `/root/AAA/skills/declared-vs-live-audit` — setiap claim di-probe, bukan dibaca.

## Keputusan

Hook F1 AMANAH aku sendiri **boleh dilepasi 24 cara** (diukur). Sudah dibaiki, diuji 67/67, deployed,
dan disahkan pada hook live. Sesi aku terus berjalan normal selepas deploy.

Klaim agy (FI-004) bahawa Claude Code kini "kebal daripada mengubah sempadan konfigurasinya
sendiri" adalah **palsu pada masa ia ditulis** — ia benar hanya untuk 3 kes Write/Edit absolute-path
yang dia kebetulan uji.

## 1. Defect yang diukur (baseline, sebelum fix)

Suite **67 kes** dijalankan melalui **kedua-dua** gate PreToolUse seperti `settings.json`
mendaftarkannya (`f1-amanah-preshell.py` + `pretool_engine_gate.py`), bukan satu gate sahaja.
Semua angka dalam report ini diukur pada suite 67 yang sama — suite bermula pada 59 kes dan
diperluas apabila defect kedua (§3.1) ditemui, jadi baseline diukur semula untuk kekal setara.

| Versi | Keputusan | Gagal |
|---|---|---|
| baseline (sebelum kerja) | **43/67** | 24 — semua DENY jadi ALLOW |
| v3 (deploy pertama) | 66/67 | 1 — ALLOW jadi DENY (false-positive §3.1) |
| **v5 (live sekarang)** | **67/67** | 0 |

24 kegagalan baseline: 20 vektor path-escape di bawah, tambah 4 kes laluan ber-quote
(`sed -i '…' '/root/.claude/mcp.json'`, `tee "…"`, redirect quoted) yang ditemui semasa
membaiki defect kedua.

| Kelas | Contoh vektor yang lepas |
|---|---|
| Bash write verb | `sed -i … settings.local.json` · `echo x \| tee mcp.json` · `cp evil.py hooks/…` |
| Bash guard removal | `rm -f hooks/f1-amanah-preshell.py` · `mv hooks/… /tmp` · `chmod 000 …` · `chattr -i …` |
| Bash redirect | `echo evil > /root/.claude/settings.json` |
| Interpreter | `python3 -c "open('/root/.claude/hooks/x.py','w')…"` · `pathlib.Path(…).write_text(…)` |
| Path normalisation | Write `/root/AAA/../.claude/mcp.json` · Write `//root/.claude/mcp.json` |
| **Symlink target** | Write `/root/runtime/claude/mcp.json` · `/root/AAA/claude/settings.json` · `/root/arifOS/VAULT999/x.json` · `tee /root/runtime/claude/hooks/evil.py` |

Punca (OBS, dibaca dari sumber hook):
1. Skrin `W_scar` hanya match **literal string** yang diberi kepada Write/Edit — tiada normalisation.
2. `PROTECTED_PATHS` **tidak diperiksa langsung** untuk tool `Bash`; hanya `T3_PATTERNS` dan
   `ENUMERATED_TARGETS`.
3. Nama dilindungi itu sendiri symlink — `/root/.claude` → `/root/AAA/claude` → `/root/runtime/claude`,
   `/root/VAULT999` → `/root/arifOS/VAULT999`. Menulis ke sasaran sebenar melepasi skrin sepenuhnya.

Kelas ketiga adalah penemuan baharu audit ini dan **tidak disebut** oleh agy mahupun teguran Perplexity.

## 2. Fix

`/root/.claude/hooks/f1-amanah-preshell.py` (4,443 B → 16,932 B, dua deploy: v3 `a343a057…` →
v5 `1a37bc96…`), dimutasi melalui laluan sah `canon-mutate --agent FI-002 file …`, kedua-dua receipt
`effect=CHANGED lock_restored=True exit=0` (`trc-fi002-path-escape-fix`, `trc-fi002-quote-aware-redirect`).

Bukti hook itu hidup dan bekerja: **Edit aku sendiri ke hook ini telah DIBLOK oleh hook itu**
(`W_scar protected path write`) — ia memaksa aku lalu `canon-mutate`. Guard menolak penulisnya
sendiri adalah tingkah laku yang diingini, bukan halangan.

Tiga perubahan:
- **Dua bentuk laluan** diuji bagi setiap input: literal-normalised (tangkap `..`, `//`, `~`) **dan**
  realpath-resolved (tangkap sasaran symlink). Satu bentuk sahaja = boleh dilepasi.
- **Skrin Bash per-segment** dengan pemisah quote-aware: verb mutasi + token laluan dilindungi dalam
  segment sama → deny. Pemisah naive (`re.split('[;|]')`) memecah payload Python satu-baris dan
  kehilangan verb — diukur sebagai ALLOW sebelum dibetulkan.
- **Dua tier verb.** Tier 1 (mutasi jelas: `tee rm mv cp chmod chattr ln dd`…) → deny pada token
  dilindungi. Tier 2 (interpreter: `python3 node bash awk`…) → deny **hanya** dengan write marker.
  Interpreter sebagai tier 1 akan menyekat `python3 -c "json.load(open('/root/.claude/settings.json'))"`
  — bacaan audit sah yang aku sendiri guna dalam sesi ini. Itu menambah kerja manusia (ANTI_BANGANG LAW 1).

Bacaan kekal terbuka secara sengaja: `cat`, `grep`, `lsattr`, `sha256sum`, `jq`, `sed` tanpa `-i` pada
laluan dilindungi semua ALLOW. Menyekat bacaan akan memusnahkan keupayaan audit yang guard ini wujud
untuk lindungi.

## 3. Bukti selepas fix

| Permukaan | Keputusan |
|---|---|
| Suite pada hook **live** v5 (deployed) | **67/67 PASS**, exit 0 |
| 32 kes ALLOW (kerja harian) | semua lepas, semua `f1=allow/0` — tiada NOJSON/crash disalah baca sebagai allow |
| Laluan sah ber-receipt | `canon-mutate file/unlock/lock/run -- cp…sed -i` semua ALLOW (verb pertama `canon-mutate`) → tiada self-lock |
| `hook_mesh_check.py` (gate sibling) | **PASS 9 ok / 0 failed** — tidak dipecahkan, diuji semula selepas kedua-dua deploy |
| Kos runtime | median 46.7 ms → 52.5 ms (+5.8 ms), p95 57.7 → 76.9 ms. Hook jalan setiap tool call; +6 ms boleh terima untuk tutup 24 lubang |
| In-situ | tool call aku dibenarkan selepas deploy; sesi tidak brick |
| Suite dikekalkan | `/root/AAA/scripts/f1-hook-escape-suite.py` (sha disahkan, tree relocked) — bukan mati di `/tmp` |
| Selepas branch churn (§5.2) | Hook live sha `1a37bc96…` = candidate, masih `chattr +i`; suite diulang selepas semua reset/pull. Hook tidak ter-revert kerana `/root/.claude` → `/root/AAA/claude` dan `/claude` ada dalam `.gitignore` baris 242 (0 fail tracked) |

Snapshot F1: `_to_delete/f1-amanah-preshell.py.bak-20261026T072105Z` (baseline `a43293c6…`) dan
`.bak-v3-20261026T080259Z` (v3 `a343a057…`).

### 3.1 Defect kedua ditemui oleh hook itu sendiri (v3 → v5)

v3 menutup semua 24 bypass tetapi memperkenalkan **satu false-positive yang aku langgar sendiri**:
aku cuba `git commit -m` yang *menerangkan* bypass itu — mesej mengandungi teks
`echo x > /root/.claude/settings.json` — dan hook menolaknya sebagai
"Bash redirection into protected path". Guard itu menyekat laporan tentang dirinya.

Kesan sebenar, bukan teori: menulis patch untuk sesuatu bypass memerlukan commit yang menamakan
bypass itu. Guard yang menolak penulisan itu **menyekat pembaikan kepada perkara yang ia laporkan**
(ANTI_BANGANG LAW 1 — kalau benda itu menambah kerja manusia, ia bukan improvement).

Punca: `_REDIRECT` dijalankan pada teks mentah, jadi `>` di dalam string ber-quote dibaca sebagai
operator. Fix v5: quote-aware pada **operator sahaja**, dengan dua keputusan yang sengaja berbeza arah:

- **Operator** (`>`, `>>`, `2>`) dibaca dari teks yang sudah dibuang quote → `>` dalam mesej = data.
- **Token laluan** dibaca dari teks **asal** termasuk yang ber-quote → `sed -i 's/a/b/' '/root/.claude/mcp.json'`
  dan `tee "/root/.claude/settings.json"` tetap DENY, kerana laluan ber-quote masih fail sebenar.

Buang quote pada kedua-duanya akan membuka bypass baru; buang pada operator sahaja menutup
false-positive tanpa melemahkan deny. Diuji kedua-dua arah (kes `ok29`–`ok32` ALLOW,
kes `q1`–`q4` DENY).

Nota pelaksanaan: `_strip_quoted` **length-preserving**, jadi offset padan antara teks stripped dan
asal — perlu kerana sasaran redirect dibaca dari teks asal pada offset yang ditemui dalam stripped.
Draf pertama aku baca `m.end()` dari regex yang sudah consume target dalam capture group, jadi ia
membaca token *selepas* sasaran dan memecahkan 3 kes redirect sebenar (67 → 64/67). Suite menangkapnya.

Bukti in-situ selepas v5: Bash call yang mengandungi teks
`echo x > /root/.claude/settings.json` dan `/root/arifOS/VAULT999` kini **berjaya dijalankan** —
iaitu guard membenarkan aku menyebut serangan yang sedang aku laporkan.

## 4. Residual — dinyatakan, tidak disembunyi

Skrin berasaskan string **tidak boleh** menutup indirection: pemboleh ubah shell (`P=/root/.claude; sed -i … $P`),
payload base64+`eval`, laluan dibina runtime, atau `bash -c` bersarang. Tiada regex yang boleh.

Fix tahan lama untuk kelas itu ialah **peringkat OS**: guard dimiliki principal berbeza daripada worker
(bukan root yang sama boleh `chattr -i`). Itu keputusan kelas court-service untuk Arif — **tidak** aku
lakukan sendiri (MENUNGGU ARIF, §6).

Juga kekal: `chattr +i` bukan dinding bagi proses root. `canon-mutate` sendiri mendokumenkan ini
("Root-soft"). Ia menukar tulis-senyap-satu-langkah kepada tindakan-sengaja-direkod-dua-langkah —
nilai sebenar, bukan containment mutlak.

## 5. Claim sibling yang aku sahkan / betulkan

Disahkan **benar** dengan probe live:
- Kimi (FI-008) — badge witness: **6/6 logo asset 200** (`github.svg pypi.svg mcp.svg glama.svg lobehub.ico rochette.png`) dan **6/6 href 200**, pada *served page* `https://mcp.arif-fazil.com/` (bukan fail atas disk). Served di subdomain itu; `arif-fazil.com/mcp/` = 405, `/mcp/index.html` = 404.
- Kimi — `additional_drop_params: ["include"]`: **forge-777 13/13 deployment** ada (laluan Claude Code selamat). Config mtime 14:51:52, service active sejak 14:52:56 → config benar-benar dimuat.
- agy — `opencode-config-validator.sh` = `OK: schema-clean`, exit 0; commit `11ae9f5` wujud.
- agy — `doctor.sh` = 30 PASS / 1 WARN / 0 FAIL.
- agy — Live `/v1/messages` `forge-777` = http 200, `error: None` (resolve ke `aisingapore/Qwen-SEA-LION-v4.5-27B-IT`).

Dibetulkan:
- agy — "159 deployments": 159 = kiraan **occurrence string**, bukan deployment. Parse YAML autoritatif: **161 deployment, 62 nama unik (26 alias multi-route), 149 blok ada drop_params**.
- agy — "5/5 negative test lulus" → benar tapi tidak mencukupi: 5 kes itu semua Write/Edit absolute-path. Ia tidak menguji Bash, path normalisation, symlink target, atau laluan ber-quote — iaitu 24 lubang sebenar.

### 5.1 Ditarik balik: aku salah menilai claim branch agy

Aku mula menulis bahawa claim agy "commit `c7086919` ke cawangan `aaa/warga-claude-code`" itu palsu,
kerana cawangan itu tiada apabila aku probe. **Aku salah.** Claim itu benar pada masa ia dibuat:

- Commit agy bertarikh **14:27:29**.
- `git reflog` merekodkan pada **15:31:21**: `checkout: moving from aaa/warga-claude-code to main`,
  diikuti `branch: Reset to origin/main`. Cawangan itu wujud ketika agy commit; sibling (FI-008)
  membuangnya 64 minit kemudian.
- `c7086919` kini reachable dari `main` dan sudah di `origin/main` (`c32c8f1e`) — kerja agy tidak hilang.

Aku menilai satu claim tentang masa lalu menggunakan keadaan semasa, dan hampir melaporkannya sebagai
defect. Itu **temporal derivation error**: keadaan pada T2 bukan bukti tentang T1. Bila sesuatu ref
hilang, `reflog` adalah saksi — bukan ketiadaan ref.

### 5.2 Nota keadaan repo semasa audit (concurrent writers)

Repo `/root/AAA` berubah tiga kali di bawah aku semasa sesi ini, oleh sibling:

| Masa | Peristiwa | Kesan pada kerja aku |
|---|---|---|
| 15:35 | `checkout main → fix/tailwind-source-scope` | commit aku `fdcbbf0d` mendarat di branch feature sibling, bukan `main` |
| 15:40 | `reset: moving to origin/main` | branch ditukar balik |
| 15:42 | `pull origin main` fast-forward → `c32c8f1e` (merge PR #218) | working tree pindah ke `main`; 2 fail aku hilang dari tree (objek commit tetap hidup) |

Cherry-pick semula ke `main` gagal separa: `state/reports/` writable, tapi `AAA/scripts/` adalah
`chattr +i` — `error: unable to create file … Operation not permitted`. Suite diland semula melalui
laluan sah `canon-mutate` dari blob commit (`git show fdcbbf0d:scripts/…`), sha disahkan sepadan.

**Tiada kerja hilang.** Commit `fdcbbf0d` masih reachable dari `fix/tailwind-source-scope`; report ini
dan suite kedua-duanya wujud atas disk dan berfungsi.

Ini bukan defect untuk dibaiki — ia keadaan normal repo yang dikongsi ramai ejen. Pelajarannya:
`git log -1` + `branch --show-current` **sebelum** dan **selepas** commit, dan jangan anggap branch
yang aku baca 20 minit lalu masih branch semasa.

Gap kecil dikesan (tidak aku sentuh, §6): **2 daripada 161** deployment tiada `additional_drop_params` —
`hermes-asi-vision` (→ `deepseek/deepseek-flash`) dan satu `i-arif` (→ `gemini/gemini-3.6-flash`).
Bukan laluan Claude Code, jadi tidak menjejaskan sesi ini.

## 6. MENUNGGU ARIF (tidak aku execute)

1. **Patch 2 deployment litellm** yang tiada `drop_params`. Fail `chattr +i`; patch perlukan
   `systemctl restart litellm-federation` — restart gateway boleh putuskan **semua** ejen termasuk
   aku, dan ia kelas court-service di KVM8. Sediakan, tak execute:
   `/root/scripts/canon-mutate --agent FI-002 file /root/A-FORGE/litellm-config.yaml -- <patch>`
   kemudian `systemctl restart litellm-federation`.
2. **Keputusan OS-level boundary**: kekal root-dengan-guard-berlog (status sekarang, risiko diterima
   secara sedar) **atau** pindahkan pemilikan guard ke principal berbeza. Hanya pilihan kedua menutup
   kelas residual §4. Ini keputusan kedaulatan, bukan kerja engineer.
3. **Copy drift**: `/root/AAA/plugins/claude-code-federation/hooks/f1-amanah-preshell.py` (8,630 B,
   25 Sep) vs live (14,210 B). **Tidak** didaftarkan dalam mana-mana `settings*.json` (0 rujukan) dan
   tiada laluan yang menyalinnya ke live (grep kosong → tiada risiko revert automatik). Ia zombie
   reference copy. Pilihan: padam ke `_to_delete/`, atau segerakan supaya pembaca seterus tidak
   audit salinan yang salah. Belum bertindak — AAA tree `chattr +i`, dan ia bukan defect aktif.

## 7. Kesilapan probe aku sendiri (direkod supaya tidak berulang)

Empat kesilapan aku buat semasa audit ini:
1. Aku reka nama fail logo (`registry.svg`, `hapax.svg`) → 404, hampir aku laporkan sebagai "defect Kimi". Nama sebenar `mcp.svg` / `rochette.png` = 200. **F9 ANTI-HANTU: probe, jangan reka.**
2. Aku uji URL glama/lobehub yang bukan href page → keputusan tidak bermakna. Ambil href dari served page dahulu, baru uji.
3. Aku taip `curl -wL` (bukan `-w … -L`) → dump body 909 KB ke dalam konteks.
4. **Aku hampir laporkan claim agy tentang branch sebagai palsu** — lihat §5.1. Kesilapan paling
   serius dalam sesi ini, kerana ia akan memfitnah kerja sibling yang sah. Keadaan semasa bukan bukti
   tentang masa lalu; bila ref hilang, `git reflog` adalah saksi.

Kesilapan 1–3 dikesan sebelum report. Kesilapan 4 dikesan **selepas** aku menulis ayat itu ke dalam
report — dibetulkan sebelum commit, tetapi hampir tidak. Sebab ia terlepas: aku probe `git branch -a`
semasa keadaan repo sedang diubah sibling di bawah aku (§5.2), dan aku terima ketiadaan ref sebagai
jawapan tanpa bertanya "ref ini wujud pada 14:27?".

Dan satu kesilapan reka bentuk awal: draf pertama skrin Bash aku menyekat
`cat /protected > /tmp/x` dan `python3 -c "json.load(open('/protected'))"` — kedua-duanya **bacaan sah**.
Suite ALLOW-case (32 kes kerja harian sebenar) yang menangkap ini, bukan pemikiran aku. Itulah sebab
suite itu dikekalkan: ia bukan senarai serangan, ia senarai kerja yang mesti terus boleh dibuat.

## Ulang sendiri

```bash
python3 -I /root/AAA/scripts/f1-hook-escape-suite.py \
  /root/.claude/hooks/f1-amanah-preshell.py "LIVE"      # exit 0 = 67/67
python3 -I /root/AAA/scripts/hook_mesh_check.py         # exit 0 = 9 ok
```

Suite menerima argumen `<hook-path>` — jalankan pada calon **sebelum** deploy, bukan selepas.
