use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "snake_case")]
pub enum ToolCategory {
    ReadOnly,
    Compute,
    Propose,
    StateMutation,
    HighImpactMutation,
    CriticalMutation,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolMetadata {
    pub arifos_is_reversible: bool,
    pub arifos_impact_radius: u8,
    pub arifos_requires_888_hold: bool,
    pub arifos_category: ToolCategory,
    #[serde(default)]
    pub arifos_allowed_roles: Vec<String>,
}

impl ToolMetadata {
    pub fn requires_sovereign_hold(&self) -> bool {
        self.arifos_requires_888_hold || self.arifos_impact_radius >= 3
    }

    pub fn is_authorized(&self, role: &str) -> bool {
        if self.arifos_allowed_roles.is_empty() {
            return role == "888-APEX";
        }
        self.arifos_allowed_roles.contains(&role.to_string())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum InterceptorVerdict {
    Approved,
    Blocked { reason: String },
    RequiresHold { reason: String },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AuditEvent {
    pub timestamp: String,
    pub event_type: String,
    pub tool_name: Option<String>,
    pub verdict: InterceptorVerdict,
    pub role: Option<String>,
    pub policy_version: String,
    pub chain_hash: String,
    pub previous_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyReloadEvent {
    pub timestamp: String,
    pub event_type: String,
    pub policy_version: String,
    pub policy_hash: String,
    pub signature_algorithm: String,
    pub signer: String,
    pub trigger: String,
    pub previous_hash: String,
    pub delta_tools_added: u32,
    pub delta_tools_modified: u32,
    pub delta_tools_blocked: u32,
}

#[derive(Debug, Clone)]
pub enum PolicyValidation {
    Valid,
    InvalidSignature { reason: String },
    StalePolicy { reason: String },
    Corrupted { reason: String },
}
