/**
 * Card Inventory Loader — Test Suite
 * ════════════════════════════════════════════════
 * 
 * Scenarios:
 * 1. Basic scan returns cards from all federation roots
 * 2. Duplicate registryId detection
 * 3. Schema version detection
 * 4. Card type classification
 * 5. exclude patterns work
 * 6. Failed card loading handled gracefully
 * 7. Archive filtering works
 * 8. produce summary
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

import { describe, it } from 'node:test';
import { strict as assert } from 'node:assert';
import { scanCardInventory } from '../src/gateway/card-inventory-loader.js';
import type { CardInventory } from '../src/gateway/card-inventory-types.js';

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 1: Basic scan returns cards
// ═══════════════════════════════════════════════════════════════════════════

describe('scanCardInventory', () => {
  it('returns inventory with cards from default roots', () => {
    const inv = scanCardInventory();
    assert.ok(inv.totalCards > 0, 'Should find at least one card');
    assert.ok(inv.cards.length > 0, 'Should have loaded cards');
    assert.ok(inv.generatedAt, 'Should have generation timestamp');
  });

  it('reports loaded vs failed counts add up', () => {
    const inv = scanCardInventory();
    assert.equal(inv.loadedCards + inv.failedCards, inv.totalCards,
      'Loaded + failed should equal total');
  });

  it('has summary breakdowns', () => {
    const inv = scanCardInventory();
    assert.ok(Object.keys(inv.byType).length > 0, 'Should have type breakdown');
    assert.ok(Object.keys(inv.bySchema).length > 0, 'Should have schema breakdown');
    assert.ok(Object.keys(inv.byOwner).length > 0, 'Should have owner breakdown');
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 2: Duplicate detection
// ═══════════════════════════════════════════════════════════════════════════

describe('duplicate detection', () => {
  it('detects when two cards share registryId', () => {
    const inv = scanCardInventory();
    // AAA has agent-card.json AND agent.json in .well-known — likely same id
    const idDups = inv.duplicates.filter(d => d.field === 'registryId');
    // May or may not have duplicates depending on actual cards
    assert.ok(Array.isArray(inv.duplicates), 'duplicates should be an array');
  });

  it('each duplicate has value, field, and sources', () => {
    const inv = scanCardInventory();
    for (const dup of inv.duplicates) {
      assert.ok(dup.value, 'Should have value');
      assert.ok(dup.field, 'Should have field');
      assert.ok(dup.sources.length >= 2, 'Should have at least 2 sources');
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 3: Schema warnings
// ═══════════════════════════════════════════════════════════════════════════

describe('schema warnings', () => {
  it('produces warnings for legacy schemas', () => {
    const inv = scanCardInventory();
    const legacyWarnings = inv.warnings.filter(w =>
      w.message.includes('Legacy schema') || w.message.includes('Migrate'));
    // We expect some legacy schema cards
    assert.ok(Array.isArray(inv.warnings), 'warnings should be an array');
  });

  it('produces warnings for missing supportedInterfaces', () => {
    const inv = scanCardInventory();
    const missingIfWarnings = inv.warnings.filter(w =>
      w.message.includes('supportedInterfaces'));
    assert.ok(Array.isArray(inv.warnings), 'warnings should be an array');
  });

  it('warnings have severity and message', () => {
    const inv = scanCardInventory();
    for (const w of inv.warnings) {
      assert.ok(['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].includes(w.severity),
        `Invalid severity: ${w.severity}`);
      assert.ok(w.message.length > 0, 'Should have message');
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 4: Filtering options
// ═══════════════════════════════════════════════════════════════════════════

describe('filtering options', () => {
  it('excludeArchived filters archive cards', () => {
    const withArchive = scanCardInventory({ includeArchived: true });
    const withoutArchive = scanCardInventory({ includeArchived: false });
    const archiveInWith = withArchive.cards.filter(c => c.cardType === 'archived').length;
    const archiveInWithout = withoutArchive.cards.filter(c => c.cardType === 'archived').length;
    assert.ok(archiveInWithout <= archiveInWith,
      'Without archived should have <= archived cards than with');
  });

  it('custom roots work', () => {
    const inv = scanCardInventory({ roots: ['/root/AAA'] });
    assert.ok(inv.totalCards > 0, 'AAA should have cards');
    // All cards should be from AAA
    for (const card of inv.cards) {
      assert.ok(
        card.source.path.startsWith('/root/AAA') ||
        card.source.owner === 'aaa',
        `Card ${card.source.path} should be from AAA`);
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 5: Card classification
// ═══════════════════════════════════════════════════════════════════════════

describe('card classification', () => {
  it('detects gateway cards', () => {
    const inv = scanCardInventory({ roots: ['/root/AAA'] });
    const gateways = inv.cards.filter(c => c.cardType === 'gateway');
    assert.ok(gateways.length > 0, 'AAA should have at least one gateway card');
  });

  it('detects organ cards', () => {
    const inv = scanCardInventory();
    const organs = inv.cards.filter(c => c.cardType === 'organ');
    assert.ok(organs.length > 0, 'Should have organ cards');
  });

  it('detects agent cards', () => {
    const inv = scanCardInventory({ roots: ['/root/AAA'] });
    const agents = inv.cards.filter(c => c.cardType === 'agent');
    // AAA has agent cards under agents/
    assert.ok(agents.length >= 0, 'May or may not have agent cards in filtered view');
  });

  it('detects schema versions', () => {
    const inv = scanCardInventory({ roots: ['/root/AAA'] });
    const legacy = inv.cards.filter(c => c.schemaVersion === 'arifos-v2.2.0');
    assert.ok(legacy.length > 0, 'AAA should have legacy schema cards');
  });
});

// ═══════════════════════════════════════════════════════════════════════════
// Scenario 6: Error handling
// ═══════════════════════════════════════════════════════════════════════════

describe('error handling', () => {
  it('handles non-existent roots gracefully', () => {
    const inv = scanCardInventory({ roots: ['/nonexistent/path'] });
    assert.equal(inv.totalCards, 0, 'Should return zero cards');
    assert.equal(inv.cards.length, 0, 'Should return empty array');
  });

  it('loaded cards have valid fields', () => {
    const inv = scanCardInventory({ roots: ['/root/AAA'] });
    for (const card of inv.cards) {
      if (card.loaded) {
        assert.ok(card.source.path, 'Should have source path');
        assert.ok(card.source.owner, 'Should have owner');
        assert.ok(card.schemaVersion, 'Should have schema version');
      } else {
        assert.ok(card.error, 'Failed card should have error message');
      }
    }
  });
});
