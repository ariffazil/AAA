import agentCard from './agent-card.json';

export interface AgentIdentity {
  name: string;
  version: string;
  description: string;
  creator: string;
  runtime: string;
}

export const CONSTITUTION_DEFAULTS = {
  version: 'v888.1.0-CONSTITUTION',
  floors: ['L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'L07', 'L08', 'L09', 'L10', 'L11', 'L12', 'L13'],
  governance_model: 'arifOS Constitutional AI',
  authority: 'Muhammad Arif bin Fazil (888 Judge)'
};

export function getBootstrapConfig(agentId: string) {
  return {
    agent_id: agentId,
    identity: agentCard.agent,
    constitution: CONSTITUTION_DEFAULTS,
    endpoints: agentCard.endpoints,
    capabilities: agentCard.capabilities,
    timestamp: new Date().toISOString()
  };
}

export function getAgentCard() {
  return agentCard;
}
