#!/usr/bin/env python3
"""Diff a served MCP tool schema against the handler signatures in its source.

  mcp_schema_signature_diff.py <server.py> <schema_cache.json> <server-key>

Both sides are machine-readable, so diff the whole surface instead of reading one tool.

WHAT THIS MEASURES (and what it does not)
  - property NAMES, in both directions. A handler in code that is not served is reported
    as CODE-ONLY; a served tool with no handler is NO HANDLER.
  - annotation-vs-served `type`, reported as INFO only. `ast` annotations are optional in
    Python, so a type disagreement with no annotation is invisible here.
  - `required` keys the code gives a default to (served REQUIRES / code optional).

IT DOES NOT measure nested object schemas, enums, defaults values, or descriptions.
An OK verdict is a statement about names, required-ness and coarse types -- never quote it
as "the schema is correct".

Exit: 0 all agree, 1 disagreement found, 2 the inputs could not be read (a crash is not a
finding -- say so instead of letting a traceback look like one).
"""

import ast
import json
import os
import sys
import time


def die(msg):
    print("EXIT 2 (input unreadable): " + msg)
    return 2


def is_tool_decorated(node):
    """True iff the function carries a tool-registration decorator.

    Only the decorator decides what counts as a tool. Without this filter the reverse
    direction reports every internal helper (get_db, log_event) as a CODE-ONLY finding,
    which is noise -- and noise in a diff is how a real row gets skipped.
    """
    for d in node.decorator_list:
        target = d.func if isinstance(d, ast.Call) else d
        name = target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
        if name and (name == "tool" or name.endswith("_tool")):
            return True
    return False


def code_signatures(path):
    """function name -> names of its declared parameters (self/ctx dropped).

    Two maps: `tool` for decorated handlers, `helper` for everything else. Only `tool`
    participates in the diff; `helper` is returned so the caller can report the ratio.
    """
    src = open(path, encoding="utf-8", errors="replace").read()
    tree = ast.parse(src)
    out = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        args = [a for a in node.args.args if a.arg not in ("self", "ctx", "cls")]
        n_default = len(node.args.defaults)
        defaulted = {a.arg for a in args[len(args) - n_default:]} if n_default else set()
        ann = {a.arg: ast.unparse(a.annotation) for a in args if a.annotation is not None}
        out[node.name] = {"args": [a.arg for a in args], "defaulted": defaulted,
                          "ann": ann, "tool": is_tool_decorated(node)}
    return out


def served_schemas(path, key):
    data = json.load(open(path, encoding="utf-8"))
    entry = data.get(key)
    if entry is None:
        return None
    tools = entry.get("tools", entry) if isinstance(entry, dict) else entry
    out = {}
    for t in tools:
        sch = t.get("inputSchema") or {}
        out[t.get("name")] = {
            "props": set((sch.get("properties") or {}).keys()),
            "required": set(sch.get("required") or []),
            "types": {k: v.get("type") for k, v in (sch.get("properties") or {}).items()},
            "desc": (t.get("description") or ""),
        }
    return out


def main(argv):
    if len(argv) != 4:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    server_py, cache_json, key = argv[1], argv[2], argv[3]

    for p, what in ((server_py, "server source"), (cache_json, "schema cache")):
        if not os.path.isfile(p):
            return die(what + " not found: " + p)

    try:
        code = code_signatures(server_py)
    except SyntaxError as e:
        return die("cannot parse " + server_py + ": " + str(e))

    allfns = code
    code = {k: v for k, v in allfns.items() if v["tool"]}
    helpers = len(allfns) - len(code)
    if not code:
        return die("no tool-registered handlers found in " + server_py +
                   " (no @tool decorator). The reverse direction cannot be trusted here.")
    print("code: %d tool-registered handlers, %d internal helpers ignored" % (len(code), helpers))

    served = served_schemas(cache_json, key)
    if served is None:
        have = sorted(json.load(open(cache_json, encoding="utf-8")).keys())
        return die("server key '" + key + "' not in " + cache_json + "; present: " + ", ".join(have))

    age_h = (time.time() - os.path.getmtime(cache_json)) / 3600.0
    print("cache: " + cache_json)
    print("       age %.1f h  -> a stale cache is the main way this diff reports a false OK" % age_h)
    if age_h > 24:
        print("       WARN cache older than 24h: treat CODE-ONLY rows as cache staleness first")
    print("")

    print("%-34s%7s%6s  %s" % ("tool", "served", "code", "status"))
    print("-" * 62)

    findings = []
    for name in sorted(set(served) | set(code)):
        s = served.get(name)
        c = code.get(name)
        if s and not c:
            status, sk, ck = "NO HANDLER", s["props"], None
        elif c and not s:
            status, sk, ck = "CODE-ONLY", set(), set(c["args"])
        else:
            sk, ck = s["props"], set(c["args"])
            status = "OK" if sk == ck else "DIFF"
        print("%-34s%7d%6d  %s" % (name, len(sk), len(ck) if ck is not None else 0, status))
        if status != "OK":
            findings.append((name, sk, ck, status))

    # required-vs-default: a param the schema demands but the code treats as optional
    for name in sorted(set(served) & set(code)):
        s, c = served[name], code[name]
        over = s["required"] & c["defaulted"]
        if over:
            findings.append((name, s["required"], c["defaulted"],
                             "REQUIRED-BUT-DEFAULTED " + str(sorted(over))))

    info = []
    for name in sorted(set(served) & set(code)):
        for a, ann in code[name]["ann"].items():
            jt = served[name]["types"].get(a)
            if jt is None:
                continue
            if "int" in ann and jt == "string":
                info.append((name, a, "code int vs served string"))
            elif "bool" in ann and jt != "boolean":
                info.append((name, a, "code bool vs served " + str(jt)))

    print("")
    print("%d served, %d in code, %d disagree" % (len(served), len(code), len(findings)))
    for name, sk, ck, status in findings:
        print("")
        print(name + "  [" + status + "]")
        if status == "CODE-ONLY":
            print("  registered in code, never served -- a stale cache, or a tool whose")
            print("  availability check dropped it. Both are findings.")
            print("  code args: " + str(sorted(ck)))
        else:
            print("  served: " + str(sorted(sk)))
            print("  code  : " + str(sorted(ck)) if ck is not None else "  code  : NO HANDLER")
    if info:
        print("")
        print("type notes (INFO -- annotations are optional, absence proves nothing):")
        for name, a, msg in info:
            print("  " + name + "." + a + ": " + msg)

    if not findings:
        print("")
        print("All names, required-ness and coarse types agree.")
        print("Scope: this does NOT attest enums, nested schemas, default values or descriptions.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
