# TOOLS.md — antigravity Agent

## Allowed Tools

### File Operations
- `view_file` — read file contents
- `write_to_file` — create/overwrite file
- `replace_file_content` / `multi_replace_file_content` — surgical string replacement
- `list_dir` — list directory files

### Git Operations
- `run_command` (e.g. `git status`, `git diff`, `git log`)

### Shell Operations
- `run_command` — execute allowed commands with approval
- `manage_task` — manage background tasks

### MCP Surfaces (Allowed Connector Topography)
- `arifos_local` — local development kernel (Rail A)
- `arifos_remote` — remote VPS audit & sealing (Rail B - 888 HOLD)
- `geox` — subsurface/petrophysical intelligence (Rail A)
- `wealth` — capital valuation & planning (Rail A)
- `well` — cognitive fatigue & wellness (Rail B)

### UI & Mockup
- `generate_image` — high-fidelity design generation and asset iteration

## Prohibited Tools

- Creating Windows ghost files (`nul`, `con`, `aux`, `prn`, `com1..9`, `lpt1..9`)
- `docker system prune` or destructive resource deletions without 888_HOLD
- Direct raw credentials manipulation
- Any tool that bypasses arifOS constitutional floors

---

*Last updated: 2026-05-22*
