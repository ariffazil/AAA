# Patch-Tool Failure Modes for Python Source Injection

> **Verified failure:** 2026-08-11, AAA capability loader (`/root/AAA/scripts/aaa_capability_loader.py`).
> **Recovery:** Backup at `aaa_capability_loader.py.bak-20260811T224459Z-pre-musyawawah` was restored before re-application.
> **Lesson location:** parent skill's "Patch-Tool Failure Modes for Python Source Injection" section.

## Reproduction transcript (excerpt)

```
$ python3 /root/AAA/scripts/aaa_capability_loader.py /root/AAA/federation/AAA_CAPABILITY_REGISTRY.yaml
File "/root/AAA/scripts/aaa_capability_loader.py", line 487
    print("
          ^
SyntaxError: unterminated string literal (detected at line 487)
```

The broken file was produced by a `patch` call that supplied a Python function with `\"\"\"` triple-quoted docstring and `f"..."` strings inside its body. The backslash-escaped quotes inside the `new_string` parameter were interpreted at the tool's input layer, producing invalid Python source on disk.

## Root cause

The `patch` tool is a string-replacement utility. It does not understand:
- Python's indentation context (a function body inside a class must match its enclosing indent)
- Triple-quoted string delimiters (`"""..."""` vs single-quote `"..."`)
- Escape rules for embedded quotes

When `new_string` contains any of:
1. Triple-quoted strings (`"""..."""`, `'''...'''`)
2. f-strings with nested double quotes inside `{}` braces
3. Backslash-escaped quotes (`\"`)
4. More than ~15 lines of mixed indentation

…then the replacement produces syntactically invalid Python, even though the input parameter looked correct to the user.

## Safe pattern (used in the recovery)

```python
from pathlib import Path

BACKUP = Path('/root/AAA/scripts/aaa_capability_loader.py.bak-20260811T224459Z-pre-musyawawah')
TARGET = Path('/root/AAA/scripts/aaa_capability_loader.py')

src = BACKUP.read_text()

# 1. Inject new imports after the marker
src = src.replace(
    "import yaml\n",
    "import yaml\nimport requests\nimport json\n",
    1
)

# 2. Inject a new function before a stable marker
musyawawah_func = '''def _musyawawah_phase(...):
    """..."""
    ...
'''
src = src.replace("# --- CLI ---", musyawawah_func + "# --- CLI ---", 1)

# 3. Replace the call site
old_return = """    return CapabilityIndex(
        ...
    )"""
new_return = """    _index_pre = CapabilityIndex(...)
    final_verdict = _musyawawah_phase(_index_pre, raw)
    return replace(_index_pre, architectural_verdict=final_verdict)"""
src = src.replace(old_return, new_return, 1)

TARGET.write_text(src)

# 4. Mandatory pre-flight: AST parse check
import ast
ast.parse(src)
print("OK")
```

## Pre-flight decision tree (run before any `patch` on Python source)

```
IF new_string contains """...""" or '''...'''    → use write_file or python heredoc
ELIF new_string contains f"...{...}..."            → use write_file or python heredoc
ELIF new_string has backslash-escaped quotes (\")  → use write_file or python heredoc
ELIF new_string has > 15 lines                     → use write_file or python heredoc
ELSE                                              → patch is safe
```

## Backup naming convention (used 2026-08-11)

`/path/to/file.py.bak-<YYYYMMDDTHHMMSSZ>-pre-<reason>`

Examples:
- `aaa_capability_loader.py.bak-20260811T224459Z-pre-musyawawah`
- `AAA_CAPABILITY_REGISTRY.yaml.bak-20260811T224459Z-pre-musyawawah`

The `<reason>` tag makes the purpose greppable:
```bash
ls -la /root/AAA/scripts/*.bak* | grep pre-musyawawah
```

## Recovery (canonical recipe)

```bash
# 1. Find a backup
ls -la /root/AAA/scripts/*.bak* | grep pre-musyawawah

# 2. Restore
cp /root/AAA/scripts/aaa_capability_loader.py.bak-20260811T224459Z-pre-musyawawah \
   /root/AAA/scripts/aaa_capability_loader.py

# 3. Verify it parses
python3 -c "import ast; ast.parse(open('/root/AAA/scripts/aaa_capability_loader.py').read()); print('OK')"

# 4. Re-apply your change using python heredoc or write_file
```

## When to use which tool

| Tool | Use case |
|------|----------|
| `patch` (Hermes internal) | Single-line edits, renames, one-line additions, typo fixes. |
| `skill_manage(action='patch')` | Editing SKILL.md or any YAML file where the patch payload contains no Python source with escaped strings. |
| `write_file` (Hermes internal) | Full file rewrite, new file creation, any Python source > ~15 lines or with escaped strings. |
| `python3 << 'PYEOF'` heredoc | Surgical insertion into an existing Python file. Most flexible: lets you use Python's text manipulation (`str.replace`, `re.sub`) before writing. |

## Related skill sections

- Parent skill: `software-development/aaa-skill-authoring-craft/SKILL.md` — see "Patch-Tool Failure Modes for Python Source Injection" section.
- Bundled companion: `software-development/hermes-agent-skill-authoring/SKILL.md` — protected; covers SKILL.md frontmatter but not Python source editing.
