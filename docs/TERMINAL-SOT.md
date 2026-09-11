# ROOT TERMINAL SOT — Shell Init Chain (KVM8 af-forge)

> **Status:** F13 directive 2026-09-12 — *"make sure all file and info bind to root terminal is updated and SOT for all future agents"*
> **Audited by:** FI-003 qwen (live probe, all files read this session)
> **Machine:** KVM8 `100.64.0.2` (seat/court node). Ports here are KVM8-local.

## The Init Chain (who loads what, in order)

```
LOGIN SHELL (ssh / su -)
  → /root/.bash_profile          (compositor: sources .profile + cargo env)
      → /root/.profile           (sources .bashrc + cargo env)
          → /root/.bashrc        (everything below)

INTERACTIVE NON-LOGIN (new terminal in tmux)
  → /root/.bashrc directly
```

`.bash_profile` and `.profile` are thin wrappers — **all real wiring lives in `.bashrc`**.

## What .bashrc loads (in order)

| Order | What | File / effect |
|---|---|---|
| 1 | **Secret vault** | `/root/.secrets/kunci-root.env` via `set -a` + `ARIFOS_VAULT_LOADED` guard (5-R Protocol). Fallback to `kunci-mas.env` alias. Second-chance loader at TZ block (path corrected 2026-09-12) |
| 2 | PATH: kimi-code | `/root/.kimi-code/bin` + `KIMI_CODE_EXPERIMENTAL_SECONDARY_MODEL=1` |
| 3 | PATH: `~/.local/bin` | (multiple idempotent exports — antigravity, qwen, composio, cua) |
| 4 | OpenClaw completions | `/root/.openclaw/completions/openclaw.bash` |
| 5 | **PS1 + HOLD detection** | `/root/scripts/arifos-ps1.sh` + `/root/scripts/arifos-ps1-hold.sh` (Zone 3 interrupt) |
| 6 | Cockpit aliases | `/root/.bash_aliases` (organs, pulse, svcs, ports, dkp, arif-fq, arif-verdict…) |
| 7 | FI wrappers | `agent-init`, `agent-seal`, `rsi`, `forge` (ssh af-forge), `opencode` → preflight wrapper |
| 8 | Banner (local only) | `arifos-banner-cache.sh` — only when NOT ssh/tmux; SSH gets PAM motd |
| 9 | **Qwen yolo functions** | `qwen()` / `qwen-code()` → `-y` auto-approve both interactive + `-p` (functions, not aliases — they survive non-interactive subshells) |
| 10 | Editor + TZ | `EDITOR=vim`, `TZ=Asia/Kuala_Lumpur` + `HERMES_TIMEZONE` (canonical TZ lock — DO NOT REMOVE block) |
| 11 | qwen env | `/root/.secrets/qwen.env` |
| 12 | Claude root workaround | `IS_SANDBOX=1` + `claude-yolo` / `claude-auto` aliases |

## Env SOTs (never hardcode, never commit)

| File | Contents |
|---|---|
| `/root/.secrets/kunci-root.env` | ALL federation keys (ZAI_API_KEY, provider keys). Mode 600. The only edit target — `kunci-mas.env` is a symlink alias |
| `/root/.secrets/qwen.env` | Qwen-specific env |
| `/root/.secrets/aaa-identity/keys/arif_private.pem` | Ed25519 sovereign key (kernel bind/seal scripts use this — sovereign never signs manually) |

## Python / venv

| Path | Role |
|---|---|
| `/root/venv/` | Canonical federation venv (python3). **NOT auto-activated** — agents/scripts call `/root/venv/bin/python3` explicitly |
| `/root/scripts/federation_ritual.py` | `init` / `seal` / `marker` — the sanctioned VAULT999-adjacent lane. `marker` = agent events (hash-chained ritual.log); `seal` = kernel session_seal |
| System python3 | Kernel/organ services run their own venvs under `/opt/arifos` |

## Board / status surfaces

- SSH login → PAM motd (one board)
- `now` → one-shot state pane (time + 10 surfaces + FRAME drift + carry)
- `pulse` → FQ + kernel verdict · `organs` → 6-organ probe
- Health convention: HTTP 401/403 = UP auth-gated; conn-refused/timeout = DOWN. FED :4000 uses `/health/liveliness` ONLY

## Conventions that bite (scar-tested)

1. `ARIFOS_VAULT_LOADED` guard — vault loads ONCE per shell; re-sourcing needs `unset ARIFOS_VAULT_LOADED` first.
2. `qwen` is a **function** (yolo). Bypass with `/root/.local/lib/qwen-code/bin/qwen` for raw flags.
3. TZ lock block is F13-marked — do not remove even when refactoring.
4. `.env-kunci-root` (old path) is dead since Aug 2026 — canonical is `.secrets/kunci-root.env`.
5. Fresh-shell smoke test: `bash -lc 'echo $ARIFOS_VAULT_LOADED $TZ'` → expect `1 Asia/Kuala_Lumpur`.

DITEMPA BUKAN DIBERI ⚒️
