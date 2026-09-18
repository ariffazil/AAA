# Quarantine ledger — skill redundancy, 2026-09-19

Tertib: recover content into the successor FIRST, then quarantine the orphan.

- **recover** `/root/AAA/skills/reflective/sovereign-recognize/SKILL.md` -> `/root/AAA/skills/human-interface/audience-scoped-disclosure/references/absorbed-sovereign-recognize.md`
  - sha_before `0cef1ae064972f7c67565ff80efc0ba5ab57247e26c4ff4a0dc648e273b84772` / sha_after `12ef447079f5b5967df241ac50bf0b2865d231fad95bb79ee4da9f4f8efd7e13`
- **recover** `/root/AAA/skills/capabilities/synthesis/AGI-decisions-reflect/SKILL.md` -> `/root/AAA/skills/domains/general/apex/recursive-audit/APEX-humility-godel/references/absorbed-AGI-decisions-reflect.md`
  - sha_before `bdd203b0bb31364cf6f6aefc11d024a1baa8b4499ace21947e42dfc315c67f2a` / sha_after `47606e90d14b576ba02c840839462e5f0cfad6b4451a543e9f3ffb8661a950c2`
- **quarantine** `/root/AAA/skills/reflective/sovereign-recognize` -> `/root/AAA/.quarantine-redundancy-2026-09-19/sovereign-recognize`
  - REVERSE: `mv /root/AAA/.quarantine-redundancy-2026-09-19/sovereign-recognize /root/AAA/skills/reflective/sovereign-recognize`
- **quarantine** `/root/AAA/skills/capabilities/synthesis/AGI-decisions-reflect` -> `/root/AAA/.quarantine-redundancy-2026-09-19/AGI-decisions-reflect`
  - REVERSE: `mv /root/AAA/.quarantine-redundancy-2026-09-19/AGI-decisions-reflect /root/AAA/skills/capabilities/synthesis/AGI-decisions-reflect`
- **repoint** `/root/AAA/skills/.archive/2026-09-16-skill-zen-quartet/sovereign-recognize` -> `/root/AAA/skills/human-interface/audience-scoped-disclosure/references/absorbed-sovereign-recognize.md`
