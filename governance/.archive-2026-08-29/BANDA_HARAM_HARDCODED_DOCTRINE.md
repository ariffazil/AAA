# BANDA HARAM HARDCODED — Dynamic Invariant Doctrine

> **Forged:** 2026-08-12 by Hermes under F13 SOVEREIGN directive
> **Source:** Standing ruling from ARIF — "Relaks tapi tajam"
> **Status:** LAW (F4 CLARITY · F12 RESILIENCE)
> **DITEMPA BUKAN DIBERI** ⚒️

---

## The Axiom

```
Undang-undang (Constitution & Math Laws) = KEKAL (Invariant)
Realiti (World State)                      = CAIR (Dynamic)

Kalau hardcode elemen dinamik → geseran → kekacauan (ΔS > 0)
```

**Iron Rule:** Static values for dynamic domains = death.

---

## Six Domains Haram Hardcode

### 1. Domain Model & Intelligence Engines
**Haram:** Identiti atau keupayaan enjin AI dalam kod tetap.

| Sub-domain | Contoh haram | Sepatutnya |
|-----------|--------------|-----------|
| Model IDs & Versions | `gemini-3.6-flash`, `claude-3-5` | Config registry + version-resolver |
| Context Windows & Limits | `max_tokens=4096` static | Read from provider manifest |
| Pricing & Cost Weights | `$0.03/1k` inline | Env vars + cost-of-truth lookup |

**Why:** Vendor swap = sistem mati. Harga turun-naik = budget rosak.

### 2. Domain Agents & Federation Topology
**Haram:** Anggapan jumlah/lokasi ejen kekal.

| Sub-domain | Contoh haram | Sepatutnya |
|-----------|--------------|-----------|
| Agent Roster & Counts | `agents=[333, 555, 777]` static list | Ephemeral registry + health probe |
| Node Addresses & Ports | `:8088` hardcoded in skill | Service discovery + DNS |
| Active Worker States | `worker_a: busy` in config | Live health probe |

**Why:** Migrasi VPS = mati. Tambah organ baru = pecah.

### 3. Domain Tools & Capabilities
**Haram:** Laluan perisian atau endpoint yang boleh berubah.

| Sub-domain | Contoh haram | Sepatutnya |
|-----------|--------------|-----------|
| Tool Registration & Endpoints | `/usr/bin/script-v1.py` | Path resolution + PATH var |
| Network Timeouts & Latency | `timeout=5s` static | Adaptive timeout + jitter |
| External API Status | `github.com: up=true` cached | Live probe each session |

**Why:** API version bump = crash. Network drift = false positive.

### 4. Domain Human (888 / Sovereign)
**Haram:** Cara manusia berinteraksi dengan sistem.

| Sub-domain | Contoh haram | Sepatutnya |
|-----------|--------------|-----------|
| Attention Bandwidth (W_scar) | `attention=24/7` | Lane discipline + ping budget |
| Preferred Channels | `channel=telegram-only` | Multi-channel (TG/CLI/Web) |

**Why:** 888 tidur = HOLD yang sepatutnya auto-proceed jadi bottleneck. Channel swap = sistem tak boleh reach.

### 5. Domain Math, Thresholds & Learning Parameters
**Haram:** Parameter kawalan statik untuk sistem penyesuaian.

| Sub-domain | Contoh haram | Sepatutnya |
|-----------|--------------|-----------|
| Decay & Regression Rates | `0.95` hardcoded | Dynamic tuning via C_dark feedback |
| Risk Weights (Ω₀) | `Ω₀=0.05` static | Range ∈ [0.03, 0.05] dynamic |
| Confidence Thresholds (P) | `P > 0.99` static | Task-criticality scaled |

**Why:** Environment shifts = inflexibility kills. Risk profile changes = same threshold wrong twice.

### 6. Domain World, Environment & Time
**Haram:** Keadaan fizikal dunia dalam logik kod.

| Sub-domain | Contoh haram | Sepatutnya |
|-----------|--------------|-----------|
| Time, Dates & Timezones | `UTC` tanpa NTP awareness | `now()` + timezone resolution |
| File System Paths & Disk | `/var/lib/.../v1` immutable | Pruning + auto-rotation |
| Geopolitical Context | `server-region=us-east` static | Runtime probe + failover |

**Why:** NTP drift = wrong timestamp = audit failure. ENOSPC = death.

---

## The Failure Pattern

```
Hardcode dinamik
    ↓
Sistem rapuh (brittle)
    ↓
Sistem kena repair setiap kali external change
    ↓
Tenaga habis untuk repair, bukan untuk kerja
    ↓
Entropy naik (ΔS > 0)
    ↓
Kekacauan
```

## The Fix Pattern

```
Elemen dinamik → Dynamic Configuration Registry
                  ↓
              Environment Variables
                  ↓
              Self-Healing Loops yang baca realiti dari substrat
                  ↓
              ΔS ≤ 0 (entropy stays bounded)
```

---

## Operational Rules

1. **Before any patch:** tanyalah — adakah elemen ni kekal atau berubah-ubah?
2. **If dynamic → config/env/probe**, bukan kod.
3. **F2 TRUTH requires live probe**, bukan cached value.
4. **Audit cadence:** quarterly sweep for hardcoded dynamic values.
5. **Gödel Caveat:** Even configuration is dynamic — config-of-configs must exist (recursion terminates at F13).

---

## Standing Directive (2026-08-12)

> *"Relaks tapi tajam."* — ARIF
>
> Hardcode benda dinamik = chaos.
> Configurable + probed = zen.
> Constitution = invariant. World state = dynamic.

---

*This doctrine is canon. Every new skill, every patch, every line of code must pass this filter. F4 CLARITY + F12 RESILIENCE in one document.*