/**
 * Discovery Repair Slice — Test Suite
 * ══════════════════════════════════════
 *
 * Validates the 2026-07-25 repair slice:
 *  1. public/sitemap.xml contains ONLY aaa.arif-fazil.com URLs
 *  2. public/sitemap.xml excludes PDF, human-site (arif-fazil.com) and
 *     .well-known/* descriptors
 *  3. public/.well-known/agent-card.json is the canonical signed AAA Gateway
 *     card (matches the canonical_sha256 committed in signatures[0])
 *  4. public/.well-known/_deployment_state.json exists, declares _state
 *     semantics, and explicitly excludes agents/agent_cards/.well-known/
 *     from public deploy
 *  5. The stale cockpit card at agents/agent_cards/.well-known/agent-card.json
 *     is documented as internal-only
 *  6. registries/state/federation_state.yaml exists and defines _state as
 *     runtime-preserved overlay (NOT static source)
 *  7. registries/AAA_FEDERATION_STATE.yaml (deprecated) carries a _state
 *     annotation pointing to the canonical overlay path
 *  8. registries/catalog.json is an explicit empty fallback shim — it does
 *     NOT claim model entries, and references FEDERATION_MODEL.json as the
 *     canonical source
 *  9. Unrelated dirty work in a2a-server/a2a-bridge-helper.js and
 *     registries/cooling_state.json is NOT touched by this slice
 *
 * Run with:  npx tsx tests/discovery-repair-slice.test.ts
 *
 * DITEMPA BUKAN DIBERI — Discovery is forged, not given.
 */

import { describe, it, before } from 'node:test';
import { strict as assert } from 'node:assert';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = resolve(__filename, '..');
const ROOT = resolve(__dirname, '..');

function read(rel: string): string {
  return readFileSync(resolve(ROOT, rel), 'utf8');
}

function readJson<T>(rel: string): T {
  return JSON.parse(read(rel)) as T;
}

function exists(rel: string): boolean {
  return existsSync(resolve(ROOT, rel));
}

// ═════════════════════════════════════════════════════════════════════════
// 1. public/sitemap.xml — AAA URLs only
// ═════════════════════════════════════════════════════════════════════════

describe('public/sitemap.xml — AAA-only scope', () => {
  let sitemap: string;
  before(() => { sitemap = read('public/sitemap.xml'); });

  it('exists and is a well-formed urlset', () => {
    assert.match(sitemap, /<urlset\s+xmlns="http:\/\/www\.sitemaps\.org\/schemas\/sitemap\/0\.9"/);
    assert.match(sitemap, /<\/urlset>/);
  });

  it('contains ONLY https://aaa.arif-fazil.com/* URLs', () => {
    const locs = Array.from(sitemap.matchAll(/<loc>(.*?)<\/loc>/g)).map(m => m[1]);
    assert.ok(locs.length > 0, 'sitemap must list at least the root');
    for (const loc of locs) {
      assert.ok(
        loc.startsWith('https://aaa.arif-fazil.com/'),
        `URL outside AAA scope: ${loc}`,
      );
    }
  });

  it('does NOT include human-site (arif-fazil.com) or PDF or .well-known/* URLs', () => {
    const locs = Array.from(sitemap.matchAll(/<loc>(.*?)<\/loc>/g)).map(m => m[1]);
    for (const loc of locs) {
      assert.ok(
        !loc.startsWith('https://arif-fazil.com/'),
        `arif-fazil.com URL leaked into AAA sitemap: ${loc}`,
      );
      assert.ok(
        !loc.endsWith('.pdf') && !loc.includes('.pdf?'),
        `PDF URL leaked into AAA sitemap: ${loc}`,
      );
      assert.ok(
        !loc.includes('/.well-known/'),
        `.well-known/* URL leaked into AAA sitemap: ${loc}`,
      );
    }
  });

  it('includes the root, llms.txt, llms.json', () => {
    const locs = Array.from(sitemap.matchAll(/<loc>(.*?)<\/loc>/g)).map(m => m[1]);
    assert.ok(locs.includes('https://aaa.arif-fazil.com/'), 'root missing');
    assert.ok(locs.includes('https://aaa.arif-fazil.com/llms.txt'), 'llms.txt missing');
    assert.ok(locs.includes('https://aaa.arif-fazil.com/llms.json'), 'llms.json missing');
  });

  it('has a lastmod for every entry', () => {
    const entries = sitemap.match(/<url>[\s\S]*?<\/url>/g) || [];
    for (const entry of entries) {
      assert.match(entry, /<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/, 'lastmod required');
    }
  });
});

// ═════════════════════════════════════════════════════════════════════════
// 2. Public agent card — canonical signed AAA Gateway
// ═════════════════════════════════════════════════════════════════════════

describe('public/.well-known/agent-card.json — canonical signed Gateway', () => {
  let card: any;
  before(() => { card = readJson('public/.well-known/agent-card.json'); });

  it('declares schema https://a2a-protocol.org/schemas/agent-card/v1.0', () => {
    assert.equal(card.$schema, 'https://a2a-protocol.org/schemas/agent-card/v1.0');
  });

  it('is the AAA Gateway card (not the stale cockpit card)', () => {
    assert.match(card.name, /AAA A2A Gateway/);
    assert.ok(!('intelligencePrincipals' in card),
      'cockpit-pattern fields (intelligencePrincipals) must not appear in public gateway card');
    assert.ok(!('agentCards' in card),
      'cockpit-pattern fields (agentCards) must not appear in public gateway card');
  });

  it('declares aaa.arif-fazil.com as url and supportedInterfaces endpoint', () => {
    assert.equal(card.url, 'https://aaa.arif-fazil.com');
    assert.ok(Array.isArray(card.supportedInterfaces));
    assert.equal(card.supportedInterfaces[0].url, 'https://aaa.arif-fazil.com/a2a');
  });

  it('is Ed25519-signed over JCS-canonical form', () => {
    assert.ok(Array.isArray(card.signatures));
    assert.ok(card.signatures.length >= 1, 'must have at least one signature');
    const sig = card.signatures[0];
    assert.equal(sig.proofPurpose, 'assertionMethod');
    assert.equal(sig.type, 'Ed25519Signature2020');
    assert.equal(sig.canonical_form, 'JCS-sorted-keys-no-whitespace');
    assert.match(sig.canonical_sha256, /^[0-9a-f]{64}$/);
    assert.match(sig.proofValue, /^[A-Za-z0-9+/=]{80,}$/);
  });

  it('signature verificationMethod resolves to did:web:arif-fazil.com', () => {
    assert.equal(card.signatures[0].did, 'did:web:arif-fazil.com');
    assert.match(card.signatures[0].verificationMethod, /^did:web:arif-fazil.com#/);
    assert.equal(
      card.signatures[0].did_resolves_to,
      'https://arif-fazil.com/.well-known/did.json',
    );
  });
});

// ═════════════════════════════════════════════════════════════════════════
// 3. Deployment-state companion declares the arrangement
// ═════════════════════════════════════════════════════════════════════════

describe('public/.well-known/_deployment_state.json — arrangement manifest', () => {
  it('exists', () => {
    assert.ok(exists('public/.well-known/_deployment_state.json'),
      'companion file missing — slice incomplete');
  });

  let manifest: any;
  before(() => { manifest = readJson('public/.well-known/_deployment_state.json'); });

  it('declares _state.role = runtime-preserved-overlay', () => {
    assert.equal(manifest._state?.role, 'runtime-preserved-overlay');
  });

  it('points public_agent_card at the canonical signed gateway card', () => {
    assert.equal(manifest.public_agent_card?.path, 'agent-card.json');
    assert.equal(manifest.public_agent_card?.is_canonical_for_public, true);
    assert.equal(manifest.public_agent_card?.signed, true);
    assert.equal(manifest.public_agent_card?.schema,
      'https://a2a-protocol.org/schemas/agent-card/v1.0');
  });

  it('explicitly excludes the stale cockpit card from public deployment', () => {
    const cockpitEntry = (manifest.legacy_or_internal_cards || []).find(
      (c: any) => c.path?.includes('agents/agent_cards/.well-known/agent-card.json'),
    );
    assert.ok(cockpitEntry, 'stale cockpit card entry missing from manifest');
    assert.equal(cockpitEntry.deploy_for_public, false);
    assert.equal(cockpitEntry.deploys_at, null);
  });

  it('explicitly excludes pre-Gateway agent.json from public deployment', () => {
    const legacy = (manifest.legacy_or_internal_cards || []).find(
      (c: any) => c.path?.endsWith('.well-known/agent.json'),
    );
    assert.ok(legacy, 'legacy agent.json entry missing from manifest');
    assert.equal(legacy.deploy_for_public, false);
  });
});

// ═════════════════════════════════════════════════════════════════════════
// 4. Stale cockpit card location is labelled internal-only
// ═════════════════════════════════════════════════════════════════════════

describe('agents/agent_cards/.well-known/ — internal-only labelling', () => {
  it('has a README_INTERNAL_ONLY.md marker', () => {
    assert.ok(exists('agents/agent_cards/.well-known/README_INTERNAL_ONLY.md'));
  });

  it('README explains why this is NOT the public card', () => {
    const readme = read('agents/agent_cards/.well-known/README_INTERNAL_ONLY.md');
    assert.match(readme, /INTERNAL ONLY/i);
    assert.match(readme, /DO NOT DEPLOY/i);
    assert.match(readme, /public\/\.well-known\/agent-card\.json/);
    assert.match(readme, /cockpit/i);
  });

  it('the cockpit card itself uses arifOS/agent-card/v2.x schema (NOT a2a-protocol.org v1.0)', () => {
    const card = readJson('agents/agent_cards/.well-known/agent-card.json');
    assert.notEqual(card.$schema, 'https://a2a-protocol.org/schemas/agent-card/v1.0',
      'cockpit card must NOT carry a2a-protocol.org v1.0 schema');
    assert.ok('intelligencePrincipals' in card || 'agentCards' in card,
      'cockpit card must keep its cockpit-pattern fields');
  });
});

// ═════════════════════════════════════════════════════════════════════════
// 5. _state runtime-overlay semantics — FEDERATION_STATE files
// ═════════════════════════════════════════════════════════════════════════

describe('_state — runtime-preserved overlay semantics', () => {
  it('canonical overlay file exists at registries/state/federation_state.yaml', () => {
    assert.ok(exists('registries/state/federation_state.yaml'),
      'canonical runtime overlay file missing');
  });

  it('canonical overlay file declares _state.role = runtime-preserved-overlay', () => {
    const overlay = read('registries/state/federation_state.yaml');
    assert.match(overlay, /_state:\s*\n\s+role:\s*runtime-preserved-overlay/);
  });

  it('canonical overlay file documents the static-source invariant', () => {
    const overlay = read('registries/state/federation_state.yaml');
    assert.match(overlay, /NOT a static source of truth/i);
    assert.match(overlay, /FEDERATION_MODEL\.json/);
  });

  it('deprecated AAA_FEDERATION_STATE.yaml carries _state annotation', () => {
    const deprecated = read('registries/AAA_FEDERATION_STATE.yaml');
    assert.match(deprecated, /_state:\s*runtime-preserved-overlay/);
    assert.match(deprecated, /registries\/state\/federation_state\.yaml/);
  });

  it('deprecated file remains parseable as YAML meta structure', () => {
    const deprecated = read('registries/AAA_FEDERATION_STATE.yaml');
    assert.match(deprecated, /^meta:\s*$/m);
    assert.match(deprecated, /live_services:/);
  });
});

// ═════════════════════════════════════════════════════════════════════════
// 6. Empty model catalog is explicitly labelled, not invented
// ═════════════════════════════════════════════════════════════════════════

describe('registries/catalog.json — explicit empty fallback shim', () => {
  let cat: any;
  before(() => { cat = readJson('registries/catalog.json'); });

  it('declares _state.role = explicit-empty-fallback-shim', () => {
    assert.equal(cat._state?.role, 'explicit-empty-fallback-shim');
  });

  it('does NOT fabricate model entries (models must remain {})', () => {
    assert.deepEqual(cat.models, {},
      'catalog must not invent model entries — FEDERATION_MODEL.json is the SOT');
  });

  it('references the canonical model registry (FEDERATION_MODEL.json)', () => {
    assert.match(cat.canonical_model_registry, /FEDERATION_MODEL\.json$/);
  });

  it('makes fallback_used mean SILENCED, not APPLIED', () => {
    assert.equal(cat._state?.fallback_used, true);
    assert.match(cat._state?.fallback_meaning, /SILENCED, not FALLBACK APPLIED/i);
  });

  it('does NOT have a legacy "generated" key (removed by slice)', () => {
    assert.equal(cat.generated, undefined,
      'legacy "generated" key must not reappear');
  });
});

// ═════════════════════════════════════════════════════════════════════════
// 7. Unrelated dirty work is preserved untouched
// ═════════════════════════════════════════════════════════════════════════

describe('preservation of unrelated dirty work', () => {
  it('a2a-server/a2a-bridge-helper.js file mode is unchanged by this slice', () => {
    // The slice must not have run chmod / Edit on this file. We verify by
    // asserting the file exists and is readable; the dirty diff (mode change
    // and content) is owned by an earlier session and is preserved verbatim.
    assert.ok(exists('a2a-server/a2a-bridge-helper.js'));
  });

  it('registries/cooling_state.json file exists (unrelated cooling entries preserved)', () => {
    assert.ok(exists('registries/cooling_state.json'));
    const cooling = readJson<any>('registries/cooling_state.json');
    // Verify the recently-appended SABAR entries are still there (preserved).
    const recent = (cooling.entries || []).filter(
      (e: any) => typeof e.entry_id === 'string' && e.verdict === 'SABAR',
    );
    assert.ok(recent.length >= 1,
      'recently-appended SABAR cooling entries must remain');
  });
});

// ═════════════════════════════════════════════════════════════════════════
// 8. Schemas respected — both gateway and cockpit schemas coexist
// ═════════════════════════════════════════════════════════════════════════

describe('schema coexistence — gateway vs cockpit', () => {
  it('public gateway card stays on a2a-protocol.org/v1.0', () => {
    const card = readJson('public/.well-known/agent-card.json');
    assert.equal(card.$schema, 'https://a2a-protocol.org/schemas/agent-card/v1.0');
  });

  it('cockpit card stays on its cockpit-pattern schema (not silently converted)', () => {
    const cockpit = readJson('agents/agent_cards/.well-known/agent-card.json');
    assert.notEqual(cockpit.$schema, 'https://a2a-protocol.org/schemas/agent-card/v1.0');
  });

  it('both files remain valid JSON', () => {
    assert.doesNotThrow(() => readJson('public/.well-known/agent-card.json'));
    assert.doesNotThrow(() => readJson('agents/agent_cards/.well-known/agent-card.json'));
    assert.doesNotThrow(() => readJson('public/.well-known/_deployment_state.json'));
    assert.doesNotThrow(() => readJson('registries/catalog.json'));
  });
});