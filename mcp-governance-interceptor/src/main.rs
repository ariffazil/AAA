use std::path::PathBuf;
use anyhow::Result;
use tracing::{info, error};

fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_target(false)
        .with_thread_ids(true)
        .init();

    info!("mcp-governance-interceptor v{}", env!("CARGO_PKG_VERSION"));

    let policy_path = std::env::var("MCP_POLICY_PATH")
        .unwrap_or_else(|_| {
            let home = dirs::home_dir().unwrap_or_else(|| PathBuf::from("/root"));
            home.join("AAA/mcp-governance-interceptor/config/mcp-governance-policy.toml")
                .to_string_lossy()
                .to_string()
        });

    info!(path = %policy_path, "Loading policy");
    let config = mcp_governance_interceptor::policy::load_policy(std::path::Path::new(&policy_path))?;

    let validation = mcp_governance_interceptor::policy::validate_policy(std::path::Path::new(&policy_path));
    match validation {
        mcp_governance_interceptor::types::PolicyValidation::Valid => {
            info!("Policy validation: VALID");
        }
        other => {
            error!(?other, "Policy validation FAILED");
            anyhow::bail!("Policy validation failed");
        }
    }

    let interceptor = mcp_governance_interceptor::interceptor::Interceptor::new(&config);

    // Demo: evaluate a few tool calls
    let test_cases = vec![
        ("fed_route", "333-AGI", false),
        ("capital_ledger", "333-AGI", false),
        ("unknown_tool", "333-AGI", false),
    ];

    for (tool, role, write) in test_cases {
        let verdict = interceptor.evaluate_tool_call(tool, role, write);
        info!(tool = tool, role = role, verdict = ?verdict, "Test evaluation");
    }

    info!("Interceptor ready. Awaiting UDS server implementation in Phase 2.");
    Ok(())
}
