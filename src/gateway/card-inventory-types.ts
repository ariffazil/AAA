/**
 * Card Inventory Loader — Schema Types
 * ═══════════════════════════════════════════════
 * 
 * Scans all agent card locations across the federation.
 * Detects duplicates, version conflicts, legacy schemas, shadow cards.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

// ── Card Schema Version ──────────────────────────────────────────────────

export type CardSchemaVersion = 
  | 'a2a-1.0'           // Current A2A 1.0 spec
  | 'a2a-0.3'           // A2A 0.3 (previous)
  | 'arifos-v2.2.0'     // Legacy arifOS agent-card schema
  | 'arifos-v1'         // Legacy arifOS v1
  | 'unknown';          // Cannot determine

// ── Card Type ────────────────────────────────────────────────────────────

export type CardType =
  | 'organ'              // Federation organ (GEOX, WEALTH, etc.)
  | 'gateway'            // AAA gateway card
  | 'agent'              // Named agent under AAA
  | 'skill'              // GEOX skill-level card
  | 'lane'               // Agent lane card
  | 'archived'           // In archive directory
  | 'legacy'             // Pre-A2A schema
  | 'unknown';           // Cannot determine

// ── Card Source ──────────────────────────────────────────────────────────

export interface CardSource {
  /** Absolute filesystem path */
  path: string;
  /** Relative path from repo root */
  relativePath: string;
  /** Organ or directory owner */
  owner: 'aaa' | 'geox' | 'aforge' | 'wealth' | 'well' | 'hermes' | 'archive' | 'unknown';
  /** Is this in a .well-known directory? */
  wellKnown: boolean;
}

// ── Loaded Card ──────────────────────────────────────────────────────────

export interface LoadedCard {
  /** Filesystem source */
  source: CardSource;
  /** Raw JSON content */
  raw: Record<string, unknown>;
  /** Detected schema version */
  schemaVersion: CardSchemaVersion;
  /** Detected card type */
  cardType: CardType;
  /** Internal registry ID (arifOS-specific, not A2A) */
  registryId: string | null;
  /** A2A name field */
  name: string | null;
  /** A2A url field */
  url: string | null;
  /** A2A version field */
  version: string | null;
  /** Has supportedInterfaces (A2A 1.0 required) */
  hasSupportedInterfaces: boolean;
  /** Has capabilities */
  hasCapabilities: boolean;
  /** Has security (legacy) or securityRequirements (A2A 1.0) */
  hasSecurity: boolean;
  /** Card loaded successfully */
  loaded: boolean;
  /** Parse error if load failed */
  error?: string;
}

// ── Duplicate Detection ──────────────────────────────────────────────────

export interface CardDuplicate {
  /** The duplicated value */
  value: string;
  /** What field was duplicated (registryId, name, url) */
  field: 'registryId' | 'name' | 'url';
  /** Sources where duplicate was found */
  sources: CardSource[];
}

// ── Schema Compliance ────────────────────────────────────────────────────

export interface SchemaWarning {
  card: CardSource;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  message: string;
  field?: string;
}

// ── Inventory Report ─────────────────────────────────────────────────────

export interface CardInventory {
  /** When this inventory was generated */
  generatedAt: string;
  /** Total cards found */
  totalCards: number;
  /** Cards successfully loaded */
  loadedCards: number;
  /** Cards that failed to load */
  failedCards: number;
  /** All loaded cards */
  cards: LoadedCard[];
  /** Duplicates detected */
  duplicates: CardDuplicate[];
  /** Schema compliance warnings */
  warnings: SchemaWarning[];
  /** Summary by type */
  byType: Record<CardType, number>;
  /** Summary by schema */
  bySchema: Record<CardSchemaVersion, number>;
  /** Summary by owner */
  byOwner: Record<string, number>;
}

// ── Scan Configuration ───────────────────────────────────────────────────

export interface CardScanConfig {
  /** Root directories to scan */
  roots: string[];
  /** Patterns to exclude */
  exclude: string[];
  /** Whether to include archived cards */
  includeArchived: boolean;
  /** Whether to include skill-level cards */
  includeSkills: boolean;
}
