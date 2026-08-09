# AAA as a REAL STATE — Institution before citizens

> **Forged:** 2026-08-09 · F13 path: **state first, then warga**  
> **Doctrine:** DITEMPA BUKAN DIBERI  
> **Not this doc:** passport stamps, `warga_status`, FI attestation ceremony  
> **This doc:** what must be true for the federation to be a *state* (institution)

---

## 0. One sentence

```
STATE = territory + law + organs + power + telephone + records + control plane
CITIZEN = who holds a passport inside that state
```

We finish **STATE**. Citizens (OpenCode FI, Hermes edge, OpenClaw gateway) already *live and work here*; formal warga stamps come **after** the state is indisputable.

---

## 1. Seven pillars of the state (must all stand)

| # | Pillar | SOT / surface | Live proof |
|---|--------|---------------|------------|
| **1 Territory** | Who/where organs are | `docs/ORGAN.md` + `federation/organs.yaml` | Ports match health probes |
| **2 Law** | F1–F13 floors | arifOS `:8088` · `GENESIS/FLOOR_TABLE.json` | `curl :8088/health` healthy |
| **3 Government** | Core organs running | arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, arifFLOW | All `:port/health` 200 |
| **4 Power grid** | Model/tokens (WHICH) | FED `:4000` + litellm `:4011` + HAProxy | `/health/liveliness` 200 |
| **5 Telephone** | How to dial anyone | `docs/CALL_MAP.md` + `federation/call_map.yaml` | File exists; skill `FORGE-call-map` |
| **6 Catalog** | Who exists (directory) | AAA 3-layer cards · registry | identity/harness/binding load |
| **7 Records** | Immutable truth | VAULT999 | AAA health `vault: CONNECTED` |

**Control plane rule:** AAA `:3001` = DISPLAY_ONLY — catalogs, routes A2A, **never adjudicates, never seals**.

---

## 2. Three books of the state (never mix)

| Book | Question | SOT |
|------|----------|-----|
| **Directory** | Who exists? What class? | Agent cards · 3-layer geometry |
| **Telephone** | How do I call them? | **CALL_MAP** |
| **Power bill** | Which LLM pays? | FED + runtime model configs |

**Capabilities (reminder):**

```
physical caps = L2 harness firmware
domain caps   = opened by L3 binding (door)
authority     = canDo/cannotDo over both
```

---

## 3. STATE readiness gate (binary)

Run:

```bash
/root/AAA/scripts/state-probe.sh
```

| Exit | Meaning |
|------|---------|
| **0** | STATE_READY — safe to later stamp citizens |
| **1** | STATE_DEGRADED — fix pillars before warga ceremony |
| **2** | STATE_DOWN — core government offline |

Gate checks (automated in `state-probe.sh`):

1. Core organs health ≥ 7/7 (8088, 7071, 7072, 7073, 3001, 8081, 18082, 18083)  
2. FED liveliness `:4000`  
3. AAA health status `healthy` · `deployment_drift=false` · QDF ≥ 0.9  
4. CALL_MAP + call_map.yaml present  
5. Agent-card registry loads (node require) with 3 layers · unclassified acceptable only for retired/test  
6. VAULT connected (from AAA health)  
7. Deploy markers: `/root/AAA/.git_commit` == `/opt/aaa/app/.git_commit` == intent of HEAD (or script-synced)

**Do not** require `warga_status: attested` for STATE_READY.

---

## 4. Who already *operates* in the state (not passport)

| Surface | Role in state | Layer | Formal warga later? |
|---------|---------------|-------|---------------------|
| OpenCode | Primary forge instrument | L2 harness | Yes (FI-001) — *later* |
| Hermes ASI | Human bridge / edge | L3 binding | Optional edge citizen stamp |
| OpenClaw | Gateway / metabolizer | L3 binding | Optional infrastructure stamp |
| Organs | Law, hands, earth, capital, vitality | L3 binding | Never “warga” — they are ministries |
| FI vendors | Alternate harnesses | L2 | FI slots when stamped |

Operating ≠ passport. **State first.**

---

## 5. Boot law (every agent in the state)

```
1. state-probe.sh   (or read STATE.md + probe ports)
2. CALL_MAP.md      (telephone)
3. ORGAN.md         (territory)
4. arif_init        when mutation path needs law
5. Then work
```

Pointers:

- Hermes: `/root/HERMES/CALL_MAP.md` + this STATE  
- OpenCode/Grok skills: `FORGE-call-map`  
- Machine: `federation/STATE.yaml`

---

## 6. Explicitly deferred (citizen phase — NOT now)

- `warga_status: attested` on Hermes / OpenClaw  
- FI renumber cleanup on every card  
- Dual openclaw function/harness merge  
- Lane A `arif_seal` of citizenship  
- Passport ceremony for every persona  

---

## 7. When is the state “real enough” for citizens?

When `state-probe.sh` exits **0** three times in a row across restarts, and:

- Directory + telephone + power documented and live  
- No false deployment drift  
- Core ministries answer health  
- Control plane remains DISPLAY_ONLY  

Then: **bring citizens in** (attestation, FI stamps, SOUL/AGENTS per warga).

---

*Institution before passport. Geometry before gala.*
