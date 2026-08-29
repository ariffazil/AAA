use tracing::{info, warn, error};
use crate::policy::PolicyConfig;
use crate::types::InterceptorVerdict;

pub struct Interceptor<'a> {
    config: &'a PolicyConfig,
}

impl<'a> Interceptor<'a> {
    pub fn new(config: &'a PolicyConfig) -> Self {
        Self { config }
    }

    pub fn evaluate_tool_call(&self, tool_name: &str, invoking_role: &str, _is_write: bool) -> InterceptorVerdict {
        let meta = match self.config.tools.get(tool_name) {
            Some(m) => m,
            None => {
                if self.config.global.default_unknown_tool == "UNCHECKED_BLOCK" {
                    warn!(tool = tool_name, "UNCHECKED_BLOCK");
                    return InterceptorVerdict::Blocked {
                        reason: format!("Tool '{}' not registered. UNCHECKED_BLOCK.", tool_name),
                    };
                }
                error!(tool = tool_name, "MISCONFIGURED default");
                return InterceptorVerdict::Blocked {
                    reason: format!("Tool '{}' unregistered + non-blocking default. Governance error.", tool_name),
                };
            }
        };
        if !meta.is_authorized(invoking_role) {
            warn!(tool = tool_name, role = invoking_role, "UNAUTHORIZED");
            return InterceptorVerdict::Blocked {
                reason: format!("Role '{}' not authorized for '{}'.", invoking_role, tool_name),
            };
        }
        if meta.requires_sovereign_hold() {
            info!(tool = tool_name, impact = meta.arifos_impact_radius, "REQUIRES_HOLD");
            return InterceptorVerdict::RequiresHold {
                reason: format!("Tool '{}' requires 888 Sovereign Hold (impact={}).", tool_name, meta.arifos_impact_radius),
            };
        }
        info!(tool = tool_name, role = invoking_role, "APPROVED");
        InterceptorVerdict::Approved
    }

    pub fn policy_version(&self) -> &str {
        &self.config.meta.version
    }
}
