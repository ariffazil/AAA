/**
 * model_resolver.ts — Canonical model resolver for AAA federation (TypeScript).
 * Reads strictly from /root/.config/federation-models.json.
 * Zero hardcoded model strings. Drift impossible by construction.
 *
 * Usage:
 *   import { resolveAgentModel, resolveTierModel, listAgents } from './model_resolver';
 *
 *   const cfg = resolveAgentModel('opencode');
 *   // → { agentId: 'opencode', provider: 'deepseek', model: 'deepseek/deepseek-v4-pro', ... }
 *
 *   const model = resolveTierModel('heavy');
 *   // → 'deepseek/deepseek-v4-pro'
 *
 * Forged: 2026-07-24 by FORGE (000Ω). DITEMPA BUKAN DIBERI.
 */

import * as fs from 'fs';
import * as path from 'path';

const CANONICAL_PATH = '/root/.config/federation-models.json';

interface AgentConfig {
  name: string;
  class: string;
  organ: string;
  primary_model: string;
  primary_provider: string;
  fallback_chain: string[];
  timeout_ms: number;
  cost_budget_daily_usd: number;
  config_file: string;
  status: string;
}

interface ProviderConfig {
  name: string;
  jurisdiction: string;
  endpoint: string;
  api_key_ref: string;
  billing: string;
  balance_usd: number | null;
  status: string;
}

interface TierConfig {
  use: string;
  model: string;
  cost: string;
}

interface FederationRegistry {
  _meta: Record<string, unknown>;
  providers: Record<string, ProviderConfig>;
  agents: Record<string, AgentConfig>;
  routing: Record<string, unknown>;
  tiers: Record<string, TierConfig>;
}

interface ResolvedAgentModel {
  agentId: string;
  agentName: string;
  provider: string;
  providerName: string;
  model: string;
  fallbackChain: string[];
  timeoutMs: number;
  costBudgetDailyUsd: number;
  apiKeyRef: string;
  endpoint: string;
  status: string;
}

interface AgentSummary {
  agentId: string;
  name: string;
  model: string;
  provider: string;
  status: string;
}

interface ProviderSummary {
  providerId: string;
  name: string;
  status: string;
  balanceUsd: number | null;
  jurisdiction: string;
  billing: string;
}

let _registryCache: FederationRegistry | null = null;
let _registryLoadTime = 0;
const CACHE_TTL_MS = 60_000; // 1 minute

function loadRegistry(): FederationRegistry {
  const now = Date.now();
  if (_registryCache && now - _registryLoadTime < CACHE_TTL_MS) {
    return _registryCache;
  }

  if (!fs.existsSync(CANONICAL_PATH)) {
    throw new Error(
      `Canonical model registry not found at ${CANONICAL_PATH}. Run: forge --option-a to create it.`
    );
  }

  const raw = fs.readFileSync(CANONICAL_PATH, 'utf-8');
  _registryCache = JSON.parse(raw) as FederationRegistry;
  _registryLoadTime = now;
  return _registryCache;
}

/** Force reload of registry cache. */
export function reloadRegistry(): void {
  _registryCache = null;
}

export function resolveAgentModel(agentId: string): ResolvedAgentModel {
  const registry = loadRegistry();
  const agents = registry.agents;

  if (!(agentId in agents)) {
    throw new Error(
      `Agent '${agentId}' not found in canonical registry. Available: ${Object.keys(agents).join(', ')}`
    );
  }

  const cfg = agents[agentId];
  const providerId = cfg.primary_provider || 'unknown';
  const providers = registry.providers;
  const providerCfg = providers[providerId] || ({} as ProviderConfig);

  return {
    agentId,
    agentName: cfg.name || agentId,
    provider: providerId,
    providerName: providerCfg.name || providerId,
    model: cfg.primary_model,
    fallbackChain: cfg.fallback_chain || [],
    timeoutMs: cfg.timeout_ms || 30000,
    costBudgetDailyUsd: cfg.cost_budget_daily_usd || 0,
    apiKeyRef: providerCfg.api_key_ref || '',
    endpoint: providerCfg.endpoint || '',
    status: cfg.status || 'UNKNOWN',
  };
}

export function resolveTierModel(tier: string): string {
  const registry = loadRegistry();
  const tiers = registry.tiers;

  if (!(tier in tiers)) {
    throw new Error(`Tier '${tier}' not found. Available: ${Object.keys(tiers).join(', ')}`);
  }

  return tiers[tier].model;
}

export function resolveFallback(agentId: string, failedModel: string): string | null {
  const cfg = resolveAgentModel(agentId);
  const chain = cfg.fallbackChain;

  for (let i = 0; i < chain.length; i++) {
    if (chain[i] === failedModel || chain[i].includes(failedModel)) {
      return i + 1 < chain.length ? chain[i + 1] : null;
    }
  }

  return chain.length > 0 ? chain[0] : null;
}

export function listAgents(statusFilter?: string): AgentSummary[] {
  const registry = loadRegistry();
  const result: AgentSummary[] = [];

  for (const [aid, cfg] of Object.entries(registry.agents)) {
    if (statusFilter && cfg.status !== statusFilter) continue;
    result.push({
      agentId: aid,
      name: cfg.name || aid,
      model: cfg.primary_model,
      provider: cfg.primary_provider || 'unknown',
      status: cfg.status || 'UNKNOWN',
    });
  }

  return result.sort((a, b) => a.agentId.localeCompare(b.agentId));
}

export function listProviders(): ProviderSummary[] {
  const registry = loadRegistry();
  const result: ProviderSummary[] = [];

  for (const [pid, cfg] of Object.entries(registry.providers)) {
    result.push({
      providerId: pid,
      name: cfg.name || pid,
      status: cfg.status || 'UNKNOWN',
      balanceUsd: cfg.balance_usd ?? null,
      jurisdiction: cfg.jurisdiction || 'unknown',
      billing: cfg.billing || 'unknown',
    });
  }

  return result.sort((a, b) => a.providerId.localeCompare(b.providerId));
}
