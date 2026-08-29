use std::collections::HashMap;
use std::fs;
use std::path::Path;

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use tracing::info;

use crate::types::{ToolMetadata, PolicyValidation};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyConfig {
    pub meta: PolicyMeta,
    pub global: GlobalConfig,
    pub tools: HashMap<String, ToolMetadata>,
    pub intent_router: IntentRouterConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PolicyMeta {
    pub version: String,
    pub created: String,
    pub signature_algorithm: String,
    pub signer: String,
    pub chain_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GlobalConfig {
    pub max_tools_per_turn: usize,
    pub intent_router_enabled: bool,
    pub interceptor_enabled: bool,
    pub audit_chain_path: String,
    pub default_unknown_tool: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IntentRouterConfig {
    pub domains: HashMap<String, DomainConfig>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DomainConfig {
    pub keywords: Vec<String>,
    pub tools: Vec<String>,
    pub priority: u8,
}

pub fn load_policy(path: &Path) -> Result<PolicyConfig> {
    let content = fs::read_to_string(path)
        .with_context(|| format!("Failed to read policy file: {}", path.display()))?;
    let config: PolicyConfig = toml::from_str(&content)
        .with_context(|| format!("Failed to parse policy TOML: {}", path.display()))?;
    info!(
        version = %config.meta.version,
        tool_count = config.tools.len(),
        "Policy loaded"
    );
    Ok(config)
}

pub fn validate_policy(path: &Path) -> PolicyValidation {
    let content = match fs::read_to_string(path) {
        Ok(c) => c,
        Err(e) => return PolicyValidation::Corrupted { reason: e.to_string() },
    };
    match toml::from_str::<PolicyConfig>(&content) {
        Ok(config) => {
            if config.meta.version.is_empty() || config.meta.signer.is_empty() {
                return PolicyValidation::Corrupted { reason: "Empty version or signer".to_string() };
            }
            PolicyValidation::Valid
        }
        Err(e) => PolicyValidation::Corrupted { reason: e.to_string() },
    }
}

pub fn resolve_toolset(config: &PolicyConfig, intent_keywords: &[String]) -> Vec<String> {
    let mut matched: Vec<(String, u8)> = Vec::new();
    for (name, domain) in &config.intent_router.domains {
        let score: u32 = domain.keywords.iter()
            .filter(|kw| intent_keywords.iter().any(|ik| kw.to_lowercase().contains(&ik.to_lowercase())))
            .count() as u32;
        if score > 0 {
            for tool in &domain.tools {
                if !matched.iter().any(|(t, _)| t == tool) {
                    matched.push((tool.clone(), domain.priority));
                }
            }
        }
    }
    matched.sort_by(|a, b| a.1.cmp(&b.1));
    let max = config.global.max_tools_per_turn;
    matched.into_iter().take(max).map(|(t, _)| t).collect()
}
