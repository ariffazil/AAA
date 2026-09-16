#!/usr/bin/env python3
"""Parse a FED litellm-config.yaml: per-lane deployment order + router fallbacks.

WHY THIS EXISTS: some model_list entries write their fields in inverted order,
with `model_name:` at the END of the block (the fed/vision and hermes-asi-vision
chains do). A splitter keyed on '- model_name:' swallows the preceding entry's
body into one block and silently drops unrelated lanes. This parser splits on
the column-0 list marker instead, then reads each field from anywhere inside.

Usage:
    python3 parse-chain-map.py [config.yaml] [lane ...]

Exit codes:
    0  ok
    1  at least one fallback rung does not resolve to a defined model_name
       (a dangling reference: no config-time error, silent runtime failure)
"""
import collections
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/root/A-FORGE/litellm-config.yaml"
wanted = set(sys.argv[2:])
lines = open(path).read().split("\n")

top_level = lambda l: bool(l) and not l.startswith(" ") and not l.startswith("-")


def bounds(start_pred):
    s = next(i for i, l in enumerate(lines) if start_pred(l))
    e = len(lines)
    for i in range(s + 1, len(lines)):
        if top_level(lines[i]):
            e = i
            break
    return s, e


def field(entry, key):
    pat = re.compile(r"^\s*-?\s*%s:\s*(.+)$" % re.escape(key))
    for x in entry:
        m = pat.match(x)
        if m:
            return m.group(1).strip()
    return None


s, e = bounds(lambda l: l.startswith("model_list:"))
entries, cur = [], None
for l in lines[s + 1:e]:
    if l.startswith("- "):
        if cur:
            entries.append(cur)
        cur = [l]
    elif cur is not None:
        cur.append(l)
if cur:
    entries.append(cur)

lanes = collections.OrderedDict()
for ent in entries:
    lanes.setdefault(field(ent, "model_name") or "(unnamed)", []).append(
        (field(ent, "model") or "?", field(ent, "order") or "-",
         field(ent, "supports_vision") or "-"))

print("== model_list: %d deployments across %d lanes ==" % (len(entries), len(lanes)))
for name, deps in lanes.items():
    if wanted and name not in wanted:
        continue
    print("\n%-20s (%d)" % (name, len(deps)))
    for model, order, vision in deps:
        print("   order=%-4s vision=%-5s %s" % (order, vision, model))

try:
    fs, _ = bounds(lambda l: l.startswith("  fallbacks:"))
except StopIteration:
    print("\n(no fallbacks block)")
    sys.exit(0)

fb, key = collections.OrderedDict(), None
for l in lines[fs + 1:]:
    m = re.match(r"^  - (\S+):\s*$", l)
    if m:
        key = m.group(1)
        fb[key] = []
        continue
    m = re.match(r"^    - (.+)$", l)
    if m and key:
        fb[key].append(m.group(1).strip())
        continue
    if l and not l.startswith(" "):
        break

print("\n== router_settings.fallbacks ==")
for k, v in fb.items():
    print("  %-18s %s" % (k, ", ".join(v)))

dangling = sorted({r for v in fb.values() for r in v} - set(lanes))
missing_keys = sorted(set(fb) - set(lanes))
if missing_keys:
    print("\n[WARN] fallbacks keys with no matching lane: %s" % ", ".join(missing_keys))
if dangling:
    print("\n[FAIL] fallback rungs with no model_name definition: %s" % ", ".join(dangling))
    sys.exit(1)
print("\n[OK] every fallback rung resolves to a defined model_name")
