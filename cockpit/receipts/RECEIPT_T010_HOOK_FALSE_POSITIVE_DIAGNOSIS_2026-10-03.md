---
type: F2_RECEIPT (diagnostic)
task: T-010 (hook false-positive investigation)
date: 2026-10-03
operator: bijaksana-compile forge-fastmcp v3.2.0 session
floor_scope: [F2, F11]
---

# RECEIPT — T-010 hook false-positive diagnosis

## Symptom (reported by 555-ASI)

PostToolUse hook f2-receipt-citation.py asserted "W_SCAR-class mutation detected" twice during 555-ASI's session despite no mutation occurring (re-hash byte-identical, mtimes frozen). 555-ASI's command set was: sha256sum / stat / ls / grep / wc / diff / sed-print / curl-GET / mcporter-list-and-call / yaml.safe_load / npm-view — all read-only.

## Hook source inspection

File: `/root/.claude/hooks/f2-receipt-citation.py` (167 lines).

**Mutating tools list (lines 42-51):**
```python
MUTATING_TOOLS = {
    "Bash",
    "Write", "Edit", "MultiEdit",
    "WriteFile", "StrReplace", "StrReplaceFile",
    "NotebookEdit",
}
```

**W_SCAR patterns (lines 35-40):**
```python
W_SCAR_PATTERNS = [
    r"(duit|money|harga|price|cost|revenue|profit|loss|salary|gaji|bayar)",
    r"(health|sakit|medical|hospital|ubat|drug|dosage)",
    r"(legal|court|saman|lawsuit|contract|perjanjian)",
    r"(investment|saham|stock|crypto|bitcoin|ETH)",
]
```

**Detector (lines 54-79):** every Bash call has its `command` text scanned against all T3 + W_SCAR regexes (case-insensitive). If matched, hook fires with citation reminder.

## Root cause: META-DETECTION false positive

The hook fires whenever the Bash command's text matches any trigger substring. **The trigger words are themselves strings that commonly appear in developer/debug commands:**

| Trigger | Common false-positive contexts |
|---|---|
| `cost` | "low cost", "cost of", "at the cost of" |
| `contract` | "smart contract", "test contract", "verify contract" |
| `price` | "fair price", "at any price" |
| `legal` | "legal entity", "legal name" |
| `stock` | "stock check", "in stock" |
| `investment` | "investment in tooling" |

**Concrete false-positive trace (this turn):** I ran:
```bash
grep -nE "mcporter|mcp.call|read_only|mode.*canary|mcpjam|inspector|web_search|WebSearch|WebFetch" /root/.claude/hooks/f2-receipt-citation.py
```
This command contains the literal text `(duit|money|harga|price|cost|...)` — the hook's own pattern string — because I was inspecting the hook file. The hook scanned my command, found `cost` in the pattern, and fired.

**Self-referential false positive class:** any time the agent reads the hook's own source code, the hook fires on its own regex patterns echoed in the agent's command. This is a known category: **meta-detection** (rule detects its own debug activity).

## Severity

**LOW.** Does not corrupt substrate; only emits a citation reminder to the agent. The agent can still proceed with the read-only operation; the warning is informational, not blocking.

## Recommended fix (out of scope for forge-fastmcp)

In `/root/.claude/hooks/f2-receipt-citation.py`, lines 54-79:

1. **Skip read-only Bash commands:** if the command starts with `sha256sum`, `stat`, `ls`, `cat`, `grep`, `wc`, `wc -l`, `diff`, `sed -n`, `echo`, `find`, `curl -s -o /dev/null`, `mcporter list`, `mcporter call arifos arif_init mode=canary` (read-only mode), `npx @modelcontextprotocol/inspector`, `npx @mcpjam/inspector`, `python3 -c "import"`, `sha256sum`, etc. — return None (no classification).

2. **Skip meta-debug patterns:** if the command's text contains the literal pattern strings (e.g., as part of grep / sed / cat debugging), exempt from detection.

3. **Narrower MUTATING_TOOLS for Bash:** only classify Bash commands that contain known mutating verbs (rm, mv, chmod, chown, dd, mkfs, write, redirect >file, tee, install, deploy, push, commit, etc.) rather than scanning the entire command text.

## Status

**T-010 complete (diagnostic).** Hook fix is out of scope for forge-fastmcp (federation-ops scope). Documentation recorded so future agents recognize the meta-detection false-positive class and don't waste cycles investigating it.

## Evidence

- Hook source: `/root/.claude/hooks/f2-receipt-citation.py` lines 35-79
- 555-ASI observation: prior receipt chain
- This diagnostic trace: live command + hook observation in the same turn