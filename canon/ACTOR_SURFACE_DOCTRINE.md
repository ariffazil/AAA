# AAA RUNTIME GEOMETRY — Actor / Surface Doctrine

> **STATUS:** RATIFIED v1.1 by F13 SOVEREIGN, 2026-08-15 ("zen AAA")
> **v1.1:** L0/L1 split (000/999 = structure) · EMD two-feet · Rule Zero · registry mapping · RCR falsifier
> **Forged from:** GLM-5.3 session — silent redirect scar + five-file churn
> **DITEMPA BUKAN DIBERI**

---

## The Canon

> **Actors are invariant. Surfaces are replaceable. Models are runtime occupants.
> Structure remembers; runtime rotates.**

---

## Geometry

```
L0  STRUCTURE (bukan actor — tak bertindak)
        ├─ 000-KERNEL   = Law        (pintu kedaulatan, constitution)
        └─ 999-VAULT999 = Witness    (saksi, tak pernah beragensi)

L1  ORGANS / ACTORS (fungsi kekal)
        ├─ 333-AGI     = Imagination
        ├─ 555-ASI     = Verification
        ├─ 777-A-FORGE = Action
        └─ 888-APEX    = Judgment

L2  CONTRACTS      — role · authority · capability (CCC) · memory scope

L3  SURFACES (FI)  — Qwen · OpenCode · Hermes · Codex · Kimi · Claude Code

L4  RUNTIME        — model · provider · route · endpoint
```

arifFlow = saraf (organ metabolism, bukan actor). 000 dan 999 ialah kerusi
fungsi: law dan witness substrate. Hanya L1 bertindak.

## EMD Two-Feet

Inhabitation bukan rantai linear. 333 = mind, 777 = hands — dua kaki
berbeza yang bertemu di kernel:

```
          333 (mind)
         /          \
        ↓            ↓
    Qwen           777 (hands)
      ↓              ↓
    GLM-5.3      tools/actions
```

333 boleh menghuni Qwen/OpenCode/Hermes (kaki kiri, berputar bebas).
Execution authority sentiasa lalu 777 (kaki kanan, tetap).
Separation of powers terpelihara pada aras actor, bukan aras surface.

## Rule Zero — Registries

**Jangan campur static dengan dynamic dalam fail yang sama.**
Medan statik + medan dinamik dijahit sekali = reput.

| Registry | Sifat | Rumah disk (sedia ada) |
|---|---|---|
| A — Actor | Static | `agent-cards/identity/` ✅ wujud |
| B — Surface | Semi-static | `agents/_external/` (FI cards) ✅ wujud |
| C — Capability (CCC) | Static-ish | `COGNITIVE_SPECIES.json` ✅ wujud |
| D — Runtime Binding | **Dynamic** | pola SOT qwen-code (`federation-models.json` + `model_binding`) — digeneralisasi |

**Zen move: bukan bina empat registry baharu.** Tiga sudah wujud sebagai fail
berasingan. Hanya D baru — dan dia sudah ship pada satu surface. Satu-satunya
pelanggar Rule Zero ialah `AGENT_MODEL_MAP.json` (identiti + provider + model +
nota + sejarah dijahit sekali; 12+ fail .bak = saksi churn). Ia diturunkan
pangkat kepada *generated view* atau dipecah mengikut lapisan — kerja T2
baharu, bukan sessi ini.

Health metrics (latency, success_rate) — FED sudah kutip (`fed_report_latency`).
Tiada lapisan baharu diperlukan.

## The Exception — Kerusi Konstitusi

888 / 666-999 seat / i-arif: `Model ⇢ Authority` — *who judges is partly
what judges.*

```yaml
constitutional:
  ratified_model: minimax-m3
  last_returned_model: minimax-m3   # echo reflex di FED
  drift: false
```

- `inhabitant_policy: ratify` — F13 + 888 sahaja, tiada putaran senyap
- **FED echo reflex** — `requested ≠ returned → drift event`
  (Z.ai redirect 2026-08-14 tak kelihatan oleh pointer-to-SOT)
- Kerusi 666/999 tidak sesekali dilayan zai coding plan (SHADOW-GLM-004)

Bukan kerana itu identiti — kerana itu kawalan.

## Litmus Falsifier — RCR

```
RCR = files_changed / model_release
```

- **Baseline diukur:** GLM-5.3 (2026-08-15) = **5+ fail**
- **Target:** GLM-6 = **1** (satu edit SOT, semua permukaan regenerate)
- Caveat jujur: release pertama selepas migrasi menanggung kos migrasi
  sekali sahaja; pengukuran bermula dari release kedua era baharu.

```
GLM-6 masih perlukan edit card + CCC + config + doctrine + shadow?
→ bukan model yang gagal. Geometry yang gagal.
```

## Provenance

- Ratifikasi: F13 SOVEREIGN, 2026-08-15 ("zen AAA"; cadangan registry dari
  Copilot di-zen-kan dengan pemetaan disk)
- Eureka resit: `b4a28ff3` (identity≠implementation) · `09db16ec` (actor≠surface)
- Scar: Z.ai silent redirect 5.2→5.3 (SEAL-d186bb9c9f934225, verified)
- Praktik pertama: qwen-code card v2.2.1 (`model_binding` → SOT)
- Epigraf: *lane adalah nama tulang; model adalah darah.*
