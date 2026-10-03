# Rust Infrastructure Crate Pattern — arifOS

> Standard structure for arifOS Rust infrastructure components.

## Directory Layout

```
project-name/
├── Cargo.toml              # Dependencies: toml, serde, sha2, ed25519-dalek, tokio, chrono, tracing
├── README.md
├── config/
│   └── *.toml              # Runtime policy/config files (TOML format)
├── src/
│   ├── main.rs             # Binary entry point + tracing init
│   ├── lib.rs              # Re-exports all modules
│   ├── types.rs            # Core types (enums, structs, verdicts)
│   ├── policy.rs           # TOML parser + validation + resolution
│   ├── audit.rs            # Append-only audit chain (SHA256 hash linking)
│   ├── crypto.rs           # Ed25519 signature verification
│   └── <domain>.rs         # Domain-specific logic
└── tests/
    └── integration.rs      # Integration tests
```

## Cargo.toml Template

```toml
[package]
name = "project-name"
version = "0.1.0"
edition = "2021"
description = "Short description"
authors = ["arifOS Federation"]

[dependencies]
toml = "0.8"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
ed25519-dalek = { version = "2", features = ["rand_core"] }
tokio = { version = "1", features = ["full"] }
sha2 = "0.10"
hex = "0.4"
chrono = { version = "0.4", features = ["serde"] }
tracing = "0.1"
tracing-subscriber = "0.3"
anyhow = "1"

[[bin]]
name = "binary-name"
path = "src/main.rs"
```

## Conventions

- **Binary entry point:** `main.rs` with `tracing_subscriber::fmt().init()` and anyhow::Result
- **Config loading:** `policy::load_policy(path)` → `Result<Config>`
- **Audit chain:** Append-only JSONL with SHA256 hash linking per entry
- **Crypto:** Ed25519 for sovereign signatures, SHA256 for chain integrity
- **Testing:** Unit tests in each module (`#[cfg(test)] mod tests`)
- **Error handling:** `anyhow::Result` throughout, `.context("description")` for error messages

## Pitfalls

- Never use `unwrap()` in production code paths — always use `?` with `.context()`
- Audit chain file must be opened with `OpenOptions::new().create(true).append(true)`
- TOML parsing fails on YAML-style syntax — validate config format early
- Ed25519 keys are exactly 32 bytes — validate before `VerifyingKey::from_bytes()`
