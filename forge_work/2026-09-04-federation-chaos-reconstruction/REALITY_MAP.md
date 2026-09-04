# FEDERATION CHAOS RECONSTRUCTION — REALITY MAP
### REALITY_ENGINEERING::FEDERATION_CHAOS_RECONSTRUCTION::2026-09-04 · Authority: ARIF (F13)

> Forensic reconstruction, witness-first, no pretending. Every row carries its evidence or says UNKNOWN.
> Probed live 2026-09-04 08:20–08:50 MYT by kimi-code/FI-008 from KVM8 (mesh SSH to KVM4/KVM2).
> Prior witness absorbed: MACHINE_MAP.md (FI-003, 09-03), HERMES_FLEET_MAP.md, SERVICE_OWNERSHIP.yaml, cron-migration receipts 20260904-001536/001732.

---

## 1. TIMELINE (T0 → T3, dated anchors only)

| Phase | Anchor | Evidence |
|---|---|---|
| **T0 Monolith** | ≤2026-09-01: everything on KVM8 | MASKED `hermes-asi-gateway.service` on KVM8 (the old gateway); `corrupt-state-20260830/` in KVM8 ~/.hermes (pre-chaos instability); KVM8 KNOWN registry expected hermes on KVM4 (retro-label) |
| **T1 Chaos** | symptoms: CPU spikes, GitHub rate-limit, instability (sovereign testimony, undated) | `ARIFOS_STRICT_MODE` hardened vault; KVM4 `config.yaml.bak-allowfix-20260903`, `bak-allowfrom`, `bak-echoloop` (emergency Telegram fixes); `carry_forward.json.real-bak-20260903` on KVM4 (carry-forward incident same day) |
| **T2 Migration** | **2026-09-02**: FED_PLACEMENT.md doctrine (KVM8=Truth/Court, KVM4=Execution, F13 ratification pending) · **2026-09-03 04:15 MYT**: KVM8 gateway drain (`gateway.run: Shutdown phase: drain done`, log) · **2026-09-03 05:xx**: KVM4 gateway up (`cron.scheduler_provider started 23:28Z` = 07:28 MYT Sep 3) · **2026-09-03 17:15**: FI-003 machine-map verification · **2026-09-03 18:09**: arif-fazil.com reconcile | KVM4 litellm binds `100.64.0.5:4000` only; KVM8 UFW→KVM4 lane verified post-enable; config note *"Telegram fail was Connection error to 127.0.0.1:4000"* (the migration's own wound) |
| **T2.5 Post-migration repairs** | **09-04 02:20** /opt split-brain quarantine · **03:47** VAULT999 mirror→KVM4 timer · **04:05** FLAME retired · **07:15–08:15 (this session)**: cron book migration 9 rituals→KVM4, SOUL unify, a2a anchor, ownership registry, ghost-cron fix | receipts `jobs.json.receipt-20260904-001536/001732`; `SOUL.kvm8-preUnify.md` backup; AAA commits b851f0cd→f2330859 |
| **T3 Current** | see map below | — |

**Chaos trigger finding [INT]:** the migration was PRAGMATIC, not doctrine-first — placement doctrine was written 2026-09-02 as ratification-pending, moves happened around it. The residue in §5 is the cost of that ordering.

---

## 2. FEDERATION MIGRATION MAP (333 — component × host × confidence)

| Component | Original | Intended (doctrine) | **Actual (witness)** | Conf. |
|---|---|---|---|---|
| Telegram (ASI💃 token) | KVM8 | KVM4 | **KVM4** (gateway holds token; KVM8 unit masked) | HIGH |
| Telegram (🦞AGI token) | KVM8 | KVM8 (edge) | **KVM8** (openclaw :18789) | HIGH |
| Telegram (🔥FORGE token) | KVM8 | dormant | **KVM8, disabled** (dual-token risk documented) | HIGH |
| Hermes gateway (H1) | KVM8 | KVM4 | **KVM4** pid 519836→(restarted 00:16Z) | HIGH |
| Hermes CLI seat (H3) | KVM8 | KVM8 | **KVM8** (on-demand pts sessions) | HIGH |
| Hermes Azwa (H2) | KVM2 | KVM2 | **KVM2** (isolated fork lane) | HIGH |
| OpenClaw | KVM8 | KVM8 | **KVM8** (never moved) | HIGH |
| FED front door | KVM8 | KVM8 | **KVM8** HAProxy :4000 | HIGH |
| FED compute (litellm) | KVM8 | KVM4 | **KVM4** (binds 100.64.0.5:4000 only) | HIGH |
| A-FORGE | KVM8 | KVM8 | **KVM8** :7071/7072 (KVM4 has read-only mirror) | HIGH |
| AAA | KVM8 | KVM8 | **KVM8** :3001 + a2a | HIGH |
| Kernel (judge) | KVM8 | KVM8 | **KVM8** :8088 (KVM2 fork ≠ judge) | HIGH |
| Memory (kernel L1–L6) | KVM8 | KVM8 | **KVM8** (inside kernel) | HIGH |
| Memory (hermes conversational) | KVM8 | KVM4 | **SPLIT**: KVM4 MEMORY.md (326B) + sessions; KVM8 sessions.db + no MEMORY.md | HIGH |
| Skills | KVM8 | mesh-distributed | **PARITY GAP**: KVM8 hermes 128 · KVM4 hermes **17** · AAA canonical 217 | HIGH |
| Tools (MCP wiring) | KVM8 | KVM4→KVM8 organs | **KVM4 wired to all organs** (arifos/aforge/geox/wealth…) | HIGH |
| Agents (A2A cards) | KVM8 | KVM8 | **KVM8** a2a-server (serving tree) | HIGH |
| API keys | KVM8 vault | both | **302/311 value-identical** (normalized hash); 9 differ, all named (§4E) | HIGH |
| Vaults (VAULT999) | KVM8 | KVM8 + mirror | **KVM8 primary + KVM4 mirror** (nightly 03:47, additive) | HIGH |
| LANES (lane_switch) | KVM8 | follow gateway | **KVM8 ONLY** — no lanes.yaml, no lane config on KVM4 gateway | HIGH |
| SOUL | KVM8 ×2 bodies | canonical | **UNIFIED today** to KVM4 canonical 13257B (one inode on KVM8 twins) | HIGH |
| Cron (agent rituals) | KVM8 | KVM4 | **9/28 MIGRATED today**; KVM8 nine disabled `state=migrated` | HIGH |
| Cron (script jobs) | KVM8 | ? undocumented | **19 ORPHANED on KVM8** (no runner — bodies are KVM8 assets) | HIGH |
| Databases (pg/qdrant/falkor/minio) | KVM8 | KVM8 | **KVM8 docker data plane** (KVM4 has fed-redis only) | HIGH |
| Voice / TTS engines | KVM8 | KVM8 | **KVM8** (AAA/audio 13 processed; apa bridges) — KVM4 has audio_cache only | MED |
| i-ARIF (voice identity) | KVM8 | KVM8 (no port, FED chains) | **KVM8 assets** (i-arif-v9.json + manifest); model alias `i-arif` resolves via FED | MED |
| NATS | KVM8 | KVM8 hub | **KVM8 hub + KVM4 nats-leaf container** (leaf→hub link config UNKNOWN) | MED |
| MCP (organ surfaces) | KVM8 | KVM8 (public via Caddy) | **KVM8** + public https endpoints consumed by KVM4 gateway | HIGH |

---

## 3. ASSUMPTION ATTACKS (555)

**A "KVM4 is fully migrated" — FALSE (as a whole), TRUE (for its mandate).**
Evidence: gateway+telegram+FED-compute live ✓. But skills 17/128, no lanes, script-cron 0/19, memory MEMORY.md=326 bytes. KVM4 is a *complete brain on a thin body*.

**B "KVM8 still owns governance" — TRUE.**
Evidence: kernel :8088 healthy (identity 73a284a6, drift aligned), judge/seal chains, AAA/A2A, VAULT999 primary, arifFlow. KVM2 fork explicitly NOT the judge (witness lane).

**C "Memory is synchronized" — FALSE.**
Evidence: three memory planes, no bridge: KVM4 MEMORY.md (326B, Sep 2) ≠ KVM8 seat (sessions.db, no MEMORY.md) ≠ kernel L1–L6 (explicit-call). Nothing syncs them; dream-engine (the intended consolidator) was stillborn-duplicated, working twin now on KVM4.

**D "Tools and skills are identical" — FALSE.**
Evidence: parity counts 128/17/217 above; E3E baseline shows discovery converges (4/4) where harnesses live — the *mesh* distributes, the *gateway home* is poor. Tools (MCP) are identical by URL; skills are not.

**E "API keys and secrets are aligned" — TRUE with 9 named exceptions.**
Evidence: 311 shared key names; normalized value-hashes: **302 identical, 9 differ** — `ARIFOS_SOVEREIGN_BASIC`, `ARIFOS_STRICT_MODE`, `ARIFOS_VECTOR_DIM`, `EMBEDDING_BACKEND`, `RERANK_BACKEND` (machine-role flags, plausibly intentional) + **`TELEGRAM_ALLOWED_CHATS/USERS/GROUP_*` (4 keys — real drift, residue of Sep-3 emergency allowlist fixes)**.
Method note: raw comparison showed 275/311 "different" — a quoting artifact; normalized pass was required. (No pretending, including to myself.)

**F "SOUL is canonical" — TRUE AS OF TODAY 08:18.**
Evidence: was forked (14436B Sep-2 twins vs 13257B Sep-3 live); unified to KVM4 canonical, one inode both KVM8 bodies, a2a anchor → `/root/.hermes/SOUL.md` (valid path both machines). Backup: `SOUL.kvm8-preUnify.md`.

**G "Config files reflect reality" — MOSTLY TRUE AFTER TODAY; runtime wins.**
Evidence: `expected_kvm` registry drift (openclaw KVM2→KVM8) fixed today; KVM4 config notes honest (they document their own Sep-3 wound); hairpin claim in MACHINE_MAP (`KVM4→KVM8:4000→KVM4`) **contradicted by live config** (`base_url: http://100.64.0.5:4000/v1` = direct-to-KVM4-litellm) — the map row is stale on this point; flagged YELLOW, unverified which path fed-aware middleware uses.

---

## 4. REALITY COMPARISON TABLES (777 — EXPECTED vs ACTUAL, G/Y/R)

| Component | Expected | Actual | Status |
|---|---|---|---|
| Telegram token (ASI) | KVM4 | KVM4 gateway, single holder | 🟢 |
| Hermes sessions | KVM4 | KVM4 (sessions + channel_directory 15 targets) | 🟢 |
| Memory files | unified/bridged | split 3 ways, no bridge | 🔴 |
| Skills on gateway | ≈mesh parity | 17 vs 128 vs 217 | 🔴 |
| Lane isolation | follows gateway | absent on KVM4 (group privacy?) | 🔴 |
| Script cron | runner somewhere | 19 jobs, zero runner | 🔴 |
| Secrets | aligned | 302/311 + 4 telegram-allowlist drift | 🟡 |
| SOUL | canonical | unified today (was forked) | 🟢 (was 🔴) |
| Ritual cron | KVM4 | migrated today, scheduler live | 🟢 (was 🔴) |
| FED path | documented hairpin | config says direct .5:4000; map stale | 🟡 |
| NATS | hub KVM8 | hub + KVM4 leaf, link config UNKNOWN | 🟡 |
| VAULT999 | KVM8 SOT | KVM8 + KVM4 mirror (03:47) | 🟢 |
| Voice/i-ARIF | KVM8 | KVM8 assets, alias via FED | 🟢 |
| Databases | KVM8 | KVM8 data plane | 🟢 |
| Governance | KVM8 | kernel/AAA/organs verified live | 🟢 |

**Count: 7 🟢 · 3 🟡 · 4 🔴**

---

## 5. 888 APEX — Q1–Q10

**Q1 What actually moved?** Hermes ASI gateway + Telegram ASI ingress + FED compute (litellm→KVM4) + opencode presence + (today) 9 cron rituals + SOUL canonicalization.
**Q2 What never moved?** Kernel/judge, AAA+A2A, all organs (A-FORGE/GEOX/WEALTH/WELL/FRAME/SIGNAL), OpenClaw, data plane (pg/qdrant/falkor/minio/searxng), VAULT999 primary, voice/TTS + i-ARIF assets, public web (Caddy), skills canonical home (AAA), secrets vault (KVM8 = registry + docs).
**Q3 What moved partially?** FED (front door KVM8 / compute KVM4 — split by design, hairpin claim unverified); cron (9/28); hermes memory (MEMORY.md only, 326B); skills (0 mesh-sync to KVM4 home); lanes (0%).
**Q4 What appears duplicated?** SOUL bodies (unified today); /root/HERMES ≡ ~/.hermes partial-inode twins (cron+logs shared, repo tree heritage); dream-engine jobs (dupe retired today); KVM2 arifosmcp fork (intentional witness); VAULT999 (intentional mirror); secrets (vault vs flat — intentional distribution).
**Q5 What still points to old locations?** 19 script jobs' book on KVM8; MACHINE_MAP hairpin row (stale); historical a2a outcome cards referencing old endpoints (archive); `now` fixed today (was ghost).
**Q6 If KVM4 disappears:** ASI💃 mute; **all model routing dies** — every path converges on KVM4 litellm (organs via KVM8 front door → backend `fed_primary 100.64.0.5:4000`; hermes direct `.5:4000` — hairpin claim DISPROVEN by live probe 08:45: KVM8→.5 direct = alive, HAProxy backend = .5, hermes base_url = .5). i-arif voice dead. *Single model-compute node = the federation's true choke point.*
**Q7 If KVM8 disappears:** kernel/judge dead, all organs dead, AAA/A2A dead, FED front door dead (hermes brain SURVIVES — direct .5 path, but bot becomes lawless+blind: no MCP organs), mesh hub dead, data plane dead, VAULT999 primary dead (mirror survives). *The federation stops governing; the bot keeps thinking alone.*
**Q8 True Source of Truth:** Identity → AAA cards + kernel sessions (KVM8). Memory → kernel L1–L6 + VAULT999 (KVM8). Telegram → tokens in kunci-mas (KVM8 vault, flat copy KVM4); ASI runtime KVM4. Governance → kernel :8088 (KVM8). Execution → A-FORGE (KVM8) + hermes gateway (KVM4). Skills → AAA canonical (KVM8). Configuration → per-organ repos (KVM8) + hermes config (KVM4).
**Q9 Verdict: C — Partial Migration Chaos, closing.** Not monolith (execution genuinely distributed); not clean federation (4 RED residues + circular FED coupling); not unknown (this map exists). The chaos is bounded and enumerated.
**Q10 Minimum-change path to ZEN** — see §6.7. Lowest entropy from CURRENT reality, no redesign.

---

## 6. SUCCESS-CRITERIA OUTPUTS

### 6.1 Federated Reality Map
§2 table IS the map. One-line shape: **brain on KVM4, law+memory+body on KVM8, witness on KVM2, circular blood supply between KVM4⇄KVM8.**

### 6.2 Migration Completeness Score
Against the placement doctrine (not against "everything on KVM4"): 23 components → **7 🟢 aligned (30%) · 3 🟡 (13%) · 4 🔴 (17%) · 9 n/a-never-in-motion (39%)**. Of components that were IN motion: **7 of 11 complete (64%)**, tails: skills, lanes, script-cron, memory-bridge.

### 6.3 Drift Inventory (live)
1. Skills parity 17/128 (gateway home) — HIGH
2. Lane isolation absent on KVM4 — HIGH (privacy class)
3. 19 orphaned script jobs — MED
4. Telegram allowlists ×4 keys differ vault↔flat — MED
5. MEMORY.md 326B vs seat sessions.db — MED (by-design split, no bridge)
6. MACHINE_MAP hairpin row vs live config — LOW (doc)
7. NATS leaf link config UNKNOWN — LOW
8. KVM2→KVM4 :4000 blocked (mechanism unknown) — LOW (witness lane)

### 6.4 Source-of-Truth Inventory
See Q8. Note the one DUAL custody: Telegram tokens (vault KVM8 = registry truth; flat KVM4 = runtime truth) — reconciled by the 4-key allowlist drift finding.

### 6.5 Hidden Coupling Inventory
1. **Circular FED**: KVM8 front door ⇄ KVM4 compute (either death = total cognition loss) — the deepest one.
2. SOUL/config references crossing machines (a2a anchor fixed to dual-valid path today).
3. VAULT999 mirror depends on KVM8 timer reaching KVM4 (mesh).
4. Cron script jobs' bodies assume KVM8 assets forever.
5. Skills mesh assumes AAA canonical reachable from all homes.

### 6.6 Top 10 Entropy Sources (current, ranked)
1. Circular FED coupling (Q6+Q7 lethality)
2. Skills parity gap on the sovereign's gateway
3. Lane isolation regression (silent, privacy class)
4. 19 runnerless cron promises
5. Memory three-way split, no consolidation bridge
6. arifFlow g=0.4605 PATHOLOGICAL (blocks Grammar re-seal)
7. Telegram allowlist drift (4 keys)
8. Twin-home inode aliasing (HERMES ≡ ~/.hermes) — cognitive tax, bit me twice today
9. WELL sensors MOCK 127d (bridge darkness — ASI proposal §3.3)
10. Authority-migration ContradictionDetector noise (7 disagreements/30min)

### 6.7 Minimum-Change Zen Plan (from CURRENT reality — no redesign)
1. **~~Kill the circular coupling~~ RESOLVED BY PROBE 08:45**: hermes KVM4 → litellm is ALREADY direct (`.5:4000`); no hairpin exists for the model path (only public front-door traffic hops KVM8→KVM4 once). Action reduces to: strike the stale MACHINE_MAP row (done in ledger) + accept that **KVM4 litellm is the single model-compute node** — a standby litellm (KVM8 container, cold) is the only real resilience lever, F13-gated.
2. **Convert the 19 script jobs to `/etc/cron.d` on KVM8** (they're scripts; they need no brain). Book archived with receipts. Phase-2 of today's migration.
3. **Mesh-sync skills to KVM4 gateway home** (existing `e3e_skill_mesh.sh` + skill-learn-ingest already do this pattern — one run + verify 17→parity).
4. **Port `lanes.yaml` to KVM4 + one two-person group test** — or consciously retire lanes if superseded. Privacy class: do not leave it UNKNOWN.
5. **Reconcile the 4 telegram allowlist keys** (single edit, vault→flat, with datestamp).
6. **Memory: no new store.** Wire dream-engine (now alive on KVM4) to write session summaries → kernel L3 (ASI proposal Phase 2 — already awaiting F13).
7. Stop: nothing else. The remaining 🟡s (NATS leaf doc, KVM2 block mechanism) are documentation-class, one probe each when next touched.

## 7. EXECUTION LEDGER (2026-09-04 ~08:35–08:40 MYT, F13 'ok go')

| Zen step | Outcome | Evidence |
|---|---|---|
| 1 circular coupling | RESOLVED-BY-PROBE (no hairpin; single-compute finding stands) | curl ×2 + HAProxy backend |
| 2 script cron | **DONE** — 14 jobs → `/etc/cron.d/hermes-legacy-scripts` (+cron-deliver.sh wrapper for 5 telegram); book receipts 003343 | crontab file + 0 enabled on KVM8 |
| 3 skills parity | **DONE** — 17 → **128** on KVM4 gateway home (rsync, exclusions) | live count |
| 4 lanes | **PORTED (file ×2 layouts) + F13 FINDING**: no lane plugin in KVM4 install → per-person group isolation NOT deployed on gateway; deploy plugin or retire doctrine (needs 2-human test) | plugins listing |
| 5 allowlists | **DONE** — union applied both env files (29/28/16/15 IDs); runtime king config.yaml untouched | diff receipts |
| 6 memory bridge | **WIRED** — dream-engine prompt += kernel L3 write (schema-tolerant, fail-open); first L3 write at next fire 2026-09-05 00:00 MYT | receipt 003434 |
| stragglers | +3 agent jobs to KVM4 (arifflow-digest 22:00, gdrive 02:00, reddit 09:00 today); fail-closed mixed-patch rejection proved validator discipline | receipts 003542×2 |

**KVM8 book: 28 jobs / 0 enabled. KVM4 book: 14 jobs / 13 enabled, scheduler restarted 00:36:25Z.**

---
*Witnesses: systemd units ×3 machines, hermes logs+config ×2, secrets vaults ×2 (hash-only), inode forensics, cron receipts ×2, E3E baseline, validator chain. No component was asserted from memory. UNKNOWNs stand as UNKNOWN. DITEMPA BUKAN DIBERI.*
