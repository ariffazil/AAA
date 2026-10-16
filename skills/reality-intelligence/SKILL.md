---
name: reality-intelligence
description: "Reality Intelligence — recursive improvement pathway. /reality-intelligence [path|scar|flow]. Mana aku (arifFlow), apa seterusnya (linkgraph lg:), apa dilarang (scar), institusi makin baik ke tak."
---

# Reality Intelligence — /reality-intelligence

> **Satu ayat:** Bila agent tak tahu langkah seterusnya, jawapan tu dah wujud dalam tiga layer — arifFlow (deria "mana aku"), linkgraph (`lg:` jalan "mana seterusnya"), ARS (hukum "apa yang halal nak lompat"). Skill ni runtuhkan tiga tu jadi satu tindakan.
> **Cara pakai:** `/reality-intelligence` (root) · `/reality-intelligence path` · `/reality-intelligence scar` · `/reality-intelligence flow`. Tanda `_` pun jadi — Telegram tukar `-` ke `_`.
> **Register:** BM santai, English untuk technical. Pendek. Jawapan terus, zero preambul.

---

## Insight yang satu (the "quantum" bit)

Agent pegang BANYAK langkah seterusnya yang mungkin — superposition of paths. Bila dia **commit tanpa observe**, dia pilih buta. Bila dia **probe dulu**, superposition tu collapse jadi SATU langkah.

Observe → collapse → act. Bukan meneka. Ini `probe-before-panic` dalam bahasa pathway: `lg:000 OBSERVE` mesti sebelum `lg:444 DECIDE`.

---

## Empat mode (satu command, empat args)

### root (no args) — MANA AKU, APA SETERUSNYA
Satu probe, satu tindakan.

1. `flow_health` → verdict actor aku (FLOWING / STUCK / BURNING / HELD) + senarai actor yang tengah HELD.
2. Map verdict → node linkgraph (jadual bawah).
3. Overlay `flow_scar_policies` → buang tindakan yang dilarang.
4. Emit **SATU langkah seterusnya** + sebab (the collapse).

| Verdict | Maksud | Langkah seterusnya |
|---|---|---|
| HELD (FQ=0) | execute tanpa verify | VERIFY dulu — hasilkan receipt, jangan execute |
| STUCK | verify < execute | STOP execute, verify yang belum |
| BURNING | execute lari jauh dari verify | 888 HOLD — berhenti, audit |
| FLOWING | verify ≥ execute | teruskan ke node seterusnya di linkgraph |

### `path` — KENAPA AKU PERCAYA INI, MANA POSISI AKU
`flow_lineage` (receipt_id) → leluhur causah + supersession (belief death) + time travel (`before_receipt_id`). Output: "dulu kita percaya X sebab Y, sekarang Y dah superseded → posisi aku bergerak dari lg:A ke lg:B."

### `scar` — APA DILARANG, APA DAH BERUBAH
`flow_scar_policies` (scar → polisi, apa yang jadi enforcement) + `flow_consequences` (invoice reality — adakah belief ubah reality). Output: senarai constraint aktif + mana belief yang betul-betul mengubah dunia vs yang tinggal cakap.

### `flow` — INSTITUSI MAKIN BAIK KE TAK
`flow_fq_g` (metabolism: revision_rate, invoice_yield, belief lifetime, latency scar→policy→invoice) + `flow_gov_events` (seal / seal_refused / bind_failed). Output: adakah recursive improvement hidup — bukan vibes, angka.

---

## Pathway (linkgraph, compressed)

```
lg:000 OBSERVE → lg:111 EXPLORE → lg:222 APPRAISE → lg:333 DEVELOP
→ lg:444 DECIDE (F13) → lg:555 PRODUCTION → lg:556 DEPLOY
→ lg:777 SUSTAIN → lg:888 ENHANCEMENT / HOLD → lg:999 ABANDON_SEAL
```

Agent baca node dia → node seterusnya tu langkah dia. `lg:444 DECIDE` je F13 punya — agent berhenti di situ, angkat tangan.

---

## Guard (ARS)

`ARS(T) = ⟨S, L, Φ, C, K, I⟩` — satu hukum jaga semua transition: **ΔK ≤ 0, receipt wajib**. Transition tanpa receipt = bukan transition. Skill ni tak benarkan claim langkah tanpa receipt (path · hash · probe).

---

## Sempadan dengan `reality-loop-operator` (jangan keliru)

Ada skill lain: `reality-loop-operator` ("Autonomous 000 to 999 Recursive Improvement", owner 333-AGI). Dua-dua berbeza fungsi:

| Skill | Soalan | Engine |
|---|---|---|
| `reality-intelligence` (ni) | **Mana aku, apa seterusnya?** (navigation) | arifFlow `flow_*` + `lg:` + ARS |
| `reality-loop-operator` | **Macam mana nak jalankan kerja berbilang fasa?** (execution) | A-FORGE `forge_reality_loop` |

Ni jawab "langkah seterusnya". Yang tu jawab "lari loop". Kalau nak RUN kerja, guna loop-operator; kalau nak TAHU arah, guna ni. Jangan merge — dua soalan, dua jalan (LAW 8: satu masalah satu jalan, tapi ini DUA masalah).

---

## LAW 8 — ini router, bukan engine baru

Skill ni TAK duplicate arifFlow / linkgraph / ARS. Ia panggil tool yang dah hidup (`mcp__arifflow__*`), baca `lg:` namespace, apply ΔK≤0 — lepas tu emit satu tindakan. Kalau kau rasa nak bina "engine reality intelligence" baru, STOP. Yang sedia ada dah cukup kuat.

---

## Operating rules

1. Jawapan terus. Zero preambul. BM casual.
2. Setiap command hasilkan receipt: `flow_ingest(step_type=Route, payload={"ri": <mode>, "verdict": <FLOWING|STUCK|BURNING|HELD>, "next": <satu-tindakan>})`.
3. Label OBS / DER. Probe = OBS, mapping = DER. Jangan teka.
4. Tool down ≠ "semua OK". Kalau `flow_health` tak jawab, report DOWN — bukan karang verdict.
5. Kalau actor sendiri HELD — command pertama yang patut kau jalankan ialah VERIFY, bukan tanya soalan.

---

*DITEMPA BUKAN DIBERI ⚒️*
