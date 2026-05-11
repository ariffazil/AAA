---
name: mmx-cli-install-fix
description: Fixes "mmx command not found" — the wrong package (minimax-mcp pip) was installed instead of the actual mmx-cli npm package.
triggers:
  - '"mmx" command not found'
  - 'minimax mcp cannot use'
  - 'which mmx returns empty'
  - mmx image generation broken
  - pip install minimax-mcp was done thinking it was the CLI
Pitfalls:
  - 'minimax-mcp on PyPI is a Claude config helper, NOT the mmx CLI'
  - 'pip install mmx fails — no such package on PyPI'
  - 'npm install @minimax/mmx fails — not in npm registry'
  - 'The correct npm package is mmx-cli (not @minimax/mmx)'
---

# mmx-cli Install Fix

## Symptoms
- `which mmx` → nothing
- `mmx --version` → command not found
- `minimax-mcp` (pip package) is installed — WRONG THING

## Root Cause
Two completely different packages share similar names:
- `minimax-mcp` (PyPI) = Claude config helper for MiniMax — NOT the CLI ❌
- `mmx-cli` (npm) = Actual MiniMax CLI with `mmx` binary ✅

## Fix (one command)

```bash
npm install -g mmx-cli
```

## Verify
```bash
which mmx        # must return /usr/bin/mmx or similar
mmx --version    # must show version (1.0.12)
mmx auth status  # must show API key + region
mmx config show  # must show config
```

## If mmx auth shows no API key
```bash
mmx auth login --api-key <your-api-key>
```

## All mmx capabilities (once installed)
- `mmx image generate --prompt "..." --aspect-ratio 16:9 --out-dir /tmp/`
- `mmx text chat --message "..."`
- `mmx speech synthesize --text "..." --out hello.mp3`
- `mmx video generate --prompt "..." --async`
- `mmx music generate --prompt "..." --out song.mp3`
- `mmx vision photo.jpg`
- `mmx search "..."`
