from pathlib import Path

repls = {
    '[[ARIF_SITES_README.md]]': '`wiki/raw/ARIF_SITES_README.md`',
    '[[HUMILITY_SPEC.md]]': '`wiki/raw/HUMILITY_SPEC.md`',
    '[[CONSTITUTION.md]]': '`wiki/raw/CONSTITUTION.md`',
    '[[README.md]]': '`README.md`',
    '[[GEOX_README.md]]': '`wiki/raw/GEOX_README.md`',
    '[[GEOX_MANIFESTO.md]]': '`wiki/raw/GEOX_MANIFESTO.md`',
    '[[Floors.md]]': '[[Floors]]',
    '[[Trinity_Architecture.md]]': '[[Trinity_Architecture]]',
    '[[K000_LAW.md]]': '`wiki/raw/K000_LAW.md`',
    '[[Metabolic_Loop.md]]': '[[Metabolic_Loop]]',
    '[[Concept_Floor_Tensions.md]]': '[[Concept_Floor_Tensions]]',
    '[[Concept_Epistemic_Circuit_Breakers.md]]': '[[Concept_Epistemic_Circuit_Breakers]]',
    '[[TRINITY_ARCHITECTURE.md]]': '`wiki/raw/TRINITY_ARCHITECTURE.md`',
    '[[Start_Here]]': '[[quickstart]]',
    '[[Concept_Metabolic_Loop]]': '[[Metabolic_Loop]]',
    '[[Concept_Software_2.0]]': 'Software 2.0',
    '[[Concept_Zero_Maintenance_Knowledge]]': 'zero-maintenance knowledge systems',
}

for path in Path('/root/arifOS/wiki/pages').glob('*.md'):
    text = path.read_text()
    new_text = text
    for old, new in repls.items():
        new_text = new_text.replace(old, new)
    if new_text != text:
        path.write_text(new_text)

print('link cleanup done')
