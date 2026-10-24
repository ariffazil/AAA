---
name: rust-federation
description: "Rust dalam federation ini — di mana ia hidup (arifFlow metabolism plane + mcp-governance-interceptor), cara build/test/lint dengan betul, boundary perlembagaan, dan declared-vs-observed. Load bila kerja menyentuh kod Rust. SOT runtime: /root/arifFlow/AGENTS.md."
triggers:
  - "/rust"
  - "arifflow build"
  - "cargo test"
  - "mcp-governance-interceptor"
---

# rust-federation — Rust in the arifOS Federation

> Truth rule (arifFlow canon): **`cargo test` + `curl :7073/health` beat any prose below.**
> If this file and the live probe disagree, the probe wins — fix this file.

## 1. The Rust Map (probed 2026-10-21 · external-review corrections applied same day)

| Component | Path | Edition | Role | Runtime state |
|---|---|---|---|---|
| **arifFlow** | `/root/arifFlow` | 2024 | Metabolism plane: receipts, FQ, invariants F0-F6, holds, VAULT999 sealing | LIVE — `arifflow.service` :7073, deployed `/opt/arifflow/bin/arifflow` = build tree `target/release/arifflow` (sha256 `272acb67…` identical, probed 2026-10-21). `cargo test --lib` 2026-10-21: **245 pass / 1 FAIL** (see §5) |
| **mcp-governance-interceptor** | `/root/AAA/mcp-governance-interceptor` | 2021 | Deterministic MCP tool-call enforcement proxy (policy/router/crypto/audit) | **HOLD / NOT-A-CONTROL** — 480 LOC, never built (no `target/`), never tested. **No MCP call is governed by this code today.** See its `README.md` |
| OS layer | apt | — | `sudo-rs`, `rust-coreutils` | LIVE — Ubuntu 25.10 (`questing`); `/usr/bin/sudo` resolves to `/usr/lib/cargo/bin/sudo` = **sudo-rs is the active sudo** (dpkg-verified) |

**Trinity:** `arifOS (law/Python) · arifFlow (flow/Rust) · A-FORGE (hands/TypeScript)` —
Rust is the **flow** plane only. It schedules, checkpoints, transmits receipts. It never judges
(verdicts = arifOS 888), never originates intent, never executes (execution = A-FORGE).

## 2. Toolchain (probed on this box — invoke the capability, don't infer it from filenames)

- `rustup` stable **1.98.1** (2026-09-01), host `x86_64-unknown-linux-gnu`. **Only stable is
  installed — no nightly toolchain.**
- Working on stable: `cargo`, `clippy`, `rustfmt`, `rust-analyzer`, `rust-gdb`.
- **Miri is NOT usable on this box.** `~/.cargo/bin/cargo-miri` is a rustup proxy symlink; miri is
  a nightly-only component and `cargo miri --version` errors here. (Lesson: a binary name in PATH
  is not a working capability — run it before claiming it.)
- **Guarantee scope (corrects earlier overclaim):** Rust eliminates memory-safety bugs and data
  races **in safe code**. It does not prevent memory leaks, deadlocks, logic bugs, or bugs inside
  `unsafe` blocks and dependencies.
- Build: `cargo build --release` · Test: `cargo test` · Lint: `cargo clippy` · Format: `cargo fmt`
- Versioning (arifFlow Iron Rule): **date-stamped `vYYYY.MM.DD` only. No semver.**

## 3. arifFlow — module map (source of truth for "what exists")

- `src/governance/` — `invariants.rs` (F0-F6 auto-enforcement), `checkpoint.rs`, `cooling.rs`,
  `lineage.rs`, `tri_witness.rs`, `vault999.rs`, `kabarkan.rs` (FQ)
- `src/topology/` — `fan_out.rs`, `pipeline.rs`, `cascade.rs`, `controlled_cycle.rs`
- `src/` core — `merkle.rs`, `jcs.rs` (RFC 8785 canonicalization, bit-compat with Node fixtures),
  `vector.rs` (QG.V0.3 seven-dimension engine), `receipt.rs`, `scheduler.rs`
- `src/bridge/` — `arifos_governance.rs`, `aforge_executor.rs` (compiled, NOT called at runtime)
- Clients: `src/py/arifflow/client.py` · `scripts/check.sh` · TS under `src/ts/`

**Declared-vs-observed (verified in `/root/arifFlow/AGENTS.md` §4, SOT):** the daemon runs the
metabolism plane (ingest/check/release/enforce/health). BSP scheduler + cross-organ bridges are
compiled but inactive. **VAULT999 sealing in the daemon ingest path is a SHA3-256 hash chain**
(`vault999.rs`: `chain_entry_hash = SHA3-256(prev_hash || position_be || checkpoint_hash)`) —
**no Merkle anchoring** (merkle.rs exists but receipts carry `merkle_root: Option`, set `None`;
the vault header itself says "No Merkle anchoring (delegated to merkle.rs when wired)" and
"No /verify endpoint for public chain integrity"). Hash chain = tamper-evident, not
Merkle-provable. Do not describe the governance plane as "live" without a probe.

## 4. Constitutional boundaries (binding when touching Rust code)

1. **F0–F6:** flow transmits, never owns · schedules, never authorizes · checkpoints, never
   judges · observes, never interprets · routes, never executes · connects, never collapses.
2. **Never weaken the fail-closed gate** — `/release` and the min-gate (0.50, `main.rs`) are
   constitutional machinery. Changing them = F13-class, single binary ask to Arif.
3. **`unsafe` blocks = grep-and-justify.** New `unsafe` requires a written invariant in the PR
   receipt. Memory safety is why this plane is Rust; don't spend it casually.
4. **Agent execution loop:** `POST /check` → execute → `POST /ingest` (Execute) → verify →
   `POST /ingest` (Verify) → `POST /release`. Shell: `arifflow_check` / `arifflow_release`.
5. Receipts are hash-chained (`previous_receipt_hash`) — the daemon rejects broken chains.
6. **Receipt independence (external review 2026-10-21):** a receipt ingested by the same actor
   that claims it is **self-attestation**. FQ is a proxy — `verify_count` is self-generable.
   SEAL-grade claims need a witness with `model_lane ≠ executor's` OR `process_tree ≠ executor's`
   (Scar-2026-10-01-002). The writer of a receipt may never be its only checker.

## 5. Known scars / gotchas

- Live-plugin hot-edits are self-blasting (see carry-forward lesson 2026-10: one line-join edit
  bricked every session's tool gate). Rebuild + restart deliberately; never patch running Rust.
- **Capability presence ≠ capability (2026-10-21):** `cargo-miri` in PATH was reported as
  "miri present" from a filename listing; it's a rustup proxy for a nightly-only component that
  errors on this box. Invoke before claiming.
- **OPEN TEST FAILURE (2026-10-21, `cargo test --lib` in /root/arifFlow):** 245 pass, 1 fail —
  `governance::invariants::tests::test_release_hold` (invariants.rs:1166, "Actor should be
  released after hold release"), 2 ignored. The suite is NOT green; don't claim it is. Fixing
  the release-hold path is near constitutional machinery — treat as flagged, not casual work.
- **VAULT999 sealing ≠ Merkle proof system** — see §3. Chain integrity is hash-based and
  self-contained; there is no public `/verify` endpoint.
- **Edition split:** interceptor edition 2021 vs arifFlow 2024 — consistency debt if shared
  crates are ever introduced.
- `invariants.rs.bak-*` / `main.rs.bak-*` files = audited rollback artifacts, not sources.
- Worktree copies under `/root/.federation-worktrees/*/mcp-governance-interceptor` — the canonical
  tree is `/root/AAA/mcp-governance-interceptor`; don't edit worktree copies.

## 6. Pointers (read before deep work)

| What | Where |
|---|---|
| arifFlow constitution + truth rule | `/root/arifFlow/AGENTS.md` |
| Kernel canon | `/root/arifFlow/ARIFLOW_KERNEL_CANON.md` |
| FQ vector spec | `/root/arifFlow/spec/QG_V0_3_VECTOR_SPEC.md` |
| JCS hash contract | `/root/arifFlow/spec/RG2_JCS_HASH_CONTRACT_v1.md` |
| Interceptor status (HOLD / not-a-control) | `/root/AAA/mcp-governance-interceptor/README.md` |
| Rust language axioms | `/root/AAA/knowledge/code/777-systems-programming.json` |
| Federation landing | `/root/AAA/CLAUDE.md` |
