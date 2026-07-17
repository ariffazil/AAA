/**
 * Card Inventory Loader
 * ═══════════════════════════════════════════════
 * 
 * Scans all agent card locations across the federation.
 * Detects duplicates, version conflicts, legacy schemas, shadow cards.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import {
  type CardInventory,
  type CardScanConfig,
  type CardSource,
  type CardDuplicate,
  type LoadedCard,
  type SchemaWarning,
  type CardType,
  type CardSchemaVersion,
} from './card-inventory-types.js';

// ── Default scan configuration ───────────────────────────────────────────

const DEFAULT_SCAN_ROOTS = [
  '/root/AAA',
  '/root/GEOX',
  '/root/A-FORGE',
  '/root/WEALTH',
  '/root/WELL',
  '/root/arifOS',
];

const DEFAULT_EXCLUDE = [
  'node_modules',
  '.git',
  'dist',
  '.venv',
  '__pycache__',
  '.backups',
  'archive',
  '_archive',
];

// ── Card file patterns ────────────────────────────────────────────────────

const CARD_FILENAMES = ['agent-card.json', 'agent.json'];

// ── Helpers ───────────────────────────────────────────────────────────────

function isoNow(): string {
  return new Date().toISOString();
}

function detectOwner(rootPath: string): CardSource['owner'] {
  const lower = rootPath.toLowerCase();
  if (lower.includes('/aaa')) return 'aaa';
  if (lower.includes('/geox')) return 'geox';
  if (lower.includes('/a-forge') || lower.includes('/a_forge')) return 'aforge';
  if (lower.includes('/wealth')) return 'wealth';
  if (lower.includes('/well')) return 'well';
  if (lower.includes('/hermes')) return 'hermes';
  if (lower.includes('/archive') || lower.includes('/backup')) return 'archive';
  return 'unknown';
}

function detectSchemaVersion(raw: Record<string, unknown>): CardSchemaVersion {
  const schema = raw['$schema'] as string | undefined;
  const schema2 = raw['schema'] as string | undefined;
  const s = (schema ?? schema2 ?? '').toLowerCase();

  if (s.includes('a2a') && (s.includes('1.0') || s.includes('v1'))) return 'a2a-1.0';
  if (s.includes('a2a') && s.includes('0.3')) return 'a2a-0.3';
  if (s.includes('arifos') && s.includes('v2')) return 'arifos-v2.2.0';
  if (s.includes('arifos') && s.includes('v1')) return 'arifos-v1';

  // Heuristic: has supportedInterfaces → likely A2A 1.0
  if (raw['supportedInterfaces']) return 'a2a-1.0';
  // Heuristic: has capabilities.actions → legacy arifOS
  const caps = raw['capabilities'] as Record<string, unknown> | undefined;
  if (caps?.['actions']) return 'arifos-v2.2.0';

  return 'unknown';
}

function detectCardType(source: CardSource, raw: Record<string, unknown>): CardType {
  const fullPath = source.path.toLowerCase();
  const relPath = source.relativePath.toLowerCase();

  if (source.owner === 'archive') return 'archived';
  if (fullPath.includes('/agents/') || fullPath.includes('/agent-cards/')) return 'agent';
  if (fullPath.includes('/skills/')) return 'skill';
  if (fullPath.includes('/lanes/') || fullPath.includes('/_lanes/')) return 'lane';
  if (fullPath.includes('/_retired/') || fullPath.includes('/archive/')) return 'archived';
  if (source.wellKnown && source.owner === 'aaa') return 'gateway';
  if (source.wellKnown && (source.owner === 'geox' || source.owner === 'aforge' ||
      source.owner === 'wealth' || source.owner === 'well' || source.owner === 'hermes')) return 'organ';

  // Root-level agent-card.json in AAA is the gateway card
  if (source.owner === 'aaa' && (relPath === 'agent-card.json' || relPath === 'agent.json')) return 'gateway';

  if (source.owner === 'geox' || source.owner === 'aforge' ||
      source.owner === 'wealth' || source.owner === 'well') return 'organ';

  return 'unknown';
}

// ── Card discovery ────────────────────────────────────────────────────────

function findCardFiles(root: string, exclude: string[]): string[] {
  const results: string[] = [];

  function walk(dir: string, depth: number) {
    if (depth > 6) return; // Max depth guard

    let entries: fs.Dirent[];
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return; // Permission denied, symlink broken, etc.
    }

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const baseName = entry.name.toLowerCase();

      // Skip excluded and hidden directories (except .well-known)
      if (entry.isDirectory()) {
        if (exclude.some(e => baseName === e.toLowerCase())) continue;
        if (baseName.startsWith('.') && baseName !== '.well-known') continue;
        walk(fullPath, depth + 1);
        continue;
      }

      // Match card filenames
      if (CARD_FILENAMES.some(f => baseName === f.toLowerCase())) {
        results.push(fullPath);
      }
    }
  }

  walk(root, 0);
  return results;
}

// ── Card loading ──────────────────────────────────────────────────────────

function loadCard(filePath: string, roots: string[]): LoadedCard {
  // Determine owner from the matching root
  let owner: CardSource['owner'] = 'unknown';
  let relativePath = filePath;
  for (const root of roots) {
    if (filePath.startsWith(root)) {
      owner = detectOwner(root);
      relativePath = filePath.slice(root.length).replace(/^\//, '');
      break;
    }
  }

  const source: CardSource = {
    path: filePath,
    relativePath,
    owner,
    wellKnown: filePath.includes('/.well-known/'),
  };

  const result: LoadedCard = {
    source,
    raw: {},
    schemaVersion: 'unknown',
    cardType: 'unknown',
    registryId: null,
    name: null,
    url: null,
    version: null,
    hasSupportedInterfaces: false,
    hasCapabilities: false,
    hasSecurity: false,
    loaded: false,
  };

  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const raw = JSON.parse(content) as Record<string, unknown>;

    result.raw = raw;
    result.schemaVersion = detectSchemaVersion(raw);
    result.cardType = detectCardType(source, raw);
    result.registryId = (raw['id'] as string) ?? (raw['agentId'] as string) ?? null;
    result.name = (raw['name'] as string) ?? null;
    result.url = (raw['url'] as string) ?? null;
    result.version = (raw['version'] as string) ?? null;
    result.hasSupportedInterfaces = Array.isArray(raw['supportedInterfaces']) && (raw['supportedInterfaces'] as unknown[]).length > 0;
    result.hasCapabilities = typeof raw['capabilities'] === 'object' && raw['capabilities'] !== null;
    result.hasSecurity = !!(raw['security'] || raw['securityRequirements']);
    result.loaded = true;
  } catch (err) {
    result.error = err instanceof Error ? err.message : String(err);
  }

  return result;
}

// ── Duplicate detection ──────────────────────────────────────────────────

function detectDuplicates(cards: LoadedCard[]): CardDuplicate[] {
  const duplicates: CardDuplicate[] = [];

  // Check registryId duplicates
  const byId = new Map<string, CardSource[]>();
  for (const card of cards) {
    if (!card.registryId) continue;
    const sources = byId.get(card.registryId) ?? [];
    sources.push(card.source);
    byId.set(card.registryId, sources);
  }
  for (const [id, sources] of byId) {
    if (sources.length > 1) {
      duplicates.push({
        value: id,
        field: 'registryId',
        sources,
      });
    }
  }

  // Check name duplicates (only for organ/gateway cards)
  const byName = new Map<string, CardSource[]>();
  for (const card of cards) {
    if (!card.name || card.cardType === 'skill') continue;
    const sources = byName.get(card.name) ?? [];
    sources.push(card.source);
    byName.set(card.name, sources);
  }
  for (const [name, sources] of byName) {
    if (sources.length > 1) {
      duplicates.push({
        value: name,
        field: 'name',
        sources,
      });
    }
  }

  return duplicates;
}

// ── Schema compliance check ──────────────────────────────────────────────

function checkSchemaCompliance(cards: LoadedCard[]): SchemaWarning[] {
  const warnings: SchemaWarning[] = [];

  for (const card of cards) {
    if (!card.loaded) {
      warnings.push({
        card: card.source,
        severity: 'HIGH',
        message: `Failed to load card: ${card.error ?? 'unknown error'}`,
      });
      continue;
    }

    // Legacy schema usage
    if (card.schemaVersion === 'arifos-v2.2.0' || card.schemaVersion === 'arifos-v1') {
      warnings.push({
        card: card.source,
        severity: 'MEDIUM',
        message: `Legacy schema: ${card.schemaVersion}. Migrate to A2A 1.0.`,
      });
    }

    // Missing supportedInterfaces for organ/gateway cards
    if ((card.cardType === 'organ' || card.cardType === 'gateway') && !card.hasSupportedInterfaces) {
      warnings.push({
        card: card.source,
        severity: 'HIGH',
        message: 'Missing supportedInterfaces — required for A2A 1.0 conformance.',
      });
    }

    // Missing name
    if (!card.name && card.cardType !== 'skill') {
      warnings.push({
        card: card.source,
        severity: 'MEDIUM',
        message: 'Missing name field.',
      });
    }

    // Unknown schema
    if (card.schemaVersion === 'unknown') {
      warnings.push({
        card: card.source,
        severity: 'LOW',
        message: 'Cannot determine schema version.',
      });
    }
  }

  // Shadow cards: cards not in .well-known that aren't agents or skills
  const wellKnownOwners = new Set(
    cards.filter(c => c.source.wellKnown && c.cardType === 'organ')
      .map(c => c.source.owner)
  );
  for (const card of cards) {
    if (card.cardType === 'organ' && !card.source.wellKnown) {
      warnings.push({
        card: card.source,
        severity: 'LOW',
        message: `Organ card outside .well-known directory.`,
      });
    }
  }

  return warnings;
}

// ── Main: Full card inventory scan ────────────────────────────────────────

export interface InventoryOptions {
  /** Override scan roots */
  roots?: string[];
  /** Include archived cards */
  includeArchived?: boolean;
  /** Include skill-level cards */
  includeSkills?: boolean;
}

export function scanCardInventory(options: InventoryOptions = {}): CardInventory {
  const generatedAt = isoNow();
  const roots = options.roots ?? DEFAULT_SCAN_ROOTS;
  const exclude = DEFAULT_EXCLUDE;

  // Phase 1: Discover card files
  const allPaths = new Set<string>();
  for (const root of roots) {
    try {
      const stat = fs.statSync(root);
      if (!stat.isDirectory()) continue;
    } catch {
      continue; // Root doesn't exist
    }
    for (const cardPath of findCardFiles(root, exclude)) {
      allPaths.add(cardPath);
    }
  }

  // Phase 2: Load all cards
  const cards = [...allPaths].map(p => loadCard(p, roots));

  // Phase 3: Filter by type if needed
  const filteredCards = cards.filter(c => {
    if (c.source.owner === 'archive' && !options.includeArchived) return false;
    if (c.cardType === 'skill' && !options.includeSkills) return false;
    return true;
  });

  // Phase 4: Detect duplicates
  const duplicates = detectDuplicates(filteredCards);

  // Phase 5: Schema compliance
  const warnings = checkSchemaCompliance(filteredCards);

  // Phase 6: Summaries
  const byType: Record<string, number> = {};
  const bySchema: Record<string, number> = {};
  const byOwner: Record<string, number> = {};
  for (const card of filteredCards) {
    byType[card.cardType] = (byType[card.cardType] ?? 0) + 1;
    bySchema[card.schemaVersion] = (bySchema[card.schemaVersion] ?? 0) + 1;
    byOwner[card.source.owner] = (byOwner[card.source.owner] ?? 0) + 1;
  }

  const loadedCards = filteredCards.filter(c => c.loaded).length;

  return {
    generatedAt,
    totalCards: allPaths.size,
    loadedCards,
    failedCards: allPaths.size - loadedCards,
    cards: filteredCards,
    duplicates,
    warnings,
    byType: byType as Record<CardType, number>,
    bySchema: bySchema as Record<CardSchemaVersion, number>,
    byOwner,
  };
}
