/**
 * model_resolver.ts — Canonical model resolver for AAA federation (TypeScript).
 * Reads from AGENT_MODEL_MAP.json via symlink at /root/.config/federation-models.json.
 * Schema: providers[] + agents[] + models[] + fallback_chains[].
 *
 * Usage:
 *   import { resolve, validate, listAgents } from './model_resolver';
 *   const cfg = resolve('opencode');
 *   // → { agentId: 'opencode', model: 'deepseek/deepseek-v4-pro', ... }
 *
 * Forged: 2026-07-24 by FORGE (000Ω). DITEMPA BUKAN DIBERI.
 */

import * as fs from 'fs';

const CANONICAL = '/root/.config/federation-models.json';

// ── Types ──

interface ProviderRecord {
  provider_id: string;
  provider_name?: string;
  endpoint_url?: string;
  api_key_ref?: string;
  status?: string;
  balance_usd?: number | null;
  jurisdiction?: string;
  billing_model?: string;
  cloud_act_exposed?: boolean;
  note?: string;
}

interface FallbackEntry {
  model_key: string;
  priority: number;
  condition: string;
}

interface AgentRecord {
  agent_id: string;
  agent_name?: string;
  primary_model: string;
  primary_provider: string;
  fallback_chain: FallbackEntry[];
  timeout_ms?: number;
  cost_budget_daily_usd?: number;
  status?: string;
}

interface ModelRecord {
  model_key: string;
  provider_ref: string;
  status?: string;
}

interface FederationRegistry {
  providers: ProviderRecord[];
  agents: AgentRecord[];
  models: ModelRecord[];
  fallback_chains?: unknown[];
  routing_rules?: unknown[];
}

interface ResolvedAgent {
  agentId: string;
  agentName: string;
  model: string;
  provider: string;
  providerName: string;
  fallbacks: string[];
  endpoint: string;
  apiKeyRef: string;
  status: string;
  timeoutMs: number;
  costDailyUsd: number;
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
  providers: number;
  agents: number;
}

// ── Cache ──

let _cache: FederationRegistry | null = null;
let _cacheTime = 0;
const CACHE_TTL = 60_000;

function load(): FederationRegistry {
  const now = Date.now();
  if (_cache && now - _cacheTime < CACHE_TTL) return _cache;
  if (!fs.existsSync(CANONICAL)) {
    throw new Error(`Registry missing: ${CANONICAL}`);
  }
  _cache = JSON.parse(fs.readFileSync(CANONICAL, 'utf-8')) as FederationRegistry;
  _cacheTime = now;
  return _cache;
}

export function reload(): void {
  _cache = null;
}

// ── Index helpers ──

function providerMap(reg: FederationRegistry): Map<string, ProviderRecord> {
  const m = new Map<string, ProviderRecord>();
  for (const p of reg.providers) m.set(p.provider_id, p);
  return m;
}

function agentMap(reg: FederationRegistry): Map<string, AgentRecord> {
  const m = new Map<string, AgentRecord>();
  for (const a of reg.agents) m.set(a.agent_id, a);
  return m;
}

// ── Public API ──

export function resolve(agentId: string): ResolvedAgent {
  const reg = load();
  const agents = agentMap(reg);
  const providers = providerMap(reg);

  const a = agents.get(agentId);
  if (!a) throw new Error(`Agent '${agentId}' not found. Available: ${[...agents.keys()].join(', ')}`);

  const pid = a.primary_provider || 'unknown';
  const p = providers.get(pid);

  const fallbacks: string[] = (a.fallback_chain || [])
    .filter((f): f is FallbackEntry => typeof f === 'object' && 'model_key' in f)
    .map(f => f.model_key);

  return {
    agentId,
    agentName: a.agent_name || agentId,
    model: a.primary_model,
    provider: pid,
    providerName: p?.provider_name || pid,
    fallbacks,
    endpoint: p?.endpoint_url || '',
    apiKeyRef: p?.api_key_ref || '',
    status: a.status || p?.status || 'UNKNOWN',
    timeoutMs: a.timeout_ms || 30000,
    costDailyUsd: a.cost_budget_daily_usd || 0,
  };
}

export function resolveFallback(agentId: string, afterModel: string): string | null {
  const cfg = resolve(agentId);
  const chain = cfg.fallbacks;
  for (let i = 0; i < chain.length; i++) {
    if (chain[i].includes(afterModel) || afterModel.includes(chain[i])) {
      return i + 1 < chain.length ? chain[i + 1] : null;
    }
  }
  return chain.length > 0 ? chain[0] : null;
}

export function validate(): ValidationResult {
  const reg = load();
  const errors: string[] = [];
  const warnings: string[] = [];
  const providers = providerMap(reg);
  const agents = agentMap(reg);

  // Build known models set
  const knownModels = new Set<string>();
  for (const m of reg.models || []) {
    if (m.model_key) knownModels.add(m.model_key);
  }

  for (const [aid, a] of agents) {
    if (!a.primary_model) errors.push(`${aid}: missing primary_model`);
    if (!providers.has(a.primary_provider)) {
      errors.push(`${aid}: provider '${a.primary_provider}' not in registry`);
    }
    for (const fb of a.fallback_chain || []) {
      const mk = fb.model_key || '';
      if (mk && !knownModels.has(mk)) {
        const found = [...knownModels].some(km => mk.includes(km) || km.includes(mk));
        if (!found) warnings.push(`${aid}: fallback model '${mk}' not in registry models catalog`);
      }
    }
  }

  for (const [pid, p] of providers) {
    if (p.status === 'DEPRECATING' || p.status === 'RATE_LIMITED') {
      warnings.push(`${pid}: ${p.status} — agents using this may fail`);
    }
    if (p.cloud_act_exposed) {
      warnings.push(`${pid}: US jurisdiction — not for sovereign data`);
    }
  }

  return { valid: errors.length === 0, errors, warnings, providers: providers.size, agents: agents.size };
}

export function listAgents(): { agentId: string; name: string; model: string; provider: string; status: string }[] {
  const reg = load();
  return reg.agents
    .map(a => ({
      agentId: a.agent_id,
      name: a.agent_name || a.agent_id,
      model: a.primary_model,
      provider: a.primary_provider || 'unknown',
      status: a.status || '?',
    }))
    .sort((a, b) => a.agentId.localeCompare(b.agentId));
}

export function listProviders(): { providerId: string; name: string; status: string; balanceUsd: number | null; jurisdiction: string }[] {
  const reg = load();
  return reg.providers
    .map(p => ({
      providerId: p.provider_id,
      name: p.provider_name || p.provider_id,
      status: p.status || '?',
      balanceUsd: p.balance_usd ?? null,
      jurisdiction: p.jurisdiction || '?',
    }))
    .sort((a, b) => a.providerId.localeCompare(b.providerId));
}
