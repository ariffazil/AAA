#!/usr/bin/env python3
"""S1 — residue manifest: address vs storage over the two skill trees.

Read-only. Publishes, for every canonical skill:
  storage path · which generation of layout it sits in · bundled flag · view address
and flags links that are broken or self-referential.

Why this is a manifest and not a bulk move: 136 of the flat/one-level skills are
NOT in .bundled_manifest — they are authored, so "tag as bundled" does not fit
them, and moving 170 directories in one pass is a mutation nothing here can
falsify. The manifest states the truth per entry; moves happen per-entry, on
touch, with a receipt.
"""
import os, json, collections

A = '/root/AAA/skills'
H = '/root/.hermes/skills'
OUT = '/root/AAA/reports/residue-manifest-20260918.json'
EXCL = {'.git', '.archive', '.system', '__pycache__', 'references', 'templates',
        'assets', 'scripts', '.archive-20260912', '.curator_backups', '.hub',
        'node_modules', '.venv'}

bundled = set()
with open(os.path.join(H, '.bundled_manifest')) as f:
    for line in f:
        if ':' in line:
            bundled.add(line.split(':', 1)[0].strip())

# ---- storage side: AAA canonical, links NOT followed
# os.walk(followlinks=False) lists a symlinked dir in `dn` but never enters it, so a
# symlinked skill would otherwise be invisible here. Record those explicitly.
storage = collections.OrderedDict()


def record(name, rel, is_link, target):
    parts = rel.split(os.sep)
    if len(parts) == 1:
        kind = 'flat-root'
    elif parts[0] == 'domains':
        kind = 'taxonomy'
    else:
        kind = 'bucket:' + parts[0]
    storage[name] = dict(rel=rel, kind=kind, bundled=name in bundled,
                         is_link=is_link, target=target)


for dp, dn, fn in os.walk(A, followlinks=False):
    if EXCL.intersection(set(dp.split(os.sep))):
        dn[:] = []
        continue
    if 'SKILL.md' in fn:
        record(os.path.basename(dp), os.path.relpath(dp, A), False, None)

for e in sorted(os.listdir(A)):
    p = os.path.join(A, e)
    if os.path.islink(p) and os.path.exists(os.path.join(p, 'SKILL.md')):
        record(e, e, True, os.path.realpath(p))

# ---- view side: the addressing tree, links followed
view = {}
for dp, dn, fn in os.walk(H, followlinks=True):
    rel = os.path.relpath(dp, H)
    if EXCL.intersection(set(rel.split(os.sep))):
        dn[:] = []
        continue
    if 'SKILL.md' in fn:
        view[os.path.realpath(dp)] = rel

no_addr = []
for n, v in sorted(storage.items()):
    p = os.path.join(A, v['rel'])
    real = os.path.realpath(p)
    if real not in view:
        no_addr.append(dict(name=n, **v))

# ---- link integrity
broken, selfref = [], []
for root in (A, H):
    for dp, dn, fn in os.walk(root, followlinks=False):
        for e in list(dn) + fn:
            p = os.path.join(dp, e)
            if os.path.islink(p):
                t = os.path.realpath(p)
                if not os.path.exists(p):
                    broken.append(dict(link=p, target=t))
                elif t in (root, os.path.dirname(p)):
                    selfref.append(dict(link=p, target=t))

kinds = collections.Counter(v['kind'].split(':')[0] for v in storage.values())
out = dict(
    generated_note='S1 residue manifest — address vs storage (2026-09-18)',
    storage_root=A, view_root=H,
    storage_skills=len(storage),
    view_addresses=len(view),
    generations=dict(kinds),
    bundled_in_manifest=sum(1 for v in storage.values() if v['bundled']),
    authored_not_in_bundled_manifest=sum(1 for v in storage.values() if not v['bundled']),
    symlinked_out_of_AAA=sum(1 for v in storage.values()
                             if v['is_link'] and not (v['target'] or '').startswith('/root/AAA')),
    no_view_address=len(no_addr),
    broken_links=broken, self_referential_links=selfref,
    no_address=no_addr,
    storage={k: v for k, v in storage.items()},
)
json.dump(out, open(OUT, 'w'), indent=1)

print(f"storage skills (AAA canonical)      : {len(storage)}")
print(f"view addresses (addressing tree)    : {len(view)}")
print(f"generations                         : {json.dumps(dict(kinds), indent=1)}")
print(f"bundled (in .bundled_manifest)      : {out['bundled_in_manifest']}")
print(f"authored, not in bundled manifest   : {out['authored_not_in_bundled_manifest']}")
print(f"canonical symlinked OUT of AAA      : {out['symlinked_out_of_AAA']}")
print(f"canonical skills with NO view addr  : {len(no_addr)}")
for r in no_addr[:25]:
    print(f"    {r['kind']:<12} {r['name']:<44} bundled={r['bundled']}")
print(f"\nbroken links      : {len(broken)}")
for b in broken: print("    ", b['link'], '->', b['target'])
print(f"self-referential  : {len(selfref)}")
for b in selfref: print("    ", b['link'], '->', b['target'])
print(f"\nwrote {OUT}")
