/**
 * A2A 1.0 Agent Card Migration
 * ═══════════════════════════════════════════════
 * 
 * Reads legacy arifOS/agent-card/v2.2.0 cards and produces
 * A2A 1.0 compliant Agent Cards.
 * 
 * Preserves: identity, capabilities, extensions, registry metadata.
 * Adds: supportedInterfaces, skills, securitySchemes, defaultModes.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';

// ── A2A 1.0 Types ─────────────────────────────────────────────────────────

interface AgentSkill {
  id: string;
  name: string;
  description: string;
  tags?: string[];
  examples?: string[];
  inputModes?: string[];
  outputModes?: string[];
}

interface AgentInterface {
  url: string;
  protocolBinding: 'JSONRPC' | 'HTTP+JSON' | 'gRPC' | 'Custom';
  protocolVersion: string;
}

interface AgentCapabilities {
  streaming?: boolean;
  pushNotifications?: boolean;
  stateTransitionHistory?: boolean;
  extensions?: AgentExtension[];
}

interface AgentExtension {
  uri: string;
  description?: string;
  required: boolean;
  params?: Record<string, unknown>;
}

interface SecurityScheme {
  type: 'apiKey' | 'http' | 'oauth2' | 'openIdConnect' | 'mutualTls';
  description?: string;
  // Discriminated fields per type
  [key: string]: unknown;
}

interface SecurityRequirement {
  [scheme: string]: string[];
}

interface AgentCard {
  name: string;
  description: string;
  url: string;
  version: string;
  supportedInterfaces: AgentInterface[];
  capabilities: AgentCapabilities;
  skills: AgentSkill[];
  defaultInputModes: string[];
  defaultOutputModes: string[];
  securitySchemes?: Record<string, SecurityScheme>;
  securityRequirements?: SecurityRequirement[];
  signature?: {
    algorithm: string;
    value: string;
    keyId?: string;
  };
}

// ── Legacy Types ──────────────────────────────────────────────────────────

interface LegacyCard {
  $schema?: string;
  schemaVersion?: string;
  id?: string;
  name?: string;
  description?: string;
  url?: string;
  version?: string;
  protocolVersion?: string;
  preferred_transport?: string;
  provider?: Record<string, unknown>;
  capabilities?: Record<string, unknown>;
  extensions?: Array<Record<string, unknown>>;
  security?: unknown[];
  federation_organs?: Record<string, unknown>;
  governance?: Record<string, unknown>;
  constitution?: Record<string, unknown>;
  floor_scope?: string[];
  mcp_native?: boolean;
  tool_calling?: boolean;
  gateway?: Record<string, unknown>;
}

// ── Migrator ──────────────────────────────────────────────────────────────

export function migrateCard(legacy: LegacyCard): AgentCard {
  const name = legacy.name ?? legacy.id ?? 'unknown';
  const url = legacy.url ?? 'https://arif-fazil.com';
  const version = legacy.version ?? '1.0.0';

  // ── supportedInterfaces ──────────────────────────────────────────────
  const interfaces: AgentInterface[] = [{
    url: `${url}/a2a`,
    protocolBinding: 'JSONRPC',
    protocolVersion: '1.0',
  }];

  // ── capabilities ─────────────────────────────────────────────────────
  const caps = legacy.capabilities ?? {};
  const capabilities: AgentCapabilities = {
    streaming: caps['streaming'] === true,
    pushNotifications: caps['pushNotifications'] === true,
    stateTransitionHistory: false,
    extensions: [],
  };

  // ── extensions (A2A format) ──────────────────────────────────────────
  const extObjects: AgentExtension[] = [];

  // Preserve existing extensions as AgentExtension objects
  const legacyExts = legacy.extensions ?? [];
  for (const ext of legacyExts) {
    const uri = (ext['uri'] as string) ?? '';
    if (!uri) continue;
    extObjects.push({
      uri,
      description: (ext['description'] as string) ?? undefined,
      required: (ext['required'] as boolean) ?? false,
      params: (ext['params'] as Record<string, unknown>) ?? undefined,
    });
  }

  // ArifOS governed identity extension
  extObjects.push({
    uri: 'https://arif-fazil.com/a2a/extensions/governed-identity/v1',
    description: 'arifOS federation governed identity — organ, registry, constitutional floors',
    required: false,
    params: {
      registryId: legacy.id ?? name.toLowerCase().replace(/\s+/g, '-'),
      organId: (legacy.provider?.['system'] as string)?.toLowerCase() ?? 'unknown',
      federationOrgans: legacy.federation_organs ?? {},
      floorScope: legacy.floor_scope ?? [],
      constitutionHash: legacy.constitution?.['hash'] ?? 'unknown',
    },
  });

  capabilities.extensions = extObjects;

  // ── skills ───────────────────────────────────────────────────────────
  const skills: AgentSkill[] = [];

  // Convert actions to skill declarations
  const actions = caps['actions'] as Record<string, unknown> | undefined;
  const supported = actions?.['supported'] as Array<Record<string, unknown>> | undefined;
  if (supported) {
    for (const action of supported) {
      skills.push({
        id: (action['name'] as string) ?? 'unknown',
        name: (action['name'] as string) ?? 'unknown',
        description: (action['description'] as string) ?? '',
        tags: ['canonical', 'kernel'],
        inputModes: ['text'],
        outputModes: ['text'],
      });
    }
  }

  // ── default modes ────────────────────────────────────────────────────
  const defaultInputModes = ['text', 'text/plain'];
  const defaultOutputModes = ['text', 'text/plain'];

  // ── security ─────────────────────────────────────────────────────────
  // A2A v1: securitySchemes = object map, securityRequirements = array
  const securitySchemes: Record<string, SecurityScheme> = {};
  const securityRequirements: SecurityRequirement[] = [];
  if (legacy.security) {
    securitySchemes['federation'] = {
      type: 'http',
      scheme: 'bearer',
      bearerFormat: 'token',
      description: 'Federation security scheme (inherited from legacy card)',
    };
    securityRequirements.push({ federation: [] });
  }

  return {
    name,
    description: legacy.description ?? `Agent card for ${name}`,
    url,
    version,
    supportedInterfaces: interfaces,
    capabilities,
    skills,
    defaultInputModes,
    defaultOutputModes,
    securitySchemes: Object.keys(securitySchemes).length > 0 ? securitySchemes : undefined,
    securityRequirements: securityRequirements.length > 0 ? securityRequirements : undefined,
    signature: {
      algorithm: 'sha256',
      value: 'UNMEASURED',
      keyId: 'pending-migration',
    },
  };
}

// ── Batch Migration ──────────────────────────────────────────────────────

export interface MigrationResult {
  source: string;
  target: string;
  card: AgentCard;
  success: boolean;
  error?: string;
}

export function migrateAllCards(
  cardPaths: string[],
  outputDir: string,
): MigrationResult[] {
  const results: MigrationResult[] = [];

  for (const cardPath of cardPaths) {
    try {
      const content = fs.readFileSync(cardPath, 'utf-8');
      const legacy = JSON.parse(content) as LegacyCard;

      // Skip non-arifOS cards (already in another format)
      if (!legacy.$schema?.includes('arifOS')) {
        continue;
      }

      const card = migrateCard(legacy);
      const baseName = path.basename(cardPath, '.json');
      const outputPath = path.join(outputDir, `${baseName}-a2a-v1.json`);

      fs.mkdirSync(outputDir, { recursive: true });
      fs.writeFileSync(outputPath, JSON.stringify(card, null, 2), 'utf-8');

      results.push({
        source: cardPath,
        target: outputPath,
        card,
        success: true,
      });
    } catch (err) {
      results.push({
        source: cardPath,
        target: '',
        card: null as unknown as AgentCard,
        success: false,
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }

  return results;
}
