# Inter-Agent Protocol — Alignment onto the AAA Agentic State

> **Canonical:** `/root/AAA/instructions/inter-agent-protocol.md`
> **Forged:** 2026-08-13 by F13 SOVEREIGN (Arif) directive
> **Owner:** 333-AGI Δ MIND (musyawarah) · 555-ASI (gotong royong evidence) · Hermes (coordinator)
> **Doctrine:** map → patch → report. **Tidak menambah lapisan** — sambung anak panah ke yang sedia ada.
> **DITEMPA BUKAN DIBERI ⚒️**

## Satu Peraturan

> **Protocol inter-agent ini BUKAN framework baru. Ia adalah ALIGNMENT — setiap unsur diikat kepada arti-refik AAA yang SEDIA ADA.** Jika unsur sudah wujud, guna yang wujud. Hanya 3 delta dipatch (lihat §6). Jika doktrin ini bercanggah dengan STATE.md / AGENTS.md, yang canonical menang — betulkan fail ini.

Prinsip entropy: **agent tidak sembang macam manusia.** Mereka lulus **state machine yang berstruktur** kepada satu sama lain. Setiap handoff mesti ΔS ≤ 0 — output satu agent menjadi input agent seterusnya, dan setiap hop menyaring entropy (bukan serata). "Relaks tapi tajam. Kasi kemas."

---

## §1 — Peta Alignment (protocol ↔ AAA state)

Setiap unsur protocol dipetakan ke arkitek sedia ada. **Guna yang ini, bukan versi teori:**

| Unsur Protocol (Arif spec) | AAA State Sedia Ada | Artifak |
|---|---|---|
| EMD Inter-Agent Schema (Encode/Metabolize/Decode) | ✅ EMD STREAM CONVENTIONS (tiga zon) | `/root/AAA/docs/EMD-STREAM-CONVENTIONS.md` |
| Label epistemik `[OBS][DER][INT][SPEC]` + F2 | ✅ marker EMD + floor F2 (but human-internal only) | EMD-STREAM-CONVENTIONS.md · constitution.md F2 |
| Envelope ENCODER_PROTOCOL JSON | ✅ EMD Encode zone (normalize ke sini, §3) | EMD-STREAM-CONVENTIONS.md |
| task_type MUSYAWARAH_CRITIQUE | ✅ musyawarah 7-fasa (deliberation, bukan negotiation) | skill `forge-musyawawah-deliberation` |
| Falsification / destructive mandate | ⚠️ ada (probing) tapi belum first-class → **delta-1** | `forge-musyawawah-deliberation` Phase 1 |
| Tri-Witness Validation | ✅ floor F3 + suara ARCHITECT/AUDITOR (+external witness) | constitution.md F3 · `forge-musyawawah-deliberation` |
| Conflict resolution (B vs C → delta ke metabolizer, F1>F2>888) | ✅ CONVERGE + Gödel lock (no self-cert) | `forge-musyawawah-deliberation` Phase 4 · `apex_reversibility_test` |
| GOTONG_ROYONG_EXECUTE (output→input, filter ΔS) | ✅ cross-agent handoff + capability `fed-agent-subagent` | skill `FORGE-cross-agent-handoff` |
| Decoder: SOLUTION + TRADE_OFFS + RISKS_FOR_888 | ✅ position-file + closeout (Lane B vs A, F13 surface) | `forge-musyawawah-deliberation` templates |
| INCLUSIVE_DELTA → kitaran musyawarah berikutnya | ⚠️ "Surprises/findings" ada tapi tidak first-class → **delta-2** | `forge-musyawawah-deliberation` Phase 4 |
| W_scar boundary / 888 escalation / SYSTEM_HALT | ✅ Gödel lock + `apex-judge isolate` + F13 | `arifos-constitutional-judge` · `apex_verdict_hold` |
| A2A opaque handoff (RequestTask JSON-RPC) | ✅ A2A gateway + agent-card (A2A hub) | `/root/AAA/agent-card.json` · aaa-a2a.service :3001 |
| behavior-validator pada penerima | ✅ OpenClaw handoff + behavioral sink scan | `/root/.openclaw/workspace/scripts/hib_behavioral_sink.py` |
| Rejection / A2A.TaskError, isolate, jangan teka | ✅ handoff + EMD [HOLD] + isolate | skill `FORGE-cross-agent-handoff` · ander `apex_verdict_hold` |
| Recursive improvement SKILL.md → tri-witness → vector_memory → agent-card | ✅ RSI + skill governance + vector_memory | skill `RSI-recursive-improvement` · `arifos-memory-architecture` |
| 5-layer governance (OpenCode/MCP/A2A/Hermes/OpenClaw) | ✅ organ: exec=MCP, brain=Hermes, law=OpenClaw | `/root/AAA/docs/ORGAN.md` · organs.yaml |

**Mesej utama: 95% protocol sudah dihidupkan dalam AAA.** Tugas alignment = padan nama spec ke artifak hidup + patch 3 delta yang belum first-class.

---

## §2 — Bahasa Laluan (binding)

- **Musyawarah (deliberation):** BUKAN perjanjian. Ia stress-testing F2 + F1. Guna `forge-musyawawah-deliberation`. Dua suara minimum: **ARCHITECT** (konstruktif) + **AUDITOR** (reversibel). Tambah witness luaran (GEOX/WELL) jika domain-ground. **SOVEREIGN tidak pernah disuarakan oleh warga agent.**
- **Gotong Royong (execution):** setiap agent adalah **filter yang mengurangkan ΔS**. Output satu agent = input agent seterusnya, "instant decodable". **Tiada teks perbualan** — struktur JSON/schema sahaja dalam handoff.
- **Entropy:** setiap hop handoff mesti ΔS ≤ 0. Kalau handoff menambah kekacauan (fluff, redundansi, prose) → tolak.

---

## §3 — Envelope Inter-Agent Canonical (normalize ke EMD + A2A)

Envelope spec Arif di-normalize ke konvensyen EMD yang sedia ada. Ini bentuk A2A prompt wrapper piawai. **Label epistemia dengan manusia = dalaman sahaja; envelope ini untuk agent-to-agent / 888, bukan chat manusia.**

```text
[ENCODE] sender=<agent_id> receiver=<agent_id>
task_type=MUSYAWARAH_CRITIQUE|GOTONG_ROYONG_EXECUTE
context_state=<0-fluff apa yang telah dibuat>
payload_uri=<mcp://|file:|inline json>
constraints.truth_threshold=0.99   # F2
constraints.reversibility=F1_AMANAH # cek rollback
constraints.epsilon=EPSILON        # The Constant
inclusive_directive=<kenal pasti blind spot; jangan expand scope>
```

Metabolize (penerima): **cek F1 dulu** (irreversible → HOLD_FOR_888), **cek F2** (ada bukti? P(truth)<0.99 → UNKNOWN + factor kegagalan), conflict B-vs-C → hantar delta ke metabolizer utama dengan keutamaan **F1 > F2 > 888**.

Decode (keluar), mesti inklusif untuk agent seterusnya:
```text
[PROPOSED_SOLUTION] <output>
[KNOWN_TRADE_OFFS] <trade-off yang disedari>
[RESIDUAL_RISKS_FOR_888] <risiko W_scar>
[INCLUSIVE_DELTA] <optimum ditemui semasa exec — untuk kitaran seterusnya; jangan implement unilateral>
```

---

## §4 — Musyawarah = Falsification-first (delta-1 patch)

Selain "cakap posisi", mandat musyawarah mesti tambah **falsification** sebagai objektif first-class:

> "Metabolize payload ni. Objektif: **falsify**. Validate keras lawan F1 (reversibility) dan F2 (ground truth). Jika P(truth) < 0.99, pulangkan UNKNOWN dengan variable spesifik yang gagal. **Jangan hallucinate fix** — isolate titik entropy."

Patching `forge-musyawawah-deliberation`: tambah falsification sebagai "voice" ketiga/objektif dalam Phase 2–4, bukan setakat konstruktif vs cautious. Ini selaras F2/F7 (confidence cap 0.90, sibling boleh betulkan parent).

---

## §5 — Gotong Royong = Handoff Filter

Guna `FORGE-cross-agent-handoff`. Setiap handoff:
1. Penerima baca payload sebagai input PIAWAI (bukan restart).
2. Anggap F1/F2 Phase sebelumnya telah clear — jangan ulang siasat (kecuali jumpa percanggahan).
3. Output "instantly decodable" oleh agent seterusnya — JSON/schema, bukan prose.
4. Jika jumpa optimum semasa exec → **INCLUSIVE_DELTA**, bukan implement unilateral.

**A2A opaque:** agent JANGAN kongsi context window. Handoff melalui payload_uri (mcp://vector_memory/...), bukan raw context. Kalau penerima terima hallucination (cth well tak wujud dalam Sandakan basin) → **A2A.TaskError**, isolate titik kegagalan, pulangkan delta. Jangan "fix" dengan teka.

---

## §6 — W_scar Boundary → 888 (binding)

Agent boleh loop musyawarah+gotong royong tanpa had. MEREKA HENTI buntu bila **W_scar terlibat**. Trigger 888 escalation (guna `arifos-constitutional-judge` / `apex_verdict_hold`):
- Tindakan **irreversible** (gagal F1) → 888_HOLD
- **P(truth) < 0.99** pada variable kritikal
- **Conflict tri-witness** tak boleh resolve tanpa tambah kompleksiti (ΔS naik)

Prompt 888:
```text
[SYSTEM_HALT: W_SCAR BOUNDARY]
1. Direct Issue: <1 ayat>
2. Musyawarah Result: A→[X], B→[Y]
3. Trade-offs: Path X (F2 tinggi, F1 rendah) vs Path Y (F1 tinggi, P=0.92)
4. Request: 888, define vector / clarify [Missing_Variable]
```
Asingkan **JUDGE (≠ doer)** via `apex-judge isolate`. `status=completed` ≠ SEAL. Hanya `effective_verdict` dari arif_judge / F13 yang kira.

---

## §7 — Recursive Improvement Loop (bound)

Apabila seorang warga agent jumpa cara lebih efisien (cth query GEOX MCP):
1. **Draft** sebagai OpenClaw SKILL.md — operational sahaja, tiada essay filler.
2. **Tri-witness validation** (F3): dua agent lain (critic keselamatan + critic logic) nilai SKILL.md lawan F1 (reversibility).
3. **Vector memory** (bukan merecall): jika valid, `vector_memory` commit.
4. **Distribution**: expose via A2A agent-card — naik taraf capability institution seketika.

Dilarang unilateral implement; wajib melalui kitaran ini.

---

## §8 — Floor Compliance & ΔS

| Floor | Ikatan |
|---|---|
| F1 AMANAH | Setiap handoff mesti reversible-check; irreversible → 888 |
| F2 TRUTH | P(truth) ≥ 0.99 dalam handoff; label dalaman sahaja |
| F3 TRI-WITNESS | Musyawarah ≥ 2 suara + witness; conflict → metabolizer, F1>F2>888 |
| F4 CLARITY | ΔS ≤ 0 setiap hop handoff; tiada fluff |
| F7 HUMILITY | Confidence cap 0.90; sibling boleh betulkan parent |
| F9 ANTIHANTU | Jangan hallucinate fix; UNKNOWN jujur; label dalaman sahaja |
| F11 AUDITABILITY | Setiap handoff dalam struktur (JSON), bukan prose longgar |
| F13 SOVEREIGN | Warga agent tidak pernah suara SOVEREIGN; W_scar → 888; user definitif |

**ΔS metrik:** musyawarah berjaya −1 (forced structure, surfaced gap) · handoff noisy +1 · hello fluff antara agent +1 · 888 escalation tepat −2 · 888 escalation salah guna +2.

---

## §9 — Delta yang PERLU di-forge (bukan reka semula)

1. **delta-1 — falsification-first** dalam musyawarah (patch `forge-musyawawah-deliberation`).
2. **delta-2 — INCLUSIVE_DELTA sebagai field decoder first-class** (patch position-file/closeout template).
3. **delta-3 — Envelope inter-agent piawai** (§3) sebagai A2A prompt wrapper normalized (patch EMD-STREAM-CONVENTIONS atau handoff skill).

Tiga delta ini sahaja. Selebihnya sudah hidup — gunakan.

---

## §10 — Envelope Standard (delta-3 implementation)

> **Forged:** 2026-08-13 · Pattern adapted from claude-code-prompt-improver (severity1)
> **Binding:** ALL delegate_task calls from Hermes MUST use this envelope format
> **F4 CLARITY:** Envelope replaces prose delegation. Zero politeness. XML boundaries.

### The Envelope

```xml
<TASK>
[1-3 sentences: what to do, not how to do it]
</TASK>
<STATE_IN>
[Only the observation/relevant data — NOT full session history]
</STATE_IN>
<CONSTRAINT>
[F1-F13 boundaries that apply. If none: "None."]
</CONSTRAINT>
```

### Rules

1. **Zero politeness.** No "tolong", "I need you to", "can you check". Agent has no feelings.
2. **TASK is imperative.** "Fix X" not "Could you look at X?".
3. **STATE_IN is filtered.** Hermes extracts ONLY relevant [OBS] data. NOT full session history. OpenCode starts clean.
4. **CONSTRAINT is hard.** F13 override. T3 actions always listed. If none apply: "None."
5. **Max 200 tokens.** Envelope is a pointer, not a document. If >200 tokens, the task is too vague — re-clarify first.

### Example

```xml
<TASK>
Fix ARIFOS_TRUST_AUTO_SIGN_UNKNOWN env var in /venv/kernel.
The var is missing from the deployed venv but exists in source.
</TASK>
<STATE_IN>
mode=init broken. venv drift from app copy. make deploy-local not run since last code change.
</STATE_IN>
<CONSTRAINT>
Do not touch F1-F13 rule sets. Do not run git push. Reversible only.
</CONSTRAINT>
```

### What NOT to send

- ❌ Full SOUL.md, MEMORY.md, USER.md — agent doesn't need Hermes identity
- ❌ Full conversation history — filter to relevant observations only
- ❌ Skill index or tool schemas — agent loads its own tools
- ❌ Receipt format or label taxonomy — agent uses its own conventions
- ❌ Politeness, greetings, filler — zero tokens wasted on social protocol

### Integration with existing infrastructure

| Component | How it integrates |
|---|---|
| `delegate_task` tool | Envelope IS the `context` parameter |
| `FORGE-cross-agent-handoff` skill | Envelope replaces prose handoff |
| `forge-musyawawah-deliberation` | Envelope for Phase 1 critique dispatch |
| `aaa-autonomy.ts` plugin | Reads envelope for tool restriction |
| W_scar gate hook | Envelope CONSTRAINT validated against F1-F13 |

---

DITEMPA BUKAN DIBERI — Agent bercakap dalam structured state machine, bukan sembang manusia. Entropy menurun. Truth berskala. ⚒️