# WEALTH MCP Monolith Split — Detailed Reference

## Context

The WEALTH MCP server had `canonical.py` at 3493 lines containing 11 tool implementations
in a single `register_canonical_tools(mcp)` function. Each tool was an `async def` decorated
with `@mcp.tool(name=...)` and contained 100-600 lines of business logic.

## Boundary Detection Strategy

### 1. Find Section Comment Headers
```python
for i, line in enumerate(lines):
    s = line.strip()
    if "═══" in s and s.startswith("# "):
        print(f"L{i+1}: {s[:80]}")
```

### 2. Find Decorator Positions
```python
for i, line in enumerate(lines):
    if "@mcp.tool(" in line:
        for j in range(i, min(i+10, len(lines))):
            if 'name="' in lines[j]:
                m = re.search(r'name="([^"]+)"', lines[j])
                if m:
                    print(f"Tool '{m.group(1)}': decorator at line {i+1}")
```

### 3. Map Exact Ranges
Each tool spans from its section comment (or imports) to the blank line before the next section:

| Tool | Start | End | Lines |
|------|-------|-----|-------|
| primitive | 64 | 375 | 312 |
| health | 376 | 752 | 377 |
| diagnose | 753 | 1145 | 393 |
| market | 1146 | 1364 | 219 |
| ledger | 1365 | 1482 | 118 |
| registry | 1483 | 1748 | 266 |
| entropy | 1885 | 2117 | 233 |
| judge_handoff | 2118 | 2274 | 157 |
| indicator | 2275 | 2862 | 588 |
| backtest | 2863 | 3194 | 332 |
| entry_plan | 3195 | 3489 | 295 |

## Indentation Handling

The original code was inside `register_canonical_tools(mcp)` (4-space indent).
When extracting, each line needs:
- Lines with 4-space indent → strip to 0, re-add 4 for new register function
- Lines with 8-space indent → strip to 4, keep as 4+nested
- Empty lines → preserve as-is

```python
def extract_section_body(start, end):
    section = lines[start-1:end-1]
    result = []
    for line in section:
        stripped = line.rstrip('\n')
        if stripped.startswith("    "):
            result.append("    " + stripped[4:])
        elif stripped.strip() == "":
            result.append("")
        else:
            result.append("    " + stripped)
    return "\n".join(result)
```

## Shared Types Module

`types.py` contains:
- Coerced type aliases (CoercedList, CoercedDict, etc.)
- Coercion functions (_coerce_json_string, _coerce_dict_to_list_of_dicts)
- Shared helper (_call_legacy_tool)

**Critical**: types.py must NOT import from tool files. Only tool files import from types.py.

## Orchestrator Pattern

```python
def register_canonical_tools(mcp):
    from wealth_mcp.tools.primitive import register_primitive
    from wealth_mcp.tools.health import register_health
    # ... etc
    
    register_primitive(mcp)
    register_health(mcp)
    # ... etc
    
    return {
        "capital_primitive": mcp._tool_manager._tools.get("capital_primitive"),
        # ... etc
    }
```

## Verification

```bash
# Syntax check all files
for f in wealth_mcp/tools/*.py; do python3 -m py_compile "$f" && echo "OK: $f"; done

# Import chain test
python3 -c 'from wealth_mcp.tools.canonical import register_canonical_tools; print("OK")'

# Tool name verification
python3 -c '
import re
tools = {"primitive": "capital_primitive", "health": "capital_health", ...}
for mod, expected in tools.items():
    with open(f"wealth_mcp/tools/{mod}.py") as f:
        content = f.read()
    match = re.search(r"name=\"([^\"]+)\"", content)
    actual = match.group(1) if match else "NOT FOUND"
    print(f"  {mod}: {"OK" if actual == expected else "MISMATCH"}")
'
```
