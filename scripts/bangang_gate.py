#!/usr/bin/env python3
"""bangang-gate — the 5-matrix ΔS filter over the canonical skill catalogue.

F13 2026-09-18: "no safety theatre at all in my skills. safety is emergent
attributes; should be in kernel."

So this gate does NOT write declarations into skills. It MEASURES, RANKS, and
ROUTES: irreversible lanes get routed to the kernel gate; weak lanes get pruned.
Nothing is bolted on to a skill body.

Matrices (adapted for plane-awareness):
  M1 F1 AMANAH      irreversible mutation with no HOLD / circuit-breaker route
  M2 F2 TRUTH       ingests raw external signal, emits without a witness step
  M3 F9 ANTI-HANTU  performed persona / filler — MACHINE PLANE ONLY
                    (human-plane register is a REQUIREMENT; a human is a paradox)
  M4 MEMBRANE       organ lane reaching another organ's internals directly
  M5 REDUNDANCY     duplicated / dead-pointed / never-fired trivial lane

ΔS is measured, not asserted: index rent paid vs evidence of use.
Read-only. Writes a ledger.
"""
import os, re, json, hashlib, collections, datetime

HOME = '/root/AAA/skills'
OUT = '/root/AAA/reports/bangang-gate-20260918.json'
FIRINGS = '/root/AAA/reports/skill-firings-20260918.json'
EXCL = {'.git', '.archive', '.system', '__pycache__', 'references', 'templates', 'assets', 'scripts', 'node_modules'}

HUMAN_PLANE = ('counsel', 'well', 'personal-lane', 'human-interface', 'voice-stack', 'audio-emd',
               'cognitive-reflex', 'welfare', 'physique-intel', 'reflective')

FM = re.compile(r'^---\s*\n(.*?)\n---', re.S)

IRREVERSIBLE = re.compile(
    r'\b(deploy|systemctl\s+(restart|start|stop)|git\s+push|force-push|'
    r'rm\s+-rf|unlink|truncate|rotate\s+(the\s+)?(key|token|secret)|revoke|'
    r'send\s+(email|message|note)|publish|post\s+to|withdraw|place\s+(an\s+)?order)\b', re.I)
HOLD_ROUTE = re.compile(r'\b(HOLD|F13|F1\b|888|circuit[- ]?break|jitu|kernel|arif_judge|arif_seal|'
                        r'authority\s+(gate|check))\b', re.I)
EXTERNAL_IN = re.compile(r'\b(paste[ds]?|external\s+(model|ai)|cross-ai|copy-paste|raw\s+(signal|output)|'
                         r'ingest(ed)?\s+(from|an?)\s+(a\s+)?(url|web|model)|unverified\s+(input|claim))\b', re.I)
WITNESS_STEP = re.compile(r'\b(verif|witness|receipt|probe|evidence|tri-?witness|cross-?check|'
                          r'falsif|ground[- ]?truth|recount|re-?measure)\w*', re.I)
PERSONA = re.compile(r'\b(roleplay|role-play|pretend\s+to\s+be|persona\s+of|mimic\s+the\s+voice|'
                     r'empathize|small\s+talk|cheerful\s+tone)\b', re.I)
CROSS_ORGAN = re.compile(r'\b(well_|wealth_|geox_|capital_|arifos_)\w+', re.I)
ORCHESTRATOR = re.compile(r'\b(orchestrator|federation|handoff|A2A|contract|gateway|kernel|bridge)\b', re.I)

firings = {}
try:
    firings = json.load(open(FIRINGS))['firings']
except Exception:
    pass

def plane_of(rel, skill):
    hay = (rel + '/' + skill).lower()
    return 'human' if any(k in hay for k in HUMAN_PLANE) else 'machine'

rows = []
seen_name = collections.defaultdict(list)
for dp, dn, fn in os.walk(HOME):
    dn[:] = [d for d in dn if d not in EXCL]
    if 'SKILL.md' not in fn:
        continue
    p = os.path.join(dp, 'SKILL.md')
    rel = os.path.relpath(dp, HOME)
    txt = open(p, encoding='utf-8', errors='replace').read()
    m = FM.match(txt)
    fm = m.group(1) if m else ''
    skill = os.path.basename(dp)
    body = txt[len(fm):]
    desc = ''
    md = re.search(r'^description:\s*(.+?)(?=\n[a-z_]+:|\n---)', fm, re.S | re.M)
    if md:
        desc = ' '.join(md.group(1).split())
    hits = []
    if IRREVERSIBLE.search(body) and not HOLD_ROUTE.search(body):
        hits.append(['M1_F1_IRREVERSIBLE_NO_HOLD', 'irreversible verb with no HOLD/kernel route'])
    if EXTERNAL_IN.search(body) and not WITNESS_STEP.search(body):
        hits.append(['M2_F2_NO_WITNESS', 'ingests external/raw signal, no witness step'])
    if PERSONA.search(body) and plane_of(rel, skill) == 'machine':
        hits.append(['M3_F9_PERSONA_THEATRE', 'performed persona in a machine-plane lane'])
    organs = sorted({o for o in ('well', 'wealth', 'geox', 'capital', 'arifos') if re.search(o, body, re.I)})
    if len(organs) >= 2 and not ORCHESTRATOR.search(body):
        hits.append(['M4_MEMBRANE_LEAK', f'reaches {organs} with no orchestrator reference'])
    rows.append(dict(skill=skill, rel=rel, plane=plane_of(rel, skill),
                     bytes=len(txt), desc_words=len(desc.split()),
                     firings=firings.get(skill, 0),
                     has_triggers=bool(re.search(r'use when|when to use|triggers?:', txt, re.I)),
                     has_pitfalls=bool(re.search(r'pitfall|gotcha', txt, re.I)),
                     has_verify=bool(re.search(r'verif|receipt|probe', txt, re.I)),
                     sha=hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16],
                     hits=hits))
    seen_name[skill].append(rel)

by_sha = collections.defaultdict(list)
for r in rows:
    by_sha[r['sha']].append(r['rel'])
dupsets = [v for v in by_sha.values() if len(v) > 1]

for r in rows:
    r['stub'] = (r['bytes'] < 1200) or (not r['has_triggers'] and r['bytes'] < 2500)
    r['never_fired'] = (r['firings'] == 0)
    r['name_ambiguous'] = len(seen_name.get(r['skill'], [])) > 1

total_bytes = sum(r['bytes'] for r in rows)
fired = sum(1 for r in rows if r['firings'] > 0)
summary = dict(
    generated=datetime.datetime.now(datetime.UTC).isoformat(),
    canonical_skills=len(rows),
    canonical_bytes=total_bytes,
    est_index_tokens=total_bytes // 4,
    fired_at_least_once=fired,
    never_fired=len(rows) - fired,
    never_fired_pct=round((len(rows) - fired) * 100 / max(1, len(rows)), 1),
    duplicate_body_groups=len(dupsets),
    duplicate_body_skills=sum(len(v) for v in dupsets),
    stubs=sum(1 for r in rows if r['stub']),
    ambiguous_names=sum(1 for r in rows if r['name_ambiguous']),
    m1_irreversible_no_hold=sum(1 for r in rows if any(h[0].startswith('M1') for h in r['hits'])),
    m2_no_witness=sum(1 for r in rows if any(h[0].startswith('M2') for h in r['hits'])),
    m3_machine_persona=sum(1 for r in rows if any(h[0].startswith('M3') for h in r['hits'])),
    m4_membrane_leak=sum(1 for r in rows if any(h[0].startswith('M4') for h in r['hits'])),
    human_plane=sum(1 for r in rows if r['plane'] == 'human'),
)
json.dump({**summary, 'duplicate_groups': dupsets, 'rows': rows}, open(OUT, 'w'), indent=1)

print(json.dumps(summary, indent=1))
for label, key in [('M1 irreversible-without-HOLD -> route to kernel gate', 'M1'),
                   ('M2 external-signal-without-witness', 'M2'),
                   ('M3 persona theatre (MACHINE plane only)', 'M3'),
                   ('M4 membrane leak', 'M4')]:
    print(f"\n-- {label} --")
    sel = [x for x in rows if any(h[0].startswith(key) for h in x['hits'])]
    for r in sel[:22]:
        print(f"   {r['skill']:<44} {r['rel']}")
print("\n-- duplicate bodies --")
for g in dupsets[:15]:
    print("   " + "  ==  ".join(g))
print("\n-- stubs --")
for r in [x for x in rows if x['stub']][:20]:
    print(f"   {r['bytes']:>6}b fire={r['firings']:<3} {r['skill']}")
print(f"\nwrote {OUT}")
