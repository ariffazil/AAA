# Scar — Wrong probe pattern → false absence → confident conclusion

**Filed:** 2026-10-04 · FI-008 · w_scar=0.8 · class: probe-methodology
**Demonstrated:** 4 instances, 2026-10-03/04, across three lanes:
1. HERMES: grepped `.arifos` path, concluded non-existence (wrong path form)
2. FI-003: KM-013 regex aimed wrong, read absence
3. FI-003: non-recursive JSON walk missed nested truth
4. FI-003: grepped `handle /api/organs` literally, missed Caddy **named matchers** (`handle @api_organs_aforge`), confidently reported "no explicit organ handles"

**Rule:** A grep that returns nothing proves the grep, not the world. Before asserting
absence: (a) name the alternative surface forms (named matchers, aliases, symlinks,
prefixed keys), (b) probe each, (c) else downgrade the claim to "absent per this
pattern only." Pairs with representation-reality-invariant: negative claims need the
same warrant as positive ones.
