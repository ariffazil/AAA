import agentCard from './agent-card.json';
import discoveryRoutingPolicy from './discovery-routing-policy.json';

export interface AgentIdentity {
  name: string;
  version: string;
  description: string;
  creator: string;
  runtime: string;
}

const BOOTSTRAP_IDENTITY: AgentIdentity = {
  name: agentCard.name,
  version: agentCard.version,
  description: agentCard.description,
  creator: agentCard.provider.organization,
  runtime: agentCard.provider.runtime
};

const BOOTSTRAP_ENDPOINTS = {
  a2a: agentCard.url,
  discovery_contract: '/.well-known/a2a-discovery.json',
  agent_card: '/.well-known/agent-card.json',
  agent_legacy: '/.well-known/agent.json',
  routing_policy: '/.well-known/a2a-routing-policy.json',
  federation_manifest: '/.well-known/arifos-federation.json'
};

export const CONSTITUTION_DEFAULTS = {
  version: 'v888.1.0-CONSTITUTION',
  floors: ['L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'L07', 'L08', 'L09', 'L10', 'L11', 'L12', 'L13'],
  governance_model: 'arifOS Constitutional AI',
  authority: 'Muhammad Arif bin Fazil (888 Judge)'
};

export function getBootstrapConfig(agentId: string) {
  return {
    agent_id: agentId,
    identity: BOOTSTRAP_IDENTITY,
    constitution: CONSTITUTION_DEFAULTS,
    endpoints: BOOTSTRAP_ENDPOINTS,
    capabilities: agentCard.capabilities,
    timestamp: new Date().toISOString()
  };
}

export function getAgentCard() {
  return agentCard;
}

export function getDiscoveryRoutingPolicy() {
  return discoveryRoutingPolicy;
}
